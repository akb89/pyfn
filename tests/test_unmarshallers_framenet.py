"""Behavior tests for unmarshallers.framenet."""

import os
import pytest

import pyFN.unmarshallers.framenet as fn_unmarshaller
import pyFN.utils.framenet as fn_utils


FULLTEXT_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources',
                                 'fulltext.xml')
LU_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources', 'lu.xml')

fulltext_annosets_list = fn_unmarshaller.unmarshall_fulltext_xml(FULLTEXT_XML_FILE)
lu_annosets_list = fn_unmarshaller.unmarshall_lexunit_xml(LU_XML_FILE)


def test_annosets_counts():
    assert len(fulltext_annosets_list) == 2
    assert len(lu_annosets_list) == 2
    assert len([item for sublist in fulltext_annosets_list for item in sublist]) == 8
    assert len([item for sublist in lu_annosets_list for item in sublist]) == 2


def test_fulltext_annoset():
    annoset = fulltext_annosets_list[0][0]
    assert annoset._id == 6557242
    assert annoset.sentence._id == 4106520
    assert annoset.sentence.text == 'That \'s where you - and Goodwill - come in .'
    assert len(annoset.fn_labels) == 5
    assert len(annoset.valence_units) == 0
    assert annoset.valence_pattern == ''

def test_lu_annoset():
    annoset = lu_annosets_list[1][0]
    assert annoset._id == 310929
    assert len(annoset.valence_units) == 6
    assert annoset.valence_pattern == 'Agent.NP.Ext Body_part.NP.Obj Agent.NP.Obj Path.PP.Dep Time.PP.Dep Agent.NP.Ext'


def test_fulltext_target():
    pass


def test_lu_target():
    annoset = lu_annosets_list[0][0]
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
