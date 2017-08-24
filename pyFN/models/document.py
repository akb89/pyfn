"""FrameNet Document object class."""

__all__ = ['Document']


class Document():
    """FrameNet Document class."""

    def __init__(self, _id, name, description, corpus):
        """Constructor."""
        self.__id = _id
        self._name = name
        self._description = description
        self._corpus = corpus

    @property
    def _id(self):
        """Return the ID of the FrameNet document."""
        return self.__id

    @property
    def name(self):
        """Return the name of the FrameNet document."""
        return self._name

    @property
    def description(self):
        """Return the description of the FrameNet document."""
        return self._description

    @property
    def corpus(self):
        """Return the FrameNet corpus of the FrameNet document."""
        return self._corpus
