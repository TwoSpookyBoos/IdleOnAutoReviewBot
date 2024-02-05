import functools
import re
from enum import Enum
from typing import Any

from flask import g


class Character:
    def __init__(self, character_index: int, character_name: str, class_name: str, base_class: str, sub_class: str, elite_class: str, all_skill_levels: dict):
        self.character_index: int = character_index
        self.character_name: str = character_name
        self.class_name: str = class_name
        self.class_name_icon: str = class_name + "-class-icon"
        self.base_class: str = base_class
        self.sub_class: str = sub_class
        self.elite_class: str = elite_class
        self.combat_level: int = all_skill_levels['Combat']
        self.mining_level: int = all_skill_levels['Mining']
        self.smithing_level: int = all_skill_levels['Smithing']
        self.choppin_level: int = all_skill_levels['Choppin']
        self.fishing_level: int = all_skill_levels['Fishing']
        self.alchemy_level: int = all_skill_levels['Alchemy']
        self.catching_level: int = all_skill_levels['Catching']
        self.trapping_level: int = all_skill_levels['Trapping']
        self.construction_level: int = all_skill_levels['Construction']
        self.worship_level: int = all_skill_levels['Worship']
        self.cooking_level: int = all_skill_levels['Cooking']
        self.breeding_level: int = all_skill_levels['Breeding']
        self.lab_level: int = all_skill_levels['Lab']
        self.sailing_level: int = all_skill_levels['Sailing']
        self.divinity_level: int = all_skill_levels['Divinity']
        self.gaming_level: int = all_skill_levels['Gaming']


class WorldName(Enum):
    PINCHY = "Pinchy"
    GENERAL = "General"
    WORLD1 = "World 1"
    WORLD2 = "World 2"
    WORLD3 = "World 3"
    WORLD4 = "World 4"
    WORLD5 = "World 5"
    BLUNDER_HILLS = "Blunder Hills"
    YUMYUM_DESERT = "Yum-Yum Desert"
    FROSTBITE_TUNDRA = "Frostbite Tundra"
    HYPERION_NEBULA = "Hyperion Nebula"
    SMOLDERIN_PLATEAU = "Smolderin' Plateau"


class AdviceBase:
    """
    Args:
        **extra: a dict of extra information that hasn't been accounted for yet
    """
    _children = "_true"
    _collapse = None
    _true = [True]
    name = ""

    def __init__(self, **extra):
        # assign all extra kwargs as a field on the object
        for k, v in extra.items():
            setattr(self, k, v)

    def __bool__(self) -> bool:
        children = getattr(self, self._children, list())
        return any(filter(bool, children))

    def __str__(self) -> str:
        return self.name

    @property
    def collapse(self) -> bool:
        children = getattr(self, self._children, list())
        return self._collapse if self._collapse is not None else not bool(children)

    @collapse.setter
    def collapse(self, _value: bool):
        self._collapse = _value


class Advice(AdviceBase):
    """
    Args:
        label (str): the display name of the advice
        item_name (str): CSS class to link the image icon to the advice, e.g. 'bean-slices'
        progression: numeric (usually), how far towards the goal did the item progress?
        goal: the target level or amount of the advice
        unit (str): if there is one, usually "%"
    """
    def __init__(self, label: str, item_name: str, progression: Any = "", goal: Any = "", unit: str = "", **extra):
        super().__init__(**extra)

        self.label: str = label
        self.item_name: str = item_name
        self.progression: str = str(progression)
        self.goal: str = str(goal)
        self.unit: str = unit

    @property
    def css_class(self) -> str:
        name = self.item_name.replace(' ', '-').lower()
        name = re.sub(r'[^\w-]', '', name)
        return name

    def __str__(self) -> str:
        return self.label


