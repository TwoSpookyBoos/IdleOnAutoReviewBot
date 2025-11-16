import functools
import json
import os
import re
import sys
from enum import Enum
from math import ceil, floor
from typing import Any, Union
from flask import g
from config import app
from consts.consts_autoreview import ignorable_labels
from consts.consts_idleon import lavaFunc, expected_talents_dict
from consts.consts_general import greenstack_amount, gstackable_codenames, gstackable_codenames_expected, quest_items_codenames, cards_max_level, \
    greenstack_item_difficulty_groups, current_world
from consts.consts_w5 import divinity_divinities_dict
from consts.consts_w4 import lab_chips_dict
from consts.consts_w3 import (
    prayers_dict, dn_skull_requirement_list, dn_skull_value_list, reversed_dn_skull_requirement_list, reversed_dn_skull_value_list,
    apocable_map_index_dict, apoc_names_list, getSkullNames, getNextSkullNames
)
from consts.consts_w2 import alchemy_jobs_list, po_box_dict
from models.custom_exceptions import VeryOldDataException
from utils.data_formatting import safe_loads, safer_get, get_obol_totals, safer_convert
from utils.number_formatting import parse_number
from utils.text_formatting import kebab, getItemCodeName, getItemDisplayName, InputType


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

            equips_data = safe_loads(raw_data.get(f'EMm0_{toon_index}', ''))
            equips_data = [{index: item_data} for index, item_data in equips_data.items()]
            for i in range(len(order[0]) - 1):
                key = str(i)
                if not any(key in d.keys() for d in equips_data):
                    equips_data.insert(i, {key: {}})
            equips_data = sorted(equips_data, key=lambda sub_dict: int(list(sub_dict.keys())[0]))
            equips_data = [list(item.values())[0] for item in equips_data]
            equips_data = [equips_data, [{} for _ in range(len(order[1]) - 1)], [{} for _ in range(len(order[2]) - 1)]]

            groups = list()
            for o, q, d in zip(order, quantity, equips_data):
                o.pop("length", None)
                q.pop("length", None)
                o = dict(sorted(o.items(), key=lambda i: int(i[0]))).values()
                q = dict(sorted(q.items(), key=lambda i: int(i[0]))).values()
                groups.append([Asset(name, float(count), **stats) for name, count, stats in zip(o, q, d)])

            inv_order = raw_data.get(f"InventoryOrder_{toon_index}", [])
            inv_quantity = raw_data.get(f"ItemQTY_{toon_index}", [])
            all_inventory = {}
            for o, q in zip(inv_order, inv_quantity):
                if o in all_inventory:
                    all_inventory[o] += safer_convert(q, 0.0)
                else:
                    all_inventory[o] = safer_convert(q, 0.0)
                groups.append([Asset(name, count) for name, count in all_inventory.items()])

            # equips, tools, foods = groups

            self.equips = groups[0] if groups else []
            self.tools = groups[1] if groups else []
            self.foods = groups[2] if groups else []
            self.inventory = groups[3] if groups else []
        else:
            self.equips = []
            self.tools = []
            self.foods = []
            self.inventory = []

def getExpectedTalents(classes_list):
    expectedTalents = []
    for className in classes_list:
        try:
            expectedTalents.extend(expected_talents_dict[className])
        except:
            continue
    return expectedTalents

