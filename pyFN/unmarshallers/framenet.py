"""Unmarshall FrameNet XML files."""

import logging
import xml.etree.ElementTree as element_tree

from pyFN.models.annotationset import AnnotationSet
from pyFN.models.corpus import Corpus
from pyFN.models.document import Document
from pyFN.models.frame import Frame
from pyFN.models.label import Label
from pyFN.models.layer import Layer
from pyFN.models.lexunit import LexUnit
from pyFN.models.sentence import Sentence

from pyFN.exceptions.xml import XMLProcessingError

import pyFN.utils.constants as const

__all__ = ['unmarshall_fulltext_xml', 'unmarshall_lexunit_xml']

logger = logging.getLogger(__name__)


def _create_label(label_tag, layer_tag):
    layer = Layer(layer_tag.get('name'), int(layer_tag.get('rank')))
    label = Label(label_tag.get('name'), layer)
    if label_tag.get('start') is not None:
        label.start = int(label_tag.get('start'))
    if label_tag.get('end') is not None:
        label.end = int(label_tag.get('end'))
    if label_tag.get('feID') is not None:
        label.fe_id = int(label_tag.get('feID'))
    if label_tag.get('itype') is not None:
        label.itype = label_tag.get('itype')
    if label_tag.get('bgColor') is not None:
        label.bg_color = label_tag.get('bgColor')
    if label_tag.get('fgColor') is not None:
        label.fg_color = label_tag.get('fgColor')
    return label


def _extract_labels(layer_tags):
    labels = []
    if not layer_tags:
        return labels
    for layer_tag in layer_tags:
        label_tags = layer_tag.findall('fn:label', const.FN_XML_NAMESPACE)
        if not label_tags:
            continue
        for label_tag in label_tags:
            labels.append(_create_label(label_tag, layer_tag))
    return labels


def _extract_fn_annoset(annoset_tag, sentence, lexunit=None):
    _id = int(annoset_tag.get('ID'))
    logger.debug('Processing annotationSet #{}'.format(_id))
    labels = _extract_labels(annoset_tag.findall('fn:layer',
                                                 const.FN_XML_NAMESPACE))
    if lexunit is None:  # processing a fulltext file
        frame = Frame(int(annoset_tag.get('frameID')),
                      annoset_tag.get('frameName'))
        lexunit = LexUnit(int(annoset_tag.get('luID')),
                          annoset_tag.get('luName'), frame)
    return AnnotationSet(_id, labels, lexunit, sentence)


def _has_fe_layer(annoset_tag):
    layer_tags = annoset_tag.findall('fn:layer', const.FN_XML_NAMESPACE)
    if not layer_tags:
        return False
    for layer_tag in layer_tags:
        if layer_tag.get('name') == 'FE':
            return True
    return False


def _is_fn_annoset(annoset_tag):
    return _has_fe_layer(annoset_tag)


def _extract_fn_annosets(annoset_tags, sentence, lexunit=None):
    return [_extract_fn_annoset(annoset_tag, sentence, lexunit=lexunit) for
            annoset_tag in annoset_tags if _is_fn_annoset(annoset_tag)]


def _extract_sentence(sentence_tag, pnw_labels, document=None):
    text_tag = sentence_tag.find('fn:text', const.FN_XML_NAMESPACE)
    sentence = Sentence(int(sentence_tag.get('ID')), text_tag.text, pnw_labels)
    logger.debug('Processing sentence #{}: {}'.format(sentence._id, sentence.text))
    if document:
        sentence.document = document
    return sentence


def _extract_pnw_labels(annoset_tags):
    all_labels = []
    if not annoset_tags:
        return all_labels
    for annoset_tag in annoset_tags:
        layer_tags = annoset_tag.findall('fn:layer', const.FN_XML_NAMESPACE)
        if not layer_tags:
            return all_labels
        labels = _extract_labels(layer_tags)
        if labels:
            all_labels.extend(labels)
        for layer_tag in layer_tags:
            if layer_tag.get('name') == 'PENN'\
             or layer_tag.get('name') == 'NER'\
             or layer_tag.get('name') == 'WSL'\
             or layer_tag.get('name') == 'BNC':
                labels = _extract_labels(layer_tag)
                if labels:
                    all_labels.extend(labels)
    return all_labels


