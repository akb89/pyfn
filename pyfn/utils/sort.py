"""Sorting utils."""

__all__ = ['sort_annosets']


def sort_annosets(annosets):
    """Sort a list of pyfn.AnnotationSet objects.

    Sort by annoset.sentence._id first and then by annoset._id
    """
    return sorted(annosets, key=lambda annoset: (annoset.sentence._id,
                                                 annoset._id))
