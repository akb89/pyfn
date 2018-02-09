"""FrameNet Sentence class."""

from pyfn.models.labelstore import LabelStore

__all__ = ['Sentence']


class Sentence():
    """FrameNet sentence class."""

    def __init__(self, _id=None, text=None, pnwb_labels=None, document=None):
        """Constructor."""
        self.__id = _id
        self._document = document
        self._text = text
        self._sentence_number = None
        self._paraphraph_number = None  # TODO : add this and doc/corpID for lexunits
        self._pnw_labelstore = LabelStore(pnwb_labels)

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
    def pnw_labelstore(self):
        """Return a LabelStore for PENN, NER, WSL and BNC labels."""
        return self._pnw_labelstore

    @document.setter
    def document(self, document):
        self._document = document

    @text.setter
    def text(self, text):
        self._text = text
