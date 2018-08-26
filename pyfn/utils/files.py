"""Files utils."""

import os

from pyfn.exceptions.parameter import InvalidParameterError

__all__ = ['get_bios_filepath', 'get_sent_filepath', 'get_semafor_filepath',
           'create_parent_dir_if_not_exists', 'get_bios_semeval_filepath',
           'get_ancestors_filepath', 'get_frame_parents_filepath',
           'get_rolemappings_filepath', 'get_fr_relation_xml_filepath']


def get_semafor_filepath(target_dirpath, splits_name):
    """Return the absolute path to the SEMAFOR file.

    If splits_name is 'train', function will return train.frame.elements.
    If splits_name is 'dev' or 'test', function will return train.frames.
    Both files will be seeked under the specified target_dirpath.
    """
    if splits_name not in ['train', 'dev', 'test']:
        raise InvalidParameterError('Unsupported splits_name: {}'.format(
            splits_name))
    if splits_name == 'train':
        return os.path.join(target_dirpath, 'train.frame.elements')
    return os.path.join(target_dirpath, '{}.frames'.format(splits_name))


def get_bios_filepath(target_dirpath, splits_name):
    """Return the absolute path of the {splits_name}.bios file.

    Look for the file under the specified taret_dirpath.
    """
    return os.path.join(target_dirpath, '{}.bios'.format(splits_name))


def get_bios_semeval_filepath(target_dirpath, splits_name):
    """Return the absolute path of the {splits_name}.bios.semeval file.

    Look for the file under the specified taret_dirpath.
    """
    return os.path.join(target_dirpath, '{}.bios.semeval'.format(splits_name))


def get_sent_filepath(target_dirpath, splits_name):
    """Return the absolute path of the {splits_name}.sentences file.

    Look for the file under the specified target_dirpath.
    """
    return os.path.join(target_dirpath, '{}.sentences'.format(splits_name))


def create_parent_dir_if_not_exists(filepath):
    """Create the parent directory of the input filepath if not exists."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


def get_ancestors_filepath(target_dirpath):
    """Return the absolute path to the ancestors.csv file."""
    os.makedirs(target_dirpath, exist_ok=True)
    return os.path.join(target_dirpath, 'ancestors.csv')


def get_frame_parents_filepath(target_dirpath):
    """Return the absolute path to the frame_parents.csv file."""
    os.makedirs(target_dirpath, exist_ok=True)
    return os.path.join(target_dirpath, 'frame_parents.csv')


def get_rolemappings_filepath(target_dirpath):
    """Return the absolute path to the frame_parent_rolemappings.csv file."""
    os.makedirs(target_dirpath, exist_ok=True)
    return os.path.join(target_dirpath, 'frame_parent_rolemappings.csv')


def get_fr_relation_xml_filepath(splits_dirpath):
    """Return the absolute path to the frRelation.xml file given splits_dirpath."""
    return os.path.join(splits_dirpath, 'frRelation.xml')
