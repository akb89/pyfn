"""Behavior tests for unmarshallers.framenet."""

import os

import pyFN.extraction.extractors.framenet as fn_extractor


SPLITS_DIRPATH = os.path.join(os.path.dirname(__file__), 'resources',
                              'splits')


def test_extract_annosets_with_ft_with_ex_flatten_false():
    annosets = list(fn_extractor.extract_annosets(SPLITS_DIRPATH, True,
                                                  True, flatten=False))
    assert len(annosets) == 4
    assert len([item for sublist in annosets for item in sublist]) == 10


def test_extract_annosets_with_ft_with_ex_flatten_true():
    annosets = list(fn_extractor.extract_annosets(SPLITS_DIRPATH, True,
                                                  True, flatten=True))
    assert len(annosets) == 10


def test_extract_annosets_with_ft_flatten_false():
    annosets = list(fn_extractor.extract_annosets(SPLITS_DIRPATH, True,
                                                  False, flatten=False))
    assert len(annosets) == 2
    assert len([item for sublist in annosets for item in sublist]) == 8


def test_extract_annosets_with_ft_flatten_true():
    annosets = list(fn_extractor.extract_annosets(SPLITS_DIRPATH, True,
                                                  False, flatten=True))
    assert len(annosets) == 8


def test_extract_annosets_with_ex_flatten_false():
    annosets = list(fn_extractor.extract_annosets(SPLITS_DIRPATH, False,
                                                  True, flatten=False))
    assert len(annosets) == 2
    assert len([item for sublist in annosets for item in sublist]) == 2


def test_extract_annosets_with_ex_flatten_true():
    annosets = list(fn_extractor.extract_annosets(SPLITS_DIRPATH, False,
                                                  True, flatten=True))
    assert len(annosets) == 2
