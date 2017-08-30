"""A set of methods used to handle and process FrameNet data."""

import logging
from collections import defaultdict
from pyFN.models.target import Target

__all__ = ['extract_pos', 'to_labels_by_layer_name', 'to_labels_by_indexes',
           'to_target', 'to_valence_units', 'to_valence_pattern',
           'to_valence_units_by_indexes']


logger = logging.getLogger(__name__)


def extract_pos(luname):
    """Return the part of speech of the lexunit name."""
    if luname is None:
        return None
    return luname.split('.')[1]


def to_labels_by_layer_name(labels):
    """Convert a list of labels to a dict of labels with layer names as keys."""
    labels_by_layer_name = defaultdict(list)
    for label in labels:
        labels_by_layer_name[label.layer.name].append(label)
    return labels_by_layer_name


def to_labels_by_indexes(labels):
    """Convert a list of labels to a dict of label.

    Keys are start#end index tuples
    """
    labels_by_indexes = defaultdict(list)
    for label in labels:
        labels_by_indexes[(label.start, label.end)].append(label)
    return labels_by_indexes


def _extract_flat_target_pnw_labels(target_indexes, pnw_labels_by_indexes):
    target_pnw_labels = [labels for indexes, labels
                         in pnw_labels_by_indexes.items()
                         if indexes in target_indexes]
    return [item for sublist in target_pnw_labels for item in sublist]


def _extract_target_pos_tags(target_indexes, pnw_labels_by_indexes):
    flat_target_pnw_labels = _extract_flat_target_pnw_labels(
        target_indexes, pnw_labels_by_indexes)
    return [label for label in flat_target_pnw_labels
            if label.layer.name =='PENN' or label.layer.name == 'BNC']


def _extract_target_string(text, indexes):
    for (start, end) in indexes:
        if start == -1 or end == -1:
            logger.debug(
                'Target indexes are not specified in sentence: {}'
                .format(text))
            return ''
    return ' '.join([text[start: end+1] for (start, end) in indexes])


def _extract_target_indexes(fn_labels):
    return [(label.start, label.end) for label in fn_labels
            if label.layer.name == 'Target']


def to_target(pnw_labels_by_indexes, fn_labels, lexunit, text):
    target_indexes = _extract_target_indexes(fn_labels)
    target_string = _extract_target_string(text, target_indexes)
    target_pos_tags = _extract_target_pos_tags(target_indexes,
                                               pnw_labels_by_indexes)
    return Target(target_string, lexunit, target_indexes, target_pos_tags)


def _contains_unspecified_fe_pt_gf(index, labels):
    """Return true iff.

    at least one label is a FE/PT/GF and not all of them are specified.
    """
    if index[0] != -1 and index[1] != -1:
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
        if (contains_fe or contains_pt or contains_gf) and \
         (not contains_fe or not contains_pt or not contains_gf):
            return True
    return False


def _contains_unspecified_indexes(index, labels):
    if index[0] == -1 or index[1] == -1:  # if start or end is not specified
        for label in labels:
            if label.name == 'PT' or label.name == 'GF':
                logger.warning(
                    'start/end indexes are not specified for PT/GF: {}'
                    .format(label.name))
                return True
            if label.name == 'FE' and label.itype is None:
                logger.warning(
                    'start/end indexes are not specified for FE {}'
                    .format(label.name))
                return True
    return False


def to_valence_units_by_indexes(labels_by_indexes):
    valence_units_by_indexes = defaultdict(list)
    for index, labels in labels_by_indexes.items():
        if _contains_unspecified_indexes(index, labels) or\
         _contains_unspecified_fe_pt_gf(index, labels):
            valence_units_by_indexes[index] = []
        else:
            if index[0] == -1 or index[1] == -1:  # if start or end is not
            # specified
                for label in labels:
                    valence_units_by_indexes[index].append('{}.{}'.format(
                        label.name, label.itype))
            else:
                fe_labels = [label for label in labels
                             if label.layer.name == 'FE']
                pt_labels = [label for label in labels
                             if label.layer.name == 'PT']
                gf_labels = [label for label in labels
                             if label.layer.name == 'GF']
                if not fe_labels and not pt_labels and not gf_labels:
                    # We are not dealing with FN FE.PT.GF layers
                    continue
                for fe_label in fe_labels:
                    valence_units_by_indexes[index].append('{}.{}.{}'.format(
                        fe_label.name, pt_labels[0].name, gf_labels[0].name))
    return valence_units_by_indexes


def to_valence_units(valence_units_by_indexes):
    all_valence_units = []
    for valence_units in valence_units_by_indexes.values():
        if not valence_units:
            return []
        all_valence_units.extend(valence_units)
    return all_valence_units


def to_valence_pattern(valence_units):
    """Convert a list of valence units to a valence pattern."""
    return ' '.join(valence_units)
