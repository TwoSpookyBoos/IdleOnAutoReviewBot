import re

from flask import g

from models.advice.advice_base import AdviceBase
from models.advice.advice_group import AdviceGroup
from models.advice.advice_group_tabbed import TabbedAdviceGroup


class AdviceSection(AdviceBase):
    """
    Contains a list of `AdviceGroup` objects

    Args:
        name (str): the name of the section (e.g. Stamps, Bribes)
        tier (str): alphanumeric tier of this section (e.g. 17/36), not always present
        header (str): text of the section title (e.g "Best Stamp tier met: 17/36", "Maestro Right Hands")
        picture (str): image file name to use as header icon
        collapse (bool | None): should the section be collapsed on load?
        groups (list<AdviceGroup>): a list of `AdviceGroup` objects, each in its own box and bg colour
        pinchy_rating (int): Tier to pass into Pinchy for this section
        pinchy_placement (str): Placement determined by Pinchy, based on pinchy_rating
    """

    _children = "groups"

    def __init__(
        self,
        name: str,
        tier: str,
        header: str,
        picture: str | None = None,
        collapse: bool | None = None,
        groups=[],
        pinchy_rating: int = 0,
        max_tier: int = 0,
        true_max_tier: int = 0,
        completed: bool | None = None,
        unreached: bool = False,
        unrated: bool = False,
        informational: bool | None = None,
        overwhelming: bool | None = False,
        optional: bool | None = None,
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.name: str = name
        self.tier: str = tier
        self._raw_header: str = header
        self.picture: str = picture
        self.groups: list[AdviceGroup | TabbedAdviceGroup] = groups
        self.pinchy_rating: int = pinchy_rating
        self.max_tier: int = max_tier
        self.true_max_tier: int = true_max_tier
        self.completed: bool | None = completed
        self.unreached = unreached
        self.unrated = unrated
        self.informational = informational
        self.overwhelming = overwhelming
        self.optional = optional
        self.check_for_optional()

    @property
    def header(self) -> str:
        if not self.tier:
            return self._raw_header

        pattern = f"({re.escape(self.tier)})"
        parts = re.split(pattern, self._raw_header)

        if self.tier in parts:
            finished = ""

            if "/" in self.tier:
                try:
                    prog, goal = self.tier.split("/")
                    finished = " finished" if int(prog) >= int(goal) else ""
                except:
                    finished = ""

            parts[1] = f"""<span class="tier-progress{finished}">{parts[1]}</span>"""

        header_markedup = "".join(parts)

        return header_markedup

    @header.setter
    def header(self, raw_header: str):
        self._raw_header = raw_header

    @property
    def css_class(self):
        return self.name.lower().replace(" ", "-")

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups: list[AdviceGroup | TabbedAdviceGroup]):
        # filters out empty groups by checking if group has no advices
        self._groups = [group for group in groups if group]
        #self.check_for_completeness()

        if g.order_tiers:
            self._groups = sorted(self._groups)

    def check_for_completeness(self):
        if self.completed is not None:
            return
        elif self.unreached:
            #Unreached is set when a player hasn't progressed far enough to see the contents of a section. As far from complete as possible
            self.completed = False
        elif not self.unrated and self.pinchy_rating >= self.true_max_tier and self.name != 'Pinchy all':
            #If the section is rated and the player has reached the true max tier, mark the Section complete even if some incomplete groups still exist
            self.completed = True
        else:
            #Default: Section is complete if all children Groups are complete
            self.completed = len([group for group in self.groups if group and not group.completed]) == 0

    def check_for_informationalness(self):
        if self.informational is not None:
            return
        else:
            #print(f"{self.name}: {len([group for group in self.groups if group and group.informational])} Info groups / {len([group for group in self.groups if group])} total Truthy groups")
            self.informational = all([group.informational for group in self.groups]) and len([group for group in self.groups if group]) > 0  #True if 0 length, False otherwise

    def set_overwhelming(self, overwhelming):
        self.overwhelming = overwhelming
        for group in self.groups:
            group.set_overwhelming(overwhelming)

    def check_for_optional(self):
        if self.optional is None:
            self.optional = self.pinchy_rating >= self.max_tier

        if self.optional is not True:
            if self.name.startswith('Pinchy'):
                self.optional = False
            else:
                for group in self.groups:
                    group.check_for_optional(self.max_tier)
                self.optional = all([group.optional for group in self.groups])  # True if ALL groups are Optional
