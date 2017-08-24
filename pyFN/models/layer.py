"""FrameNet Layer class."""

__all__ = ['Layer']


class Layer():
    """FrameNet Layer class."""

    def __init__(self, name, rank):
        """Constructor."""
        self._name = name
        self._rank = rank

    @property
    def name(self):
        """Return the lexunit name."""
        return self._name

    @property
    def rank(self):
        """Return the layer rank."""
        return self._rank
