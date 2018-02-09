"""Constants used by pyfn."""

import os

__all__ = ['FN_XML_NAMESPACE']


FN_XML_NAMESPACE = {'fn': 'http://framenet.icsi.berkeley.edu'}

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
