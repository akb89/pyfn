"""A set of methods used to handle and process FrameNet data."""

import logging
from collections import defaultdict

__all__ = ['extract_pos', 'to_labels_by_layer_name', 'to_labels_by_indexes', 'to_target',
           'to_valence_units', 'to_valence_pattern']


logger = logging.getLogger(__name__)


def extract_pos(luname):
    """Return the part of speech of the lexunit name."""
    return luname.split('.')[1]


def to_labels_by_layer_name(labels):
    """Convert a list of labels to a dict of labels with layer names as keys."""
    labels_by_layer_name = defaultdict(list)
    for label in labels:
        labels_by_layer_name[label.layer.name].append(label)
    return labels_by_layer_name


def to_labels_by_indexes(labels):
    """Convert a list of labels to a dict of labels with start#end index tuples as keys."""
    labels_by_indexes = defaultdict(list)
    for label in labels:
        labels_by_indexes[(label.start, label.end)].append(label)
    return labels_by_indexes


def to_target(labels, lexunit):
    return


def _contains_unspecified_fe_pt_gf(labels_by_indexes):
    """Return true iff at least one label is a FE/PT/GF and not all of them are specified."""
    for indexes, labels in labels_by_indexes.items():
        if indexes[0] is not None and indexes[1] is not None:
            contains_fe = False
            contains_pt = False
            contains_gf = False
            for label in labels:
                if label.layer.name == 'FE':
                    contains_fe = True
                if label.layer.name == 'PT':
                    contains_pt = True
                if label.layer.name == 'GF':
                    contains_gf = True
            if (contains_fe or contains_pt or contains_gf) and (not contains_fe or not contains_pt or not contains_gf):
                return True
    return False


def _contains_unspecified_indexes(labels_by_indexes):
    for indexes, labels in labels_by_indexes.items():
        if indexes[0] is None or indexes[1] is None:  # if start or end is not specified
            for label in labels:
                if label.name == 'PT' or label.name == 'GF':
                    logger.warning('start/end indexes are not specified for PT/GF: {}'.format(label.name))
                    return True
                if label.name == 'FE' and label.itype is None:
                    logger.warning('start/end indexes are not specified for FE {}'.format(label.name))
                    return True
    return False


def _contains_invalid_labels(labels_by_indexes):
    return _contains_unspecified_indexes(labels_by_indexes)\
     or _contains_unspecified_fe_pt_gf(labels_by_indexes)


def to_valence_units(labels_by_indexes):
    valence_units = []
    if _contains_invalid_labels(labels_by_indexes):
        return []
    for indexes, labels in labels_by_indexes.items():
        if indexes[0] is None or indexes[1] is None:  # if start or end is not specified
            for label in labels:
                valence_units.append('{}.{}'.format(label.name, label.itype))
        else:
            fe_labels = [label for label in labels if label.layer.name == 'FE']
            pt_labels = [label for label in labels if label.layer.name == 'PT']
            gf_labels = [label for label in labels if label.layer.name == 'GF']
            if not fe_labels and not pt_labels and not gf_labels:
                # We are not dealing with FN FE.PT.GF layers
                continue
            for fe_label in fe_labels:
                valence_units.append('{}.{}.{}'.format(fe_label.name, pt_labels[0].name, gf_labels[0].name))
    return valence_units


def to_valence_pattern(valence_units):
    """Convert a list of valence units to a valence pattern."""
    return ' '.join(valence_units)
