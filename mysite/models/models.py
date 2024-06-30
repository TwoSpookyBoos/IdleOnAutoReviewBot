import copy
import functools
import json
import re
import sys
from collections import defaultdict
from enum import Enum
from math import ceil, floor
from typing import Any

from flask import g

from utils.data_formatting import getCharacterDetails, safe_loads
from consts import expectedStackables, greenstack_progressionTiers, card_data, maxMeals, maxMealLevel, jade_emporium, max_IndexOfVials, getReadableVialNames, \
    buildingsDict, atomsList, prayersDict, labChipsList, bribesDict, shrinesList, pristineCharmsList, sigilsDict, \
    sailingDict, guildBonusesList, labBonusesList, lavaFunc, vialsDict, sneakingGemstonesFirstIndex, sneakingGemstonesList, \
    getMoissaniteValue, getGemstoneValue, getGemstonePercent, sneakingGemstonesStatList, stampsDict, stampTypes, marketUpgradeList, \
    achievementsList, forgeUpgradesDict, arcadeBonuses, saltLickList, allMeritsDict, bubblesDict, familyBonusesDict, poBoxDict, equinoxBonusesDict, \
    maxDreams, dreamsThatUnlockNewBonuses, ceilUpToBase, starsignsDict, gfood_codes, getStyleNameFromIndex, divinity_divinitiesDict, getDivinityNameFromIndex, \
    maxCookingTables, getNextESFamilyBreakpoint, expected_talentsDict, colliderStorageLimitList, gamingSuperbitsDict, labJewelsDict
from utils.text_formatting import kebab, getItemCodeName, getItemDisplayName

def session_singleton(cls):
    def getinstance(*args, **kwargs):
        if not hasattr(g, "account"):
            return cls(*args, **kwargs)
        return g.account

    return getinstance


class Equipment:
    def __init__(self, raw_data, toon_index, safeStatus: bool):
        if safeStatus:
            order = raw_data.get(f"EquipOrder_{toon_index}", [])
            quantity = raw_data.get(f"EquipQTY_{toon_index}", [])
            groups = list()
            for o, q in zip(order, quantity):
                o.pop("length", None)
                q.pop("length", None)
                o = dict(sorted(o.items(), key=lambda i: int(i[0]))).values()
                q = dict(sorted(q.items(), key=lambda i: int(i[0]))).values()
                groups.append([Asset(name, float(count)) for name, count in zip(o, q)])

            equips, tools, foods = groups

            self.equips = equips
            self.tools = tools
            self.foods = foods
        else:
            self.equips = {}
            self.tools = {}
            self.foods = []

def getExpectedTalents(base_class, sub_class, elite_class):
    expectedTalents = []
    for className in [base_class, sub_class, elite_class]:
        try:
            expectedTalents.extend(expected_talentsDict[className])
        except:
            continue
    return expectedTalents

def getSpecializedSkills(base_class, sub_class, elite_class):
    specializedSkillsList = []
    if base_class == "Mage":
        specializedSkillsList.append("Choppin")
    elif base_class == "Warrior":
        specializedSkillsList.append("Mining")

    if sub_class == "Barbarian":
        specializedSkillsList.append("Fishing")
    elif sub_class == "Bowman":
        specializedSkillsList.append("Catching")
    elif sub_class == "Hunter":
        specializedSkillsList.append("Trapping")
    elif sub_class == "Wizard":
        specializedSkillsList.append("Worship")

    if elite_class == "Blood Berserker":
        specializedSkillsList.append("Cooking")

    return specializedSkillsList

class Character:
    def __init__(
        self,
        raw_data: dict,
        character_index: int,
        character_name: str,
        class_name: str,
        base_class: str,
        sub_class: str,
        elite_class: str,
        equipped_prayers: list,
        all_skill_levels: dict,
        max_talents: dict,
        current_preset_talents: dict,
        secondary_preset_talents: dict,
        po_boxes: list[int]):

        self.character_index: int = character_index
        self.character_name: str = character_name

        self.class_name: str = class_name
        self.class_name_icon: str = class_name.replace(" ", "-") + "-icon"
        self.base_class: str = base_class
        self.sub_class: str = sub_class
        self.elite_class: str = elite_class
        self.max_talents_over_books: int = 100
        self.symbols_of_beyond = 0
        self.family_guy_bonus = 0
        self.max_talents: dict = max_talents
        self.current_preset_talents: dict = current_preset_talents
        self.secondary_preset_talents: dict = secondary_preset_talents
        self.specialized_skills: list[str] = getSpecializedSkills(self.base_class, self.sub_class, self.elite_class)
        self.expected_talents: list[int] = getExpectedTalents(self.base_class, self.sub_class, self.elite_class)

        self.combat_level: int = all_skill_levels["Combat"]
        self.mining_level: int = all_skill_levels["Mining"]
        self.smithing_level: int = all_skill_levels["Smithing"]
        self.choppin_level: int = all_skill_levels["Choppin"]
        self.fishing_level: int = all_skill_levels["Fishing"]
        self.alchemy_level: int = all_skill_levels["Alchemy"]
        self.catching_level: int = all_skill_levels["Catching"]
        self.trapping_level: int = all_skill_levels["Trapping"]
        self.construction_level: int = all_skill_levels["Construction"]
        self.worship_level: int = all_skill_levels["Worship"]
        self.cooking_level: int = all_skill_levels["Cooking"]
        self.breeding_level: int = all_skill_levels["Breeding"]
        self.lab_level: int = all_skill_levels["Lab"]
        self.sailing_level: int = all_skill_levels["Sailing"]
        self.divinity_level: int = all_skill_levels["Divinity"]
        self.gaming_level: int = all_skill_levels["Gaming"]
        self.farming_level: int = all_skill_levels["Farming"]
        self.sneaking_level: int = all_skill_levels["Sneaking"]
        self.summoning_level: int = all_skill_levels["Summoning"]
        self.equipped_prayers = []
        for prayerIndex in equipped_prayers:
            if prayerIndex != -1:  #-1 is the placeholder value for an empty prayer slot
                try:
                    self.equipped_prayers.append(prayersDict[prayerIndex]['Name'])
                except:
                    continue
        self.skills = all_skill_levels
        self.divinity_style: str = "None"
        self.divinity_link: str = "Unlinked"
        self.current_polytheism_link = "Unlinked"
        self.secondary_polytheism_link = "Unlinked"
        self.po_boxes_invested = {}
        for poBoxIndex, poBoxValues in poBoxDict.items():
            try:
                self.po_boxes_invested[poBoxValues['Name']] = {
                    'Level': po_boxes[poBoxIndex],
                    'Bonus1Value': lavaFunc(
                        poBoxValues['1_funcType'],
                        po_boxes[poBoxIndex],
                        poBoxValues['1_x1'],
                        poBoxValues['1_x2'],
                    ),
                    'Bonus1String': '',
                    'Bonus2Value': lavaFunc(
                        poBoxValues['2_funcType'],
                        po_boxes[poBoxIndex],
                        poBoxValues['2_x1'],
                        poBoxValues['2_x2'],
                    ) if po_boxes[poBoxIndex] >= poBoxValues['2_minCount'] else 0,
                    'Bonus2String': '',
                    'Bonus3Value': lavaFunc(
                        poBoxValues['3_funcType'],
                        po_boxes[poBoxIndex],
                        poBoxValues['3_x1'],
                        poBoxValues['3_x2'],
                    ) if po_boxes[poBoxIndex] >= poBoxValues['3_minCount'] else 0,
                    'Bonus3String': '',
                }
                if self.po_boxes_invested[poBoxValues['Name']]['Level'] > 0:
                    self.po_boxes_invested[poBoxValues['Name']]['Bonus1String'] = (f"{poBoxValues['1_pre']}"
                                                                                   f"{self.po_boxes_invested[poBoxValues['Name']]['Bonus1Value']}"
                                                                                   f"{poBoxValues['1_post']}"
                                                                                   f" {poBoxValues['1_stat']}")
                    self.po_boxes_invested[poBoxValues['Name']]['Bonus2String'] = (f"{poBoxValues['2_pre']}"
                                                                                   f"{self.po_boxes_invested[poBoxValues['Name']]['Bonus2Value']}"
                                                                                   f"{poBoxValues['2_post']}"
                                                                                   f" {poBoxValues['2_stat']}")
                    self.po_boxes_invested[poBoxValues['Name']]['Bonus3String'] = (f"{poBoxValues['3_pre']}"
                                                                                   f"{self.po_boxes_invested[poBoxValues['Name']]['Bonus3Value']}"
                                                                                   f"{poBoxValues['3_post']}"
                                                                                   f" {poBoxValues['3_stat']}")
            except:
                self.po_boxes_invested[poBoxValues['Name']] = {
                    'Level': 0,
                    'Bonus1Value': 0,
                    'Bonus1String': '',
                    'Bonus2Value': 0,
                    'Bonus2String': '',
                    'Bonus3Value': 0,
                    'Bonus3String': '',
                }

        self.apoc_dict: dict = {
            name: {
                **{f"Basic W{i} Enemies": list() for i in range(1, 7)},
                "Easy Extras": [],
                "Medium Extras": [],
                "Difficult Extras": [],
                "Insane": [],
                "Impossible": [],
                "Total": 0,
            }
            for name in ("ZOW", "CHOW", "MEOW")
        }
        self.equipment = Equipment(raw_data, character_index, self.combat_level >= 1)

        self.setPolytheismLink()

    def addUnmetApoc(self, apocType: str, apocRating: str, mapInfoList: list):
        self.apoc_dict[apocType][apocRating].append(mapInfoList)

    def increaseApocTotal(self, apocType: str):
        self.apoc_dict[apocType]["Total"] += 1

    def sortApocByProgression(self):
        for apocType, difficulties in self.apoc_dict.items():
            for difficulty, enemies in difficulties.items():
                if difficulty != "Total":
                    if len(enemies) > 0:
                        difficulties[difficulty] = sorted(
                            enemies, key=lambda item: item[2], reverse=True
                        )

    def setDivinityStyle(self, styleName: str):
        self.divinity_style = styleName

    def setDivinityLink(self, linkName: str):
        self.divinity_link = linkName

    def setPolytheismLink(self):
        if self.class_name == "Elemental Sorcerer":
            try:
                current_preset_level = self.current_preset_talents.get("505", 0)
                if current_preset_level > 0:
                    self.current_polytheism_link = divinity_divinitiesDict[(current_preset_level % 10) - 1]['Name']  #Dict starts at 1 for Snake, not 0
            except:
                pass
            try:
                secondary_preset_level = self.secondary_preset_talents.get("505", 0)
                if secondary_preset_level > 0:
                    self.secondary_polytheism_link = divinity_divinitiesDict[(secondary_preset_level % 10) - 1]['Name']  #Dict starts at 1 for Snake, not 0
            except:
                pass

    def setFamilyGuyBonus(self, value: float):
        self.family_guy_bonus = value

    def setSymbolsOfBeyondMax(self, value: int):
        self.symbols_of_beyond = 1 + value if value > 0 else 0

    def increase_max_talents_over_books(self, value: int):
        try:
            self.max_talents_over_books += value
        except:
            pass

    def __str__(self):
        return self.character_name

    def __int__(self):
        return self.character_index

    def __bool__(self):
        """
        If someone creates a character but never logs into them,
        that character will have no levels available in the JSON.
        The code to find combat and skill levels defaults to 0s when that scenario happens.
        This will make sure the character has been logged into before.
        """
        return self.combat_level >= 1


