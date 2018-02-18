"""Welcome to pyfn.

This is the entry point of the application.
"""

import os
import logging
import argparse

import pyfn.marshalling.marshallers.bios as biosm
import pyfn.marshalling.marshallers.semafor as semaform
import pyfn.marshalling.marshallers.semeval as semeval
import pyfn.marshalling.unmarshallers.bios as biosu
import pyfn.marshalling.unmarshallers.framenet as fnxml


from pyfn.exceptions.parameter import InvalidParameterError

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
        with_exemplars = args.with_exemplars == 'true'
        annosets_dict = fnxml.get_annosets_dict(args.source_path,
                                                args.splits,
                                                with_exemplars)
    if args.source_format == 'bios':
        logger.info('Unmarshalling data from BIOS tagging format')
        if args.sent == '__undefined__':
            raise InvalidParameterError(
                'Unspecified sentence file. For BIOS unmarshalling you need '
                'to specify the --sent parameter pointing at the '
                '.sentences file absolute filepath')
        annosets = biosu.unmarshall_annosets(args.source_path, args.sent)
    if args.source_format == 'semafor':
        pass
    if args.target_format == 'bios':
        output_sentences = args.output_sentences == 'true'
        biosm.marshall_annosets_dict(annosets_dict, args.target_path,
                                     args.filter, output_sentences)
    if args.target_format == 'semeval':
        if args.source_format == 'fnxml':
            splits_name = args.splits
            annosets = annosets_dict[splits_name]
            output_filepath = os.path.join(args.target_path,
                                           '{}.gold.xml'.format(splits_name))
        if args.source_format == 'bios':
            output_filepath = args.target_path
            print(output_filepath)
        semeval.marshall_annosets(annosets, output_filepath)
    if args.target_format == 'semafor':
        output_sentences = args.output_sentences == 'true'
        semaform.marshall_annosets_dict(annosets_dict, args.target_path,
                                        args.filter, output_sentences)


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
                                choices=['semafor', 'bios', 'semeval',
                                         'fnxml'],
                                help='''Source format. Choose between:
    - semafor: the format used by the semafor parser
    - bios: the BIOS format used by the open-sesame parser
    - semeval: the SEMEVAL 2008 XML format
    - fnxml: the standard FrameNet XML format
    ''')
    parser_convert.add_argument('--to', required=True,
                                dest='target_format',
                                choices=['semafor', 'bios', 'semeval',
                                         'fnxml'],
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
    parser_convert.add_argument('--output_sentences',
                                choices=['true', 'false'],
                                default='false',
                                help='Whether or not to output the .sentences '
                                     'files in bios or semafor marshalling')
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
    - overlap_fes: filters out all overlapping frame elements (e.g. for
    training with BIOS-tagged data which do not support overlapping fes)
    - disc_fes: filters out discontinuous frame elements
    - disc_targets: filters out discontinuous targets
    - no_fes: filters out annotationsets with no frame element layers
    ''')
    args = parser.parse_args()
    args.func(args)
