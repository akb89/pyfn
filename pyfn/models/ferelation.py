"""FrameNet FERelation class."""

__all__ = ['FERelation']


class FERelation():
    """FERelation."""

    def __init__(self, _id=None, sub_fe=None, sup_fe=None,
                 frame_relation=None):
        """Constructor."""
        self.__id = _id
        self._sub_fe = sub_fe
        self._sup_fe = sup_fe
        self._frame_relation = frame_relation

    @property
    def _id(self):
        return self.__id

    @property
    def sub_fe(self):
        """Return the sub FrameElement of the FERelation."""
        return self._sub_fe

    @property
    def sup_fe(self):
        """Return the sup FrameElement of the FERelation."""
        return self._sup_fe

    @property
    def frame_relation(self):
        """Return the FrameRelation of the FERelation."""
        return self._frame_relation
