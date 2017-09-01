"""(Enriched) FrameNet AnnotationSet object class."""

import pyFN.utils.framenet as fn_utils
from pyFN.models.labelstore import LabelStore
from pyFN.models.valenceunitstore import ValenceUnitStore
from pyFN.models.valencepattern import ValencePattern

__all__ = ['AnnotationSet']


class AnnotationSet():
    """FrameNet AnnotationSet class."""

    def __init__(self, _id, fn_labels, lexunit, sentence, c_date=None,
                 fe_dict=None):
        """Constructor."""
        self.__id = _id
        self._sentence = sentence
        self._target = fn_utils.to_target(
            sentence.pnw_labelstore.labels_by_indexes, fn_labels, lexunit,
            sentence.text)
        self._fnlabelstore = LabelStore(fn_labels)
        self._vustore = ValenceUnitStore(self._fnlabelstore, fe_dict)
        self._valence_pattern = ValencePattern(self._vustore.valence_units)
        self._c_date = c_date

    @property
    def _id(self):
        """Return the ID of the annotationset."""
        return self.__id

    @property
    def sentence(self):
        """Return the sentence containing the specified annotationset."""
        return self._sentence

    @property
    def target(self):
        """Return the target."""
        return self._target

    @property
    def fnlabelstore(self):
        """Return a LabelStore object."""
        return self._fnlabelstore

    @property
    def vustore(self):
        """Return an ValenceUnitStore object."""
        return self._vustore

    @property
    def valence_pattern(self):
        """Return a ValencePattern object."""
        return self._valence_pattern

    @property
    def c_date(self):
        """Return the annotationset created Date cDate."""
        return self._c_date

    @_id.setter
    def _id(self, _id):
        self.__id = _id

    @fnlabelstore.setter
    def fnlabelstore(self, fn_labels):
        self._fnlabelstore = LabelStore(fn_labels)

    @sentence.setter
    def sentence(self, sentence):
        self._sentence = sentence


    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return (self._id) == (other._id)

    def __ne__(self, other):
        return not(self == other)
