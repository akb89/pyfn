"""Load FN data."""

import os
import pickle
import logging
import mmh3
import pyfn.utils.constants as const
import pyfn.utils.xml as xml_utils

__all__ = ['load_fe_dict']

logger = logging.getLogger(__name__)


def _get_fe_dict_identifier(frame_xml_dirpath):
    identifier = ''
    xml_filepaths = xml_utils.extract(frame_xml_dirpath)
    for xml_filepath in xml_filepaths:
        identifier = '{}{}{}'.format(identifier,
                                     os.path.basename(xml_filepath),
                                     os.path.getmtime(xml_filepath))
    return str(mmh3.hash(identifier))


def load_fe_dict(frame_xml_dirpath):
    """Load a {fe_id: FrameElement} dictionary."""
    identifier = _get_fe_dict_identifier(frame_xml_dirpath)
    fe_dict_filepath = os.path.join(const.DATA_DIR,
                                    '{}.pkl'.format(identifier))
    if os.path.exists(fe_dict_filepath):
        logger.debug('Found fe dict matching config identifier. Loading...')
        with open(fe_dict_filepath, 'rb') as identifier_stream:
            return pickle.load(identifier_stream)
    logger.debug('Could not find fe dict matching identifier:')
    # TODO: implement frame unmarshaller
    # fe_dict = unmarshaller.unmarshall_frame_xml(frame_xml_dirpath)
    fe_dict = {}
    with open(fe_dict, 'wb') as identifier_stream:
        pickle.dump(fe_dict, identifier_stream,
                    protocol=pickle.HIGHEST_PROTOCOL)
    return fe_dict
