"""Marshaller to BIOS tagging scheme.

BEGINNING = B
INSIDE = I
OUTSIDE = O
SINGULAR = S
"""

__all__ = ['marshall_annosets_dict']


def marshall_annosets_dict(annosets_dict, target_dirpath):
    """Convert a dict of splits-pyfn.AnnotationSet to BIOS splits."""
    for splits_name, annosets in annosets_dict:
        pass
