"""Marshalling utils.

A set of functions potentially shared across marshallers.
"""

__all__ = ['marshall_sent_dict', 'get_sent_num', 'get_sent_dict',
           'get_start_index', 'get_end_index']


def marshall_sent_dict(sent_dict, sent_filepath):
    """Marshall a {pyfn.sentence.text:sentence_num} dict to stream."""
    with open(sent_filepath, 'w', encoding='utf-8') as sent_stream:
        for sent_text in sorted(sent_dict.keys()):
            print(sent_text, file=sent_stream)


def get_sent_num(text, sent_dict):
    if text not in sent_dict:
        sent_dict[text] = len(sent_dict)
    return sent_dict[text]


def get_sent_dict(sent_filepath):
    sent_dict = {}
    sent_iter = 0
    with open(sent_filepath, 'r') as sent_stream:
        for line in sent_stream:
            line = line.rstrip()
            sent_dict[sent_iter] = line
            sent_iter += 1
    return sent_dict


def get_end_index(token_num, tokens, text):
    return get_start_index(token_num, tokens, text) \
        + len(tokens[token_num]) - 1


def get_start_index(token_num, tokens, text):
    start = 0
    for token_index, token in enumerate(tokens):
        while text[start] != token[0]:
            start += 1
        if token_index == token_num:
            return start
        start += len(token)
