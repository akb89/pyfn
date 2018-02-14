"""Unmarshalling BIOS tagging format to pyfn.AnnotationSet objects."""

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


def _get_end_index(token_num, tokens, text):
    return _get_start_index(token_num, tokens, text) \
        + len(tokens[token_num]) - 1


def _get_start_index(token_num, tokens, text):
    start = 0
    for token_index, token in enumerate(tokens):
        while text[start] != token[0]:
            start += 1
        if token_index == token_num:
            return start
        start += len(token)

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
                          start=_get_start_index(int(line_split[0]), tokens,
                                                 text),
                          end=_get_end_index(int(line_split[0]), tokens, text))
            labelstore.labels.append(label)
        elif line_split[14].startswith('B-'):
            label_name = line_split[14][2:]
            label = Label(name=label_name, layer=Layer(name='FE'),
                          start=_get_start_index(int(line_split[0]), tokens,
                                                 text))
            for iline in lines[lines.index(line)+1:]:
                iline_split = iline.split('\t')
                if iline_split[14].startswith('I-') and iline_split[14][2:] == label_name:
                    label.end = _get_end_index(int(iline_split[0]),
                                               tokens, text)
                    continue
                else:
                    labelstore.labels.append(label)
                    return _get_labelstore(lines[lines.index(iline):],
                                           tokens, text, labelstore)
            if label.end is None:
                print('Could not assign end index')
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
            string=tokens[token_index],
            lexunit=lexunit,
            indexes=[(_get_start_index(token_index, tokens,
                                       annoset.sentence.text),
                      _get_end_index(token_index, tokens,
                                     annoset.sentence.text))])
    else:
        if token_index - last_target_token_index > 1:
            annoset.target.indexes.append(
                (_get_start_index(token_index, tokens,
                                  annoset.sentence.text),
                 _get_end_index(token_index, tokens,
                                annoset.sentence.text)))
        else:
            annoset.target.indexes = [
                (annoset.target.indexes[
                    len(annoset.target.indexes)-1][0],
                 _get_end_index(token_index, tokens,
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


def _create_sentence(_id, text):
    return Sentence(_id=_id, text=text)


def _get_sent_dict(sent_filepath):
    sent_dict = {}
    sent_iter = 0
    with open(sent_filepath, 'r') as sent_stream:
        for line in sent_stream:
            line = line.rstrip()
            sent_dict[sent_iter] = line
            sent_iter += 1
    return sent_dict


def unmarshall_annosets(bios_filepath, sent_filepath):
    """Unmarshall a BIOS-tagged file to pyfn.AnnotationSet objects."""
    annosets = []
    sent_dict = _get_sent_dict(sent_filepath)
    with open(bios_filepath, 'r') as bios_stream:
        index = -1
        annoset_id = 0
        lines = []
        for line in bios_stream:
            line = line.rstrip()  # Careful: in gold FN data, some lines are
            # not trimmed. Ex: '_whitespace_ Simply put , Stephanopoulos did
            # as much...'
            if line != '':
                line_split = line.split('\t')
                sent_index = int(line_split[6])
                if sent_index != index:
                    sentence = _create_sentence(sent_index,
                                                sent_dict[sent_index])
                    index = sent_index
                lines.append(line)
            else:
                annoset = _create_annoset(lines, sentence, annoset_id)
                annoset_id += 1
                annosets.append(annoset)
                lines = []
    return annosets