def getSpecializedSkills(classes_list):
    specializedSkillsList = []
    if "Warrior" in classes_list:
        specializedSkillsList.append("Mining")
    elif "Archer" in classes_list:
        specializedSkillsList.append("Smithing")
    elif "Mage" in classes_list:
        specializedSkillsList.append("Chopping")

    if "Barbarian" in classes_list:
        specializedSkillsList.append("Fishing")
    elif "Squire" in classes_list:
        specializedSkillsList.append("Construction")
    elif "Bowman" in classes_list:
        specializedSkillsList.append("Catching")
    elif "Hunter" in classes_list:
        specializedSkillsList.append("Trapping")
    elif "Wizard" in classes_list:
        specializedSkillsList.append("Worship")
    elif "Shaman" in classes_list:
        specializedSkillsList.append("Alchemy")

    if 'Blood Berserker' in classes_list:
        specializedSkillsList.append('Cooking')
    elif 'Divine Knight' in classes_list:
        specializedSkillsList.append('Gaming')
    elif 'Siege Breaker' in classes_list:
        specializedSkillsList.append('Sailing')
    elif 'Beast Master' in classes_list:
        specializedSkillsList.append('Breeding')
    elif 'Elemental Sorcerer' in classes_list:
        specializedSkillsList.append('Divinity')
    elif 'Bubonic Conjuror' in classes_list:
        specializedSkillsList.append('Laboratory')

    if 'Death Bringer' in classes_list:
        specializedSkillsList.append('Farming')
    elif 'Wind Walker' in classes_list:
        specializedSkillsList.append('Sneaking')

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
        master_class: str,
        equipped_prayers: list,
        all_skill_levels: dict,
        max_talents: dict,
        current_map_index: int,
        current_preset_talents: dict,
        secondary_preset_talents: dict,
        current_preset_talent_bar: dict,
        secondary_preset_talent_bar: dict,
        obols: list[str],
        obol_upgrades: dict,
        po_boxes: list[int],
        equipped_lab_chips: list[str],
        inventory_bags: dict,
        kill_dict: dict,
        big_alch_bubbles: list[str],
        alchemy_job: int,
        main_stats: dict[str, int],
        equipped_cardset: str,
        equipped_cards: list['Card'] = None,
        equipped_cards_codenames: list[str] = None,
        equipped_star_signs: list[int] = None
    ):

        self.character_index: int = character_index
        self.character_name: str = character_name

        self.class_name: str = class_name
        self.class_name_icon: str = class_name.replace(" ", "-") + "-icon"
        self.base_class: str = base_class
        self.sub_class: str = sub_class
        self.elite_class: str = elite_class
        self.master_class: str = master_class
        self.all_classes: list[str] = [base_class, sub_class, elite_class, master_class]
        self.max_talents_over_books: int = 100
        self.symbols_of_beyond = 0
        self.family_guy_bonus = 0
        self.current_map_index = current_map_index
        self.max_talents: dict = max_talents
        self.current_preset_talents: dict = current_preset_talents
        self.secondary_preset_talents: dict = secondary_preset_talents
        self.current_preset_talent_bar: dict = current_preset_talent_bar
        self.secondary_preset_talent_bar: dict = secondary_preset_talent_bar
        self.fix_talent_bars()
        self.specialized_skills: list[str] = getSpecializedSkills(self.all_classes)
        self.expected_talents: list[int] = getExpectedTalents(self.all_classes)
        self.inventory_bags: dict = inventory_bags
        self.inventory_slots: int = 0
        self.kill_dict: dict = kill_dict
        self.fixKillDict()
        self.big_alch_bubbles: list[str] = big_alch_bubbles
        self.alchemy_job: int = alchemy_job
        self.alchemy_job_string = 'Unassigned'
        self.alchemy_job_group = 'Unassigned'
        self.decode_alchemy_job()
        self.crystal_spawn_chance: float = 0.0

        self.combat_level: int = all_skill_levels["Combat"]
        self.mining_level: int = all_skill_levels["Mining"]
        self.smithing_level: int = all_skill_levels["Smithing"]
        self.choppin_level: int = all_skill_levels["Chopping"]
        self.fishing_level: int = all_skill_levels["Fishing"]
        self.alchemy_level: int = all_skill_levels["Alchemy"]
        self.catching_level: int = all_skill_levels["Catching"]
        self.trapping_level: int = all_skill_levels["Trapping"]
        self.construction_level: int = all_skill_levels["Construction"]
        self.worship_level: int = all_skill_levels["Worship"]
        self.cooking_level: int = all_skill_levels["Cooking"]
        self.breeding_level: int = all_skill_levels["Breeding"]
        self.lab_level: int = all_skill_levels["Laboratory"]
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
                    self.equipped_prayers.append(prayers_dict[prayerIndex]['Name'])
                except:
                    continue
        self.skills = all_skill_levels
        self.divinity_style: str = "None"
        self.divinity_link: str = "Unlinked"
        self.current_polytheism_link = "Unlinked"
        self.secondary_polytheism_link = "Unlinked"
        self.obols = get_obol_totals(obols, obol_upgrades)

        self.po_boxes_invested = {}
        for poBoxIndex, poBoxValues in po_box_dict.items():
            try:
                self.po_boxes_invested[poBoxValues['Name']] = {
                    'Level': po_boxes[poBoxIndex],
                    'Max Level': poBoxValues['Max Level'],
                    'Tab': poBoxValues['Tab'],
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
                    'Max Level': poBoxValues['Max Level'],
                    'Tab': poBoxValues['Tab'],
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
                    self.equipped_lab_chips.append(lab_chips_dict[chipIndex]['Name'])
                except:
                    continue
        self.equipped_card_doublers: list[str] = self.get_card_doublers()

        self.apoc_dict: dict = {
            name: {
                **{f"Basic W{i} Enemies": list() for i in range(1, current_world+1)},
                "Easy Extras": [],
                "Medium Extras": [],
                "Difficult Extras": [],
                "Insane": [],
                "Impossible": [],
                "Total": 0,
            }
            for name in apoc_names_list
        }
        self.equipment = Equipment(raw_data, character_index, self.combat_level >= 1)
        self.printed_materials = {}

        self.setPolytheismLink()

        self.main_stats = main_stats
        self.equipped_cardset = equipped_cardset
        self.equipped_cards = equipped_cards if equipped_cards else []
        self.equipped_cards_codenames = equipped_cards_codenames if equipped_cards_codenames else []
        self.equipped_star_signs = equipped_star_signs if equipped_star_signs else []

    def fix_talent_bars(self):
        #Current preset
        try:
            temp_list = []
            for list_of_attack_bars in self.current_preset_talent_bar:
                if isinstance(list_of_attack_bars, int):
                    # Accounts who claimed WW through the AFK trick aren't initialized properly into a list
                    temp_list.append(list_of_attack_bars)
                elif isinstance(list_of_attack_bars, list):
                    for talent_entry in list_of_attack_bars:
                        if talent_entry != 'Null':
                            temp_list.append(talent_entry)
            self.current_preset_talent_bar = temp_list
            # self.current_preset_talent_bar = [
            #     attack_entry
            #     for list_of_attack_bars in self.current_preset_talent_bar
            #     for attack_entry in list_of_attack_bars
            #     if attack_entry != 'Null'
            # ]
            # print(f"Character{self.character_index} Primary bar: {self.current_preset_talent_bar}")
        except:
            self.current_preset_talent_bar = []

        #Secondary preset
        try:
            temp_list = []
            for list_of_attack_bars in self.current_preset_talent_bar:
                if isinstance(list_of_attack_bars, int):
                    # Accounts who claimed WW through the AFK trick aren't initialized properly into a list
                    temp_list.append(list_of_attack_bars)
                elif isinstance(list_of_attack_bars, list):
                    for talent_entry in list_of_attack_bars:
                        if talent_entry != 'Null':
                            temp_list.append(talent_entry)
            self.current_preset_talent_bar = temp_list
            # self.secondary_preset_talent_bar = [
            #     attack_entry
            #     for list_of_attack_bars in self.secondary_preset_talent_bar
            #     for attack_entry in list_of_attack_bars
            #     if attack_entry != 'Null'
            # ]
            # print(f"Character{self.character_index} Secondary bar: {self.secondary_preset_talent_bar}")
        except:
            self.secondary_preset_talent_bar = []

    def fixKillDict(self):
        for mapIndex in self.kill_dict:
            #If the map is already a List as expected,
            # if each entry isn't already float or int,
            #  try to convert every entry to a float or set to 0 if error
            if isinstance(self.kill_dict[mapIndex], list):
                for killIndex, killCount in enumerate(self.kill_dict[mapIndex]):
                    if not isinstance(killCount, float) or not isinstance(killCount, int):
                        try:
                            self.kill_dict[mapIndex][killIndex] = parse_number(killCount)
                        except:
                            self.kill_dict[mapIndex][killIndex] = 0
            else:
                #Sometimes users have just raw strings, floats, or ints that aren't in a list
                # Try to put them into a list AND convert to float/int at the same time
                #  else default to a list containing zeroes as some maps have multiple portals
                try:
                    self.kill_dict[mapIndex] = [parse_number(self.kill_dict[mapIndex])]
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
                    self.current_polytheism_link = divinity_divinities_dict[(current_preset_level % 10) - 1]['Name']  #Dict starts at 1 for Snake, not 0
            except:
                pass
            try:
                secondary_preset_level = self.secondary_preset_talents.get("505", 0)
                if secondary_preset_level > 0:
                    self.secondary_polytheism_link = divinity_divinities_dict[(secondary_preset_level % 10) - 1]['Name']  #Dict starts at 1 for Snake, not 0
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

    def isArctisLinked(self):
        return 'Arctis' in [
            self.divinity_link, self.current_polytheism_link, self.secondary_polytheism_link
        ]

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

    def decode_alchemy_job(self):
        if self.alchemy_job == -1:
            return  #Keep the default of 'Unassigned'

        if 0 <= self.alchemy_job <= 3:
            self.alchemy_job_string = alchemy_jobs_list[self.alchemy_job]
            self.alchemy_job_group = 'Bubble Cauldron'
        elif 4 <= self.alchemy_job <= 7:
            self.alchemy_job_string = alchemy_jobs_list[self.alchemy_job]
            self.alchemy_job_group = 'Liquid Cauldron'
        elif 100 <= self.alchemy_job:
            self.alchemy_job_group = 'Sigils'
            try:
                # The first character assigned to a Sigil is X.1, second is X.2, etc. up through X.4
                # Example of 101.3 would mean 2nd sigil (Pumped Kicks), 3rd character slot.
                # All I care about is which Sigil, not the ordering, so cast to int
                self.alchemy_job_string = alchemy_jobs_list[int(self.alchemy_job)-92]
            except:
                self.alchemy_job_string = f"Sigil-{self.alchemy_job}"

        else:
            self.alchemy_job_string = f'UnknownJob{self.alchemy_job}'
            self.alchemy_job_group = 'UnknownJobGroup'

    def get_card_doublers(self):
        return [chip for chip in ['Omega Nanochip', 'Omega Motherboard'] if chip in self.equipped_lab_chips]

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
        return [[attr, getattr(self, attr, False)] for attr in ["optional", "completed", "informational", "unrated", "unreached", "overwhelming"]]


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
        unit (str): if there is one, usually "%" or x
    """

    def __init__(
            self, label: str,
            picture_class: str,
            progression: Any = "",
            goal: Any = "",
            unit: str = "",
            value_format: str = "{value}{unit}",
            resource: str = "",
            completed: bool | None = None,
            unrated: bool = False,
            overwhelming: bool = False,
            optional: bool = False,
            potential: Any = "",
            **extra
    ):
        super().__init__(**extra)

        self.label: str = label if extra.get("as_link") else LabelBuilder(label).label
        if picture_class and picture_class[0].isdigit():
            picture_class = f"x{picture_class}"
        self.picture_class: str = picture_class
        self.progression: str = str(progression)
        self.potential: str = str(potential)
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

        numeric_progression = self.__extract_float(self.progression)
        numeric_potential = self.__extract_float(self.potential)
        numeric_goal = self.__extract_float(self.goal)

        self.percent: float = 0.0
        if(numeric_goal is not None and numeric_progression is not None):
            # NOTE: This was an idea to handle cases, where progras is decending
            # Ill have to look into the overwhelming attr
            # if(numeric_goal < numeric_progression):
            #     numeric_progression, numeric_goal = numeric_goal, numeric_progression
            #     numeric_potential = numeric_goal - numeric_progression

            self.percent = self.__calculate_progress_box_width_numeric(
                numeric_progression, numeric_goal
            )
            self.potential_percent = self.__calculate_progress_box_width_numeric(
                numeric_potential, numeric_goal
            )

            # prevent overflow of potential percent
            if (self.percent + self.potential_percent) > 100:
                self.potential_percent = 100 - self.percent

        self.overwhelming = overwhelming
        self.optional = optional

    @property
    def css_class(self) -> str:
        name = kebab(self.picture_class)
        return name

    def __str__(self) -> str:
        return self.label

    def __extract_float(self, value: str | float | int) -> float | None:
        """
        Extracts a float from a string, 
        """
        if (value is None):
            return None
        if (isinstance(value, str)):
            float_re = re.compile(r'((?:\d+|,)+(?:\.\d+)?)')
            res = float_re.search(value)
            if res is None or len(res.groups()) != 1:
                return None

            # Sanitize the value from all commas
            val = res[0].replace(',', '')
            try:
                return float(val)
            except ValueError:
                # Just in case
                return None
        elif (isinstance(value, (int, float))):
            return float(value)
        return value

    def __calculate_progress_box_width_numeric(self, calc_num: float, goal_num: float) -> float:
        if calc_num is None or goal_num is None:
            return 0.0

        if goal_num == 0:
            return 0.0 # A goal of 0 currently makes no sense, since descending progression is not supported

        percentage = round(100 * calc_num / goal_num, 2)
        return min(percentage, 100.0)

    def update_optional(self, parent_value: bool):
        self.optional = parent_value

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
        overwhelming: bool | None = False,
        optional: bool = False,
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
        self.overwhelming = overwhelming
        self.optional = optional

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
            text += f"{'Optional ' if self.optional else ''}Tier {self.tier}"
        if self.informational:
            text += "Info"
        if self.pre_string:
            text += f"{' - ' if text else ''}{self.pre_string}"
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
                    self.advices['default'] = list[Advice] = sorted(
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
        elif self.tier != '':
            return False
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

    def set_overwhelming(self, overwhelming):
        self.overwhelming = overwhelming
        if isinstance(self.advices, list):
            for advice in self.advices:
                advice.overwhelming = overwhelming
        if isinstance(self.advices, dict):
            for value in self.advices.values():
                for advice in value:
                    advice.overwhelming = overwhelming

    def check_for_optional(self, max_tier: int, override=None):
        if override is not None:
            self.optional = override
        if self.optional is not True:
            if self.tier.isdigit():
                self.optional = int(self.tier) > max_tier
        if self.optional:
            # If Optional, all Children will be Optional too
            if isinstance(self.advices, list):
                for advice in self.advices:
                    advice.update_optional(self.optional)
            if isinstance(self.advices, dict):
                for value in self.advices.values():
                    for advice in value:
                        advice.update_optional(self.optional)

class TabbedAdviceGroupTab:
    completed = None
    informational = None
    optional = None

    def __init__(self, picture_class: str = "", label: str = ""):
        self.picture_class = picture_class
        self.label = label

    @property
    def dataset(self) -> list:
        return [[attr, getattr(self, attr, False)] for attr in ["completed", "informational", "optional"]]


class TabbedAdviceGroup:
    completed = None
    informational = None
    optional = None
    _children = "tabbed_advices"
    __compare_by = ["tier"]

    def __init__(self, tabbed_advices: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]]):
        self.tabbed_advices = tabbed_advices
        self.tier = min([advice_group._coerce_to_int("tier") for _, advice_group in tabbed_advices.values()])
        self.check_for_informationalness()

    def check_for_completeness(self):
        if self.completed is not None:
            return
        self.completed = True
        for tab, advice_group in self.tabbed_advices.values():
            advice_group.check_for_completeness()
            if not advice_group.completed:
                self.completed = False
            else:
                tab.completed = True

    def check_for_informationalness(self):
        if self.informational is not None:
            return
        self.informational = True
        for tab, advice_group in self.tabbed_advices.values():
            if not advice_group.informational:
                self.informational = False
            else:
                tab.informational = True

    def check_for_optional(self, max_tier: int):
        self.optional = True
        for tab, advice_group in self.tabbed_advices.values():
            advice_group.check_for_optional(max_tier)
            if not advice_group.optional:
                self.optional = False
            else:
                tab.optional = True

    def set_overwhelming(self, overwhelming: bool):
        for _, group in self.tabbed_advices.values():
            group.set_overwhelming(overwhelming)

    def remove_empty_subgroups(self):
        for _, group in self.tabbed_advices.values():
            group.remove_empty_subgroups()

    @property
    def dataset(self) -> list:
        return [[attr, getattr(self, attr, False)] for attr in ["completed", "informational", "optional"]]

    @property
    def tabbed_advices(self):
        return self._tabbed_advices

    @tabbed_advices.setter
    def tabbed_advices(self, tabbed_advices: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]]):
        self._tabbed_advices = {key: tabbed_advice for key, tabbed_advice in tabbed_advices.items() if tabbed_advice[1]}

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


class Asset:
    def __init__(self, codename: Union[str, "Asset"], amount: float, name: str = "", **stats):
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
            self.stats = {}
            self.set_stats(stats)
            pass

    def set_stats(self, stats: dict):
        wanted_stats = {
            'UQ1txt': 'misc_1_txt',
            'UQ1val': 'misc_1_val',
            'UQ2txt': 'misc_2_txt',
            'UQ2val': 'misc_2_val'
        }
        for key, value in stats.items():
            try:
                if value != 0:
                    self.stats[wanted_stats[key]] = value
                    pass
            except KeyError:
                pass

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
        return self.amount >= greenstack_amount

    @property
    def progression(self) -> int:
        return self.amount * 100 // greenstack_amount

class Assets(dict):
    def __init__(self, assets: Union[dict[str, int], "Assets", None] = None):
        self.tiers = greenstack_item_difficulty_groups

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
    def __init__(self, codename, name, cardset, count, coefficient, value_per_level, description):
        self.codename = codename
        self.count = ceil(float(count))
        self.cardset = cardset
        self.name = name
        self.coefficient = coefficient
        self.star = self.getStars()
        self.level = self.star + 1 if self.count > 0 else 0
        self.css_class = name + " Card"
        self.diff_to_next = (
            ceil(self.getCardsForStar(self.star + 1)) or sys.maxsize
        ) - self.count
        self.value_per_level = value_per_level
        self.description = description
        self.max_level = cards_max_level

    def getStars(self):
        return next(
            (
                i
                for i in range(cards_max_level-1, -1, -1)
                if self.count >= round(self.getCardsForStar(i))
            ),
            -1,
        )

    def getCardsForStar(self, star):
        """
        0 stars always requires 1 card.
        1 star is set per enemy.
        2 stars = 3x additional what 1star took, for a total of 1+3 = 4x (2^2).
        3 stars = 5x additional what 1star took, for a total of 4+5 = 9x (3^2).
        4 stars = 16x additional what 1star took, for a total of 9+16 = 25x (5^2).
        5 stars = 459x additional what 1star took, for a total of 25+459 = 484x (22^2).
        6 stars = 14,670x additional what 1star took, for a total of 484+14,670 = 15,129x  (123^2).
        7 stars = 496x additional what 1star took, for a total of 15,129+496 = 15,625x (125^2).
        """
        if star == 0:
            return 1
        previous_star = star - 1
        if self.name == 'Chaotic Chizoar':
            tier_coefficient = previous_star + 1 + floor(previous_star/3)
            # `_customBlock_RunCodeOfTypeXforThingY , CardLv==e` in source. Last updated in v2.43 Nov 11
            # The formula in the code includes `*1.5` at the end. That's the self.coefficient for Chaotic Chizoar
            # which is accounted for below in the total_cards_needed. Adding it again here will give bad answers.
        else:
            tier_coefficient = previous_star + 1 + (floor(previous_star/3) + (16 * floor(previous_star/4) + 100 * floor(previous_star/5)))
        total_cards_needed = (self.coefficient * tier_coefficient**2) + 1
        # print(f"{star} star {self.name} needs {total_cards_needed:,} cards [({self.coefficient} * {tier_coefficient}^2) + 1]")
        return total_cards_needed

    def getCardDoublerMultiplier(self, optional_character: Character=None):
        card_doubler = 1
        if optional_character and optional_character.equipped_card_doublers and self.codename in optional_character.equipped_cards_codenames:
            equipped_slot = optional_character.equipped_cards_codenames.index(self.codename)
            if (equipped_slot == 0 and "Omega Nanochip" in optional_character.equipped_card_doublers) or (equipped_slot == 7 and "Omega Motherboard" in optional_character.equipped_card_doublers):
                card_doubler = 2
        return card_doubler

    def getCurrentValue(self, optional_character: Character=None):
        return self.level * self.value_per_level * self.getCardDoublerMultiplier(optional_character)

    def getMaxValue(self, optional_character: Character=None):
        return cards_max_level * self.value_per_level * self.getCardDoublerMultiplier(optional_character)

    def getFormattedXY(self, optional_character: Character=None):
        result = (
            f"{'+' if '+' in self.description else ''}"
            + f"{self.getCurrentValue(optional_character):.3g}/{self.getMaxValue(optional_character):.3g}"
            + f"{'%' if '%' in self.description else ''}"
            + f"{self.description.replace('+{', '').replace('%', '')}"
        )
        return result

    def getAdvice(self, optional_starting_note='', optional_ending_note='', optional_character: Character=None):
        a = Advice(
            label=f"{optional_starting_note}{' ' if optional_starting_note else ''}{self.cardset}- {self.name} card:<br>{self.getFormattedXY(optional_character)}"
                  f"{'<br>' if optional_ending_note else ''}{optional_ending_note}",
            picture_class=self.css_class,
            progression=self.level,
            goal=self.max_level,
        )
        return a

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
        for skullValue in dn_skull_value_list:
            self.lowest_skulls_dict[skullValue] = []
        if len(mapsdict) > 0:
            for enemy_map_index in self.maps_dict:
                self.lowest_skulls_dict[self.maps_dict[enemy_map_index].skull_mk_value].append(
                    [self.maps_dict[enemy_map_index].map_name,
                     self.maps_dict[enemy_map_index].kills_to_next_skull,
                     self.maps_dict[enemy_map_index].percent_toward_next_skull,
                     self.maps_dict[enemy_map_index].monster_image,
                     self.maps_dict[enemy_map_index].kill_count],
                )
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
    def __init__(
            self, mapname: str,
            monstername: str,
            mapindex: int,
            portalrequirement: int,
            zowrating: str,
            chowrating: str,
            meowrating: str,
            wowrating: str,
            monsterimage: str = ""
    ):
        self.map_name: str = mapname
        self.map_index: int = mapindex
        self.monster_name: str = monstername
        self.portal_requirement: int = portalrequirement
        self.zow_rating: str = zowrating
        self.chow_rating: str = chowrating
        self.meow_rating: str = meowrating
        self.wow_rating: str = wowrating
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
        elif ratingType == 'WOW':
            return self.wow_rating
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
            print(f"models.EnemyMap.addRawKLA()~ Unable to add additionalKills value of {type(additionalKills)} {additionalKills} to {self.map_name} because: {reason}")
            #logger.warning(f"Unable to add additionalKills value of {type(additionalKills)} {additionalKills} to {self.map_name} because: {reason}")

    def generateDNSkull(self):
        self.kill_count = int(self.kill_count)
        for counter in range(0, len(dn_skull_requirement_list)):
            if self.kill_count >= dn_skull_requirement_list[counter]:
                self.skull_mk_value = dn_skull_value_list[counter]
        self.skull_name = getSkullNames(self.skull_mk_value)
        if self.skull_mk_value == reversed_dn_skull_value_list[0]:
            #If map's skull is highest, currently Eclipse Skull, set in defaults
            self.kills_to_next_skull = 0
            self.percent_toward_next_skull = 100
        else:
            for skullValueIndex in range(1, len(reversed_dn_skull_value_list)):
                if self.skull_mk_value == reversed_dn_skull_value_list[skullValueIndex]:
                    self.kills_to_next_skull = ceil(reversed_dn_skull_requirement_list[skullValueIndex - 1] - self.kill_count)
                    self.percent_toward_next_skull = floor(round(self.kill_count / reversed_dn_skull_requirement_list[skullValueIndex - 1] * 100))

def buildMaps() -> dict[int, dict]:
    mapDict = {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {},
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
        #mapData[7]: str = wow rating
        #mapData[8]: str = image
        if mapData[1] in apocable_map_index_dict[0]:
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
            wowrating=mapData[7],
            monsterimage=mapData[8]
        )
    return mapDict


@session_singleton
class Account:

    def __init__(self, json_data, source_string: InputType):
        self.raw_data = safe_loads(json_data)
        self.version = safer_get(self.raw_data, 'DoOnceREAL', 0.00)
        if self.version < 297:  # 297.x was the W7 release patch
            raise VeryOldDataException(self.version)
        self.data_source = source_string.value
        self.alerts_Advices = {
            'General': [],
            'World 1': [],
            'World 2': [],
            'World 3': [],
            'World 4': [],
            'World 5': [],
            'The Caverns Below': [],
            'World 6': []
        }
        #General
        self.inventory = {
            'Characters Missing Bags': {},
            'Account Wide Inventory': {},
            'Account Wide Inventory Slots Owned': 0,
            'Account Wide Inventory Slots Max': 0,
        }
        self.storage = {
            'Used Chests': [],
            'Used Chests Slots': 0,
            'Missing Chests': [],
            'Missing Chests Slots': 0,
            'Other Storage': {},
            'Other Slots Owned': 0,
            'Other Slots Max': 0,
            'Total Slots Owned': 0,
            'Total Slots Max': 0
        }
