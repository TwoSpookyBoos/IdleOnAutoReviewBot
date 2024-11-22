import copy
import functools
import json
import os
import re
import sys

from config import app
from collections import defaultdict
from enum import Enum
from math import ceil, floor
from typing import Any, Union
from flask import g
from utils.data_formatting import getCharacterDetails, safe_loads, safer_get
from utils.text_formatting import kebab, getItemCodeName, getItemDisplayName
from consts import (
    # General
    lavaFunc, ceilUpToBase, ValueToMulti, ignorable_labels,
    items_codes_and_names,
    currentWorld, maxCharacters,
    expectedStackables, greenstack_progressionTiers, gfood_codes,
    card_data,
    gemShopDict,
    guildBonusesList, familyBonusesDict, getNextESFamilyBreakpoint,
    achievementsList, allMeritsDict, starsignsDict,
    base_crystal_chance,
    filter_recipes, filter_never,
    event_points_shop_dict,
    npc_tokens,
    # W1
    stampsDict, stampTypes, bribesDict,
    forgeUpgradesDict,
    statuesDict, statueTypeList, statueCount,
    # W2
    bubblesDict,
    vialsDict, max_IndexOfVials, getReadableVialNames, max_VialLevel,
    sigilsDict,
    arcadeBonuses,
    poBoxDict,
    ballotDict,
    fishingToolkitDict,
    obolsDict, ignorable_obols_list,
    islands_dict, islands_trash_shop_costs,
    killroy_dict,
    # W3
    refineryDict, buildingsDict, saltLickList, atomsList, colliderStorageLimitList, shrinesList, arbitrary_shrine_goal, arbitrary_shrine_note,
    prayersDict,
    equinoxBonusesDict, maxDreams, dreamsThatUnlockNewBonuses,
    expected_talentsDict,
    printerAllIndexesBeingPrinted,
    dnSkullValueList, reversed_dnSkullValueList, dnSkullRequirementList, reversed_dnSkullRequirementList,
    getSkullNames, getNextSkullNames, apocableMapIndexDict, apocAmountsList, apocNamesList,
    # W4
    riftRewardsDict,
    labJewelsDict, labBonusesDict, nblbMaxBubbleCount, labChipsDict,
    maxMeals, maxMealLevel, cookingMealDict, maxCookingTables,
    maxNumberOfTerritories, indexFirstTerritoryAssignedPet, territoryNames, slotUnlockWavesList, breedingUpgradesDict, breedingGeneticsList,
    breedingShinyBonusList, breedingSpeciesDict, getShinyLevelFromDays, getDaysToNextShinyLevel, getBreedabilityMultiFromDays, getBreedabilityHeartFromMulti,
    # W5
    sailingDict, numberOfArtifactTiers, captainBuffs,
    getStyleNameFromIndex, divinity_divinitiesDict, divinity_offeringsDict, getDivinityNameFromIndex, divinity_DivCostAfter3,
    gamingSuperbitsDict,

    # W6
    jade_emporium, pristineCharmsList, sneakingGemstonesFirstIndex, sneakingGemstonesList, sneakingGemstonesStatList,
    getMoissaniteValue, getGemstoneBaseValue, getGemstoneBoostedValue, getGemstonePercent,
    marketUpgradeDetails, landrankDict, cropDepotDict, maxFarmingCrops,
    summoningBattleCountsDict, summoningDict,
    # Caverns
    caverns_villagers, caverns_conjuror_majiks, caverns_engineer_schematics, caverns_engineer_schematics_unlock_order, caverns_cavern_names,
    caverns_measurer_measurements, getCavernResourceImage, schematics_unlocking_buckets, max_buckets, max_sediments, sediment_bars, getVillagerEXPRequired,
    monument_bonuses, bell_clean_improvements, bell_ring_bonuses, getBellExpRequired, getBellImprovementBonus, monument_names, released_monuments
)


def session_singleton(cls):
    def getinstance(*args, **kwargs):
        if not hasattr(g, "account"):
            return cls(*args, **kwargs)
        return g.account

    return getinstance


def getJSONDataFromFile(filePath):
    with open(filePath, 'r') as inputFile:
        jsonData = json.load(inputFile)
    inputFile.close()
    return jsonData

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
    if base_class == "Warrior":
        specializedSkillsList.append("Mining")
    elif base_class == "Archer":
        specializedSkillsList.append("Smithing")
    elif base_class == "Mage":
        specializedSkillsList.append("Choppin")

    if sub_class == "Barbarian":
        specializedSkillsList.append("Fishing")
    elif sub_class == "Squire":
        specializedSkillsList.append("Construction")
    elif sub_class == "Bowman":
        specializedSkillsList.append("Catching")
    elif sub_class == "Hunter":
        specializedSkillsList.append("Trapping")
    elif sub_class == "Wizard":
        specializedSkillsList.append("Worship")
    elif sub_class == "Shaman":
        specializedSkillsList.append("Alchemy")

    if elite_class == "Blood Berserker":
        specializedSkillsList.append("Cooking")
    elif elite_class == "Divine Knight":
        specializedSkillsList.append("Gaming")
    elif elite_class == "Siege Breaker":
        specializedSkillsList.append("Sailing")
    elif elite_class == "Beast Master":
        specializedSkillsList.append("Breeding")
    elif elite_class == "Elemental Sorcerer":
        specializedSkillsList.append("Divinity")
    elif elite_class == "Bubonic Conjuror":
        specializedSkillsList.append("Lab")

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
        po_boxes: list[int],
        equipped_lab_chips: list[str],
        inventory_bags: dict,
        kill_dict: dict,
    ):

        self.character_index: int = character_index
        self.character_name: str = character_name

        self.class_name: str = class_name
        self.class_name_icon: str = class_name.replace(" ", "-") + "-icon"
        self.base_class: str = base_class
        self.sub_class: str = sub_class
        self.elite_class: str = elite_class
        self.all_classes: list[str] = [base_class, sub_class, elite_class]
        self.max_talents_over_books: int = 100
        self.symbols_of_beyond = 0
        self.family_guy_bonus = 0
        self.max_talents: dict = max_talents
        self.current_preset_talents: dict = current_preset_talents
        self.secondary_preset_talents: dict = secondary_preset_talents
        self.specialized_skills: list[str] = getSpecializedSkills(self.base_class, self.sub_class, self.elite_class)
        self.expected_talents: list[int] = getExpectedTalents(self.base_class, self.sub_class, self.elite_class)
        self.inventory_bags: dict = inventory_bags
        self.kill_dict: dict = kill_dict
        self.fixKillDict()
        self.crystal_spawn_chance: float = 0.0

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
                        po_boxes[poBoxIndex] - poBoxValues['2_minCount'],
                        poBoxValues['2_x1'],
                        poBoxValues['2_x2'],
                    ) if po_boxes[poBoxIndex] >= poBoxValues['2_minCount'] else 0,
                    'Bonus2String': '',
                    'Bonus3Value': lavaFunc(
                        poBoxValues['3_funcType'],
                        po_boxes[poBoxIndex] - poBoxValues['3_minCount'],
                        poBoxValues['3_x1'],
                        poBoxValues['3_x2'],
                    ) if po_boxes[poBoxIndex] >= poBoxValues['3_minCount'] else 0,
                    'Bonus3String': '',
                }
                if self.po_boxes_invested[poBoxValues['Name']]['Level'] > 0:
                    self.po_boxes_invested[poBoxValues['Name']]['Bonus1String'] = (
                        f"{poBoxValues['1_pre']}{self.po_boxes_invested[poBoxValues['Name']]['Bonus1Value']}{poBoxValues['1_post']} {poBoxValues['1_stat']}")
                    self.po_boxes_invested[poBoxValues['Name']]['Bonus2String'] = (
                        f"{poBoxValues['2_pre']}{self.po_boxes_invested[poBoxValues['Name']]['Bonus2Value']}{poBoxValues['2_post']} {poBoxValues['2_stat']}")
                    self.po_boxes_invested[poBoxValues['Name']]['Bonus3String'] = (
                        f"{poBoxValues['3_pre']}{self.po_boxes_invested[poBoxValues['Name']]['Bonus3Value']}{poBoxValues['3_post']} {poBoxValues['3_stat']}")
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
        self.equipped_lab_chips: list[str] = []
        for chipIndex in equipped_lab_chips:
            if chipIndex != -1:
                try:
                    self.equipped_lab_chips.append(labChipsDict[chipIndex]['Name'])
                except:
                    continue

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
            for name in apocNamesList
        }
        self.equipment = Equipment(raw_data, character_index, self.combat_level >= 1)
        self.printed_materials = {}

        self.setPolytheismLink()

    def fixKillDict(self):
        for mapIndex in self.kill_dict:
            #If the map is already a List as expected,
            # if each entry isn't already float or int,
            #  try to convert every entry to a float or set to 0 if error
            if isinstance(self.kill_dict[mapIndex], list):
                for killIndex, killCount in enumerate(self.kill_dict[mapIndex]):
                    if not isinstance(killCount, float) or not isinstance(killCount, int):
                        try:
                            self.kill_dict[mapIndex][killIndex] = float(killCount)
                        except:
                            self.kill_dict[mapIndex][killIndex] = 0
            else:
                #Sometimes users have just raw strings, floats, or ints that aren't in a list
                # Try to put them into a list AND convert to float at the same time
                #  else default to a list containing zeroes as some maps have multiple portals
                try:
                    self.kill_dict[mapIndex] = [float(self.kill_dict[mapIndex])]
                except:
                    self.kill_dict[mapIndex] = [0, 0, 0]

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

    def setPrintedMaterials(self, printDict):
        self.printed_materials = printDict

    def setCrystalSpawnChance(self, value: float):
        self.crystal_spawn_chance = value

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
    CAVERNS = "Caverns"
    WORLD6 = "World 6"
    BLUNDER_HILLS = "Blunder Hills"
    YUMYUM_DESERT = "Yum-Yum Desert"
    FROSTBITE_TUNDRA = "Frostbite Tundra"
    HYPERION_NEBULA = "Hyperion Nebula"
    SMOLDERIN_PLATEAU = "Smolderin' Plateau"
    SPIRITED_VALLEY = "Spirited Valley"
    THE_CAVERNS_BELOW = "The Caverns Below"


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

    @property
    def dataset(self) -> list:
        return [[attr, getattr(self, attr, False)] for attr in ["completed", "informational", "unrated", "unreached"]]


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

    def __init__(
            self, label: str,
            picture_class: str,
            progression: Any = "",
            goal: Any = "",
            unit: str = "",
            value_format: str = "{value}{unit}",
            resource: str = "",
            completed: bool = None,
            unrated: bool = False,
            **extra
    ):
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
        if completed is None:
            self.completed: bool = self.goal in ("✔", "") or self.label.startswith(ignorable_labels)
        else:
            self.completed = completed
        self.unrated: bool = unrated

        if self.goal == "✔":
            self.status = "gilded"

        self.percent = self.__calculate_progress_box_width()


    @property
    def css_class(self) -> str:
        name = kebab(self.picture_class)
        return name

    def __str__(self) -> str:
        return self.label

    def __calculate_progress_box_width(self) -> str:
        percentage = next((num for num in [self.goal, self.progression] if num.endswith("%")), None)
        if not all(num.endswith("%") for num in [self.goal, self.progression]) and percentage:
            return percentage

        float_re = re.compile(r'\d+(.\d+)?')
        progression = float_re.search(self.progression)
        goal = float_re.search(self.goal)
        try:
            percentage = round(100 * float(progression[0]) / float(goal[0]), 2)
            percentage = percentage if percentage < 100 else 100
            return str(percentage) + '%'
        except (ZeroDivisionError, IndexError, TypeError, ValueError):
            return "0"

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
        tier: str | int,
        pre_string: str,
        post_string: str = "",
        formatting: str = "",
        picture_class: str = "",
        collapse: bool | None = None,
        advices: list[Advice] | dict[str, list[Advice]] = [],
        completed: bool = None,
        informational: bool = False,
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.tier: str = str(tier)
        self.pre_string: str = pre_string
        self.post_string: str = post_string
        self.formatting: str = formatting
        self._picture_class: str = picture_class
        self.advices = advices
        self.completed = completed
        self.informational = informational

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

    def sort_advices(self, reverseBool):
        if 'default' in self.advices:
            if isinstance(self.advices['default'], list):
                try:
                    self.advices['default']: list[Advice] = sorted(
                        self.advices['default'],
                        key=lambda a: float(str(a.progression).strip('%')),
                        reverse=reverseBool
                    )
                except:
                    pass

    def check_for_completeness(self, ignorable=tuple('Weekly Ballot')):
        """
        Used when a bool for complete was not passed in during initialization of the AdviceGroup
        """
        if self.completed is not None:
            return
        else:
            if isinstance(self.advices, list):
                temp_advices = [advice for advice in self.advices if not advice.completed]
            elif isinstance(self.advices, dict):
                temp_advices = []
                for key, value in self.advices.items():
                    if isinstance(value, list):
                        #flattern to a single list
                        temp_advices.extend([advice for advice in value if not advice.completed])
            else:
                temp_advices = []
            self.completed = len(temp_advices) == 0  #True if 0 length, False otherwise

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
        completed: bool | None = None,
        unreached: bool = False,
        unrated: bool = False,
        informational: bool | None = None,
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.name: str = name
        self.tier: str = tier
        self._raw_header: str = header
        self.picture: str = picture
        self.groups: list[AdviceGroup] = groups
        self.pinchy_rating: int = pinchy_rating
        self.completed: bool | None = completed
        self.unreached = unreached
        self.unrated = unrated
        self.informational = informational

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
    def groups(self, groups: list[AdviceGroup]):
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
        else:
            self.completed = len([group for group in self.groups if group and not group.completed]) == 0  #True if 0 length, False otherwise

    def check_for_informationalness(self):
        if self.informational is not None:
            return
        else:
            #print(f"{self.name}: {len([group for group in self.groups if group and group.informational])} Info groups / {len([group for group in self.groups if group])} total Truthy groups")
            self.informational = len([group for group in self.groups if group and not group.informational]) == 0 and len([group for group in self.groups if group]) > 0  #True if 0 length, False otherwise

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
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.name: str = name.value
        self.sections: list[AdviceSection] = sections
        self.banner: list[str] | None = banner
        self.title: str = title
        if completed is not None:
            self.completed = completed
        else:
            self.check_for_completeness()
        if informational is not None:
            self.informational = informational
        else:
            self.check_for_informationalness()
        if unrated is not None:
            self.unrated = unrated
        else:
            self.check_for_unratedness()

    @property
    def id(self):
        return kebab(self.name)

    def hide_unreached_sections(self):
        self.sections = [section for section in self.sections if not section.unreached]

    def check_for_completeness(self):
        """
        Used when a bool for complete was not passed in during initialization of the AdviceWorld
        """
        self.completed = len([section for section in self.sections if not section.completed]) == 0  #True if 0 length, False otherwise

    def check_for_informationalness(self):
        self.informational = len([section for section in self.sections if not section.informational]) == 0 and len(
            [section for section in self.sections if section]) > 0

    def check_for_unratedness(self):
        self.unrated = len([section for section in self.sections if not section.unrated]) == 0 and len(
            [section for section in self.sections if section]) > 0


greenStackAmount = 10**7
gstackable_codenames = [item for items in expectedStackables.values() for item in items]
gstackable_codenames_expected = [
    item for items in list(expectedStackables.values())[:-1] for item in items
]
quest_items_codenames = expectedStackables["Missable Quest Items"]


class Asset:
    def __init__(self, codename: Union[str, "Asset"], amount: float, name: str = ""):
        if isinstance(codename, Asset):
            self.name: str = codename.name
            self.codename: str = codename.codename
            self.amount: float = codename.amount
            self.quest: str = codename.quest
            self.quest_giver: str = codename.quest_giver
        else:
            self.name: str = name if name else getItemDisplayName(codename)
            self.codename: str = codename if codename else getItemCodeName(name)
            self.amount: float = amount
            self.quest: str = ""
            self.quest_giver: str = ""

    def __eq__(self, other):
        match other:
            case str():
                return other == self.codename or other == self.name
            case Assets():
                return other.codename == self.codename and other.name == self.name

    def __str__(self):
        return f"{self.name}: {self.amount}"

    def __repr__(self):
        return f"<class {self.__class__.__name__}: {self.__str__()}>"

    def __hash__(self):
        return str(self.__dict__).__hash__()

    def __add__(self, other: Union["Asset", int]):
        return Asset(self, 0).add(other)

    def __iadd__(self, other: Union["Asset", int]):
        match other:
            case Asset():
                self.amount += other.amount
            case int():
                self.amount += other
            case _:
                print(f"RHS operand not of valid type: '{type(other)}'. Not added.")

        return self

    def add(self, other: Union["Asset", int]):
        return self.__iadd__(other)

    @property
    def greenstacked(self) -> bool:
        return self.amount >= greenStackAmount

    @property
    def progression(self) -> int:
        return self.amount * 100 // greenStackAmount


class Assets(dict):
    def __init__(self, assets: Union[dict[str, int], "Assets", None] = None):
        self.tiers = greenstack_progressionTiers

        if assets is None:
            assets = dict()

        if isinstance(assets, Assets):
            super().__init__(
                tuple(
                    (codename, Asset(asset, 0)) for codename, asset in assets.items()
                )
            )
        else:
            super().__init__(
                tuple(
                    (codename, Asset(codename, count)) for codename, count in assets.items()
                )
            )

    def __add__(self, other: Union["Assets", Asset, dict[str, int]]):
        """Creates a new Assets object as a sum of the two Asset-like operands"""
        return Assets(self).add(other)

    def add(self, other):
        return self.__iadd__(other)

    def __iadd__(self, other: Union["Assets", Asset, dict[str, int]]):
        """Adds the other resource to self in-place"""
        match other:
            case Assets() | dict():
                for codename, asset in other.items():
                    self.get(codename).add(asset)
            case Asset():
                self.get(other.codename).add(other)
            case _:
                print(f"RHS operand not of valid type: '{type(other)}'. Not added.")

        return self

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


class EnemyWorld:
    def __init__(self, worldnumber: int, mapsdict: dict):
        self.world_number: int = worldnumber
        self.maps_dict: dict = mapsdict
        self.lowest_skulls_dict: dict = {}
        self.lowest_skull_value: int = -1
        self.total_mk = sum(enemy_map.skull_mk_value for enemy_map in mapsdict.values())
        self.current_lowest_skull_name: str = "None"
        self.next_lowest_skull_name: str = "Normal Skull"
        for skullValue in dnSkullValueList:
            self.lowest_skulls_dict[skullValue] = []
        if len(mapsdict) > 0:
            for enemy_map_index in self.maps_dict:
                self.lowest_skulls_dict[self.maps_dict[enemy_map_index].skull_mk_value].append(
                    [self.maps_dict[enemy_map_index].map_name,
                     self.maps_dict[enemy_map_index].kills_to_next_skull,
                     self.maps_dict[enemy_map_index].percent_toward_next_skull,
                     self.maps_dict[enemy_map_index].monster_image])
            for skullDict in self.lowest_skulls_dict:
                self.lowest_skulls_dict[skullDict] = sorted(self.lowest_skulls_dict[skullDict], key=lambda item: item[2], reverse=True)
            for skullDict in self.lowest_skulls_dict:
                if len(self.lowest_skulls_dict[skullDict]) > 0:
                    if self.lowest_skull_value == -1:
                        self.lowest_skull_value = skullDict
            self.current_lowest_skull_name = getSkullNames(self.lowest_skull_value)
            self.next_lowest_skull_name = getNextSkullNames(self.lowest_skull_value)

    def __str__(self):
        if self.world_number == 0:
            return "Barbarian Only Extras"
        else:
            return f"World {self.world_number}"


