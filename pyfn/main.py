"""Welcome to pyfn.

This is the entry point of the application.
"""

import os
import argparse

import logging
import logging.config

import pyfn.utils.config as config_utils
import pyfn.marshalling.marshallers.bios as biosm
import pyfn.marshalling.marshallers.rofames as rofamesm
import pyfn.marshalling.marshallers.semeval as semeval
import pyfn.marshalling.unmarshallers.bios as biosu
import pyfn.marshalling.unmarshallers.framenet as fnxml
import pyfn.marshalling.unmarshallers.rofames as rofamesu


from pyfn.exceptions.parameter import InvalidParameterError

logging.config.dictConfig(
    config_utils.load(
        os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

logger = logging.getLogger(__name__)


def _extract_splits_name(source_path):
    return os.path.splitext(os.path.basename(source_path))[0]


def _convert(args):
    if args.source_format == args.target_format:
        raise InvalidParameterError(
            'Source and Target formats are the same! Please specify different '
            'source/target formats')
    if args.source_path == args.target_path:
        raise InvalidParameterError(
            'Source and Target paths are the same! Please specify different '
            'source/target paths')
    # TODO: add validation for input directory structure
    if args.source_format == 'fnxml':
        annosets_dict = fnxml.get_annosets_dict(args.source_path,
                                                args.splits,
                                                args.with_exemplars)
    if args.source_format == 'bios':
        if args.sent == '__undefined__':
            raise InvalidParameterError(
                'Unspecified sentence file. For bios unmarshalling you need '
                'to specify the --sent parameter pointing at the '
                '.sentences file absolute filepath')
        annosets = biosu.unmarshall_annosets(args.source_path, args.sent)
    if args.source_format == 'rofames':
        if args.sent == '__undefined__':
            raise InvalidParameterError(
                'Unspecified sentence file. For rofames unmarshalling you '
                'need to specify the --sent parameter pointing at the '
                '.sentences file absolute filepath')
        annosets = rofamesu.unmarshall_annosets(args.source_path, args.sent)
    if args.target_format == 'bios':
        biosm.marshall_annosets_dict(annosets_dict, args.target_path,
                                     args.filter, args.output_sentences,
                                     args.excluded_frames,
                                     args.excluded_sentences,
                                     args.excluded_annosets)
    if args.target_format == 'semeval':
        if args.source_format == 'fnxml':
            splits_name = args.splits
            annosets = annosets_dict[splits_name]
            output_filepath = os.path.join(args.target_path,
                                           '{}.gold.xml'.format(splits_name))
        if args.source_format == 'bios' or args.source_format == 'rofames':
            output_filepath = args.target_path
        semeval.marshall_annosets(annosets, output_filepath,
                                  args.excluded_frames,
                                  args.excluded_sentences,
                                  args.excluded_annosets)
    if args.target_format == 'rofames':
        rofamesm.marshall_annosets_dict(annosets_dict, args.target_path,
                                        args.filter, args.output_sentences,
                                        args.excluded_frames,
                                        args.excluded_sentences,
                                        args.excluded_annosets)


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
                                choices=['rofames', 'bios', 'semeval',
                                         'fnxml'],
                                help='''Source format. Choose between:
    - rofames: the format used by the rofames fork of the semafor parser
    - bios: the BIOS format used by the open-sesame parser
    - semeval: the SEMEVAL 2008 XML format
    - fnxml: the standard FrameNet XML format
    ''')
    parser_convert.add_argument('--to', required=True,
                                dest='target_format',
                                choices=['rofames', 'bios', 'semeval',
                                         'fnxml'],
                                help='''Target format. Choose between:
    - conll: the CoNLL format used by the rofames fork of the semafor parser
    - bios: the BIOS format used by the open-sesame parser
    - semeval: the SEMEVAL 2008 XML format
    - fnxml: the standard FrameNet XML format
    ''')
    parser_convert.add_argument('--with_exemplars',
                                action='store_true', default=False,
                                help='Whether or not to use exemplars in '
                                     'splits. Default to false')
    parser_convert.add_argument('--output_sentences',
                                action='store_true', default=False,
                                help='Whether or not to output the .sentences '
                                     'files in bios or rofames marshalling')
    parser_convert.add_argument('--splits',
                                choices=['train', 'dev', 'test'],
                                default='test',
                                help='Names of FrameNet splits to be '
                                     'unmarshalled')
    parser_convert.add_argument('--sent',
                                default='__undefined__',
                                help='Absolute path to the '
                                     '{train,dev,test}.sentences file for '
                                     'BIOS unmarshalling')
    parser_convert.add_argument('--filter',
                                nargs='+',
                                default=[],
                                help='''Filtering options for the training set:
    - overlap_fes: filters out annosets with overlapping frame elements
    - disc_fes: filters out annosets with discontinuous frame elements
    - disc_targets: filters out annosets with discontinuous targets
    - no_fes: filters out annotationsets with no frame element labels
    ''')
    parser_convert.add_argument('--excluded_frames',
                                nargs='+',
                                type=int,
                                default=[],
                                help='List of frame ids to be excluded from '
                                     'unmarshalled FrameNet XML')
    parser_convert.add_argument('--excluded_sentences',
                                nargs='+',
                                type=int,
                                default=[],
                                help='List of sentence ids to be excluded '
                                     'from unmarshalled FrameNet XML')
    parser_convert.add_argument('--excluded_annosets',
                                nargs='+',
                                type=int,
                                default=[],
                                help='List of annoset ids to be excluded from '
                                     'unmarshalled FrameNet XML')
    args = parser.parse_args()
    args.func(args)
