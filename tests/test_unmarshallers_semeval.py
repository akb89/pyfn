"""Behavior tests for unmarshallers.semeval."""

import os

import pyfn.marshalling.unmarshallers.semeval as semeval_unmarshaller


SEMEVAL_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources', 'semeval.xml')

semeval_annosets_list = list(semeval_unmarshaller.unmarshall_semeval07_xml(SEMEVAL_XML_FILE))


def test_semeval_annoset():
    annoset = semeval_annosets_list[0][0]
    assert annoset._id == 0
    assert annoset.sentence._id == 0
    assert annoset.sentence.text == 'The boats may appear deceptively primitive , but many of them have their own electric generators and all the modern conveniences .'
    assert len(annoset.fn_labelstore.labels) == 3
    assert annoset.target.lexunit.frame.name == 'Likelihood'
    assert annoset.target.string == 'may'
    assert len(annoset.vustore.valence_units) == 2
    assert annoset.valence_pattern.with_fe_name == 'Hypothetical_event.undefined.undefined Hypothetical_event.undefined.undefined'
