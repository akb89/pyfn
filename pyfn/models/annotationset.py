"""(Enriched) FrameNet AnnotationSet object class."""

from pyfn.models.labelstore import LabelStore
from pyfn.models.target import Target
from pyfn.models.valenceunitstore import ValenceUnitStore
from pyfn.models.valencepattern import ValencePattern

__all__ = ['AnnotationSet']


# pylint: disable=R0902
class AnnotationSet():
    """FrameNet AnnotationSet class."""

    # pylint: disable=R0913
    def __init__(self, _id=None, sentence=None, target=None,
                 labelstore=None, vustore=None, valence_pattern=None,
                 c_date=None, xml_schema_type=None):
        """Constructor."""
        self.__id = _id
        self._sentence = sentence
        self._target = target
        self._labelstore = labelstore
        self._vustore = vustore
        self._valence_pattern = valence_pattern
        self._c_date = c_date
        self._xml_schema_type = xml_schema_type

    @classmethod
    def from_fn_data(cls, _id, fn_labels, lexunit, sentence, xml_schema_type,
                     fe_dict, c_date=None):
        """Return an instance of AnnotationSet generated from given FN data."""
        target = Target.from_fn_data(fn_labels, sentence.text,
                                     sentence.pnw_labelstore.labels_by_indexes,
                                     lexunit)
        labelstore = LabelStore(fn_labels)
        vustore = ValenceUnitStore.from_fn_data(
            labelstore.labels_by_indexes, fe_dict)
        valence_pattern = ValencePattern(vustore.valence_units)
        return cls(_id=_id, sentence=sentence, target=target,
                   labelstore=labelstore, vustore=vustore,
                   valence_pattern=valence_pattern, c_date=c_date,
                   xml_schema_type=xml_schema_type)

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
        """Return the annotated target."""
        return self._target

    @property
    def labelstore(self):
        """Return a LabelStore object."""
        return self._labelstore

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

    @property
    def xml_schema_type(self):
        """Return the initial XML format.

        The XML format corresponds to the schema from which the AnnotationSet
        was generated: FN 'fulltext', 'exemplar' (lu) or 'semeval'.
        """
        return self._xml_schema_type

    @_id.setter
    def _id(self, _id):
        self.__id = _id

    @target.setter
    def target(self, target):
        self._target = target

    @labelstore.setter
    def labelstore(self, labelstore):
        self._labelstore = labelstore

    @sentence.setter
    def sentence(self, sentence):
        self._sentence = sentence

    @valence_pattern.setter
    def valence_pattern(self, valence_pattern):
        self._valence_pattern = valence_pattern

    def __hash__(self):
        """Return hash on AnnotationSet _id."""
        return hash(self._id)

    def __eq__(self, other):
        """Compare _id fields of two AnnotationSet instances."""
        return (self._id) == (other._id)

    def __ne__(self, other):
        """Return standard not equal comparator."""
        return not self == other
