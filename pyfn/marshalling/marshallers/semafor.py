"""Marshaller to SEMAFOR/SEMAFOR format.

SEMAFOR file format:
0   1       2               3       4       5                   6
1   0.0     #(Frame + FEs)  Frame   Lexunit target_token_num    target_string

7           8    9                   10     11                  ...
sent_num    FE1  FE1_start:end_token FE2    FE2_start:end_token ...

multi-token targets are written 'start_end' with start = start_token_num and
end = end_token_num (hence discontinuous targets are not fully supported)
multi-token FEs are written 'start:end'
"""

import logging

import pyfn.utils.files as files_utils
import pyfn.utils.filter as filt_utils
import pyfn.utils.marshalling as marsh_utils

from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['marshall_annosets_dict']

logger = logging.getLogger(__name__)


def _get_token_num(index, text):
    token_num = -1
    prev_char_is_whitespace = True
    for char_index, char in enumerate(text):
        if char.isspace():
            prev_char_is_whitespace = True
            continue
        if prev_char_is_whitespace:
            token_num += 1
        prev_char_is_whitespace = False
        if char_index == index:
            return token_num
    raise Exception('Could not determine token number for char index '
                    '{} in sentence \'{}\''
                    .format(index, text))


def _get_fe_chunks(annoset):
    # Annosets are filtered so no start/end index points at a whitespace
    fe_chunks = ''
    if 'FE' not in annoset.labelstore.labels_by_layer_name:
        return fe_chunks
    for label in annoset.labelstore.labels_by_layer_name['FE']:
        if label.start != -1 and label.end != -1:
            start_token = _get_token_num(label.start, annoset.sentence.text)
            end_token = _get_token_num(label.end, annoset.sentence.text)
            if start_token == end_token:
                fe_chunks = '{}\t{}\t{}'.format(
                    fe_chunks, label.name, start_token).strip()
            else:
                fe_chunks = '{}\t{}\t{}:{}'.format(
                    fe_chunks, label.name, start_token, end_token).strip()
    return fe_chunks


def _get_frame_fe_num(annoset):
    frame_fe_num = 1  # at least the frame
    if 'FE' not in annoset.labelstore.labels_by_layer_name:
        return frame_fe_num
    for label in annoset.labelstore.labels_by_layer_name['FE']:
        if label.start != -1 and label.end != -1:
            frame_fe_num += 1
    return frame_fe_num


def _get_max_index(indexes):
    max_index = -1
    for (start, end) in indexes:
        if start == -1 or end == -1:
            raise InvalidParameterError('Target start/end indexes are '
                                        'undefined')
        if max_index == -1:
            max_index = max(start, end)
        else:
            max_index = max(max_index, start, end)
    return max_index


def _get_min_index(indexes):
    min_index = -1
    for (start, end) in indexes:
        if start == -1 or end == -1:
            raise InvalidParameterError('Target start/end indexes are '
                                        'undefined')
        if min_index == -1:
            min_index = min(start, end)
        else:
            min_index = min(min_index, start, end)
    return min_index


def _get_target_token_num(target, text):
    min_index = _get_min_index(target.indexes)
    max_index = _get_max_index(target.indexes)
    min_token_num = _get_token_num(min_index, text)
    max_token_num = _get_token_num(max_index, text)
    if min_token_num == max_token_num:
        return min_token_num
    return '{}_{}'.format(min_token_num, max_token_num)


def _get_semafor_line(annoset, sent_dict, train_mode):
    if not train_mode:
        return '1\t0.0\t1\t{}\t{}\t{}\t{}\t{}'.format(
            annoset.target.lexunit.frame.name,
            annoset.target.lexunit.name,
            _get_target_token_num(annoset.target, annoset.sentence.text),
            annoset.target.string,
            marsh_utils.get_sent_num(annoset.sentence.text, sent_dict))
    return '1\t0.0\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
        _get_frame_fe_num(annoset),
        annoset.target.lexunit.frame.name,
        annoset.target.lexunit.name,
        _get_target_token_num(annoset.target, annoset.sentence.text),
        annoset.target.string,
        marsh_utils.get_sent_num(annoset.sentence.text, sent_dict),
        _get_fe_chunks(annoset)).strip()


def _marshall_semafor(annosets, filtering_options, sent_dict,
                      semafor_filepath, excluded_frames,
                      excluded_sentences, excluded_annosets, train_mode):
    files_utils.create_parent_dir_if_not_exists(semafor_filepath)
    with open(semafor_filepath, 'w', encoding='utf-8') as semafor_stream:
        for annoset in filt_utils.filter_and_sort_annosets(annosets,
                                                           filtering_options,
                                                           excluded_frames,
                                                           excluded_sentences,
                                                           excluded_annosets):
            semafor_line = _get_semafor_line(annoset, sent_dict, train_mode)
            print(semafor_line, file=semafor_stream)


def marshall_annosets_dict(annosets_dict, target_dirpath, filtering_options,
                           output_sentences, excluded_frames,
                           excluded_sentences, excluded_annosets):
    """Convert a dict of {splits:pyfn.AnnotationSet} to SEMAFOR splits files.

    The train spits will be converted to a .frame.elements file containing
    both frame and frame element labels depending on filtering options.
    The dev/test splits will be converted to a .frames file containing
    frame labels only.

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
        logger.info('Marshalling {} splits to semafor format'
                    .format(splits_name))
        semafor_filepath = files_utils.get_semafor_filepath(target_dirpath,
                                                            splits_name)
        sent_filepath = files_utils.get_sent_filepath(target_dirpath,
                                                      splits_name)
        sent_dict = {}
        if splits_name not in ['train', 'dev', 'test']:
            raise InvalidParameterError('Unsupported splits_name: {}'.format(
                splits_name))
        if splits_name in ('dev', 'test'):
            # No special filtering on dev/test
            _marshall_semafor(annosets, [], sent_dict,
                              semafor_filepath, excluded_frames,
                              excluded_sentences, excluded_annosets,
                              train_mode=False)
        elif splits_name == 'train':
            _marshall_semafor(annosets, filtering_options, sent_dict,
                              semafor_filepath, excluded_frames,
                              excluded_sentences, excluded_annosets,
                              train_mode=True)
        # print out sentences file
        if output_sentences:
            marsh_utils.marshall_sent_dict(sent_dict, sent_filepath)
