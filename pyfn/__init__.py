"""Welcome to pyfn.

pyfn can be used to process FrameNet XML data.
"""

import os
import logging
import logging.config

import pyfn.marshalling.unmarshallers.semeval as semeval_unmarshaller
import pyfn.loading.loader as loader
import pyfn.utils.filter as filter_utils
import pyfn.utils.config as config_utils
from pyfn.models.annotationset import AnnotationSet
from pyfn.models.frame import Frame
from pyfn.models.labelstore import LabelStore
from pyfn.models.lexunit import LexUnit
from pyfn.models.sentence import Sentence
from pyfn.models.target import Target
from pyfn.models.valencepattern import ValencePattern

__all__ = ['unmarshall_semeval07_xml', 'AnnotationSet', 'Frame', 'LabelStore',
           'LexUnit', 'Sentence', 'Target', 'ValencePattern']

logging.config.dictConfig(
    config_utils.load(
        os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

logger = logging.getLogger(__name__)


def filter_annosets(source_annosets, target_annosets):
    return filter_utils.filter_annosets(source_annosets, target_annosets)


def unmarshall_semeval07_xml(xml_filepath, flatten=False):
    return semeval_unmarshaller.unmarshall_semeval07_xml(xml_filepath, flatten)


def load_fe_dict(frame_xml_dirpath):
    return loader.load_fe_dict(frame_xml_dirpath)


def load_config(config_file):
    """Load an ImmutableConfig from a YAML configuration file."""
    return config_utils.load(config_file)