class EnemyMap:
    def __init__(self, mapname: str, monstername: str, mapindex: int, portalrequirement: int, zowrating: str, chowrating: str, meowrating: str, monsterimage: str = ""):
        self.map_name: str = mapname
        self.map_index: int = mapindex
        self.monster_name: str = monstername
        self.portal_requirement: int = portalrequirement
        self.zow_rating: str = zowrating
        self.chow_rating: str = chowrating
        self.meow_rating: str = meowrating
        self.kill_count: float = 0
        self.skull_mk_value: int = 0
        self.skull_name: str = "None"
        self.kills_to_next_skull: int = 0
        self.percent_toward_next_skull: int = 0
        self.zow_dict = {}
        if monsterimage:
            self.monster_image = monsterimage.lower()
        else:
            self.monster_image = monstername

    def __str__(self):
        return self.map_name

    def getRating(self, ratingType: str):
        if ratingType == 'ZOW':
            return self.zow_rating
        elif ratingType == 'CHOW':
            return self.chow_rating
        elif ratingType == 'MEOW':
            return self.meow_rating
        else:
            return 'Insane'

    def updateZOWDict(self, characterIndex: int, KLAValue: float):
        if characterIndex not in self.zow_dict:
            self.zow_dict[characterIndex] = {}
        self.zow_dict[characterIndex] = int(abs(float(KLAValue) - self.portal_requirement))

    def addRawKLA(self, additionalKills: float):
        try:
            self.kill_count += abs(float(additionalKills) - self.portal_requirement)
        except Exception as reason:
            print(f"Unable to add additionalKills value of {type(additionalKills)} {additionalKills} to {self.map_name} because: {reason}")
            #logger.warning(f"Unable to add additionalKills value of {type(additionalKills)} {additionalKills} to {self.map_name} because: {reason}")

    def generateDNSkull(self):
        self.kill_count = int(self.kill_count)
        for counter in range(0, len(dnSkullRequirementList)):
            if self.kill_count >= dnSkullRequirementList[counter]:
                self.skull_mk_value = dnSkullValueList[counter]
        self.skull_name = getSkullNames(self.skull_mk_value)
        if self.skull_mk_value == reversed_dnSkullValueList[0]:
            #If map's skull is highest, currently Eclipse Skull, set in defaults
            self.kills_to_next_skull = 0
            self.percent_toward_next_skull = 100
        else:
            for skullValueIndex in range(1, len(reversed_dnSkullValueList)):
                if self.skull_mk_value == reversed_dnSkullValueList[skullValueIndex]:
                    self.kills_to_next_skull = ceil(reversed_dnSkullRequirementList[skullValueIndex-1] - self.kill_count)
                    self.percent_toward_next_skull = floor((self.kill_count / reversed_dnSkullRequirementList[skullValueIndex-1]) * 100)

def buildMaps() -> dict[int, dict]:
    mapDict = {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        #7: {},
        #8: {}
    }
    rawMaps = getJSONDataFromFile(os.path.join(app.static_folder, 'enemy-maps.json'))
    for mapData in rawMaps["mapData"]:
        #["Spore Meadows", 1, "Green Mushroom", 11, "Basic W1 Enemies", "Basic W1 Enemies", "Basic W1 Enemies"],
        #mapData[0]: str = map name
        #mapData[1]: int = map index
        #mapData[2]: str = enemy name
        #mapData[3]: int = portal requirement
        #mapData[4]: str = zow rating
        #mapData[5]: str = chow rating
        #mapData[6]: str = meow rating
        if mapData[1] in apocableMapIndexDict[0]:
            world = 0
        else:
            world = floor(mapData[1] / 50) + 1
        mapDict[world][mapData[1]] = EnemyMap(
            mapname=mapData[0],
            mapindex=mapData[1],
            monstername=mapData[2],
            portalrequirement=mapData[3],
            zowrating=mapData[4],
            chowrating=mapData[5],
            meowrating=mapData[6],
            monsterimage=mapData[7]
        )
    return mapDict

