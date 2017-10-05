"""Extract AnnotationSet objects from FrameNet XML files."""

import itertools
import logging

import pyFN.utils.xml as xml_utils
import pyFN.marshalling.unmarshallers.exemplar as exemplar_unmarshaller
import pyFN.marshalling.unmarshallers.fulltext as fulltext_unmarshaller


__all__ = ['extract_annosets']

logger = logging.getLogger(__name__)


def _extract_ex_annosets(ex_filepaths, fe_dict=None, flatten=False):
    generators = []
    for exemplar_filepath in ex_filepaths:
        generators.append(exemplar_unmarshaller.unmarshall_exemplar_xml(
            exemplar_filepath, fe_dict, flatten))
    return generators


def _extract_ft_annosets(ft_filepaths, fe_dict=None, flatten=False):
    generators = []
    for fulltext_filepath in ft_filepaths:
        generators.append(fulltext_unmarshaller.unmarshall_fulltext_xml(
            fulltext_filepath, fe_dict, flatten))
    return generators


def extract_annosets(splits_dirpath, with_fulltexts, with_exemplars,
                     fe_dict=None, flatten=False):
    """Return a list of pyFN.AnnotationSet extracted from splits paths.

    The splits directory should contain two subdirectories name 'fulltext'
    and 'lu'.
    Returns a list of generators over AnnotationSet with [AnnotationSet] <->
    1 fulltext or exemplar XML file if flatten=False
    Returns a generator over AnnotationSet (a single list) if flatten=True
    """
    logger.info('Extracting pyFN.AnnotationSet items from {}'
                .format(splits_dirpath))
    ft_annosets = []
    ex_annosets = []
    if with_fulltexts:
        ft_filepaths = xml_utils.get_xml_filepaths(splits_dirpath,
                                                   'fulltext')
        ft_annosets = _extract_ft_annosets(ft_filepaths, fe_dict, flatten)
    if with_exemplars:
        ex_filepaths = xml_utils.get_xml_filepaths(splits_dirpath,
                                                   'lu')
        ex_annosets = _extract_ex_annosets(ex_filepaths, fe_dict, flatten)
    return itertools.chain(*ft_annosets, *ex_annosets)
