import json
from collections import defaultdict

import itemDecoder

from models import AdviceSection, AdviceGroup, Advice
from utils import get_logger
import itertools

logger = get_logger(__name__)

greenStackAmount = 10 ** 7
expectedStackables = {
    "Missable Quest Items": [
        "Quest3", "Quest4", "Quest7", "Quest12", "Quest21", "Quest14", "Quest22", "Quest23", "Quest24", "GoldricP1", "GoldricP2", "GoldricP3",
        "Quest32"
    ],
    "Base Monster Materials": [
        "Grasslands1", "Grasslands2", "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3", "Sewers1",
        "Sewers2", "TreeInterior1", "TreeInterior2",  # W1
        "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4",  # W2
        "SnowA1", "SnowA2", "SnowA3", "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4", "SnowA4", "SnowC5",
        # W3
        "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1", "GalaxyB2", "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2",
        "GalaxyC3", "GalaxyC4",  # W4
        "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5", "LavaB6", "LavaC1", "LavaC2",  # W5
        "SpiA1", "SpiA2", "SpiA3", "SpiA4", "SpiA5", "SpiB1", "SpiB2", "SpiB3", "SpiB4", "SpiC1", "SpiC2", "SpiD1", "SpiD2", "SpiD3", "Sewers3", "Quest15",  # W6
        "Hgg"  # Specialty Monster Materials
    ],
    "Crystal Enemy Drops": [
        "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1",  # W1
        "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2",  # W2
        "FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3",  # W3
        "FoodPotMana4", "Leaf4",  # W4
        "FoodPotYe5", "Leaf5",  # W5
        "Leaf6",  # W6
        "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",  # Standard statues
        "EquipmentStatues1", "EquipmentStatues5",  # Plausible but time consuming
        "rtt0", "StoneZ1", "StoneT1", "StoneW1", "StoneA1"  # W1 Slow drops
    ],
    "Printable Skilling Resources": [
        "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree",  # Tier1 Easy Logs
        "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",  # Tier1 Slow Ores
        "Fish1", "Fish2", "Fish3",  # Tier1 Fish
        "Bug1", "Bug2",  # Tier1 Bugs

        "PalmTree", "StumpTree", "SaharanFoal", "Tree7",  # Tier1 Slow Logs

        "AlienTree", "Tree8", "Tree9", "Tree11", "Tree10",  # Tier2 Logs
        "Starfire", "Marble", "Dreadlo",  # Tier2 Ores
        "Fish4", "Fish5", "Fish6", "Fish7", "Fish8",  # Tier2 Fish
        "Bug3", "Bug4", "Bug5", "Bug6", "Bug7", "Bug8",  # Tier2 Bugs
        "Fish9", "Fish10", "Fish11", "Fish13", "Fish12",  # Tier3 Fish
        "Bug9", "Bug11", "Bug10",  # Tier3 Bugs

        "Godshard",  # W6 Ore
        "Tree12", "Tree13",  # W6 Logs
        "Bug12", "Bug13",  # W6 Bugs
    ],
    "Other Skilling Resources": [
        "CraftMat1", "CraftMat5", "CraftMat6", "CraftMat7", "CraftMat8", "CraftMat9", "CraftMat10", "CraftMat11",  # Tier1, 2, and 3 Anvil
        "Critter1", "Critter2", "Critter3", "Soul1", "CopperBar",  # Tier3 Critters, Souls, Bars
        "CraftMat12", "CraftMat13", "Critter4", "Critter5", "Critter6", "Soul2", "IronBar",  # Tier4 Anvil, Critters, Souls, Bars
        "CraftMat14", "Critter7", "Critter8", "Soul3", "GoldBar",  # Tier5 Anvil, Critters, Souls, Bars
        "Critter9", "Critter10", "Soul4", "PlatBar", "FoodMining1", "FoodFish1", "FoodCatch1",  # Tier6 Critters, Souls, Bars, and Crafted
        "Soul5", "DementiaBar", "Peanut",  # Tier7 Souls, Bars, Crafted
        "Soul6", "VoidBar", "Bullet", "BulletB",  # Tier8 Souls, Bars, Crafted
        "Soul7", "LustreBar", "Quest68",  # Tier9 Bars, Crafted
        "StarfireBar", "Bullet3", "FoodChoppin1",  # Tier10 Bars, Crafted
        "DreadloBar", "EquipmentSmithingTabs2", "Refinery1",  # Tier11 Bars, Crafted, Salts
        "Critter1A", "Refinery2", "Critter2A", "Refinery3", "Critter3A", "Critter4A", "Critter5A", "Refinery4", "Critter6A", "Critter7A", "Critter8A",
        "Critter9A", "Critter10A"  # Tier12 Salts, Shiny Critters
    ],
    "Vendor Shops": [
        "FoodHealth14", "FoodHealth15", "FoodHealth16", "FoodHealth17", "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4",
        "FoodPotYe4", "OilBarrel6", "OilBarrel7", "FoodHealth4", "FoodHealth9", "FoodHealth11", "Quest19"  # Sorted by daily quantity
        # "FoodHealth4", "Quest19", #W2
        # "FoodHealth11", "FoodHealth9", "FoodPotGr3", #W3
        # "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4", #W4
        # "OilBarrel6", "FoodHealth14", "FoodHealth15", #W5 shop
        # "FoodHealth16", "FoodHealth17", "OilBarrel7", #W6 Shop
    ],
    "Misc": [
        "FoodPotMana3", "FoodPotGr3", "ButterBar", "FoodPotRe1", "FoodPotRe2",
    ],
    "W6 Probably": [
        "OilBarrel2",  # Slime Barrel, 1 in 3334
        "DesertC2b",  # Ghost, 1 in 2k
        "Quest78",  # Equinox Mirror
        "PureWater",  # First Alchemy water
        "FoodTrapping1", "FoodWorship1",  # Critter Numnums and Soulble Gum
        "PeanutG", "FoodG9",  # Golden Peanuts and Golden W5 Sammy
        "CraftMat3",  # Cue Tape
        "StoneT2", "StoneW2", "StoneA2", "StoneZ2",  # W2 upgrade stones and Mystery2
        "Key2", "Key3"  # Efaunt and Chizoar keys
    ],
    "Cheater": [
        "Sewers1b", "TreeInterior1b", "BabaYagaETC", "JobApplication",  # W1 Rare Drops
        "DesertA1b", "DesertA3b", "MidnightCookie",  # W2 Rare Drops
        "SnowA2a", "SnowB2a", "SnowC4a", "Quest78",  # W3 Rare Drops
        "GalaxyA2b", "GalaxyC1b",  # W4 Rare Drops
        "LavaA1b", "LavaA5b", "LavaB3b",  # W5 Rare Drops
        "SpiA2b", "SpiB2b",  # W6 Rare Drops
        "Quest17", "Quest29", "EfauntDrop1", "EfauntDrop2", "Chiz0", "Chiz1", "TrollPart", "KrukPart", "KrukPart2",  # World Boss Materials
        "CraftMat2",  # Crimson String
        "Refinery5", "Refinery6",  # Purple and Nullo Salts
        "OilBarrel1", "OilBarrel3", "OilBarrel4", "OilBarrel5",  # Oil Barrels
        "PureWater2",  # Alchemy Dense water
        "GodshardBar", "MarbleBar",
        "Quest1", "Quest2", "Quest5", "Quest6", "Quest8", "Quest10", "Quest11", "Quest13", "Quest16", "Quest17", "Quest18", "Quest20", "Quest25",
        "Quest26", "Quest27", "Quest28", "Quest29", "Quest30", "Quest31", "Quest33", "Quest34", "Quest36", "Quest37", "Quest38", "Quest39", "Quest40",
        "Quest41", "Quest42", "Quest43", "Quest44", "Quest45", "Quest46", "Quest47", "Quest48", "Quest49", "Quest50", "Quest9",
        "Mayo", "Trash", "Trash2", "Trash3",  # Treasure Hunt rewards
        "Meatloaf", "FoodHealth5", "FoodHealth8", "FoodPotYe3", "BobJoePickle", "BallJoePickle", "BoneJoePickle",
        "FoodPotYe1", "FoodPotYe3",  # EXP 1 and 3
        "FoodEvent1", "FoodEvent2", "FoodEvent3", "FoodEvent4", "FoodEvent5", "FoodEvent6", "FoodEvent7", "FoodEvent8",  # Event Foods
        "Pearl1", "Pearl2", "Pearl3", "Pearl4",
        "Pearl5", "Pearl6",  # Skilling Speed Pearls, EXP pearls
        "Line1", "Line2", "Line3", "Line4", "Line5", "Line6", "Line7", "Line8", "Line9", "Line10", "Line11", "Line12", "Line13", "Line14",  # Fishing Lines
        "ExpBalloon1", "ExpBalloon2", "ExpBalloon3",  # Experience Balloons
        "Timecandy1", "Timecandy2", "Timecandy3", "Timecandy4", "Timecandy5", "Timecandy6", "Timecandy7", "Timecandy8", "Timecandy9",  # Time Candies
        "SilverPen", "Ladle",
        "PetEgg", "Whetstone", "Quest72", "Quest73", "Quest76", "Quest77",  # Other Time Skips
        "Quest70", "Quest71", "Quest75",  # Loot Bags
        "Quest69", "Quest74",  # Unobtainables
        "EquipmentStatues6", "EquipmentStatues15",  # Kachow and Bullseye
        "EquipmentStatues8", "EquipmentStatues9", "EquipmentStatues10", "EquipmentStatues11", "EquipmentStatues12", "EquipmentStatues13",
        # W2 Statues
        "EquipmentStatues16", "EquipmentStatues17", "EquipmentStatues18", "EquipmentStatues19",  # W3 Statues
        "EquipmentStatues20", "EquipmentStatues21", "EquipmentStatues22", "EquipmentStatues23", "EquipmentStatues24",
        "EquipmentStatues25",  # W4 and W5 Statues
        "FoodG1", "FoodG2", "FoodG3", "FoodG4", "FoodG5", "FoodG6", "FoodG7", "FoodG8", "FoodG10", "Gfoodcoupon", # Gold Foods
        "ResetFrag", "ResetCompleted", "ResetCompletedS", "ClassSwap",
        "ClassSwapB", "ResetBox",
    ]
}
gstackable_codenames = [item for items in expectedStackables.values() for item in items]
gstackable_codenames_expected = [item for items in list(expectedStackables.values())[:-1] for item in items]

