"""A set of methods used to handle and process FrameNet data."""

import logging
from pyFN.models.target import Target

__all__ = ['extract_pos', 'to_target']


logger = logging.getLogger(__name__)


def extract_pos(luname):
    """Return the part of speech of the lexunit name."""
    if luname is None:
        return None
    return luname.split('.')[1]


def _extract_flat_target_pnw_labels(target_indexes, pnw_labels_by_indexes):
    target_pnw_labels = [labels for indexes, labels
                         in pnw_labels_by_indexes.items()
                         if indexes in target_indexes]
    return [item for sublist in target_pnw_labels for item in sublist]


def _extract_target_pos_tags(target_indexes, pnw_labels_by_indexes):
    flat_target_pnw_labels = _extract_flat_target_pnw_labels(
        target_indexes, pnw_labels_by_indexes)
    return [label for label in flat_target_pnw_labels
            if label.layer.name =='PENN' or label.layer.name == 'BNC']


def _extract_target_string(text, indexes):
    for (start, end) in indexes:
        if start == -1 or end == -1:
            logger.debug(
                'Target indexes are not specified in sentence: {}'
                .format(text))
            return ''
    return ' '.join([text[start: end+1] for (start, end) in indexes])


def _extract_target_indexes(fn_labels):
    return [(label.start, label.end) for label in fn_labels
            if label.layer.name == 'Target']


def to_target(pnw_labels_by_indexes, fn_labels, lexunit, text):
    target_indexes = _extract_target_indexes(fn_labels)
    target_string = _extract_target_string(text, target_indexes)
    target_pos_tags = _extract_target_pos_tags(target_indexes,
                                               pnw_labels_by_indexes)
    return Target(target_string, lexunit, target_indexes, target_pos_tags)
