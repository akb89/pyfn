"""Filtering utils."""

import re
import logging

__all__ = ['left_difference', 'filter_annosets']

logger = logging.getLogger(__name__)


def get_text_hash(text):
    return re.sub(r'\s+', '', text.strip())


def _get_sent_hash_set(annosets):
    return {get_text_hash(annoset.sentence.text) for annoset in
            annosets}


def left_difference(source_annosets, target_annosets):
    """Return difference between source and target.

    Remove annosets from source found in target.

    Remove all annosets from source which contain a sentence attribute
    which text hash is in the set of the sentences hash
    of the target annosets
    """
    for annoset in source_annosets:
        if get_text_hash(annoset.sentence.text) \
         not in _get_sent_hash_set(target_annosets):
            yield annoset
        else:
            print('Found hash: {}'.format(get_text_hash(
                annoset.sentence.text)))


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


def filter_annosets(annosets):
    """Filter annosets."""
    for annoset in annosets:
        if _is_invalid_annoset(annoset):
            # TODO: add stats
            logger.debug(
                'Invalid AnnotationSet #{}. No FE or multiple FE '
                'labels specified on the same item'.format(
                    annoset._id))
        else:
            yield annoset
