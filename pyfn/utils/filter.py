"""Filtering utils."""

import re
import logging

__all__ = ['left_difference', 'filter_and_sort_annosets']

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


def _has_overlapping_fes(annoset):
    if not annoset.labelstore.labels_by_layer_name['FE']:
        return False
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


def _has_invalid_labels(annoset):
    for label in annoset.labelstore.labels:
        if label.start == -1 and label.end != -1 or label.start != -1 and label.end == -1:
            return True
    return False


def _is_valid_annoset(annoset, filtering_options):
    # No matter what, remove annosets containing invalid labels, i.e. labels
    # with combined specified and unspecified start/end indexes
    if _has_invalid_labels(annoset):
        return False
    # Remove annosets with overlapping frame elements (e.g. for BIOS train)
    if 'overlap_fes' in filtering_options:
        if _has_overlapping_fes(annoset):
            return False
    # Remove annosets with discontinuous frame elements (for rofames?)
    if 'disct_fes' in filtering_options:
        pass
    # Filter annosets with no frame element layers
    if 'no_fes' in filtering_options:
        pass  # TODO: don't check only layers, check also labels
    return True


def _filter_annosets(annosets, filtering_options):
    """Filter annosets."""
    for annoset in annosets:
        if _is_valid_annoset(annoset, filtering_options):
            yield annoset


def _sort_annosets(annosets):
    """Sort a list of pyfn.AnnotationSet objects.

    Sort by annoset.sentence._id first and then by annoset._id
    """
    return sorted(annosets, key=lambda annoset: (annoset.sentence._id,
                                                 annoset._id))


def filter_and_sort_annosets(annosets, filtering_options):
    return _sort_annosets(_filter_annosets(annosets, filtering_options))
