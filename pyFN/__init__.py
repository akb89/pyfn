"""Welcome to pyFN.

pyFN can be used to process FrameNet XML data.
"""

import os
import logging
import logging.config

import pyFN.unmarshallers.fulltext as fulltext_unmarshaller
import pyFN.unmarshallers.lexunit as lexunit_unmarshaller
import pyFN.unmarshallers.semeval as semeval_unmarshaller
import pyFN.utils.config as config_utils
from pyFN.models.annotationset import AnnotationSet

__all__ = ['unmarshall_fulltext_xml', 'unmarshall_lexunit_xml',
           'unmarshall_semeval07_xml', 'AnnotationSet']

logging.config.dictConfig(config_utils.load(os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))
logger = logging.getLogger(__name__)


def unmarshall_fulltext_xml(xml_filepath):
    return fulltext_unmarshaller.unmarshall_fulltext_xml(xml_filepath)


def unmarshall_lexunit_xml(xml_filepath):
    return lexunit_unmarshaller.unmarshall_lexunit_xml(xml_filepath)


def unmarshall_semeval07_xml(xml_filepath):
    return semeval_unmarshaller.unmarshall_semeval07_xml(xml_filepath)
