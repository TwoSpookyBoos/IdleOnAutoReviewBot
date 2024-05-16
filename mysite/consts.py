import math

from utils.logging import get_logger


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
    [1, "SS", {'Infinity Hammer': 1, 'Bleach Liquid Cauldrons': 1, 'Crystal 3d Printer': 1, 'Richelin Kitchen': 1, 'Golden Sprinkler': 1, 'Shroom Familiar': 1},
     "These are the highest priority as 1st purchase per world."],
    [2, "S", {'Extra Card Slot': 4, 'Brimstone Forge Slot': 1}, ""],
    [3, "A", {'Item Backpack Space': 1, 'Storage Chest Space': 4, 'Carry Capacity': 2, 'Weekly Dungeon Boosters': 3, 'Brimstone Forge Slot': 4,
              'Bleach Liquid Cauldrons': 2, 'Zen Cogs': 2, 'Tower Building Slots': 1, 'Royal Egg Cap': 3, 'Richelin Kitchen': 3, 'Souped Up Tube': 1,
              'Chest Sluggo': 3, 'Divinity Sparkie': 2, 'Lava Sprouts': 2, 'Plot of Land': 2}, ""],
    [4, "B", {'Item Backpack Space': 2, 'Storage Chest Space': 8, 'Carry Capacity': 4, 'Food Slot': 1, 'Bleach Liquid Cauldrons': 3, 'More Sample Spaces': 2,
              'Zen Cogs': 4, 'Tower Building Slots': 2, 'Royal Egg Cap': 5, 'Fenceyard Space': 2, 'Chest Sluggo': 6, 'Lava Sprouts': 4, 'Plot of Land': 4,
              'Shroom Familiar': 2, 'Instagrow Generator': 1}, ""],
    [5, "C", {'Item Backpack Space': 3, 'Storage Chest Space': 12, 'Carry Capacity': 6, 'Food Slot': 2, 'Bleach Liquid Cauldrons': 4, 'More Sample Spaces': 4,
              'Burning Bad Books': 2, 'Tower Building Slots': 4, 'Fenceyard Space': 4, 'Chest Sluggo': 9, 'Golden Sprinkler': 2, 'Lava Sprouts': 6,
              'Plot of Land': 6, 'Shroom Familiar': 3, 'Instagrow Generator': 2}, ""],
    [6, "D",
     {'Item Backpack Space': 4, 'Carry Capacity': 8, 'More Storage Space': 5, 'Brimstone Forge Slot': 8, 'Ivory Bubble Cauldrons': 4, 'Obol Storage Space': 3,
      'More Sample Spaces': 6, 'Burning Bad Books': 4, 'Zen Cogs': 8, 'Souped Up Tube': 3, 'Fenceyard Space': 6, 'Chest Sluggo': 12, 'Plot of Land': 8,
      'Instagrow Generator': 4}, ""],
    [7, "Practical Max",
     {'Item Backpack Space': 6, 'Carry Capacity': 10, 'More Storage Space': 10, 'Card Presets': 1, 'Brimstone Forge Slot': 16, 'Sigil Supercharge': 10,
      'Fluorescent Flaggies': 2, 'Golden Sprinkler': 4, 'Plot of Land': 12, 'Instagrow Generator': 8},
     "I wouldn't recommend going any further as of v2.02. This tier is for the dedicated Gem Farmers from Colo and Normal-difficulty World Bosses."],
    [8, "True Max",
     {'Card Presets': 5, 'Daily Teleports': 10, 'Daily Minigame Plays': 4, 'Weekly Dungeon Boosters': 11, 'Obol Storage Space': 12, 'Prayer Slots': 4,
      'Cog Inventory Space': 20, 'Fluorescent Flaggies': 6, 'Richelin Kitchen': 10, 'Souped Up Tube': 5, 'Pet Storage': 12, 'Divinity Sparkie': 6},
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
                "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4"
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
                "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5",],
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
                "Bullet", "BulletB",],
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
                "FoodMining1", "FoodFish1", "FoodCatch1",
            ],
            },
        12: {
            "Missable Quest Items": ["GoldricP1", "GoldricP2", "GoldricP3", "Quest21"],
            "Base Monster Materials": ["Sewers3"],
            "Crystal Enemy Drops": [
                "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",
                "rtt0", "StoneZ1", "StoneT1",],
            "Other Skilling Resources": [
                "GoldBar", "DementiaBar", "VoidBar", "LustreBar",
                "Peanut", "Quest68", "Bullet3",],  #I really hate that the Slush Bucket is listed as Quest68
            },
        13: {
            "Base Monster Materials": [
                "Quest15", "Hgg"],
            "Crystal Enemy Drops": [
                "EquipmentStatues1", "EquipmentStatues5",
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
                "FoodPotMana3", "FoodPotRe1", "ButterBar", "OilBarrel2", "Ghost", "Quest78",],
        },
        14: {
            "Crystal Enemy Drops": [
                "StoneW2",],  #"StoneA2",],
            "Other Skilling Resources": [
                "DreadloBar", "MarbleBar", "GodshardBar",
                "FoodTrapping1", "FoodWorship1",
                "Critter1A", "Critter2A", "Critter3A", "Critter4A", "Critter5A", "Critter6A", "Critter7A", "Critter8A", "Critter9A", "Critter10A", "Critter11A"],
            "Misc": [
                "Key2", "Key3"]
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
        "Skill": ["Drippy Drop Stamp", "Fishhead Stamp"],
        "Misc": ["Biblio Stamp"],
        "Specific": {'Drippy Drop Stamp': 30},
        "Optional": ["Hermes Stamp", "Talent III Stamp"]}},
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
        "Skill": ["Fly Intel Stamp", "Holy Mackerel Stamp", "Cooked Meal Stamp"],
        "Specific": {'Pickaxe Stamp': 55, 'Hatchet Stamp': 55, 'Card Stamp': 50},
        "Optional": ["Agile Stamp", "Book Stamp", "Talent II Stamp"]}},
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
        "Skill": ["Gamejoy Stamp", "Divine Stamp", "Multitool Stamp"],
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
        "Specific": {'Drippy Drop Stamp': 100, 'Ladle Stamp': 150, 'Potion Stamp': 40}}},
    25: {"TotalStampLevels": 7000, "Stamps": {
        "Combat": ["Conjocharmo Stamp"],
        "Specific": {'Pickaxe Stamp': 95, 'Hatchet Stamp': 95, 'Golden Apple Stamp': 60, 'Multitool Stamp': 100}}},
    26: {"TotalStampLevels": 7500, "Stamps": {
        "Specific": {'Ladle Stamp': 180}}},
    27: {"TotalStampLevels": 8000, "Stamps": {
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
        "Specific": {'Golden Sixes Stamp': 120}}},
    36: {"TotalStampLevels": 12000, "Stamps": {
        "Combat": ["Stat Wallstreet Stamp"],
        "Skill": ["Amplestample Stamp"],
        "Specific": {'Maxo Slappo Stamp': 98, 'Sashe Sidestamp': 98, 'Intellectostampo': 98}}},
    37: {"TotalStampLevels": 12500, "Stamps": {
        "Specific": {'Ladle Stamp': 270}}},
    38: {"TotalStampLevels": 13000, "Stamps": {
        "Combat": ["Sukka Foo"],
        "Skill": ["Triad Essence Stamp", "Summoner Stone Stamp"],
        "Specific": {'Triad Essence Stamp': 80},
        "Optional": ["Void Axe Stamp"]}},
}
smithing_progressionTiers = [
    # int tier, int Cash Points Purchased, int Monster Points Purchased, int Forge Totals, str Notes
    [0, 0, 0, 0, ""],
    [1, 20, 85, 60, "all W1 enemies"],
    [2, 60, 150, 120, "early W2 enemies through Pincermin"],
    [3, 100, 225, 180, "all W2 enemies"],
    [4, 150, 350, 240, "most W3 enemies, excluding Dedotated Rams"],
    [5, 200, 500, 291, "early W4 enemies through Soda Cans"],
    [6, 600, 700, 291, "all W4 enemies"]
]

