from enum import Enum

from models.advice.advice_base import AdviceBase
from models.advice.advice_section import AdviceSection
from utils.text_formatting import kebab


class WorldName(Enum):
    PINCHY = "Pinchy"
    GENERAL = "General"
    MASTER_CLASSES = 'Master Classes'
    WORLD1 = "World 1"
    WORLD2 = "World 2"
    WORLD3 = "World 3"
    WORLD4 = "World 4"
    WORLD5 = "World 5"
    CAVERNS = "Caverns"
    WORLD6 = "World 6"
    BLUNDER_HILLS = "Blunder Hills"
    YUMYUM_DESERT = "Yum-Yum Desert"
    FROSTBITE_TUNDRA = "Frostbite Tundra"
    HYPERION_NEBULA = "Hyperion Nebula"
    SMOLDERIN_PLATEAU = "Smolderin' Plateau"
    SPIRITED_VALLEY = "Spirited Valley"
    THE_CAVERNS_BELOW = "The Caverns Below"
    SHIMMERFIN_DEEP = "Shimmerfin Deep"


class AdviceWorld(AdviceBase):
    """
    World-level advice container

    Args:
        name (WorldName): world name, e.g. General, World 1
        collapse (bool): should the world be collapsed on load?
        sections (list<AdviceSection>): a list of `AdviceSection` objects
        banner (list[str]): banner image name(s)
    """

    _children = "sections"

    def __init__(
        self,
        name: WorldName,
        collapse: bool | None = None,
        sections: list[AdviceSection] = list(),
        banner: list[str] | None = None,
        title: str = "",
        completed: bool | None = None,
        informational: bool | None = None,
        unrated: bool | None = None,
        overwhelming: bool | None = False,
        optional: bool | None = None,
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.name: str = name.value
        self.sections: list[AdviceSection] = sections
        self.banner: list[str] | None = banner
        self.title: str = title
        self.completed = completed
        if self.completed is None:
            self.check_for_completeness()
        self.informational = informational
        if self.informational is None:
            self.check_for_informationalness()
        self.unrated = unrated
        if self.unrated is None:
            self.check_for_unratedness()
        self.overwhelming = overwhelming
        if self.overwhelming is None:
            self.check_for_overwhelming()
        self.optional = optional
        if self.optional is None:
            self.check_for_optional()

    @property
    def id(self):
        return kebab(self.name)

    def hide_unreached_sections(self):
        self.sections = [section for section in self.sections if not section.unreached]

    def check_for_completeness(self):
        """
        Used when a bool for complete was not passed in during initialization of the AdviceWorld
        """
        if self.completed is None:
            self.completed = len([section for section in self.sections if not section.completed]) == 0  #True if 0 length, False otherwise

    def check_for_informationalness(self):
        if self.informational is None:
            self.informational = all([section.informational for section in self.sections if section])

    def check_for_unratedness(self):
        if self.unrated is None:
            self.unrated = all([section.unrated for section in self.sections if section])

    def check_for_overwhelming(self):
        if self.overwhelming is None:
            self.overwhelming = all([section.overwhelming for section in self.sections if section])  #True if ALL sections are Overwhelming

    def check_for_optional(self):
        if self.optional is None:
            if self.name.startswith('Pinchy'):
                self.optional = False
            else:
                self.optional = all([section.optional for section in self.sections if section])  #True if ALL sections are Optional

