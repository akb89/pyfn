"""FrameNet Label class."""

__all__ = ['Label']


# pylint: disable=R0902
class Label():
    """FrameNet Label class."""

    # pylint: disable=R0913
    def __init__(self, name=None, layer=None, start=None, end=None, fe_id=None,
                 itype=None, fg_color=None, bg_color=None):
        """Constructor."""
        self._name = name
        self._start = start
        self._end = end
        self._layer = layer
        self._fe_id = fe_id
        self._itype = itype
        self._fg_color = fg_color
        self._bg_color = bg_color

    @property
    def name(self):
        """Return the label name."""
        return self._name

    @property
    def start(self):
        """Return the label start char index."""
        return self._start

    @property
    def end(self):
        """Return the label end char index."""
        return self._end

    @property
    def fe_id(self):
        """Return the label feID (if it is a FrameElement)."""
        return self._fe_id

    @property
    def itype(self):
        """Return the label instantiation type (if set)."""
        return self._itype

    @property
    def fg_color(self):
        """Return the label fgColor (if it is a FrameElement)."""
        return self._fg_color

    @property
    def bg_color(self):
        """Return the label bgColor (if it is a FrameElement)."""
        return self._bg_color

    @property
    def layer(self):
        """Return the label layer."""
        return self._layer

    @start.setter
    def start(self, start):
        self._start = start

    @end.setter
    def end(self, end):
        self._end = end

    @fe_id.setter
    def fe_id(self, fe_id):
        self._fe_id = fe_id

    @itype.setter
    def itype(self, itype):
        self._itype = itype

    @fg_color.setter
    def fg_color(self, fg_color):
        self._fg_color = fg_color

    @bg_color.setter
    def bg_color(self, bg_color):
        self._bg_color = bg_color

    def __str__(self):
        """Return stringified label.

        Return {name}#{layer.name}#{itype} if label is a null
        instantiation (itype).
        Return {name}#{layer.name}#{start}#{end} otherwise.
        """
        if self.itype:
            return '{}#{}#{}'.format(self.name, self.layer.name, self.itype)
        return '{}#{}#{}#{}'.format(self.name, self.layer.name, self.start,
                                    self.end)

    def __repr__(self):
        """Return stringified object."""
        return str(self)
