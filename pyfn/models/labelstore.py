"""Storing different formats for labels."""

from collections import defaultdict

__all__ = ['LabelStore']


class LabelStore():
    """Storing lists or dict of labels."""

    def __init__(self, labels):
        """Constructor."""
        self._labels = labels

    @property
    def labels(self):
        """Return a list of Label objects."""
        return self._labels

    @property
    def labels_by_indexes(self):
        """Return a dict of Label objects, excluding PENN, NER and WSL labels.

        Keys are tuples (label.startChar, label.endChar) and values are lists
        of labels
        """
        if not self._labels:
            return {}
        labels_by_indexes = defaultdict(list)
        for label in self._labels:
            labels_by_indexes[(label.start, label.end)].append(label)
        return labels_by_indexes

    @property
    def labels_by_layer_name(self):
        """Return a dict of Label objects, excluding PENN, NER and WSL labels.

        Keys are layer names and values are lists of Label objects
        """
        if not self._labels:
            return {}
        labels_by_layer_name = defaultdict(list)
        for label in self._labels:
            labels_by_layer_name[label.layer.name].append(label)
        return labels_by_layer_name

    @property
    def labels_by_layer(self):
        """Return a dict of Label objects.

        Keys are Layer objects and values are lists of Label objects
        Labelstore in annoset exclude PENN, NER and WSL labels.
        Thoses labels are included in the pnw_labelstore of the Sentence instances
        """
        if not self._labels:
            return {}
        labels_by_layer = defaultdict(list)
        for label in self._labels:
            labels_by_layer[label.layer].append(label)
        return labels_by_layer

    @labels.setter
    def labels(self, labels):
        self._labels = labels
