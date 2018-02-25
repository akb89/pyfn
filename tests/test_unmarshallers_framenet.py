"""Behavior tests for unmarshallers.framenet."""

import os

import pyfn.marshalling.unmarshallers.framenet as framenet


SPLITS_DIRPATH = os.path.join(os.path.dirname(__file__), 'resources',
                              'splits')
LU_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources',
                           'splits', 'lu', 'lu.xml')
FULLTEXT_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources',
                                 'splits', 'fulltext', 'fulltext.xml')
ex_annosets_list = list(framenet._unmarshall_exemplar_xml(LU_XML_FILE, {}))
fulltext_annosets_list = list(framenet._unmarshall_fulltext_xml(FULLTEXT_XML_FILE, {}))


def test_get_fe_dict():
    FRAME1_XML_FILEPATH = os.path.join(SPLITS_DIRPATH, 'frame', 'Being_at_risk.xml')
    FRAME2_XML_FILEPATH = os.path.join(SPLITS_DIRPATH, 'frame', 'Request.xml')
    fe_dict = framenet._get_fe_dict([FRAME1_XML_FILEPATH, FRAME2_XML_FILEPATH])
    assert len(fe_dict) == 24
    assert fe_dict[1492]._id == 1492
    assert fe_dict[1492].name == 'Means'
    assert fe_dict[1492].coretype == 'Peripheral'


def test_fulltext_annosets_counts():
    assert len(fulltext_annosets_list) == 2
    assert len([item for sublist in fulltext_annosets_list for item in sublist]) == 8


def test_fulltext_annoset():
    annoset = fulltext_annosets_list[0][0]
    assert annoset._id == 6557242
    assert annoset.sentence._id == 4106520
    assert annoset.sentence.text == 'That \'s where you - and Goodwill - come in .'
    assert len(annoset.labelstore.labels) == 5
    assert len(annoset.vustore.valence_units) == 2
    assert annoset.valence_pattern.with_fe_name == 'Figure.Sfin.Dep Ground.undefined.undefined'

def test_fulltext_ini_fe():
    annoset = fulltext_annosets_list[1][3]
    assert annoset._id == 6557332
    assert annoset.valence_pattern.with_fe_name == 'Employee.INI Employer.INI'

def test_fulltext_target():
    pass


def test_ex_annosets_counts():
    assert len(ex_annosets_list) == 2
    assert len([item for sublist in ex_annosets_list for item in sublist]) == 2


def test_lu_annoset():
    annoset = ex_annosets_list[1][0]
    assert annoset._id == 310929
    assert len(annoset.vustore.valence_units) == 6
    assert annoset.valence_pattern.with_fe_name ==\
     'Agent.NP.Ext Agent.NP.Ext Agent.NP.Obj Body_part.NP.Obj Path.PP.Dep Time.PP.Dep'


def test_lu_target():
    annoset = ex_annosets_list[0][0]
    assert annoset.target.string == 'Arch'
    assert annoset.target.lexunit._id == 65
    assert annoset.target.lexunit.name == 'arch.v'
    assert annoset.target.lexunit.pos == 'v'
    assert annoset.target.lexunit.frame._id == 16
    assert annoset.target.lexunit.frame.name == 'Body_movement'
    assert len(annoset.target.indexes) == 1
    assert annoset.target.indexes == [(0, 3)]
    assert len(annoset.target.pos_tags) == 1
    assert annoset.target.pos_tags[0].name == 'VVB'


def test_extract_annosets_with_ft_with_ex_flatten_false():
    annosets = list(framenet.extract_annosets(
        SPLITS_DIRPATH, with_fulltexts=True, with_exemplars=True, fe_dict={},
        flatten=False))
    assert len(annosets) == 4
    assert len([item for sublist in annosets for item in sublist]) == 10


def test_extract_annosets_with_ft_with_ex_flatten_true():
    annosets = list(framenet.extract_annosets(
        SPLITS_DIRPATH, True, True, {}, flatten=True))
    assert len(annosets) == 10


def test_extract_annosets_with_ft_flatten_false():
    annosets = list(framenet.extract_annosets(
        SPLITS_DIRPATH, True, False, {}, flatten=False))
    assert len(annosets) == 2
    assert len([item for sublist in annosets for item in sublist]) == 8


def test_extract_annosets_with_ft_flatten_true():
    annosets = list(framenet.extract_annosets(
        SPLITS_DIRPATH, True, False, {}, flatten=True))
    assert len(annosets) == 8


def test_extract_annosets_with_ex_flatten_false():
    annosets = list(framenet.extract_annosets(
        SPLITS_DIRPATH, False, True, {}, flatten=False))
    assert len(annosets) == 2
    assert len([item for sublist in annosets for item in sublist]) == 2


def test_extract_annosets_with_ex_flatten_true():
    annosets = list(framenet.extract_annosets(
        SPLITS_DIRPATH, False, True, {}, flatten=True))
    assert len(annosets) == 2
