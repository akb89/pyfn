"""Unmarshall fulltext XML files."""

import logging
import xml.etree.ElementTree as element_tree
import pyFN.utils.constants as const
import pyFN.marshalling.unmarshallers.framenet as fn_unmarshaller
from pyFN.models.corpus import Corpus
from pyFN.models.document import Document
from pyFN.exceptions.xml import XMLProcessingError

__all__ = ['unmarshall_fulltext_xml']

logger = logging.getLogger(__name__)


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


def unmarshall_fulltext_xml(xml_file_path, fe_dict=None):
    """Unmarshall a FrameNet fulltext XML file from file path.

    Return a generator on AnnotationSet instances extracted from the
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
    for sentence_tag in sentence_tags:
        annosets = fn_unmarshaller.extract_fn_annosets_from_sentence_tag(
            sentence_tag, document=document, fe_dict=fe_dict)
        if annosets:
            yield annosets
