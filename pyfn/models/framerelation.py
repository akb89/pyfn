"""FrameNet FrameRelation class."""

__all__ = ['FrameRelation']


class FrameRelation():
    """FrameRelation."""

    def __init__(self, _id=None, sub_frame=None, sup_frame=None, frtype=None):
        """Constructor."""
        self.__id = _id
        self._sub_frame = sub_frame
        self._sup_frame = sup_frame
        self._frtype = frtype

    @property
    def _id(self):
        return self.__id

    @property
    def sub_frame(self):
        """Return the subFrame of the FrameRelation."""
        return self._sub_frame

    @property
    def sup_frame(self):
        """Return supFrame of the FrameRelation."""
        return self._sup_frame

    @property
    def frtype(self):
        """Return the FrameRelationType of the FrameRelation."""
        return self._frtype