def _extract_fn_annosets_from_sentence_tags(sentence_tag, document=None,
                                            lexunit=None):
    """Return a List<AnnotationSet> extracted from a single <sentence> tag."""
    annoset_tags = sentence_tag.findall('fn:annotationSet',
                                        const.FN_XML_NAMESPACE)
    if not annoset_tags:
        return []
    logger.debug('Processing {} annotationSet tags'.format(len(annoset_tags)))
    pnw_labels = _extract_pnw_labels(annoset_tags)
    sentence = _extract_sentence(sentence_tag, pnw_labels, document=document)
    return _extract_fn_annosets(annoset_tags, sentence, lexunit=lexunit)


def _extract_annosets_from_sentence_tags(sentence_tags, document=None,
                                         lexunit=None):
    annosets_list = []
    if not sentence_tags:
        return annosets_list
    for sentence_tag in sentence_tags:
        annosets = _extract_fn_annosets_from_sentence_tags(sentence_tag,
                                                           document=document,
                                                           lexunit=lexunit)
        if annosets:
            annosets_list.append(annosets)
    return annosets_list


def _extract_document(header_tag):
    """Return a Document instance from a fulltext <header> tag."""
    corpus_tag = header_tag.find('fn:corpus', const.FN_XML_NAMESPACE)
    corpus = Corpus(int(corpus_tag.get('ID')), corpus_tag.get('name'))
    document_tag = corpus_tag.find('fn:document', const.FN_XML_NAMESPACE)
    if document_tag is None:
        raise XMLProcessingError('Could not extract document from tag')
    return Document(int(document_tag.get('ID')),
                    '{}__{}'.format(corpus.name,
                                    document_tag.get('description')),
                    document_tag.get('description'),
                    corpus)


def unmarshall_lexunit_xml(xml_file_path):
    """Unmarshall a FrameNet lu XML file from file path.

    Return a list of list of AnnotationSet instances extracted from the
    lu XML file. A single list of AnnotationSet instances corresponds
    to all the AnnotationSets of a single Sentence.

    Args
    ----
        param1 xml_files_path: full path to a FrameNet lu XML file.

    """
    logger.info('Unmarshalling FrameNet lu XML file: {}'.format(xml_file_path))
    tree = element_tree.parse(xml_file_path)
    root = tree.getroot()
    frame = Frame(int(root.get('frameID')), root.get('frame'))
    lexunit = LexUnit(int(root.get('ID')), root.get('name'), frame)
    subcorpus_tags = root.findall('fn:subCorpus', const.FN_XML_NAMESPACE)
    if not subcorpus_tags:
        return []
    full_annosets_list = []
    for subcorpus_tag in subcorpus_tags:
        sentence_tags = subcorpus_tag.findall('fn:sentence',
                                              const.FN_XML_NAMESPACE)
        annosets_list = _extract_annosets_from_sentence_tags(sentence_tags,
                                                             lexunit=lexunit)
        if annosets_list:
            full_annosets_list.extend(annosets_list)
    return full_annosets_list


def unmarshall_fulltext_xml(xml_file_path):
    """Unmarshall a FrameNet fulltext XML file from file path.

    Return a list of list of AnnotationSet instances extracted from the
    fulltext XML file. A single list of AnnotationSet instances corresponds
    to all the AnnotationSets of a single Sentence.

    Args
    ----
        param1 xml_files_path: full path to a FrameNet fulltext XML file.

    """
    logger.info('Unmarshalling FrameNet fulltext XML file: {}'.format(xml_file_path))
    tree = element_tree.parse(xml_file_path)
    root = tree.getroot()
    try:
        document = _extract_document(root.find('fn:header',
                                               const.FN_XML_NAMESPACE))
    except XMLProcessingError as err:
        raise XMLProcessingError('Could not process XML file: {}. Cause: {}'
                                 .format(xml_file_path, str(err)))
    sentence_tags = root.findall('fn:sentence', const.FN_XML_NAMESPACE)
    return _extract_annosets_from_sentence_tags(sentence_tags,
                                                document=document)