class WorldName(Enum):
    PINCHY = "Pinchy"
    GENERAL = "General"
    WORLD1 = "World 1"
    WORLD2 = "World 2"
    WORLD3 = "World 3"
    WORLD4 = "World 4"
    WORLD5 = "World 5"
    WORLD6 = "World 6"
    BLUNDER_HILLS = "Blunder Hills"
    YUMYUM_DESERT = "Yum-Yum Desert"
    FROSTBITE_TUNDRA = "Frostbite Tundra"
    HYPERION_NEBULA = "Hyperion Nebula"
    SMOLDERIN_PLATEAU = "Smolderin' Plateau"
    SPIRITED_VALLEY = "Spirited Valley"


class AdviceBase:
    """
    Args:
        **extra: a dict of extra information that hasn't been accounted for yet
    """

    _children = "_true"
    _collapse = None
    _true = [True]
    name = ""

    def __init__(self, collapse: bool | None = None, **extra):
        # assign all extra kwargs as a field on the object
        self._collapse: bool | None = collapse
        for k, v in extra.items():
            setattr(self, k, v)

    def __bool__(self) -> bool:
        children = getattr(self, self._children, list())
        if isinstance(children, dict):
            children = sum(children.values(), list())
        return any(filter(bool, children))

    def __str__(self) -> str:
        return self.name

    @property
    def collapse(self) -> bool:
        return self._collapse if self._collapse is not None else not bool(self)

    @collapse.setter
    def collapse(self, _value: bool):
        self._collapse = _value


class LabelBuilder:
    wrapper = "span"

    def __init__(self, label):
        matches = re.findall(r"\{\{.+?}}", label)

        if not matches:
            self.label = label
            return

        for match in matches:
            text, url = match.strip("{} ").split("|")
            link = f'<a href="{url}">{text}</a>'

            label = label.replace(match, link)

        self.label = f"<{self.wrapper}>{label}</{self.wrapper}>"


class Advice(AdviceBase):
    """
    Args:
        label (str): the display name of the advice
        picture_class (str): CSS class to link the image icon to the advice, e.g. 'bean-slices'
        progression: numeric (usually), how far towards the goal did the item progress?
        goal: the target level or amount of the advice
        unit (str): if there is one, usually "%"
    """

    def __init__(self, label: str, picture_class: str, progression: Any = "", goal: Any = "", unit: str = "", value_format: str = "{value}{unit}", resource: str = "",
                 **extra):
        super().__init__(**extra)

        self.label: str = label if extra.get("as_link") else LabelBuilder(label).label
        if picture_class and picture_class[0].isdigit():
            picture_class = f"x{picture_class}"
        self.picture_class: str = picture_class
        self.progression: str = str(progression)
        self.goal: str = str(goal)
        self.unit: str = unit
        self.value_format: str = value_format
        self.resource: str = kebab(resource)

        if self.unit:
            if self.progression:
                self.progression = self.value_format.format(
                    value=self.progression, unit=self.unit
                )
            if self.goal:
                self.goal = self.value_format.format(value=self.goal, unit=self.unit)

    @property
    def css_class(self) -> str:
        name = kebab(self.picture_class)
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

    def __init__(
        self,
        tier: str,
        pre_string: str,
        post_string: str = "",
        formatting: str = "",
        picture_class: str = "",
        collapse: bool | None = None,
        advices: list[Advice] | dict[str, list[Advice]] = [],
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.tier: str = str(tier)
        self.pre_string: str = pre_string
        self.post_string: str = post_string
        self.formatting: str = formatting
        self._picture_class: str = picture_class
        self.advices = advices

    def __str__(self) -> str:
        return ", ".join(map(str, self.advices))

    @property
    def advices(self):
        return self._advices

    @advices.setter
    def advices(self, _advices):
        self._advices = (
            {"default": _advices} if isinstance(_advices, list) else _advices
        )

    @property
    def picture_class(self) -> str:
        name = kebab(self._picture_class)
        return name

    @property
    def heading(self) -> str:
        text = ""
        if self.tier:
            text += f"Tier {self.tier}"
            if self.pre_string:
                text += " - "
        text += self.pre_string
        if text:
            text += ":"

        return text

    def _is_valid_operand(self, other):
        return all(hasattr(other, field) for field in self.__compare_by)

    def _coerce_to_int(self, field):
        try:
            return int(getattr(self, field))
        except ValueError:
            return 999

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return all(
            self._coerce_to_int(field) == other._coerce_to_int(field)
            for field in self.__compare_by
        )

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return all(
            self._coerce_to_int(field) < other._coerce_to_int(field)
            for field in self.__compare_by
        )

    def remove_empty_subgroups(self):
        if isinstance(self.advices, list):
            self.advices = [value for value in self.advices if value]
        if isinstance(self.advices, dict):
            self.advices = {key: value for key, value in self.advices.items() if value}

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
        groups: list[AdviceGroup] = [],
        pinchy_rating: int = 0,
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.name: str = name
        self.tier: str = tier
        self._raw_header: str = header
        self.picture: str = picture
        self._groups: list[AdviceGroup] = groups
        self.pinchy_rating: int = pinchy_rating

    @property
    def header(self) -> str:
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

    def __init__(
        self,
        name: WorldName,
        collapse: bool | None = None,
        sections: list[AdviceSection] = list(),
        banner: str = "",
        title: str = "",
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.name: str = name.value
        self.sections: list[AdviceSection] = sections
        self.banner: str = banner
        self.title: str = title

    @property
    def id(self):
        return kebab(self.name)


greenStackAmount = 10**7
gstackable_codenames = [item for items in expectedStackables.values() for item in items]
gstackable_codenames_expected = [
    item for items in list(expectedStackables.values())[:-1] for item in items
]
quest_items_codenames = expectedStackables["Missable Quest Items"]


class Asset:
    def __init__(self, codename: str, amount: float, name: str = ""):
        self.name: str = name if name else getItemDisplayName(codename)
        self.codename: str = codename if codename else getItemCodeName(name)
        self.amount: float = amount
        self.greenstacked: bool = self.amount >= greenStackAmount
        self.progression: int = self.amount * 100 // greenStackAmount
        self.quest: str = ""

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.codename or other == self.name

    def __str__(self):
        return f"{self.name}: {self.amount}"

    def __repr__(self):
        return f"<class {self.__class__.__name__}: {self.__str__()}>"

    def __hash__(self):
        return str(self.__dict__).__hash__()


class Assets(dict):
    def __init__(self, assets: dict[str, int]):
        self.tiers = greenstack_progressionTiers
        super().__init__(
            tuple(
                (codename, Asset(codename, count)) for codename, count in assets.items()
            )
        )

    def get(self, item, default=None):
        return super().get(item, default if default else Asset(item, 0))

    @property
    def items_gstacked(self) -> dict[str, Asset]:
        """Not used since it includes the "Cheater" group"""
        return {asset.codename: asset for asset in self.values() if asset.greenstacked}

    @property
    def items_gstacked_expected(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items_gstacked.items()
            if codename in gstackable_codenames
        }

    @property
    def items_gstacked_cheater(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items_gstacked.items()
            if codename not in gstackable_codenames_expected
        }

    @property
    def items_gstacked_unprecedented(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items_gstacked.items()
            if codename not in gstackable_codenames
        }

    @property
    def items_gstackable(self) -> dict[str, Asset]:
        """Not used since it includes the "Cheater" group"""
        return {
            codename: asset
            for codename, asset in self.items()
            if codename in gstackable_codenames and not asset.greenstacked
        }

    @property
    def items_gstackable_expected(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items()
            if codename in gstackable_codenames_expected and not asset.greenstacked
        }

    @property
    def items_gstackable_tiered(self) -> dict[int, dict[str, list[Asset]]]:
        tiered = dict()

        for tier, categories in self.tiers.items():
            categorised = dict()
            for category, items in categories.items():
                item_list = [
                    self.get(item)
                    for item in items
                    if item in self.items_gstackable_expected
                    and self.get(item) not in self.quest_items_missed
                ]
                if item_list:
                    categorised[category] = sorted(item_list, key=lambda item: item.progression, reverse=True)
            if categorised:
                tiered["Timegated" if tier == 0 else tier] = categorised

        return tiered

    @property
    def quest_items(self) -> set[Asset]:
        return {self.get(codename) for codename in quest_items_codenames}

    @property
    def quest_items_gstacked(self) -> set[Asset]:
        return {asset for asset in self.quest_items if asset.greenstacked}

    @property
    def quest_items_gstackable(self) -> set[Asset]:
        return self.quest_items.difference(self.quest_items_gstacked)

    @property
    def quest_items_missed(self) -> set[Asset]:
        return self.quest_items.difference(self.quest_items_gstacked)


class Card:
    def __init__(self, codename, name, cardset, count, coefficient):
        self.codename = codename
        self.count = ceil(float(count))
        self.cardset = cardset
        self.name = name
        self.coefficient = coefficient
        self.star = self.getStars()
        self.css_class = name + " Card"
        self.diff_to_next = (
            ceil(self.getCardsForStar(self.star + 1)) or sys.maxsize
        ) - self.count

    def getStars(self):
        return next(
            (
                i
                for i in range(5, -1, -1)
                if self.count >= round(self.getCardsForStar(i))
            ),
            -1,
        )

    def getCardsForStar(self, star):
        """
        0 stars always requires 1 card
        1 star is set per enemy
        2 stars = 3x additional what 1star took, for a total of 4x (2^2)
        3 stars = 5x additional what 1star took, for a total of 4+5 = 9x (3^2)
        4 stars = 16x additional what 1star took, for a total of 9+16 = 25x (5^2)
        5 stars = 459 additional what 1star took, for a total of 25+459 = 484x (22^2)
        """

        tier_coefficient = {
            # cchiz is ... special? ... who knows why...
            5: 22 if self.name != "Chaotic Chizoar" else 6,
            4: 5,
            3: 3,
            2: 2,
            1: 1,
        }.get(star, 0)

        return (self.coefficient * tier_coefficient**2) + 1

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.name}, {self.count}, {self.star}-star]"


