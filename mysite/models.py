import re
from enum import Enum
from typing import Any


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
        **extra (dict): a dict of extra information that hasn't been accounted for yet
    """
    _children = ""
    name = ""

    def __init__(self, **extra):
        # assign all extra kwargs as a field on the object
        for k, v in extra.items():
            setattr(self, k, v)

    def __bool__(self) -> bool:
        return bool(getattr(self, self._children, list()))

    def __str__(self) -> str:
        return self.name


class Advice(AdviceBase):
    """
    Args:
        label (str): the display name of the advice
        item_name (str): CSS class to link the image icon to the advice, e.g. 'bean-slices'
        progression: numeric (usually), how far towards the goal did the item progress?
        goal: the target level or amount of the advice
        unit (str): if there is one, usually "%"
    """

    def __init__(self, label: str, item_name: str, progression: Any, goal: Any = "", unit: str = "", **extra):
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


class AdviceGroup(AdviceBase):
    """
    Contains a list of `Advice` objects

    Args:
        formatting (str): HTML tag name (e.g. strong, em)
        collapsed (bool): should the group be collapsed on load?
        tier (str): alphanumeric tier of this group's advices (e.g. 17, S)
        pre_string (str): the start of the group title
        advices (list<Advice>): a list of `Advice` objects, each advice on a separate line
        post_string (str): trailing advice
    """
    _children = "advices"

    def __init__(self, formatting: str, collapse: bool, tier: str, pre_string: str, advices: list[Advice], post_string: str, **extra):
        super().__init__(**extra)

        self.formatting: str = formatting
        self.collapse: bool = collapse
        self.tier: str = tier
        self.pre_string: str = pre_string
        self.advices: list[Advice] = advices
        self.post_string: str = post_string

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


class AdviceSection(AdviceBase):
    """
    Contains a list of `AdviceGroup` objects

    Args:
        collapse (bool): should the section be collapsed on load?
        name (str): the name of the section (e.g. Stamps, Bribes)
        tier (str): alphanumeric tier of this section (e.g. 17/36), not always present
        raw_header (str): text of the section title (e.g "Best Stamp tier met: 17/36. Recommended stamp actions", "Maestro Right Hands")
        groups (list<AdviceGroup>): a list of `AdviceGroup` objects, each in its own box and bg colour
        header (str): either `raw_header` or `raw_header` with the tier part wrapped in `<span>`, if exists
    """
    _children = "groups"

    def __init__(self, collapse: bool, picture: str, name: str, tier: str, header: str, groups: list[AdviceGroup], pinchy_rating: str = "", **extra):
        super().__init__(**extra)

        self.collapse: bool = collapse
        self.name: str = name
        self.picture: str = picture
        self.tier: str = tier
        self._raw_header: str = header
        self.groups: list[AdviceGroup] = groups
        self.pinchy_rating: str = pinchy_rating

    @property
    def header(self) -> str:
        if not self.tier:
            return self._raw_header

        pattern = f"({re.escape(self.tier)})"
        parts = re.split(pattern, self._raw_header)

        if self.tier in parts:
            parts[1] = f"""<span class="tier-progress">{parts[1]}</span>"""

        header_markedup = ''.join(parts)

        return header_markedup

    @header.setter
    def header(self, raw_header: str):
        self._raw_header = raw_header


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

    def __init__(self, name: WorldName, collapse: bool, sections: list[AdviceSection], banner: str = "", **extra):
        super().__init__(**extra)

        self.name: str = name.value
        self.collapse: bool = collapse
        self.sections: list[AdviceSection] = sections
        self.banner: str = banner
        self.children: list[AdviceBase] = self.sections
