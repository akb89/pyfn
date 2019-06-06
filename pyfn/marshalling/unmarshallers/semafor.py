"""Unmarshall SEMAFOR .frame.elements files."""

import pyfn.utils.marshalling as marsh_utils

from pyfn.models.annotationset import AnnotationSet
from pyfn.models.frame import Frame
from pyfn.models.label import Label
from pyfn.models.labelstore import LabelStore
from pyfn.models.layer import Layer
from pyfn.models.lexunit import LexUnit
from pyfn.models.sentence import Sentence
from pyfn.models.target import Target


__all__ = ['unmarshall_annosets']


def _get_labelstore(line_split, text):
    labels = []
    if len(line_split) <= 8:
        return LabelStore(labels=[])
    for index, item in enumerate(line_split[8:]):
        if index % 2 == 0:
            label = Label(name=item, layer=Layer(name='FE'))
        else:
            start_token = _get_start_token(line_split[8:][index])
            end_token = _get_end_token(line_split[8:][index])
            label.start = marsh_utils.get_start_index(
                start_token, text.split(), text)
            label.end = marsh_utils.get_end_index(
                end_token, text.split(), text)
            labels.append(label)
    return LabelStore(labels=labels)


def _get_target(start_token, end_token, luname, framename, text):
    lexunit = LexUnit(frame=Frame(name=framename), name=luname)
    if end_token - start_token < 2:
        indexes = [(marsh_utils.get_start_index(start_token, text.split(),
                                                text),
                    marsh_utils.get_end_index(end_token, text.split(), text))]
    else:
        indexes = [(marsh_utils.get_start_index(start_token, text.split(),
                                                text),
                    marsh_utils.get_end_index(start_token, text.split(),
                                              text)),
                   (marsh_utils.get_start_index(end_token, text.split(),
                                                text),
                    marsh_utils.get_end_index(end_token, text.split(),
                                              text))]
    return Target(lexunit=lexunit, indexes=indexes)


def _get_end_token(token_indexes):
    if '_' in token_indexes:
        return int(token_indexes.split('_')[1])
    if ':' in token_indexes:
        return int(token_indexes.split(':')[1])
    return int(token_indexes)


def _get_start_token(token_indexes):
    if '_' in token_indexes:
        return int(token_indexes.split('_')[0])
    if ':' in token_indexes:
        return int(token_indexes.split(':')[0])
    return int(token_indexes)


def unmarshall_annosets(semafor_filepath, sent_filepath):
    """Unmarshall a semafor .frame.elements file to pyfn.AnnotationSets."""
    annosets = []
    sent_dict = marsh_utils.get_sent_dict(sent_filepath)
    with open(semafor_filepath, 'r', encoding='utf-8') as semafor_stream:
        for line in semafor_stream:
            line = line.strip()
            line_split = line.split('\t')
            sent_index = int(line_split[7])
            sentence = Sentence(_id=sent_index,
                                text=sent_dict[sent_index])
            target = _get_target(_get_start_token(line_split[5]),
                                 _get_end_token(line_split[5]),
                                 line_split[4],
                                 line_split[3],
                                 sent_dict[sent_index])
            labelstore = _get_labelstore(line_split, sent_dict[sent_index])
            annoset = AnnotationSet(sentence=sentence, target=target,
                                    labelstore=labelstore)
            annosets.append(annoset)
    return annosets
