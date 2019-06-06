"""Welcome to pyfn.

This is the entry point of the application.
"""

import os
import argparse

import logging
import logging.config

import pyfn.marshalling.marshallers.bios as biosm
import pyfn.marshalling.marshallers.hierarchy as hierm
import pyfn.marshalling.marshallers.semafor as semaform
import pyfn.marshalling.marshallers.semeval as semeval
import pyfn.marshalling.unmarshallers.bios as biosu
import pyfn.marshalling.unmarshallers.framenet as fnxml
import pyfn.marshalling.unmarshallers.semafor as semaforu

import pyfn.utils.config as config_utils
import pyfn.utils.files as futils

from pyfn.exceptions.parameter import InvalidParameterError

logging.config.dictConfig(
    config_utils.load(
        os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

logger = logging.getLogger(__name__)


def _extract_splits_name(source_path):
    return os.path.splitext(os.path.basename(source_path))[0]


def _generate(args):
    train_annosets = fnxml.get_annosets_dict(args.splits_path, 'train',
                                             args.with_exemplars)['train']
    fr_relation_xml = futils.get_fr_relation_xml_filepath(args.splits_path)
    frame_relations, fe_relations = fnxml.extract_relations(fr_relation_xml)
    hierm.marshall_relations(train_annosets, frame_relations, fe_relations,
                             args.target_path)


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
    if args.source_format == 'semafor':
        if args.sent == '__undefined__':
            raise InvalidParameterError(
                'Unspecified sentence file. For semafor unmarshalling you '
                'need to specify the --sent parameter pointing at the '
                '.sentences file absolute filepath')
        annosets = semaforu.unmarshall_annosets(args.source_path, args.sent)
    # Starting marshalling
    if args.target_format == 'bios':
        os.makedirs(args.target_path, exist_ok=True)
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
        if args.source_format == 'bios' or args.source_format == 'semafor':
            output_filepath = args.target_path
        semeval.marshall_annosets(annosets, output_filepath,
                                  args.excluded_frames,
                                  args.excluded_sentences,
                                  args.excluded_annosets)
    if args.target_format == 'semafor':
        os.makedirs(args.target_path, exist_ok=True)
        semaform.marshall_annosets_dict(annosets_dict, args.target_path,
                                        args.filter, args.output_sentences,
                                        args.excluded_frames,
                                        args.excluded_sentences,
                                        args.excluded_annosets)


def main():
    """Launch the pyfn application."""
    parser = argparse.ArgumentParser(prog='pyfn')
    subparsers = parser.add_subparsers()
    parser_generate = subparsers.add_parser(
        'generate', formatter_class=argparse.RawTextHelpFormatter,
        help='generate hierarchy files')
    parser_generate.set_defaults(func=_generate)
    parser_generate.add_argument('--source', required=True,
                                 dest='splits_path',
                                 help='absolute filepath to source dir')
    parser_generate.add_argument('--target', required=True,
                                 dest='target_path',
                                 help='absolute filepath to target dir')
    parser_generate.add_argument('--with_exemplars',
                                 action='store_true', default=False,
                                 help='whether or not to use exemplars in '
                                      'splits. Default to false')

    parser_convert = subparsers.add_parser(
        'convert', formatter_class=argparse.RawTextHelpFormatter,
        help='convert source file from given format to target file in given '
             'format')
    parser_convert.set_defaults(func=_convert)
    parser_convert.add_argument('--source', required=True,
                                dest='source_path',
                                help='absolute filepath to source dir')
    parser_convert.add_argument('--target', required=True,
                                dest='target_path',
                                help='absolute path to target dir or file.'
                                     'is dirpath if --to is semafor or bios. '
                                     'is filepath if --to is semeval')
    parser_convert.add_argument('--from', required=True,
                                dest='source_format',
                                choices=['semafor', 'bios', 'semeval',
                                         'fnxml'],
                                help='''source format. Choose between:
    - semafor: the format used by the semafor parser
    - bios: the BIOS format used by the open-sesame parser
    - semeval: the SEMEVAL 2008 XML format
    - fnxml: the standard FrameNet XML format
    ''')
    parser_convert.add_argument('--to', required=True,
                                dest='target_format',
                                choices=['semafor', 'bios', 'semeval',
                                         'fnxml'],
                                help='''target format. Choose between:
    - conll: the CoNLL format used by the semafor parser
    - bios: the BIOS format used by the open-sesame parser
    - semeval: the SEMEVAL 2008 XML format
    - fnxml: the standard FrameNet XML format
    ''')
    parser_convert.add_argument('--with_exemplars',
                                action='store_true', default=False,
                                help='whether or not to use exemplars in '
                                     'splits. Default to false')
    parser_convert.add_argument('--output_sentences',
                                action='store_true', default=False,
                                help='whether or not to output the .sentences '
                                     'files in bios or semafor marshalling')
    parser_convert.add_argument('--splits',
                                choices=['train', 'dev', 'test'],
                                default='test',
                                help='names of FrameNet splits to be '
                                     'unmarshalled')
    parser_convert.add_argument('--sent',
                                default='__undefined__',
                                help='absolute path to the '
                                     '{train,dev,test}.sentences file for '
                                     'BIOS unmarshalling')
    parser_convert.add_argument('--filter',
                                nargs='+',
                                default=[],
                                help='''filtering options for the training set:
    - overlap_fes: filter out annosets with overlapping frame elements
    - disc_fes: filter out annosets with discontinuous frame elements
    - disc_targets: filter out annosets with discontinuous targets
    - no_fes: filter out annotationsets with no frame element labels
    - non_breaking_spaces: filter out annotationsets with sentence.text
      containing non-breaking spaces
    ''')
    parser_convert.add_argument('--excluded_frames',
                                nargs='+',
                                type=int,
                                default=[],
                                help='list of frame ids to be excluded from '
                                     'unmarshalled FrameNet XML')
    parser_convert.add_argument('--excluded_sentences',
                                nargs='+',
                                type=int,
                                default=[],
                                help='list of sentence ids to be excluded '
                                     'from unmarshalled FrameNet XML')
    parser_convert.add_argument('--excluded_annosets',
                                nargs='+',
                                type=int,
                                default=[],
                                help='list of annoset ids to be excluded from '
                                     'unmarshalled FrameNet XML')
    args = parser.parse_args()
    args.func(args)
