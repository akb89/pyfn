"""Welcome to pyfn.

This is the entry point of the application.
"""

import os
import re
import itertools
import logging
import argparse

import pyfn.extraction.extractors.framenet as extractor

from pyfn.exceptions.parameter import InvalidParameterError

logger = logging.getLogger(__name__)


def _marshall_to_bios(annosets_dict, target_path):
    pass


def _get_text_hash(text):
    return re.sub(r'\s+', '#', text.strip())


def _filter_annosets(annosets, filtered_sent_hash_set):
    for annoset in annosets:
        text_hash = _get_text_hash(annoset.sentence.text)
        if text_hash not in filtered_sent_hash_set:
            yield annoset


def _get_sent_hash_set(annosets):
    return {_get_text_hash(annoset.sentence.text) for annoset in
            annosets}


def _filter_annosets_dict(annosets_dict):
    # At least test and train, dev is optional
    filtered_annosets_dict = {}
    test_annosets, _test_annosets = itertools.tee(annosets_dict['test'])
    filtered_sent_hash_set = _get_sent_hash_set(_test_annosets)
    filtered_annosets_dict['test'] = test_annosets
    if annosets_dict['dev']:
        dev_annosets, _dev_annosets = itertools.tee(annosets_dict['dev'])
        filtered_sent_hash_set |= _get_sent_hash_set(_dev_annosets)
        filtered_annosets_dict['dev'] = _filter_annosets(
            dev_annosets, filtered_sent_hash_set)
    filtered_annosets_dict['train'] = _filter_annosets(
        annosets_dict['train'], filtered_sent_hash_set)
    return filtered_annosets_dict


def _get_annosets_dict_from_fn_xml(fn_splits_dirpath, with_exemplars=False):
    annosets_dict = {}
    for splits_name in os.listdir(fn_splits_dirpath):
        if os.path.isdir(os.path.join(fn_splits_dirpath, splits_name)):
            splits_dirpath = os.path.join(fn_splits_dirpath, splits_name)
            annosets = extractor.extract_annosets(
                splits_dirpath, with_fulltexts=True,
                with_exemplars=with_exemplars, flatten=True)
            annosets_dict[splits_name] = annosets
    return annosets_dict


def _convert(args):
    if args.source_format == args.target_format:
        raise InvalidParameterError(
            'Source and Target formats are the same! Please specify different '
            'source/target formats')
    if args.source_path == args.target_path:
        raise InvalidParameterError(
            'Source and Target paths are the same! Please specify different '
            'source/target paths')
    if args.source_format == 'fnxml':
        # TODO: check input directory structure: should contain only
        # train/dev/test dir (other keywords not allowed) and each dir should
        # contain either fulltext, either lu dir, nothing else
        with_exemplars = args.with_exemplars == 'true'
        annosets_dict = _filter_annosets_dict(
            _get_annosets_dict_from_fn_xml(args.source_path, with_exemplars))
    if args.target_format == 'bios':
        # TODO: if the splits_dict contains more than one item but
        # the target_path is a filepath and not a dirpath, change the
        # target_path to the parent directory_path
        _marshall_to_bios(annosets_dict, args.target_path)
    if args.target_format == 'semeval':
        pass


def main():
    """Launch the pyfn application."""
    parser = argparse.ArgumentParser(prog='pyfn')
    subparsers = parser.add_subparsers()
    parser_convert = subparsers.add_parser(
        'convert', formatter_class=argparse.RawTextHelpFormatter,
        help='Convert source file from given format to target file in given '
             'format')
    parser_convert.set_defaults(func=_convert)
    parser_convert.add_argument('--source', required=True,
                                dest='source_path',
                                help='Absolute filepath to source file')
    parser_convert.add_argument('--target', required=True,
                                dest='target_path',
                                help='Absolute filepath to target file')
    parser_convert.add_argument('--from', required=True,
                                dest='source_format',
                                choices=['conll', 'bios', 'semeval', 'fnxml'],
                                help='''Source format. Choose between:
    - conll: the CoNLL format used by the semafor parser
    - bios: the BIOS format used by the open-sesame parser
    - semeval: the SEMEVAL 2008 XML format
    - fnxml: the standard FrameNet XML format
    ''')
    parser_convert.add_argument('--to', required=True,
                                dest='target_format',
                                choices=['conll', 'bios', 'semeval', 'fnxml'],
                                help='''Target format. Choose between:
    - conll: the CoNLL format used by the semafor parser
    - bios: the BIOS format used by the open-sesame parser
    - semeval: the SEMEVAL 2008 XML format
    - fnxml: the standard FrameNet XML format
    ''')
    parser_convert.add_argument('--with_exemplars',
                                choices=['true', 'false'],
                                default='false',
                                help='Whether or not to use exemplars in '
                                     'splits. Default to false')
    args = parser.parse_args()
    args.func(args)