###WORLD 2 PROGRESSION TIERS###
bubbles_progressionTiers = [
    # int tier, int TotalBubblesUnlocked,
    # dict {OrangeSampleBubbles},
    # dict {GreenSampleBubbles},
    # dict {PurpleSampleBubbles},
    # dict {UtilityBubbles},
    # str BubbleValuePercentage,
    # str Notes
    [0, 0, {}, {}, {}, {}, "0%", ""],
    [1, 10,
     {'Roid Ragin': 12, 'Warriors Rule': 6, 'Hearty Diggy': 12, 'Wyoming Blood': 6, 'Sploosh Sploosh': 6, 'Stronk Tools': 8},
     {'Swift Steppin': 12, 'Archer or Bust': 6, 'Sanic Tools': 8, 'Bug^2': 6},
     {'Stable Jenius': 12, 'Mage is Best': 6, 'Hocus Choppus': 12, 'Molto Loggo': 6, 'Le Brain Tools': 8},
     {'FMJ': 5, 'Shaquracy': 5, 'Prowesessary': 7, 'Hammer Hammer': 6},
     "10%",
     "MINIMUM recommended Utility bubbles for finishing W2. Prowess hard-caps at 2x."],
    [2, 20,
     {'Roid Ragin': 25, 'Warriors Rule': 13, 'Hearty Diggy': 25, 'Wyoming Blood': 13, 'Sploosh Sploosh': 13, 'Stronk Tools': 18},
     {'Swift Steppin': 25, 'Archer or Bust': 13, 'Sanic Tools': 18, 'Bug^2': 13},
     {'Stable Jenius': 25, 'Mage is Best': 13, 'Hocus Choppus': 25, 'Molto Loggo': 13, 'Le Brain Tools': 18},
     {'FMJ': 10, 'Shaquracy': 10, 'Prowesessary': 15, 'Hammer Hammer': 14, 'All for Kill': 25},
     "20%",
     "MINIMUM recommended Utility bubbles for starting W3. Prowess hard-caps at 2x."],
    [3, 40,
     {'Roid Ragin': 67, 'Warriors Rule': 34, 'Hearty Diggy': 67, 'Wyoming Blood': 20, 'Sploosh Sploosh': 20, 'Stronk Tools': 47},
     {'Swift Steppin': 67, 'Archer or Bust': 34, 'Sanic Tools': 47, 'Bug^2': 20},
     {'Stable Jenius': 67, 'Mage is Best': 34, 'Hocus Choppus': 67, 'Molto Loggo': 20, 'Le Brain Tools': 47},
     {'FMJ': 15, 'Shaquracy': 15, 'Prowesessary': 40, 'Hammer Hammer': 41, 'All for Kill': 67},
     "40%",
     "MINIMUM recommended Utility bubbles for starting W4. Prowess hard-caps at 2x."],
    [4, 60,
     {'Roid Ragin': 100, 'Warriors Rule': 50, 'Hearty Diggy': 100, 'Wyoming Blood': 30, 'Sploosh Sploosh': 30, 'Stronk Tools': 70},
     {'Swift Steppin': 100, 'Archer or Bust': 50, 'Sanic Tools': 70, 'Bug^2': 30},
     {'Stable Jenius': 100, 'Mage is Best': 50, 'Hocus Choppus': 100, 'Molto Loggo': 30, 'Le Brain Tools': 70},
     {'FMJ': 20, 'Shaquracy': 20, 'Prowesessary': 60, 'Hammer Hammer': 65, 'All for Kill': 100},
     "50%",
     "MINIMUM recommended Utility bubbles for starting W5. Prowess hard-caps at 2x, which you should be reaching now!"],
    [5, 80,
     {'Roid Ragin': 150, 'Warriors Rule': 75, 'Hearty Diggy': 150, 'Wyoming Blood': 45, 'Sploosh Sploosh': 45, 'Stronk Tools': 105, 'Multorange': 45},
     {'Swift Steppin': 150, 'Archer or Bust': 75, 'Bug^2': 45, 'Premigreen': 45, },
     {'Stable Jenius': 150, 'Mage is Best': 75, 'Molto Loggo': 45, 'Le Brain Tools': 105, 'Severapurple': 45, },
     {'FMJ': 30, 'Shaquracy': 30, 'Hammer Hammer': 105, 'All for Kill': 150},
     "60%",
     "MINIMUM recommended Utility bubbles for starting W6 push. Keep watch of your No Bubble Left Behind list (from W4 Lab) to keep cheap/easy bubbles off when possible!"],
    [6, 100,
     {'Roid Ragin': 234, 'Warriors Rule': 117, 'Hearty Diggy': 234, 'Wyoming Blood': 70, 'Sploosh Sploosh': 70, 'Stronk Tools': 164, 'Multorange': 70,
      'Dream of Ironfish': 70},
     {'Swift Steppin': 234, 'Archer or Bust': 117, 'Bug^2': 70, 'Premigreen': 70, 'Fly in Mind': 94},
     {'Stable Jenius': 234, 'Mage is Best': 117, 'Molto Loggo': 70, 'Le Brain Tools': 164, 'Severapurple': 70, 'Tree Sleeper': 94},
     {'Cookin Roadkill': 105, 'All for Kill': 167},
     "70%",
     "Cookin Roadkill 105 = 60% bubble strength. All for Kill hard-cap at 167, you're finished!"],
    [7, 100,
     {'Roid Ragin': 400, 'Warriors Rule': 200, 'Hearty Diggy': 400, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 280, 'Multorange': 120,
      'Dream of Ironfish': 120},
     {'Swift Steppin': 400, 'Archer or Bust': 200, 'Bug^2': 120, 'Premigreen': 120},
     {'Stable Jenius': 400, 'Mage is Best': 200, 'Hocus Choppus': 400, 'Molto Loggo': 120, 'Le Brain Tools': 280, 'Severapurple': 120, 'Tree Sleeper': 160},
     {'Laaarrrryyyy': 150, 'Hammer Hammer': 150, },
     "80%",
     "Larry at 150 = 72% chance for +2 levels. Somewhere around level 125-150, this bubble should pass 100m Dementia Ore cost and be available to level with Boron upgrades from the W3 Atom Collider in Construction.  It should be, in my opinion, the ONLY Utility Bubble you spend these daily clicks on until it reaches 501. If you cannot afford the Particles needed to level Larry, invest into Sampling Bubbles."],
    [8, 100,
     {'Roid Ragin': 567, 'Warriors Rule': 284, 'Hearty Diggy': 567, 'Stronk Tools': 397, 'Multorange': 170, 'Dream of Ironfish': 170, 'Shimmeron': 227},
     {'Swift Steppin': 567, 'Archer or Bust': 284, 'Premigreen': 170},
     {'Stable Jenius': 567, 'Mage is Best': 284, 'Hocus Choppus': 567, 'Le Brain Tools': 397, 'Severapurple': 170, 'Tree Sleeper': 227},
     {'Hammer Hammer': 180, },
     "85%",
     ""],
    [9, 100,
     {'Roid Ragin': 615, 'Warriors Rule': 308, 'Hearty Diggy': 615, 'Stronk Tools': 430, 'Multorange': 185, 'Dream of Ironfish': 185, 'Shimmeron': 246},
     {'Swift Steppin': 615, 'Archer or Bust': 308, 'Premigreen': 185},
     {'Stable Jenius': 615, 'Mage is Best': 308, 'Hocus Choppus': 615, 'Le Brain Tools': 430, 'Severapurple': 185, 'Tree Sleeper': 246},
     {'Hammer Hammer': 210, },
     "86%",
     ""],
    [10, 100,
     {'Roid Ragin': 670, 'Warriors Rule': 335, 'Hearty Diggy': 670, 'Stronk Tools': 469, 'Multorange': 201, 'Dream of Ironfish': 201, 'Shimmeron': 268},
     {'Swift Steppin': 670, 'Archer or Bust': 335, 'Premigreen': 201},
     {'Stable Jenius': 670, 'Mage is Best': 335, 'Hocus Choppus': 670, 'Le Brain Tools': 469, 'Severapurple': 201, 'Tree Sleeper': 268},
     {'Laaarrrryyyy': 501, },
     "87%",
     ""],
    [11, 100,
     {'Roid Ragin': 700, 'Warriors Rule': 367, 'Hearty Diggy': 734, 'Stronk Tools': 514, 'Multorange': 220, 'Dream of Ironfish': 220, 'Shimmeron': 294},
     {'Swift Steppin': 700, 'Archer or Bust': 367, 'Premigreen': 220},
     {'Stable Jenius': 700, 'Mage is Best': 367, 'Hocus Choppus': 734, 'Le Brain Tools': 514, 'Severapurple': 220, 'Tree Sleeper': 294},
     {'Cookin Roadkill': 630, 'Hammer Hammer': 270, },
     "88%",
     ""],
    [12, 100,
     {'Roid Ragin': 720, 'Warriors Rule': 405, 'Hearty Diggy': 810, 'Stronk Tools': 567, 'Multorange': 243, 'Dream of Ironfish': 243, 'Shimmeron': 324},
     {'Swift Steppin': 720, 'Archer or Bust': 405, 'Premigreen': 243},
     {'Stable Jenius': 720, 'Mage is Best': 405, 'Hocus Choppus': 810, 'Le Brain Tools': 567, 'Severapurple': 243, 'Tree Sleeper': 324},
     {'Startue Exp': 240, 'Hammer Hammer': 300, },
     "89%",
     ""],
    [13, 100,
     {'Roid Ragin': 740, 'Warriors Rule': 450, 'Hearty Diggy': 900, 'Stronk Tools': 630, 'Multorange': 270, 'Dream of Ironfish': 270, 'Shimmeron': 360},
     {'Swift Steppin': 740, 'Archer or Bust': 450, 'Premigreen': 270},
     {'Stable Jenius': 740, 'Mage is Best': 450, 'Hocus Choppus': 900, 'Le Brain Tools': 630, 'Severapurple': 270, 'Tree Sleeper': 360},
     {'Droppin Loads': 280},
     "90%",
     ""],
    [14, 100,
     {'Roid Ragin': 760, 'Warriors Rule': 506, 'Hearty Diggy': 1012, 'Multorange': 304, 'Shimmeron': 405},
     {'Swift Steppin': 760, 'Archer or Bust': 506, 'Premigreen': 304},
     {'Stable Jenius': 760, 'Mage is Best': 506, 'Hocus Choppus': 1012, 'Severapurple': 304},
     {'Call Me Bob': 200},
     "91%",
     ""],
    [15, 100,
     {'Roid Ragin': 780, 'Warriors Rule': 575, 'Hearty Diggy': 1150, 'Multorange': 345, 'Shimmeron': 460},
     {'Swift Steppin': 780, 'Archer or Bust': 575, 'Premigreen': 345},
     {'Stable Jenius': 780, 'Mage is Best': 575, 'Hocus Choppus': 1150, 'Severapurple': 345},
     {'Big P': 140, 'Big Game Hunter': 70, 'Mr Massacre': 117},
     "92%",
     ""],
    [16, 100,
     {'Roid Ragin': 800, 'Warriors Rule': 665, 'Hearty Diggy': 1329, 'Multorange': 399, 'Shimmeron': 532},
     {'Swift Steppin': 800, 'Archer or Bust': 665, 'Premigreen': 399},
     {'Stable Jenius': 800, 'Mage is Best': 665, 'Hocus Choppus': 1329, 'Severapurple': 399},
     {'Big P': 240, 'Big Game Hunter': 120, 'Mr Massacre': 200},
     "93%",
     ""],
    [17, 100,
     {'Roid Ragin': 820, 'Warriors Rule': 784, 'Hearty Diggy': 1567, 'Multorange': 470, 'Shimmeron': 627},
     {'Swift Steppin': 820, 'Archer or Bust': 784, 'Premigreen': 470},
     {'Stable Jenius': 820, 'Mage is Best': 784, 'Hocus Choppus': 1567, 'Severapurple': 470},
     {'Big P': 340, 'Carpenter': 284, 'Big Game Hunter': 170, 'Mr Massacre': 284},
     "94%",
     ""],
    [18, 100,
     {'Roid Ragin': 840, 'Warriors Rule': 950, 'Hearty Diggy': 1900, 'Multorange': 570, 'Shimmeron': 760},
     {'Swift Steppin': 840, 'Archer or Bust': 950, 'Premigreen': 570},
     {'Stable Jenius': 840, 'Mage is Best': 950, 'Hocus Choppus': 1900, 'Severapurple': 570},
     {'Laaarrrryyyy': 900, 'Big P': 540, 'Call Me Bob': 500, 'Carpenter': 450, 'Big Game Hunter': 270, 'Mr Massacre': 450},
     "95%",
     ""],
    [19, 100,
     {'Roid Ragin': 860, 'Warriors Rule': 1200, 'Multorange': 720},
     {'Swift Steppin': 860, 'Archer or Bust': 1200},
     {'Stable Jenius': 860, 'Mage is Best': 1200, 'Severapurple': 720},
     {'Call Me Bob': 700, 'Cropius Mapper': 630, 'Lo Cost Mo Jade': 360},
     "96%",
     ""],
    [20, 100,
     {'Roid Ragin': 880, 'Warriors Rule': 1617, 'Multorange': 970},
     {'Swift Steppin': 880, 'Archer or Bust': 1617},
     {'Stable Jenius': 880, 'Mage is Best': 1617, 'Severapurple': 970},
     {'Laaarrrryyyy': 1900, 'Big P': 1140, 'Carpenter': 950, 'Big Game Hunter': 570, 'Mr Massacre': 950, 'Diamond Chef': 553, 'Lo Cost Mo Jade': 760},
     "97%",
     ""],
    [21, 120,
     {'Roid Ragin': 900, 'Warriors Rule': 2450, 'Multorange': 1470},
     {'Swift Steppin': 900, 'Archer or Bust': 2450},
     {'Stable Jenius': 900, 'Mage is Best': 2450, 'Severapurple': 1470},
     {'Essence Boost-Orange': 400, 'Essence Boost-Green': 400, 'Call Me Bob': 1000, 'Diamond Chef': 890},
     "98%",
     ""],
    [22, 140,
     {'Roid Ragin': 950, 'Warriors Rule': 4950, 'Multorange': 2970},
     {'Swift Steppin': 950, 'Archer or Bust': 4950},
     {'Stable Jenius': 950, 'Mage is Best': 4950, 'Severapurple': 2970},
     {'Diamond Chef': 1226, 'Carpenter': 2331},
     "99%",
     ""],
    [23, 160,
     {'Roid Ragin': 1000, 'Hearty Diggy': 9900, 'Stronk Tools': 6930, 'Dream of Ironfish': 2970, 'Shimmeron': 3960, 'Slabi Orefish': 5940,
      'Slabi Strength': 5940},
     {'Swift Steppin': 1000, 'Sanic Tools': 6930, 'Premigreen': 2970, 'Fly in Mind': 3960, 'Slabo Critterbug': 5940, 'Slabo Agility': 5940},
     {'Stable Jenius': 1000, 'Hocus Choppus': 9900, 'Le Brain Tools': 6930, 'Tree Sleeper': 3960, 'Slabe Logsoul': 5940, 'Slabe Wisdom': 5940},
     {'Diamond Chef': 1897, 'Carpenter': 2450},
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
    [5, {'Movespeed': 1}, "Frigid Soul"],  # This buff only works under 170% move speed, so can become useless quite quickly.
    [6, {'TD Points': 10}, "Dioxide Synthesis"],
    [7, {'Multikill': 10}, "Purple Salt"],
    [8, {'EXP': 100}, "Dune Soul"],
    [9, {'Alchemy Liquids': 100}, "Mousey"],
    [10, {'Damage': 250}, "Pingy"]
]
deathNote_progressionTiers = [
    # 0-4 int tier. int w1LowestSkull, int w2LowestSkull, int w3LowestSkull, int w4LowestSkull,
    # 5-9 int w5LowestSkull, int w6LowestSkull, int w7LowestSkull, int w8LowestSkull, int zowCount, int chowCount,
    # 10-11 int meowCount, str Notes
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ""],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, ""],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, ""],
    [3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, ""],
    [4, 4, 4, 4, 2, 0, 0, 0, 0, 15, 0, 0,
     "The recommendation for ZOWs is 12hrs or less (8,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"],
    [5, 5, 5, 5, 3, 0, 0, 0, 0, 26, 0, 0,
     "The Voidwalker questline requires W1-W3 at all Plat Skulls. Aim to complete this by Mid W5 as Vman's account-wide buffs are insanely strong."],
    [6, 7, 5, 5, 4, 0, 0, 0, 0, 40, 15, 0,
     "The recommendation for CHOWs is 12hrs or less (83,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"],
    [7,  10, 7,  5,  5,  1,  0,     0, 0, 40, 26, 0, ""],
    [8,  10, 10, 7,  5,  2,  0,     0, 0, 40, 40, 0, ""],
    [9,  10, 10, 10, 5,  3,  0,     0, 0, 40, 40, 0, ""],
    [10, 10, 10, 10, 7,  4,  0,     0, 0, 53, 53, 0, ""],
    [11, 10, 10, 10, 10, 5,  0,     0, 0, 53, 53, 0, "Complete Lava Skull, then BB Super CHOW, before you start working on Eclipse Skulls. "],
    [12, 10, 10, 10, 10, 7,  0,     0, 0, 66, 66, 0, ""],
    [13, 10, 10, 10, 10, 10, 0,     0, 0, 66, 66, 0, ""],
    [14, 10, 10, 10, 10, 10, 0,     0, 0, 73, 66, 0, ""],
    [15, 10, 10, 10, 10, 10, 0,     0, 0, 73, 73, 0, "The recommendation for Super CHOWs is 24hrs or less (4m+ KPH)"],
    [16, 20, 10, 10, 10, 10, 0,     0, 0, 80, 73, 26, ""],
    [17, 20, 20, 10, 10, 10, 1,     0, 0, 84, 80, 40, ""],
    [18, 20, 20, 20, 10, 10, 2,     0, 0, 85, 80, 53, ""],
    [19, 20, 20, 20, 20, 10, 3,     0, 0, 85, 80, 66, ""],
    [20, 20, 20, 20, 20, 20, 4,     0, 0, 85, 82, 66, ""],
    [21, 20, 20, 20, 20, 20, 5,     0, 0, 85, 83, 66, ""],
    [22, 20, 20, 20, 20, 20, 7,     0, 0, 85, 83, 66, ""],
    [23, 20, 20, 20, 20, 20, 10,    0, 0, 85, 83, 66, ""],
    [24, 20, 20, 20, 20, 20, 10,    0, 0, 85, 83, 73, ""],
    [25, 20, 20, 20, 20, 20, 20,    0, 0, 85, 83, 80, ""],
    [26, 20, 20, 20, 20, 20, 20,    0, 0, 85, 83, 82, ""],
    [27, 20, 20, 20, 20, 20, 20,    0, 0, 85, 85, 83, "As of v2.08, completing a Super CHOW on Boops is impossible."],
    [28, 20, 20, 20, 20, 20, 20,    0, 0, 86, 86, 86, "Info only"]
]
buildingsPostBuffs_progressionTiers = [
    [0, "Unlock", [], "", ""],
    [1, "SS", ["3D Printer", "Cost Cruncher", "Automation Arm"], "", ""],
    [2, "S", ["Talent Book Library", "Death Note", "Salt Lick", "Trapper Drone", "Boulder Roller", "Kraken Cosplayer", "Poisonic Elder"], "", ""],
    [3, "A", ["Chest Space", "Pulse Mage", "Fireball Lobber", "Frozone Malone", "Stormcaller", "Party Starter", "Voidinator", "Clover Shrine", "Crescent Shrine", "Undead Shrine"], "", ""],
    [4, "B", ["Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine", "Summereading Shrine", "Atom Collider"], "", ""],
    [5, "C", ["Primordial Shrine"], "", ""],
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
    [1, {'The Royal Sampler (Rooted Soul)': 5}, ""],
    [2, {'Skilled Dimwit (Forest Soul)':20}, ""],
    [3, {'Balance of Pain (Squishy Soul)':11}, ""],
    [4, {'Skilled Dimwit (Forest Soul)':35, 'Balance of Pain (Squishy Soul)':20}, ""],
    [5, {'Midas Minded (Dune Soul)':20}, ""],
    [6, {'Skilled Dimwit (Forest Soul)':50, 'Midas Minded (Dune Soul)':50, 'Balance of Pain (Squishy Soul)':30}, ""],
    [7, {'Shiny Snitch (Forest Soul)':50, 'Zerg Rushogen (Forest Soul)':20, 'Jawbreaker (Dune Soul)':50, 'Ruck Sack (Rooted Soul)':50, 'Balance of Proficiency (Squishy Soul)':50}, ""],
    [8, {'Unending Energy (Forest Soul)':50, 'Big Brain Time (Forest Soul)':50, 'Antifun Spirit (Rooted Soul)':10, 'Fibers of Absence (Frigid Soul)':50, 'Beefy For Real (Frigid Soul)':40}, ""],
    [9, {'Tachion of the Titans (Dune Soul)':1, 'Balance of Precision (Dune Soul)':1, 'Circular Criticals (Rooted Soul)':1, 'Vacuous Tissue (Frigid Soul)':1, 'Glitterbug (Squishy Soul)':1}, ""],
]

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
                "Faster Shiny Pet Lv Up Rate": 24,
                "Bonuses from All Meals": 10
            },
            "ShinyNotes": "Start by focusing on pets that increase Shiny Speed rate. This will decrease the amount of time needed to level up pets in the future."
            },
        7: {
            "Tier": 7,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Infinite Star Signs": 25,
                "Base Efficiency for All Skills": 20
                },
            "ShinyNotes": ""
            },
        8: {
            "Tier": 8,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Base Critter Per Trap": 10,
                "Drop Rate": 15
                },
            "ShinyNotes": ""
            },
        9: {
            "Tier": 9,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Faster Refinery Speed": 15,
                "Lower Minimum Travel Time for Sailing": 5
                },
            "ShinyNotes": ""
        },
        10: {
            "Tier": 10,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Multikill Per Tier": 20,
                "Higher Artifact Find Chance": 15
                },
            "ShinyNotes": ""
        },
        11: {
            "Tier": 11,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Faster Shiny Pet Lv Up Rate": 28,
                "Infinite Star Signs": 36
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

###WORLD 6 PROGRESSION TIERS###

###UI CONSTS###
maxTiersPerGroup = 3
switches = [
    {
        "label": "Autoloot purchased",
        "name": "autoloot",
        "true": "",
        "false": "",
    },
    {
        "label": "Sheepie pet acquired",
        "name": "sheepie",
        "true": "",
        "false": "",
    },
    {
        "label": "Doot pet acquired",
        "name": "doot",
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
        "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1",  # W1
        "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2",  # W2
        "FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3",  # W3
        "FoodPotMana4", "Leaf4",  # W4
        "FoodPotYe5", "Leaf5",  # W5
        "Leaf6",  # W6
        "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",  # Standard statues
        "EquipmentStatues1", "EquipmentStatues5",  # Plausible but time consuming
        "rtt0", "StoneZ1", "StoneT1", "StoneW1", "StoneA1",  #W1 Slow drops = Town TP + Stones
        "StoneT2", "StoneZ2",  "StoneW2",  #"StoneA2", # W2 upgrade stones and Mystery2
        "PureWater",  #W3 Slow drops = Distilled Water
        "FoodG9",  #W5 Slow drops = Golden W5 Sammy
    ],
    "Printable Skilling Resources": [
        "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", "PalmTree", "StumpTree", "SaharanFoal",  # Logs1
        "Tree7", "AlienTree", "Tree8", "Tree9", "Tree11", "Tree10", "Tree12", "Tree13",  # Logs2

        "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",  # Ores1
        "Starfire", "Marble", "Dreadlo", "Godshard",  # Ores2

        "Fish1", "Fish2", "Fish3", "Fish4", # Small Fish
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
        "Refinery1", "Refinery2", "Refinery3", "Refinery4", "Refinery5", "Refinery6"
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
        "SilverPen", "Ladle",
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
        "EquipmentStatues8", "EquipmentStatues9", "EquipmentStatues10", "EquipmentStatues11", "EquipmentStatues12", "EquipmentStatues13",  # W2 Statues
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

numberOfSecretClasses = 3  # Last verified as of v2.08
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
def lavaFunc(funcType: str, level: int, x1: int, x2: int, roundResult=False):
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


###WORLD 1 CONSTS###
bribesList = [
    "Insider Trading", "Tracking Chips", "Mandatory Fire Sale", "Sleeping On the Job", "Artificial Demand", "The Art of the Deal",
    "Overstock Regulations", "Double EXP Scheme", "Tagged Indicators", "Fossil Fuel Legislation", "Five Aces in the Deck", "Fake Teleport Tickets", "The Art of the Steal",
    "Counterfeit Telepassports", "Weighted Marbles", "Changing the Code", "Taxidermied Cog Pouches", "Guild VIP Fraud", "Library Double Agent", "The Art of the Fail",
    "Photoshopped Dmg Range", "Glitched Acc Formula", "Firewalled Defence", "Bottomless Bags", "AFKeylogging", "Guild GP Hack", "The Art of the Bail",
    "Random Garbage", "Godlier Creation", "Fishermaster", "Muscles on Muscles", "Bottle Service", "Star Scraper", "The Art of the Grail",
    "Artifact Pilfering", "Forge Cap Smuggling", "Gold from Lead", "Nugget Fabrication", "Divine PTS Miscounting", "Loot Table Tampering", "The Art of the Flail"
]
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
}
stampNameDict = {
    "Combat": {
        0: "Sword Stamp", 1: "Heart Stamp", 2: "Mana Stamp", 3: "Tomahawk Stamp", 4: "Target Stamp",
        5: "Shield Stamp", 6: "Longsword Stamp", 7: "Kapow Stamp", 8: "Fist Stamp", 9: "Battleaxe Stamp",
        10: "Agile Stamp", 11: "Vitality Stamp", 12: "Book Stamp", 13: "Manamoar Stamp", 14: "Clover Stamp",
        15: "Scimitar Stamp", 16: "Bullseye Stamp", 17: "Feather Stamp", 18: "Polearm Stamp", 19: "Violence Stamp",
        20: "Buckler Stamp", 21: "Hermes Stamp", 22: "Sukka Foo", 23: "Arcane Stamp", 24: "Avast Yar Stamp",
        25: "Steve Sword", 26: "Blover Stamp", 27: "Stat Graph Stamp", 28: "Gilded Axe Stamp",
        29: "Diamond Axe Stamp", 30: "Tripleshot Stamp", 31: "Blackheart Stamp", 32: "Maxo Slappo Stamp", 33: "Sashe Sidestamp", 34: "Intellectostampo",
        35: "Conjocharmo Stamp", 36: "Dementia Sword Stamp", 37: "Golden Sixes Stamp", 38: "Stat Wallstreet Stamp", 39: "Void Sword Stamp",
        40: "Void Axe Stamp", 41: "Captalist Stats Stamp"
    },
    "Skill": {
        0: "Pickaxe Stamp", 1: "Hatchet Stamp", 2: "Anvil Zoomer Stamp", 3: "Lil' Mining Baggy Stamp", 4: "Twin Ores Stamp",
        5: "Choppin' Bag Stamp", 6: "Duplogs Stamp", 7: "Matty Bag Stamp", 8: "Smart Dirt Stamp", 9: "Cool Diggy Tool Stamp",
        10: "High IQ Lumber Stamp", 11: "Swag Swingy Tool Stamp", 12: "Alch Go Brrr Stamp", 13: "Brainstew Stamp", 14: "Drippy Drop Stamp",
        15: "Droplots Stamp", 16: "Fishing Rod Stamp", 17: "Fishhead Stamp", 18: "Catch Net Stamp", 19: "Fly Intel Stamp",
        20: "Bag o Heads Stamp", 21: "Holy Mackerel Stamp", 22: "Bugsack Stamp", 23: "Buzz Buzz Stamp", 24: "Hidey Box Stamp",
        25: "Purp Froge Stamp", 26: "Spikemouth Stamp", 27: "Shiny Crab Stamp", 28: "Gear Stamp", 29: "Stample Stamp",
        30: "Saw Stamp", 31: "Amplestample Stamp", 32: "SpoOoky Stamp", 33: "Flowin Stamp", 34: "Prayday Stamp",
        35: "Banked Pts Stamp", 36: "Cooked Meal Stamp", 37: "Spice Stamp", 38: "Ladle Stamp", 39: "Nest Eggs Stamp",
        40: "Egg Stamp", 41: "Lab Tube Stamp", 42: "Sailboat Stamp", 43: "Gamejoy Stamp", 44: "Divine Stamp",
        45: "Multitool Stamp", 46: "Skelefish Stamp", 47: "Crop Evo Stamp", 48: "Sneaky Peeky Stamp", 49: "Jade Mint Stamp",
        50: "Summoner Stone Stamp", 51: "White Essence Stamp", 52: "Triad Essence Stamp", 53: "Dark Triad Essence Stamp"
    },
    "Misc": {
        0: "Questin Stamp", 1: "Mason Jar Stamp", 2: "Crystallin", 3: "Arcade Ball Stamp", 4: "Gold Ball Stamp",
        5: "Potion Stamp", 6: "Golden Apple Stamp", 7: "Ball Timer Stamp", 8: "Card Stamp", 9: "Forge Stamp",
        10: "Vendor Stamp", 11: "Sigil Stamp", 12: "Talent I Stamp", 13: "Talent II Stamp", 14: "Talent III Stamp",
        15: "Talent IV Stamp", 16: "Talent V Stamp", 17: "Talent S Stamp", 18: "Multikill Stamp", 19: "Biblio Stamp",
        20: "DNA Stamp", 21: "Refinery Stamp", 22: "Atomic Stamp"
    }
}
stampTypes = ["Combat", "Skill", "Misc"]
unavailableStampsList = [
    'Shiny Crab Stamp', 'Gear Stamp', 'SpoOoky Stamp', 'Prayday Stamp',  #Skill
    'Talent I Stamp', 'Talent V Stamp',  #Misc
]  # Last verified as of v2.08
starsignsList: list[str] = [

]

###WORLD 2 CONSTS###
max_IndexOfVials = 75  # Last verified as of v2.08
max_IndexOfBubbles = 29  # Last verified as of v2.08
max_IndexOfSigils = 3  # Last verified as of v2.08
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
def getReadableVialNames(inputNumber):
    try:
        inputNumber = int(inputNumber)
    except:
        return f"Unknown Vial {inputNumber}"
    match inputNumber:
        case 0:
            return "Copper Corona (Copper Ore)"
        case 1:
            return "Sippy Splinters (Oak Logs)"
        case 2:
            return "Mushroom Soup (Spore Cap)"
        case 3:
            return "Spool Sprite (Thread)"
        case 4:
            return "Barium Mixture (Copper Bar)"
        case 5:
            return "Dieter Drink (Bean Slices)"
        case 6:
            return "Skinny 0 Cal (Snake Skin)"
        case 7:
            return "Thumb Pow (Trusty Nails)"
        case 8:
            return "Jungle Juice (Jungle Logs)"
        case 9:
            return "Barley Brew (Iron Bar)"
        case 10:
            return "Anearful (Glublin Ear)"
        case 11:
            return "Tea With Pea (Potty Rolls)"
        case 12:
            return "Gold Guzzle (Gold Ore)"
        case 13:
            return "Ramificoction (Bullfrog Horn)"
        case 14:
            return "Seawater (Goldfish)"
        case 15:
            return "Tail Time (Rats Tail)"
        case 16:
            return "Fly In My Drink (Fly)"
        case 17:
            return "Mimicraught (Megalodon Tooth)"
        case 18:
            return "Blue Flav (Platinum Ore)"
        case 19:
            return "Slug Slurp (Hermit Can)"
        case 20:
            return "Pickle Jar (BobJoePickle)"
        case 21:
            return "Fur Refresher (Floof Ploof)"
        case 22:
            return "Sippy Soul (Forest Soul)"
        case 23:
            return "Crab Juice (Crabbo)"
        case 24:
            return "Void Vial (Void Ore)"
        case 25:
            return "Red Malt (Redox Salts)"
        case 26:
            return "Ew Gross Gross (Mosquisnow)"
        case 27:
            return "The Spanish Sahara (Tundra Logs)"
        case 28:
            return "Poison Tincture (Poison Froge)"
        case 29:
            return "Etruscan Lager (Mamooth Tusk)"
        case 30:
            return "Chonker Chug (Dune Soul)"
        case 31:
            return "Bubonic Burp (Mousey)"
        case 32:
            return "Visible Ink (Pen)"
        case 33:
            return "Orange Malt (Explosive Salts)"
        case 34:
            return "Snow Slurry (Snow Ball)"
        case 35:
            return "Slowergy Drink (Frigid Soul)"
        case 36:
            return "Sippy Cup (Sippy Straw)"
        case 37:
            return "Bunny Brew (Bunny)"
        case 38:
            return "40-40 Purity (Contact Lense)"
        case 39:
            return "Shaved Ice (Purple Salt)"
        case 40:
            return "Goosey Glug (Honker)"
        case 41:
            return "Ball Pickle Jar (BallJoePickle)"
        case 42:
            return "Capachino (Purple Mush Cap)"
        case 43:
            return "Donut Drink (Half Eaten Donut)"
        case 44:
            return "Long Island Tea (Sand Shark)"
        case 45:
            return "Spook Pint (Squishy Soul)"
        case 46:
            return "Calcium Carbonate (Tongue Bone)"
        case 47:
            return "Bloat Draft (Blobfish)"
        case 48:
            return "Choco Milkshake (Crumpled Wrapper)"
        case 49:
            return "Pearl Seltzer (Pearler Shell)"
        case 50:
            return "Krakenade (Kraken)"
        case 51:
            return "Electrolyte (Condensed Zap)"
        case 52:
            return "Ash Agua (Suggma Ashes)"
        case 53:
            return "Maple Syrup (Maple Logs)"
        case 54:
            return "Hampter Drippy (Hampter)"
        case 55:
            return "Dreadnog (Dreadlo Bar)"
        case 56:
            return "Dusted Drink (Dust Mote)"
        case 57:
            return "Oj Jooce (Orange Slice)"
        case 58:
            return "Oozie Ooblek (Oozie Soul)"
        case 59:
            return "Venison Malt (Mongo Worm Slices)"
        case 60:
            return "Marble Mocha (Marble Ore)"
        case 61:
            return "Willow Sippy (Willow Logs)"
        case 62:
            return "Shinyfin Stew (Equinox Fish)"
        case 63:
            return "Dreamy Drink (Dream Particulate)"
        case 64:
            return "Ricecakorade (Rice Cake)"
        case 65:
            return "Ladybug Serum (Ladybug)"
        case 66:
            return "Flavorgil (Caulifish)"
        case 67:
            return "Greenleaf Tea (Leafy Branch)"
        case 68:
            return "Firefly Grog (Firefly)"
        case 69:
            return "Dabar Special (Godshard Bar)"
        case 70:
            return "Refreshment (Breezy Soul)"
        case 71:
            return "Gibbed Drink (Eviscerated Horn)"
        case 72:
            return "Ded Sap (Effervescent Log)"
        case 73:
            return "Royale Cola (Royal Headpiece)"
        case 74:
            return "Turtle Tisane (Tuttle)"
        case _:
            return f"Unknown Vial {inputNumber}"

def getReadableBubbleNames(inputNumber, color):
    try:
        inputNumber = int(inputNumber)
    except:
        return f"Unknown Bubble {color} {inputNumber}"
    match color:
        case "Orange":
            match inputNumber:
                case 0:
                    return "Roid Ragin"
                case 1:
                    return "Warriors Rule"
                case 2:
                    return "Hearty Diggy"
                case 3:
                    return "Wyoming Blood"
                case 4:
                    return "Reely Smart"
                case 5:
                    return "Big Meaty Claws"
                case 6:
                    return "Sploosh Sploosh"
                case 7:
                    return "Stronk Tools"
                case 8:
                    return "FMJ"
                case 9:
                    return "Bappity Boopity"
                case 10:
                    return "Brittley Spears"
                case 11:
                    return "Call Me Bob"
                case 12:
                    return "Carpenter"
                case 13:
                    return "Buff Boi Talent"
                case 14:
                    return "Orange Bargain"
                case 15:
                    return "Penny of Strength"
                case 16:
                    return "Multorange"
                case 17:
                    return "Dream of Ironfish"
                case 18:
                    return "Shimmeron"
                case 19:
                    return "Bite But Not Chew"
                case 20:
                    return "Spear Powah"
                case 21:
                    return "Slabi Orefish"
                case 22:
                    return "Gamer at Heart"
                case 23:
                    return "Slabi Strength"
                case 24:
                    return "Power Trione"
                case 25:
                    return "Farquad Force"
                case 26:
                    return "Endgame Eff I"
                case 27:
                    return "Tome Strength"
                case 28:
                    return "Essence Boost-Orange"
                case 29:
                    return "Crop Chapter"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"
        case "Green":
            match inputNumber:
                case 0:
                    return "Swift Steppin"
                case 1:
                    return "Archer or Bust"
                case 2:
                    return "Hammer Hammer"
                case 3:
                    return "Lil Big Damage"
                case 4:
                    return "Anvilnomics"
                case 5:
                    return "Quick Slap"
                case 6:
                    return "Sanic Tools"
                case 7:
                    return "Bug^2"
                case 8:
                    return "Shaquracy"
                case 9:
                    return "Cheap Shot"
                case 10:
                    return "Bow Jack"
                case 11:
                    return "Call Me Ash"
                case 12:
                    return "Cuz I Catch Em All"
                case 13:
                    return "Fast Boi Talent"
                case 14:
                    return "Green Bargain"
                case 15:
                    return "Dollar Of Agility"
                case 16:
                    return "Premigreen"
                case 17:
                    return "Fly in Mind"
                case 18:
                    return "Kill Per Kill"
                case 19:
                    return "Afk Expexp"
                case 20:
                    return "Bow Power"
                case 21:
                    return "Slabo Critterbug"
                case 22:
                    return "Sailor At Heart"
                case 23:
                    return "Slabo Agility"
                case 24:
                    return "Power Tritwo"
                case 25:
                    return "Quickdraw Quiver"
                case 26:
                    return "Essence Boost-Green"
                case 27:
                    return "Endgame Eff II"
                case 28:
                    return "Tome Agility"
                case 29:
                    return "Stealth Chapter"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"
        case "Purple":
            match inputNumber:
                case 0:
                    return "Stable Jenius"
                case 1:
                    return "Mage is Best"
                case 2:
                    return "Hocus Choppus"
                case 3:
                    return "Molto Loggo"
                case 4:
                    return "Noodubble"
                case 5:
                    return "Name I Guess"
                case 6:
                    return "Le Brain Tools"
                case 7:
                    return "Cookin Roadkill"
                case 8:
                    return "Brewstachio"
                case 9:
                    return "All for Kill"
                case 10:
                    return "Matty Stafford"
                case 11:
                    return "Call Me Pope"
                case 12:
                    return "Gospel Leader"
                case 13:
                    return "Smart Boi Talent"
                case 14:
                    return "Purple Bargain"
                case 15:
                    return "Nickel Of Wisdom"
                case 16:
                    return "Severapurple"
                case 17:
                    return "Tree Sleeper"
                case 18:
                    return "Hyperswift"
                case 19:
                    return "Matrix Evolved"
                case 20:
                    return "Wand Pawur"
                case 21:
                    return "Slabe Logsoul"
                case 22:
                    return "Pious At Heart"
                case 23:
                    return "Slabe Wisdom"
                case 24:
                    return "Power Trithree"
                case 25:
                    return "Smarter Spells"
                case 26:
                    return "Endgame Eff III"
                case 27:
                    return "Essence Boost-Purple"
                case 28:
                    return "Tome Wisdom"
                case 29:
                    return "Essence Chapter"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"
        case "Yellow":
            match inputNumber:
                case 0:
                    return "Lotto Skills"
                case 1:
                    return "Droppin Loads"
                case 2:
                    return "Startue Exp"
                case 3:
                    return "Level Up Gift"
                case 4:
                    return "Prowesessary"
                case 5:
                    return "Stamp Tramp"
                case 6:
                    return "Undeveloped Costs"
                case 7:
                    return "Da Daily Drip"
                case 8:
                    return "Grind Time"
                case 9:
                    return "Laaarrrryyyy"
                case 10:
                    return "Cogs For Hands"
                case 11:
                    return "Sample It"
                case 12:
                    return "Big Game Hunter"
                case 13:
                    return "Ignore Overdues"
                case 14:
                    return "Yellow Bargain"
                case 15:
                    return "Mr Massacre"
                case 16:
                    return "Egg Ink"
                case 17:
                    return "Diamond Chef"
                case 18:
                    return "Card Champ"
                case 19:
                    return "Petting The Rift"
                case 20:
                    return "Boaty Bubble"
                case 21:
                    return "Big P"
                case 22:
                    return "Bit By Bit"
                case 23:
                    return "Gifts Abound"
                case 24:
                    return "Atom Split"
                case 25:
                    return "Cropius Mapper"
                case 26:
                    return "Essence Boost-Yellow"
                case 27:
                    return "Hinge Buster"
                case 28:
                    return "Ninja Looter"
                case 29:
                    return "Lo Cost Mo Jade"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"


###WORLD 3 CONSTS###
maxDreams = 31  # Last verified as of v2.08
buildingsList: list[str] = [
    "3D Printer", "Talent Book Library", "Death Note", "Salt Lick", "Chest Space", "Cost Cruncher", "Trapper Drone", "Automation Arm", "Atom Collider",
    "Pulse Mage", "Fireball Lobber", "Boulder Roller", "Frozone Malone", "Stormcaller", "Party Starter", "Kraken Cosplayer", "Poisonic Elder", "Voidinator",
    "Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine", "Clover Shrine", "Summereading Shrine", "Crescent Shrine", "Undead Shrine", "Primordial Shrine"
]
shrinesList: list[str] = [
    "Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine", "Clover Shrine", "Summereading Shrine", "Crescent Shrine", "Undead Shrine", "Primordial Shrine"
]
atomsList: list[str] = [
    "Hydrogen - Stamp Decreaser", "Helium - Talent Power Stacker", "Lithium - Bubble Insta Expander", "Beryllium - Post Office Penner",
    "Boron - Particle Upgrader", "Carbon - Wizard Maximizer", "Nitrogen - Construction Trimmer", "Oxygen - Library Booker",
    "Fluoride - Void Plate Chef", "Neon - Damage N' Cheapener", "Sodium - Snail Kryptonite"
]
prayersList: list[str] = [
    "Big Brain Time (Forest Soul)", "Skilled Dimwit (Forest Soul)", "Unending Energy (Forest Soul)",
    "Shiny Snitch (Forest Soul)", "Zerg Rushogen (Forest Soul)",
    "Tachion of the Titans (Dune Soul)", "Balance of Precision (Dune Soul)", "Midas Minded (Dune Soul)", "Jawbreaker (Dune Soul)",
    "The Royal Sampler (Rooted Soul)", "Antifun Spirit (Rooted Soul)", "Circular Criticals (Rooted Soul)", "Ruck Sack (Rooted Soul)",
    "Fibers of Absence (Frigid Soul)", "Vacuous Tissue (Frigid Soul)", "Beefy For Real (Frigid Soul)",
    "Balance of Pain (Squishy Soul)", "Balance of Proficiency (Squishy Soul)","Glitterbug (Squishy Soul)",
]

###WORLD 4 CONSTS###
maxCookingTables = 10  # Last verified as of v2.08
maxMeals = 67  # Last verified as of v2.08
maxMealLevel = 90  # Last verified as of v2.08
labChipsList: list[str] = [
    "Grounded Nanochip", "Grounded Motherboard", "Grounded Software", "Grounded Processor", "Potato Chip",
    "Conductive Nanochip", "Conductive Motherboard", "Conductive Software", "Conductive Processor", "Chocolatey Chip",
    "Galvanic Nanochip", "Galvanic Motherboard", "Galvanic Software", "Galvanic Processor", "Wood Chip",
    "Silkrode Nanochip", "Silkrode Motherboard", "Silkrode Software", "Silkrode Processor", "Poker Chip",
    "Omega Nanochip", "Omega Motherboard"
]
labBonusesList = [
    "Animal Farm", "Wired In", "Gilded Cyclical Tubing", "No Bubble Left Behind", "Killer's Brightside",
    "Shrine World Tour", "Viaduct of the Gods", "Certified Stamp Book", "Spelunker Obol", "Fungi Finger Pocketer",
    "My 1st Chemistry Set", "Unadulterated Banking Fury", "Sigils of Olden Alchemy", "Viral Connection",
    "Artifact Attraction", "Slab Sovereignty", "Spiritual Growth", "Depot Studies PhD"
]

###WORLD 5 CONSTS###
numberOfArtifacts = 33  # Last verified as of v2.08
numberOfArtifactTiers = 4  # Last verified as of v2.08
currentMaxChestsSum = 45  # Last verified as of v2.08
artifactsList = [
    'Moai Head', 'Maneki Kat', 'Ruble Cuble', 'Fauxory Tusk', 'Gold Relic',
    'Genie Lamp', 'Silver Ankh', 'Emerald Relic', 'Fun Hippoete', 'Arrowhead',
    '10 AD Tablet', 'Ashen Urn', 'Amberite', 'Triagulon', 'Billcye Tri',
    'Frost Relic', 'Chilled Yarn', 'Causticolumn', 'Jade Rock', 'Dreamcatcher',
    'Gummy Orb', 'Fury Relic', 'Cloud Urn', 'Weatherbook', 'Giants Eye',
    'Crystal Steak', 'Trilobite Rock', 'Opera Mask', 'Socrates', 'The True Lantern',
    'The Onyx Lantern', 'The Shim Lantern', 'The Winz Lantern'
]

###WORLD 6 CONSTS###
jade_emporium = [
  {
    "name": "Quick Ref Access",
    "bonus": "Adds the Sneaking skill to your QuickRef menu! Manage your Ninja Twins from anywhere!"
  },
  {
    "name": "Gold Food Beanstalk",
    "bonus": "Grows a giant beanstalk behind the ninja castle! Drop a stack of 10,000 Gold Food to add it with the beanstalk and permanently gain its bonus!"
  },
  {
    "name": "Supersized Gold Beanstacking",
    "bonus": "You can now drop a stack of 100,000 Gold Food to supersize it! This will obviously give a bigger bonus, and will even enlargen the food on the stalk!"
  },
  {
    "name": "Charmed, I'm Sure",
    "bonus": "All your Ninja Twins can now equip two of the same charm at once!"
  },
  {
    "name": "Mob Cosplay Craze",
    "bonus": "Certain monsters in World 6 will now have a rare chance to drop Ninja Hats, but only the ones you've found already from the Ninja Castle!"
  },
  {
    "name": "Level Exemption",
    "bonus": "Completely and utterly removes the UNDER-LEVELED bonus reduction of all stamps in your collection, now and forever. Amen."
  },
  {
    "name": "Gaming to the MAX",
    "bonus": "All plant types in Gaming have +1 Max Evolution, but this one is 50,000x rarer than normal and will make you wonder if evolution is even real (it is)"
  },
  {
    "name": "Revenge of the Pickle",
    "bonus": "Adds a new boss page to the left of World 1 in Deathnote. Each BoneJoePickle in your inventory counts as +1 Boss Deathnote Kill!"
  },
  {
    "name": "The Artifact Matrix",
    "bonus": "Extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to Artifact Find Chance!"
  },
  {
    "name": "The Slab Matrix",
    "bonus": "Further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to all bonuses from the Slab!"
  },
  {
    "name": "The Spirit Matrix",
    "bonus": "Even further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to W6 Skill exp gain!"
  },
  {
    "name": "The Crop Matrix",
    "bonus": "Yet again even further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to Crop Depot!"
  },
  {
    "name": "MSA Expander I",
    "bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically Farming EXP!"
  },
  {
    "name": "MSA Expander II",
    "bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically Jade Coin Gain!"
  },
  {
    "name": "MSA Expander III",
    "bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically All Essence Gain!"
  },
  {
    "name": "Deal Sweetening",
    "bonus": "Earn +25% more Magic Beans from the mysterious Legumulyte bean merchant found in the Troll Broodnest map."
  },
  {
    "name": "No Meal Left Behind",
    "bonus": "Every 24 hours, your lowest level Meal gets +1 Lv. This only works on Meals Lv 5 or higher, and doesn't trigger on days you don't play."
  },
  {
    "name": "Jade Coin Magnetism",
    "bonus": "Adds a new bonus of +5% Jade Coin Gain per 10 items found after 1000 items, as shown at The Slab in World 5."
  },
  {
    "name": "Essence Confetti",
    "bonus": "Adds a new bonus of +3% All Essence Gain per 10 items found after 1000 items, as shown at The Slab in World 5."
  },
  {
    "name": "Shrine Collective Bargaining Agreement",
    "bonus": "Shrines no longer lose EXP when moved around, so you can finally bring those baddies out of retirement!"
  },
  {
    "name": "Papa Blob's Quality Guarantee",
    "bonus": "Increases the Max Level of all cooking meals by +10. Better meals, better levels, Papa Blob's."
  },
  {
    "name": "Chef Geustloaf's Cutting Edge Philosophy",
    "bonus": "Increases the Max Level of all cooking meals by +10 again! But oh hoho, you sir are no Chef Geustloaf! Good luck cooking to these LVs!"
  },
  {
    "name": "Crop Depot Scientist",
    "bonus": "Employs a friendly scientist blobulyte to keep a Data Sheet of all the crops you've ever found!"
  },
  {
    "name": "Science Environmentally Sourced Pencil",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+15% Cash from Mobs' per crop found!"
  },
  {
    "name": "Science Pen",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '1.02x Plant Evolution Chance in Gaming (multiplicative)' per Crop!"
  },
  {
    "name": "Science Marker",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+8% Jade Coin Gain' per Crop!"
  },
  {
    "name": "Science Featherpen",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '1.10x Cooking Speed (multiplicative)' per Crop!"
  },
  {
    "name": "Reinforced Science Pencil",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+20% Total Damage' per Crop!"
  },
  {
    "name": "Science Crayon",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+7% Shiny Pet Lv Up Rate and Pet Breeding Rate' per Crop!"
  },
  {
    "name": "Science Paintbrush",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+0.1 Base Critter caught in Trapping' per Crop!"
  },
  {
    "name": "New Critter",
    "bonus": "Unlocks a new critter type to capture! These have their own very special vial in Alchemy."
  },
  {
    "name": "Ionized Sigils",
    "bonus": "Sigils can now be upgraded a 3rd time. Push past lame ol' yellow, and further increasing those sigil boosts!"
  },
  {
    "name": "The Endercaptain",
    "bonus": "Adds the Endercaptain to Recruitment pool. They're very rare, and have a hidden account-wide +25% Loot Multi and Artifact Find."
  },
  {
    "name": "True Godly Blessings",
    "bonus": "All Divinity Gods give 1.05x higher Blessing bonus per God Rank. Whats a Blessing bonus? Select a god, it's the one on the bottom, go look."
  },
  {
    "name": "Brighter Lighthouse Bulb",
    "bonus": "You can now find 3 additional Artifacts from The Edge island."
  },
  {
    "name": "Sovereign Artifacts",
    "bonus": "You can now find Sovereign Artifacts from sailing, but only if you've found the Eldritch form first."
  },
  {
    "name": "New Bribes",
    "bonus": "Mr. Pigibank is up to no good once again, and he's looking to get some funding from his favorite patron... you. Well, your wallet specifically."
  },
  {
    "name": "Laboratory Bling",
    "bonus": "Adds 3 new Jewels to unlock at the Jewel Spinner in W4 Town. Or, get one for free every 700 total Lab LV as shown in Rift Skill Mastery."
  }
]
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
maxFarmingCrops = 120  # Last verified as of 2.08
marketUpgradeList = [
    "Land Plots", "Stronger Vines", "Nutritious Soil", "Smarter Seeds",
    "Biology Boost", "Product Doubler", "More Beenz", "Enhanced Deeds",
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

#slabString last pulled from code in 2.08
slabString = "Copper Iron Gold Plat Dementia Void Lustre Starfire Marble Dreadlo Godshard CopperBar IronBar GoldBar PlatBar DementiaBar VoidBar LustreBar StarfireBar MarbleBar DreadloBar GodshardBar OakTree BirchTree JungleTree ForestTree ToiletTree PalmTree StumpTree SaharanFoal Tree7 AlienTree Tree8 Tree9 Tree11 Tree10 Tree12 Tree13 Leaf1 Leaf2 Leaf3 Leaf4 Leaf5 Leaf6 Fish1 Fish2 Fish3 Fish4 Fish5 Fish6 Fish7 Fish8 Fish9 Fish10 Fish11 Fish12 Fish13 Bug1 Bug2 Bug3 Bug4 Bug5 Bug6 Bug7 Bug8 Bug9 Bug11 Bug10 Bug12 Bug13 Critter1 Critter1A Critter2 Critter2A Critter3 Critter3A Critter4 Critter4A Critter5 Critter5A Critter6 Critter6A Critter7 Critter7A Critter8 Critter8A Critter9 Critter9A Critter10 Critter10A Critter11 Critter11A Soul1 Soul2 Soul3 Soul4 Soul5 Soul6 Soul7 Refinery1 Refinery2 Refinery3 Refinery4 Refinery5 Refinery6 CraftMat1 CraftMat2 CraftMat3 CraftMat5 CraftMat6 CraftMat7 CraftMat9 CraftMat8 CraftMat10 CraftMat11 CraftMat12 CraftMat13 CraftMat14 OilBarrel1 OilBarrel2 OilBarrel3 OilBarrel4 OilBarrel5 OilBarrel6 OilBarrel7 PureWater PureWater2 Grasslands1 Grasslands2 Grasslands3 Grasslands4 Jungle1 Jungle2 Jungle3 Forest1 Forest2 Forest3 Sewers1 Sewers1b Sewers2 Sewers3 TreeInterior1 TreeInterior1b TreeInterior2 DesertA1 DesertA1b DesertA2 DesertA3 DesertA3b DesertB1 DesertB2 DesertB3 DesertB4 DesertC1 DesertC2 DesertC2b DesertC3 DesertC4 SnowA1 SnowA2 SnowA2a SnowA3 SnowA4 SnowB1 SnowB2 SnowB2a SnowB5 SnowB3 SnowB4 SnowC1 SnowC2 SnowC3 SnowC4 SnowC4a SnowC5 GalaxyA1 GalaxyA2 GalaxyA2b GalaxyA3 GalaxyA4 GalaxyB1 GalaxyB2 GalaxyB3 GalaxyB4 GalaxyB5 GalaxyC1 GalaxyC1b GalaxyC2 GalaxyC3 GalaxyC4 LavaA1 LavaA1b LavaA2 LavaA3 LavaA4 LavaA5 LavaA5b LavaB1 LavaB2 LavaB3 LavaB3b LavaB4 LavaB5 LavaB6 LavaC1 LavaC2 SpiA1 SpiA2 SpiA2b SpiA3 SpiA4 SpiA5 SpiB1 SpiB2 SpiB2b SpiB3 SpiB4 SpiC1 SpiC2 SpiD1 SpiD2 SpiD3 BabaYagaETC Hgg Quest17 Quest29 EfauntDrop1 EfauntDrop2 Chiz0 Chiz1 TrollPart KrukPart KrukPart2 EquipmentHats11 EquipmentHats12 EquipmentHats13 EquipmentHats14 EquipmentHats1 EquipmentHats15 EquipmentHats17 EquipmentHats20 EquipmentHats3 EquipmentHats16 EquipmentHats21 EquipmentHats18 EquipmentHats22 EquipmentHats28 EquipmentHats19 TestObj13 EquipmentHats41 EquipmentHats26 EquipmentHats52 EquipmentHats53 EquipmentHats54 EquipmentHats61 EquipmentHats58 EquipmentHats59 EquipmentHats60 EquipmentHats68 EquipmentHats70 EquipmentHats71 EquipmentHats74 EquipmentHats77 EquipmentHats83 EquipmentHats105 EquipmentHats106 EquipmentHats5 EquipmentHats6 EquipmentHats7 EquipmentHats8 EquipmentHats9 EquipmentHats10 EquipmentHats4Choppin EquipmentHats25 EquipmentHats107 EquipmentHats29 EquipmentHats39 EquipmentHats27 EquipmentHats30 EquipmentHats44 EquipmentHats2 EquipmentHats67 EquipmentHats64 EquipmentHats66 EquipmentHats79 EquipmentHats73 EquipmentHats51 EquipmentHats56 EquipmentHats63 EquipmentHats85 EquipmentHats86 EquipmentHats87 EquipmentHats88 EquipmentHats42 EquipmentHats69 EquipmentHats108 EquipmentHats55 EquipmentHats75 EquipmentHats76 EquipmentHats65 EquipmentHats80 EquipmentHats81 EquipmentHats78 EquipmentHats90 EquipmentHats91 EquipmentHats92 EquipmentHats93 EquipmentHats94 EquipmentHats95 EquipmentHats96 EquipmentHats97 EquipmentHats98 EquipmentHats99 EquipmentHats100 EquipmentHats101 EquipmentHats102 EquipmentHats103 EquipmentHats104 EquipmentPunching1 EquipmentPunching2 EquipmentPunching3 EquipmentPunching4 EquipmentPunching5 EquipmentPunching6 EquipmentPunching7 EquipmentPunching8 EquipmentPunching9 EquipmentPunching10 EquipmentPunching11 TestObj1 TestObj7 TestObj3 EquipmentSword1 EquipmentSword2 EquipmentSword3 EquipmentSword4 EquipmentSword5 EquipmentSword6 EquipmentSword7 EquipmentSword8 EquipmentSword9 EquipmentBows1 EquipmentBows3 EquipmentBows4 EquipmentBows5 EquipmentBows6 EquipmentBows7 EquipmentBows8 EquipmentBows9 EquipmentBows10 EquipmentBows11 EquipmentBows12 EquipmentBows13 EquipmentBows14 EquipmentWands1 EquipmentWands2 EquipmentWands5 EquipmentWands6 EquipmentWands3 EquipmentWands7 EquipmentWands8 EquipmentWands9 EquipmentWands10 EquipmentWands11 EquipmentWands12 EquipmentWands13 EquipmentShirts1 EquipmentShirts17 EquipmentShirts19 EquipmentShirts20 EquipmentShirts24 EquipmentShirts25 EquipmentShirts2 EquipmentShirts16 EquipmentShirts3 EquipmentShirts21 EquipmentShirts10 EquipmentShirts11 EquipmentShirts12 EquipmentShirts13 EquipmentShirts18 EquipmentShirts14 EquipmentShirts5 EquipmentShirts23 EquipmentShirts22 EquipmentShirts15 EquipmentShirts26 EquipmentShirts27 EquipmentShirts31 EquipmentShirts28 EquipmentShirts29 EquipmentShirts30 EquipmentShirts6 EquipmentShirts32 EquipmentShirts33 EquipmentShirts34 EquipmentShirts35 EquipmentShirts36 EquipmentShirts37 EquipmentShirts38 EquipmentPants1 EquipmentPants2 EquipmentPants3 EquipmentPants4 EquipmentPants17 EquipmentPants5 EquipmentPants6 EquipmentPants20 EquipmentPants21 EquipmentPants10 EquipmentPants15 EquipmentPants16 EquipmentPants18 EquipmentPants19 EquipmentPants22 EquipmentPants23 EquipmentPants9 EquipmentPants24 EquipmentPants25 EquipmentPants8 EquipmentPants26 EquipmentPants27 EquipmentPants29 EquipmentPants30 EquipmentShoes1 EquipmentShoes9 EquipmentShoes15 EquipmentShoes3 EquipmentShoes20 EquipmentShoes4 EquipmentShoes5 EquipmentShoes21 EquipmentShoes22 EquipmentShoes7 EquipmentShoes16 EquipmentShoes17 EquipmentShoes18 EquipmentShoes19 EquipmentShoes2 EquipmentShoes23 EquipmentShoes26 EquipmentShoes27 EquipmentShoes28 EquipmentShoes29 EquipmentShoes30 EquipmentShoes31 EquipmentShoes32 EquipmentShoes33 EquipmentShoes39 EquipmentShoes24 EquipmentShoes25 EquipmentShoes34 EquipmentShoes35 EquipmentShoes36 EquipmentShoes37 EquipmentShoes38 EquipmentPendant9 EquipmentPendant10 EquipmentPendant11 EquipmentPendant12 EquipmentPendant14 EquipmentPendant16 EquipmentPendant17 EquipmentPendant18 EquipmentPendant19 EquipmentPendant20 EquipmentPendant21 EquipmentPendant22 EquipmentPendant23 EquipmentPendant24 EquipmentPendant25 EquipmentPendant26 EquipmentPendant27 EquipmentPendant28 EquipmentPendant31 EquipmentPendant29 EquipmentPendant30 EquipmentRings2 EquipmentRings3 EquipmentRings6 EquipmentRings7 EquipmentRings11 EquipmentRings12 EquipmentRings13 EquipmentRings14 EquipmentRings15 EquipmentRings16 EquipmentRings21 EquipmentRings20 EquipmentRings19 EquipmentRingsFishing1 EquipmentRingsFishing2 EquipmentRingsFishing3 EquipmentRings22 EquipmentRings18 EquipmentRings36 EquipmentRings23 EquipmentRings24 EquipmentRings25 EquipmentRings26 EquipmentRings27 EquipmentRings28 EquipmentRings29 EquipmentRings35 EquipmentRings30 EquipmentRings33 EquipmentRings31 EquipmentRings32 EquipmentRings34 EquipmentRingsChat10 EquipmentCape0 EquipmentCape2 EquipmentCape3 EquipmentCape4 EquipmentCape5 EquipmentCape6 EquipmentCape7 EquipmentCape8 EquipmentCape9 EquipmentCape10 EquipmentCape11 EquipmentCape12 EquipmentCape13 EquipmentCape14 EquipmentKeychain0 EquipmentKeychain1 EquipmentKeychain2 EquipmentKeychain3 EquipmentKeychain4 EquipmentKeychain5 EquipmentKeychain6 EquipmentKeychain7 EquipmentKeychain8 EquipmentKeychain9 EquipmentKeychain10 EquipmentKeychain11 EquipmentKeychain12 EquipmentKeychain13 EquipmentKeychain14 EquipmentKeychain15 EquipmentKeychain16 EquipmentKeychain17 EquipmentKeychain18 EquipmentKeychain19 EquipmentKeychain20 EquipmentKeychain21 EquipmentKeychain22 EquipmentKeychain23 EquipmentKeychain24 EquipmentKeychain25 EquipmentKeychain26 EquipmentKeychain27 EquipmentKeychain28 EquipmentKeychain29 Trophy1 Trophy2 Trophy3 Trophy5 Trophy6 Trophy7 Trophy8 Trophy9 Trophy10 Trophy11 Trophy12 Trophy13 Trophy14 Trophy15 Trophy16 Trophy17 Trophy18 Trophy19 Trophy20 Trophy21 Trophy22 EquipmentNametag1 EquipmentNametag3 EquipmentNametag4 EquipmentNametag5 EquipmentNametag6b EquipmentNametag7 EquipmentNametag8 EquipmentNametag9 EquipmentNametag10 EquipmentTools1 EquipmentTools2 EquipmentTools3 EquipmentTools5 EquipmentTools6 EquipmentTools7 EquipmentTools11 EquipmentTools8 EquipmentTools12 EquipmentTools9 EquipmentTools14 EquipmentTools15 EquipmentTools10 EquipmentTools13 EquipmentToolsHatchet0 EquipmentToolsHatchet3 EquipmentToolsHatchet1 EquipmentToolsHatchet2b EquipmentToolsHatchet2 EquipmentToolsHatchet4 EquipmentToolsHatchet5 EquipmentToolsHatchet7 EquipmentToolsHatchet6 EquipmentToolsHatchet8 EquipmentToolsHatchet9 EquipmentToolsHatchet12 EquipmentToolsHatchet10 EquipmentToolsHatchet11 FishingRod2 FishingRod3 FishingRod4 FishingRod5 FishingRod6 FishingRod7 FishingRod8 FishingRod9 FishingRod10 FishingRod11 FishingRod12 CatchingNet2 CatchingNet3 CatchingNet4 CatchingNet5 CatchingNet6 CatchingNet7 CatchingNet8 CatchingNet9 CatchingNet10 CatchingNet11 CatchingNet12 TrapBoxSet1 TrapBoxSet2 TrapBoxSet3 TrapBoxSet4 TrapBoxSet5 TrapBoxSet6 TrapBoxSet7 TrapBoxSet8 TrapBoxSet9 TrapBoxSet10 WorshipSkull1 WorshipSkull2 WorshipSkull3 WorshipSkull4 WorshipSkull5 WorshipSkull6 WorshipSkull7 WorshipSkull8 WorshipSkull9 WorshipSkull10 WorshipSkull11 DNAgun0 DNAgun1 DNAgun2 DNAgun3 FoodHealth1 FoodHealth3 FoodHealth2 Peanut FoodHealth4 FoodHealth6 FoodHealth7 FoodHealth10 FoodHealth9 FoodHealth11 FoodHealth13 FoodHealth12 FoodHealth14 FoodHealth15 FoodHealth16 FoodHealth17 FoodHealth5 FoodEvent8 Meatloaf FoodPotOr1 FoodPotOr2 FoodPotOr3 FoodPotOr4 FoodPotRe1 FoodPotRe2 FoodPotRe3 FoodPotRe4 FoodPotGr1 FoodPotGr2 FoodPotGr3 FoodPotGr4 FoodEvent7 FoodPotMana1 FoodPotMana2 FoodPotMana3 FoodPotMana4 FoodPotYe1 FoodPotYe2 FoodPotYe3 FoodPotYe4 FoodPotYe5 FoodEvent6 Pearl3 FoodMining1 FoodEvent1 Pearl2 FoodChoppin1 FoodEvent2 FoodFish1 FoodEvent3 Pearl1 FoodCatch1 FoodEvent4 FoodTrapping1 FoodWorship1 Bullet BulletB Bullet3 MidnightCookie FoodEvent5 PeanutG FoodG1 FoodG2 FoodG3 FoodG4 FoodG5 FoodG6 FoodG7 FoodG8 FoodG9 FoodG10 FoodG11 FoodG12 FoodG13 ButterBar rtt0 ResetFrag ResetCompleted ResetCompletedS ClassSwap ClassSwapB ResetBox Ht StonePremRestore StonePremStatswap Key1 Key2 Key3 Key4 Key5 TixCol SilverPen PremiumGem TalentPoint1 TalentPoint2 TalentPoint3 TalentPoint4 TalentPoint5 TalentPoint6 Gfoodcoupon ItemsCoupon1 ItemsCoupon2 ExpBalloon1 ExpBalloon2 ExpBalloon3 Pearl4 Pearl6 Pearl5 Quest30 Quest35 Quest36 Quest38 Quest39 Quest40 Quest42 Quest43 Quest44 Quest49 Quest50 Quest70 Quest71 Quest72 Quest73 Quest75 Quest85 Quest76 Quest77 Quest79 Quest80 GemP30 Quest81 Quest82 Timecandy1 Timecandy2 Timecandy3 Timecandy4 Timecandy5 Timecandy6 Timecandy7 Timecandy8 Timecandy9 StoneWe StoneWeb StoneW1 StoneW2 StoneW3 StoneW3b StoneW6 StoneW4 StoneW5 StoneW7 StoneW8 StoneAe StoneAeB StoneA1 StoneA1b StoneA2 StoneA2b StoneA3 StoneA3b StoneA4 StoneA5 StoneA6 StoneA7 StoneTe StoneT1 StoneT1e StoneT1eb StoneT2 StoneT3 StoneT4 StoneT5 StoneT6 StoneT7 StoneHelm1 StoneHelm6 StoneHelm1b StoneHelm7 StoneZ1 StoneZ2 StoneZ3 StoneZ4 StonePremSTR StonePremAGI StonePremWIS StonePremLUK JobApplication SmithingHammerChisel SmithingHammerChisel2 SmithingHammerChisel3 BobJoePickle BallJoePickle BoneJoePickle Quest1 Crystal1 Crystal2 Crystal3 Crystal4 Crystal5 PeanutS Quest3 Quest4 Mayo Trash Trash2 Trash3 Quest5 Quest6 Quest7 Quest10 Quest11 Quest12 Quest13 Quest14 Quest15 Quest16 Quest18 Quest19 Quest20 Quest21 Quest22 Quest23 Quest24 Quest25 Quest26 Quest27 GoldricP1 GoldricP2 GoldricP3 Cutter Quest32 Quest33 Quest34 Quest37 Quest41 Quest45 Quest46 Quest47 Quest48 Quest51 Quest52 PalmTreeD Quest53 Quest54 Quest55 Quest56 Quest57 Quest58 Quest59 Quest60 Quest61 Quest62 Quest63 Quest64 Quest65 Quest66 Quest67 Whetstone Quest68 Quest69 Quest74 Quest78 Quest83 Quest84 BadgeG1 BadgeG2 BadgeG3 BadgeD1 BadgeD2 BadgeD3 NPCtoken1 NPCtoken2 NPCtoken3 NPCtoken5 NPCtoken6 NPCtoken4 NPCtoken9 NPCtoken10 NPCtoken11 NPCtoken13 NPCtoken7 Quest9 NPCtoken15 NPCtoken12 NPCtoken14 NPCtoken16 NPCtoken17 NPCtoken18 NPCtoken19 NPCtoken20 NPCtoken21 NPCtoken27 NPCtoken22 NPCtoken24 NPCtoken25 NPCtoken26 NPCtoken23 NPCtoken28 NPCtoken29 NPCtoken30 NPCtoken31 NPCtoken32 NPCtoken33 NPCtoken34 NPCtoken35 NPCtoken36 NPCtoken37 NPCtoken38 NPCtoken39 NPCtoken40 NPCtoken41 BadgeI1 BadgeI2 BadgeI3 EquipmentStatues1 EquipmentStatues2 EquipmentStatues3 EquipmentStatues4 EquipmentStatues5 EquipmentStatues6 EquipmentStatues7 EquipmentStatues8 EquipmentStatues9 EquipmentStatues10 EquipmentStatues11 EquipmentStatues12 EquipmentStatues13 EquipmentStatues14 EquipmentStatues15 EquipmentStatues16 EquipmentStatues17 EquipmentStatues18 EquipmentStatues19 EquipmentStatues20 EquipmentStatues21 EquipmentStatues22 EquipmentStatues23 EquipmentStatues24 EquipmentStatues25 EquipmentStatues26 EquipmentStatues27 EquipmentStatues28 EquipmentSmithingTabs2 EquipmentSmithingTabs3 EquipmentSmithingTabs4 EquipmentSmithingTabs5 EquipmentSmithingTabs6 SmithingRecipes1 SmithingRecipes2 SmithingRecipes3 SmithingRecipes4 SmithingRecipes5 SmithingRecipes6 TalentBook1 TalentBook2 TalentBook3 TalentBook4 TalentBook5 MaxCapBagT2 MaxCapBag1 MaxCapBag2 MaxCapBag3 MaxCapBag4 MaxCapBag5 MaxCapBagMi6 MaxCapBagMi7 MaxCapBagMi8 MaxCapBagMi9 MaxCapBagMi10 MaxCapBagMi11 MaxCapBagT1 MaxCapBag7 MaxCapBag9 MaxCapBagT3 MaxCapBagT4 MaxCapBagT5 MaxCapBagT6 MaxCapBagT7 MaxCapBagT8 MaxCapBagT9 MaxCapBagT10 MaxCapBagT11 MaxCapBag6 MaxCapBag8 MaxCapBag10 MaxCapBagF3 MaxCapBagF4 MaxCapBagF5 MaxCapBagF6 MaxCapBagF7 MaxCapBagF8 MaxCapBagF9 MaxCapBagF10 MaxCapBagF11 MaxCapBagM1 MaxCapBagM2 MaxCapBagM3 MaxCapBagM4 MaxCapBagM5 MaxCapBagM6 MaxCapBagM7 MaxCapBagM8 MaxCapBagM9 MaxCapBagM10 MaxCapBagM11 MaxCapBagM12 MaxCapBagFi1 MaxCapBagFi2 MaxCapBagFi3 MaxCapBagFi4 MaxCapBagFi5 MaxCapBagFi6 MaxCapBagFi7 MaxCapBagFi8 MaxCapBagFi9 MaxCapBagFi10 MaxCapBagFi11 MaxCapBagB1 MaxCapBagB2 MaxCapBagB3 MaxCapBagB4 MaxCapBagB5 MaxCapBagB6 MaxCapBagB7 MaxCapBagB8 MaxCapBagB9 MaxCapBagB10 MaxCapBagB11 MaxCapBagTr1 MaxCapBagTr3 MaxCapBagTr4 MaxCapBagTr5 MaxCapBagTr6 MaxCapBagTr7 MaxCapBagTr8 MaxCapBagTr9 MaxCapBagTr10 MaxCapBagS1 MaxCapBagS3 MaxCapBagS4 MaxCapBagS5 MaxCapBagS6 MaxCapBagS7 MaxCapBagS8 MaxCapBagS9 MaxCapBagS10 ObolBronze0 ObolSilver0 ObolGold0 ObolPlatinum0 ObolPink0 ObolBronze1 ObolSilver1 ObolGold1 ObolPlatinum1 ObolPink1 ObolBronze2 ObolSilver2 ObolGold2 ObolPlatinum2 ObolPink2 ObolBronze3 ObolSilver3 ObolGold3 ObolPlatinum3 ObolPink3 ObolBronzeDamage ObolSilverDamage ObolGoldDamage ObolPlatinumDamage ObolPinkDamage ObolSilverMoney ObolGoldMoney ObolBronzeMining ObolSilverMining ObolGoldMining ObolPlatinumMining ObolPinkMining ObolBronzeChoppin ObolSilverChoppin ObolGoldChoppin ObolPlatinumChoppin ObolPinkChoppin ObolBronzeFishing ObolSilverFishing ObolGoldFishing ObolPlatinumFishing ObolPinkFishing ObolBronzeCatching ObolSilverCatching ObolGoldCatching ObolPlatinumCatching ObolPinkCatching ObolSilverLuck ObolGoldLuck ObolPlatinumLuck ObolPinkLuck ObolBronzePop ObolSilverPop ObolGoldPop ObolPlatinumPop ObolPinkPop ObolBronzeKill ObolSilverKill ObolGoldKill ObolPlatinumKill ObolPinkKill ObolBronzeEXP ObolSilverEXP ObolGoldEXP ObolPlatinumEXP ObolPinkEXP ObolBronzeCard ObolSilverCard ObolGoldCard ObolPlatinumCard ObolPinkCard ObolBronzeDef ObolSilverDef ObolGoldDef ObolPlatinumDef ObolPinkDef ObolBronzeTrapping ObolSilverTrapping ObolGoldTrapping ObolPlatinumTrapping ObolPinkTrapping ObolBronzeCons ObolSilverCons ObolGoldCons ObolPlatinumCons ObolPinkCons ObolBronzeWorship ObolSilverWorship ObolGoldWorship ObolPlatinumWorship ObolPinkWorship ObolFrog ObolAmarokA ObolEfauntA ObolKnight ObolSlush ObolChizoarA ObolTroll ObolLava ObolKruk ObolHyper0 ObolHyper1 ObolHyper2 ObolHyper3 ObolHyperB0 ObolHyperB1 ObolHyperB2 ObolHyperB3 StampA1 StampA2 StampA3 StampA4 StampA5 StampA6 StampA7 StampA8 StampA9 StampA10 StampA11 StampA12 StampA13 StampA14 StampA15 StampA16 StampA17 StampA18 StampA19 StampA20 StampA21 StampA22 StampA23 StampA24 StampA25 StampA26 StampA27 StampA28 StampA29 StampA30 StampA31 StampA32 StampA33 StampA34 StampA35 StampA36 StampA37 StampA38 StampA39 StampA40 StampA41 StampA42 StampB1 StampB2 StampB3 StampB4 StampB5 StampB6 StampB7 StampB8 StampB9 StampB10 StampB11 StampB12 StampB13 StampB14 StampB15 StampB16 StampB17 StampB18 StampB19 StampB20 StampB21 StampB22 StampB23 StampB24 StampB25 StampB26 StampB27 StampB28 StampB29 StampB30 StampB31 StampB32 StampB33 StampB34 StampB35 StampB36 StampB37 StampB38 StampB39 StampB40 StampB41 StampB42 StampB43 StampB44 StampB45 StampB46 StampB47 StampB48 StampB49 StampB50 StampB51 StampB52 StampB53 StampB54 StampC1 StampC2 StampC3 StampC4 StampC5 StampC6 StampC7 StampC8 StampC9 StampC10 StampC11 StampC12 StampC13 StampC14 StampC15 StampC16 StampC17 StampC18 StampC19 StampC20 StampC21 StampC22 StampC23 InvBag1 InvBag2 InvBag3 InvBag4 InvBag5 InvBag6 InvBag7 InvBag8 InvBag100 InvBag101 InvBag102 InvBag103 InvBag104 InvBag105 InvBag106 InvBag107 InvBag108 InvBag109 InvBag110 InvBag111 InvStorage1 InvStorage2 InvStorage3 InvStorage4 InvStorage5 InvStorage6 InvStorage7 InvStorage8 InvStorage9 InvStorage10 InvStorage11 InvStorage12 InvStorage13 InvStorage14 InvStorage15 InvStorage16 InvStorage17 InvStorage18 InvStorage19 InvStorage20 InvStorage21 InvStorage22 InvStorage23 InvStorage24 InvStorage25 InvStorage26 InvStorage27 InvStorage28 InvStorageF InvStorageS InvStorageC InvStorageD InvStorageN Weight1 Weight2 Weight3 Weight4 Weight5 Weight6 Weight7 Weight8 Weight9 Weight10 Weight11 Weight12 Weight13 Weight14 Line1 Line2 Line3 Line4 Line5 Line6 Line7 Line8 Line9 Line10 Line11 Line12 Line13 Line14 Ladle PetEgg Genetic0 Genetic1 Genetic2 Genetic3 CardPack1 CardPack2 CardPack3 CardPack4 CardPack5 CardPack6 CardPack7 DungCredits2 Cash XP XPskill DungEnhancer0 DungEnhancer1 DungEnhancer2 DungRNG0 DungRNG1 DungRNG2 DungRNG3 DungRNG4 DungeonA1 DungeonA2 DungeonA3 DungeonA4 DungeonA5 DungeonA6 DungeonA7 DungeonA8 KeyFrag DungCredits1 LootDice Tree7D PlatD Fish1D Fish3D Cashb Dung3Ice FoodHealth1d FoodHealth2d FoodHealth3d DungWeaponPunchA1 DungWeaponPunchA2 DungWeaponPunchA3 DungWeaponPunchA4 DungWeaponPunchA5 DungWeaponPunchB1 DungWeaponPunchB2 DungWeaponPunchB3 DungWeaponPunchB4 DungWeaponPunchB5 DungWeaponPunchC1 DungWeaponPunchC2 DungWeaponPunchC3 DungWeaponPunchC4 DungWeaponPunchC5 DungWeaponPunchD1 DungWeaponPunchD2 DungWeaponPunchD3 DungWeaponPunchD4 DungWeaponPunchD5 DungWeaponPunchE1 DungWeaponPunchE2 DungWeaponPunchE3 DungWeaponPunchE4 DungWeaponPunchE5 DungWeaponPunchF1 DungWeaponPunchF2 DungWeaponPunchF3 DungWeaponPunchF4 DungWeaponPunchF5 DungWeaponSwordA1 DungWeaponSwordA2 DungWeaponSwordA3 DungWeaponSwordA4 DungWeaponSwordA5 DungWeaponSwordB1 DungWeaponSwordB2 DungWeaponSwordB3 DungWeaponSwordB4 DungWeaponSwordB5 DungWeaponSwordC1 DungWeaponSwordC2 DungWeaponSwordC3 DungWeaponSwordC4 DungWeaponSwordC5 DungWeaponSwordD1 DungWeaponSwordD2 DungWeaponSwordD3 DungWeaponSwordD4 DungWeaponSwordD5 DungWeaponSwordE1 DungWeaponSwordE2 DungWeaponSwordE3 DungWeaponSwordE4 DungWeaponSwordE5 DungWeaponSwordF1 DungWeaponSwordF2 DungWeaponSwordF3 DungWeaponSwordF4 DungWeaponSwordF5 DungWeaponBowA1 DungWeaponBowA2 DungWeaponBowA3 DungWeaponBowA4 DungWeaponBowA5 DungWeaponBowB1 DungWeaponBowB2 DungWeaponBowB3 DungWeaponBowB4 DungWeaponBowB5 DungWeaponBowC1 DungWeaponBowC2 DungWeaponBowC3 DungWeaponBowC4 DungWeaponBowC5 DungWeaponBowD1 DungWeaponBowD2 DungWeaponBowD3 DungWeaponBowD4 DungWeaponBowD5 DungWeaponBowE1 DungWeaponBowE2 DungWeaponBowE3 DungWeaponBowE4 DungWeaponBowE5 DungWeaponBowF1 DungWeaponBowF2 DungWeaponBowF3 DungWeaponBowF4 DungWeaponBowF5 DungWeaponWandA1 DungWeaponWandA2 DungWeaponWandA3 DungWeaponWandA4 DungWeaponWandA5 DungWeaponWandB1 DungWeaponWandB2 DungWeaponWandB3 DungWeaponWandB4 DungWeaponWandB5 DungWeaponWandC1 DungWeaponWandC2 DungWeaponWandC3 DungWeaponWandC4 DungWeaponWandC5 DungWeaponWandD1 DungWeaponWandD2 DungWeaponWandD3 DungWeaponWandD4 DungWeaponWandD5 DungWeaponWandE1 DungWeaponWandE2 DungWeaponWandE3 DungWeaponWandE4 DungWeaponWandE5 DungWeaponWandF1 DungWeaponWandF2 DungWeaponWandF3 DungWeaponWandF4 DungWeaponWandF5 DungEquipmentHats0 DungEquipmentHats1 DungEquipmentHats2 DungEquipmentHats3 DungEquipmentHats4 DungEquipmentShirt0 DungEquipmentShirt1 DungEquipmentShirt2 DungEquipmentShirt3 DungEquipmentShirt4 DungEquipmentPants0 DungEquipmentPants1 DungEquipmentPants2 DungEquipmentPants3 DungEquipmentPants4 DungEquipmentShoes0 DungEquipmentShoes1 DungEquipmentShoes2 DungEquipmentShoes3 DungEquipmentShoes4 DungEquipmentPendant0 DungEquipmentPendant1 DungEquipmentPendant2 DungEquipmentPendant3 DungEquipmentPendant4 DungEquipmentRings0 DungEquipmentRings1 DungEquipmentRings2 DungEquipmentRings3 DungEquipmentRings4"
slabList = slabString.split(' ')
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
