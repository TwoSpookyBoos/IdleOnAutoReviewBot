
from models.models import TabbedAdviceGroup, AdviceGroup, session_data


def add_tabbed_advice_group_or_spread_advice_group_list(src: dict, target: TabbedAdviceGroup, tabbed_key_name: str):
    if session_data.tabbed_advice_groups:
        src[tabbed_key_name] = target
    else:
        target_dict: dict[str, AdviceGroup] = {tab.label: advice_group for tab, advice_group in target.tabbed_advices.values()}
        src.update(target_dict)
