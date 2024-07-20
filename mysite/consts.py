import math
from utils.logging import get_logger
from utils.text_formatting import getItemDisplayName

logger = get_logger(__name__)

###GENERAL PROGRESSION TIERS###
combatLevels_progressionTiers = [
    # int tier, int TotalAccountLevel, str TAL reward, int PlayerLevels, str PL reward, str notes
    [0, 0, "", 0, "", ""],
    [1, 8, "Character 2",
     25, "Personal - Circle Obol Slot 2", ""],
    [2, 30, "Character 3",
     32, "Personal - Square Obol Slot 1", ""],
    [3, 60, "Family - Circle Obol Slot 1",
     40, "Personal - Circle Obol Slot 3", ""],
    [4, 70, "Character 4 and Family - Circle Obol Slot 1",
     48, "Personal - Circle Obol Slot 4", ""],
    [5, 80, "Family - Circle Obol Slot 2",
     60, "Personal - Square Obol Slot 2", ""],
    [6, 100, "Family - Circle Obol Slot 3",
     70, "Personal - Circle Obol Slot 5", ""],
    [7, 150, "Character 5",
     80, "Personal - Circle Obol Slot 6", ""],
    [8, 160, "Family - Circle Obol Slot 4",
     90, "Personal - Square Obol Slot 3", ""],
    [9, 200, "Family - Square Obol Slot 1",
     98, "Personal - Circle Obol Slot 7", ""],
    [10, 250, "Family - Circle Obol Slot 5",
     105, "Personal - Hexagon Obol Slot 1", ""],
    [11, 300, "Character 6",
     112, "Personal - Circle Obol Slot 8", ""],
    [12, 350, "Family - Circle Obol Slot 6",
     120, "Personal - Square Obol Slot 4", ""],
    [13, 400, "Family - Circle Obol Slot 7 and Family - Hexagon Obol Slot 1",
     130, "Personal - Circle Obol Slot 9", ""],
    [14, 470, "Family - Circle Obol Slot 8",
     140, "Personal - Square Obol Slot 5", ""],
    [15, 500, "Character 7",
     150, "Vman Quest, if class = Mman", ""],
    [16, 650, "Family - Sparkle Obol Slot 1",
     152, "Personal - Circle Obol Slot 10", ""],
    [17, 700, "Family - Square Obol Slot 2",
     170, "Personal - Circle Obol Slot 11", ""],
    [18, 750, "Character 8",
     180, "Personal - Hexagon Obol Slot 2", ""],
    [19, 875, "Family - Circle Obol Slot 9",
     190, "Personal - Square Obol Slot 6", ""],
    [20, 900, "Family - Hexagon Obol Slot 2",
     210, "Personal - Circle Obol Slot 12", ""],
    [21, 1100, "Character 9",
     250, "Personal - Sparkle Obol Slot 1 and Credit towards Equinox Dream 11", ""],
    [22, 1150, "Family - Square Obol Slot 3",
     425, "Able to equip The Divine Scarf", ""],
    [23, 1200, "Family - Sparkle Obol Slot 2",
     450, "Able to equip One of the Divine Trophy", ""],
    [24, 1250, "Family - Circle Obol Slot 10",
     500, "Credit towards Equinox Dream 23", ""],
    [25, 1500, "Character 10 and Family - Circle Obol Slot 11",
     500, "Credit towards Equinox Dream 23", ""],
    [26, 1750, "Family - Hexagon Obol Slot 3",
     500, "Credit towards Equinox Dream 23", ""],
    [27, 2000, "Family - Square Obol Slot 4",
     500, "Credit towards Equinox Dream 23",  ""],
    [28, 2100, "Family - Circle Obol Slot 12",
     500, "Credit towards Equinox Dream 23", ""],
    [29, 2500, "Family - Sparkle Obol Slot 3",
     500, "Credit towards Equinox Dream 23", ""],
    [30, 3000, "Family - Hexagon Obol Slot 4",
     500, "Credit towards Equinox Dream 23", ""],
    [31, 5000, "Family - Sparkle Obol Slot 4",
     500, "Credit towards Equinox Dream 23", ""],
    [32, 5300, "Unlock all Tome challenges",
     500, "Credit towards Equinox Dream 23", ""]
]
gemShop_progressionTiers = [
    # int tier, str tierName, dict recommendedPurchases, str notes
    [0, "", {}, ""],
    [1, "SS", {
        'Infinity Hammer': 1, 'Bleach Liquid Cauldrons': 1, 'Crystal 3d Printer': 1, 'Richelin Kitchen': 1, 'Golden Sprinkler': 1, 'Instagrow Generator': 1},
     "These are the highest priority as 1st purchase per world."
     ],
    [2, "S", {
        'Extra Card Slot': 4, 'Brimstone Forge Slot': 1},
     ""],
    [3, "A", {
        'Item Backpack Space': 1, 'Storage Chest Space': 4, 'Carry Capacity': 2, 'Weekly Dungeon Boosters': 1,
        'Brimstone Forge Slot': 4, 'Bleach Liquid Cauldrons': 2, 'Zen Cogs': 2, 'Tower Building Slots': 1,
        'Royal Egg Cap': 3, 'Richelin Kitchen': 3, 'Souped Up Tube': 1,
        'Chest Sluggo': 2, 'Divinity Sparkie': 2, 'Lava Sprouts': 2,
        'Instagrow Generator': 3, 'Shroom Familiar': 1, 'Plot of Land': 2},
     ""],
    [4, "B", {
        'Item Backpack Space': 2, 'Storage Chest Space': 8, 'Carry Capacity': 4, 'Weekly Dungeon Boosters': 2, 'Food Slot': 1,
        'Bleach Liquid Cauldrons': 3, 'More Sample Spaces': 2, 'Zen Cogs': 4, 'Tower Building Slots': 2,
        'Royal Egg Cap': 5, 'Fenceyard Space': 2, 'Chest Sluggo': 6, 'Lava Sprouts': 4,
        'Plot of Land': 4, 'Instagrow Generator': 5},
     ""],
    [5, "C", {
        'Item Backpack Space': 3, 'Storage Chest Space': 12, 'Carry Capacity': 6, 'Weekly Dungeon Boosters': 3, 'Food Slot': 2,
        'Bleach Liquid Cauldrons': 4, 'More Sample Spaces': 4, 'Burning Bad Books': 2, 'Tower Building Slots': 4,
        'Fenceyard Space': 4, 'Chest Sluggo': 9, 'Golden Sprinkler': 2, 'Lava Sprouts': 6,
        'Plot of Land': 6, 'Shroom Familiar': 2, 'Instagrow Generator': 7},
     ""],
    [6, "D", {
        'Item Backpack Space': 4, 'Carry Capacity': 8, 'More Storage Space': 5, 'Brimstone Forge Slot': 8,
        'Ivory Bubble Cauldrons': 4, 'Obol Storage Space': 3, 'More Sample Spaces': 6, 'Burning Bad Books': 4, 'Zen Cogs': 8,
        'Souped Up Tube': 3, 'Fenceyard Space': 6, 'Chest Sluggo': 12,
        'Plot of Land': 8, 'Instagrow Generator': 8,},
     ""],
    [7, "Practical Max", {
        'Item Backpack Space': 6, 'Carry Capacity': 10, 'More Storage Space': 10, 'Card Presets': 1,
        'Brimstone Forge Slot': 16, 'Sigil Supercharge': 10,
        'Fluorescent Flaggies': 2,
        'Golden Sprinkler': 4,
        'Plot of Land': 12, 'Shroom Familiar': 3,
    },
     "I wouldn't recommend going any further as of v2.02. This tier is for the dedicated Gem Farmers from Colo and Normal-difficulty World Bosses."],
    [8, "True Max",
     {
        #Inventory and Storage
        'Item Backpack Space': 6, 'Storage Chest Space': 12, 'Carry Capacity': 10, 'Food Slot': 2, 'More Storage Space': 10, 'Card Presets': 5,
        #Dailies N' Resets
        'Daily Teleports': 10, 'Daily Minigame Plays': 4,
        #Cards
        'Extra Card Slot': 4,
        #Goods & Services
        'Weekly Dungeon Boosters': 11,
        #World 1&2
        'Infinity Hammer': 1, 'Brimstone Forge Slot': 16, 'Ivory Bubble Cauldrons': 4, 'Bleach Liquid Cauldrons': 4,
        'Obol Storage Space': 12, 'Sigil Supercharge': 10,
        #World 3
        'Crystal 3d Printer': 1, 'More Sample Spaces': 6, 'Burning Bad Books': 4, 'Prayer Slots': 4,
        'Zen Cogs': 8, 'Cog Inventory Space': 20, 'Tower Building Slots': 4, 'Fluorescent Flaggies': 6,
        #World 4
        'Royal Egg Cap': 5, 'Richelin Kitchen': 10, 'Souped Up Tube': 5, 'Pet Storage': 12, 'Fenceyard Space': 6,
        #World 5
        'Chest Sluggo': 12, 'Divinity Sparkie': 6, 'Golden Sprinkler': 4, 'Lava Sprouts': 6,
        #World 6
        'Plot of Land': 12, 'Shroom Familiar': 3, 'Instagrow Generator': 8,
     },
     "This final tier is for the truly depraved. Many of these bonuses are very weak or outright useless."]
]
greenstack_progressionTiers = {
        0: {  # The timegated tier
            "Vendor Shops": [
                "CraftMat3",  # W1 Cue Tape
                "FoodHealth4", "Quest19",  # W2 Saucy Weiner and Gold Dubloon
                "FoodHealth9", "FoodHealth11",  #W3
                "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4",  #W4
                "FoodHealth14", "FoodHealth15", "OilBarrel6",  #W5
                "FoodHealth16", "FoodHealth17", "OilBarrel7",  #W6
            ],
            "Misc": [
                "FoodPotGr3",  # Previously Tier10
                "FoodPotRe2"   # Previously Tier11.
            ],
            "Other Skilling Resources": [
                "Refinery1", "Refinery2", "Refinery3", "Refinery4", "Refinery5", "Refinery6"],
        },
        1: {
            "Printable Skilling Resources": [
                "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", "PalmTree", "StumpTree", "SaharanFoal",
                "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",
                "Fish1", "Fish2", "Fish3",
                "Bug1", "Bug2"],
            },
        2: {
            "Printable Skilling Resources": [
                "Tree7", "AlienTree", "Tree8", "Tree9", "Tree11",
                "Starfire", "Marble",
                "Fish4", "Fish5", "Fish6", "Fish7",
                "Bug3", "Bug4", "Bug5", "Bug6", "Bug7", "Bug8"],
            "Other Skilling Resources": [
                "CraftMat1",],
            "Vendor Shops": [
                "FoodHealth14", "FoodHealth15",]
            },
        3: {
            "Base Monster Materials": [
                "Grasslands1", "Grasslands2", "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3",],
            "Printable Skilling Resources": [
                "Tree10",
                "Dreadlo",
                "Fish8", "Fish9", "Fish10",
                "Bug9", "Bug11"],
            "Other Skilling Resources": [
                "CraftMat5",],
            "Vendor Shops": [
                "FoodHealth12", "FoodHealth13",],
            },
        4: {
            "Base Monster Materials": [
                "Sewers1", "Sewers2", "TreeInterior1", "TreeInterior2",],
            "Printable Skilling Resources": [
                "Tree12",
                "Godshard",
                "Fish11", "Fish12", "Fish13",
                "Bug12", "Bug13",],
            "Other Skilling Resources": [
                "CraftMat6", "Soul1",],
            "Vendor Shops": [
                "FoodHealth16", "FoodHealth17",
                "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4",]
            },
        5: {
                "Base Monster Materials": [
                    "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4",
                    "SnowA1", "SnowA2", "SnowA3",],
                "Printable Skilling Resources": [
                    "Tree13",],
                "Other Skilling Resources": [
                    "CraftMat7", "CraftMat9",
                    "Critter1", "Critter2",
                    "Soul2",],
            },
        6: {
            "Base Monster Materials": [
                "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4",
                "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1", "GalaxyB2", ],
            "Other Skilling Resources": [
                "CraftMat8", "CraftMat10",
                "Critter3", "Critter4",
                "Soul3",]
            },
        7: {
            "Base Monster Materials": [
                "SnowA4", "SnowC5",
                "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2", "GalaxyC3",],
            "Crystal Enemy Drops": [
                "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1"],
            "Other Skilling Resources": [
                "CraftMat11",
                "Critter5",
                "Soul4",],
            },
        8: {
            "Base Monster Materials": [
                "GalaxyC4",
                "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5"],
            "Crystal Enemy Drops": [
                "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2",],
            "Other Skilling Resources": [
                "CraftMat12",
                "Critter6", "Critter7",
                "Soul5",],
            },
        9: {
            "Base Monster Materials": [
                "LavaB6", "LavaC1", "LavaC2",  #Can beat Kruk and move to W6 without fighting these
                "SpiA1", "SpiA2", "SpiA3", "SpiA4", "SpiA5", "SpiB1", "SpiB2", "SpiB3",],
            "Crystal Enemy Drops": [
                "FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3"],
            "Other Skilling Resources": [
                "CraftMat13", "CraftMat14",
                "Critter8", "Critter9",
                "Soul6",],
            },
        10: {
            "Base Monster Materials": [
                "SpiB4", "SpiC1", "SpiC2", "SpiD1", "SpiD2", "SpiD3",],
            "Crystal Enemy Drops": [
                "FoodPotMana4", "Leaf4",
                "FoodPotYe5", "Leaf5",
                "Leaf6",],
            "Printable Skilling Resources": [],
            "Other Skilling Resources": [
                "Critter10", "Critter11",
                "Soul7",
                "CopperBar", "IronBar",
                "FoodMining1", "FoodFish1", "FoodCatch1", "Bullet", "BulletB",],
            "Vendor Shops": [
                "OilBarrel6", "OilBarrel7",],
            },
        11: {
            "Missable Quest Items": [
                "Quest3", "Quest4", "Quest7", "Quest12"
                "Quest14", "Quest22", "Quest23", "Quest24",
                "Quest32",
            ],
            "Other Skilling Resources": [
                "PlatBar",

            ],
            },
        12: {
            "Missable Quest Items": ["GoldricP1", "GoldricP2", "GoldricP3", "Quest21"],
            "Base Monster Materials": ["Sewers3"],
            "Crystal Enemy Drops": [
                "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",
                "rtt0", "StoneZ1", "StoneT1",],  #W1 Tool in particular drops from both W1 and W2 crystal farms
            "Other Skilling Resources": [
                "GoldBar", "DementiaBar", "VoidBar", "LustreBar",
                "Peanut", "Quest68", "Bullet3",],  #I really hate that the Slush Bucket is listed as Quest68
            },
        13: {
            "Base Monster Materials": [
                "Quest15"],
            "Crystal Enemy Drops": [
                "EquipmentStatues1", "EquipmentStatues5",  #Power and Health statues are still more common than W2 statues
                "EquipmentStatues10", "EquipmentStatues12", "EquipmentStatues13", "EquipmentStatues8", "EquipmentStatues11",  #W2 statues
                "StoneA1", "StoneW1",
                "StoneZ2", "StoneT2",
                "PureWater",
                "FoodG9",],
            "Other Skilling Resources": [
                "StarfireBar",
                "FoodChoppin1",
                "EquipmentSmithingTabs2",
                "PeanutG",],
            "Misc": [
                "FoodPotMana3", "FoodPotRe1", "ButterBar", ],
        },
        14: {
            "Base Monster Materials": [
                "Hgg"],
            "Crystal Enemy Drops": [
                "StoneW2", "SilverPen"],  #"StoneA2",],
            "Other Skilling Resources": [
                "DreadloBar", "MarbleBar", "GodshardBar",
                "FoodTrapping1", "FoodWorship1",
                "Critter1A", "Critter2A", "Critter3A", "Critter4A", "Critter5A", "Critter6A", "Critter7A", "Critter8A", "Critter9A", "Critter10A", "Critter11A",
                "Ladle",
            ],
            "Misc": [
                "OilBarrel2", "DesertC2b", "Quest78",
            ]
        },
    }

###WORLD 1 PROGRESSION TIERS###
bribes_progressionTiers = [
        #int tier, int w1purchased, int w2purchased, int w3purchased, int w4purchased, int trashIslandpurchased, int w6purchased
        [0, 0, -7, -7, -6, -7, -8],
        [1, 6, -7, -7, -6, -7, -8],
        [2, 6, 7, -7, -6, -7, -8],
        [3, 6, 7, 7, -6, -7, -8],
        [4, 6, 7, 7, 6, -7, -8],
        [5, 6, 7, 7, 6, 7, -8],  #The 8th bribe in w5 cannot be purchased until Jade Emporium
        [6, 6, 7, 7, 6, 7, 7, ]  #The 7th bribe in w6 can't be purchased yet
]
stamps_progressionTiers = {
    # int Tier, int Total Stamp Level, list[int] Required combat stamps, list[int] Required Skill stamps, list[int] Required Misc stamps,
    # dict Specific stamp levels, list IgnorableStamps
    0: {"TotalStampLevels": 0, "Stamps": {}},
    1: {"TotalStampLevels": 50, "Stamps": {}},
    2: {"TotalStampLevels": 100, "Stamps": {}},
    3: {"TotalStampLevels": 150, "Stamps": {
        "Combat": ["Mana Stamp", "Tomahawk Stamp", "Target Stamp", "Shield Stamp", "Vitality Stamp"],
        "Skill": ["Choppin' Bag Stamp"],
        "Misc": ["Vendor Stamp"]}},
    4: {"TotalStampLevels": 200, "Stamps": {
        "Combat": ["Fist Stamp", "Manamoar Stamp"],
        "Skill": ["Lil' Mining Baggy Stamp", "Fishing Rod Stamp", "Catch Net Stamp"],
        "Misc": ["Talent S Stamp"],
        "Optional": ["Clover Stamp"]}},
    5: {"TotalStampLevels": 250, "Stamps": {
        "Combat": ["Longsword Stamp", "Battleaxe Stamp"],
        "Skill": ["Anvil Zoomer Stamp", "Matty Bag Stamp"],
        "Misc": ["Questin Stamp"],
        "Specific": {'Pickaxe Stamp': 25, 'Hatchet Stamp': 25},
        "Optional": ["Kapow Stamp"]}},
    6: {"TotalStampLevels": 300, "Stamps": {
        "Combat": ["Feather Stamp", "Polearm Stamp", "Buckler Stamp"],
        "Skill": ["Purp Froge Stamp"], "MiscStamps": ["Potion Stamp"]}},
    7: {"TotalStampLevels": 400, "Stamps": {
        "Specific": {'Pickaxe Stamp': 35, 'Hatchet Stamp': 35}}},
    8: {"TotalStampLevels": 500, "Stamps": {
        "Combat": ["Scimitar Stamp", "Bullseye Stamp", ],
        "Skill": ["Drippy Drop Stamp"],
        "Misc": ["Biblio Stamp"],
        "Specific": {'Drippy Drop Stamp': 30},
        "Optional": ["Hermes Stamp", "Fishhead Stamp", "Talent III Stamp"]}},
    9: {"TotalStampLevels": 600, "Stamps": {
        "Combat": ["Stat Graph Stamp"],
        "Skill": ["High IQ Lumber Stamp"],
        "Misc": ["Mason Jar Stamp", "Crystallin"],
        "Specific": {'Mason Jar Stamp': 12}}},
    10: {"TotalStampLevels": 700, "Stamps": {
        "Skill": ["Twin Ores Stamp", "Duplogs Stamp", "Cool Diggy Tool Stamp", "Swag Swingy Tool Stamp", "Alch Go Brrr Stamp",
                  "Droplots Stamp", "Bugsack Stamp", "Hidey Box Stamp", "Spikemouth Stamp"],
        "Specific": {'Drippy Drop Stamp': 40, 'Matty Bag Stamp': 50}}},
    11: {"TotalStampLevels": 800, "Stamps": {
         "Skill": ["Stample Stamp", "Spice Stamp", "Egg Stamp"],
         "Misc": ["Sigil Stamp"],
         "Specific": {'Pickaxe Stamp': 45, 'Hatchet Stamp': 45, 'Mason Jar Stamp': 24}}},
    12: {"TotalStampLevels": 900, "Stamps": {
        "Skill": ["Brainstew Stamp", "Bag o Heads Stamp", "Skelefish Stamp"],
        "Misc": ["Card Stamp"],
        "Specific": {'Drippy Drop Stamp': 50},
        "Optional": ["Saw Stamp"]}},
    13: {"TotalStampLevels": 1000, "Stamps": {
        "Skill": ["Holy Mackerel Stamp", "Cooked Meal Stamp"],
        "Specific": {'Pickaxe Stamp': 55, 'Hatchet Stamp': 55, 'Card Stamp': 50},
        "Optional": ["Agile Stamp", "Book Stamp", "Fly Intel Stamp", "Talent II Stamp"]}},
    14: {"TotalStampLevels": 1500, "Stamps": {
        "Combat": ["Avast Yar Stamp"],
        "Skill": ["Banked Pts Stamp", "Nest Eggs Stamp"],
        "Misc": ["Holy Mackerel Stamp"],
        "Specific": {'Matty Bag Stamp': 100, 'Crystallin': 60},
        "Optional": ["Arcane Stamp"]}},
    15: {"TotalStampLevels": 2000, "Stamps": {
        "Skill": ["Lab Tube Stamp"],
        "Misc": ["Golden Apple Stamp"],
        "Specific": {'Pickaxe Stamp': 65, 'Hatchet Stamp': 65, 'Card Stamp': 100},
        "Optional": ["Gilded Axe Stamp", "DNA Stamp"]}},
    16: {"TotalStampLevels": 2500, "Stamps": {
        "Combat": ["Blackheart Stamp"],
        "Skill": ["Ladle Stamp", "Sailboat Stamp"],
        "Misc": ["Talent III Stamp"],
        "Specific": {'Golden Apple Stamp': 28}}},
    17: {"TotalStampLevels": 3000, "Stamps": {
        "Combat": ["Steve Sword", "Diamond Axe Stamp"],
        "Skill": ["Gamejoy Stamp", "Divine Stamp"],
        "Specific": {'Bugsack Stamp': 80, 'Bag o Heads Stamp': 80}}},
    18: {"TotalStampLevels": 3500, "Stamps": {
        "Combat": ["Sashe Sidestamp"],
        "Specific": {'Pickaxe Stamp': 75, 'Hatchet Stamp': 75, 'Drippy Drop Stamp': 90, 'Crystallin': 100}}},
    19: {"TotalStampLevels": 4000, "Stamps": {
        "Specific": {'Matty Bag Stamp': 150}}},
    20: {"TotalStampLevels": 4500, "Stamps": {
        "Skill": ["Crop Evo Stamp"],
        "Misc": ["Multikill Stamp"],
        "Specific": {'Card Stamp': 150, 'Ladle Stamp': 100, 'Potion Stamp': 20},
        "Optional": ["Void Sword Stamp"]}},
    21: {"TotalStampLevels": 5000, "Stamps": {
        "Combat": ["Tripleshot Stamp", "Maxo Slappo Stamp"],
        "Skill": ["Buzz Buzz Stamp"],
        "Specific": {'Pickaxe Stamp': 85, 'Hatchet Stamp': 85, 'Mason Jar Stamp': 52, 'Golden Apple Stamp': 40}}},
    22: {"TotalStampLevels": 5500, "Stamps": {
        "Specific": {'Bugsack Stamp': 120, 'Bag o Heads Stamp': 120}}},
    23: {"TotalStampLevels": 6000, "Stamps": {
        "Combat": ["Violence Stamp", "Intellectostampo"],
        "Skill": ["Flowin Stamp"],
        "Specific": {'Matty Bag Stamp': 200, 'Crystallin': 150},
        "Optional": ["Blover Stamp"]}},
    24: {"TotalStampLevels": 6500, "Stamps": {
        "Combat": ["Dementia Sword Stamp"],
        "Skill": ["Sneaky Peeky Stamp", "Jade Mint Stamp", "White Essence Stamp"],
        "Misc": ["Forge Stamp"],
        "Specific": {'Drippy Drop Stamp': 100, 'Ladle Stamp': 150, 'Potion Stamp': 40, 'Forge Stamp': 40}}},
    25: {"TotalStampLevels": 7000, "Stamps": {
        "Combat": ["Conjocharmo Stamp"],
        "Specific": {'Pickaxe Stamp': 95, 'Hatchet Stamp': 95, 'Golden Apple Stamp': 60, 'Multitool Stamp': 100}}},
    26: {"TotalStampLevels": 7500, "Stamps": {
        "Specific": {'Ladle Stamp': 180, 'Forge Stamp': 100}}},
    27: {"TotalStampLevels": 8000, "Stamps": {
        "Skill": ["Multitool Stamp"],
        "Specific": {'Matty Bag Stamp': 280, 'Multitool Stamp': 150}}},
    28: {"TotalStampLevels": 8400, "Stamps": {
        "Skill": ["Dark Triad Essence Stamp"],
        "Misc": ["Atomic Stamp"],
        "Specific": {'Pickaxe Stamp': 105, 'Hatchet Stamp': 105, 'Mason Jar Stamp': 80, 'Crystallin': 200, 'Bugsack Stamp': 144, 'Bag o Heads Stamp': 144, }}},
    29: {"TotalStampLevels": 8800, "Stamps": {
        "Specific": {'Drippy Drop Stamp': 110, 'Potion Stamp': 60}}},
    30: {"TotalStampLevels": 9200, "Stamps": {
        "Specific": {'Card Stamp': 200, 'Crystallin': 250}}},
    31: {"TotalStampLevels": 9600, "Stamps": {
        "Specific": {'Golden Apple Stamp': 80}}},
    32: {"TotalStampLevels": 10000, "Stamps": {
        "Specific": {'Mason Jar Stamp': 100}}},
    33: {"TotalStampLevels": 10500, "Stamps": {
        "Specific": {'Bugsack Stamp': 168, 'Bag o Heads Stamp': 168}}},
    34: {"TotalStampLevels": 11000, "Stamps": {
        "Specific": {'Golden Apple Stamp': 100, 'Multitool Stamp': 210}}},
    35: {"TotalStampLevels": 11500, "Stamps": {
        "Combat": ["Golden Sixes Stamp"],
        "Specific": {'Golden Sixes Stamp': 120, 'Forge Stamp': 160}}},
    36: {"TotalStampLevels": 12000, "Stamps": {
        "Combat": ["Stat Wallstreet Stamp"],
        "Skill": ["Amplestample Stamp"],
        "Specific": {'Maxo Slappo Stamp': 98, 'Sashe Sidestamp': 98, 'Intellectostampo': 98}}},
    37: {"TotalStampLevels": 12500, "Stamps": {
        "Specific": {'Ladle Stamp': 270}}},
    38: {"TotalStampLevels": 13000, "Stamps": {
        "Combat": ["Sukka Foo"],
        "Skill": ["Triad Essence Stamp", "Summoner Stone Stamp"],
        "Specific": {'Triad Essence Stamp': 80, 'Forge Stamp': 220},
        "Optional": ["Void Axe Stamp"]}},
}
smithing_progressionTiers = [
    # int tier, int Cash Points Purchased, int Monster Points Purchased, int Forge Totals, str Notes
    [0, 0, 0, 0, ""],
    [1, 20, 85, 60, "bullfrog-horn"],
    [2, 60, 150, 120, "pincer-arm."],
    [3, 100, 225, 180, "shrapshell"],
    [4, 150, 350, 240, "sippy-straw"],
    [5, 200, 500, 291, "bottle-cap"],
    [6, 600, 700, 291, "condensed-zap"]
]
owl_progressionTiers = {
    0: {},
    1: {
        "MegaFeathersOwned": 9,
    },
    2: {
        "MegaFeathersOwned": 17,
        "BonusesOfOrion": 23
    },
    3: {
        "MegaFeathersOwned": 24,
        "BonusesOfOrion": 29
    },
}

###WORLD 2 PROGRESSION TIERS###
bubbles_progressionTiers = [
    # int tier,
    # int TotalBubblesUnlocked,
    # dict {OrangeSampleBubbles},
    # dict {GreenSampleBubbles},
    # dict {PurpleSampleBubbles},
    # dict {UtilityBubbles},
    # str BubbleValuePercentage,
    # str Orange, Green, Purple Notes
    # str Utility Notes
    [0, 0, {}, {}, {}, {}, "0% max value", ""],
    [1, 10,
     {'Roid Ragin': 12, 'Warriors Rule': 6, 'Hearty Diggy': 12, 'Wyoming Blood': 6, 'Sploosh Sploosh': 6, 'Stronk Tools': 8},
     {'Swift Steppin': 12, 'Archer Or Bust': 6, 'Sanic Tools': 8, 'Bug^2': 6},
     {'Stable Jenius': 12, 'Mage Is Best': 6, 'Hocus Choppus': 12, 'Molto Loggo': 6, 'Le Brain Tools': 8},
     {'Fmj': 5, 'Shaquracy': 5, 'Prowesessary': 7, 'Hammer Hammer': 6},
     "10% max value",
     "MINIMUM recommended Utility bubbles for finishing W2. Prowess hard-caps at 2x."],
    [2, 20,
     {'Roid Ragin': 25, 'Warriors Rule': 13, 'Hearty Diggy': 25, 'Wyoming Blood': 13, 'Sploosh Sploosh': 13, 'Stronk Tools': 18},
     {'Swift Steppin': 25, 'Archer Or Bust': 13, 'Sanic Tools': 18, 'Bug^2': 13},
     {'Stable Jenius': 25, 'Mage Is Best': 13, 'Hocus Choppus': 25, 'Molto Loggo': 13, 'Le Brain Tools': 18},
     {'Fmj': 10, 'Shaquracy': 10, 'Prowesessary': 15, 'Hammer Hammer': 14, 'All For Kill': 25},
     "20% max value",
     "MINIMUM recommended Utility bubbles for starting W3. Prowess hard-caps at 2x."],
    [3, 40,
     {'Roid Ragin': 67, 'Warriors Rule': 34, 'Hearty Diggy': 67, 'Wyoming Blood': 20, 'Sploosh Sploosh': 20, 'Stronk Tools': 47},
     {'Swift Steppin': 67, 'Archer Or Bust': 34, 'Sanic Tools': 47, 'Bug^2': 20},
     {'Stable Jenius': 67, 'Mage Is Best': 34, 'Hocus Choppus': 67, 'Molto Loggo': 20, 'Le Brain Tools': 47},
     {'Fmj': 15, 'Shaquracy': 15, 'Prowesessary': 40, 'Hammer Hammer': 41, 'All For Kill': 67},
     "40% max value",
     "MINIMUM recommended Utility bubbles for starting W4. Prowess hard-caps at 2x."],
    [4, 60,
     {'Roid Ragin': 100, 'Warriors Rule': 50, 'Hearty Diggy': 100, 'Wyoming Blood': 30, 'Sploosh Sploosh': 30, 'Stronk Tools': 70},
     {'Swift Steppin': 100, 'Archer Or Bust': 50, 'Sanic Tools': 70, 'Bug^2': 30},
     {'Stable Jenius': 100, 'Mage Is Best': 50, 'Hocus Choppus': 100, 'Molto Loggo': 30, 'Le Brain Tools': 70},
     {'Fmj': 20, 'Shaquracy': 20, 'Prowesessary': 60, 'Hammer Hammer': 65, 'All For Kill': 100},
     "50% max value",
     "MINIMUM recommended Utility bubbles for starting W5. Prowess hard-caps at 2x, which you should be reaching now!"],
    [5, 80,
     {'Roid Ragin': 150, 'Warriors Rule': 75, 'Hearty Diggy': 150, 'Wyoming Blood': 45, 'Sploosh Sploosh': 45, 'Stronk Tools': 105, 'Multorange': 45},
     {'Swift Steppin': 150, 'Archer Or Bust': 75, 'Bug^2': 45, 'Premigreen': 45, },
     {'Stable Jenius': 150, 'Mage Is Best': 75, 'Molto Loggo': 45, 'Le Brain Tools': 105, 'Severapurple': 45, },
     {'Fmj': 30, 'Shaquracy': 30, 'Hammer Hammer': 105, 'All For Kill': 150},
     "60% max value",
     "MINIMUM recommended Utility bubbles for starting W6 push. Keep watch of your No Bubble Left Behind list (from W4 Lab) to keep cheap/easy bubbles off when possible!"],
    [6, 100,
     {'Roid Ragin': 234, 'Warriors Rule': 117, 'Hearty Diggy': 234, 'Wyoming Blood': 70, 'Sploosh Sploosh': 70, 'Stronk Tools': 164, 'Multorange': 70,
      'Dream Of Ironfish': 70},
     {'Swift Steppin': 234, 'Archer Or Bust': 117, 'Bug^2': 70, 'Premigreen': 70, 'Fly In Mind': 94},
     {'Stable Jenius': 234, 'Mage Is Best': 117, 'Molto Loggo': 70, 'Le Brain Tools': 164, 'Severapurple': 70, 'Tree Sleeper': 94},
     {'Cookin Roadkill': 105, 'All For Kill': 167},
     "70% max value",
     "Cookin Roadkill 105 = 60% bubble strength. All for Kill hard-cap at 167, you're finished!"],
    [7, 100,
     {'Roid Ragin': 400, 'Warriors Rule': 200, 'Hearty Diggy': 400, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 280, 'Multorange': 120,
      'Dream Of Ironfish': 120},
     {'Swift Steppin': 400, 'Archer Or Bust': 200, 'Bug^2': 120, 'Premigreen': 120},
     {'Stable Jenius': 400, 'Mage Is Best': 200, 'Hocus Choppus': 400, 'Molto Loggo': 120, 'Le Brain Tools': 280, 'Severapurple': 120, 'Tree Sleeper': 160},
     {'Laaarrrryyyy': 150, 'Hammer Hammer': 150, },
     "80% max value",
     "Larry at 150 = 72% chance for +2 levels. Somewhere around level 125-150, this bubble should pass 100m Dementia Ore cost and be available to level with Boron upgrades from the W3 Atom Collider in Construction.  It should be, in my opinion, the ONLY Utility Bubble you spend these daily clicks on until it reaches 501. If you cannot afford the Particles needed to level Larry, invest into Sampling Bubbles."],
    [8, 100,
     {'Roid Ragin': 567, 'Warriors Rule': 284, 'Hearty Diggy': 567, 'Stronk Tools': 397, 'Multorange': 170, 'Dream Of Ironfish': 170, 'Shimmeron': 227},
     {'Swift Steppin': 567, 'Archer Or Bust': 284, 'Premigreen': 170},
     {'Stable Jenius': 567, 'Mage Is Best': 284, 'Hocus Choppus': 567, 'Le Brain Tools': 397, 'Severapurple': 170, 'Tree Sleeper': 227},
     {'Hammer Hammer': 180, },
     "85% max value",
     ""],
    [9, 100,
     {'Roid Ragin': 615, 'Warriors Rule': 308, 'Hearty Diggy': 615, 'Stronk Tools': 430, 'Multorange': 185, 'Dream Of Ironfish': 185, 'Shimmeron': 246},
     {'Swift Steppin': 615, 'Archer Or Bust': 308, 'Premigreen': 185},
     {'Stable Jenius': 615, 'Mage Is Best': 308, 'Hocus Choppus': 615, 'Le Brain Tools': 430, 'Severapurple': 185, 'Tree Sleeper': 246},
     {'Hammer Hammer': 210, },
     "86% max value",
     ""],
    [10, 100,
     {'Roid Ragin': 670, 'Warriors Rule': 335, 'Hearty Diggy': 670, 'Stronk Tools': 469, 'Multorange': 201, 'Dream Of Ironfish': 201, 'Shimmeron': 268},
     {'Swift Steppin': 670, 'Archer Or Bust': 335, 'Premigreen': 201},
     {'Stable Jenius': 670, 'Mage Is Best': 335, 'Hocus Choppus': 670, 'Le Brain Tools': 469, 'Severapurple': 201, 'Tree Sleeper': 268},
     {'Laaarrrryyyy': 501, },
     "87% max value",
     ""],
    [11, 100,
     {'Roid Ragin': 700, 'Warriors Rule': 367, 'Hearty Diggy': 734, 'Stronk Tools': 514, 'Multorange': 220, 'Dream Of Ironfish': 220, 'Shimmeron': 294},
     {'Swift Steppin': 700, 'Archer Or Bust': 367, 'Premigreen': 220},
     {'Stable Jenius': 700, 'Mage Is Best': 367, 'Hocus Choppus': 734, 'Le Brain Tools': 514, 'Severapurple': 220, 'Tree Sleeper': 294},
     {'Cookin Roadkill': 630, 'Hammer Hammer': 270, },
     "88% max value",
     ""],
    [12, 100,
     {'Roid Ragin': 720, 'Warriors Rule': 405, 'Hearty Diggy': 810, 'Stronk Tools': 567, 'Multorange': 243, 'Dream Of Ironfish': 243, 'Shimmeron': 324},
     {'Swift Steppin': 720, 'Archer Or Bust': 405, 'Premigreen': 243},
     {'Stable Jenius': 720, 'Mage Is Best': 405, 'Hocus Choppus': 810, 'Le Brain Tools': 567, 'Severapurple': 243, 'Tree Sleeper': 324},
     {'Startue Exp': 240, 'Hammer Hammer': 300, },
     "89% max value",
     ""],
    [13, 100,
     {'Roid Ragin': 740, 'Warriors Rule': 450, 'Hearty Diggy': 900, 'Stronk Tools': 630, 'Multorange': 270, 'Dream Of Ironfish': 270, 'Shimmeron': 360},
     {'Swift Steppin': 740, 'Archer Or Bust': 450, 'Premigreen': 270},
     {'Stable Jenius': 740, 'Mage Is Best': 450, 'Hocus Choppus': 900, 'Le Brain Tools': 630, 'Severapurple': 270, 'Tree Sleeper': 360},
     {'Droppin Loads': 280},
     "90% max value",
     ""],
    [14, 100,
     {'Roid Ragin': 760, 'Warriors Rule': 506, 'Hearty Diggy': 1012, 'Multorange': 304, 'Shimmeron': 405},
     {'Swift Steppin': 760, 'Archer Or Bust': 506, 'Premigreen': 304},
     {'Stable Jenius': 760, 'Mage Is Best': 506, 'Hocus Choppus': 1012, 'Severapurple': 304},
     {'Call Me Bob': 200},
     "91% max value",
     ""],
    [15, 100,
     {'Roid Ragin': 780, 'Warriors Rule': 575, 'Hearty Diggy': 1150, 'Multorange': 345, 'Shimmeron': 460},
     {'Swift Steppin': 780, 'Archer Or Bust': 575, 'Premigreen': 345},
     {'Stable Jenius': 780, 'Mage Is Best': 575, 'Hocus Choppus': 1150, 'Severapurple': 345},
     {'Big P': 140, 'Big Game Hunter': 70, 'Mr Massacre': 117},
     "92% max value",
     ""],
    [16, 100,
     {'Roid Ragin': 800, 'Warriors Rule': 665, 'Hearty Diggy': 1329, 'Multorange': 399, 'Shimmeron': 532},
     {'Swift Steppin': 800, 'Archer Or Bust': 665, 'Premigreen': 399},
     {'Stable Jenius': 800, 'Mage Is Best': 665, 'Hocus Choppus': 1329, 'Severapurple': 399},
     {'Big P': 240, 'Big Game Hunter': 120, 'Mr Massacre': 200},
     "93% max value",
     ""],
    [17, 100,
     {'Roid Ragin': 820, 'Warriors Rule': 784, 'Hearty Diggy': 1567, 'Multorange': 470, 'Shimmeron': 627},
     {'Swift Steppin': 820, 'Archer Or Bust': 784, 'Premigreen': 470},
     {'Stable Jenius': 820, 'Mage Is Best': 784, 'Hocus Choppus': 1567, 'Severapurple': 470},
     {'Big P': 340, 'Carpenter': 284, 'Big Game Hunter': 170, 'Mr Massacre': 284},
     "94% max value",
     ""],
    [18, 100,
     {'Roid Ragin': 840, 'Warriors Rule': 950, 'Hearty Diggy': 1900, 'Multorange': 570, 'Shimmeron': 760},
     {'Swift Steppin': 840, 'Archer Or Bust': 950, 'Premigreen': 570},
     {'Stable Jenius': 840, 'Mage Is Best': 950, 'Hocus Choppus': 1900, 'Severapurple': 570},
     {'Laaarrrryyyy': 900, 'Big P': 540, 'Call Me Bob': 500, 'Carpenter': 450, 'Big Game Hunter': 270, 'Mr Massacre': 450},
     "95% max value",
     ""],
    [19, 100,
     {'Roid Ragin': 860, 'Warriors Rule': 1200, 'Multorange': 720},
     {'Swift Steppin': 860, 'Archer Or Bust': 1200},
     {'Stable Jenius': 860, 'Mage Is Best': 1200, 'Severapurple': 720},
     {'Call Me Bob': 700, 'Cropius Mapper': 630, 'Lo Cost Mo Jade': 360},
     "96% max value",
     ""],
    [20, 100,
     {'Roid Ragin': 880, 'Warriors Rule': 1617, 'Multorange': 970},
     {'Swift Steppin': 880, 'Archer Or Bust': 1617},
     {'Stable Jenius': 880, 'Mage Is Best': 1617, 'Severapurple': 970},
     {'Cookin Roadkill': 1330, 'Big P': 940, 'Laaarrrryyyy': 1900, 'Carpenter': 950, 'Big Game Hunter': 570, 'Mr Massacre': 950, 'Diamond Chef': 553, 'Lo Cost Mo Jade': 760},
     "97% max value",
     ""],
    [21, 120,
     {'Roid Ragin': 900, 'Warriors Rule': 2450, 'Multorange': 1470},
     {'Swift Steppin': 900, 'Archer Or Bust': 2450},
     {'Stable Jenius': 900, 'Mage Is Best': 2450, 'Severapurple': 1470},
     {'Essence Boost-Orange': 400, 'Essence Boost-Green': 400, 'Call Me Bob': 1000, 'Diamond Chef': 890},
     "98% max value",
     ""],
    [22, 120,
     {'Roid Ragin': 950, 'Warriors Rule': 4950, 'Multorange': 2970},
     {'Swift Steppin': 950, 'Archer Or Bust': 4950},
     {'Stable Jenius': 950, 'Mage Is Best': 4950, 'Severapurple': 2970},
     {'Carpenter': 2450, 'Big P': 1440},
     "99% max value",
     ""],
    [23, 120,
     {'Roid Ragin': 9000,
      'Slabi Orefish': 540, 'Slabi Strength': 540, 'Endgame Eff I': 540, 'Tome Strength': 540},
     {'Swift Steppin': 9000, 'Sanic Tools': 630,
      'Slabo Critterbug': 540, 'Slabo Agility': 540, 'Endgame Eff II': 540, 'Tome Agility': 540},
     {'Stable Jenius': 9000,
      'Slabe Logsoul': 540, 'Slabe Wisdom': 540, 'Endgame Eff III': 540, 'Tome Wisdom': 540},
     {'Droppin Loads': 630, 'Startue Exp': 540},
     "90% catchup",
     ""],
    [24, 140,
     {'Roid Ragin': 9500, 'Stronk Tools': 1330, 'Dream Of Ironfish': 570,
      'Slabi Orefish': 1140, 'Slabi Strength': 1140, 'Endgame Eff I': 1140, 'Tome Strength': 1140},
     {'Swift Steppin': 9500, 'Sanic Tools': 1330, 'Fly In Mind': 760,
      'Slabo Critterbug': 1140, 'Slabo Agility': 1140, 'Endgame Eff II': 1140, 'Tome Agility': 1140},
     {'Stable Jenius': 9500, 'Le Brain Tools': 1330, 'Tree Sleeper': 760,
      'Slabe Logsoul': 1140, 'Slabe Wisdom': 1140, 'Endgame Eff III': 1140, 'Tome Wisdom': 1140},
     {'Droppin Loads': 1330, 'Startue Exp': 1140},
     "95% catchup",
     ""],
    [25, 160,
     {'Roid Ragin': 10000, 'Hearty Diggy': 9900, 'Stronk Tools': 6930, 'Dream Of Ironfish': 2970, 'Shimmeron': 3960,
      'Slabi Orefish': 5940, 'Slabi Strength': 5940, 'Endgame Eff I': 5940, 'Tome Strength': 5940},
     {'Swift Steppin': 10000, 'Sanic Tools': 6930, 'Premigreen': 2970, 'Fly In Mind': 3960,
      'Slabo Critterbug': 5940, 'Slabo Agility': 5940, 'Endgame Eff II': 5940, 'Tome Agility': 5940},
     {'Stable Jenius': 10000, 'Hocus Choppus': 9900, 'Le Brain Tools': 6930, 'Tree Sleeper': 3960,
      'Slabe Logsoul': 5940, 'Slabe Wisdom': 5940, 'Endgame Eff III': 5940, 'Tome Wisdom': 5940},
     {'Cookin Roadkill': 6930, 'Droppin Loads': 6930, 'Startue Exp': 5940, 'Laaarrrryyyy': 9900, 'Big Game Hunter': 2970, 'Mr Massacre': 4950, 'Lo Cost Mo Jade': 3960},
     "99% catchup",
     ""],
]
vials_progressionTiers = [
    # int tier, int TotalVialsUnlocked, int TotalVialsMaxed, list ParticularVials, str Notes
    [0, 0, 0, [], ""],
    [1, 7, 0, [], "This is the number of vials requiring an unlock roll of 75 or less. "],
    [2, 14, 0, [], "This is the number of vials requiring an unlock roll of 85 or less. "],
    [3, 19, 0, [], "This is the number of vials requiring an unlock roll of 90 or less. "],
    [4, 27, 0, [], "This is the number of vials requiring an unlock roll of 95 or less. "],
    [5, 33, 0, [], "This is the number of vials requiring an unlock roll of 98 or less. "],
    [6, 38, 0, [], "This is all vials up through W4, excluding the Arcade Pickle. "],
    [7, 51, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [8, 63, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [9, 67, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [10, 70, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [11, 70, 4, ['Copper Corona (Copper Ore)', 'Sippy Splinters (Oak Logs)', 'Jungle Juice (Jungle Logs)', 'Tea With Pea (Potty Rolls)'],
     "This is the first half of W6, excluding the Arcade Pickle. "],
    [12, 70, 8, ['Gold Guzzle (Gold Ore)', 'Seawater (Goldfish)', 'Fly In My Drink (Fly)', 'Blue Flav (Platinum Ore)'], ""],
    [13, 72, 12, ['Slug Slurp (Hermit Can)', 'Void Vial (Void Ore)', 'Ew Gross Gross (Mosquisnow)', 'The Spanish Sahara (Tundra Logs)'], ""],
    [14, 72, 16, ['Mushroom Soup (Spore Cap)', 'Maple Syrup (Maple Logs)', 'Marble Mocha (Marble Ore)', 'Skinny 0 Cal (Snake Skin)'], ""],
    [15, 72, 20, ['Long Island Tea (Sand Shark)', 'Anearful (Glublin Ear)', 'Willow Sippy (Willow Logs)', 'Dieter Drink (Bean Slices)'], ""],
    [16, 72, 24, ['Shinyfin Stew (Equinox Fish)', 'Ramificoction (Bullfrog Horn)', 'Tail Time (Rats Tail)', 'Dreamy Drink (Dream Particulate)'], ""],
    [17, 72, 28, ['Mimicraught (Megalodon Tooth)', 'Fur Refresher (Floof Ploof)', 'Etruscan Lager (Mamooth Tusk)', 'Dusted Drink (Dust Mote)'], ""],
    [18, 72, 32, ['Ded Sap (Effervescent Log)', 'Sippy Soul (Forest Soul)', 'Visible Ink (Pen)', 'Snow Slurry (Snow Ball)'], ""],
    [19, 72, 36, ['Sippy Cup (Sippy Straw)', 'Goosey Glug (Honker)', 'Crab Juice (Crabbo)', 'Chonker Chug (Dune Soul)'], ""],
    [20, 72, 40, ['40-40 Purity (Contact Lense)', 'Ladybug Serum (Ladybug)', 'Bubonic Burp (Mousey)', 'Capachino (Purple Mush Cap)'], ""],
    [21, 72, 44, ['Donut Drink (Half Eaten Donut)', 'Krakenade (Kraken)', 'Calcium Carbonate (Tongue Bone)', 'Spool Sprite (Thread)'], ""],
    [22, 72, 48, ['Choco Milkshake (Crumpled Wrapper)', 'Electrolyte (Condensed Zap)', 'Ash Agua (Suggma Ashes)', 'Oj Jooce (Orange Slice)'], ""],
    [23, 72, 52, ['Thumb Pow (Trusty Nails)', 'Slowergy Drink (Frigid Soul)', 'Bunny Brew (Bunny)', 'Flavorgil (Caulifish)'], ""],
    [24, 72, 56, ['Spook Pint (Squishy Soul)', 'Firefly Grog (Firefly)', 'Barium Mixture (Copper Bar)', 'Bloat Draft (Blobfish)'], ""],
    [25, 73, 60, ['Barley Brew (Iron Bar)', 'Oozie Ooblek (Oozie Soul)', 'Ricecakorade (Rice Cake)', 'Greenleaf Tea (Leafy Branch)'], ""],
    [26, 74, 65, ['Venison Malt (Mongo Worm Slices)', 'Gibbed Drink (Eviscerated Horn)', 'Royale Cola (Royal Headpiece)', 'Refreshment (Breezy Soul)',
                  'Turtle Tisane (Tuttle)'], ""],
    # [27, 75, 69, ['Red Malt (Redox Salts)', 'Poison Tincture (Poison Froge)', 'Orange Malt (Explosive Salts)', 'Shaved Ice (Purple Salt)'], "Currently considered impossible"],
    # [28, 75, 73, ['Dreadnog (Dreadlo Bar)', 'Dabar Special (Godshard Bar)', 'Pearl Seltzer (Pearler Shell)', 'Hampter Drippy (Hampter)'], "Currently considered impossible"],
    # [29, 75, 76, ['Pickle Jar (BobJoePickle)', 'Ball Pickle Jar (BallJoePickle)'], "Currently considered impossible"],
]
sigils_progressionTiers = {
    0: {"Label": "S", "Sigils":[]},
    1: {"Label": "A", "Sigils":[]},
    2: {"Label": "B", "Sigils":[]},
    3: {"Label": "C", "Sigils":[]},
    4: {"Label": "D", "Sigils":[]},
    5: {"Label": "F", "Sigils":[]},
}

###WORLD 3 PROGRESSION TIERS###
saltLick_progressionTiers = [
    [0, {}, ""],
    [1, {'Obol Storage': 8}, "Froge"],
    [2, {'Printer Sample Size': 20}, "Redox Salts"],
    [3, {'Refinery Speed': 10}, "Explosive Salts"],
    [4, {'Max Book': 10}, "Spontaneity Salts"],
    [5, {'TD Points': 10}, "Dioxide Synthesis"],
    [6, {'Multikill': 10}, "Purple Salt"],
    [7, {'EXP': 100}, "Dune Soul"],
    [8, {'Alchemy Liquids': 100}, "Mousey"],
    [9, {'Damage': 250}, "Pingy"]
]
deathNote_progressionTiers = [
    # 0-4 int tier. int w1LowestSkull, int w2LowestSkull, int w3LowestSkull, int w4LowestSkull,
    # 5-9 int w5LowestSkull, int w6LowestSkull, int w7LowestSkull, int w8LowestSkull, int zowCount, int chowCount,
    # 10-11 int meowCount, str Notes
    [0,  0,  0,  0,  0,  0,  0,     0, 0,   0, 0, 0, ""],
    [1,  1,  1,  1,  0,  0,  0,     0, 0,   0, 0, 0, ""],
    [2,  2,  2,  2,  0,  0,  0,     0, 0,   0, 0, 0, ""],
    [3,  3,  3,  3,  1,  0,  0,     0, 0,   0, 0, 0, ""],
    [4,  4,  4,  4,  2,  0,  0,     0, 0,   0, 0, 0, ""],  #The recommendation for ZOWs is 12hrs or less (8,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!
    [5,  5,  5,  5,  3,  0,  0,     0, 0,   0, 0, 0,
     "The Voidwalker questline requires W1-W3 at all Plat Skulls. Aim to complete this by Mid W5 as Vman's account-wide buffs are insanely strong."],
    [6,  7,  5,  5,  4,  0,  0,     0, 0,   0, 0, 0, ""],  #"The recommendation for CHOWs is 12hrs or less (83,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"
    [7,  10, 7,  5,  5,  1,  0,     0, 0,   0, 0, 0, ""],
    [8,  10, 10, 7,  5,  2,  0,     0, 0,   0, 0, 0, ""],
    [9,  10, 10, 10, 5,  3,  0,     0, 0,   0, 0, 0, ""],
    [10, 10, 10, 10, 7,  4,  0,     0, 0,   0, 0, 0, ""],
    [11, 10, 10, 10, 10, 5,  0,     0, 0,   0, 0, 0, ""],  #"Complete Lava Skull, then BB Super CHOW, before you start working on Eclipse Skulls. "
    [12, 10, 10, 10, 10, 7,  0,     0, 0,   0, 0, 0, ""],
    [13, 10, 10, 10, 10, 10, 0,     0, 0,   0, 0, 0, ""],
    [14, 10, 10, 10, 10, 10, 0,     0, 0,   0, 0, 0, ""],
    [15, 10, 10, 10, 10, 10, 0,     0, 0,   0, 0, 0, ""],
    [16, 20, 10, 10, 10, 10, 0,     0, 0,   0, 0, 0, ""],
    [17, 20, 20, 10, 10, 10, 1,     0, 0,   0, 0, 0, ""],
    [18, 20, 20, 20, 10, 10, 2,     0, 0,   0, 0, 0, ""],
    [19, 20, 20, 20, 20, 10, 3,     0, 0,   15, 15, 15, "Aim for Super CHOWs in 24hrs each (4m+ KPH)"],
    [20, 20, 20, 20, 20, 20, 4,     0, 0,   26, 26, 26, ""],
    [21, 20, 20, 20, 20, 20, 5,     0, 0,   40, 40, 40, ""],
    [22, 20, 20, 20, 20, 20, 7,     0, 0,   53, 53, 53, ""],
    [23, 20, 20, 20, 20, 20, 10,    0, 0,   66, 66, 66, ""],
    [24, 20, 20, 20, 20, 20, 10,    0, 0,   73, 73, 73, ""],
    [25, 20, 20, 20, 20, 20, 20,    0, 0,   80, 80, 80, ""],
    [26, 20, 20, 20, 20, 20, 20,    0, 0,   84, 84, 83, "As of v2.11, completing a Super CHOW on Boops is impossible."],
    [27, 20, 20, 20, 20, 20, 20,    0, 0,   86, 86, 86, "Info only"]
]
buildingsPostBuffs_progressionTiers = [
    [0, "Unlock", [], "", ""],
    [1, "SS", ["3D Printer", "Cost Cruncher", "Automation Arm"], "", ""],
    [2, "S", ["Talent Book Library", "Death Note", "Salt Lick", "Trapper Drone", "Boulder Roller", "Kraken Cosplayer", "Poisonic Elder"], "", ""],
    [3, "A", ["Chest Space", "Pulse Mage", "Fireball Lobber", "Frozone Malone", "Stormcaller", "Party Starter", "Voidinator", "Clover Shrine", "Crescent Shrine", "Undead Shrine"], "", ""],
    [4, "B", ["Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine", "Summereading Shrine"], "", ""],
    [5, "C", ["Atom Collider", "Primordial Shrine"], "", ""],
    [6, "D", [], "", ""],
    [7, "F", [], "", ""]
]
buildingsPreBuffs_progressionTiers = [
    [0, "Unlock", [], "", ""],
    [1, "SS", ["3D Printer", "Cost Cruncher", "Automation Arm"], "", ""],
    [2, "S", ["Talent Book Library", "Death Note", "Salt Lick", "Trapper Drone", "Boulder Roller", "Kraken Cosplayer", "Poisonic Elder"], "", ""],
    [3, "A", ["Chest Space", "Stormcaller", "Party Starter", "Clover Shrine", "Crescent Shrine", "Undead Shrine"], "", ""],
    [4, "B", ["Frozone Malone", "Voidinator"], "", ""],
    [5, "C", ["Atom Collider", "Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine"], "", ""],
    [6, "D", ["Pulse Mage", "Fireball Lobber", "Summereading Shrine"], "", ""],
    [7, "F", ["Primordial Shrine"], "", ""]
]
prayers_progressionTiers = [
    #Tier, PrayerDict, 	Notes
    [0, {}, ""],
    [1, {'The Royal Sampler': 5}, ""],
    [2, {'Skilled Dimwit': 20}, ""],
    [3, {'Balance of Pain': 11}, ""],
    [4, {'Skilled Dimwit': 35, 'Balance of Pain':20}, ""],
    [5, {'Midas Minded':20}, ""],
    [6, {'Skilled Dimwit': 50, 'Midas Minded': 50, 'Balance of Pain': 30}, ""],
    [7, {'Shiny Snitch': 50, 'Zerg Rushogen': 20, 'Jawbreaker': 50, 'Ruck Sack': 50, 'Balance of Proficiency': 50}, ""],
    [8, {'Unending Energy': 50, 'Big Brain Time': 50, 'Antifun Spirit': 10, 'Fibers of Absence': 50, 'Beefy For Real': 40}, ""],
    [9, {'Tachion of the Titans': 1, 'Balance of Precision': 1, 'Circular Criticals': 1, 'Vacuous Tissue': 1, 'Glitterbug': 1}, ""],
]
equinox_progressionTiers = {
    'Recommended': ['Equinox Symbols', 'Equinox Resources', 'Metal Detector', 'Slow Roast Wiz', 'Liquidvestment', 'Faux Jewels', 'Matching Scims', 'Equinox Dreams'],
    'Optional': ['Shades of K', 'Laboratory Fuse', 'Food Lust']
}
atoms_progressionTiers = {
    0: {},
    1: {
        'Atoms': {
            'Hydrogen - Stamp Decreaser': 5,
            'Helium - Talent Power Stacker': 1
        },
    },
    2: {
        'Atoms': {
            'Lithium - Bubble Insta Expander': 1,
        },
    },
    3: {
        'Atoms': {
            'Boron - Particle Upgrader': 1,
            'Helium - Talent Power Stacker': 2,
        },
    },
    4: {
        'Atoms': {
            'Helium - Talent Power Stacker': 3,
        },
    },
    5: {
        'Atoms': {
            'Nitrogen - Construction Trimmer': 1,
            'Oxygen - Library Booker': 1,
        },
    },
    6: {
        'Atoms': {
            'Hydrogen - Stamp Decreaser': 18,
            'Helium - Talent Power Stacker': 4,
        },
    },
    7: {
        'Atoms': {
            'Fluoride - Void Plate Chef': 3,
            'Helium - Talent Power Stacker': 5,
        },
    },
    8: {
        'Atoms': {
            'Fluoride - Void Plate Chef': 7,
            'Helium - Talent Power Stacker': 6,
        },
    },
    9: {
        'Atoms': {
            "Neon - Damage N' Cheapener": 2,
            'Fluoride - Void Plate Chef': 11,
            'Helium - Talent Power Stacker': 7,
        },
    },
    10: {
        'Atoms': {
            "Neon - Damage N' Cheapener": 10,
            'Fluoride - Void Plate Chef': 15,
        },
    },
    11: {
        'Atoms': {
            'Helium - Talent Power Stacker': 8,
            'Fluoride - Void Plate Chef': 20,
        },
    },
    12: {
        'Atoms': {
            "Neon - Damage N' Cheapener": 20,
            'Helium - Talent Power Stacker': 9,
        },
    },
    13: {
        'Atoms': {
            'Boron - Particle Upgrader': 30,
            'Hydrogen - Stamp Decreaser': 30,
            "Neon - Damage N' Cheapener": 30,
            'Fluoride - Void Plate Chef': 30,
        },
    },
    14: {
        'Atoms': {
            'Helium - Talent Power Stacker': 10,
        },
    },
}

###WORLD 4 PROGRESSION TIERS###
breeding_progressionTiers = {
        0: {
            "Tier": 0,
            "TerritoriesUnlocked": 0,
            "PetSlots": 2,
            "TerritoryNotes": "",
            "ArenaWaves": 0,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        1: {
            "Tier": 1,
            "TerritoriesUnlocked": 3,
            "PetSlots": 3,
            "TerritoryNotes": "",
            "ArenaWaves": 3,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        2: {
            "Tier": 2,
            "TerritoriesUnlocked": 7,
            "PetSlots": 4,
            "TerritoryNotes": "",
            "ArenaWaves": 15,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        3: {
            "Tier": 3,
            "TerritoriesUnlocked": 10,
            "PetSlots": 4,
            "TerritoryNotes": "",
            "ArenaWaves": 50,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        4: {
            "Tier": 4,
            "TerritoriesUnlocked": 14,
            "PetSlots": 5,
            "TerritoryNotes": "",
            "ArenaWaves": 125,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        5: {
            "Tier": 5,
            "TerritoriesUnlocked": 20,
            "PetSlots": 6,
            "TerritoryNotes": "",
            "ArenaWaves": 200,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        #0-5 are Territory/Arena focused.
        #6 is blended
        #7+ are Shiny focused
        6: {
            "Tier": 6,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Faster Shiny Pet Lv Up Rate": [24, 6],
                "Bonuses from All Meals": [10, 5],
                "Infinite Star Signs": [25, 5],
                "Base Efficiency for All Skills": [20, 5],
            },
            "ShinyNotes": "Start by focusing on pets that increase Shiny Speed rate. This will decrease the amount of time needed to level up pets in the future."
            },
        7: {
            "Tier": 7,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Base Critter Per Trap": [10, 5],
                "Drop Rate": [15, 5],
                "Faster Refinery Speed": [15, 5],
                "Lower Minimum Travel Time for Sailing": [5, 5],
                },
            "ShinyNotes": ""
            },
        8: {
            "Tier": 8,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Multikill Per Tier": [20, 5],
                "Higher Artifact Find Chance": [15, 5],
                "Faster Shiny Pet Lv Up Rate": [28, 7],
                "Infinite Star Signs": [37, 7],
                "Summoning EXP": [10, 5]
                },
            "ShinyNotes": ""
            },
        9: {
            "Tier": 9,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Bonuses from All Meals": [26, 13],
                "Base Efficiency for All Skills": [48, 12],
                },
            "ShinyNotes": ""
        },
        10: {
            "Tier": 10,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Drop Rate": [36, 12],
                "Base Critter Per Trap": [22, 11],
                },
            "ShinyNotes": ""
        },
        11: {
            "Tier": 11,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Summoning EXP": [22, 11],
                "Faster Refinery Speed": [33, 11],
                "Multikill Per Tier": [44, 11],
                "Infinite Star Signs": [45, 8],
            },
            "ShinyNotes": ""
        }
    }
rift_progressionTiers = {
    0: [0,  "",             0],
    1: [5,  "3 to 5M",      100],
    2: [10, "30M",          140],
    3: [15, "68M",          160],
    4: [20, "185M",         180],
    5: [25, "1,120M",       180],
    6: [30, "12B",          220],
    7: [35, "125B",         220],
    8: [40, "1,554B",       240],
    9: [45, "20T",          240],
    10: [50, "101T",        240],
    11: [55, "528T",        240],
}

###WORLD 5 PROGRESSION TIERS###
divinity_progressionTiers = {
    0: {},
    1: {"GodsUnlocked": 1},
    2: {"GodsUnlocked": 2},
    3: {"GodsUnlocked": 3},
    4: {"GodsUnlocked": 4},
    5: {"GodsUnlocked": 5},
    6: {"GodsUnlocked": 6},
    7: {"GodsUnlocked": 7},
    8: {"GodsUnlocked": 8},
    9: {"GodsUnlocked": 9},
    10: {"GodsUnlocked": 10},
    11: {"MaxDivLevel": 50},
    12: {"MinDivLevel": 40}
}
sailing_progressionTiers = {
    0: {},
    1: {
        'IslandsDiscovered': 1,
        'CaptainsAndBoats': 3,
        'Artifacts': {
            'Moai Head': 1,
            'Fauxory Tusk': 2
        }
    },
    2: {
        'IslandsDiscovered': 4,
        'CaptainsAndBoats': 5,
        'Artifacts': {
            'Gold Relic': 1,
            '10 AD Tablet': 2
        }
    },
    3: {
        'IslandsDiscovered': 5,
        'CaptainsAndBoats': 9,
        'Artifacts': {
            'Maneki Kat': 1,
            'Ruble Cuble': 1,
            'Genie Lamp': 1,
            'Silver Ankh': 1,
            'Emerald Relic': 1,
            'Fun Hippoete': 1,
            'Arrowhead': 1,
            'Ashen Urn': 2
        }
    },
    4: {
        'IslandsDiscovered': 6,
        'CaptainsAndBoats': 10,
        'Artifacts': {
            'Amberite': 2,
            'Gold Relic': 2,
        }
    },
    5: {
        'IslandsDiscovered': 7,
        'CaptainsAndBoats': 11,
        'Artifacts': {
            'Jade Rock': 2,
        }
    },
    6: {
        'IslandsDiscovered': 8,
        'CaptainsAndBoats': 12,
        'Artifacts': {
            'Triagulon': 1,
            'Billcye Tri': 1,
            'Frost Relic': 1,
            'Chilled Yarn': 1,
            'Causticolumn': 1,
            'Dreamcatcher': 1,
            'Gummy Orb': 1
        }
    },
    7: {
        'IslandsDiscovered': 9,
        'CaptainsAndBoats': 13,
        'Artifacts': {
            'Fury Relic': 2,
        },
        'Beanstacked': True
    },
    8: {
        'IslandsDiscovered': 12,
        'CaptainsAndBoats': 15,
        'Artifacts': {
            'Crystal Steak': 2,
        }
    },
    9: {
        'IslandsDiscovered': 14,
        'CaptainsAndBoats': 17,
        'Artifacts': {
            'Socrates': 2,
        }
    },
    10: {
        'IslandsDiscovered': 15,
        'CaptainsAndBoats': 19,
        'Artifacts': {
            'Cloud Urn': 1,
            'Weatherbook': 1,
            'Trilobite Rock': 1,
            'Opera Mask': 1,
            'The True Lantern': 1
        }
    },
    11: {
        'CaptainsAndBoats': 20,
        'Artifacts': {
            'Fauxory Tusk': 3,
            '10 AD Tablet': 3,
            'Fury Relic': 3
        },
        'Eldritch': True
    },
    12: {
        'Artifacts': {
            'Crystal Steak': 3,
            'Socrates': 3
        }
    },
    13: {
        'Artifacts': {
            'Amberite': 3,
            'Gold Relic': 3,
            'Chilled Yarn': 3
        }
    },
    14: {
        'Artifacts': {
            'Moai Head': 2,
            'Maneki Kat': 2,
            'Ruble Cuble': 2,
            'Genie Lamp': 2,
            'Silver Ankh': 2,
            'Emerald Relic': 2,
            'Fun Hippoete': 2,
            'Arrowhead': 2,
            'Ashen Urn': 2,
            'Triagulon': 2,
            'Billcye Tri': 2,
            'Frost Relic': 2,
            'Causticolumn': 2,
            'Jade Rock': 2,
            'Dreamcatcher': 2,
            'Gummy Orb': 2,
            'Cloud Urn': 2,
            'Weatherbook': 2,
            'Trilobite Rock': 2,
            'Opera Mask': 2,
            'The True Lantern': 2
        },
        #'SuperBeanstacked': True
    },
    15: {
        'Artifacts': {
            'Moai Head': 3,
            'Maneki Kat': 3,
            'Ruble Cuble': 3,
            'Genie Lamp': 3,
            'Silver Ankh': 3,
            'Emerald Relic': 3,
            'Fun Hippoete': 3,
            'Arrowhead': 3,
            'Ashen Urn': 3,
            'Triagulon': 3,
            'Billcye Tri': 3,
            'Frost Relic': 3,
            'Causticolumn': 3,
            'Jade Rock': 3,
            'Gummy Orb': 3,
            'Cloud Urn': 3,
            'Weatherbook': 3,
            'Trilobite Rock': 3,
            'Opera Mask': 3,
            'The True Lantern': 3
        },
    },
    16: {
        'Artifacts': {
            'Fauxory Tusk': 4,
            #'10 AD Tablet': 4,  #Still debating this one. I don't know if you'll care about Speed at this point
            'Fury Relic': 4,
            'Gold Relic': 4,
            'Amberite': 4
        },
        'Sovereign': True
    },
    17: {
        'Artifacts': {
            'The Onyx Lantern': 3,
            #'10 AD Tablet': 4,  #Still debating this one. I don't know if you'll care about Speed at this point
            'The Winz Lantern': 4
        },
        'ExtraLanterns': True
    },
    18: {
        'Artifacts': {
            'Moai Head': 4,
            'Maneki Kat': 4,
            'Ruble Cuble': 4,
            #'Fauxory Tusk': 4,
            #'Gold Relic': 4,
            'Genie Lamp': 4,
            'Silver Ankh': 4,
            'Emerald Relic': 4,
            'Fun Hippoete': 4,
            'Arrowhead': 4,
            '10 AD Tablet': 4,
            'Ashen Urn': 4,
            'Amberite': 4,
            'Triagulon': 4,
            'Billcye Tri': 4,
            'Frost Relic': 4,
            #'Chilled Yarn': 4,
            'Causticolumn': 4,
            'Jade Rock': 4,
            'Gummy Orb': 4,
            #'Fury Relic': 4,
            'Cloud Urn': 4,
            'Weatherbook': 4,
            'Crystal Steak': 4,
            'Trilobite Rock': 4,
            'Opera Mask': 4,
            'Socrates': 4,
            'The True Lantern': 4,
            'The Onyx Lantern': 4,
            'The Shim Lantern': 4,
            #'The Winz Lantern': 4
        },
    },
    19: {
        'Artifacts': {
            #These last 2 are worthless, but get them anyway.
            'Giants Eye': 4,
            'Dreamcatcher': 4,
        },
    }
}


###WORLD 6 PROGRESSION TIERS###

###UI CONSTS###
maxTiersPerGroup = 3
#If you add a new switch here, you need to also add a default in \static\scripts\main.js:defaults
switches = [
    {
        "label": "Autoloot purchased",
        "name": "autoloot",
        "true": "",
        "false": "",
    },
    {
        "label": "Rift Slug acquired",
        "name": "riftslug",
        "true": "",
        "false": "",
    },
    {
        "label": "Doot acquired",
        "name": "doot",
        "true": "",
        "false": "",
    },
    {
        "label": "Sheepie acquired",
        "name": "sheepie",
        "true": "",
        "false": "",
    },
    {
        "label": "Order groups by tier",
        "name": "order_tiers",
        "true": "",
        "false": "",
    },
    {
        "label": "Hide Completed",
        "name": "hide_completed",
        "true": "",
        "false": "",
    },
    {
        "label": "Show progress bars",
        "name": "progress_bars",
        "true": "",
        "false": "",
    },
    {
        "label": "Handedness",
        "name": "handedness",
        "true": "L",
        "false": "R",
    },
    # {"label": "Legacy style", "name": "legacy", "true": "", "false": ""},
]

###GENERAL / MULTI-USE CONSTS###
currentWorld = 6
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
expectedStackables = {
    "Missable Quest Items": [
        "Quest3", "Quest4", "Quest7", "Quest12", "Quest21", "Quest14", "Quest22", "Quest23", "Quest24", "GoldricP1", "GoldricP2", "GoldricP3",
        "Quest32"
    ],
    "Base Monster Materials": [
        "Grasslands1", "Grasslands2", "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3", "Sewers1",
        "Sewers2", "TreeInterior1", "TreeInterior2",  # W1
        "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4",  # W2
        "SnowA1", "SnowA2", "SnowA3", "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4", "SnowA4", "SnowC5",  # W3
        "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1", "GalaxyB2", "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2",
        "GalaxyC3", "GalaxyC4",  # W4
        "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5", "LavaB6", "LavaC1", "LavaC2",  # W5
        "SpiA1", "SpiA2", "SpiA3", "SpiA4", "SpiA5", "SpiB1", "SpiB2", "SpiB3", "SpiB4", "SpiC1", "SpiC2", "SpiD1", "SpiD2", "SpiD3",  # W6
        "Sewers3", "Quest15", "Hgg"  # Specialty Monster Materials
    ],
    "Crystal Enemy Drops": [
        "SilverPen",
        "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1",  # W1
        "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2",  # W2
        "FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3",  # W3
        "FoodPotMana4", "Leaf4",  # W4
        "FoodPotYe5", "Leaf5",  # W5
        "Leaf6",  # W6
        "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",  # "W1" statues, some in W1-W3
        "EquipmentStatues1", "EquipmentStatues5",  # Plausible but time consuming
        "EquipmentStatues10", "EquipmentStatues12", "EquipmentStatues13", "EquipmentStatues8", "EquipmentStatues11",  # W2 statues are all slower than Power/Health
        "rtt0", "StoneZ1", "StoneT1", "StoneW1", "StoneA1",  #W1 Slow drops = Town TP + Stones
        "StoneT2", "StoneZ2",  "StoneW2",  #"StoneA2", # W2 upgrade stones and Mystery2
        "PureWater",  #W3 Slow drops = Distilled Water
        "FoodG9",  #W5 Slow drops = Golden W5 Sammy
        "FoodG11", "FoodG12"
    ],
    "Printable Skilling Resources": [
        "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", "PalmTree", "StumpTree", "SaharanFoal",  # Logs1
        "Tree7", "AlienTree", "Tree8", "Tree9", "Tree11", "Tree10", "Tree12", "Tree13",  # Logs2

        "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",  # Ores1
        "Starfire", "Marble", "Dreadlo", "Godshard",  # Ores2

        "Fish1", "Fish2", "Fish3", "Fish4",  # Small Fish
        "Fish5", "Fish6", "Fish7", "Fish8",  # Medium Fish
        "Fish9", "Fish10", "Fish11", "Fish13", "Fish12",  # Large Fish

        "Bug1", "Bug2", "Bug3", "Bug4",  # W2 Bugs
        "Bug5", "Bug6", "Bug7", "Bug8",  # W3-4 Bugs
        "Bug9", "Bug11", "Bug10", "Bug12", "Bug13",  # W5-6 Bugs
    ],
    "Other Skilling Resources": [
        "CraftMat1", "CraftMat5", "CraftMat6", "CraftMat7", "CraftMat8", "CraftMat9", "CraftMat10", "CraftMat11", "CraftMat12", "CraftMat13",  #Anvil1
        "CraftMat14",
        "Critter1", "Critter2", "Critter3", "Critter4", "Critter5", "Critter6",  #Critter1
        "Critter7", "Critter8", "Critter9", "Critter10", "Critter11",
        "Critter1A", "Critter2A",  "Critter3A", "Critter4A", "Critter5A", "Critter6A", "Critter7A", "Critter8A",  #ShinyCritter1
        "Critter9A", "Critter10A", "Critter11A",  #ShinyCritter2
        "Soul1", "Soul2", "Soul3", "Soul4", "Soul5", "Soul6", "Soul7",  #WorshipSouls
        "CopperBar", "IronBar", "GoldBar", "PlatBar", "DementiaBar", "VoidBar", "LustreBar",  #SmeltedBars1
        "StarfireBar", "DreadloBar", "MarbleBar", "GodshardBar",  #SmeltedBars2
        "Bullet", "BulletB", "FoodMining1", "FoodFish1", "FoodCatch1", "Peanut",  #Crafted1
        "Quest68", "Bullet3", "FoodChoppin1", "EquipmentSmithingTabs2",  #Crafted2
        "PeanutG",  #Gold Peanut Crafted
        "FoodTrapping1", "FoodWorship1",  # Critter Numnums and Soulble Gum Crafted
        "Refinery1", "Refinery2", "Refinery3", "Refinery4", "Refinery5", "Refinery6",
        "Ladle",
    ],
    "Vendor Shops": [
        "FoodHealth14", "FoodHealth15", "FoodHealth16", "FoodHealth17", "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4",
        "FoodPotYe4", "OilBarrel6", "OilBarrel7", "FoodHealth4", "FoodHealth9", "FoodHealth11", "Quest19", "CraftMat3",  # Sorted by daily quantity
        # "FoodHealth4", "Quest19", #W2
        # "FoodHealth11", "FoodHealth9", "FoodPotGr3", #W3
        # "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4", #W4
        # "OilBarrel6", "FoodHealth14", "FoodHealth15", #W5 shop
        # "FoodHealth16", "FoodHealth17", "OilBarrel7", #W6 Shop
    ],
    "Misc": [
        "FoodPotGr3",  #Decent Speed from W3 Shop + Sir Stache
        "FoodPotRe2",  #Average Life Potion from W2 Shop + Gigafrogs
        "FoodPotRe1",  #Small Life Potion from W1 Sewers and Tree mobs, not crystals
        "ButterBar",  #Catching Butterflies
        "FoodPotMana3",  #Decent Mana Potion from Bloques
        "OilBarrel2",  # Slime Barrel, 1 in 3334
        "DesertC2b",  # Ghost, 1 in 2k
        "Quest78",  # Equinox Mirror
        "Key2", "Key3"  # Efaunt and Chizoar keys
    ],
    "Cheater": [
        "Sewers1b", "TreeInterior1b", "BabaYagaETC", "JobApplication",  # W1 Rare Drops
        "DesertA1b", "DesertA3b", "MidnightCookie",  # W2 Rare Drops
        "SnowA2a", "SnowB2a", "SnowC4a",  # W3 Rare Drops
        "GalaxyA2b", "GalaxyC1b",  # W4 Rare Drops
        "LavaA1b", "LavaA5b", "LavaB3b",  # W5 Rare Drops
        "SpiA2b", "SpiB2b",  # W6 Rare Drops
        "EfauntDrop1", "EfauntDrop2", "Chiz0", "Chiz1", "TrollPart", "KrukPart", "KrukPart2",  # World Boss Materials
        "CraftMat2",  # Crimson String
        "OilBarrel1", "OilBarrel3", "OilBarrel4", "OilBarrel5",  # Oil Barrels
        "PureWater2",  # Alchemy Dense water
        "Quest1", "Quest2", "Quest5", "Quest6", "Quest8", "Quest10", "Quest11", "Quest13", "Quest16", "Quest17", "Quest18", "Quest20", "Quest25",
        "Quest26", "Quest27", "Quest28", "Quest29", "Quest30", "Quest31", "Quest33", "Quest34", "Quest36", "Quest37", "Quest38", "Quest39", "Quest40",
        "Quest41", "Quest42", "Quest43", "Quest44", "Quest45", "Quest46", "Quest47", "Quest48", "Quest49", "Quest50", "Quest9",
        "Mayo", "Trash", "Trash2", "Trash3",  # Treasure Hunt rewards
        "Meatloaf", "FoodHealth5",  #Small quantity foods
        "BobJoePickle", "BallJoePickle", "BoneJoePickle",  #Pickles
        "FoodPotYe1", "FoodPotYe3",  # EXP 1 and 3
        "FoodEvent1", "FoodEvent2", "FoodEvent3", "FoodEvent4", "FoodEvent5", "FoodEvent6", "FoodEvent7", "FoodEvent8",  # Event Foods
        "Pearl1", "Pearl2", "Pearl3", "Pearl4", "Pearl5", "Pearl6",  # Skilling Speed Pearls, EXP pearls
        "Line1", "Line2", "Line3", "Line4", "Line5", "Line6", "Line7", "Line8", "Line9", "Line10", "Line11", "Line12", "Line13", "Line14",  # Fishing Lines
        "ExpBalloon1", "ExpBalloon2", "ExpBalloon3",  # Experience Balloons
        "Timecandy1", "Timecandy2", "Timecandy3", "Timecandy4", "Timecandy5", "Timecandy6", "Timecandy7", "Timecandy8", "Timecandy9",  # Time Candies
        "PetEgg", "Whetstone", "Quest72", "Quest73", "Quest76", "Quest77",  # Other Time Skips
        "Quest70", "Quest71", "Quest75", "Gfoodcoupon", "ItemsCoupon1", "ItemsCoupon2",  # Loot Bags
        "FoodHealth8", "Quest69", "Quest74",  # Unobtainables
        "EquipmentStatues6", "EquipmentStatues15",  # Kachow and Bullseye
        "EquipmentStatues9",  # Oceanman Statue only comes from Catching
        "EquipmentStatues16", "EquipmentStatues17", "EquipmentStatues18", "EquipmentStatues19",  # W3 Statues
        "EquipmentStatues20", "EquipmentStatues21", "EquipmentStatues22", "EquipmentStatues23", "EquipmentStatues24",
        "EquipmentStatues25",  # W4 and W5 Statues
        "FoodG1", "FoodG2", "FoodG3", "FoodG4", "FoodG5", "FoodG6", "FoodG7", "FoodG8", "FoodG10",  # Gold Foods
        "ResetFrag", "ResetCompleted", "ResetCompletedS", "ClassSwap",
        "ClassSwapB", "ResetBox",
    ]
}

card_data = {
    "Blunder Hills": {
        "Crystal0": ["Crystal Carrot", 3],
        "acorn": ["Nutto", 10],
        "beanG": ["Bored Bean", 7],
        "branch": ["Walking Stick", 10],
        "carrotO": ["Carrotman", 10],
        "frogBIG": ["Gigafrog", 10],
        "frogG": ["Frog", 6],
        "goblinG": ["Glublin", 10],
        "mushG": ["Green Mushroom", 5],
        "mushR": ["Red Mushroom", 10],
        "mushW": ["Wood Mushroom", 10],
        "plank": ["Wode Board", 10],
        "poopSmall": ["Poop", 10],
        "ratB": ["Rat", 10],
        "slimeG": ["Slime", 8],
        "snakeG": ["Baby Boa", 9],
    },
    "Yum-Yum Desert": {
        "Bandit_Bob": ["Bandit Bob", 1],
        "Crystal1": ["Crystal Crabal", 3],
        "coconut": ["Mafioso", 10],
        "crabcake": ["Crabcake", 10],
        "jarSand": ["Sandy Pot", 10],
        "mimicA": ["Mimic", 10],
        "moonman": ["Moonmoon", 10],
        "pincermin": ["Pincermin", 10],
        "potato": ["Mashed Potato", 10],
        "sandcastle": ["Sand Castle", 10],
        "sandgiant": ["Sand Giant", 10],
        "shovelR": ["Dig Doug", 10],
        "snailZ": ["Snelbie", 10],
        "steak": ["Tyson", 10],
    },
    "Easy Resources": {
        "BirchTree": ["Bleach Logs", 10],
        "Bug1": ["Fly", 10],
        "Bug2": ["Butterfly", 10],
        "Copper": ["Copper Ore", 10],
        "Fish1": ["Goldfish", 10],
        "Fish2": ["Hermit Can", 10],
        "Fish3": ["Jellyfish", 10],
        "ForestTree": ["Forest Fibres", 10],
        "ForgeA": ["Fire Forge", 10],
        "Gold": ["Gold Ore", 10],
        "Iron": ["Iron Ore", 10],
        "JungleTree": ["Jungle Logs", 10],
        "OakTree": ["Oak Logs", 10],
    },
    "Medium Resources": {
        "Bug3": ["Sentient Cereal", 10],
        "Bug4": ["Fruitfly", 10],
        "CritterCard1": ["Froge", 4],
        "CritterCard2": ["Crabbo", 4],
        "CritterCard3": ["Scorpie", 4],
        "Dementia": ["Dementia Ore", 10],
        "Fish4": ["Bloach", 10],
        "ForgeB": ["Cinder Forge", 10],
        "PalmTree": ["Tropilogs", 10],
        "Plat": ["Platinum Ore", 10],
        "SoulCard1": ["Forest Soul", 3],
        "SoulCard2": ["Dune Soul", 3],
        "StumpTree": ["Veiny Logs", 10],
        "ToiletTree": ["Potty Rolls", 10],
        "Void": ["Void Ore", 10],
    },
    "Frostbite Tundra": {
        "Crystal2": ["Crystal Cattle", 10],
        "bloque": ["Bloque", 14],
        "eye": ["Neyeptune", 17],
        "flake": ["Frost Flake", 12],
        "glass": ["Quenchie", 17],
        "mamoth": ["Mamooth", 15],
        "penguin": ["Penguin", 15],
        "ram": ["Dedotated Ram", 20],
        "sheep": ["Sheepie", 11],
        "skele": ["Xylobone", 15],
        "skele2": ["Bloodbone", 15],
        "snakeB": ["Cryosnake", 17],
        "snowball": ["Snowman", 15],
        "speaker": ["Bop Box", 17],
        "stache": ["Sir Stache", 13],
        "thermostat": ["Thermister", 15],
    },
    "Hard Resources": {
        "AlienTree": ["Alien Hive Chunk", 10],
        "Bug10": ["Dust Mote", 15],
        "Bug12": ["Ladybug", 15],
        "Bug13": ["Firefly", 15],
        "Bug5": ["Mosquisnow", 10],
        "Bug6": ["Flycicle", 10],
        "Bug7": ["Worker Bee", 10],
        "Bug8": ["Fairy", 10],
        "Bug9": ["Scarab", 12],
        "CritterCard10": ["Blobfish", 12],
        "CritterCard4": ["Mousey", 4],
        "CritterCard5": ["Owlio", 4],
        "CritterCard6": ["Pingy", 5],
        "CritterCard7": ["Bunny", 6],
        "CritterCard8": ["Dung Beat", 7],
        "CritterCard9": ["Honker", 9],
        "Dreadlo": ["Dreadlo Ore", 15],
        "Fish10": ["Shellfish", 18],
        "Fish11": ["Jumbo Shrimp", 24],
        "Fish12": ["Caulifish", 30],
        "Fish5": ["Skelefish", 8],
        "Fish6": ["Sand Shark", 10],
        "Fish7": ["Manta Ray", 10],
        "Fish8": ["Kraken", 10],
        "Fish9": ["Icefish", 15],
        "Godshard": ["Godshard Ore", 400],
        "Lustre": ["Lustre Ore", 10],
        "SaharanFoal": ["Tundra Logs", 10],
        "SoulCard3": ["Rooted Soul", 3],
        "SoulCard4": ["Frigid Soul", 4],
        "SoulCard5": ["Squishy Soul", 5],
        "SoulCard6": ["Oozie Soul", 7],
        "SoulCard7": ["Breezy Soul", 7],
        "Starfire": ["Starfire Ore", 12],
        "Tree10": ["Dandielogs", 15],
        "Tree12": ["Bamboo Logs", 15],
        "Tree13": ["Effervescent Logs", 15],
        "Tree7": ["Wispy Lumber", 10],
        "Tree8": ["Cubed Logs", 10],
        "Tree9": ["Maple Logs", 12],
    },
    "Hyperion Nebula": {
        "Crystal3": ["Crystal Custard", 10],
        "demonP": ["Demon Genie", 19],
        "mushP": ["Purp Mushroom", 15],
        "w4a2": ["TV", 17],
        "w4a3": ["Donut", 18],
        "w4b1": ["Flying Worm", 21],
        "w4b2": ["Soda Can", 20],
        "w4b3": ["Gelatinous Cuboid", 22],
        "w4b4": ["Choccie", 23],
        "w4b5": ["Biggole Wurm", 24],
        "w4c1": ["Clammie", 26],
        "w4c2": ["Octodar", 27],
        "w4c3": ["Flombeige", 28],
        "w4c4": ["Stilted Seeker", 30],
    },
    "Smolderin' Plateau": {
        "Crystal4": ["Crystal Capybara", 15],
        "w5a1": ["Suggma", 25],
        "w5a2": ["Maccie", 28],
        "w5a3": ["Mister Brightside", 32],
        "w5a4": ["Cheese Nub", 35],
        "w5a5": ["Stiltmole", 45],
        "w5b1": ["Molti", 48],
        "w5b2": ["Purgatory Stalker", 52],
        "w5b3": ["Citringe", 60],
        "w5b4": ["Lampar", 65],
        "w5b5": ["Fire Spirit", 70],
        "w5b6": ["Biggole Mole", 75],
        "w5c1": ["Crawler", 80],
        "w5c2": ["Tremor Wurm", 100],
    },
    "Spirited Valley": {
        "Crystal5": ["Crystal Candalight", 5000],
        "w6a1": ["Sprout Spirit", 50],
        "w6a2": ["Ricecake", 60],
        "w6a3": ["River Spirit", 75],
        "w6a4": ["Baby Troll", 85],
        "w6a5": ["Woodlin Spirit", 100],
        "w6b1": ["Bamboo Spirit", 150],
        "w6b2": ["Lantern Spirit", 170],
        "w6b3": ["Mama Troll", 200],
        "w6b4": ["Leek Spirit", 250],
        "w6c1": ["Ceramic Spirit", 400],
        "w6c2": ["Skydoggie Spirit", 500],
        "w6d1": ["Royal Egg", 900],
        "w6d2": ["Minichief Spirit", 1300],
        "w6d3": ["Samurai Guardian", 2500],
    },
    "Dungeons": {
        "cactus": ["Cactopunk", 2],
        "frogD": ["Globohopper", 2],
        "frogGG": ["Eldritch Croaker", 5],
        "frogGR": ["Grandfrogger", 1.5],
        "frogGR2": ["Rotting Grandfrogger", 1.5],
        "frogGR3": ["Forlorn Grandfrogger", 1.5],
        "frogGR4": ["Vengeful Grandfrogger", 1],
        "frogP": ["Poisonic Frog", 1.5],
        "frogR": ["Lava Slimer", 2],
        "frogW": ["Chromatium Frog", 3],
        "frogY": ["King Frog", 2],
        "iceBossZ": ["Glaciaxus", 2],
        "iceBossZ2": ["Golden Glaciaxus", 1.5],
        "iceBossZ3": ["Caustic Glaciaxus", 1.5],
        "iceknight": ["Ice Guard", 8],
        "potatoB": ["Crescent Spud", 5],
        "rocky": ["Grumblo", 2],
        "snakeZ": ["Snakenhotep", 1.5],
        "snakeZ2": ["Enraged Snakenhotep", 1.5],
        "snakeZ3": ["Inevitable Snakenhotep", 1.5],
        "steakR": ["Beefie", 2],
        "target": ["Target", 2],
        "totem": ["Lazlo", 2],
    },
    "Bosses n Nightmares": {
        "Boss2A": ["Efaunt", 1.5],
        "Boss2B": ["Chaotic Efaunt", 1.5],
        "Boss2C": ["Gilded Efaunt", 11],
        "Boss3A": ["Chizoar", 1.5],
        "Boss3B": ["Chaotic Chizoar", 1.5],
        "Boss3C": ["Blighted Chizoar", 12],
        "Boss4A": ["Massive Troll", 2],
        "Boss4B": ["Chaotic Troll", 2],
        "Boss4C": ["Blitzkrieg Troll", 4],
        "Boss5A": ["Kattlekruk", 3],
        "Boss5B": ["Chaotic Kattlekruk", 4],
        "Boss5C": ["Sacrilegious Kattlekruk", 5],
        "Boss6A": ["Emperor", 6],
        "Boss6B": ["Chaotic Emperor", 9],
        "Boss6C": ["Sovereign Emperor", 13],
        "babaHour": ["Biggie Hours", 1.5],
        "babaMummy": ["King Doot", 1.5],
        "babayaga": ["Baba Yaga", 1.5],
        "mini3a": ["Dilapidated Slush", 5],
        "mini4a": ["Mutated Mush", 5],
        "poopBig": ["Dr Defecaus", 1.5],
        "poopD": ["Boop", 1],
        "wolfA": ["Amarok", 1.5],
        "wolfB": ["Chaotic Amarok", 1.5],
        "wolfC": ["Radiant Amarok", 10],
        "mini5a": ["Domeo Magmus", 4],
        "mini6a": ["Demented Spiritlord", 5]
    },
    "Events": {
        "EasterEvent1": ["Egggulyte", 1.5],
        "EasterEvent2": ["Egg Capsule", 1.5],
        "SummerEvent1": ["Coastiolyte", 8],
        "SummerEvent2": ["Summer Spirit", 8],
        "crabcakeB": ["Mr Blueberry", 4],
        "fallEvent1": ["Falloween Pumpkin", 3],
        "ghost": ["Ghost (Event)", 2],
        "loveEvent": ["Loveulyte", 1.5],
        "loveEvent2": ["Chocco Box", 1.5],
        "loveEvent3": ["Giant Rose", 1.5],
        "sheepB": ["Floofie", 3],
        "shovelY": ["Plasti Doug", 4],
        "slimeR": ["Valentslime", 2],
        "snakeY": ["Shell Snake", 3],
        "springEvent1": ["Bubbulyte", 1],
        "springEvent2": ["Spring Splendor", 1],
        "xmasEvent": ["Giftmas Blobulyte", 1.5],
        "xmasEvent2": ["Meaning of Giftmas", 1.5],
        "xmasEvent3": ["Golden Giftmas Box", 1],
    },
}

numberOfSecretClasses = 3  # Last verified as of v2.10
humanReadableClasses = {
    1: "Beginner",
    2: "Journeyman",
    3: "Maestro",
    4: "Voidwalker",
    5: "Infinilyte",
    6: "Rage Basics",
    7: "Warrior",
    8: "Barbarian",
    9: "Squire",
    10: "Blood Berserker",
    11: "Death Bringer",
    12: "Divine Knight",
    13: "Royal Guardian",
    18: "Calm Basics",
    19: "Archer",
    20: "Bowman",
    21: "Hunter",
    22: "Siege Breaker",
    23: "Mayheim",
    24: "Wind Walker",
    25: "Beast Master",
    30: "Savvy Basics",
    31: "Mage",
    32: "Wizard",
    33: "Shaman",
    34: "Elemental Sorcerer",
    35: "Spiritual Monk",
    36: "Bubonic Conjuror",
    37: "Arcane Cultist"
}

skillIndexList = ["Combat",
                  "Mining", "Smithing", "Choppin",
                  "Fishing", "Alchemy", "Catching",
                  "Trapping", "Construction", "Worship",
                  "Cooking", "Breeding", "Lab",
                  "Sailing", "Divinity", "Gaming",
                  "Farming", "Sneaking", "Summoning"]
emptySkillList = [0] * 25

expectedInventoryBagValuesDict = {
    0:1,
    1:1,
    2:1,
    3:2,
    4:2,
    5:2,
    6:2,
    7:2,
    20:4,
    21:4,
    22:4,
    23:4,
    24:4,
    25:4,
    100:2,
    101:2,
    102:4,
    103:4,
    104:1,
    105:1,
    106:1,
    107:1,
    108:2,
    109:3,
    110:1,
    111:3,
}
expectedStorageChestValuesDict = {
    0:3,
    1:3,
    2:3,
    3:3,
    4:3,
    5:4,
    6:4,
    7:4,
    8:4,
    9:5,
    10:5,
    11:5,
    12:5,
    13:6,
    14:5,
    15:6,
    16:6,
    17:6,
    18:6,
    19:7,
    20:7,
    21:8,
    22:9,
    23:9,
    24:9,
    25:9,
    26:9,
    27:10,
    30:9,
    31:9,
    32:9,
    33:9,
    34:9,
    35:9,
    36:9,
    37:9,
    38:9,
    39:9,
    40:9,
    41:9,
    100:3,
    101:3,
    102:4,
    103:4,
    104:3,
}
gemShopDict = {
    #Inventory and Storage
    'Item Backpack Space': 0,
    'Storage Chest Space': 0,
    'Carry Capacity': 0,
    'Food Slot': 0,
    'More Storage Space': 0,
    'Card Presets': 0,

    #Dailies N' Resets
    'Daily Teleports': 0,
    'Daily Minigame Plays': 0,

    #Cards
    'Extra Card Slot': 0,

    #Goods & Services
    'Weekly Dungeon Boosters': 0,

    #World 1&2
    'Infinity Hammer': 0,
    'Brimstone Forge Slot': 0,
    'Ivory Bubble Cauldrons': 0,
    'Bleach Liquid Cauldrons': 0,
    'Obol Storage Space': 0,
    'Sigil Supercharge': 0,

    #World 3
    'Crystal 3d Printer': 0,
    'More Sample Spaces': 0,
    'Burning Bad Books': 0,
    'Prayer Slots': 0,
    'Zen Cogs': 0,
    'Cog Inventory Space': 0,
    'Tower Building Slots': 0,
    'Fluorescent Flaggies': 0,

    #World 4
    'Royal Egg Cap': 0,
    'Richelin Kitchen': 0,
    'Souped Up Tube': 0,
    'Pet Storage': 0,
    'Fenceyard Space': 0,

    #World 5
    'Chest Sluggo': 0,
    'Divinity Sparkie': 0,
    'Golden Sprinkler': 0,
    'Lava Sprouts': 0,

    #World 6
    'Plot of Land': 0,
    'Pristine Charm': 0,
    'Shroom Familiar': 0,
    'Sand of Time': 0,
    'Instagrow Generator': 0,
    'Life Refill': 0,
    'Compost Bag': 0,
    'Summoner Stone': 0,

    #Fomo
    'FOMO-1': 0,
    'FOMO-2': 0,
    'FOMO-3': 0,
    'FOMO-4': 0,
    'FOMO-5': 0,
    'FOMO-6': 0,
    'FOMO-7': 0,
    'FOMO-8': 0
    }  # Default 0s
guildBonusesList = [
    "Guild Gifts", "Stat Runes", "Rucksack", "Power of Pow", "REM Fighting", "Make or Break",
    "Multi Tool", "Sleepy Skiller", "Coin Supercharger", "Bonus GP for small guilds", "Gold Charm", "Star Dazzle",
    "C2 Card Spotter", "Bestone", "Skilley Skillet", "Craps", "Anotha One", "Wait A Minute"
]
familyBonusClassTierLevelReductions = [10, 30, 70, 999]
familyBonusesDict = {
    #"Beginner": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Journeyman": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Luck', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Maestro": {'funcType': 'decay', 'x1': 6, 'x2': 100, 'Stat': 'Printer Sample Rate', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[1]},
    "Voidwalker": {'funcType': 'decay', 'x1': 5, 'x2': 250, 'Stat': 'Fighting AFK Gains', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[2]},
    #"Infinilyte": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    #"Rage Basics": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Warrior": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Strength', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Barbarian": {'funcType': 'decay', 'x1': 25, 'x2': 100, 'Stat': 'Weapon Power', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[1]},
    "Squire": {'funcType': 'decay', 'x1': 40, 'x2': 100, 'Stat': 'Total HP', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[1]},
    "Blood Berserker": {'funcType': 'decay', 'x1': 20, 'x2': 180, 'Stat': 'Total Damage', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[2]},
    #"Death Bringer": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Divine Knight": {'funcType': 'decay', 'x1': 50, 'x2': 150, 'Stat': 'Refinery Speed', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[2]},
    #"Royal Guardian": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    #"Calm Basics": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Archer": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Agility', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Bowman": {'funcType': 'decay', 'x1': 38, 'x2': 100, 'Stat': 'EXP when fighting monsters actively', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[1]},
    "Hunter": {'funcType': 'decay', 'x1': 30, 'x2': 100, 'Stat': 'Efficiency for all skills', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[1]},
    "Siege Breaker": {'funcType': 'decay', 'x1': 20, 'x2': 170, 'Stat': 'Faster Minimum Boat Travel Time', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[2]},
    #"Mayheim": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    #"Wind Walker": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Beast Master": {'funcType': 'decay', 'x1': 5, 'x2': 180, 'Stat': 'All Skill AFK Gains', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[2]},
    #"Savvy Basics": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Mage": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Wisdom', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Wizard": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 6, 'Stat': 'Star Talent Points', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[1]},
    "Shaman": {'funcType': 'decayMulti', 'x1': 0.4, 'x2': 100, 'Stat': 'Higher Bonuses from Golden Foods', 'PrePlus': False, 'PostDisplay': 'x', 'levelDiscount': familyBonusClassTierLevelReductions[1]},
    "Elemental Sorcerer": {'funcType': 'decay', 'x1': 20, 'x2': 350, 'Stat': 'Lv For All Talents Above Lv 1', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[2]},
    #"Spiritual Monk": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
    "Bubonic Conjuror": {'funcType': 'decay', 'x1': 5, 'x2': 180, 'Stat': 'All Stat. STR, AGI, WIS, LUK.', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': familyBonusClassTierLevelReductions[2]},
    #"Arcane Cultist": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': familyBonusClassTierLevelReductions[0]},
}
esFamilyBonusBreakpointsList = [0, 88, 108, 131, 157, 186, 219, 258, 303, 356, 419, 497, 594, 719, 885, 1118, 1468, 2049, 3210, 6681, 1272447]
printerIndexesBeingPrintedByCharacterIndex = [
    [5, 6],  #Character Index 0
    [12, 13],
    [19, 20],
    [26, 27],
    [33, 34],
    [40, 41],  #Character Index 5
    [47, 48],
    [54, 55],
    [61, 62],
    [68, 69],  #Character Index 9
]
#This flattens the above list of lists. Nested list comprehension sucks to read
printerAllIndexesBeingPrinted = [index for characterIndex in printerIndexesBeingPrintedByCharacterIndex for index in characterIndex]

def getNextESFamilyBreakpoint(currentLevel: int) -> int:
    result = -1
    for requirement in esFamilyBonusBreakpointsList:
        try:
            if currentLevel > requirement:
                result += 1
            else:
                break
        except:
            continue
    try:
        return esFamilyBonusBreakpointsList[result+1]
    except:
        return esFamilyBonusBreakpointsList[-1]


#achievementsList last pulled from code in 2.08. Search for: RegAchieves = function ()
#Replace: "], ["  with:  "],\n["  before pasting in
achievementsList = [
    ["Learn_2_Forge", "1", "Get_the_mining_certificate_from_Glumlee.", "*STEAM_EXCLUSIVE_&*10_gems_&*1hr_time_candy", "0"],
    ["Another_Me!", "1", "Create_a_2nd_character._Trust_me,_you_wanna_do_this_ASAP.", "*STEAM_EXCLUSIVE_&*8_gems", "0"],
    ["Sleepy_Gamer", "1", "Claim_100+_hours_of_AFK_rewards.", "*STEAM_EXCLUSIVE_&*5_gems_&*1hr_time_candy", "0"],
    ["Classy!", "1", "Choose_one_of_the_3_starting_classes_from_Promotheus.", "*STEAM_EXCLUSIVE_&*18_gems_&*2hr_time_candy", "0"],
    ["Hitting_the_Mark", "1", "Chop_15_yellow_sections_in_a_row_during_the_Choppin'_Minigame.", "{5%_Chopping_EXP_for_&all_character", "0"],
    ["Learn_2_Entertain", "1", "Get_the_golden_jam_from_the_Picnic_Stowaway.", "*STEAM_EXCLUSIVE_&*15_gems_&*2hr_time_candy", "0"],
    ["5_'hunned_Copper", "1", "Have_a_stack_of_exactly_500_Copper_Ore_in_your_Storage_Chest.", "*RNG_Item_unlock", "0"],
    ["Rookie_Player", "1", "Reach_level_20_on_any_character.", "*STEAM_EXCLUSIVE_&*8_gems", "0"],
    ["1.5_Ki'log'grams", "1", "Have_a_stack_of_exactly_1500_Oak_Logs_in_your_Storage_Chest.", "*RNG_Item_unlock", "0"],
    ["Small_Savings", "1", "Save_up_10000_coins.", "*STEAM_EXCLUSIVE_&*8_gems", "0"],
    ["Copper_Quipment", "1", "Equip_the_Copper_Helmet_and_Copper_Platebody", "*RNG_Item_unlock", "0"],
    ["The_Sculpture_Within", "1", "Buy_the_Sculpting_Tools_from_the_Blunder_Hills_town_shop", "*STEAM_EXCLUSIVE_&*10_gems", "0"],
    ["Card_Collector", "1", "Collect_10_unique_cards._They_drop_randomly_from_monsters!", "*STEAM_EXCLUSIVE_&*8_gems_", "0"],
    ["Do_What_You're_Told", "1", "Complete_25_unique_quests._Unique_here_means_different,_not_interesting_btw_lol", "*STEAM_EXCLUSIVE_&*8_gems", "0"],
    ["Learn_2_Translate", "1", "Get_the_scouting_report_from_Stiltzcho,_the_friendly_jungle_leaf", "*STEAM_EXCLUSIVE_&*20_gems_&*2_'2hr_time_candy'", "0"],
    ["Wode_Together", "250", "Defeat_250_Wode_Boards_with_at_least_1_other_party_member", "*RNG_Item_unlock", "0"],
    ["2_Tons_of_Iron", "1", "Have_a_stack_of_exactly_2,000_Iron_Ore_in_your_Storage_Chest.", "*RNG_Item_unlock", "0"],
    ["Giga_Decimation", "1", "Defeat_all_Giga_Frogs_before_any_respawn.", "*Encroaching_Forest_BG_&for_Title_Screen", "0"],
    ["Shut_it_Poochy", "1", "Defeat_Amarok,_the_stone_golem_wolf_of_the_Encroaching_Forest.", "*RNG_Item_unlock", "0"],
    ["Average_Player", "1", "Reach_level_40_on_any_character", "*STEAM_EXCLUSIVE_&*12_gems", "0"],
    ["Slimeicidal_Endeavor", "1", "Defeat_25,000_slimes_in_total._This_counts_kills_from_all_your_characters!", "*Jungle_Background_&for_Title_Screen", "0"],
    ["Right_to_Bear_Iron", "1", "Equip_an_Iron_Helmet,_Iron_Chestplate,_Iron_Pants,_and_one_Iron_Tool.", "*RNG_Item_unlock", "0"],
    ["5-6_Pick_up_Sticks", "1", "Have_a_stack_of_exactly_20,000_Sticks_in_your_Storage_Chest.", "*Tree_Interior_BG_&for_Title_Screen", "0"],
    ["20_Bundles_of_Jungle", "1", "Have_a_stack_of_exactly_20,000_Forest_Fibers_in_your_Storage_Chest.", "*RNG_Item_unlock", "0"],
    ["Colosseum_Contender", "1", "Get_a_score_of_25,000_or_more_in_the_Dewdrop_Colosseum.", "*RNG_Item_unlock", "0"],
    ["Crystal_Beatdown", "1", "Defeat_a_Crystal_monster,_who_have_a_1_in_2000_chance_of_spawning_when_a_monster_dies.",
    "*STEAM_EXCLUSIVE_&*8_gems_&*2_'1hr_time_candy'", "0"],
    ["Ten_Trips_of_Gold", "1", "Have_a_stack_of_exactly_30,000_Gold_Ore_in_your_Storage_Chest.", "*Mining_Cave_Background_&for_Title_Screen", "0"],
    ["Minecart_Maniac", "1", "Slam_on_a_yellow_ore_vein_in_the_Mining_Minigame,_which_gives_3_points!", "{5%_Mining_EXP_Bonus_&for_all_characters", "0"],
    ["Spike_Minigame_Master", "1", "Get_a_score_of_13_in_the_spike_minigame._Remember_to_say_'If_u_love_me_let_me_go'",
    "*STEAM_EXCLUSIVE_&*20_gems_&*4hr_Time_Candy", "0"],
    ["Anvil_Expansion", "1", "Craft_the_anvil_expander,_and_unlock_a_new_tab_of_item_recipes!", "*STEAM_EXCLUSIVE_&*10_gems", "0"],
    ["Steppin'_on_the_Rats", "500", "Defeat_500_Rats_with_at_least_1_other_party_member", "*Sewers_BG", "0"],
    ["Tree_Top_Dropout", "1", "Reach_the_top_of_the_Giant_Tree_in_Blunder_Hills", "*STEAM_EXCLUSIVE_&*15_gems", "0"],
    ["Naked_and_Unafraid", "1", "Enter_the_Sewers_with_no_equipment_or_weapon,_and_defeat_a_sewer_poop._Don't_want_to_get_your_stuff_dirty!",
    "*RNG_item_unlock", "0"],
    ["House_Flipper", "1", "Defeat_Baba_Yaga_in_under_25_seconds_after_they_spawn_in_the_Birch_Enclave", "RNG_Item_unlock", "0"],
    ["Platinum_200G", "1", "Have_a_stack_of_exactly_200,000_Platinum_Ore_in_your_Storage_Chest.", "*W1_Boss_Key_EZ-Access", "0"],
    ["Guild_Member", "1", "Claim_500_GP_for_your_guild.", "*STEAM_EXCLUSIVE_&*14_gems", "0"],
    ["Boss_Buster", "1", "Defeat_both_minibosses_in_Blunder_Hills", "*STEAM_EXCLUSIVE_&*15_gems", "0"],
    ["Nutty_Crafter", "42", "Craft_42_golden_peanuts,_whatever_those_might_be!", "{5%_Gold_Food_Bonus_&for_all_characters", "0"],
    ["Minecart_Master", "1", "Get_a_score_of_103+_in_the_Mining_Minigame,_beating_the_developers_highscore!",
    "*STEAM_EXCLUSIVE_&*25_gems_&*2_'4hr_time_candy'", "0"],
    ["Choppin'_to_the_Beat", "1", "Get_a_score_of_141+_in_the_Choppin'_Minigame,_beating_the_developers_highscore!",
    "*STEAM_EXCLUSIVE_&*25_gems_&*4hr_time_candy", "0"],
    ["Decked_Out_in_Gold", "1", "Equip_Golden_Helmet,_Chestplate,_Pants,_Shoes,_two_Golden_tools,_and_the_Defenders_Dignity_ring.", "*{3%_Arcade_balls/hr",
    "0"],
    ["Nice_Fur_Suit", "1", "Equip_all_4_pieces_of_Amarok_armor.", "*Forest_Villa_Teleport", "0"],
    ["Half_a_Mill-log", "1", "Have_a_stack_of_exactly_500,000_Veiny_Logs_in_your_Storage_Chest.", "*W1_Colosseum_EZ-Access_&*W1_Shops_EZ-Access", "0"],
    ["Bad_Doggy!", "1", "Defeat_Chaotic_Amarok.", "*STEAM_EXCLUSIVE_&*25_gems_&*2_'2hr_time_candy'", "0"],
    ["Two-Time_Savior", "2", "Equip_the_Blunder_Hero_Trophy,_while_also_having_another_in_your_inventory.", "{5%_Faster_Respawn_for_&all_Blunder_Hills_mobs",
    "0"],
    ["Million_Null_'n_Void", "1", "Have_a_stack_of_exactly_1,000,000_Void_Ore_in_your_Storage_Chest.", "*Deep_Mining_Teleport", "0"],
    ["Lucky_7s", "1", "SECRET_ACHIEVEMENT_------------------------_Punch_a_monster,_win_the_Jackpot!_Well,_hypothetically...",
    "*{1%_Arcade_balls/hr_&*15_Gems_&*7_'1hr_time_candy'", "0"],
    ["What_a_View!", "1", "SECRET_ACHIEVEMENT_------------------------_Climb_the_2nd_tallest_tree_in_all_of_Blunder_Hills,_and_say_'Great_view,_1_star'",
    "*{1%_Arcade_balls/hr", "0"],
    ["Cavernous_Nook", "1", "-", "*Knowledge_of_the_&Cavern_Secret_Location", "0"],
    ["Seriousleaf-ast!", "1", "SECRET_ACHIEVEMENT_------------------------_Score_a_point_in_the_Choppin'_Minigame_while_the_leaf_is_zooming_at_hyperspeed",
    "*{1%_Arcade_balls/hr", "0"],
    ["Peanut_Pioneer", "1", "SECRET_ACHIEVEMENT_------------------------_Talk_to_the_jungle_bush,_join_the_club...",
    "*STEAM_EXCLUSIVE_&*25_gems_&*2_'2hr_time_candy'", "0"],
    ["Meel_Time!", "1", "SECRET_ACHIEVEMENT_------------------------_Shake_it!_To_the_left,_to_the_left!_Oh_yea!!!", "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Pro_Gamer_Move", "1", "SECRET_ACHIEVEMENT_------------------------_Keep_the_oil._Precious,_precious_oil...",
    "*STEAM_EXCLUSIVE_&*10_gems_&*1hr_time_candy", "0"],
    ["Meet_the_Dev", "1", "SECRET_ACHIEVEMENT_------------------------_I_heard_he's_12_feet_tall_and_can_spawn_bosses_just_by_talking...",
    "*STEAM_EXCLUSIVE_&*40_gems_&*4_'2hr_time_candy'", "0"],
    ["Heyo!", "1", "Say_'Hi'_to_250_different_people_without_closing_the_game.", "*5_'Tab_1'_Talent_Pts_&*{1%_Arcade_balls/hr", "0"],
    ["Anothervil_Expansion", "1", "Craft_the_Anvil_III_expander._More_things_to_craft,_hooray!", "*STEAM_EXCLUSIVE_&*30_gems", "0"],
    ["Based_Roots", "20", "Reach_The_Roots,_which_is_the_map_below_the_Sticks_monsters_in_the_Giant_Tree", "*Acorn_Hat_Recipe", "0"],
    ["Dungeon_Pinch", "1", "Deal_100_or_more_damage_in_a_single_hit_in_any_party_dungeon.", "*{1%_Class_EXP_bonus_&for_all_characters", "0"],
    ["Big_Frog_Angry", "1", "Defeat_Grandfrogger_on_his_1st_Difficulty.", "*{2%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Big_Frog_Furious", "1", "Defeat_Grandfrogger_on_his_2nd_Difficulty.", "*{3%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Big_Frog_Big_Sad", "1", "Defeat_Grandfrogger_on_his_3rd_Difficulty.", "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["2_minute_meal", "1", "Spawn_Grandfrogger_within_2_minutes_of_entering_the_dungeon.", "*{3%_Class_EXP_bonus_&for_all_characters", "0"],
    ["Big_Frog_Big_Mad", "1", "Defeat_Grandfrogger_on_his_4th_Difficulty,_and_avoid_becoming_one_with_the_soup...",
    "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["Down_by_the_Desert", "1", "Reach_world_2!", "*STEAM_EXCLUSIVE_&*18_gems", "0"],
    ["Elite_Player", "1", "Reach_level_60_on_any_character", "*STEAM_EXCLUSIVE_&*16_gems", "0"],
    ["Retirement_Fund", "1", "Save_up_1,000,000_coins,_also_known_as_1_Platinum_coin!", "*STEAM_EXCLUSIVE_&*15_gems", "0"],
    ["More_and_More_Me!", "1", "Create_your_4th_character,_who_will_never_appreciate_the_struggle_your_first_3_characters_had.", "*STEAM_EXCLUSIVE_&*16_gems",
    "0"],
    ["Golden_Fly", "1", "Pass_through_the_small_golden_hoop_in_the_Catching_Minigame._It's_worth_3_points!", "*{5%_Catching_&Efficiency", "0"],
    ["Hammer_Bub", "1", "Level_up_the_'Hammer_Hammer'_Alchemy_bubble_to_Lv._10", "*RNG_item_unlock", "0"],
    ["Wassup_Yo!", "1", "Say_'Hi'_to_100_unique_people_without_closing_the_game_or_changing_Servers.", "*2_'Tab_2'_Talent_Pts_&*{2%_Arcade_balls/hr", "0"],
    ["Gold_School", "1", "Have_a_stack_of_exactly_1500_Goldfish_in_your_Storage_Chest.", "*{1%_Arcade_balls/hr", "0"],
    ["Buzz_Buzz", "1", "Have_a_stack_of_exactly_2500_Flies_in_your_Storage_Chest.", "*3_'Tab_2'_Talent_Pts", "0"],
    ["Careful,_it's_Sharp!", "1", "Have_a_stack_of_exactly_15_Glass_Shards_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Hybernation", "1", "Leave_one_of_your_players_AFK_for_an_entire_week,_which_is_168_hours!_Anything_more_counts_too!",
    "*{3%_Arcade_balls/hr_&*Good_nights_sleep", "0"],
    ["Vial_Noob", "1", "Get_3_vials_to_Lv._4,_which_are_the_green_ones", "*RNG_item_unlock", "0"],
    ["Specializational!", "2", "Choose_a_subclass_for_two_of_your_characters.", "*RNG_item_unlock", "0"],
    ["Obols_Oh_Boy!", "1", "Have_10_Silver_Obols_equipped_at_once._The_Family_tab_counts_here!", "{2%_Arcade_balls/hr", "0"],
    ["Well_Learned", "1", "Get_a_lv_92_or_higher_Star_Book_from_Alchemy!_The_1st_one,_specifically.", "*RNG_item_unlock", "0"],
    ["B-o-B_to_Help", "1", "Complete_75_unique_quests_on_a_single_character._I'm_not_sure_what_B-o-B_stands_for_either...", "*STEAM_EXCLUSIVE_&*16_gems", "0"],
    ["Card_Enthusiast", "1", "Collect_30_unique_cards._If_u_wanna_trade,_I_got_some_spare_Amarok_cards!", "*STEAM_EXCLUSIVE_&*16_gems", "0"],
    ["Efaunt_Trumped", "1", "Defeat_Efaunt,_the_Mummified_Elephant_God._He_will_remember_you_doing_this.", "*RNG_item_unlock", "0"],
    ["Fishing_Finesse", "1", "Get_a_score_of_67+_in_the_Fishing_Minigame,_beating_the_developers_highscore!",
    "*STEAM_EXCLUSIVE_&*25_gems_&*2_'4hr_time_candy'", "0"],
    ["Catching_Coronation", "1", "Get_a_score_of_128+_in_the_Catching_Minigame,_beating_the_developers_highscore!",
    "*STEAM_EXCLUSIVE_&*25_gems_&*4hr_time_candy", "0"],
    ["Crystal_Superslam", "1", "Defeat_100_Crystal_Mobs._This_could_go_a_couple_rounds...", "*STEAM_EXCLUSIVE_&*20_gems_&*2_'2hr_time_candy'", "0"],
    ["Slumbering_Gamer", "1", "Claim_2000+_hours_of_AFK_progress_across_all_characters._So_lazy!", "*STEAM_EXCLUSIVE_&*12_gems_&*'12hr_time_candy'", "0"],
    ["My_First_Trophy!", "1", "Equip_any_trophy,_other_than_the_limited_edition_ones_which_don't_count_lol.", "*STEAM_EXCLUSIVE_&*25_gems_&*'4hr_time_candy'",
    "0"],
    ["A_Fish_Too_Far", "1000", "Catch_a_total_of_1000_fish_across_all_Fishing_Minigame_plays.", "*Beach_Background_&for_Title_Screen", "0"],
    ["Rat-a-tat-tat", "1", "Level_up_the_'FMJ'_Alchemy_bubble_to_Lv._30", "*RNG_item_unlock", "0"],
    ["Pillars_of_Sand", "1", "Defeat_250,000_Sandy_Pots_combined_across_all_characters._Forget_the_Pillars_of_Salt_though.",
    "*Desert_Oasis_BG_&for_Title_Screen", "0"],
    ["Vial_Connoisseur", "1", "Get_6_vials_to_Lv._7,_which_are_the_pink_ones", "*RNG_item_unlock", "0"],
    ["Coarse_Cards", "1", "Level_up_cards_for_Mafioso,_Sandcastle,_Pincermin,_and_Mashed_Potato,_all_up_to_1_star.", "*Coarse_Mountains_BG_&for_Title_Screen",
    "0"],
    ["Trial_by_Time", "1", "Run_from_Town_to_Efaunt's_Tomb_in_under_2_minutes._No_teleporting_using_the_World_Map.", "*{2%_Arcade_balls/hr", "0"],
    ["Golden_Obolden!", "1", "Have_15_Golden_Obols_equipped_at_once._The_Family_tab_counts_here!", "{20%_Obol_Fragments_&gained_when_trashing_&obols", "0"],
    ["Monocle_No_More", "1", "Defeat_160_Sand_Giants_within_10_minutes_of_entering_the_map._Auto_must_be_off.", "*Twilight_Desert_BG_&for_Title_Screen", "0"],
    ["Jellyfish_Jelly", "1", "Have_a_stack_of_exactly_6000_Jellyfish_in_your_Storage_Chest._I_heard_their_Jelly_goes_good_with_burgers_btw.",
    "*RNG_item_unlock", "0"],
    ["Super_Cereal", "1", "Have_a_stack_of_exactly_50,000_Sentient_Cereal_in_your_Storage_Chest.", "*W2_Colosseum_EZ-Access_&*W2_Shops_EZ-Access", "0"],
    ["Sweet_Victory", "1", "Get_a_Score_of_200,000_or_more_in_the_Sandstone_Colosseum", "*{2%_Arcade_balls/hr", "0"],
    ["Ink_Blot", "101", "Use_101_silver_pens_in_the_Post_Office", "20%_chance_to_keep_&silver_pens_after_&using_one", "0"],
    ["Demon_Demolisher", "1", "Defeat_the_big_hourglass_and_the_toilet_paper_guy!", "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Dumbo_Destroyer", "1", "Defeat_Chaotic_Efaunt._Look_out_for_the_kick,_kapow!", "*STEAM_EXCLUSIVE_&*35_gems_&*2_'2hr_time_candy'", "0"],
    ["Threadin'_the_Needle", "1", "Pass_through_the_teenie_tiny_Lava_hoop_in_the_Catching_Minigame._It_only_appears_if_you_go_through_25_hoops_in_a_row!",
    "{5%_catching_EXP_for_&all_characters", "0"],
    ["S-M-R-T", "1", "Level_up_the_'Smarty_Boi'_Alchemy_bubble_to_Lv._50", "-10%_Bubble_upgrading_&costs", "0"],
    ["Two_Desserts!", "2", "Have_the_YumYum_Sheriff_trophy_equipped,_while_also_having_another_in_your_inventory.",
    "{5%_faster_respawn_for_&YumYum_Desert_Monsters", "0"],
    ["Nuget_Nightmare", "1", "Kill_Crabbycakes_manually,_without_Auto_on,_until_one_drops_a_Nuget_Cake._Good_luck...", "*Nuget_Cake_Hat_Recipe", "0"],
    ["Bigtime_Bloacher", "1", "Have_a_stack_of_exactly_100,000_Bloaches_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Vial_Junkee", "1", "Get_10_vials_to_Lv._9,_which_are_the_hyperlight_Orange_ones._Stop_focusing_so_much_on_vials,_it's_not_healthy!",
    "{20%_Sigil_Charging_&Speed", "0"],
    ["Fruit_Salad", "1", "Have_a_stack_of_exactly_1,000,000_Fruit_Flies_in_your_Storage_Chest.", "{5%_catching_speed_&for_all_characters", "0"],
    ["Your_Skin,_My_Skin", "1", "Wear_the_Efaunt_helmet,_Ribcage,_Hipillium,_and_Ankles._Also_have_1_Efaunt_Obol_equipped.", "*Djonnuttown_Teleport", "0"],
    ["WAAAAAAAHH!", "1",
    "SECRET_ACHIEVEMENT_------------------------_Complete_all_available_Treasure_Hunts!_You_can_find_them_on_Youtube,_just_search_for_it!",
    "*{3%_Arcade_balls/hr", "0"],
    ["Bobjoepicklejar", "1", "SECRET_ACHIEVEMENT_------------------------_Pickles_belong_in_containers,_after_all!", "*{1%_Arcade_balls/hr", "0"],
    ["Fish_Aint_Biting", "1", "SECRET_ACHIEVEMENT_------------------------_I'm_tellin'_ya,_the_fish_ain't_bitin'_today_gosh_darn_it!",
    "{5%_Fishing_Exp_for_&all_characters", "0"],
    ["Skill_Master", "1",
    "SECRET_ACHIEVEMENT_------------------------_Goldric's_bag_of_peanuts_may_be_nearly_empty,_but_even_just_one_peanut_is_enough_for_some...",
    "*W2_Boss_Key_EZ-Access", "0"],
    ["Tomb_Raider", "1", "Defeat_Snakenhotep_on_his_1st_Difficulty.", "*{2%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Tomb_Defiler", "1", "Defeat_Snakenhotep_on_his_2nd_Difficulty.", "*{3%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Tomb_Completionist", "1", "Defeat_Snakenhotep_on_his_3rd_Difficulty.", "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Wazzzzam!", "125", "Wazam_125_rooms_in_Snakenhotep's_Dungeon_by_performing_exceptionally_well_in_a_room.", "*{6%_Multikill_bonus_&for_all_characters",
    "0"],
    ["Just_Passing_By", "30", "Pass_30_rooms_in_Snakenhotep's_Dungeon_by_doing_the_thingy_the_room_says_to_do.", "*{2%_Multikill_bonus_&for_all_characters",
    "0"],
    ["Dungeon_Slap", "1", "Deal_1000_or_more_damage_in_a_single_hit_within_any_Dungeon.", "*{2%_Class_EXP_bonus_&for_all_characters", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["Snowy_Wonderland", "1", "Reach_World_3,_the_coolest_world_in_the_game!", "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Veteran_Gamer", "1", "Reach_level_80_on_any_character._I'm_glad_you're_enjoying_the_game,_hope_you_get_to_Lv._100!", "*STEAM_EXCLUSIVE_&*20_gems", "0"],
    ["A_Family_of_Me!", "1",
    "Create_your_8th_character,_who_will_never_get_the_love_you_gave_to_your_earlier_characters_when_making_new_ones_was_still_special.",
    "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Croakin'_Froge", "1", "Have_a_stack_of_exactly_250_Doge_-I_mean_froge-_critters_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Sad_Souls", "1", "Have_a_stack_of_exactly_1,000_Forest_Souls_in_your_Storage_Chest.", "*{1%_Arcade_balls/hr", "0"],
    ["Checkout_Takeout", "1000", "Checkout_a_total_of_1000_talent_books_from_the_Talent_Book_Library", "*{5_Book_Max_LV_&*{30%_Library_charge_&rate", "0"],
    ["Yawning_Cogs", "1", "Have_4_unclaimed_Yellow_Cogs_during_any_single_moment_in_time,_apart_from_March_16,_2022_at_3.07pm", "*{2%_Arcade_balls/hr", "0"],
    ["Blunder_Skull", "1", "Get_a_Copper_Skull_or_higher_on_every_Blunder_Hills_monster_in_the_Deathnote.", "*RNG_item_unlock", "0"],
    ["Too_Cute_To_Live", "1", "You're_gonna_kill_all_them_lil'_poofs?_You_monster..._well,_at_least_make_it_quick,_like_20s_or_less_after_entering_the_map.",
    "*{5%_Total_Multikill_&on_all_monsters", "0"],
    ["Big_Mobs_Eek", "5",
    "Defeat_5_Giant_Monsters._Giants_only_spawn_IF_you_equip_the_Titan_Tachion_prayer,_unlocked_by_beating_wave_10_of_Waka_Tower_Defence_(world_2)",
    "*STEAM_EXCLUSIVE_&*15_gems_&*2_'2hr_time_candy'", "0"],
    ["Powdered_Neutronium", "1", "Rank_up_the_Explosive_Combustion_refinery_chamber_to_Rank_2.", "*STEAM_EXCLUSIVE_&*15_gems_&*3_'2hr_time_candy'", "0"],
    ["Soulslike", "1", "Have_4_Prayers_in_your_Prayer_Rock_thingy._You_get_Prayers_by_placing_these_wizard_dudes_into_towers_and_stuff_and_kickin'_butt!",
    "*{2%_Arcade_balls/hr", "0"],
    ["Good_Times_Roll", "1", "Beat_wave_50_in_Glublin_Gorefest_using_ONLY_Boulder_Roller_wizards._No_freeze,_no_confetti,_just_boulder.", "*RNG_item_unlock",
    "0"],
    ["Cog_in_the_System", "1", "Have_20_Grey_Cogs_placed_on_the_board_at_once._Not_sure_why_this_is_an_achievement,_cogs_are_boring.",
    "*{5%_Build_Speed_&in_Construction", "0"],
    ["I_Create...", "1", "Upgrade_buildings_in_construction_a_total_of_50_times._Any_buildings,_utilities,_wizards,_shrines,_they_all_count!",
    "*{1%_Arcade_balls/hr", "0"],
    ["I_Sawed...", "1", "Upgrade_buildings_in_construction_a_total_of_250_times.", "*RNG_item_unlock", "0"],
    ["Hairy_Ice_Comb", "3000", "Manually_loot_1000_floof_poofs,_melty_cubes,_and_moustache_comb_stacks_--_AFK_claiming_doesn't_count.",
    "*Frosty_Peaks_BG_&for_Title_Screen", "0"],
    ["Giant_Slayer", "25", "Defeat_5_Giant_Mobs_of_each_type;_Bloque,_Mamooth,_Snowman,_Penguin,_Thermister._Do_it_in_that_monster_order.",
    "*Tundra_Outback_BG_&for_Title_Screen", "0"],
    ["Saharan_Skull", "1", "Get_a_Golden_Skull_or_higher_on_every_YumYum_Desert_monster_in_the_Deathnote.", "*{1%_Printer_Sample_&Rate", "0"],
    ["Fat_Souls", "1", "Have_a_stack_of_exactly_10,000_Dune_Souls_in_your_Storage_Chest.", "*Start_with_{15_&more_points_in_Worship_&Tower_Defence", "0"],
    ["Borrowed_Pens", "1", "Remember_all_those_pens_you_lent_out_in_school_and_never_got_back?_You've_got_13_seconds_to_vent_your_anger_on_every_penguin_mob!",
    "*{3%_Arcade_balls/hr", "0"],
    ["Large_Fortune", "1",
    "Save_up_100,000,000_coins._But_remember,_as_far_as_the_idleon_government_knows,_none_of_those_coins_came_from_a_taxable_income_wink_wink.",
    "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Sqeakin'_Mousey", "1",
    "Have_a_stack_of_exactly_60,000_Mouseys_in_your_Storage_Chest._Imagine_the_noise_in_that_chest_of_yours..._or_even_the_smell,_ugh.",
    "*Hunters_Grove_BG_&for_Title_Screen", "0"],
    ["Geared_for_Success", "1", "Have_40_Yellow_Cogs_placed_on_the_board_at_once._Alright_now_I_see_how_this_is_achievement_worthy,_cogs_are_kinda_neat.",
    "*{5%_Construction_EXP_&gain", "0"],
    ["Guild_Higher-Up", "1", "Contribute_3,000_GP_to_your_guild,_putting_you_above_the_other_guild_members_who_only_have_the_500_GP_Achievment!",
    "*STEAM_EXCLUSIVE_&*22_gems", "0"],
    ["Legendary_Gamer", "1", "Reach_level_100_on_any_character!_Just_4_more_digits_and_you'd_have_a_phone_number!", "*STEAM_EXCLUSIVE_&*23_gems", "0"],
    ["Entangled_Compounds", "1", "Rank_up_the_Spontaneous_Combustion_refinery_chamber_to_Rank_3.", "*{5_'Tab_3'_Talent_Pts", "0"],
    ["There_Can_Be_Only_1", "1", "Beat_wave_50_of_Wakawaka_War_without_using_more_than_1_of_any_specific_tower._Can't_have_2_pulsers,_or_2_frozones!",
    "*STEAM_EXCLUSIVE_&*25_gems_&*3_'12hr_time_candy'", "0"],
    ["Blurple_Skull", "1", "Get_a_Dementia_Skull_or_higher_on_every_Frostbite_Tundra_monster_in_the_Deathnote.",
    "*STEAM_EXCLUSIVE_&*30_gems_&*5_'72hr_time_candy'", "0"],
    ["Souped_Up_Salts", "1", "Rank_up_the_Redox_Combustion_refinery_chamber_to_Rank_10.", "*RNG_item_unlock", "0"],
    ["I_Constructed!", "1", "Upgrade_buildings_in_construction_a_total_of_900_times.", "*{10_'Tab_3'_Talent_Pts", "0"],
    ["Cogs_Be_Waitin'", "1", "Have_16_unclaimed_Grey_Cogs_at_once._Jeez,_I'm_glad_anthropomorphic_cogs_aren't_real.", "*{4%_Arcade_balls/hr", "0"],
    ["Simpin'_for_NPC's", "1", "Complete_150_unique_quests_on_a_single_character._Apparently_people_find_'simp'_offensive,_and_I'm_kinda_offended_by_that...",
    "*STEAM_EXCLUSIVE_&*24_gems", "0"],
    ["Top_Cogs", "1", "78_Cogs._All_purple_cogs._Did_I_say_cogs_are_great?_I_think_cogs_are_great._Cog_cog_cog!", "*W3_Boss_Key_EZ-Access", "0"],
    ["Card_Dude", "1", "Collect_120_unique_cards._Not_sure_why_something_as_mundane_as_'dude'_is_the_descriptor_here,_don't_read_too_much_into_it.",
    "*STEAM_EXCLUSIVE_&*24_gems", "0"],
    ["Crystal_Champ", "1", "Defeat_2000_crystal_mobs._You_must've_watched_a_whole_lotta_Dev_Streams_to_get_this!",
    "*STEAM_EXCLUSIVE_&*30_gems_&*12hr_time_candy", "0"],
    ["Smirky_Souls", "1", "Have_a_stack_of_exactly_250,000_Rooted_Souls_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Comatosed_Gamer", "1", "Claim_30,000+_Hrs_of_AFK_gains._Thats_two_years,_woah!", "*STEAM_EXCLUSIVE_&*25_gems_&*24hr_time_candy", "0"],
    ["Knock_on_Wood", "1", "Beat_wave_50_of_Acorn_Assault_with_just_4_towers_active._Place_down_a_5th_tower_at_any_time,_and_it_wont_count!",
    "*{3%_Arcade_balls/hr", "0"],
    ["The_Goose_is_Loose", "1", "Have_a_HONK_of_exactly_1,000,000_Honkers_in_your_HONK_Chest._HONKHONKHONK_HOOOONK!!!", "*HONK_Hat_Recipe", "0"],
    ["Sepia_Vision", "1", "Have_a_stack_of_exactly_500_Black_Lenses_in_your_Storage_Chest._Better_complete_this_before_I_make_it_1,000!",
    "*Crystal_Caverns_BG_&for_Title_Screen", "0"],
    ["Rattle_them_Bones", "1", "Defeat_every_Bloodbone_in_just_12_seconds_after_entering_the_map._Wow,_wild.", "*Pristalle_Lake_BG_&for_Title_Screen", "0"],
    ["A_Most_Nice_Sale", "1", "SECRET_ACHIEVEMENT_------------------------_You_SOLD_gems_to_the_World_3_town_store...?_All_at_once?_How_many...?_Nice.",
    "*STEAM_EXCLUSIVE_&*1_gem_&*1_'24hr_time_candy'", "0"],
    ["Cool_Score!", "1", "Get_a_Score_of_2,500,000_or_more_in_the_Chillsnap_Colosseum", "*W3_Colosseum_EZ-Access_&*W3_Shops_EZ-Access", "0"],
    ["Dungeon_Wallop", "1", "Deal_25000_or_more_damage_in_a_single_hit_within_any_Dungeon.", "*{4%_Crit_Chance_Bonus_&for_all_characters_&outside_of_dungeon",
    "0"],
    ["Boss_Defeated", "1", "Defeat_Glaciaxus_on_its_1st_difficulty", "*{2%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Manager_Defeated", "1", "Defeat_Glaciaxus_on_its_2nd_difficulty", "*{3%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Kingpin_Defeated", "1", "Defeat_Glaciaxus_on_its_3rd_difficulty", "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Capitalist_Win", "1000", "Complete_1000_jobs_within_the_Glacial_Basement_dungeon.", "*{5%_Class_EXP_for_all_&characters_outside_&of_dungeons", "0"],
    ["Equinox_Visitor", "1", "Find_the_Equinox_Mirror_drop_from_Bloodbones,_a_1_in_1000_drop,_and_use_it_to_visit_the_Equinox_Valley.",
    "*{4%_Total_DMG_for_all_&characters", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*STEAM_EXCLUSIVE_&*30_gems_&*Item3", "0"],
    ["Milky_Wayfarer", "1", "Reach_World_4,_the_purple_one_with_outer_space_stuff!", "*STEAM_EXCLUSIVE_&*RNG_item_unlock_&*Some_Gems_and_Candy", "0"],
    ["Channel_Surfing", "1", "Have_a_stack_of_exactly_75,000_TV_remotes_in_your_Storage_Chest.", "*Nebula_BG_&for_Title_Screen", "0"],
    ["Bottle_Capital", "1", "Have_a_stack_of_exactly_800,000_Bottle_Caps_in_your_Storage_Chest.", "*{10_Star_Tab_&Talent_Pts", "0"],
    ["Too_Many_Tentacles", "1", "Have_a_stack_of_exactly_10,000,000_Wriggly_Balls_in_your_Storage_Chest._Green_Stack_bro!", "*{3%_Arcade_balls/hr", "0"],
    ["Mythical_Gamer", "1", "Reach_level_125_on_any_character!_This_used_to_be_a_HUGE_deal,_now_it's_just_a_big_deal.", "*STEAM_EXCLUSIVE_&*30_gems", "0"],
    ["Matrix_Wickermen", "8760", "Accumulate_8760_hours,_or_an_entire_year,_of_Lab_AFK_time_across_all_players.", "*RNG_item_unlock", "0"],
    ["Bland_Dish", "1", "SECRET_ACHIEVEMENT_------------------------_What_exactly_were_you_expecting_to_cook,_an_invisible_meal?", "{6_Tab_1_&Talent_Pts",
    "0"],
    ["Lv._5_Nothing", "1", "SECRET_ACHIEVEMENT_------------------------_Ah,_I_see_you_enjoy_reading_upgrade_flavor_text_as_well!",
    "*STEAM_EXCLUSIVE_&*30_gems_&*2_'12hr_time_candy'", "0"],
    ["I_Like_This_Pet", "1", "Get_a_Breedability_III_heart_on_at_least_2_Pets_within_the_nest.", "Pet_Breedability_&multiplier_goes_up_&1.20x_faster", "0"],
    ["I_LOVE_These_Pets", "1", "Get_a_Breedability_VII_heart_on_at_least_15_pets_within_the_nest.", "{10_Tab_3_&Talent_Pts", "0"],
    ["Shiny_Shells", "1", "Have_6_bronze_(or_rarer)_eggs_in_your_nest_at_the_same_time,_waiting_to_be_hatched!", "{10%_Faster_Egg_&Incubator_Speed", "0"],
    ["Gilded_Shells", "1", "Have_12_gold_(or_rarer)_eggs_in_your_nest_at_the_same_time,_waiting_to_be_hatched!", "Eggs_increase_in_&rarity_1.10x_more_&often",
    "0"],
    ["Barley_Lost", "1", "Fail_a_pet_battle_with_the_enemy_team_having_only_5%_HP_or_less._Wait,_it's_spelled_HOW???", "{5%_Pet_Fight_&Damage", "0"],
    ["Petless", "1", "Trash_a_total_of_2500_pets._How_could_you_be_so_heartless,_so_cold...", "*STEAM_EXCLUSIVE_&*50_gems_&*1_'72hr_time_candy'", "0"],
    ["Cabbage_Patch", "1", "Have_5_kitchens_all_cooking_cabbages_at_the_same_time._Remember_gamers,_eat_your_vegetables,_they_ain't_so_bad!",
    "{10%_Meal_Cooking_&Speed", "0"],
    ["Le_Pretzel_Bleu", "1", "Have_8_kitchens_all_cooking_Pretzels_at_the_same_time._Don't_get_it_twisted,_them_pretzels_are_the_real_deal.",
    "{20%_Meal_Cooking_&Speed", "0"],
    ["Michelin_Ranked", "1", "Upgrade_any_kitchen_stat_to_Lv._300,_giving_you_an_elite_crown_over_the_upgrade_bars,_thus_resulting_in_dopamine.",
    "*RNG_item_unlock", "0"],
    ["WOAH_That's_Fast", "1", "Have_a_speed_of_'Too_Fast'_displayed_while_cooking_an_Eggplant._No_this_is_not_a_metaphor.", "*{2%_Arcade_balls/hr", "0"],
    ["Stars_Among_Stars", "1", "Complete_all_constellations_in_the_Hyperion_Nebula._Thats_what_world_4_is_called_btw.", "*Eternity_Beach_BG_&for_Title_Screen",
    "0"],
    ["Chippin'_Away", "25", "Claim_25_chips_from_the_Chip_Repository._I_was_gonna_make_this_250_chips,_but_people_from_the_future_told_me_not_to.",
    "*{2%_Arcade_balls/hr", "0"],
    ["Hunned_Times_a_Day", "10000", "Claim_spices_by_any_means_10,000_times._Like,_individual_claims.", "{8_Tab_2_&Talent_Pts", "0"],
    ["Good_Plate", "1", "Upgrade_a_meal_at_the_Dinner_Menu_to_the_point_where_it_gets_a_diamond_plate!", "*RNG_item_unlock_&*W4_Shops_EZ-Access", "0"],
    ["Great_Plate", "1", "Upgrade_a_meal_at_the_Dinner_Menu_to_the_point_where_it_gets_a_purple_plate!", "*{2%_Arcade_balls/hr", "0"],
    ["Best_Plate", "1", "Upgrade_a_meal_at_the_Dinner_Menu_to_the_point_where_it_gets_a_void_pearl_plate!",
    "-10%_lower_cost_&to_upgrade_meals_&at_the_Dinner_Table", "0"],
    ["Space_Party!!!", "1", "Dance_with_at_least_5_other_people_while_you're_all_in_World_4_town!", "*{2%_Arcade_balls/hr", "0"],
    ["Zero_G_Scorin'", "1", "Get_a_Score_of_10,000,000_or_more_in_the_Astro_Colosseum", "{5%_Cash_from_&Monsters", "0"],
    ["Hibernating_Gamer", "1", "Glaim_111,000_hours_of_AFK_time._Jeez,_thats_like_an_entire_year_of_all_characters_idling_to_the_max.",
    "*STEAM_EXCLUSIVE_&*100_gems_&*1_'72hr_time_candy'", "0"],
    ["Mutant_Massacrer", "1", "Defeat_both_Mutant_Minibosses,_the_W3_Slush_and_W4_Mush._You_must_defeat_Slush_before_Mush,_in_that_order.",
    "*STEAM_EXCLUSIVE_&*RNG_item_unlock_&*Some_Gems_and_Candy", "0"],
    ["Soda_Poisoning", "1", "Beat_wave_50_of_Clash_of_Cans_with_3_Poisonic_Elders_at_Lv_5_or_higher._Also,_you_can't_sell_towers.",
    "*Starfield_Belt_BG_&for_Title_Screen", "0"],
    ["The_True_King", "1000000", "Reach_a_total_of_1_million_Orb_Kills.", "{10_Tab_4_Talent_Pts", "0"],
    ["The_True_Pirate", "1000000", "Reach_a_total_of_1_million_Plunderous_Kills._This_one_is_the_true_challenge_of_the_three.",
    "{15_Tab_4_Talent_Pts_&{1%_Total_Dmg", "0"],
    ["The_True_Emperor", "1000000", "Reach_a_total_of_1_million_Wormhole_Kills.", "{12_Tab_4_Talent_Pts", "0"],
    ["Veritable_Master", "1",
    "SECRET_ACHIEVEMENT_------------------------_Destruction_comes_to_all_who_cross_your_path,_no_matter_how_many_times_you_cross_paths.",
    "{1_Void_Talent_Pt", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["Maple_Logger", "1", "Have_a_stack_of_exactly_200,000_Maple_Logs_in_your_Storage_Chest.", "{1%_Damage_for_all_&characters", "0"],
    ["Vitamin_D-licious", "1", "Have_a_stack_of_exactly_5,000,000_Orange_Slices_in_your_Storage_Chest.", "{50%_Forge_Ore_&Capacity", "0"],
    ["Wurm_Wumbo", "1", "Have_a_stack_of_exactly_100,000,000_Mongo_Worm_Slices_in_your_Storage_Chest.", "*Wurm_Catacombs_BG", "0"],
    ["Supernatural_Gamer", "1", "Reach_level_300_on_any_character!_My_oh_my!_This_would_have_been_inconceivable_just_a_few_years_ago!", "{10%_All_Skill_EXP",
    "0"],
    ["Smokin'_Stars", "1", "Complete_all_constellations_in_the_Smolderin'_Plateau._You_can_check_your_progress_within_the_Telescope.", "{20%_All_Skill_EXP",
    "0"],
    ["The_Plateauourist", "1", "Reach_World_5,_a_personal_favorite_world_of_mine!_Look,_I_like_lava_what_can_I_say.", "{4_Daily_Crystal_Mob_&Spawn_Guarantee",
    "0"],
    ["No_Krakens?_):", "1", "Reach_Wave_50_of_Citric_Conflict_tower_defence_without_placing_a_single_Kraken_Towers._Not_even_one.", "{25%_Class_EXP", "0"],
    ["Artifact_Finder", "1", "Collect_15_Artifacts_from_Sailing", "*1_Extra_Chest_Slot_in_&Sailing_Loot_Pile", "0"],
    ["Artifact_Enjoyer", "1", "Collect_all_30_Artifacts_from_Sailing", "*Magma_Rivertown_BG", "0"],
    ["Artifact_Jones", "1", "Collect_all_30_ANCIENT_Artifacts_from_Sailing._All_that_glitters_is_not_gold,_but_it_sure_is_shiny!", "{20_Star_Talent_Pts", "0"],
    ["Gilded_Vessel", "1", "Upgrade_a_boat_to_Lv_100_in_Sailing._It'll_turn_gold_to_reflect_its_power!", "*1_Extra_Chest_Slot_in_&Sailing_Loot_Pile", "0"],
    ["Maroon_Warship", "1", "Upgrade_a_boat_to_Lv_300_in_Sailing._This_is_the_pinnacle_of_naval_prowess,_it_doesn't_get_fancier_than_this!",
    "{1_Lv_to_all_Talents_&for_all_characters", "0"],
    ["Glory_To_Nobisect", "1", "Unlock_the_3rd_Divinity_God.", "{10_'Tab_4'_Talent_Pts", "0"],
    ["All_Hail_Purrmep", "1", "Unlock_the_7th_Divinity_God.", "{10_Alternate_Particle_&Alchemy_Upgrades_Per_&Day", "0"],
    ["Long_Live_Bagur", "1", "Unlock_the_10th_and_final_Divinity_God.", "{10%_All_Skill_EXP", "0"],
    ["POiNG_Champion", "1", "Get_a_POiNG_score_of_25,000_or_more!_My_personal_highscore_is_38,323_at_the_time_of_coding_this!", "{10_'Tab_4'_Talent_Pts", "0"],
    ["Lucky_Harvest", "1", "Harvest_a_plant_with_a_Bit_worth_who's_first_3_digits_are_777._For_example,_77.7K_Bits_would_count,_or_777M_Bits_too!",
    "*1.05x_Bit_Gain_in_&Gaming", "0"],
    ["Chemical_Collector", "1000", "Harvest_a_total_of_1000_Chemical-type_Plants_in_Gaming.", "{3%_Damage_for_all_&characters", "0"],
    ["Voraci_Vantasia", "500", "Harvest_a_total_of_500_Voraci-type_Plants_in_Gaming.", "{10%_Divinity_Points_&Gained", "0"],
    ["Bonsai_Bonanza", "100", "Harvest_a_total_of_100_Bonsai-type_Plants_in_Gaming.", "*W5_Shop_EZ-Access", "0"],
    ["Perfect_Trade_Deal", "1",
    "Make_a_trade_with_Blobby_G_worth_a_gold_bar_amount_that_starts_with_777,_like_777K_or_7.77M_for_example._PS;_776_and_778_work_too_lol",
    "{1_additional_Treasure_&Per_Chest_for_Sailing", "0"],
    ["True_Naval_Captain", "1", "Buy_all_20_Boats_in_Sailing._Uh,_yea,_there_is_a_scroll_bar_below_the_boats,_you_can_buy_more_than_5_boats_#",
    "{20%_Captain_EXP_&for_sailing", "0"],
    ["Legendary_Orb", "1", "On_your_Divine_Knight,_get_an_Orb_Score_of_400_or_more_on_OJ_Bay._This_is_the_number_above_your_Orb!", "*Smoggy_Basin_BG", "0"],
    ["Legendary_Flag", "1", "On_your_Siege_Breaker,_get_a_Flag_Score_of_150_or_more_on_Erruption_River._This_is_the_number_above_your_Flag!",
    "{2%_Damage_for_all_&characters", "0"],
    ["Legendary_Wormhole", "1", "On_your_Elemental_Sorcerer,_get_a_Wormhole_Score_of_83_or_more_on_Niagrilled_Falls._This_is_the_number_above_your_Wormhole!",
    "{10%_Divinity_Points_&Gained", "0"],
    ["Utter_DISRESPECT", "1", "SECRET_ACHIEVEMENT_------------------------_Why_did_you_even_hire_the_poor_fella_in_the_first_place???", "{20_Star_Talent_Pts",
    "0"],
    ["Sneaky_Stealing", "1",
    "SECRET_ACHIEVEMENT_------------------------_Walk_to_a_uh..._weird_location?_Well_it's_not_that_weird,_but_it's_just_like,_what_ya_doin'_back_there?",
    "{25%_Shop_Capacity_&for_all_Town_Shops", "0"],
    ["Broken_Controller", "1",
    "SECRET_ACHIEVEMENT_------------------------_You_got..._zero?_Literally_zero??_Jeez,_Im_sorry_but_I_think_you_need_to_uninstall_^",
    "*1.05x_Bit_Gain_in_&Gaming", "0"],
    ["Lavathian_Skulls", "1",
    "Get_a_Lava_Skull_or_higher_on_every_Smolderin'_Plateau_monster_in_the_Deathnote._Yea,_the_100M_Kill_Skull._This_is_gonna_take_a_while.",
    "{2%_Faster_Monster_&Respawn_Time_for_&All_World_5_mobs", "0"],
    ["Seaworthy_Captain", "1", "Level_up_a_Sailing_Captain_to_Lv_15._Few_captains_in_the_universe_can_rival_their_ability_to_plunder!",
    "{1%_ALL_STAT_for_&all_characters", "0"],
    ["Grand_Captain", "1", "Level_up_a_Sailing_Captain_to_Lv_10._They_shall_sail_the_seas_with_confidence!", "{20%_Captain_EXP_&for_sailing", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["Valley_Visitor", "1", "Reach_World_6,_the_Spirited_Valley!_You'll_love_it_here,_all_the_spirits_are_very_friendly!", "{10%_Money_for_all_&characters",
    "0"],
    ["Scorin'_the_Ladies", "1", "Have_a_stack_of_exactly_250,000_Ladybugs_in_your_Storage_Chest.", "{10%_Catching_&Efficiency", "0"],
    ["Effervess_Enthusiess", "1", "Have_a_stack_of_exactly_5,000,000_Effervescent_Logs_in_your_Storage_Chest.", "{10%_Choppin_Efficiency", "0"],
    ["That's_MY_Crown", "1", "Have_a_stack_of_exactly_100,000,000_Royal_Headpiece_in_your_Storage_Chest.", "*Dharma_Mesa_BG", "0"],
    ["Leet_Lanterns", "1", "SECRET_ACHIEVEMENT_------------------------_Oh_yea,_that's_a_good_number._Sure,_it's_no_69420,_but_it's_vintage!",
    "{4%_Damage_for_all_&characters", "0"],
    ["Lil'_Overgrowth", "1", "Get_an_overgrowth_of_32x_on_a_single_crop.", "*1.05x_Crop_Evo_&chance", "0"],
    ["Major_Overgrowth", "1", "Get_an_overgrowth_of_1,024x_on_a_single_crop.", "{15%_Farming_EXP", "0"],
    ["Unreal_Overgrowth", "1", "Get_an_overgrowth_of_8,192x_on_a_single_crop.", "{20%_Class_EXP", "0"],
    ["Doctor_Repellant", "1", "Have_10,000_or_more_Apple_crops_in_your_Depot_at_once._You_can_lock_the_first_crop_before_it_grows_to_guarantee_an_apple!",
    "*W6_Shop_EZ_Access", "0"],
    ["Cob_Enjoyer", "1", "Have_1,000,000_or_more_Corn_crops_in_your_Depot_at_once._Mmmm,_Corn!", "{15%_All_Skill_EXP", "0"],
    ["Science_Undergrad", "1", "Find_30_unique_crops,_as_shown_by_the_Crop_Scientist!", "{10%_Farm_EXP", "0"],
    ["Science_Graduate", "1", "Find_70_unique_crops,_as_shown_by_the_Crop_Scientist!", "*Spirit_Fields_BG", "0"],
    ["Science_Post_Doc", "1", "Find_110_unique_crops,_as_shown_by_the_Crop_Scientist!", "{1%_All_Stat_&for_all_characters", "0"],
    ["Crop_Flooding", "1", "SECRET_ACHIEVEMENT_------------------------_That's..._That's_enough..._THAT'S_ENOUGH_WATER!_THAT'S_ENOUGH!",
    "{5%_Magic_Beans_&from_Legumulyte", "0"],
    ["Legumulucky", "1", "Make_a_crop_trade_with_the_Legumulyte_worth_exactly_777_magic_beans.", "{2%_Damage_for_all_&characters", "0"],
    ["Big_Time_Land_Owner", "1", "Get_27_plots_of_land_in_your_farm.", "*1.15x_Crop_OG_Chance", "0"],
    ["Ceramic_Sneaking", "1", "Reach_the_Sneaking_Floor_with_the_Petrified_Ceramist_guest.", "*1.03x_Jade_Gain", "0"],
    ["Top_Floor_Sneaking", "1", "Reach_what_seems_like_the_top_Floor_of_Sneaking_with_the_Eldar_Kingulyte_guest.", "*1.07x_Jade_Gain", "0"],
    ["Untying_Extraordinaire", "1", "Untie_6_other_Ninja_Twins.", "*1.05x_Stealth_for_&all_Ninja_Twins", "0"],
    ["Lucky_Stealy", "1", "Successfully_find_6_items_in_a_row,_in_a_single_AFK_claim_within_Sneaking.", "*1.05x_Jade_Gain", "0"],
    ["Yellow_Belt", "1", "Find_a_论50_Yellow_Belt_Sneaking_Charm._Yes,_exactly_论50.", "{10%_Sneaking_EXP_gain", "0"],
    ["Straw_Hat_Stacking", "1", "SECRET_ACHIEVEMENT_------------------------_It's_a_shame_you_can't_wear_them_all_at_once...",
    "*1.01x_DMG_Multiplier_&for_all_characters", "0"],
    ["Best_Bloomie", "1", "Get_a_Bloomy_Summoning_Familiar.", "*1.05x_All_Essence_&Gain", "0"],
    ["Regalis_My_Beloved", "1", "Get_a_Regalis_Summoning_Familiar.", "*1.01x_larger_Winners_&Bonuses_from_Summoning", "0"],
    ["This,_is,_Summoning!", "1", "Survive_for_200_seconds_in_the_Endless_Summoning_Mode,_which_isn't_out_yet.", "*1.05x_All_Essence_&Gain", "0"],
    ["Summoning_CM", "1", "Get_10_Career_Wins_within_Summoning", "{3%_Damage_for_all_&characters", "0"],
    ["Summoning_IM", "1", "Get_25_Career_Wins_within_Summoning", "{20%_Money_for_all_&characters", "0"],
    ["Summoning_GM", "1", "Get_58_Career_Wins_within_Summoning", "{6%_Drop_Chance_&for_all_characters", "0"],
    ["Penta_Defence", "1", "Reach_Wave_50_in_Breezy_Battle_without_placing_more_than_5_Towers_in_total.", "*Lullaby_Airways_BG", "0"],
    ["Spectre_Stars", "1", "Complete_all_constellations_in_the_Spirited_Valley._You_can_check_your_progress_within_the_Telescope.",
    "*1.01x_larger_Winners_&Bonuses_from_Summoning", "0"],
    ["Beanstacker_Trainee", "1", "Add_5_different_golden_foods_to_The_Beanstalk.", "{2%_All_Golden_Food_&Bonuses", "0"],
    ["Big_Big_Hampter", "1", "SECRET_ACHIEVEMENT_------------------------_Hampter_is_worth_it!", "{4%_Drop_Chance_&for_all_characters", "0"],
    ["Ghost_Buster", "1", "SECRET_ACHIEVEMENT_------------------------_You_took_out_the_baddest_spirit_of_them_all!", "*Bamboo_Forest_BG", "0"],
    ["Beanstacker_Prodigy", "1", "Add_14_different_golden_foods_to_The_Beanstalk.", "{3%_All_Golden_Food_&Bonuses", "0"],
    ["W6_is_Donezo", "1", "Get_a_Lava_Skull_or_higher_on_every_Spirited_Valley_monster_in_the_Deathnote.", "*1.01x_DMG_Multiplier_&for_all_characters", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"],
    ["FILLERZZZ_ACH", "20", "-", "*FILLERZ_&*FILLERZ_&*FILLERZ", "0"]
]
allMeritsDict = {
    0: {
        0: {"Name": "Shared Inventory Bags", "Level": 0, "MaxLevel": 5},
        1: {"Name": "W1 Respawn", "Level": 0, "MaxLevel": 10},
        2: {"Name": "Lowest Character EXP", "Level": 0, "MaxLevel": 12},
        3: {"Name": "Hemoglobin max level", "Level": 0, "MaxLevel": 10},
        4: {"Name": "Boss Keys dropped", "Level": 0, "MaxLevel": 10},
        5: {"Name": "Amarok Recipes", "Level": 0, "MaxLevel": 5},
        6: {"Name": "W1 Star Talents", "Level": 0, "MaxLevel": 6},
        7: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
    },  #World1
    1: {
        0: {"Name": "Obol Drop Rate", "Level": 0, "MaxLevel": 7},
        1: {"Name": "W2 Respawn", "Level": 0, "MaxLevel": 10},
        2: {"Name": "AFK Gains", "Level": 0, "MaxLevel": 10},
        3: {"Name": "Convert Better max level", "Level": 0, "MaxLevel": 10},
        4: {"Name": "Boss Gems dropped", "Level": 0, "MaxLevel": 8},
        5: {"Name": "Efaunt Recipes", "Level": 0, "MaxLevel": 5},
        6: {"Name": "W2 Star Talents", "Level": 0, "MaxLevel": 8},
        7: {"Name": "Arcade Ball rate", "Level": 0, "MaxLevel": 5},
    },  #World2
    2: {
        0: {"Name": "Build and Food slots", "Level": 0, "MaxLevel": 4},
        1: {"Name": "W3 Respawn", "Level": 0, "MaxLevel": 10},
        2: {"Name": "Max Book levels", "Level": 0, "MaxLevel": 5},
        3: {"Name": "Telekinetic Storage max level", "Level": 0, "MaxLevel": 10},
        4: {"Name": "Printer Sample Size", "Level": 0, "MaxLevel": 10},
        5: {"Name": "Chizoar Recipes", "Level": 0, "MaxLevel": 5},
        6: {"Name": "Refinery Salt Consumption", "Level": 0, "MaxLevel": 5},
        7: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
    },  #World3
    3: {
        0: {"Name": "Daily Crystals", "Level": 0, "MaxLevel": 3},
        1: {"Name": "W4 Respawn", "Level": 0, "MaxLevel": 10},
        2: {"Name": "Breeding Egg Capacity", "Level": 0, "MaxLevel": 2},
        3: {"Name": "Spice Spillage max level", "Level": 0, "MaxLevel": 5},
        4: {"Name": "Lab Connection Range", "Level": 0, "MaxLevel": 8},
        5: {"Name": "Troll Recipes", "Level": 0, "MaxLevel": 4},
        6: {"Name": "Additional NBLB bubbles", "Level": 0, "MaxLevel": 3},
        7: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
    },  #World4
    4: {
        0: {"Name": "Tab 4 Talent Points", "Level": 0, "MaxLevel": 20},
        1: {"Name": "W5 Respawn", "Level": 0, "MaxLevel": 10},
        2: {"Name": "Sailing Loot Pile Capacity", "Level": 0, "MaxLevel": 7},
        3: {"Name": "Stat Overload max level", "Level": 0, "MaxLevel": 10},
        4: {"Name": "W5 Skill EXP", "Level": 0, "MaxLevel": 5},
        5: {"Name": "Kattlekruk Recipes", "Level": 0, "MaxLevel": 9},
        6: {"Name": "Atom Upgrade cost reduction", "Level": 0, "MaxLevel": 4},
        7: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},},  #World5
    5: {
        0: {"Name": "Tab 5 Talent Points", "Level": 0, "MaxLevel": 20},
        1: {"Name": "W6 Respawn", "Level": 0, "MaxLevel": 10},
        2: {"Name": "Farming Plots, OG, and EXP", "Level": 0, "MaxLevel": 15},
        3: {"Name": "Jade Gain", "Level": 0, "MaxLevel": 20},
        4: {"Name": "Summoning Winner bonuses", "Level": 0, "MaxLevel": 10},
        5: {"Name": "Emperor Recipes", "Level": 0, "MaxLevel": 9},
        6: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        7: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
    },  #World6
    6: {
        0: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        1: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        2: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        3: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        4: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        5: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        6: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        7: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
    },  #World7
    7: {
        0: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        1: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        2: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        3: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        4: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        5: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        6: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
        7: {"Name": "Not Implemented", "Level": 0, "MaxLevel": 0},
    },  #World8
}

expected_talentsDict = {
    "Beginner": [
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
    ],
    "Journeyman": [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        75, 76, 77, 78, 79,
        #Plus the 3 rows from Journeyman Tab2
        15, 16, 17, 18, 19,  #Top row
        20, 21, 22, 23, 24,  #Middle row
        25, 26, 27, 28, 29  #Bottom row
    ],
    "Maestro": [
        30, 31, 32, 33, 34,
        35, 36, 37, 38, 39,
        40, 41, 42, 43, 44
    ],
    "Voidwalker": [
        45, 46, 47, 48, 49,
        50, 51, 52, 53, 54,
        55, 56, 57, 58, 59
    ],
    #"Infinilyte": [],

    "Warrior": [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        85, 86, 87, 88, 89,
        #Plus the 3 rows from Warrior Tab2
        90, 91, 92, 93, 94,
        95, 96, 97, 98, 99,
        100, 101, 102, 103, 104
    ],
    "Barbarian": [
        105, 106, 107, 108, 109,
        110, 111, 112, 81, 114,
        115, 116, 117, 118, 119
    ],
    "Squire": [
        120, 121, 122, 123, 124,
        125, 111, 127, 81, 129,
        130, 131, 132, 133, 119
    ],
    "Blood Berserker": [
        135, 136, 137, 138, 139,
        140, 141, 142, 143, 144,
        145, 146, 147, 148, 149
    ],
    #"Death Bringer": [],
    "Divine Knight": [
        165, 166, 167, 168, 169,
        170, 141, 142, 143, 144,
        175, 176, 177, 178, 149
    ],
    #"Royal Guardian": [],

    "Archer": [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        263, 266, 267, 268, 269,
        #Plus the 3 rows from Archer Tab2
        270, 271, 272, 273, 274,
        284, 276, 277, 278, 279,
        280, 281, 282, 283, 265
    ],
    "Bowman": [
        285, 286, 287, 288, 289,
        290, 291, 292, 293, 294,
        295, 296, 297, 298, 299
    ],
    "Hunter": [
        300, 301, 302, 303, 304,
        305, 291, 307, 293, 309,
        310, 311, 312, 313, 299
    ],
    "Siege Breaker": [
        360, 316, 317, 318, 319,
        320, 366, 367, 368, 144,
        325, 326, 327, 328, 374
    ],
    #"Mayheim": [],
    #"Wind Walker": [],
    "Beast Master": [
        315, 361, 362, 363, 364,
        365, 366, 367, 368, 144,
        370, 371, 372, 373, 374
    ],

    "Mage": [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        445, 446, 447, 448, 449,
        #Plus the 3 rows from Mage Tab2
        450, 451, 452, 453, 454,
        455, 456, 457, 458, 459,
        460, 461, 462, 464, 463  #Not a typo, 464 is before 463
    ],
    "Wizard": [
        465, 466, 467, 468, 469,
        470, 486, 472, 488, 474,
        475, 476, 477, 478, 494
    ],
    "Shaman": [
        480, 481, 482, 483, 484,
        485, 486, 487, 488, 489,
        490, 491, 492, 493, 494
    ],
    "Elemental Sorcerer": [
        495, 496, 497, 498, 499,
        500, 531, 532, 533, 144,
        505, 506, 507, 508, 539
    ],
    #"Spiritual Monk": [],
    "Bubonic Conjuror": [
        525, 526, 527, 528, 529,
        530, 531, 532, 533, 144,
        535, 536, 537, 538, 539
    ],
    #"Arcane Cultist": [],

}
hardcap_symbols = 280
hardcap_enhancement_eclipse = 250  #Lava might add more in the future, but there are no bonuses above 250 in v2.10
skill_talentsDict = {
    # Optimal is an optional list for calculating library.getJeapordyGoal
    # [0] = the starting level
    # [1] = the interval of levels after the starting level which provide a bonus
    # [2] = does this talent benefit from bonuses over the max book level, True of False]
    # Example: Symbols of Beyond gives a benefit every 20 levels and does NOT benefit from bonuses like Rift Slug of Arctis
    # 2nd example: Apocalypse ZOW gives a bonus every 33 and DOES benefit from bonuses

    #Wisdom Skills
    "Choppin": {
        "High": {
            460: {"Name": "Log on Logs", "Tab": "Mage"},
            445: {"Name": "Smart Efficiency", "Tab": "Savvy Basics"},
            462: {"Name": "Deforesting All Doubt", "Tab": "Mage"},
            461: {"Name": "Leaf Thief", "Tab": "Mage"},
            539: {"Name": "Symbols of Beyond P", "Tab": "Elite Class", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            532: {"Name": "Skill Wiz", "Tab": "Elite Class"},
        },
        "Medium": {
            533: {"Name": "Utmost Intellect", "Tab": "Elite Class"},
            456: {"Name": "Unt'WIS'ted Robes", "Tab": "Mage"},
            459: {"Name": "Individual Insight", "Tab": "Mage"},
            488: {"Name": "Wis Wumbo", "Tab": "Mage Subclass"},
            449: {"Name": "Active Afk-er", "Tab": "Savvy Basics"},
        },
        "Low": {
            452: {"Name": "Mana Overdrive", "Tab": "Mage"},
            472: {"Name": "Staring Statues", "Tab": "Wizard"},
            487: {"Name": "Stupendous Statues", "Tab": "Shaman"},
            1: {"Name": "Mana Booster", "Tab": "Savvy Basics"},
            144: {"Name": "The Family Guy", "Tab": "Elite Class"},
            486: {"Name": "Occult Obols", "Tab": "Mage Subclass", 'Hardcap': 125},
        },
        "EXP Only": {
            464: {"Name": "Inner Peace", "Tab": "Mage"},
        },
    },
    "Alchemy": {
        "Medium": {
            492: {"Name": "Bubble Breakthrough", "Tab": "Shaman"},
        },
        "Low": {
            493: {"Name": "Sharing Some Smarts", "Tab": "Shaman"},  # Account-wide EXP bumped to Low
        },
    },
    "Lab": {
        "Low": {
            538: {"Name": "Upload Squared", "Tab": "Bubonic Conjuror"},
            537: {"Name": "Essence Transferral", "Tab": "Bubonic Conjuror"},
            536: {"Name": "Green Tube", "Tab": "Bubonic Conjuror"},  # Account-wide EXP bumped to Low
        },
    },
    "Worship": {
        "High": {
            476: {"Name": "Sooouls", "Tab": "Wizard"},
        },
        "Medium": {
            303: {"Name": "Stop Right There", "Tab": "Hunter"},
        },
        "Low": {
            478: {"Name": "Nearby Outlet", "Tab": "Wizard"},
            475: {"Name": "Charge Syphon", "Tab": "Wizard", 'Hardcap': 200},
        },
        "EXP Only": {
            477: {"Name": "Bless Up", "Tab": "Wizard"},
        },
    },
    "Divinity": {
        "Medium": {
            505: {"Name": "Polytheism", "Tab": "Elemental Sorcerer"},  # Account-wide divinity points
            506: {"Name": "Shared Beliefs", "Tab": "Elemental Sorcerer"},  # Account-wide EXP bumped to Medium because Divinity extra important
        },
    },
    #Strength Skills
    "Cooking": {
        "High": {
            148: {"Name": "Overflowing Ladle", "Tab": "Blood Berserker"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Blood Berserker", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
        },
        "Medium": {
            146: {"Name": "Apocalypse Chow", "Tab": "Blood Berserker"},
        },
        "Low": {
            147: {"Name": "Waiting to Cool", "Tab": "Blood Berserker"},
        },
    },
    "Fishing": {
        "High": {
            115: {"Name": "Worming Undercover", "Tab": "Barbarian"},
            85: {"Name": "Brute Efficiency", "Tab": "Rage Basics"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Elite Class", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            142: {"Name": "Skill Strengthen", "Tab": "Elite Class"},
        },
        "Medium": {
            99: {"Name": "Haungry for Gold", "Tab": "Warrior"},
            143: {"Name": "Overblown Testosterone", "Tab": "Elite Class"},
            96: {"Name": "'STR'ess Tested Garb", "Tab": "Warrior"},
            94: {"Name": "Firmly Grasp It", "Tab": "Warrior"},
            98: {"Name": "Absolute Unit", "Tab": "Warrior"},
            81: {"Name": "Str Summore", "Tab": "Warrior Subclass"},
            89: {"Name": "Idle Skilling", "Tab": "Rage Basics"},
            118: {"Name": "Catching Some Zzz's", "Tab": "Barbarian"},
        },
        "Low": {
            112: {"Name": "Strongest Statues", "Tab": "Barbarian", 'Hardcap': 200},
            116: {"Name": "Bobbin' Bobbers", "Tab": "Barbarian", 'Hardcap': 200},
            111: {"Name": "Fistful of Obol", "Tab": "Warrior Subclass", 'Hardcap': 125},
        },
        "EXP Only": {
            117: {"Name": "All Fish Diet", "Tab": "Barbarian"},
        },
    },
    "Mining": {
        "High": {
            100: {"Name": "Big Pick", "Tab": "Warrior"},
            85: {"Name": "Brute Efficiency", "Tab": "Rage Basics"},
            103: {"Name": "Tool Proficiency", "Tab": "Warrior"},
            101: {"Name": "Copper Collector", "Tab": "Warrior"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Elite Class", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            142: {"Name": "Skill Strengthen", "Tab": "Elite Class"},
        },
        "Medium": {
            99: {"Name": "Haungry for Gold", "Tab": "Warrior"},
            143: {"Name": "Overblown Testosterone", "Tab": "Elite Class"},
            96: {"Name": "'STR'ess Tested Garb", "Tab": "Warrior"},
            94: {"Name": "Firmly Grasp It", "Tab": "Warrior"},
            98: {"Name": "Absolute Unit", "Tab": "Warrior"},
            81: {"Name": "Str Summore", "Tab": "Warrior Subclass"},
            89: {"Name": "Idle Skilling", "Tab": "Rage Basics"},
        },
        "Low": {
            92: {"Name": "Health Overdrive", "Tab": "Warrior"},
            127: {"Name": "Shieldiest Statues", "Tab": "Squire", 'Hardcap': 200},
            112: {"Name": "Strongest Statues", "Tab": "Barbarian", 'Hardcap': 200},
            95: {"Name": "Strength in Numbers", "Tab": "Warrior"},
            0: {"Name": "Health Booster", "Tab": "Rage Basics"},
            144: {"Name": "The Family Guy", "Tab": "Elite Class"},
            111: {"Name": "Fistful of Obol", "Tab": "Warrior Subclass", 'Hardcap': 125},
        },
        "EXP Only": {
            104: {"Name": "Tempestuous Emotions", "Tab": "Warrior"},
        },
    },
    "Construction": {
        "Medium": {
            131: {"Name": "Redox Rates", "Tab": "Squire"},
        },
        "Low": {
            130: {"Name": "Refinery Throttle", "Tab": "Squire", "Optimal": [0, 8, True]},
        },
        "EXP Only": {
            132: {"Name": "Sharper Saws", "Tab": "Squire", 'Hardap': 160},
        },
    },
    "Gaming": {
        "Medium": {
            177: {"Name": "Bitty Litty", "Tab": "Divine Knight"},
        },
        "Low": {
            175: {"Name": "Undying Passion", "Tab": "Divine Knight"},
            176: {"Name": "One Thousand Hours Played", "Tab": "Divine Knight"},  # Account-wide EXP bumped to Low
        },
    },
    #Agility Skills
    "Smithing": {
        "High": {},
        "Medium": {},
        "Low": {
            269: {"Name": "Broken Time", "Tab": "Calm Basics"},
            281: {"Name": "Acme Anvil", "Tab": "Archer"},
        },
        "EXP Only": {
            282: {"Name": "Yea I Already Know", "Tab": "Archer"},
            265: {"Name": "Focused Soul", "Tab": "Archer"},
        },
    },
    "Catching": {
        "High": {
            263: {"Name": "Elusive Efficiency", "Tab": "Calm Basics"},
            295: {"Name": "Teleki-net-ic Logs", "Tab": "Bowman"},
            296: {"Name": "Briar Patch Runner", "Tab": "Bowman"},
            374: {"Name": "Symbols of Beyond G", "Tab": "Elite Class", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            367: {"Name": "Skill Ambidexterity", "Tab": "Elite Class"},
        },
        "Medium": {
            298: {"Name": "Sunset on the Hives", "Tab": "Bowman"},
            368: {"Name": "Adaptation Revelation", "Tab": "Elite Class"},
            276: {"Name": "Garb of Un'AGI'ng Quality", "Tab": "Archer"},
            278: {"Name": "Sanic Speed", "Tab": "Archer"},
            293: {"Name": "Agi Again", "Tab": "Archer Subclass"},
        },
        "Low": {
            292: {"Name": "Shwifty Statues", "Tab": "Bowman", 'Hardcap': 200},
            144: {"Name": "The Family Guy", "Tab": "Elite Class"},
            291: {"Name": "Shoeful of Obol", "Tab": "Archer Subclass", 'Hardcap': 125},
        },
        "EXP Only": {
            282: {"Name": "Yea I Already Know", "Tab": "Archer"},
            265: {"Name": "Focused Soul", "Tab": "Archer"},
            297: {"Name": "Bug Enthusiast", "Tab": "Bowman"},
        },
    },
    "Sailing": {
        "Low": {
            326: {"Name": "Expertly Sailed", "Tab": "Siege Breaker"},  # Account-wide EXP bumped to Low
            327: {"Name": "Captain Peptalk", "Tab": "Siege Breaker"},  # Account-wide Captain EXP bumped to low
        },
    },
    "Trapping": {
        "High": {
            263: {"Name": "Elusive Efficiency", "Tab": "Calm Basics"},
            311: {"Name": "Invasive Species", "Tab": "Hunter"},
            310: {"Name": "Eagle Eye", "Tab": "Hunter"},
            374: {"Name": "Symbols of Beyond G", "Tab": "Elite Class", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            367: {"Name": "Skill Ambidexterity", "Tab": "Elite Class"},
        },
        "Medium": {
            368: {"Name": "Adaptation Revelation", "Tab": "Elite Class"},
            276: {"Name": "Garb of Un'AGI'ng Quality", "Tab": "Archer"},
            278: {"Name": "Sanic Speed", "Tab": "Archer"},
            293: {"Name": "Agi Again", "Tab": "Archer Subclass"},
        },
        "Low": {
            144: {"Name": "The Family Guy", "Tab": "Elite Class"},
            291: {"Name": "Shoeful of Obol", "Tab": "Archer Subclass", 'Hardcap': 125},
        },
        "EXP Only": {
            282: {"Name": "Yea I Already Know", "Tab": "Archer"},
            265: {"Name": "Focused Soul", "Tab": "Archer"},
        },
    },
    "Breeding": {
        "High": {
            373: {"Name": "Curviture Of The Paw", "Tab": "Beast Master"},
        },
        "Low": {
            372: {"Name": "Shining Beacon of Egg", "Tab": "Beast Master"},  # Account-wide EXP bumped to Low
        },
    },
    # Utility is talents that apply to multiple skills at a bottom-of-the-group priority (Mostly Jman stuff + Drop Rate)
    "Utility": {
        "High": {
            43: {"Name": "Right Hand of Action", "Tab": "Maestro"},
            32: {"Name": "Printer Go Brrr", "Tab": "Maestro", "Optimal": [0, 40, True]},
            34: {"Name": "One Step Ahead", "Tab": "Maestro"},
            59: {"Name": "Blood Marrow", "Tab": "Voidwalker"},
            57: {"Name": "Species Epoch", "Tab": "Voidwalker"},
            49: {"Name": "Enhancement Eclipse", "Tab": "Voidwalker", "Optimal": [0, 25, False], 'Hardcap': hardcap_enhancement_eclipse},
            53: {"Name": "Eternal WIS", "Tab": "Voidwalker"},
            51: {"Name": "Eternal STR", "Tab": "Voidwalker"},
            52: {"Name": "Eternal AGI", "Tab": "Voidwalker"},
        },
        "Medium": {
            41: {"Name": "Crystal Countdown", "Tab": "Maestro"},
            28: {"Name": "Cards Galore", "Tab": "Journeyman"},
            29: {"Name": "Rares Everywhere", "Tab": "Journeyman"},
            24: {"Name": "Curse of Mr Looty Booty", "Tab": "Journeyman"},
            56: {"Name": "Voodoo Statufication", "Tab": "Voidwalker"},
            78: {"Name": "Extra Bags", "Tab": "Beginner"},
            39: {"Name": "Colloquial Containers", "Tab": "Maestro"},
        },
        "Low": {
            279: {"Name": "Robbinghood", "Tab": "Archer"},
            37: {"Name": "Skilliest Statue", "Tab": "Maestro", 'Hardcap': 200},
        },
        "EXP Only": {
            42: {"Name": "Left Hand of Learning", "Tab": "Maestro"},
            40: {"Name": "Maestro Transfusion", "Tab": "Maestro"},
            38: {"Name": "Bliss N Chips", "Tab": "Maestro"},
        },
    },
}
combat_talentsDict = {
    #Talents here are unique from the skill_talentsDict above
    #Elite Classes
    "Blood Berserker": {
        "High": {},
        "Medium": {
            108: {"Name": "No Pain No Gain", "Tab": "Barbarian"},
            97: {"Name": "Carry a Big Stick", "Tab": "Warrior"},
            6: {"Name": "Gilded Sword", "Tab": "Rage Basics"},
        },
        "Low": {
            103: {"Name": "Idle Brawling", "Tab": "Rage Basics"},
            5: {"Name": "Sharpened Axe", "Tab": "Rage Basics"},
            141: {"Name": "Charred Skulls", "Tab": "Blood Berserker"},
        },
    },
    "Divine Knight": {
        "High": {
            168: {"Name": "Orb of Remembrance", "Tab": "Divine Knight"},
            120: {"Name": "Shockwave Slash", "Tab": "Squire", "Optimal": [0, 30, True]},
            165: {"Name": "Knightly Disciple", "Tab": "Divine Knight"},  #Inconsistent levels for extra attacks per Stark. Idk, just max book it and deal with it
            169: {"Name": "Imbued Shockwaves", "Tab": "Divine Knight"},
            121: {"Name": "Daggerang", "Tab": "Squire", "Optimal": [0, 30, True]},
            166: {"Name": "Mega Mongorang", "Tab": "Divine Knight", "Optimal": [0, 25, True]},
        },
        "Medium": {
            178: {"Name": "King of the Remembered", "Tab": "Divine Knight"},
            129: {"Name": "Blocky Bottles", "Tab": "Squire"},
            125: {"Name": "Precision Power", "Tab": "Squire"},
            97: {"Name": "Carry a Big Stick", "Tab": "Warrior"},
            6: {"Name": "Gilded Sword", "Tab": "Rage Basics"},
        },
        "Low": {
            103: {"Name": "Idle Brawling", "Tab": "Rage Basics"},
            5: {"Name": "Sharpened Axe", "Tab": "Rage Basics"},
            141: {"Name": "Charred Skulls", "Tab": "Divine Knight"},
        },
    },
    "Bubonic Conjuror": {
        "High": {
            490: {"Name": "Cranium Cooking", "Tab": "Shaman"},
            481: {"Name": "Auspicious Aura", "Tab": "Shaman"},
            483: {"Name": "Tenteyecle", "Tab": "Shaman"},
            529: {"Name": "Raise Dead", "Tab": "Bubonic Conjuror", 'Hardcap': 200},
            526: {"Name": "Flatulent Spirit", "Tab": "Bubonic Conjuror"},
            525: {"Name": "Chemical Warfare", "Tab": "Bubonic Conjuror"},
        },
        "Medium": {
            485: {"Name": "Virile Vials", "Tab": "Shaman"},
            455: {"Name": "Knowledge Is Power", "Tab": "Mage"},
            457: {"Name": "Power Overwhelming", "Tab": "Mage"},
            6: {"Name": "Gilded Sword", "Tab": "Savvy Basics"},
        },
        "Low": {
            103: {"Name": "Idle Casting", "Tab": "Savvy Basics"},
            5: {"Name": "Sharpened Axe", "Tab": "Savvy Basics"},
            531: {"Name": "Memorial Skulls", "Tab": "Bubonic Conjuror"},
        },
    },
    "Elemental Sorcerer": {
        "High": {
            469: {"Name": "Mana Is Life", "Tab": "Wizard"},
            496: {"Name": "Lightning Barrage", "Tab": "Elemental Sorcerer"},
            497: {"Name": "Radiant Chainbolt", "Tab": "Elemental Sorcerer"},
            467: {"Name": "Tornado", "Tab": "Wizard"},
            466: {"Name": "Floor Is Lava", "Tab": "Wizard"},
            498: {"Name": "Dimensional Wormhole", "Tab": "Elemental Sorcerer"},
        },
        "Medium": {
            508: {"Name": "Wormhole Emperor", "Tab": "Elemental Sorcerer"},
            474: {"Name": "Fuscia Flasks", "Tab": "Wizard"},
            470: {"Name": "Paperwork, Great", "Tab": "Wizard"},
            455: {"Name": "Knowledge Is Power", "Tab": "Mage"},
            457: {"Name": "Power Overwhelming", "Tab": "Mage"},
            6: {"Name": "Gilded Sword", "Tab": "Savvy Basics"},
        },
        "Low": {
            507: {"Name": "Gods Chosen Children", "Tab": "Elemental Sorcerer"},
            103: {"Name": "Idle Casting", "Tab": "Savvy Basics"},
            5: {"Name": "Sharpened Axe", "Tab": "Savvy Basics"},
            531: {"Name": "Memorial Skulls", "Tab": "Elemental Sorcerer"},
        },
    },
    "Siege Breaker": {
        "High": {
            318: {"Name": "Pirate Flag", "Tab": "Siege Breaker"},
            319: {"Name": "Plunder Ye Deceased", "Tab": "Siege Breaker"},
            316: {"Name": "Suppressing Fire", "Tab": "Siege Breaker", 'Optimal': [0, 33, True]},
            317: {"Name": "Firebomb", "Tab": "Siege Breaker", 'Optimal': [0, 50, True]},
            315: {"Name": "Cannonball", "Tab": "Siege Breaker"},
            285: {"Name": "Homing Arrows", "Tab": "Bowman", 'Optimal': [0, 15, True]},
            270: {"Name": "Piercing Arrow", "Tab": "Archer", 'Optimal': [0, 40, True]},
        },
        "Medium": {
            #287: {"Name": "Flax Instastring", "Tab": "Bowman"},  #I believe this only procs single target, making it fairly useless
            289: {"Name": "Woah, That Was Fast", "Tab": "Bowman"},
            286: {"Name": "Magic Shortbow", "Tab": "Bowman", 'Optimal': [0, 20, True]},
            328: {"Name": "Archlord Of The Pirates", "Tab": "Siege Breaker"},
            290: {"Name": "Speedna", "Tab": "Bowman"},
            273: {"Name": "Strafe", "Tab": "Archer"},
            284: {"Name": "Veins of the Infernal", "Tab": "Archer"},
            277: {"Name": "High Polymer Limbs", "Tab": "Archer"},
            6: {"Name": "Gilded Sword", "Tab": "Calm Basics"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Calm Basics"},
            5: {"Name": "Sharpened Axe", "Tab": "Calm Basics"},
            366: {"Name": "Stacked Skulls", "Tab": "Siege Breaker"},
        },
    },
    "Beast Master": {
        "High": {
            302: {"Name": "Uwu Rawrrr", "Tab": "Hunter"},
            362: {"Name": "Whale Wallop", "Tab": "Beast Master", 'Optimal': [0, 17, True]},
            301: {"Name": "Bear Trap", "Tab": "Hunter", 'Optimal': [0, 30, True]},
            300: {"Name": "Three-Sixty Noscope", "Tab": "Hunter",},
            270: {"Name": "Piercing Arrow", "Tab": "Archer", 'Optimal': [0, 40, True]},
            363: {"Name": "Nacho Party", "Tab": "Beast Master", 'Optimal': [0, 13, True]},
            361: {"Name": "Boar Rush", "Tab": "Beast Master", 'Optimal': [0, 20, True]},
        },
        "Medium": {
            328: {"Name": "Archlord Of The Pirates", "Tab": "Siege Breaker"},
            290: {"Name": "Looty Mc Shooty", "Tab": "Bowman"},
            #273: {"Name": "Strafe", "Tab": "Archer"},
            284: {"Name": "Veins of the Infernal", "Tab": "Archer"},
            277: {"Name": "High Polymer Limbs", "Tab": "Archer"},
            6: {"Name": "Gilded Sword", "Tab": "Calm Basics"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Calm Basics"},
            5: {"Name": "Sharpened Axe", "Tab": "Calm Basics"},
            366: {"Name": "Stacked Skulls", "Tab": "Beast Master"},
        },
    },
    "Voidwalker": {
        "High": {
            19: {"Name": "Gimme Gimme", "Tab": "Journeyman"},
            26: {"Name": "Cmon Out Crystals", "Tab": "Journeyman"},
            46: {"Name": "Void Radius", "Tab": "Voidwalker"},
            45: {"Name": "Void Trial Rerun", "Tab": "Voidwalker"},
            47: {"Name": "Bossing Vain", "Tab": "Voidwalker"},
        },
        "Medium": {
            50: {"Name": "Power Orb", "Tab": "Voidwalker"},
            48: {"Name": "Quad Jab", "Tab": "Voidwalker"},
            33: {"Name": "Triple Jab", "Tab": "Maestro"},
            18: {"Name": "Two Punch Man", "Tab": "Journeyman"},
            31: {"Name": "Skillage Damage", "Tab": "Maestro"},
            20: {"Name": "Lucky Hit", "Tab": "Journeyman"},
            54: {"Name": "Eternal Luk", "Tab": "Voidwalker"},
            21: {"Name": "F'LUK'ey Fabrics", "Tab": "Journeyman"},
            38: {"Name": "Bliss N Chips", "Tab": "Maestro"},
            6: {"Name": "Gilded Sword", "Tab": "Beginner"},
        },
        "Low": {
            5: {"Name": "Sharpened Axe", "Tab": "Beginner"},
            36: {"Name": "Clever Clover Obols", "Tab": "Maestro"},
        }
    },
}

def lavaFunc(funcType: str, level: int, x1: int | float, x2: int | float, roundResult=False):
    result = 0
    match funcType:
        case 'add':
            if x2 != 0:
                result = (((x1 + x2) / x2 + 0.5 * (level - 1)) / (x1/x2)) * level * x1
            else:
                result = level * x1
        case 'decay':
            result = (level * x1) / (level + x2)
        case 'intervalAdd':
            result = x1 + math.floor(level / x2)
        case 'decayMulti':
            result = 1 + (level * x1) / (level + x2)
        case 'bigBase':
            result = x1 + x2 * level
        case 'special1':
            result = 100 - (level * x1) / (level + x2)
        case _:
            result = 0
    if roundResult:
        return round(result)
    else:
        return result

def ceilUpToBase(inputValue: int, base: int) -> int:
    toReturn = base
    while toReturn <= inputValue:
        toReturn += base
    return toReturn


###WORLD 1 CONSTS###
bribesDict = {
    "W1": ["Insider Trading", "Tracking Chips", "Mandatory Fire Sale", "Sleeping On the Job", "Artificial Demand", "The Art of the Deal"],
    "W2": ["Overstock Regulations", "Double EXP Scheme", "Tagged Indicators", "Fossil Fuel Legislation", "Five Aces in the Deck", "Fake Teleport Tickets", "The Art of the Steal"],
    "W3": ["Counterfeit Telepassports", "Weighted Marbles", "Changing the Code", "Taxidermied Cog Pouches", "Guild VIP Fraud", "Library Double Agent", "The Art of the Fail"],
    "W4": ["Photoshopped Dmg Range", "Glitched Acc Formula", "Firewalled Defence", "Bottomless Bags", "AFKeylogging", "Guild GP Hack"],
    "Trash Island": ["The Art of the Bail", "Random Garbage", "Godlier Creation", "Fishermaster", "Muscles on Muscles", "Bottle Service", "Star Scraper"],
    "W6": ["The Art of the Grail", "Artifact Pilfering", "Forge Cap Smuggling", "Gold from Lead", "Nugget Fabrication", "Divine PTS Miscounting", "Loot Table Tampering", "The Art of the Flail"]
}
unpurchasableBribes = ["The Art of the Flail"]  # These bribes are in the game, but cannot be purchased as of v2.10
stamp_maxes = {
    #Combat
    #Skill
    "Mason Jar Stamp": 160,
    "Lil' Mining Baggy Stamp": 300,
    "Choppin' Bag Stamp": 320,
    "Matty Bag Stamp": 410,  #420 is possible but exploity
    "Bag o Heads Stamp": 224,
    "Bugsack Stamp": 224,
    "Drippy Drop Stamp": 155,
    "Cooked Meal Stamp": 465,
    "Ladle Stamp": 320,
    "Multitool": 220,
    #Misc
    "Crystallin": 270,
    "Forge Stamp": 230,
    "Biblio Stamp": 64,
}
stampsDict = {
    "Combat": {
        0: {'Name': "Sword Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'spore-cap'},
        1: {'Name': "Heart Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'oak-logs'},
        2: {'Name': "Mana Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'copper-pre'},
        3: {'Name': "Tomahawk Stamp", 'funcType': 'decay', 'x1': 6, 'x2': 40, 'Material': 'copper-bar'},
        4: {'Name': "Target Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'thread'},
        5: {'Name': "Shield Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'iron-ore'},
        6: {'Name': "Longsword Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'bean-slices'},
        7: {'Name': "Kapow Stamp", 'funcType': 'decay', 'x1': 8, 'x2': 40, 'Material': 'trusty-nails'},
        8: {'Name': "Fist Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'bleach-logs'},
        9: {'Name': "Battleaxe Stamp", 'funcType': 'decay', 'x1': 10, 'x2': 40, 'Material': 'grass-leaf'},
        10: {'Name': "Agile Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'copper-chopper'},
        11: {'Name': "Vitality Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'snake-skin'},
        12: {'Name': "Book Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'iron-bar'},
        13: {'Name': "Manamoar Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'glublin-ear'},
        14: {'Name': "Clover Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'iron-platebody'},
        15: {'Name': "Scimitar Stamp", 'funcType': 'add', 'x1': 3, 'x2': 0, 'Material': 'goldfish'},
        16: {'Name': "Bullseye Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'sentient-cereal'},
        17: {'Name': "Feather Stamp", 'funcType': 'decay', 'x1': 5, 'x2': 50, 'Material': 'coconotnotto'},
        18: {'Name': "Polearm Stamp", 'funcType': 'decay', 'x1': 16, 'x2': 40, 'Material': 'steel-axe'},
        19: {'Name': "Violence Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'dementia-ore'},
        20: {'Name': "Buckler Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'platinum-bar'},
        21: {'Name': "Hermes Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'rooted-soul'},
        22: {'Name': "Sukka Foo", 'funcType': 'decay', 'x1': 20, 'x2': 60, 'Material': 'amarok-slab'},
        23: {'Name': "Arcane Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'gold-bar'},
        24: {'Name': "Avast Yar Stamp", 'funcType': 'add', 'x1': 6, 'x2': 0, 'Material': 'bunny'},
        25: {'Name': "Steve Sword", 'funcType': 'decay', 'x1': 20, 'x2': 60, 'Material': 'fruitfly'},
        26: {'Name': "Blover Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'jellyfish'},
        27: {'Name': "Stat Graph Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'mystery-upgrade-stone-i'},
        28: {'Name': "Gilded Axe Stamp", 'funcType': 'add', 'x1': 8, 'x2': 0, 'Material': 'thingymabob'},
        29: {'Name': "Diamond Axe Stamp", 'funcType': 'decay', 'x1': 20, 'x2': 60, 'Material': 'pvc-pipe'},
        30: {'Name': "Tripleshot Stamp", 'funcType': 'add', 'x1': 3, 'x2': 0, 'Material': 'tangled-cords'},
        31: {'Name': "Blackheart Stamp", 'funcType': 'add', 'x1': 10, 'x2': 0, 'Material': 'purple-screw'},
        32: {'Name': "Maxo Slappo Stamp", 'funcType': 'add', 'x1': 4, 'x2': 0, 'Material': 'maple-logs'},
        33: {'Name': "Sashe Sidestamp", 'funcType': 'add', 'x1': 4, 'x2': 0, 'Material': 'scarab'},
        34: {'Name': "Intellectostampo", 'funcType': 'add', 'x1': 4, 'x2': 0, 'Material': 'oozie-soul'},
        35: {'Name': "Conjocharmo Stamp", 'funcType': 'add', 'x1': 4, 'x2': 0, 'Material': 'suggma-ashes'},
        36: {'Name': "Dementia Sword Stamp", 'funcType': 'decay', 'x1': 25, 'x2': 80, 'Material': 'dreadlo-ore'},
        37: {'Name': "Golden Sixes Stamp", 'funcType': 'decay', 'x1': 20, 'x2': 80, 'Material': 'kraken'},
        38: {'Name': "Stat Wallstreet Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'mystery-upgrade-stone-ii'},
        39: {'Name': "Void Sword Stamp", 'funcType': 'add', 'x1': 12, 'x2': 0, 'Material': 'rice-cake'},
        40: {'Name': "Void Axe Stamp", 'funcType': 'decay', 'x1': 35, 'x2': 200, 'Material': 'bamboo-logs'},
        41: {'Name': "Captalist Stats Stamp", 'funcType': 'decay', 'x1': 5, 'x2': 100, 'Material': 'firefly'},
    },
    "Skill": {
        0: {'Name': "Pickaxe Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'oak-logs'},
        1: {'Name': "Hatchet Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'thread'},
        2: {'Name': "Anvil Zoomer Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'copper-ore'},
        3: {'Name': "Lil' Mining Baggy Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'jungle-logs'},
        4: {'Name': "Twin Ores Stamp", 'funcType': 'decay', 'x1': 15, 'x2': 40, 'Material': 'thief-hoof'},
        5: {'Name': "Choppin' Bag Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'carrot-cube'},
        6: {'Name': "Duplogs Stamp", 'funcType': 'decay', 'x1': 15, 'x2': 40, 'Material': 'militia-helm'},
        7: {'Name': "Matty Bag Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'cramped-material-pouch'},
        8: {'Name': "Smart Dirt Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'plank'},
        9: {'Name': "Cool Diggy Tool Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'iron-hatchet'},
        10: {'Name': "High IQ Lumber Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'bullfrog-horn'},
        11: {'Name': "Swag Swingy Tool Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'copper-pickaxe'},
        12: {'Name': "Alch Go Brrr Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'forest-fibres'},
        13: {'Name': "Brainstew Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'gold-ore'},
        14: {'Name': "Drippy Drop Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'pocket-sand'},
        15: {'Name': "Droplots Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'bloach'},
        16: {'Name': "Fishing Rod Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'fly'},
        17: {'Name': "Fishhead Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'megalodon-tooth'},
        18: {'Name': "Catch Net Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'goldfish'},
        19: {'Name': "Fly Intel Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'crabby-cakey'},
        20: {'Name': "Bag o Heads Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'butterfly'},
        21: {'Name': "Holy Mackerel Stamp", 'funcType': 'decay', 'x1': 20, 'x2': 40, 'Material': 'platinum-ore'},
        22: {'Name': "Bugsack Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'hermit-can'},
        23: {'Name': "Buzz Buzz Stamp", 'funcType': 'decay', 'x1': 20, 'x2': 40, 'Material': 'potty-rolls'},
        24: {'Name': "Hidey Box Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'crabbo'},
        25: {'Name': "Purp Froge Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'scorpie'},
        26: {'Name': "Spikemouth Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'mousey'},
        27: {'Name': "Shiny Crab Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'owlio'},
        28: {'Name': "Gear Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'sticky-stick'},
        29: {'Name': "Stample Stamp", 'funcType': 'decay', 'x1': 4, 'x2': 30, 'Material': 'floof-ploof'},
        30: {'Name': "Saw Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'dementia-bar'},
        31: {'Name': "Amplestample Stamp", 'funcType': 'decay', 'x1': 5, 'x2': 30, 'Material': 'mosquisnow'},
        32: {'Name': "SpoOoky Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'forest-soul'},
        33: {'Name': "Flowin Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'redox-salts'},
        34: {'Name': "Prayday Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'cracked-glass'},
        35: {'Name': "Banked Pts Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'dune-soul'},
        36: {'Name': "Cooked Meal Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'skelefish'},
        37: {'Name': "Spice Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'purple-mush-cap'},
        38: {'Name': "Ladle Stamp", 'funcType': 'add', 'x1': 25, 'x2': 0, 'Material': 'sand-shark'},
        39: {'Name': "Nest Eggs Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'alien-hive-chunk'},
        40: {'Name': "Egg Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'half-eaten-donut'},
        41: {'Name': "Lab Tube Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'bottle-cap'},
        42: {'Name': "Sailboat Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'stilt-pole'},
        43: {'Name': "Gamejoy Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'dandielogs'},
        44: {'Name': "Divine Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'orange-slice'},
        45: {'Name': "Multitool Stamp", 'funcType': 'add', 'x1': 10, 'x2': 0, 'Material': 'dust-mote'},
        46: {'Name': "Skelefish Stamp", 'funcType': 'decay', 'x1': 0.2, 'x2': 20, 'Material': 'skelefish'},
        47: {'Name': "Crop Evo Stamp", 'funcType': 'add', 'x1': 5, 'x2': 0, 'Material': 'icefish'},
        48: {'Name': "Sneaky Peeky Stamp", 'funcType': 'decay', 'x1': 50, 'x2': 150, 'Material': 'leafy-horn'},
        49: {'Name': "Jade Mint Stamp", 'funcType': 'add', 'x1': 0.5, 'x2': 0, 'Material': 'stacked-rice-cake'},
        50: {'Name': "Summoner Stone Stamp", 'funcType': 'decay', 'x1': 50, 'x2': 150, 'Material': 'breezy-soul'},
        51: {'Name': "White Essence Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'ladybug'},
        52: {'Name': "Triad Essence Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'caulifish'},
        53: {'Name': "Dark Triad Essence Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'effervescent logs'},
    },
    "Misc": {
        0: {'Name': "Questin Stamp", 'funcType': 'decay', 'x1': 70, 'x2': 50, 'Material': 'slime-sludge'},
        1: {'Name': "Mason Jar Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'glass-shard'},
        2: {'Name': "Crystallin", 'funcType': 'decay', 'x1': 110, 'x2': 50, 'Material': 'boring-brick'},
        3: {'Name': "Arcade Ball Stamp", 'funcType': 'decay', 'x1': 50, 'x2': 100, 'Material': 'copper-ore'},
        4: {'Name': "Gold Ball Stamp", 'funcType': 'decay', 'x1': 40, 'x2': 100, 'Material': 'golfish'},
        5: {'Name': "Potion Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'icing-ironbite'},
        6: {'Name': "Golden Apple Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'golden-nomwich'},
        7: {'Name': "Ball Timer Stamp", 'funcType': 'decay', 'x1': 12, 'x2': 30, 'Material': 'oak-logs'},
        8: {'Name': "Card Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'furled-flag'},
        9: {'Name': "Forge Stamp", 'funcType': 'decay', 'x1': 120, 'x2': 250, 'Material': 'godshard-ore'},
        10: {'Name': "Vendor Stamp", 'funcType': 'decay', 'x1': 35, 'x2': 100, 'Material': 'cue-tape'},
        11: {'Name': "Sigil Stamp", 'funcType': 'decay', 'x1': 40, 'x2': 150, 'Material': 'ram-wool'},
        12: {'Name': "Talent I Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'frog-leg'},
        13: {'Name': "Talent II Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'pincer-arm'},
        14: {'Name': "Talent III Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'arctic-leaf'},
        15: {'Name': "Talent IV Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'royal-suggma-urn'},
        16: {'Name': "Talent V Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'copper-ore'},
        17: {'Name': "Talent S Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'twisty-leaf'},
        18: {'Name': "Multikill Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'spore-cap'},
        19: {'Name': "Biblio Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'tundra-logs'},
        20: {'Name': "DNA Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'worker-bee'},
        21: {'Name': "Refinery Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'cheesy-crumbs'},
        22: {'Name': "Atomic Stamp", 'funcType': 'decay', 'x1': 20, 'x2': 80, 'Material': 'bamboo'},
    }
}
stampTypes = ["Combat", "Skill", "Misc"]
unavailableStampsList = [
    'Shiny Crab Stamp', 'Gear Stamp', 'SpoOoky Stamp', 'Prayday Stamp',  #Skill
    'Talent I Stamp', 'Talent V Stamp',  #Misc
]  # Last verified as of v2.10
starsignsDict = {
    1: {'Name': "The Buff Guy", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    2: {'Name': "Flexo Bendo", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    3: {'Name': "The Book Worm", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    4: {'Name': "The Fuzzy Dice", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    5: {'Name': "Dwarfo Beardus", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    6: {'Name': "Hipster Logger", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    7: {'Name': "Pie Seas", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    8: {'Name': "Shoe Fly", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    9: {'Name': "Blue Hedgehog", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    10: {'Name': "Gum Drop", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    11: {'Name': "Activelius", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    12: {'Name': "Pack Mule", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    13: {'Name': "Ned Kelly", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    14: {'Name': "Robinhood", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    15: {'Name': "Pirate Booty", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    16: {'Name': "Muscle Man", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    17: {'Name': "Fast Frog", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    18: {'Name': "Smart Stooge", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    19: {'Name': "Lucky Larry", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    20: {'Name': "Silly Snoozer", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    21: {'Name': "The Big Comatose", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    22: {'Name': "Miniature Game", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    23: {'Name': "Mount Eaterest", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    24: {'Name': "Bob Build Guy", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    25: {'Name': "The Big Brain", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    26: {'Name': "The OG Skiller", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    27: {'Name': "Grim Reaper", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    28: {'Name': "The Fallen Titan", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    29: {'Name': "The Forsaken", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    30: {'Name': "Mr No Sleep", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    31: {'Name': "Sir Savvy", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    32: {'Name': "All Rounder", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    33: {'Name': "Fatty Doodoo", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    34: {'Name': "Chronus Cosmos", 'Passive': True, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    35: {'Name': "All Rounderi", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    36: {'Name': "Centaurii", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    37: {'Name': "Murmollio", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    38: {'Name': "Strandissi", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    39: {'Name': "Agitagi", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    40: {'Name': "Wispommo", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    41: {'Name': "Lukiris", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    42: {'Name': "Pokaminni", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    43: {'Name': "Gor Bowzor", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    44: {'Name': "Hydron Cosmos", 'Passive': True, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    45: {'Name': "Trapezoidburg", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    46: {'Name': "Sawsaw Salala", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    47: {'Name': "Preys Bea", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    48: {'Name': "Cullingo", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    49: {'Name': "Gum Drop Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    50: {'Name': "Grim Reaper Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    51: {'Name': "Sir Savvy Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    52: {'Name': "The Bulwark", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    53: {'Name': "Big Brain Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    54: {'Name': "The Fiesty", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    55: {'Name': "The Overachiever", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    56: {'Name': "Comatose Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    57: {'Name': "S. Snoozer Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    58: {'Name': "Breedabilli", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    59: {'Name': "Gordonius Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    60: {'Name': "Power Bowower", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    61: {'Name': "Scienscion", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    62: {'Name': "Artifosho", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    63: {'Name': "Divividov", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    64: {'Name': "C. Shanti Minor", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    65: {'Name': "Muscle Magnus", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    66: {'Name': "Cropiovo Minor", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    67: {'Name': "Fabarmi", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    68: {'Name': "O.G. Signalais", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    69: {'Name': "Lightspeed Frog", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    70: {'Name': "Beanbie Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    71: {'Name': "Damarian Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    72: {'Name': "Lotto Larrinald", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    73: {'Name': "Intellostooge", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    74: {'Name': "S. Tealio", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    75: {'Name': "Sneekee E. X.", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    76: {'Name': "Jadaciussi", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    77: {'Name': "Druipi Major", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    78: {'Name': "Sumo Magno", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    79: {'Name': "Killian Maximus", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    80: {'Name': "Seraph Cosmos", 'Passive': True, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    81: {'Name': "Glimmer of Beyond", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    82: {'Name': "Fillerz48", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    83: {'Name': "Fillerz49", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    84: {'Name': "Fillerz50", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    85: {'Name': "Fillerz51", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    86: {'Name': "Fillerz52", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    87: {'Name': "Fillerz53", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    88: {'Name': "Fillerz54", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    89: {'Name': "Fillerz55", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    90: {'Name': "Fillerz56", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    91: {'Name': "Fillerz57", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    92: {'Name': "Fillerz58", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    93: {'Name': "Fillerz59", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
    94: {'Name': "Fillerz32", 'Passive': False, '1_Value': 0, '1_Stat': '', '2_Value': 0, '2_Stat': '', '3_Value': 0, '3_Stat': ''},
}
forgeUpgradesDict = {
    0: {
        "UpgradeName": "New Forge Slot",
        "Purchased": 0,
        "MaxPurchases": 16
    },
    1: {
        "UpgradeName": "Ore Capacity Boost",
        "Purchased": 0,
        "MaxPurchases": 50
    },
    2: {
        "UpgradeName": "Forge Speed",
        "Purchased": 0,
        "MaxPurchases": 90
    },
    3: {
        "UpgradeName": "Forge EXP Gain (Does Nothing!)",
        "Purchased": 0,
        "MaxPurchases": 85
    },
    4: {
        "UpgradeName": "Bar Bonanza",
        "Purchased": 0,
        "MaxPurchases": 75
    },
    5: {
        "UpgradeName": "Puff Puff Go",
        "Purchased": 0,
        "MaxPurchases": 60
    }
}

###WORLD 2 CONSTS###
max_IndexOfVials = 75  # Last verified as of v2.10
max_IndexOfBubbles = 29  # Last verified as of v2.10
max_IndexOfSigils = 3  # Last verified as of v2.10
vialsDict = {
    0: {"Name": "Copper Corona", "Material": "Copper", "x1": 3, "x2": 0, "funcType": "add"},
    1: {"Name": "Sippy Splinter", "Material": "OakTree", "x1": 3, "x2": 0, "funcType": "add"},
    2: {"Name": "Mushroom Soup", "Material": "Grasslands1", "x1": 3, "x2": 0, "funcType": "add"},
    3: {"Name": "Spool Sprite", "Material": "CraftMat1", "x1": 3, "x2": 0, "funcType": "add"},
    4: {"Name": "Barium Mixture", "Material": "CopperBar", "x1": 3, "x2": 0, "funcType": "add"},
    5: {"Name": "Dieter Drink", "Material": "Grasslands3", "x1": 1, "x2": 0, "funcType": "add"},
    6: {"Name": "Skinny 0 Cal", "Material": "Jungle2", "x1": 2.5, "x2": 0, "funcType": "add"},
    7: {"Name": "Thumb Pow", "Material": "CraftMat5", "x1": 1, "x2": 0, "funcType": "add"},
    8: {"Name": "Jungle Juice", "Material": "JungleTree", "x1": 1, "x2": 0, "funcType": "add"},
    9: {"Name": "Barley Brew", "Material": "IronBar", "x1": 1, "x2": 0, "funcType": "add"},
    10: {"Name": "Anearful", "Material": "Forest1", "x1": 2, "x2": 0, "funcType": "add"},
    11: {"Name": "Tea With Pea", "Material": "ToiletTree", "x1": 3, "x2": 0, "funcType": "add"},
    12: {"Name": "Gold Guzzle", "Material": "Gold", "x1": 1, "x2": 0, "funcType": "add"},
    13: {"Name": "Ramificoction", "Material": "Forest3", "x1": 1, "x2": 0, "funcType": "add"},
    14: {"Name": "Seawater", "Material": "Fish1", "x1": 1, "x2": 0, "funcType": "add"},
    15: {"Name": "Tail Time", "Material": "Sewers2", "x1": 0.5, "x2": 0, "funcType": "add"},
    16: {"Name": "Fly In My Drink", "Material": "Bug1", "x1": 3, "x2": 0, "funcType": "add"},
    17: {"Name": "Mimicraught", "Material": "DesertA2", "x1": 1, "x2": 0, "funcType": "add"},
    18: {"Name": "Blue Flav", "Material": "Plat", "x1": 30, "x2": 7, "funcType": "decay"},
    19: {"Name": "Slug Slurp", "Material": "Fish2", "x1": 2, "x2": 0, "funcType": "add"},
    20: {"Name": "Pickle Jar", "Material": "BobJoePickle", "x1": 50, "x2": 0, "funcType": "add"},
    21: {"Name": "Fur Refresher", "Material": "SnowA1", "x1": 2, "x2": 0, "funcType": "add"},
    22: {"Name": "Sippy Soul", "Material": "Soul1", "x1": 1, "x2": 0, "funcType": "add"},
    23: {"Name": "Crab Juice", "Material": "Critter2", "x1": 4, "x2": 0, "funcType": "add"},
    24: {"Name": "Void Vial", "Material": "Void", "x1": 1, "x2": 0, "funcType": "add"},
    25: {"Name": "Red Malt", "Material": "Refinery1", "x1": 1, "x2": 0, "funcType": "add"},
    26: {"Name": "Ew Gross Gross", "Material": "Bug5", "x1": 1, "x2": 0, "funcType": "add"},
    27: {"Name": "The Spanish Sahara", "Material": "SaharanFoal", "x1": 1, "x2": 0, "funcType": "add"},
    28: {"Name": "Poison Tincture", "Material": "Critter1A", "x1": 3, "x2": 0, "funcType": "add"},
    29: {"Name": "Etruscan Lager", "Material": "SnowB2", "x1": 1, "x2": 0, "funcType": "add"},
    30: {"Name": "Chonker Chug", "Material": "Soul2", "x1": 1, "x2": 0, "funcType": "add"},
    31: {"Name": "Bubonic Burp", "Material": "Critter4", "x1": 1, "x2": 0, "funcType": "add"},
    32: {"Name": "Visible Ink", "Material": "SnowB3", "x1": 1, "x2": 0, "funcType": "add"},
    33: {"Name": "Orange Malt", "Material": "Refinery2", "x1": 5, "x2": 0, "funcType": "add"},
    34: {"Name": "Snow Slurry", "Material": "SnowB5", "x1": 0.5, "x2": 0, "funcType": "add"},
    35: {"Name": "Slowergy Drink", "Material": "Soul4", "x1": 1, "x2": 0, "funcType": "add"},
    36: {"Name": "Sippy Cup", "Material": "Snowc1", "x1": 1, "x2": 0, "funcType": "add"},
    37: {"Name": "Bunny Brew", "Material": "Critter7", "x1": 1, "x2": 0, "funcType": "add"},
    38: {"Name": "40-40 Purity", "Material": "SnowC4", "x1": 1, "x2": 0, "funcType": "add"},
    39: {"Name": "Shaved Ice", "Material": "Refinery5", "x1": 1, "x2": 0, "funcType": "add"},
    40: {"Name": "Goosey Glug", "Material": "Critter9", "x1": 1, "x2": 0, "funcType": "add"},
    41: {"Name": "Ball Pickle Jar", "Material": "BallJoePickle", "x1": 25, "x2": 0, "funcType": "add"},
    42: {"Name": "Capachino", "Material": "GalaxyA1", "x1": 4, "x2": 0, "funcType": "add"},
    43: {"Name": "Donut Drink", "Material": "GalaxyA3", "x1": 5, "x2": 0, "funcType": "add"},
    44: {"Name": "Long Island Tea", "Material": "Fish6", "x1": 6, "x2": 0, "funcType": "add"},
    45: {"Name": "Spook Pint", "Material": "Soul5", "x1": 5, "x2": 0, "funcType": "add"},
    46: {"Name": "Calcium Carbonate", "Material": "GalaxyB3", "x1": 11, "x2": 0, "funcType": "add"},
    47: {"Name": "Bloat Draft", "Material": "Critter10", "x1": 3, "x2": 0, "funcType": "add"},
    48: {"Name": "Choco Milkshake", "Material": "GalaxyB4", "x1": 50, "x2": 7, "funcType": "decay"},
    49: {"Name": "Pearl Seltzer", "Material": "GalaxyC1b", "x1": 0.5, "x2": 0, "funcType": "add"},
    50: {"Name": "Krakenade", "Material": "Fish8", "x1": 1, "x2": 0, "funcType": "add"},
    51: {"Name": "Electrolyte", "Material": "GalaxyC4", "x1": 2, "x2": 0, "funcType": "add"},
    52: {"Name": "Ash Agua", "Material": "LavaA1", "x1": 2, "x2": 0, "funcType": "add"},
    53: {"Name": "Maple Syrup", "Material": "Tree9", "x1": 2, "x2": 0, "funcType": "add"},
    54: {"Name": "Hampter Drippy", "Material": "LavaA5b", "x1": 2, "x2": 0, "funcType": "add"},
    55: {"Name": "Dreadnog", "Material": "DreadloBar", "x1": 2, "x2": 0, "funcType": "add"},
    56: {"Name": "Dusted Drink", "Material": "Bug10", "x1": 2, "x2": 0, "funcType": "add"},
    57: {"Name": "Oj Jooce", "Material": "LavaB3", "x1": 2, "x2": 0, "funcType": "add"},
    58: {"Name": "Oozie Ooblek", "Material": "Soul6", "x1": 2, "x2": 0, "funcType": "add"},
    59: {"Name": "Venison Malt", "Material": "LavaC2", "x1": 2, "x2": 0, "funcType": "add"},
    60: {"Name": "Marble Mocha", "Material": "Marble", "x1": 5, "x2": 0, "funcType": "add"},
    61: {"Name": "Willow Sippy", "Material": "Tree11", "x1": 4, "x2": 0, "funcType": "add"},
    62: {"Name": "Shinyfin Stew", "Material": "Fish13", "x1": 7, "x2": 0, "funcType": "add"},
    63: {"Name": "Dreamy Drink", "Material": "Bug11", "x1": 3.5, "x2": 0, "funcType": "add"},
    64: {"Name": "Ricecakorade", "Material": "SpiA2", "x1": 2, "x2": 0, "funcType": "add"},
    65: {"Name": "Ladybug Serum", "Material": "Bug12", "x1": 4, "x2": 0, "funcType": "add"},
    66: {"Name": "Flavorgil", "Material": "Fish12", "x1": 7, "x2": 0, "funcType": "add"},
    67: {"Name": "Greenleaf Tea", "Material": "SpiB1", "x1": 1.5, "x2": 0, "funcType": "add"},
    68: {"Name": "Firefly Grog", "Material": "Bug13", "x1": 5, "x2": 0, "funcType": "add"},
    69: {"Name": "Dabar Special", "Material": "GodshardBar", "x1": 4, "x2": 0, "funcType": "add"},
    70: {"Name": "Refreshment", "Material": "Soul7", "x1": 2, "x2": 0, "funcType": "add"},
    71: {"Name": "Gibbed Drink", "Material": "SpiC2", "x1": 3.5, "x2": 0, "funcType": "add"},
    72: {"Name": "Ded Sap", "Material": "Tree13", "x1": 3.5, "x2": 0, "funcType": "add"},
    73: {"Name": "Royale Cola", "Material": "SpiD3", "x1": 3.5, "x2": 0, "funcType": "add"},
    74: {"Name": "Turtle Tisane", "Material": "Critter11", "x1": 4, "x2": 0, "funcType": "add"},
}
sigilsDict = {
    "Big Muscle":       {"Index": 0,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [2, 100, 50000]},
    "Pumped Kicks":     {"Index": 2,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [3, 150, 60000]},
    "Odd Literarture":  {"Index": 4,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [5, 200, 70000]},
    "Good Fortune":     {"Index": 6,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [8, 300, 90000]},
    "Plunging Sword":   {"Index": 8,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [15, 700, 100000]},
    "Wizardly Hat":     {"Index": 10, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [24, 1250, 130000]},
    "Envelope Pile":    {"Index": 12, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [60, 2500, 160000]},
    "Shiny Beacon":     {"Index": 14, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [120, 4000, 200000]},
    "Metal Exterior":   {"Index": 16, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [250, 7000, 240000]},
    "Two Starz":        {"Index": 18, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [500, 10000, 280000]},
    "Pipe Gauge":       {"Index": 20, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [700, 12000, 320000]},
    "Trove":            {"Index": 22, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [1300, 14000, 400000]},
    "Pea Pod":          {"Index": 24, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [2100, 15000, 420000]},
    "Tuft Of Hair":     {"Index": 26, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [3000, 25000, 450000]},
    "Emoji Veggie":     {"Index": 28, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [4500, 33000, 480000]},
    "Vip Parchment":    {"Index": 30, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [6300, 42000, 520000]},
    "Dream Catcher":    {"Index": 32, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [7000, 50000, 560000]},
    "Duster Studs":     {"Index": 34, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [8000, 60000, 600000]},
    "Garlic Glove":     {"Index": 36, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [9000, 70000, 650000]},
    "Lab Tesstube":     {"Index": 38, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [12000, 80000, 700000]},
    "Peculiar Vial":    {"Index": 40, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [17000, 120000, 750000]},
    "Loot Pile":        {"Index": 42, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [23000, 160000, 900000]},
    "Div Spiral":       {"Index": 44, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [26000, 200000, 1200000]},
    "Cool Coin":        {"Index": 46, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [30000, 250000, 2000000]},
}
arcadeBonuses = {
    0:  {"Stat": "Base Damage", "x1": 1, "x2": 0, "funcType": "add", "displayType": ""},
    1:  {"Stat": "Base Defence", "x1": 0.2, "x2": 0, "funcType": "add", "displayType": ""},
    2:  {"Stat": "Total Accuracy", "x1": 60, "x2": 100, "funcType": "decay", "displayType": ""},
    3:  {"Stat": "Mining EXP gain", "x1": 60, "x2": 100, "funcType": "decay", "displayType": "%"},
    4:  {"Stat": "Fishing EXP gain", "x1": 60, "x2": 100, "funcType": "", "displayType": "%"},
    5:  {"Stat": "Sample Size", "x1": 4, "x2": 100, "funcType": "decay", "displayType": "%"},
    6:  {"Stat": "AFK Gains Rate", "x1": 4, "x2": 100, "funcType": "decay", "displayType": "%"},
    7:  {"Stat": "Cap for all Liquids", "x1": 25, "x2": 100, "funcType": "decay", "displayType": "%"},
    8:  {"Stat": "Multikill per Tier", "x1": 10, "x2": 100, "funcType": "decay", "displayType": "%"},
    9:  {"Stat": "Catching EXP gain", "x1": 50, "x2": 100, "funcType": "decay", "displayType": "%"},
    10: {"Stat": "Cash from Mobs", "x1": 20, "x2": 100, "funcType": "decay", "displayType": "%"},
    11: {"Stat": "Cash from Mobs", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    12: {"Stat": "Class EXP gain", "x1": 20, "x2": 100, "funcType": "decay", "displayType": "%"},
    13: {"Stat": "Shiny Critter Chance", "x1": 100, "x2": 100, "funcType": "decay", "displayType": "%"},
    14: {"Stat": "Trapping EXP", "x1": 50, "x2": 100, "funcType": "decay", "displayType": "%"},
    15: {"Stat": "Starting TD Pts", "x1": 1, "x2": 0, "funcType": "add", "displayType": ""},
    16: {"Stat": "Tab 1 Talent Pt", "x1": 1, "x2": 10, "funcType": "intervalAdd", "displayType": ""},
    17: {"Stat": "Weapon Power", "x1": 0.07, "x2": 0, "funcType": "add", "displayType": ""},
    18: {"Stat": "Skill EXP gain", "x1": 20, "x2": 100, "funcType": "decay", "displayType": "%"},
    19: {"Stat": "Base STR", "x1": 1, "x2": 0, "funcType": "add", "displayType": ""},
    20: {"Stat": "Base AGI", "x1": 1, "x2": 0, "funcType": "add", "displayType": ""},
    21: {"Stat": "Base WIS", "x1": 1, "x2": 0, "funcType": "add", "displayType": ""},
    22: {"Stat": "Base LUK", "x1": 1, "x2": 0, "funcType": "add", "displayType": ""},
    23: {"Stat": "Trapping Critters", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    24: {"Stat": "Worship Souls", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    25: {"Stat": "Refinery Speed", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    26: {"Stat": "Forge Capacity", "x1": 100, "x2": 100, "funcType": "decay", "displayType": "%"},
    27: {"Stat": "Drop Rate", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    28: {"Stat": "Cooking Speed multi", "x1": 40, "x2": 100, "funcType": "decay", "displayType": "%"},
    29: {"Stat": "Lab EXP gain", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    30: {"Stat": "Breeding Pet DMG", "x1": 40, "x2": 100, "funcType": "decay", "displayType": "%"},
    31: {"Stat": "Nugget Generation", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    32: {"Stat": "Artifact Find Chance", "x1": 50, "x2": 100, "funcType": "decay", "displayType": "%"},
    33: {"Stat": "Sailing Loot", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    34: {"Stat": "White Essence gain", "x1": 40, "x2": 100, "funcType": "decay", "displayType": "%"},
    35: {"Stat": "Jade gain", "x1": 50, "x2": 100, "funcType": "decay", "displayType": "%"},
    36: {"Stat": "Farming EXP", "x1": 30, "x2": 100, "funcType": "decay", "displayType": "%"},
    37: {"Stat": "Divinity EXP", "x1": 40, "x2": 100, "funcType": "decay", "displayType": "%"},
}
#poBoxDict last taken from code in 2.09: #PostOffUpgradeInfo = function ()
#Translate using the Post Office tab in AR spreadsheet
poBoxDict = {
    0: {'Name': 'Civil War Memory Box',
        '1_funcType': 'add', '1_x1': 1, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Base Damage',
        '2_funcType': 'decay', '2_x1': 13, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Fight AFK Gains', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 10, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Critical Chance', '3_minCount': 100},
    1: {'Name': 'Locally Sourced Organs',
        '1_funcType': 'intervalAdd', '1_x1': 1, '1_x2': 2, '1_pre': '', '1_post': '', '1_stat': 'Base Max HP',
        '2_funcType': 'add', '2_x1': 0.1, '2_x2': 0, '2_pre': '', '2_post': '%', '2_stat': 'Max HP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Faster Respawns', '3_minCount': 100},
    2: {'Name': 'Magician Starterpack',
        '1_funcType': 'intervalAdd', '1_x1': 1, '1_x2': 3, '1_pre': '', '1_post': '', '1_stat': 'Base Max MP',
        '2_funcType': 'add', '2_x1': 0.1, '2_x2': 0, '2_pre': '', '2_post': '%', '2_stat': 'Max MP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 17, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Faster Cooldowns', '3_minCount': 100},
    3: {'Name': 'Box of Unwanted Stats',
        '1_funcType': 'add', '1_x1': 0.25, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Base Accuracy',
        '2_funcType': 'add', '2_x1': 0.3, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'Base Defence', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 29, '3_x2': 170, '3_pre': '', '3_post': '%', '3_stat': 'Monster EXP', '3_minCount': 100},
    4: {'Name': 'Dwarven Supplies',
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Mining Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Mining AFK Gain', '3_minCount': 100},
    5: {'Name': 'Blacksmith Box',
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Smithing EXP',
        '2_funcType': 'decay', '2_x1': 75, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Production Speed', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 150, '3_pre': '', '3_post': '%', '3_stat': 'to Craft +1 Slot', '3_minCount': 100},
    6: {'Name': 'Taped Up Timber',
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Choppin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Choppin AFK Gain', '3_minCount': 100},
    7: {'Name': 'Carepack From Mum',
        '1_funcType': 'decay', '1_x1': 23, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Not Consume Food',
        '2_funcType': 'decay', '2_x1': 30, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Health Food Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Boost Food Effect', '3_minCount': 100},
    8: {'Name': 'Sealed Fishheads',
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Fishin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Fishin AFK Gain', '3_minCount': 100},
    9: {'Name': 'Potion Package',
        '1_funcType': 'decay', '1_x1': 70, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Brewing Speed',
        '2_funcType': 'decay', '2_x1': 60, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Alchemy EXP', '2_minCount': 25,
        '3_funcType': 'add', '3_x1': 0.1, '3_x2': 0, '3_pre': '', '3_post': '', '3_stat': 'Cranium Cook Time', '3_minCount': 100},
    10: {'Name': 'Bug Hunting Supplies',
         '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Catchin Efficiency',
         '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Catchin AFK Gain', '3_minCount': 100},
    11: {'Name': 'Non Predatory Loot Box',
         '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Drop Rarity',
         '2_funcType': 'add', '2_x1': 0.25, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'LUK', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 65, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Crystal Mob Spawn', '3_minCount': 100},
    12: {'Name': 'Deaths Storage Unit',
         '1_funcType': 'decay', '1_x1': 22, '1_x2': 200, '1_pre': '', '1_post': '', '1_stat': 'Weapon Power',
         '2_funcType': 'decay', '2_x1': 15, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Basic Atk Speed', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 15, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 100},
    13: {'Name': 'Utilitarian Capsule',
         '1_funcType': 'decay', '1_x1': 5, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Printer Sample Size',
         '2_funcType': 'decay', '2_x1': 15, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Multikill per Tier', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 39, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Cash from Mobs', '3_minCount': 100},
    14: {'Name': 'Lazzzy Lootcrate',
         '1_funcType': 'decay', '1_x1': 30, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': '2X AFK XP chance',
         '2_funcType': 'decay', '2_x1': 35, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'AFK exp if 36hr+', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 35, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'AFK Cash if 36hr+', '3_minCount': 100},
    15: {'Name': 'Science Spare Parts',
         '1_funcType': 'add', '1_x1': 4, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Lab Efficiency',
         '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Lab EXP gain', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '', '3_stat': 'Base LUK', '3_minCount': 100},
    16: {'Name': 'Trapping Lockbox',
         '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Trapping Efficiency',
         '2_funcType': 'decay', '2_x1': 50, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Trapping EXP', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 45, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Critters Trapped', '3_minCount': 100},
    17: {'Name': 'Construction Container',
         '1_funcType': 'add', '1_x1': 0.25, '1_x2': 0, '1_pre': '', '1_post': '%', '1_stat': 'Base Build Rate',
         '2_funcType': 'decay', '2_x1': 75, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Shrine Charge Rate', '2_minCount': 25,
         '3_funcType': 'add', '3_x1': 0.5, '3_x2': 0, '3_pre': '', '3_post': '%', '3_stat': 'Construction EXP', '3_minCount': 100},
    18: {'Name': 'Crate of the Creator',
         '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Worship Efficiency',
         '2_funcType': 'decay', '2_x1': 200, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Max Charge', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 90, '3_x2': 200, '3_pre': '', '3_post': '', '3_stat': 'Starting Worship Pts', '3_minCount': 100},
    19: {'Name': 'Chefs Essentials',
         '1_funcType': 'add', '1_x1': 4, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Cooking Efficiency',
         '2_funcType': 'decay', '2_x1': 60, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Cooking EXP gain', '2_minCount': 25,
         '3_funcType': 'decay', '3_x1': 88, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'for 2x Ladle Drop', '3_minCount': 100},
    20: {'Name': 'Myriad Crate',
         '1_funcType': 'decay', '1_x1': 400, '1_x2': 20000, '1_pre': '', '1_post': '', '1_stat': 'Base All Stat',
         '2_funcType': 'decay', '2_x1': 1000, '2_x2': 20000, '2_pre': '', '2_post': '', '2_stat': 'Base All Efficiency', '2_minCount': 100,
         '3_funcType': 'decay', '3_x1': 100, '3_x2': 20000, '3_pre': '', '3_post': '%', '3_stat': 'All Skills exp', '3_minCount': 300},
    21: {'Name': "Scurvy C'arr'ate",
         '1_funcType': 'decay', '1_x1': 8, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'afk counts for sailing',
         '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'AGI', '2_minCount': 50,
         '3_funcType': 'decay', '3_x1': 25, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 200},
    22: {'Name': 'Box of Gosh',
         '1_funcType': 'decay', '1_x1': 75, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'Divinity EXP',
         '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'WIS', '2_minCount': 50,
         '3_funcType': 'decay', '3_x1': 30, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Divinity Gain', '3_minCount': 200},
    23: {'Name': 'Gaming Lootcrate',
         '1_funcType': 'decay', '1_x1': 14, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'afk counts for gaming',
         '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'STR', '2_minCount': 50,
         '3_funcType': 'decay', '3_x1': 25, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 200},
}
bubbleCauldronColorList = ['Orange', 'Green', 'Purple', 'Yellow']
bubblesDict = {
    0: {
        0: {'Name': 'Roid Ragin', 'Material': 'OakTree', 'x1': 1, 'x2': 0, 'funcType': 'add'},
        1: {'Name': 'Warriors Rule', 'Material': 'Grasslands1', 'x1': 2, 'x2': 50, 'funcType': 'decayMulti'},
        2: {'Name': 'Hearty Diggy', 'Material': 'JungleTree', 'x1': 50, 'x2': 100, 'funcType': 'decay'},
        3: {'Name': 'Wyoming Blood', 'Material': 'Bug1', 'x1': 23.5, 'x2': 1.5, 'funcType': 'bigBase'},
        4: {'Name': 'Reely Smart', 'Material': 'CraftMat6', 'x1': 100, 'x2': 80, 'funcType': 'decay'},
        5: {'Name': 'Big Meaty Claws', 'Material': 'DesertB2', 'x1': 4, 'x2': 0, 'funcType': 'add'},
        6: {'Name': 'Sploosh Sploosh', 'Material': 'Fish2', 'x1': 23.5, 'x2': 1.5, 'funcType': 'bigBase'},
        7: {'Name': 'Stronk Tools', 'Material': 'Plat', 'x1': 65, 'x2': 70, 'funcType': 'decay'},
        8: {'Name': 'Fmj', 'Material': 'Bug4', 'x1': 0.5, 'x2': 0, 'funcType': 'add'},
        9: {'Name': 'Bappity Boopity', 'Material': 'CraftMat8', 'x1': 35, 'x2': 100, 'funcType': 'decay'},
        10: {'Name': 'Brittley Spears', 'Material': 'Critter1', 'x1': 40, 'x2': 50, 'funcType': 'decay'},
        11: {'Name': 'Call Me Bob', 'Material': 'SnowA3', 'x1': 25, 'x2': 2.5, 'funcType': 'bigBase'},
        12: {'Name': 'Carpenter', 'Material': 'Refinery2', 'x1': 5, 'x2': 50, 'funcType': 'decay'},
        13: {'Name': 'Buff Boi Talent', 'Material': 'Critter4', 'x1': 5, 'x2': 1, 'funcType': 'bigBase'},
        14: {'Name': 'Orange Bargain', 'Material': 'Soul4', 'x1': 40, 'x2': 12, 'funcType': 'decay'},
        15: {'Name': 'Penny Of Strength', 'Material': 'Fish5', 'x1': 18, 'x2': 30, 'funcType': 'decay'},
        16: {'Name': 'Multorange', 'Material': 'GalaxyA3', 'x1': 1.4, 'x2': 30, 'funcType': 'decayMulti'},
        17: {'Name': 'Dream Of Ironfish', 'Material': 'CraftMat13', 'x1': 12, 'x2': 30, 'funcType': 'decay'},
        18: {'Name': 'Shimmeron', 'Material': 'CraftMat14', 'x1': 80, 'x2': 40, 'funcType': 'decay'},
        19: {'Name': 'Bite But Not Chew', 'Material': 'GalaxyC4', 'x1': 50, 'x2': 40, 'funcType': 'decay'},
        20: {'Name': 'Spear Powah', 'Material': 'Bits', 'x1': 40, 'x2': 60, 'funcType': 'decay'},
        21: {'Name': 'Slabi Orefish', 'Material': 'Soul6', 'x1': 3, 'x2': 60, 'funcType': 'decay'},
        22: {'Name': 'Gamer At Heart', 'Material': 'SailTr9', 'x1': 20, 'x2': 60, 'funcType': 'decay'},
        23: {'Name': 'Slabi Strength', 'Material': 'LavaB3b', 'x1': 25, 'x2': 60, 'funcType': 'decay'},
        24: {'Name': 'Power Trione', 'Material': 'SailTr20', 'x1': 23, 'x2': 50, 'funcType': 'decay'},
        25: {'Name': 'Farquad Force', 'Material': 'Basic-Crop-4', 'x1': 30, 'x2': 60, 'funcType': 'decay'},
        26: {'Name': 'Endgame Eff I', 'Material': 'SpiA2b', 'x1': 3, 'x2': 60, 'funcType': 'decay'},
        27: {'Name': 'Tome Strength', 'Material': 'Yellow-Essence', 'x1': 2.5, 'x2': 60, 'funcType': 'decay'},
        28: {'Name': 'Essence Boost-Orange', 'Material': 'Tree13', 'x1': 50, 'x2': 60, 'funcType': 'decay'},
        29: {'Name': 'Crop Chapter', 'Material': 'Purple-Essence', 'x1': 12, 'x2': 50, 'funcType': 'decay'},
        30: {'Name': 'Orange30', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        31: {'Name': 'Orange31', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        32: {'Name': 'Orange32', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        33: {'Name': 'Orange33', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        34: {'Name': 'Orange34', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        35: {'Name': 'Orange35', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        36: {'Name': 'Orange36', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        37: {'Name': 'Orange37', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        38: {'Name': 'Orange38', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        39: {'Name': 'Orange39', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
    },  #Orange Bubbles
    1: {
        0: {'Name': 'Swift Steppin', 'Material': 'Copper', 'x1': 1, 'x2': 0, 'funcType': 'add'},
        1: {'Name': 'Archer Or Bust', 'Material': 'Grasslands1', 'x1': 2, 'x2': 50, 'funcType': 'decayMulti'},
        2: {'Name': 'Hammer Hammer', 'Material': 'Iron', 'x1': 23, 'x2': 2, 'funcType': 'bigBase'},
        3: {'Name': 'Lil Big Damage', 'Material': 'Fish1', 'x1': 20, 'x2': 100, 'funcType': 'decay'},
        4: {'Name': 'Anvilnomics', 'Material': 'ForestTree', 'x1': 40, 'x2': 100, 'funcType': 'decay'},
        5: {'Name': 'Quick Slap', 'Material': 'DesertB1', 'x1': 4, 'x2': 0, 'funcType': 'add'},
        6: {'Name': 'Sanic Tools', 'Material': 'Jungle1', 'x1': 65, 'x2': 70, 'funcType': 'decay'},
        7: {'Name': 'Bug^2', 'Material': 'Bug3', 'x1': 23.5, 'x2': 1.5, 'funcType': 'bigBase'},
        8: {'Name': 'Shaquracy', 'Material': 'Fish4', 'x1': 1, 'x2': 0, 'funcType': 'add'},
        9: {'Name': 'Cheap Shot', 'Material': 'Bug5', 'x1': 7, 'x2': 100, 'funcType': 'decay'},
        10: {'Name': 'Bow Jack', 'Material': 'Soul1', 'x1': 40, 'x2': 50, 'funcType': 'decay'},
        11: {'Name': 'Call Me Ash', 'Material': 'SaharanFoal', 'x1': 25, 'x2': 2, 'funcType': 'bigBase'},
        12: {'Name': 'Cuz I Catch Em All', 'Material': 'Soul3', 'x1': 3, 'x2': 100, 'funcType': 'decayMulti'},
        13: {'Name': 'Fast Boi Talent', 'Material': 'Bug6', 'x1': 5, 'x2': 1, 'funcType': 'bigBase'},
        14: {'Name': 'Green Bargain', 'Material': 'Critter5', 'x1': 40, 'x2': 12, 'funcType': 'decay'},
        15: {'Name': 'Dollar Of Agility', 'Material': 'CraftMat11', 'x1': 18, 'x2': 30, 'funcType': 'decay'},
        16: {'Name': 'Premigreen', 'Material': 'Critter8', 'x1': 1.4, 'x2': 30, 'funcType': 'decayMulti'},
        17: {'Name': 'Fly In Mind', 'Material': 'Bug7', 'x1': 12, 'x2': 40, 'funcType': 'decay'},
        18: {'Name': 'Kill Per Kill', 'Material': 'Refinery4', 'x1': 70, 'x2': 40, 'funcType': 'decay'},
        19: {'Name': 'Afk Expexp', 'Material': 'Bug8', 'x1': 40, 'x2': 40, 'funcType': 'decay'},
        20: {'Name': 'Bow Power', 'Material': 'Bits', 'x1': 40, 'x2': 60, 'funcType': 'decay'},
        21: {'Name': 'Slabo Critterbug', 'Material': 'Tree9', 'x1': 3, 'x2': 60, 'funcType': 'decay'},
        22: {'Name': 'Sailor At Heart', 'Material': 'SailTr11', 'x1': 16, 'x2': 60, 'funcType': 'decay'},
        23: {'Name': 'Slabo Agility', 'Material': 'LavaB6', 'x1': 25, 'x2': 60, 'funcType': 'decay'},
        24: {'Name': 'Power Tritwo', 'Material': 'SailTr24', 'x1': 23, 'x2': 50, 'funcType': 'decay'},
        25: {'Name': 'Quickdraw Quiver', 'Material': 'Jade-Coin', 'x1': 40, 'x2': 60, 'funcType': 'decay'},
        26: {'Name': 'Essence Boost-Green', 'Material': 'Tree12', 'x1': 50, 'x2': 60, 'funcType': 'decay'},
        27: {'Name': 'Endgame Eff II', 'Material': 'Bulbo-Crop-0', 'x1': 3, 'x2': 60, 'funcType': 'decay'},
        28: {'Name': 'Tome Agility', 'Material': 'Bug13', 'x1': 2.5, 'x2': 60, 'funcType': 'decay'},
        29: {'Name': 'Stealth Chapter', 'Material': 'Mushie-Crop-15', 'x1': 10, 'x2': 50, 'funcType': 'decay'},
        30: {'Name': 'Green30', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        31: {'Name': 'Green31', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        32: {'Name': 'Green32', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        33: {'Name': 'Green33', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        34: {'Name': 'Green34', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        35: {'Name': 'Green35', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        36: {'Name': 'Green36', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        37: {'Name': 'Green37', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        38: {'Name': 'Green38', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        39: {'Name': 'Green39', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
    },  #Green Bubbles
    2: {
        0: {'Name': 'Stable Jenius', 'Material': 'BirchTree', 'x1': 1, 'x2': 0, 'funcType': 'add'},
        1: {'Name': 'Mage Is Best', 'Material': 'Grasslands1', 'x1': 2, 'x2': 50, 'funcType': 'decayMulti'},
        2: {'Name': 'Hocus Choppus', 'Material': 'CraftMat5', 'x1': 50, 'x2': 100, 'funcType': 'decay'},
        3: {'Name': 'Molto Loggo', 'Material': 'IronBar', 'x1': 23.5, 'x2': 1.5, 'funcType': 'bigBase'},
        4: {'Name': 'Noodubble', 'Material': 'CraftMat7', 'x1': 100, 'x2': 60, 'funcType': 'decay'},
        5: {'Name': 'Name I Guess', 'Material': 'Gold', 'x1': 4, 'x2': 0, 'funcType': 'add'},
        6: {'Name': 'Le Brain Tools', 'Material': 'Bug3', 'x1': 65, 'x2': 70, 'funcType': 'decay'},
        7: {'Name': 'Cookin Roadkill', 'Material': 'ToiletTree', 'x1': 120, 'x2': 70, 'funcType': 'decay'},
        8: {'Name': 'Brewstachio', 'Material': 'DesertC1', 'x1': 50, 'x2': 100, 'funcType': 'decay'},
        9: {'Name': 'All For Kill', 'Material': 'StumpTree', 'x1': 40, 'x2': 100, 'funcType': 'decay'},
        10: {'Name': 'Matty Stafford', 'Material': 'Refinery1', 'x1': 40, 'x2': 50, 'funcType': 'decay'},
        11: {'Name': 'Call Me Pope', 'Material': 'Critter2', 'x1': 2.4, 'x2': 70, 'funcType': 'decayMulti'},
        12: {'Name': 'Gospel Leader', 'Material': 'Bug5', 'x1': 60, 'x2': 30, 'funcType': 'decay'},
        13: {'Name': 'Smart Boi Talent', 'Material': 'SnowC1', 'x1': 5, 'x2': 1, 'funcType': 'bigBase'},
        14: {'Name': 'Purple Bargain', 'Material': 'Soul1', 'x1': 40, 'x2': 12, 'funcType': 'decay'},
        15: {'Name': 'Nickel Of Wisdom', 'Material': 'AlienTree', 'x1': 18, 'x2': 30, 'funcType': 'decay'},
        16: {'Name': 'Severapurple', 'Material': 'Void', 'x1': 1.4, 'x2': 30, 'funcType': 'decayMulti'},
        17: {'Name': 'Tree Sleeper', 'Material': 'Soul5', 'x1': 12, 'x2': 40, 'funcType': 'decay'},
        18: {'Name': 'Hyperswift', 'Material': 'Fish7', 'x1': 30, 'x2': 30, 'funcType': 'decay'},
        19: {'Name': 'Matrix Evolved', 'Material': 'Tree8', 'x1': 60, 'x2': 40, 'funcType': 'decay'},
        20: {'Name': 'Wand Pawur', 'Material': 'Bits', 'x1': 40, 'x2': 60, 'funcType': 'decay'},
        21: {'Name': 'Slabe Logsoul', 'Material': 'Bug9', 'x1': 3, 'x2': 60, 'funcType': 'decay'},
        22: {'Name': 'Pious At Heart', 'Material': 'SailTr13', 'x1': 300, 'x2': 100, 'funcType': 'decay'},
        23: {'Name': 'Slabe Wisdom', 'Material': 'LavaC1', 'x1': 25, 'x2': 60, 'funcType': 'decay'},
        24: {'Name': 'Power Trithree', 'Material': 'SailTr28', 'x1': 23, 'x2': 50, 'funcType': 'decay'},
        25: {'Name': 'Smarter Spells', 'Material': 'White-Essence', 'x1': 25, 'x2': 60, 'funcType': 'decay'},
        26: {'Name': 'Endgame Eff III', 'Material': 'Green-Essence', 'x1': 3, 'x2': 60, 'funcType': 'decay'},
        27: {'Name': 'Essence Boost-Purple', 'Material': 'Soul7', 'x1': 50, 'x2': 100, 'funcType': 'decay'},
        28: {'Name': 'Tome Wisdom', 'Material': 'Sushi-Crop-11', 'x1': 2.5, 'x2': 60, 'funcType': 'decay'},
        29: {'Name': 'Essence Chapter', 'Material': 'Jade-Coin', 'x1': 15, 'x2': 50, 'funcType': 'decay'},
        30: {'Name': 'Purple30', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        31: {'Name': 'Purple31', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        32: {'Name': 'Purple32', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        33: {'Name': 'Purple33', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        34: {'Name': 'Purple34', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        35: {'Name': 'Purple35', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        36: {'Name': 'Purple36', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        37: {'Name': 'Purple37', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        38: {'Name': 'Purple38', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        39: {'Name': 'Purple39', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
    },  #Purple Bubbles
    3: {
        0: {'Name': 'Lotto Skills', 'Material': 'CraftMat1', 'x1': 1, 'x2': 0, 'funcType': 'add'},
        1: {'Name': 'Droppin Loads', 'Material': 'Fish1', 'x1': 40, 'x2': 70, 'funcType': 'decay'},
        2: {'Name': 'Startue Exp', 'Material': 'DesertA1', 'x1': 25, 'x2': 60, 'funcType': 'decay'},
        3: {'Name': 'Level Up Gift', 'Material': 'DesertA3', 'x1': 100, 'x2': 30, 'funcType': 'decay'},
        4: {'Name': 'Prowesessary', 'Material': 'ToiletTree', 'x1': 1.5, 'x2': 60, 'funcType': 'decayMulti'},
        5: {'Name': 'Stamp Tramp', 'Material': 'Bug2', 'x1': 1, 'x2': 0, 'funcType': 'add'},
        6: {'Name': 'Undeveloped Costs', 'Material': 'Fish3', 'x1': 40, 'x2': 70, 'funcType': 'decay'},
        7: {'Name': 'Da Daily Drip', 'Material': 'CraftMat9', 'x1': 30, 'x2': 100, 'funcType': 'decay'},
        8: {'Name': 'Grind Time', 'Material': 'Liquid1', 'x1': 9.7, 'x2': 0.3, 'funcType': 'bigBase'},
        9: {'Name': 'Laaarrrryyyy', 'Material': 'Dementia', 'x1': 120, 'x2': 100, 'funcType': 'decay'},
        10: {'Name': 'Cogs For Hands', 'Material': 'SnowA2', 'x1': 4, 'x2': 0, 'funcType': 'add'},
        11: {'Name': 'Sample It', 'Material': 'Soul2', 'x1': 12, 'x2': 40, 'funcType': 'decay'},
        12: {'Name': 'Big Game Hunter', 'Material': 'Critter3', 'x1': 60, 'x2': 30, 'funcType': 'decay'},
        13: {'Name': 'Ignore Overdues', 'Material': 'Tree7', 'x1': 100, 'x2': 60, 'funcType': 'decay'},
        14: {'Name': 'Yellow Bargain', 'Material': 'Critter6', 'x1': 40, 'x2': 12, 'funcType': 'decay'},
        15: {'Name': 'Mr Massacre', 'Material': 'Refinery3', 'x1': 90, 'x2': 50, 'funcType': 'decay'},
        16: {'Name': 'Egg Ink', 'Material': 'Spice0', 'x1': 40, 'x2': 40, 'funcType': 'decay'},
        17: {'Name': 'Diamond Chef', 'Material': 'Spice6', 'x1': 0.3, 'x2': 13, 'funcType': 'decayMulti'},
        18: {'Name': 'Card Champ', 'Material': 'Spice9', 'x1': 100, 'x2': 40, 'funcType': 'decay'},
        19: {'Name': 'Petting The Rift', 'Material': 'Critter10', 'x1': 15, 'x2': 50, 'funcType': 'decay'},
        20: {'Name': 'Boaty Bubble', 'Material': 'Bits', 'x1': 135, 'x2': 70, 'funcType': 'decay'},
        21: {'Name': 'Big P', 'Material': 'SailTr1', 'x1': 0.5, 'x2': 60, 'funcType': 'decayMulti'},
        22: {'Name': 'Bit By Bit', 'Material': 'Tree10', 'x1': 50, 'x2': 70, 'funcType': 'decay'},
        23: {'Name': 'Gifts Abound', 'Material': 'Bug10', 'x1': 40, 'x2': 60, 'funcType': 'decay'},
        24: {'Name': 'Atom Split', 'Material': 'LavaC2', 'x1': 14, 'x2': 40, 'funcType': 'decay'},
        25: {'Name': 'Cropius Mapper', 'Material': 'SpiA5', 'x1': 5, 'x2': 70, 'funcType': 'decay'},
        26: {'Name': 'Essence Boost-Yellow', 'Material': 'Bug12', 'x1': 50, 'x2': 60, 'funcType': 'decay'},
        27: {'Name': 'Hinge Buster', 'Material': 'Earthy-Crop-9', 'x1': 100, 'x2': 70, 'funcType': 'decay'},
        28: {'Name': 'Ninja Looter', 'Material': 'Blue-Essence', 'x1': 0.5, 'x2': 60, 'funcType': 'decayMulti'},
        29: {'Name': 'Lo Cost Mo Jade', 'Material': 'SpiD1', 'x1': 99, 'x2': 40, 'funcType': 'decay'},
        30: {'Name': 'Yellow30', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        31: {'Name': 'Yellow31', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        32: {'Name': 'Yellow32', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        33: {'Name': 'Yellow33', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        34: {'Name': 'Yellow34', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        35: {'Name': 'Yellow35', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        36: {'Name': 'Yellow36', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        37: {'Name': 'Yellow37', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        38: {'Name': 'Yellow38', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
        39: {'Name': 'Yellow39', 'Material': '', 'x1': 0, 'x2': 0, 'funcType': 'decay'},
    },  #Yellow Bubbles
}
atrisk_basicBubbles = [
    "Roid Ragin",
    "Hearty Diggy",
    "Wyoming Blood",
    "Sploosh Sploosh",
    "Stronk Tools",
    "Fmj",
    "Swift Steppin",
    "Hammer Hammer",
    "Lil Big Damage",
    "Anvilnomics",
    "Bug^2",
    "Shaquracy",
    "Cheap Shot",
    "Call Me Ash",
    "Fast Boi Talent",
    "Stable Jenius",
    "Name I Guess",
    "Le Brain Tools",
    "Cookin Roadkill",
    "All For Kill",
    "Gospel Leader",
    "Droppin Loads",
    "Prowesessary",
    "Stamp Tramp",
    "Undeveloped Costs",
    "Laaarrrryyyy",
    "Ignore Overdues",
]
atrisk_lithiumBubbles = [
    "Penny Of Strength",
    "Fly In Mind",
    'Afk Expexp',
    'Slabbo Critterbug',
    'Nickel Of Wisdom',
    'Severapurple',
    'Hyperswift',
    'Matrix Evolved',
    'Slabe Logsoul',
    'Bit By Bit',
    'Gifts Abound',
]
def getReadableVialNames(inputNumber):
    try:
        return f"{vialsDict[int(inputNumber)]['Name']} ({getItemDisplayName(vialsDict[int(inputNumber)]['Material'])})"
    except:
        return f"Unknown Vial {inputNumber}"

def getReadableBubbleNames(inputNumber, color):
    try:
        return bubblesDict[bubbleCauldronColorList.index(color)][inputNumber]
    except:
        return f"Unknown {color} Bubble {inputNumber}"


###WORLD 3 CONSTS###
maxDreams = 31  # Last verified as of v2.10
dreamsThatUnlockNewBonuses = [1, 3, 6, 8, 11, 14, 18, 21, 24, 29]
equinoxBonusesDict = {
    2: {'Name': 'Equinox Dreams', 'BaseLevel': 5, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 5, 'Category': 'Recommended'},
    3: {'Name': 'Equinox Resources', 'BaseLevel': 4, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 4, 'Category': 'Recommended'},
    4: {'Name': 'Shades of K', 'BaseLevel': 3, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 3, 'Category': 'Optional'},
    5: {'Name': 'Liquidvestment', 'BaseLevel': 4, 'MaxLevelIncreases': {7: 3, 16: 4}, 'FinalMaxLevel': 11, 'Category': 'Recommended'},
    6: {'Name': 'Matching Scims', 'BaseLevel': 8, 'MaxLevelIncreases': {13: 5, 19: 10}, 'FinalMaxLevel': 23, 'Category': 'Recommended'},
    7: {'Name': 'Slow Roast Wiz', 'BaseLevel': 5, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 5, 'Category': 'Recommended'},
    8: {'Name': 'Laboratory Fuse', 'BaseLevel': 10, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 10, 'Category': 'Optional'},
    9: {'Name': 'Metal Detector', 'BaseLevel': 6, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 6, 'Category': 'Recommended'},
    10: {'Name': 'Faux Jewels', 'BaseLevel': 6, 'MaxLevelIncreases': {22: 5, 27: 10}, 'FinalMaxLevel': 21, 'Category': 'Recommended'},
    11: {'Name': 'Food Lust', 'BaseLevel': 10, 'MaxLevelIncreases': {26: 4}, 'FinalMaxLevel': 14, 'Category': 'Optional'},
    12: {'Name': 'Equinox Symbols', 'BaseLevel': 5, 'MaxLevelIncreases': {31: 4}, 'FinalMaxLevel': 9, 'Category': 'Recommended'},
}
buildingsDict = {
    #Buildings
    0: {'Name': '3D Printer', 'Image': 'three-d-printer', 'BaseMaxLevel': 10, 'Type': 'Utility'},
    1: {'Name': 'Talent Book Library', 'Image': 'talent-book-library', 'BaseMaxLevel': 101, 'Type': 'Utility'},
    2: {'Name': 'Death Note', 'Image': 'death-note', 'BaseMaxLevel': 51, 'Type': 'Utility'},
    3: {'Name': 'Salt Lick', 'Image': 'salt-lick', 'BaseMaxLevel': 10, 'Type': 'Utility'},
    4: {'Name': 'Chest Space', 'Image': 'chest-space', 'BaseMaxLevel': 25, 'Type': 'Utility'},
    5: {'Name': 'Cost Cruncher', 'Image': 'cost-cruncher','BaseMaxLevel': 60, 'Type': 'Utility'},
    6: {'Name': 'Trapper Drone', 'Image': 'critter-drone', 'BaseMaxLevel': 15, 'Type': 'Utility'},
    7: {'Name': 'Automation Arm', 'Image': 'automation-arm', 'BaseMaxLevel': 5, 'Type': 'Utility'},
    8: {'Name': 'Atom Collider', 'Image': 'atom-collider', 'BaseMaxLevel': 200, 'Type': 'Utility'},
    #TD Towers
    9: {'Name': 'Pulse Mage', 'Image': 'pulse-mage', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    10: {'Name': 'Fireball Lobber', 'Image': 'fireball-lobber', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    11: {'Name': 'Boulder Roller', 'Image': 'boulder-roller', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    12: {'Name': 'Frozone Malone', 'Image': 'frozone-malone', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    13: {'Name': 'Stormcaller', 'Image': 'stormcaller', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    14: {'Name': 'Party Starter', 'Image': 'party-starter', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    15: {'Name': 'Kraken Cosplayer', 'Image': 'kraken-cosplayer', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    16: {'Name': 'Poisonic Elder', 'Image': 'poisonic-elder', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    17: {'Name': 'Voidinator', 'Image': 'voidinator', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    #Shrines
    18: {'Name': 'Woodular Shrine', 'Image': 'woodular-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    19: {'Name': 'Isaccian Shrine', 'Image': 'isaccian-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    20: {'Name': 'Crystal Shrine', 'Image': 'crystal-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    21: {'Name': 'Pantheon Shrine', 'Image': 'pantheon-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    22: {'Name': 'Clover Shrine', 'Image': 'clover-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    23: {'Name': 'Summereading Shrine', 'Image': 'summereading-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    24: {'Name': 'Crescent Shrine', 'Image': 'crescent-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    25: {'Name': 'Undead Shrine', 'Image': 'undead-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
    26: {'Name': 'Primordial Shrine', 'Image': 'primordial-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine'},
}
buildingsTowerMaxLevel = 140
shrinesList: list[str] = [
    "Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine", "Clover Shrine", "Summereading Shrine", "Crescent Shrine", "Undead Shrine", "Primordial Shrine"
]
#AtomInfo in code. Last pulled 2.11 Kanga
atomsList: list[list] = [
    ["Hydrogen - Stamp Decreaser", 1, 1.35, 2, 1, "Every day you log in, the resource cost to upgrade a stamp's max lv decreases by {% up to a max of 90%. This reduction resets back to 0% when upgrading any stamp max lv."],
    ["Helium - Talent Power Stacker", 0, 10, 10, 1, "All talents that give more bonus per 'Power of 10 resources you own' will count +{ more powers of 10 than you actually own when giving the bonus."],
    ["Lithium - Bubble Insta Expander", 10, 1.25, 25, 1, "No Bubble Left Behind bonus now has a 15% chance to level up the lowest bubble out of ALL bubbles, not just the first 15 of each colour. Also, +{% chance to give +1 additional Lv."],
    ["Beryllium - Post Office Penner", 20, 1.26, 75, 7, "Every day, 1 silver pen from your Post Office will instantly convert into 1 PO Box for all characters. This conversion happens { times per day."],
    ["Boron - Particle Upgrader", 70, 1.37, 175, 2, "When a bubble has a cost of 100M or more to upgrade, you can instead spend particles. However, you can only do this { times a day, after which the cost will return to resources."],
    ["Carbon - Wizard Maximizer", 250, 1.27, 500, 2, "All wizard towers in construction get +{ max levels. Also, all wizards get a +2% damage bonus for each wizard tower level above 50 in construction. Total bonus: }% wizard dmg."],
    ["Nitrogen - Construction Trimmer", 500, 1.25, 1000, 15, "Gold trimmed construction slots give +{% more build rate than before. Also, you now have 1 additional trimmed slot."],
    ["Oxygen - Library Booker", 2000, 1.24, 3250, 2, "Increases the Checkout Refresh Speed of the Talent Library by +{%. Also, the Minimum Talent LV is increased by +<, and the Maximum Talent LV is increased by +10."],
    ["Fluoride - Void Plate Chef", 12000, 1.23, 10000, 1, "Multiplies your cooking speed by +{% for every meal at Lv 30+. In other words, every plate with a studded black void plate. Total bonus: >% cooking speed"],
    ["Neon - Damage N' Cheapener", 40000, 1.22, 40000, 1, "Increases your total damage by +{%. Also, reduces the cost of all atom upgrades by {% too."],
    ["Sodium - Snail Kryptonite", 50000, 2, 50000, 5, "When you fail a snail upgrade, it's LV gets reset to the nearest 5 (Up to Lv {) instead of back to 0, like failing at Lv 7 will reset to Lv 5."],
]
colliderStorageLimitList = [15, 25, 100, 250, 1050]
prayersList: list[str] = [
    "Big Brain Time (Forest Soul)", "Skilled Dimwit (Forest Soul)", "Unending Energy (Forest Soul)",
    "Shiny Snitch (Forest Soul)", "Zerg Rushogen (Forest Soul)",
    "Tachion of the Titans (Dune Soul)", "Balance of Precision (Dune Soul)", "Midas Minded (Dune Soul)", "Jawbreaker (Dune Soul)",
    "The Royal Sampler (Rooted Soul)", "Antifun Spirit (Rooted Soul)", "Circular Criticals (Rooted Soul)", "Ruck Sack (Rooted Soul)",
    "Fibers of Absence (Frigid Soul)", "Vacuous Tissue (Frigid Soul)", "Beefy For Real (Frigid Soul)",
    "Balance of Pain (Squishy Soul)", "Balance of Proficiency (Squishy Soul)","Glitterbug (Squishy Soul)",
]
prayersDict = {
    0: {"Name": "Big Brain Time", "Material": "Forest Soul", "Display": "Big Brain Time (Forest Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Class EXP', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 225, 'curse_x2': 25, 'curse_stat': 'Max HP for all monsters', 'curse_pre': '+', 'curse_post': '%'},
    1: {"Name": "Skilled Dimwit", "Material": "Forest Soul", "Display": "Skilled Dimwit (Forest Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Skill Efficiency', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 18, 'curse_x2': 2, 'curse_stat': 'Skill EXP Gain', 'curse_pre': '-', 'curse_post': '%'},
    2: {"Name": "Unending Energy", "Material": "Forest Soul", "Display": "Unending Energy (Forest Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 22.5, 'bonus_x2': 2.5, 'bonus_stat': 'Class and Skill EXP', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 1, 'curse_x2': 0, 'curse_stat': 'Max AFK time is now 10 hours. Use with caution', 'curse_pre': '', 'curse_post': ''},
    3: {"Name": "Shiny Snitch", "Material": "Forest Soul", "Display": "Shiny Snitch (Forest Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 18, 'bonus_x2': 2, 'bonus_stat': 'Shiny Critters per trap', 'bonus_pre': '+', 'bonus_post': '',
        "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'lower', 'curse_pre': 'Your Shiny chance is now ', 'curse_post': 'x'},
    4: {"Name": "Zerg Rushogen", "Material": "Forest Soul", "Display": "Zerg Rushogen (Forest Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 4.5, 'bonus_x2': 0.5, 'bonus_stat': 'All AFK Gain Rate', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 10.8, 'curse_x2': 1.2, 'curse_stat': 'Carry Capacity', 'curse_pre': '-', 'curse_post': '%'},
    5: {"Name": "Tachion of the Titans", "Material": "Dune Soul", "Display": "Tachion of the Titans (Dune Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 1, 'bonus_x2': 0, 'bonus_stat': 'Giant Monsters can now spawn on Monster Kill', 'bonus_pre': '', 'bonus_post': '',
        "curse_funcType": 'bigBase', 'curse_x1': 1, 'curse_x2': 0, 'curse_stat': 'Giant Monsters can now spawn...', 'curse_pre': '', 'curse_post': ''},
    6: {"Name": "Balance of Precision", "Material": "Dune Soul", "Display": "Balance of Precision (Dune Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Total Accuracy', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 4.5, 'curse_x2': 0.5, 'curse_stat': 'Total Damage', 'curse_pre': '-', 'curse_post': '%'},
    7: {"Name": "Midas Minded", "Material": "Dune Soul", "Display": "Midas Minded (Dune Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 18, 'bonus_x2': 2, 'bonus_stat': 'Drop Rate', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 225, 'curse_x2': 2.5, 'curse_stat': 'Max HP for all monsters', 'curse_pre': '+', 'curse_post': '%'},
    8: {"Name": "Jawbreaker", "Material": "Dune Soul", "Display": "Jawbreaker (Dune Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 36, 'bonus_x2': 4, 'bonus_stat': 'Coins from Monsters', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 180, 'curse_x2': 20, 'curse_stat': 'Max HP for all monsters', 'curse_pre': '+', 'curse_post': '%'},
    9: {"Name": "The Royal Sampler", "Material": "Rooted Soul", "Display": "The Royal Sampler (Rooted Soul)",
        "bonus_funcType": 'bigBase', 'bonus_x1': 13.5, 'bonus_x2': 1.5, 'bonus_stat': 'Printer Sample Rate', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 27, 'curse_x2': 3, 'curse_stat': 'All EXP gain. Remove all samples on this character to Unequip.', 'curse_pre': '-', 'curse_post': '%'},
    10: {"Name": "Antifun Spirit", "Material": "Rooted Soul", "Display": "Antifun Spirit (Rooted Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 630, 'bonus_x2': 70, 'bonus_stat': 'Minigame Reward Multi', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 8.1, 'curse_x2': 0.9, 'curse_stat': 'plays per attempt', 'curse_pre': 'Minigames cost ', 'curse_post': ''},
    11: {"Name": "Circular Criticals", "Material": "Rooted Soul", "Display": "Circular Criticals (Rooted Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 9, 'bonus_x2': 1, 'bonus_stat': 'Critical Hit Chance', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'Critical Damage', 'curse_pre': '-', 'curse_post': '%'},
    12: {"Name": "Ruck Sack", "Material": "Rooted Soul", "Display": "Ruck Sack (Rooted Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Carry Capacity', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'All AFK Gain Rate', 'curse_pre': '-', 'curse_post': '%'},
    13: {"Name": "Fibers of Absence", "Material": "Frigid Soul", "Display": "Fibers of Absence (Frigid Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Kills for Deathnote and opening portals', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'Total Damage', 'curse_pre': '-', 'curse_post': '%'},
    14: {"Name": "Vacuous Tissue", "Material": "Frigid Soul", "Display": "Vacuous Tissue (Frigid Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 100, 'bonus_x2': 0, 'bonus_stat': 'Dungeon Credits and Flurbos from Boosted Runs', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 2, 'curse_x2': 0, 'curse_stat': 'Dungeon Passes per run', 'curse_pre': 'Use ', 'curse_post': 'x'},
    15: {"Name": "Beefy For Real", "Material": "Frigid Soul", "Display": "Beefy For Real (Frigid Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 18, 'bonus_x2': 2, 'bonus_stat': 'Total Damage', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 9, 'curse_x2': 1, 'curse_stat': 'Total Defence and Accuracy', 'curse_pre': '-', 'curse_post': '%'},
    16: {"Name": "Balance of Pain", "Material": "Squishy Soul", "Display": "Balance of Pain (Squishy Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 7.2, 'bonus_x2': 0.8, 'bonus_stat': 'Multikill per Damage Tier', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'Total Defence and Accuracy', 'curse_pre': '-', 'curse_post': '%'},
    17: {"Name": "Balance of Proficiency", "Material": "Squishy Soul", "Display": "Balance of Proficiency (Squishy Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Skill EXP Gain', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 18, 'curse_x2': 2, 'curse_stat': 'Skill Efficiency', 'curse_pre': '-', 'curse_post': '%'},
    18: {"Name": "Glitterbug", "Material": "Squishy Soul", "Display": "Glitterbug (Squishy Soul)",
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'chance for Giant Mobs to summon 2 Crystal Mobs', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 18, 'curse_x2': 2, 'curse_stat': 'less likely to spawn', 'curse_pre': 'Giant Mobs are ', 'curse_post': '%'},
}
saltLickList: list[str] = [
    'Printer Sample Size', 'Obol Storage', 'Refinery Speed', 'EXP', 'Max Book',
    'Alchemy Liquids', 'TD Points', 'Movespeed', 'Multikill', 'Damage',
]
maxStaticBookLevels = 140
maxScalingBookLevels = 30
maxSummoningBookLevels = 29
maxOverallBookLevels = 100 + maxStaticBookLevels + maxScalingBookLevels + maxSummoningBookLevels

###WORLD 4 CONSTS###
maxCookingTables = 10  # Last verified as of v2.10
maxMeals = 67  # Last verified as of v2.10
maxMealLevel = 90  # Last verified as of v2.10
cookingCloseEnough = 450

cookingMealDict = {
    0:{"Name": "Turkey a la Thank", "Description": "Do I smell gratitude? Oh, no, that's colonialization...", "Effect": "+{% Total Damage", "BaseValue": 2},
    1:{"Name": "Egg", "Description": "It's just an egg.", "Effect": "+{% Meal Cooking Speed", "BaseValue": 5},
    2:{"Name": "Salad", "Description": "Yea uhm, could I get a burger, but hold the meat and buns?", "Effect": "+{% Cash from Monsters", "BaseValue": 3},
    3:{"Name": "Pie", "Description": "Cartoon characters with a fear of levitation HATE the smell of this!", "Effect": "+{% New Recipe Cooking Speed", "BaseValue": 5},
    4:{"Name": "Frenk Fries", "Description": "You're breeding pets in outer space, don't be shocked that there's no France!", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 5},
    5:{"Name": "Spaghetti", "Description": "Your mom made this. It's her spaghetti.", "Effect": "+{% Breeding EXP", "BaseValue": 4},
    6:{"Name": "Corn", "Description": "To think the government is subsidizing this... its bonus is terrible!!!", "Effect": "+{% Skill Efficiency", "BaseValue": 2},
    7:{"Name": "Garlic Bread", "Description": "The letter H ain't lookin' so good after eating a few of these...", "Effect": "+{% VIP Library Membership", "BaseValue": 4},
    8:{"Name": "Garlicless Bread", "Description": "Many revolutions in the world originate from an increase in the price of bread", "Effect": "+{% Lab EXP", "BaseValue": 2},
    9:{"Name": "Pizza", "Description": "Mama mia mahhh piiiiiiiizzza!!! Wait I already did that joke, replace this one", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 9},
    10:{"Name": "Apple", "Description": "Aw jeez Richard, I sure am hungry for apples!", "Effect": "+{ Base DEF", "BaseValue": 5},
    11:{"Name": "Pancakes", "Description": "Ohhh, they're called 'pan'cakes because they're like cakes made in a pan haha", "Effect": "+{Px Line Width in Lab Mainframe", "BaseValue": 2},
    12:{"Name": "Corndog", "Description": "Ohhh, they're called 'corn'dogs because... wait, why are they called corndogs?", "Effect": "+{% Meal Cooking Speed", "BaseValue": 12},
    13:{"Name": "Cabbage", "Description": "This is a MONUMENTALLY IMPORTANT vegetable, as well as upgrade.", "Effect": "+{% All Cooking Spd per 10 upgrade Lvs", "BaseValue": 5},
    14:{"Name": "Potato Pea Pastry", "Description": "Yuhhhh it's that Triple P threat! Look out for them P's bro!", "Effect": "+{% Lower Egg Incubator Time", "BaseValue": 1},
    15:{"Name": "Dango", "Description": "Look, I'm not sure what these are either, just go with it.", "Effect": "+{% Lower Kitchen Upgrade Costs", "BaseValue": 2},
    16:{"Name": "Sourish Fish", "Description": "Shhh stop saying they're sweet, you're gonna get me in trouble!", "Effect": "+{% VIP Library Membership", "BaseValue": 4},
    17:{"Name": "Octoplop", "Description": "They really did just plop an octopus on a plate and call it a day.", "Effect": "+{% Total Damage", "BaseValue": 2},
    18:{"Name": "Croissant", "Description": "Carl loves these!", "Effect": "+{% Pet Fighting Damage", "BaseValue": 1},
    19:{"Name": "Canopy", "Description": "...oh, you said 'Can of Pea's. You know, that does make a lot more sense.", "Effect": "+{% New Recipe Cooking Speed", "BaseValue": 10},
    20:{"Name": "Cannoli", "Description": "Ain't got no joke for this one, it's existence is enough of a joke.", "Effect": "+{% Points earned in Tower Defence", "BaseValue": 1},
    21:{"Name": "Cheese", "Description": "Sourced organically, straight from the moon!", "Effect": "+{% Cooking EXP", "BaseValue": 5},
    22:{"Name": "Sawdust", "Description": "'Id rather starve than eat that' - Angie, 2021", "Effect": "+{% Lab EXP", "BaseValue": 5},
    23:{"Name": "Eggplant", "Description": "Idk what you Zoomers are up to with those eggplant emojis, but I don't like it...", "Effect": "+{% Pet Breedability Speed in Fenceyard", "BaseValue": 5},
    24:{"Name": "Cheesy Bread", "Description": "Another bread meal? Wow so unoriginal, I'm glad I already left a 1 star rating.", "Effect": "+{% Total Accuracy", "BaseValue": 1},
    25:{"Name": "Wild Boar", "Description": "It's not really wild anymore is it, it looks kinda dead and roasted.", "Effect": "+{Px Line Width in Lab Mainframe", "BaseValue": 2},
    26:{"Name": "Donut", "Description": "Mmmmm... doooooooonut...", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 15},
    27:{"Name": "Riceball", "Description": "Dude it's just a ball of rice, like what do you want me to say about it?", "Effect": "+{% Skill Efficiency", "BaseValue": 3},
    28:{"Name": "Cauliflower", "Description": "The white part is called Curd! Hmm, time to recategorize this as an educational game!", "Effect": "+{% Basic Atk Speed", "BaseValue": 1},
    29:{"Name": "Durian Fruit", "Description": "This must have been in the room when Kurt said it smelled like 'teen spirit'...", "Effect": "+{% Lower Kitchen Upgrade costs", "BaseValue": 6},
    30:{"Name": "Orange", "Description": "The true arch-nemesis of rappers and poets alike.", "Effect": "+{% VIP Library Membership", "BaseValue": 3},
    31:{"Name": "Bunt Cake", "Description": "Bunt cake more like Punt cake because I'm kicking this trash straight to the garbage.", "Effect": "+{% Cash from Monsters", "BaseValue": 7},
    32:{"Name": "Chocolate Truffle", "Description": "I mean it's got a bite taken out of it, pretty gross.", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 25},
    33:{"Name": "Leek", "Description": "Prowess lowers the efficiency needed when efficiency bar is orange in AFK info", "Effect": "+{% skilling prowess", "BaseValue": 2},
    34:{"Name": "Fortune Cookie", "Description": "It reads: 'Salvation lies not within enjoying video games, but from gitting gud at them'", "Effect": "+{% Faster Library checkout Speed", "BaseValue": 4},
    35:{"Name": "Pretzel", "Description": "I love pretzels, people really be sleepin' on the versatility they bring to the table!", "Effect": "+{% Lab EXP", "BaseValue": 7},
    36:{"Name": "Sea Urchin", "Description": "At least one person reading this has eating one of these. Oh, it's you? Good for you.", "Effect": "+{% Critters from traps", "BaseValue": 1},
    37:{"Name": "Mashed Potato", "Description": "This nutritious meal reminds me of the potato monster from that IdleOn video game!", "Effect": "+{% Cooking EXP", "BaseValue": 6},
    38:{"Name": "Mutton", "Description": "Yeap I tell you hwat Bobby, this is a real man's meal right here!", "Effect": "+{% Crit Chance", "BaseValue": 1},
    39:{"Name": "Wedding Cake", "Description": "Imagine getting married lol so cringe haha am I right??!?! High-five, fellow kids!", "Effect": "+{% Pet Fighting Damage", "BaseValue": 2},
    40:{"Name": "Eel", "Description": "The younger sibling of the Loch Ness Monster. He's real, but no one really cares.", "Effect": "+{% Line Width in Lab Mainframe", "BaseValue": 1},
    41:{"Name": "Whipped Cocoa", "Description": "Why is this being served on a plate? Was the cup not good enough for you??", "Effect": "+{% Skill Efficiency", "BaseValue": 4},
    42:{"Name": "Onion", "Description": "No, I'm not crying, this onion is just stimulating the lachrymal glands in my eyes.", "Effect": "+{% Total Damage", "BaseValue": 3},
    43:{"Name": "Soda", "Description": "Yea those red marks are grill marks, our chef doesn't know what he's doing.", "Effect": "+{% Meal Cooking Speed", "BaseValue": 20},
    44:{"Name": "Sushi Roll", "Description": "For something called a 'sushi roll', it isn't moving around very much.", "Effect": "+{% VIP Library Membership", "BaseValue": 7},
    45:{"Name": "Buncha Banana", "Description": "Straight from the island of Karjama! Or something like that, starts with a K at least.", "Effect": "+{ Max LVs for TP Pete Star Talent", "BaseValue": 4},
    46:{"Name": "Pumpkin", "Description": "According to the author of the Iliad, its value should peak right around January...", "Effect": "+{% Liquid Cap for liquids 1 and 2", "BaseValue": 2},
    47:{"Name": "Cotton Candy", "Description": "The most exquisite of fairground cuisine!", "Effect": "+{% Divinity EXP", "BaseValue": 2},
    48:{"Name": "Massive Fig", "Description": "This thing has gotta weigh at least 30!", "Effect": "+{% Total Damage", "BaseValue": 3},
    49:{"Name": "Head Chef Geustloaf", "Description": "How DARE you question the honorable Chef Geustloaf's cooking abilities!", "Effect": "+{% Bits Gained in Gaming", "BaseValue": 4},
    50:{"Name": "Kiwi Fruit", "Description": "Is there a reason these are so hard to cook? Aren't you just like... cutting it in half?", "Effect": "+{% Liquid Cap for liquids 3 and 4", "BaseValue": 2},
    51:{"Name": "Popped Corn", "Description": "Effectively no different than a normal bowl of popcorn, but it's still impressive!", "Effect": "+{% Sailing Speed", "BaseValue": 2},
    52:{"Name": "Double Cherry", "Description": "So like... why did the yellow circle want these again? This bonus is pretty bad.", "Effect": "+{% Meal Cooking Speed", "BaseValue": 30},
    53:{"Name": "Ratatouey", "Description": "Hey cmon man how should I know how to spell Ratatouille, there's no France remember?", "Effect": "+{% Lower Kitchen Upgrade costs", "BaseValue": 8},
    54:{"Name": "Giant Tomato", "Description": "It's big, it's large, it's round, it's red, and it'll fill you up thats for sure!", "Effect": "+{% Gaming EXP", "BaseValue": 5},
    55:{"Name": "Wrath Grapes", "Description": "I'd be angry too if I were a grape.", "Effect": "+{% Divinity EXP", "BaseValue": 4},
    56:{"Name": "Sausy Sausage", "Description": "Plump innit! Would go great with some momey milk!", "Effect": "+{% Bits Gained in Gaming", "BaseValue": 6},
    57:{"Name": "Seasoned Marrow", "Description": "You ate all the edible stuff around the bone? Why not try the stuff inside the bone!", "Effect": "+{% Farming EXP", "BaseValue": 3},
    58:{"Name": "Sticky Bun", "Description": "This frosting better be made of superglue or I'm suing for false advertising.", "Effect": "+{% All Summoning Essence Gain", "BaseValue": 5},
    59:{"Name": "Frazzleberry", "Description": "Big. Blue. Beautiful. Boing. Boat. Broom. Balls. Backgammon. Bort.", "Effect": "+{% Sneaking EXP", "BaseValue": 2},
    60:{"Name": "Misterloin Steak", "Description": "Make sure to paint on the grill marks to really give it that extra taste!", "Effect": "+{% Jade gain from Sneaking", "BaseValue": 6},
    61:{"Name": "Large Pohayoh", "Description": "Aye lad if thah ain't tha larjes' fookin' poh'ay'oh eyev evah seen wih me own eyes!", "Effect": "+{% Summoning EXP", "BaseValue": 2},
    62:{"Name": "Bill Jack Pepper", "Description": "It's Him.", "Effect": "+{% Crop Evolution Chance", "BaseValue": 5},
    63:{"Name": "Burned Marshmallow", "Description": "IMPORTANT, this bonus DOUBLES at Farming Lv 50. Triples at Farming Lv 100, and so on!", "Effect": "+{% Meal Cooking Speed", "BaseValue": 40},
    64:{"Name": "Yumi Peachring", "Description": "Don't disrespect the ring. All hail the ring.", "Effect": "+{% All Golden Food bonus", "BaseValue": 2},
    65:{"Name": "Plumpcakes", "Description": "Ohhh, they're called 'plump'cakes because they're dummy thicc can I get an amen!", "Effect": "+{% Total Damage", "BaseValue": 6},
    66:{"Name": "Nyanborgir", "Description": "It's the greatest meal ever! Bonus DOUBLES at Summoning Lv 50, Triples at 100, etc", "Effect": "+{% Crop Evolution Chance", "BaseValue": 9},
}

labChipsDict = {
    0: {"Name": "Grounded Nanochip", "Description": "+{% Total Defence", "Effect": "Boosts total defence", "Material": "Copper", "MaterialCost": 20000, "Meal": "Meal0", "MealCost": 100, "Spice": "Spice0", "SpiceCost": 100, "Value10": 0, "EffectID": "def", "BaseValue": 10},
    1: {"Name": "Grounded Motherboard", "Description": "+{% Move Speed if total is less than 170%", "Effect": "Boosts total movement speed", "Material": "OakTree", "MaterialCost": 30000, "Meal": "Meal1", "MealCost": 100, "Spice": "Spice0", "SpiceCost": 100, "Value10": 0, "EffectID": "move", "BaseValue": 30},
    2: {"Name": "Grounded Software", "Description": "+{% Total Accuracy", "Effect": "Boosts total accuracy", "Material": "Fish1", "MaterialCost": 20000, "Meal": "Meal3", "MealCost": 100, "Spice": "Spice1", "SpiceCost": 100, "Value10": 0, "EffectID": "acc", "BaseValue": 10},
    3: {"Name": "Grounded Processor", "Description": "+{% Drop Rate if total is less than 5.00x", "Effect": "Boosts total drop rate", "Material": "DesertA1", "MaterialCost": 10000, "Meal": "Meal4", "MealCost": 100, "Spice": "Spice1", "SpiceCost": 100, "Value10": 0, "EffectID": "dr", "BaseValue": 60},
    4: {"Name": "Potato Chip", "Description": "+{% Basic Attack spd. *Can Only Equip 1 per player*", "Effect": "Boosts attack speed", "Material": "Bug1", "MaterialCost": 20000, "Meal": "Meal6", "MealCost": 100, "Spice": "Spice2", "SpiceCost": 100, "Value10": 1, "EffectID": "atkspd", "BaseValue": 20},
    5: {"Name": "Conductive Nanochip", "Description": "+{% Lab EXP Gain", "Effect": "Boosts lab exp gain", "Material": "StumpTree", "MaterialCost": 100000, "Meal": "Meal9", "MealCost": 100, "Spice": "Spice3", "SpiceCost": 100, "Value10": 0, "EffectID": "labexp", "BaseValue": 30},
    6: {"Name": "Conductive Motherboard", "Description": "+{% Line Width within Mainframe", "Effect": "Boosts mainframe line width", "Material": "Gold", "MaterialCost": 100000, "Meal": "Meal12", "MealCost": 100, "Spice": "Spice4", "SpiceCost": 100, "Value10": 0, "EffectID": "linewidth", "BaseValue": 12},
    7: {"Name": "Conductive Software", "Description": "+{% Fighting AFK Gain Rate *Can Only Equip 1 per player*", "Effect": "Boosts Fighting AFK gain rate", "Material": "Critter2", "MaterialCost": 10000, "Meal": "Meal15", "MealCost": 100, "Spice": "Spice4", "SpiceCost": 100, "Value10": 1, "EffectID": "fafk", "BaseValue": 15},
    8: {"Name": "Conductive Processor", "Description": "+{% Skilling AFK Gain Rate *Can Only Equip 1 per player*", "Effect": "Boosts Skilling AFK gain Rate", "Material": "Bug5", "MaterialCost": 100000, "Meal": "Meal18", "MealCost": 100, "Spice": "Spice5", "SpiceCost": 100, "Value10": 1, "EffectID": "safk", "BaseValue": 15},
    9: {"Name": "Chocolatey Chip", "Description": "{% chance to spawn a crystal mob when one dies. *Can Only Equip 1 per player*", "Effect": "Chance for Crystal Mob revival", "Material": "CraftMat8", "MaterialCost": 200000, "Meal": "Meal21", "MealCost": 100, "Spice": "Spice6", "SpiceCost": 100, "Value10": 1, "EffectID": "crys", "BaseValue": 75},
    10: {"Name": "Galvanic Nanochip", "Description": "+{% Monster Respawn Rate", "Effect": "Boosts Mob respawn rate", "Material": "SnowC1", "MaterialCost": 100000, "Meal": "Meal24", "MealCost": 100, "Spice": "Spice7", "SpiceCost": 100, "Value10": 0, "EffectID": "resp", "BaseValue": 10},
    11: {"Name": "Galvanic Motherboard", "Description": "+{% Total Skilling Efficiency for all skills", "Effect": "Boosts skilling efficiency", "Material": "Fish5", "MaterialCost": 250000, "Meal": "Meal27", "MealCost": 100, "Spice": "Spice8", "SpiceCost": 100, "Value10": 0, "EffectID": "toteff", "BaseValue": 20},
    12: {"Name": "Galvanic Software", "Description": "+{% Total Damage", "Effect": "Boosts total damage", "Material": "Dementia", "MaterialCost": 300000, "Meal": "Meal29", "MealCost": 100, "Spice": "Spice9", "SpiceCost": 100, "Value10": 0, "EffectID": "dmg", "BaseValue": 10},
    13: {"Name": "Galvanic Processor", "Description": "+{ Base Efficiency for all skills", "Effect": "Boosts base skilling efficiency", "Material": "GalaxyB2", "MaterialCost": 100000, "Meal": "Meal31", "MealCost": 100, "Spice": "Spice10", "SpiceCost": 100, "Value10": 0, "EffectID": "eff", "BaseValue": 250},
    14: {"Name": "Wood Chip", "Description": "+{% Multikill per Damage Tier for all worlds", "Effect": "Boosts multikill", "Material": "Tree8", "MaterialCost": 250000, "Meal": "Meal33", "MealCost": 100, "Spice": "Spice11", "SpiceCost": 100, "Value10": 0, "EffectID": "mkill", "BaseValue": 15},
    15: {"Name": "Silkrode Nanochip", "Description": "Doubles the bonuses of all active Star Signs. *Can Only Equip 1 per player*", "Effect": "Bolsters active star signs", "Material": "CraftMat10", "MaterialCost": 2000000, "Meal": "Meal35", "MealCost": 100, "Spice": "Spice12", "SpiceCost": 100, "Value10": 1, "EffectID": "star", "BaseValue": 1},
    16: {"Name": "Silkrode Motherboard", "Description": "Doubles MISC bonuses of currently equipped Trophy. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped trophy", "Material": "Soul5", "MaterialCost": 2000000, "Meal": "Meal37", "MealCost": 100, "Spice": "Spice13", "SpiceCost": 100, "Value10": 1, "EffectID": "troph", "BaseValue": 1},
    17: {"Name": "Silkrode Software", "Description": "Doubles MISC bonuses of keychain equipped in the upper keychain slot. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped keychain", "Material": "Bug8", "MaterialCost": 2000000, "Meal": "Meal39", "MealCost": 100, "Spice": "Spice13", "SpiceCost": 100, "Value10": 1, "EffectID": "key1", "BaseValue": 1},
    18: {"Name": "Silkrode Processor", "Description": "Doubles MISC bonuses of currently equipped Pendant. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped pendant", "Material": "Critter10", "MaterialCost": 2000000, "Meal": "Meal41", "MealCost": 100, "Spice": "Spice14", "SpiceCost": 100, "Value10": 1, "EffectID": "pend", "BaseValue": 1},
    19: {"Name": "Poker Chip", "Description": "Your weapon gives 1.{x more Weapon Power. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped Weapon", "Material": "CraftMat14", "MaterialCost": 2000000, "Meal": "Meal43", "MealCost": 100, "Spice": "Spice14", "SpiceCost": 100, "Value10": 1, "EffectID": "weppow", "BaseValue": 25},
    20: {"Name": "Omega Nanochip", "Description": "Doubles bonus of card equipped in top left slot. *Can Only Equip 1 per player*", "Effect": "Bolsters an equipped card", "Material": "Bug8", "MaterialCost": 10000000, "Meal": "Meal45", "MealCost": 100, "Spice": "Spice15", "SpiceCost": 100, "Value10": 1, "EffectID": "card1", "BaseValue": 1},
    21: {"Name": "Omega Motherboard", "Description": "Doubles bonus of card equipped in bottom right slot. *Can Only Equip 1 per player*", "Effect": "Bolsters an equipped card", "Material": "Fish8", "MaterialCost": 10000000, "Meal": "Meal47", "MealCost": 100, "Spice": "Spice16", "SpiceCost": 100, "Value10": 1, "EffectID": "card2", "BaseValue": 1},
}

# I don't know what values 4 and 5 do. Added in case they turn out to be useful 
labBonusesDict = {
    0: {"Name": "Animal Farm", "Description": "+1% Total Damage for every different species you have bred within Pet Breeding. You just need to breed the pet type one time for it to count! @ - @ Total Bonus: {%", "BaseValue": 1, "Coordinates": [91, 90], "Value4": 90, "Value5": 0},
    1: {"Name": "Wired In", "Description": "All Uploaded Players print 2x more resources from their section of the 3D Printer. The displayed amount will NOT appear doubled, just to avoid confusion as to what your actual base Sampling Rate is, but it will be displayed in blue.", "BaseValue": 2, "Coordinates": [250, 90], "Value4": 90, "Value5": 1},
    2: {"Name": "Gilded Cyclical Tubing", "Description": "All refinery cycles occur 3x faster. Faster cycles means more salts!", "BaseValue": 3, "Coordinates": [356, 90], "Value4": 90, "Value5": 1},
    3: {"Name": "No Bubble Left Behind", "Description": "Every 24 hours, your 3 lowest level Alchemy Bubbles gets +1 Lv. This only applies to bubbles Lv 5 or higher, so it's more like 'your lowest level bubble that is at least level 5'. ALSO, it only works on the first 15 bubbles of each colour! @ Doesn't trigger on days that you don't login.", "BaseValue": 1, "Coordinates": [450, 90], "Value4": 90, "Value5": 0},
    4: {"Name": "Killer's Brightside", "Description": "All monster kills count for 2x more than normal for things like opening portals and Death Note. Doesn't increase resource drops or exp gain.", "BaseValue": 2, "Coordinates": [538, 90], "Value4": 90, "Value5": 1},
    5: {"Name": "Shrine World Tour", "Description": "If a shrine is placed within town, instead of in a monster map, it will act as though it is placed in EVERY map in that entire world!", "BaseValue": 1, "Coordinates": [651, 90], "Value4": 90, "Value5": 0},
    6: {"Name": "Viaduct of the Gods", "Description": "All alchemy liquids have x5 higher max capacity. However, you regenerate alchemy liquids -30% slower.", "BaseValue": 5, "Coordinates": [753, 90], "Value4": 90, "Value5": 1},
    7: {"Name": "Certified Stamp Book", "Description": "All Stamps, except for MISC tab stamps, give DOUBLE the bonus.", "BaseValue": 2, "Coordinates": [824, 90], "Value4": 90, "Value5": 1},
    8: {"Name": "Spelunker Obol", "Description": "1.50x higher effects from all active Jewels within the Mainframe, and gives you +50% rememberance of the game Idle Skilling. @ This bonus always has a 80px connection range no matter what!", "BaseValue": 1.5, "Coordinates": [945, 90], "Value4": 90, "Value5": 1},
    9: {"Name": "Fungi Finger Pocketer", "Description": "+2% extra cash from monsters for every 1 million Green Mushroom kills your account has, which can be viewed at Death Note. @ - @ Total Bonus: {%", "BaseValue": 2, "Coordinates": [990, 90], "Value4": 90, "Value5": 0},
    10: {"Name": "My 1st Chemistry Set", "Description": "All Vials in Alchemy give DOUBLE the bonus. The bonus description will reflect this doubling.", "BaseValue": 2, "Coordinates": [1177, 90], "Value4": 90, "Value5": 1},
    11: {"Name": "Unadulterated Banking Fury", "Description": "+2% Total Damage for each 'green stack' of resources in your bank. A 'green stack' is a stack in your Storage Chest with 10 million or more items, since the number turns Green after 10M! @ - @ Total Bonus: {%", "BaseValue": 2, "Coordinates": [1300, 90], "Value4": 90, "Value5": 0},
    12: {"Name": "Sigils of Olden Alchemy", "Description": "Allows you to level up Alchemy Sigils by assigning players in alchemy, at a base rate of 1 sigil xp per hour. @ Sigils can be leveled up just twice: Once to unlock their bonus, and once more to boost their bonus. Their bonuses are passive, and apply to all characters always.", "BaseValue": 1, "Coordinates": [400, 90], "Value4": 90, "Value5": 0},
    13: {"Name": "Viral Connection", "Description": "All mainframe bonuses and jewels have a 50% larger connection range, unless it states otherwise. @ This bonus always has a 80px connection range no matter what!", "BaseValue": 50, "Coordinates": [1430, 90], "Value4": 90, "Value5": 0},
    14: {"Name": "Artifact Attraction", "Description": "Artifact find chance is 1.5x higher! If you've found all artifacts at max rarity, then this bonus changes to 1,000x artifact find chance!", "BaseValue": 50, "Coordinates": [1530, 90], "Value4": 90, "Value5": 0},
    15: {"Name": "Slab Sovereignty", "Description": "All bonuses given by the Slab are 1.25x higher!", "BaseValue": 25, "Coordinates": [1630, 90], "Value4": 90, "Value5": 0},
    16: {"Name": "Spiritual Growth", "Description": "Boosts EXP multi for all three World 6 skills by +50%!", "BaseValue": 50, "Coordinates": [1790, 90], "Value4": 90, "Value5": 0},
    17: {"Name": "Depot Studies PhD", "Description": "All bonuses given at the Crop Depot are 1.30x higher!", "BaseValue": 30, "Coordinates": [1950, 90], "Value4": 90, "Value5": 0},
}
nblbMaxBubbleCount = 10

labJewelsDict = {
    0: {'Name': "Amethyst Rhinestone", "Description": "Meal cooking is }x faster. This bonus is applied TWICE if all 3 purple jewels are active.", "BaseValue": 1.5}, 
    1: {'Name': "Purple Navette", "Description": "Animal Farm' mainframe bonus gives an additional +}% per species. If Animal Farm is not active, then this does nothing.", "BaseValue": 0.5}, 
    2: {'Name': "Purple Rhombol", "Description": "All players get +}% Lab EXP gain.", "BaseValue": 40}, 
    3: {'Name': "Sapphire Rhinestone", "Description": "Construction slot 1 is now trimmed up, and has }x building Speed. Also trims slot 2 if all 4 blue jewels are active.", "BaseValue": 3}, 
    4: {'Name': "Sapphire Navette", "Description": "All players get +}% All Stat. STR, AGI, WIS, and LUCK to boot.", "BaseValue": 3}, 
    5: {'Name': "Sapphire Rhombol", "Description": "Even if this jewel is off, all players within a 150px radius of this jewel, shown by the circle, have +25% Line Width. @ Also gives +}% Breeding EXP, but only when active.", "BaseValue": 25}, 
    6: {'Name': "Sapphire Pyramite", "Description": "Every 24 hours, the } lowest level Kitchen Upgrades across all owned kitchens gain +1 Lv.", "BaseValue": 2}, 
    7: {'Name': "Pyrite Rhinestone", "Description": "No Bubble Left Behind' mainframe bonus gives +} levels instead of +1, and does so for the lowest 4 bubbles instead of 3.", "BaseValue": 2}, 
    8: {'Name': "Pyrite Navette", "Description": "All players get }x 'non-consume' chance, and raises the max chance from 90% to 98%, allowing for longer AFK with food.", "BaseValue": 3}, 
    9: {'Name': "Pyrite Rhombol", "Description": "All mainframe bonuses and jewels have a }% larger connection range, except for this jewel. This jewel has an 80px connection range no matter what!", "BaseValue": 30}, 
    10:{'Name': "Pyrite Pyramite", "Description": "All players deal 1.}x more damage. This bonus is applied TWICE if all 4 Orange Jewels are active.", "BaseValue":10}, 
    11:{'Name': "Emerald Rhinestone", "Description": "}% reduced incubation egg time. Mo eggs mo problems tho, fo sho.", "BaseValue":28}, 
    12:{'Name': "Emerald Navette", "Description": "All players have } higher base efficiency in all skills, and +10% skill action speed. This bonus is applied TWICE if all 5 Green Jewels are active.", "BaseValue":200}, 
    13:{'Name': "Emerald Rhombol", "Description": "Fungi Finger Pocketer' mainframe bonus gives an additional +}% cash bonus per million mushroom kills", "BaseValue":1}, 
    14:{'Name': "Emerald Pyramite", "Description": "Meal cooking is }% faster for every 25 total upgrade levels across all kitchens.", "BaseValue":1},
    15:{'Name': "Emerald Ulthurite", "Description": "Special Pets in the Fenceyard level up their Passive Bonuses +}% faster", "BaseValue":30}, 
    16:{'Name': "Black Diamond Rhinestone", "Description": "All meal bonuses, as shown in the Dinner Table Menu, actually give 1.}x higher bonus than what is shown.", "BaseValue":16}, 
    17:{'Name': "Black Diamond Ulthurite", "Description": "Unadulterated Banking Fury' gives an additional +}% Total Damage per greened stack. Bolsters 'Unadulterated Banking Fury'", "BaseValue":1}, 
    18:{'Name': "Pure Opal Rhinestone", "Description": "Slab Sovereignty' gives an additional }% boost to all Slab Bonuses!", "BaseValue":20}, 
    19:{'Name': "Pure Opal Navette", "Description": "+}% higher effects from all active bonuses and jewels within the Mainframe, except for Spelunker Obol. @ This is a multiplier, so +10% would be 1.10x, ya feel me? @ This bonus always has a 80px connection range no matter what!", "BaseValue":10}, 
    20:{'Name': "Pure Opal Rhombol", "Description": "Depot Studies PhD' gives an additional }% boost to all Crop Depot bonuses!", "BaseValue": 10},
}

labBonusesList = [
    "Animal Farm", "Wired In", "Gilded Cyclical Tubing", "No Bubble Left Behind", "Killer's Brightside",
    "Shrine World Tour", "Viaduct of the Gods", "Certified Stamp Book", "Spelunker Obol", "Fungi Finger Pocketer",
    "My 1st Chemistry Set", "Unadulterated Banking Fury", "Sigils of Olden Alchemy", "Viral Connection",
    "Artifact Attraction", "Slab Sovereignty", "Spiritual Growth", "Depot Studies PhD"
]

maxNumberOfTerritories = 24  # as of w6 launch
indexFirstTerritoryAssignedPet = 28
slotUnlockWavesList = [2, 15, 50, 125]
territoryNames = [
    "", "Grasslands", "Jungle", "Encroaching Forest", "Tree Interior", "Stinky Sewers",
    "Desert Oasis", "Beach Docks", "Coarse Mountains", "Twilight Desert", "The Crypt",
    "Frosty Peaks", "Tundra Outback", "Crystal Caverns", "Pristalle Lake",
    "Nebulon Mantle", "Starfield Skies", "Shores of Eternity",
    "Molten Bay", "Smokey Lake", "Wurm Catacombs",
    "Spirit Fields", "Bamboo Forest", "Lullaby Airways", "Dharma Mesa"
]
breedingUpgradesDict: dict[int, dict[str, str | int]] = {
    0: {
        'Name': 'No Upgrade Selected',
        'BonusText': "TAP AN UPGRADE ABOVE! Also, as a reward for reading this, I'll let you know that upgrading this 'nothing' bonus actually boosts breeding exp gain!!",
        'BonusValue': 2,
        'MaxLevel': 100,
        'MaxValue': 200,
        'UnlockLevel': 1,
    },
    1: {
        'Name': 'Genetic Splicing',
        'BonusText': "Unlocks the 1st Breeding Multiplier, Gene Boosting. Genes are found while fighting with the DNA Splicer tool purchased at the Town Shop.",
        'BonusValue': 4,
        'MaxLevel': 20,
        'MaxValue': 80,
        'UnlockLevel': 1,
    },
    2: {
        'Name': 'Egg Capacity',
        'BonusText': "Increases the maximum number of eggs your incubator can hold. The more eggs you currently hold, the rarer it is to get a new one.",
        'BonusValue': 1,
        'MaxLevel': 5,
        'MaxValue': 5,
        'UnlockLevel': 5,
    },
    3: {
        'Name': 'Breedability Pulse',
        'BonusText': "Unlocks the 2nd Breeding Multiplier, Breedability. Pets placed in the Fenceyard with the Breedable Gene increase this multi over time.",
        'BonusValue': 25,
        'MaxLevel': 10,
        'MaxValue': 250,
        'UnlockLevel': 10,
    },
    4: {
        'Name': 'Fence Extension',
        'BonusText': "Increases the number of slots in your Fence Yard, allowing for more pets to roam around, free range style!",
        'BonusValue': 1,
        'MaxLevel': 10,
        'MaxValue': 10,
        'UnlockLevel': 15,
    },
    5: {
        'Name': 'Rarity of the Egg',
        'BonusText': "Unlocks the 3rd Breeding Multi, Rarity. When the egg incubator is full, theres a chance to increase the rarity of another egg!",
        'BonusValue': 0,
        'MaxLevel': 10,
        'MaxValue': 3.5,
        'UnlockLevel': 20,
    },
    6: {
        'Name': 'Blooming Axe',
        'BonusText': "Forage pets contribute a fraction of their forage speed toward Fight Power. Now you no longer need at least 1 fighting pet!",
        'BonusValue': 6,
        'MaxLevel': 10,
        'MaxValue': 60,
        'UnlockLevel': 25,
    },
    7: {
        'Name': 'Pastpresent Brood',
        'BonusText': "Unlocks the 4th Breeding Multiplier, Pastpres. This increases based on the number of different pets discovered from the previous world.",
        'BonusValue': 0.15,
        'MaxLevel': 5,
        'MaxValue': 1.75,
        'UnlockLevel': 30,
    },
    8: {
        'Name': 'Paint Bucket',
        'BonusText': "Unlocks Shiny Pet Breeding. Shiny Pets come in 1 of 5 colours, and boost their Special Passive bonus when in the Fenceyard.",
        'BonusValue': 2,
        'MaxLevel': 100,
        'MaxValue': 201,
        'UnlockLevel': 40,
    },
    9: {
        'Name': 'Overwhelmed Golden Egg',
        'BonusText': "Your New Pet Chance is multiplied for every 100 kitchen upgrade levels across all kitchens! So 200 Lvs would apply it twice!!",
        'BonusValue': 0.02,
        'MaxLevel': 20,
        'MaxValue': 1.4,
        'UnlockLevel': 50,
    },
    10: {
        'Name': 'Failsafe Restitution Cloud',
        'BonusText': "Unlocks the 5th Breeding Multiplier, Failure. This increases every time you fail to get a pet, up to a max, and depletes when you succeed.",
        'BonusValue': 10,
        'MaxLevel': 25,
        'MaxValue': 250,
        'UnlockLevel': 60,
    },
    11: {
        'Name': 'Shattershell Iteration',
        'BonusText': "Every time you use up your last incubator egg, there is a chance to produce 2 more eggs immediately.",
        'BonusValue': 6,
        'MaxLevel': 10,
        'MaxValue': 60,
        'UnlockLevel': 70,
    },

}
breedingGeneticsList: list[str] = [
    "Fighter", "Defender", "Forager", "Fleeter", "Breeder", "Special", "Mercenary", "Boomer",
    "Sniper", "Amplifier", "Tsar", "Rattler", "Cursory", "Fastidious", "Flashy", "Opticular",
    "Monolithic", "Alchemic", "Badumdum", "Defstone", "Targeter", "Looter", "Refiller", "Eggshell",
    "Lazarus", "Trasher", "Miasma", "Converter", "Heavyweight", "Fastihoop", "Ninja",
    "Superboomer", "Peapeapod", "Borger"
]
breedingShinyBonusList: list[str] = [
    "Faster Shiny Pet Lv Up Rate",  #0
    "Infinite Star Signs",
    "Total Damage",  #2
    "Drop Rate",
    "Base Efficiency for All Skills",  #4
    "Base WIS",
    "Base STR",  #6
    "Base AGI",
    "Base LUK",  #8
    "Class EXP",
    "Skill EXP",  #10
    "Tab 1 Talent Pts",
    "Tab 2 Talent Pts",  #12
    "Tab 3 Talent Pts",
    "Tab 4 Talent Pts",  #14
    "Star Talent Pts",
    "Faster Refinery Speed",  #16
    "Base Critter Per Trap",
    "Multikill Per Tier",  #18
    "Bonuses from All Meals",
    "Line Width in Lab",  #20
    "Higher Artifact Find Chance",
    "Sail Captain EXP Gain",  #22
    "Lower Minimum Travel Time for Sailing",
    "Farming EXP",  #24
    "Summoning EXP"
]
breedingSpeciesDict: dict[int, dict] = {
    #Built using references to Genetics and ShinyBonus lists because I kept making typos + Wiki isn't consistent to copy/paste from
    1: {
        0: {
            'Name': 'Green Mushroom',
            'Genetic': breedingGeneticsList[0],  #Fighter
            'ShinyBonus': breedingShinyBonusList[0],  #Faster Shiny Pet Lv Up Rate,
        },
        1: {
            'Name': 'Squirrel',
            'Genetic': breedingGeneticsList[2],  #Forager
            'ShinyBonus': breedingShinyBonusList[1],  #Infinite Star Signs
        },
        2: {
            'Name': 'Frog',
            'Genetic': breedingGeneticsList[7],  #Boomer
            'ShinyBonus': breedingShinyBonusList[2],  #Total Damage
        },
        3: {
            'Name': 'Bored Bean',
            'Genetic': breedingGeneticsList[3],  #Fleeter
            'ShinyBonus': breedingShinyBonusList[16],  #Faster Refinery Speed
        },
        4: {
            'Name': 'Red Mushroom',
            'Genetic': breedingGeneticsList[0],  #Fighter
            'ShinyBonus': breedingShinyBonusList[19],  #Bonuses from All Meals
        },
        5: {
            'Name': 'Slime',
            'Genetic': breedingGeneticsList[12],  #Cursory
            'ShinyBonus': breedingShinyBonusList[3],  #Drop Rate
        },
        6: {
            'Name': 'Piggo',
            'Genetic': breedingGeneticsList[9],  #Amplifier
            'ShinyBonus': breedingShinyBonusList[1],  #Infinite Star Signs
        },
        7: {
            'Name': 'Baby Boa',
            'Genetic': breedingGeneticsList[20],  #Targeter
            'ShinyBonus': breedingShinyBonusList[18],  #Multikill Per Tier
        },
        8: {
            'Name': 'Carrotman',
            'Genetic': breedingGeneticsList[6],  #Mercenary
            'ShinyBonus': breedingShinyBonusList[4],  #Base Efficiency for All Skills
        },
        9: {
            'Name': 'Glublin',
            'Genetic': breedingGeneticsList[22],  #Refiller
            'ShinyBonus': breedingShinyBonusList[1],  #Infinite Star Signs
        },
        10: {
            'Name': 'Wode Board',
            'Genetic': breedingGeneticsList[26],  #Miasma
            'ShinyBonus': breedingShinyBonusList[0],  #Faster Shiny Pet Lv Up Rate
        },
        11: {
            'Name': 'Gigafrog',
            'Genetic': breedingGeneticsList[9],  #Amplifier
            'ShinyBonus': breedingShinyBonusList[4],  #Base Efficiency for All Skills
        },
        12: {
            'Name': 'Wild Boar',
            'Genetic': breedingGeneticsList[28],  #Heavyweight
            'ShinyBonus': breedingShinyBonusList[7],  #Base AGI
        },
        13: {
            'Name': 'Walking Stick',
            'Genetic': breedingGeneticsList[22],  #Refiller
            'ShinyBonus': breedingShinyBonusList[17],  #Base Critter Per Trap
        },
        14: {
            'Name': 'Nutto',
            'Genetic': breedingGeneticsList[33],  #Borger
            'ShinyBonus': breedingShinyBonusList[2],  #Total Damage
        },
        15: {
            'Name': 'Poop',
            'Genetic': breedingGeneticsList[10],  #Tsar
            'ShinyBonus': breedingShinyBonusList[24],  #Farming EXP
        },
        16: {
            'Name': 'Rat',
            'Genetic': breedingGeneticsList[16],  #Monolithic
            'ShinyBonus': breedingShinyBonusList[18],  #Multikill Per Tier
        },
    },
    2: {
        0: {
            'Name': 'Sandy Pot',
            'Genetic': breedingGeneticsList[21],  #Looter
            'ShinyBonus': breedingShinyBonusList[9],  #Class EXP
        },
        1: {
            'Name': 'Mimic',
            'Genetic': breedingGeneticsList[1],  #Defender
            'ShinyBonus': breedingShinyBonusList[11],  #Tab 1 Talent Pts
        },
        2: {
            'Name': 'Crabcake',
            'Genetic': breedingGeneticsList[3],  #Fleeter
            'ShinyBonus': breedingShinyBonusList[10],  #Skill EXP
        },
        3: {
            'Name': 'Mafioso',
            'Genetic': breedingGeneticsList[2],  #Forager
            'ShinyBonus': breedingShinyBonusList[12],  #Tab 2 Talent Pts
        },
        4: {
            'Name': 'Mallay',
            'Genetic': breedingGeneticsList[15],  #Opticular
            'ShinyBonus': breedingShinyBonusList[20],  #Line Width in Lab
        },
        5: {
            'Name': 'Sand Castle',
            'Genetic': breedingGeneticsList[19],  #Defstone
            'ShinyBonus': breedingShinyBonusList[6],  #Base STR
        },
        6: {
            'Name': 'Pincermin',
            'Genetic': breedingGeneticsList[0],  #Fighter
            'ShinyBonus': breedingShinyBonusList[2],  #Total Damage
        },
        7: {
            'Name': 'Mashed Potato',
            'Genetic': breedingGeneticsList[9],  #Amplifier
            'ShinyBonus': breedingShinyBonusList[4],  #Base Efficiency for All Skills
        },
        8: {
            'Name': 'Tyson',
            'Genetic': breedingGeneticsList[13],  #Fastidious
            'ShinyBonus': breedingShinyBonusList[21],  #Higher Artifact Find Chance
        },
        9: {
            'Name': 'Whale',
            'Genetic': breedingGeneticsList[18],  #Badumdum
            'ShinyBonus': breedingShinyBonusList[16],  #Faster Refinery Speed
        },
        10: {
            'Name': 'Moonmoon',
            'Genetic': breedingGeneticsList[7],  #Mercenary
            'ShinyBonus': breedingShinyBonusList[5],  #Base WIS
        },
        11: {
            'Name': 'Sand Giant',
            'Genetic': breedingGeneticsList[11],  #Rattler
            'ShinyBonus': breedingShinyBonusList[4],  #Base Efficiency for All Skills
        },
        12: {
            'Name': 'Snelbie',
            'Genetic': breedingGeneticsList[16],  #Monolithic
            'ShinyBonus': breedingShinyBonusList[14],  #Tab 4 Talent Pts
        },
        13: {
            'Name': 'Dig Doug',
            'Genetic': breedingGeneticsList[24],  #Lazarus
            'ShinyBonus': breedingShinyBonusList[24],  #Farming EXP
        },
        14: {
            'Name': 'Beefie',
            'Genetic': breedingGeneticsList[25],  #Trasher
            'ShinyBonus': breedingShinyBonusList[8],  #Base LUK
        },
        15: {
            'Name': 'Crescent Spud',
            'Genetic': breedingGeneticsList[16],  #Monolithic
            'ShinyBonus': breedingShinyBonusList[0],  #Faster Shiny Pet Lv Up Rate
        },
        16: {
            'Name': 'Chippy',
            'Genetic': breedingGeneticsList[23],  #Eggshell
            'ShinyBonus': breedingShinyBonusList[25],  #Summoning EXP
        },
    },
    3: {
		0: {
            'Name': 'Sheepie',
            'Genetic': breedingGeneticsList[8],  #Sniper
            'ShinyBonus': breedingShinyBonusList[19],  #Bonuses from All Meals
        },
		1: {
            'Name': 'Frost Flake',
            'Genetic': breedingGeneticsList[30],  #Ninja
            'ShinyBonus': breedingShinyBonusList[13],  #Tab 3 Talent Pts
        },
		2: {
            'Name': 'Sir Stache',
            'Genetic': breedingGeneticsList[23],  #Eggshell
            'ShinyBonus': breedingShinyBonusList[1],  #Infinite Star Signs
        },
		3: {
            'Name': 'Xylobone',
            'Genetic': breedingGeneticsList[15],  #Opticular
            'ShinyBonus': breedingShinyBonusList[3],  #Drop Rate
        },
		4: {
            'Name': 'Bunny',
            'Genetic': breedingGeneticsList[14],  #Flashy
            'ShinyBonus': breedingShinyBonusList[8],  #Base LUK
        },
		5: {
            'Name': 'Bloque',
            'Genetic': breedingGeneticsList[17],  #Alchemic
            'ShinyBonus': breedingShinyBonusList[18],  #Multikill Per Tier
        },
		6: {
            'Name': 'Mamooth',
            'Genetic': breedingGeneticsList[21],  #Looter
            'ShinyBonus': breedingShinyBonusList[21],  #Higher Artifact Find Chance
        },
		7: {
            'Name': 'Snowman',
            'Genetic': breedingGeneticsList[19],  #Defstone
            'ShinyBonus': breedingShinyBonusList[9],  #Class EXP
        },
		8: {
            'Name': 'Penguin',
            'Genetic': breedingGeneticsList[13],  #Fastidious
            'ShinyBonus': breedingShinyBonusList[1],  #Infinite Star Signs
        },
		9: {
            'Name': 'Thermister',
            'Genetic': breedingGeneticsList[8],  #Sniper
            'ShinyBonus': breedingShinyBonusList[10],  #Skill EXP
        },
		10: {
            'Name': 'Quenchie',
            'Genetic': breedingGeneticsList[7],  #Boomer
            'ShinyBonus': breedingShinyBonusList[0],  #Faster Shiny Pet Lv Up Rate
        },
		11: {
            'Name': 'Cryosnake',
            'Genetic': breedingGeneticsList[23],  #Eggshell
            'ShinyBonus': breedingShinyBonusList[15],  #Star Talent Pts
        },
		12: {
            'Name': 'Mecho Mouse',
            'Genetic': breedingGeneticsList[25],  #Trasher
            'ShinyBonus': breedingShinyBonusList[6],  #Base STR
        },
		13: {
            'Name': 'Bop Box',
            'Genetic': breedingGeneticsList[27],  #Converter
            'ShinyBonus': breedingShinyBonusList[1],  #Infinite Star Signs
        },
		14: {
            'Name': 'Neyeptune',
            'Genetic': breedingGeneticsList[24],  #Lazarus
            'ShinyBonus': breedingShinyBonusList[24],  #Farming EXP
        },
		15: {
            'Name': 'Dedotated Ram',
            'Genetic': breedingGeneticsList[9],  #Amplifier
            'ShinyBonus': breedingShinyBonusList[18],  #Multikill Per Tier
        },
		16: {
            'Name': 'Bloodbone',
            'Genetic': breedingGeneticsList[20],  #Targeter
            'ShinyBonus': breedingShinyBonusList[24],  #Farming EXP
        },
        17: {
            'Name': 'Panda',
            'Genetic': breedingGeneticsList[27],  #Converter
            'ShinyBonus': breedingShinyBonusList[2],  #Total Damage
        },
    },
    4: {
        0: {
            'Name': 'Purp Mushroom',
            'Genetic': breedingGeneticsList[10],  #Tsar
            'ShinyBonus': breedingShinyBonusList[24],  #Farming EXP
        },
        1: {
            'Name': 'TV',
            'Genetic': breedingGeneticsList[11],  #Rattler
            'ShinyBonus': breedingShinyBonusList[22],  #Sail Captain EXP Gain
        },
        2: {
            'Name': 'Donut',
            'Genetic': breedingGeneticsList[14],  #Flashy
            'ShinyBonus': breedingShinyBonusList[25],  #Summoning EXP
        },
        3: {
            'Name': 'Demon Genie',
            'Genetic': breedingGeneticsList[31],  #Superboomer
            'ShinyBonus': breedingShinyBonusList[16],  #Faster Refinery Speed
        },
        4: {
            'Name': 'Flying Worm',
            'Genetic': breedingGeneticsList[33],  #Borger
            'ShinyBonus': breedingShinyBonusList[7],  #Base AGI
        },
        5: {
            'Name': 'Dog',
            'Genetic': breedingGeneticsList[32],  #Peapeapod
            'ShinyBonus': breedingShinyBonusList[23],  #Lower Minimum Travel Time for Sailing
        },
        6: {
            'Name': 'Soda Can',
            'Genetic': breedingGeneticsList[29],  #Fastihoop
            'ShinyBonus': breedingShinyBonusList[21],  #Higher Artifact Find Chance
        },
        7: {
            'Name': 'Gelatinous Cuboid',
            'Genetic': breedingGeneticsList[14],  #Flashy
            'ShinyBonus': breedingShinyBonusList[2],  #Total Damage
        },
        8: {
            'Name': 'Choccie',
            'Genetic': breedingGeneticsList[31],  #Superboomer
            'ShinyBonus': breedingShinyBonusList[3],  #Drop Rate
        },
        9: {
            'Name': 'Biggole Wurm',
            'Genetic': breedingGeneticsList[10],  #Tsar
            'ShinyBonus': breedingShinyBonusList[9],  #Class EXP
        },
        10: {
            'Name': 'Cool Bird',
            'Genetic': breedingGeneticsList[33],  #Borger
            'ShinyBonus': breedingShinyBonusList[6],  #Base STR
        },
        11: {
            'Name': 'Clammie',
            'Genetic': breedingGeneticsList[6],  #Mercenary
            'ShinyBonus': breedingShinyBonusList[10],  #Skill EXP
        },
        12: {
            'Name': 'Octodar',
            'Genetic': breedingGeneticsList[12],  #Cursory
            'ShinyBonus': breedingShinyBonusList[17],  #Base Critter Per Trap
        },
        13: {
            'Name': 'Flombeige',
            'Genetic': breedingGeneticsList[25],  #Trasher
            'ShinyBonus': breedingShinyBonusList[7],  #Base AGI
        },
        14: {
            'Name': 'Stilted Seeker',
            'Genetic': breedingGeneticsList[33],  #Borger
            'ShinyBonus': breedingShinyBonusList[5],  #Base WIS
        },
        15: {
            'Name': 'Hedgehog',
            'Genetic': breedingGeneticsList[32],  #Peapeapod
            'ShinyBonus': breedingShinyBonusList[8],  #Base LUK
        },
    },
}
breedingTotalPets = sum([len(petValues) for worldIndex, petValues in breedingSpeciesDict.items()])

shinyDaysList = [0, 3, 11, 33, 85, 200, 448, 964, 2013, 4107, 8227, 16234, 31633, 60989, 116522, 999999999]

def getShinyLevelFromDays(days: float) -> int:
    shinyLevel = 0
    for requirement in shinyDaysList:
        if float(days) > requirement:
            shinyLevel += 1
        else:
            break
    return shinyLevel

def getDaysToNextShinyLevel(days: float) -> float:
    shinyLevel = 0
    for requirement in shinyDaysList:
        if float(days) > requirement:
            shinyLevel += 1
    #logger.debug(f"Input days of {days} found to be less than {shinyDaysList[highestExceeded]} by {shinyDaysList[highestExceeded] - float(days)} days")
    try:
        daysRemaining = shinyDaysList[shinyLevel] - float(days)
        return daysRemaining
    except Exception as reason:
        logger.warning(f"With shinyLevel of {shinyLevel}, Defaulting Shiny days Remaining to 0. Reason: {reason}")
        return 0


###WORLD 5 CONSTS###
artifactTiers = ["Base", "Ancient", "Eldritch", "Sovereign"]
numberOfArtifactTiers = len(artifactTiers)
currentMaxChestsSum = 45  # Last verified as of v2.10
artifactsList = [
    'Moai Head', 'Maneki Kat', 'Ruble Cuble', 'Fauxory Tusk', 'Gold Relic',
    'Genie Lamp', 'Silver Ankh', 'Emerald Relic', 'Fun Hippoete', 'Arrowhead',
    '10 AD Tablet', 'Ashen Urn', 'Amberite', 'Triagulon', 'Billcye Tri',
    'Frost Relic', 'Chilled Yarn', 'Causticolumn', 'Jade Rock', 'Dreamcatcher',
    'Gummy Orb', 'Fury Relic', 'Cloud Urn', 'Weatherbook', 'Giants Eye',
    'Crystal Steak', 'Trilobite Rock', 'Opera Mask', 'Socrates', 'The True Lantern',
    'The Onyx Lantern', 'The Shim Lantern', 'The Winz Lantern'
]
numberOfArtifacts = len(artifactsList)
sailingDict = {
    1: {'Name': 'Safari Island', 'NormalTreasure': 'sailing-treasure-1', 'RareTreasure': 'sailing-treasure-2', 'Distance': 25, 'Artifacts': {
        0: {'Name': 'Moai Head'},
        1: {'Name': 'Maneki Kat'},
        2: {'Name': 'Ruble Cuble'},
        3: {'Name': 'Fauxory Tusk'}}},
    2: {'Name': 'Beachy Coast', 'NormalTreasure': 'sailing-treasure-3', 'RareTreasure': 'sailing-treasure-4', 'Distance': 100, 'Artifacts': {
        4: {'Name': 'Gold Relic'},
        5: {'Name': 'Genie Lamp'},
        6: {'Name': 'Silver Ankh'}}},
    3: {'Name': 'Isolated Woods', 'NormalTreasure': 'sailing-treasure-5', 'RareTreasure': 'sailing-treasure-6', 'Distance': 250, 'Artifacts': {
        7: {'Name': 'Emerald Relic'},
        8: {'Name': 'Fun Hippoete'}}},
    4: {'Name': 'Rocky Peaks', 'NormalTreasure': 'sailing-treasure-7', 'RareTreasure': 'sailing-treasure-8', 'Distance': 1000, 'Artifacts': {
        9: {'Name': 'Arrowhead'},
        10: {'Name': '10 AD Tablet'},
        11: {'Name': 'Ashen Urn'}}},
    5: {'Name': 'Stormy North', 'NormalTreasure': 'sailing-treasure-9', 'RareTreasure': 'sailing-treasure-10', 'Distance': 3000, 'Artifacts': {
        12: {'Name': 'Amberite'},
        13: {'Name': 'Triagulon'},
        14: {'Name': 'Billcye Tri'}}},
    6: {'Name': 'Snowy South', 'NormalTreasure': 'sailing-treasure-11', 'RareTreasure': 'sailing-treasure-12', 'Distance': 10000, 'Artifacts': {
        15: {'Name': 'Frost Relic'},
        16: {'Name': 'Chilled Yarn'}}},
    7: {'Name': 'Toxic Bay Inc', 'NormalTreasure': 'sailing-treasure-13', 'RareTreasure': 'sailing-treasure-14', 'Distance': 25000, 'Artifacts': {
        17: {'Name': 'Causticolumn'},
        18: {'Name': 'Jade Rock'}}},
    8: {'Name': 'Candied Island', 'NormalTreasure': 'sailing-treasure-15', 'RareTreasure': 'sailing-treasure-16', 'Distance': 100000, 'Artifacts': {
        19: {'Name': 'Dreamcatcher'},
        20: {'Name': 'Gummy Orb'}}},
    9: {'Name': 'Fungi Meadows', 'NormalTreasure': 'sailing-treasure-17', 'RareTreasure': 'sailing-treasure-18', 'Distance': 300000, 'Artifacts': {
        21: {'Name': 'Fury Relic'}}},
    10: {'Name': 'Cloudy Quay', 'NormalTreasure': 'sailing-treasure-19', 'RareTreasure': 'sailing-treasure-20', 'Distance': 1000000, 'Artifacts': {
        22: {'Name': 'Cloud Urn'},
        23: {'Name': 'Weatherbook'}}},
    11: {'Name': 'Dungeon Cove', 'NormalTreasure': 'sailing-treasure-21', 'RareTreasure': 'sailing-treasure-22', 'Distance': 2000000, 'Artifacts': {
        24: {'Name': 'Giants Eye'}}},
    12: {'Name': 'Crystal Enclave', 'NormalTreasure': 'sailing-treasure-23', 'RareTreasure': 'sailing-treasure-24', 'Distance': 5000000, 'Artifacts': {
        25: {'Name': 'Crystal Steak'}}},
    13: {'Name': 'Petulent Garage', 'NormalTreasure': 'sailing-treasure-25', 'RareTreasure': 'sailing-treasure-26', 'Distance': 15000000, 'Artifacts': {
        26: {'Name': 'Trilobite Rock'}}},
    14: {'Name': 'Isle of Note', 'NormalTreasure': 'sailing-treasure-27', 'RareTreasure': 'sailing-treasure-28', 'Distance': 40000000, 'Artifacts': {
        27: {'Name': 'Opera Mask'},
        28: {'Name': 'Socrates'}}},
    15: {'Name': 'The Edge', 'NormalTreasure': 'sailing-treasure-29', 'RareTreasure': 'sailing-treasure-30', 'Distance': 100000000, 'Artifacts': {
        29: {'Name': 'The True Lantern'},
        30: {'Name': 'The Onyx Lantern'},
        31: {'Name': 'The Shim Lantern'},
        32: {'Name': 'The Winz Lantern'}}},
}
divinity_divinitiesDict = {
    1: {
        "Name": "Snehebatu",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'green-bits'
    },
    2: {
        "Name": "Arctis",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'sailing-treasure-0'
    },
    3: {
        "Name": "Nobisect",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'red-bits'
    },
    4: {
        "Name": "Harriep",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'coins'
    },
    5: {
        "Name": "Goharut",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'red-bits'
    },
    6: {
        "Name": "Omniphau",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'particles'
    },
    7: {
        "Name": "Purrmep",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'coins'
    },
    8: {
        "Name": "Flutterbis",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'particles'
    },
    9: {
        "Name": "Kattlekruk",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'purple-bits'
    },
    10: {
        "Name": "Bagur",
        "Unlocked": False,
        "BlessingLevel": 0,
        'BlessingMaterial': 'particles'
    },
    }
divinity_offeringsDict = {
    0: {
        "Name":"Olive Branch",
        "Image":"offering-1",
        "Chance":1,
    },
    1: {
        "Name": "Incense",
        "Image": "offering-5",
        "Chance": 5,
    },
    2: {
        "Name": "Giftbox",
        "Image": "offering-10",
        "Chance": 10,
    },
    3: {
        "Name": "Tithe",
        "Image": "offering-25",
        "Chance": 25,
    },
    4: {
        "Name": "Hearty Meal",
        "Image": "offering-50",
        "Chance": 50,
    },
    5: {
        "Name": "Sacrifice",
        "Image": "offering-100",
        "Chance": 100,
    },
}
divinity_stylesDict = {
    0: {
        "Name": "Kinesis",
        "UnlockLevel": 1,
        "Points": 1,
        "Exp": 1,
    },
    1: {
        "Name": "Chakra",
        "UnlockLevel": 5,
        "Points": 2,
        "Exp": 2,
    },
    2: {
        "Name": "Focus",
        "UnlockLevel": 10,
        "Points": 4,
        "Exp": 1,
    },
    3: {
        "Name": "Mantra",
        "UnlockLevel": 15,
        "Points": 0,
        "Exp": 1,
        "Notes": "(To all characters)"
    },
    4: {
        "Name": "Vitalic",
        "UnlockLevel": 25,
        "Points": 2,
        "Exp": 7,
    },
    5: {
        "Name": "TranQi",
        "UnlockLevel": 40,
        "Points": 0,
        "Exp": 3,
        "Notes": "(Even when not Meditating)"
    },
    6: {
        "Name": "Zen",
        "UnlockLevel": 60,
        "Points": 8,
        "Exp": 8,
    },
    7: {
        "Name": "Mindful",
        "UnlockLevel": 80,
        "Points": 15,
        "Exp": 10,
    },
}
divLevelReasonsDict = {
    0: "",
    2: "to activate Doot",
    40: "to unlock the TranQi Style.",
    50: "to unlock the Multitool Stamp from Poigu's quest."
}
#From code, GamingUpg = function (). Last updated 2.11 Kangaroo
gamingSuperbitsDict = {
    #
    0: {'Name': 'Bits per Achievement', 'BonusText': "x1.03 Bits per Achievement you've unlocked", 'Cost': 1e9, 'CodeString': '_'},
    1: {'Name': 'Plant Evo', 'BonusText': '+1 Max Evolution for all plants. This is 20x rarer than normal evolutions', 'Cost': 30e9, 'CodeString': 'a'},
    2: {'Name': 'Obol Stat Booster', 'BonusText': 'All obols give +40% more STR/AGI/WIS/LUK than what they say they do!', 'Cost': 0, 'CodeString': 'b'},
    3: {'Name': 'MSA Sailing', 'BonusText': 'MSA now gives +1% bonus Sailing Speed per 10 total Waves', 'Cost': 0, 'CodeString': 'c'},
    4: {'Name': 'Moar Bubbles', 'BonusText': '+20% chance for +1 more bubble boosted by No Bubble Left Behind', 'Cost': 0, 'CodeString': 'd'},
    5: {'Name': 'Plant Evo II', 'BonusText': '+1 Max Evolution for all plants. This one is 5000x rarer than normal', 'Cost': 0, 'CodeString': 'e'},
    6: {'Name': 'Worship Totem HP', 'BonusText': '+5 Max HP for Worship Totem during Tower Defence summon battle', 'Cost': 0, 'CodeString': 'f'},
    7: {'Name': 'MSA Totalizer', 'BonusText': 'Unlock the Totalizer for the Miniature Soul Apparatus (MSA) in World 3', 'Cost': 0, 'CodeString': 'g'},
    8: {'Name': 'Shrine Speed', 'BonusText': 'All shrines level up +50% faster than normal', 'Cost': 0, 'CodeString': 'h'},
    9: {'Name': 'No more Praying', 'BonusText': 'If no Prayers equipped, get 1/5th bonus of all prayers, and no curses', 'Cost': 0, 'CodeString': 'i'},
    10: {'Name': 'Double EXP', 'BonusText': '+15% chance for Double Exp whenever claiming AFK gains', 'Cost': 0, 'CodeString': 'j'},
    11: {'Name': 'MSA Class EXP', 'BonusText': 'MSA now gives +1% bonus Class EXP per 10 total Waves', 'Cost': 0, 'CodeString': 'k'},
    12: {'Name': 'Library Checkouts', 'BonusText': '+1% faster Library Checkout Speed per Gaming Lv.', 'Cost': 0, 'CodeString': 'l'},
    13: {'Name': 'MSA Mealing', 'BonusText': 'MSA now gives +10% bonus Meal Cooking speed per 10 total Waves', 'Cost': 0, 'CodeString': 'm'},
    14: {'Name': 'Spice is Nice', 'BonusText': 'All spice claimed, either manually or automatically, is worth 1.5x more.', 'Cost': 0, 'CodeString': 'n'},
    15: {'Name': 'Worship Totem HPr', 'BonusText': '+10 Max HP for Worship Totem during Tower Defence summon battle', 'Cost': 0, 'CodeString': 'o'},
    16: {'Name': 'MSA Skill EXP', 'BonusText': 'MSA now gives +1% bonus Skill Exp per 10 total Waves', 'Cost': 0, 'CodeString': 'p'},
    17: {'Name': 'Spice is Nicer', 'BonusText': 'All spice claimed, either manually or automatically, is worth 2x more.', 'Cost': 0, 'CodeString': 'q'},
    18: {'Name': 'Plant Evo III', 'BonusText': '+1 Max Evolution for all plants. This one is 250x rarer than normal', 'Cost': 0, 'CodeString': 'r'},
    19: {'Name': 'Noobie Gains', 'BonusText': 'Your lowest Leveled character gets 1.5x Class EXP', 'Cost': 0, 'CodeString': 's'},
    20: {'Name': 'MSA Big Bits', 'BonusText': 'MSA now gives +50% Bits for Gaming per 10 total Waves', 'Cost': 0, 'CodeString': 't'},
    21: {'Name': 'Atom Redux', 'BonusText': 'All atom upgrading is now 10% cheaper', 'Cost': 0, 'CodeString': 'u'},
    22: {'Name': 'Even Moar Bubbles', 'BonusText': '+30% chance for +1 more bubble boosted by No Bubble Left Behind', 'Cost': 0, 'CodeString': 'v'},
    23: {'Name': 'Isotope Discovery', 'BonusText': 'All atoms now have +10 Max LV', 'Cost': 0, 'CodeString': 'w'},
}


def getDivinityNameFromIndex(inputValue: int) -> str:
    return divinity_divinitiesDict.get(inputValue, {"Name": f"UnknownDivinity{inputValue}"}).get("Name")
def getOfferingNameFromIndex(inputValue):
    return divinity_offeringsDict.get(inputValue, {"Name": f"UnknownOffering{inputValue}"}).get("Name")

def getStyleNameFromIndex(inputValue: int) -> str:
    return divinity_stylesDict.get(inputValue, {"Name": f"UnknownStyle{inputValue}"}).get("Name")


###WORLD 6 CONSTS###
jade_emporium = [
    {
        "Name": "Quick Ref Access",
        "Bonus": "Adds the Sneaking skill to your QuickRef menu! Manage your Ninja Twins from anywhere!",
        "CodeString": "_"
    },
    {
        "Name": "MSA Expander I",
        "Bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically Farming EXP!",
        "CodeString": "l"
    },
    {
        "Name": "Level Exemption",
        "Bonus": "Completely and utterly removes the UNDER-LEVELED bonus reduction of all stamps in your collection, now and forever. Amen.",
        "CodeString": "e"
    },
    {
        "Name": "The Artifact Matrix",
        "Bonus": "Extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to Artifact Find Chance!",
        "CodeString": "h"
    },
    {
        "Name": "Crop Depot Scientist",
        "Bonus": "Employs a friendly scientist blobulyte to keep a Data Sheet of all the crops you've ever found!",
        "CodeString": "v"
    },
    {
        "Name": "Reinforced Science Pencil",
        "Bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+20% Total Damage' per Crop!",
        "CodeString": "A"
    },
    {
        "Name": "Essence Confetti",
        "Bonus": "Adds a new bonus of +3% All Essence Gain per 10 items found after 1000 items, as shown at The Slab in World 5.",
        "CodeString": "r"
    },
    {
        "Name": "Gold Food Beanstalk",
        "Bonus": "Grows a giant beanstalk behind the ninja castle! Drop a stack of 10,000 Gold Food to add it with the beanstalk and permanently gain its bonus!",
        "CodeString": "a"
    },
    {
        "Name": "Jade Coin Magnetism",
        "Bonus": "Adds a new bonus of +5% Jade Coin Gain per 10 items found after 1000 items, as shown at The Slab in World 5.",
        "CodeString": "q"
    },
    {
        "Name": "Science Pen",
        "Bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '1.02x Plant Evolution Chance in Gaming (multiplicative)' per Crop!",
        "CodeString": "x"
    },
    {
        "Name": "Shrine Collective Bargaining Agreement",
        "Bonus": "Shrines no longer lose EXP when moved around, so you can finally bring those baddies out of retirement!",
        "CodeString": "s"
    },
    {
        "Name": "Science Marker",
        "Bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+8% Jade Coin Gain' per Crop!",
        "CodeString": "y"
    },
    {
        "Name": "MSA Expander II",
        "Bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically Jade Coin Gain!",
        "CodeString": "m"
    },
    {
        "Name": "No Meal Left Behind",
        "Bonus": "Every 24 hours, your lowest level Meal gets +1 Lv. This only works on Meals Lv 5 or higher, and doesn't trigger on days you don't play.",
        "CodeString": "p"
    },
    {
        "Name": "Science Featherpen",
        "Bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '1.10x Cooking Speed (multiplicative)' per Crop!",
        "CodeString": "z"
    },
    {
        "Name": "Revenge of the Pickle",
        "Bonus": "Adds a new boss page to the left of World 1 in Deathnote. Each BoneJoePickle in your inventory counts as +1 Boss Deathnote Kill!",
        "CodeString": "g"
    },
    {
        "Name": "The Slab Matrix",
        "Bonus": "Further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to all bonuses from the Slab!",
        "CodeString": "i"
    },
    {
        "Name": "Science Environmentally Sourced Pencil",
        "Bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+15% Cash from Mobs' per crop found!",
        "CodeString": "w"
    },
    {
        "Name": "MSA Expander III",
        "Bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically All Essence Gain!",
        "CodeString": "n"
    },
    {
        "Name": "Papa Blob's Quality Guarantee",
        "Bonus": "Increases the Max Level of all cooking meals by +10. Better meals, better levels, Papa Blob's.",
        "CodeString": "t"
    },
    {
        "Name": "Science Crayon",
        "Bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+7% Shiny Pet Lv Up Rate and Pet Breeding Rate' per Crop!",
        "CodeString": "B"
    },
    {
        "Name": "Supersized Gold Beanstacking",
        "Bonus": "You can now drop a stack of 100,000 Gold Food to supersize it! This will obviously give a bigger bonus, and will even enlargen the food on the stalk!",
        "CodeString": "b"
    },
    {
        "Name": "Charmed, I'm Sure",
        "Bonus": "All your Ninja Twins can now equip two of the same charm at once!",
        "CodeString": "c"
    },
    {
        "Name": "Deal Sweetening",
        "Bonus": "Earn +25% more Magic Beans from the mysterious Legumulyte bean merchant found in the Troll Broodnest map.",
        "CodeString": "o"
    },
    {
        "Name": "The Spirit Matrix",
        "Bonus": "Even further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to W6 Skill exp gain!",
        "CodeString": "j"
    },
    {
        "Name": "The Crop Matrix",
        "Bonus": "Yet again even further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to Crop Depot!",
        "CodeString": "k"
    },
    {
        "Name": "Gaming to the MAX",
        "Bonus": "All plant types in Gaming have +1 Max Evolution, but this one is 50,000x rarer than normal and will make you wonder if evolution is even real (it is)",
        "CodeString": "f"
    },
    {
        "Name": "Chef Geustloaf's Cutting Edge Philosophy",
        "Bonus": "Increases the Max Level of all cooking meals by +10 again! But oh hoho, you sir are no Chef Geustloaf! Good luck cooking to these LVs!",
        "CodeString": "u"
    },
    {
        "Name": "Sovereign Artifacts",
        "Bonus": "You can now find Sovereign Artifacts from sailing, but only if you've found the Eldritch form first.",
        "CodeString": "I"
    },
    {
        "Name": "New Critter",
        "Bonus": "Unlocks a new critter type to capture! These have their own very special vial in Alchemy.",
        "CodeString": "D"
    },
    {
        "Name": "Brighter Lighthouse Bulb",
        "Bonus": "You can now find 3 additional Artifacts from The Edge island.",
        "CodeString": "H"
    },
    {
        "Name": "Laboratory Bling",
        "Bonus": "Adds 3 new Jewels to unlock at the Jewel Spinner in W4 Town. Or, get one for free every 700 total Lab LV as shown in Rift Skill Mastery.",
        "CodeString": "K"
    },
    {
        "Name": "Science Paintbrush",
        "Bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+0.1 Base Critter caught in Trapping' per Crop!",
        "CodeString": "C"
    },
    {
        "Name": "Ionized Sigils",
        "Bonus": "Sigils can now be upgraded a 3rd time. Push past lame ol' yellow, and further increasing those sigil boosts!",
        "CodeString": "E"
    },
    {
        "Name": "The Endercaptain",
        "Bonus": "Adds the Endercaptain to Recruitment pool. They're very rare, and have a hidden account-wide +25% Loot Multi and Artifact Find.",
        "CodeString": "F"
    },
    {
        "Name": "Mob Cosplay Craze",
        "Bonus": "Certain monsters in World 6 will now have a rare chance to drop Ninja Hats, but only the ones you've found already from the Ninja Castle!",
        "CodeString": "d"
    },
    {
        "Name": "New Bribes",
        "Bonus": "Mr. Pigibank is up to no good once again, and he's looking to get some funding from his favorite patron... you. Well, your wallet specifically.",
        "CodeString": "J"
    },
    {
        "Name": "True Godly Blessings",
        "Bonus": "All Divinity Gods give 1.05x higher Blessing bonus per God Rank. Whats a Blessing bonus? Select a god, it's the one on the bottom, go look.",
        "CodeString": "G"
    },

]
gfood_codes = ["PeanutG", "ButterBar", *[f"FoodG{i}" for i in range(1, 14)]]
pristineCharmsList: list[str] = [
    "Sparkle Log", "Fruit Rolle", "Glowing Veil", "Cotton Candy", "Sugar Bomb",
    "Gumm Eye", "Bubblegum Law", "Sour Wowzer", "Crystal Comb", "Rock Candy",
    "Lollipop Law", "Taffy Disc", "Stick of Chew", "Treat Sack", "Gumm Stick",
    "Lolly Flower", "Gumball Necklace", "Liqorice Rolle",
]
sneakingGemstonesList: list[str] = [
    "Aquamarine", "Emerald", "Garnet", "Starite", "Topaz", "Moissanite"
]
sneakingGemstonesStatList: list[str] = [
    "Stealth", "Jade", "Door Damage", "Gold Charm Bonus", "Sneak EXP", "Gemstone Bonuses"
]
sneakingGemstonesFirstIndex = 233
sneakingGemstonesCount = len(sneakingGemstonesList)
sneakingGemstonesMaxValueDict = {"Aquamarine": 10000, "Emerald": 5000, "Garnet": 2500, "Starite": 200, "Topaz": 1000, "Moissanite": 300}
maxFarmingCrops = 160  # Last verified as of 2.11 Land Rank update
landrankDict = {
    0: {'Name': 'Evolution Boost', 'UnlockLevel': 1, 'Value': 250},
    1: {'Name': 'Production Boost', 'UnlockLevel': 5, 'Value': 5},
    2: {'Name': 'Soil Exp Boost', 'UnlockLevel': 20, 'Value': 25},
    3: {'Name': 'Evolution Megaboost', 'UnlockLevel': 30, 'Value': 600},
    4: {'Name': 'Seed of Stealth', 'UnlockLevel': 60, 'Value': 2},
    5: {'Name': 'Farmtastic Boost', 'UnlockLevel': 80, 'Value': 90},
    6: {'Name': 'Soil Exp Megaboost', 'UnlockLevel': 125, 'Value': 200},
    7: {'Name': 'Overgrowth Boost', 'UnlockLevel': 180, 'Value': 120},
    8: {'Name': 'Production Megaboost', 'UnlockLevel': 250, 'Value': 100},
    9: {'Name': 'Seed of Loot', 'UnlockLevel': 400, 'Value': 10},
    10: {'Name': 'Evolution Superboost', 'UnlockLevel': 500, 'Value': 3000},
    11: {'Name': 'Overgrowth Megaboost', 'UnlockLevel': 600, 'Value': 340},
    12: {'Name': 'Farmtastic Megaboost', 'UnlockLevel': 700, 'Value': 110},
    13: {'Name': 'Soil Exp Superboost', 'UnlockLevel': 900, 'Value': 520},
    14: {'Name': 'Seed of Damage', 'UnlockLevel': 1200, 'Value': 20},
    15: {'Name': 'Evolution Ultraboost', 'UnlockLevel': 1300, 'Value': 40000},
    16: {'Name': 'Farmtastic Superboost', 'UnlockLevel': 1500, 'Value': 220},
    17: {'Name': 'Production Superboost', 'UnlockLevel': 1750, 'Value': 600},
    18: {'Name': 'Overgrowth Superboost', 'UnlockLevel': 2000, 'Value': 240},
    19: {'Name': 'Seed of Stats', 'UnlockLevel': 3500, 'Value': 5},
}
marketUpgradeList = [
    "Land Plots", "Stronger Vines", "Nutritious Soil", "Smarter Seeds",
    "Biology Boost", "Product Doubler", "More Beenz", "Rank Boost",
    "Overgrowth", "Evolution GMO", "Speed GMO", "OG Fertilizer",
    "EXP GMO", "Land Rank", "Value GMO", "Super GMO"]
marketUpgradeFirstIndex = 2
marketUpgradeLastIndex = marketUpgradeFirstIndex + len(marketUpgradeList)

def getMoissaniteValue(moissaniteLevel: int):
    try:
        if moissaniteLevel > 0:
            return 3+(300*(moissaniteLevel/(moissaniteLevel+1000)))
        else:
            return 0
    except:
        return 0
def getGemstoneValue(gemstoneName: str, gemstoneLevel: int, moissaniteLevel: int, moissaniteValue: float):
    moissaniteMulti = 1 + (moissaniteValue / 100)
    value = 0
    if gemstoneLevel > 0:
        if gemstoneName == "Aquamarine":
            value = 40 + (10000 * (gemstoneLevel / (gemstoneLevel + 1000)))
        elif gemstoneName == "Emerald":
            value = 15 + (5000  * (gemstoneLevel / (gemstoneLevel + 1000)))
        elif gemstoneName == "Garnet":
            value = 12 + (2500  * (gemstoneLevel / (gemstoneLevel + 1000)))
        elif gemstoneName == "Starite":
            value = 5 +  (200   * (gemstoneLevel / (gemstoneLevel + 1000)))
        elif gemstoneName == "Topaz":
            value = 10 + (1000  * (gemstoneLevel / (gemstoneLevel + 1000)))

    if moissaniteLevel > 0:
        value *= moissaniteMulti
    return value
def getGemstonePercent(gemstoneName: str, gemstoneValue: float):
    try:
        return 100 * (gemstoneValue / sneakingGemstonesMaxValueDict[gemstoneName])
    except Exception as reason:
        logger.exception(f"Could not find max value for Gemstone: {gemstoneName} because: {reason}")
    pass


# Maps to the RewardID, 1 indexed because Lava
summoningRewards = [
    "",
    "x Total DMG", "x Jade Gain", "x Farming SPD", "x Artifact Find",
    "Lab Con Range", "x All Essence", "x Sneak EXP", "x Sigil SPD",
    "x Farming EXP", "% Drop Rate", "x Crop EVO", "% AFK Gains",
    "% Skill EXP", "x Construct SPD", "x Skill Effncy.", "x Cooking SPD",
    "x Gaming Bits", "x Shiny EXP", "% All Stat", "Library Max"
]

# Plenty of unknown values. HP, damage, speed, reward size, etc seem to require calculation 
summoningDict = {
    "White": {
        0: {
            "EnemyID": "Pet1", "Value2": 29, "Value3": 24, "Value4": 12, "OpponentName": "Pablo and his Plump Piggies",
            "RewardID": summoningRewards[1], "Value8": 0, "Image": "piggo",
        },
        1: {
            "EnemyID": "Pet2", "Value2": 25, "Value3": 26, "Value4": 12, "OpponentName": "Gam3rPr0digy and their Boar Stampede",
            "RewardID": summoningRewards[2], "Value8": 1, "Image": "wild-boar",
        },
        2: {
            "EnemyID": "Pet3", "Value2": 23, "Value3": 22, "Value4": 17, "OpponentName": "Donald and his Quacky Ducks",
            "RewardID": summoningRewards[3], "Value8": 2, "Image": "mallay",
        },
        3: {
            "EnemyID": "Pet0", "Value2": 28, "Value3": 23, "Value4": 12, "OpponentName": "Sandy and her Nutty Squirrels",
            "RewardID": summoningRewards[6], "Value8": 3, "Image": "squirrel",
        },
        4: {
            "EnemyID": "Pet4", "Value2": 30, "Value3": 25, "Value4": 18, "OpponentName": "Popo and their Largest of Mammalians",
            "RewardID": summoningRewards[4], "Value8": 5, "Image": "whale",
        },
        5: {
            "EnemyID": "Pet6", "Value2": 34, "Value3": 21, "Value4": 18, "OpponentName": "Little Susie and her Bunny Family",
            "RewardID": summoningRewards[2], "Value8": 7, "Image": "bunny",
        },
        6: {
            "EnemyID": "Pet5", "Value2": 26, "Value3": 29, "Value4": 14, "OpponentName": "MoveFan84 and his Famous Nacho Batallion",
            "RewardID": summoningRewards[1], "Value8": 13, "Image": "chippy",
        },
        7: {
            "EnemyID": "Pet10", "Value2": 30, "Value3": 38, "Value4": 15, "OpponentName": "Ronaldo and his Cool Freakin' Birdz",
            "RewardID": summoningRewards[5], "Value8": 24, "Image": "cool-bird",
        },
        8: {
            "EnemyID": "Pet11", "Value2": 34, "Value3": 30, "Value4": 16, "OpponentName": "Master Oogman and his Speedy Hedgehogs",
            "RewardID": summoningRewards[3], "Value8": 40, "Image": "hedgehog",
        },
    },
    "Green": {
        0: {
            "EnemyID": "mushG", "Value2": 26, "Value3": 41, "Value4": 8, "OpponentName": "Jonesy and his Lil Mushies",
            "RewardID": summoningRewards[1], "Value8": 4, "Image": "green-mushroom",
        },
        1: {
            "EnemyID": "mushR", "Value2": 20, "Value3": 38, "Value4": 13, "OpponentName": "Walter and his Lil Shrooms",
            "RewardID": summoningRewards[7], "Value8": 5, "Image": "red-mushroom",
        },
        2: {
            "EnemyID": "frogG", "Value2": 27, "Value3": 18, "Value4": 9, "OpponentName": "Lex and her Hoppy Frogs",
            "RewardID": summoningRewards[2], "Value8": 6, "Image": "frog",
        },
        3: {
            "EnemyID": "beanG", "Value2": 47, "Value3": 32, "Value4": 16, "OpponentName": "Bongo and his Lazy Beans",
            "RewardID": summoningRewards[1], "Value8": 8, "Image": "bored-bean",
        },
        4: {
            "EnemyID": "slimeG", "Value2": 23, "Value3": 15, "Value4": 10, "OpponentName": "Sam and his Goopy Slimes",
            "RewardID": summoningRewards[5], "Value8": 10, "Image": "slime",
        },
        5: {
            "EnemyID": "snakeG", "Value2": 33, "Value3": 24, "Value4": 14, "OpponentName": "Mika and his Itty Bitty Baby Boas",
            "RewardID": summoningRewards[2], "Value8": 12, "Image": "baby-boa",
        },
        6: {
            "EnemyID": "carrotO", "Value2": 42, "Value3": 22, "Value4": 24, "OpponentName": "Guy Montag and his Walking Veggies",
            "RewardID": summoningRewards[3], "Value8": 15, "Image": "carrotman",
        },
        7: {
            "EnemyID": "goblinG", "Value2": 38, "Value3": 34, "Value4": 16, "OpponentName": "Gork and his Ugly Glublins",
            "RewardID": summoningRewards[4], "Value8": 17, "Image": "glublin",
        },
        8: {
            "EnemyID": "plank", "Value2": 44, "Value3": 21, "Value4": 21, "OpponentName": "Ed and his Stolen Planks",
            "RewardID": summoningRewards[8], "Value8": 19, "Image": "wode-board",
        },
        9: {
            "EnemyID": "frogBIG", "Value2": 56, "Value3": 33, "Value4": 22, "OpponentName": "Gigachad and his Awesome Gigafrogs",
            "RewardID": summoningRewards[5], "Value8": 21, "Image": "gigafrog",
        },
        10: {
            "EnemyID": "poopSmall", "Value2": 26, "Value3": 19, "Value4": 11, "OpponentName": "TP Pete Jr and his Battle Poops",
            "RewardID": summoningRewards[6], "Value8": 25, "Image": "poop",
        },
        11: {
            "EnemyID": "ratB", "Value2": 31, "Value3": 19, "Value4": 13, "OpponentName": "Michael and his Rodents",
            "RewardID": summoningRewards[4], "Value8": 28, "Image": "rat",
        },
        12: {
            "EnemyID": "branch", "Value2": 32, "Value3": 31, "Value4": 20, "OpponentName": "Kyle and his Branch Brigade",
            "RewardID": summoningRewards[3], "Value8": 31, "Image": "walking-stick",
        },
        13: {
            "EnemyID": "acorn", "Value2": 42, "Value3": 25, "Value4": 17, "OpponentName": "Aaron and his Aacorn Gang",
            "RewardID": summoningRewards[6], "Value8": 39, "Image": "nutto",
        },
        14: {
            "EnemyID": "mushW", "Value2": 26, "Value3": 37, "Value4": 13, "OpponentName": "Kip and his Lil Fungi",
            "RewardID": summoningRewards[1], "Value8": 50, "Image": "wood-mushroom",
        },
    },
    "Yellow": {
        0: {
            "EnemyID": "jarSand", "Value2": 31, "Value3": 20, "Value4": 12, "OpponentName": "Karen and her Pots",
            "RewardID": summoningRewards[9], "Value8": 9, "Image": "sandy-pot",
        },
        1: {
            "EnemyID": "mimicA", "Value2": 33, "Value3": 30, "Value4": 16, "OpponentName": "Jimmy and his Enthusiastic Mimics",
            "RewardID": summoningRewards[7], "Value8": 11, "Image": "mimic",
        },
        2: {
            "EnemyID": "crabcake", "Value2": 35, "Value3": 43, "Value4": 21, "OpponentName": "Eugene and his Frosted Crabs",
            "RewardID": summoningRewards[10], "Value8": 14, "Image": "crabcake",
        },
        3: {
            "EnemyID": "coconut", "Value2": 49, "Value3": 25, "Value4": 14, "OpponentName": "Nobby and his Gang of Nuts",
            "RewardID": summoningRewards[2], "Value8": 16, "Image": "mafioso",
        },
        4: {
            "EnemyID": "sandcastle", "Value2": 32, "Value3": 17, "Value4": 17, "OpponentName": "Tiny Tim and his Cool Castles",
            "RewardID": summoningRewards[8], "Value8": 18, "Image": "sand-castle",
        },
        5: {
            "EnemyID": "pincermin", "Value2": 39, "Value3": 54, "Value4": 26, "OpponentName": "Tira and her Shrewd Pincermen",
            "RewardID": summoningRewards[7], "Value8": 22, "Image": "pincermin",
        },
        6: {
            "EnemyID": "potato", "Value2": 57, "Value3": 58, "Value4": 28, "OpponentName": "Misha and her Super Spuds",
            "RewardID": summoningRewards[3], "Value8": 26, "Image": "mashed-potato",
        },
        7: {
            "EnemyID": "steak", "Value2": 55, "Value3": 37, "Value4": 23, "OpponentName": "Wlad and his Rootin' Tootin' Tysons",
            "RewardID": summoningRewards[5], "Value8": 30, "Image": "tyson",
        },
        8: {
            "EnemyID": "moonman", "Value2": 27, "Value3": 29, "Value4": 22, "OpponentName": "Mac and his Many Moonmoons",
            "RewardID": summoningRewards[11], "Value8": 34, "Image": "moonmoon",
        },
        9: {
            "EnemyID": "sandgiant", "Value2": 50, "Value3": 21, "Value4": 23, "OpponentName": "Sir Reginald and his Gentlemen Giants",
            "RewardID": summoningRewards[4], "Value8": 45, "Image": "sand-giant",
        },
        10: {
            "EnemyID": "snailZ", "Value2": 42, "Value3": 26, "Value4": 25, "OpponentName": "Shelby and her Shelled Snelbies",
            "RewardID": summoningRewards[1], "Value8": 60, "Image": "snelbie",
        },
    },
    "Blue": {
        0: {
            "EnemyID": "sheep", "Value2": 32, "Value3": 31, "Value4": 14, "OpponentName": "Paulie and his Sheepie Herd",
            "RewardID": summoningRewards[12], "Value8": 20, "Image": "sheepie",
        },
        1: {
            "EnemyID": "flake", "Value2": 35, "Value3": 28, "Value4": 14, "OpponentName": "Dirk and his Celsius Flakes",
            "RewardID": summoningRewards[9], "Value8": 23, "Image": "frost-flake",
        },
        2: {
            "EnemyID": "stache", "Value2": 30, "Value3": 19, "Value4": 14, "OpponentName": "Mr Harrison and his Mighty Staches",
            "RewardID": summoningRewards[6], "Value8": 27, "Image": "sir-stache",
        },
        3: {
            "EnemyID": "bloque", "Value2": 40, "Value3": 27, "Value4": 12, "OpponentName": "Gibby and his Bloque Offensive",
            "RewardID": summoningRewards[1], "Value8": 29, "Image": "bloque",
        },
        4: {
            "EnemyID": "mamoth", "Value2": 37, "Value3": 22, "Value4": 14, "OpponentName": "Esther and her Trampler Mamooths",
            "RewardID": summoningRewards[8], "Value8": 32, "Image": "mamooth",
        },
        5: {
            "EnemyID": "snowball", "Value2": 33, "Value3": 26, "Value4": 20, "OpponentName": "Frosty and his Relatives",
            "RewardID": summoningRewards[13], "Value8": 35, "Image": "snowman",
        },
        6: {
            "EnemyID": "penguin", "Value2": 52, "Value3": 24, "Value4": 22, "OpponentName": "The Accountant and his Trusty Penguins",
            "RewardID": summoningRewards[2], "Value8": 38, "Image": "penguin",
        },
        7: {
            "EnemyID": "thermostat", "Value2": 43, "Value3": 39, "Value4": 25, "OpponentName": "Fermi and his Thermies",
            "RewardID": summoningRewards[4], "Value8": 41, "Image": "thermister",
        },
        8: {
            "EnemyID": "glass", "Value2": 35, "Value3": 27, "Value4": 15, "OpponentName": "Kristen and her Chill Quenchies",
            "RewardID": summoningRewards[10], "Value8": 46, "Image": "quenchie",
        },
        9: {
            "EnemyID": "snakeB", "Value2": 31, "Value3": 18, "Value4": 14, "OpponentName": "Rob and his Ice Cold Killer Snakes",
            "RewardID": summoningRewards[14], "Value8": 49, "Image": "cryosnake",
        },
        10: {
            "EnemyID": "speaker", "Value2": 30, "Value3": 38, "Value4": 21, "OpponentName": "Lil Plump and his Dope Bops",
            "RewardID": summoningRewards[15], "Value8": 51, "Image": "bop-box",
        },
        11: {
            "EnemyID": "eye", "Value2": 39, "Value3": 23, "Value4": 18, "OpponentName": "Nadia and her All Seeing Eyes",
            "RewardID": summoningRewards[7], "Value8": 54, "Image": "neyeptune",
        },
        12: {
            "EnemyID": "ram", "Value2": 37, "Value3": 42, "Value4": 21, "OpponentName": "Shepherd and his Flock of Rams",
            "RewardID": summoningRewards[5], "Value8": 65, "Image": "dedotated-ram",
        },
        13: {
            "EnemyID": "skele2", "Value2": 33, "Value3": 31, "Value4": 30, "OpponentName": "Brody and his Infamous Bloodbones",
            "RewardID": summoningRewards[11], "Value8": 74, "Image": "bloodbone",
        },
    },
    "Purple": {
        0: {
            "EnemyID": "mushP", "Value2": 33, "Value3": 32, "Value4": 16, "OpponentName": "ProXD and his Mushrooms of Mischief",
            "RewardID": summoningRewards[16], "Value8": 33, "Image": "purp-mushroom",
        },
        1: {
            "EnemyID": "w4a2", "Value2": 31, "Value3": 36, "Value4": 23, "OpponentName": "Tallie and her Rambunctious TVs",
            "RewardID": summoningRewards[9], "Value8": 36, "Image": "tv",
        },
        2: {
            "EnemyID": "w4a3", "Value2": 37, "Value3": 37, "Value4": 21, "OpponentName": "Homer and his Epic Donuts",
            "RewardID": summoningRewards[1], "Value8": 37, "Image": "donut",
        },
        3: {
            "EnemyID": "demonP", "Value2": 53, "Value3": 34, "Value4": 31, "OpponentName": "Nostalgo and his Genies of Olde",
            "RewardID": summoningRewards[3], "Value8": 42, "Image": "demon-genie",
        },
        4: {
            "EnemyID": "w4b2", "Value2": 28, "Value3": 29, "Value4": 18, "OpponentName": "Dalia and her Hyperactive Drinks",
            "RewardID": summoningRewards[12], "Value8": 43, "Image": "soda-can",
        },
        5: {
            "EnemyID": "w4b1", "Value2": 19, "Value3": 23, "Value4": 10, "OpponentName": "Werm and his Worms",
            "RewardID": summoningRewards[6], "Value8": 47, "Image": "flying-worm",
        },
        6: {
            "EnemyID": "w4b3", "Value2": 36, "Value3": 36, "Value4": 22, "OpponentName": "JelloL0ver87 and his Beloved Gel Cubes",
            "RewardID": summoningRewards[8], "Value8": 52, "Image": "gelatinous-cuboid",
        },
        7: {
            "EnemyID": "w4b4", "Value2": 46, "Value3": 32, "Value4": 28, "OpponentName": "Megacorp Representative and his Product",
            "RewardID": summoningRewards[13], "Value8": 56, "Image": "choccie",
        },
        8: {
            "EnemyID": "w4b5", "Value2": 37, "Value3": 33, "Value4": 30, "OpponentName": "Werm's Stepsister and her Worms",
            "RewardID": summoningRewards[1], "Value8": 61, "Image": "biggole-wurm",
        },
        9: {
            "EnemyID": "w4c1", "Value2": 26, "Value3": 26, "Value4": 14, "OpponentName": "DQ and their abandoned Clammies",
            "RewardID": summoningRewards[2], "Value8": 62, "Image": "clammie",
        },
        10: {
            "EnemyID": "w4c2", "Value2": 19, "Value3": 24, "Value4": 10, "OpponentName": "Dee and her 'dars",
            "RewardID": summoningRewards[4], "Value8": 66, "Image": "octodar",
        },
        11: {
            "EnemyID": "w4c3", "Value2": 33, "Value3": 30, "Value4": 24, "OpponentName": "Gordon and his Eloquent Flombeiges",
            "RewardID": summoningRewards[10], "Value8": 70, "Image": "flombeige",
        },
        12: {
            "EnemyID": "w4c4", "Value2": 66, "Value3": 39, "Value4": 30, "OpponentName": "Giuseppe and his Power Tools",
            "RewardID": summoningRewards[14], "Value8": 78, "Image": "stilted-seeker",
        },

    },
    "Red": {
        0: {
            "EnemyID": "w5a1", "Value2": 24, "Value3": 20, "Value4": 10, "OpponentName": "Jawz and his Hot Smokin Suggmas",
            "RewardID": summoningRewards[17], "Value8": 44, "Image": "suggma",
        },
        1: {
            "EnemyID": "w5a2", "Value2": 20, "Value3": 28, "Value4": 12, "OpponentName": "Macdonald and his Homemade Maccies",
            "RewardID": summoningRewards[15], "Value8": 48, "Image": "maccie",
        },
        2: {
            "EnemyID": "w5a3", "Value2": 43, "Value3": 36, "Value4": 29, "OpponentName": "Brandon and his Iconic Brightsides",
            "RewardID": summoningRewards[1], "Value8": 53, "Image": "mister-brightside",
        },
        3: {
            "EnemyID": "w5a4", "Value2": 30, "Value3": 27, "Value4": 18, "OpponentName": "Lola and her Crazy Crackers",
            "RewardID": summoningRewards[5], "Value8": 55, "Image": "cheese-nub",
        },
        4: {
            "EnemyID": "w5a5", "Value2": 32, "Value3": 32, "Value4": 28, "OpponentName": "Mr M and his Holey Moleys",
            "RewardID": summoningRewards[11], "Value8": 57, "Image": "stiltmole",
        },
        5: {
            "EnemyID": "w5b1", "Value2": 20, "Value3": 27, "Value4": 11, "OpponentName": "The Don's Molto Bene Moltis",
            "RewardID": summoningRewards[16], "Value8": 59, "Image": "molti",
        },
        6: {
            "EnemyID": "w5b2", "Value2": 22, "Value3": 27, "Value4": 18, "OpponentName": "Smoggy Shaman and their Scary Bones",
            "RewardID": summoningRewards[7], "Value8": 63, "Image": "purgatory-stalker",
        },
        7: {
            "EnemyID": "w5b3", "Value2": 23, "Value3": 24, "Value4": 18, "OpponentName": "Thomas and his Halftime Breakforce",
            "RewardID": summoningRewards[18], "Value8": 69, "Image": "citringe",
        },
        8: {
            "EnemyID": "w5b4", "Value2": 28, "Value3": 30, "Value4": 24, "OpponentName": "Larry and his Lava Lamps",
            "RewardID": summoningRewards[9], "Value8": 71, "Image": "lampar",
        },
        9: {
            "EnemyID": "w5b5", "Value2": 31, "Value3": 31, "Value4": 28, "OpponentName": "OwO and their Spirit Army",
            "RewardID": summoningRewards[3], "Value8": 75, "Image": "fire-spirit",
        },
        10: {
            "EnemyID": "w5b6", "Value2": 34, "Value3": 37, "Value4": 23, "OpponentName": "Briggs and his Mole Workforce",
            "RewardID": summoningRewards[6], "Value8": 79, "Image": "biggole-mole",
        },
        11: {
            "EnemyID": "w5c1", "Value2": 21, "Value3": 22, "Value4": 11, "OpponentName": "Krepe and his Crawlies",
            "RewardID": summoningRewards[4], "Value8": 82, "Image": "crawler",
        },
        12: {
            "EnemyID": "w5c2", "Value2": 34, "Value3": 25, "Value4": 22, "OpponentName": "Grinder23 and his Favorite Mobs",
            "RewardID": summoningRewards[10], "Value8": 84, "Image": "tremor-wurm",
        },
    },
    "Cyan": {
        0: {
            "EnemyID": "w6a1", "Value2": 22, "Value3": 25, "Value4": 16, "OpponentName": "Spiffy Jr and their Whelming Liquids",
            "RewardID": summoningRewards[19], "Value8": 58, "Image": "sprout-spirit",
        },
        1: {
            "EnemyID": "w6a2", "Value2": 27, "Value3": 34, "Value4": 19, "OpponentName": "iFarm and their 0cal Units",
            "RewardID": summoningRewards[2], "Value8": 64, "Image": "ricecake",
        },
        2: {
            "EnemyID": "w6a3", "Value2": 35, "Value3": 39, "Value4": 27, "OpponentName": "Spiffy Sr and his Bigtime Liquids",
            "RewardID": summoningRewards[8], "Value8": 67, "Image": "river-spirit",
        },
        3: {
            "EnemyID": "w6a4", "Value2": 33, "Value3": 27, "Value4": 22, "OpponentName": "Bart and his Trollsquad",
            "RewardID": summoningRewards[12], "Value8": 68, "Image": "baby-troll",
        },
        4: {
            "EnemyID": "w6a5", "Value2": 36, "Value3": 35, "Value4": 29, "OpponentName": "Grunkle and their Rooted Whimsy",
            "RewardID": summoningRewards[14], "Value8": 72, "Image": "woodlin-spirit",
        },
        5: {
            "EnemyID": "w6b1", "Value2": 46, "Value3": 36, "Value4": 34, "OpponentName": "Barb and her Overworked Blobs",
            "RewardID": summoningRewards[13], "Value8": 73, "Image": "bamboo-spirit",
        },
        6: {
            "EnemyID": "w6b2", "Value2": 25, "Value3": 29, "Value4": 22, "OpponentName": "Lumi and her Bright Lights",
            "RewardID": summoningRewards[1], "Value8": 76, "Image": "lantern-spirit",
        },
        7: {
            "EnemyID": "w6b3", "Value2": 36, "Value3": 33, "Value4": 26, "OpponentName": "Marge and her Troll Patrol",
            "RewardID": summoningRewards[16], "Value8": 77, "Image": "mama-troll",
        },
        8: {
            "EnemyID": "w6b4", "Value2": 45, "Value3": 34, "Value4": 31, "OpponentName": "Lief and his Overzealous Leeks",
            "RewardID": summoningRewards[5], "Value8": 80, "Image": "leek-spirit",
        },
        9: {
            "EnemyID": "w6c1", "Value2": 29, "Value3": 27, "Value4": 19, "OpponentName": "Seru and their Ceramic Entities",
            "RewardID": summoningRewards[15], "Value8": 81, "Image": "ceramic-spirit",
        },
        10: {
            "EnemyID": "w6c2", "Value2": 38, "Value3": 33, "Value4": 27, "OpponentName": "Mr Walker and his Untiring Doggies",
            "RewardID": summoningRewards[17], "Value8": 83, "Image": "skydoggie-spirit",
        },
        11: {
            "EnemyID": "w6d1", "Value2": 23, "Value3": 24, "Value4": 14, "OpponentName": "Duke of Yolk and his Subjects",
            "RewardID": summoningRewards[3], "Value8": 85, "Image": "royal-egg",
        },
        12: {
            "EnemyID": "w6d2", "Value2": 27, "Value3": 31, "Value4": 16, "OpponentName": "Sorel and her Esteemed Sludge",
            "RewardID": summoningRewards[18], "Value8": 86, "Image": "minichief-spirit",
        },
        13: {
            "EnemyID": "w6d3", "Value2": 42, "Value3": 41, "Value4": 32, "OpponentName": "Shinji and his Inevitable Army",
            "RewardID": summoningRewards[20], "Value8": 87, "Image": "samurai-guardian",
        },
    },
}

summoningBattleCountsDict = {
    k: len(v)
    for k, v in summoningDict.items()
    # len(summoningDict["White"]),
    # len(summoningDict["Green"]),
    # len(summoningDict["Yellow"]),
    # len(summoningDict["Blue"]),
    # len(summoningDict["Purple"]),
    # len(summoningDict["Red"]),
    # len(summoningDict["Cyan"]),
}
summoningBattleCountsDict["All"] = sum(summoningBattleCountsDict.values())

### SLAB CONSTS ###
#slabString last pulled from code in 2.08
slabList = "Copper Iron Gold Plat Dementia Void Lustre Starfire Marble Dreadlo Godshard CopperBar IronBar GoldBar PlatBar DementiaBar VoidBar LustreBar StarfireBar MarbleBar DreadloBar GodshardBar OakTree BirchTree JungleTree ForestTree ToiletTree PalmTree StumpTree SaharanFoal Tree7 AlienTree Tree8 Tree9 Tree11 Tree10 Tree12 Tree13 Leaf1 Leaf2 Leaf3 Leaf4 Leaf5 Leaf6 Fish1 Fish2 Fish3 Fish4 Fish5 Fish6 Fish7 Fish8 Fish9 Fish10 Fish11 Fish12 Fish13 Bug1 Bug2 Bug3 Bug4 Bug5 Bug6 Bug7 Bug8 Bug9 Bug11 Bug10 Bug12 Bug13 Critter1 Critter1A Critter2 Critter2A Critter3 Critter3A Critter4 Critter4A Critter5 Critter5A Critter6 Critter6A Critter7 Critter7A Critter8 Critter8A Critter9 Critter9A Critter10 Critter10A Critter11 Critter11A Soul1 Soul2 Soul3 Soul4 Soul5 Soul6 Soul7 Refinery1 Refinery2 Refinery3 Refinery4 Refinery5 Refinery6 CraftMat1 CraftMat2 CraftMat3 CraftMat5 CraftMat6 CraftMat7 CraftMat9 CraftMat8 CraftMat10 CraftMat11 CraftMat12 CraftMat13 CraftMat14 OilBarrel1 OilBarrel2 OilBarrel3 OilBarrel4 OilBarrel5 OilBarrel6 OilBarrel7 PureWater PureWater2 Grasslands1 Grasslands2 Grasslands3 Grasslands4 Jungle1 Jungle2 Jungle3 Forest1 Forest2 Forest3 Sewers1 Sewers1b Sewers2 Sewers3 TreeInterior1 TreeInterior1b TreeInterior2 DesertA1 DesertA1b DesertA2 DesertA3 DesertA3b DesertB1 DesertB2 DesertB3 DesertB4 DesertC1 DesertC2 DesertC2b DesertC3 DesertC4 SnowA1 SnowA2 SnowA2a SnowA3 SnowA4 SnowB1 SnowB2 SnowB2a SnowB5 SnowB3 SnowB4 SnowC1 SnowC2 SnowC3 SnowC4 SnowC4a SnowC5 GalaxyA1 GalaxyA2 GalaxyA2b GalaxyA3 GalaxyA4 GalaxyB1 GalaxyB2 GalaxyB3 GalaxyB4 GalaxyB5 GalaxyC1 GalaxyC1b GalaxyC2 GalaxyC3 GalaxyC4 LavaA1 LavaA1b LavaA2 LavaA3 LavaA4 LavaA5 LavaA5b LavaB1 LavaB2 LavaB3 LavaB3b LavaB4 LavaB5 LavaB6 LavaC1 LavaC2 SpiA1 SpiA2 SpiA2b SpiA3 SpiA4 SpiA5 SpiB1 SpiB2 SpiB2b SpiB3 SpiB4 SpiC1 SpiC2 SpiD1 SpiD2 SpiD3 BabaYagaETC Hgg Quest17 Quest29 EfauntDrop1 EfauntDrop2 Chiz0 Chiz1 TrollPart KrukPart KrukPart2 EquipmentHats11 EquipmentHats12 EquipmentHats13 EquipmentHats14 EquipmentHats1 EquipmentHats15 EquipmentHats17 EquipmentHats20 EquipmentHats3 EquipmentHats16 EquipmentHats21 EquipmentHats18 EquipmentHats22 EquipmentHats28 EquipmentHats19 TestObj13 EquipmentHats41 EquipmentHats26 EquipmentHats52 EquipmentHats53 EquipmentHats54 EquipmentHats61 EquipmentHats58 EquipmentHats59 EquipmentHats60 EquipmentHats68 EquipmentHats70 EquipmentHats71 EquipmentHats74 EquipmentHats77 EquipmentHats83 EquipmentHats105 EquipmentHats106 EquipmentHats5 EquipmentHats6 EquipmentHats7 EquipmentHats8 EquipmentHats9 EquipmentHats10 EquipmentHats4Choppin EquipmentHats25 EquipmentHats107 EquipmentHats29 EquipmentHats39 EquipmentHats27 EquipmentHats30 EquipmentHats44 EquipmentHats2 EquipmentHats67 EquipmentHats64 EquipmentHats66 EquipmentHats79 EquipmentHats73 EquipmentHats51 EquipmentHats56 EquipmentHats63 EquipmentHats85 EquipmentHats86 EquipmentHats87 EquipmentHats88 EquipmentHats42 EquipmentHats69 EquipmentHats108 EquipmentHats55 EquipmentHats75 EquipmentHats76 EquipmentHats65 EquipmentHats80 EquipmentHats81 EquipmentHats78 EquipmentHats90 EquipmentHats91 EquipmentHats92 EquipmentHats93 EquipmentHats94 EquipmentHats95 EquipmentHats96 EquipmentHats97 EquipmentHats98 EquipmentHats99 EquipmentHats100 EquipmentHats101 EquipmentHats102 EquipmentHats103 EquipmentHats104 EquipmentPunching1 EquipmentPunching2 EquipmentPunching3 EquipmentPunching4 EquipmentPunching5 EquipmentPunching6 EquipmentPunching7 EquipmentPunching8 EquipmentPunching9 EquipmentPunching10 EquipmentPunching11 TestObj1 TestObj7 TestObj3 EquipmentSword1 EquipmentSword2 EquipmentSword3 EquipmentSword4 EquipmentSword5 EquipmentSword6 EquipmentSword7 EquipmentSword8 EquipmentSword9 EquipmentBows1 EquipmentBows3 EquipmentBows4 EquipmentBows5 EquipmentBows6 EquipmentBows7 EquipmentBows8 EquipmentBows9 EquipmentBows10 EquipmentBows11 EquipmentBows12 EquipmentBows13 EquipmentBows14 EquipmentWands1 EquipmentWands2 EquipmentWands5 EquipmentWands6 EquipmentWands3 EquipmentWands7 EquipmentWands8 EquipmentWands9 EquipmentWands10 EquipmentWands11 EquipmentWands12 EquipmentWands13 EquipmentShirts1 EquipmentShirts17 EquipmentShirts19 EquipmentShirts20 EquipmentShirts24 EquipmentShirts25 EquipmentShirts2 EquipmentShirts16 EquipmentShirts3 EquipmentShirts21 EquipmentShirts10 EquipmentShirts11 EquipmentShirts12 EquipmentShirts13 EquipmentShirts18 EquipmentShirts14 EquipmentShirts5 EquipmentShirts23 EquipmentShirts22 EquipmentShirts15 EquipmentShirts26 EquipmentShirts27 EquipmentShirts31 EquipmentShirts28 EquipmentShirts29 EquipmentShirts30 EquipmentShirts6 EquipmentShirts32 EquipmentShirts33 EquipmentShirts34 EquipmentShirts35 EquipmentShirts36 EquipmentShirts37 EquipmentShirts38 EquipmentPants1 EquipmentPants2 EquipmentPants3 EquipmentPants4 EquipmentPants17 EquipmentPants5 EquipmentPants6 EquipmentPants20 EquipmentPants21 EquipmentPants10 EquipmentPants15 EquipmentPants16 EquipmentPants18 EquipmentPants19 EquipmentPants22 EquipmentPants23 EquipmentPants9 EquipmentPants24 EquipmentPants25 EquipmentPants8 EquipmentPants26 EquipmentPants27 EquipmentPants29 EquipmentPants30 EquipmentShoes1 EquipmentShoes9 EquipmentShoes15 EquipmentShoes3 EquipmentShoes20 EquipmentShoes4 EquipmentShoes5 EquipmentShoes21 EquipmentShoes22 EquipmentShoes7 EquipmentShoes16 EquipmentShoes17 EquipmentShoes18 EquipmentShoes19 EquipmentShoes2 EquipmentShoes23 EquipmentShoes26 EquipmentShoes27 EquipmentShoes28 EquipmentShoes29 EquipmentShoes30 EquipmentShoes31 EquipmentShoes32 EquipmentShoes33 EquipmentShoes39 EquipmentShoes24 EquipmentShoes25 EquipmentShoes34 EquipmentShoes35 EquipmentShoes36 EquipmentShoes37 EquipmentShoes38 EquipmentPendant9 EquipmentPendant10 EquipmentPendant11 EquipmentPendant12 EquipmentPendant14 EquipmentPendant16 EquipmentPendant17 EquipmentPendant18 EquipmentPendant19 EquipmentPendant20 EquipmentPendant21 EquipmentPendant22 EquipmentPendant23 EquipmentPendant24 EquipmentPendant25 EquipmentPendant26 EquipmentPendant27 EquipmentPendant28 EquipmentPendant31 EquipmentPendant29 EquipmentPendant30 EquipmentRings2 EquipmentRings3 EquipmentRings6 EquipmentRings7 EquipmentRings11 EquipmentRings12 EquipmentRings13 EquipmentRings14 EquipmentRings15 EquipmentRings16 EquipmentRings21 EquipmentRings20 EquipmentRings19 EquipmentRingsFishing1 EquipmentRingsFishing2 EquipmentRingsFishing3 EquipmentRings22 EquipmentRings18 EquipmentRings36 EquipmentRings23 EquipmentRings24 EquipmentRings25 EquipmentRings26 EquipmentRings27 EquipmentRings28 EquipmentRings29 EquipmentRings35 EquipmentRings30 EquipmentRings33 EquipmentRings31 EquipmentRings32 EquipmentRings34 EquipmentRingsChat10 EquipmentCape0 EquipmentCape2 EquipmentCape3 EquipmentCape4 EquipmentCape5 EquipmentCape6 EquipmentCape7 EquipmentCape8 EquipmentCape9 EquipmentCape10 EquipmentCape11 EquipmentCape12 EquipmentCape13 EquipmentCape14 EquipmentKeychain0 EquipmentKeychain1 EquipmentKeychain2 EquipmentKeychain3 EquipmentKeychain4 EquipmentKeychain5 EquipmentKeychain6 EquipmentKeychain7 EquipmentKeychain8 EquipmentKeychain9 EquipmentKeychain10 EquipmentKeychain11 EquipmentKeychain12 EquipmentKeychain13 EquipmentKeychain14 EquipmentKeychain15 EquipmentKeychain16 EquipmentKeychain17 EquipmentKeychain18 EquipmentKeychain19 EquipmentKeychain20 EquipmentKeychain21 EquipmentKeychain22 EquipmentKeychain23 EquipmentKeychain24 EquipmentKeychain25 EquipmentKeychain26 EquipmentKeychain27 EquipmentKeychain28 EquipmentKeychain29 Trophy1 Trophy2 Trophy3 Trophy5 Trophy6 Trophy7 Trophy8 Trophy9 Trophy10 Trophy11 Trophy12 Trophy13 Trophy14 Trophy15 Trophy16 Trophy17 Trophy18 Trophy19 Trophy20 Trophy21 Trophy22 EquipmentNametag1 EquipmentNametag3 EquipmentNametag4 EquipmentNametag5 EquipmentNametag6b EquipmentNametag7 EquipmentNametag8 EquipmentNametag9 EquipmentNametag10 EquipmentTools1 EquipmentTools2 EquipmentTools3 EquipmentTools5 EquipmentTools6 EquipmentTools7 EquipmentTools11 EquipmentTools8 EquipmentTools12 EquipmentTools9 EquipmentTools14 EquipmentTools15 EquipmentTools10 EquipmentTools13 EquipmentToolsHatchet0 EquipmentToolsHatchet3 EquipmentToolsHatchet1 EquipmentToolsHatchet2b EquipmentToolsHatchet2 EquipmentToolsHatchet4 EquipmentToolsHatchet5 EquipmentToolsHatchet7 EquipmentToolsHatchet6 EquipmentToolsHatchet8 EquipmentToolsHatchet9 EquipmentToolsHatchet12 EquipmentToolsHatchet10 EquipmentToolsHatchet11 FishingRod2 FishingRod3 FishingRod4 FishingRod5 FishingRod6 FishingRod7 FishingRod8 FishingRod9 FishingRod10 FishingRod11 FishingRod12 CatchingNet2 CatchingNet3 CatchingNet4 CatchingNet5 CatchingNet6 CatchingNet7 CatchingNet8 CatchingNet9 CatchingNet10 CatchingNet11 CatchingNet12 TrapBoxSet1 TrapBoxSet2 TrapBoxSet3 TrapBoxSet4 TrapBoxSet5 TrapBoxSet6 TrapBoxSet7 TrapBoxSet8 TrapBoxSet9 TrapBoxSet10 WorshipSkull1 WorshipSkull2 WorshipSkull3 WorshipSkull4 WorshipSkull5 WorshipSkull6 WorshipSkull7 WorshipSkull8 WorshipSkull9 WorshipSkull10 WorshipSkull11 DNAgun0 DNAgun1 DNAgun2 DNAgun3 FoodHealth1 FoodHealth3 FoodHealth2 Peanut FoodHealth4 FoodHealth6 FoodHealth7 FoodHealth10 FoodHealth9 FoodHealth11 FoodHealth13 FoodHealth12 FoodHealth14 FoodHealth15 FoodHealth16 FoodHealth17 FoodHealth5 FoodEvent8 Meatloaf FoodPotOr1 FoodPotOr2 FoodPotOr3 FoodPotOr4 FoodPotRe1 FoodPotRe2 FoodPotRe3 FoodPotRe4 FoodPotGr1 FoodPotGr2 FoodPotGr3 FoodPotGr4 FoodEvent7 FoodPotMana1 FoodPotMana2 FoodPotMana3 FoodPotMana4 FoodPotYe1 FoodPotYe2 FoodPotYe3 FoodPotYe4 FoodPotYe5 FoodEvent6 Pearl3 FoodMining1 FoodEvent1 Pearl2 FoodChoppin1 FoodEvent2 FoodFish1 FoodEvent3 Pearl1 FoodCatch1 FoodEvent4 FoodTrapping1 FoodWorship1 Bullet BulletB Bullet3 MidnightCookie FoodEvent5 PeanutG FoodG1 FoodG2 FoodG3 FoodG4 FoodG5 FoodG6 FoodG7 FoodG8 FoodG9 FoodG10 FoodG11 FoodG12 FoodG13 ButterBar rtt0 ResetFrag ResetCompleted ResetCompletedS ClassSwap ClassSwapB ResetBox Ht StonePremRestore StonePremStatswap Key1 Key2 Key3 Key4 Key5 TixCol SilverPen PremiumGem TalentPoint1 TalentPoint2 TalentPoint3 TalentPoint4 TalentPoint5 TalentPoint6 Gfoodcoupon ItemsCoupon1 ItemsCoupon2 ExpBalloon1 ExpBalloon2 ExpBalloon3 Pearl4 Pearl6 Pearl5 Quest30 Quest35 Quest36 Quest38 Quest39 Quest40 Quest42 Quest43 Quest44 Quest49 Quest50 Quest70 Quest71 Quest72 Quest73 Quest75 Quest85 Quest76 Quest77 Quest79 Quest80 GemP30 Quest81 Quest82 Timecandy1 Timecandy2 Timecandy3 Timecandy4 Timecandy5 Timecandy6 Timecandy7 Timecandy8 Timecandy9 StoneWe StoneWeb StoneW1 StoneW2 StoneW3 StoneW3b StoneW6 StoneW4 StoneW5 StoneW7 StoneW8 StoneAe StoneAeB StoneA1 StoneA1b StoneA2 StoneA2b StoneA3 StoneA3b StoneA4 StoneA5 StoneA6 StoneA7 StoneTe StoneT1 StoneT1e StoneT1eb StoneT2 StoneT3 StoneT4 StoneT5 StoneT6 StoneT7 StoneHelm1 StoneHelm6 StoneHelm1b StoneHelm7 StoneZ1 StoneZ2 StoneZ3 StoneZ4 StonePremSTR StonePremAGI StonePremWIS StonePremLUK JobApplication SmithingHammerChisel SmithingHammerChisel2 SmithingHammerChisel3 BobJoePickle BallJoePickle BoneJoePickle Quest1 Crystal1 Crystal2 Crystal3 Crystal4 Crystal5 PeanutS Quest3 Quest4 Mayo Trash Trash2 Trash3 Quest5 Quest6 Quest7 Quest10 Quest11 Quest12 Quest13 Quest14 Quest15 Quest16 Quest18 Quest19 Quest20 Quest21 Quest22 Quest23 Quest24 Quest25 Quest26 Quest27 GoldricP1 GoldricP2 GoldricP3 Cutter Quest32 Quest33 Quest34 Quest37 Quest41 Quest45 Quest46 Quest47 Quest48 Quest51 Quest52 PalmTreeD Quest53 Quest54 Quest55 Quest56 Quest57 Quest58 Quest59 Quest60 Quest61 Quest62 Quest63 Quest64 Quest65 Quest66 Quest67 Whetstone Quest68 Quest69 Quest74 Quest78 Quest83 Quest84 BadgeG1 BadgeG2 BadgeG3 BadgeD1 BadgeD2 BadgeD3 NPCtoken1 NPCtoken2 NPCtoken3 NPCtoken5 NPCtoken6 NPCtoken4 NPCtoken9 NPCtoken10 NPCtoken11 NPCtoken13 NPCtoken7 Quest9 NPCtoken15 NPCtoken12 NPCtoken14 NPCtoken16 NPCtoken17 NPCtoken18 NPCtoken19 NPCtoken20 NPCtoken21 NPCtoken27 NPCtoken22 NPCtoken24 NPCtoken25 NPCtoken26 NPCtoken23 NPCtoken28 NPCtoken29 NPCtoken30 NPCtoken31 NPCtoken32 NPCtoken33 NPCtoken34 NPCtoken35 NPCtoken36 NPCtoken37 NPCtoken38 NPCtoken39 NPCtoken40 NPCtoken41 BadgeI1 BadgeI2 BadgeI3 EquipmentStatues1 EquipmentStatues2 EquipmentStatues3 EquipmentStatues4 EquipmentStatues5 EquipmentStatues6 EquipmentStatues7 EquipmentStatues8 EquipmentStatues9 EquipmentStatues10 EquipmentStatues11 EquipmentStatues12 EquipmentStatues13 EquipmentStatues14 EquipmentStatues15 EquipmentStatues16 EquipmentStatues17 EquipmentStatues18 EquipmentStatues19 EquipmentStatues20 EquipmentStatues21 EquipmentStatues22 EquipmentStatues23 EquipmentStatues24 EquipmentStatues25 EquipmentStatues26 EquipmentStatues27 EquipmentStatues28 EquipmentSmithingTabs2 EquipmentSmithingTabs3 EquipmentSmithingTabs4 EquipmentSmithingTabs5 EquipmentSmithingTabs6 SmithingRecipes1 SmithingRecipes2 SmithingRecipes3 SmithingRecipes4 SmithingRecipes5 SmithingRecipes6 TalentBook1 TalentBook2 TalentBook3 TalentBook4 TalentBook5 MaxCapBagT2 MaxCapBag1 MaxCapBag2 MaxCapBag3 MaxCapBag4 MaxCapBag5 MaxCapBagMi6 MaxCapBagMi7 MaxCapBagMi8 MaxCapBagMi9 MaxCapBagMi10 MaxCapBagMi11 MaxCapBagT1 MaxCapBag7 MaxCapBag9 MaxCapBagT3 MaxCapBagT4 MaxCapBagT5 MaxCapBagT6 MaxCapBagT7 MaxCapBagT8 MaxCapBagT9 MaxCapBagT10 MaxCapBagT11 MaxCapBag6 MaxCapBag8 MaxCapBag10 MaxCapBagF3 MaxCapBagF4 MaxCapBagF5 MaxCapBagF6 MaxCapBagF7 MaxCapBagF8 MaxCapBagF9 MaxCapBagF10 MaxCapBagF11 MaxCapBagM1 MaxCapBagM2 MaxCapBagM3 MaxCapBagM4 MaxCapBagM5 MaxCapBagM6 MaxCapBagM7 MaxCapBagM8 MaxCapBagM9 MaxCapBagM10 MaxCapBagM11 MaxCapBagM12 MaxCapBagFi1 MaxCapBagFi2 MaxCapBagFi3 MaxCapBagFi4 MaxCapBagFi5 MaxCapBagFi6 MaxCapBagFi7 MaxCapBagFi8 MaxCapBagFi9 MaxCapBagFi10 MaxCapBagFi11 MaxCapBagB1 MaxCapBagB2 MaxCapBagB3 MaxCapBagB4 MaxCapBagB5 MaxCapBagB6 MaxCapBagB7 MaxCapBagB8 MaxCapBagB9 MaxCapBagB10 MaxCapBagB11 MaxCapBagTr1 MaxCapBagTr3 MaxCapBagTr4 MaxCapBagTr5 MaxCapBagTr6 MaxCapBagTr7 MaxCapBagTr8 MaxCapBagTr9 MaxCapBagTr10 MaxCapBagS1 MaxCapBagS3 MaxCapBagS4 MaxCapBagS5 MaxCapBagS6 MaxCapBagS7 MaxCapBagS8 MaxCapBagS9 MaxCapBagS10 ObolBronze0 ObolSilver0 ObolGold0 ObolPlatinum0 ObolPink0 ObolBronze1 ObolSilver1 ObolGold1 ObolPlatinum1 ObolPink1 ObolBronze2 ObolSilver2 ObolGold2 ObolPlatinum2 ObolPink2 ObolBronze3 ObolSilver3 ObolGold3 ObolPlatinum3 ObolPink3 ObolBronzeDamage ObolSilverDamage ObolGoldDamage ObolPlatinumDamage ObolPinkDamage ObolSilverMoney ObolGoldMoney ObolBronzeMining ObolSilverMining ObolGoldMining ObolPlatinumMining ObolPinkMining ObolBronzeChoppin ObolSilverChoppin ObolGoldChoppin ObolPlatinumChoppin ObolPinkChoppin ObolBronzeFishing ObolSilverFishing ObolGoldFishing ObolPlatinumFishing ObolPinkFishing ObolBronzeCatching ObolSilverCatching ObolGoldCatching ObolPlatinumCatching ObolPinkCatching ObolSilverLuck ObolGoldLuck ObolPlatinumLuck ObolPinkLuck ObolBronzePop ObolSilverPop ObolGoldPop ObolPlatinumPop ObolPinkPop ObolBronzeKill ObolSilverKill ObolGoldKill ObolPlatinumKill ObolPinkKill ObolBronzeEXP ObolSilverEXP ObolGoldEXP ObolPlatinumEXP ObolPinkEXP ObolBronzeCard ObolSilverCard ObolGoldCard ObolPlatinumCard ObolPinkCard ObolBronzeDef ObolSilverDef ObolGoldDef ObolPlatinumDef ObolPinkDef ObolBronzeTrapping ObolSilverTrapping ObolGoldTrapping ObolPlatinumTrapping ObolPinkTrapping ObolBronzeCons ObolSilverCons ObolGoldCons ObolPlatinumCons ObolPinkCons ObolBronzeWorship ObolSilverWorship ObolGoldWorship ObolPlatinumWorship ObolPinkWorship ObolFrog ObolAmarokA ObolEfauntA ObolKnight ObolSlush ObolChizoarA ObolTroll ObolLava ObolKruk ObolHyper0 ObolHyper1 ObolHyper2 ObolHyper3 ObolHyperB0 ObolHyperB1 ObolHyperB2 ObolHyperB3 StampA1 StampA2 StampA3 StampA4 StampA5 StampA6 StampA7 StampA8 StampA9 StampA10 StampA11 StampA12 StampA13 StampA14 StampA15 StampA16 StampA17 StampA18 StampA19 StampA20 StampA21 StampA22 StampA23 StampA24 StampA25 StampA26 StampA27 StampA28 StampA29 StampA30 StampA31 StampA32 StampA33 StampA34 StampA35 StampA36 StampA37 StampA38 StampA39 StampA40 StampA41 StampA42 StampB1 StampB2 StampB3 StampB4 StampB5 StampB6 StampB7 StampB8 StampB9 StampB10 StampB11 StampB12 StampB13 StampB14 StampB15 StampB16 StampB17 StampB18 StampB19 StampB20 StampB21 StampB22 StampB23 StampB24 StampB25 StampB26 StampB27 StampB28 StampB29 StampB30 StampB31 StampB32 StampB33 StampB34 StampB35 StampB36 StampB37 StampB38 StampB39 StampB40 StampB41 StampB42 StampB43 StampB44 StampB45 StampB46 StampB47 StampB48 StampB49 StampB50 StampB51 StampB52 StampB53 StampB54 StampC1 StampC2 StampC3 StampC4 StampC5 StampC6 StampC7 StampC8 StampC9 StampC10 StampC11 StampC12 StampC13 StampC14 StampC15 StampC16 StampC17 StampC18 StampC19 StampC20 StampC21 StampC22 StampC23 InvBag1 InvBag2 InvBag3 InvBag4 InvBag5 InvBag6 InvBag7 InvBag8 InvBag100 InvBag101 InvBag102 InvBag103 InvBag104 InvBag105 InvBag106 InvBag107 InvBag108 InvBag109 InvBag110 InvBag111 InvStorage1 InvStorage2 InvStorage3 InvStorage4 InvStorage5 InvStorage6 InvStorage7 InvStorage8 InvStorage9 InvStorage10 InvStorage11 InvStorage12 InvStorage13 InvStorage14 InvStorage15 InvStorage16 InvStorage17 InvStorage18 InvStorage19 InvStorage20 InvStorage21 InvStorage22 InvStorage23 InvStorage24 InvStorage25 InvStorage26 InvStorage27 InvStorage28 InvStorageF InvStorageS InvStorageC InvStorageD InvStorageN Weight1 Weight2 Weight3 Weight4 Weight5 Weight6 Weight7 Weight8 Weight9 Weight10 Weight11 Weight12 Weight13 Weight14 Line1 Line2 Line3 Line4 Line5 Line6 Line7 Line8 Line9 Line10 Line11 Line12 Line13 Line14 Ladle PetEgg Genetic0 Genetic1 Genetic2 Genetic3 CardPack1 CardPack2 CardPack3 CardPack4 CardPack5 CardPack6 CardPack7 DungCredits2 Cash XP XPskill DungEnhancer0 DungEnhancer1 DungEnhancer2 DungRNG0 DungRNG1 DungRNG2 DungRNG3 DungRNG4 DungeonA1 DungeonA2 DungeonA3 DungeonA4 DungeonA5 DungeonA6 DungeonA7 DungeonA8 KeyFrag DungCredits1 LootDice Tree7D PlatD Fish1D Fish3D Cashb Dung3Ice FoodHealth1d FoodHealth2d FoodHealth3d DungWeaponPunchA1 DungWeaponPunchA2 DungWeaponPunchA3 DungWeaponPunchA4 DungWeaponPunchA5 DungWeaponPunchB1 DungWeaponPunchB2 DungWeaponPunchB3 DungWeaponPunchB4 DungWeaponPunchB5 DungWeaponPunchC1 DungWeaponPunchC2 DungWeaponPunchC3 DungWeaponPunchC4 DungWeaponPunchC5 DungWeaponPunchD1 DungWeaponPunchD2 DungWeaponPunchD3 DungWeaponPunchD4 DungWeaponPunchD5 DungWeaponPunchE1 DungWeaponPunchE2 DungWeaponPunchE3 DungWeaponPunchE4 DungWeaponPunchE5 DungWeaponPunchF1 DungWeaponPunchF2 DungWeaponPunchF3 DungWeaponPunchF4 DungWeaponPunchF5 DungWeaponSwordA1 DungWeaponSwordA2 DungWeaponSwordA3 DungWeaponSwordA4 DungWeaponSwordA5 DungWeaponSwordB1 DungWeaponSwordB2 DungWeaponSwordB3 DungWeaponSwordB4 DungWeaponSwordB5 DungWeaponSwordC1 DungWeaponSwordC2 DungWeaponSwordC3 DungWeaponSwordC4 DungWeaponSwordC5 DungWeaponSwordD1 DungWeaponSwordD2 DungWeaponSwordD3 DungWeaponSwordD4 DungWeaponSwordD5 DungWeaponSwordE1 DungWeaponSwordE2 DungWeaponSwordE3 DungWeaponSwordE4 DungWeaponSwordE5 DungWeaponSwordF1 DungWeaponSwordF2 DungWeaponSwordF3 DungWeaponSwordF4 DungWeaponSwordF5 DungWeaponBowA1 DungWeaponBowA2 DungWeaponBowA3 DungWeaponBowA4 DungWeaponBowA5 DungWeaponBowB1 DungWeaponBowB2 DungWeaponBowB3 DungWeaponBowB4 DungWeaponBowB5 DungWeaponBowC1 DungWeaponBowC2 DungWeaponBowC3 DungWeaponBowC4 DungWeaponBowC5 DungWeaponBowD1 DungWeaponBowD2 DungWeaponBowD3 DungWeaponBowD4 DungWeaponBowD5 DungWeaponBowE1 DungWeaponBowE2 DungWeaponBowE3 DungWeaponBowE4 DungWeaponBowE5 DungWeaponBowF1 DungWeaponBowF2 DungWeaponBowF3 DungWeaponBowF4 DungWeaponBowF5 DungWeaponWandA1 DungWeaponWandA2 DungWeaponWandA3 DungWeaponWandA4 DungWeaponWandA5 DungWeaponWandB1 DungWeaponWandB2 DungWeaponWandB3 DungWeaponWandB4 DungWeaponWandB5 DungWeaponWandC1 DungWeaponWandC2 DungWeaponWandC3 DungWeaponWandC4 DungWeaponWandC5 DungWeaponWandD1 DungWeaponWandD2 DungWeaponWandD3 DungWeaponWandD4 DungWeaponWandD5 DungWeaponWandE1 DungWeaponWandE2 DungWeaponWandE3 DungWeaponWandE4 DungWeaponWandE5 DungWeaponWandF1 DungWeaponWandF2 DungWeaponWandF3 DungWeaponWandF4 DungWeaponWandF5 DungEquipmentHats0 DungEquipmentHats1 DungEquipmentHats2 DungEquipmentHats3 DungEquipmentHats4 DungEquipmentShirt0 DungEquipmentShirt1 DungEquipmentShirt2 DungEquipmentShirt3 DungEquipmentShirt4 DungEquipmentPants0 DungEquipmentPants1 DungEquipmentPants2 DungEquipmentPants3 DungEquipmentPants4 DungEquipmentShoes0 DungEquipmentShoes1 DungEquipmentShoes2 DungEquipmentShoes3 DungEquipmentShoes4 DungEquipmentPendant0 DungEquipmentPendant1 DungEquipmentPendant2 DungEquipmentPendant3 DungEquipmentPendant4 DungEquipmentRings0 DungEquipmentRings1 DungEquipmentRings2 DungEquipmentRings3 DungEquipmentRings4".split(' ')
knownSlabIgnorablesList = ["Mega-Rare_Drop", "Rare_Drop", "LockedInvSpace", "Blank"]
#This replacement list is needed due to a restriction for the image mapping variable names not being able to start with a Number
slab_itemNameFindList = ["Timecandy1", "Timecandy2", "Timecandy3", "Timecandy4", "Timecandy5", "Timecandy6", "EquipmentHats108", "EquipmentNametag10"]
slab_itemNameReplacementList = ["time-candy-1-hr", "time-candy-2-hr", "time-candy-4-hr", "time-candy-12-hr", "time-candy-24-hr", "time-candy-72-hr",
                                "third-anniversary-ice-cream-topper", "third-anniversary-idleon-nametag"]
dungeonDropsList = [
    "Quest51", "Quest52", "PalmTreeD", "Quest53", "Quest54", "Quest55",
    "DungCredits2", "Cash", "XP", "XPskill", "DungEnhancer0", "DungEnhancer1", "DungEnhancer2",
    "DungRNG0", "DungRNG1", "DungRNG2", "DungRNG3", "DungRNG4",
    "DungeonA1", "DungeonA2", "DungeonA3", "DungeonA4", "DungeonA5", "DungeonA6", "DungeonA7", "DungeonA8",
    "KeyFrag", "DungCredits1", "LootDice", "Tree7D", "PlatD", "Fish1D", "Fish3D", "Cashb", "Dung3Ice",
    "FoodHealth1d", "FoodHealth2d", "FoodHealth3d"
]
maxDungeonWeaponsAvailable = 23 #This is the value saved in the JSON, 0-23 = 24 total. Last verified in 2.08
dungeonWeaponsList = [
    "DungWeaponPunchA1", "DungWeaponPunchA2", "DungWeaponPunchA3", "DungWeaponPunchA4", "DungWeaponPunchA5", "DungWeaponPunchB1", "DungWeaponPunchB2", "DungWeaponPunchB3", "DungWeaponPunchB4", "DungWeaponPunchB5", "DungWeaponPunchC1", "DungWeaponPunchC2", "DungWeaponPunchC3", "DungWeaponPunchC4", "DungWeaponPunchC5", "DungWeaponPunchD1", "DungWeaponPunchD2", "DungWeaponPunchD3", "DungWeaponPunchD4", "DungWeaponPunchD5", "DungWeaponPunchE1", "DungWeaponPunchE2", "DungWeaponPunchE3", "DungWeaponPunchE4", #"DungWeaponPunchE5", "DungWeaponPunchF1", "DungWeaponPunchF2", "DungWeaponPunchF3", "DungWeaponPunchF4", "DungWeaponPunchF5",
    "DungWeaponSwordA1", "DungWeaponSwordA2", "DungWeaponSwordA3", "DungWeaponSwordA4", "DungWeaponSwordA5", "DungWeaponSwordB1", "DungWeaponSwordB2", "DungWeaponSwordB3", "DungWeaponSwordB4", "DungWeaponSwordB5", "DungWeaponSwordC1", "DungWeaponSwordC2", "DungWeaponSwordC3", "DungWeaponSwordC4", "DungWeaponSwordC5", "DungWeaponSwordD1", "DungWeaponSwordD2", "DungWeaponSwordD3", "DungWeaponSwordD4", "DungWeaponSwordD5", "DungWeaponSwordE1", "DungWeaponSwordE2", "DungWeaponSwordE3", "DungWeaponSwordE4", #"DungWeaponSwordE5", "DungWeaponSwordF1", "DungWeaponSwordF2", "DungWeaponSwordF3", "DungWeaponSwordF4", "DungWeaponSwordF5",
    "DungWeaponBowA1", "DungWeaponBowA2", "DungWeaponBowA3", "DungWeaponBowA4", "DungWeaponBowA5", "DungWeaponBowB1", "DungWeaponBowB2", "DungWeaponBowB3", "DungWeaponBowB4", "DungWeaponBowB5", "DungWeaponBowC1", "DungWeaponBowC2", "DungWeaponBowC3", "DungWeaponBowC4", "DungWeaponBowC5", "DungWeaponBowD1", "DungWeaponBowD2", "DungWeaponBowD3", "DungWeaponBowD4", "DungWeaponBowD5", "DungWeaponBowE1", "DungWeaponBowE2", "DungWeaponBowE3", "DungWeaponBowE4", #"DungWeaponBowE5", "DungWeaponBowF1", "DungWeaponBowF2", "DungWeaponBowF3", "DungWeaponBowF4", "DungWeaponBowF5",
    "DungWeaponWandA1", "DungWeaponWandA2", "DungWeaponWandA3", "DungWeaponWandA4", "DungWeaponWandA5", "DungWeaponWandB1", "DungWeaponWandB2", "DungWeaponWandB3", "DungWeaponWandB4", "DungWeaponWandB5", "DungWeaponWandC1", "DungWeaponWandC2", "DungWeaponWandC3", "DungWeaponWandC4", "DungWeaponWandC5", "DungWeaponWandD1", "DungWeaponWandD2", "DungWeaponWandD3", "DungWeaponWandD4", "DungWeaponWandD5", "DungWeaponWandE1", "DungWeaponWandE2", "DungWeaponWandE3", "DungWeaponWandE4", #"DungWeaponWandE5", "DungWeaponWandF1", "DungWeaponWandF2", "DungWeaponWandF3", "DungWeaponWandF4", #"DungWeaponWandF5",
]
maxDungeonArmorsAvailable = 3  #This is the value saved in the JSON, 0-3 = 4 total. Last verified in 2.08
dungeonArmorsList = [
    "DungEquipmentHats0", "DungEquipmentHats1", "DungEquipmentHats2", "DungEquipmentHats3", #"DungEquipmentHats4",
    "DungEquipmentShirt0", "DungEquipmentShirt1", "DungEquipmentShirt2", "DungEquipmentShirt3", #"DungEquipmentShirt4",
    "DungEquipmentPants0", "DungEquipmentPants1", "DungEquipmentPants2", "DungEquipmentPants3", #"DungEquipmentPants4",
    "DungEquipmentShoes0", "DungEquipmentShoes1", "DungEquipmentShoes2", "DungEquipmentShoes3", #"DungEquipmentShoes4",
] #This list was pulled from the items.yaml file
maxDungeonJewelryAvailable = 3   #This is the value saved in the JSON, 0-3 = 4 total. Last verified in 2.08
dungeonJewelryList = [
    "DungEquipmentPendant0", "DungEquipmentPendant1", "DungEquipmentPendant2", "DungEquipmentPendant3", #"DungEquipmentPendant4",
    "DungEquipmentRings0", "DungEquipmentRings1", "DungEquipmentRings2", "DungEquipmentRings3", #"DungEquipmentRings4",
] #This list was pulled from the items.yaml file

reclaimableQuestItems = {
    "CraftMat2": {
        "ItemName": "Crimson String",
        "QuestGiver": "Scripticus",
        "QuestName": "Hardcore Gamer Status, Here I Come!",
        "QuestNameCoded": "Scripticus2"
    },
    "Quest1": {
        "ItemName": "Mining Certificate",
        "QuestGiver": "Glumlee",
        "QuestName": "Literally Burning Your Money",
        "QuestNameCoded": "Glumlee3"
    },
    "Quest5": {
        "ItemName": "Class Certificate",
        "QuestGiver": "Promotheus",
        "QuestName": "Three Right Answers",
        "QuestNameCoded": "Promotheus2"
    },
    "InvBag4": {
        "ItemName": "Inventory Bag D",
        "QuestGiver": "Promotheus",
        "QuestName": "The Witcher, But Not Really",
        "QuestNameCoded": "Promotheus4"
    },
    "Quest6": {
        "ItemName": "Scouting Report",
        "QuestGiver": "Stiltzcho",
        "QuestName": "Investigator By Day, Prankster By Night",
        "QuestNameCoded": "Stiltzcho3"
    },
    "Quest20": {
        "ItemName": "Signed Arrest Warrant",
        "QuestGiver": "Bandit Bob",
        "QuestName": "Bringing Bob's Boxes",
        "QuestNameCoded": "Bandit_Bob3"
    },
    "Quest27": {
        "ItemName": "Bag o' Nuts",
        "QuestGiver": "Goldric",
        "QuestName": "Dress To Impress",
        "QuestNameCoded": "Goldric5"
    },
    "Trophy13": {
        "ItemName": "Club Maestro",
        "QuestGiver": "Cactolyte",
        "QuestName": "Maestro! The Stro! Mman!",
        "QuestNameCoded": "Cactolyte4"
    },
    "Quest59": {
        "ItemName": "Shuvelle's Vote",
        "QuestGiver": "Shuvelle",
        "QuestName": "Mayoral Movie Taste",
        "QuestNameCoded": "Shuvelle4"
    },
    "Quest60": {
        "ItemName": "Yondergreens Vote",
        "QuestGiver": "Yondergreen",
        "QuestName": "Legislative Action",
        "QuestNameCoded": "Yondergreen4"
    },
    "Quest61": {
        "ItemName": "Bill Brr's Vote",
        "QuestGiver": "Bill Brr",
        "QuestName": "Coin Shenanigans",
        "QuestNameCoded": "Bill_Brr4"
    },
    "SmithingHammerChisel3": {
        "ItemName": "Onyx Tools",
        "QuestGiver": "Monolith",
        "QuestName": "Onyx Statue Crafting",
        "QuestNameCoded": "Monolith2"
    },
    "EquipmentNametag4": {
        "ItemName": "Vman Nametag",
        "QuestGiver": "Nebulyte",
        "QuestName": "VMAN ACHIEVED!",
        "QuestNameCoded": "Nebulyte4"
    }
}
#vendorItems last pulled from code in 2.08. Search for: ShopNames = function ()
vendorItems = {
    "W1 Town": "FoodHealth1 FoodHealth3 FoodHealth2 CraftMat3 FoodPotMana1 FoodPotOr1 FoodPotRe1 FoodPotGr1 OilBarrel1 StoneW1 StoneA1 StoneT1 EquipmentRings7 EquipmentStatues1 SmithingHammerChisel StampA5 StampA6 StampA3 InvBag104 InvStorage2 InvStorage6 InvStorage7 Quest86 rtt0 ResetFrag".split(' '),
    "Tiki Shop": "FoodHealth3 FoodHealth2 FoodHealth5 FoodPotOr2 FoodPotYe1 StoneA2 StampA12 EquipmentPendant12 Quest37 InvBag105 InvStorage8 InvStorage12 rtt0 ResetFrag".split(' '),
    "W2 Town": "FoodHealth6 FoodHealth7 FoodHealth4 Quest19 BobJoePickle StoneW2 StoneA2 StoneT2 FoodPotOr2 FoodPotGr2 FoodPotRe2 InvBag106 InvStorage9 InvStorage10 InvStorage13 InvStorage15 SmithingHammerChisel2 StampC11 rtt0 ResetFrag".split(' '),
    "Faraway Piers": "Line1 Weight1 Line5 Weight5 Weight10 Line10 Weight11 StoneT1 StoneT2 StampB8 StampA15 NPCtoken27 ResetFrag".split(' '),
    "W3 Town": "FoodHealth10 FoodHealth9 FoodHealth11 TrapBoxSet1 WorshipSkull1 StoneW3 StoneA3 StoneT3 FoodPotOr3 FoodPotGr3 FoodPotRe3 InvBag107 InvStorage16 InvStorage17 InvStorage18 InvStorage19 InvStorage20 InvStorage21 rtt0 ResetFrag Quest57 Quest67 Whetstone".split(' '),
    "W4 Town": "Quest65 Quest66 FoodHealth13 FoodHealth12 DNAgun0 StoneW4 StoneA4 StoneT4 FoodPotOr4 FoodPotGr4 FoodPotRe4 FoodPotYe4 InvBag108 StampB41 StampB38 StampC12 Quest83".split(' '),
    "W5 Town": "FoodHealth14 FoodHealth15 OilBarrel6 StoneW5 StoneA5 StoneT5 StampC22 Quest84".split(' '),
    "W6 Town": "BoneJoePickle Quest80 FoodHealth16 FoodHealth17 OilBarrel7 StoneW8 StoneA7 StoneT7 StampC10 InvStorage26 InvStorage27 InvStorage28".split(' ')}
vendors = {
    "W2 Town": "Crystal1",
    "Faraway Piers": "Crystal1",
    "W3 Town": "Crystal2",
    "W4 Town": "Crystal3",
    "W5 Town": "Crystal4",
    "W6 Town": "Crystal5"
}
#anvilItems last pulled from code in 2.08. Search for: ItemToCraftNAME = function ()
anvilItems = {
    "Anvil Tab I": "EquipmentPunching1 TestObj1 EquipmentBows1 EquipmentWands1 EquipmentHats1 EquipmentShirts1 EquipmentPants1 EquipmentShoes9 EquipmentTools2 MaxCapBag1 EquipmentToolsHatchet3 MaxCapBag7 EquipmentHats15 EquipmentPunching2 MaxCapBag8 MaxCapBagM2 EquipmentHats17 EquipmentShirts11 EquipmentPants2 EquipmentShoes1 EquipmentHats20 EquipmentHats3 EquipmentHats16 EquipmentHats21 TestObj7 EquipmentBows3 EquipmentWands2 EquipmentRings2 EquipmentTools3 MaxCapBag2 EquipmentToolsHatchet1 MaxCapBag9 EquipmentHats18 EquipmentShirts12 EquipmentPants3 EquipmentSmithingTabs2 EquipmentShirts2 EquipmentPendant10 EquipmentShoes15 EquipmentRings3 EquipmentHats8 FoodMining1 FoodChoppin1 EquipmentShoes7 EquipmentShirts10 EquipmentShirts20 OilBarrel5 EquipmentRings14 EquipmentPants15 EquipmentPants18 Peanut PeanutG InvBag102 EquipmentShirts25 EquipmentShirts24 EquipmentShirts3 BadgeG1 BadgeG2 BadgeG3 EquipmentHats67 NPCtoken1 NPCtoken2 NPCtoken3 EquipmentRings26 EquipmentHats22 EquipmentShirts18 EquipmentPants17 EquipmentShoes20 EquipmentPants22 EquipmentPants23 FillerMaterial EquipmentPendant17 FishingRod2 MaxCapBagFi1 CatchingNet2 MaxCapBagB1 FishingRod3 MaxCapBagFi2 CatchingNet3 MaxCapBagB2 TrapBoxSet2 MaxCapBagTr1 WorshipSkull2 MaxCapBagS1".split(" "),
    "Anvil Tab II": "EquipmentHats28 EquipmentShirts13 EquipmentPants4 EquipmentShoes3 EquipmentPunching3 TestObj3 EquipmentBows5 EquipmentWands5 EquipmentTools5 MaxCapBag3 EquipmentToolsHatchet2 MaxCapBagT3 FishingRod4 MaxCapBagFi3 CatchingNet4 MaxCapBagB3 EquipmentRings11 EquipmentPendant16 MaxCapBagF3 MaxCapBagM4 EquipmentHats19 EquipmentShirts14 EquipmentPants5 EquipmentShoes4 EquipmentPendant26 EquipmentSword1 EquipmentBows6 EquipmentWands6 EquipmentTools6 MaxCapBag4 EquipmentToolsHatchet4 MaxCapBagT4 FishingRod5 MaxCapBagFi4 CatchingNet5 MaxCapBagB4 MaxCapBagF4 MaxCapBagM5 FillerMaterial EquipmentSmithingTabs3 Quest13 Quest35 Bullet BulletB EquipmentHats64 TestObj13 EquipmentHats41 EquipmentHats26 FillerMaterial EquipmentShirts5 EquipmentShirts23 EquipmentShirts22 EquipmentShoes16 EquipmentShoes18 EquipmentShoes19 EquipmentShoes17 FoodFish1 FoodCatch1 Quest36 InvBag103 EquipmentHats52 EquipmentShirts26 EquipmentPants20 EquipmentShoes21 EquipmentRings16 EquipmentRings27 EquipmentPendant27 FillerMaterial TrapBoxSet3 MaxCapBagTr3 WorshipSkull3 MaxCapBagS3 BadgeD1 BadgeD2 BadgeD3 ResetCompletedS NPCtoken28 NPCtoken29 NPCtoken30 FillerMaterial".split(" "),
    "Anvil Tab III": "EquipmentHats53 EquipmentShirts15 EquipmentPants6 EquipmentShoes5 EquipmentPunching4 EquipmentSword2 EquipmentBows7 EquipmentWands3 EquipmentTools7 MaxCapBag5 EquipmentToolsHatchet5 MaxCapBagT5 FishingRod6 MaxCapBagFi5 CatchingNet6 MaxCapBagB5 TrapBoxSet4 MaxCapBagTr4 WorshipSkull4 MaxCapBagS4 EquipmentRings28 EquipmentRings29 MaxCapBagF5 MaxCapBagM6 EquipmentHats54 EquipmentShirts27 EquipmentPants21 EquipmentShoes22 EquipmentPunching5 EquipmentSword3 EquipmentBows8 EquipmentWands7 EquipmentTools11 MaxCapBagMi6 EquipmentToolsHatchet7 MaxCapBagT6 FishingRod7 MaxCapBagFi6 CatchingNet7 MaxCapBagB6 TrapBoxSet5 MaxCapBagTr5 WorshipSkull5 MaxCapBagS5 MaxCapBagF6 MaxCapBagM7 Trophy20 EquipmentSmithingTabs4 EquipmentHats61 EquipmentHats58 EquipmentHats59 EquipmentHats60 EquipmentShirts31 EquipmentShirts28 EquipmentShirts29 EquipmentShirts30 FoodTrapping1 FoodWorship1 InvBag109 EquipmentHats66 BadgeI1 BadgeI2 BadgeI3 Quest68 NPCtoken39 NPCtoken40 NPCtoken41 EquipmentPendant25 EquipmentHats68 EquipmentShirts6 EquipmentPants9 EquipmentShoes23".split(" "),
    "Anvil Tab IV": "EquipmentHats70 EquipmentShirts32 EquipmentPants24 EquipmentShoes24 EquipmentPunching6 EquipmentSword4 EquipmentBows9 EquipmentWands8 EquipmentTools8 MaxCapBagMi7 EquipmentToolsHatchet6 MaxCapBagT7 FishingRod8 MaxCapBagFi7 CatchingNet8 MaxCapBagB7 TrapBoxSet6 MaxCapBagTr6 WorshipSkull6 MaxCapBagS6 EquipmentShoes26 EquipmentShoes27 EquipmentShoes28 EquipmentShoes29 EquipmentShoes31 EquipmentShoes33 MaxCapBagF7 MaxCapBagM8 EquipmentHats71 EquipmentShirts33 EquipmentPants25 EquipmentShoes25 EquipmentPunching7 EquipmentSword5 EquipmentBows10 EquipmentWands9 EquipmentTools12 MaxCapBagMi8 EquipmentToolsHatchet8 MaxCapBagT8 FishingRod9 MaxCapBagFi8 CatchingNet9 MaxCapBagB8 TrapBoxSet7 MaxCapBagTr7 WorshipSkull7 MaxCapBagS7 MaxCapBagF8 MaxCapBagM9 FillerMaterial EquipmentSmithingTabs5 InvBag111 DNAgun1 DNAgun2 DNAgun3 EquipmentRings30 FillerMaterial FillerMaterial FillerMaterial EquipmentHats74 EquipmentShirts34 EquipmentPants8 EquipmentShoes34".split(" "),
    "Anvil Tab V": "EquipmentHats77 EquipmentShirts35 EquipmentPants26 EquipmentShoes35 EquipmentPunching8 EquipmentSword6 EquipmentBows11 EquipmentWands10 EquipmentTools9 MaxCapBagMi9 EquipmentToolsHatchet9 MaxCapBagT9 FishingRod10 MaxCapBagFi9 CatchingNet10 MaxCapBagB9 TrapBoxSet8 MaxCapBagTr8 WorshipSkull9 MaxCapBagS8 MaxCapBagF9 MaxCapBagM10 Bullet3 EquipmentSmithingTabs6 EquipmentHats83 EquipmentShirts36 EquipmentPants27 EquipmentShoes36 EquipmentPunching9 EquipmentSword7 EquipmentBows12 EquipmentWands11 EquipmentPendant30 EquipmentHats107 EquipmentShoes39 EquipmentRings35".split(" "),
    "Anvil Tab VI": "EquipmentHats105 EquipmentShirts37 EquipmentPants29 EquipmentShoes37 EquipmentPunching10 EquipmentSword8 EquipmentBows13 EquipmentWands12 EquipmentTools14 MaxCapBagMi10 EquipmentToolsHatchet12 MaxCapBagT10 FishingRod11 MaxCapBagFi10 CatchingNet11 MaxCapBagB10 TrapBoxSet9 MaxCapBagTr9 WorshipSkull10 MaxCapBagS9 MaxCapBagF10 MaxCapBagM11 EquipmentRings36 FillerMaterial EquipmentHats106 EquipmentShirts38 EquipmentPants30 EquipmentShoes38 EquipmentPunching11 EquipmentSword9 EquipmentBows14 EquipmentWands13 EquipmentTools15 MaxCapBagMi11 EquipmentToolsHatchet10 MaxCapBagT11 FishingRod12 MaxCapBagFi11 CatchingNet12 MaxCapBagB11 TrapBoxSet10 MaxCapBagTr10 WorshipSkull11 MaxCapBagS10 MaxCapBagF11 MaxCapBagM12 FoodG13 EquipmentSmithingTabs7".split(" ")
}
anvilTabs = {
    "Anvil Tab II": "EquipmentSmithingTabs2",
    "Anvil Tab III": "EquipmentSmithingTabs3",
    "Anvil Tab IV": "EquipmentSmithingTabs4",
    "Anvil Tab V":"EquipmentSmithingTabs5",
    "Anvil Tab VI": "EquipmentSmithingTabs6",
    #"Anvil Tab VII": "EquipmentSmithingTabs7",
}
