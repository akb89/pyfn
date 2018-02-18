"""Marshalling utils.

A set of functions potentially shared across marshallers.
"""

__all__ = ['marshall_sent_dict', 'get_sent_num']


def marshall_sent_dict(sent_dict, sent_filepath):
    """Marshall a {pyfn.sentence.text:sentence_num} dict to stream."""
    with open(sent_filepath, 'w', encoding='utf-8') as sent_stream:
        for sent_text in sorted(sent_dict.keys()):
            print(sent_text, file=sent_stream)


def get_sent_num(text, sent_dict):
    if text not in sent_dict:
        sent_dict[text] = len(sent_dict)
    return sent_dict[text]
