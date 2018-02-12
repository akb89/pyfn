"""Marshalling to SEMEVAL format.

The format matches the XML file expected by the perl evaluation script
of the SEMEVAL 2007 shared task on frame semantic structure extraction.
"""

import os
import datetime
import pytz
import lxml.etree as element_tree

import pyfn.utils.filter as f_utils
import pyfn.utils.sort as sort_utils

from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['marshall_annosets']


def _marshall_annosets(annosets, output_filepath):
    if not annosets:
        raise InvalidParameterError('No input annosets to marshall. Check '
                                    'input parameters and try again.')
    root = element_tree.Element('corpus')
    root.set('XMLCreated', datetime.datetime.now(
        pytz.utc).strftime('%a %b %d %H:%M:%S %Z %Y'))
    documents = element_tree.SubElement(root, 'documents')
    document = element_tree.SubElement(documents, 'document')
    paragraphs = element_tree.SubElement(document, 'paragraphs')
    paragraph = element_tree.SubElement(paragraphs, 'paragraph')
    sentences = element_tree.SubElement(paragraph, 'sentences')
    for annoset in sort_utils.sort_annosets(f_utils.filter_annosets(annosets)):
        pass
    tree = element_tree.ElementTree(root)
    tree.write(output_filepath, encoding='UTF-8', xml_declaration=True,
               pretty_print=True)


def marshall_annosets(annosets_dict, mode, output_dirpath):
    """Marshall a list of pyfn.AnnotationSet objects to SEMEVAL XML."""
    output_filepath = os.path.join(output_dirpath, '{}.gold.xml'.format(mode))
    _marshall_annosets(annosets_dict[mode], output_filepath)
