"""Behavior tests for unmarshallers.framenet."""

import os

import pyFN.marshalling.unmarshallers.fulltext as fulltext_unmarshaller


FULLTEXT_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources',
                                 'fulltext.xml')

fulltext_annosets_list = list(fulltext_unmarshaller.unmarshall_fulltext_xml(FULLTEXT_XML_FILE))


def test_annosets_counts():
    assert len(fulltext_annosets_list) == 2
    assert len([item for sublist in fulltext_annosets_list for item in sublist]) == 8


def test_fulltext_annoset():
    annoset = fulltext_annosets_list[0][0]
    assert annoset._id == 6557242
    assert annoset.sentence._id == 4106520
    assert annoset.sentence.text == 'That \'s where you - and Goodwill - come in .'
    assert len(annoset.fnlabelstore.labels) == 5
    assert len(annoset.vustore.valence_units) == 0
    assert annoset.valence_pattern.with_fe_name == ''

def test_fulltext_ini_fe():
    annoset = fulltext_annosets_list[1][3]
    assert annoset._id == 6557332
    assert annoset.valence_pattern.with_fe_name == 'Employee.INI Employer.INI'

def test_fulltext_target():
    pass
