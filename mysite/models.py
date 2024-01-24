from typing import Any


class Advice:
    """
    label - the display name of the advice
    item_name - CSS class to link the image icon to the advice
    progression - numeric (usually), how far towards the goal did the item progress?
    goal - the target level or amount of the advice
    unit - if there is one, usually %
    extra - a dict of extra information pertaining to the advice that we haven't accounted for yet
    """
    def __init__(self, label: str, item_name: str, progression: Any, goal: Any = "", unit: str = "", extra: dict = {}):
        self.label: str = label
        self.item_name: str = item_name
        self.progression: str = str(progression)
        self.goal: str = str(goal)
        self.unit: str = unit
        self.extra: dict = extra

    @property
    def css_class(self) -> str:
        return self.item_name.replace(' ', '-').lower()


class AdviceGroup:
    """
    formatting - HTML tag name (e.g. strong, em)
    collapsed - should the group be collapsed on load?
    tier - alphanumeric tier of this group's advices (e.g. 17, S)
    pre_string - the start of the group title
    advices - a list of Advice objects, each advice on a separate line
    post_string - trailing advice
    """
    def __init__(self, formatting: str, collapse: bool, tier: str, pre_string: str, advices: list[Advice], post_string: str, group_extra: dict = {}):
        self.formatting: str = formatting
        self.collapse: bool = collapse
        self.tier: str = tier
        self.pre_string: str = pre_string
        self.advices: list[Advice] = advices
        self.post_string: str = post_string
        self.group_extra: dict = group_extra

    def __bool__(self):
        return len(self.advices) > 0


class AdviceSection:
    """
    collapse - should the section be collapsed on load?
    section_name - the name of the section (e.g. Stamps, Bribes)
    section_tier - alphanumeric tier of this section (e.g. 17/36), not always present
    section_header - text of the section title (e.g "Best Stamp tier met: 17/36. Recommended stamp actions", "Maestro Right Hands")
    groups - a list of AdviceGroup objects, each in its own box and bg colour
    """
    def __init__(self, collapse: bool, section_name: str, section_tier: str, section_header: str, groups: list[AdviceGroup], section_pinchy_rating: str = "", section_extra: dict = {}):
        self.collapse: bool = collapse
        self.section_name: str = section_name
        self.section_tier: str = section_tier
        self.section_header: str = section_header
        self.groups: list[AdviceGroup] = groups
        self.section_pinchy_rating: str = section_pinchy_rating
        self.section_extra: dict = section_extra

    def header_parts(self):
        parts = self.section_header.split(self.section_tier)
        parts.insert(1, self.section_tier)
        return parts

    def __bool__(self):
        return len(self.groups) > 0


class AdviceWorld:
    """
    collapse - should the world be collapsed on load?
    sections - a list of AdviceSection objects
    banner - banner image name
    """
    def __init__(self, collapse: bool, sections: list[AdviceSection], banner: str = "", world_extra: dict = {}):
        self.collapse: bool = collapse
        self.sections: list[AdviceSection] = sections
        self.banner: str = banner
        self.world_extra: dict = world_extra

    def __bool__(self):
        return len(self.sections) > 0
