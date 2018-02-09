"""Filtering utils."""

__all__ = ['filter_annosets']


def _get_concat_sentence_set(annosets):
    return {annoset.sentence.text.strip().replace(' ', '') for
            annoset in annosets}


def filter_annosets(source_annosets, target_annosets):
    """Filter annosets from source with annosets from target.

    Remove all annosets from source which contain a sentence attribute
    which concatenation is in the set of the concatenated sentences
    of target annosets
    """
    target_concat_sentence_set = _get_concat_sentence_set(target_annosets)
    for annoset in source_annosets:
        if annoset.sentence.text.strip().replace(' ', '') \
             not in target_concat_sentence_set:
            yield annoset