@functools.total_ordering
class AdviceGroup(AdviceBase):
    """
    Contains a list of `Advice` objects

    Args:
        tier (str): alphanumeric tier of this group's advices (e.g. 17, S)
        pre_string (str): the start of the group title
        post_string (str): trailing advice
        formatting (str): HTML tag name (e.g. strong, em)
        collapsed (bool): should the group be collapsed on load?
        advices (list<Advice>): a list of `Advice` objects, each advice on a separate line
    """
    _children = "advices"
    __compare_by = ["tier"]

    def __init__(self, tier: str, pre_string: str, post_string: str = "", formatting: str = "", collapse: bool | None = None, advices: list[Advice] = [], **extra):
        super().__init__(**extra)

        self.tier: str = str(tier)
        self.pre_string: str = pre_string
        self.post_string: str = post_string
        self.formatting: str = formatting
        self._collapse: bool | None = collapse
        self.advices: list[Advice] = advices

    def __str__(self) -> str:
        return ', '.join(map(str, self.advices))

    @property
    def show_table_header(self) -> bool:
        return self.show_progression or self.show_goal

    @property
    def show_progression(self) -> bool:
        return any(advice.progression for advice in self.advices)

    @property
    def show_goal(self) -> bool:
        return any(advice.goal for advice in self.advices)

    @property
    def heading(self) -> str:
        return (f"Tier {self.tier} - " if self.tier else "") + self.pre_string

    def _is_valid_operand(self, other):
        return all(hasattr(other, field) for field in self.__compare_by)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return all(
            getattr(self, field) == getattr(other, field)
            for field in self.__compare_by
        )

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return all(
            getattr(self, field) < getattr(other, field)
            for field in self.__compare_by
        )


class AdviceSection(AdviceBase):
    """
    Contains a list of `AdviceGroup` objects

    Args:
        name (str): the name of the section (e.g. Stamps, Bribes)
        tier (str): alphanumeric tier of this section (e.g. 17/36), not always present
        header (str): text of the section title (e.g "Best Stamp tier met: 17/36. Recommended stamp actions", "Maestro Right Hands")
        picture (str): image file name to use as header icon
        collapse (bool | None): should the section be collapsed on load?
        groups (list<AdviceGroup>): a list of `AdviceGroup` objects, each in its own box and bg colour
        pinchy_rating (str): Pinchy rating for this section
    """
    _children = "groups"

    def __init__(self, name: str, tier: str, header: str, picture: str | None = None, collapse: bool | None = None, groups: list[AdviceGroup] = [], pinchy_rating: str = "", **extra):
        super().__init__(**extra)

        self.name: str = name
        self.tier: str = tier
        self._raw_header: str = header
        self.picture: str = picture
        self._collapse: bool | None = collapse
        self._groups: list[AdviceGroup] = groups
        self.pinchy_rating: str = pinchy_rating

    @property
    def header(self) -> str:
        self._raw_header = self._raw_header.replace(".", ".<br>")
        if not self.tier:
            return self._raw_header

        pattern = f"({re.escape(self.tier)})"
        parts = re.split(pattern, self._raw_header)

        if self.tier in parts:
            finished = ""

            if "/" in self.tier:
                prog, goal = self.tier.split("/")
                finished = " finished" if prog == goal else ""

            parts[1] = f"""<span class="tier-progress{finished}">{parts[1]}</span>"""

        header_markedup = ''.join(parts)

        return header_markedup

    @header.setter
    def header(self, raw_header: str):
        self._raw_header = raw_header

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups: list[AdviceGroup]):
        # filters out empty groups by checking if group has no advices
        self._groups = [group for group in groups if group]

        if g.order_tiers:
            self._groups = sorted(self._groups)


class AdviceWorld(AdviceBase):
    """
    World-level advice container

    Args:
        name (WorldName): world name, e.g. General, World 1
        collapse (bool): should the world be collapsed on load?
        sections (list<AdviceSection>): a list of `AdviceSection` objects
        banner (str): banner image name
    """
    _children = "sections"

    def __init__(self, name: WorldName, collapse: bool = None, sections: list[AdviceSection] = [], banner: str = "", **extra):
        super().__init__(**extra)

        self.name: str = name.value
        self._collapse: bool | None = collapse
        self.sections: list[AdviceSection] = sections
        self.banner: str = banner
