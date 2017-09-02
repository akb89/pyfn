"""A set of methods used to handle and process FrameNet data."""

import logging
from pyFN.models.target import Target

__all__ = ['extract_pos', 'to_target']


logger = logging.getLogger(__name__)


def extract_pos(luname):
    """Return the part of speech of the lexunit name."""
    if luname is None:
        return None
    return luname.split('.')[1]
