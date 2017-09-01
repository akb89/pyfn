"""FrameNet FrameElement class."""

__all__ = ['FrameElement']


class FrameElement():
    """FrameElement."""

    def __init__(self, _id, name, coretype=None, itype=None):
        """Constructor."""
        self.__id = _id
        self._name = name
        self._coretype = coretype
        self._itype = itype

    @property
    def _id(self):
        return self.__id

    @property
    def name(self):
        return self._name

    @property
    def coretype(self):
        return self._coretype

    @property
    def itype(self):
        return self._itype

    @coretype.setter
    def coretype(self, coretype):
        self._coretype = coretype

    @itype.setter
    def itype(self, itype):
        self._itype = itype
