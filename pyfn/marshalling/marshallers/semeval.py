"""Marshalling to SEMEVAL format.

The format matches the XML file expected by the perl evaluation script
of the SEMEVAL 2007 shared task on frame semantic structure extraction.
"""

import datetime
import logging
import pytz
import lxml.etree as etree

import pyfn.utils.filter as f_utils

from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['marshall_annosets']

logger = logging.getLogger(__name__)


# pylint: disable-msg=R0914
def _add_fe_labels(layers_tag, layer_id, annoset, label_id):
    fe_layer = etree.SubElement(layers_tag, 'layer')
    fe_layer.set('ID', str(layer_id))
    fe_layer.set('name', 'FE')
    fe_label_tags = etree.SubElement(fe_layer, 'labels')
    if 'FE' in annoset.labelstore.labels_by_layer_name:
        for fe_label in annoset.labelstore.labels_by_layer_name['FE']:
            if fe_label.start != -1 and fe_label.end != -1:
                fe_label_tag = etree.SubElement(fe_label_tags, 'label')
                fe_label_tag.set('ID', str(label_id))
                label_id += 1
                fe_label_tag.set('name', fe_label.name)
                fe_label_tag.set('start', str(fe_label.start))
                fe_label_tag.set('end', str(fe_label.end))
    return label_id


def _has_fe_labels(annoset):
    return 'FE' in annoset.labelstore.labels_by_layer_name


def _add_target_labels(layers_tag, layer_id, annoset, label_id):
    target_layer = etree.SubElement(layers_tag, 'layer')
    target_layer.set('ID', str(layer_id))
    target_layer.set('name', 'Target')
    target_labels = etree.SubElement(target_layer, 'labels')
    for target_index in annoset.target.indexes:
        target_label = etree.SubElement(target_labels, 'label')
        target_label.set('ID', str(label_id))
        target_label.set('name', 'Target')
        label_id += 1
        target_label.set('start', str(target_index[0]))
        target_label.set('end', str(target_index[1]))
    return label_id


def _get_annoset_tag(annosets_tag, annoset, annoset_id):
    annoset_tag = etree.SubElement(annosets_tag, 'annotationSet')
    annoset_tag.set('ID', str(annoset_id))
    annoset_tag.set('frameName', annoset.target.lexunit.frame.name)
    return annoset_tag


def _get_sentence_tag(annoset, sentences_tag, sent_id):
    sentence_tag = etree.SubElement(sentences_tag, 'sentence')
    sentence_tag.set('ID', str(sent_id))
    text = etree.SubElement(sentence_tag, 'text')
    text.text = annoset.sentence.text
    return sentence_tag


def _marshall_annosets(annosets, output_filepath, excluded_frames,
                       excluded_sentences, excluded_annosets):
    if not annosets:
        raise InvalidParameterError('No input annosets to marshall. Check '
                                    'input parameters and try again.')
    root = etree.Element('corpus')
    root.set('XMLCreated', datetime.datetime.now(
        pytz.utc).strftime('%a %b %d %H:%M:%S %Z %Y'))
    documents_tag = etree.SubElement(root, 'documents')
    document_tag = etree.SubElement(documents_tag, 'document')
    paragraphs_tag = etree.SubElement(document_tag, 'paragraphs')
    paragraph_tag = etree.SubElement(paragraphs_tag, 'paragraph')
    sentences_tag = etree.SubElement(paragraph_tag, 'sentences')
    sent_text = ''
    sent_id = 0  # to match the semval numbering of sentences
    annoset_id = 1
    layer_id = 1
    label_id = 1
    for annoset in f_utils.filter_and_sort_annosets(annosets, [],
                                                    excluded_frames,
                                                    excluded_sentences,
                                                    excluded_annosets):
        if annoset.sentence.text != sent_text:
            sentence = _get_sentence_tag(annoset, sentences_tag, sent_id)
            sent_id += 1
            sent_text = annoset.sentence.text
            annosets_tag = etree.SubElement(sentence, 'annotationSets')
        annoset_tag = _get_annoset_tag(annosets_tag, annoset, annoset_id)
        annoset_id += 1
        layers_tag = etree.SubElement(annoset_tag, 'layers')
        label_id = _add_target_labels(layers_tag, layer_id, annoset, label_id)
        layer_id += 1
        if _has_fe_labels(annoset):
            label_id = _add_fe_labels(layers_tag, layer_id, annoset, label_id)
            layer_id += 1
    tree = etree.ElementTree(root)
    tree.write(output_filepath, encoding='UTF-8', xml_declaration=True,
               pretty_print=True)


def marshall_annosets(annosets, output_filepath, excluded_frames,
                      excluded_sentences, excluded_annosets):
    """Marshall a list of pyfn.AnnotationSet objects to SEMEVAL XML.

    annosets: a list of annosets to marshall.
    output_filepath: the absolute path to the output .xml file
    excluded_frames: a list of frame #id to exclude from the output
    excluded_sentences: a list of sentence #id to exclude from the output
    excluded_annosets: a list of annotationset #id to exclude from the output
    """
    logger.info('Marshalling pyfn.AnnotationSet objects to SEMEVAL XML...')
    if not annosets:
        raise InvalidParameterError('Input pyfn.AnnotationSet list is empty')
    logger.info('Saving output to {}'.format(output_filepath))
    _marshall_annosets(annosets, output_filepath, excluded_frames,
                       excluded_sentences, excluded_annosets)
