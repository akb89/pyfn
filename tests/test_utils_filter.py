"""Testing filtering utils."""

import pyfn.utils.filter as f_utils

from pyfn.models.annotationset import AnnotationSet
from pyfn.models.labelstore import LabelStore
from pyfn.models.label import Label
from pyfn.models.layer import Layer


def test_has_overlapping_fes():
    annoset = AnnotationSet(labelstore=LabelStore(labels=[]))
    label_1 = Label(name=None, layer=Layer(name='FE'), start=96, end=105)
    label_2 = Label(name=None, layer=Layer(name='FE'), start=90, end=105)
    annoset.labelstore.labels.extend([label_1, label_2])
    assert f_utils._has_overlapping_fes(annoset) is True
