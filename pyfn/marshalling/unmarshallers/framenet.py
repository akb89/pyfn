"""Unmarshall FrameNet XML files."""

import os
import itertools
import logging

import xml.etree.ElementTree as etree

import pyfn.utils.constants as const
import pyfn.utils.filter as f_utils
import pyfn.utils.xml as xml_utils

from pyfn.exceptions.xml import XMLProcessingError

from pyfn.models.annotationset import AnnotationSet
from pyfn.models.corpus import Corpus
from pyfn.models.document import Document
from pyfn.models.frame import Frame
from pyfn.models.label import Label
from pyfn.models.layer import Layer
from pyfn.models.lexunit import LexUnit
from pyfn.models.sentence import Sentence

__all__ = ['extract_annosets', 'get_annosets_dict', 'extract_fn_annosets']

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
    # For FrameNet XML format
    label_tags = layer_tag.findall('fn:label', const.FN_XML_NAMESPACE)
    if label_tags:
        return label_tags
    # For SEMEVAL XML format
    labels_tags = layer_tag.findall('labels')
    if not labels_tags:
        return []
    label_tags = []
    for labels_tag in labels_tags:
        tmp_label_tags = labels_tag.findall('label')
        label_tags.extend(tmp_label_tags)
    return label_tags


def _extract_labels(layer_tags, layer_names):
    if not layer_tags:
        return []
    labels = []
    for layer_tag in layer_tags:
        if layer_tag.get('name') in layer_names:
            label_tags = _extract_label_tags(layer_tag)
            if not label_tags:
                continue
            for label_tag in label_tags:
                labels.append(_create_label(label_tag, layer_tag))
    return labels


def _extract_fn_annoset(annoset_tag, sentence, xml_schema_type,
                        annoset_layer_names, lexunit=None, fe_dict=None):
    _id = int(annoset_tag.get('ID'))
    logger.debug('Processing annotationSet #{}'.format(_id))
    labels = _extract_labels(_extract_layer_tags(annoset_tag),
                             annoset_layer_names)
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
    # For FrameNet XML format
    layer_tags = annoset_tag.findall('fn:layer', const.FN_XML_NAMESPACE)
    if layer_tags:
        return layer_tags
    # For SEMEVAL XML format
    layers_tags = annoset_tag.findall('layers')
    if not layers_tags:
        return []
    layer_tags = []
    for layers_tag in layers_tags:
        tmp_layer_tags = layers_tag.findall('layer')
        layer_tags.extend(tmp_layer_tags)
    return layer_tags


def _has_target_layer(annoset_tag):
    layer_tags = _extract_layer_tags(annoset_tag)
    if not layer_tags:
        return False
    for layer_tag in layer_tags:
        if layer_tag.get('name') == 'Target':
            label_tags = _extract_label_tags(layer_tag)
            if not label_tags:
                return False  # has a Target layer but no labels
            for label_tag in label_tags:
                if label_tag.get('start') is None or label_tag.get('end') is None:
                    return False
            return True
    return False


def _is_fn_annoset(annoset_tag):
    return _has_target_layer(annoset_tag)


