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
    target_sent_hash_set = _get_sent_hash_set(target_annosets)
    for annoset in source_annosets:
        if get_text_hash(annoset.sentence.text) \
         not in target_sent_hash_set:
            yield annoset
        else:  # TODO: check that we found at least one
            logger.debug('Found hash: {}'.format(get_text_hash(
                annoset.sentence.text)))


def _has_overlapping_fes(annoset):
    if not annoset.labelstore.labels_by_layer_name['FE']:
        return False
    labels_indexes = []
    for label in annoset.labelstore.labels_by_layer_name['FE']:
        if label.start == -1 and label.end == -1:
            continue  # CNI, DNI, INI cases
        for start, end in labels_indexes:
            if label.start >= start and label.start <= end:
                return True
            if label.end >= start and label.end <= end:
                return True
            if label.start <= start and label.end >= end:
                return True
        labels_indexes.append((label.start, label.end))
    return False


def _has_invalid_labels(annoset):
    """Checking for both FE and Target labels."""
    for label in annoset.labelstore.labels:
        # if the label has an unspecified start/end index
        if label.start == -1 and label.end != -1 or label.start != -1 and label.end == -1:
            return True
        # if the label index points at a whitespace
        if (label.start != -1 and annoset.sentence.text[label.start].isspace()) \
         or (label.end != -1 and annoset.sentence.text[label.end].isspace()):
            logger.debug('Found label index pointing at whitespace '
                         'for annoset #{}'.format(annoset._id))
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
    # Remove annosets with discontinuous frame elements
    if 'disc_fes' in filtering_options:
        if _has_discontinuous_fes(annoset):
            return False
    # Remove annosets with discontinuous targets
    if 'disc_targets' in filtering_options:
        if _has_discontinuous_targets(annoset):
            return False
    # Filter annosets with no frame element layers
    if 'no_fes' in filtering_options:
        pass  # TODO: don't check only layers, check also labels
        #  the semeval evaluation script will skip sentences with no gold FEs
    return True


def _get_target_index_hash(target):
    return '#'.join(['{}#{}'.format(start, end) for (start, end)
                     in target.indexes])


def _get_annoset_target_hash(annoset):
    return '{}#{}#{}'.format(_get_target_index_hash(annoset.target),
                             annoset.target.lexunit.name,
                             annoset.target.lexunit.frame.name)


def _get_annoset_hash(annoset):
    return '{}#{}#{}#{}'.format(get_text_hash(annoset.sentence.text),
                                annoset.target.indexes,  # TODO: not sure about this. Same annosets for sentences with different tokenization may remain
                                annoset.target.lexunit.name,
                                annoset.target.lexunit.frame.name)


def _filter_annosets(annosets, filtering_options):
    """Filter annosets."""
    annoset_hash_set = set()
    for annoset in annosets:
        annoset_hash = _get_annoset_hash(annoset)
        if _is_valid_annoset(annoset, filtering_options) \
         and annoset_hash not in annoset_hash_set:
            annoset_hash_set.add(annoset_hash)
            yield annoset


def _sort_annosets(annosets):
    """Sort a list of pyfn.AnnotationSet objects.

    Sort by annoset.sentence.text first and then by annoset target hash
    (target.string#target.start#target.end#target.lexunit.name#target.lexunit.frame.name)
    """
    # sort by sentence text as sentences with same text can have different _id
    return sorted(annosets, key=lambda annoset: (annoset.sentence.text,
                                                 _get_annoset_target_hash(
                                                     annoset)))


def filter_and_sort_annosets(annosets, filtering_options):
    return _sort_annosets(_filter_annosets(annosets, filtering_options))
