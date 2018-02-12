"""Marshalling to SEMEVAL format.

The format matches the XML file expected by the perl evaluation script
of the SEMEVAL 2007 shared task on frame semantic structure extraction.
"""

import os
import lxml.etree as element_tree
from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['marshall_annosets']


def _marshall_annosets(annosets, output_filepath):
    if not annosets:
        raise InvalidParameterError('No input annosets to marshall. Check '
                                    'input parameters and try again.')
    root = element_tree.Element('corpus')
    tree = element_tree.ElementTree(root)
    tree.write(output_filepath, encoding='UTF-8', xml_declaration=True,
               pretty_print=True)


def marshall_annosets(annosets_dict, mode, output_dirpath):
    """Marshall a list of pyfn.AnnotationSet objects to SEMEVAL XML."""
    output_filepath = os.path.join(output_dirpath, '{}.gold.xml'.format(mode))
    _marshall_annosets(annosets_dict[mode], output_filepath)
