from math import ceil, floor

from consts.consts_autoreview import ValueToMulti
from consts.consts_general import inventory_bags_dict, specialized_skills_dict
from consts.consts_w2 import alchemy_jobs_list, get_obol_totals, po_box_dict
from consts.consts_w3 import prayers_dict
from consts.consts_w4 import lab_chips_dict
from consts.consts_w5 import divinity_divinities_dict
from consts.idleon.consts_idleon import expected_talents_dict
from consts.idleon.lava_func import lava_func
from consts.general.equipment import (
    equip_slot_chip_doublers,
    equip_slot_count,
    gallery_slot_indexes,
    gallery_unlock_kills_index,
    gown_slot_index,
    hatrack_slot_index,
    hatrack_unlock_kills_index,
    tool_slot_count,
)
from consts.general.talents import (
    talent_bonus_banned_above,
    talent_bonus_banned_indexes,
    talent_bonus_banned_range,
)
from models.general.equipment import Equipment
from models.w2.post_office import PostOfficeBox
from models.w3.apocalypse import ApocProgress, new_apocalypses
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.safer_data_handling import safer_index

logger = get_logger(__name__)


def talent_bonus_banned(talent_index: int) -> bool:
    low, high = talent_bonus_banned_range
    return (
        low <= talent_index <= high
        or talent_index in talent_bonus_banned_indexes
        or talent_index > talent_bonus_banned_above
    )


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
        equipped_star_signs: list[int] = None,
        active_talent_preset: int = 0
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
        self.arctis_bonus_max = 0
        self.timmy_talented_bonus = 0
        self.total_bonus_talent_levels: int = 0
        self.current_map_index = current_map_index
        self.max_talents: dict = max_talents
        self.current_preset_talents: dict = current_preset_talents
        self.secondary_preset_talents: dict = secondary_preset_talents
        # "PlayerStuff"[1] in source. Last updated in v2.531.0
        self.active_talent_preset: int = active_talent_preset
        self.active_super_talents: set[int] = set()
        self.super_talent_levels: int = 0
        self.current_preset_talent_bar: dict = current_preset_talent_bar
        self.secondary_preset_talent_bar: dict = secondary_preset_talent_bar
        self.fix_talent_bars()
        self.specialized_skills: list[str] = get_specialized_skills(self.all_classes)
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

        self.po_boxes_invested: dict[str, PostOfficeBox] = {
            info['Name']: PostOfficeBox(info, safer_index(po_boxes, index, None))
            for index, info in po_box_dict.items()
        }
        self.equipped_lab_chips: list[str] = []
        for chipIndex in equipped_lab_chips:
            if chipIndex != -1:
                try:
                    self.equipped_lab_chips.append(lab_chips_dict[chipIndex]['Name'])
                except:
                    continue
        self.equipped_card_doublers: list[str] = self.get_card_doublers()

        self.apocalypses: dict[str, ApocProgress] = new_apocalypses()
        self.equipment = Equipment(raw_data, character_index, self.combat_level >= 1)

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

    def calculate_inventory_slots(self, account_wide_slots: int):
        self.inventory_slots = account_wide_slots
        for bag, slots in self.inventory_bags.items():
            if int(bag) == 112:
                continue  # 4th anniversary bag counts account wide
            if isinstance(slots, int | float | str):
                self.inventory_slots += parse_number(slots)
            else:
                logger.warning(
                    f"Funky bag value found in {self.character_index}'s bagsDict for bag {bag}: "
                    f"{type(slots)} {slots}. Searching for expected value."
                )
                if int(bag) in inventory_bags_dict:
                    logger.debug(f"Bag {bag} has a known value: {inventory_bags_dict[int(bag)]}. All is well :)")
                else:
                    logger.error(f"Bag {bag} has no known value. Defaulting to 0 :(")
                self.inventory_slots += inventory_bags_dict.get(int(bag), 0)

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

    def calculate_bonus_talent_levels(
        self,
        account_wide_bonus: int,
        arctis_linked: bool,
        big_p_value: float,
        coral_kid_level: float,
        timmy_talented: bool,
        max_book_level: int,
        es_family_value: float,
    ):
        # "OptLacc[430]" in source: Coral Kid boosts the Arctis minor link. Last updated in v2.531.0
        # "DivMinorBonus" in source: base 15 scaled by divinity level. Last updated in v2.531.0
        arctis_base = 15 * max(1, big_p_value) * ValueToMulti(round(coral_kid_level))
        divinity_minor = self.divinity_level / (self.divinity_level + 60)
        self.arctis_bonus_max = ceil(arctis_base * divinity_minor)
        character_bonus = self.arctis_bonus_max if arctis_linked else 0

        # "AllTalentLV" in source. Last updated in v2.531.0
        if timmy_talented:
            self.timmy_talented_bonus = max(0, floor((self.combat_level - 500) / 100))
        character_bonus += self.timmy_talented_bonus

        # Symbols of Beyond: 1 + 1 per 20 levels of the elite's own copy
        symbols_level = 0
        if any(elite in self.all_classes for elite in ["Blood Berserker", "Divine Knight"]):
            symbols_level = self.max_talents.get("149", 0) // 20
        elif any(elite in self.all_classes for elite in ["Siege Breaker", "Beast Master"]):
            symbols_level = self.max_talents.get("374", 0) // 20
        elif any(elite in self.all_classes for elite in ["Elemental Sorcerer", "Bubonic Conjuror"]):
            symbols_level = self.max_talents.get("539", 0) // 20
        self.symbols_of_beyond = 1 + symbols_level if symbols_level > 0 else 0
        character_bonus += self.symbols_of_beyond

        self.total_bonus_talent_levels = account_wide_bonus + character_bonus
        self.max_talents_over_books = max_book_level + self.total_bonus_talent_levels

        # Family Guy: floor(ES Family value * Family Guy multi) extra levels
        if self.class_name == 'Elemental Sorcerer':
            family_guy_multi = ValueToMulti(lava_func(
                'decay', self.max_talents_over_books + self.max_talents.get('374', 0), 40, 100
            ))
            self.family_guy_bonus = floor(es_family_value * family_guy_multi) - floor(es_family_value)
            self.max_talents_over_books += self.family_guy_bonus

    def calculate_crystal_spawn_chance(self, account_wide: float, crescent_shrine_value: float):
        # Assumes Cmon Out Crystals is max booked
        cmon_out_crystals_multi = max(1, ValueToMulti(lava_func(
            'decay',
            self.max_talents_over_books if self.max_talents.get("26", 0) > 0 else 0,
            300,
            100
        )))
        crystals_4_dayys_multi = max(1, ValueToMulti(lava_func(
            'decay', self.max_talents.get("619", 0), 174, 50
        )))
        shrine_and_po = ValueToMulti(
            self.po_boxes_invested['Non Predatory Loot Box'].bonus_3_value + crescent_shrine_value
        )
        self.crystal_spawn_chance = account_wide * (
            shrine_and_po * cmon_out_crystals_multi * crystals_4_dayys_multi
        )

    def isArctisLinked(self):
        return 'Arctis' in [
            self.divinity_link, self.current_polytheism_link, self.secondary_polytheism_link
        ]

    # "CardBonusREAL" in source. Last updated in v2.531.0
    def get_equipped_card_bonus(
        self, description: str, flopping_multi: float = 1.0
    ) -> float:
        return flopping_multi * sum(
            card.getCurrentValue(optional_character=self)
            for card in self.equipped_cards
            if card.description == description
        )

    def get_bonus_levels(self, talent_index: int, bonus_cap: float = 9999) -> int:
        if talent_bonus_banned(talent_index):
            return 0
        return floor(min(bonus_cap, self.total_bonus_talent_levels))

    # "AllTalentLV" in source. Last updated in v2.531.0
    def get_talent_level(self, talent_index: int, bonus_cap: float = 9999) -> int:
        base = self.current_preset_talents.get(str(talent_index), 0)
        if base <= 0.5 or talent_bonus_banned(talent_index):
            return base
        # Super levels skip the cap; active preset only, unlike getbonus2
        super_levels = self.super_talent_levels * (
            talent_index in self.active_super_talents
        )
        return base + self.get_bonus_levels(talent_index, bonus_cap) + super_levels

    # "GetTalentNumber"(1, t) in source. Last updated in v2.531.0
    def get_talent_value(self, talent_index: int, bonus_cap: float = 9999) -> float:
        level = self.get_talent_level(talent_index, bonus_cap)
        talent = all_talentsDict.get(talent_index)
        if level <= 0 or talent is None:
            return 0
        return lava_func(talent['funcX'], level, talent['x1'], talent['x2'])

    def _kills_left(self, kills_index: int) -> float:
        return safer_index(self.kill_dict.get(kills_index, [1]), 0, 1)

    @property
    def gallery_bonus_active(self) -> bool:
        return self._kills_left(gallery_unlock_kills_index) <= 0

    @property
    def hatrack_bonus_active(self) -> bool:
        return self._kills_left(hatrack_unlock_kills_index) <= 0

    # Gear/tool part of "TotalStatsETCmap" in source. Last updated in v2.531.0
    def get_gear_misc_bonus(self, codename: str, gown_bonus: float) -> float:
        # Gallery/Hatrack take over their slots once open
        total = 0
        for slot in range(equip_slot_count):
            if self.gallery_bonus_active and slot in gallery_slot_indexes:
                continue
            if self.hatrack_bonus_active and slot == hatrack_slot_index:
                continue
            value = self.equipment.get_misc_bonus(slot, codename)
            if equip_slot_chip_doublers.get(slot) in self.equipped_lab_chips:
                value *= 2
            if slot == gown_slot_index and gown_bonus >= 1:
                value *= ValueToMulti(gown_bonus)
            total += value
        for slot in range(tool_slot_count):
            total += self.equipment.get_misc_bonus(slot, codename, tools=True)
        return total

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


def getExpectedTalents(classes_list):
    expectedTalents = []
    for className in classes_list:
        if className != 'None':
            try:
                expectedTalents.extend(expected_talents_dict[className])
            except:
                logger.warning(f"Failed to add expected talents for {className}")
                continue
    return expectedTalents


def get_specialized_skills(classes_list):
    specialized_skills_list = [specialized_skills_dict.get(class_name) for class_name in classes_list]
    return specialized_skills_list