@session_singleton
class Account:
    _key_cards = "Cards0"

    def __init__(self, json_data, run_type="web"):
        self.raw_data = safe_loads(json_data)
        self._prep_alerts_AG()
        self._parse_wave_1(run_type)
        self._calculate_wave_1()
        self._calculate_wave_2()

    def _prep_alerts_AG(self):
        self.alerts_AdviceDict = {
            'General': [],
            'World 1': [],
            'World 2': [],
            'World 3': [],
            'World 4': [],
            'World 5': [],
            'The Caverns Below': [],
            'World 6': []
        }

    def _parse_wave_1(self, run_type):
        self._parse_switches()
        self._parse_characters(run_type)
        self._parse_general()
        self._parse_w1()
        self._parse_w2()
        self._parse_w3()
        self._parse_w4()
        self._parse_w5()
        self._parse_caverns()
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

        #consts.maxTiersPerGroup = 1 if g.one_tier else consts.maxTiersPerGroup

        # Companions
        self.sheepie_owned = g.sheepie
        self.doot_owned = g.doot
        self.riftslug_owned = g.riftslug
        # print(f"Switches alone: Doot={g.doot}, Slug={g.riftslug}, Sheepie={g.sheepie}")
        if not all([self.doot_owned, self.sheepie_owned, self.riftslug_owned]):
            # If the data comes from Toolbox, it'll be a dictionary called companion singular
            raw_companion = self.raw_data.get('companion', None)
            # If the data comes from Efficiency, it'll be a flat list of just companion ID: "companions": [7, 10, 4, 5, 9, 2, 3, 6]
            raw_companions = self.raw_data.get('companions', None)
            if raw_companion is not None:
                if isinstance(raw_companion, dict):
                    for companionInfo in raw_companion.get('l', []):
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
            elif raw_companions is not None:
                # print(f"Efficiency Companions data found: {raw_companions}")
                try:
                    self.doot_owned = g.doot or 0 in raw_companions
                    g.doot = self.doot_owned
                    self.riftslug_owned = g.riftslug or 1 in raw_companions
                    g.riftslug = self.riftslug_owned
                    self.sheepie_owned = g.sheepie or 4 in raw_companions
                    g.sheepie = self.sheepie_owned
                except Exception as e:
                    print(f"Efficiency Companions parse error: {e}, raw_companions={raw_companions}")
            # else:
            #     print(f"No companion data present in JSON")
        # print(f"Account model: Doot={self.doot_owned}, Slug={self.riftslug_owned}, Sheepie={self.sheepie_owned}")
        # print(f"Switches after: Doot={g.doot}, Slug={g.riftslug}, Sheepie={g.sheepie}")

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
        self.max_toon_count = max(maxCharacters, playerCount)  # OPTIMIZE: find a way to read this from somewhere
        self._parse_character_class_lists()

    def _parse_character_class_lists(self):
        self.beginners: list[Character] = [toon for toon in self.all_characters if "Beginner" in toon.all_classes or "Journeyman" in toon.all_classes]
        self.jmans: list[Character] = [toon for toon in self.all_characters if "Journeyman" in toon.all_classes]
        self.maestros: list[Character] = [toon for toon in self.all_characters if "Maestro" in toon.all_classes]
        self.vmans: list[Character] = [toon for toon in self.all_characters if "Voidwalker" in toon.all_classes]

        self.barbs: list[Character] = [toon for toon in self.all_characters if "Barbarian" in toon.all_classes]
        self.bbs: list[Character] = [toon for toon in self.all_characters if "Blood Berserker" in toon.all_classes]
        self.dks: list[Character] = [toon for toon in self.all_characters if "Divine Knight" in toon.all_classes]

    def _parse_general(self):
        # General / Multiple uses
        self.raw_optlacc_dict = {k: v for k, v in enumerate(safe_loads(self.raw_data.get("OptLacc", [])))}
        # Toolbox provides serverVars,Efficiency provides servervars, otherwise return an empty dict if neither present
        self.raw_serverVars_dict = safe_loads(self.raw_data.get("serverVars", self.raw_data.get("servervars", {})))

        self.stored_assets = self._all_stored_items()
        self.worn_assets = self._all_worn_items()
        self.all_assets = self.stored_assets + self.worn_assets

        self.cards = self._make_cards()

        self.minigame_plays_remaining = safer_get(self.raw_optlacc_dict, 33, 0)
        self.daily_world_boss_kills = safer_get(self.raw_optlacc_dict, 195, 0)
        self.daily_particle_clicks_remaining = safer_get(self.raw_optlacc_dict, 135, 0)

        self._parse_class_unique_kill_stacks()
        self._parse_general_gemshop()
        self._parse_family_bonuses()
        self._parse_dungeon_upgrades()
        self._parse_general_achievements()
        self._parse_general_merits()
        self._parse_general_guild_bonuses()
        self._parse_general_printer()
        self._parse_general_maps()
        self._parse_general_colo_scores()
        self._parse_general_event_points_shop()
        self._parse_general_quests()
        self._parse_general_npc_tokens()

    def _parse_general_gemshop(self):
        self.gemshop = {}
        raw_gem_items_purchased = safe_loads(self.raw_data.get("GemItemsPurchased", []))
        for purchaseName, purchaseIndex in gemShopDict.items():
            try:
                self.gemshop[purchaseName] = int(raw_gem_items_purchased[purchaseIndex])
            except:
                self.gemshop[purchaseName] = 0

    def _parse_general_quests(self):
        self.compiled_quests = {}
        for charIndex, questsDict in enumerate(self.all_quests):
            for questName, questStatus in questsDict.items():
                if questName not in self.compiled_quests:
                    self.compiled_quests[questName] = {
                        'CompletedCount': 0,
                        'CompletedChars': [],
                        'AcceptedCount': 0,
                        'AcceptedChars': [],
                        'UnacceptedCount': 0,
                        'UnacceptedChars': []
                    }
                if questStatus == 1:
                    status = 'Completed'
                elif questStatus == 0:
                    status = 'Accepted'
                else:  #Won't be reliable. If they haven't interacted with the NPC, their quest may not appear here at all.
                    status = 'Unaccepted'
                self.compiled_quests[questName][f'{status}Count'] += 1
                self.compiled_quests[questName][f'{status}Chars'].append(charIndex)

    def _parse_general_npc_tokens(self):
        self.npc_tokens = {}
        raw_npc_tokens = self.raw_data.get('CYNPC', [])
        for tokenIndex, tokenName in enumerate(npc_tokens):
            try:
                self.npc_tokens[tokenName] = int(raw_npc_tokens[tokenIndex])
            except:
                self.npc_tokens[tokenName] = 0
        # for tokenName, tokenCount in self.npc_tokens.items():
        #     self.all_assets.get(tokenName).add(tokenCount)

    def _parse_class_unique_kill_stacks(self):
        self.dk_orb_kills = safer_get(self.raw_optlacc_dict, 138, 0)
        self.sb_plunder_kills = safer_get(self.raw_optlacc_dict, 139, 0)
        self.es_wormhole_kills = safer_get(self.raw_optlacc_dict, 152, 0)

    def _parse_family_bonuses(self):
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

    def _parse_dungeon_upgrades(self):
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

    def _parse_general_achievements(self):
        self.achievements = {}
        raw_reg_achieves = safe_loads(self.raw_data.get('AchieveReg', []))
        for achieveIndex, achieveData in enumerate(achievementsList):
            try:
                if achieveData[0].replace('_', ' ') != "FILLERZZZ ACH":
                    self.achievements[achieveData[0].replace('_', ' ')] = {
                        'Complete': raw_reg_achieves[achieveIndex] == -1,
                        'Raw': raw_reg_achieves[achieveIndex]
                    }
            except:
                self.achievements[achieveData[0].replace('_', ' ')] = {
                    'Complete': False,
                    'Raw': 0
                }

    def _parse_general_merits(self):
        self.merits = copy.deepcopy(allMeritsDict)
        raw_merits_list = safe_loads(self.raw_data.get("TaskZZ2", []))
        for worldIndex in self.merits:
            for meritIndex in self.merits[worldIndex]:
                try:
                    self.merits[worldIndex][meritIndex]["Level"] = int(raw_merits_list[worldIndex][meritIndex])
                except:
                    continue  # Already defaulted to 0 in Consts

    def _parse_general_guild_bonuses(self):
        self.guildBonuses = {}
        raw_guild = safe_loads(self.raw_data.get('Guild', [[]]))
        for bonusIndex, bonusName in enumerate(guildBonusesList):
            try:
                self.guildBonuses[bonusName] = raw_guild[0][bonusIndex]
            except:
                self.guildBonuses[bonusName] = 0

    def _parse_general_printer(self):
        self.printer = {
            'HighestValue': 0,
            'AllSamplesSorted': {},
            'CurrentPrintsByCharacter': {},
            'AllCurrentPrints': {},
        }

        raw_print = safe_loads(self.raw_data.get('Print', [0, 0, 0, 0, 0, 'Blank']))[5:]
        raw_printer_xtra = safe_loads(self.raw_data.get('PrinterXtra', []))
        self._parse_general_item_filter(raw_printer_xtra)
        self.printer['HighestValue'] = max([p for p in raw_print if isinstance(p, int)] + [p for p in raw_printer_xtra if isinstance(p, int)], default=0)

        try:
            sample_names = raw_print[0::2] + raw_printer_xtra[0:119:2]
            sample_values = raw_print[1::2] + raw_printer_xtra[1:119:2]
        except:
            sample_names = []
            sample_values = []
        for sampleIndex, sampleItem in enumerate(sample_names):
            if sampleItem:
                if sampleIndex in printerAllIndexesBeingPrinted:
                    if sampleIndex//7 not in self.printer['CurrentPrintsByCharacter']:
                        self.printer['CurrentPrintsByCharacter'][sampleIndex // 7] = {}
                    if getItemDisplayName(sampleItem) not in self.printer['CurrentPrintsByCharacter'][sampleIndex//7]:
                        self.printer['CurrentPrintsByCharacter'][sampleIndex // 7][getItemDisplayName(sampleItem)] = []
                    try:
                        self.printer['CurrentPrintsByCharacter'][sampleIndex // 7][getItemDisplayName(sampleItem)].append(sample_values[sampleIndex])
                    except Exception as reason:
                        print(f"failed on characterIndex '{sampleIndex // 7}', sampleIndex '{sampleIndex}', sampleItem '{sampleItem}', because: {reason}")
                else:
                    if sampleItem != 'Blank':  #Don't want blanks in the AllSorted list, but they're desired in the Character-Specific group
                        if getItemDisplayName(sampleItem) not in self.printer['AllSamplesSorted']:
                            self.printer['AllSamplesSorted'][getItemDisplayName(sampleItem)] = []
                        try:
                            self.printer['AllSamplesSorted'][getItemDisplayName(sampleItem)].append(float(sample_values[sampleIndex]))
                        except Exception as reason:
                            print(f"models._parse_general_printer Failed on sampleIndex '{sampleIndex}', sampleItem '{sampleItem}', because: {reason}")
        for sampleItem in self.printer['AllSamplesSorted']:
            self.printer['AllSamplesSorted'][sampleItem].sort(reverse=True)
        for characterIndex, printDict in self.printer['CurrentPrintsByCharacter'].items():
            if characterIndex < self.playerCount:
                self.all_characters[characterIndex].setPrintedMaterials(printDict)
            for printName, printValues in printDict.items():
                if printName not in self.printer['AllCurrentPrints']:
                    self.printer['AllCurrentPrints'][printName] = []
                self.printer['AllCurrentPrints'][printName] += printValues

    def _parse_general_item_filter(self, raw_printer_xtra):
        self.item_filter = []
        if len(raw_printer_xtra) >= 121:
            for codeName in raw_printer_xtra[120:]:
                if codeName != 'Blank':
                    self.item_filter.append(codeName)

    def _parse_general_maps(self):
        self.enemy_maps = buildMaps()
        self.enemy_worlds = {}

    def _parse_general_colo_scores(self):
        self.colo_scores = {}
        raw_colo_scores = safe_loads(self.raw_data.get('FamValColosseumHighscores', []))
        for coloIndex, coloScore in enumerate(raw_colo_scores):
            try:
                self.colo_scores[coloIndex] = int(coloScore)
            except:
                self.colo_scores[coloIndex] = 0

    def _parse_general_event_points_shop(self):
        self.event_points_shop = {
            'Points Owned': safer_get(self.raw_optlacc_dict, 310, 0),
            'Raw Purchases': safer_get(self.raw_optlacc_dict, 311, ''),
            'Bonuses': {}
        }
        if isinstance(self.event_points_shop['Raw Purchases'], str):
            self.event_points_shop['Raw Purchases'] = list(self.event_points_shop['Raw Purchases'])
        else:
            print(f"models._parse_general_event_points_shop: Purchases not String type: {type(self.event_points_shop['Raw Purchases'])} with value of: {self.event_points_shop['Raw Purchases']}")
            self.event_points_shop['Raw Purchases'] = []
        for bonusName, bonusDetails in event_points_shop_dict.items():
            try:
                self.event_points_shop['Bonuses'][bonusName] = {
                    'Owned': bonusDetails['Code'] in self.event_points_shop['Raw Purchases'],
                    'Cost': bonusDetails['Cost'],
                    'Description': bonusDetails['Description'],
                }
            except:
                self.event_points_shop['Bonuses'][bonusName] = {
                    'Owned': False,
                    'Cost': bonusDetails['Cost'],
                    'Description': bonusDetails['Description'],
                }

    def _parse_w1(self):
        self._parse_w1_starsigns()
        self._parse_w1_forge()
        self._parse_w1_bribes()
        self._parse_w1_stamps()
        self._parse_w1_owl()
        self._parse_w1_statues()

    def _parse_w1_starsigns(self):
        self.star_signs = {}
        self.star_sign_extras = {"UnlockedSigns": 0}
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
                if self.star_signs[signValuesDict['Name']]['Unlocked']:
                    self.star_sign_extras['UnlockedSigns'] += 1
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
        self.owl = {
            'Discovered': bool(safer_get(self.raw_optlacc_dict, 265, False)),
            'FeatherGeneration': safer_get(self.raw_optlacc_dict, 254, 0),
            'BonusesOfOrion': safer_get(self.raw_optlacc_dict, 255, 0),
            'FeatherRestarts': safer_get(self.raw_optlacc_dict, 258, 0),
            'MegaFeathersOwned': safer_get(self.raw_optlacc_dict, 262, 0)
        }

    def _parse_w1_statues(self):
        self.statues = {}
        self.maxed_statues = 0
        #"StuG": "[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0]",
        raw_statue_type_list = safe_loads(self.raw_data.get("StuG", []))
        if not raw_statue_type_list:
            raw_statue_type_list = [0]*statueCount
        self.onyx_statues_unlocked = max(raw_statue_type_list, default=0) >= statueTypeList.index("Onyx")
        statue_levels = [0]*statueCount

        #Find the maximum value across all characters. Only matters while Normal, since Gold shares across all characters
        for char in self.safe_characters:
            try:
                char_statues = safe_loads(self.raw_data.get(f"StatueLevels_{char.character_index}"))
                for statueIndex, statueDetails in enumerate(char_statues):
                    if statueDetails[0] > statue_levels[statueIndex]:
                        statue_levels[statueIndex] = statueDetails[0]
            except:
                continue

        for statueIndex, statueDetails in statuesDict.items():
            try:
                self.statues[statueDetails['Name']] = {
                    'Level': statue_levels[statueIndex],
                    'Type': statueTypeList[raw_statue_type_list[statueIndex]],  #Description: Normal, Gold, Onyx
                    'TypeNumber': raw_statue_type_list[statueIndex],  #Integer: 0-2
                    'ItemName': statueDetails['ItemName'],
                    'Effect': statueDetails['Effect'],
                    'BaseValue': statueDetails['BaseValue'],
                    'Value': statueDetails['BaseValue'],  # Handled in _calculate_w1_statue_multi()
                    'Farmer': statueDetails['Farmer'],
                    'Target': statueDetails['Target'],
                }
            except:
                self.statues[statueDetails['Name']] = {
                    'Level': 0,
                    'Type': statueTypeList[raw_statue_type_list[statueIndex]],
                    'TypeNumber': raw_statue_type_list[0],
                    'ItemName': statueDetails['ItemName'],
                    'Effect': statueDetails['Effect'],
                    'BaseValue': statueDetails['BaseValue'],
                    'Value': statueDetails['BaseValue'],  # Handled in _calculate_w1_statue_multi()
                    'Farmer': statueDetails['Farmer'],
                    'Target': statueDetails['Target'],
                }
            if self.statues[statueDetails['Name']]['TypeNumber'] >= len(statueTypeList)-1:
                self.maxed_statues += 1

    def _parse_w2(self):
        self._parse_w2_vials()
        self._parse_w2_cauldrons()
        self._parse_w2_bubbles()
        self._parse_w2_p2w()
        self._parse_w2_arcade()
        self._parse_w2_ballot()
        self._parse_w2_obols()
        self._parse_w2_islands()
        self._parse_w2_killroy()

    def _parse_w2_vials(self):
        self.alchemy_vials = {}
        manualVialsAdded = 0
        raw_alchemy_vials = safe_loads(self.raw_data.get("CauldronInfo", [0, 0, 0, 0, {}])[4])
        if "length" in raw_alchemy_vials:
            del raw_alchemy_vials["length"]
        while len(raw_alchemy_vials) < max_IndexOfVials:
            raw_alchemy_vials[int(max_IndexOfVials - manualVialsAdded)] = 0
            manualVialsAdded += 1
        for vialKey, vialValue in raw_alchemy_vials.items():
            try:
                if int(vialKey) < max_IndexOfVials:
                    self.alchemy_vials[getReadableVialNames(vialKey)] = {
                        'Level': int(vialValue),
                        'Value': lavaFunc(
                            vialsDict[int(vialKey)]['funcType'],
                            int(vialValue),
                            vialsDict[int(vialKey)]['x1'],
                            vialsDict[int(vialKey)]['x2'],
                        ),
                        'Material': vialsDict[int(vialKey)]['Material']
                    }
            except:
                try:
                    self.alchemy_vials[getReadableVialNames(vialKey)] = {"Level": 0, "Value": 0, 'Material': vialsDict[int(vialKey)]['Material']}
                except:
                    continue
        self.maxed_vials = 0
        for vial in self.alchemy_vials.values():
            if vial.get("Level", 0) >= max_VialLevel:
                self.maxed_vials += 1

    def _parse_w2_cauldrons(self):
        raw_cauldron_upgrades = self.raw_data.get('CauldUpgLVs', [])
        self.alchemy_cauldrons = {
            'OrangeUnlocked': 0,
            'GreenUnlocked': 0,
            'PurpleUnlocked': 0,
            'YellowUnlocked': 0,
            'TotalUnlocked': 0,
        }
        try:
            self.alchemy_cauldrons["OrangeBoosts"] = [
                raw_cauldron_upgrades[0],
                raw_cauldron_upgrades[1],
                raw_cauldron_upgrades[2],
                raw_cauldron_upgrades[3],
            ]
            self.alchemy_cauldrons["GreenBoosts"] = [
                raw_cauldron_upgrades[4],
                raw_cauldron_upgrades[5],
                raw_cauldron_upgrades[6],
                raw_cauldron_upgrades[7],
            ]
            self.alchemy_cauldrons["PurpleBoosts"] = [
                raw_cauldron_upgrades[8],
                raw_cauldron_upgrades[9],
                raw_cauldron_upgrades[10],
                raw_cauldron_upgrades[11],
            ]
            self.alchemy_cauldrons["PurpleBoosts"] = [
                raw_cauldron_upgrades[12],
                raw_cauldron_upgrades[13],
                raw_cauldron_upgrades[14],
                raw_cauldron_upgrades[15],
            ]
        except:
            self.alchemy_cauldrons["OrangeBoosts"]: [0, 0, 0, 0]
            self.alchemy_cauldrons["GreenBoosts"]: [0, 0, 0, 0]
            self.alchemy_cauldrons["PurpleBoosts"]: [0, 0, 0, 0]
            self.alchemy_cauldrons["YellowBoosts"]: [0, 0, 0, 0]
        try:
            self.alchemy_cauldrons["WaterDroplets"] = [raw_cauldron_upgrades[18], raw_cauldron_upgrades[19]]
            self.alchemy_cauldrons["LiquidNitrogen"] = [raw_cauldron_upgrades[22], raw_cauldron_upgrades[23]]
            self.alchemy_cauldrons["TrenchSeawater"] = [raw_cauldron_upgrades[26], raw_cauldron_upgrades[27]]
            self.alchemy_cauldrons["ToxicMercury"] = [raw_cauldron_upgrades[30], raw_cauldron_upgrades[31]]
        except:
            self.alchemy_cauldrons["WaterDroplets"] = [0, 0]
            self.alchemy_cauldrons["LiquidNitrogen"] = [0, 0]
            self.alchemy_cauldrons["TrenchSeawater"] = [0, 0]
            self.alchemy_cauldrons["ToxicMercury"] = [0, 0]

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
                except:
                    pass  # Already defaulted to 0s in consts.sigilsDict

    def _parse_w2_arcade(self):
        self.arcade = {}
        raw_arcade_upgrades = safe_loads(self.raw_data.get("ArcadeUpg", []))
        for upgradeIndex, upgradeDetails in arcadeBonuses.items():
            try:
                self.arcade[upgradeIndex] = {
                    'Level': raw_arcade_upgrades[upgradeIndex],
                    'Value': lavaFunc(
                        upgradeDetails.get("funcType"),
                        raw_arcade_upgrades[upgradeIndex],
                        upgradeDetails.get("x1"),
                        upgradeDetails.get("x2")
                    )
                }
                self.arcade[upgradeIndex]["Display"] = (
                    f"+{self.arcade[upgradeIndex]['Value']:.2f}{upgradeDetails['displayType']} {upgradeDetails['Stat']}"
                )
            except:
                self.arcade[upgradeIndex] = {
                    'Level': 0,
                    'Value': lavaFunc(
                        upgradeDetails.get("funcType"),
                        0,
                        upgradeDetails.get("x1"),
                        upgradeDetails.get("x2")
                    )
                }
                self.arcade[upgradeIndex]["Display"] = (
                    f"+{self.arcade[upgradeIndex]['Value']:.2f}{arcadeBonuses[upgradeIndex]['displayType']} {arcadeBonuses[upgradeIndex]['Stat']}"
                )

    def _parse_w2_ballot(self):
        self.ballot = {
            "CurrentBuff": self.raw_serverVars_dict.get('voteCategories', ["Unknown"])[0],
            "Buffs": {}
        }
        for buffIndex, buffValuesDict in ballotDict.items():
            self.ballot['Buffs'][buffIndex] = {
                'Description': buffValuesDict['Description'],
                'BaseValue': buffValuesDict['BaseValue'],
                'Value': buffValuesDict['BaseValue'],
                'Image': buffValuesDict['Image'],
            }

    def _parse_w2_obols(self):
        #Please send help, I hate Obols so much
        self.obols = {
            'Unknown': {
                'Unknown': {'Total': 0},
                'Circle': {'Total': 0},
                'Square': {'Total': 0},
                'Hexagon': {'Total': 0},
                'Sparkle': {'Total': 0},
            },
            'Drop Rate': {
                'Circle': {'Total': 0},
                'Square': {'Total': 0},
                'Hexagon': {'Total': 0},
                'Sparkle': {'Total': 0},
            },
            'Choppin': {
                'Circle': {'Total': 0},
                'Square': {'Total': 0},
                'Hexagon': {'Total': 0},
                'Sparkle': {'Total': 0},
            },
        }
        raw_owned_obols = []
        for jsonkey in [
            "ObolEqO1","ObolEqO2", "ObolEqO0_0", "ObolEqO0_1", "ObolEqO0_2", "ObolEqO0_3", "ObolEqO0_4",
            "ObolEqO0_5", "ObolEqO0_6", "ObolEqO0_7", "ObolEqO0_8", "ObolEqO0_9"
        ]:
            raw_owned_obols += safe_loads(self.raw_data.get(jsonkey, []))
        raw_obol_inventory_list = safe_loads(self.raw_data.get("ObolInvOr"))
        for subdict in raw_obol_inventory_list:
            raw_owned_obols += subdict.values()
        for obol in raw_owned_obols:
            if obol not in ignorable_obols_list:
                obolBonusType = obolsDict.get(obol, {}).get('Bonus', 'Unknown')
                obolShape = obolsDict.get(obol, {}).get('Shape', 'Unknown')
                self.obols[obolBonusType][obolShape]['Total'] += 1
                if obol not in self.obols[obolBonusType][obolShape]:
                    self.obols[obolBonusType][obolShape][obol] = {'Count': 1}
                else:
                    self.obols[obolBonusType][obolShape][obol]['Count'] += 1
        #print(f"session_data.account.obols: {self.obols['Drop Rate']}")

    def _parse_w2_islands(self):
        self.islands = {
            'Trash': int(float(safer_get(self.raw_optlacc_dict, 161, 0))),  #[161]: 362.202271805249
            'Bottles': int(float(safer_get(self.raw_optlacc_dict, 162, 0))),  #[162]: 106.90044163281846
        }

        raw_islands_list = list(str(safer_get(self.raw_optlacc_dict, 169, '')))  #[169]: "_dcabe" or could be int 0 for whatever reason...
        for islandName, islandData in islands_dict.items():
            self.islands[islandName] = {
                'Unlocked': islandData['Code'] in raw_islands_list,
                'Description': islandData['Description']
            }

        self.nothing_hours = safer_get(self.raw_optlacc_dict, 184, 0)

    def _parse_w2_killroy(self):
        self._parse_w2_killroy_skull_shop()
        self.killroy = {}
        self.killroy_total_fights = safer_get(self.raw_optlacc_dict, 112, 0)
        for upgradeName, upgradeDict in killroy_dict.items():
            self.killroy[upgradeName] = {
                'Available': False,
                'Remaining': max(0, upgradeDict['Required Fights'] - self.killroy_total_fights),
                'Upgrades': safer_get(self.raw_optlacc_dict, upgradeDict['UpgradesIndex'], 0),
                'Image': upgradeDict['Image']
            }

    def _parse_w2_killroy_skull_shop(self):
        self.killroy_skullshop = {
            'Third Battle Unlocked': safer_get(self.raw_optlacc_dict, 227, 0) == 1,
            'Artifact Purchases': safer_get(self.raw_optlacc_dict, 228, 0),
            'Artifact Multi': 1 + (safer_get(self.raw_optlacc_dict, 228, 0) / (300 + safer_get(self.raw_optlacc_dict, 228, 0))),
            'Crop Purchases': safer_get(self.raw_optlacc_dict, 229, 0),
            'Crop Multi': 1 + ((safer_get(self.raw_optlacc_dict, 229, 0) / (300 + safer_get(self.raw_optlacc_dict, 229, 0))) * 9),
            'Crop Multi Plus 1': 1 + (((1 + safer_get(self.raw_optlacc_dict, 229, 0)) / (1 + 300 + safer_get(self.raw_optlacc_dict, 229, 0))) * 9),
            'Jade Purchases': safer_get(self.raw_optlacc_dict, 230, 0),
            'Jade Multi': 1 + ((safer_get(self.raw_optlacc_dict, 230, 0) / (300 + safer_get(self.raw_optlacc_dict, 230, 0))) * 2),
        }

    def _parse_w3(self):
        self._parse_w3_refinery()
        self._parse_w3_buildings()
        self._parse_w3_library()
        self._parse_w3_deathnote()
        self._parse_w3_equinox_dreams()
        self._parse_w3_equinox_bonuses()
        self._parse_w3_shrines()
        self._parse_w3_atom_collider()
        self._parse_w3_prayers()
        self._parse_w3_saltlick()

    def _parse_w3_refinery(self):
        self.refinery = {}
        raw_refinery_list = safe_loads(self.raw_data.get("Refinery", []))
        for saltColor, saltDetails in refineryDict.items():
            try:
                self.refinery[saltColor] = {
                    'Rank': raw_refinery_list[saltDetails[0]][1],
                    'Running': raw_refinery_list[saltDetails[0]][3],
                    'AutoRefine': raw_refinery_list[saltDetails[0]][4],
                    'Image': saltDetails[1],
                    'CyclesPerSynthCycle': saltDetails[2],
                    'PreviousSaltConsumption': saltDetails[3],
                    'NextSaltConsumption': saltDetails[4],
                    'NextSaltCyclesPerSynthCycle': saltDetails[5]
                }
            except:
                self.refinery[saltColor] = {
                    'Rank': 0,
                    'Running': False,
                    'AutoRefine': 0,
                    'Image': saltDetails[1],
                    'CyclesPerSynthCycle': saltDetails[2],
                    'PreviousSaltConsumption': saltDetails[3],
                    'NextSaltConsumption': saltDetails[4],
                    'NextSaltCyclesPerSynthCycle': saltDetails[5]
                }

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
        self.library = {
            'BooksReady': safer_get(self.raw_optlacc_dict, 55, 0)
        }

    def _parse_w3_deathnote(self):
        self.apocCharactersIndexList = [c.character_index for c in self.barbs]
        self.bbCharactersIndexList = [c.character_index for c in self.bbs]
        self.meowBBIndex = self._parse_w3_meowBBIndex()
        self.rift_meowed = self._parse_w3_deathnote_rift_meowed()
        self._parse_w3_deathnote_kills()

    def _parse_w3_meowBBIndex(self):
        if len(self.bbCharactersIndexList) == 1:
            return self.bbCharactersIndexList[0]
        elif len(self.bbCharactersIndexList) >= 2:
            return self.bbCharactersIndexList[1]
        else:
            return None

    def _parse_w3_deathnote_rift_meowed(self):
        if self.meowBBIndex is not None:
            riftPresent = False
            for remainingMap in self.all_characters[self.meowBBIndex].apoc_dict['MEOW']['Medium Extras']:
                if remainingMap[0] == 'The Rift':
                    riftPresent = True
                    break
            if not riftPresent:
                self.rift_meowed = True
        else:
            riftPresent = True
        return not riftPresent

    def _parse_w3_deathnote_kills(self):
        # total up all kills across characters
        for characterIndex, characterData in enumerate(self.all_characters):
            characterKillsDict = characterData.kill_dict

            # If the character's subclass is Barbarian, add their special Apoc-Only kills to EnemyMap's zow_dict
            if characterIndex in self.apocCharactersIndexList:
                for worldIndex in range(0, len(apocableMapIndexDict)):
                    for mapIndex in apocableMapIndexDict[worldIndex]:
                        try:
                            self.enemy_maps[worldIndex][mapIndex].updateZOWDict(characterIndex, characterKillsDict.get(mapIndex, [0])[0])
                        except:
                            self.enemy_maps[worldIndex][mapIndex].updateZOWDict(characterIndex, 0)

            # Regardless of class, for each map within each world, add this player's kills to EnemyMap's kill_count
            for worldIndex in range(1, len(apocableMapIndexDict)):
                for mapIndex in apocableMapIndexDict[worldIndex]:
                    try:
                        self.enemy_maps[worldIndex][mapIndex].addRawKLA(characterKillsDict.get(mapIndex, [0])[0])
                    except:
                        self.enemy_maps[worldIndex][mapIndex].addRawKLA(0)

        # Have each EnemyMap calculate its Skull Value, Name, Count to Next, and Percent to Next now that all kills are totaled
        # Barbarian Only in worldIndex 0
        for worldIndex in range(1, len(self.enemy_maps)):
            for enemy_map in self.enemy_maps[worldIndex]:
                self.enemy_maps[worldIndex][enemy_map].generateDNSkull()
            # After each Map in that World has its Skull Info, create the corresponding EnemyWorld
            self.enemy_worlds[worldIndex] = EnemyWorld(worldIndex, self.enemy_maps[worldIndex])

        # Barbarian Only in 0
        for barbCharacterIndex in self.apocCharactersIndexList:
            for worldIndex in range(0, len(self.enemy_maps)):
                for enemy_map in self.enemy_maps[worldIndex]:
                    if barbCharacterIndex in self.enemy_maps[worldIndex][enemy_map].zow_dict:
                        # print("DN~ INFO barbCharacterIndex", barbCharacterIndex, "found in worldIndex", worldIndex, "enemy_map", enemy_map)
                        kill_count = self.enemy_maps[worldIndex][enemy_map].zow_dict[barbCharacterIndex]
                        for apocIndex, apocAmount in enumerate(apocAmountsList):
                            if kill_count < apocAmount:
                                # characterDict[barbCharacterIndex].apoc_dict[apocNamesList[apocIndex]][enemyMaps[worldIndex][enemy_map].zow_rating].append([
                                self.all_characters[barbCharacterIndex].addUnmetApoc(
                                    apocNamesList[apocIndex],
                                    self.enemy_maps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                                    [
                                        self.enemy_maps[worldIndex][enemy_map].map_name,  # map name
                                        apocAmount - kill_count if apocIndex < 3 else kill_count,  # kills short of zow/chow/meow
                                        floor((kill_count / apocAmount) * 100),  # percent toward zow/chow/meow
                                        self.enemy_maps[worldIndex][enemy_map].monster_image,  # monster image
                                        worldIndex
                                    ]
                                )
                            else:
                                self.all_characters[barbCharacterIndex].increaseApocTotal(apocNamesList[apocIndex])
                    else:
                        # This condition can be hit when reviewing data from before a World release
                        # For example, JSON data from w5 before w6 is released hits this to populate 0% toward W6 kills
                        for apocIndex, apocAmount in enumerate(apocAmountsList):
                            self.all_characters[barbCharacterIndex].addUnmetApoc(
                                apocNamesList[apocIndex], self.enemy_maps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                                [
                                    self.enemy_maps[worldIndex][enemy_map].map_name,  # map name
                                    apocAmountsList[apocIndex],  # kills short of zow/chow/meow
                                    0,  # percent toward zow/chow/meow
                                    self.enemy_maps[worldIndex][enemy_map].monster_image,  # monster image
                                    worldIndex
                                ]
                            )
            # Sort them
            self.all_characters[barbCharacterIndex].sortApocByProgression()

    def _parse_w3_equinox_dreams(self):
        self.equinox_unlocked = self.achievements['Equinox Visitor']['Complete']
        self.equinox_dreams = [True]  #d_0 in the code is Dream 1. By padding the first slot, we can get Dream 1 by that same index: equinox_dreams[1]
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
                    5: int(raw_shrines_list[shrineIndex][5]),
                    "BaseValue": (
                        buildingsDict[18+shrineIndex]['ValueBase']
                        + (buildingsDict[18+shrineIndex]['ValueIncrement'] * (int(raw_shrines_list[shrineIndex][3]) - 1))
                        if int(raw_shrines_list[shrineIndex][3]) > 0 else 0
                    ),
                    "Value": (
                        buildingsDict[18+shrineIndex]['ValueBase']
                        + (buildingsDict[18+shrineIndex]['ValueIncrement'] * (int(raw_shrines_list[shrineIndex][3]) - 1))
                        if int(raw_shrines_list[shrineIndex][3]) > 0 else 0
                    ),
                    'Image': buildingsDict[18+shrineIndex]['Image']
                }
            except:
                self.shrines[shrineName] = {
                    "MapIndex": 0,
                    1: 0,
                    2: 0,
                    "Level": 0,
                    "Hours": 0.0,
                    5: 0,
                    "BaseValue": 0,
                    "Value": 0,
                    'Image': buildingsDict[18 + shrineIndex]['Image']
                }

    def _parse_w3_atom_collider(self):
        self.atom_collider = {
            'OnOffStatus': bool(safer_get(self.raw_optlacc_dict, 132, 1)),
        }
        try:
            self.atom_collider['StorageLimit'] = colliderStorageLimitList[safer_get(self.raw_optlacc_dict, 133, -1)]
        except:
            self.atom_collider['StorageLimit'] = colliderStorageLimitList[-1]
        try:
            self.atom_collider['Particles'] = self.raw_data.get("Divinity", {})[39]
        except:
            self.atom_collider['Particles'] = "Unknown"  #0.0

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
        self._parse_w4_breeding()

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
        self.cooking['Tables'] = raw_cooking_list
        self.cooking['Tables Owned'] = sum(1 for table in self.cooking['Tables'] if table[0] == 2)

    def _parse_w4_cooking_meals(self):
        emptyMeal = [0] * maxMeals
        # Meals contains 4 lists of lists. The first 3 are as long as the number of plates. The 4th is general shorter.
        emptyMeals = [emptyMeal for meal in range(4)]
        raw_meals_list = safe_loads(self.raw_data.get("Meals", emptyMeals))
        # Make the sublists maxMeals long
        for sublistIndex, value in enumerate(raw_meals_list):
            if isinstance(raw_meals_list[sublistIndex], list):
                while len(raw_meals_list[sublistIndex]) < maxMeals:
                    raw_meals_list[sublistIndex].append(0)
                while len(raw_meals_list[sublistIndex]) > maxMeals:
                    raw_meals_list[sublistIndex].pop()

        self.meals = {}
        # Count the number of unlocked meals, unlocked meals under 11, and unlocked meals under 30
        for index, mealLevel in enumerate(raw_meals_list[0]):
            # Create meal dict
            self.meals[cookingMealDict[index]["Name"]] = {
                "Level": int(mealLevel),
                "Value": int(mealLevel) * cookingMealDict[index]["BaseValue"],  # Mealmulti applied in calculate section
                "BaseValue": cookingMealDict[index]["BaseValue"]
            }

            if int(mealLevel) > 0:
                self.cooking['MealsUnlocked'] += 1
                self.cooking['PlayerTotalMealLevels'] += int(mealLevel)
                if int(mealLevel) < 11:
                    self.cooking['MealsUnder11'] += 1
                if int(mealLevel) < 30:
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
        for labChipIndex, labChip in labChipsDict.items():
            try:
                self.labChips[labChip["Name"]] = max(0, int(raw_labChips_list[labChipIndex]))
            except:
                self.labChips[labChip["Name"]] = 0

    def _parse_w4_lab_bonuses(self, raw_lab):
        #TODO: Actually figure out lab :(
        self.labBonuses = {}
        for index, node in labBonusesDict.items():
            self.labBonuses[node["Name"]] = {
                "Enabled": True,
                "Owned": True,  # For W6 nodes
                "Value": node["BaseValue"],  # Currently no modifiers available, might change if the pure opal navette changes
                "BaseValue": node["BaseValue"]
            }

    def _parse_w4_jewels(self, raw_lab):
        #TODO: Account for if the jewel is actually connected.

        self.labJewels = {}
        for jewelIndex, jewelInfo in labJewelsDict.items():
            try:
                self.labJewels[jewelInfo["Name"]] = {
                    "Owned": bool(raw_lab[14][jewelIndex]),
                    "Enabled": bool(raw_lab[14][jewelIndex]),  # Same as owned until connection range is implemented
                    "Value": jewelInfo["BaseValue"],  # Jewelmulti added in calculate section
                    "BaseValue": jewelInfo["BaseValue"]
                }
            except:
                self.labJewels[jewelInfo["Name"]] = {
                    "Owned": False,
                    "Enabled": False,  # Same as owned until connection range is implemented
                    "Value": jewelInfo["BaseValue"],  # Jewelmulti added in calculate section
                    "BaseValue": jewelInfo["BaseValue"]
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
        for riftLevel, riftBonusDict in riftRewardsDict.items():
            self.rift[riftBonusDict['Shorthand']] = self.rift['Level'] >= riftLevel

    def _parse_w4_breeding(self):
        self.breeding = {
            'Egg Slots': 3,
            'Unlocked Counts': {
                "W1": 0,
                "W2": 0,
                "W3": 0,
                "W4": 0,
                "W5": 0,
                "W6": 0,
                "W7": 0,
                "W8": 0,
            },
            'Total Unlocked Count': 0,
            'Breedability Days': {
                "W1": [],
                "W2": [],
                "W3": [],
                "W4": [],
                "W5": [],
                "W6": [],
                "W7": [],
                "W8": [],
            },
            'Shiny Days': {
                "W1": [],
                "W2": [],
                "W3": [],
                "W4": [],
                "W5": [],
                "W6": [],
                "W7": [],
                "W8": [],
            },
            "Genetics": {},
            "Species": {},
            "Total Shiny Levels": {},
            "Grouped Bonus": {},
            'Territories': {},
            'Highest Unlocked Territory Number': 0,
            'Highest Unlocked Territory Name': '',
            'Upgrades': {},
            'ArenaMaxWave': 0,
            'PetSlotsUnlocked': 2,
        }
        raw_breeding_list = safe_loads(self.raw_data.get("Breeding", []))
        raw_territory_list = safe_loads(self.raw_data.get("Territory", []))
        raw_breeding_pets = safe_loads(self.raw_data.get("Pets", []))

        self._parse_w4_breeding_defaults()
        self._parse_w4_breeding_misc()
        self._parse_w4_breeding_upgrades(raw_breeding_list)
        self._parse_w4_breeding_territories(raw_breeding_pets, raw_territory_list)
        self._parse_w4_breeding_pets(raw_breeding_list)
        self.breeding['Egg Slots'] += (
            self.gemshop['Royal Egg Cap']
            + self.breeding['Upgrades']['Egg Capacity']['Level']
            + self.merits[3][2]['Level']
        )

    def _parse_w4_breeding_defaults(self):
        # Abilities defaulted to False
        for genetic in breedingGeneticsList:
            self.breeding["Genetics"][genetic] = False

        # Total Shiny Bonus Levels defaulted to 0
        #Grouped Bonus per Shiny Bonus defaulted to empty list
        for bonus in breedingShinyBonusList:
            self.breeding["Total Shiny Levels"][bonus] = 0
            self.breeding['Grouped Bonus'][bonus] = []

    def _parse_w4_breeding_misc(self):
        #Highest Arena Wave
        try:
            self.breeding['ArenaMaxWave'] = int(self.raw_data["OptLacc"][89])
        except:
            pass

        #Number of Pet Slots Unlocked
        for requirement in slotUnlockWavesList:
            if self.breeding['ArenaMaxWave'] > requirement:
                self.breeding['PetSlotsUnlocked'] += 1

    def _parse_w4_breeding_upgrades(self, rawBreeding):
        for upgradeIndex, upgradeValuesDict in breedingUpgradesDict.items():
            try:
                self.breeding['Upgrades'][upgradeValuesDict['Name']] = {
                    'Level': rawBreeding[2][upgradeIndex],
                    'MaxLevel': upgradeValuesDict['MaxLevel'],
                    'Value': upgradeValuesDict['BonusValue'] * rawBreeding[2][upgradeIndex]
                }
            except:
                self.breeding['Upgrades'][upgradeValuesDict['Name']] = {
                    'Level': 0,
                    'MaxLevel': upgradeValuesDict['MaxLevel'],
                    'Value': 0
                }

    def _parse_w4_breeding_territories(self, rawPets, rawTerritory):
        anyPetsAssignedPerTerritory: list[bool] = []
        for territoryIndex in range(0, maxNumberOfTerritories):
            try:
                if rawPets[indexFirstTerritoryAssignedPet + 0 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                elif rawPets[indexFirstTerritoryAssignedPet + 1 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                elif rawPets[indexFirstTerritoryAssignedPet + 2 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                elif rawPets[indexFirstTerritoryAssignedPet + 3 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                else:
                    anyPetsAssignedPerTerritory.append(False)
            except:
                anyPetsAssignedPerTerritory.append(False)

            # Spice Progress above 0 or any pet assigned to territory
            try:
                if rawTerritory[territoryIndex][0] > 0 or anyPetsAssignedPerTerritory[territoryIndex] == True:
                    #Can't decide which of these 3 will end up being the most useful, so assigning them all for now
                    self.breeding['Territories'][territoryNames[territoryIndex+1]] = {'Unlocked': True}
                    self.breeding["Highest Unlocked Territory Number"] = territoryIndex+1
                    self.breeding["Highest Unlocked Territory Name"] = territoryNames[territoryIndex+1]
            except:
                self.breeding['Territories'][territoryNames[territoryIndex + 1]] = {'Unlocked': False}

    def _parse_w4_breeding_pets(self, rawBreeding):
        #Unlocked Counts per World
        for index in range(0, 8):
            try:
                self.breeding['Unlocked Counts'][f"W{index+1}"] = rawBreeding[1][index]
                self.breeding['Total Unlocked Count'] += rawBreeding[1][index]
            except:
                continue  #Already defaulted to 0 during initialization

        # Breedability Days
        for index in range(13, 21):
            try:
                self.breeding['Breedability Days'][f"W{index - 12}"] = rawBreeding[index]
            except:
                continue  # Already default to [] during initialization

        #Shiny Days
        for index in range(22, 30):
            try:
                self.breeding['Shiny Days'][f"W{index-21}"] = rawBreeding[index]
            except:
                continue  #Already defaulted to [] during initialization

        #Parse data for each individual pet, increase their shiny bonus level, and mark their Genetic as obtained
        for worldIndex, worldPetsDict in breedingSpeciesDict.items():
            self.breeding['Species'][worldIndex] = {}
            for petIndex, petValuesDict in worldPetsDict.items():
                try:
                    self.breeding['Species'][worldIndex][petValuesDict['Name']] = {
                        'Unlocked': self.breeding['Unlocked Counts'][f"W{worldIndex}"] > petIndex,
                        'Genetic': petValuesDict['Genetic'],
                        'ShinyBonus': petValuesDict['ShinyBonus'],
                        'ShinyLevel': getShinyLevelFromDays(self.breeding['Shiny Days'][f"W{worldIndex}"][petIndex]),
                        'DaysToShinyLevel': getDaysToNextShinyLevel(self.breeding['Shiny Days'][f"W{worldIndex}"][petIndex]),
                        'BreedabilityDays': self.breeding['Breedability Days'][f"W{worldIndex}"][petIndex],
                        'BreedabilityMulti': getBreedabilityMultiFromDays(self.breeding['Breedability Days'][f"W{worldIndex}"][petIndex]),
                        'BreedabilityHeart': getBreedabilityHeartFromMulti(getBreedabilityMultiFromDays(self.breeding['Breedability Days'][f"W{worldIndex}"][petIndex])),
                    }
                    #Increase the total shiny bonus level
                    self.breeding["Total Shiny Levels"][petValuesDict['ShinyBonus']] += self.breeding['Species'][worldIndex][petValuesDict['Name']]['ShinyLevel']
                    #If this pet is unlocked, but their Genetic isn't marked as unlocked, update the Abilities
                    if self.breeding['Species'][worldIndex][petValuesDict['Name']]['Unlocked'] and not self.breeding["Genetics"][petValuesDict['Genetic']]:
                        self.breeding["Genetics"][petValuesDict['Genetic']] = True
                except Exception as reason:
                    print(f"models._parse_w4_breeding_pets EXCEPTION: Failed to parse breeding pet {petValuesDict['Name']}: {reason}")
                    self.breeding['Species'][worldIndex][petValuesDict['Name']] = {
                        'Unlocked': False,
                        'Genetic': petValuesDict['Genetic'],
                        'ShinyBonus': petValuesDict['ShinyBonus'],
                        'ShinyLevel': 0,
                        'DaysToShinyLevel': 0,
                        'BreedabilityDays': 0.0,
                        'BreedabilityMulti': 1,
                        'BreedabilityHeart': 'breedability-heart-1',
                    }
                # Add this pet to the shiny bonus grouped list
                self.breeding['Grouped Bonus'][petValuesDict['ShinyBonus']].append(
                    (
                        petValuesDict['Name'],
                        self.breeding['Species'][worldIndex][petValuesDict['Name']]['ShinyLevel'],
                        self.breeding['Species'][worldIndex][petValuesDict['Name']]['DaysToShinyLevel'],
                    )
                )

        #Sort the Grouped bonus by Days to next Shiny Level
        for groupedBonus in self.breeding["Grouped Bonus"]:
            self.breeding["Grouped Bonus"][groupedBonus].sort(key=lambda x: float(x[2]))

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
            #Bits Owned sometimes Float, sometimes String
            try:
                self.gaming['BitsOwned'] = float(raw_gaming_list[0])
            except:
                pass

            try:
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
                self.gaming['SuperBitsString'] = str(raw_gaming_list[12])
                self.gaming['Envelopes'] = raw_gaming_list[13]
            except:
                pass

        for index, valuesDict in gamingSuperbitsDict.items():
            try:
                self.gaming['SuperBits'][valuesDict['Name']] = {
                    'Unlocked': valuesDict['CodeString'] in self.gaming['SuperBitsString'],
                    'BonusText': valuesDict['BonusText']
                }
            except:
                self.gaming['SuperBits'][valuesDict['Name']] = {
                    'Unlocked': False,
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
        raw_gaming_sprout_list = safe_loads(self.raw_data.get("GamingSprout", []))
        try:
            self.gaming['Imports'] = {
                'Snail': {
                    'SnailRank': raw_gaming_sprout_list[32][1]
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
        self._parse_w5_sailing_boats()
        self._parse_w5_sailing_captains()

    def _parse_w5_sailing_boats(self):
        raw_sailing_boats = safe_loads(safe_loads(self.raw_data.get("Boats", [])))  # Some users have needed to have data converted twice
        for boatIndex, boatDetails in enumerate(raw_sailing_boats):
            try:
                self.sailing['Boats'][boatIndex] = {
                    'Captain': boatDetails[0],
                    'Destination': boatDetails[1],
                    'LootUpgrades': boatDetails[3],
                    'SpeedUpgrades': boatDetails[5],
                    'TotalUpgrades': boatDetails[3] + boatDetails[5]
                }
            except:
                self.sailing['Boats'][boatIndex] = {
                    'Captain': -1,
                    'Destination': -1,
                    'LootUpgrades': 0,
                    'SpeedUpgrades': 0,
                    'TotalUpgrades': 0
                }

    def _parse_w5_sailing_captains(self):
        raw_sailing_captains = safe_loads(safe_loads(self.raw_data.get("Captains", [])))  # Some users have needed to have data converted twice
        for captainIndex, captainDetails in enumerate(raw_sailing_captains):
            try:
                self.sailing['Captains'][captainIndex] = {
                    'Tier': captainDetails[0],
                    'TopBuff': captainBuffs[captainDetails[1]],
                    'BottomBuff': captainBuffs[captainDetails[2]],
                    'Level': captainDetails[3],
                    #'EXP': captainDetails[4],
                    'TopBuffBaseValue': captainDetails[5],
                    'BottomBuffBaseValue': captainDetails[6],
                }
            except:
                self.sailing['Captains'][captainIndex] = {
                    'Tier': 0,
                    'TopBuff': 'None',
                    'BottomBuff': 'None',
                    'Level': 0,
                    #'EXP': 0,
                    'TopBuffBaseValue': 0,
                    'BottomBuffBaseValue': 0,
                }

    def _parse_w5_divinity(self):
        self.divinity = {
            'Divinities': copy.deepcopy(divinity_divinitiesDict),
            'DivinityLinks': {}
        }
        raw_divinity_list = safe_loads(self.raw_data.get("Divinity", []))
        while len(raw_divinity_list) < 40:
            raw_divinity_list.append(0)
        self.divinity['DivinityPoints'] = raw_divinity_list[24]
        if isinstance(self.divinity['DivinityPoints'], str):
            try:
                self.divinity['DivinityPoints'] = int(float(self.divinity['DivinityPoints']))
            except Exception as reason:
                print(f"models._parse_w5_divinity: WARNING Could not convert '{type(self.divinity['DivinityPoints'])}' {self.divinity['DivinityPoints']} to int: {reason}. Defaulting to 0")
                self.divinity['DivinityPoints'] = 0
        self.divinity['GodsUnlocked'] = min(10, raw_divinity_list[25])
        self.divinity['GodRank'] = max(0, raw_divinity_list[25] - 10)
        self.divinity['LowOffering'] = raw_divinity_list[26]
        self.divinity['HighOffering'] = raw_divinity_list[27]
        self.divinity['LowOfferingGoal'] = ""
        self.divinity['HighOfferingGoal'] = ""
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

    def _parse_caverns(self):
        self.caverns = {
            'Villagers': {},
            'Caverns': {},
            'CavernsUnlocked': 0,
            'Schematics': {},
            'TotalSchematics': 0,
            'Majiks': {},
            'TotalMajiks': 0,
            'Measurements': {},
        }
        raw_caverns_list: list[list] = safe_loads(self.raw_data.get('Holes', []))
        while len(raw_caverns_list) < 24:
            raw_caverns_list.append([])
        self._parse_caverns_villagers(raw_caverns_list[1], raw_caverns_list[2], raw_caverns_list[3], raw_caverns_list[23])
        self._parse_caverns_actual_caverns(raw_caverns_list[7])
        self._parse_caverns_majiks(raw_caverns_list[4], raw_caverns_list[5], raw_caverns_list[6])
        self._parse_caverns_schematics(raw_caverns_list[13])
        self._parse_caverns_measurements(raw_caverns_list[22])
        self._parse_caverns_biome1(raw_caverns_list)

        #print([k for k, v in self.caverns['Schematics'].items() if v['Unlocked']])  #Unlocked schematic check
        # for key in self.caverns:
        #     print(f"{key}: {self.caverns[key]}")

    def _parse_caverns_villagers(self, villager_levels, villager_exp, opals_invested, parallel_villagers):
        for villager_index, villager_data in enumerate(caverns_villagers):
            try:
                self.caverns['Villagers'][villager_data['Name']] = {
                    'Unlocked': villager_levels[villager_index] > 0,
                    'UnlockedCavern': villager_data['UnlockedAtCavern'],
                    'Level':    villager_levels[villager_index],
                    'Opals':    opals_invested[villager_index],
                    'Title':    f"{villager_data['Name']}, {villager_data['Role']}",
                    'VillagerNumber': villager_data['VillagerNumber'],
                    'LevelPercent': 100 * (float(villager_exp[villager_index])/getVillagerEXPRequired(villager_index, villager_levels[villager_index])),
                }
                self.gemshop[f"Parallel Villagers {villager_data['Role']}"] = parallel_villagers[villager_index]
            except:
                self.caverns['Villagers'][villager_data['Name']] = {
                    'Unlocked': villager_data['Name'] == 'Polonai',
                    'UnlockedCavern': villager_data['UnlockedAtCavern'],
                    'Level': 0,
                    'Opals': 0,
                    'Title': f"{villager_data['Name']}, {villager_data['Role']}",
                    'VillagerNumber': villager_data['VillagerNumber'],
                    'LevelPercent': 0,
                }
                self.gemshop[f"Parallel Villagers {villager_data['Role']}"] = 0

    def _parse_caverns_actual_caverns(self, opals_per_cavern):
        for cavern_index, cavern_name in caverns_cavern_names.items():
            try:
                self.caverns['Caverns'][cavern_name] = {
                    'Unlocked': self.caverns['Villagers']['Polonai']['Level'] >= cavern_index,
                    'OpalsFound': 0 if cavern_name == 'Camp' else opals_per_cavern[cavern_index-1],
                    'Image': f'cavern-{cavern_index}',
                    'CavernNumber': cavern_index
                }
            except:
                self.caverns['Caverns'][cavern_name] = {
                    'Unlocked': False,
                    'OpalsFound': 0,
                    'Image': f'cavern-{cavern_index}',
                    'CavernNumber': cavern_index
                }

    def _parse_caverns_majiks(self, hole_majiks, village_majiks, idleon_majiks):
        self.caverns['TotalMajiks'] = sum([sum(hole_majiks), sum(village_majiks), sum(idleon_majiks)])
        raw_majiks: dict = {
            'Hole': hole_majiks,
            'Village': village_majiks,
            'IdleOn': idleon_majiks
        }
        for majik_type, majiks in caverns_conjuror_majiks.items():
            for majik_index, majik_data in enumerate(majiks):
                try:
                    self.caverns['Majiks'][majik_data['Name']] = {
                        'MajikType': majik_type,
                        'MajikIndex': majik_index,
                        'Level': raw_majiks[majik_type][majik_index],
                        'MaxLevel': majik_data['MaxLevel'],
                        'Description': majik_data['Description'],
                        'Value': 0  #Calculated later in _calculate_caverns_majiks
                    }
                except:
                    self.caverns['Majiks'][majik_data['Name']] = {
                        'MajikType': majik_type,
                        'MajikIndex': majik_index,
                        'Level': 0,
                        'MaxLevel': majik_data['MaxLevel'],
                        'Description': majik_data['Description'],
                        'Value': 0  # Calculated later in _calculate_caverns_majiks
                    }

    def _parse_caverns_schematics(self, raw_schematics_list):
        try:
            self.caverns['TotalSchematics'] = sum(raw_schematics_list)
        except Exception as e:
            #print(f"Error summing raw_schematics_list: {e}")
            pass
        for schematic_index, schematic_details in enumerate(caverns_engineer_schematics):
            clean_name = schematic_details[0].replace("_", " ")
            resource_type = getCavernResourceImage(schematic_details[2])
            try:
                self.caverns['Schematics'][clean_name] = {
                    'Purchased': raw_schematics_list[schematic_index] > 0,
                    'Image': f'engineer-schematic-{schematic_index}',
                    'Description': schematic_details[5].replace("_", " "),
                    'UnlockOrder': caverns_engineer_schematics_unlock_order.index(schematic_index)+1,
                    'Resource': resource_type
                }
            except Exception as e:
                #print(f"Error processing schematic {clean_name} at index {schematic_index}: {e}")
                self.caverns['Schematics'][clean_name] = {
                    'Purchased': False,
                    'Image': f'engineer-schematic-{schematic_index}',
                    'Description': schematic_details[5].replace("_", " "),
                    'UnlockOrder': caverns_engineer_schematics_unlock_order.index(schematic_index)+1,
                    'Resource': resource_type
                }

    def _parse_caverns_measurements(self, raw_measurements_list):
        for measurement_index, measurement_details in enumerate(caverns_measurer_measurements):
            try:
                self.caverns['Measurements'][measurement_index] = {
                    'Level': raw_measurements_list[measurement_index],
                    'Unit': measurement_details[0],
                    'Description': measurement_details[1],
                    'ScalesWith': measurement_details[2],
                    'Image': f"measurement-{measurement_index}",
                    'Resource': measurement_details[3],
                    'MeasurementNumber': measurement_index+1
                }
            except:
                self.caverns['Measurements'][measurement_index] = {
                    'Level': 0,
                    'Unit': measurement_details[0],
                    'Description': measurement_details[1],
                    'ScalesWith': measurement_details[2],
                    'Image': f"measurement-{measurement_index}",
                    'Resource': measurement_details[3],
                    'MeasurementNumber': measurement_index+1
                }

    def _parse_caverns_biome1(self, raw_caverns_list):
        self._parse_caverns_the_well(raw_caverns_list)
        self._parse_caverns_motherlode(raw_caverns_list)
        self._parse_caverns_the_den(raw_caverns_list)
        self._parse_caverns_bravery_monument(raw_caverns_list)
        self._parse_caverns_the_bell(raw_caverns_list)

    def _parse_caverns_the_well(self, raw_caverns_list):
        try:
            self.caverns['Caverns']['The Well']['BucketTargets'] = [int(entry) for entry in raw_caverns_list[10][:max_buckets]]
        except:
            self.caverns['Caverns']['The Well']['BucketTargets'] = [0]*max_buckets
        try:
            self.caverns['Caverns']['The Well']['SedimentsOwned'] = [int(entry) for entry in raw_caverns_list[9]]
        except:
            #Gravel starts at 0, the rest are Negative
            self.caverns['Caverns']['The Well']['SedimentsOwned'] = [entry*-1 for entry in sediment_bars]
        try:
            self.caverns['Caverns']['The Well']['SedimentLevels'] = raw_caverns_list[8]
        except:
            self.caverns['Caverns']['The Well']['SedimentLevels'] = [0]*max_sediments
        try:
            self.caverns['Caverns']['The Well']['BarExpansion'] = raw_caverns_list[11][10]
        except:
            self.caverns['Caverns']['The Well']['BarExpansion'] = False
        try:
            self.caverns['Caverns']['The Well']['Holes-11-9'] = raw_caverns_list[11][9]
        except:
            self.caverns['Caverns']['The Well']['Holes-11-9'] = 0

    def _parse_caverns_motherlode(self, raw_caverns_list):
        cavern_name = 'Motherlode'
        motherlode_offset = 0
        try:
            self.caverns['Caverns'][cavern_name]['ResourcesCollected'] = raw_caverns_list[11][0 + motherlode_offset]
        except:
            self.caverns['Caverns'][cavern_name]['ResourcesCollected'] = 0
        try:
            self.caverns['Caverns'][cavern_name]['LayersDestroyed'] = raw_caverns_list[11][1 + motherlode_offset]
        except:
            self.caverns['Caverns'][cavern_name]['LayersDestroyed'] = 0

    def _parse_caverns_the_den(self, raw_caverns_list):
        try:
            self.caverns['Caverns']['The Den']['HighScore'] = round(float(raw_caverns_list[11][8]))
        except:
            self.caverns['Caverns']['The Den']['HighScore'] = 0

    def _parse_caverns_bravery_monument(self, raw_caverns_list):
        monument_name = 'Bravery Monument'
        monument_index = 0

        # Layer Data
        try:
            self.caverns['Caverns'][monument_name]['Hours'] = int(raw_caverns_list[14][0 + 2 * monument_index])
        except:
            self.caverns['Caverns'][monument_name]['Hours'] = 0
        try:
            self.caverns['Caverns'][monument_name]['LayersCleared'] = int(raw_caverns_list[14][1 + 2 * monument_index])
        except:
            self.caverns['Caverns'][monument_name]['LayersCleared'] = 0

        # Setup Bonuses
        self.caverns['Caverns'][monument_name]['Bonuses'] = {}
        for bonus_index, bonus_details in monument_bonuses[monument_name].items():
            try:
                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                    'Level': raw_caverns_list[15][bonus_index],
                    'Description': bonus_details['Description'],
                    'ScalingValue': bonus_details['ScalingValue'],
                    'ValueType': bonus_details['ValueType'],
                    'Image': bonus_details['Image'],
                    'Value': 0,  #Calculated later in _calculate_caverns_monuments()
                }
            except:
                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                    'Level': 0,
                    'Description': bonus_details['Description'],
                    'ScalingValue': bonus_details['ScalingValue'],
                    'ValueType': bonus_details['ValueType'],
                    'Image': bonus_details['Image'],
                    'Value': 0,  # Calculated later in _calculate_caverns_monuments()
                }

    def _parse_caverns_the_bell(self, raw_caverns_list):
        cavern_name = 'The Bell'

        #Charge
        try:
            self.caverns['Caverns'][cavern_name]['Charges'] = {
                'Ring': [raw_caverns_list[18][0], raw_caverns_list[18][1], getBellExpRequired(0, raw_caverns_list[18][1])],
                'Ping': [raw_caverns_list[18][2], raw_caverns_list[18][3], getBellExpRequired(1, raw_caverns_list[18][3])],
                'Clean': [raw_caverns_list[18][4], raw_caverns_list[18][5], getBellExpRequired(2, raw_caverns_list[18][5])],
                'Renew': [raw_caverns_list[18][6], raw_caverns_list[18][7], getBellExpRequired(3, raw_caverns_list[18][7])],
            }
        except:
            self.caverns['Caverns'][cavern_name]['Charges'] = {
                'Ring': [0, 0, getBellExpRequired(0, 0)],
                'Ping': [0, 0, getBellExpRequired(1, 0)],
                'Clean': [0, 0, getBellExpRequired(2, 0)],
                'Renew': [0, 0, getBellExpRequired(3, 0)],
            }

        #Ring Bonuses
        self.caverns['Caverns'][cavern_name]['Ring Bonuses'] = {}
        ring_levels = raw_caverns_list[17]
        for ring_index, ring_details in bell_ring_bonuses.items():
            try:
                self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index] = {
                    'Level': int(ring_levels[ring_index]),
                    'Description': ring_details['Description'],
                    'ScalingValue': ring_details['ScalingValue'],
                    'Image': ring_details['Image']
                }
            except:
                self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index] = {
                    'Level': 0,
                    'Description': ring_details['Description'].replace('{', '0.00'),
                    'ScalingValue': ring_details['ScalingValue'],
                    'Image': ring_details['Image']
                }
            self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Value'] = (
                    self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Level']
                    * self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['ScalingValue']
            )
            self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Description'] = (
                self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Description'].replace(
                    '{', f"{self.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Value']:.2f}"
                )
            )

        #Improvements
        self.caverns['Caverns'][cavern_name]['Improvements'] = {}
        improvement_levels = raw_caverns_list[16]
        for improvement_index, improvement_details in bell_clean_improvements.items():
            try:
                self.caverns['Caverns'][cavern_name]['Improvements'][improvement_index] = {
                    'Level': improvement_levels[improvement_index],
                    'Description': improvement_details['Description'],
                    'Image': improvement_details['Image'],
                    'Resource': improvement_details['Resource']
                }
            except:
                self.caverns['Caverns'][cavern_name]['Improvements'][improvement_index] = {
                    'Level': 0,
                    'Description': improvement_details['Description'],
                    'Image': improvement_details['Image'],
                    'Resource': improvement_details['Resource']
                }

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
            'CurrentMastery': safer_get(self.raw_optlacc_dict, 231, 0),
            'MaxMastery': safer_get(self.raw_optlacc_dict, 232, 0),
        }
        raw_ninja_list = safe_loads(self.raw_data.get("Ninja", []))
        self._parse_w6_gemstones(raw_ninja_list)
        self._parse_w6_jade_emporium(raw_ninja_list)
        self._parse_w6_beanstalk(raw_ninja_list)

    def _parse_w6_gemstones(self, raw_ninja_list):
        raw_pristine_charms_list = raw_ninja_list[107] if raw_ninja_list else []
        for pristineCharmIndex, pristineCharmDict in enumerate(pristineCharmsList):
            try:
                self.sneaking["PristineCharms"][pristineCharmDict['Name']] = {
                    'Obtained': bool(raw_pristine_charms_list[pristineCharmIndex]),
                    'Image': pristineCharmDict['Image'],
                    'Bonus': pristineCharmDict['Bonus'],
                }
            except:
                self.sneaking["PristineCharms"][pristineCharmDict['Name']] = {
                    'Obtained': False,
                    'Image': pristineCharmDict['Image'],
                    'Bonus': pristineCharmDict['Bonus'],
                }
        for gemstoneIndex, gemstoneName in enumerate(sneakingGemstonesList):
            self.sneaking["Gemstones"][gemstoneName] = {
                "Level": safer_get(self.raw_optlacc_dict, sneakingGemstonesFirstIndex + gemstoneIndex, 0),
                "BaseValue": 0,
                "BoostedValue": 0.0,
                "Percent": 0,
                "Stat": ''
            }
            try:
                self.sneaking["Gemstones"][gemstoneName]["Stat"] = sneakingGemstonesStatList[gemstoneIndex]
            except:
                continue
        try:
            self.sneaking["Gemstones"]["Moissanite"]["BaseValue"] = getMoissaniteValue(self.sneaking["Gemstones"]["Moissanite"]["Level"])
        except:
            pass  #Already defaulted to 0
        for gemstoneName in sneakingGemstonesList[0:-1]:
            try:
                self.sneaking["Gemstones"][gemstoneName]["BaseValue"] = getGemstoneBaseValue(
                    gemstoneName,
                    self.sneaking["Gemstones"][gemstoneName]["Level"],
                )
                self.sneaking["Gemstones"][gemstoneName]["BoostedValue"] = getGemstoneBoostedValue(
                    self.sneaking["Gemstones"][gemstoneName]["BaseValue"],
                    self.sneaking["Gemstones"]["Moissanite"]["BaseValue"]
                )
            except:
                continue  #Already defaulted to 0
        for gemstoneName in sneakingGemstonesList:
            try:
                self.sneaking["Gemstones"][gemstoneName]["Percent"] = getGemstonePercent(
                    gemstoneName,
                    self.sneaking["Gemstones"][gemstoneName]["BaseValue"]
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
            'MagicBeans': 0,
            'Crops': {},
            'CropCountsPerSeed': {
                'Basic': 0,
                'Earthy': 0,
                'Bulbo': 0,
                'Sushi': 0,
                'Mushie': 0,
                'Glassy': 0,
            },
            "CropsUnlocked": 0,
            "MarketUpgrades": {},
            "CropStacks": {
                "Evolution Gmo": 0,  # 200
                "Speed Gmo": 0,  # 1,000
                "Exp Gmo": 0,  # 2,500
                "Value Gmo": 0,  # 10,000
                "Super Gmo": 0  # 100,000
            },
            'LandRankDatabase': {},
            'Depot': {},
        }

        raw_farmcrop_dict = safe_loads(self.raw_data.get("FarmCrop", {}))
        self._parse_w6_farming_crops(raw_farmcrop_dict)
        self._parse_w6_farming_crop_depot()

        raw_farmupg_list = safe_loads(self.raw_data.get("FarmUpg", []))
        self._parse_w6_farming_markets(raw_farmupg_list)

        raw_farmrank_list = safe_loads(self.raw_data.get("FarmRank", [[0]*36]))
        self._parse_w6_farming_land_ranks(raw_farmrank_list)

        self.farming['Total Plots'] = (
            1
            + self.farming['MarketUpgrades']['Land Plots']['Level']
            + self.gemshop['Plot of Land']
            + min(3, self.merits[5][2]['Level'])
        )

    def _parse_w6_farming_crops(self, rawCrops):
        if isinstance(rawCrops, dict):
            for cropIndexStr, cropAmountOwned in rawCrops.items():
                try:
                    self.farming["CropsUnlocked"] += 1  # Once discovered, crops will always appear in this dict.
                    if int(cropIndexStr) < 21:
                        self.farming['CropCountsPerSeed']['Basic'] += 1
                    elif int(cropIndexStr) < 46:
                        self.farming['CropCountsPerSeed']['Earthy'] += 1
                    elif int(cropIndexStr) < 61:
                        self.farming['CropCountsPerSeed']['Bulbo'] += 1
                    elif int(cropIndexStr) < 84:
                        self.farming['CropCountsPerSeed']['Sushi'] += 1
                    elif int(cropIndexStr) < 107:
                        self.farming['CropCountsPerSeed']['Mushie'] += 1
                    else:
                        self.farming['CropCountsPerSeed']['Glassy'] += 1
                    self.farming['Crops'][int(cropIndexStr)] = float(cropAmountOwned)
                    if float(cropAmountOwned) >= 200:
                        self.farming["CropStacks"]["Evolution Gmo"] += 1
                    if float(cropAmountOwned) >= 1000:
                        self.farming["CropStacks"]["Speed Gmo"] += 1
                    if float(cropAmountOwned) >= 2500:
                        self.farming["CropStacks"]["Exp Gmo"] += 1
                    if float(cropAmountOwned) >= 10000:
                        self.farming["CropStacks"]["Value Gmo"] += 1
                    if float(cropAmountOwned) >= 100000:
                        self.farming["CropStacks"]["Super Gmo"] += 1
                except:
                    continue

    def _parse_w6_farming_crop_depot(self):
        for bonusIndex, bonusDetails in cropDepotDict.items():
            self.farming['Depot'][bonusIndex] = {
                'BonusString': bonusDetails['BonusString'],
                'Image': bonusDetails['Image'],
                'ScalingType': bonusDetails['funcType'],
                'ScalingNumber': bonusDetails['x1'],
                'Unlocked': self.sneaking['JadeEmporium'][bonusDetails['EmporiumUnlockName']]['Obtained'],
                'BaseValue': lavaFunc(
                    bonusDetails['funcType'],
                    self.farming['CropsUnlocked'],
                    bonusDetails['x1'],
                    bonusDetails['x2']
                ),
                'BaseValuePlus1': lavaFunc(
                    bonusDetails['funcType'],
                    min(maxFarmingCrops, self.farming['CropsUnlocked'] + 1),
                    bonusDetails['x1'],
                    bonusDetails['x2']
                ),
                'MaxValue': lavaFunc(
                    bonusDetails['funcType'],
                    maxFarmingCrops,
                    bonusDetails['x1'],
                    bonusDetails['x2']
                ),
                'Value': 0,
                'ValuePlus1': 0,
            }

    def _parse_w6_farming_markets(self, rawMarkets):
        try:
            self.farming['MagicBeans'] = int(float(rawMarkets[1]))
        except:
            pass
        for marketUpgradeIndex, marketUpgrade in enumerate(marketUpgradeDetails):
            try:
                self.farming["MarketUpgrades"][marketUpgrade[0].replace('_', ' ').title()] = {
                    'Level': rawMarkets[marketUpgradeIndex + 2],
                    'Description': marketUpgrade[1].replace('_', ' '),
                    'Value': rawMarkets[marketUpgradeIndex + 2] * float(marketUpgrade[8]),
                    'StackedValue': rawMarkets[marketUpgradeIndex + 2] * float(marketUpgrade[8]),  #Updated later in calculate function
                    'UpgradesAtSameCrop': int(marketUpgrade[2]),
                    'CropTypeValue': float(marketUpgrade[3]),
                    'BaseCost': int(marketUpgrade[4]),
                    'CostIncrement': float(marketUpgrade[5]),
                    'UnlockRequirement': int(marketUpgrade[6]),
                    'MaxLevel': int(marketUpgrade[7]),
                    'BonusPerLevel': float(marketUpgrade[8]),
                    'MarketType': 'Day' if marketUpgradeIndex < 8 else 'Night'
                }
            except:
                self.farming["MarketUpgrades"][marketUpgrade[0].replace('_', ' ').title()] = {
                    'Level': 0,
                    'Description': marketUpgrade[1].replace('_', ' '),
                    'Value': 0,
                    'StackedValue': 0,  # Updated later in calculate function
                    'UpgradesAtSameCrop': marketUpgrade[2],
                    'CropTypeValue': marketUpgrade[3],
                    'BaseCost': marketUpgrade[4],
                    'CostIncrement': marketUpgrade[5],
                    'UnlockRequirement': marketUpgrade[6],
                    'MaxLevel': marketUpgrade[7],
                    'BonusPerLevel': marketUpgrade[8],
                    'MarketType': 'Day' if marketUpgradeIndex < 8 else 'Night'
                }

    def _parse_w6_farming_land_ranks(self, rawRanks):
        try:
            self.farming['LandRankPlotRanks'] = rawRanks[0]
            self.farming['LandRankTotalRanks'] = sum(rawRanks[0])
            self.farming['LandRankMinPlot'] = min([v for v in rawRanks[0] if v > 0], default=0)
            self.farming['LandRankMaxPlot'] = max(rawRanks[0], default=0)
        except:
            self.farming['LandRankPlotRanks'] = [0]*36
            self.farming['LandRankTotalRanks'] = 0
            self.farming['LandRankMinPlot'] = 0
            self.farming['LandRankMaxPlot'] = 0
        for upgradeIndex, upgradeValuesDict in landrankDict.items():
            try:
                self.farming['LandRankDatabase'][upgradeValuesDict['Name']] = {
                    'Level': rawRanks[2][upgradeIndex],
                    'BaseValue': upgradeValuesDict['Value'],
                    'Value': (
                        (1.7 * upgradeValuesDict['Value'] * rawRanks[2][upgradeIndex]) / (rawRanks[2][upgradeIndex] + 80)
                        if upgradeIndex not in [4, 9, 14, 19]
                        else upgradeValuesDict['Value'] * rawRanks[2][upgradeIndex]
                    )
                }
            except:
                self.farming['LandRankDatabase'][upgradeValuesDict['Name']] = {
                    'Level': 0,
                    'BaseValue': upgradeValuesDict['Value'],
                    'Value': 0
                }

    def _parse_w6_summoning(self):
        self.summoning = {}
        raw_summoning_list = safe_loads(self.raw_data.get('Summon', []))

        # raw_summoning_list[0] = Upgrades
        try:
            self.summoning["Upgrades"] = raw_summoning_list[0]
        except:
            self.summoning["Upgrades"] = [0] * 69  # As of 2.09 Red/Cyan, there are exactly 69 upgrades #TODO: Replace with a value in consts

        # raw_summoning_list[1] = List of codified names of enemies from battles won
        self.summoning["Battles"] = {}
        self.summoning["BattleDetails"] = {}
        for color in summoningDict:
            self.summoning["BattleDetails"][color] = {}
        try:
            self._parse_w6_summoning_battles(raw_summoning_list[1])
        except:
            self._parse_w6_summoning_battles([])

        # raw_summoning_list[2] looks to be essence owned
        # raw_summoning_list[3] I have no idea what this is

        # raw_summoning_list[4] = list[int] familiars in the Sanctuary, starting with Slime in [0], Vrumbi in [1], etc.
        self.summoning['SanctuaryTotal'] = 0
        try:
            self._parse_w6_summoning_sanctuary(raw_summoning_list[4])
        except:
            self._parse_w6_summoning_sanctuary([])

        #Used later to create a list of Advices for Winner Bonuses. Can be added directly into an AdviceGroup as the advices attribute
        self.summoning['WinnerBonusesAdvice'] = []

    def _parse_w6_summoning_battles(self, rawBattles):
        try:
            self.summoning['Battles']['Total'] = len(rawBattles)
        except:
            self.summoning['Battles']['Total'] = 0

        if self.summoning['Battles']['Total'] >= summoningBattleCountsDict["All"]:
            self.summoning["Battles"] = summoningBattleCountsDict
            self.summoning['AllBattlesWon'] = True
        else:
            self.summoning['AllBattlesWon'] = False
            for colorName, colorDict in summoningDict.items():
                self.summoning["Battles"][colorName] = 0
                for battleIndex, battleValuesDict in colorDict.items():
                    if battleIndex + 1 >= self.summoning["Battles"][colorName] and battleValuesDict['EnemyID'] in rawBattles:
                        self.summoning["Battles"][colorName] = battleIndex + 1

        for colorName, colorDict in summoningDict.items():
            for battleIndex, battleValuesDict in colorDict.items():
                self.summoning["BattleDetails"][colorName][battleIndex + 1] = {
                    'Defeated': battleValuesDict['EnemyID'] in rawBattles,
                    'Image': battleValuesDict['Image'],
                    'RewardType': battleValuesDict['RewardID'],
                    'RewardQTY': battleValuesDict['RewardQTY'],
                    'RewardBaseValue': battleValuesDict['RewardQTY'] * 3.5,
                }

    def _parse_w6_summoning_sanctuary(self, rawSanctuary):
        if rawSanctuary:
            try:
                # [2,3,2,1,1,0,0,0,0,0,0,0,0,0]
                self.summoning['SanctuaryTotal'] = int(rawSanctuary[0])  # Gray Slimes
                self.summoning['SanctuaryTotal'] += 3 * int(rawSanctuary[1])  # Vrumbi
                self.summoning['SanctuaryTotal'] += 12 * int(rawSanctuary[2])  # Bloomie
                self.summoning['SanctuaryTotal'] += 60 * int(rawSanctuary[3])  # Tonka
                self.summoning['SanctuaryTotal'] += 360 * int(rawSanctuary[4])  # Regalis
                # self.summoning['SanctuaryTotal'] += 2520 * int(raw_summoning_list[4][5])  #Sparkie
            except:
                pass

    def _calculate_wave_1(self):
        self._calculate_general()
        self._calculate_w1()
        self._calculate_w2()
        self._calculate_w3()
        self._calculate_w4()
        self._calculate_w5()
        self._calculate_caverns()
        self._calculate_w6()

    def _calculate_general(self):
        self._calculate_general_alerts()
        self._calculate_general_item_filter()
        self.highestWorldReached = self._calculate_general_highest_world_reached()
        #print(f"session_data.account.highestWorldReached = {self.highestWorldReached}")

    def _calculate_general_alerts(self):
        if self.stored_assets.get("Trophy2").amount >= 75 and self.equinox_dreams[17]:
            self.alerts_AdviceDict['General'].append(Advice(
                label=f"You have {self.stored_assets.get('Trophy2').amount}/75 Lucky Lads to craft a Luckier Lad!",
                picture_class="luckier-lad"
            ))

    def _calculate_general_item_filter(self):
        raw_fishing_toolkit_lures = safe_loads(self.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[0]
        raw_fishing_toolkit_lines = safe_loads(self.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[1]
        for filtered_codeName in self.item_filter:
            filtered_displayName = getItemDisplayName(filtered_codeName)
            if (
                filtered_codeName == 'Trophy2'  #Lucky Lad
                and 'Trophy20' not in self.registered_slab  #Luckier Lad
                and self.stored_assets.get("Trophy2").amount < 75
            ):
                self.alerts_AdviceDict['General'].append(Advice(
                    label=f"Lucky filtered before 75 for Luckier Lad",
                    picture_class="lucky-lad",
                    resource="luckier-lad"
                ))
            elif filtered_displayName in filter_recipes:
                for itemName in filter_recipes[filtered_displayName]:
                    if getItemCodeName(itemName) not in self.registered_slab:
                        self.alerts_AdviceDict['General'].append(Advice(
                            label=f"{filtered_displayName} filtered, {itemName} not in Slab",
                            picture_class=filtered_displayName,
                            resource=itemName
                        ))
            elif filtered_displayName in filter_never and self.autoloot:
                self.alerts_AdviceDict['General'].append(Advice(
                    label=f"Why did you filter {filtered_displayName}???",
                    picture_class=filtered_displayName,
                ))
            elif filtered_codeName not in self.registered_slab:
                self.alerts_AdviceDict['General'].append(Advice(
                    label=f"{filtered_displayName} filtered, not in Slab",
                    picture_class=filtered_displayName,
                ))
            elif filtered_displayName in fishingToolkitDict['Lures']:
                if fishingToolkitDict['Lures'].index(filtered_displayName) not in raw_fishing_toolkit_lures.values():
                    self.alerts_AdviceDict['General'].append(Advice(
                        label=f"{filtered_displayName} filtered, not in Fishing Toolkit",
                        picture_class=filtered_displayName,
                    ))
            elif filtered_displayName in fishingToolkitDict['Lines']:
                if fishingToolkitDict['Lines'].index(filtered_displayName) not in raw_fishing_toolkit_lines.values():
                    self.alerts_AdviceDict['General'].append(Advice(
                        label=f"{filtered_displayName} filtered, not in Fishing Toolkit",
                        picture_class=filtered_displayName,
                    ))

    def _calculate_general_highest_world_reached(self):
        if (
            safer_get(self.raw_optlacc_dict, 194, 0) > 0
            or self.achievements['Valley Visitor']['Complete']
            or self.enemy_worlds[6].maps_dict[251].kill_count > 0
        ):
            return 6
        elif (
            self.achievements['The Plateauourist']['Complete']
            or self.enemy_worlds[5].maps_dict[201].kill_count > 0
        ):
            return 5
        elif (
            self.achievements['Milky Wayfarer']['Complete']
            or self.enemy_worlds[4].maps_dict[151].kill_count > 0
        ):
            return 4
        elif (
            self.achievements['Snowy Wonderland']['Complete']
            or self.enemy_worlds[3].maps_dict[101].kill_count > 0
        ):
            return 3
        elif (
            self.achievements['Down by the Desert']['Complete']
            or self.enemy_worlds[2].maps_dict[51].kill_count > 0
        ):
            return 2
        else:
            return 1

    def _calculate_w1(self):
        self._calculate_w1_starsigns()
        self._calculate_w1_statues()

    def _calculate_w1_starsigns(self):
        self.star_sign_extras['SeraphMulti'] = min(3, 1.1 ** ceil((max(self.all_skills['Summoning'], default=0) + 1) / 20))
        self.star_sign_extras['SeraphGoal'] = min(220, ceilUpToBase(max(self.all_skills['Summoning'], default=0), 20))
        min_level_stacks = ceil((min(self.all_skills['Summoning'], default=0) + 1) / 20)
        max_level_stacks = ceil((max(self.all_skills['Summoning'], default=0) + 1) / 20)
        inequality_notice = ' (Note: Some characters lower leveled)' if min_level_stacks != max_level_stacks else ''
        if bool(self.star_signs.get("Seraph Cosmos", {}).get('Unlocked', False)):
            self.star_sign_extras['SeraphEval'] = f"Multis signs by {self.star_sign_extras['SeraphMulti']:.2f}x."
        else:
            self.star_sign_extras['SeraphEval'] = f"Locked. Would increase other signs by {self.star_sign_extras['SeraphMulti']:.2f}x if unlocked.{inequality_notice}"
            self.star_sign_extras['SeraphMulti'] = 1
        if self.star_sign_extras['SeraphGoal'] < 240:
            self.star_sign_extras['SeraphEval'] += f" Increases every 20 Summoning levels.{inequality_notice}"
        self.star_sign_extras['SeraphAdvice'] = Advice(
            label=f"{{{{ Star Sign|#star-signs }}}}: Seraph Cosmos: {self.star_sign_extras['SeraphEval']}",
            picture_class="seraph-cosmos",
            progression=max(self.all_skills['Summoning'], default=0),
            goal=self.star_sign_extras['SeraphGoal'])

        if self.labChips.get('Silkrode Nanochip', 0) > 0:
            self.star_sign_extras['DoublerOwned'] = True
            self.star_sign_extras['SilkrodeNanoEval'] = f"{self.labChips.get('Silkrode Nanochip', 0)} owned. Doubles star signs when equipped."
            self.star_sign_extras['SilkrodeNanoMulti'] = 2
        else:
            self.star_sign_extras['DoublerOwned'] = False
            self.star_sign_extras['SilkrodeNanoEval'] = "None Owned. Would double other signs if equipped."
            self.star_sign_extras['SilkrodeNanoMulti'] = 1
        self.star_sign_extras['SilkrodeNanoAdvice'] = Advice(
            label=f"Lab Chip: Silkrode Nanochip: {self.star_sign_extras['SilkrodeNanoEval']}",
            picture_class="silkrode-nanochip",
            progression=1 if self.labChips.get('Silkrode Nanochip', 0) > 0 else 0,
            goal=1
        )

    def _calculate_w1_statues(self):
        voodooStatuficationMulti = []
        for char in self.safe_characters:
            if char.class_name == "Voidwalker":
                voodooStatuficationMulti.append(
                    lavaFunc(
                        'decay',
                        char.max_talents_over_books + char.max_talents.get("56", 0),
                        200,
                        200
                    )
                )
        voodooStatuficationMulti = 1 + max(voodooStatuficationMulti, default=0)

        onyxMulti = 2 + 0.3 * self.sailing['Artifacts'].get('The Onyx Lantern', {}).get('Level', 0)

        for statueName, statueDetails in self.statues.items():
            if statueDetails['Type'] == "Onyx":
                self.statues[statueName]["Value"] *= onyxMulti
            self.statues[statueName]["Value"] *= voodooStatuficationMulti

    def _calculate_w2(self):
        self.vialMasteryMulti = 1 + (self.maxed_vials * .02) if self.rift['VialMastery'] else 1
        self._calculate_w2_sigils()
        self._calculate_w2_cauldrons()
        self._calculate_w2_ballot()
        self._calculate_w2_islands_trash()
        self._calculate_w2_killroy()

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

    def _calculate_w2_ballot(self):
        equinoxMulti = ValueToMulti(self.equinox_bonuses['Voter Rights']['CurrentLevel'])
        for buffIndex, buffValuesDict in self.ballot['Buffs'].items():
            self.ballot['Buffs'][buffIndex]['Value'] *= equinoxMulti
            # Check for + or +x% replacements
            if "{" in buffValuesDict['Description']:
                self.ballot['Buffs'][buffIndex]['Description'] = buffValuesDict['Description'].replace("{", f"{self.ballot['Buffs'][buffIndex]['Value']:.3f}")
            # Check for multi replacements
            if "}" in buffValuesDict['Description']:
                self.ballot['Buffs'][buffIndex]['Description'] = buffValuesDict['Description'].replace("}", f"{ValueToMulti(self.ballot['Buffs'][buffIndex]['Value']):.3f}")

    def _calculate_w2_islands_trash(self):
        for item in islands_trash_shop_costs:
            self.islands['Trash Island'][item] = {'Cost': islands_trash_shop_costs[item]}
        #Onetime purchases
        self.islands['Trash Island']['Skelefish Stamp']['Unlocked'] = self.stamps['Skelefish Stamp']['Delivered'] or self.stored_assets.get('StampB47').amount > 0
        self.islands['Trash Island']['Amplestample Stamp']['Unlocked'] = self.stamps['Amplestample Stamp']['Delivered'] or self.stored_assets.get('StampB32').amount > 0
        self.islands['Trash Island']['Golden Sixes Stamp']['Unlocked'] = self.stamps['Golden Sixes Stamp']['Delivered'] or self.stored_assets.get('StampA38').amount > 0
        self.islands['Trash Island']['Stat Wallstreet Stamp']['Unlocked'] = self.stamps['Stat Wallstreet Stamp']['Delivered'] or self.stored_assets.get('StampA39').amount > 0
        self.islands['Trash Island']['Unlock New Bribe Set']['Unlocked'] = self.bribes['Trash Island']['Random Garbage'] >= 0

        #Repeated purchases
        self.islands['Trash Island']['Garbage Purchases'] = safer_get(self.raw_optlacc_dict, 163, 0)
        self.islands['Trash Island']['Bottle Purchases'] = safer_get(self.raw_optlacc_dict, 164, 0)

    def _calculate_w2_killroy(self):
        for upgradeName, upgradeDict in killroy_dict.items():
            if not self.killroy[upgradeName]['Available']:
                self.killroy[upgradeName]['Available'] = (
                    safer_get(self.raw_optlacc_dict, 112, 0) >= upgradeDict['Required Fights']
                    or self.killroy[upgradeName]['Upgrades'] > 0
                ) and self.equinox_bonuses['Shades of K']['CurrentLevel'] >= upgradeDict['Required Equinox']

    def _calculate_w3(self):
        self._calculate_w3_building_max_levels()
        self._calculate_w3_collider_base_costs()
        self._calculate_w3_collider_cost_reduction()
        self._calculate_w3_shrine_values()
        self._calculate_w3_shrine_advices()

    def _calculate_w3_building_max_levels(self):
        # Placed towers here since it's used for both Construction mastery and atom levels
        towers = [towerName for towerName, towerValuesDict in self.construction_buildings.items() if towerValuesDict['Type'] == 'Tower']
        if self.rift['SkillMastery']:
            totalLevel = sum(self.all_skills['Construction'])
            if totalLevel >= 500:
                self.construction_buildings["Trapper Drone"]['MaxLevel'] += 35

            if totalLevel >= 1000:
                self.construction_buildings["Talent Book Library"]['MaxLevel'] += 100

            if totalLevel >= 1500:
                shrines = [shrineName for shrineName, shrineValuesDict in self.construction_buildings.items() if shrineValuesDict['Type'] == 'Shrine']
                for shrineName in shrines:
                    try:
                        self.construction_buildings[shrineName]['MaxLevel'] += 30
                    except:
                        continue

            if totalLevel >= 2500:
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
        self.atom_collider['CostReductionMax'] = ValueToMulti(
            7 * 4  #Max merit
            + 1 * 20  #Max Atom Collider building
            + 1 * 30  #Max Neon
            + 10  #Superbit
            + 14  #Atom Split bubble
            + 20  #Stamp
        )
        self.atom_collider['CostReductionRaw'] = ValueToMulti(
            7 * self.merits[4][6]['Level']
            + (self.construction_buildings['Atom Collider']['Level'] / 10)
            + 1 * self.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']
            + 10 * self.gaming['SuperBits']['Atom Redux']['Unlocked']
            + self.alchemy_bubbles['Atom Split']['BaseValue']
            + self.stamps['Atomic Stamp']['Value']
        )
        self.atom_collider['CostReductionMulti'] = 1 / self.atom_collider['CostReductionRaw']
        self.atom_collider['CostReductionMulti1Higher'] = 1 / (self.atom_collider['CostReductionRaw'] + 0.01)
        self.atom_collider['CostDiscount'] = (1 - (1 / self.atom_collider['CostReductionRaw'])) * 100
        self.atom_collider['CostDiscountMax'] = (1 - (1 / self.atom_collider['CostReductionMax'])) * 100

        for atomName, atomValuesDict in self.atom_collider['Atoms'].items():
            # Calculate base cost to upgrade to next level, if not max level
            if atomValuesDict['Level'] < atomValuesDict['MaxLevel']:
                self.atom_collider['Atoms'][atomName]['DiscountedCostToUpgrade'] = (self.atom_collider['Atoms'][atomName]['BaseCostToUpgrade']
                                                                                    * self.atom_collider['CostReductionMulti'])
                self.atom_collider['Atoms'][atomName]['DiscountedCostToMax'] = (self.atom_collider['Atoms'][atomName]['BaseCostToMax']
                                                                                * self.atom_collider['CostReductionMulti'])

    def _calculate_w3_shrine_values(self):
        cchizoar_multi = ValueToMulti(5 * (1 + next(c.getStars() for c in self.cards if c.name == 'Chaotic Chizoar')))
        for shrine in self.shrines:
            self.shrines[shrine]['Value'] *= cchizoar_multi

    def _calculate_w3_shrine_advices(self):
        self.shrine_advices = {}
        for shrine_name in self.shrines:
            self.shrine_advices[shrine_name] = Advice(
                label=f"Level {self.shrines[shrine_name]['Level']} {shrine_name}:"
                      f" +{self.shrines[shrine_name]['Value']:.0f}%"
                      f"<br>{arbitrary_shrine_note}",
                picture_class=self.shrines[shrine_name]['Image'],
                progression=self.shrines[shrine_name]['Level'],
                goal=arbitrary_shrine_goal
            )
        cchizoar_multi = 1 + (5 * (1 + next(c.getStars() for c in self.cards if c.name == 'Chaotic Chizoar')) / 100)
        self.shrine_advices['Chaotic Chizoar Card'] = Advice(
            label=f"Chaotic Chizoar card to increase Shrine ({cchizoar_multi}x multi already included)",
            picture_class="chaotic-chizoar-card",
            progression=1 + next(c.getStars() for c in self.cards if c.name == "Chaotic Chizoar"),
            goal=6
        )

    def _calculate_w4(self):
        self._calculate_w4_cooking_max_plate_levels()
        self._calculate_w4_jewel_multi()
        self._calculate_w4_meal_multi()
        self._calculate_w4_lab_bonuses()

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

    def _calculate_w4_jewel_multi(self):
        jewelMulti = 1
        if self.labBonuses["Spelunker Obol"]["Enabled"]:
            jewelMulti = self.labBonuses["Spelunker Obol"]["Value"]
            if self.labJewels["Pure Opal Navette"]["Enabled"]:  # Nested since jewel does nothing without spelunker
                self.labBonuses["Spelunker Obol"]["Value"] += self.labJewels["Pure Opal Navette"]["BaseValue"] / 100
                jewelMulti += self.labJewels["Pure Opal Navette"]["BaseValue"] / 100  # The displayed value does nothing since the effect is used before spelunker obol is accounted for
        for jewel in self.labJewels:
            self.labJewels[jewel]["Value"] *= jewelMulti if jewel != 'Pure Opal Navette' else 1

    def _calculate_w4_meal_multi(self):
        mealMulti = 1
        if self.labJewels["Black Diamond Rhinestone"]["Enabled"]:
            mealMulti += self.labJewels["Black Diamond Rhinestone"]["Value"]/100

        mealMulti += self.breeding['Total Shiny Levels']['Bonuses from All Meals']/100

        for meal in self.meals:
            self.meals[meal]["Value"] = float(self.meals[meal]["Value"]) * mealMulti

    def _calculate_w4_lab_bonuses(self):
        self.labBonuses['No Bubble Left Behind']['Value'] = 3

        self.labBonuses['No Bubble Left Behind']['Value'] += 1 * self.labJewels['Pyrite Rhinestone']['Enabled']  #Up to +1
        self.labBonuses['No Bubble Left Behind']['Value'] += 1 * self.sailing['Artifacts']['Amberite']['Level']  #Up to +4 as of 2.11
        self.labBonuses['No Bubble Left Behind']['Value'] += 1 * self.gaming['SuperBits']['Moar Bubbles']['Unlocked']  #20% chance at +1
        self.labBonuses['No Bubble Left Behind']['Value'] += 1 * self.gaming['SuperBits']['Even Moar Bubbles']['Unlocked']  #30% chance at +1
        self.labBonuses['No Bubble Left Behind']['Value'] += 1 * self.merits[3][6]['Level']  #Up to 3
        #Grand total: 3 + 1 + 4 + 1 + 1 + 3 = 13 possible. 11 guaranteed, 2 are chances

        #Reduce this down to 0 if the lab bonus isn't enabled
        self.labBonuses['No Bubble Left Behind']['Value'] *= self.labBonuses['No Bubble Left Behind']['Enabled']
        #Now for the bullshit: Lava has a hidden cap of 10 bubbles
        self.labBonuses['No Bubble Left Behind']['Value'] = min(nblbMaxBubbleCount, self.labBonuses['No Bubble Left Behind']['Value'])

    def _calculate_w5(self):
        self._calculate_w5_divinity_offering_costs()

    def _calculate_w5_divinity_offering_costs(self):
        self.divinity['LowOfferingGoal'] = self._divinityUpgradeCost(self.divinity['LowOffering'], self.divinity['GodsUnlocked'] + self.divinity['GodRank'])
        self.divinity['HighOfferingGoal'] = self._divinityUpgradeCost(self.divinity['HighOffering'], self.divinity['GodsUnlocked'] + self.divinity['GodRank'])

    def _divinityUpgradeCost(self, offeringIndex, unlockedDivinity):
        cost = (20 * pow(unlockedDivinity + 1.3, 2.3) * pow(2.2, unlockedDivinity) + 60) * divinity_offeringsDict.get(offeringIndex, {}).get("Chance", 1) / 100
        if unlockedDivinity >= 3:
            cost = cost * pow(min(1.8, max(1, 1 + self.raw_serverVars_dict.get("DivCostAfter3", divinity_DivCostAfter3) / 100)), unlockedDivinity - 2)
        return ceil(cost)

    def _calculate_caverns(self):
        self._calculate_caverns_majiks()
        self._calculate_caverns_measurements()
        self._calculate_caverns_the_well()
        self._calculate_caverns_monuments()
        self._calculate_caverns_the_bell()

    def _calculate_caverns_majiks(self):
        for majik_type, majiks in caverns_conjuror_majiks.items():
            for majik_index, majik_data in enumerate(majiks):
                if majik_data['Scaling'] == 'add':
                    try:
                        self.caverns['Majiks'][majik_data['Name']]['Value'] = (
                            self.caverns['Majiks'][majik_data['Name']]['Level'] * majik_data['BonusPerLevel']
                        )
                        self.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (
                           majik_data['MaxLevel'] * majik_data['BonusPerLevel']
                        )
                    except Exception as e:
                        print(f"Caverns Majik value calc error for level {self.caverns['Majiks'][majik_data['Name']]['Level']} {majik_data['Name']}: {e}")
                elif majik_data['Scaling'] == 'value':
                    try:
                        self.caverns['Majiks'][majik_data['Name']]['Value'] = (ValueToMulti(
                            self.caverns['Majiks'][majik_data['Name']]['Level'] * majik_data['BonusPerLevel']
                        ))
                        self.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (ValueToMulti(
                            majik_data['MaxLevel'] * majik_data['BonusPerLevel']
                        ))
                    except:
                        print(f"Caverns Majik value calc error for level {self.caverns['Majiks'][majik_data['Name']]['Level']} {majik_data['Name']}: {e}")
                elif majik_data['Scaling'] == 'multi':
                    try:
                        self.caverns['Majiks'][majik_data['Name']]['Value'] = (
                            # BonusPerLevel to the power of Level
                            majik_data['BonusPerLevel'] ** self.caverns['Majiks'][majik_data['Name']]['Level']
                        )
                        self.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (
                            # BonusPerLevel to the power of Level
                            majik_data['BonusPerLevel'] ** majik_data['MaxLevel']
                        )
                    except Exception as e:
                        print(f"Caverns Majik value calc error for level {self.caverns['Majiks'][majik_data['Name']]['Level']} {majik_data['Name']}: {e}")
                self.caverns['Majiks'][majik_data['Name']]['Description'] = (
                    f"{self.caverns['Majiks'][majik_data['Name']]['Value']}/{self.caverns['Majiks'][majik_data['Name']]['MaxValue']}"
                    f"{self.caverns['Majiks'][majik_data['Name']]['Description']}"
                )
                #print(f"{majik_data['Name']} value set to {self.caverns['Majiks'][majik_data['Name']]['Value']}")

    def _calculate_caverns_measurements(self):
        total_skill_levels = 0
        for skill, skill_levels in self.all_skills.items():
            total_skill_levels += sum(skill_levels) if skill != 'Combat' else 0
        fake_multi = total_skill_levels / 5000 + max(0, (total_skill_levels - 18000) / 1500)
        if 5 > fake_multi:
            real_multi = 1 + (18 * fake_multi / 100)
        else:
            real_multi = 1 + (18 * fake_multi + 8 * (fake_multi - 5)) / 100
        self.caverns['Measurements'][1]['Value'] = (
            2 * self.caverns['Measurements'][1]['Level']
            * self.caverns['Majiks']['Lengthmeister']['Value']
            * real_multi
        )

    def _calculate_caverns_the_well(self):
        self.caverns['Caverns']['The Well']['BucketsUnlocked'] = 1 + sum(
            [
                1 for schematic_name in schematics_unlocking_buckets if self.caverns['Schematics'][schematic_name]['Purchased']
            ]
        )
        self.caverns['Caverns']['The Well']['Buckets'] = safe_loads(self.raw_data.get('Holes', {}))

    def _calculate_caverns_monuments(self):
        cosmos_multi = max(1, self.caverns['Majiks']['Monumental Vibes']['Value'])
        for monument_index, monument_name in enumerate(monument_names):
            if monument_index < released_monuments:
                # The 9th bonus multiplies other bonuses, but not itself. Must be calculated first.
                ninth = self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]
                ninth_multi = (
                    max(1,
                        0.1 * ceil(
                            ninth['Level'] / (250 + ninth['Level'])
                            * 10
                            * cosmos_multi
                        )
                    )
                )
                try:
                    self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Value'] = ninth_multi
                    self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'] = (
                        self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'].replace(
                            '}', f"{self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Value']:,.3f}")
                    )
                except:
                    self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Value'] = 1
                    self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'] = (
                        self.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'].replace('}', '1')
                    )
                for bonus_index, bonus_details in monument_bonuses[monument_name].items():
                    if bonus_index % 10 != 9:
                        if bonus_details['ScalingValue'] < 30:
                            result = (
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']
                                * self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['ScalingValue']
                                * cosmos_multi
                                * ninth_multi
                            )
                        else:
                            result = (
                                0.1 * ceil(
                                    ninth['Level'] / (250 + ninth['Level'])
                                    * 10
                                    * cosmos_multi
                                    * ninth_multi
                                )
                            )
                        if bonus_details['ValueType'] == 'Percent':
                            try:
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = result
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                    self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace(
                                        '{', f"{self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value']:,.2f}")
                                )
                            except:
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = 0
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                    self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace('{', '0')
                                )
                        elif bonus_details['ValueType'] == 'Multi':
                            try:
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = ValueToMulti(result)
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                    self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace(
                                        '}', f"{self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value']:,.3f}")
                                )
                            except:
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = 1
                                self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                    self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace('}', '1')
                                )
                    #print(f"{monument_name} Bonus {bonus_index}: Level {self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']} = {self.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description']}")
        self._calculate_caverns_monuments_bravery()

    def _calculate_caverns_monuments_bravery(self):
        monument_name = 'Bravery Monument'
        self.caverns['Caverns'][monument_name]['Sword Count'] = (
            min(9, 3  # Starting amount
                + (2 * (self.caverns['Caverns'][monument_name]['Hours'] >= 80))
                + (1 * (self.caverns['Caverns'][monument_name]['Hours'] >= 750))
                + (1 * (self.caverns['Caverns'][monument_name]['Hours'] >= 5000))
                + (1 * (self.caverns['Caverns'][monument_name]['Hours'] >= 24000))
            )
        )
        self.caverns['Caverns'][monument_name]['Max Swords'] = (
                min(9, 3 + 2 + 1 + 1 + 1)
        )
        self.caverns['Caverns'][monument_name]['Sword Min'] = (
            3
            + (1 * floor(self.caverns['Caverns'][monument_name]['Hours'] / 6) * self.caverns['Schematics']['The Story Changes Over Time...']['Purchased'])
        )
        self.caverns['Caverns'][monument_name]['Sword Max'] = (
            (25 + (10 * floor(self.caverns['Caverns'][monument_name]['Hours'] / 6)
                   * self.caverns['Schematics']['The Story Changes Over Time...']['Purchased']))
            * ValueToMulti(self.caverns['Measurements'][1]['Value'])
        )
        self.caverns['Caverns'][monument_name]['Rethrows'] = (
            0
            + (5 * (self.caverns['Caverns'][monument_name]['Hours'] >= 300))
            + (10 * (self.caverns['Caverns'][monument_name]['Hours'] >= 10000))
        )
        self.caverns['Caverns'][monument_name]['Max Rethrows'] = (
            5 + 10
        )
        self.caverns['Caverns'][monument_name]['Retellings'] = (
            1 * (self.caverns['Caverns'][monument_name]['Hours'] >= 2000)
        )
        self.caverns['Caverns'][monument_name]['Max Retellings'] = (
            1
        )

    def _calculate_caverns_the_bell(self):
        cavern_name = 'The Bell'
        self.caverns['Caverns'][cavern_name]['Total Improvements'] = sum(
            [ci_details['Level'] for ci_details in self.caverns['Caverns'][cavern_name]['Improvements'].values()]
        )
        self.caverns['Caverns'][cavern_name]['Stack Size'] = 25
        self.caverns['Caverns'][cavern_name]['Total Stacks'] = (
                self.caverns['Caverns'][cavern_name]['Total Improvements'] // self.caverns['Caverns'][cavern_name]['Stack Size']
        )
        for ci_index, ci_details in self.caverns['Caverns'][cavern_name]['Improvements'].items():
            try:
                self.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Value'] = getBellImprovementBonus(
                    ci_index,
                    ci_details['Level'],
                    self.caverns['Caverns'][cavern_name]['Total Stacks'],
                    self.caverns['Schematics']["Improvement Stackin'"]['Purchased']
                )
            except:
                self.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Value'] = 0
            self.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Description'] = (
                self.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Description'].replace(
                    '{', f"{self.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Value']:,.0f}"
                )
            )

    def _calculate_w6(self):
        self._calculate_w6_summoning_winner_bonuses()
        self._calculate_w6_farming()

    def _calculate_w6_summoning_winner_bonuses(self):
        mga = 1.3
        player_mga = 1.3 if self.sneaking['PristineCharms']['Crystal Comb']['Obtained'] else 1
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"{{{{ Pristine Charm|#sneaking }}}}: Crystal Comb: "
                  f"{player_mga}/1.3x",
            picture_class=self.sneaking['PristineCharms']['Crystal Comb']['Image'],
            progression=int(self.sneaking['PristineCharms']['Crystal Comb']['Obtained']),
            goal=1
        ))

        if not self.sneaking['JadeEmporium']['Brighter Lighthouse Bulb']['Obtained']:
            winzLanternPostString = ". Unlocked from {{ Jade Emporium|#sneaking }}"
        else:
            winzLanternPostString = ""

        mgb = ValueToMulti(
            (25 * numberOfArtifactTiers)
            + self.merits[5][4]['MaxLevel']
            + 1  #int(self.achievements['Spectre Stars'])
            + 1  #int(self.achievements['Regalis My Beloved'])
        )
        player_mgb = ValueToMulti(
            (25 * self.sailing['Artifacts']['The Winz Lantern']['Level'])
            + self.merits[5][4]['Level']
            + int(self.achievements['Spectre Stars']['Complete'])
            + int(self.achievements['Regalis My Beloved']['Complete'])
        )

        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"{{{{ Artifact|#sailing }}}}: The Winz Lantern: "
                  f"{1 + (.25 * self.sailing['Artifacts']['The Winz Lantern']['Level'])}/2x{winzLanternPostString}",
            picture_class="the-winz-lantern",
            progression=self.sailing['Artifacts']['The Winz Lantern']['Level'],
            goal=4
        ))
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"W6 Larger Winner bonuses merit: "
                  f"+{self.merits[5][4]['Level']}/{self.merits[5][4]['MaxLevel']}%",
            picture_class="merit-5-4",
            progression=self.merits[5][4]["Level"],
            goal=self.merits[5][4]["MaxLevel"]
        ))
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"W6 Achievement: Spectre Stars: "
                  f"+{int(self.achievements['Spectre Stars']['Complete'])}/1%",
            picture_class="spectre-stars",
            progression=int(self.achievements['Spectre Stars']['Complete']),
            goal=1
        ))
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"W6 Achievement: Regalis My Beloved: "
                  f"+{int(self.achievements['Regalis My Beloved']['Complete'])}/1%",
            picture_class="regalis-my-beloved",
            progression=self.summoning['SanctuaryTotal'] if not self.achievements['Regalis My Beloved']['Complete'] else 360,
            goal=360
        ))
        self.summoning['WinnerBonusesMulti'] = max(1, player_mga * player_mgb)
        self.summoning['WinnerBonusesMultiMax'] = max(1, mga * mgb)
        self.summoning['WinnerBonusesAdvice'].append(Advice(
            label=f"Winner Bonuses Multi: {self.summoning['WinnerBonusesMulti']:.3f}/{self.summoning['WinnerBonusesMultiMax']:.3f}x",
            picture_class="summoning",
            progression=f"{self.summoning['WinnerBonusesMulti']:.3f}",
            goal=f"{self.summoning['WinnerBonusesMultiMax']:.3f}",
            #unit="x"
        ))
        #print(f"Summoning Winner Bonus Multis: {mga} * {mgb} = {self.summoning['WinnerBonusesMulti']}")

    def _calculate_w6_farming(self):
        self._calculate_w6_farming_crop_depot()
        self._calculate_w6_farming_markets()
        self._calculate_w6_farming_crop_value()
        self._calculate_w6_farming_crop_evo()
        self._calculate_w6_farming_crop_speed()
        self._calculate_w6_farming_bean_bonus()
        self._calculate_w6_farming_og()

    def _calculate_w6_farming_crop_depot(self):
        lab_multi = ValueToMulti(
            (self.labBonuses['Depot Studies PhD']['Value'] + self.labJewels['Pure Opal Rhombol']['Value']) * self.labBonuses['Depot Studies PhD']['Enabled']
        )
        #print(f"models._calculate_w6_farming_crop_depot lab_multi = {lab_multi}")
        for bonusName, bonusDetails in self.farming['Depot'].items():
            self.farming['Depot'][bonusName]['Value'] = self.farming['Depot'][bonusName]['BaseValue'] * lab_multi
            self.farming['Depot'][bonusName]['ValuePlus1'] = self.farming['Depot'][bonusName]['BaseValuePlus1'] * lab_multi

    def _calculate_w6_farming_markets(self):
        super_multi_current_stacks = ValueToMulti(self.farming['MarketUpgrades']['Super Gmo']['Value'] * self.farming['CropStacks']['Super Gmo'])
        super_multi_max_stacks = ValueToMulti(self.farming['MarketUpgrades']['Super Gmo']['Value'] * maxFarmingCrops)
        #print(f"models._calculate_w6_farming_day_market super_multi = {super_multi}")
        for name, details in self.farming['MarketUpgrades'].items():
            try:
                if "}" in details['Description']:  #Multiplicative
                    val = ValueToMulti(details['Value'])
                    self.farming['MarketUpgrades'][name]['Description'] = details['Description'].replace("}", f"{val:.3g}")
                else:
                    self.farming['MarketUpgrades'][name]['Description'] = details['Description'].replace("{", f"{details['Value']:g}")
                if name in self.farming['CropStacks']:
                    if name == 'Super Gmo':
                        self.farming['MarketUpgrades'][name]['StackedValue'] = super_multi_current_stacks
                        self.farming['MarketUpgrades'][name]['Description'] += (
                            f".<br>{self.farming['CropStacks'][name]} stacks = "
                            f"{super_multi_current_stacks:,.4g}x"
                        )
                    elif name == 'Evolution Gmo':
                        self.farming['MarketUpgrades'][name]['StackedValue'] = super_multi_current_stacks * pow(ValueToMulti(details['Value']), self.farming['CropStacks'][name])
                        self.farming['MarketUpgrades'][name]['Description'] += (
                            f".<br>{self.farming['CropStacks'][name]} stacks = "
                            f"{self.farming['MarketUpgrades'][name]['StackedValue']:,.4g}x"
                        )
                    else:
                        self.farming['MarketUpgrades'][name]['StackedValue'] = super_multi_current_stacks * (ValueToMulti(details['Value'] * self.farming['CropStacks'][name]))
                        self.farming['MarketUpgrades'][name]['Description'] += (
                            f".<br>{self.farming['CropStacks'][name]} stacks = "
                            f"{self.farming['MarketUpgrades'][name]['StackedValue']:,.5g}x"
                        )

            except Exception as reason:
                print(f"models._calculate_w6_farming_day_market: Exception substituting value for {name}: {reason}")
                continue

    def _calculate_w6_farming_crop_value(self):
        #if ("CropsBonusValue" == e)
        #return Math.min(100, Math.round(Math.max(1, Math.floor(1 + (c.randomFloat() + q._customBlock_FarmingStuffs("BasketUpgQTY", 0, 5) / 100))) * (1 + q._customBlock_FarmingStuffs("LandRankUpgBonusTOTAL", 1, 0) / 100) * (1 + (q._customBlock_FarmingStuffs("LankRankUpgBonus", 1, 0) * c.asNumber(a.engine.getGameAttribute("FarmRank")[0][0 | t]) + q._customBlock_Summoning("VotingBonusz", 29, 0)) / 100)));
        self.farming['Value'] = {}
        self.farming['Value']['Doubler Multi'] = floor(ValueToMulti(self.farming['MarketUpgrades']['Product Doubler']['Value']))
        self.farming['Value']['Mboost Sboost Multi'] = ValueToMulti(
            self.farming['LandRankDatabase']['Production Megaboost']['Value'] + self.farming['LandRankDatabase']['Production Superboost']['Value']
        )
        self.farming['Value']['Value GMO Current'] = self.farming['MarketUpgrades']['Value Gmo']['StackedValue']

        #Calculate with the Min Plot Rank
        self.farming['Value']['Pboost Ballot Multi Min'] = ValueToMulti(
            (self.farming['LandRankDatabase']['Production Boost']['Value']) * self.farming.get('LandRankMinPlot', 0)  #Value of PBoost * Lowest Plot Rank
            + (self.ballot['Buffs'][29]['Value'] * int(self.ballot['CurrentBuff'] == 29))  #Plus value of Ballot Buff * Active status
        )
        self.farming['Value']['BeforeCapMin'] = round(
            max(1, self.farming['Value']['Doubler Multi'])  #end of max
            * self.farming['Value']['Mboost Sboost Multi']
            * self.farming['Value']['Pboost Ballot Multi Min']
            * self.farming['Value']['Value GMO Current']
            )  #end of round

        #Now calculate with the Max Plot Rank
        self.farming['Value']['Pboost Ballot Multi Max'] = ValueToMulti(
            (self.farming['LandRankDatabase']['Production Boost']['Value']) * self.farming.get('LandRankMaxPlot', 0)  # Value of PBoost * Highest Plot Rank
            + (self.ballot['Buffs'][29]['Value'] * int(self.ballot['CurrentBuff'] == 29))  # Plus value of Ballot Buff * Active status
        )
        self.farming['Value']['BeforeCapMax'] = round(
            max(1, self.farming['Value']['Doubler Multi'])  # end of max
            * self.farming['Value']['Mboost Sboost Multi']
            * self.farming['Value']['Pboost Ballot Multi Max']
            * self.farming['Value']['Value GMO Current']
        )  # end of round
        self.farming['Value']['FinalMin'] = min(10000, self.farming['Value']['BeforeCapMin'])
        self.farming['Value']['FinalMax'] = min(10000, self.farming['Value']['BeforeCapMax'])
        #print(f"models._calculate_w6_farming_crop_value CropValue BEFORE cap = {self.farming['Value']['BeforeCap']}")
        #print(f"models._calculate_w6_farming_crop_value CropValue AFTER cap = {self.farming['Value']['Final']}")

    def _calculate_w6_farming_crop_evo(self):
        # Alchemy
        self.farming['Mama Trolls Unlocked'] = False
        self.farming['Evo'] = {}
        self.farming['Evo']['Maps Opened'] = 0
        for char in self.all_characters:
            for mapIndex in range(251, 264):  # Clearing the fake portal at Samurai Guardians doesn't count
                try:
                    if int(float(char.kill_dict.get(mapIndex, [1])[0])) <= 0:
                        self.farming['Evo']['Maps Opened'] += 1
                        if mapIndex == 257 and not self.farming['Mama Trolls Unlocked']:
                            self.farming['Mama Trolls Unlocked'] = True
                except:
                    continue
        self.farming['Evo']['Cropius Final Value'] = self.farming['Evo']['Maps Opened'] * self.alchemy_bubbles['Cropius Mapper']['BaseValue']
        self.farming['Evo']['Vial Value'] = self.alchemy_vials['Flavorgil (Caulifish)']['Value'] * self.vialMasteryMulti
        self.farming['Evo']['Vial Value'] *= 2 if self.labBonuses['My 1st Chemistry Set']['Enabled'] else 1
        self.farming['Evo']['Alch Multi'] = (
            ValueToMulti(self.farming['Evo']['Cropius Final Value'])
            # * ValueToMulti(session_data.account.alchemy_bubbles['Crop Chapter']['BaseValue'])
            * ValueToMulti(self.farming['Evo']['Vial Value'])
        )
        # Stamp
        self.farming['Evo']['Stamp Value'] = (
                max(1, 2 * self.labBonuses['Certified Stamp Book']['Enabled'])
                * max(1, 1.25 * self.sneaking['PristineCharms']['Liqorice Rolle']['Obtained'])
                * self.stamps['Crop Evo Stamp']['Value']
        )
        self.farming['Evo']['Stamp Multi'] = ValueToMulti(self.farming['Evo']['Stamp Value'])
        # Meals
        self.farming['Evo']['Nyan Stacks'] = ceil((max(self.all_skills['Summoning'], default=0) + 1) / 50)
        self.farming['Evo']['Meals Multi'] = (
                ValueToMulti(self.meals['Bill Jack Pepper']['Value'])
                * ValueToMulti(self.meals['Nyanborgir']['Value'] * self.farming['Evo']['Nyan Stacks'])
        )
        # Markets
        self.farming['Evo']['Farm Multi'] = ValueToMulti(self.farming['MarketUpgrades']['Biology Boost']['Value']) * self.farming['MarketUpgrades']['Evolution Gmo']['StackedValue']
        # Land Ranks
        self.farming['Evo']['LR Multi'] = (
                ValueToMulti(self.farming['LandRankDatabase']['Evolution Boost']['Value'] * self.farming['LandRankMinPlot'])
                * ValueToMulti(self.farming['LandRankDatabase']['Evolution Megaboost']['Value'])
                * ValueToMulti(self.farming['LandRankDatabase']['Evolution Superboost']['Value'])
                * ValueToMulti(self.farming['LandRankDatabase']['Evolution Ultraboost']['Value'])
        )
        # Summoning
        self.farming['Evo']['Summ Battles'] = {
            'Yellow': [9],
            'Blue': [14],
            'Red': [5]
        }
        battle_reward_total = 0
        for color, battlesList in self.farming['Evo']['Summ Battles'].items():
            for battle in battlesList:
                if self.summoning['Battles'][color] >= battle:
                    battle_reward_total += self.summoning["BattleDetails"][color][battle]['RewardBaseValue']
        self.farming['Evo']['Summon Multi'] = ValueToMulti(self.summoning['WinnerBonusesMulti'] * battle_reward_total)
        # Starsign
        self.farming['Evo']['Starsign Final Value'] = (
                3 * self.star_signs['Cropiovo Minor']['Unlocked']
                * max(self.all_skills['Farming'], default=0)
                * self.star_sign_extras['SilkrodeNanoMulti']
                * self.star_sign_extras['SeraphMulti']
        )
        self.farming['Evo']['SS Multi'] = ValueToMulti(self.farming['Evo']['Starsign Final Value'])
        # Misc
        self.farming['Evo']['Total Farming Levels'] = sum(self.all_skills['Farming'])
        self.farming['Evo']['Skill Mastery Bonus Bool'] = self.rift['SkillMastery'] and self.farming['Evo']['Total Farming Levels'] >= 300
        self.farming['Evo']['Ballot Active'] = self.ballot['CurrentBuff'] == 29
        if self.farming['Evo']['Ballot Active']:
            self.farming['Evo']['Ballot Status'] = "is Active"
        elif not self.farming['Evo']['Ballot Active'] and self.ballot['CurrentBuff'] != "Unknown":
            self.farming['Evo']['Ballot Status'] = "is Inactive"
        else:
            self.farming['Evo']['Ballot Status'] = "status is not available in provided data"
        self.farming['Evo']['Ballot Multi Max'] = ValueToMulti(self.ballot['Buffs'][29]['Value'])
        self.farming['Evo']['Ballot Multi Current'] = max(1, self.farming['Evo']['Ballot Multi Max'] * self.farming['Evo']['Ballot Active'])
        self.farming['Evo']['Misc Multi'] = (
                ValueToMulti(5 * self.achievements["Lil' Overgrowth"]['Complete'])
                * self.killroy_skullshop['Crop Multi']
                * ValueToMulti(15 * self.farming['Evo']['Skill Mastery Bonus Bool'] * self.rift['SkillMastery'])
                * self.farming['Evo']['Ballot Multi Current']
        )
        # subtotal doesn't include Crop Chapter
        self.farming['Evo']['Subtotal Multi'] = (
            self.farming['Evo']['Alch Multi']
            * self.farming['Evo']['Stamp Multi']
            * self.farming['Evo']['Meals Multi']
            * self.farming['Evo']['Farm Multi']
            * self.farming['Evo']['LR Multi']
            * self.farming['Evo']['Summon Multi']
            * self.farming['Evo']['SS Multi']
            * self.farming['Evo']['Misc Multi']
        )

    def _calculate_w6_farming_crop_speed(self):
        self.farming['Speed'] = {}
        # Summoning
        self.farming['Speed']['Summ Battles'] = {
            'White': [3, 9],
            'Green': [7, 13],
            'Yellow': [7],
            'Purple': [4],
            'Red': [10],
            'Cyan': [12]
        }
        battle_reward_total = 0
        for color, battlesList in self.farming['Speed']['Summ Battles'].items():
            for battle in battlesList:
                if self.summoning['Battles'][color] >= battle:
                    battle_reward_total += self.summoning["BattleDetails"][color][battle]['RewardBaseValue']
        self.farming['Speed']['Summon Multi'] = ValueToMulti(self.summoning['WinnerBonusesMulti'] * battle_reward_total)
        # Vial and Day Market
        self.farming['Speed']['Vial Value'] = self.alchemy_vials['Ricecakorade (Rice Cake)']['Value'] * self.vialMasteryMulti
        self.farming['Speed']['Vial Value'] *= 2 if self.labBonuses['My 1st Chemistry Set']['Enabled'] else 1
        self.farming['Speed']['VM Multi'] = ValueToMulti(self.farming['Speed']['Vial Value'] + self.farming['MarketUpgrades']['Nutritious Soil']['Value'])
        # Night Market
        self.farming['Speed']['NM Multi'] = self.farming['MarketUpgrades']['Speed Gmo']['StackedValue']
        # Total
        self.farming['Speed']['Total Multi'] = self.farming['Speed']['Summon Multi'] * self.farming['Speed']['VM Multi'] * self.farming['Speed']['NM Multi']

    def _calculate_w6_farming_bean_bonus(self):
        self.farming['Bean'] = {}
        self.farming['Bean']['mga'] = ValueToMulti(self.farming['MarketUpgrades']['More Beenz']['Value'])
        self.farming['Bean']['mgb'] = ValueToMulti(
            (25 * self.sneaking['JadeEmporium']['Deal Sweetening']['Obtained'])
            + (5 * self.achievements['Crop Flooding']['Complete'])
        )
        self.farming['Bean']['Total Multi'] = self.farming['Bean']['mga'] * self.farming['Bean']['mgb']

    def _calculate_w6_farming_og(self):
        # Fun calculations
        self.farming['OG'] = {}
        self.farming['OG']['Ach Multi'] = ValueToMulti(15 * self.achievements['Big Time Land Owner']['Complete'])
        self.farming['OG']['Starsign Final Value'] = (
                15 * self.star_signs['O.G. Signalais']['Unlocked']
                * self.star_sign_extras['SilkrodeNanoMulti']
                * self.star_sign_extras['SeraphMulti']
        )
        self.farming['OG']['SS Multi'] = ValueToMulti(self.farming['OG']['Starsign Final Value'])
        self.farming['OG']['NM Multi'] = ValueToMulti(self.farming['MarketUpgrades']['Og Fertilizer']['Value'])
        self.farming['OG']['Merit Multi'] = ValueToMulti(2 * self.merits[5][2]['Level'])
        self.farming['OG']['LR Multi'] = (ValueToMulti(
            self.farming['LandRankDatabase']['Overgrowth Boost']['Value']
            + self.farming['LandRankDatabase']['Overgrowth Megaboost']['Value']
            + self.farming['LandRankDatabase']['Overgrowth Superboost']['Value']
        ))
        self.farming['OG']['Pristine Multi'] = ValueToMulti(50 * self.sneaking['PristineCharms']['Taffy Disc']['Obtained'])
        self.farming['OG']['Total Multi'] = (
                self.farming['OG']['Ach Multi']
                * self.farming['OG']['SS Multi']
                * self.farming['OG']['NM Multi']
                * self.farming['OG']['Merit Multi']
                * self.farming['OG']['LR Multi']
                * self.farming['OG']['Pristine Multi']
        )

    def _calculate_wave_2(self):
        self._calculate_w3_library_max_book_levels()
        self._calculate_general_character_over_books()
        self._calculate_general_crystal_spawn_chance()

    def _calculate_w3_library_max_book_levels(self):
        self.library['StaticSum'] = (
            0
            + (25 * (0 < self.construction_buildings['Talent Book Library']['Level']))
            + (5 * self.achievements['Checkout Takeout']['Complete'])
            + (10 * (0 < self.atom_collider['Atoms']['Oxygen - Library Booker']['Level']))
            + (25 * self.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0))
        )
        self.library['ScalingSum'] = (
            0
            + 2 * self.merits[2][2]['Level']
            + 2 * self.saltlick.get('Max Book', 0)
        )
        # summGroupA = (1 + (.25 * self.sailing['Artifacts'].get('The Winz Lantern', {}).get('Level', 0))
        #               + .01 * self.merits[5][4]['Level']
        #               + .01 * (0 < self.achievements.get('Spectre Stars', False))
        #               + .01 * (0 < self.achievements.get('Regalis My Beloved', False))
        #               )
        # summGroupB = 1 + (.3 * self.sneaking.get('PristineCharms', {}).get('Crystal Comb', 0))
        self.library['SummoningSum'] = round(
            10.5 * (self.summoning['Battles']['Cyan'] >= 14)
            * self.summoning['WinnerBonusesMulti']
        )
        self.library['MaxBookLevel'] = 100 + self.library['StaticSum'] + self.library['ScalingSum'] + self.library['SummoningSum']

    def _calculate_general_character_over_books(self):
        self.bonus_talents = {
            "Rift Slug": {
                "Value": 25 * self.riftslug_owned,
                "Image": "rift-slug",
                "Label": f"Companion: Rift Slug: "
                         f"+{25 * self.riftslug_owned}/25",
                "Progression": 1 if self.riftslug_owned else 0,
                "Goal": 1
            },
            "ES Family": {
                "Value": floor(self.family_bonuses["Elemental Sorcerer"]['Value']),
                "Image": 'elemental-sorcerer-icon',
                "Label": f"ES Family Bonus: "
                         f"+{floor(self.family_bonuses['Elemental Sorcerer']['Value'])}.<br>"
                         f"Next increase at Class Level: ",
                "Progression": self.family_bonuses['Elemental Sorcerer']['Level'],
                "Goal": getNextESFamilyBreakpoint(self.family_bonuses['Elemental Sorcerer']['Level'])
            },
            "Equinox Symbols": {
                "Value": self.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
                "Image": 'equinox-symbols',
                "Label": f"{{{{ Equinox|#equinox }}}}: Equinox Symbols: "
                         f"+{self.equinox_bonuses['Equinox Symbols']['CurrentLevel']}/{self.equinox_bonuses['Equinox Symbols']['FinalMaxLevel']}",
                "Progression": self.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
                "Goal": self.equinox_bonuses['Equinox Symbols']['FinalMaxLevel']
            },
            "Maroon Warship": {
                "Value": 1 * self.achievements['Maroon Warship']['Complete'],
                "Image": "maroon-warship",
                "Label": f"W5 Achievement: Maroon Warship: "
                         f"+{1 * self.achievements['Maroon Warship']['Complete']}/1",
                "Progression": 1 if self.achievements['Maroon Warship']['Complete'] else 0,
                "Goal": 1
            },
            "Sneaking Mastery": {
                "Value": 5 if self.sneaking['MaxMastery'] >= 3 else 0,
                "Image": "sneaking-mastery",
                "Label": f"{{{{ Rift|#rift }}}}: Sneaking Mastery: "
                         f"+{5 if self.sneaking['MaxMastery'] >= 3 else 0}/5 (Mastery III)",
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
                arctis_base = 15
                #bigp_value = self.alchemy_bubbles['Big P']['BaseValue']
                #div_minorlink_value = char.divinity_level / (char.divinity_level + 60)
                #final_result = ceil(arctis_base * bigp_value * div_minorlink_value)
                character_specific_bonuses += ceil(arctis_base * self.alchemy_bubbles['Big P']['BaseValue'] * (char.divinity_level / (char.divinity_level + 60)))

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

    def _calculate_general_crystal_spawn_chance(self):
        #This assumes you have the Shrine bonus and the Star Talent maxed
        poop_value = 10 * (1 + next(c.getStars() for c in self.cards if c.name == 'Poop'))
        genie_value = 15 * (1 + next(c.getStars() for c in self.cards if c.name == 'Demon Genie'))

        # If they have both doublers, add together and 2x
        if self.labChips['Omega Nanochip'] and self.labChips['Omega Motherboard']:
            total_card_chance = 2 * (poop_value + genie_value)
        # If they only have 1 doubler, double whichever is stronger
        elif self.labChips['Omega Nanochip'] or self.labChips['Omega Motherboard']:
            total_card_chance = (2 * max(poop_value, genie_value)) + min(poop_value, genie_value)
        # If they have neither doubler, use base values only
        else:
            total_card_chance = poop_value + genie_value

        account_wide = (
            base_crystal_chance
            * ValueToMulti(self.stamps['Crystallin']['Value'])
            * ValueToMulti(total_card_chance)
        )

        for char in self.all_characters:
            cmon_out_crystals_multi = max(1, ValueToMulti(lavaFunc(
                'decay',
                char.max_talents_over_books if char.max_talents.get("26", 0) > 0 else 0,  #This is an assumption that Cmon Out Crystals is max booked
                300,
                100
            )))
            crystals_4_dayys_multi = max(1, ValueToMulti(lavaFunc(
                'decay',
                char.max_talents.get("619", 0),
                174,
                50
            )))
            shrine_and_po = ValueToMulti(char.po_boxes_invested['Non Predatory Loot Box']['Bonus3Value'] + self.shrines['Crescent Shrine']['Value'])
            try:
                character_influenced = (
                    shrine_and_po
                    * cmon_out_crystals_multi
                    * crystals_4_dayys_multi
                )
            except Exception as reason:
                print(f"Character Specific crystal spawn chance calc exception for {char.character_name}: {reason}")
                character_influenced = 1
            char.setCrystalSpawnChance(account_wide * character_influenced)
        self.highest_crystal_spawn_chance = max([char.crystal_spawn_chance for char in self.all_characters if "Journeyman" not in char.all_classes],
                                                default=base_crystal_chance)
        self.highest_jman_crystal_spawn_chance = max([char.crystal_spawn_chance for char in self.all_characters if "Journeyman" in char.all_classes],
                                                     default=base_crystal_chance)

    def _make_cards(self):
        card_counts = safe_loads(self.raw_data.get(self._key_cards, {}))
        cards = [
            Card(codename, name, cardset, int(float(safer_get(card_counts, codename, 0))), coefficient)
            for cardset, cards in card_data.items()
            for codename, (name, coefficient) in cards.items()
        ]

        return cards

    def _all_stored_items(self) -> Assets:
        chest_keys = (("ChestOrder", "ChestQuantity"),)
        name_quantity_key_pairs = chest_keys + tuple(
            (f"InventoryOrder_{i}", f"ItemQTY_{i}") for i in self.safe_playerIndexes
        )
        all_stuff_stored_or_in_inv = dict.fromkeys(items_codes_and_names.keys(), 0)

        for name_key, quantity_key in name_quantity_key_pairs:
            pair_item_name_to_quantity = zip(self.raw_data.get(name_key, list()), self.raw_data.get(quantity_key, list()))
            for name, count in pair_item_name_to_quantity:
                if name not in all_stuff_stored_or_in_inv:
                    all_stuff_stored_or_in_inv[name] = int(count)
                else:
                    all_stuff_stored_or_in_inv[name] += int(count)

        return Assets(all_stuff_stored_or_in_inv)

    def _all_worn_items(self) -> Assets:
        stuff_worn = defaultdict(int)
        for toon in self.safe_characters:
            for item in [*toon.equipment.foods, *toon.equipment.equips]:
                if item.codename == 'Blank':
                    continue
                stuff_worn[item.codename] += item.amount

        return Assets(stuff_worn)