@session_singleton
class Account:
    _key_cards = "Cards0"

    def __init__(self, json_data, run_type="web"):
        self.raw_data = (
            json.loads(json_data) if isinstance(json_data, str) else json_data
        )
        self._parse_wave_1(run_type)
        self._calculate_wave_1()
        self._calculate_wave_2()

    def _parse_wave_1(self, run_type):
        self._parse_switches()
        self._parse_characters(run_type)
        self._parse_general()
        self._parse_w1()
        self._parse_w2()
        self._parse_w3()
        self._parse_w4()
        self._parse_w5()
        self._parse_w6()

    def _parse_switches(self):
        # AutoLoot
        if g.autoloot:
            self.autoloot = True
        elif self.raw_data.get("AutoLoot", 0) == 1:
            self.autoloot = True
            g.autoloot = True
        else:
            self.autoloot = False

        # Companions
        self.sheepie_owned = g.sheepie
        self.doot_owned = g.doot
        self.riftslug_owned = g.riftslug
        if not self.doot_owned or not self.sheepie_owned or not self.riftslug_owned:
            rawCompanions = self.raw_data.get('companion', [])
            if rawCompanions:
                for companionInfo in rawCompanions.get('l', []):
                    companionID = int(companionInfo.split(',')[0])
                    if companionID == 0:
                        self.doot_owned = True
                        g.doot = True
                    if companionID == 1:
                        self.riftslug_owned = True
                        g.riftslug = True
                    if companionID == 4:
                        self.sheepie_owned = True
                        g.sheepie = True

    def _parse_characters(self, run_type):
        playerCount, playerNames, playerClasses, characterDict, perSkillDict = getCharacterDetails(
            self.raw_data, run_type
        )
        self.names = playerNames
        self.playerCount = playerCount
        self.classes = playerClasses
        self.all_characters: list[Character] = [Character(self.raw_data, **char) for char in characterDict.values()]
        self.safe_characters: list[Character] = [char for char in self.all_characters if char]  # Use this if touching raw_data instead of all_characters
        self.safe_playerIndexes: list[int] = [char.character_index for char in self.all_characters if char]
        self.all_skills = perSkillDict
        self.all_quests = [safe_loads(self.raw_data.get(f"QuestComplete_{i}", "{}")) for i in range(self.playerCount)]
        self.max_toon_count = 10  # OPTIMIZE: find a way to read this from somewhere

    def _parse_general(self):
        # General / Multiple uses
        self.gemshop = {}
        self.family_bonuses = {}
        for className in familyBonusesDict.keys():
            # Create the skeleton for all current classes, with level and value of 0
            self.family_bonuses[className] = {'Level': 0, 'Value': 0}
        for char in self.safe_characters:
            for className in [char.base_class, char.sub_class, char.elite_class]:
                if className in familyBonusesDict:
                    if char.combat_level > self.family_bonuses[className]['Level']:
                        self.family_bonuses[className]['Level'] = char.combat_level
        for className in self.family_bonuses.keys():
            try:
                self.family_bonuses[className]['Value'] = lavaFunc(
                    familyBonusesDict[className]['funcType'],
                    self.family_bonuses[className]['Level'] - familyBonusesDict[className]['levelDiscount'],
                    familyBonusesDict[className]['x1'],
                    familyBonusesDict[className]['x2'])
            except:
                self.family_bonuses[className]['Value'] = 0
            self.family_bonuses[className]['DisplayValue'] = (f"{'+' if familyBonusesDict[className]['PrePlus'] else ''}"
                                                              f"{self.family_bonuses[className]['Value']:.2f}"
                                                              f"{familyBonusesDict[className]['PostDisplay']}"
                                                              f" {familyBonusesDict[className]['Stat']}")

        self.raw_optlacc_dict = safe_loads(self.raw_data.get("OptLacc", {}))

        self.dungeon_upgrades = {}
        raw_dungeon_upgrades = safe_loads(self.raw_data.get('DungUpg', []))
        if raw_dungeon_upgrades:
            try:
                self.dungeon_upgrades["MaxWeapon"] = raw_dungeon_upgrades[3][0]
                self.dungeon_upgrades["MaxArmor"] = [raw_dungeon_upgrades[3][4], raw_dungeon_upgrades[3][5], raw_dungeon_upgrades[3][6],
                                                     raw_dungeon_upgrades[3][7]]
                self.dungeon_upgrades["MaxJewelry"] = [raw_dungeon_upgrades[3][8], raw_dungeon_upgrades[3][9]]
                self.dungeon_upgrades["FlurboShop"] = raw_dungeon_upgrades[5]
                self.dungeon_upgrades["CreditShop"] = raw_dungeon_upgrades[5]
            except:
                self.dungeon_upgrades["MaxWeapon"] = 0
                self.dungeon_upgrades["MaxArmor"] = [0, 0, 0, 0]
                self.dungeon_upgrades["MaxJewelry"] = [0, 0]
                self.dungeon_upgrades["FlurboShop"] = [0, 0, 0, 0, 0, 0, 0, 0]
                self.dungeon_upgrades["CreditShop"] = [0, 0, 0, 0, 0, 0, 0, 0]

        self.achievements = {}
        raw_reg_achieves = safe_loads(self.raw_data.get('AchieveReg', []))
        for achieveIndex, achieveData in enumerate(achievementsList):
            try:
                if achieveData[0].replace('_', ' ') != "FILLERZZZ ACH":
                    self.achievements[achieveData[0].replace('_', ' ')] = raw_reg_achieves[achieveIndex] == -1
            except:
                self.achievements[achieveData[0].replace('_', ' ')] = False

        self.merits = copy.deepcopy(allMeritsDict)
        raw_merits_list = safe_loads(self.raw_data.get("TaskZZ2", []))
        for worldIndex in self.merits:
            for meritIndex in self.merits[worldIndex]:
                try:
                    self.merits[worldIndex][meritIndex]["Level"] = int(raw_merits_list[worldIndex][meritIndex])
                except:
                    continue  # Already defaulted to 0 in Consts

        self.assets = self._all_owned_items()
        self.cards = self._make_cards()
        self.guildBonuses = {}
        raw_guild = self.raw_data.get('guildData', {}).get('stats', [])
        for bonusIndex, bonusName in enumerate(guildBonusesList):
            try:
                self.guildBonuses[bonusName] = raw_guild[0][bonusIndex]
            except:
                self.guildBonuses[bonusName] = 0

    def _parse_w1(self):
        self._parse_w1_starsigns()
        self._parse_w1_forge()
        self._parse_w1_bribes()
        self._parse_w1_stamps()
        self._parse_w1_owl()

    def _parse_w1_starsigns(self):
        self.star_signs = {}
        raw_star_signs = safe_loads(self.raw_data.get("StarSg", {}))
        for signIndex, signValuesDict in starsignsDict.items():
            self.star_signs[signValuesDict['Name']] = {
                'Unlocked': False,
                'Index': signIndex,
                'Passive': signValuesDict['Passive'],
                '1_Value': signValuesDict.get('1_Value', 0),
                '1_Stat': signValuesDict.get('1_Stat', ''),
                '2_Value': signValuesDict.get('2_Value', 0),
                '2_Stat': signValuesDict.get('2_Stat', ''),
                '3_Value': signValuesDict.get('3_Value', 0),
                '3_Stat': signValuesDict.get('3_Stat', ''),
            }
            try:
                # Some StarSigns are saved as strings "1" to mean unlocked.
                # The names in the JSON also have underscores instead of spaces
                self.star_signs[signValuesDict['Name']]['Unlocked'] = int(raw_star_signs[signValuesDict['Name'].replace(" ", "_")]) > 0
            except:
                pass

    def _parse_w1_forge(self):
        self.forge_upgrades = copy.deepcopy(forgeUpgradesDict)
        raw_forge_upgrades = self.raw_data.get("ForgeLV", [])
        for upgradeIndex, upgrade in enumerate(raw_forge_upgrades):
            try:
                self.forge_upgrades[upgradeIndex]["Purchased"] = upgrade
            except:
                continue  # Already defaulted to 0 in Consts

    def _parse_w1_bribes(self):
        self.bribes = {}
        raw_bribes_list = safe_loads(self.raw_data.get("BribeStatus", []))
        bribeIndex = 0
        for bribeSet in bribesDict:
            self.bribes[bribeSet] = {}
            for bribeName in bribesDict[bribeSet]:
                try:
                    self.bribes[bribeSet][bribeName] = int(raw_bribes_list[bribeIndex])
                except:
                    self.bribes[bribeSet][bribeName] = -1  # -1 means unavailable for purchase, 0 means available, and 1 means purchased
                bribeIndex += 1

    def _parse_w1_stamps(self):
        self.stamps = {}
        self.stamp_totals = {"Total": 0}
        for stampType in stampTypes:
            self.stamp_totals[stampType] = 0
        raw_stamps_list = safe_loads(self.raw_data.get("StampLv", [{}, {}, {}]))
        raw_stamps_dict = {}
        for stampTypeIndex, stampTypeValues in enumerate(raw_stamps_list):
            raw_stamps_dict[int(stampTypeIndex)] = {}
            for stampKey, stampValue in stampTypeValues.items():
                if stampKey != "length":
                    raw_stamps_dict[int(stampTypeIndex)][int(stampKey)] = int(stampValue)
        raw_stamp_max_list = safe_loads(self.raw_data.get("StampLvM", {0: {}, 1: {}, 2: {}}))
        raw_stamp_max_dict = {}
        for stampTypeIndex, stampTypeValues in enumerate(raw_stamp_max_list):
            raw_stamp_max_dict[int(stampTypeIndex)] = {}
            for stampKey, stampValue in stampTypeValues.items():
                if stampKey != "length":
                    try:
                        raw_stamp_max_dict[int(stampTypeIndex)][int(stampKey)] = int(stampValue)
                    except Exception as reason:
                        print(f"Unexpected stampTypeIndex {stampTypeIndex} or stampKey {stampKey} or stampValue: {stampValue}: {reason}")
                        try:
                            raw_stamp_max_dict[int(stampTypeIndex)][int(stampKey)] = 0
                            print(f"Able to set the value of stamp {stampTypeIndex}-{stampKey} to 0. Hopefully no accuracy was lost.")
                        except:
                            print(f"Couldn't set the value to 0, meaning it was the Index or Key that was bad. You done messed up, cowboy.")
        for stampType in stampsDict:
            for stampIndex, stampValuesDict in stampsDict[stampType].items():
                try:
                    self.stamps[stampValuesDict['Name']] = {
                        "Index": int(stampIndex),
                        "Material": stampValuesDict['Material'],
                        "Level": int(floor(raw_stamps_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))),
                        "Max": int(floor(raw_stamp_max_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))),
                        "Delivered": int(floor(raw_stamp_max_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))) > 0,
                        "StampType": stampType,
                        "Value": lavaFunc(
                            stampValuesDict['funcType'],
                            int(floor(raw_stamps_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))),
                            stampValuesDict['x1'],
                            stampValuesDict['x2'],
                        )
                    }
                    self.stamp_totals["Total"] += self.stamps[stampValuesDict['Name']]["Level"]
                    self.stamp_totals[stampType] += self.stamps[stampValuesDict['Name']]["Level"]
                except:
                    self.stamps[stampValuesDict['Name']] = {
                        "Index": stampIndex,
                        "Level": 0,
                        "Max": 0,
                        "Delivered": False,
                        "StampType": stampType,
                        "Value": 0
                    }

    def _parse_w1_owl(self):
        self.owl = {}
        try:
            self.owl['FeatherGeneration'] = self.raw_optlacc_dict[254]
            self.owl['BonusesOfOrion'] = self.raw_optlacc_dict[255]
            self.owl['FeatherRestarts'] = self.raw_optlacc_dict[258]
            self.owl['MegaFeathersOwned'] = self.raw_optlacc_dict[262]
        except:
            self.owl['FeatherGeneration'] = 0
            self.owl['BonusesOfOrion'] = 0
            self.owl['FeatherRestarts'] = 0
            self.owl['MegaFeathersOwned'] = 0

    def _parse_w2(self):
        self._parse_w2_vials()
        self._parse_w2_cauldrons()
        self._parse_w2_bubbles()
        self._parse_w2_p2w()
        self._parse_w2_arcade()

    def _parse_w2_vials(self):
        self.alchemy_vials = {}
        try:
            manualVialsAdded = 0
            raw_alchemy_vials = safe_loads(self.raw_data.get("CauldronInfo", [0, 0, 0, 0, {}])[4])
            if "length" in raw_alchemy_vials:
                del raw_alchemy_vials["length"]
            while len(raw_alchemy_vials) < max_IndexOfVials:
                raw_alchemy_vials[int(max_IndexOfVials - manualVialsAdded)] = 0
                manualVialsAdded += 1
            for vialKey, vialValue in raw_alchemy_vials.items():
                try:
                    self.alchemy_vials[getReadableVialNames(vialKey)] = {
                        "Level": int(vialValue),
                        "Value": lavaFunc(
                            vialsDict.get(int(vialKey)).get("funcType"),
                            int(vialValue),
                            vialsDict.get(int(vialKey)).get("x1"),
                            vialsDict.get(int(vialKey)).get("x2")
                        )
                    }
                except:
                    self.alchemy_vials[getReadableVialNames(vialKey)] = {"Level": 0, "Value": 0}
        except:
            pass
        self.maxed_vials = 0
        for vial in self.alchemy_vials.values():
            if vial.get("Level", 0) >= 13:
                self.maxed_vials += 1

    def _parse_w2_cauldrons(self):
        self.alchemy_cauldrons = {
            'OrangeUnlocked': 0,
            'GreenUnlocked': 0,
            'PurpleUnlocked': 0,
            'YellowUnlocked': 0,
            'TotalUnlocked': 0,
        }

    def _parse_w2_bubbles(self):
        self.alchemy_bubbles = {}

        # Set defaults to 0
        for cauldronIndex in bubblesDict:
            for bubbleIndex in bubblesDict[cauldronIndex]:
                self.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']] = {
                    "CauldronIndex": cauldronIndex,
                    "BubbleIndex": bubbleIndex,
                    "Level": 0,
                    "BaseValue": 0,
                    "Material": getItemDisplayName(bubblesDict[cauldronIndex][bubbleIndex]['Material'])
                }

        # Try to read player levels and calculate base value
        try:
            all_raw_bubbles = [self.raw_data["CauldronInfo"][0], self.raw_data["CauldronInfo"][1], self.raw_data["CauldronInfo"][2],
                               self.raw_data["CauldronInfo"][3]]
            for cauldronIndex in bubblesDict:
                for bubbleIndex in bubblesDict[cauldronIndex]:
                    try:
                        self.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']]['Level'] = int(all_raw_bubbles[cauldronIndex][str(bubbleIndex)])
                        self.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']]['BaseValue'] = lavaFunc(
                            bubblesDict[cauldronIndex][bubbleIndex]["funcType"],
                            int(all_raw_bubbles[cauldronIndex][str(bubbleIndex)]),
                            bubblesDict[cauldronIndex][bubbleIndex]["x1"],
                            bubblesDict[cauldronIndex][bubbleIndex]["x2"])
                        if int(all_raw_bubbles[cauldronIndex][str(bubbleIndex)]) > 0:
                            self.alchemy_cauldrons['TotalUnlocked'] += 1
                            #Keep track of cauldron counts
                            if cauldronIndex == 0:
                                self.alchemy_cauldrons['OrangeUnlocked'] += 1
                            elif cauldronIndex == 1:
                                self.alchemy_cauldrons['GreenUnlocked'] += 1
                            elif cauldronIndex == 2:
                                self.alchemy_cauldrons['PurpleUnlocked'] += 1
                            elif cauldronIndex == 3:
                                self.alchemy_cauldrons['YellowUnlocked'] += 1
                    except:
                        continue  # Level and BaseValue already defaulted to 0 above
        except:
            pass

    def _parse_w2_p2w(self):
        self.alchemy_p2w = {
            "Sigils": sigilsDict
        }
        raw_p2w_list = safe_loads(self.raw_data.get("CauldronP2W", []))
        if raw_p2w_list:
            for subElementIndex, subElementValue in enumerate(raw_p2w_list):
                if not isinstance(subElementValue, list):
                    raw_p2w_list[subElementIndex] = [subElementValue]
            try:
                self.alchemy_p2w["Cauldrons"] = raw_p2w_list[0]
            except:
                self.alchemy_p2w["Cauldrons"] = [0] * 12
            try:
                self.alchemy_p2w["Liquids"] = raw_p2w_list[1]
            except:
                self.alchemy_p2w["Liquids"] = [0] * 8
            try:
                self.alchemy_p2w["Vials"] = raw_p2w_list[2]
            except:
                self.alchemy_p2w["Vials"] = [0] * 2
            try:
                self.alchemy_p2w["Player"] = raw_p2w_list[3]
            except:
                self.alchemy_p2w["Player"] = [0] * 2
            for sigilName in self.alchemy_p2w["Sigils"]:
                try:
                    self.alchemy_p2w["Sigils"][sigilName]["PlayerHours"] = float(raw_p2w_list[4][self.alchemy_p2w["Sigils"][sigilName]["Index"]])
                    self.alchemy_p2w["Sigils"][sigilName]["Level"] = raw_p2w_list[4][self.alchemy_p2w["Sigils"][sigilName]["Index"] + 1] + 1
                except Exception as reason:
                    print(f"{reason}")
                    pass  # Already defaulted to 0s in consts.sigilsDict

    def _parse_w2_arcade(self):
        self.arcade = {}
        raw_arcade_upgrades = safe_loads(self.raw_data.get("ArcadeUpg", []))
        for upgradeIndex, upgradeLevel in enumerate(raw_arcade_upgrades):
            try:
                self.arcade[upgradeIndex] = {
                    "Level": upgradeLevel,
                    "Value": lavaFunc(
                        arcadeBonuses.get(upgradeIndex).get("funcType"),
                        upgradeLevel,
                        arcadeBonuses.get(upgradeIndex).get("x1"),
                        arcadeBonuses.get(upgradeIndex).get("x2")
                    )
                }
                self.arcade[upgradeIndex][
                    "Display"] = f"+{self.arcade[upgradeIndex]['Value']:.2f}{arcadeBonuses[upgradeIndex]['displayType']} {arcadeBonuses[upgradeIndex]['Stat']}"
            except:
                self.arcade[upgradeIndex] = {
                    "Level": upgradeLevel,
                    "Value": 0
                }
                try:
                    self.arcade[upgradeIndex][
                        "Display"] = f"+{self.arcade[upgradeIndex]['Value']}{arcadeBonuses[upgradeIndex]['displayType']} {arcadeBonuses[upgradeIndex]['Stat']}"
                except:
                    self.arcade[upgradeIndex]["Display"] = f"+% UnknownUpgrade{upgradeIndex}"

    def _parse_w3(self):
        self._parse_w3_buildings()
        self._parse_w3_library()
        self._parse_w3_deathnote()
        self._parse_w3_equinox_dreams()
        self._parse_w3_equinox_bonuses()
        self._parse_w3_shrines()
        self._parse_w3_atom_collider()
        self._parse_w3_prayers()
        self._parse_w3_saltlick()

    def _parse_w3_buildings(self):
        self.construction_buildings = {}
        raw_buildings_list = safe_loads(self.raw_data.get("Tower", []))
        for buildingIndex, buildingValuesDict in buildingsDict.items():
            try:
                self.construction_buildings[buildingValuesDict['Name']] = {
                    'Level': int(raw_buildings_list[buildingIndex]),
                    'MaxLevel': buildingValuesDict['BaseMaxLevel'],
                    'Image': buildingValuesDict['Image'],
                    'Type': buildingValuesDict['Type'],
                }
            except:
                self.construction_buildings[buildingValuesDict['Name']] = {
                    'Level': 0,
                    'MaxLevel': buildingValuesDict['BaseMaxLevel'],
                    'Image': buildingValuesDict['Image'],
                    'Type': buildingValuesDict['Type'],
                }

    def _parse_w3_library(self):
        self.library = {}

    def _parse_w3_deathnote(self):
        self.rift_meowed = False
        self.meowBBIndex = 0

    def _parse_w3_equinox_dreams(self):
        self.equinox_unlocked = self.achievements['Equinox Visitor']
        self.equinox_dreams = [True]
        raw_equinox_dreams = safe_loads(self.raw_data.get("WeeklyBoss", {}))
        self.equinox_dreams += [
            float(raw_equinox_dreams.get(f'd_{i}', 0)) == -1
            for i in range(maxDreams)
        ]
        self.total_dreams_completed = sum(self.equinox_dreams) - 1  # Remove the placeholder in 0th index
        self.total_equinox_bonuses_unlocked = 0
        self.remaining_equinox_dreams_unlocking_new_bonuses = []
        for dreamNumber in dreamsThatUnlockNewBonuses:
            if self.equinox_dreams[dreamNumber] == True:
                self.total_equinox_bonuses_unlocked += 1
            else:
                self.remaining_equinox_dreams_unlocking_new_bonuses.append(dreamNumber)

    def _parse_w3_equinox_bonuses(self):
        self.equinox_bonuses = {}
        raw_equinox_bonuses = safe_loads(self.raw_data.get("Dream", [0] * 30))
        for bonusIndex, bonusValueDict in equinoxBonusesDict.items():
            upgradeName = bonusValueDict['Name']
            self.equinox_bonuses[upgradeName] = {
                'PlayerMaxLevel': 0,  # This will get updated in the next Try block. Do not fret, dear reader.
                'Category': bonusValueDict['Category'],
                'Unlocked': self.total_equinox_bonuses_unlocked >= bonusIndex - 2,
                'FinalMaxLevel': bonusValueDict['FinalMaxLevel'],
                'RemainingUpgrades': []
            }
            try:
                self.equinox_bonuses[upgradeName]['CurrentLevel'] = int(raw_equinox_bonuses[bonusIndex])
            except:
                self.equinox_bonuses[upgradeName]['CurrentLevel'] = 0
            if self.equinox_bonuses[upgradeName]['Unlocked']:
                self.equinox_bonuses[upgradeName]['PlayerMaxLevel'] = bonusValueDict['BaseLevel']
                for dreamIndex, bonusMaxLevelIncrease in bonusValueDict['MaxLevelIncreases'].items():
                    if self.equinox_dreams[dreamIndex]:
                        self.equinox_bonuses[upgradeName]['PlayerMaxLevel'] += bonusMaxLevelIncrease
                    else:
                        self.equinox_bonuses[upgradeName]['RemainingUpgrades'].append(dreamIndex)

    def _parse_w3_shrines(self):
        self.shrines = {}
        raw_shrines_list = safe_loads(self.raw_data.get("Shrine", []))
        for shrineIndex, shrineName in enumerate(shrinesList):
            try:
                self.shrines[shrineName] = {
                    "MapIndex": int(raw_shrines_list[shrineIndex][0]),
                    1: int(raw_shrines_list[shrineIndex][1]),
                    2: int(raw_shrines_list[shrineIndex][2]),
                    "Level": int(raw_shrines_list[shrineIndex][3]),
                    "Hours": float(raw_shrines_list[shrineIndex][4]),
                    5: int(raw_shrines_list[shrineIndex][5])
                }
            except:
                self.shrines[shrineName] = {
                    "MapIndex": 0,
                    1: 0,
                    2: 0,
                    "Level": 0,
                    "Hours": 0.0,
                    5: 0
                }

    def _parse_w3_atom_collider(self):
        self.atom_collider = {}
        try:
            self.atom_collider['Particles'] = self.raw_data.get("Divinity", {})[39]
        except:
            self.atom_collider['Particles'] = "Unknown"  #0.0

        try:
            self.atom_collider['StorageLimit'] = colliderStorageLimitList[self.raw_optlacc_dict[133]]  #colliderStorageLimitList[self.raw_optlacc_dict[132]]
        except:
            self.atom_collider['StorageLimit'] = "Unknown"  #colliderStorageLimitList[0]

        try:
            self.atom_collider['OnOffStatus'] = bool(self.raw_optlacc_dict[132])
        except:
            self.atom_collider['OnOffStatus'] = True  #0

        self._parse_w3_atoms()

    def _parse_w3_atoms(self):
        self.atom_collider['Atoms'] = {}
        raw_atoms_list = safe_loads(self.raw_data.get("Atoms", []))
        for atomIndex, atomInfoList in enumerate(atomsList):
            try:
                self.atom_collider['Atoms'][atomInfoList[0]] = {
                    'Level': int(raw_atoms_list[atomIndex]),
                    'MaxLevel': 20,
                    'AtomInfo1': atomInfoList[1],
                    'AtomInfo2': atomInfoList[2],
                    'AtomInfo3': atomInfoList[3],
                    'AtomInfo4': atomInfoList[4],
                    'BaseCostToUpgrade': 0,
                    'DiscountedCostToUpgrade': 0,
                    'BaseCostToMax': 0,
                    'DiscountedCostToMax': 0
                }
            except:
                self.atom_collider['Atoms'][atomInfoList[0]] = {
                    'Level': 0,
                    'MaxLevel': 20,
                    'AtomInfo1': atomInfoList[1],
                    'AtomInfo2': atomInfoList[2],
                    'AtomInfo3': atomInfoList[3],
                    'AtomInfo4': atomInfoList[4],
                    'BaseCostToUpgrade': 0,
                    'DiscountedCostToUpgrade': 0,
                    'BaseCostToMax': 0,
                    'DiscountedCostToMax': 0
                }

    def _parse_w3_prayers(self):
        self.prayers = {}
        raw_prayers_list = safe_loads(self.raw_data.get("PrayOwned", []))
        for prayerIndex, prayerValuesDict in prayersDict.items():
            self.prayers[prayerValuesDict['Name']] = {
                'DisplayName': prayerValuesDict['Display'],
                'Material': prayerValuesDict['Material'],
                'Level': 0,
                'BonusValue': 0,
                'BonusString': f"Level at least once to receive the bonus!",
                'CurseValue': 0,
                'CurseString': f"Level at least once to receive the curse!"
            }
            try:
                self.prayers[prayerValuesDict['Name']]['Level'] = int(raw_prayers_list[prayerIndex])
                self.prayers[prayerValuesDict['Name']]['BonusValue'] = lavaFunc(
                    prayerValuesDict['bonus_funcType'],
                    self.prayers[prayerValuesDict['Name']]['Level'],
                    prayerValuesDict['bonus_x1'],
                    prayerValuesDict['bonus_x2']) if self.prayers[prayerValuesDict['Name']]['Level'] > 0 else 0
                self.prayers[prayerValuesDict['Name']]['BonusString'] = (f"{prayerValuesDict['bonus_pre']}"
                                                                         f"{self.prayers[prayerValuesDict['Name']]['BonusValue']}"
                                                                         f"{prayerValuesDict['bonus_post']}"
                                                                         f" {prayerValuesDict['bonus_stat']}")
                self.prayers[prayerValuesDict['Name']]['CurseValue'] = lavaFunc(
                    prayerValuesDict['curse_funcType'],
                    self.prayers[prayerValuesDict['Name']]['Level'],
                    prayerValuesDict['curse_x1'],
                    prayerValuesDict['curse_x2']) if self.prayers[prayerValuesDict['Name']]['Level'] > 0 else 0
                self.prayers[prayerValuesDict['Name']]['CurseString'] = (f"{prayerValuesDict['curse_pre']}"
                                                                         f"{self.prayers[prayerValuesDict['Name']]['CurseValue']}"
                                                                         f"{prayerValuesDict['curse_post']}"
                                                                         f" {prayerValuesDict['curse_stat']}")
            except:
                pass

    def _parse_w3_saltlick(self):
        self.saltlick = {}
        raw_saltlick_list = safe_loads(self.raw_data.get("SaltLick"))
        for saltlickIndex, saltlickName in enumerate(saltLickList):
            try:
                self.saltlick[saltlickName] = int(raw_saltlick_list[saltlickIndex])
            except:
                self.saltlick[saltlickName] = 0

    def _parse_w4(self):
        self._parse_w4_cooking()
        self._parse_w4_lab()
        self._parse_w4_rift()

    def _parse_w4_cooking(self):
        self.cooking = {
            'MealsUnlocked': 0,
            'MealsUnder11': 0,
            'MealsUnder30': 0,
            'PlayerMaxPlateLvl': 30,  # 30 is the default starting point
            'PlayerTotalMealLevels': 0,
            'MaxTotalMealLevels': maxMeals * maxMealLevel,
            'PlayerMissingPlateUpgrades': []
        }
        self._parse_w4_cooking_tables()
        self._parse_w4_cooking_meals()

    def _parse_w4_cooking_tables(self):
        emptyTable = [0] * 11  # Some tables only have 10 fields, others have 11. Scary.
        emptyCooking = [emptyTable for table in range(maxCookingTables)]
        raw_cooking_list = safe_loads(self.raw_data.get("Cooking", emptyCooking))
        for sublistIndex, value in enumerate(raw_cooking_list):
            if isinstance(raw_cooking_list[sublistIndex], list):
                #Pads out the length of all tables to 11 entries, to be safe.
                while len(raw_cooking_list[sublistIndex]) < 11:
                    raw_cooking_list[sublistIndex].append(0)

    def _parse_w4_cooking_meals(self):
        emptyMeal = [0] * maxMeals
        # Meals contains 4 lists of lists. The first 3 are as long as the number of plates. The 4th is general shorter.
        emptyMeals = [emptyMeal for meal in range(4)]
        raw_meals_list = safe_loads(self.raw_data.get("Meals", emptyMeals))
        for sublistIndex, value in enumerate(raw_meals_list):
            if isinstance(raw_meals_list[sublistIndex], list):
                while len(raw_meals_list[sublistIndex]) < maxMeals:
                    raw_meals_list[sublistIndex].append(0)

        # Count the number of unlocked meals, unlocked meals under 11, and unlocked meals under 30
        for mealLevel in raw_meals_list[0]:
            if mealLevel > 0:
                self.cooking['MealsUnlocked'] += 1
                self.cooking['PlayerTotalMealLevels'] += mealLevel
                if mealLevel < 11:
                    self.cooking['MealsUnder11'] += 1
                if mealLevel < 30:
                    self.cooking['MealsUnder30'] += 1

    def _parse_w4_lab(self):
        raw_lab = safe_loads(self.raw_data.get("Lab", []))
        self._parse_w4_lab_chips(raw_lab)
        self._parse_w4_lab_bonuses(raw_lab)
        self._parse_w4_jewels(raw_lab)

    def _parse_w4_lab_chips(self, raw_lab):
        self.labChips = {}
        raw_labChips_list = raw_lab
        if len(raw_labChips_list) >= 15:
            raw_labChips_list = raw_labChips_list[15]
        for labChipIndex, labChipName in enumerate(labChipsList):
            try:
                self.labChips[labChipName] = int(raw_labChips_list[labChipIndex])
            except:
                self.labChips[labChipName] = 0

    def _parse_w4_lab_bonuses(self, raw_lab):
        #TODO: Actually figure out lab :(
        self.labBonuses = {}
        for labBonusIndex, labBonusName in enumerate(labBonusesList):
            self.labBonuses[labBonusName] = {
                "Enabled": True,
                "Value": 1
            }
    def _parse_w4_jewels(self, raw_lab):
        #TODO: Account for if the jewel is actually connected.
        jewelmulti = 1+0.5+0.1*raw_lab[14][16] # Will have to be fixed when labbonuses are implemented properly. index 16 is puropal navette

        self.labJewels = {}
        for jewelIndex, jewelInfo in labJewelsDict.items():
            self.labJewels[jewelInfo["Name"]] = {
                "Enabled": bool(raw_lab[14][jewelIndex]),
                "Value": jewelInfo["BaseValue"]*jewelmulti
            }

    def _parse_w4_rift(self):
        self.rift = {
            'Unlocked': False,
            'Level': self.raw_data.get("Rift", [0])[0],
        }
        self.rift_level = self.raw_data.get("Rift", [0])[0]
        if self.rift['Level'] > 0:
            self.rift['Unlocked'] = True
        else:
            for characterIndex in range(0, len(self.all_quests)):
                if self.all_quests[characterIndex].get("Rift_Ripper1", 0) == 1:
                    self.rift['Unlocked'] = True
                    break
        self.rift['TrapBoxVacuum'] = self.rift['Level'] >= 5
        self.rift['InfiniteStars'] = self.rift['Level'] >= 10
        self.rift['SkillMastery'] = self.rift['Level'] >= 15
        self.rift['EclipseSkulls'] = self.rift['Level'] >= 20
        self.rift['StampMastery'] = self.rift['Level'] >= 25
        self.rift['EldritchArtifacts'] = self.rift['Level'] >= 30
        self.rift['VialMastery'] = self.rift['Level'] >= 35
        self.rift['ConstructionMastery'] = self.rift['Level'] >= 40
        self.rift['RubyCards'] = self.rift['Level'] >= 45

    def _parse_w5(self):
        self.gaming = {
            'BitsOwned': 0,
            'FertilizerValue': 0,
            'FertilizerSpeed': 0,
            'FertilizerCapacity': 0,
            'MutationsUnlocked': 0,
            'EvolutionChance': 0,
            'DNAOwned': 0,
            'Nugget': 0,
            'Acorns': 0,
            'PoingHighscore': 0,
            'LogbookString': "",
            'Logbook': {},
            'SuperBitsString': "",
            'SuperBits': {},
            'Envelopes': 0,
            'Imports': {}
        }
        self._parse_w5_gaming()
        self._parse_w5_gaming_sprouts()
        self._parse_w5_slab()
        self._parse_w5_sailing()
        self._parse_w5_divinity()

    def _parse_w5_gaming(self):
        raw_gaming_list = safe_loads(self.raw_data.get("Gaming", []))
        if raw_gaming_list:
            try:
                self.gaming['BitsOwned'] = raw_gaming_list[0]
                self.gaming['FertilizerValue'] = raw_gaming_list[1]
                self.gaming['FertilizerSpeed'] = raw_gaming_list[2]
                self.gaming['FertilizerCapacity'] = raw_gaming_list[3]
                self.gaming['MutationsUnlocked'] = raw_gaming_list[4]
                self.gaming['DNAOwned'] = raw_gaming_list[5]
                self.gaming['EvolutionChance'] = raw_gaming_list[7]
                self.gaming['Nugget'] = raw_gaming_list[8]
                self.gaming['Acorns'] = raw_gaming_list[9]
                self.gaming['EvolutionChance'] = raw_gaming_list[10]
                self.gaming['LogbookString'] = raw_gaming_list[11]
                self.gaming['SuperBitsString'] = raw_gaming_list[12]
                self.gaming['Envelopes'] = raw_gaming_list[13]
            except:
                pass

        for index, valuesDict in gamingSuperbitsDict.items():
            self.gaming['SuperBits'][valuesDict['Name']] = {
                'Unlocked': valuesDict['CodeString'] in self.gaming['SuperBitsString'],
                'BonusText': valuesDict['BonusText']
            }

    def _parse_w5_gaming_sprouts(self):
        # [0] through [24] = actual sprouts
        # [300, 25469746.803332243, 0, 0, 655, 70],  # [25] = Sprinkler Import
        # [315, 1335, 0, 0, 654, 383],  # [26] = Shovel Import
        # [300, 1335, 503, 711, 429.34312394215203, 237.05230565943967],  # [27] = Squirrel Import
        # [275, 287171, 26, 0, 82, 153],  # [28] = Seashell Import
        # [260, 1, 0, 0, 82, 225],  # [29] = Kitsune Roxie Import
        # [224, 1345, 0, 0, 98, 383],  # [30] = Log Import
        # [1, 842957708.5889401, 0, 0, 83, 70],  # [31] = Poing Import
        # [160, 23, 0, 0, 77, 295],  # [32] = Snail Import
        # [0, 21884575.351264, 0, 0, 309, 210],  # [33] = Box9 Import
        # [0, 842957708.5889401, 0, 0, 0, 0],  # [34] = Box10 Import
        raw_gaming_sprouts_list = safe_loads(self.raw_data.get("GamingSprouts", []))
        try:
            self.gaming['Imports'] = {
                'Snail': {
                    'SnailRank': raw_gaming_sprouts_list[32][1]
                }
            }
        except:
            self.gaming['Imports'] = {
                'Snail': {
                    'SnailRank': 0
                }
            }

    def _parse_w5_slab(self):
        self.registered_slab = safe_loads(self.raw_data.get("Cards1", []))

    def _parse_w5_sailing(self):
        self.sailing = {"Artifacts": {}, "Boats": {}, "Captains": {}, "Islands": {}, 'IslandsDiscovered': 1, 'CaptainsOwned': 1, 'BoatsOwned': 1}
        raw_sailing_list = safe_loads(safe_loads(self.raw_data.get("Sailing", [])))  # Some users have needed to have data converted twice
        try:
            self.sailing['CaptainsOwned'] += raw_sailing_list[2][0]
            self.sailing['BoatsOwned'] += raw_sailing_list[2][1]
            self.sum_artifact_tiers = sum(raw_sailing_list[3])
        except:
            self.sum_artifact_tiers = 0
        for islandIndex, islandValuesDict in sailingDict.items():
            try:
                self.sailing['Islands'][islandValuesDict['Name']] = {
                    'Unlocked': True if raw_sailing_list[0][islandIndex] == -1 else False,
                    'Distance': islandValuesDict['Distance'],
                    'NormalTreasure': islandValuesDict['NormalTreasure'],
                    'RareTreasure': islandValuesDict['RareTreasure']
                }
                self.sailing['IslandsDiscovered'] += 1 if self.sailing['Islands'][islandValuesDict['Name']]['Unlocked'] else 0
            except:
                self.sailing['Islands'][islandValuesDict['Name']] = {
                    'Unlocked': False,
                    'Distance': islandValuesDict['Distance'],
                    'NormalTreasure': islandValuesDict['NormalTreasure'],
                    'RareTreasure': islandValuesDict['RareTreasure']
                }
            for artifactIndex, artifactValuesDict in islandValuesDict['Artifacts'].items():
                try:
                    self.sailing['Artifacts'][artifactValuesDict['Name']] = {
                        'Level': raw_sailing_list[3][artifactIndex]
                    }
                except:
                    self.sailing['Artifacts'][artifactValuesDict['Name']] = {
                        'Level': 0
                    }

    def _parse_w5_divinity(self):
        self.divinity = {
            'Divinities': copy.deepcopy(divinity_divinitiesDict),
            'DivinityLinks': {}
        }
        raw_divinity_list = safe_loads(self.raw_data.get("Divinity", []))
        while len(raw_divinity_list) < 40:
            raw_divinity_list.append(0)

        self.divinity['GodsUnlocked'] = min(10, raw_divinity_list[25])
        self.divinity['GodRank'] = max(0, raw_divinity_list[25] - 10)
        self.divinity['LowOffering'] = raw_divinity_list[26]
        self.divinity['HighOffering'] = raw_divinity_list[27]
        for divinityIndex in self.divinity['Divinities']:
            if self.divinity['GodsUnlocked'] >= divinityIndex:
                self.divinity['Divinities'][divinityIndex]["Unlocked"] = True
            # Snake has a divinityIndex of 0, Blessing level stored in 28
            self.divinity['Divinities'][divinityIndex]["BlessingLevel"] = raw_divinity_list[divinityIndex + 27]
        for character in self.safe_characters:
            try:
                character.setDivinityStyle(getStyleNameFromIndex(raw_divinity_list[character.character_index]))
                character.setDivinityLink(getDivinityNameFromIndex(raw_divinity_list[character.character_index + 12] + 1))
            except:
                continue

    def _parse_w6(self):
        self._parse_w6_sneaking()
        self._parse_w6_farming()
        self._parse_w6_summoning()

    def _parse_w6_sneaking(self):
        self.sneaking = {
            "PristineCharms": {},
            "Gemstones": {},
            'Beanstalk': {},
            "JadeEmporium": {},
        }
        try:
            self.sneaking['CurrentMastery'] = self.raw_optlacc_dict[231]
        except:
            self.sneaking['CurrentMastery'] = 0
        try:
            self.sneaking['MaxMastery'] = self.raw_optlacc_dict[232]
        except:
            self.sneaking['MaxMastery'] = 0
        raw_ninja_list = safe_loads(self.raw_data.get("Ninja", []))
        self._parse_w6_gemstones(raw_ninja_list)
        self._parse_w6_jade_emporium(raw_ninja_list)
        self._parse_w6_beanstalk(raw_ninja_list)

    def _parse_w6_gemstones(self, raw_ninja_list):
        raw_pristine_charms_list = raw_ninja_list[107] if raw_ninja_list else []
        for pristineCharmIndex, pristineCharmName in enumerate(pristineCharmsList):
            try:
                self.sneaking["PristineCharms"][pristineCharmName] = bool(raw_pristine_charms_list[pristineCharmIndex])
            except:
                self.sneaking["PristineCharms"][pristineCharmName] = False
        for gemstoneIndex, gemstoneName in enumerate(sneakingGemstonesList):
            self.sneaking["Gemstones"][gemstoneName] = {"Level": 0, "Value": 0, "Percent": 0, "Stat": ''}
            try:
                self.sneaking["Gemstones"][gemstoneName]["Level"] = self.raw_optlacc_dict[sneakingGemstonesFirstIndex + gemstoneIndex]
            except:
                continue
            try:
                self.sneaking["Gemstones"][gemstoneName]["Stat"] = sneakingGemstonesStatList[gemstoneIndex]
            except:
                continue
        try:
            self.sneaking["Gemstones"]["Moissanite"]["Value"] = getMoissaniteValue(self.sneaking["Gemstones"]["Moissanite"]["Level"])
        except:
            self.sneaking["Gemstones"]["Moissanite"]["Value"] = 0
        for gemstoneName in sneakingGemstonesList[0:-1]:
            try:
                self.sneaking["Gemstones"][gemstoneName]["Value"] = getGemstoneValue(
                    gemstoneName,
                    self.sneaking["Gemstones"][gemstoneName]["Level"],
                    self.sneaking["Gemstones"]["Moissanite"]["Level"],
                    self.sneaking["Gemstones"]["Moissanite"]["Value"]
                )
            except:
                continue
        for gemstoneName in sneakingGemstonesList:
            try:
                self.sneaking["Gemstones"][gemstoneName]["Percent"] = getGemstonePercent(
                    gemstoneName,
                    self.sneaking["Gemstones"][gemstoneName]["Value"]
                )
            except:
                continue

    def _parse_w6_jade_emporium(self, raw_ninja_list):
        try:
            raw_emporium_purchases = list(raw_ninja_list[102][9])
        except:
            raw_emporium_purchases = [""]
        for upgradeIndex, upgradeDict in enumerate(jade_emporium):
            try:
                self.sneaking['JadeEmporium'][upgradeDict['Name']] = {
                    'Obtained': upgradeDict['CodeString'] in raw_emporium_purchases,
                    'Bonus': upgradeDict['Bonus']
                }
            except:
                continue

    def _parse_w6_beanstalk(self, raw_ninja_list):
        raw_beanstalk_list = raw_ninja_list[104] if raw_ninja_list else []
        for gfoodIndex, gfoodName in enumerate(gfood_codes):
            try:
                self.sneaking['Beanstalk'][gfoodName] = {
                    'Name': getItemDisplayName(gfoodName),
                    'Beanstacked': raw_beanstalk_list[gfoodIndex] > 0,
                    'SuperBeanstacked': raw_beanstalk_list[gfoodIndex] > 1,
                }
            except:
                self.sneaking['Beanstalk'][gfoodName] = {
                    'Name': getItemDisplayName(gfoodName),
                    'Beanstacked': False,
                    'SuperBeanstacked': False,
                }

    def _parse_w6_farming(self):
        self.farming = {
            "CropsUnlocked": 0,
            "MarketUpgrades": {},
            "CropStacks": {
                "EvolutionGMO": 0,  # 200
                "SpeedGMO": 0,  # 1,000
                "ExpGMO": 0,  # 2,500
                "ValueGMO": 0,  # 10,000
                "SuperGMO": 0  # 100,000
            },
        }
        raw_farmcrop_dict = safe_loads(self.raw_data.get("FarmCrop", {}))
        if isinstance(raw_farmcrop_dict, dict):
            for cropIndexStr, cropAmountOwned in raw_farmcrop_dict.items():
                self.farming["CropsUnlocked"] += 1  # Once discovered, crops will always appear in this dict.
                if cropAmountOwned >= 200:
                    self.farming["CropStacks"]["EvolutionGMO"] += 1
                if cropAmountOwned >= 1000:
                    self.farming["CropStacks"]["SpeedGMO"] += 1
                if cropAmountOwned >= 2500:
                    self.farming["CropStacks"]["ExpGMO"] += 1
                if cropAmountOwned >= 10000:
                    self.farming["CropStacks"]["ValueGMO"] += 1
                if cropAmountOwned >= 100000:
                    self.farming["CropStacks"]["SuperGMO"] += 1
        raw_farmupg_list = safe_loads(self.raw_data.get("FarmUpg", {}))
        if isinstance(raw_farmupg_list, list):
            for marketUpgradeIndex, marketUpgradeName in enumerate(marketUpgradeList):
                try:
                    self.farming["MarketUpgrades"][marketUpgradeName] = raw_farmupg_list[marketUpgradeIndex + 2]
                except:
                    self.farming["MarketUpgrades"][marketUpgradeName] = 0

    def _parse_w6_summoning(self):
        self.summoning = {}
        raw_summoning_list = safe_loads(self.raw_data.get('Summon', []))
        try:
            self.summoning["Upgrades"] = raw_summoning_list[0]
        except:
            self.summoning["Upgrades"] = [0] * 69  # As of 2.09 Red/Cyan, there are exactly 69 upgrades
        try:
            self.summoning["BattlesWon"] = raw_summoning_list[1]
        except:
            self.summoning["BattlesWon"] = []
        # raw_summoning_list[2] looks to be essence owned
        # raw_summoning_list[3] I have no idea what this is
        # raw_summoning_list[4] looks to be list[int] familiars in the Sanctuary, starting with Slime in [0], Vrumbi in [1], etc.
        try:
            # [2,3,2,1,1,0,0,0,0,0,0,0,0,0]
            self.summoning['SanctuaryTotal'] = int(raw_summoning_list[4][0])  # Gray Slimes
            self.summoning['SanctuaryTotal'] += 3 * int(raw_summoning_list[4][1])  # Vrumbi
            self.summoning['SanctuaryTotal'] += 12 * int(raw_summoning_list[4][2])  # Bloomie
            self.summoning['SanctuaryTotal'] += 60 * int(raw_summoning_list[4][3])  # Tonka
            self.summoning['SanctuaryTotal'] += 360 * int(raw_summoning_list[4][4])  # Regalis
            # self.summoning['SanctuaryTotal'] += 2520 * int(raw_summoning_list[4][5])  #Sparkie
        except:
            self.summoning['SanctuaryTotal'] = 0
        self.summoning['WinnerBonusesAdvice'] = []

    def _calculate_wave_1(self):
        self._calculate_general()
        self._calculate_w1()
        self._calculate_w2()
        self._calculate_w3()
        self._calculate_w4()
        self._calculate_w5()
        self._calculate_w6()

    def _calculate_general(self):
        pass

    def _calculate_w1(self):
        self.star_sign_extras = {
            'SeraphMulti': min(3, 1.1 ** ceil((max(self.all_skills.get('Summoning', [0])) + 1) / 20)),
            'SeraphGoal': min(240, ceilUpToBase(max(self.all_skills.get('Summoning', [0])), 20))
        }
        if bool(self.star_signs.get("Seraph Cosmos", {}).get('Unlocked', False)):
            self.star_sign_extras['SeraphEval'] = f"Multis signs by {self.star_sign_extras['SeraphMulti']:.2f}x."
        else:
            self.star_sign_extras['SeraphEval'] = f"Locked. Would increase other signs by {self.star_sign_extras['SeraphMulti']:.2f}x if unlocked."
            self.star_sign_extras['SeraphMulti'] = 1
        if self.star_sign_extras['SeraphGoal'] < 240:
            self.star_sign_extras['SeraphEval'] += " Increases every 20 Summoning levels."
        self.star_sign_extras['SeraphAdvice'] = Advice(
            label=f"Starsign: Seraph Cosmos: {self.star_sign_extras['SeraphEval']}",
            picture_class="seraph-cosmos",
            progression=max(self.all_skills.get('Summoning', [0])),
            goal=self.star_sign_extras['SeraphGoal'])

        if self.labChips.get('Silkrode Nanochip', 0) > 0:
            self.star_sign_extras['DoublerOwned'] = True
            self.star_sign_extras['SilkrodeNanoEval'] = f"{self.labChips.get('Silkrode Nanochip', 0)} owned. Doubles starsigns when equipped."
            self.star_sign_extras['SilkrodeNanoMulti'] = 2
        else:
            self.star_sign_extras['DoublerOwned'] = False
            self.star_sign_extras['SilkrodeNanoEval'] = "None Owned. Would double other signs if equipped."
            self.star_sign_extras['SilkrodeNanoMulti'] = 1
        self.star_sign_extras['SilkrodeNanoAdvice'] = Advice(
            label=f"Lab Chip: Silkrode Nanochip: {self.star_sign_extras['SilkrodeNanoEval']}",
            picture_class="silkrode-nanochip")

    def _calculate_w2(self):
        self.vialMasteryMulti = 1 + (self.maxed_vials * .02) if self.rift['VialMastery'] else 1
        self._calculate_w2_sigils()
        self._calculate_w2_cauldrons()

    def _calculate_w2_cauldrons(self):
        perCauldronBubblesUnlocked = [
            self.alchemy_cauldrons['OrangeUnlocked'],
            self.alchemy_cauldrons['GreenUnlocked'],
            self.alchemy_cauldrons['PurpleUnlocked'],
            self.alchemy_cauldrons['YellowUnlocked']
        ]
        bubbleUnlockListByWorld = [20, 0, 0, 0, 0, 0, 0, 0, 0]
        for bubbleColorCount in perCauldronBubblesUnlocked:
            worldCounter = 1
            while bubbleColorCount >= 5 and worldCounter <= len(bubbleUnlockListByWorld) - 1:
                bubbleUnlockListByWorld[worldCounter] += 5
                bubbleColorCount -= 5
                worldCounter += 1
            if bubbleColorCount > 0 and worldCounter <= len(bubbleUnlockListByWorld) - 1:
                bubbleUnlockListByWorld[worldCounter] += bubbleColorCount
                bubbleColorCount = 0
        self.alchemy_cauldrons['BubblesPerWorld'] = bubbleUnlockListByWorld

        self.alchemy_cauldrons['NextWorldMissingBubbles'] = min(
            [cauldronValue // 5 for cauldronValue in perCauldronBubblesUnlocked],
            default=0
        ) + 1

    def _calculate_w2_sigils(self):
        for sigilName in self.alchemy_p2w["Sigils"]:
            if self.alchemy_p2w["Sigils"][sigilName]["Level"] == 2:
                if self.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']:
                    # If you have purchased Ionized Sigils, the numbers needed to Gold get subtracted from your hours already
                    red_Hours = self.alchemy_p2w["Sigils"][sigilName]["Requirements"][2]
                else:
                    # To precharge Red sigils before buying the upgreade, you need Gold + Red hours
                    red_Hours = self.alchemy_p2w["Sigils"][sigilName]["Requirements"][1] + self.alchemy_p2w["Sigils"][sigilName]["Requirements"][2]
                if self.alchemy_p2w["Sigils"][sigilName]["PlayerHours"] >= red_Hours:
                    self.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = 3
                else:
                    self.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = self.alchemy_p2w["Sigils"][sigilName]["Level"]
            elif self.alchemy_p2w["Sigils"][sigilName]["Level"] == 3:
                self.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = 3
            else:
                self.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = self.alchemy_p2w["Sigils"][sigilName]["Level"]
            # Before the +1, -1 would mean not unlocked, 0 would mean Blue tier, 1 would be Yellow tier, and 2 would mean Red tier
            # After the +1, 0/1/2/3

    def _calculate_w3(self):
        self._calculate_w3_tower_max_levels()
        self._calculate_w3_library_max_book_levels()
        self._calculate_w3_collider_base_costs()
        self._calculate_w3_collider_cost_reduction()

    def _calculate_w3_tower_max_levels(self):
        towers = [towerName for towerName, towerValuesDict in self.construction_buildings.items() if towerValuesDict['Type'] == 'Tower']
        if sum(self.all_skills['Construction']) > 2500 and self.rift['SkillMastery']:
            for towerName in towers:
                try:
                    self.construction_buildings[towerName]['MaxLevel'] += 30
                except:
                    continue

        if self.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level'] > 0:
            for towerName in towers:
                try:
                    self.construction_buildings[towerName]['MaxLevel'] += 2 * self.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level']
                except:
                    continue

    def _calculate_w3_library_max_book_levels(self):
        self.library['StaticSum'] = (0
                      + (25 * (0 < self.construction_buildings['Talent Book Library']['Level']))
                      + (5 * (0 < self.achievements.get('Checkout Takeout', False)))
                      + (10 * (0 < self.atom_collider['Atoms']['Oxygen - Library Booker']['Level']))
                      + (25 * self.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0))
                      )
        self.library['ScalingSum'] = (0
                       + 2 * self.merits[2][2]['Level']
                       + 2 * self.saltlick.get('Max Book', 0)
                       )
        summGroupA = (1 + (.25 * self.sailing['Artifacts'].get('The Winz Lantern', {}).get('Level', 0))
                      + .01 * self.merits[5][4]['Level']
                      + .01 * (0 < self.achievements.get('Spectre Stars', False))
                      + .01 * (0 < self.achievements.get('Regalis My Beloved', False))
                      )
        summGroupB = 1 + (.3 * self.sneaking.get('PristineCharms', {}).get('Crystal Comb', 0))
        self.library['SummoningSum'] = round(0
                              + 10.5 * ('w6d3' in self.summoning['BattlesWon'])
                              * summGroupA
                              * summGroupB
                              )
        self.library['MaxBookLevel'] = 100 + self.library['StaticSum'] + self.library['ScalingSum'] + self.library['SummoningSum']

    def _calculate_w3_collider_base_costs(self):
        #Formula for base cost: (AtomInfo[3] + AtomInfo[1] * AtomCurrentLevel) * POWER(AtomInfo[2], AtomCurrentLevel)
        for atomName, atomValuesDict in self.atom_collider['Atoms'].items():
            #Update max level from 20 to 30, if Isotope Discovery unlocked
            if self.gaming['SuperBits']['Isotope Discovery']['Unlocked']:
                self.atom_collider['Atoms'][atomName]['MaxLevel'] += 10

            #If atom isn't already at max level:
            if atomValuesDict['Level'] < atomValuesDict['MaxLevel']:
                # Calculate base cost to upgrade to next level
                self.atom_collider['Atoms'][atomName]['BaseCostToUpgrade'] = (
                    (atomValuesDict['AtomInfo3']
                        + (atomValuesDict['AtomInfo1'] * atomValuesDict['Level']))
                    * pow(atomValuesDict['AtomInfo2'], atomValuesDict['Level'])
                )
                # Calculate base cost to max level
                for level in range(self.atom_collider['Atoms'][atomName]['Level'], self.atom_collider['Atoms'][atomName]['MaxLevel']):
                    self.atom_collider['Atoms'][atomName]['BaseCostToMax'] += (
                        (self.atom_collider['Atoms'][atomName]['AtomInfo3']
                            + (self.atom_collider['Atoms'][atomName]['AtomInfo1'] * level))
                        * pow(self.atom_collider['Atoms'][atomName]['AtomInfo2'], level)
                    )

    def _calculate_w3_collider_cost_reduction(self):
        self.atom_collider['CostReductionRaw'] = (1 +
            (
                7 * self.merits[4][6]['Level']
                + ((self.construction_buildings['Atom Collider']['Level'] - 1) // 10)  # 50 doesn't give 5%, you need 51.
                + 1 * self.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']
                + 10 * self.gaming['SuperBits']['Atom Redux']['Unlocked']
                + self.alchemy_bubbles['Atom Split']['BaseValue']
                + self.stamps['Atomic Stamp']['Value']
            )
            / 100
        )
        self.atom_collider['CostReductionMulti'] = 1 / self.atom_collider['CostReductionRaw']
        self.atom_collider['CostReductionMulti1Higher'] = 1 / (self.atom_collider['CostReductionRaw'] + 0.01)
        self.atom_collider['CostDiscount'] = (1 - (1 / self.atom_collider['CostReductionRaw'])) * 100

        for atomName, atomValuesDict in self.atom_collider['Atoms'].items():
            # Calculate base cost to upgrade to next level, if not max level
            if atomValuesDict['Level'] < atomValuesDict['MaxLevel']:
                self.atom_collider['Atoms'][atomName]['DiscountedCostToUpgrade'] = (self.atom_collider['Atoms'][atomName]['BaseCostToUpgrade']
                                                                                    * self.atom_collider['CostReductionMulti'])
                self.atom_collider['Atoms'][atomName]['DiscountedCostToMax'] = (self.atom_collider['Atoms'][atomName]['BaseCostToMax']
                                                                                * self.atom_collider['CostReductionMulti'])

    def _calculate_w4(self):
        self._calculate_w4_cooking_max_plate_levels()

    def _calculate_w4_cooking_max_plate_levels(self):
        # Sailing Artifact Increases
        causticolumn_level = self.sailing['Artifacts'].get('Causticolumn', {}).get('Level', 0)
        self.cooking['PlayerMaxPlateLvl'] += 10 * int(causticolumn_level)
        if causticolumn_level < 1:
            self.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Base Causticolumn", "causticolumn"))
        if causticolumn_level < 2:
            self.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Ancient Causticolumn", "causticolumn"))
        if causticolumn_level < 3:
            if self.rift['EldritchArtifacts']:
                self.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Eldritch Causticolumn", "causticolumn"))
            else:
                self.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Eldritch Causticolumn."
                                                               " Eldritch Artifacts are unlocked by completing {{ Rift|#rift }} 30", "eldritch-artifact"))
        if causticolumn_level < 4:
            if self.sneaking['JadeEmporium']["Sovereign Artifacts"]['Obtained']:
                self.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Sovereign Causticolumn", "causticolumn"))
            else:
                self.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Sovereign Causticolumn. Sovereign Artifacts unlock from "
                                                               "{{ Jade Emporium|#sneaking }}", "sovereign-artifacts"))
        # Jade Emporium Increases
        if self.sneaking['JadeEmporium']["Papa Blob's Quality Guarantee"]['Obtained']:
            self.cooking['PlayerMaxPlateLvl'] += 10
        else:
            self.cooking['PlayerMissingPlateUpgrades'].append(("Purchase \"Papa Blob's Quality Guarantee\" from "
                                                               "{{ Jade Emporium|#sneaking }}", "papa-blobs-quality-guarantee"))
        if self.sneaking['JadeEmporium']["Chef Geustloaf's Cutting Edge Philosophy"]['Obtained']:
            self.cooking['PlayerMaxPlateLvl'] += 10
        else:
            self.cooking['PlayerMissingPlateUpgrades'].append(("Purchase \"Chef Geustloaf's Cutting Edge Philosophy\" from "
                                                               "{{ Jade Emporium|#sneaking }}", "chef-geustloafs-cutting-edge-philosophy"))

        self.cooking['CurrentRemainingMeals'] = (self.cooking['MealsUnlocked'] * self.cooking['PlayerMaxPlateLvl']) - self.cooking['PlayerTotalMealLevels']
        self.cooking['MaxRemainingMeals'] = (maxMeals * maxMealLevel) - self.cooking['PlayerTotalMealLevels']

    def _calculate_w5(self):
        self._calculate_w5_divinity_link_advice()

    def _calculate_w5_divinity_link_advice(self):
        self.divinity['DivinityLinks'] = {
            0: [
                Advice(
                    label="No Divinities unlocked to link to",
                    picture_class=""
                )
            ],
            1: [
                Advice(
                    label="No harm in linking everyone, as Snehebatu is your only choice",
                    picture_class="snehebatu"
                )
            ],
            2: [
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                )
            ],
            3: [
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                )
            ],
            4: [
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                )
            ],
            5: [
                Advice(
                    label="Move Meditators to Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                )
            ],
            6: [
                Advice(
                    label="Move Meditators to Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                )
            ],
            7: [
                Advice(
                    label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
                    picture_class="purrmep"
                ),
                Advice(
                    label="Meditators in Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Cooking BB generally wants Snake",
                    picture_class="cooking-ladle"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                ),

            ],
            8: [
                Advice(
                    label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
                    picture_class="purrmep"
                ),
                Advice(
                    label="Meditators in Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Cooking BB generally wants Snake",
                    picture_class="cooking-ladle"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                ),
            ],
            9: [
                Advice(
                    label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
                    picture_class="purrmep"
                ),
                Advice(
                    label="Meditators in Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Cooking BB generally wants Snake",
                    picture_class="cooking-ladle"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                ),
            ],
            10: [
                Advice(
                    label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
                    picture_class="purrmep"
                ),
                Advice(
                    label="Meditators in Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Cooking BB generally wants Snake",
                    picture_class="cooking-ladle"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                ),
            ],
            11: [
                Advice(
                    label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
                    picture_class="purrmep"
                ),
                Advice(
                    label="Meditators in Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Cooking BB generally wants Snake",
                    picture_class="cooking-ladle"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                ),
            ],
            12: [
                Advice(
                    label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
                    picture_class="purrmep"
                ),
                Advice(
                    label="Meditators in Lab",
                    picture_class="goharut"
                ),
                Advice(
                    label="Lab bonuses fully online",
                    picture_class="arctis"
                ),
                Advice(
                    label="1 Map Pusher",
                    picture_class="nobisect"
                ),
                Advice(
                    label="Cooking BB generally wants Snake",
                    picture_class="cooking-ladle"
                ),
                Advice(
                    label="Extra characters can link to Snake if not Meditating",
                    picture_class="snehebatu"
                ),
                Advice(
                    label="Omniphau is a gamble. Refinery and 3D Printer rewards are nice- The other 4/6 are pretty meh.",
                    picture_class="omniphau"
                ),
            ],
        }

    def _calculate_w6(self):
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"{{{{ Pristine Charm|#sneaking }}}}: Crystal Comb: {1 + (.3 * self.sneaking.get('PristineCharms', {}).get('Crystal Comb', 0))}x",
            picture_class="crystal-comb",
            progression=1 if self.sneaking.get("PristineCharms", {}).get('Crystal Comb', False) else 0,
            goal=1
        ))
        if not self.sneaking['JadeEmporium']['Brighter Lighthouse Bulb']['Obtained']:
            winzLanternPostString = ". Unlocked from {{ Jade Emporium|#sneaking }}"
        else:
            winzLanternPostString = ""
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"{{{{ Artifact|#sailing }}}}: The Winz Lantern: {1 + (.25 * self.sailing['Artifacts'].get('The Winz Lantern', {}).get('Level', 0))}x{winzLanternPostString}",
            picture_class="the-winz-lantern",
            progression=self.sailing['Artifacts'].get('The Winz Lantern', {}).get('Level', 0),
            goal=4
        ))
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"W6 Larger Winner bonuses merit: +{self.merits[5][4]['Level']}%",
            picture_class="merit-5-4",
            progression=self.merits[5][4]["Level"],
            goal=self.merits[5][4]["MaxLevel"]
        ))
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"W6 Achievement: Spectre Stars: +{1 * (0 < self.achievements.get('Spectre Stars', False))}%",
            picture_class="spectre-stars",
            progression=1 if self.achievements.get('Spectre Stars', False) else 0,
            goal=1
        ))
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"W6 Achievement: Regalis My Beloved: +{1 * (0 < self.achievements.get('Regalis My Beloved', False))}%",
            picture_class="regalis-my-beloved",
            progression=360 if self.achievements.get('Regalis My Beloved', False) else self.summoning['SanctuaryTotal'],
            goal=360
        ))

    def _calculate_wave_2(self):
        self._calculate_general_character_over_books()

    def _calculate_general_character_over_books(self):
        self.bonus_talents = {
            "Rift Slug": {
                "Value": 25 * self.riftslug_owned,
                "Image": "rift-slug",
                "Label": f"Companion: Rift Slug: +{25 * self.riftslug_owned}",
                "Progression": 1 if self.riftslug_owned else 0,
                "Goal": 1
            },
            "ES Family": {
                "Value": floor(self.family_bonuses["Elemental Sorcerer"]['Value']),
                "Image": 'elemental-sorcerer-icon',
                "Label": f"ES Family Bonus: +{floor(self.family_bonuses['Elemental Sorcerer']['Value'])}.<br>"
                         f"Next increase at Class Level: ",
                "Progression": self.family_bonuses['Elemental Sorcerer']['Level'],
                "Goal": getNextESFamilyBreakpoint(self.family_bonuses['Elemental Sorcerer']['Level'])
            },
            "Equinox Symbols": {
                "Value": self.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
                "Image": 'equinox-symbols',
                "Label": f"{{{{ Equinox|#equinox }}}}: Equinox Symbols: +{self.equinox_bonuses['Equinox Symbols']['CurrentLevel']}",
                "Progression": self.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
                "Goal": self.equinox_bonuses['Equinox Symbols']['FinalMaxLevel']
            },
            "Maroon Warship": {
                "Value": 1 * self.achievements['Maroon Warship'],
                "Image": "maroon-warship",
                "Label": f"W5 Achievement: Maroon Warship: +{1 * self.achievements['Maroon Warship']}",
                "Progression": 1 if self.achievements['Maroon Warship'] else 0,
                "Goal": 1
            },
            "Sneaking Mastery": {
                "Value": 5 if self.sneaking['MaxMastery'] >= 3 else 0,
                "Image": "sneaking-mastery",
                "Label": f"{{{{ Rift|#rift }}}}: Sneaking Mastery: +{5 if self.sneaking['MaxMastery'] >= 3 else 0} (Mastery III)",
                "Progression": self.sneaking['MaxMastery'],
                "Goal": 3
            },
            # If Slug is owned: +25
            # If Sneaking Mastery 3 unlocked: +5
        }
        self.bonus_talents_account_wide_sum = 0
        for bonusName, bonusValuesDict in self.bonus_talents.items():
            try:
                self.bonus_talents_account_wide_sum += bonusValuesDict.get('Value', 0)
            except:
                continue

        for char in self.safe_characters:
            character_specific_bonuses = 0

            # Arctis minor link
            if self.doot_owned or char.divinity_link == "Arctis" or char.current_polytheism_link == "Arctis" or char.secondary_polytheism_link == "Arctis":
                bigp_value = self.alchemy_bubbles['Big P']['BaseValue']
                div_minorlink_value = char.divinity_level / (char.divinity_level + 60)
                arctis_base = 15
                final_result = ceil(arctis_base * bigp_value * div_minorlink_value)
                character_specific_bonuses += ceil(15 * self.alchemy_bubbles['Big P']['BaseValue'] * (char.divinity_level / (char.divinity_level + 60)))

            # Symbols of Beyond = 1 per 20 levels
            if char.class_name in ["Blood Berserker", "Divine Knight"]:
                character_specific_bonuses += char.max_talents.get("149", 0) // 20  #Symbols of Beyond - Red
                char.setSymbolsOfBeyondMax(char.max_talents.get("149", 0) // 20)
            elif char.class_name in ["Siege Breaker", "Beast Master"]:
                character_specific_bonuses += char.max_talents.get("374", 0) // 20  # Symbols of Beyond - Green
                char.setSymbolsOfBeyondMax(char.max_talents.get("374", 0) // 20)
            elif char.class_name in ["Elemental Sorcerer", "Bubonic Conjuror"]:
                character_specific_bonuses += char.max_talents.get("539", 0) // 20  # Symbols of Beyond - Purple
                char.setSymbolsOfBeyondMax(char.max_talents.get("539", 0) // 20)

            char.max_talents_over_books = self.library['MaxBookLevel'] + self.bonus_talents_account_wide_sum + character_specific_bonuses

            # If they're an ES, use max level of Family Guy to calculate floor(ES Family Value * Family Guy)
            if char.class_name == "Elemental Sorcerer":
                try:
                    #TODO: Move one-off talent value calculation
                    family_guy_bonus = lavaFunc(
                        'decay',
                        char.max_talents_over_books + char.max_talents.get("374", 0),
                        40,
                        100
                    )
                    family_guy_multi = 1 + (family_guy_bonus/100)
                    char.max_talents_over_books += floor(self.family_bonuses["Elemental Sorcerer"]['Value'] * family_guy_multi)
                    char.setFamilyGuyBonus(floor(self.family_bonuses["Elemental Sorcerer"]['Value'] * family_guy_multi) - floor(self.family_bonuses["Elemental Sorcerer"]['Value']))
                except:
                    pass

    def _make_cards(self):
        card_counts = safe_loads(self.raw_data.get(self._key_cards, {}))
        cards = [
            Card(codename, name, cardset, int(float(card_counts.get(codename, 0))), coefficient)
            for cardset, cards in card_data.items()
            for codename, (name, coefficient) in cards.items()
        ]

        return cards

    def _all_owned_items(self) -> Assets:
        chest_keys = (("ChestOrder", "ChestQuantity"),)
        name_quantity_key_pairs = chest_keys + tuple(
            (f"InventoryOrder_{i}", f"ItemQTY_{i}") for i in self.safe_playerIndexes
        )
        all_stuff_owned = defaultdict(int)

        for codename in gstackable_codenames:
            all_stuff_owned[codename] = 0

        for name_key, quantity_key in name_quantity_key_pairs:
            for name, count in zip(
                self.raw_data[name_key], self.raw_data[quantity_key]
            ):
                try:
                    all_stuff_owned[name] += int(count)
                except Exception as reason:
                    continue

        return Assets(all_stuff_owned)
