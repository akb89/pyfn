"""Behavior tests for unmarshallers.framenet."""

import os

import pyFN.marshalling.unmarshallers.lexunit as lexunit_unmarshaller


LU_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources', 'lu.xml')

lu_annosets_list = list(lexunit_unmarshaller.unmarshall_lexunit_xml(LU_XML_FILE))


def test_annosets_counts():
    assert len(lu_annosets_list) == 2
    assert len([item for sublist in lu_annosets_list for item in sublist]) == 2


def test_lu_annoset():
    annoset = lu_annosets_list[1][0]
    assert annoset._id == 310929
    assert len(annoset.vustore.valence_units) == 6
    assert annoset.valence_pattern.with_fe_name ==\
     'Agent.NP.Ext Agent.NP.Ext Agent.NP.Obj Body_part.NP.Obj Path.PP.Dep Time.PP.Dep'


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
