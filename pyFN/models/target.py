"""FrameNet AnnotationSet's Target class."""

__all__ = ['Target']


class Target():
    """FrameNet target class."""

    def __init__(self, string, lexunit, indexes=None, penn_tags=None,
                 similarity=None):
        """Constructor."""
        self._string = string
        self._lexunit = lexunit
        self._indexes = indexes
        self._penn_tags = penn_tags
        self._similarity = similarity

    @property
    def string(self):
        """Return the string of the FrameNet target."""
        return self._string

    @property
    def lexunit(self):
        """Return the lexunit object.

        The lexunit corresponds to the specified annotationset object.
        """
        return self._lexunit

    @property
    def indexes(self):
        """Return a list of indexes: startChar#endChar#rank."""
        return self._indexes

    @property
    def penn_tags(self):
        """Return a list of PENN tags for the given target."""
        return self._penn_tags

    @property
    def similarity(self):
        """Return the Similarity of the target to itself.

        This is used to determine the max similarity score for each similarity
        measure.
        """
        return self._similarity

    @string.setter
    def string(self, string):
        self._string = string

    @lexunit.setter
    def lexunit(self, lexunit):
        self._lexunit = lexunit

    @indexes.setter
    def indexes(self, indexes):
        self._indexes = indexes

    @penn_tags.setter
    def penn_tags(self, penn_tags):
        self._penn_tags = penn_tags

    @similarity.setter
    def similarity(self, similarity):
        self._similarity = similarity
