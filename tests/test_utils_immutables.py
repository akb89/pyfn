"""Tests for utils.immutables."""

import pytest

from pyfn.utils.immutables import FrozenDict
from pyfn.utils.immutables import ImmutableConfig

from pyfn.exceptions.method import InvalidMethodError
from pyfn.exceptions.parameter import InvalidParameterError


def test_frozen_dict():
    """Test that assigning a value to a frozen dict raises an
    InvalidMethodError."""
    mutable_dict = {'key': 'I can assign a value to a mutable dict'}
    assert mutable_dict['key'] == 'I can assign a value to a mutable dict'
    frozen_dict = FrozenDict(mutable_dict)
    with pytest.raises(InvalidMethodError, message='Cannot assign value to a\
                                                    FrozenDict'):
        frozen_dict['key'] = 'Raise an error as a frozen dict is immutable'


def test_immutable_config_exception_string():
    """Test that passing a string to ImmutableConfig raises an
    InvalidParameterError.
    """
    dict_config = {'key': 'value'}
    ImmutableConfig(dict_config)
    string_config = 'key: value'
    with pytest.raises(InvalidParameterError, message='ImmutableConfig requires\
                                                    an instance of a dict as\
                                                    input parameter'):
        ImmutableConfig(string_config)


def test_immutable_config_exception_list():
    """Test that passing a list to ImmutableConfig raises an
    InvalidParameterError.
    """
    dict_config = {'key': 'value'}
    ImmutableConfig(dict_config)
    list_config = ['key', 'value']
    with pytest.raises(InvalidParameterError, message='ImmutableConfig requires\
                                                    an instance of a dict as\
                                                    input parameter'):
        ImmutableConfig(list_config)


def test_immutable_config():
    """Test that ImmutableConfig returns a FrozenDict (of FrozenDict(s))."""
    mutable_config = {'key1': {'key2': {'key3': 'value1'}}, 'key4': 'value2'}
    immutable_config = ImmutableConfig(mutable_config)
    print(immutable_config)
    assert _contains_only_frozen_dict(immutable_config)


def _contains_only_frozen_dict(input_dict):
    if not isinstance(input_dict, FrozenDict):
        return False
    results = []
    for key in input_dict:
        value = input_dict[key]
        if isinstance(value, dict):
            results.append(_contains_only_frozen_dict(value))
    return False if False in results else True
