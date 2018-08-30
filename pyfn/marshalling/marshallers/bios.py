"""Marshaller to BIOS tagging scheme.

BEGINNING = B
INSIDE = I
OUTSIDE = O
SINGULAR = S

BIOS file format:
0   1       2       3               4   5           6       7       8
ID  FORM    LEMMA   PLEMMA(NLTK)    POS PPOS(NLTK)  FEAT    PFEAT   HEAD

9       10      11      12          13      14      15
PHEAD   DEPREL  PDEPREL FILLPRED    PRED    APREDS  FE_CORETYPE
"""

import itertools
import logging

import pyfn.utils.files as files_utils
import pyfn.utils.filter as filt_utils
import pyfn.utils.marshalling as marsh_utils

from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['marshall_annosets_dict']

logger = logging.getLogger(__name__)


def _get_fe_label(start, end, fe_labels):
    for label in fe_labels:
        # FIXME: careful, this is not compatible with discontinuous labels
        if label.start >= start and label.end <= end:
            return 'S-{}'.format(label.name)
        if label.start == start:
            return 'B-{}'.format(label.name)
        if label.start < start <= label.end:
            return 'I-{}'.format(label.name)
    return 'O'


def _get_lexunit(start, end, target):
    if (start, end) in target.indexes:
        return target.lexunit
    for istart, iend in target.indexes:
        if not (iend < start or istart > end):
            return target.lexunit
    return '_'


def _get_frame_name(lexunit):
    return '_' if lexunit == '_' else lexunit.frame.name


def _get_lexunit_name(lexunit):
    return '_' if lexunit == '_' else lexunit.name


def _get_token_lemma(token, pos, lemmatizer):
    if pos.startswith('V'):
        return lemmatizer.lemmatize(token, pos='v')
    return lemmatizer.lemmatize(token)


def _get_token_index_3uples(text):
    token_index_3uples = []
    tokens = text.split()
    start_index = 0
    for token in tokens:
        while token[0] != text[start_index]:
            start_index += 1
        token_index_3uples.append((token, start_index,
                                   start_index+len(token)-1))
        start_index += len(token)
    return token_index_3uples


def _get_valence_units_by_indexes(vus_by_indexes_dict, start, end):
    valence_units = []
    for (vu_start, vu_end), vus in vus_by_indexes_dict.items():
        if not (vu_end < start or vu_start > end):
            valence_units.extend(vus)
    return valence_units


def _get_fe_coretype(fe_label, vus):
    if fe_label == 'O':
        raise InvalidParameterError('Unspecified FE label: {}'.format(fe_label))
    if not vus:
        raise InvalidParameterError('Input ValenceUnit list is empty')
    fe_name = fe_label[2:]
    for vu in vus:
        if vu.fe.name == fe_name:
            return vu.fe.coretype
    raise Exception('Could not output FE coreType: no matching FE name \'{}\' '
                    'found in ValenceUnit list {}'.format(fe_name, vus))


def _get_bios_lines(annoset, sent_dict, with_fe_anno=False):
    bios_lines = []
    token_index_3uples = _get_token_index_3uples(annoset.sentence.text)
    sent_num = marsh_utils.get_sent_num(annoset.sentence.text, sent_dict)
    token_num = 1
    for token_3uple in token_index_3uples:
        if not with_fe_anno or 'FE' not in annoset.labelstore.labels_by_layer_name:
            fe_label = 'O'
            fe_coretype = '_'
        else:
            fe_label = _get_fe_label(
                token_3uple[1], token_3uple[2],
                annoset.labelstore.labels_by_layer_name['FE'])
            if fe_label == 'O':
                fe_coretype = '_'
            else:
                vus = _get_valence_units_by_indexes(annoset.vustore.valence_units_by_indexes,
                                                    token_3uple[1],
                                                    token_3uple[2])
                fe_coretype = _get_fe_coretype(fe_label, vus)
        bios_line = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
            token_num,
            token_3uple[0],
            '_',
            '_',
            '_',
            '_',
            sent_num,
            '_', '_', '_', '_', '_',
            _get_lexunit_name(_get_lexunit(token_3uple[1], token_3uple[2],
                                           annoset.target)),
            _get_frame_name(_get_lexunit(token_3uple[1], token_3uple[2],
                                         annoset.target)),
            fe_label,
            fe_coretype)
        bios_lines.append(bios_line)
        token_num += 1
    return bios_lines


