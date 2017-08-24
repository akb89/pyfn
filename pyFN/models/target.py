"""FrameNet AnnotationSet's Target class."""

__all__ = ['Target']


class Target():
    """FrameNet target class."""

    def __init__(self, string, lexunit, indexes=None, pos_tags=None):
        """Constructor."""
        self._string = string
        self._lexunit = lexunit
        self._indexes = indexes
        self._pos_tags = pos_tags

    @property
    def string(self):
        """Return the string of the target."""
        return self._string

    @property
    def lexunit(self):
        """Return the lexunit corresponding to the target."""
        return self._lexunit

    @property
    def indexes(self):
        """Return a list of indexe tuples (start, end)."""
        return self._indexes

    @property
    def pos_tags(self):
        """Return a list of PENN or BNC POS tags for the given target."""
        return self._pos_tags

    @string.setter
    def string(self, string):
        self._string = string

    @lexunit.setter
    def lexunit(self, lexunit):
        self._lexunit = lexunit

    @indexes.setter
    def indexes(self, indexes):
        self._indexes = indexes

    @pos_tags.setter
    def pos_tags(self, pos_tags):
        self._pos_tags = pos_tags
