"""Extract AnnotationSet objects from FrameNet XML files."""

import os
import itertools
import logging

import pyfn.utils.xml as xml_utils
import pyfn.utils.filter as f_utils
import pyfn.marshalling.unmarshallers.exemplar as exemplar_unmarshaller
import pyfn.marshalling.unmarshallers.fulltext as fulltext_unmarshaller


__all__ = ['extract_annosets', 'get_annosets_dict']

logger = logging.getLogger(__name__)


def _filter_annosets_dict(annosets_dict):
    # At least test and train, dev is optional
    filtered_annosets_dict = {}
    test_annosets, _test_annosets, __test_annosets = itertools.tee(
        annosets_dict['test'], 3)
    filtered_annosets_dict['test'] = test_annosets
    if annosets_dict['dev']:
        filtered_dev_annosets = f_utils.filter_annosets(
            annosets_dict['dev'], _test_annosets)
        dev_annosets, _dev_annosets = itertools.tee(filtered_dev_annosets)
        filtered_annosets_dict['dev'] = dev_annosets
        filtered_annosets_dict['train'] = f_utils.filter_annosets(
            annosets_dict['train'], itertools.chain(_dev_annosets,
                                                    __test_annosets))
    else:
        filtered_annosets_dict['train'] = f_utils.filter_annosets(
            annosets_dict['train'], _test_annosets)
    return filtered_annosets_dict


def _get_annosets_dict_from_fn_xml(fn_splits_dirpath, with_exemplars):
    annosets_dict = {}
    for splits_name in os.listdir(fn_splits_dirpath):
        if os.path.isdir(os.path.join(fn_splits_dirpath, splits_name)):
            splits_dirpath = os.path.join(fn_splits_dirpath, splits_name)
            annosets = extract_annosets(
                splits_dirpath, with_fulltexts=True,
                with_exemplars=with_exemplars, flatten=True)
            annosets_dict[splits_name] = annosets
    return annosets_dict


def get_annosets_dict(source_path, with_exemplars):
    """Return a string to AnnotationSet generator dict.

    Keys are splits name (train, dev, test) and values are generators
    on AnnotationSet objects.
    """
    logger.info('Creating pyfn.AnnotationSet dict from {}'.format(source_path))
    return _filter_annosets_dict(
        _get_annosets_dict_from_fn_xml(source_path, with_exemplars))


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
    """Return a list of pyfn.AnnotationSet extracted from splits paths.

    The splits directory should contain two subdirectories name 'fulltext'
    and 'lu'.
    Returns a list of generators over AnnotationSet with [AnnotationSet] <->
    1 fulltext or exemplar XML file if flatten==False
    Returns a generator over AnnotationSet (a single list) if flatten==True
    """
    logger.info('Extracting pyfn.AnnotationSet items from {}'
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
