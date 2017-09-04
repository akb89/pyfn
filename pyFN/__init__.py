"""Welcome to pyFN.

pyFN can be used to process FrameNet XML data.
"""

import os
import logging
import logging.config

import pyFN.marshalling.unmarshallers.fulltext as fulltext_unmarshaller
import pyFN.marshalling.unmarshallers.lexunit as lexunit_unmarshaller
import pyFN.marshalling.unmarshallers.semeval as semeval_unmarshaller
import pyFN.utils.config as config_utils
import pyFN.loading.loader as loader
from pyFN.models.annotationset import AnnotationSet
from pyFN.models.frame import Frame
from pyFN.models.labelstore import LabelStore
from pyFN.models.lexunit import LexUnit
from pyFN.models.sentence import Sentence
from pyFN.models.target import Target
from pyFN.models.valencepattern import ValencePattern

__all__ = ['unmarshall_fulltext_xml', 'unmarshall_lexunit_xml',
           'unmarshall_semeval07_xml', 'AnnotationSet', 'Frame', 'LabelStore',
           'LexUnit', 'Sentence', 'Target', 'ValencePattern']

logging.config.dictConfig(
    config_utils.load(
        os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

logger = logging.getLogger(__name__)


def unmarshall_fulltext_xml(xml_filepath, fe_dict=None):
    return fulltext_unmarshaller.unmarshall_fulltext_xml(xml_filepath, fe_dict)


def unmarshall_lexunit_xml(xml_filepath, fe_dict=None):
    return lexunit_unmarshaller.unmarshall_lexunit_xml(xml_filepath, fe_dict)


def unmarshall_semeval07_xml(xml_filepath):
    return semeval_unmarshaller.unmarshall_semeval07_xml(xml_filepath)


def load_fe_dict(frame_xml_dirpath):
    return loader.load_fe_dict(frame_xml_dirpath)
