"""FrameNet Corpus object class."""

__all__ = ['Corpus']


class Corpus():
    """FrameNet Corpus class."""

    def __init__(self, _id, name):
        """Constructor."""
        self.__id = _id
        self._name = name

    @property
    def _id(self):
        """Return the ID of the FrameNet corpus."""
        return self.__id

    @property
    def name(self):
        """Return the name of the FrameNet corpus."""
        return self._name
