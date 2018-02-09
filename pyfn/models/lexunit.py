"""FrameNet LexUnit class."""

__all__ = ['LexUnit']


class LexUnit():
    """FrameNet LexUnit class."""

    def __init__(self, frame, _id=None, name=None):
        """Constructor."""
        self.__id = _id
        self._name = name
        self._frame = frame

    @property
    def _id(self):
        """Return the lexunit ID."""
        return self.__id

    @property
    def name(self):
        """Return the lexunit name."""
        return self._name

    @property
    def pos(self):
        """Return the part of speech (POS) of the lexical unit."""
        if self._name is None:
            return None
        return self._name.split('.')[1]

    @property
    def frame(self):
        """Return the frame object corresponding to the lexunit."""
        return self._frame

    @_id.setter
    def _id(self, _id):
        self.__id = _id

    @name.setter
    def name(self, name):
        self._name = name
