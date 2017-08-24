"""Welcome to pyFN.

pyFN can be used to process FrameNet XML data.
"""

import os
import logging
import logging.config

import pyFN.unmarshallers.framenet as fn_unmarshaller
import pyFN.utils.config as config_utils

__all__ = ['unmarshall_fulltext_xml', 'unmarshall_lexunit_xml']

logging.config.dictConfig(config_utils.load(os.path.abspath('pyFN/logging/logging.yml')))
logger = logging.getLogger(__name__)


def unmarshall_fulltext_xml(xml_file_path):
    return fn_unmarshaller.unmarshall_fulltext_xml(xml_file_path)


def unmarshall_lexunit_xml(xml_file_path):
    return fn_unmarshaller.unmarshall_lexunit_xml(xml_file_path)