def _marshall_bios(annosets, filtering_options, sent_dict, bios_filepath,
                   excluded_frames, excluded_sentences, excluded_annosets,
                   with_fe_anno):
    files_utils.create_parent_dir_if_not_exists(bios_filepath)
    with open(bios_filepath, 'w', encoding='utf-8') as bios_stream:
        for annoset in filt_utils.filter_and_sort_annosets(annosets,
                                                           filtering_options,
                                                           excluded_frames,
                                                           excluded_sentences,
                                                           excluded_annosets):
            bios_lines = _get_bios_lines(annoset, sent_dict, with_fe_anno)
            print('\n'.join(bios_lines), file=bios_stream)
            print('', file=bios_stream)  # at the end of a sentence


def marshall_annosets_dict(annosets_dict, target_dirpath, filtering_options,
                           output_sentences, excluded_frames,
                           excluded_sentences, excluded_annosets):
    """Convert a dict of {splits:pyfn.AnnotationSet} to BIOS splits files.

    Args
    ----
        annosets_dict: a splits to annosets dictionary (as generated by
        the framenet unmarshaller).
        target_dirpath: the absolute path to the target directory where to
        save the output file(s)
        filtering_options: a list of options to pass to the pyfn.utils.filter.
        ('overlap_fes', 'disc_fes', 'disc_targets', 'no_fes', 'non_breaking_spaces')
        output_sentences: True or False. Whether or not to also output a .sentences file
        listing all sentences (string), one per line.
        excluded_frames: a list of frame #id to exclude from the output
        excluded_sentences: a list of sentence #id to exclude from the output
        excluded_annosets: a list of annotationset #id to exclude from the output
    """
    for splits_name, annosets in annosets_dict.items():
        bios_filepath = files_utils.get_bios_filepath(target_dirpath,
                                                      splits_name)
        bios_semeval_filepath = files_utils.get_bios_semeval_filepath(
            target_dirpath, splits_name)
        sent_filepath = files_utils.get_sent_filepath(target_dirpath,
                                                      splits_name)
        sent_dict = {}
        if splits_name not in ['train', 'dev', 'test']:
            raise InvalidParameterError('Invalid splits_name: {}'.format(
                splits_name))
        if splits_name in ('dev', 'test'):
            annosets, _annosets = itertools.tee(annosets, 2)
            logger.info('Marshalling splits:pyfn.AnnotationSet dict to '
                        '.bios.semeval for {} splits with [] filtering '
                        'options...'.format(splits_name))
            _marshall_bios(annosets, [], sent_dict,  # No special filtering on dev/test
                           bios_semeval_filepath, excluded_frames,
                           excluded_sentences,
                           excluded_annosets, with_fe_anno=False)
            logger.info('Marshalling splits:pyfn.AnnotationSet dict to '
                        '.bios for {} splits with {} filtering '
                        'options...'.format(splits_name, filtering_options))
            _marshall_bios(_annosets, filtering_options, sent_dict,
                           bios_filepath, excluded_frames, excluded_annosets,
                           excluded_sentences, with_fe_anno=True)
        elif splits_name == 'train':
            logger.info('Marshalling splits:pyfn.AnnotationSet dict to '
                        '.bios for {} splits with {} filtering '
                        'options...'.format(splits_name, filtering_options))
            _marshall_bios(annosets, filtering_options, sent_dict,
                           bios_filepath, excluded_frames,
                           excluded_sentences, excluded_annosets,
                           with_fe_anno=True)
        # print out sentences file
        if output_sentences:
            marsh_utils.marshall_sent_dict(sent_dict, sent_filepath)
