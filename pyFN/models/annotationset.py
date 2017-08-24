"""(Enriched) FrameNet AnnotationSet object class."""

import pyFN.utils.framenet as fn_utils

__all__ = ['AnnotationSet']


class AnnotationSet():
    """FrameNet AnnotationSet class."""

    def __init__(self, _id, fn_labels, lexunit, sentence):
        """Constructor."""
        self.__id = _id
        self._fn_labels = fn_labels
        self._fn_labels_by_layer_name = fn_utils.to_labels_by_layer_name(fn_labels)
        self._fn_labels_by_indexes = fn_utils.to_labels_by_indexes(fn_labels)
        self._sentence = sentence
        self._target = fn_utils.to_target(fn_labels, lexunit)
        self._valence_units = fn_utils.to_valence_units(self._labels_by_layer_name)
        self._valence_pattern = fn_utils.to_valence_pattern(self._valence_units)

    @property
    def _id(self):
        """Return the ID of the annotationset."""
        return self.__id

    @property
    def fn_labels(self):
        """Return a list of FrameNet labels."""
        return self._fn_labels

    @property
    def fn_labels_by_layer_name(self):
        """Return a dict of (FrameNet) labels, excluding PENN, NER and WSL labels.

        Keys are layer names and values are lists of labels
        """
        return self._fn_labels_by_layer_name

    @property
    def fn_labels_by_indexes(self):
        """Return a dict of labels.

        Keys are tuples (label.startChar, label.endChar) and values are lists
        of labels
        """
        return self._fn_labels_by_indexes

    @property
    def sentence(self):
        """Return the sentence containing the specified annotationset."""
        return self._sentence

    @property
    def target(self):
        """Return the target."""
        return self._target

    @property
    def valence_units(self):
        """Return a list of valence units."""
        return self._valence_units

    @property
    def valence_pattern(self):
        """Return a valence pattern."""
        return self._valence_pattern

    @_id.setter
    def _id(self, _id):
        self.__id = _id

    @labels.setter
    def labels(self, labels):
        self._labels = labels

    @sentence.setter
    def sentence(self, sentence):
        self._sentence = sentence


    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return (self._id) == (other._id)

    def __ne__(self, other):
        return not(self == other)
