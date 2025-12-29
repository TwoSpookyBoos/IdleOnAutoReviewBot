from consts.consts_w2 import get_obol_totals, po_box_dict, alchemy_jobs_list
from consts.consts_w3 import prayers_dict, apoc_names_list
from consts.consts_w4 import lab_chips_dict
from consts.consts_w5 import divinity_divinities_dict
from consts.idleon.consts_idleon import current_world, expected_talents_dict
from consts.idleon.lava_func import lava_func
from models.general.equipment import Equipment
from utils.number_formatting import parse_number
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)

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
                    'Bonus1Value': lava_func(
                        poBoxValues['1_funcType'],
                        po_boxes[poBoxIndex],
                        poBoxValues['1_x1'],
                        poBoxValues['1_x2'],
                    ),
                    'Bonus1String': '',
                    'Bonus2Value': lava_func(
                        poBoxValues['2_funcType'],
                        po_boxes[poBoxIndex] - poBoxValues['2_minCount'],
                        poBoxValues['2_x1'],
                        poBoxValues['2_x2'],
                    ) if po_boxes[poBoxIndex] >= poBoxValues['2_minCount'] else 0,
                    'Bonus2String': '',
                    'Bonus3Value': lava_func(
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
                            enemies, key=lambda item: item[1], reverse=True
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
