"""Unmarshall FrameNet XML files."""

import logging

import pyfn.utils.constants as const
from pyfn.models.annotationset import AnnotationSet
from pyfn.models.frame import Frame
from pyfn.models.label import Label
from pyfn.models.layer import Layer
from pyfn.models.lexunit import LexUnit
from pyfn.models.sentence import Sentence

__all__ = ['extract_fn_annosets']

logger = logging.getLogger(__name__)


def _create_label(label_tag, layer_tag):
    layer = Layer(layer_tag.get('name'))
    if layer_tag.get('rank'):
        layer.rank = int(layer_tag.get('rank'))
    label = Label(label_tag.get('name'), layer)
    if label_tag.get('start') is not None:
        label.start = int(label_tag.get('start'))
    else:
        label.start = -1
    if label_tag.get('end') is not None:
        label.end = int(label_tag.get('end'))
    else:
        label.end = -1
    if label_tag.get('feID') is not None:
        label.fe_id = int(label_tag.get('feID'))
    if label_tag.get('itype') is not None:
        label.itype = label_tag.get('itype')
    if label_tag.get('bgColor') is not None:
        label.bg_color = label_tag.get('bgColor')
    if label_tag.get('fgColor') is not None:
        label.fg_color = label_tag.get('fgColor')
    return label


def _extract_label_tags(layer_tag):
    label_tags = layer_tag.findall('fn:label', const.FN_XML_NAMESPACE)
    if label_tags:
        return label_tags
    labels_tags = layer_tag.findall('labels')
    if not labels_tags:
        return []
    label_tags = []
    for labels_tag in labels_tags:
        tmp_label_tags = labels_tag.findall('label')
        label_tags.extend(tmp_label_tags)
    return label_tags


def _extract_labels(layer_tags):
    if not layer_tags:
        return []
    labels = []
    for layer_tag in layer_tags:
        label_tags = _extract_label_tags(layer_tag)
        if not label_tags:
            continue
        for label_tag in label_tags:
            labels.append(_create_label(label_tag, layer_tag))
    return labels


def _extract_fn_annoset(annoset_tag, sentence, xml_schema_type, lexunit=None,
                        fe_dict=None):
    _id = int(annoset_tag.get('ID'))
    logger.debug('Processing annotationSet #{}'.format(_id))
    labels = _extract_labels(_extract_layer_tags(annoset_tag))
    if lexunit is None:  # processing a fulltext file
        frame = Frame(annoset_tag.get('frameName'))
        if annoset_tag.get('frameID'):
            frame._id = int(annoset_tag.get('frameID'))
        lexunit = LexUnit(frame)
        if annoset_tag.get('luID'):
            lexunit._id = int(annoset_tag.get('luID'))
        if annoset_tag.get('luName'):
            lexunit.name = annoset_tag.get('luName')
    return AnnotationSet.from_fn_data(_id=_id, fn_labels=labels,
                                      lexunit=lexunit, sentence=sentence,
                                      fe_dict=fe_dict,
                                      xml_schema_type=xml_schema_type)


def _extract_layer_tags(annoset_tag):
    layer_tags = annoset_tag.findall('fn:layer', const.FN_XML_NAMESPACE)
    if layer_tags:
        return layer_tags
    layers_tags = annoset_tag.findall('layers')
    if not layers_tags:
        return []
    layer_tags = []
    for layers_tag in layers_tags:
        tmp_layer_tags = layers_tag.findall('layer')
        layer_tags.extend(tmp_layer_tags)
    return layer_tags


def _has_fe_layer(annoset_tag):
    layer_tags = _extract_layer_tags(annoset_tag)
    if not layer_tags:
        return False
    for layer_tag in layer_tags:
        if layer_tag.get('name') == 'FE':
            return True
    return False


def _is_fn_annoset(annoset_tag):
    return _has_fe_layer(annoset_tag)


def _extract_fn_annosets(annoset_tags, sentence, xml_schema_type, lexunit=None,
                         fe_dict=None):
    return [_extract_fn_annoset(annoset_tag, sentence, xml_schema_type,
                                lexunit=lexunit, fe_dict=fe_dict)
            for annoset_tag in annoset_tags
            if _is_fn_annoset(annoset_tag)]


def _extract_sentence_text(sentence_tag):
    text_tag = sentence_tag.find('fn:text', const.FN_XML_NAMESPACE)
    if text_tag is not None:
        return text_tag.text
    return sentence_tag.find('text').text


def _extract_sentence(sentence_tag, pnwb_labels, document=None):
    sentence_text = _extract_sentence_text(sentence_tag)
    sentence = Sentence(text=sentence_text, _id=int(sentence_tag.get('ID')),
                        pnwb_labels=pnwb_labels)
    logger.debug('Processing sentence #{}: {}'.format(sentence._id,
                                                      sentence.text))
    if document:
        sentence.document = document
    return sentence


def _extract_pnwb_labels(annoset_tags):
    all_labels = []
    if not annoset_tags:
        return all_labels
    for annoset_tag in annoset_tags:
        layer_tags = _extract_layer_tags(annoset_tag)
        if not layer_tags:
            return all_labels
        labels = _extract_labels(layer_tags)
        if labels:
            all_labels.extend(labels)
        # TODO: replace by a list of valid layer tag name set globally
        for layer_tag in layer_tags:
            if layer_tag.get('name') == 'PENN'\
             or layer_tag.get('name') == 'NER'\
             or layer_tag.get('name') == 'WSL'\
             or layer_tag.get('name') == 'BNC':
                labels = _extract_labels(layer_tag)
                if labels:
                    all_labels.extend(labels)
    return all_labels


def _extract_annoset_tags(sentence_tag):
    annoset_tags = sentence_tag.findall('fn:annotationSet',
                                        const.FN_XML_NAMESPACE)
    if annoset_tags:
        return annoset_tags
    annosets_tags = sentence_tag.findall('annotationSets')
    if not annosets_tags:
        return []
    annoset_tags = []
    for annosets_tag in annosets_tags:
        tmp_annoset_tags = annosets_tag.findall('annotationSet')
        annoset_tags.extend(tmp_annoset_tags)
    return annoset_tags


def extract_fn_annosets(sentence_tag, xml_schema_type,
                        document=None, lexunit=None,
                        fe_dict=None):
    """Return a [AnnotationSet,...,] extracted from a single <sentence> tag."""
    annoset_tags = _extract_annoset_tags(sentence_tag)
    if not annoset_tags:
        return []
    logger.debug('Processing {} annotationSet tags'.format(len(annoset_tags)))
    pnwb_labels = _extract_pnwb_labels(annoset_tags)
    sentence = _extract_sentence(sentence_tag, pnwb_labels, document=document)
    return _extract_fn_annosets(annoset_tags, sentence, xml_schema_type,
                                lexunit=lexunit, fe_dict=fe_dict)
