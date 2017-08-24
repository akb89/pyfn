"""A set of methods used to handle and process FrameNet data."""

__all__ = ['to_labels_by_layer_name', 'to_labels_by_indexes', 'to_target',
           'to_valence_units', 'to_valence_pattern']


def to_labels_by_layer_name(labels):
    pass


def to_labels_by_indexes(labels):
    pass


def to_target(labels, lexunit):
    pass


def to_valence_units(labels_by_layer_name):
    pass


def to_valence_pattern(valence_units):
    """Convert a list of valence units to a valence pattern."""
    return ' '.join(valence_units)