quest_items_codenames = expectedStackables["Missable Quest Items"]

missableGStacksDict = {
    #  ItemName               Codename     Quest Codeame          Quest Name                                          Wiki link to the item                             Recommended Class/Farming notes
    "Dog Bone":              ["Quest12",   "Dog_Bone1",           "Dog Bone: Why he Die???",                          "https://idleon.wiki/wiki/Dog_Bone",              "Active ES or time candy."],
    "Ketchup Bottle":        ["Quest3",    "Picnic_Stowaway2",    "Picnic Stowaway: Beating Up Frogs for some Sauce", "https://idleon.wiki/wiki/Ketchup_Bottle",        "Active ES or time candy."],
    "Mustard Bottle":        ["Quest4",    "Picnic_Stowaway2",    "Picnic Stowaway: Beating Up Frogs for some Sauce", "https://idleon.wiki/wiki/Mustard_Bottle",        "Active ES or time candy."],
    "Strange Rock":          ["Quest7",    "Stiltzcho2",          "Stiltzcho: No Stone Unturned",                     "https://idleon.wiki/wiki/Strange_Rock",          "Active ES or time candy."],
    "Time Thingy":           ["Quest21",   "Funguy3",             "Funguy: Partycrastination",                        "https://idleon.wiki/wiki/Time_Thingy",           "Active ES or time candy."],
    "Employment Statistics": ["Quest14",   "TP_Pete2",            "TP Pete: The Rats are to Blame!",                  "https://idleon.wiki/wiki/Employment_Statistics", "Active ES or time candy."],
    "Corporatube Sub":       ["Quest22",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Corporatube_Sub",       "Active ES or time candy."],
    "Instablab Follower":    ["Quest23",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Instablab_Follower",    "Active ES or time candy."],
    "Cloudsound Follower":   ["Quest24",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Cloudsound_Follower",   "Active ES or time candy."],
    "Casual Confidante":     ["GoldricP1", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Casual_Confidante",     "Active ES or time candy."],
    "Triumphant Treason":    ["GoldricP2", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Triumphant_Treason",    "Active ES or time candy."],
    "Claiming Cashe":        ["GoldricP3", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Claiming_Cashe",        "Active ES or time candy."],
    "Monster Rating":        ["Quest32",   "XxX_Cattleprod_XxX3", "XxX_Cattleprod_XxX: Ok, NOW it's Peak Gaming!",    "https://idleon.wiki/wiki/Monster_Rating",        "Monster Ratings can drop from Crystal enemies, making Divine Knight the better farmer for Monster Ratings."]
}


class Asset:
    def __init__(self, codename: str, amount: float, name: str = ""):
        self.name: str = name if name else itemDecoder.getItemDisplayName(codename)
        self.codename: str = codename if codename else itemDecoder.getItemCodeName(name)
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
    def __init__(self, assets: dict[str, int], tiers: dict[int, dict]):
        self.tiers = tiers
        super().__init__(tuple((codename, Asset(codename, count)) for codename, count in assets.items()))

    def get(self, item, default=None):
        return super().get(item, default if default else Asset(item, 0))

    @property
    def items_gstacked(self) -> dict[str, Asset]:
        """Not used since it includes the "Cheater" group"""
        return {asset.codename: asset for asset in self.values() if asset.greenstacked}

    @property
    def items_gstacked_expected(self) -> dict[str, Asset]:
        return {codename: asset for codename, asset in self.items_gstacked.items() if codename in gstackable_codenames}

    @property
    def items_gstacked_cheater(self) -> dict[str, Asset]:
        return {codename: asset for codename, asset in self.items_gstacked.items() if codename not in gstackable_codenames_expected}

    @property
    def items_gstacked_unprecedented(self) -> dict[str, Asset]:
        return {codename: asset for codename, asset in self.items_gstacked.items() if codename not in gstackable_codenames}

    @property
    def items_gstackable(self) -> dict[str, Asset]:
        """Not used since it includes the "Cheater" group"""
        return {codename: asset for codename, asset in self.items() if codename in gstackable_codenames and not asset.greenstacked}

    @property
    def items_gstackable_expected(self) -> dict[str, Asset]:
        return {codename: asset for codename, asset in self.items() if codename in gstackable_codenames_expected and not asset.greenstacked}

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
                    categorised[category] = item_list
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


def getEquinoxDreams(inputJSON) -> dict:
    try:
        rawDreams = json.loads(inputJSON["WeeklyBoss"])
    except Exception as reason:
        logger.error("Unable to access WeeklyBoss data from JSON: %s", reason)
        return dict(
            Dream1=False,
            Dream12=False,
            Dream29=False
        )

    results = dict(
        Dream1=rawDreams.get("d_0") == -1,
        Dream12=rawDreams.get("d_11") == -1,
        Dream29=rawDreams.get("d_28") == -1,
    )
    logger.debug("OUTPUT results: %s", results)

    return results


def all_owned_items(inputJSON: dict, playerCount: int, gstack_tiers: dict) -> Assets:
    name_quantity_key_pairs = tuple((f"InventoryOrder_{i}", f"ItemQTY_{i}") for i in range(playerCount)) + (("ChestOrder", "ChestQuantity"),)
    all_stuff_owned = defaultdict(int)

    for codename in gstackable_codenames:
        all_stuff_owned[codename] = 0

    for name_key, quantity_key in name_quantity_key_pairs:
        for name, count in zip(inputJSON[name_key], inputJSON[quantity_key]):
            all_stuff_owned[name] += count

    return Assets(all_stuff_owned, gstack_tiers)


def getMissableGStacks(inputJSON, playerCount, owned_stuff: Assets):
    advice_ObtainedQuestGStacks = owned_stuff.quest_items_gstacked
    advice_EndangeredQuestGStacks = list(owned_stuff.quest_items_gstackable)
    advice_MissedQuestGStacks = []

    quest_statuses_per_player = [json.loads(inputJSON.get(f"QuestComplete_{i}", "{}")) for i in range(playerCount)]
    quest_names = quest_statuses_per_player[0].keys()
    quest_completed = [
        name
        for name in quest_names
        if all(quests[name] == 1 for quests in quest_statuses_per_player)
        # Quest value one of (-1, 0, 1). -1 means not started.
    ]

    for quest_item in list(advice_EndangeredQuestGStacks):
        item_data = missableGStacksDict[quest_item.name]
        quest_codename = item_data[1]

        if quest_codename in quest_completed:
            quest_item.quest = item_data[2]
            advice_MissedQuestGStacks.append(quest_item)
            advice_EndangeredQuestGStacks.remove(quest_item)

    sections = list()

    note = (
        "These items are currently recommended for players trying to complete the "
        "endgame Equinox Dreams to collect 20, 75, and 200 greenstacks. If you're "
        "nowhere near that, don't worry about collecting them right away. Simply "
        "leave the quest uncompleted on your Wizard/Elemental Sorcerer and your "
        "Squire/Divine Knight to clean up later!"
    )

    if len(advice_ObtainedQuestGStacks) > 0:
        tier_obtained = f"{len(advice_ObtainedQuestGStacks)}/{len(missableGStacksDict)}"
        if len(advice_ObtainedQuestGStacks) == len(missableGStacksDict):
            header_obtained = f"You have obtained all {tier_obtained} missable quest item Greensacks! Way to go, you heap hoarder ❤️"
        else:
            header_obtained = f"You have obtained {tier_obtained} missable quest item Greenstacks"

        section_obtained = AdviceSection(
            name="Obtained Greenstacks",
            tier=tier_obtained,
            header=header_obtained,
            picture="Greenstack.png",
            note=note
        )
        # sections.append(section_obtained)

    if len(advice_EndangeredQuestGStacks) > 0:
        tier_obtainable = f"{len(advice_EndangeredQuestGStacks)}/{len(missableGStacksDict)}"
        header_obtainable = f"You can still obtain {tier_obtainable} missable quest item Greenstacks. Be sure <strong>NOT</strong> to turn in their quests until GStacking them:"
        sections.append(
            AdviceSection(
                name="Endangered Greenstacks",
                tier=tier_obtainable,
                header=header_obtainable,
                picture="Greenstack.png",
                note=note,
                groups=[
                    AdviceGroup(
                        tier="",
                        pre_string="",
                        advices=[
                            Advice(
                                label=item.name,
                                item_name=item.name,
                                progression=item.progression,
                                unit="%"
                            )
                            for item in advice_EndangeredQuestGStacks
                        ]
                    )
                ]
            )
        )

    if len(advice_MissedQuestGStacks) > 0:
        tier_missed = f"{len(advice_MissedQuestGStacks)}/{len(missableGStacksDict)}"
        header_missed = f"You have already missed {tier_missed} missable quest item Greenstacks. You're locked out of these until you get more character slots :("
        section_missed = AdviceSection(
            name="Missed Greenstacks",
            tier=tier_missed,
            header=header_missed,
            picture="Greenstack.png",
            note=note,
            groups=[
                AdviceGroup(
                    tier="",
                    pre_string="",
                    advices=[
                        Advice(
                            label=item.name,
                            item_name=item.name,
                            progression=item.quest,
                        )
                        for item in advice_MissedQuestGStacks
                    ]
                )
            ]
        )
        # sections.append(section_missed)

    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_ObtainedQuestGStacks:", advice_ObtainedQuestGStacks)
    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_EndangeredQuestGStacks:", advice_EndangeredQuestGStacks)
    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_MissedQuestGStacks:", advice_MissedQuestGStacks)

    return sections
    #return [advice_ObtainedQuestGStacks, advice_EndangeredQuestGStacks, advice_MissedQuestGStacks]


def setGStackProgressionTier(inputJSON, playerCount, progressionTiers):
    equinoxDreamsStatus = getEquinoxDreams(inputJSON)
    all_owned_stuff: Assets = all_owned_items(inputJSON, playerCount, progressionTiers)
    sections_quest_gstacks = getMissableGStacks(inputJSON, playerCount, all_owned_stuff)

    unprecedented_gstacks = all_owned_stuff.items_gstacked_unprecedented
    if unprecedented_gstacks:
        gstacks = [f"{gstack.name} ({gstack.codename})" for gstack in unprecedented_gstacks.values()]
        logger.warning('Unexpected GStack(s): %s', gstacks)

    #Get count of max expected gstacks
    expectedStackablesCount = len(set(gstackable_codenames_expected))
    expectedGStacksCount = len(all_owned_stuff.items_gstacked_expected)
    remainingToDoGStacksByTier = all_owned_stuff.items_gstackable_tiered

    groups = list()
    for tier, categories in remainingToDoGStacksByTier.items():
        tier_subsection = {
            category: [
                Advice(
                    label=item.name,
                    item_name=item.name,
                    progression=item.progression,
                    unit="%"
                ) for item in items
            ]
            for category, items in categories.items()
        }
        groups.append(
            AdviceGroup(
                tier=str(tier),
                pre_string="",
                advices=tier_subsection
            )
        )

    cheat_group = AdviceGroup(
        tier="",
        pre_string="Curious... you also managed to greenstack these unprecedented items:",
        post_string="Share your unyielding persistence with us, please!",
        advices=[
            Advice(
                label=name,
                item_name=name
            )
            for name, item in all_owned_stuff.items_gstacked_unprecedented.items()
        ]
    )
    groups.append(cheat_group)

    tier = f"{expectedGStacksCount} out of max (realistic) {expectedStackablesCount}"
    header = f"You currently have {tier} GStacks."
    show_limit = len(groups)
    if expectedGStacksCount >= 200 or equinoxDreamsStatus["Dream29"] == True:
        header += " You best ❤️ (until Lava adds further Dream tasks) Other possible targets are still listed below."
        show_limit = 4
    elif expectedGStacksCount >= 75 or equinoxDreamsStatus["Dream12"] == True:
        header += " Equinox Dream 29 requires 200. Aim for items up through Tier 10! There are a few extras included for flexibility."
        show_limit = 3
    elif expectedGStacksCount >= 20 or equinoxDreamsStatus["Dream1"] == True:
        header += " Equinox Dream 12 requires 75. Aim for items up through Tier 2! There are a few extras included for flexibility."
        show_limit = 2
    elif expectedGStacksCount < 20 and equinoxDreamsStatus["Dream1"] == False:
        header += " Equinox Dream 1 requires 20. Aim for items in Tier 1! There are a few extras included for flexibility."
        show_limit = 2

    for group in groups[show_limit:]:
        group.hide = True

    section_regular_gstacks = AdviceSection(
        name="Greenstacks",
        tier=tier,
        header=header,
        picture="Greenstack.png",
        groups=groups
    )

    return sections_quest_gstacks, section_regular_gstacks
