"""Marshaller to BIOS tagging scheme.

BEGINNING = B
INSIDE = I
OUTSIDE = O
SINGULAR = S

BIOS file format:
0   1       2       3               4   5           6       7       8
ID  FORM    LEMMA   PLEMMA(NLTK)    POS PPOS(NLTK)  FEAT    PFEAT   HEAD

9       10      11      12          13      14
PHEAD   DEPREL  PDEPREL FILLPRED    PRED    APREDS
"""

import os
import logging
import nltk

from nltk.stem import WordNetLemmatizer

import pyfn.utils.filter as f_utils
import pyfn.utils.sort as sort_utils
from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['marshall_annosets_dict']

logger = logging.getLogger(__name__)


def _get_fe_label(start, end, fe_labels):
    for label in fe_labels:
        if start == label.start and end == label.end:
            return 'S-{}'.format(label.name)
        if start == label.start:
            return 'B-{}'.format(label.name)
        if start > label.start and end <= label.end:
            return 'I-{}'.format(label.name)
    return 'O'


def _get_frame_label(start, end, target):
    if (start, end) in target.indexes:
        return target.lexunit.frame.name
    return '_'


def _get_lexunit_label(start, end, target):
    if (start, end) in target.indexes:
        return target.lexunit.name
    return '_'


def _get_token_lemma(token, pos, lemmatizer):
    if pos.startswith('V'):
        return lemmatizer.lemmatize(token, pos='v')
    return lemmatizer.lemmatize(token)


def _get_tokens_ppos(text):
    return [item[1] for item in nltk.pos_tag(text.split())]


def _get_tokens_pos(token_index_3uples, pos_labels_by_indexes):
    tokens_pos = []
    for _, start, end in token_index_3uples:
        if (start, end) in pos_labels_by_indexes:
            for label in pos_labels_by_indexes[(start, end)]:
                if label.layer.name == 'PENN' or label.layer.name == 'BNC':
                    tokens_pos.append(label.name.upper())
                else:
                    raise InvalidParameterError('')
        else:
            tokens_pos.append('_')
    return tokens_pos


def _get_sent_num(sentence, sent_dict):
    if sentence._id not in sent_dict:
        sent_dict[sentence._id] = (len(sent_dict), sentence.text)
    return sent_dict[sentence._id][0]


def _get_token_index_3uples(text):
    """Return a dict: {token: (start, end)} of token to start/end indexe tuples."""
    token_index_3uples = []
    tokens = text.split()
    start_index = 0
    for token in tokens:
        while token[0] != text[start_index]:
            start_index += 1
        token_index_3uples.append((token, start_index, start_index+len(token)-1))
        start_index += len(token)
    return token_index_3uples


def _get_bios_lines(annoset, sent_dict, lemmatizer, train_mode=False):
    bios_lines = []
    token_index_3uples = _get_token_index_3uples(annoset.sentence.text)
    sent_num = _get_sent_num(annoset.sentence, sent_dict)
    token_num = 0
    pos_tags = _get_tokens_pos(
        token_index_3uples, annoset.sentence.pnw_labelstore.labels_by_indexes)
    ppos_tags = _get_tokens_ppos(annoset.sentence.text)
    # Checking some stuff:
    if len(token_index_3uples) != len(pos_tags) or len(pos_tags) != len(ppos_tags):
        raise InvalidParameterError('')
    for token_3uple, pos, ppos in zip(token_index_3uples, pos_tags, ppos_tags):
        if not train_mode or 'FE' not in annoset.labelstore.labels_by_layer_name:
            fe_label = '_'
        else:
            fe_label = _get_fe_label(
                token_3uple[1], token_3uple[2],
                annoset.labelstore.labels_by_layer_name['FE'])
        bios_line = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
            token_num,
            token_3uple[0],
            '_',
            _get_token_lemma(token_3uple[0], ppos, lemmatizer),
            pos,
            ppos,
            sent_num,
            '_', '_', '_', '_', '_',
            _get_lexunit_label(token_3uple[1], token_3uple[2], annoset.target),
            _get_frame_label(token_3uple[1], token_3uple[2], annoset.target),
            fe_label)
        bios_lines.append(bios_line)
        token_num += 1
    return bios_lines


def _get_bios_filepath(target_dirpath, splits_name):
    return os.path.join(target_dirpath, '{}.bios'.format(splits_name))


def _get_sent_filepath(target_dirpath, splits_name):
    return os.path.join(target_dirpath, '{}.sentences'.format(splits_name))


def _marshall_sent_dict(sent_dict, sent_stream):
    for num_text in sorted(sent_dict.values(), key=lambda tup: tup[0]):
        print(num_text[1], file=sent_stream)


def _marshall_bios(annosets, filtering_options, sent_dict, lemmatizer,
                   bios_stream, train_mode=False):
    if train_mode:
        f_annosets = sort_utils.sort_annosets(
            f_utils.filter_annosets(annosets, filtering_options))
    else:
        f_annosets = sort_utils.sort_annosets(
            f_utils.filter_annosets(annosets, []))
    for annoset in f_annosets:
        bios_lines = _get_bios_lines(annoset, sent_dict, lemmatizer,
                                     train_mode)
        print('\n'.join(bios_lines), file=bios_stream)
        print('', file=bios_stream)  # at the end of a sentence


def marshall_annosets_dict(annosets_dict, target_dirpath, filtering_options):
    """Convert a dict of splits-pyfn.AnnotationSet to BIOS splits files."""
    lemmatizer = WordNetLemmatizer()
    for splits_name, annosets in annosets_dict.items():
        bios_filepath = _get_bios_filepath(target_dirpath, splits_name)
        sent_filepath = _get_sent_filepath(target_dirpath, splits_name)
        with open(bios_filepath, 'w', encoding='utf-8') as bios_stream, \
         open(sent_filepath, 'w', encoding='utf-8') as sent_stream:
            sent_dict = {}
            if splits_name == 'dev' or splits_name == 'test':
                _marshall_bios(annosets, filtering_options, sent_dict,
                               lemmatizer, bios_stream, train_mode=False)
            elif splits_name == 'train':
                _marshall_bios(annosets, filtering_options, sent_dict,
                               lemmatizer, bios_stream, train_mode=True)
            else:
                raise InvalidParameterError('Invalid splits_name: {}'.format(
                    splits_name))
            # print out sentences file
            _marshall_sent_dict(sent_dict, sent_stream)
