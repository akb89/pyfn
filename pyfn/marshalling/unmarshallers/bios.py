"""Unmarshalling BIOS tagging format to pyfn.AnnotationSet objects."""

import pyfn.utils.marshalling as marsh_utils

from pyfn.exceptions.parameter import InvalidParameterError

from pyfn.models.annotationset import AnnotationSet
from pyfn.models.frame import Frame
from pyfn.models.label import Label
from pyfn.models.labelstore import LabelStore
from pyfn.models.layer import Layer
from pyfn.models.lexunit import LexUnit
from pyfn.models.sentence import Sentence
from pyfn.models.target import Target

__all__ = ['unmarshall_annosets']


def _has_fe_labels(lines):
    for line in lines:
        line_split = line.split('\t')
        if line_split[14] != '_' and line_split[14] != 'O':
            return True
    return False


def _get_labelstore(lines, tokens, text, labelstore):
    # Multiple cases to handle:
    # 1. S-tag
    # 2. B-tag
    # 3. continuous I-tag (coming right after the same B or I tag)
    # 4 discontinuous I-tag (not coming after the same B or I tag)
    if not _has_fe_labels(lines):
        return labelstore
    for line in lines:
        line_split = line.split('\t')
        if line_split[14].startswith('S-'):
            label = Label(name=line_split[14][2:], layer=Layer(name='FE'),
                          start=marsh_utils.get_start_index(
                              int(line_split[0])-1, tokens, text),
                          end=marsh_utils.get_end_index(int(line_split[0])-1,
                                                        tokens, text))
            labelstore.labels.append(label)
        elif line_split[14].startswith('B-'):
            label_name = line_split[14][2:]
            label = Label(name=label_name, layer=Layer(name='FE'),
                          start=marsh_utils.get_start_index(
                              int(line_split[0])-1, tokens, text))
            for iline in lines[lines.index(line)+1:]:
                iline_split = iline.split('\t')
                if iline_split[14].startswith('I-') \
                 and iline_split[14][2:] == label_name:
                    label.end = marsh_utils.get_end_index(
                        int(iline_split[0])-1, tokens, text)
                    continue
                labelstore.labels.append(label)
                return _get_labelstore(lines[lines.index(iline):],
                                           tokens, text, labelstore)
            labelstore.labels.append(label)
            return labelstore
        elif line_split[14].startswith('I-'):
            raise InvalidParameterError(
                'Discontinuous FE annotation detected '
                'for line [{}] in sentence \'{}\'. Discontinuous FEs are not '
                'supported by pyfn for the BIOS tagging format'.format(
                    line, ' '.join(tokens)))
    return labelstore


def _update_annoset_target(annoset, tokens, token_index, lexunit,
                           last_target_token_index):
    if not annoset.target:
        annoset.target = Target(
            lexunit=lexunit,
            indexes=[(marsh_utils.get_start_index(token_index-1, tokens,
                                                  annoset.sentence.text),
                      marsh_utils.get_end_index(token_index-1, tokens,
                                                annoset.sentence.text))])
    else:
        if token_index - last_target_token_index > 1:
            annoset.target.indexes.append(
                (marsh_utils.get_start_index(token_index-1, tokens,
                                             annoset.sentence.text),
                 marsh_utils.get_end_index(token_index-1, tokens,
                                           annoset.sentence.text)))
        else:
            annoset.target.indexes = [
                (annoset.target.indexes[
                    len(annoset.target.indexes)-1][0],
                 marsh_utils.get_end_index(token_index-1, tokens,
                                           annoset.sentence.text))]


def _create_annoset(lines, sentence, annoset_id):
    annoset = AnnotationSet(_id=annoset_id, sentence=sentence)
    last_target_token_index = 0
    _tokens = [line.split('\t')[1] for line in lines]
    tokens = sentence.text.split()
    if len(tokens) != len(_tokens):
        raise InvalidParameterError('Number of tokens in sentence do not '
                                    'align between .bios and .sentences file')
    for line in lines:
        line_split = line.split('\t')
        if line_split[12] != '_':
            _update_annoset_target(annoset, tokens, int(line_split[0]),
                                   LexUnit(name=line_split[12],
                                           frame=Frame(name=line_split[13])),
                                   last_target_token_index)
            last_target_token_index = int(line_split[0])
    annoset.labelstore = _get_labelstore(lines, tokens, sentence.text,
                                         LabelStore(labels=[]))
    return annoset


def _create_sent_dict(bios_filepath):
    sent_dict = {}
    with open(bios_filepath, 'r', encoding='utf-8') as bios_stream:
        tokens = []
        sent_index = -1
        for line in bios_stream:
            line = line.strip()
            if line != '':
                tokens.append(line.split('\t')[1])
                sent_index = int(line.split('\t')[6])
            else:
                sent_dict[sent_index] = ' '.join(tokens)
                tokens = []
    return sent_dict


def unmarshall_annosets(bios_filepath, sent_filepath=None):
    """Unmarshall a BIOS-tagged file to pyfn.AnnotationSet objects.

    If the sent_filepath is specified, the sentences dict will be created
    from the .sentences file. Else, it will be created from the tokens in
    the .bios file.
    """
    annosets = []
    if sent_filepath:
        sent_dict = marsh_utils.get_sent_dict(sent_filepath)
    else:
        sent_dict = _create_sent_dict(bios_filepath)
    with open(bios_filepath, 'r', encoding='utf-8') as bios_stream:
        index = -1
        annoset_id = 0
        lines = []
        for line in bios_stream:
            line = line.strip()
            if line != '':
                line_split = line.split('\t')
                sent_index = int(line_split[6])
                if sent_index != index:
                    sentence = Sentence(_id=sent_index,
                                        text=sent_dict[sent_index])
                    index = sent_index
                lines.append(line)
            else:
                annoset = _create_annoset(lines, sentence, annoset_id)
                annoset_id += 1
                annosets.append(annoset)
                lines = []
    return annosets
