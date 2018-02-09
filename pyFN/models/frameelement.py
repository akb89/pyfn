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
        """Return FrameElement name."""
        return self._name

    @property
    def coretype(self):
        """Return FrameElement core type.

        Core Types include: 'Core', 'Core-Unexpressed', 'Peripheral' or
        'Extra-Thematic'. See FrameNet book for details.
        """
        return self._coretype

    @property
    def itype(self):
        """Return FrameElement instantiation type.

        itypes include 'INI', 'CNI' and 'DNI'. Seee FrameNet book for details.
        """
        return self._itype

    @coretype.setter
    def coretype(self, coretype):
        self._coretype = coretype

    @itype.setter
    def itype(self, itype):
        self._itype = itype
