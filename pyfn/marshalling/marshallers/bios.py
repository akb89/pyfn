"""Marshaller to BIOS tagging scheme.

BEGINNING = B
INSIDE = I
OUTSIDE = O
SINGULAR = S

BIOS file format:
0   1       2       3               4   5           6       7       8       9       10      11      12          13      14
ID  FORM    LEMMA   PLEMMA(NLTK)    POS PPOS(NLTK)  FEAT    PFEAT   HEAD    PHEAD   DEPREL  PDEPREL FILLPRED    PRED    APREDS
"""

import os
import logging

import pyfn.utils.filter as f_utils

__all__ = ['marshall_annosets_dict']

logger = logging.getLogger(__name__)


def _get_sent_num(text, sent_dict):
    sent_hash = f_utils.get_text_hash(text)
    return 0


def _get_token_index_dict(text):
    """Return a dict: {token: (start, end)} of token to start/end indexe tuples."""
    token_index_dict = {}
    tokens = text.split()
    start_index = 0
    for token in tokens:
        while token[0] != text[start_index]:
            start_index += 1
        token_index_dict[token] = (start_index, start_index+len(token)-1)
        start_index += len(token)
    return token_index_dict


def _get_bios_lines(annoset, sent_dict):
    bios_lines = []
    token_index_dict = _get_token_index_dict(annoset.sentence.text)
    sent_num = _get_sent_num(annoset.sentence.text, sent_dict)
    for key, value in token_index_dict.items():
        print(key, value)
    # for labels in annoset.labelstore.labels_by_indexes.values():
    #     for label in labels:
    #         print(label.name, label.layer.name)
    return bios_lines


def _is_invalid_annoset(annoset):
    if 'FE' not in annoset.labelstore.labels_by_layer_name:
        return True
    labels_indexes = []
    for label in annoset.labelstore.labels_by_layer_name['FE']:
        if label.start == -1 and label.end == -1:
            # CNI, DNI, INI cases
            continue
        for index in labels_indexes:
            if (label.start >= index[0] and label.start <= index[1]) or \
             (label.end >= index[0] and label.end <= index[1]):
                return True
        labels_indexes.append((label.start, label.end))
    return False


def _get_output_filepath(target_dirpath, splits_name):
    return os.path.join(target_dirpath, '{}.bios'.format(splits_name))


def marshall_annosets_dict(annosets_dict, target_dirpath):
    """Convert a dict of splits-pyfn.AnnotationSet to BIOS splits files."""
    for splits_name, annosets in annosets_dict.items():
        output_filepath = _get_output_filepath(target_dirpath, splits_name)
        with open(output_filepath, 'w', encoding='utf-8') as output_stream:
            sent_dict = {}
            for annoset in annosets:
                if _is_invalid_annoset(annoset):
                    # TODO: add stats
                    logger.debug(
                        'Invalid AnnotationSet #{}. No FE or multiple FE '
                        'labels specified on the same item'.format(
                            annoset._id))
                else:
                    bios_lines = _get_bios_lines(annoset, sent_dict)
                    for bios_line in bios_lines:
                        print(bios_line, file=output_stream)
                    print('\n', file=output_stream)  # at the end of a sentence
