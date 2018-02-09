"""FrameNet Frame class."""

__all__ = ['Frame']


# pylint: disable=R0903
class Frame():
    """FrameNet Frame class."""

    def __init__(self, name, _id=None):
        """Constructor."""
        self.__id = _id
        self._name = name

    @property
    def _id(self):
        """Return the frame ID."""
        return self.__id

    @property
    def name(self):
        """Return the frame name."""
        return self._name

    @_id.setter
    def _id(self, _id):
        """Set the frame _id."""
        self.__id = _id

    @name.setter
    def name(self, name):
        """Set the frame name."""
        self._name = name
