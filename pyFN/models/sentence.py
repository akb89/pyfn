"""FrameNet Sentence class."""

import pyFN.utils.framenet as fn_utils

__all__ = ['Sentence']


class Sentence():
    """FrameNet sentence class."""

    def __init__(self, _id, text, pnwb_labels, document=None):
        """Constructor."""
        self.__id = _id
        self._document = document
        self._text = text
        self._pnwb_labels = pnwb_labels
        self._pnw_labels_by_layer_name = fn_utils.to_labels_by_layer_name(pnwb_labels)
        self._pnw_labels_by_indexes = fn_utils.to_labels_by_indexes(pnwb_labels)

    @property
    def _id(self):
        """Return the ID of the FrameNet sentence."""
        return self.__id

    @property
    def text(self):
        """Return the text of the FramNet sentence."""
        return self._text

    @property
    def document(self):
        """Return the document object containing the FrameNet sentence."""
        return self._document

    @property
    def pnwb_labels(self):
        """Return PENN, NER, WSL and BNC labels."""
        return self._pnwb_labels

    @document.setter
    def document(self, document):
        self._document = document
