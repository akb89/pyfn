"""Filtering utils."""

import re

__all__ = ['filter_annosets']


def get_text_hash(text):
    return re.sub(r'\s+', '', text.strip())


def _get_sent_hash_set(annosets):
    return {get_text_hash(annoset.sentence.text) for annoset in
            annosets}


def filter_annosets(source_annosets, target_annosets):
    """Filter annosets from source with annosets from target.

    Remove all annosets from source which contain a sentence attribute
    which text hash is in the set of the sentences hash
    of the target annosets
    """
    for annoset in source_annosets:
        if get_text_hash(annoset.sentence.text) \
         not in _get_sent_hash_set(target_annosets):
            yield annoset
        else:
            print('Found hash: {}'.format(get_text_hash(annoset.sentence.text)))
