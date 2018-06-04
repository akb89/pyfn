"""Marshalling to hierarchy files.

Generates ancestors.csv, frame_parent_rolemappings.csv and frame_parents.csv
"""

import itertools
from collections import defaultdict

import logging

import pyfn.utils.files as files_utils
import pyfn.utils.constants as const

__all__ = ['marshall_relations']

logger = logging.getLogger(__name__)


# pylint: disable-msg=R0914
def _get_parents(frame_name, frame_relations_dict):
    parents = []
    if frame_name not in frame_relations_dict:
        return parents
    for parent_name in frame_relations_dict[frame_name]:
        parents.append(parent_name)
    return parents


def _get_frame_parents_dict(frames, frame_relations_dict):
    parents_dict = {}
    for frame_name in sorted(name for name in {frame.name for frame in
                                               frames}):
        parents = _get_parents(frame_name, frame_relations_dict)
        if parents:
            parents_dict[frame_name] = parents
    return parents_dict


def _get_ancestors(frame_name, frame_relations_dict):
    ancestors = []
    if frame_name not in frame_relations_dict:
        return ancestors
    for parent_name in frame_relations_dict[frame_name]:
        ancestors.append(parent_name)
        ancestors.extend(_get_ancestors(parent_name, frame_relations_dict))
    return ancestors


def _get_ancestors_dict(frames, frame_relations_dict):
    ancestors_dict = {}
    for frame_name in sorted(name for name in {frame.name for frame in
                                               frames}):
        ancestors_dict[frame_name] = _get_ancestors(frame_name,
                                                    frame_relations_dict)
    return ancestors_dict


def _get_fe_relations_dict(fe_relations, fe_id_set, relation_type_names):
    fe_relations_dict = defaultdict(list)
    for fe_relation in fe_relations:
        if fe_relation.frame_relation.frtype.name not in relation_type_names:
            continue
        if fe_relation.sub_fe._id not in fe_id_set \
         or fe_relation.sup_fe._id not in fe_id_set:
            continue
        child = '{}.{}'.format(fe_relation.frame_relation.sub_frame.name,
                               fe_relation.sub_fe.name)
        parent = '{}.{}'.format(fe_relation.frame_relation.sup_frame.name,
                                fe_relation.sup_fe.name)
        fe_relations_dict[child].append(parent)
    return fe_relations_dict


def _get_frame_relations_dict(frame_relations, frame_id_set,
                              relation_type_names):
    frame_relations_dict = defaultdict(list)
    for frame_relation in frame_relations:
        if frame_relation.frtype.name not in relation_type_names:
            continue
        if frame_relation.sub_frame._id not in frame_id_set or \
         frame_relation.sup_frame._id not in frame_id_set:
            continue
        frame_relations_dict[frame_relation.sub_frame.name].append(
            frame_relation.sup_frame.name)
    return frame_relations_dict


def _get_fe_id_set(annosets):
    return {label.fe_id for annoset in annosets for label
            in annoset.labelstore.labels_by_layer_name['FE']}


def _get_frame_id_set(annosets):
    return {annoset.target.lexunit.frame._id for annoset in annosets}


def marshall_relations(annosets, frame_relations, fe_relations,
                       target_dirpath):
    """Marshall a relations to csv files."""
    annosets, _annosets, __annosets = itertools.tee(annosets, 3)
    frame_id_set = _get_frame_id_set(annosets)
    frame_relations_dict = _get_frame_relations_dict(
        frame_relations, frame_id_set, const.HIERARCHY_RELATION_TYPES)
    frames = [annoset.target.lexunit.frame for annoset in _annosets]
    ancestors_dict = _get_ancestors_dict(frames, frame_relations_dict)
    ancestors_output_file = files_utils.get_ancestors_filepath(target_dirpath)
    with open(ancestors_output_file, 'w', encoding='utf-8') \
     as ancestors_stream:
        for frame_name, ancestors in ancestors_dict.items():
            if not ancestors:
                print(frame_name, file=ancestors_stream)
            else:
                print('{},{}'.format(frame_name, ','.join(ancestors)),
                      file=ancestors_stream)
    frame_parents_dict = _get_frame_parents_dict(frames, frame_relations_dict)
    frame_parents_output_file = files_utils.get_frame_parents_filepath(
        target_dirpath)
    with open(frame_parents_output_file, 'w', encoding='utf-8') \
     as frame_parents_stream:
        for frame_name, parents in frame_parents_dict.items():
            print('{},{}'.format(frame_name, ','.join(parents)),
                  file=frame_parents_stream)
    fe_id_set = _get_fe_id_set(__annosets)
    fe_relations_dict = _get_fe_relations_dict(
        fe_relations, fe_id_set, const.HIERARCHY_RELATION_TYPES)
    rolemappings_output_file = files_utils.get_rolemappings_filepath(
        target_dirpath)
    with open(rolemappings_output_file, 'w', encoding='utf-8') \
     as rolemappings_stream:
        for role_name, roles in sorted(fe_relations_dict.items()):
            print('{},{}'.format(role_name, ','.join(roles)),
                  file=rolemappings_stream)
