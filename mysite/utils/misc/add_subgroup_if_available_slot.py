from flask import g as session_data


def add_subgroup_if_available_slot(dictionary: dict, subgroup_label):
    if subgroup_label not in dictionary and len(dictionary) < session_data.account.max_subgroups:
        dictionary[subgroup_label] = []
