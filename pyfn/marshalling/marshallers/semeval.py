"""Marshalling to SEMEVAL format.

The format matches the XML file expected by the perl evaluation script
of the SEMEVAL 2007 shared task on frame semantic structure extraction.
"""

import os
import datetime
import pytz
import lxml.etree as etree

import pyfn.utils.filter as f_utils
import pyfn.utils.sort as sort_utils

from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['marshall_annosets']


def _marshall_annosets(annosets, output_filepath):
    if not annosets:
        raise InvalidParameterError('No input annosets to marshall. Check '
                                    'input parameters and try again.')
    root = etree.Element('corpus')
    root.set('XMLCreated', datetime.datetime.now(
        pytz.utc).strftime('%a %b %d %H:%M:%S %Z %Y'))
    documents = etree.SubElement(root, 'documents')
    document = etree.SubElement(documents, 'document')
    paragraphs = etree.SubElement(document, 'paragraphs')
    paragraph = etree.SubElement(paragraphs, 'paragraph')
    sentences = etree.SubElement(paragraph, 'sentences')
    sent_hash = ''
    sent_id = 1
    annoset_id = 1
    layer_id = 1
    label_id = 1
    for annoset in sort_utils.sort_annosets(f_utils.filter_annosets(annosets)):
        if sent_hash != f_utils.get_text_hash(annoset.sentence.text):
            sentence = etree.SubElement(sentences, 'sentence')
            sentence.set('ID', str(sent_id))
            sent_id += 1
            sent_hash = f_utils.get_text_hash(annoset.sentence.text)
            text = etree.SubElement(sentence, 'text')
            text.text = annoset.sentence.text
            annosets_tag = etree.SubElement(sentence, 'annotationSets')
        annoset_tag = etree.SubElement(annosets_tag, 'annotationSet')
        annoset_tag.set('ID', str(annoset_id))
        annoset_id += 1
        annoset_tag.set('frameName', annoset.target.lexunit.frame.name)
        layers = etree.SubElement(annoset_tag, 'layers')
        target_layer = etree.SubElement(layers, 'layer')
        target_layer.set('ID', str(layer_id))
        layer_id += 1
        target_layer.set('name', 'Target')
        target_labels = etree.SubElement(target_layer, 'labels')
        for target_index in annoset.target.indexes:
            target_label = etree.SubElement(target_labels, 'label')
            target_label.set('ID', str(label_id))
            label_id += 1
            target_label.set('start', str(target_index[0]))
            target_label.set('end', str(target_index[1]))
        fe_layer = etree.SubElement(layers, 'layer')
        fe_layer.set('ID', str(layer_id))
        layer_id += 1
        fe_layer.set('name', 'FE')
        fe_label_tags = etree.SubElement(fe_layer, 'labels')
        for fe_label in annoset.labelstore.labels_by_layer_name['FE']:
            if fe_label.start != -1 and fe_label.end != -1:
                fe_label_tag = etree.SubElement(fe_label_tags, 'label')
                fe_label_tag.set('ID', str(label_id))
                label_id += 1
                fe_label_tag.set('name', fe_label.name)
                fe_label_tag.set('start', str(fe_label.start))
                fe_label_tag.set('end', str(fe_label.end))
    tree = etree.ElementTree(root)
    tree.write(output_filepath, encoding='UTF-8', xml_declaration=True,
               pretty_print=True)


def marshall_annosets(annosets_dict, mode, output_dirpath):
    """Marshall a list of pyfn.AnnotationSet objects to SEMEVAL XML."""
    output_filepath = os.path.join(output_dirpath, '{}.gold.xml'.format(mode))
    _marshall_annosets(annosets_dict[mode], output_filepath)