def _extract_fn_annosets(annoset_tags, sentence, xml_schema_type,
                         annoset_layer_names, lexunit=None,
                         fe_dict=None):
    return [_extract_fn_annoset(annoset_tag, sentence, xml_schema_type,
                                annoset_layer_names,
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


def _extract_sent_labels(annoset_tags, layer_names):
    all_labels = []
    for annoset_tag in annoset_tags:
        layer_tags = _extract_layer_tags(annoset_tag)
        all_labels.extend(_extract_labels(layer_tags, layer_names))
    return all_labels


def _extract_annoset_tags(sentence_tag):
    # For FrameNet XML format
    annoset_tags = sentence_tag.findall('fn:annotationSet',
                                        const.FN_XML_NAMESPACE)
    if annoset_tags:
        return annoset_tags
    # For SEMEVAL XML format
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
    pnwb_labels = _extract_sent_labels(annoset_tags, const.SENT_LAYERS)
    sentence = _extract_sentence(sentence_tag, pnwb_labels, document=document)
    return _extract_fn_annosets(annoset_tags, sentence, xml_schema_type,
                                const.ANNO_LAYERS,
                                lexunit=lexunit, fe_dict=fe_dict)


def _filter_annosets_dict(annosets_dict):
    # At least test and train, dev is optional
    filtered_annosets_dict = {}
    test_annosets, _test_annosets, __test_annosets = itertools.tee(
        annosets_dict['test'], 3)
    filtered_annosets_dict['test'] = test_annosets
    if annosets_dict['dev']:
        filtered_dev_annosets = f_utils.left_difference(
            annosets_dict['dev'], _test_annosets)
        dev_annosets, _dev_annosets = itertools.tee(filtered_dev_annosets)
        filtered_annosets_dict['dev'] = dev_annosets
        filtered_annosets_dict['train'] = f_utils.left_difference(
            annosets_dict['train'], itertools.chain(_dev_annosets,
                                                    __test_annosets))
    else:
        filtered_annosets_dict['train'] = f_utils.left_difference(
            annosets_dict['train'], _test_annosets)
    return filtered_annosets_dict


def _get_annosets_dict_from_fn_xml(fn_splits_dirpath, splits, with_exemplars):
    if splits == 'test':
        return {'test': extract_annosets(os.path.join(fn_splits_dirpath,
                                                      'test'),
                                         with_fulltexts=True,
                                         with_exemplars=with_exemplars,
                                         flatten=True),
                'dev': [], 'train': []}
    if splits == 'dev':
        return {'test': extract_annosets(os.path.join(fn_splits_dirpath,
                                                      'test'),
                                         with_fulltexts=True,
                                         with_exemplars=with_exemplars,
                                         flatten=True),
                'dev': extract_annosets(os.path.join(fn_splits_dirpath,
                                                     'dev'),
                                        with_fulltexts=True,
                                        with_exemplars=with_exemplars,
                                        flatten=True),
                'train': []}
    if splits == 'train':
        return {'test': extract_annosets(os.path.join(fn_splits_dirpath,
                                                      'test'),
                                         with_fulltexts=True,
                                         with_exemplars=with_exemplars,
                                         flatten=True),
                'dev': extract_annosets(os.path.join(fn_splits_dirpath,
                                                     'dev'),
                                        with_fulltexts=True,
                                        with_exemplars=with_exemplars,
                                        flatten=True),
                'train': extract_annosets(os.path.join(fn_splits_dirpath,
                                                       'train'),
                                          with_fulltexts=True,
                                          with_exemplars=with_exemplars,
                                          flatten=True)}
    return {}


def get_annosets_dict(source_path, splits, with_exemplars):
    """Return a string to AnnotationSet generator dict.

    Keys are splits name (train, dev, test) and values are generators
    on AnnotationSet objects.
    """
    logger.info('Creating pyfn.AnnotationSet dict from {}'.format(source_path))
    return _filter_annosets_dict(
        _get_annosets_dict_from_fn_xml(source_path, splits, with_exemplars))


def _unmarshall_exemplar_xml(xml_file_path, fe_dict=None, flatten=False):
    """Unmarshall a FrameNet lu XML file from file path.

    Return a generator over a list of AnnotationSet instances extracted
    from the lu XML file. A single list of AnnotationSet instances corresponds
    to all the AnnotationSets of a single Sentence.

    Args
    ----
        param1 xml_files_path: full path to a FrameNet lu XML file.

    """
    logger.info('Unmarshalling FrameNet lu XML file: {}'.format(xml_file_path))
    tree = etree.parse(xml_file_path)
    root = tree.getroot()
    frame = Frame(root.get('frame'), _id=int(root.get('frameID')))
    lexunit = LexUnit(frame, _id=int(root.get('ID')), name=root.get('name'))
    subcorpus_tags = root.findall('fn:subCorpus', const.FN_XML_NAMESPACE)
    for subcorpus_tag in subcorpus_tags:
        sentence_tags = subcorpus_tag.findall('fn:sentence',
                                              const.FN_XML_NAMESPACE)
        for sentence_tag in sentence_tags:
            annosets = extract_fn_annosets(
                sentence_tag, xml_schema_type='exemplar', lexunit=lexunit,
                fe_dict=fe_dict)
            if annosets:
                if not flatten:
                    yield annosets
                if flatten:
                    for annoset in annosets:
                        yield annoset


def _extract_document(header_tag):
    """Return a Document instance from a fulltext <header> tag."""
    corpus_tag = header_tag.find('fn:corpus', const.FN_XML_NAMESPACE)
    corpus = Corpus(int(corpus_tag.get('ID')), corpus_tag.get('name'),
                    corpus_tag.get('description'))
    document_tag = corpus_tag.find('fn:document', const.FN_XML_NAMESPACE)
    if document_tag is None:
        raise XMLProcessingError('Could not extract document from tag')
    return Document(int(document_tag.get('ID')),
                    document_tag.get('name'),
                    document_tag.get('description'),
                    corpus)


def _unmarshall_fulltext_xml(xml_file_path, fe_dict=None, flatten=False):
    """Unmarshall a FrameNet fulltext XML file from file path.

    Return a generator on AnnotationSet instances extracted from the
    fulltext XML file. A single list of AnnotationSet instances corresponds
    to all the AnnotationSets of a single Sentence.

    Args
    ----
        param1 xml_files_path: full path to a FrameNet fulltext XML file.

    """
    logger.info('Unmarshalling FrameNet fulltext XML file: {}'.format(
        xml_file_path))
    tree = etree.parse(xml_file_path)
    root = tree.getroot()
    try:
        document = _extract_document(root.find('fn:header',
                                               const.FN_XML_NAMESPACE))
    except XMLProcessingError as err:
        raise XMLProcessingError('Could not process XML file: {}. Cause: {}'
                                 .format(xml_file_path, str(err)))
    sentence_tags = root.findall('fn:sentence', const.FN_XML_NAMESPACE)
    for sentence_tag in sentence_tags:
        annosets = extract_fn_annosets(
            sentence_tag, xml_schema_type='fulltext', document=document,
            fe_dict=fe_dict)
        if annosets:
            if not flatten:
                yield annosets
            if flatten:
                for annoset in annosets:
                    yield annoset


def _extract_ex_annosets(ex_filepaths, fe_dict=None, flatten=False):
    generators = []
    for exemplar_filepath in ex_filepaths:
        generators.append(_unmarshall_exemplar_xml(
            exemplar_filepath, fe_dict, flatten))
    return generators


def _extract_ft_annosets(ft_filepaths, fe_dict=None, flatten=False):
    generators = []
    for fulltext_filepath in ft_filepaths:
        generators.append(_unmarshall_fulltext_xml(
            fulltext_filepath, fe_dict, flatten))
    return generators


def extract_annosets(splits_dirpath, with_fulltexts, with_exemplars,
                     fe_dict=None, flatten=False):
    """Return a list of pyfn.AnnotationSet extracted from splits paths.

    The splits directory should contain two subdirectories name 'fulltext'
    and 'lu'.
    Returns a list of generators over AnnotationSet with [AnnotationSet] <->
    1 fulltext or exemplar XML file if flatten==False
    Returns a generator over AnnotationSet (a single list) if flatten==True
    """
    logger.info('Extracting pyfn.AnnotationSet items from {}'
                .format(splits_dirpath))
    ft_annosets = []
    ex_annosets = []
    if with_fulltexts:
        ft_filepaths = xml_utils.get_xml_filepaths(splits_dirpath,
                                                   'fulltext')
        ft_annosets = _extract_ft_annosets(ft_filepaths, fe_dict, flatten)
    if with_exemplars:
        ex_filepaths = xml_utils.get_xml_filepaths(splits_dirpath,
                                                   'lu')
        ex_annosets = _extract_ex_annosets(ex_filepaths, fe_dict, flatten)
    return itertools.chain(*ft_annosets, *ex_annosets)
