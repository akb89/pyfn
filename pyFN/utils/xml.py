"""XML processing utils."""

import os

__all__ = ['extract']


def extract(directory):
    """Extract all filepaths ending with .xml from directory and return as list."""
    return [os.path.join(directory, filename) for filename in
            os.listdir(directory) if filename.endswith('.xml')]
