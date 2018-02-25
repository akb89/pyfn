"""Storing valence units in multiple format."""

from collections import defaultdict

import logging

from pyfn.models.frameelement import FrameElement
from pyfn.models.valenceunit import ValenceUnit

__all__ = ['ValenceUnitStore']

logger = logging.getLogger(__name__)


# pylint: disable=R0916
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


# pylint: disable=R0912
def _to_valence_units_by_indexes(labels_by_indexes, fe_dict):
    valence_units_by_indexes = defaultdict(list)
    for index, labels in labels_by_indexes.items():
        if _contains_unspecified_indexes(index, labels):
            valence_units_by_indexes[index] = []
        else:
            if index[0] == -1 or index[1] == -1:  # if start or end is not
                # specified
                for label in labels:
                    if fe_dict:
                        fe = fe_dict[label.fe_id]
                    else:
                        fe = FrameElement(_id=label.fe_id,
                                          name=label.name)
                    fe.itype = label.itype
                    valence_unit = ValenceUnit(fe)
                    valence_units_by_indexes[index].append(valence_unit)
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
                    if fe_dict:
                        fe = fe_dict[fe_label.fe_id]
                    else:
                        fe = FrameElement(_id=fe_label.fe_id,
                                          name=fe_label.name)
                    if pt_labels and gf_labels:  # TODO check also this
                        valence_unit = ValenceUnit(fe, pt_labels[0].name,
                                                   gf_labels[0].name)
                        valence_units_by_indexes[index].append(valence_unit)
                    else:
                        valence_unit = ValenceUnit(fe, 'undefined',
                                                   'undefined')
                        valence_units_by_indexes[index].append(valence_unit)
    return valence_units_by_indexes


def _to_valence_units(valence_units_by_indexes):
    all_valence_units = []
    for valence_units in valence_units_by_indexes.values():
        if not valence_units:
            return []  # Strict rule: if there is one problem, return []
        all_valence_units.extend(valence_units)
    return all_valence_units


class ValenceUnitStore():
    """ValenceUnitStore."""

    def __init__(self, valence_units, valence_units_by_indexes):
        """Constructor."""
        self._valence_units = valence_units
        self._valence_units_by_indexes = valence_units_by_indexes

    @classmethod
    def from_fn_data(cls, fn_labels_by_indexes, fe_dict):
        """Return ValenceUnitStore instance generated from FrameNet data."""
        valence_units_by_indexes = _to_valence_units_by_indexes(
            fn_labels_by_indexes, fe_dict)
        valence_units = _to_valence_units(valence_units_by_indexes)
        return cls(valence_units, valence_units_by_indexes)

    @property
    def valence_units_by_indexes(self):
        """Return an index to ValenceUnit objects dict."""
        return self._valence_units_by_indexes

    @property
    def valence_units(self):
        """Return a list of ValenceUnit objects."""
        return self._valence_units
