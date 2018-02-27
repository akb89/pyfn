"""Testing filtering utils."""

import pyfn.utils.filter as f_utils

from pyfn.models.annotationset import AnnotationSet
from pyfn.models.labelstore import LabelStore
from pyfn.models.label import Label
from pyfn.models.layer import Layer
from pyfn.models.lexunit import LexUnit
from pyfn.models.frame import Frame
from pyfn.models.target import Target
from pyfn.models.sentence import Sentence


def test_has_overlapping_fes():
    label_1 = Label(name=None, layer=Layer(name='FE'), start=96, end=105)
    label_2 = Label(name=None, layer=Layer(name='FE'), start=90, end=105)
    label_3 = Label(name=None, layer=Layer(name='FE'), start=40, end=89)
    label_4 = Label(name=None, layer=Layer(name='FE'), start=91, end=97)
    label_5 = Label(name=None, layer=Layer(name='FE'), start=105, end=134)
    label_6 = Label(name=None, layer=Layer(name='FE'), start=91, end=134)
    annoset = AnnotationSet(labelstore=LabelStore(labels=[label_1, label_2]))
    annoset1 = AnnotationSet(labelstore=LabelStore(labels=[label_2, label_3]))
    annoset2 = AnnotationSet(labelstore=LabelStore(labels=[label_4, label_5, label_6]))
    assert f_utils._has_overlapping_fes(annoset) is True
    assert f_utils._has_overlapping_fes(annoset1) is False
    assert f_utils._has_overlapping_fes(annoset2) is True

def test_get_annoset_hash():
    annoset = AnnotationSet(sentence=Sentence(_id=1, text=' This IS a    TEST o test '),
                            target=Target(lexunit=LexUnit(name='test test.n',
                                                          frame=Frame(name='Test')),
                                          indexes=[(14,17), (21,24)]))
    assert f_utils._get_annoset_hash(annoset) == 'thisisatestotest#14#17#21#24#test test.n#Test'

def test_filter_annosets():
    excluded_annoset_id = AnnotationSet(_id=1)
    excluded_frame = AnnotationSet(
        _id=2, target=Target(lexunit=LexUnit(frame=Frame(_id=1, name='Excluded'))))
    duplicate_annoset1 = AnnotationSet(
        _id=3, sentence=Sentence(_id=1, text=' This IS a    TEST o test '),
        target=Target(lexunit=LexUnit(name='test test.n',
                                      frame=Frame(_id=2, name='Test')),
                      indexes=[(14, 17), (21, 24)]),
        labelstore=LabelStore(labels=[Label(start=1, end=2)]))
    duplicate_annoset2 = AnnotationSet(
        _id=4, sentence=Sentence(_id=2, text=' This IS a    TEST o test '),
        target=Target(lexunit=LexUnit(name='test test.n',
                                      frame=Frame(_id=2, name='Test')),
                      indexes=[(14, 17), (21, 24)]),
        labelstore=LabelStore(labels=[Label(start=1, end=2)]))
    missing_label = AnnotationSet(
        _id=5, sentence=Sentence(_id=3),
        target=Target(lexunit=LexUnit(frame=Frame(_id=2, name='Test'))),
        labelstore=LabelStore(labels=[Label(start=-1, end=2)]))
    whitespace_label = AnnotationSet(
        _id=6, sentence=Sentence(_id=4, text=' pointing at whitespace'),
        target=Target(lexunit=LexUnit(frame=Frame(_id=2, name='Test'))),
        labelstore=LabelStore(labels=[Label(start=0, end=2)]))
    excluded_sentence_id = AnnotationSet(
        _id=7, sentence=Sentence(_id=5),
        target=Target(lexunit=LexUnit(name='test test.n',
                                      frame=Frame(_id=2, name='Test'))))
    annosets = [excluded_annoset_id, excluded_sentence_id, excluded_frame,
                duplicate_annoset1, duplicate_annoset2, missing_label,
                whitespace_label]
    filtered_annosets = list(f_utils._filter_annosets(
        annosets, [], [1], [5], [1]))
    assert len(filtered_annosets) == 1
    assert filtered_annosets[0]._id == 3
