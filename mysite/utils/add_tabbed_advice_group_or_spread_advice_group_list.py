from flask import g as session_data

from models.models import TabbedAdviceGroup, AdviceGroup


def add_tabbed_advice_group_or_spread_advice_group_list(src: dict, target: TabbedAdviceGroup, tabbed_key_name: str):
    if session_data.tabbed_advice_groups:
        src[tabbed_key_name] = target
    else:
        target_dict: dict[str, AdviceGroup] = {tab.label: advice_group for tab, advice_group in target.tabbed_advices.values()}
        # Merge the two dicts. We assume no duplicate keys to keep this operation simple
        src = src | target_dict
    return src