"""XML processing utils."""

import os

__all__ = ['extract', 'get_xml_filepaths']


def extract(directory):
    """Extract all filepaths ending with .xml from directory and return as list."""
    return [os.path.join(directory, filename) for filename in
            os.listdir(directory) if filename.endswith('.xml')]


def get_xml_filepaths(splits_dirpath, subdir):
    """Return a list of fullpaths for XML files in splits_dirpath/subdir.

    The subdir parameter is either 'fulltext', either 'lu'.
    """
    dirpath = os.path.join(splits_dirpath, subdir)
    if os.path.exists(dirpath):
        return extract(dirpath)
    return []
