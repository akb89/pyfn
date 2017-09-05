"""(Enriched) FrameNet AnnotationSet object class."""

from pyFN.models.labelstore import LabelStore
from pyFN.models.target import Target
from pyFN.models.valenceunitstore import ValenceUnitStore
from pyFN.models.valencepattern import ValencePattern

__all__ = ['AnnotationSet']


class AnnotationSet():
    """FrameNet AnnotationSet class."""

    def __init__(self, _id, sentence, target, fn_labelstore, vustore=None,
                 valence_pattern=None, c_date=None):
        """Constructor."""
        self.__id = _id
        self._sentence = sentence
        self._target = target
        self._fn_labelstore = fn_labelstore
        self._vustore = vustore
        self._valence_pattern = valence_pattern
        self._c_date = c_date

    @classmethod
    def from_fn_data(cls, _id, fn_labels, lexunit, sentence, c_date=None,
                     fe_dict=None):
        target = Target.from_fn_data(fn_labels, sentence.text,
                                     sentence.pnw_labelstore.labels_by_indexes,
                                     lexunit)
        fn_labelstore = LabelStore(fn_labels)
        vustore = ValenceUnitStore.from_fn_data(
            fn_labelstore.labels_by_indexes, fe_dict)
        valence_pattern = ValencePattern(vustore.valence_units)
        return AnnotationSet(_id, sentence, target, fn_labelstore, vustore,
                             valence_pattern, c_date)

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
    def fn_labelstore(self):
        """Return a LabelStore object."""
        return self._fn_labelstore

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

    @fn_labelstore.setter
    def fn_labelstore(self, fn_labels):
        self._fn_labelstore = LabelStore(fn_labels)

    @sentence.setter
    def sentence(self, sentence):
        self._sentence = sentence


    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return (self._id) == (other._id)

    def __ne__(self, other):
        return not(self == other)
