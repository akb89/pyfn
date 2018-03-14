"""FrameNet FrameRelationType class."""

__all__ = ['FrameRelationType']


class FrameRelationType():
    """FrameRelationType."""

    def __init__(self, _id=None, name=None, sub_frame_name=None,
                 sup_frame_name=None):
        """Constructor."""
        self.__id = _id
        self._name = name
        self._sub_frame_name = sub_frame_name
        self._sup_frame_name = sup_frame_name

    @property
    def _id(self):
        return self.__id

    @property
    def name(self):
        """Return the name of the FrameRelationType."""
        return self._name

    @property
    def sub_frame_name(self):
        """Return the subFrameName of the FrameRelationType."""
        return self._sub_frame_name

    @property
    def sup_frame_name(self):
        """Return supFrameName of the FrameRelationType."""
        return self._sup_frame_name
