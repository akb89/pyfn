"""Unmarshall SemEval 2007 FrameNet XML files."""

import logging
import xml.etree.ElementTree as element_tree

import pyFN.unmarshallers.framenet as fn_unmarshaller

__all__ = ['unmarshall_semeval07_xml']

logger = logging.getLogger(__name__)


def unmarshall_semeval07_xml(xml_file_path):
    """Unmarshall a SemEval 2007 FrameNet XML file from file path.

    Return a generator of AnnotationSet instances extracted from the
    XML file. A single list of AnnotationSet instances corresponds
    to all the AnnotationSets of a single Sentence.

    Args
    ----
        param1 xml_files_path: full path to a SemEval 2007 FrameNet XML file.

    """
    logger.info('Unmarshalling SemEval FrameNet XML file: {}'.format(xml_file_path))
    tree = element_tree.parse(xml_file_path)
    root = tree.getroot()
    documents_tags = root.findall('documents')
    for documents_tag in documents_tags:
        document_tags = documents_tag.findall('document')
        for document_tag in document_tags:
            paragraphs_tags = document_tag.findall('paragraphs')
            for paragraphs_tag in paragraphs_tags:
                paragraph_tags = paragraphs_tag.findall('paragraph')
                for paragraph_tag in paragraph_tags:
                    sentences_tags = paragraph_tag.findall('sentences')
                    for sentences_tag in sentences_tags:
                        sentence_tags = sentences_tag.findall('sentence')
                        for sentence_tag in sentence_tags:
                            annosets = fn_unmarshaller.extract_fn_annosets_from_sentence_tag(sentence_tag)
                            if annosets:
                                yield annosets
