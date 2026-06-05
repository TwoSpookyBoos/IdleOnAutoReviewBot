from functools import cached_property

from utils.logging import get_logger
from utils.safer_data_handling import safe_loads

from consts.consts_general import (
    greenstack_item_difficulty_groups,
    gstack_unique_expected,
    quest_items_codenames,
)

logger = get_logger(__name__)


class GreenStacks:
    def __init__(self, raw_data: dict):
        self._codenames: list[str] = safe_loads(raw_data.get("GreenStacks", []))
        self._quest_items: set[str] = set(quest_items_codenames)

    @cached_property
    def unprecedented(self) -> list[str]:
        return [
            codename
            for codename in self._codenames
            if codename not in gstack_unique_expected
        ]

    @cached_property
    def expected(self) -> set[str]:
        return {
            codename
            for codename in gstack_unique_expected
            if codename not in self._codenames
        }

    @property
    def count(self) -> int:
        return len(self._codenames)

    @property
    def expected_by_tier(self) -> dict[int, dict[str, list[str]]]:
        tiered = dict()
        expected_set = self.expected
        expected_quest_set = self.expected_quest_items
        for tier, categories in greenstack_item_difficulty_groups.items():
            categorised = dict()
            for category, items in categories.items():
                item_list = [
                    codename
                    for codename in items
                    if codename in expected_set and codename not in expected_quest_set
                ]
                if item_list:
                    categorised[category] = item_list
            if categorised:
                tiered["Timegated" if tier == 0 else tier] = categorised
        return tiered

    @cached_property
    def collected_quest_items(self) -> set[str]:
        """Memoized set of greenstacked quest item codenames"""
        return self._quest_items.intersection(self._codenames)

    @cached_property
    def expected_quest_items(self) -> set[str]:
        """Memoized set of quest item codenames not yet greenstacked"""
        return self._quest_items.difference(self._codenames)
