"""FrameNet AnnotationSet's Target class."""

import logging

__all__ = ['Target']

logger = logging.getLogger(__name__)


def _extract_flat_target_pnw_labels(target_indexes, pnw_labels_by_indexes):
    target_pnw_labels = [labels for indexes, labels
                         in pnw_labels_by_indexes.items()
                         if indexes in target_indexes]
    return [item for sublist in target_pnw_labels for item in sublist]


def _extract_target_pos_tags(target_indexes, pnw_labels_by_indexes):
    flat_target_pnw_labels = _extract_flat_target_pnw_labels(
        target_indexes, pnw_labels_by_indexes)
    return [label for label in flat_target_pnw_labels
            if label.layer.name == 'PENN' or label.layer.name == 'BNC']


def _extract_target_string(text, indexes):
    for (start, end) in indexes:
        if start == -1 or end == -1:
            logger.debug(
                'Target indexes are not specified in sentence: {}'
                .format(text))
            return ''
    return ' '.join([text[start: end+1] for (start, end) in indexes])


def _extract_target_indexes(fn_labels):
    return sorted([(label.start, label.end) for label in fn_labels
                   if label.layer.name == 'Target'])


class Target():
    """FrameNet target class."""

    def __init__(self, string=None, lexunit=None, indexes=None, pos_tags=None):
        """Constructor."""
        self._string = string
        self._lexunit = lexunit
        self._indexes = indexes
        self._pos_tags = pos_tags

    @classmethod
    def from_fn_data(cls, fn_labels, text, pnw_labels_by_indexes, lexunit):
        """Return Target instance generated from FrameNet data."""
        indexes = _extract_target_indexes(fn_labels)
        string = _extract_target_string(text, indexes)
        pos_tags = _extract_target_pos_tags(indexes, pnw_labels_by_indexes)
        return cls(string, lexunit, indexes=indexes, pos_tags=pos_tags)

    @property
    def string(self):
        """Return the string of the target."""
        return self._string

    @property
    def lexunit(self):
        """Return the lexunit corresponding to the target."""
        return self._lexunit

    @property
    def indexes(self):
        """Return a (sorted) list of index tuples (start, end)."""
        return sorted(self._indexes)

    @property
    def pos_tags(self):
        """Return a list of PENN or BNC POS tags for the given target."""
        return self._pos_tags

    @string.setter
    def string(self, string):
        self._string = string

    @lexunit.setter
    def lexunit(self, lexunit):
        self._lexunit = lexunit

    @indexes.setter
    def indexes(self, indexes):
        self._indexes = indexes

    @pos_tags.setter
    def pos_tags(self, pos_tags):
        self._pos_tags = pos_tags
