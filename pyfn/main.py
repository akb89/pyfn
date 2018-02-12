"""Welcome to pyfn.

This is the entry point of the application.
"""

import logging
import argparse

import pyfn.marshalling.unmarshallers.framenet as fnxml
import pyfn.marshalling.marshallers.bios as bios
import pyfn.marshalling.marshallers.semeval as semeval

from pyfn.exceptions.parameter import InvalidParameterError

logger = logging.getLogger(__name__)


def _convert(args):
    if args.source_format == args.target_format:
        raise InvalidParameterError(
            'Source and Target formats are the same! Please specify different '
            'source/target formats')
    if args.source_path == args.target_path:
        raise InvalidParameterError(
            'Source and Target paths are the same! Please specify different '
            'source/target paths')
    annosets_dict = {}
    if args.source_format == 'fnxml':
        # TODO: check input directory structure: should contain only
        # train/dev/test dir (other keywords not allowed) and each dir should
        # contain either fulltext, either lu dir, nothing else
        # TODO: when mode is set only parse the mode env
        with_exemplars = args.with_exemplars == 'true'
        annosets_dict = fnxml.get_annosets_dict(args.source_path,
                                                args.splits,
                                                with_exemplars)
    if args.target_format == 'bios':
        # TODO: if the splits_dict contains more than one item but
        # the target_path is a filepath and not a dirpath, change the
        # target_path to the parent directory_path
        bios.marshall_annosets_dict(annosets_dict, args.target_path)
    if args.target_format == 'semeval':
        # TODO: check that target path is a dirpath
        semeval.marshall_annosets(annosets_dict, args.splits, args.target_path)


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
    parser_convert.add_argument('--splits',
                                choices=['train', 'dev', 'test'],
                                default='train',
                                help='FrameNet splits to be unmarshalled')
    args = parser.parse_args()
    args.func(args)
