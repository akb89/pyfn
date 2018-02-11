"""Extract AnnotationSet objects from FrameNet XML files."""

import os
import re
import itertools
import logging

import pyfn.utils.xml as xml_utils
import pyfn.marshalling.unmarshallers.exemplar as exemplar_unmarshaller
import pyfn.marshalling.unmarshallers.fulltext as fulltext_unmarshaller


__all__ = ['extract_annosets', 'get_annosets_dict']

logger = logging.getLogger(__name__)


def _get_text_hash(text):
    return re.sub(r'\s+', '', text.strip())


def _filter_annosets(annosets, filtered_sent_hash_set):
    for annoset in annosets:
        text_hash = _get_text_hash(annoset.sentence.text)
        if text_hash not in filtered_sent_hash_set:
            yield annoset
        else:
            print('Found hash: {}'.format(text_hash))


def _get_sent_hash_set(annosets):
    return {_get_text_hash(annoset.sentence.text) for annoset in
            annosets}


def _filter_annosets_dict(annosets_dict):
    # At least test and train, dev is optional
    filtered_annosets_dict = {}
    test_annosets, _test_annosets = itertools.tee(annosets_dict['test'])
    test_sent_hash_set = _get_sent_hash_set(_test_annosets)
    filtered_annosets_dict['test'] = test_annosets
    if annosets_dict['dev']:
        dev_annosets, _dev_annosets = itertools.tee(annosets_dict['dev'])
        filtered_annosets_dict['dev'] = _filter_annosets(
            dev_annosets, test_sent_hash_set)
        dev_sent_hash_set = set(_get_sent_hash_set(_dev_annosets)).union(
            test_sent_hash_set)
        filtered_annosets_dict['train'] = _filter_annosets(
            annosets_dict['train'], dev_sent_hash_set)
    else:
        filtered_annosets_dict['train'] = _filter_annosets(
            annosets_dict['train'], test_sent_hash_set)
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
