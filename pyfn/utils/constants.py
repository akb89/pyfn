"""Constants used by pyfn."""

import os

__all__ = ['FN_XML_NAMESPACE', 'DATA_DIR', 'SENT_LAYERS', 'ANNO_LAYERS']


FN_XML_NAMESPACE = {'fn': 'http://framenet.icsi.berkeley.edu'}

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

ANNO_LAYERS = ['FE', 'PT', 'GF', 'Target']  # layers stored in the
# annoset.labelstore
SENT_LAYERS = ['PENN', 'BNC']  # layers stored in the sentence.labelstore

HIERARCHY_RELATION_TYPES = ['Inheritance', 'SubFrame']
