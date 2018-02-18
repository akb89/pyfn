"""Files utils."""

import os

from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['get_bios_filepath', 'get_sent_filepath', 'get_semafor_filepath']


def get_semafor_filepath(target_dirpath, splits_name):
    if splits_name not in ['train', 'dev', 'test']:
        raise InvalidParameterError('Unsupported splits_name: {}'.format(
            splits_name))
    if splits_name == 'train':
        return os.path.join(target_dirpath, 'train.frame.elements')
    return os.path.join(target_dirpath, '{}.frames'.format(splits_name))


def get_bios_filepath(target_dirpath, splits_name):
    return os.path.join(target_dirpath, '{}.bios'.format(splits_name))


def get_sent_filepath(target_dirpath, splits_name):
    return os.path.join(target_dirpath, '{}.sentences'.format(splits_name))
