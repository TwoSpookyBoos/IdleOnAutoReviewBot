import math
import yaml
from pathlib import Path
from utils.logging import get_logger
from utils.text_formatting import getItemDisplayName
from config import app

logger = get_logger(__name__)

with open(Path(app.static_folder) / 'items.yaml', 'r') as f:
    items_codes_and_names = yaml.load(f, yaml.Loader)

###GENERAL PROGRESSION TIERS###
combatLevels_progressionTiers = [
    # int tier, int TotalAccountLevel, str TAL reward, int PlayerLevels, str PL reward, str notes
    [0, 0, "", 0, "", ""],
    [1, 8, "Character 2", 25, "Personal - Circle Obol Slot 2", ""],
    [2, 30, "Character 3", 32, "Personal - Square Obol Slot 1", ""],
    [3, 60, "Family - Circle Obol Slot 1", 40, "Personal - Circle Obol Slot 3", ""],
    [4, 70, "Character 4 and Family - Circle Obol Slot 1", 48, "Personal - Circle Obol Slot 4", ""],
    [5, 80, "Family - Circle Obol Slot 2", 60, "Personal - Square Obol Slot 2", ""],
    [6, 100, "Family - Circle Obol Slot 3", 70, "Personal - Circle Obol Slot 5", ""],
    [7, 150, "Character 5", 80, "Personal - Circle Obol Slot 6", ""],
    [8, 160, "Family - Circle Obol Slot 4", 90, "Personal - Square Obol Slot 3", ""],
    [9, 200, "Family - Square Obol Slot 1", 98, "Personal - Circle Obol Slot 7", ""],
    [10, 250, "Family - Circle Obol Slot 5", 105, "Personal - Hexagon Obol Slot 1", ""],
    [11, 300, "Character 6", 112, "Personal - Circle Obol Slot 8", ""],
    [12, 350, "Family - Circle Obol Slot 6", 120, "Personal - Square Obol Slot 4", ""],
    [13, 400, "Family - Circle Obol Slot 7 and Family - Hexagon Obol Slot 1", 130, "Personal - Circle Obol Slot 9", ""],
    [14, 470, "Family - Circle Obol Slot 8", 140, "Personal - Square Obol Slot 5", ""],
    [15, 500, "Character 7", 150, "Vman Quest, if class = Mman", ""],
    [16, 650, "Family - Sparkle Obol Slot 1", 152, "Personal - Circle Obol Slot 10", ""],
    [17, 700, "Family - Square Obol Slot 2", 170, "Personal - Circle Obol Slot 11", ""],
    [18, 750, "Character 8", 180, "Personal - Hexagon Obol Slot 2", ""],
    [19, 875, "Family - Circle Obol Slot 9", 190, "Personal - Square Obol Slot 6", ""],
    [20, 900, "Family - Hexagon Obol Slot 2", 210, "Personal - Circle Obol Slot 12", ""],
    [21, 1100, "Character 9", 250, "Personal - Sparkle Obol Slot 1 and Credit towards Equinox Dream 11", ""],
    [22, 1150, "Family - Square Obol Slot 3", 425, "Able to equip The Divine Scarf", ""],
    [23, 1200, "Family - Sparkle Obol Slot 2", 450, "Able to equip One of the Divine Trophy", ""],
    [24, 1250, "Family - Circle Obol Slot 10", 500, "Credit towards Equinox Dream 23", ""],
    [25, 1500, "Character 10 and Family - Circle Obol Slot 11", 500, "Credit towards Equinox Dream 23", ""],
    [26, 1750, "Family - Hexagon Obol Slot 3", 500, "Credit towards Equinox Dream 23", ""],
    [27, 2000, "Family - Square Obol Slot 4", 500, "Credit towards Equinox Dream 23",  ""],
    [28, 2100, "Family - Circle Obol Slot 12", 500, "Credit towards Equinox Dream 23", ""],
    [29, 2500, "Family - Sparkle Obol Slot 3", 500, "Credit towards Equinox Dream 23", ""],
    [30, 3000, "Family - Hexagon Obol Slot 4", 500, "Credit towards Equinox Dream 23", ""],
    [31, 5000, "Family - Sparkle Obol Slot 4", 500, "Credit towards Equinox Dream 23", ""],
    [32, 5300, "Unlock all Tome challenges", 500, "Credit towards Equinox Dream 23", ""]
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
        'Conjuror Pts': 1,
        'Instagrow Generator': 3, 'Shroom Familiar': 1, 'Plot of Land': 2},
     ""],
    [4, "B", {
        'Item Backpack Space': 2, 'Storage Chest Space': 8, 'Carry Capacity': 4, 'Weekly Dungeon Boosters': 2, 'Food Slot': 1,
        'Bleach Liquid Cauldrons': 3, 'More Sample Spaces': 2, 'Zen Cogs': 4, 'Tower Building Slots': 2,
        'Royal Egg Cap': 5, 'Fenceyard Space': 2, 'Chest Sluggo': 6, 'Lava Sprouts': 4,
        'Parallel Villagers The Engineer': 1, 'Parallel Villagers The Conjuror': 1, 'Conjuror Pts': 3,
        'Plot of Land': 4, 'Instagrow Generator': 5},
     ""],
    [5, "C", {
        'Item Backpack Space': 3, 'Storage Chest Space': 12, 'Carry Capacity': 6, 'Weekly Dungeon Boosters': 3, 'Food Slot': 2,
        'Bleach Liquid Cauldrons': 4, 'More Sample Spaces': 4, 'Tower Building Slots': 4,
        'Fenceyard Space': 4, 'Chest Sluggo': 9, 'Golden Sprinkler': 2, 'Lava Sprouts': 6,
        'Parallel Villagers The Explorer': 1, 'Parallel Villagers The Measurer': 1, 'Resource Boost': 2, 'Conjuror Pts': 6,
        'Plot of Land': 6, 'Shroom Familiar': 2, 'Instagrow Generator': 7},
     ""],
    [6, "D", {
        'Item Backpack Space': 4, 'Carry Capacity': 8, 'More Storage Space': 5, 'Brimstone Forge Slot': 8,
        'Ivory Bubble Cauldrons': 4, 'More Sample Spaces': 6, 'Zen Cogs': 8,
        'Souped Up Tube': 3, 'Fenceyard Space': 6, 'Chest Sluggo': 12,
        'Resource Boost': 4, 'Conjuror Pts': 12, 'Opal': 8,
        'Plot of Land': 8, 'Instagrow Generator': 8,
    },
     ""],
    [7, "Practical Max", {
        'Item Backpack Space': 6, 'Carry Capacity': 10, 'More Storage Space': 10, 'Card Presets': 1,
        'Brimstone Forge Slot': 16, 'Sigil Supercharge': 10,
        'Fluorescent Flaggies': 2, 'Burning Bad Books': 4,
        'Golden Sprinkler': 4, 'Divinity Sparkie': 6,
        'Resource Boost': 10, 'Conjuror Pts': 12, 'Opal': 20,
        'Parallel Villagers The Engineer': 1, 'Parallel Villagers The Conjuror': 1, 'Parallel Villagers The Explorer': 1, 'Parallel Villagers The Measurer': 1,
        'Plot of Land': 12, 'Shroom Familiar': 6,
    },
     "I wouldn't recommend going any further as of v2.26."],
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
        #Caverns
        'Resource Boost': 10, 'Conjuror Pts': 12, 'Opal': 20,
        #World 6
        'Plot of Land': 12, 'Shroom Familiar': 6, 'Instagrow Generator': 8,
     },
     "This final tier is for the truly depraved. Many of these bonuses are very weak or outright useless."]
]
greenstack_item_difficulty_groups = {
        0: {  # The timegated tier
            "Vendor Shops": [
                "CraftMat3",  # W1 Cue Tape
                "FoodPotRe2", "FoodHealth4", "Quest19",  # W2
                "FoodHealth9", "FoodHealth11", "FoodPotGr3",  #W3
                "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4",  #W4
                "FoodHealth14", "FoodHealth15", "OilBarrel6",  #W5
                "FoodHealth16", "FoodHealth17", "OilBarrel7",  #W6
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
                "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2", "GalaxyC3", "GalaxyC4"],
            "Crystal Enemy Drops": [
                "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1"],
            "Other Skilling Resources": [
                "CraftMat11",
                "Critter5",
                "Soul4",],
            },
        8: {
            "Base Monster Materials": [
                "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5",
                "SpiA1", "SpiA2",
            ],
            "Crystal Enemy Drops": [
                "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3",],
            "Other Skilling Resources": [
                "CraftMat12",
                "Critter6", "Critter7",
                "Soul5",],
            },
        9: {
            "Base Monster Materials": [
                "LavaB6", "LavaC1", "LavaC2",  #Can beat Kruk and move to W6 without fighting these
                "SpiA3", "SpiA4", "SpiA5", "SpiB1", "SpiB2", "SpiB3", "SpiB4", "SpiC1", "SpiC2",],
            "Crystal Enemy Drops": [
                "FoodHealth10", "FoodPotOr3", "FoodPotYe2", ],
            "Other Skilling Resources": [
                "CraftMat13", "CraftMat14",
                "Critter8", "Critter9",
                "Soul6",],
            },
        10: {
            "Base Monster Materials": [
                 "SpiD1", "SpiD2", "SpiD3",],
            "Crystal Enemy Drops": [
                "Leaf2",
                "Leaf3",
                "FoodPotMana4", "Leaf4",
                "FoodPotYe5", "Leaf5",
                "Leaf6",],
            "Printable Skilling Resources": [],
            "Other Skilling Resources": [
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
            "Crystal Enemy Drops": [
                "FoodPotOr1",
            ],
            "Other Skilling Resources": [
                "PlatBar",
                "Critter10", "Critter11",
            ],
            },
        12: {
            "Missable Quest Items": ["GoldricP1", "GoldricP2", "GoldricP3", "Quest21"],
            "Base Monster Materials": ["Sewers3"],
            "Crystal Enemy Drops": [
                "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",
                ],
            "Other Skilling Resources": [
                "GoldBar", "DementiaBar", "VoidBar", "LustreBar",
                "Peanut", "Quest68", "Bullet3", "FoodChoppin1",],  #I really hate that the Slush Bucket is listed as Quest68
            "Rare Drops": ["FoodPotRe1",],
            },
        13: {
            "Base Monster Materials": [
                "Quest15", "Hgg"],
            "Crystal Enemy Drops": [
                "EquipmentStatues1", "EquipmentStatues5",  #Power and Health statues are still more common than W2 statues
                "EquipmentStatues10", "EquipmentStatues12", "EquipmentStatues13", "EquipmentStatues8", "EquipmentStatues11",  #W2 statues
                "EquipmentStatues18",  #W3 EhExPee statue
                "rtt0",
                "StoneA1", "StoneW1", "StoneZ1", "StoneT1",
                "StoneZ2", "StoneT2",
                "PureWater",
                "FoodG9",],
            "Other Skilling Resources": [
                "StarfireBar", "DreadloBar",
                "EquipmentSmithingTabs2",
                'EquipmentSmithingTabs3',
                "PeanutG",
            ],
            "Rare Drops": [
                "FoodPotMana3", "ButterBar", "EquipmentStatues9", "OilBarrel2", "FoodPotRe2", "FoodPotGr3", "FoodHealth9",
            ],
        },
        14: {
            "Crystal Enemy Drops": [
                "StoneW2", 'ResetFrag', "SilverPen"],  #"StoneA2",],
            "Other Skilling Resources": [
                "MarbleBar", "GodshardBar",
                "FoodTrapping1", "FoodWorship1",
                "Critter1A", "Critter2A", "Critter3A", "Critter4A", "Critter5A", "Critter6A", "Critter7A", "Critter8A", "Critter9A", "Critter10A", "Critter11A",
                "Ladle",
            ],
            "Rare Drops": [
                "DesertC2b", "Quest78", "EfauntDrop1"
            ]
        },
    }
greenstack_progressionTiers = {
    1: {'Dream Number': 1, 'Required Stacks': 20},
    2: {'Dream Number': 12, 'Required Stacks': 75},
    3: {'Dream Number': 29, 'Required Stacks': 200},
}
achievements_progressionTiers = {
    0: {},
    1: {
        'EZ Access': {
            'Super Cereal': {'World': 2, 'Reward': 'W2 Colo and Shops', 'Rating': ''},
        },
        #'Free Teleports': {},
        'Monster Respawn': {},
        'Recipes': {},
        'Dungeon RNG Items': {
            '2 Tons of Iron': {'World': 1, 'Reward': 'Golden Dice', 'Rating': ''},
        },
        'Other Nice Rewards': {
            'Golden Fly': {'World': 2, 'Reward': '5% Catching Efficiency', 'Rating': ''},
        },
    },
    2: {
        'EZ Access': {
            'Platinum 200G': {'World': 1, 'Reward': 'W1 Key', 'Rating': ''},
            'Half a Mill-log': {'World': 1, 'Reward': 'W1 Colo and Shops', 'Rating': ''},
            'Skill Master': {'World': 2, 'Reward': 'W2 Key', 'Rating': ''},
            'Cool Score!': {'World': 3, 'Reward': 'W3 Colo and Shop', 'Rating': ''},
        },
        # 'Free Teleports': {
        #     'Nice Fur Suit': {'World': 1, 'Reward': 'Free Teleport to Encroaching Forest Villas / Wode Boards / Amarok', 'Rating': ''},
        #     "Million Null 'n Void": {'World': 1, 'Reward': 'Free Teleport to Echoing Egress / Void Ore', 'Rating': ''},
        # },
        'Monster Respawn': {},
        'Recipes': {
            'Based Roots': {'World': 1, 'Reward': 'Acorn Hat', 'Rating': ''},
        },
        'Dungeon RNG Items': {
            'House Flipper': {'World': 1, 'Reward': 'Horn of the Foal', 'Rating': ''},
            "Croakin' Froge": {'World': 3, 'Reward': 'Plump Dice', 'Rating': ''},
        },
        'Other Nice Rewards': {
            'Cog in the System': {'World': 3, 'Reward': '5% cons build speed', 'Rating': ''},
        },
    },
    3: {
        'EZ Access': {
            'Top Cogs': {'World': 3, 'Reward': 'W3 Key', 'Rating': ''},
            'Good Plate': {'World': 4, 'Reward': 'W4 Shop', 'Rating': ''},

        },
        # 'Free Teleports': {
        #     'Your Skin, My Skin': {'World': 2, 'Reward': 'Free Teleport to Djonnuttown / Snelbies / Efaunt', 'Rating': ''},
        # },
        'Monster Respawn': {
            'Two-Time Savior': {'World': 1, 'Reward': '5% Mob Respawn in W1', 'Rating': ''},

        },
        'Recipes': {
            'Nuget Nightmare': {'World': 2, 'Reward': 'Nuget Cake Hat', 'Rating': ''},
            'The Goose is Loose': {'World': 3, 'Reward': 'HONK Hat', 'Rating': ''},
        },
        'Dungeon RNG Items': {
            'Souped Up Salts': {'World': 3, 'Reward': 'RNG Voucher', 'Rating': ''},

        },
        'Other Nice Rewards': {
            'Golden Obolden!': {'World': 2, 'Reward': '+20% Obol Frags', 'Rating': ''},
            'Ink Blot': {'World': 2, 'Reward': '20% non-consume Silver Pen', 'Rating': ''},
            'Vial Junkee': {'World': 2, 'Reward': '20% Sigil Speed', 'Rating': ''},
            'Fruit Salad': {'World': 2, 'Reward': '5% catching speed', 'Rating': ''},
            'Checkout Takeout': {'World': 3, 'Reward': '+5 Book max level', 'Rating': ''},
            'Shiny Shells': {'World': 4, 'Reward': '10% Breeding Incubator Speed', 'Rating': ''},
            'Cabbage Patch': {'World': 4, 'Reward': '10% Meal Cooking Speed', 'Rating': ''},
            'Le Pretzel Bleu': {'World': 4, 'Reward': '20% Meal Cooking Speed', 'Rating': ''},
            'Best Plate': {'World': 4, 'Reward': '10% cheaper Kitchen upgrades', 'Rating': ''},
        },
    },
    4: {
        'EZ Access': {
            'Bonsai Bonanza': {'World': 5, 'Reward': 'W5 Shop', 'Rating': ''},
        },
        #'Free Teleports': {},
        'Monster Respawn': {

            'Lavathian Skulls': {'World': 5, 'Reward': '2% Mob Respawn in W5', 'Rating': ''},
        },
        'Recipes': {},
        'Dungeon RNG Items': {},
        'Other Nice Rewards': {
            'The Plateauourist': {'World': 5, 'Reward': '+4 Daily Crystals', 'Rating': ''},
            'Artifact Finder': {'World': 5, 'Reward': '+1 Sailing Loot Pile', 'Rating': ''},
            'Gilded Vessel': {'World': 5, 'Reward': '+1 Sailing Loot Pile', 'Rating': ''},
            'True Naval Captain': {'World': 5, 'Reward': '20% Sailing EXP', 'Rating': ''},
            'Grand Captain': {'World': 5, 'Reward': '20% Sailing EXP', 'Rating': ''},
            'Voraci Vantasia': {'World': 5, 'Reward': '+10% Divinity Points', 'Rating': ''},
            'Legendary Wormhole': {'World': 5, 'Reward': '+10% Divinity Points', 'Rating': ''},
            'All Hail Purrmep': {'World': 5, 'Reward': '+10 Particle clicks daily', 'Rating': ''},
            'Lucky Harvest': {'World': 5, 'Reward': '1.05x Bit Gain', 'Rating': ''},
            'Broken Controller': {'World': 5, 'Reward': '1.05x Bit Gain', 'Rating': ''},
            'Vitamin D-licious': {'World': 5, 'Reward': '+50% Forge Ore Capacity', 'Rating': ''},
            'Maroon Warship': {'World': 5, 'Reward': '+1 Level to all talents', 'Rating': ''},
            'Sneaky Stealing': {'World': 5, 'Reward': '25% Shop Capacity', 'Rating': ''},
        },
    },
    5: {
        'EZ Access': {
            'Doctor Repellant': {'World': 6, 'Reward': 'W6 Shop', 'Rating': ''},
        },
        #'Free Teleports': {},
        'Monster Respawn': {
            'Two Desserts!': {'World': 2, 'Reward': '5% Mob Respawn in W2', 'Rating': ''},
        },
        'Recipes': {},
        'Dungeon RNG Items': {'Mutant Massacrer': {'World': 4, 'Reward': 'Coin Flip', 'Rating': ''}},  #Steam only
        'Other Nice Rewards': {
            'Gilded Shells': {'World': 4, 'Reward': '1.1x Egg Rarity chance', 'Rating': ''},
            'Perfect Trade Deal': {'World': 5, 'Reward': '+1 Treasure per Chest', 'Rating': ''},
            "Lil' Overgrowth": {'World': 6, 'Reward': '1.05x Crop Evo', 'Rating': ''},
            'Big Time Land Owner': {'World': 6, 'Reward': '1.15x Crop OG', 'Rating': ''},
            'Crop Flooding': {'World': 6, 'Reward': '5% Magic Beans', 'Rating': ''},
            'Ceramic Sneaking': {'World': 6, 'Reward': '1.03x Jade', 'Rating': ''},
            'Lucky Stealy': {'World': 6, 'Reward': '1.05x Jade', 'Rating': ''},
            'Top Floor Sneaking': {'World': 6, 'Reward': '1.07x Jade', 'Rating': ''},
            'Untying Extraordinaire': {'World': 6, 'Reward': '1.05x Stealth', 'Rating': ''},
            'Best Bloomie': {'World': 6, 'Reward': '1.05x Essence', 'Rating': ''},
            'Spectre Stars': {'World': 6, 'Reward': '1% Larger Winner bonuses', 'Rating': ''},
            'Regalis My Beloved': {'World': 6, 'Reward': '1% Larger Winner bonuses', 'Rating': ''},
            "Scorin' the Ladies": {'World': 6, 'Reward': '10% Catch Eff', 'Rating': ''},
            'Effervess Enthusiess': {'World': 6, 'Reward': '10% Chop Eff', 'Rating': ''},
            'Summoning GM': {'World': 6, 'Reward': '6% Drop Rate', 'Rating': ''},
            'Big Big Hampter': {'World': 6, 'Reward': '4% Drop Rate', 'Rating': ''},
        },
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
        "Skill": ["Lil' Mining Baggy Stamp"],
        "Optional": ["Clover Stamp"]}},
    5: {"TotalStampLevels": 250, "Stamps": {
        "Combat": ["Longsword Stamp"],
        "Skill": ["Anvil Zoomer Stamp", "Matty Bag Stamp"],
        "Optional": ["Kapow Stamp"]}},
    6: {"TotalStampLevels": 300, "Stamps": {}},
    7: {"TotalStampLevels": 400, "Stamps": {
        "Skill": ["Fishing Rod Stamp", "Catch Net Stamp"],
        "Specific": {'Pickaxe Stamp': 35, 'Hatchet Stamp': 35}}},
    8: {"TotalStampLevels": 500, "Stamps": {
        "Combat": ["Battleaxe Stamp", "Scimitar Stamp", "Bullseye Stamp"],
        "Skill": ["Drippy Drop Stamp"],
        "Misc": ["Biblio Stamp"],
        "Specific": {'Drippy Drop Stamp': 30},
        "Optional": ["Hermes Stamp", "Talent III Stamp"]}},
    9: {"TotalStampLevels": 600, "Stamps": {
        "Misc": ["Crystallin", "Talent S Stamp"]}},
    10: {"TotalStampLevels": 700, "Stamps": {
        "Combat": ["Polearm Stamp", "Buckler Stamp", "Stat Graph Stamp"],
        "Skill": ["Twin Ores Stamp", "Duplogs Stamp", "Cool Diggy Tool Stamp", "Swag Swingy Tool Stamp", "Alch Go Brrr Stamp",
                  "Droplots Stamp", "Bugsack Stamp", "Hidey Box Stamp", "Spikemouth Stamp", "Purp Froge Stamp"],
        "Specific": {'Drippy Drop Stamp': 40, 'Matty Bag Stamp': 30}}},
    11: {"TotalStampLevels": 800, "Stamps": {
         "Skill": ["Stample Stamp", "Spice Stamp", "Egg Stamp"],
         "Misc": ["Mason Jar Stamp", "Sigil Stamp"],
         "Specific": {'Pickaxe Stamp': 45, 'Hatchet Stamp': 45, 'Mason Jar Stamp': 12}}},
    12: {"TotalStampLevels": 1000, "Stamps": {
        "Skill": ["Brainstew Stamps", "Bag o Heads Stamp", "Skelefish Stamp", "Holy Mackerel Stamp", "Cooked Meal Stamp"],
        "Misc": ["Card Stamp"],
        "Specific": {
            'Drippy Drop Stamp': 50,
            'Pickaxe Stamp': 55, 'Hatchet Stamp': 55, 'Card Stamp': 50
        },
        "Optional": ["Saw Stamp", "Agile Stamp", "Book Stamp", "Smart Dirt Stamp", "High IQ Lumber Stamp", "Fishhead Stamp", "Fly Intel Stamp", "Talent II Stamp"]
    }},
    13: {"TotalStampLevels": 2500, "Stamps": {
        "Combat": ["Avast Yar Stamp", "Blackheart Stamp", "Steve Sword",],
        "Skill": ["Banked Pts Stamp", "Nest Eggs Stamp", "Lab Tube Stamp", "Ladle Stamp", "Sailboat Stamp"],
        "Misc": ["Refinery", "Golden Apple Stamp"],
        "Specific": {
            'Matty Bag Stamp': 100, 'Crystallin': 60,
            'Pickaxe Stamp': 65, 'Hatchet Stamp': 65, 'Card Stamp': 100,
            'Golden Apple Stamp': 28
        },
        "Optional": ["Arcane Stamp", "Gilded Axe Stamp", "DNA Stamp"]
    }},
    14: {"TotalStampLevels": 4000, "Stamps": {
        "Combat": ["Diamond Axe Stamp", "Sashe Sidestamp"],
        "Skill": ["Gamejoy Stamp", "Divine Stamp"],
        "Misc": ["Potion Stamp", "Questin Stamp"],
        "Specific": {
            'Bugsack Stamp': 80, 'Bag o Heads Stamp': 80, 'Pickaxe Stamp': 75, 'Hatchet Stamp': 75,
            'Drippy Drop Stamp': 90, 'Crystallin': 100,
        },
        "Optional": ["Feather Stamp"],
    }},
    15: {"TotalStampLevels": 5500, "Stamps": {
        "Combat": ["Tripleshot Stamp", "Maxo Slappo Stamp"],
        "Skill": ["Crop Evo Stamp", "Buzz Buzz Stamp"],
        "Misc": ["Multikill Stamp"],
        "Specific": {
            'Matty Bag Stamp': 150, 'Card Stamp': 150, 'Ladle Stamp': 100, 'Potion Stamp': 20,
            'Pickaxe Stamp': 85, 'Hatchet Stamp': 85, 'Mason Jar Stamp': 52, 'Golden Apple Stamp': 40, 'Crop Evo Stamp': 20,
        },
        "Optional": ["Void Sword Stamp"]
    }},
    16: {"TotalStampLevels": 7500, "Stamps": {
        "Combat": ["Violence Stamp", "Intellectostampo", "Dementia Sword Stamp"],
        "Skill": ["Multitool Stamp", "Flowin Stamp", "Sneaky Peeky Stamp", "Jade Mint Stamp", "White Essence Stamp"],
        "Misc": ["Forge Stamp"],
        "Specific": {
            'Matty Bag Stamp': 200, 'Crystallin': 150,
            'Bugsack Stamp': 120, 'Bag o Heads Stamp': 120, 'Multitool Stamp': 100,
            'Drippy Drop Stamp': 100, 'Potion Stamp': 40, 'Golden Apple Stamp': 60,
            'Pickaxe Stamp': 95, 'Hatchet Stamp': 95, 'Ladle Stamp': 180, 'Forge Stamp': 100
        },
        "Optional": ["Blover Stamp"]
    }},
    17: {"TotalStampLevels": 9200, "Stamps": {
        "Combat": ["Conjocharmo Stamp", 'Captalist Stats Stamp'],
        "Skill": ["Dark Triad Essence Stamp"],
        "Misc": ["Atomic Stamp"],
        "Specific": {
            'Mason Jar Stamp': 80, 'Bugsack Stamp': 168, 'Bag o Heads Stamp': 168, 'Multitool Stamp': 210,
            'Pickaxe Stamp': 105, 'Hatchet Stamp': 105,
            'Drippy Drop Stamp': 110, 'Potion Stamp': 60,
            'Card Stamp': 200,
        }
    }},
    18: {"TotalStampLevels": 11000, "Stamps": {
        "Specific": {
            'Mason Jar Stamp': 88, 'Matty Bag Stamp': 280, 'Crystallin': 250,
            'Golden Apple Stamp': 100,
        }
    }},
    19: {"TotalStampLevels": 13000, "Stamps": {
        "Combat": ["Golden Sixes Stamp", "Stat Wallstreet Stamp"],
        "Skill": ["Amplestample Stamp", "Triad Essence Stamp", "Summoner Stone Stamp"],
        "Specific": {
            'Golden Sixes Stamp': 120,
            'Maxo Slappo Stamp': 98, 'Sashe Sidestamp': 98, 'Intellectostampo': 98,
            'Mason Jar Stamp': 92, "Matty Bag Stamp": 320, 'Crystallin': 260,
            'Triad Essence Stamp': 80, 'Forge Stamp': 220
        },
        "Optional": ["Sukka Foo", "Void Axe Stamp"]
    }},
    20: {"TotalStampLevels": 13000, "Stamps": {
        "Specific": {
            "Mason Jar Stamp": 96, "Matty Bag Stamp": 380, 'Crystallin': 270,
            "Lil' Mining Baggy Stamp": 280, 'Forge Stamp': 230, 'Summoner Stone Stamp': 120, 'Drippy Drop Stamp': 155,
            "Choppin' Bag Stamp": 300, 'Intellectostampo': 161, 'Maxo Slappo Stamp': 133,
            'Cool Diggy Tool Stamp': 280, 'Swag Swingy Tool Stamp': 360, 'Golden Apple Stamp': 112,
            'Hatchet Stamp': 295, 'Pickaxe Stamp': 255,
            'Sashe Sidestamp': 126,  'Conjocharmo Stamp': 170,
            'Captalist Stats Stamp': 140,
            'Anvil Zoomer Stamp': 125, 'Skelefish Stamp': 32, 'Fishing Rod Stamp': 120, 'Catch Net Stamp': 120, 'Divine Stamp': 120,
            'White Essence Stamp': 104, 'Triad Essence Stamp': 112, 'Dark Triad Essence Stamp': 96, 'Nest Eggs Stamp': 240,
        },
    }},
    21: {"TotalStampLevels": 13000, "Stamps": {"Specific": {},}},  # Info tier for Capacity stamps, populated later from stamp_maxes
    22: {"TotalStampLevels": 13000, "Stamps": {"Specific": {},}},  # Info tier for all other previously tiered stamps, populated later from stamp_maxes
    23: {"TotalStampLevels": 13000, "Stamps": {"Specific": {},}},  # Info tier for all non-tiered stamps, populated later from stamp_maxes
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
        "MegaFeathersOwned": 1,
    },
    2: {
        "MegaFeathersOwned": 9,
    },
    3: {
        "MegaFeathersOwned": 17,
        "BonusesOfOrion": 23
    },
    4: {
        "MegaFeathersOwned": 24,
        "BonusesOfOrion": 29
    },
}
starsigns_progressionTiers = {
    0: {
        "UnlockedSigns": 0,
        "SpecificSigns": [],
        "Goal": "",
    },
    1: {
        "UnlockedSigns": 13,
        "SpecificSigns": ["Chronus Cosmos"],
        "Goal": "The Chronus Cosmos sign"
    },
    2: {
        "UnlockedSigns": 24,
        "SpecificSigns": ["Pie Seas", "Shoe Fly"],
        "Goal": "The Hydron tab",
    },
    3: {
        "UnlockedSigns": 32,
        "SpecificSigns": ["Hydron Cosmos"],
        "Goal": "The Hydron Cosmos sign"
    },
    4: {
        "UnlockedSigns": 58,
        "SpecificSigns": ["The Forsaken"],
        "Goal": "The Seraph tab"
    },
    5: {
        "UnlockedSigns": 64,
        "SpecificSigns": ["Seraph Cosmos"],
        "Goal": "The Seraph Cosmos sign"
    },
    6: {
        "UnlockedSigns": 0,
        "SpecificSigns": [
            #Chronus signs that could have been skipped previously but are good
            "Blue Hedgehog", "Gum Drop", "The OG Skiller", "Mr No Sleep",
            #Hydron
            "Trapezoidburg", "Preys Bea", "Gum Drop Major", "The Overachiever", "Divividov",
            # Seraph
            "Damarian Major",  #Left-most branch
            "Killian Maximus",  #Left-inner branch
        ],
        "Goal": "The rest of the notable signs"
    },  #Go back and unlock the rest of the good stuff
}
statues_progressionTiers = {
    0: {},
    1: {"SpecificLevels": {
        "Power Statue": 20, "Speed Statue": 20, "Mining Statue": 20, "Feasty Statue": 20, "Health Statue": 20, "Lumberbob Statue": 20,
        "Ol Reliable Statue": 20, "Exp Book Statue": 20, "Anvil Statue": 20, "Cauldron Statue": 20,
        "Beholder Statue": 20,
        "Pecunia Statue": 20, "Mutton Statue": 20, "Egg Statue": 20,
    },},
    2: {"MinStatueTypeNumber": 1, "MinStatueType": "Gold", 'SpecificTypes': [
        'Power Statue', 'Speed Statue', 'Mining Statue', 'Feasty Statue', 'Health Statue', 'Kachow Statue', 'Lumberbob Statue',
        'Thicc Skin Statue', 'Oceanman Statue', 'Ol Reliable Statue', 'Exp Book Statue', 'Anvil Statue', 'Cauldron Statue',
        'Beholder Statue', 'Bullseye Statue',
        'Box Statue', 'Twosoul Statue', 'EhExPee Statue', 'Seesaw Statue',
        'Pecunia Statue', 'Mutton Statue', 'Egg Statue',
        'Battleaxe Statue', 'Spiral Statue', 'Boat Statue',
        'Compost Statue', 'Stealth Statue', 'Essence Statue'
    ],},
    3: {"MinStatueTypeNumber": 2, "MinStatueType": "Onyx", 'SpecificTypes': [
        'Power Statue', 'Speed Statue', 'Mining Statue', 'Feasty Statue', 'Health Statue', 'Lumberbob Statue',
        'Ol Reliable Statue', 'Exp Book Statue', 'Anvil Statue', 'Cauldron Statue',
        'Beholder Statue',
        'Pecunia Statue', 'Mutton Statue', 'Egg Statue'
    ],},
    4: {"MinStatueTypeNumber": 2, "MinStatueType": "Onyx", 'SpecificTypes': [
        'Thicc Skin Statue',
        'EhExPee Statue',
        'Battleaxe Statue', 'Spiral Statue', 'Boat Statue',
        'Compost Statue', 'Stealth Statue', 'Essence Statue'
    ],},
    5: {"MinStatueTypeNumber": 2, "MinStatueType": "Onyx", 'SpecificTypes': [
        'Kachow Statue', 'Oceanman Statue', 'Bullseye Statue',
        'Box Statue', 'Twosoul Statue', 'Seesaw Statue'
    ],},
    6: {'SpecificLevels': {
        'Power Statue': 40, 'Speed Statue': 40, 'Mining Statue': 40, 'Feasty Statue': 40, 'Health Statue': 40, 'Lumberbob Statue': 40,
        'Oceanman Statue': 40, 'Ol Reliable Statue': 40, 'Exp Book Statue': 40, 'Anvil Statue': 40, 'Cauldron Statue': 40,
        'Beholder Statue': 40, 'Box Statue': 40, 'Twosoul Statue': 40, 'Seesaw Statue': 40, 'EhExPee Statue': 40,
        'Pecunia Statue': 40, 'Mutton Statue': 40, 'Egg Statue': 40,
        'Battleaxe Statue': 40, 'Spiral Statue': 40, 'Boat Statue': 40,
        'Compost Statue': 40, 'Stealth Statue': 40, 'Essence Statue': 40,
    },},
    7: {'SpecificLevels': {
        'Mining Statue': 150, 'Feasty Statue': 150, 'Lumberbob Statue': 150,
    },},
    8: {'SpecificLevels': {
        'Mining Statue': 200, 'Feasty Statue': 200, 'Lumberbob Statue': 200,
    },},
    9: {'SpecificLevels': {
        'Mining Statue': 240, 'Feasty Statue': 240, 'Lumberbob Statue': 240,
    },},
    10: {'SpecificLevels': {
        'Speed Statue': 80,
        'Oceanman Statue': 80, 'Ol Reliable Statue': 80, 'Anvil Statue': 80, 'Cauldron Statue': 80,
        'Beholder Statue': 80, 'EhExPee Statue': 80,
        'Pecunia Statue': 80, 'Mutton Statue': 80, 'Egg Statue': 80,
        'Battleaxe Statue': 80, 'Spiral Statue': 80, 'Boat Statue': 80,
        'Compost Statue': 80, 'Stealth Statue': 80, 'Essence Statue': 80,
    },},
    11: {"MinStatueTypeNumber": 2, "MinStatueType": "Onyx", 'SpecificTypes': [
        'Dragon Warrior Statue'
    ],
         'SpecificLevels': {
        'Mining Statue': 280, 'Feasty Statue': 280, 'Lumberbob Statue': 280, 'Dragon Warrior Statue': 150,
        },
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
     {'Fmj': 10, 'Shaquracy': 10, 'Prowesessary': 15, 'Hammer Hammer': 14, 'All For Kill': 25, "Name I Guess": 10},
     "20% max value",
     "MINIMUM recommended Utility bubbles for starting W3. Prowess hard-caps at 2x."],
    [3, 40,
     {'Roid Ragin': 67, 'Warriors Rule': 34, 'Hearty Diggy': 67, 'Wyoming Blood': 20, 'Sploosh Sploosh': 20, 'Stronk Tools': 47},
     {'Swift Steppin': 67, 'Archer Or Bust': 34, 'Sanic Tools': 47, 'Bug^2': 20},
     {'Stable Jenius': 67, 'Mage Is Best': 34, 'Hocus Choppus': 67, 'Molto Loggo': 20, 'Le Brain Tools': 47},
     {'Fmj': 15, 'Shaquracy': 15, 'Prowesessary': 40, 'Hammer Hammer': 41, 'All For Kill': 67, "Name I Guess": 20},
     "40% max value",
     "MINIMUM recommended Utility bubbles for starting W4. Prowess hard-caps at 2x."],
    [4, 60,
     {'Roid Ragin': 100, 'Warriors Rule': 50, 'Hearty Diggy': 100, 'Wyoming Blood': 30, 'Sploosh Sploosh': 30, 'Stronk Tools': 70},
     {'Swift Steppin': 100, 'Archer Or Bust': 50, 'Sanic Tools': 70, 'Bug^2': 30},
     {'Stable Jenius': 100, 'Mage Is Best': 50, 'Hocus Choppus': 100, 'Molto Loggo': 30, 'Le Brain Tools': 70},
     {'Fmj': 20, 'Shaquracy': 20, 'Prowesessary': 60, 'Hammer Hammer': 65, 'All For Kill': 100, "Name I Guess": 30},
     "50% max value",
     "MINIMUM recommended Utility bubbles for starting W5. Prowess hard-caps at 2x, which you should be reaching now!"],
    [5, 80,
     {'Roid Ragin': 150, 'Warriors Rule': 75, 'Hearty Diggy': 150, 'Wyoming Blood': 45, 'Sploosh Sploosh': 45, 'Stronk Tools': 105, 'Multorange': 45},
     {'Swift Steppin': 150, 'Archer Or Bust': 75, 'Bug^2': 45, 'Premigreen': 45, },
     {'Stable Jenius': 150, 'Mage Is Best': 75, 'Molto Loggo': 45, 'Le Brain Tools': 105, 'Severapurple': 45, },
     {'Fmj': 30, 'Shaquracy': 30, 'Hammer Hammer': 100, 'All For Kill': 150, "Name I Guess": 40},
     "60% max value",
     "MINIMUM recommended Utility bubbles for starting W6 push. Keep watch of your No Bubble Left Behind list (from W4 Lab) to keep cheap/easy bubbles off when possible!"],
    [6, 100,
     {'Roid Ragin': 234, 'Warriors Rule': 117, 'Hearty Diggy': 234, 'Wyoming Blood': 70, 'Sploosh Sploosh': 70, 'Stronk Tools': 164, 'Multorange': 70,
      'Dream Of Ironfish': 70},
     {'Swift Steppin': 234, 'Archer Or Bust': 117, 'Bug^2': 70, 'Premigreen': 70, 'Fly In Mind': 94},
     {'Stable Jenius': 234, 'Mage Is Best': 117, 'Molto Loggo': 70, 'Le Brain Tools': 164, 'Severapurple': 70, 'Tree Sleeper': 94},
     {'All For Kill': 167, "Name I Guess": 100},
     "70% max value",
     "All for Kill hard-caps at 167, you're finished!"],
    [7, 120,
     {'Roid Ragin': 400, 'Warriors Rule': 200, 'Hearty Diggy': 400, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 280, 'Multorange': 120,
      'Dream Of Ironfish': 120},
     {'Swift Steppin': 400, 'Archer Or Bust': 200, 'Bug^2': 120, 'Premigreen': 120},
     {'Stable Jenius': 400, 'Mage Is Best': 200, 'Hocus Choppus': 400, 'Molto Loggo': 120, 'Le Brain Tools': 280, 'Severapurple': 120, 'Tree Sleeper': 160},
     {'Laaarrrryyyy': 150, 'Hammer Hammer': 150, 'Cookin Roadkill': 105, "Name I Guess": 150},
     "80% max value",
     "Larry at 150 = 72% chance for +2 levels. Somewhere around level 125-150, this bubble should pass 100m Dementia Ore cost and be available to level with Boron upgrades from the W3 Atom Collider in Construction.  It should be, in my opinion, the ONLY Utility Bubble you spend these daily clicks on until it reaches 501. If you cannot afford the Particles needed to level Larry, invest into Sampling Bubbles."],
    [8, 120,
     {'Roid Ragin': 567, 'Warriors Rule': 284, 'Hearty Diggy': 567, 'Stronk Tools': 397, 'Multorange': 170, 'Dream Of Ironfish': 170},
     {'Swift Steppin': 567, 'Archer Or Bust': 284, 'Premigreen': 170},
     {'Stable Jenius': 567, 'Mage Is Best': 284, 'Hocus Choppus': 567, 'Le Brain Tools': 397, 'Severapurple': 170, 'Tree Sleeper': 227},
     {'Hammer Hammer': 180},
     "85% max value",
     ""],
    # [9, 120,
    #  {'Roid Ragin': 615, 'Warriors Rule': 308, 'Hearty Diggy': 615, 'Stronk Tools': 430, 'Multorange': 185, 'Dream Of Ironfish': 185},
    #  {'Swift Steppin': 615, 'Archer Or Bust': 308, 'Premigreen': 185},
    #  {'Stable Jenius': 615, 'Mage Is Best': 308, 'Hocus Choppus': 615, 'Le Brain Tools': 430, 'Severapurple': 185, 'Tree Sleeper': 246},
    #  {'Hammer Hammer': 210},
    #  "86% max value",
    #  ""],
    # [10, 120,
    #  {'Roid Ragin': 670, 'Warriors Rule': 335, 'Hearty Diggy': 670, 'Stronk Tools': 469, 'Multorange': 201, 'Dream Of Ironfish': 201},
    #  {'Swift Steppin': 670, 'Archer Or Bust': 335, 'Premigreen': 201},
    #  {'Stable Jenius': 670, 'Mage Is Best': 335, 'Hocus Choppus': 670, 'Le Brain Tools': 469, 'Severapurple': 201, 'Tree Sleeper': 268},
    #  {'Laaarrrryyyy': 501},
    #  "87% max value",
    #  ""],
    # [11, 120,
    #  {'Roid Ragin': 700, 'Warriors Rule': 367, 'Hearty Diggy': 734, 'Stronk Tools': 514, 'Multorange': 220, 'Dream Of Ironfish': 220},
    #  {'Swift Steppin': 700, 'Archer Or Bust': 367, 'Premigreen': 220},
    #  {'Stable Jenius': 700, 'Mage Is Best': 367, 'Hocus Choppus': 734, 'Le Brain Tools': 514, 'Severapurple': 220, 'Tree Sleeper': 294},
    #  {'Cookin Roadkill': 630, 'Hammer Hammer': 270},
    #  "88% max value",
    #  ""],
    # [12, 120,
    #  {'Roid Ragin': 720, 'Warriors Rule': 405, 'Hearty Diggy': 810, 'Stronk Tools': 567, 'Multorange': 243, 'Dream Of Ironfish': 243},
    #  {'Swift Steppin': 720, 'Archer Or Bust': 405, 'Premigreen': 243},
    #  {'Stable Jenius': 720, 'Mage Is Best': 405, 'Hocus Choppus': 810, 'Le Brain Tools': 567, 'Severapurple': 243, 'Tree Sleeper': 324},
    #  {'Startue Exp': 240, 'Hammer Hammer': 300},
    #  "89% max value",
    #  ""],
    [9, 120,
     {'Roid Ragin': 740, 'Warriors Rule': 450, 'Hearty Diggy': 900, 'Stronk Tools': 630, 'Multorange': 270, 'Dream Of Ironfish': 270},
     {'Swift Steppin': 740, 'Archer Or Bust': 450, 'Premigreen': 270},
     {'Stable Jenius': 740, 'Mage Is Best': 450, 'Hocus Choppus': 900, 'Le Brain Tools': 630, 'Severapurple': 270, 'Tree Sleeper': 360},
     {'Laaarrrryyyy': 501, 'Cookin Roadkill': 630, 'Startue Exp': 240, 'Hammer Hammer': 300,
      'Droppin Loads': 280, 'Shimmeron': 360, 'Buff Boi Talent': 100, 'Fast Boi Talent': 100, 'Smart Boi Talent': 100,},
     "90% max value",
     ""],
    # [14, 120,
    #  {'Roid Ragin': 760, 'Warriors Rule': 506, 'Multorange': 304},
    #  {'Swift Steppin': 760, 'Archer Or Bust': 506, 'Premigreen': 304},
    #  {'Stable Jenius': 760, 'Mage Is Best': 506, 'Severapurple': 304},
    #  {'Call Me Bob': 200, 'Shimmeron': 405},
    #  "91% max value",
    #  ""],
    # [15, 120,
    #  {'Roid Ragin': 780, 'Warriors Rule': 575, 'Multorange': 345},
    #  {'Swift Steppin': 780, 'Archer Or Bust': 575, 'Premigreen': 345},
    #  {'Stable Jenius': 780, 'Mage Is Best': 575, 'Severapurple': 345},
    #  {'Big P': 140, 'Big Game Hunter': 70, 'Mr Massacre': 117, 'Shimmeron': 460},
    #  "92% max value",
    #  ""],
    # [16, 120,
    #  {'Roid Ragin': 800, 'Warriors Rule': 665, 'Multorange': 399},
    #  {'Swift Steppin': 800, 'Archer Or Bust': 665, 'Premigreen': 399},
    #  {'Stable Jenius': 800, 'Mage Is Best': 665, 'Severapurple': 399},
    #  {'Big P': 240, 'Big Game Hunter': 120, 'Mr Massacre': 200, 'Shimmeron': 532},
    #  "93% max value",
    #  ""],
    # [17, 120,
    #  {'Roid Ragin': 820, 'Warriors Rule': 784, 'Multorange': 470},
    #  {'Swift Steppin': 820, 'Archer Or Bust': 784, 'Premigreen': 470},
    #  {'Stable Jenius': 820, 'Mage Is Best': 784, 'Severapurple': 470},
    #  {'Big P': 340, 'Call Me Bob': 300, 'Big Game Hunter': 170, 'Mr Massacre': 284, 'Shimmeron': 627},
    #  "94% max value",
    #  ""],
    [10, 120,
     {'Roid Ragin': 840, 'Warriors Rule': 950, 'Multorange': 570, },
     {'Swift Steppin': 840, 'Archer Or Bust': 950, 'Premigreen': 570},
     {'Stable Jenius': 840, 'Mage Is Best': 950,  'Severapurple': 570},
     {'Laaarrrryyyy': 900, 'Big P': 540, 'Call Me Bob': 500, 'Carpenter': 450, 'Big Game Hunter': 270, 'Mr Massacre': 450, 'Shimmeron': 760, "Grind Time": 500},
     "95% max value",
     ""],
    # [19, 120,
    #  {'Roid Ragin': 860, 'Warriors Rule': 1200, 'Multorange': 720},
    #  {'Swift Steppin': 860, 'Archer Or Bust': 1200},
    #  {'Stable Jenius': 860, 'Mage Is Best': 1200, 'Severapurple': 720},
    #  {'Call Me Bob': 700, 'Cropius Mapper': 630, 'Lo Cost Mo Jade': 360, 'Buff Boi Talent': 200, 'Fast Boi Talent': 200, 'Smart Boi Talent': 200,},
    #  "96% max value",
    #  ""],
    # [20, 120,
    #  {'Roid Ragin': 880, 'Warriors Rule': 1617, 'Multorange': 970},
    #  {'Swift Steppin': 880, 'Archer Or Bust': 1617},
    #  {'Stable Jenius': 880, 'Mage Is Best': 1617, 'Severapurple': 970},
    #  {'Cookin Roadkill': 1330, 'Big P': 940, 'Laaarrrryyyy': 1900, 'Call Me Bob': 1000, 'Big Game Hunter': 570, 'Mr Massacre': 950, 'Diamond Chef': 553, 'Lo Cost Mo Jade': 760},
    #  "97% max value",
    #  ""],
    [11, 120,
     {'Roid Ragin': 900, 'Warriors Rule': 2450, 'Multorange': 1470},
     {'Swift Steppin': 900, 'Archer Or Bust': 2450},
     {'Stable Jenius': 900, 'Mage Is Best': 2450, 'Severapurple': 1470},
     {
        'Cropius Mapper': 630, 'Buff Boi Talent': 200, 'Fast Boi Talent': 200, 'Smart Boi Talent': 200,  #Old t19
        'Call Me Bob': 1000, 'Big Game Hunter': 570, 'Mr Massacre': 950, 'Lo Cost Mo Jade': 760, 'Cookin Roadkill': 1330, 'Big P': 940, 'Laaarrrryyyy': 1900, #Old t20
        'Essence Boost-Orange': 400, 'Essence Boost-Green': 400, 'Carpenter': 950, 'Diamond Chef': 890  #Old t21
     },
     "98% max value",
     ""],
    [12, 120,
     {'Roid Ragin': 950, 'Warriors Rule': 4950, 'Multorange': 2970},
     {'Swift Steppin': 950, 'Archer Or Bust': 4950},
     {'Stable Jenius': 950, 'Mage Is Best': 4950, 'Severapurple': 2970},
     {
        'Big P': 1440, 'Call Me Bob': 2500, 'Nickel Of Wisdom': 120, "Penny Of Strength": 120, "Dollar Of Agility": 120,
        'Buff Boi Talent': 300, 'Fast Boi Talent': 300, 'Smart Boi Talent': 300,
        'Droppin Loads': 1330, 'Startue Exp': 1140, "Grind Time": 5000
     },
     "99% max value",
     ""],
    [13, 120,
     {  #'Roid Ragin': 9000,
      'Slabi Orefish': 540, 'Slabi Strength': 540,  # 'Endgame Eff I': 540,
      'Tome Strength': 540},
     {  #'Swift Steppin': 9000,
      'Sanic Tools': 630,
      'Slabo Critterbug': 540, 'Slabo Agility': 540,  # 'Endgame Eff II': 540,
      'Tome Agility': 540},
     {  #'Stable Jenius': 9000,
      'Slabe Logsoul': 540, 'Slabe Wisdom': 540, 'Endgame Eff III': 540},  # 'Tome Wisdom': 540},
     {'Nickel Of Wisdom': 270, "Penny Of Strength": 270, "Dollar Of Agility": 270, 'Card Champ': 360, 'Egg Ink': 360},
     "90% catchup",
     ""],
    [14, 140,
     {  #'Roid Ragin': 9500,
      'Stronk Tools': 1330, 'Dream Of Ironfish': 570,
      'Slabi Orefish': 1140, 'Slabi Strength': 1140,  # 'Endgame Eff I': 1140,
      'Tome Strength': 1140},
     {  #'Swift Steppin': 9500,
      'Sanic Tools': 1330, 'Fly In Mind': 760,
      'Slabo Critterbug': 1140, 'Slabo Agility': 1140,  # 'Endgame Eff II': 1140,
      'Tome Agility': 1140},
     {  #'Stable Jenius': 9500,
      'Le Brain Tools': 1330, 'Tree Sleeper': 760,
      'Slabe Logsoul': 1140, 'Slabe Wisdom': 1140, 'Endgame Eff III': 1140},  # 'Tome Wisdom': 1140},
     {'Nickel Of Wisdom': 570, "Penny Of Strength": 570, "Dollar Of Agility": 570, 'Card Champ': 760, 'Egg Ink': 760},
     "95% catchup",
     ""],
    [15, 160,
     {'Roid Ragin': 10000, 'Hearty Diggy': 9900, 'Stronk Tools': 6930, 'Dream Of Ironfish': 2970,
      'Slabi Orefish': 5940, 'Slabi Strength': 5940, 'Endgame Eff I': 5940, 'Tome Strength': 5940},
     {'Swift Steppin': 10000, 'Sanic Tools': 6930, 'Premigreen': 2970, 'Fly In Mind': 3960,
      'Slabo Critterbug': 5940, 'Slabo Agility': 5940, 'Endgame Eff II': 5940, 'Tome Agility': 5940},
     {'Stable Jenius': 10000, 'Hocus Choppus': 9900, 'Le Brain Tools': 6930, 'Tree Sleeper': 3960,
      'Slabe Logsoul': 5940, 'Slabe Wisdom': 5940, 'Endgame Eff III': 5940, 'Tome Wisdom': 5940},
     {'Cookin Roadkill': 6930, 'Call Me Bob': 10000, 'Carpenter': 4950, 'Nickel Of Wisdom': 2970, "Penny Of Strength": 2970, "Dollar Of Agility": 2970,
      'Droppin Loads': 6930, 'Startue Exp': 5940, 'Laaarrrryyyy': 9900, 'Big Game Hunter': 2970, 'Mr Massacre': 4950, 'Shimmeron': 3960, 'Lo Cost Mo Jade': 3960,
      'Hammer Hammer': 10000, "Grind Time": 10000, 'Buff Boi Talent': 800, 'Fast Boi Talent': 800, 'Smart Boi Talent': 800,
      'Card Champ': 3960, 'Egg Ink': 3960,
      'Essence Chapter': 4950, 'Quickdraw Quiver': 5940, 'Smarter Spells': 5940, 'Ninja Looter': 5940, 'Crop Chapter': 4950
      },
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
    [27, 75, 69, ['Red Malt (Redox Salts)', 'Orange Malt (Explosive Salts)', 'Dreadnog (Dreadlo Bar)', 'Dabar Special (Godshard Bar)'], ""],
    # [28, 75, 73, ['Poison Tincture (Poison Froge)', 'Shaved Ice (Purple Salt)', 'Pearl Seltzer (Pearler Shell)', 'Hampter Drippy (Hampter)'], "Currently considered impossible"],
    # [29, 75, 76, ['Pickle Jar (BobJoePickle)', 'Ball Pickle Jar (BallJoePickle)'], "Currently considered impossible"],
]
sigils_progressionTiers = {
    0: {},
    1: {
        "Unlock": {
            "Big Muscle": 1, "Pumped Kicks": 1, "Odd Litearture": 1, "Good Fortune": 1, "Plunging Sword": 1, "Wizardly Hat": 1, "Envelope Pile": 1,

        },
        "LevelUp": {

        },
    },
    2: {
        "Unlock": {
            "Shiny Beacon": 1, "Metal Exterior": 1, "Two Starz": 1, "Pipe Gauge": 1, "Trove": 1, "Pea Pod": 1,
        },
        "LevelUp": {
            "Envelope Pile": 2, "Odd Litearture": 2, "Big Muscle": 2, "Pumped Kicks": 2,
        },
    },
    3: {
        "Unlock": {
            "Tuft Of Hair": 1, "Emoji Veggie": 1, "VIP Parchment": 1, "Dream Catcher": 1, "Duster Studs": 1, "Garlic Glove": 1, "Lab Tesstube": 1, "Peculiar Vial": 1,
        },
        "LevelUp": {
            "Pea Pod": 2, "Pipe Gauge": 2, "Good Fortune": 2, "Plunging Sword": 2,
        },
    },
    4: {
        "Unlock": {
            "Loot Pile": 1, "Div Spiral": 1, "Cool Coin": 1,
        },
        "LevelUp": {
            "Peculiar Vial": 2, "Emoji Veggie": 2, "Trove": 2,
        },
    },
    5: {
        "LevelUp": {
            "Cool Coin": 2, "Div Spiral": 2, "Dream Catcher": 2, "Shiny Beacon": 2,
        },
        "Other": {
            "Ionized Sigils": True
        },
    },
    6: {
        "LevelUp": {
            "Pea Pod": 3, "Envelope Pile": 3, "Emoji Veggie": 3,
        },
    },
    7: {
        "LevelUp": {
            "Trove": 3, "Pipe Gauge": 3, "Dream Catcher": 3,
        },
    },
    8: {
        "LevelUp": {
            "Peculiar Vial": 3, "Big Muscle": 3, "Pumped Kicks": 3, "Odd Litearture": 3,
        },
    },
    9: {
        "LevelUp": {
            "Cool Coin": 3, "Good Fortune": 3,
        },
    },
    10: {
        "LevelUp": {
            "Div Spiral": 3, "Loot Pile": 2, "Shiny Beacon": 3,
        },
    },
    11: {
        "LevelUp": {
            "Garlic Glove": 2, "Plunging Sword": 2, "Two Starz": 2, "Duster Studs": 2, "Lab Tesstube": 2,
        },
    },
    12: {
        "LevelUp": {
            "Loot Pile": 3, "Garlic Glove": 3, "Plunging Sword": 3, "Two Starz": 3, "Duster Studs": 3,  "Lab Tesstube": 3,
        },
    },
    13: {
        "LevelUp": {
            "Wizardly Hat": 2, "Metal Exterior": 2, "VIP Parchment": 2, "Tuft Of Hair": 2,
        },
    },
    14: {
        "LevelUp": {
            "Wizardly Hat": 3, "Metal Exterior": 3, "VIP Parchment": 3, "Tuft Of Hair": 3,
        },
    },
}
killroy_progressionTiers = {
    0: {},
    1: {'Upgrades': {'Timer': 2, 'Talent Points': 1}, 'Note': 'Unlock Talent Points and place 1 point'},
    2: {'Upgrades': {'Timer': 15, 'Skulls': 1}, 'Note': 'Unlock Skulls and place 1 point'},
}
islands_progressionTiers = {
    0: {},
    1: {'Islands': ['Trash Island']},
    2: {'Islands': ['Seasalt Island', 'Shimmer Island']},
    3: {'Islands': ['Crystal Island', 'Rando Island']},
    4: {'Islands': ['Fractal Island']},
}

###WORLD 3 PROGRESSION TIERS###
saltLick_progressionTiers = [
    [0, {}, ""],
    [1, {'Obol Storage': 8}, "Froge"],
    [2, {'Printer Sample Size': 20}, "Redox Salts"],
    [3, {'Max Book': 10}, "Spontaneity Salts"],
    [4, {'TD Points': 10}, "Dioxide Synthesis"],
    [5, {'Multikill': 10}, "Purple Salt"],
    [6, {'EXP': 100}, "Dune Soul"],
    [7, {'Alchemy Liquids': 100}, "Mousey"],
    [8, {'Damage': 250}, "Pingy"],
    [9, {'Refinery Speed': 100}, "Explosive Salts"],
]
deathNote_progressionTiers = [
    # 0-4 int tier. int w1LowestSkull, int w2LowestSkull, int w3LowestSkull, int w4LowestSkull,
    # 5-9 int w5LowestSkull, int w6LowestSkull, int w7LowestSkull, int w8LowestSkull, int zowCount, int chowCount,
    # 10-11 int meowCount, str Notes
    [0,  0,  0,  0,  0,  0,  0,     0, 0,   0,  0,  0,  0, ""],
    [1,  1,  1,  1,  0,  0,  0,     0, 0,   0,  0,  0,  0, ""],
    [2,  2,  2,  2,  0,  0,  0,     0, 0,   0,  0,  0,  0, ""],
    [3,  3,  3,  3,  1,  0,  0,     0, 0,   0,  0,  0,  0, ""],
    [4,  4,  4,  4,  2,  0,  0,     0, 0,   0,  0,  0,  0, ""],  #The recommendation for ZOWs is 12hrs or less (8,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!
    [5,  5,  5,  5,  3,  0,  0,     0, 0,   0,  0,  0,  0, "The Voidwalker questline requires W1-W3 at all Plat Skulls. Aim to complete this by Mid W5 as Vman's account-wide buffs are insanely strong."],
    [6,  7,  5,  5,  4,  0,  0,     0, 0,   0,  0,  0,  0, ""],  #"The recommendation for CHOWs is 12hrs or less (83,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"
    [7,  10, 7,  5,  5,  1,  0,     0, 0,   0,  0,  0,  0, ""],
    [8,  10, 10, 7,  5,  2,  0,     0, 0,   0,  0,  0,  0, ""],
    [9,  10, 10, 10, 5,  3,  0,     0, 0,   0,  0,  0,  0, ""],
    [10, 10, 10, 10, 7,  4,  0,     0, 0,   0,  0,  0,  0, ""],
    [11, 10, 10, 10, 10, 5,  0,     0, 0,   0,  0,  0,  0, ""],  #"Complete Lava Skull, then BB Super CHOW, before you start working on Eclipse Skulls. "
    [12, 10, 10, 10, 10, 7,  0,     0, 0,   0,  0,  0,  0, ""],
    [13, 10, 10, 10, 10, 10, 0,     0, 0,   0,  0,  0,  0, ""],
    [14, 10, 10, 10, 10, 10, 0,     0, 0,   0,  0,  0,  0, ""],
    [15, 10, 10, 10, 10, 10, 0,     0, 0,   0,  0,  0,  0, ""],
    [16, 20, 10, 10, 10, 10, 0,     0, 0,   0,  0,  0,  0, ""],
    [17, 20, 20, 10, 10, 10, 1,     0, 0,   0,  0,  0,  0, ""],
    [18, 20, 20, 20, 10, 10, 2,     0, 0,   0,  0,  0,  0, ""],
    [19, 20, 20, 20, 20, 10, 3,     0, 0,   15, 15, 15, 0, "Aim for Super CHOWs in 24hrs each (4m+ KPH)"],
    [20, 20, 20, 20, 20, 20, 4,     0, 0,   26, 26, 26, 0, ""],
    [21, 20, 20, 20, 20, 20, 5,     0, 0,   40, 40, 40, 0, ""],
    [22, 20, 20, 20, 20, 20, 7,     0, 0,   53, 53, 53, 0, ""],
    [23, 20, 20, 20, 20, 20, 10,    0, 0,   66, 66, 66, 0, ""],
    [24, 20, 20, 20, 20, 20, 10,    0, 0,   73, 73, 73, 0, ""],
    [25, 20, 20, 20, 20, 20, 20,    0, 0,   80, 80, 80, 0, ""],
    [26, 20, 20, 20, 20, 20, 20,    0, 0,   84, 84, 83, 0, "As of v2.11, completing a Super CHOW on Boops is impossible."],
    [27, 20, 20, 20, 20, 20, 20,    0, 0,   86, 86, 86, 86, "Info only"]
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
    'Recommended': [
        'Equinox Symbols', 'Equinox Resources', 'Metal Detector', 'Slow Roast Wiz',
        'Liquidvestment', 'Faux Jewels', 'Matching Scims', 'Equinox Dreams', 'Voter Rights'
    ],
    'Optional': [
        'Shades of K', 'Laboratory Fuse', 'Food Lust'
    ]
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
            #"Neon - Damage N' Cheapener": 2,
            'Fluoride - Void Plate Chef': 11,
            'Helium - Talent Power Stacker': 7,
        },
    },
    10: {
        'Atoms': {
            #"Neon - Damage N' Cheapener": 10,
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
            #"Neon - Damage N' Cheapener": 20,
            'Helium - Talent Power Stacker': 9,
        },
    },
    13: {
        'Atoms': {
            'Boron - Particle Upgrader': 30,
            'Hydrogen - Stamp Decreaser': 30,
            #"Neon - Damage N' Cheapener": 30,
            'Fluoride - Void Plate Chef': 30,
        },
    },
    14: {
        'Atoms': {
            'Helium - Talent Power Stacker': 10,
        },
    },
}
sampling_progressionTiers = {
    0: {"Materials": {"Oak Logs": 0,     "Copper Ore": 0,     "Goldfish": 0,     "Fly": 0,     "Spore Cap": 0}, "NonDootDiscount": 1},
    1: {"Materials": {"Oak Logs": 150,   "Copper Ore": 60,    "Goldfish": 50,    "Fly": 50,    "Spore Cap": 20}, "NonDootDiscount": 1},
    2: {"Materials": {"Oak Logs": 1000,  "Copper Ore": 700,   "Goldfish": 100,   "Fly": 100,   "Spore Cap": 70}, "NonDootDiscount": 1},
    3: {"Materials": {"Oak Logs": 8e3,   "Copper Ore": 10e3,  "Goldfish": 500,   "Fly": 500,   "Spore Cap": 500}, "NonDootDiscount": .7},
    4: {"Materials": {"Oak Logs": 300e3, "Copper Ore": 500e3, "Goldfish": 5e3,   "Fly": 5e3,   "Spore Cap": 400e3}, "NonDootDiscount": .7},
    5: {"Materials": {"Oak Logs": 16e6,  "Copper Ore": 20e6,  "Goldfish": 2e6,   "Fly": 900e3, "Spore Cap": 1e6}, "NonDootDiscount": .7},
    6: {"Materials": {"Oak Logs": 200e6, "Copper Ore": 160e6, "Goldfish": 20e6,  "Fly": 9e6,   "Spore Cap": 2.5e6}, "NonDootDiscount": .75},
    7: {"Materials": {"Oak Logs": 1.5e9, "Copper Ore": 1.2e9, "Goldfish": 150e6, "Fly": 68e6,  "Spore Cap": 10e6}, "NonDootDiscount": .8},
    8: {"Materials": {"Oak Logs": 10e9,  "Copper Ore": 8e9,   "Goldfish": 1e9,   "Fly": 454e6, "Spore Cap": 20e6}, "NonDootDiscount": .85},
    9: {"Materials": {"Oak Logs": 22e9,  "Copper Ore": 15e9,  "Goldfish": 2e9,   "Fly": 1e9,   "Spore Cap": 30e6}, "NonDootDiscount": .90},
    10:{"Materials": {"Oak Logs": 100e9, "Copper Ore": 250e9, "Goldfish": 10e9,  "Fly": 8e9,   "Spore Cap": 40e6}, "NonDootDiscount": .90},
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
            },
            "ShinyNotes": ""
        },
        12: {
            "Tier": 12,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
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
            'Fauxory Tusk': 1
        }
    },
    2: {
        'IslandsDiscovered': 4,
        'CaptainsAndBoats': 5,
        'Artifacts': {
            'Gold Relic': 1,
            '10 AD Tablet': 2,
            'Fauxory Tusk': 2
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
            'Chilled Yarn': 4,
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
farming_progressionTiers = {
    0: {},
    1: {
        'Farming Level': 10,
        'Day Market': {
            'Land Plots': 4,
            'Stronger Vines': 6,
            'Nutritious Soil': 7,
        },
        'Crops Unlocked': 19,  #Total number of crops is 19 for Overgrowth to be purchasable
        'Suggestions': {
            'EvoChance': [4, 4.5],
            'CropIndex': [11, 29]  #11 = Basic/Lime, 29 = Earthy/Avocado
        },
        'Night Market': {
            'Overgrowth': 1,
        },
    },  #Get Overgrowth
    2: {
        'Farming Level': 50,
        'Day Market': {
            'Land Plots': 7,
            'Stronger Vines': 34,
            'Nutritious Soil': 34,
            'Product Doubler': 12,
            'Biology Boost': 26,
        },
        'Crops Unlocked': 61,  #Total number of crops is 61 for Land Ranks to be purchasable
        'Suggestions': {
            'EvoChance': [325, 335],
            'CropIndex': [21, 41, 55, 72],  #21 = Basic/Golden Blueberry, 41 = Earthy/Lettuce, 55 = Bulbo/Pink Daisy, 72 = Sushi/11
        },
        'Night Market': {
            'Land Rank': 1,
            'Evolution Gmo': 20,  #1.16x
            'Speed Gmo': 10,  #3%
        },
    },  #Get Land Ranks
    3: {
        'Farming Level': 120,
        'Day Market': {
            'Land Plots': 11,
            'Stronger Vines': 56,
            'Nutritious Soil': 54,
            'Biology Boost': 45,
            'Product Doubler': 28,
            'More Beenz': 28,
            'Rank Boost': 19,
        },
        'Land Ranks': {
            1: {
                'Evolution Boost': 25,
                'Soil Exp Boost': 25,
                'Evolution Megaboost': 25,
                'Production Boost': 50,
                'Soil Exp Megaboost': 25,
            },
            2: {
                'Soil Exp Boost': 50,
                'Production Boost': 80,
                'Overgrowth Boost': 50,
            },
            3: {
                'Production Boost': 100,
                'Production Megaboost': 100,
                'Overgrowth Boost': 75,
                'Soil Exp Megaboost': 50,
            },  #425 total
        },
        'Crops Unlocked': 116,
        'Suggestions': {
            'EvoChance': [1e12, 10e12],
            'Speed': [8, 20],
            'CropIndex': [46, 61, 84, 104, 119],  #46 = Earthy/Gold Sliced Tomato, 61 = Bulbo/Golden Tulip, 84 = Sushi/Max, 104 = Mushie/20, 119 = Normal Glassy/Onigiri
            'Stacks': ['Evolution', 'Speed'],
        },
        'Night Market': {
            'Evolution Gmo': 30,  # 1.24x
            'Speed Gmo': 25,  # 7.5%
            'Og Fertilizer': 10,  # 1.1x
        },
        #Soil Exp Boost : Mega : Super is around 4:2:3
        #OG Boost : Mega :  Super is around 4:5:8
        #Farmtastic pretty optional
    },  #1k stacks. Reach 120 farming and the first few Glassy
    4: {
        'Day Market': {
            'Land Plots': 12,
            'Stronger Vines': 62,
            'Nutritious Soil': 60,
            'Biology Boost': 56,
            'Product Doubler': 35,
            'More Beenz': 37,
            'Rank Boost': 24,
        },
        'Land Ranks': {
            1: {
                'Evolution Superboost': 25,
                'Soil Exp Boost': 100,
                'Soil Exp Megaboost': 100,
            },  #550 total
        },
        'Crops Unlocked': 123,
        'Suggestions': {
            'EvoChance': [1e16, 1e18],
            'Speed': [30, 40],
            'OG': [2.5, 6.25],  #Guarantees 2x OG at 2.5 OG, guarantees 4x OG
            'CropIndex': [107, 123],  #107 = Mushie/Final, 122 = Red Glassy/Mango
            'Stacks': ['Evolution', 'Speed'],
        },
        'Night Market': {
            'Evolution Gmo': 40,  #1.32x
            'Og Fertilizer': 20,  #1.20x
            'Super Gmo': 10,  #5%
            'Value Gmo': 1
        },
        #Value is around 10x
    },  #Repeat the 1k stacks. Day Market Farming to afford 100% Product Doubler, Bean Farming for 5% Super GMO
    5: {
        #'Day Market': {},  #Intentionally excluded.
        #'Land Ranks': {1: {},},  #Intentionally excluded.
        'Crops Unlocked': 126,
        'Suggestions': {
            'EvoChance': [1e22, 5e22],
            'Speed': [30, 40],
            'CropIndex': [126],  #126 at end of 1k stacking, before 100k stacking
            'Stacks': ['Evolution', 'Speed', 'Value'],
            'No Trade': "Do not complete a Bean trade! Start back at Apples and stack to 100k of each crop"
        },
        #'Night Market': {},
    },  #End of 1k stacking, before 100k stacking. No Bean Trade
    6: {
        'Day Market': {
            'Land Plots': 16,
            'Stronger Vines': 84,
            'Nutritious Soil': 87,
            'Smarter Seeds': 86,
            #'Biology Boost': 56,    #Intentionally excluded.
            'Product Doubler': 50,
            'More Beenz': 55,
            'Rank Boost': 37,
        },
        'Land Ranks': {
            1: {
                'Overgrowth Megaboost': 100,
                'Soil Exp Superboost': 100,
                'Evolution Ultraboost': 25,
            },  #775/1400
            2: {
                'Overgrowth Boost': 200,
                'Overgrowth Megaboost': 250,
            },  #950/1400
            3: {
                'Soil Exp Boost': 220,
                'Soil Exp Megaboost': 110,
                'Soil Exp Superboost': 170,
            },  #1200/1400
            4: {
                'Soil Exp Boost': 330,
                'Soil Exp Megaboost': 165,
                'Soil Exp Superboost': 255,
            },  #1400/1400
        },
        'Crops Unlocked': 127,
        'Suggestions': {
            'EvoChance': [1e23, 5e23],
            'Speed': [250, 400],
            'OG': [6.25, 15.625],
            'CropIndex': [127],
            'Stacks': ['Evolution', 'Speed', 'Value', 'Super'],
        },
        'Night Market': {
            'Evolution Gmo': 65,  #1.52x
            'Speed Gmo': 35,  #10.5%
            'Og Fertilizer': 57,  #1.57x
            'Super Gmo': 20,  #10%
            'Value Gmo': 5
        },
    },  #First round of 100k stacking + Day Market at the same time
    7: {
        'Stats': {
            'Value': 100
        },
        'Crops Unlocked': 127,
        'Land Ranks': {
            1: {
                'Overgrowth Superboost': 1
            },
        },
        'Suggestions': {
            'Stacks': ['Evolution', 'Speed', 'Value', 'Super'],
        },
        'Night Market': {
            'Evolution Gmo': 88,  #1.70x
            'Speed Gmo': 50,  #15%
            'Super Gmo': 30,  #15%
            'Value Gmo': 10
        }
    },  #Unlock Overgrowth Superboost land rank, 100x+ total Value, 15% Speed and 15% Super GMO
    8: {
        'Crops Unlocked': 160,
        'Suggestions': {
            'EvoChance': [1e66, 1e68],
            'Stacks': ['Evolution', 'Speed', 'Value', 'Super'],
        },
        'Night Market': {
            'Evolution Gmo': 125,  #2.00x
            'Super Gmo': 40,  #20%
            'Value Gmo': 20,
        }
    },  #Unlock 160 crops by focusing on Evo GMO, Super GMO, and Speed GMO
    9: {
        'Farming Level': 300,
        'Crops Unlocked': 180,
        'Day Market': {
            'Land Plots': 20,
            'Stronger Vines': 170,  #340%
            'Product Doubler': 100,
            'More Beenz': 100,
            'Rank Boost': 100,
        },
        'Suggestions': {
            'EvoChance': [1e91, 1e93],
            'Stacks': ['Evolution', 'Speed', 'Value', 'Super'],
        },
        'Night Market': {
            'Evolution Gmo': 187,  #2.50x
            'Speed Gmo': 80,
            'Og Fertilizer': 200,
            'Exp Gmo': 100,
            'Super Gmo': 50,
            'Value Gmo': 50,
        },
        'Land Ranks': {
            1: {
                'Seed of Stealth': 1,
                'Seed of Loot': 1,
                'Seed of Damage': 1,
                'Seed of Stats': 1,
            },
        },
    },  #Progress that is still quick-ish to futureproof for possible new crops being added in the future
    10: {
        'Crops Unlocked': 230,
        'Suggestions': {
            'Stacks': ['Evolution', 'Speed', 'Value', 'Super'],
        },
        'Day Market': {
            'Stronger Vines': 220,  #440%
            'Nutritious Soil': 219,  #Finish eggplants, stop before the Cabbage that is needed for Stronger Vines
            'More Beenz': 154,  #308%, end of whatever square Sushi plant that is
            'Rank Boost': 109,  #327%, end of the white triple-tip mushroom plant
        },
        'Night Market': {
            'Speed Gmo': 100,
            'Og Fertilizer': 220,
            'Value Gmo': 80,
        },
        'Alchemy Bubbles': {
            'Hinge Buster': 6930,
            'Stealth Chapter': 4950,
            'Tome Wisdom': 5940,
            'Endgame Eff II': 5940,
            'Farquad Force': 5940,
        }
    }  #440% Vines, then 99% the Alchemy Bubbles
}

###UI CONSTS###
#If you add a new switch here, you need to also add a default in \static\scripts\main.js:defaults
switches = [
    {
        "label": "Overwhelmed Mode",
        "name": "overwhelmed",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Autoloot purchased",
        "name": "autoloot",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Rift Slug acquired",
        "name": "riftslug",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Doot acquired",
        "name": "doot",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Sheepie acquired",
        "name": "sheepie",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Order groups by tier",
        "name": "order_tiers",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Hide Completed",
        "name": "hide_completed",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Hide Informational Groups",
        "name": "hide_informational",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Hide Unrated Sections",
        "name": "hide_unrated",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Show progress bars",
        "name": "progress_bars",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Handedness",
        "name": "handedness",
        "true": "L",
        "false": "R",
        "static": "false",
    },
    # {"label": "Legacy style", "name": "legacy", "true": "", "false": ""},
]

###GENERAL / MULTI-USE CONSTS###
currentWorld = 6
maxCharacters = 10
break_you_best = "<br>You best ❤️"
break_keep_it_up = "<br>Keep it up! You're on the right track! ❤️"
infinity_string = "∞"
versions_patches = {
    0: "Unknown",
    190: "v1.92 Falloween Event",  #This should have been the last version number before w6
    211: "v2.07 Rift Expansion",
    217: "v2.10 The Owl",
    218: "v2.11 The Roo",
    219: "v2.12 Land Ranks",
    220: "v2.13 Bonus Ballot",
    221: "v2.14 Summer Break",
    230: "v2.20 The Caverns Below",
    231: "v2.21 Endless Summoning",
    232: "v2.22 The Fixening",
    233: "v2.23 Justice Monument",
    234: "v2.24 Giftmas Event / v2.25 Saveload TD",
    236: "v2.26 Death Bringer Class",
    237: "v2.27 Upgrade Vault",
    241: "v2.28 Valenslimes Event"
}
ignorable_labels: tuple = ('Weekly Ballot',)
missableGStacksDict = {
    #  ItemName               Codename     Quest Codeame          Quest Name                                          Wiki link to the item                             Recommended Class/Farming notes
    "Dog Bone":              ["Quest12",   "Dog_Bone1",           "Dog Bone: Why he Die???",                          "https://idleon.wiki/wiki/Dog_Bone",              "Active ES or time candy.", 'dog-bone-npc'],
    "Ketchup Bottle":        ["Quest3",    "Picnic_Stowaway2",    "Picnic Stowaway: Beating Up Frogs for some Sauce", "https://idleon.wiki/wiki/Ketchup_Bottle",        "Active ES or time candy.", 'picnic-stowaway'],
    "Mustard Bottle":        ["Quest4",    "Picnic_Stowaway2",    "Picnic Stowaway: Beating Up Frogs for some Sauce", "https://idleon.wiki/wiki/Mustard_Bottle",        "Active ES or time candy.", 'picnic-stowaway'],
    "Strange Rock":          ["Quest7",    "Stiltzcho2",          "Stiltzcho: No Stone Unturned",                     "https://idleon.wiki/wiki/Strange_Rock",          "Active ES or time candy.", 'stiltzcho'],
    "Time Thingy":           ["Quest21",   "Funguy3",             "Funguy: Partycrastination",                        "https://idleon.wiki/wiki/Time_Thingy",           "Active ES or time candy.", 'funguy'],
    "Employment Statistics": ["Quest14",   "TP_Pete2",            "TP Pete: The Rats are to Blame!",                  "https://idleon.wiki/wiki/Employment_Statistics", "Active ES or time candy.", 'tp-pete'],
    "Corporatube Sub":       ["Quest22",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Corporatube_Sub",       "Active ES or time candy.", 'mutton'],
    "Instablab Follower":    ["Quest23",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Instablab_Follower",    "Active ES or time candy.", 'mutton'],
    "Cloudsound Follower":   ["Quest24",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Cloudsound_Follower",   "Active ES or time candy.", 'mutton'],
    "Casual Confidante":     ["GoldricP1", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Casual_Confidante",     "Active ES or time candy.", 'goldric'],
    "Triumphant Treason":    ["GoldricP2", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Triumphant_Treason",    "Active ES or time candy.", 'goldric'],
    "Claiming Cashe":        ["GoldricP3", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Claiming_Cashe",        "Active ES or time candy.", 'goldric'],
    "Monster Rating":        ["Quest32",   "XxX_Cattleprod_XxX3", "XxX_Cattleprod_XxX: Ok, NOW it's Peak Gaming!",    "https://idleon.wiki/wiki/Monster_Rating",        "Monster Ratings can drop from Crystal enemies, making Divine Knight the better farmer for Monster Ratings.", 'xxx-cattleprod-xxx']
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
        "SilverPen", 'ResetFrag',
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
        "PureWater", "EquipmentStatues18",  #W3 Slow drops = Distilled Water + EhExPee Statue
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
        "Quest68", "Bullet3", "FoodChoppin1", "EquipmentSmithingTabs2", 'EquipmentSmithingTabs3',  #Crafted2
        "PeanutG",  #Gold Peanut Crafted
        "FoodTrapping1", "FoodWorship1",  # Critter Numnums and Soulble Gum Crafted
        "Refinery1", "Refinery2", "Refinery3", "Refinery4", "Refinery5", "Refinery6",
        "Ladle",
    ],
    "Vendor Shops": [
        "FoodHealth14", "FoodHealth15", "FoodHealth16", "FoodHealth17", "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4",
        "FoodPotYe4", "OilBarrel6", "OilBarrel7", "FoodHealth4", "FoodHealth9", "FoodHealth11", "Quest19", "CraftMat3",  # Sorted by daily quantity
        "FoodPotGr3",  #Decent Speed from W3 Shop + Sir Stache
        "FoodPotRe2",  #Average Life Potion from W2 Shop + Gigafrogs
    ],
    "Rare Drops": [
        "FoodPotGr3",  #Decent Speed from W3 Shop + Sir Stache
        "FoodPotRe2",  #Average Life Potion from W2 Shop + Gigafrogs
        "FoodPotRe1",  #Small Life Potion from W1 Sewers and Tree mobs, not crystals
        "ButterBar",  #Catching Butterflies
        "EquipmentStatues9",  #Oceanman statue can be candied from W2 bugs
        "FoodPotMana3",  #Decent Mana Potion from Bloques
        "FoodHealth9",  #Yeti Ham from Bop Box
        "OilBarrel2",  # Slime Barrel, 1 in 3334
        "DesertC2b",  # Ghost, 1 in 2k
        "Quest78",  # Equinox Mirror
        "EfauntDrop1",  # Basic Efaunt material
        "Key2", "Key3"  # Efaunt and Chizoar keys
    ],
    "Cheater": [
        "Sewers1b", "TreeInterior1b", "BabaYagaETC", "JobApplication",  # W1 Rare Drops
        "DesertA1b", "DesertA3b", "MidnightCookie",  # W2 Rare Drops
        "SnowA2a", "SnowB2a", "SnowC4a",  # W3 Rare Drops
        "GalaxyA2b", "GalaxyC1b",  # W4 Rare Drops
        "LavaA1b", "LavaA5b", "LavaB3b",  # W5 Rare Drops
        "SpiA2b", "SpiB2b",  # W6 Rare Drops
        "EfauntDrop2", "Chiz0", "Chiz1", "TrollPart", "KrukPart", "KrukPart2",  # World Boss Materials
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
        "EquipmentStatues16", "EquipmentStatues17", "EquipmentStatues19",  # W3 Statues
        "EquipmentStatues20", "EquipmentStatues21", "EquipmentStatues22",  # W4 Statues
        "EquipmentStatues23", "EquipmentStatues24", "EquipmentStatues25",  # W5 Statues
        "FoodG1", "FoodG2", "FoodG3", "FoodG4", "FoodG5", "FoodG6", "FoodG7", "FoodG8", "FoodG10",  # Gold Foods
        "ResetCompleted", "ResetCompletedS", "ClassSwap",
        "ClassSwapB", "ResetBox",
    ]
}
greenStackAmount = 10**7
gstackable_codenames = [item for items in expectedStackables.values() for item in items]
gstackable_codenames_expected = [
    item for items in list(expectedStackables.values())[:-1] for item in items
]
quest_items_codenames = expectedStackables["Missable Quest Items"]
key_cards = "Cards0"
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
        "caveB": ['Gloomie Mushroom', 5000],
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
    14: "Death Bringer",
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
skillIndexList = [
    "Combat",
    "Mining", "Smithing", "Choppin",
    "Fishing", "Alchemy", "Catching",
    "Trapping", "Construction", "Worship",
    "Cooking", "Breeding", "Lab",
    "Sailing", "Divinity", "Gaming",
    "Farming", "Sneaking", "Summoning"
                  ]
emptySkillList = [0] * 25
balloonable_skillsList = [
    "Mining", "Smithing", "Choppin",
    "Fishing", "Alchemy", "Catching",
    "Trapping", "Worship",
    "Cooking",  #"Lab" isn't balloonable, oddly enough. You can pearl it though
]
pearlable_skillsList = [
    "Mining", "Smithing", "Choppin",
    "Fishing", "Alchemy", "Catching",
    "Trapping", "Worship",
    "Cooking", "Lab",
]
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
    105:16,
}
gemShopDict = {
    # Inventory and Storage
    'Item Backpack Space': 55,
    'Storage Chest Space': 56,
    'Carry Capacity': 58,
    'Food Slot': 59,
    'More Storage Space': 109,
    'Card Presets': 66,

    # Dailies N' Resets
    'Daily Teleports': 71,
    'Daily Minigame Plays': 72,

    # Cards
    'Extra Card Slot': 63,

    # Goods & Services
    'Weekly Dungeon Boosters': 84,

    # World 1&2
    'Infinity Hammer': 103,
    'Brimstone Forge Slot': 104,
    'Ivory Bubble Cauldrons': 105,
    'Bleach Liquid Cauldrons': 106,
    'Obol Storage Space': 57,
    'Sigil Supercharge': 110,

    # World 3
    'Crystal 3d Printer': 111,
    'More Sample Spaces': 112,
    'Burning Bad Books': 113,
    'Prayer Slots': 114,
    'Zen Cogs': 115,
    'Cog Inventory Space': 116,
    'Tower Building Slots': 117,
    'Fluorescent Flaggies': 118,

    # World 4
    'Royal Egg Cap': 119,
    'Richelin Kitchen': 120,
    'Souped Up Tube': 123,
    'Pet Storage': 124,
    'Fenceyard Space': 125,

    # World 5
    'Chest Sluggo': 129,
    'Divinity Sparkie': 130,
    'Golden Sprinkler': 131,
    'Lava Sprouts': 133,

    # World 6
    'Plot of Land': 135,
    'Pristine Charm': 136,
    'Shroom Familiar': 137,
    'Sand of Time': 138,
    'Instagrow Generator': 139,
    'Life Refill': 140,
    'Compost Bag': 141,
    'Summoner Stone': 142,

    # Fomo
    'FOMO-1': 87,
    'FOMO-2': 88,
    'FOMO-3': 89,
    'FOMO-4': 90,
    'FOMO-5': 91,
    'FOMO-6': 92,
    'FOMO-7': 93,
    'FOMO-8': 94,

    # Oddities
    'Blinding Lantern': 0,
    'Parallel Villagers': 1,
    'Resource Boost': 2,
    'Conjuror Pts': 4,
    'Opal': 5
    }  # Default 0s
guildBonusesList = [
    "Guild Gifts", "Stat Runes", "Rucksack", "Power of Pow", "REM Fighting", "Make or Break",
    "Multi Tool", "Sleepy Skiller", "Coin Supercharger", "Bonus GP for small guilds", "Gold Charm", "Star Dazzle",
    "C2 Card Spotter", "Bestone", "Skilley Skillet", "Craps", "Anotha One", "Wait A Minute"
]
familyBonusClassTierLevelReductions = [9, 29, 69, 999]  #Character must be this high of a level to get bonuses
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
arbitrary_es_family_goal = esFamilyBonusBreakpointsList[13]  #719 fairly feasible in v2.12, 885 feels too tough atm
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
            if currentLevel >= requirement:
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
achievement_categories = [
    'EZ Access',  #'Free Teleports',
    'Monster Respawn', 'Recipes', 'Dungeon RNG Items', 'Other Nice Rewards']
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
    ["Crystal_Beatdown", "1", "Defeat_a_Crystal_monster,_who_have_a_1_in_2000_chance_of_spawning_when_a_monster_dies.", "*STEAM_EXCLUSIVE_&*8_gems_&*2_'1hr_time_candy'", "0"],
    ["Ten_Trips_of_Gold", "1", "Have_a_stack_of_exactly_30,000_Gold_Ore_in_your_Storage_Chest.", "*Mining_Cave_Background_&for_Title_Screen", "0"],
    ["Minecart_Maniac", "1", "Slam_on_a_yellow_ore_vein_in_the_Mining_Minigame,_which_gives_3_points!", "{5%_Mining_EXP_Bonus_&for_all_characters", "0"],
    ["Spike_Minigame_Master", "1", "Get_a_score_of_13_in_the_spike_minigame._Remember_to_say_'If_u_love_me_let_me_go'", "*STEAM_EXCLUSIVE_&*20_gems_&*4hr_Time_Candy", "0"],
    ["Anvil_Expansion", "1", "Craft_the_anvil_expander,_and_unlock_a_new_tab_of_item_recipes!", "*STEAM_EXCLUSIVE_&*10_gems", "0"],
    ["Steppin'_on_the_Rats", "500", "Defeat_500_Rats_with_at_least_1_other_party_member", "*Sewers_BG", "0"],
    ["Tree_Top_Dropout", "1", "Reach_the_top_of_the_Giant_Tree_in_Blunder_Hills", "*STEAM_EXCLUSIVE_&*15_gems", "0"],
    ["Naked_and_Unafraid", "1", "Enter_the_Sewers_with_no_equipment_or_weapon,_and_defeat_a_sewer_poop._Don't_want_to_get_your_stuff_dirty!", "*RNG_item_unlock", "0"],
    ["House_Flipper", "1", "Defeat_Baba_Yaga_in_under_25_seconds_after_they_spawn_in_the_Birch_Enclave", "RNG_Item_unlock", "0"],
    ["Platinum_200G", "1", "Have_a_stack_of_exactly_200,000_Platinum_Ore_in_your_Storage_Chest.", "*W1_Boss_Key_EZ-Access", "0"],
    ["Guild_Member", "1", "Claim_500_GP_for_your_guild.", "*STEAM_EXCLUSIVE_&*14_gems", "0"],
    ["Boss_Buster", "1", "Defeat_both_minibosses_in_Blunder_Hills", "*STEAM_EXCLUSIVE_&*15_gems", "0"],
    ["Nutty_Crafter", "42", "Craft_42_golden_peanuts,_whatever_those_might_be!", "{5%_Gold_Food_Bonus_&for_all_characters", "0"],
    ["Minecart_Master", "1", "Get_a_score_of_103+_in_the_Mining_Minigame,_beating_the_developers_highscore!", "*STEAM_EXCLUSIVE_&*25_gems_&*2_'4hr_time_candy'", "0"],
    ["Choppin'_to_the_Beat", "1", "Get_a_score_of_141+_in_the_Choppin'_Minigame,_beating_the_developers_highscore!", "*STEAM_EXCLUSIVE_&*25_gems_&*4hr_time_candy", "0"],
    ["Decked_Out_in_Gold", "1", "Equip_Golden_Helmet,_Chestplate,_Pants,_Shoes,_two_Golden_tools,_and_the_Defenders_Dignity_ring.", "*{3%_Arcade_balls/hr", "0"],
    ["Nice_Fur_Suit", "1", "Equip_all_4_pieces_of_Amarok_armor.", "*Forest_Villa_Teleport", "0"],
    ["Half_a_Mill-log", "1", "Have_a_stack_of_exactly_500,000_Veiny_Logs_in_your_Storage_Chest.", "*W1_Colosseum_EZ-Access_&*W1_Shops_EZ-Access", "0"],
    ["Bad_Doggy!", "1", "Defeat_Chaotic_Amarok.", "*STEAM_EXCLUSIVE_&*25_gems_&*2_'2hr_time_candy'", "0"],
    ["Two-Time_Savior", "2", "Equip_the_Blunder_Hero_Trophy,_while_also_having_another_in_your_inventory.", "{5%_Faster_Respawn_for_&all_Blunder_Hills_mobs", "0"],
    ["Million_Null_'n_Void", "1", "Have_a_stack_of_exactly_1,000,000_Void_Ore_in_your_Storage_Chest.", "*Deep_Mining_Teleport", "0"],
    ["Lucky_7s", "1", "SECRET_ACHIEVEMENT_------------------------_Punch_a_monster,_win_the_Jackpot!_Well,_hypothetically...", "*{1%_Arcade_balls/hr_&*15_Gems_&*7_'1hr_time_candy'", "0"],
    ["What_a_View!", "1", "SECRET_ACHIEVEMENT_------------------------_Climb_the_2nd_tallest_tree_in_all_of_Blunder_Hills,_and_say_'Great_view,_1_star'", "*{1%_Arcade_balls/hr", "0"],
    ["Cavernous_Nook", "1", "-", "*Knowledge_of_the_&Cavern_Secret_Location", "0"],
    ["Seriousleaf-ast!", "1", "SECRET_ACHIEVEMENT_------------------------_Score_a_point_in_the_Choppin'_Minigame_while_the_leaf_is_zooming_at_hyperspeed", "*{1%_Arcade_balls/hr", "0"],
    ["Peanut_Pioneer", "1", "SECRET_ACHIEVEMENT_------------------------_Talk_to_the_jungle_bush,_join_the_club...", "*STEAM_EXCLUSIVE_&*25_gems_&*2_'2hr_time_candy'", "0"],
    ["Meel_Time!", "1", "SECRET_ACHIEVEMENT_------------------------_Shake_it!_To_the_left,_to_the_left!_Oh_yea!!!", "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Pro_Gamer_Move", "1", "SECRET_ACHIEVEMENT_------------------------_Keep_the_oil._Precious,_precious_oil...", "*STEAM_EXCLUSIVE_&*10_gems_&*1hr_time_candy", "0"],
    ["Meet_the_Dev", "1", "SECRET_ACHIEVEMENT_------------------------_I_heard_he's_12_feet_tall_and_can_spawn_bosses_just_by_talking...", "*STEAM_EXCLUSIVE_&*40_gems_&*4_'2hr_time_candy'", "0"],
    ["Heyo!", "1", "Say_'Hi'_to_250_different_people_without_closing_the_game.", "*5_'Tab_1'_Talent_Pts_&*{1%_Arcade_balls/hr", "0"],
    ["Anothervil_Expansion", "1", "Craft_the_Anvil_III_expander._More_things_to_craft,_hooray!", "*STEAM_EXCLUSIVE_&*30_gems", "0"],
    ["Based_Roots", "20", "Reach_The_Roots,_which_is_the_map_below_the_Sticks_monsters_in_the_Giant_Tree", "*Acorn_Hat_Recipe", "0"],
    ["Dungeon_Pinch", "1", "Deal_100_or_more_damage_in_a_single_hit_in_any_party_dungeon.", "*{1%_Class_EXP_bonus_&for_all_characters", "0"],
    ["Big_Frog_Angry", "1", "Defeat_Grandfrogger_on_his_1st_Difficulty.", "*{2%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Big_Frog_Furious", "1", "Defeat_Grandfrogger_on_his_2nd_Difficulty.", "*{3%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Big_Frog_Big_Sad", "1", "Defeat_Grandfrogger_on_his_3rd_Difficulty.", "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["2_minute_meal", "1", "Spawn_Grandfrogger_within_2_minutes_of_entering_the_dungeon.", "*{3%_Class_EXP_bonus_&for_all_characters", "0"],
    ["Big_Frog_Big_Mad", "1", "Defeat_Grandfrogger_on_his_4th_Difficulty,_and_avoid_becoming_one_with_the_soup...", "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
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
    ["More_and_More_Me!", "1", "Create_your_4th_character,_who_will_never_appreciate_the_struggle_your_first_3_characters_had.", "*STEAM_EXCLUSIVE_&*16_gems", "0"],
    ["Golden_Fly", "1", "Pass_through_the_small_golden_hoop_in_the_Catching_Minigame._It's_worth_3_points!", "*{5%_Catching_&Efficiency", "0"],
    ["Hammer_Bub", "1", "Level_up_the_'Hammer_Hammer'_Alchemy_bubble_to_Lv._10", "*RNG_item_unlock", "0"],
    ["Wassup_Yo!", "1", "Say_'Hi'_to_100_unique_people_without_closing_the_game_or_changing_Servers.", "*2_'Tab_2'_Talent_Pts_&*{2%_Arcade_balls/hr", "0"],
    ["Gold_School", "1", "Have_a_stack_of_exactly_1500_Goldfish_in_your_Storage_Chest.", "*{1%_Arcade_balls/hr", "0"],
    ["Buzz_Buzz", "1", "Have_a_stack_of_exactly_2500_Flies_in_your_Storage_Chest.", "*3_'Tab_2'_Talent_Pts", "0"],
    ["Careful,_it's_Sharp!", "1", "Have_a_stack_of_exactly_15_Glass_Shards_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Hybernation", "1", "Leave_one_of_your_players_AFK_for_an_entire_week,_which_is_168_hours!_Anything_more_counts_too!", "*{3%_Arcade_balls/hr_&*Good_nights_sleep", "0"],
    ["Vial_Noob", "1", "Get_3_vials_to_Lv._4,_which_are_the_green_ones", "*RNG_item_unlock", "0"],
    ["Specializational!", "2", "Choose_a_subclass_for_two_of_your_characters.", "*RNG_item_unlock", "0"],
    ["Obols_Oh_Boy!", "1", "Have_10_Silver_Obols_equipped_at_once._The_Family_tab_counts_here!", "{2%_Arcade_balls/hr", "0"],
    ["Well_Learned", "1", "Get_a_lv_92_or_higher_Star_Book_from_Alchemy!_The_1st_one,_specifically.", "*RNG_item_unlock", "0"],
    ["B-o-B_to_Help", "1", "Complete_75_unique_quests_on_a_single_character._I'm_not_sure_what_B-o-B_stands_for_either...", "*STEAM_EXCLUSIVE_&*16_gems", "0"],
    ["Card_Enthusiast", "1", "Collect_30_unique_cards._If_u_wanna_trade,_I_got_some_spare_Amarok_cards!", "*STEAM_EXCLUSIVE_&*16_gems", "0"],
    ["Efaunt_Trumped", "1", "Defeat_Efaunt,_the_Mummified_Elephant_God._He_will_remember_you_doing_this.", "*RNG_item_unlock", "0"],
    ["Fishing_Finesse", "1", "Get_a_score_of_67+_in_the_Fishing_Minigame,_beating_the_developers_highscore!", "*STEAM_EXCLUSIVE_&*25_gems_&*2_'4hr_time_candy'", "0"],
    ["Catching_Coronation", "1", "Get_a_score_of_128+_in_the_Catching_Minigame,_beating_the_developers_highscore!", "*STEAM_EXCLUSIVE_&*25_gems_&*4hr_time_candy", "0"],
    ["Crystal_Superslam", "1", "Defeat_100_Crystal_Mobs._This_could_go_a_couple_rounds...", "*STEAM_EXCLUSIVE_&*20_gems_&*2_'2hr_time_candy'", "0"],
    ["Slumbering_Gamer", "1", "Claim_2000+_hours_of_AFK_progress_across_all_characters._So_lazy!", "*STEAM_EXCLUSIVE_&*12_gems_&*'12hr_time_candy'", "0"],
    ["My_First_Trophy!", "1", "Equip_any_trophy,_other_than_the_limited_edition_ones_which_don't_count_lol.", "*STEAM_EXCLUSIVE_&*25_gems_&*'4hr_time_candy'", "0"],
    ["A_Fish_Too_Far", "1000", "Catch_a_total_of_1000_fish_across_all_Fishing_Minigame_plays.", "*Beach_Background_&for_Title_Screen", "0"],
    ["Rat-a-tat-tat", "1", "Level_up_the_'FMJ'_Alchemy_bubble_to_Lv._30", "*RNG_item_unlock", "0"],
    ["Pillars_of_Sand", "1", "Defeat_250,000_Sandy_Pots_combined_across_all_characters._Forget_the_Pillars_of_Salt_though.", "*Desert_Oasis_BG_&for_Title_Screen", "0"],
    ["Vial_Connoisseur", "1", "Get_6_vials_to_Lv._7,_which_are_the_pink_ones", "*RNG_item_unlock", "0"],
    ["Coarse_Cards", "1", "Level_up_cards_for_Mafioso,_Sandcastle,_Pincermin,_and_Mashed_Potato,_all_up_to_1_star.", "*Coarse_Mountains_BG_&for_Title_Screen", "0"],
    ["Trial_by_Time", "1", "Run_from_Town_to_Efaunt's_Tomb_in_under_2_minutes._No_teleporting_using_the_World_Map.", "*{2%_Arcade_balls/hr", "0"],
    ["Golden_Obolden!", "1", "Have_15_Golden_Obols_equipped_at_once._The_Family_tab_counts_here!", "{20%_Obol_Fragments_&gained_when_trashing_&obols", "0"],
    ["Monocle_No_More", "1", "Defeat_160_Sand_Giants_within_10_minutes_of_entering_the_map._Auto_must_be_off.", "*Twilight_Desert_BG_&for_Title_Screen", "0"],
    ["Jellyfish_Jelly", "1", "Have_a_stack_of_exactly_6000_Jellyfish_in_your_Storage_Chest._I_heard_their_Jelly_goes_good_with_burgers_btw.", "*RNG_item_unlock", "0"],
    ["Super_Cereal", "1", "Have_a_stack_of_exactly_50,000_Sentient_Cereal_in_your_Storage_Chest.", "*W2_Colosseum_EZ-Access_&*W2_Shops_EZ-Access", "0"],
    ["Sweet_Victory", "1", "Get_a_Score_of_200,000_or_more_in_the_Sandstone_Colosseum", "*{2%_Arcade_balls/hr", "0"],
    ["Ink_Blot", "101", "Use_101_silver_pens_in_the_Post_Office", "20%_chance_to_keep_&silver_pens_after_&using_one", "0"],
    ["Demon_Demolisher", "1", "Defeat_the_big_hourglass_and_the_toilet_paper_guy!", "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Dumbo_Destroyer", "1", "Defeat_Chaotic_Efaunt._Look_out_for_the_kick,_kapow!", "*STEAM_EXCLUSIVE_&*35_gems_&*2_'2hr_time_candy'", "0"],
    ["Threadin'_the_Needle", "1", "Pass_through_the_teenie_tiny_Lava_hoop_in_the_Catching_Minigame._It_only_appears_if_you_go_through_25_hoops_in_a_row!", "{5%_catching_EXP_for_&all_characters", "0"],
    ["S-M-R-T", "1", "Level_up_the_'Smarty_Boi'_Alchemy_bubble_to_Lv._50", "-10%_Bubble_upgrading_&costs", "0"],
    ["Two_Desserts!", "2", "Have_the_YumYum_Sheriff_trophy_equipped,_while_also_having_another_in_your_inventory.", "{5%_faster_respawn_for_&YumYum_Desert_Monsters", "0"],
    ["Nuget_Nightmare", "1", "Kill_Crabbycakes_manually,_without_Auto_on,_until_one_drops_a_Nuget_Cake._Good_luck...", "*Nuget_Cake_Hat_Recipe", "0"],
    ["Bigtime_Bloacher", "1", "Have_a_stack_of_exactly_100,000_Bloaches_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Vial_Junkee", "1", "Get_10_vials_to_Lv._9,_which_are_the_hyperlight_Orange_ones._Stop_focusing_so_much_on_vials,_it's_not_healthy!", "{20%_Sigil_Charging_&Speed", "0"],
    ["Fruit_Salad", "1", "Have_a_stack_of_exactly_1,000,000_Fruit_Flies_in_your_Storage_Chest.", "{5%_catching_speed_&for_all_characters", "0"],
    ["Your_Skin,_My_Skin", "1", "Wear_the_Efaunt_helmet,_Ribcage,_Hipillium,_and_Ankles._Also_have_1_Efaunt_Obol_equipped.", "*Djonnuttown_Teleport", "0"],
    ["WAAAAAAAHH!", "1", "SECRET_ACHIEVEMENT_------------------------_Complete_all_available_Treasure_Hunts!_You_can_find_them_on_Youtube,_just_search_for_it!", "*{3%_Arcade_balls/hr", "0"],
    ["Bobjoepicklejar", "1", "SECRET_ACHIEVEMENT_------------------------_Pickles_belong_in_containers,_after_all!", "*{1%_Arcade_balls/hr", "0"],
    ["Fish_Aint_Biting", "1", "SECRET_ACHIEVEMENT_------------------------_I'm_tellin'_ya,_the_fish_ain't_bitin'_today_gosh_darn_it!", "{5%_Fishing_Exp_for_&all_characters", "0"],
    ["Skill_Master", "1", "SECRET_ACHIEVEMENT_------------------------_Goldric's_bag_of_peanuts_may_be_nearly_empty,_but_even_just_one_peanut_is_enough_for_some...", "*W2_Boss_Key_EZ-Access", "0"],
    ["Tomb_Raider", "1", "Defeat_Snakenhotep_on_his_1st_Difficulty.", "*{2%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Tomb_Defiler", "1", "Defeat_Snakenhotep_on_his_2nd_Difficulty.", "*{3%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Tomb_Completionist", "1", "Defeat_Snakenhotep_on_his_3rd_Difficulty.", "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Wazzzzam!", "125", "Wazam_125_rooms_in_Snakenhotep's_Dungeon_by_performing_exceptionally_well_in_a_room.", "*{6%_Multikill_bonus_&for_all_characters", "0"],
    ["Just_Passing_By", "30", "Pass_30_rooms_in_Snakenhotep's_Dungeon_by_doing_the_thingy_the_room_says_to_do.", "*{2%_Multikill_bonus_&for_all_characters", "0"],
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
    ["A_Family_of_Me!", "1", "Create_your_8th_character,_who_will_never_get_the_love_you_gave_to_your_earlier_characters_when_making_new_ones_was_still_special.", "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Croakin'_Froge", "1", "Have_a_stack_of_exactly_250_Doge_-I_mean_froge-_critters_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Sad_Souls", "1", "Have_a_stack_of_exactly_1,000_Forest_Souls_in_your_Storage_Chest.", "*{1%_Arcade_balls/hr", "0"],
    ["Checkout_Takeout", "1000", "Checkout_a_total_of_1000_talent_books_from_the_Talent_Book_Library", "*{5_Book_Max_LV_&*{30%_Library_charge_&rate", "0"],
    ["Yawning_Cogs", "1", "Have_4_unclaimed_Yellow_Cogs_during_any_single_moment_in_time,_apart_from_March_16,_2022_at_3.07pm", "*{2%_Arcade_balls/hr", "0"],
    ["Blunder_Skull", "1", "Get_a_Copper_Skull_or_higher_on_every_Blunder_Hills_monster_in_the_Deathnote.", "*RNG_item_unlock", "0"],
    ["Too_Cute_To_Live", "1", "You're_gonna_kill_all_them_lil'_poofs?_You_monster..._well,_at_least_make_it_quick,_like_20s_or_less_after_entering_the_map.", "*{5%_Total_Multikill_&on_all_monsters", "0"],
    ["Big_Mobs_Eek", "5", "Defeat_5_Giant_Monsters._Giants_only_spawn_IF_you_equip_the_Titan_Tachion_prayer,_unlocked_by_beating_wave_10_of_Waka_Tower_Defence_(world_2)", "*STEAM_EXCLUSIVE_&*15_gems_&*2_'2hr_time_candy'", "0"],
    ["Powdered_Neutronium", "1", "Rank_up_the_Explosive_Combustion_refinery_chamber_to_Rank_2.", "*STEAM_EXCLUSIVE_&*15_gems_&*3_'2hr_time_candy'", "0"],
    ["Soulslike", "1", "Have_4_Prayers_in_your_Prayer_Rock_thingy._You_get_Prayers_by_placing_these_wizard_dudes_into_towers_and_stuff_and_kickin'_butt!", "*{2%_Arcade_balls/hr", "0"],
    ["Good_Times_Roll", "1", "Beat_wave_50_in_Glublin_Gorefest_using_ONLY_Boulder_Roller_wizards._No_freeze,_no_confetti,_just_boulder.", "*RNG_item_unlock", "0"],
    ["Cog_in_the_System", "1", "Have_20_Grey_Cogs_placed_on_the_board_at_once._Not_sure_why_this_is_an_achievement,_cogs_are_boring.", "*{5%_Build_Speed_&in_Construction", "0"],
    ["I_Create...", "1", "Upgrade_buildings_in_construction_a_total_of_50_times._Any_buildings,_utilities,_wizards,_shrines,_they_all_count!", "*{1%_Arcade_balls/hr", "0"],
    ["I_Sawed...", "1", "Upgrade_buildings_in_construction_a_total_of_250_times.", "*RNG_item_unlock", "0"],
    ["Hairy_Ice_Comb", "3000", "Manually_loot_1000_floof_poofs,_melty_cubes,_and_moustache_comb_stacks_--_AFK_claiming_doesn't_count.", "*Frosty_Peaks_BG_&for_Title_Screen", "0"],
    ["Giant_Slayer", "25", "Defeat_5_Giant_Mobs_of_each_type;_Bloque,_Mamooth,_Snowman,_Penguin,_Thermister._Do_it_in_that_monster_order.", "*Tundra_Outback_BG_&for_Title_Screen", "0"],
    ["Saharan_Skull", "1", "Get_a_Golden_Skull_or_higher_on_every_YumYum_Desert_monster_in_the_Deathnote.", "*{1%_Printer_Sample_&Rate", "0"],
    ["Fat_Souls", "1", "Have_a_stack_of_exactly_10,000_Dune_Souls_in_your_Storage_Chest.", "*Start_with_{15_&more_points_in_Worship_&Tower_Defence", "0"],
    ["Borrowed_Pens", "1", "Remember_all_those_pens_you_lent_out_in_school_and_never_got_back?_You've_got_13_seconds_to_vent_your_anger_on_every_penguin_mob!", "*{3%_Arcade_balls/hr", "0"],
    ["Large_Fortune", "1", "Save_up_100,000,000_coins._But_remember,_as_far_as_the_idleon_government_knows,_none_of_those_coins_came_from_a_taxable_income_wink_wink.", "*STEAM_EXCLUSIVE_&*25_gems", "0"],
    ["Sqeakin'_Mousey", "1", "Have_a_stack_of_exactly_60,000_Mouseys_in_your_Storage_Chest._Imagine_the_noise_in_that_chest_of_yours..._or_even_the_smell,_ugh.", "*Hunters_Grove_BG_&for_Title_Screen", "0"],
    ["Geared_for_Success", "1", "Have_40_Yellow_Cogs_placed_on_the_board_at_once._Alright_now_I_see_how_this_is_achievement_worthy,_cogs_are_kinda_neat.", "*{5%_Construction_EXP_&gain", "0"],
    ["Guild_Higher-Up", "1", "Contribute_3,000_GP_to_your_guild,_putting_you_above_the_other_guild_members_who_only_have_the_500_GP_Achievment!", "*STEAM_EXCLUSIVE_&*22_gems", "0"],
    ["Legendary_Gamer", "1", "Reach_level_100_on_any_character!_Just_4_more_digits_and_you'd_have_a_phone_number!", "*STEAM_EXCLUSIVE_&*23_gems", "0"],
    ["Entangled_Compounds", "1", "Rank_up_the_Spontaneous_Combustion_refinery_chamber_to_Rank_3.", "*{5_'Tab_3'_Talent_Pts", "0"],
    ["There_Can_Be_Only_1", "1", "Beat_wave_50_of_Wakawaka_War_without_using_more_than_1_of_any_specific_tower._Can't_have_2_pulsers,_or_2_frozones!", "*STEAM_EXCLUSIVE_&*25_gems_&*3_'12hr_time_candy'", "0"],
    ["Blurple_Skull", "1", "Get_a_Dementia_Skull_or_higher_on_every_Frostbite_Tundra_monster_in_the_Deathnote.", "*STEAM_EXCLUSIVE_&*30_gems_&*5_'72hr_time_candy'", "0"],
    ["Souped_Up_Salts", "1", "Rank_up_the_Redox_Combustion_refinery_chamber_to_Rank_10.", "*RNG_item_unlock", "0"],
    ["I_Constructed!", "1", "Upgrade_buildings_in_construction_a_total_of_900_times.", "*{10_'Tab_3'_Talent_Pts", "0"],
    ["Cogs_Be_Waitin'", "1", "Have_16_unclaimed_Grey_Cogs_at_once._Jeez,_I'm_glad_anthropomorphic_cogs_aren't_real.", "*{4%_Arcade_balls/hr", "0"],
    ["Simpin'_for_NPC's", "1", "Complete_150_unique_quests_on_a_single_character._Apparently_people_find_'simp'_offensive,_and_I'm_kinda_offended_by_that...", "*STEAM_EXCLUSIVE_&*24_gems", "0"],
    ["Top_Cogs", "1", "78_Cogs._All_purple_cogs._Did_I_say_cogs_are_great?_I_think_cogs_are_great._Cog_cog_cog!", "*W3_Boss_Key_EZ-Access", "0"],
    ["Card_Dude", "1", "Collect_120_unique_cards._Not_sure_why_something_as_mundane_as_'dude'_is_the_descriptor_here,_don't_read_too_much_into_it.", "*STEAM_EXCLUSIVE_&*24_gems", "0"],
    ["Crystal_Champ", "1", "Defeat_2000_crystal_mobs._You_must've_watched_a_whole_lotta_Dev_Streams_to_get_this!", "*STEAM_EXCLUSIVE_&*30_gems_&*12hr_time_candy", "0"],
    ["Smirky_Souls", "1", "Have_a_stack_of_exactly_250,000_Rooted_Souls_in_your_Storage_Chest.", "*RNG_item_unlock", "0"],
    ["Comatosed_Gamer", "1", "Claim_30,000+_Hrs_of_AFK_gains._Thats_two_years,_woah!", "*STEAM_EXCLUSIVE_&*25_gems_&*24hr_time_candy", "0"],
    ["Knock_on_Wood", "1", "Beat_wave_50_of_Acorn_Assault_with_just_4_towers_active._Place_down_a_5th_tower_at_any_time,_and_it_wont_count!", "*{3%_Arcade_balls/hr", "0"],
    ["The_Goose_is_Loose", "1", "Have_a_HONK_of_exactly_1,000,000_Honkers_in_your_HONK_Chest._HONKHONKHONK_HOOOONK!!!", "*HONK_Hat_Recipe", "0"],
    ["Sepia_Vision", "1", "Have_a_stack_of_exactly_500_Black_Lenses_in_your_Storage_Chest._Better_complete_this_before_I_make_it_1,000!", "*Crystal_Caverns_BG_&for_Title_Screen", "0"],
    ["Rattle_them_Bones", "1", "Defeat_every_Bloodbone_in_just_12_seconds_after_entering_the_map._Wow,_wild.", "*Pristalle_Lake_BG_&for_Title_Screen", "0"],
    ["A_Most_Nice_Sale", "1", "SECRET_ACHIEVEMENT_------------------------_You_SOLD_gems_to_the_World_3_town_store...?_All_at_once?_How_many...?_Nice.", "*STEAM_EXCLUSIVE_&*1_gem_&*1_'24hr_time_candy'", "0"],
    ["Cool_Score!", "1", "Get_a_Score_of_2,500,000_or_more_in_the_Chillsnap_Colosseum", "*W3_Colosseum_EZ-Access_&*W3_Shops_EZ-Access", "0"],
    ["Dungeon_Wallop", "1", "Deal_25000_or_more_damage_in_a_single_hit_within_any_Dungeon.", "*{4%_Crit_Chance_Bonus_&for_all_characters_&outside_of_dungeon", "0"],
    ["Boss_Defeated", "1", "Defeat_Glaciaxus_on_its_1st_difficulty", "*{2%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Manager_Defeated", "1", "Defeat_Glaciaxus_on_its_2nd_difficulty", "*{3%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Kingpin_Defeated", "1", "Defeat_Glaciaxus_on_its_3rd_difficulty", "*{5%_Total_DMG_for_all_&characters_outside_&of_dungeons", "0"],
    ["Capitalist_Win", "1000", "Complete_1000_jobs_within_the_Glacial_Basement_dungeon.", "*{5%_Class_EXP_for_all_&characters_outside_&of_dungeons", "0"],
    ["Equinox_Visitor", "1", "Find_the_Equinox_Mirror_drop_from_Bloodbones,_a_1_in_1000_drop,_and_use_it_to_visit_the_Equinox_Valley.", "*{4%_Total_DMG_for_all_&characters", "0"],
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
    ["Bland_Dish", "1", "SECRET_ACHIEVEMENT_------------------------_What_exactly_were_you_expecting_to_cook,_an_invisible_meal?", "{6_Tab_1_&Talent_Pts", "0"],
    ["Lv._5_Nothing", "1", "SECRET_ACHIEVEMENT_------------------------_Ah,_I_see_you_enjoy_reading_upgrade_flavor_text_as_well!", "*STEAM_EXCLUSIVE_&*30_gems_&*2_'12hr_time_candy'", "0"],
    ["I_Like_This_Pet", "1", "Get_a_Breedability_III_heart_on_at_least_2_Pets_within_the_nest.", "Pet_Breedability_&multiplier_goes_up_&1.20x_faster", "0"],
    ["I_LOVE_These_Pets", "1", "Get_a_Breedability_VII_heart_on_at_least_15_pets_within_the_nest.", "{10_Tab_3_&Talent_Pts", "0"],
    ["Shiny_Shells", "1", "Have_6_bronze_(or_rarer)_eggs_in_your_nest_at_the_same_time,_waiting_to_be_hatched!", "{10%_Faster_Egg_&Incubator_Speed", "0"],
    ["Gilded_Shells", "1", "Have_12_gold_(or_rarer)_eggs_in_your_nest_at_the_same_time,_waiting_to_be_hatched!", "Eggs_increase_in_&rarity_1.10x_more_&often", "0"],
    ["Barley_Lost", "1", "Fail_a_pet_battle_with_the_enemy_team_having_only_5%_HP_or_less._Wait,_it's_spelled_HOW???", "{5%_Pet_Fight_&Damage", "0"],
    ["Petless", "1", "Trash_a_total_of_2500_pets._How_could_you_be_so_heartless,_so_cold...", "*STEAM_EXCLUSIVE_&*50_gems_&*1_'72hr_time_candy'", "0"],
    ["Cabbage_Patch", "1", "Have_5_kitchens_all_cooking_cabbages_at_the_same_time._Remember_gamers,_eat_your_vegetables,_they_ain't_so_bad!", "{10%_Meal_Cooking_&Speed", "0"],
    ["Le_Pretzel_Bleu", "1", "Have_8_kitchens_all_cooking_Pretzels_at_the_same_time._Don't_get_it_twisted,_them_pretzels_are_the_real_deal.", "{20%_Meal_Cooking_&Speed", "0"],
    ["Michelin_Ranked", "1", "Upgrade_any_kitchen_stat_to_Lv._300,_giving_you_an_elite_crown_over_the_upgrade_bars,_thus_resulting_in_dopamine.", "*RNG_item_unlock", "0"],
    ["WOAH_That's_Fast", "1", "Have_a_speed_of_'Too_Fast'_displayed_while_cooking_an_Eggplant._No_this_is_not_a_metaphor.", "*{2%_Arcade_balls/hr", "0"],
    ["Stars_Among_Stars", "1", "Complete_all_constellations_in_the_Hyperion_Nebula._Thats_what_world_4_is_called_btw.", "*Eternity_Beach_BG_&for_Title_Screen", "0"],
    ["Chippin'_Away", "25", "Claim_25_chips_from_the_Chip_Repository._I_was_gonna_make_this_250_chips,_but_people_from_the_future_told_me_not_to.", "*{2%_Arcade_balls/hr", "0"],
    ["Hunned_Times_a_Day", "10000", "Claim_spices_by_any_means_10,000_times._Like,_individual_claims.", "{8_Tab_2_&Talent_Pts", "0"],
    ["Good_Plate", "1", "Upgrade_a_meal_at_the_Dinner_Menu_to_the_point_where_it_gets_a_diamond_plate!", "*RNG_item_unlock_&*W4_Shops_EZ-Access", "0"],
    ["Great_Plate", "1", "Upgrade_a_meal_at_the_Dinner_Menu_to_the_point_where_it_gets_a_purple_plate!", "*{2%_Arcade_balls/hr", "0"],
    ["Best_Plate", "1", "Upgrade_a_meal_at_the_Dinner_Menu_to_the_point_where_it_gets_a_void_pearl_plate!", "-10%_lower_cost_&to_upgrade_meals_&at_the_Dinner_Table", "0"],
    ["Space_Party!!!", "1", "Dance_with_at_least_5_other_people_while_you're_all_in_World_4_town!", "*{2%_Arcade_balls/hr", "0"],
    ["Zero_G_Scorin'", "1", "Get_a_Score_of_10,000,000_or_more_in_the_Astro_Colosseum", "{5%_Cash_from_&Monsters", "0"],
    ["Hibernating_Gamer", "1", "Glaim_111,000_hours_of_AFK_time._Jeez,_thats_like_an_entire_year_of_all_characters_idling_to_the_max.", "*STEAM_EXCLUSIVE_&*100_gems_&*1_'72hr_time_candy'", "0"],
    ["Mutant_Massacrer", "1", "Defeat_both_Mutant_Minibosses,_the_W3_Slush_and_W4_Mush._You_must_defeat_Slush_before_Mush,_in_that_order.", "*STEAM_EXCLUSIVE_&*RNG_item_unlock_&*Some_Gems_and_Candy", "0"],
    ["Soda_Poisoning", "1", "Beat_wave_50_of_Clash_of_Cans_with_3_Poisonic_Elders_at_Lv_5_or_higher._Also,_you_can't_sell_towers.", "*Starfield_Belt_BG_&for_Title_Screen", "0"],
    ["The_True_King", "1000000", "Reach_a_total_of_1_million_Orb_Kills.", "{10_Tab_4_Talent_Pts", "0"],
    ["The_True_Pirate", "1000000", "Reach_a_total_of_1_million_Plunderous_Kills._This_one_is_the_true_challenge_of_the_three.", "{15_Tab_4_Talent_Pts_&{1%_Total_Dmg", "0"],
    ["The_True_Emperor", "1000000", "Reach_a_total_of_1_million_Wormhole_Kills.", "{12_Tab_4_Talent_Pts", "0"],
    ["Veritable_Master", "1", "SECRET_ACHIEVEMENT_------------------------_Destruction_comes_to_all_who_cross_your_path,_no_matter_how_many_times_you_cross_paths.", "{1_Void_Talent_Pt", "0"],
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
    ["Supernatural_Gamer", "1", "Reach_level_300_on_any_character!_My_oh_my!_This_would_have_been_inconceivable_just_a_few_years_ago!", "{10%_All_Skill_EXP", "0"],
    ["Smokin'_Stars", "1", "Complete_all_constellations_in_the_Smolderin'_Plateau._You_can_check_your_progress_within_the_Telescope.", "{20%_All_Skill_EXP", "0"],
    ["The_Plateauourist", "1", "Reach_World_5,_a_personal_favorite_world_of_mine!_Look,_I_like_lava_what_can_I_say.", "{4_Daily_Crystal_Mob_&Spawn_Guarantee", "0"],
    ["No_Krakens?_):", "1", "Reach_Wave_50_of_Citric_Conflict_tower_defence_without_placing_a_single_Kraken_Towers._Not_even_one.", "{25%_Class_EXP", "0"],
    ["Artifact_Finder", "1", "Collect_15_Artifacts_from_Sailing", "*1_Extra_Chest_Slot_in_&Sailing_Loot_Pile", "0"],
    ["Artifact_Enjoyer", "1", "Collect_all_30_Artifacts_from_Sailing", "*Magma_Rivertown_BG", "0"],
    ["Artifact_Jones", "1", "Collect_all_30_ANCIENT_Artifacts_from_Sailing._All_that_glitters_is_not_gold,_but_it_sure_is_shiny!", "{20_Star_Talent_Pts", "0"],
    ["Gilded_Vessel", "1", "Upgrade_a_boat_to_Lv_100_in_Sailing._It'll_turn_gold_to_reflect_its_power!", "*1_Extra_Chest_Slot_in_&Sailing_Loot_Pile", "0"],
    ["Maroon_Warship", "1", "Upgrade_a_boat_to_Lv_300_in_Sailing._This_is_the_pinnacle_of_naval_prowess,_it_doesn't_get_fancier_than_this!", "{1_Lv_to_all_Talents_&for_all_characters", "0"],
    ["Glory_To_Nobisect", "1", "Unlock_the_3rd_Divinity_God.", "{10_'Tab_4'_Talent_Pts", "0"],
    ["All_Hail_Purrmep", "1", "Unlock_the_7th_Divinity_God.", "{10_Alternate_Particle_&Alchemy_Upgrades_Per_&Day", "0"],
    ["Long_Live_Bagur", "1", "Unlock_the_10th_and_final_Divinity_God.", "{10%_All_Skill_EXP", "0"],
    ["POiNG_Champion", "1", "Get_a_POiNG_score_of_25,000_or_more!_My_personal_highscore_is_38,323_at_the_time_of_coding_this!", "{10_'Tab_4'_Talent_Pts", "0"],
    ["Lucky_Harvest", "1", "Harvest_a_plant_with_a_Bit_worth_who's_first_3_digits_are_777._For_example,_77.7K_Bits_would_count,_or_777M_Bits_too!", "*1.05x_Bit_Gain_in_&Gaming", "0"],
    ["Chemical_Collector", "1000", "Harvest_a_total_of_1000_Chemical-type_Plants_in_Gaming.", "{3%_Damage_for_all_&characters", "0"],
    ["Voraci_Vantasia", "500", "Harvest_a_total_of_500_Voraci-type_Plants_in_Gaming.", "{10%_Divinity_Points_&Gained", "0"],
    ["Bonsai_Bonanza", "100", "Harvest_a_total_of_100_Bonsai-type_Plants_in_Gaming.", "*W5_Shop_EZ-Access", "0"],
    ["Perfect_Trade_Deal", "1", "Make_a_trade_with_Blobby_G_worth_a_gold_bar_amount_that_starts_with_777,_like_777K_or_7.77M_for_example._PS;_776_and_778_work_too_lol", "{1_additional_Treasure_&Per_Chest_for_Sailing", "0"],
    ["True_Naval_Captain", "1", "Buy_all_20_Boats_in_Sailing._Uh,_yea,_there_is_a_scroll_bar_below_the_boats,_you_can_buy_more_than_5_boats_#", "{20%_Captain_EXP_&for_sailing", "0"],
    ["Legendary_Orb", "1", "On_your_Divine_Knight,_get_an_Orb_Score_of_400_or_more_on_OJ_Bay._This_is_the_number_above_your_Orb!", "*Smoggy_Basin_BG", "0"],
    ["Legendary_Flag", "1", "On_your_Siege_Breaker,_get_a_Flag_Score_of_150_or_more_on_Erruption_River._This_is_the_number_above_your_Flag!", "{2%_Damage_for_all_&characters", "0"],
    ["Legendary_Wormhole", "1", "On_your_Elemental_Sorcerer,_get_a_Wormhole_Score_of_83_or_more_on_Niagrilled_Falls._This_is_the_number_above_your_Wormhole!", "{10%_Divinity_Points_&Gained", "0"],
    ["Utter_DISRESPECT", "1", "SECRET_ACHIEVEMENT_------------------------_Why_did_you_even_hire_the_poor_fella_in_the_first_place???", "{20_Star_Talent_Pts", "0"],
    ["Sneaky_Stealing", "1", "SECRET_ACHIEVEMENT_------------------------_Walk_to_a_uh..._weird_location?_Well_it's_not_that_weird,_but_it's_just_like,_what_ya_doin'_back_there?", "{25%_Shop_Capacity_&for_all_Town_Shops", "0"],
    ["Broken_Controller", "1", "SECRET_ACHIEVEMENT_------------------------_You_got..._zero?_Literally_zero??_Jeez,_Im_sorry_but_I_think_you_need_to_uninstall_^", "*1.05x_Bit_Gain_in_&Gaming", "0"],
    ["Lavathian_Skulls", "1", "Get_a_Lava_Skull_or_higher_on_every_Smolderin'_Plateau_monster_in_the_Deathnote._Yea,_the_100M_Kill_Skull._This_is_gonna_take_a_while.", "{2%_Faster_Monster_&Respawn_Time_for_&All_World_5_mobs", "0"],
    ["Seaworthy_Captain", "1", "Level_up_a_Sailing_Captain_to_Lv_15._Few_captains_in_the_universe_can_rival_their_ability_to_plunder!", "{1%_ALL_STAT_for_&all_characters", "0"],
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
    ["Valley_Visitor", "1", "Reach_World_6,_the_Spirited_Valley!_You'll_love_it_here,_all_the_spirits_are_very_friendly!", "{10%_Money_for_all_&characters", "0"],
    ["Scorin'_the_Ladies", "1", "Have_a_stack_of_exactly_250,000_Ladybugs_in_your_Storage_Chest.", "{10%_Catching_&Efficiency", "0"],
    ["Effervess_Enthusiess", "1", "Have_a_stack_of_exactly_5,000,000_Effervescent_Logs_in_your_Storage_Chest.", "{10%_Choppin_Efficiency", "0"],
    ["That's_MY_Crown", "1", "Have_a_stack_of_exactly_100,000,000_Royal_Headpiece_in_your_Storage_Chest.", "*Dharma_Mesa_BG", "0"],
    ["Leet_Lanterns", "1", "SECRET_ACHIEVEMENT_------------------------_Oh_yea,_that's_a_good_number._Sure,_it's_no_69420,_but_it's_vintage!", "{4%_Damage_for_all_&characters", "0"],
    ["Lil'_Overgrowth", "1", "Get_an_overgrowth_of_32x_on_a_single_crop.", "*1.05x_Crop_Evo_&chance", "0"],
    ["Major_Overgrowth", "1", "Get_an_overgrowth_of_1,024x_on_a_single_crop.", "{15%_Farming_EXP", "0"],
    ["Unreal_Overgrowth", "1", "Get_an_overgrowth_of_8,192x_on_a_single_crop.", "{20%_Class_EXP", "0"],
    ["Doctor_Repellant", "1", "Have_10,000_or_more_Apple_crops_in_your_Depot_at_once._You_can_lock_the_first_crop_before_it_grows_to_guarantee_an_apple!", "*W6_Shop_EZ_Access", "0"],
    ["Cob_Enjoyer", "1", "Have_1,000,000_or_more_Corn_crops_in_your_Depot_at_once._Mmmm,_Corn!", "{15%_All_Skill_EXP", "0"],
    ["Science_Undergrad", "1", "Find_30_unique_crops,_as_shown_by_the_Crop_Scientist!", "{10%_Farm_EXP", "0"],
    ["Science_Graduate", "1", "Find_70_unique_crops,_as_shown_by_the_Crop_Scientist!", "*Spirit_Fields_BG", "0"],
    ["Science_Post_Doc", "1", "Find_110_unique_crops,_as_shown_by_the_Crop_Scientist!", "{1%_All_Stat_&for_all_characters", "0"],
    ["Crop_Flooding", "1", "SECRET_ACHIEVEMENT_------------------------_That's..._That's_enough..._THAT'S_ENOUGH_WATER!_THAT'S_ENOUGH!", "{5%_Magic_Beans_&from_Legumulyte", "0"],
    ["Legumulucky", "1", "Make_a_crop_trade_with_the_Legumulyte_worth_exactly_777_magic_beans.", "{2%_Damage_for_all_&characters", "0"],
    ["Big_Time_Land_Owner", "1", "Get_27_plots_of_land_in_your_farm.", "*1.15x_Crop_OG_Chance", "0"],
    ["Ceramic_Sneaking", "1", "Reach_the_Sneaking_Floor_with_the_Petrified_Ceramist_guest.", "*1.03x_Jade_Gain", "0"],
    ["Top_Floor_Sneaking", "1", "Reach_what_seems_like_the_top_Floor_of_Sneaking_with_the_Eldar_Kingulyte_guest.", "*1.07x_Jade_Gain", "0"],
    ["Untying_Extraordinaire", "1", "Untie_6_other_Ninja_Twins.", "*1.05x_Stealth_for_&all_Ninja_Twins", "0"],
    ["Lucky_Stealy", "1", "Successfully_find_6_items_in_a_row,_in_a_single_AFK_claim_within_Sneaking.", "*1.05x_Jade_Gain", "0"],
    ["Yellow_Belt", "1", "Find_a_论50_Yellow_Belt_Sneaking_Charm._Yes,_exactly_论50.", "{10%_Sneaking_EXP_gain", "0"],
    ["Straw_Hat_Stacking", "1", "SECRET_ACHIEVEMENT_------------------------_It's_a_shame_you_can't_wear_them_all_at_once...", "*1.01x_DMG_Multiplier_&for_all_characters", "0"],
    ["Best_Bloomie", "1", "Get_a_Bloomy_Summoning_Familiar.", "*1.05x_All_Essence_&Gain", "0"],
    ["Regalis_My_Beloved", "1", "Get_a_Regalis_Summoning_Familiar.", "*1.01x_larger_Winners_&Bonuses_from_Summoning", "0"],
    ["This,_is,_Summoning!", "1", "Survive_for_200_seconds_in_the_Endless_Summoning_Mode,_which_isn't_out_yet.", "*1.05x_All_Essence_&Gain", "0"],
    ["Summoning_CM", "1", "Get_10_Career_Wins_within_Summoning", "{3%_Damage_for_all_&characters", "0"],
    ["Summoning_IM", "1", "Get_25_Career_Wins_within_Summoning", "{20%_Money_for_all_&characters", "0"],
    ["Summoning_GM", "1", "Get_58_Career_Wins_within_Summoning", "{6%_Drop_Chance_&for_all_characters", "0"],
    ["Penta_Defence", "1", "Reach_Wave_50_in_Breezy_Battle_without_placing_more_than_5_Towers_in_total.", "*Lullaby_Airways_BG", "0"],
    ["Spectre_Stars", "1", "Complete_all_constellations_in_the_Spirited_Valley._You_can_check_your_progress_within_the_Telescope.", "*1.01x_larger_Winners_&Bonuses_from_Summoning", "0"],
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
    "Death Bringer": [
        195, 196, 197, 198, 199,
        200, 201, 202, 203, 204,
        205, 206, 207, 208, 209
    ],
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
    "VIP": [
        641, 642, 643, 644, 645
    ],
}
hardcap_symbols = 280  #Last verified as of v2.23
hardcap_enhancement_eclipse = 250  #Lava might add more in the future, but there are no bonuses above 250 in v2.10
librarySubgroupTiers = [
    '', 'Skilling - High Priority', 'Skilling - Medium Priority', 'Skilling - Low Priority', 'Skilling - Lowest Priority',
    'Combat - High Priority', 'Combat - Medium Priority', 'Combat - Low Priority', 'ALL Unmaxed Talents'
]  #Why is there a placeholder in [0] again?
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
            460: {"Name": "Log on Logs", "Tab": "Tab 2"},
            445: {"Name": "Smart Efficiency", "Tab": "Tab 1"},
            462: {"Name": "Deforesting All Doubt", "Tab": "Tab 2"},
            461: {"Name": "Leaf Thief", "Tab": "Tab 2"},
            539: {"Name": "Symbols of Beyond P", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            532: {"Name": "Skill Wiz", "Tab": "Tab 4"},
        },
        "Medium": {
            533: {"Name": "Utmost Intellect", "Tab": "Tab 4"},
            456: {"Name": "Unt'WIS'ted Robes", "Tab": "Tab 2"},
            459: {"Name": "Individual Insight", "Tab": "Tab 2"},
            488: {"Name": "Wis Wumbo", "Tab": "Tab 3"},
            449: {"Name": "Active Afk-er", "Tab": "Tab 1"},
        },
        "Low": {
            452: {"Name": "Mana Overdrive", "Tab": "Tab 2"},
            472: {"Name": "Staring Statues", "Tab": "Tab 3"},
            487: {"Name": "Stupendous Statues", "Tab": "Tab 3"},
            1: {"Name": "Mana Booster", "Tab": "Tab 1"},
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            486: {"Name": "Occult Obols", "Tab": "Tab 3"},
        },
        "Lowest": {
            464: {"Name": "Inner Peace", "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
    "Alchemy": {
        "Medium": {
            492: {"Name": "Bubble Breakthrough", "Tab": "Tab 3"},
        },
        "Low": {
            493: {"Name": "Sharing Some Smarts", "Tab": "Tab 3"},  # Account-wide EXP bumped to Low
        },
    },
    "Lab": {
        "Low": {
            538: {"Name": "Upload Squared", "Tab": "Tab 4"},
            537: {"Name": "Essence Transferral", "Tab": "Tab 4"},
            536: {"Name": "Green Tube", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
        },
    },
    "Worship": {
        "High": {
            476: {"Name": "Sooouls", "Tab": "Tab 3"},
        },
        "Medium": {
            303: {"Name": "Stop Right There", "Tab": "Tab 3"},
        },
        "Low": {
            478: {"Name": "Nearby Outlet", "Tab": "Tab 3"},
            475: {"Name": "Charge Syphon", "Tab": "Tab 3", 'Hardcap': 200},
        },
        "Lowest": {
            477: {"Name": "Bless Up", "Tab": "Tab 3"},
        },
    },
    "Divinity": {
        "Medium": {
            505: {"Name": "Polytheism", "Tab": "Tab 4"},  # Account-wide divinity points
            506: {"Name": "Shared Beliefs", "Tab": "Tab 4"},  # Account-wide EXP bumped to Medium because Divinity extra important
        },
    },
    #Strength Skills
    'Farming': {
        'High': {
            207: {'Name': 'Dank Ranks', 'Tab': 'Tab 5'}
        },
        'Medium': {
            205: {'Name': 'Mass Irrigation', 'Tab': 'Tab 5'}
        },
        'Low': {
            206: {'Name': "Agricultural 'Preciation", 'Tab': 'Tab 5'}
        },
    },
    "Cooking": {
        "High": {
            148: {"Name": "Overflowing Ladle", "Tab": "Tab 4"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
        },
        "Medium": {
            146: {"Name": "Apocalypse Chow", "Tab": "Tab 4"},
        },
        "Low": {
            147: {"Name": "Waiting to Cool", "Tab": "Tab 4"},
        },
    },
    "Fishing": {
        "High": {
            115: {"Name": "Worming Undercover", "Tab": "Tab 3"},
            85: {"Name": "Brute Efficiency", "Tab": "Tab 1"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            142: {"Name": "Skill Strengthen", "Tab": "Tab 4"},
        },
        "Medium": {
            99: {"Name": "Haungry for Gold", "Tab": "Tab 2"},
            143: {"Name": "Overblown Testosterone", "Tab": "Tab 4"},
            96: {"Name": "'STR'ess Tested Garb", "Tab": "Tab 2"},
            94: {"Name": "Firmly Grasp It", "Tab": "Tab 2"},
            98: {"Name": "Absolute Unit", "Tab": "Tab 2"},
            81: {"Name": "Str Summore", "Tab": "Tab 3"},
            89: {"Name": "Idle Skilling", "Tab": "Tab 1"},
            118: {"Name": "Catching Some Zzz's", "Tab": "Tab 3"},
        },
        "Low": {
            112: {"Name": "Strongest Statues", "Tab": "Tab 3"},
            116: {"Name": "Bobbin' Bobbers", "Tab": "Tab 3", 'Hardcap': 200},
            111: {"Name": "Fistful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            117: {"Name": "All Fish Diet", "Tab": "Tab 3"},
        },
    },
    "Mining": {
        "High": {
            100: {"Name": "Big Pick", "Tab": "Tab 2"},
            85: {"Name": "Brute Efficiency", "Tab": "Tab 1"},
            103: {"Name": "Tool Proficiency", "Tab": "Tab 2"},
            101: {"Name": "Copper Collector", "Tab": "Tab 2"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            142: {"Name": "Skill Strengthen", "Tab": "Tab 4"},
        },
        "Medium": {
            99: {"Name": "Haungry for Gold", "Tab": "Tab 2"},
            143: {"Name": "Overblown Testosterone", "Tab": "Tab 4"},
            96: {"Name": "'STR'ess Tested Garb", "Tab": "Tab 2"},
            94: {"Name": "Firmly Grasp It", "Tab": "Tab 2"},
            98: {"Name": "Absolute Unit", "Tab": "Tab 2"},
            81: {"Name": "Str Summore", "Tab": "Tab 3"},
            89: {"Name": "Idle Skilling", "Tab": "Tab 1"},
        },
        "Low": {
            92: {"Name": "Health Overdrive", "Tab": "Tab 2"},
            127: {"Name": "Shieldiest Statues", "Tab": "Tab 3"},
            112: {"Name": "Strongest Statues", "Tab": "Tab 3"},
            95: {"Name": "Strength in Numbers", "Tab": "Tab 2"},
            0: {"Name": "Health Booster", "Tab": "Tab 1"},
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            111: {"Name": "Fistful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            104: {"Name": "Tempestuous Emotions", "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
    "Construction": {
        "Medium": {
            131: {"Name": "Redox Rates", "Tab": "Tab 3"},
        },
        "Low": {
            130: {"Name": "Refinery Throttle", "Tab": "Tab 3", "Optimal": [0, 8, True]},
        },
        "Lowest": {
            132: {"Name": "Sharper Saws", "Tab": "Tab 3", 'Hardap': 160},
        },
    },
    "Gaming": {
        "Medium": {
            177: {"Name": "Bitty Litty", "Tab": "Tab 4"},
        },
        "Low": {
            175: {"Name": "Undying Passion", "Tab": "Tab 4"},
            176: {"Name": "One Thousand Hours Played", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
        },
    },
    #Agility Skills
    "Smithing": {
        "High": {},
        "Medium": {},
        "Low": {
            269: {"Name": "Broken Time", "Tab": "Tab 1"},
            281: {"Name": "Acme Anvil", "Tab": "Tab 2"},
        },
        "Lowest": {
            282: {"Name": "Yea I Already Know", "Tab": "Tab 2"},
            265: {"Name": "Focused Soul", "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
    "Catching": {
        "High": {
            263: {"Name": "Elusive Efficiency", "Tab": "Tab 1"},
            295: {"Name": "Teleki-net-ic Logs", "Tab": "Tab 3"},
            296: {"Name": "Briar Patch Runner", "Tab": "Tab 3"},
            374: {"Name": "Symbols of Beyond G", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            367: {"Name": "Skill Ambidexterity", "Tab": "Tab 4"},
        },
        "Medium": {
            298: {"Name": "Sunset on the Hives", "Tab": "Tab 3"},
            368: {"Name": "Adaptation Revelation", "Tab": "Tab 4"},
            276: {"Name": "Garb of Un'AGI'ng Quality", "Tab": "Tab 2"},
            278: {"Name": "Sanic Speed", "Tab": "Tab 2"},
            293: {"Name": "Agi Again", "Tab": "Tab 3"},
        },
        "Low": {
            292: {"Name": "Shwifty Statues", "Tab": "Tab 3"},
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            291: {"Name": "Shoeful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            282: {"Name": "Yea I Already Know", "Tab": "Tab 2"},
            265: {"Name": "Focused Soul", "Tab": "Tab 2"},
            297: {"Name": "Bug Enthusiast", "Tab": "Tab 3"},
        },
    },
    "Sailing": {
        "Low": {
            326: {"Name": "Expertly Sailed", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
            327: {"Name": "Captain Peptalk", "Tab": "Tab 4"},  # Account-wide Captain EXP bumped to low
        },
    },
    "Trapping": {
        "High": {
            263: {"Name": "Elusive Efficiency", "Tab": "Tab 1"},
            311: {"Name": "Invasive Species", "Tab": "Tab 3"},
            310: {"Name": "Eagle Eye", "Tab": "Tab 3"},
            374: {"Name": "Symbols of Beyond G", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            367: {"Name": "Skill Ambidexterity", "Tab": "Tab 4"},
        },
        "Medium": {
            368: {"Name": "Adaptation Revelation", "Tab": "Tab 4"},
            276: {"Name": "Garb of Un'AGI'ng Quality", "Tab": "Tab 2"},
            278: {"Name": "Sanic Speed", "Tab": "Tab 2"},
            293: {"Name": "Agi Again", "Tab": "Tab 3"},
        },
        "Low": {
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            291: {"Name": "Shoeful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            282: {"Name": "Yea I Already Know", "Tab": "Tab 2"},
            265: {"Name": "Focused Soul", "Tab": "Tab 2"},
        },
    },
    "Breeding": {
        "High": {
            373: {"Name": "Curviture Of The Paw", "Tab": "Tab 4"},
        },
        "Low": {
            372: {"Name": "Shining Beacon of Egg", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
        },
    },
    # Utility is talents that apply to multiple skills at a bottom-of-the-group priority (Mostly Jman stuff + Drop Rate)
    "Utility": {
        "High": {
            43: {"Name": "Right Hand of Action", "Tab": "Tab 3"},
            32: {"Name": "Printer Go Brrr", "Tab": "Tab 3", "Optimal": [0, 40, True]},
            34: {"Name": "One Step Ahead", "Tab": "Tab 3"},
            59: {"Name": "Blood Marrow", "Tab": "Tab 4"},
            57: {"Name": "Species Epoch", "Tab": "Tab 4"},
            49: {"Name": "Enhancement Eclipse", "Tab": "Tab 4", "Optimal": [0, 25, False], 'Hardcap': hardcap_enhancement_eclipse},
            53: {"Name": "Eternal WIS", "Tab": "Tab 4"},
            51: {"Name": "Eternal STR", "Tab": "Tab 4"},
            52: {"Name": "Eternal AGI", "Tab": "Tab 4"},
        },
        "Medium": {
            41: {"Name": "Crystal Countdown", "Tab": "Tab 3"},
            28: {"Name": "Cards Galore", "Tab": "Tab 2"},
            29: {"Name": "Rares Everywhere", "Tab": "Tab 2"},
            24: {"Name": "Curse of Mr Looty Booty", "Tab": "Tab 2"},
            56: {"Name": "Voodoo Statufication", "Tab": "Tab 4"},
            78: {"Name": "Extra Bags", "Tab": "Tab 1"},
            39: {"Name": "Colloquial Containers", "Tab": "Tab 3"},
        },
        "Low": {
            279: {"Name": "Robbinghood", "Tab": "Tab 2"},
            37: {"Name": "Skilliest Statue", "Tab": "Tab 3"},
            27: {"Name": "Reroll Pls", "Tab": "Tab 2"},
        },
        "Lowest": {
            42: {"Name": "Left Hand of Learning", "Tab": "Tab 3"},
            40: {"Name": "Maestro Transfusion", "Tab": "Tab 3"},
            38: {"Name": "Bliss N Chips", "Tab": "Tab 3"},
            17: {'Name': 'Supernova Player', "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
}
combat_talentsDict = {
    # Talents here are unique from the skill_talentsDict above
    # Warriors
    "Death Bringer": {
        "High": {
            198: {'Name': 'Graveyard Shift', 'Tab': 'Tab 5'},
            196: {'Name': 'Grimoire', 'Tab': 'Tab 5'},
            199: {'Name': 'Detonation', 'Tab': 'Tab 5'},
            200: {'Name': 'Marauder Style', 'Tab': 'Tab 5'},
            197: {'Name': 'Sentinel Axes', 'Tab': 'Tab 5'},

        },
        "Medium": {
            195: {'Name': 'Wraith Form', 'Tab': 'Tab 5'},
            202: {'Name': "Famine O' Fish", 'Tab': 'Tab 5'},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            110: {"Name": "Apocalypse Zow", "Tab": "Tab 3"},
            141: {"Name": "Charred Skulls", "Tab": "Tab 4"},
            140: {"Name": "Tough Steaks", "Tab": "Tab 4"},
        },
    },
    "Blood Berserker": {
        "High": {},
        "Medium": {
            108: {"Name": "No Pain No Gain", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            110: {"Name": "Apocalypse Zow", "Tab": "Tab 3"},
            141: {"Name": "Charred Skulls", "Tab": "Tab 4"},
            140: {"Name": "Tough Steaks", "Tab": "Tab 4"},
        },
    },
    "Barbarian": {
        "High": {},
        "Medium": {
            108: {"Name": "No Pain No Gain", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            110: {"Name": "Apocalypse Zow", "Tab": "Tab 3"},
        },
    },
    "Divine Knight": {
        "High": {
            168: {"Name": "Orb of Remembrance", "Tab": "Tab 4"},
            120: {"Name": "Shockwave Slash", "Tab": "Tab 3", "Optimal": [0, 30, True]},
            165: {"Name": "Knightly Disciple", "Tab": "Tab 4"},  #Inconsistent levels for extra attacks per Stark. Idk, just max book it and deal with it
            169: {"Name": "Imbued Shockwaves", "Tab": "Tab 4"},
            121: {"Name": "Daggerang", "Tab": "Tab 3", "Optimal": [0, 30, True]},
            166: {"Name": "Mega Mongorang", "Tab": "Tab 4"},
        },
        "Medium": {
            178: {"Name": "King of the Remembered", "Tab": "Tab 4"},
            129: {"Name": "Blocky Bottles", "Tab": "Tab 3"},
            125: {"Name": "Precision Power", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            141: {"Name": "Charred Skulls", "Tab": "Tab 4"},
            170: {"Name": "Gamer Strength", "Tab": "Tab 4"},
        },
    },
    "Squire": {
        "High": {
            120: {"Name": "Shockwave Slash", "Tab": "Tab 3", "Optimal": [0, 30, True]},
            121: {"Name": "Daggerang", "Tab": "Tab 3", "Optimal": [0, 30, True]},},
        "Medium": {
            129: {"Name": "Blocky Bottles", "Tab": "Tab 3"},
            125: {"Name": "Precision Power", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },

    # Mages
    "Bubonic Conjuror": {
        "High": {
            490: {"Name": "Cranium Cooking", "Tab": "Tab 3"},
            481: {"Name": "Auspicious Aura", "Tab": "Tab 3"},
            483: {"Name": "Tenteyecle", "Tab": "Tab 3"},
            529: {"Name": "Raise Dead", "Tab": "Tab 4", 'Hardcap': 200},
            526: {"Name": "Flatulent Spirit", "Tab": "Tab 4"},
            525: {"Name": "Chemical Warfare", "Tab": "Tab 4"},
        },
        "Medium": {
            485: {"Name": "Virile Vials", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            531: {"Name": "Memorial Skulls", "Tab": "Tab 4"},
            530: {"Name": "Wired In Power", "Tab": "Tab 4"},
        },
    },
    "Shaman": {
        "High": {
            490: {"Name": "Cranium Cooking", "Tab": "Tab 3"},
            481: {"Name": "Auspicious Aura", "Tab": "Tab 3"},
            483: {"Name": "Tenteyecle", "Tab": "Tab 3"},
        },
        "Medium": {
            485: {"Name": "Virile Vials", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },
    "Elemental Sorcerer": {
        "High": {
            469: {"Name": "Mana Is Life", "Tab": "Tab 3"},
            496: {"Name": "Lightning Barrage", "Tab": "Tab 4"},
            497: {"Name": "Radiant Chainbolt", "Tab": "Tab 4"},
            467: {"Name": "Tornado", "Tab": "Tab 3"},
            466: {"Name": "Floor Is Lava", "Tab": "Tab 3"},
            498: {"Name": "Dimensional Wormhole", "Tab": "Tab 4"},
        },
        "Medium": {
            508: {"Name": "Wormhole Emperor", "Tab": "Tab 4"},
            474: {"Name": "Fuscia Flasks", "Tab": "Tab 3"},
            470: {"Name": "Paperwork, Great", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            507: {"Name": "Gods Chosen Children", "Tab": "Tab 4"},
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            531: {"Name": "Memorial Skulls", "Tab": "Tab 4"},
            463: {"Name": "Choppin It Up Ez", "Tab": "Tab 2"},
            451: {"Name": "Mini Fireball", "Tab": "Tab 2"},
            500: {"Name": "Believer Strength", "Tab": "Tab 4"},
        },
    },
    "Wizard": {
        "High": {
            469: {"Name": "Mana Is Life", "Tab": "Tab 3"},
            467: {"Name": "Tornado", "Tab": "Tab 3"},
            466: {"Name": "Floor Is Lava", "Tab": "Tab 3"},
        },
        "Medium": {
            474: {"Name": "Fuscia Flasks", "Tab": "Tab 3"},
            470: {"Name": "Paperwork, Great", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            463: {"Name": "Choppin It Up Ez", "Tab": "Tab 2"},
            451: {"Name": "Mini Fireball", "Tab": "Tab 2"},
        },
    },

    # Archers
    "Siege Breaker": {
        "High": {
            318: {"Name": "Pirate Flag", "Tab": "Tab 4"},
            319: {"Name": "Plunder Ye Deceased", "Tab": "Tab 4"},
            316: {"Name": "Suppressing Fire", "Tab": "Tab 4", 'Optimal': [0, 33, True]},
            317: {"Name": "Firebomb", "Tab": "Tab 4", 'Optimal': [0, 50, True]},
            315: {"Name": "Cannonball", "Tab": "Tab 4"},
            285: {"Name": "Homing Arrows", "Tab": "Tab 3", 'Optimal': [0, 15, True]},
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
        },
        "Medium": {
            289: {"Name": "Woah, That Was Fast", "Tab": "Tab 3"},
            286: {"Name": "Magic Shortbow", "Tab": "Tab 3", 'Optimal': [0, 20, True]},
            328: {"Name": "Archlord Of The Pirates", "Tab": "Tab 4"},
            290: {"Name": "Speedna", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            366: {"Name": "Stacked Skulls", "Tab": "Tab 4"},
            320: {"Name": "Crew Rowing Strength", "Tab": "Tab 4"},
        },
    },
    "Bowman": {
        "High": {
            285: {"Name": "Homing Arrows", "Tab": "Tab 3", 'Optimal': [0, 15, True]},
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
        },
        "Medium": {
            289: {"Name": "Woah, That Was Fast", "Tab": "Tab 3"},
            286: {"Name": "Magic Shortbow", "Tab": "Tab 3", 'Optimal': [0, 20, True]},
            290: {"Name": "Speedna", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },
    "Beast Master": {
        "High": {
            362: {"Name": "Whale Wallop", "Tab": "Tab 4", 'Optimal': [0, 17, True]},
            301: {"Name": "Bear Trap", "Tab": "Tab 3", 'Optimal': [0, 30, True]},
            300: {"Name": "Three-Sixty Noscope", "Tab": "Tab 3",},
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
            363: {"Name": "Nacho Party", "Tab": "Tab 4", 'Optimal': [0, 13, True]},
            361: {"Name": "Boar Rush", "Tab": "Tab 4", 'Optimal': [0, 20, True]},
        },
        "Medium": {
            305: {"Name": "Looty Mc Shooty", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            366: {"Name": "Stacked Skulls", "Tab": "Tab 4"},
            365: {"Name": "Animalistic Ferocity", "Tab": "Tab 4"},
        },
    },
    "Hunter": {
        "High": {
            301: {"Name": "Bear Trap", "Tab": "Tab 3", 'Optimal': [0, 30, True]},
            300: {"Name": "Three-Sixty Noscope", "Tab": "Tab 3",},
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
        },
        "Medium": {
            305: {"Name": "Looty Mc Shooty", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },

    # Secret Class
    "Voidwalker": {
        "High": {
            19: {"Name": "Gimme Gimme", "Tab": "Tab 2"},
            26: {"Name": "Cmon Out Crystals", "Tab": "Tab 2"},
            46: {"Name": "Void Radius", "Tab": "Tab 4"},
            45: {"Name": "Void Trial Rerun", "Tab": "Tab 4"},
            47: {"Name": "Bossing Vain", "Tab": "Tab 4"},
            58: {"Name": "Master of the System", "Tab": "Tab 4"},
        },
        "Medium": {
            50: {"Name": "Power Orb", "Tab": "Tab 4"},
            48: {"Name": "Quad Jab", "Tab": "Tab 4"},
            33: {"Name": "Triple Jab", "Tab": "Tab 3"},
            18: {"Name": "Two Punch Man", "Tab": "Tab 2"},
            31: {"Name": "Skillage Damage", "Tab": "Tab 3"},
            20: {"Name": "Lucky Hit", "Tab": "Tab 2"},
            54: {"Name": "Eternal Luk", "Tab": "Tab 4"},
            21: {"Name": "F'LUK'ey Fabrics", "Tab": "Tab 2"},
            38: {"Name": "Bliss N Chips", "Tab": "Tab 3"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            36: {"Name": "Clever Clover Obols", "Tab": "Tab 3"},
        }
    },
    "Maestro": {
        "High": {
            19: {"Name": "Gimme Gimme", "Tab": "Tab 2"},
            26: {"Name": "Cmon Out Crystals", "Tab": "Tab 2"},
        },
        "Medium": {
            33: {"Name": "Triple Jab", "Tab": "Tab 3"},
            18: {"Name": "Two Punch Man", "Tab": "Tab 2"},
            31: {"Name": "Skillage Damage", "Tab": "Tab 3"},
            20: {"Name": "Lucky Hit", "Tab": "Tab 2"},
            21: {"Name": "F'LUK'ey Fabrics", "Tab": "Tab 2"},
            38: {"Name": "Bliss N Chips", "Tab": "Tab 3"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            36: {"Name": "Clever Clover Obols", "Tab": "Tab 3"},
        }
    },
}
unbookable_talents_list = [
    10, 11, 12,  #Tab 1 STR, AGI, WIS
    75, 79,      #Beginner tab1 Happy Dude and Sleepin' on the Job
    23,          #Journeyman Lucky Horseshoe
    86, 87,      #Warrior tab1 Meat Shank and Critikill
    266, 267,    #Archer tab1 Featherweight and I See You
    446, 447,    #Mage tab1 Overclocked Energy and Farsight
]
base_crystal_chance = 0.0005  # 1 in 2000
filter_recipes = {
    "Lucky Lad": ["Luckier Lad"],
    "Beginner Recipe": [
        "Copper Band", "Iron Boots", "Steel Band", "Goo Galoshes", "Fur Shirt", "Dooble Goopi", "Bleached Designer Wode Patch Pants",
        "Serrated Rex Ring", "Fishing Overalls", "Bandito Pantaloon",
        "Blue Tee", "Peanut", "Golden Peanut",  #IDK about including these. They're technically from quests but maybe they count too? :shrug:
    ],
    "Novice Recipe": [
        "Defenders Dignity", "Strung Bludgeon", "Polished Bludgeon", "Googley Eyes", "Dootjat Eye", "Protectors Pride", "Skullfish Pendant",
        "Star Talent Reset Potion"
    ],
    "Apprentice Recipe": [
        "Midnight Stopwatch", "Dawn Stopwatch",
    ],
    "Journeyman Recipe": [
        "Bolstered DNA Splicer", "Double Barreled DNA Splicer", "Ergonomic DNA Splicer",
    ],
    "Adept Recipe": [
        "Magma Core Headdress", "Magma Core Wavemaille", "Magma Core Battleskirt", "Magma Core Lavarunners",
        "Molten Core Knucklers", "Magma Maul", "Sediment Core Grunkler", "Cattle Core Soothsayer Staff",
        "Colossal Food Pouch", "Colossal Matty Pouch", "Coldseeker Bullet",
        "Shiny Bored Beanie", "Divvy Slippers", "Zero Point Stopwatch"
    ],
    "Master Recipe": [
        "Pentastud Slapper", "Elegant Spear", "Pristine Longbow", "Sparky Marble Staff", "Demented Emperor Opal",
        "Crown of the Gods", "Robe of the Gods", "Tatters of the Gods", "Drip of the Gods",
        "Mittens of the Gods", "Massive Godbreaker", "Doublestring Godshooter", "Magnifique Godcaster", "Golden Cake"
    ],
}
filter_never = [
    #Statues
    "Power Statue", "Speed Statue", "Mining Statue", "Feasty Statue", "Health Statue", "Kachow Statue", "Lumberbob Statue",
    "Thicc Skin Statue", "Oceanman Statue", "Ol Reliable Statue", "Exp Book Statue", "Anvil Statue", "Cauldron Statue", "Beholder Statue", "Bullseye Statue",
    "Box Statue", "Twosoul Statue", "EhExPee Statue", "Seesaw Statue",
    "Pecunia Statue", "Mutton Statue", "Egg Statue",
    "Battleaxe Statue", "Spiral Statue", "Boat Statue",
    "Compost Statue", "Stealth Statue", "Essence Statue",
    #Golden Foods
    "Golden Jam", "Golden Kebabs", "Golden Meat Pie", "Golden Nomwich", "Golden Ham", "Golden Bread", "Golden Ribs", "Golden Cheese",
    "Golden Grilled Cheese Nomwich", "Golden Hampter Gummy Candy", "Golden Nigiri", "Golden Dumpling", "Golden Cake", "Gold Food Coupon",
    #Choppin Efficiency talent
    "Grass Leaf",
    #Consumables
    "Gem", "Gem Envelope", "Small Experience Balloon", "Medium Experience Balloon", "Large Experience Balloon",
    "1 HR Time Candy", "2 HR Time Candy", "4 HR Time Candy", "12 HR Time Candy", "24 HR Time Candy", "72 HR Time Candy",
    "Steamy Time Candy", "Spooky Time Candy", "Cosmic Time Candy",
    "Forest Villa Key", "Efaunt's Tomb Key", "Chizoar's Cavern Key", "Troll's Enclave Key", "Kruk's Volcano Key",
    "Silver Pen", "Pet Egg", "Cooking Ladle",
    "Candy Canes", "Aqua Pearl", "Mistleberries",
    "Dungeon Credits", "Dungeon Credits Flurbo Edition",
    #W1 Rares
    "Golden Plop", "Woodular Circle", "Red Frisbee",
    #W2 Rares
    "Glass Shard", "Nuget Cake", "Ghost", "Midnight Cookie",
    #W3 Rares
    "Ice Age 3", "Black Lense",
    #W4 Rares
    "Lost Batteries", "Pearler Shell",
    #W5 Rares
    "Royal Suggma Urn", "Hampter", "OJ Juice", "Magma Obol of Big Time Domeo",
    #W6 Rares
    "Stacked Rice Cake", "Dark Lantern",
    #Event Lootboxes
    "Event Point",
    "Summer Cooler", "Beach Oyster", "Golden Oyster",
    "Choco Box", "Lovey Dovey Letter",
    "Egg Capsule", "Gummy Bunny", "Goldegg Capsule",
    "Phone Box", "Spring Baggie", "Anniversary Box", "Falloween Treat", "2021 Giftmas Box",
]

def lavaFunc(funcType: str, level: int, x1: int | float, x2: int | float, roundResult=False):
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
        case 'pow':
            result = pow(x1, level)
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

def ValueToMulti(value: float, min_value=1.0):
    return max(min_value, 1 + (value / 100))


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
stampTypes = ["Combat", "Skill", "Misc"]
unavailableStampsList = [
    'Shiny Crab Stamp', 'Gear Stamp', 'SpoOoky Stamp', 'Prayday Stamp',  #Skill
    'Talent I Stamp', 'Talent V Stamp',  #Misc
]  # Last verified as of v2.10
stamp_maxes = {
    #Combat
    "Sword Stamp": 205,
    "Target Stamp": 175,
    "Fist Stamp": 58,
    "Book Stamp": 72,
    "Bullseye Stamp": 110,
    "Buckler Stamp": 182,
    "Avast Yar Stamp": 120,
    "Gilded Axe Stamp": 162,
    "Maxo Slappo Stamp": 140,
    "Dementia Sword Stamp": 200,
    "Void Axe Stamp": 255,
    "Heart Stamp": 170,
    "Shield Stamp": 150,
    "Battleaxe Stamp": 152,
    "Manamoar Stamp": 99,
    "Feather Stamp": 165,
    "Hermes Stamp": 75,
    "Steve Sword": 320,
    "Diamond Axe Stamp": 230,
    "Sashe Sidestamp": 133,
    "Golden Sixes Stamp": 210,
    "Captalist Stats Stamp": 160,
    "Mana Stamp": 165,
    "Longsword Stamp": 136,
    "Agile Stamp": 36,
    "Clover Stamp": 82,
    "Polearm Stamp": 246,
    "Sukka Foo": 220,
    "Blover Stamp": 104,
    "Tripleshot Stamp": 300,
    "Intellectostampo": 168,
    "Stat Wallstreet Stamp": 78,
    "Tomahawk Stamp": 136,
    "Kapow Stamp": 99,
    "Vitality Stamp": 132,
    "Scimitar Stamp": 108,
    "Violence Stamp": 87,
    "Arcane Stamp": 78,
    "Stat Graph Stamp": 95,
    "Blackheart Stamp": 450,
    "Conjocharmo Stamp": 210,
    "Void Sword Stamp": 180,
    #Skill
    "Pickaxe Stamp": 455,
    "Twin Ores Stamp": 120,
    "Smart Dirt Stamp": 165,
    "Alch Go Brrr Stamp": 124,
    "Fishing Rod Stamp": 150,
    "Bag o Heads Stamp": 224,
    "Hidey Box Stamp": 300,
    "Cooked Meal Stamp": 480,
    "Egg Stamp": 480,
    "Divine Stamp": 168,
    "Sneaky Peeky Stamp": 144,
    "Triad Essence Stamp": 136,
    "Hatchet Stamp": 465,
    "Choppin' Bag Stamp": 330,
    "Cool Diggy Tool Stamp": 340,
    "Brainstew Stamps": 155,
    "Fishhead Stamp": 125,
    "Holy Mackerel Stamp": 155,
    "Purp Froge Stamp": 130,
    "Stample Stamp": 124,
    "Flowin Stamp": 82,
    "Spice Stamp": 510,
    "Lab Tube Stamp": 340,
    "Multitool Stamp": 230,
    "Jade Mint Stamp": 150,
    "Dark Triad Essence Stamp": 128,
    "Anvil Zoomer Stamp": 155,
    "Duplogs Stamp": 120,
    "High IQ Lumber Stamp": 165,
    "Drippy Drop Stamp": 160,
    "Catch Net Stamp": 150,
    "Bugsack Stamp": 224,
    "Spikemouth Stamp": 78,
    "Saw Stamp": 90,
    "Ladle Stamp": 320,
    "Sailboat Stamp": 160,
    "Skelefish Stamp": 42,
    "Summoner Stone Stamp": 128,
    "Lil' Mining Baggy Stamp": 310,
    "Matty Bag Stamp": 410,
    "Swag Swingy Tool Stamp": 410,
    "Droplots Stamp": 84,
    "Fly Intel Stamp": 120,
    "Buzz Buzz Stamp": 155,
    "Amplestample Stamp": 68,
    "Banked Pts Stamp": 282,
    "Nest Eggs Stamp": 320,
    "Gamejoy Stamp": 115,
    "Crop Evo Stamp": 85,
    "White Essence Stamp": 136,
    #Misc
    "Questin Stamp": 330,
    "Gold Ball Stamp": 280,
    "Card Stamp": 330,
    "DNA Stamp": 48,
    "Mason Jar Stamp": 160,
    "Potion Stamp": 105,
    "Forge Stamp": 240,
    "Talent II Stamp": 50,
    "Talent S Stamp": 72,
    "Refinery Stamp": 90,
    "Crystallin": 270,
    "Golden Apple Stamp": 136,
    "Vendor Stamp": 150,
    "Talent III Stamp": 66,
    "Multikill Stamp": 112,
    "Atomic Stamp": 144,
    "Arcade Ball Stamp": 310,
    "Ball Timer Stamp": 90,
    "Sigil Stamp": 324,
    "Talent IV Stamp": 56,
    "Biblio Stamp": 66,
}
stampsDict = {
    "Combat": {
        0: {'Name': "Sword Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'spore-cap'},
        1: {'Name': "Heart Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'oak-logs'},
        2: {'Name': "Mana Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'copper-ore'},
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
        4: {'Name': "Twin Ores Stamp", 'funcType': 'decay', 'x1': 15, 'x2': 40, 'Material': 'thief-hood'},
        5: {'Name': "Choppin' Bag Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'carrot-cube'},
        6: {'Name': "Duplogs Stamp", 'funcType': 'decay', 'x1': 15, 'x2': 40, 'Material': 'militia-helm'},
        7: {'Name': "Matty Bag Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'cramped-material-pouch'},
        8: {'Name': "Smart Dirt Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'plank'},
        9: {'Name': "Cool Diggy Tool Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'iron-hatchet'},
        10: {'Name': "High IQ Lumber Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'bullfrog-horn'},
        11: {'Name': "Swag Swingy Tool Stamp", 'funcType': 'add', 'x1': 2, 'x2': 0, 'Material': 'copper-pickaxe'},
        12: {'Name': "Alch Go Brrr Stamp", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'forest-fibres'},
        13: {'Name': "Brainstew Stamps", 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'gold-ore'},
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
        4: {'Name': "Gold Ball Stamp", 'funcType': 'decay', 'x1': 40, 'x2': 100, 'Material': 'goldfish'},
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
capacity_stamps = ["Mason Jar Stamp", "Lil' Mining Baggy Stamp", "Choppin' Bag Stamp", "Matty Bag Stamp", "Bag o Heads Stamp", "Bugsack Stamp"]
stamps_progressionTiers[max(stamps_progressionTiers)-2]['Stamps']['Specific'] = {stampName: stamp_maxes[stampName] for stampName in capacity_stamps}
tiered_stamps = set()
for tier in stamps_progressionTiers:
    for requiredStamp in stamps_progressionTiers[tier].get('Stamps', {}).get('Specific', []):
        if requiredStamp not in capacity_stamps and requiredStamp != 'Crop Evo Stamp':
            tiered_stamps.add(requiredStamp)
ordered_tiers_stamps = []
remaining_stamps = []
for stampType in stampsDict:
    for stamp in stampsDict[stampType].values():
        if stamp['Name'] not in unavailableStampsList and stamp['Name'] not in capacity_stamps:
            if stamp['Name'] in tiered_stamps:
                ordered_tiers_stamps.append(stamp['Name'])
            else:
                remaining_stamps.append(stamp['Name'])
stamps_progressionTiers[max(stamps_progressionTiers)-1]['Stamps']['Specific'] = {stamp: stamp_maxes[stamp] for stamp in ordered_tiers_stamps}
stamps_progressionTiers[max(stamps_progressionTiers)]['Stamps']['Specific'] = {stamp: stamp_maxes[stamp] for stamp in remaining_stamps}

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
arbitrary_forge_capacity_goal = 150001
arbitrary_forge_capacity_note = f"Goal of {arbitrary_forge_capacity_goal:,} is the last Godshard Bar we can reach guaranteed as of v2.12"
statuesDict = {
    0:  {"Name": "Power Statue", "ItemName": "EquipmentStatues1", "Effect": "Base Damage", "BaseValue": 3, "Farmer": "Crystals with DK at Beans", "Target": "bored-bean"},
    1:  {"Name": "Speed Statue", "ItemName": "EquipmentStatues2", "Effect": "% Move Speed", "BaseValue": 0.1, "Farmer": "W1-W3 Crystals with DK", "Target": "w1-w3-crystals"},
    2:  {"Name": "Mining Statue", "ItemName": "EquipmentStatues3", "Effect": "Mining Power", "BaseValue": 0.3, "Farmer": "Crystals with DK at Beans", "Target": "bored-bean"},
    3:  {"Name": "Feasty Statue", "ItemName": "EquipmentStatues4", "Effect": "% Food Effect", "BaseValue": 1, "Farmer": "W1-W3 Crystals with DK", "Target": "w1-w3-crystals"},
    4:  {"Name": "Health Statue", "ItemName": "EquipmentStatues5", "Effect": "Base Health", "BaseValue": 3, "Farmer": "Crystals with DK at Beans", "Target": "bored-bean"},
    5:  {"Name": "Kachow Statue", "ItemName": "EquipmentStatues6", "Effect": "% Crit Damage", "BaseValue": 0.4, "Farmer": "Monolith Quest on All characters", "Target": "monolith"},
    6:  {"Name": "Lumberbob Statue", "ItemName": "EquipmentStatues7", "Effect": "Choppin Power", "BaseValue": 0.3, "Farmer": "Crystals with DK at Beans", "Target": "bored-bean"},
    7:  {"Name": "Thicc Skin Statue", "ItemName": "EquipmentStatues8", "Effect": "Base Defence", "BaseValue": 1, "Farmer": "Crystals with DK at Sandy Pot or Tyson", "Target": "crystal-crabal"},
    8:  {"Name": "Oceanman Statue", "ItemName": "EquipmentStatues9", "Effect": "Fishing Power", "BaseValue": 0.3, "Farmer": "AFK or Candy with Vman at W2 Bugs", "Target": "fly-nest"},
    9:  {"Name": "Ol Reliable Statue", "ItemName": "EquipmentStatues10", "Effect": "Catchin Power", "BaseValue": 0.3, "Farmer": "Crystals with DK at Sandy Pot or Tyson", "Target": "crystal-crabal"},
    10: {"Name": "Exp Book Statue", "ItemName": "EquipmentStatues11", "Effect": "% Class EXP", "BaseValue": 0.1, "Farmer": "Crystals with DK at Sandy Pot or Tyson", "Target": "crystal-crabal"},
    11: {"Name": "Anvil Statue", "ItemName": "EquipmentStatues12", "Effect": "% Product SPD", "BaseValue": 0.5, "Farmer": "Crystals with DK at Sandy Pot or Tyson", "Target": "crystal-crabal"},
    12: {"Name": "Cauldron Statue", "ItemName": "EquipmentStatues13", "Effect": "% Alchemy EXP", "BaseValue": 0.5, "Farmer": "Crystals with DK at Sandy Pot or Tyson", "Target": "crystal-crabal"},
    13: {"Name": "Beholder Statue", "ItemName": "EquipmentStatues14", "Effect": "% Crit Chance", "BaseValue": 0.2, "Farmer": "Crystals with DK at Beans", "Target": "bored-bean"},
    14: {"Name": "Bullseye Statue", "ItemName": "EquipmentStatues15", "Effect": "% Accuracy", "BaseValue": 0.8, "Farmer": "Active ES at Wood Mushroom or Candy at Nutto", "Target": "wood-mushroom"},
    15: {"Name": "Box Statue", "ItemName": "EquipmentStatues16", "Effect": "Trappin Power", "BaseValue": 0.3, "Farmer": "Candy or Active ES at Penguins", "Target": "penguin"},
    16: {"Name": "Twosoul Statue", "ItemName": "EquipmentStatues17", "Effect": "Worship Power", "BaseValue": 0.3, "Farmer": "Candy or Active ES at Quenchies", "Target": "quenchie"},
    17: {"Name": "EhExPee Statue", "ItemName": "EquipmentStatues18", "Effect": "% Skill EXP", "BaseValue": 0.1, "Farmer": "Crystals with DK at Bloodbones", "Target": "bloodbone"},
    18: {"Name": "Seesaw Statue", "ItemName": "EquipmentStatues19", "Effect": "% Cons EXP", "BaseValue": 0.5, "Farmer": "Candy or Active ES at Cryosnakes", "Target": "cryosnake"},
    19: {"Name": "Pecunia Statue", "ItemName": "EquipmentStatues20", "Effect": "% Coins", "BaseValue": 1, "Farmer": "Crystals with DK at Clammies", "Target": "clammie"},
    20: {"Name": "Mutton Statue", "ItemName": "EquipmentStatues21", "Effect": "% Cooking EXP", "BaseValue": 0.3, "Farmer": "Crystals with DK at Clammies", "Target": "clammie"},
    21: {"Name": "Egg Statue", "ItemName": "EquipmentStatues22", "Effect": "% Breeding EXP", "BaseValue": 0.4, "Farmer": "Crystals with DK at Clammies", "Target": "clammie"},
    22: {"Name": "Battleaxe Statue", "ItemName": "EquipmentStatues23", "Effect": "% Damage", "BaseValue": 0.2, "Farmer": "Crystals with DK at Tremor Wurms", "Target": "tremor-wurm"},
    23: {"Name": "Spiral Statue", "ItemName": "EquipmentStatues24", "Effect": "% Divinity EXP", "BaseValue": 1, "Farmer": "Crystals with DK at Tremor Wurms", "Target": "tremor-wurm"},
    24: {"Name": "Boat Statue", "ItemName": "EquipmentStatues25", "Effect": "% Sailing SPD", "BaseValue": 0.5, "Farmer": "Crystals with DK at Tremor Wurms", "Target": "tremor-wurm"},
    25: {"Name": "Compost Statue", "ItemName": "EquipmentStatues26", "Effect": "% Farming EXP", "BaseValue": 0.4, "Farmer": "Crystals with DK at Minichiefs", "Target": "minichief-spirit"},
    26: {"Name": "Stealth Statue", "ItemName": "EquipmentStatues27", "Effect": "% Stealth", "BaseValue": 0.3, "Farmer": "Crystals with DK at Minichiefs", "Target": "minichief-spirit"},
    27: {"Name": "Essence Statue", "ItemName": "EquipmentStatues28", "Effect": "% White ESS", "BaseValue": 0.6, "Farmer": "Crystals with DK at Minichiefs", "Target": "minichief-spirit"},
    28: {"Name": "Dragon Warrior Statue", "ItemName": "EquipmentStatues29", "Effect": "% Statues Bonus", "BaseValue": 0, "Farmer": "AFK {{Cavern 9|#villagers}}", "Target": "gloomie-mushroom"}
}
statueTypeList = ["Normal", "Gold", "Onyx"]
statueCount = len(statuesDict.keys())
event_points_shop_dict = {
    'Golden Tome': {'Cost': 25, 'Code': '_', 'Description': 'Adds a new DMG Multi bonus type to the Tome in World 4', 'Image': 'event-shop-0'},
    'Stamp Stack': {'Cost': 30, 'Code': 'a', 'Description': 'Get +3 Stamp LVs every day for a random Stamp', 'Image': 'event-shop-1'},
    'Bubble Broth': {'Cost': 15, 'Code': 'b', 'Description': 'Get +5 LVs for a random Alchemy Bubble every day', 'Image': 'event-shop-2'},
    'Equinox Enhancement': {'Cost': 15, 'Code': 'c', 'Description': 'Get 1.5x faster Bar fill Rate in Equinox Valley in World 3', 'Image': 'event-shop-3'},
    'Supreme Wiring': {'Cost': 45, 'Code': 'd', 'Description': "+2% Printer Output per day, taking new sample resets this", 'Image': 'event-shop-4'},
    'Sleepy Joe Armstrong': {'Cost': 25, 'Code': 'e', 'Description': "+20% AFK Gains for all things IdleOn related", 'Image': 'event-shop-5'},
    'Village Encouragement': {'Cost': 30, 'Code': 'f','Description': "All Villagers in World 5 Camp get 1.25x EXP Gain", 'Image': 'event-shop-6'},
    'Gilded Vote Button': {'Cost': 35, 'Code': 'g', 'Description': "Get +17% higher Ballot Bonus Multi from Voting", 'Image': 'event-shop-7'},
    'Extra Page': {'Cost': 20, 'Code': 'h', 'Description': "Get +1 more Filter page", 'Image': 'event-shop-8'},
    'Coin Stacking': {'Cost': 15, 'Code': 'i', 'Description': 'Get 1.5x multiplier to all coins', 'Image': 'event-shop-9'},
    'More Storage': {'Cost': 10, 'Code': 'j', 'Description': 'Get +12 storage slots', 'Image': 'event-shop-10'}
}  #Found near end of NinjaInfo function in the source code

###WORLD 2 CONSTS###
max_IndexOfVials = 75  # Last verified as of v2.10
max_VialLevel = 13  # Last verified as of 2.12
vial_costs = [1, 100, 1000, 2500, 10e3, 50e3, 100e3, 500e3, 1e6, 5e6, 25e6, 100e6, 1e9]
max_IndexOfImplementedBubbles = 29  # Last verified as of v2.25
max_IndexOfSigils = 3  # Last verified as of v2.25
min_NBLB = 2
max_NBLB = 1500
nblb_max_index = 24
nblb_skippable = [
    'Reely Smart', 'Bappity Boopity', 'Bite But Not Chew',  #Orange
    'Lil Big Damage', 'Anvilnomics', 'Cheap Shot',  #Green
    'Noodubble',  #Purple
    'Petting The Rift',  #Yellow
]
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
    "Odd Litearture":   {"Index": 4,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [5, 200, 70000]},
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
    "VIP Parchment":    {"Index": 30, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [6300, 42000, 520000]},
    "Dream Catcher":    {"Index": 32, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [7000, 50000, 560000]},
    "Duster Studs":     {"Index": 34, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [8000, 60000, 600000]},
    "Garlic Glove":     {"Index": 36, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [9000, 70000, 650000]},
    "Lab Tesstube":     {"Index": 38, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [12000, 80000, 700000]},
    "Peculiar Vial":    {"Index": 40, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [17000, 120000, 750000]},
    "Loot Pile":        {"Index": 42, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [23000, 160000, 900000]},
    "Div Spiral":       {"Index": 44, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [26000, 200000, 1200000]},
    "Cool Coin":        {"Index": 46, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [30000, 250000, 2000000]},
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
        28: {'Name': 'Ninja Looter', 'Material': 'Blue-Essence', 'x1': 0.3, 'x2': 60, 'funcType': 'decayMulti'},
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
atrisk_advancedBubbles = [
    "Warriors Rule",
    "Big Meaty Claws",
    "Call Me Bob",
    "Multorange",
    "Bite But Not Chew",
    "Archer Or Bust",
    "Quick Slap",
    "Sanic Tools",
    "Bow Jack",
    "Cuz I Catch Em All",
    "Mage Is Best",
    "Brewstachio",
    "Smart Boi Talent",
    "Purple Bargain",
    "Startue Exp",
    "Level Up Gift",
    "Cogs For Hands",
    "Sample It",
]
atrisk_lithiumBubbles = [
    "Penny Of Strength",
    "Fly In Mind",
    'Afk Expexp',
    'Slabo Critterbug',
    'Nickel Of Wisdom',
    'Severapurple',
    'Hyperswift',
    'Matrix Evolved',
    'Slabe Logsoul',
    'Bit By Bit',
    'Gifts Abound',
]
atrisk_lithiumAdvancedBubbles = []

arcadeBonuses = {
    0:  {"Stat": "Base Damage", "x1": 1, "x2": 0, "funcType": "add", "displayType": ""},
    1:  {"Stat": "Base Defence", "x1": 0.2, "x2": 0, "funcType": "add", "displayType": ""},
    2:  {"Stat": "Total Accuracy", "x1": 60, "x2": 100, "funcType": "decay", "displayType": ""},
    3:  {"Stat": "Mining EXP gain", "x1": 60, "x2": 100, "funcType": "decay", "displayType": "%"},
    4:  {"Stat": "Fishing EXP gain", "x1": 60, "x2": 100, "funcType": "decay", "displayType": "%"},
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
    38: {"Stat": "Villager XP multi", "x1": 40, "x2": 100, "funcType": "decay", "displayType": "%"},
    39: {"Stat": "Gold Ball gain", "x1": 1, "x2": 0, "funcType": "add", "displayType": "%"},
}
arcade_max_level = 100
#poBoxDict last taken from code in 2.09: #PostOffUpgradeInfo = function ()
#Translate using the Post Office tab in AR spreadsheet
post_office_tabs = ["Bob's Boxes", "Charlie's Crates"]
poBoxDict = {
    0: {
        'Name': 'Civil War Memory Box', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 1, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Base Damage',
        '2_funcType': 'decay', '2_x1': 13, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Fight AFK Gains', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 10, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Critical Chance', '3_minCount': 100,
    },
    1: {
        'Name': 'Locally Sourced Organs', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'intervalAdd', '1_x1': 1, '1_x2': 2, '1_pre': '', '1_post': '', '1_stat': 'Base Max HP',
        '2_funcType': 'add', '2_x1': 0.1, '2_x2': 0, '2_pre': '', '2_post': '%', '2_stat': 'Max HP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Faster Respawns', '3_minCount': 100,
    },
    2: {
        'Name': 'Magician Starterpack', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'intervalAdd', '1_x1': 1, '1_x2': 3, '1_pre': '', '1_post': '', '1_stat': 'Base Max MP',
        '2_funcType': 'add', '2_x1': 0.1, '2_x2': 0, '2_pre': '', '2_post': '%', '2_stat': 'Max MP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 17, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Faster Cooldowns', '3_minCount': 100,
    },
    3: {
        'Name': 'Box of Unwanted Stats', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 0.25, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Base Accuracy',
        '2_funcType': 'add', '2_x1': 0.3, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'Base Defence', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 29, '3_x2': 170, '3_pre': '', '3_post': '%', '3_stat': 'Monster EXP', '3_minCount': 100,
    },
    4: {
        'Name': 'Dwarven Supplies', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Mining Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Mining AFK Gain', '3_minCount': 100,
    },
    5: {
        'Name': 'Blacksmith Box', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Smithing EXP',
        '2_funcType': 'decay', '2_x1': 75, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Production Speed', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 150, '3_pre': '', '3_post': '%', '3_stat': 'to Craft +1 Slot', '3_minCount': 100,
    },
    6: {
        'Name': 'Taped Up Timber', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Choppin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Choppin AFK Gain', '3_minCount': 100,
    },
    7: {
        'Name': 'Carepack From Mum', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 23, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Not Consume Food',
        '2_funcType': 'decay', '2_x1': 30, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Health Food Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Boost Food Effect', '3_minCount': 100,
    },
    8: {
        'Name': 'Sealed Fishheads', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Fishin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Fishin AFK Gain', '3_minCount': 100,
    },
    9: {
        'Name': 'Potion Package', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 70, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Brewing Speed',
        '2_funcType': 'decay', '2_x1': 60, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Alchemy EXP', '2_minCount': 25,
        '3_funcType': 'add', '3_x1': 0.1, '3_x2': 0, '3_pre': '', '3_post': '', '3_stat': 'Cranium Cook Time', '3_minCount': 100,
    },
    10: {
        'Name': 'Bug Hunting Supplies', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Catchin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Catchin AFK Gain', '3_minCount': 100,
    },
    11: {
        'Name': 'Non Predatory Loot Box', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Drop Rarity',
        '2_funcType': 'add', '2_x1': 0.25, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'LUK', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 65, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Crystal Mob Spawn', '3_minCount': 100,
    },
    12: {
        'Name': 'Deaths Storage Unit', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 22, '1_x2': 200, '1_pre': '', '1_post': '', '1_stat': 'Weapon Power',
        '2_funcType': 'decay', '2_x1': 15, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Basic Atk Speed', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 100,
    },
    13: {
        'Name': 'Utilitarian Capsule', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 5, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Printer Sample Size',
        '2_funcType': 'decay', '2_x1': 15, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Multikill per Tier', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 39, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Cash from Mobs', '3_minCount': 100,
    },
    14: {
        'Name': 'Lazzzy Lootcrate', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 30, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': '2X AFK XP chance',
        '2_funcType': 'decay', '2_x1': 35, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'AFK exp if 36hr+', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 35, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'AFK Cash if 36hr+', '3_minCount': 100,
    },
    15: {
        'Name': 'Science Spare Parts', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 4, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Lab Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Lab EXP gain', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '', '3_stat': 'Base LUK', '3_minCount': 100,
    },
    16: {
        'Name': 'Trapping Lockbox', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Trapping Efficiency',
        '2_funcType': 'decay', '2_x1': 50, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Trapping EXP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 45, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Critters Trapped', '3_minCount': 100,
    },
    17: {
        'Name': 'Construction Container', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 0.25, '1_x2': 0, '1_pre': '', '1_post': '%', '1_stat': 'Base Build Rate',
        '2_funcType': 'decay', '2_x1': 75, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Shrine Charge Rate', '2_minCount': 25,
        '3_funcType': 'add', '3_x1': 0.5, '3_x2': 0, '3_pre': '', '3_post': '%', '3_stat': 'Construction EXP', '3_minCount': 100,
    },
    18: {
        'Name': 'Crate of the Creator', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Worship Efficiency',
        '2_funcType': 'decay', '2_x1': 200, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Max Charge', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 90, '3_x2': 200, '3_pre': '', '3_post': '', '3_stat': 'Starting Worship Pts', '3_minCount': 100,
    },
    19: {
        'Name': 'Chefs Essentials', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 4, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Cooking Efficiency',
        '2_funcType': 'decay', '2_x1': 60, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Cooking EXP gain', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 88, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'for 2x Ladle Drop', '3_minCount': 100,
    },
    20: {
        'Name': 'Myriad Crate', 'Tab': post_office_tabs[1], 'Max Level': 100000,
        '1_funcType': 'decay', '1_x1': 400, '1_x2': 20000, '1_pre': '', '1_post': '', '1_stat': 'Base All Stat',
        '2_funcType': 'decay', '2_x1': 1000, '2_x2': 20000, '2_pre': '', '2_post': '', '2_stat': 'Base All Efficiency', '2_minCount': 100,
        '3_funcType': 'decay', '3_x1': 100, '3_x2': 20000, '3_pre': '', '3_post': '%', '3_stat': 'All Skills exp', '3_minCount': 300,
    },
    21: {
        'Name': "Scurvy C'arr'ate", 'Tab': post_office_tabs[1], 'Max Level': 800,
        '1_funcType': 'decay', '1_x1': 8, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'afk counts for sailing',
        '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'AGI', '2_minCount': 50,
        '3_funcType': 'decay', '3_x1': 25, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 200,
    },
    22: {
        'Name': 'Box of Gosh', 'Tab': post_office_tabs[1], 'Max Level': 800,
        '1_funcType': 'decay', '1_x1': 75, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'Divinity EXP',
        '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'WIS', '2_minCount': 50,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Divinity Gain', '3_minCount': 200,
    },
    23: {
        'Name': 'Gaming Lootcrate', 'Tab': post_office_tabs[1], 'Max Level': 800,
        '1_funcType': 'decay', '1_x1': 14, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'afk counts for gaming',
        '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'STR', '2_minCount': 50,
        '3_funcType': 'decay', '3_x1': 25, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 200,
    },
}
max_poBox_before_myriad = sum([v['Max Level'] for v in poBoxDict.values() if v['Name'] != 'Myriad Crate'])
max_poBox_after_myriad = max_poBox_before_myriad + poBoxDict[20]['Max Level']
ballotDict = {
    0:  {'BaseValue': 25, 'Description': "All your characters deal }x more damage to enemies", 'Image': "ballot-1"},
    1:  {'BaseValue': 25, 'Description': "All your characters deal }x more damage to enemies", 'Image': "ballot-1"},
    2:  {'BaseValue': 15, 'Description': "Increases STR AGI WIS and LUK for all characters by {%", 'Image': "ballot-2"},
    3:  {'BaseValue': 30, 'Description': "Increases Defence and Accuracy by +{% for all characters", 'Image': "ballot-3"},
    4:  {'BaseValue': 30, 'Description': "Logging in each day gives +{ more GP to your guild than you normally do", 'Image': "ballot-4"},
    5:  {'BaseValue': 20, 'Description': "}x Kill per Kill, making monster kills worth more for portals and deathnote", 'Image': "ballot-5"},
    6:  {'BaseValue': 15, 'Description': "{% AFK gain for both fighting and skills for all characters", 'Image': "ballot-6"},
    7:  {'BaseValue': 42, 'Description': "Boosts all Mining EXP gain and Mining Efficiency by +{%", 'Image': "ballot-7"},
    8:  {'BaseValue': 50, 'Description': "Boosts all Fishing EXP gain and Fishing Efficiency by +{%", 'Image': "ballot-8"},
    9:  {'BaseValue': 38, 'Description': "Boosts all Chopping' EXP gain and Choppin' Efficiency by +{%", 'Image': "ballot-9"},
    10: {'BaseValue': 46, 'Description': "Boosts all Catching EXP gain and Catching Efficiency by +{%", 'Image': "ballot-10"},
    11: {'BaseValue': 20, 'Description': "Increases the amount of resources produced by the 3D printer by }x", 'Image': "ballot-11"},
    12: {'BaseValue': 25, 'Description': "Boosts liquid generation rate for all Alchemy liquids by +{%", 'Image': "ballot-12"},
    13: {'BaseValue': 63, 'Description': "Boosts all Cooking EXP gain and Cooking speed by +{%", 'Image': "ballot-13"},
    14: {'BaseValue': 50, 'Description': "Boosts Dungeon Credit and Dungeon Flurbo gain by }x", 'Image': "ballot-14"},
    15: {'BaseValue': 60, 'Description': "All your characters gain +{% more class EXP from monsters", 'Image': "ballot-15"},
    16: {'BaseValue': 50, 'Description': "Speeds up Egg incubation and Breeding EXP gain by +{%", 'Image': "ballot-16"},
    17: {'BaseValue': 80, 'Description': "Boosts Sigil EXP gain by }x, still requires Sigils active in Lab", 'Image': "ballot-17"},
    18: {'BaseValue': 40, 'Description': "Boosts Construction Build Rate and Construction EXP gain by +{%", 'Image': "ballot-18"},
    19: {'BaseValue': 53, 'Description': "Boosts Shrine EXP gain by a staggering }x", 'Image': "ballot-19"},
    20: {'BaseValue': 31, 'Description': "Boosts Artifact Find Chance in Sailing by }x", 'Image': "ballot-20"},
    21: {'BaseValue': 80, 'Description': "Boosts New Species chance when using DNA in gaming by }x", 'Image': "ballot-21"},
    22: {'BaseValue': 75, 'Description': "Find +{% more gold Nuggets when digging with the shovel in gaming", 'Image': "ballot-22"},
    23: {'BaseValue': 60, 'Description': "Boosts Divinity PTS gain by }x and Divinity EXP gain by +{%", 'Image': "ballot-23"},
    24: {'BaseValue': 50, 'Description': "Boosts Sailing Captain EXP gain and Sailing Speed by }x", 'Image': "ballot-24"},
    25: {'BaseValue': 65, 'Description': "Boosts Sneaking Stealth by }x and EXP gain by +{% for all your Ninja Twins", 'Image': "ballot-25"},
    26: {'BaseValue': 30, 'Description': "Boosts bonuses from all Golden food by +{%", 'Image': "ballot-26"},
    27: {'BaseValue': 38, 'Description': "Increases Drop Rate for all your characters by +{%", 'Image': "ballot-27"},
    28: {'BaseValue': 40, 'Description': "Boosts Summoning EXP gain by +40% and all Essence gained by }x", 'Image': "ballot-28"},
    29: {'BaseValue': 40, 'Description': "Boosts Crop Value, and Farming EXP gain, AND Next Crop Chance by +{%", 'Image': "ballot-29"},
    30: {'BaseValue': 45, 'Description': "Increases Trapping EXP gain and Worship EXP gain by +{%", 'Image': "ballot-30"},
    31: {'BaseValue': 90, 'Description': "Increases Lab EXP gain by +{%", 'Image': "ballot-31"},
    32: {'BaseValue': 40, 'Description': "Boosts Equinox Bar Fill rate by }x", 'Image': "ballot-32"},
    33: {'BaseValue': 50, 'Description': "Boosts Refinery Cycle Speed by +{%", 'Image': "ballot-33"},
    34: {'BaseValue': 52, 'Description': "Increases cash earned from monsters by +{%", 'Image': "ballot-34"},
}
fishingToolkitDict = {
    "Lures": [
        'Fly', 'Wormie Weight', 'Iron Hook', 'Basic Bobber', 'Dualhook Prongs', 'Pound of Steel', 'Pound of Feathers',
        'Massless Unit for Physics Questions', 'Literal Elephant', 'Valve Patented Circle Thingies', 'Dynamite', 'Not Dynamite',
        'Triple Threat', 'Crash Box', 'Fat Albert',
    ],
    "Lines": [
        'Fishing Twine', 'Copper Twine', 'Silver Twine', 'Gold Twine', 'Platinum Twine', 'Leafy Vines', 'Fun Flags', 'Electrical Wiring',
        'Wiener Links', 'Zeus Gon Fishin', 'Needledrop', 'Scripticus Spoons', 'Its a Boy Celebration', 'Its a Girl Celebration', 'Its Alright Celebration'
    ],
}
obolsDict = {
    #Drop Rate
    "ObolBronzePop":    {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolBronzePop")},
    "ObolSilverPop":    {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolSilverPop")},
    "ObolHyper0":       {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolHyper0")},
    "ObolSilverLuck":   {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolSilverLuck")},
    "ObolGoldLuck":     {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolGoldLuck")},
    "ObolKnight":       {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolKnight")},
    "ObolHyperB0":       {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolHyper0")},
    "ObolPlatinumLuck": {"Shape": "Hexagon", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolPlatinumLuck")},
    "ObolLava":         {"Shape": "Hexagon", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolLava")},
    "ObolPinkLuck":     {"Shape": "Sparkle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolPinkLuck")},
}
ignorable_obols_list = [
    'Blank', 'LockedInvSpace', 'ObolLocked1', 'ObolLocked2', 'ObolLocked3', 'ObolLocked4',
]
islands_dict = {
    'Trash Island':     {'Code': '_', 'Description': 'Trade garbage that washs up each day for items',},
    'Rando Island':     {'Code': 'a', 'Description': 'Guaranteed Random Event once a week',},
    'Crystal Island':   {'Code': 'b', 'Description': 'Fight daily giant crystal mobs that drop candy',},
    'Seasalt Island':   {'Code': 'c', 'Description': 'Catch legendary fish for crafting World 6 equips',},
    'Shimmer Island':   {'Code': 'd', 'Description': 'Do Weekly Challenges for Shimmer Upgrades',},
    'Fractal Island':   {'Code': 'e', 'Description': 'Dump your time candy here for... nothing...?',},
}
islands_trash_shop_costs = {
    'Skelefish Stamp': 20,
    'Amplestample Stamp': 40,
    'Golden Sixes Stamp': 80,
    'Stat Wallstreet Stamp': 300,
    'Unlock New Bribe Set': 135,
    'Filthy Damage Special Talent Book': 450,
    'Trash Tuna Nametag': 1500
}
islands_fractal_rewards_dict = {
    24: {'Reward': '1 in 100000 chance for Master of Nothing Trophy per hour of Nothing AFK', 'Image': 'master-of-nothing'},
    200: {'Reward': '1.25x Dungeon Credits and Flurbos gained', 'Image': 'ballot-14'},
    750: {'Reward': '-30% Kitchen Upgrade Costs', 'Image': 'cooking-table'},
    2500: {'Reward': '1.20x Chance to find Sailing Artifacts', 'Image': 'artifact-find-chance'},
    10e3: {'Reward': 'Dirty Shovel digs up +25% more Gold Nuggets', 'Image': 'dirty-shovel'},
    20e3: {'Reward': '+100 Star Talent Pts', 'Image': 'star-talent-icon'},
    40e3: {'Reward': 'World 6 Bonus... I wonder what it will be...', 'Image': 'rift-tbd'},
    60e3: {'Reward': 'World 7 Bonus... I wonder what it will be...', 'Image': 'rift-tbd'},
}
killroy_dict = {
    'Timer': {
        'Required Fights': 0,
        'Required Equinox': 0,
        'UpgradesIndex': 106,
        'Image': 'killroy-timer'
    },
    'Talent Points': {
        'Required Fights': 2,
        'Required Equinox': 0,
        'UpgradesIndex': 107,
        'Image': 'killroy-talent-points'},
    'Skulls': {
        'Required Fights': 16,
        'Required Equinox': 0,
        'UpgradesIndex': 108,
        'Image': 'killroy-skulls'
    },
    'Respawn': {
        'Required Fights': 36,
        'Required Equinox': 1,
        'UpgradesIndex': 109,
        'Image': 'killroy-respawn'
    },
    'Dungeon Credits': {
        'Required Fights': 64,
        'Required Equinox': 2,
        'UpgradesIndex': 110,
        'Image': 'killroy-dungeon-credits'
    },
    'Pearls': {
        'Required Fights': 100,
        'Required Equinox': 3,
        'UpgradesIndex': 111,
        'Image': 'killroy-pearls'
    },
        }
killroy_only_1_level = ['Talent Points', 'Dungeon Credits', 'Pearls']

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
max_printer_sample_rate = 90
arbitrary_shrine_goal = 26
arbitrary_shrine_note = f"Shrines have no Max level, goal of {arbitrary_shrine_goal} is arbitrary"
maxDreams = 36  # Last verified as of v2.10
dreamsThatUnlockNewBonuses = [1, 3, 6, 8, 11, 14, 18, 21, 24, 29, 32]
equinoxBonusesDict = {
    2: {'Name': 'Equinox Dreams', 'BaseLevel': 5, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 5, 'Category': 'Recommended', 'SummoningExpands': False},
    3: {'Name': 'Equinox Resources', 'BaseLevel': 4, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 4, 'Category': 'Recommended', 'SummoningExpands': False},
    4: {'Name': 'Shades of K', 'BaseLevel': 3, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 3, 'Category': 'Optional', 'SummoningExpands': False},
    5: {'Name': 'Liquidvestment', 'BaseLevel': 4, 'MaxLevelIncreases': {7: 3, 16: 4}, 'FinalMaxLevel': 11, 'Category': 'Recommended', 'SummoningExpands': False},
    6: {'Name': 'Matching Scims', 'BaseLevel': 8, 'MaxLevelIncreases': {13: 5, 19: 10, 35: 10}, 'FinalMaxLevel': 33, 'Category': 'Recommended', 'SummoningExpands': True},
    7: {'Name': 'Slow Roast Wiz', 'BaseLevel': 5, 'MaxLevelIncreases': {33: 6}, 'FinalMaxLevel': 11, 'Category': 'Recommended', 'SummoningExpands': True},
    8: {'Name': 'Laboratory Fuse', 'BaseLevel': 10, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 10, 'Category': 'Optional', 'SummoningExpands': False},
    9: {'Name': 'Metal Detector', 'BaseLevel': 6, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 6, 'Category': 'Recommended', 'SummoningExpands': True},
    10: {'Name': 'Faux Jewels', 'BaseLevel': 6, 'MaxLevelIncreases': {22: 5, 27: 10}, 'FinalMaxLevel': 21, 'Category': 'Recommended', 'SummoningExpands': True},
    11: {'Name': 'Food Lust', 'BaseLevel': 10, 'MaxLevelIncreases': {26: 4}, 'FinalMaxLevel': 14, 'Category': 'Optional', 'SummoningExpands': True},
    12: {'Name': 'Equinox Symbols', 'BaseLevel': 5, 'MaxLevelIncreases': {31: 4}, 'FinalMaxLevel': 9, 'Category': 'Recommended', 'SummoningExpands': True},
    13: {'Name': 'Voter Rights', 'BaseLevel': 15, 'MaxLevelIncreases': {36: 15}, 'FinalMaxLevel': 30, 'Category': 'Recommended', 'SummoningExpands': True},
}
refineryDict = {
    # "salt": [json index, advice image name, cycles per Synth cycle, consumption of previous salt, next salt consumption, next salt cycles per Synth cycle]
    "Red": [3, "redox-salts", 4, 0, 2, 4],
    "Orange": [4, "explosive-salts", 4, 2, 2, 4],
    "Blue": [5, "spontaneity-salts", 4, 2, 1, 1],
    "Green": [6, "dioxide-synthesis", 1, 1, 2, 1],
    "Purple": [7, "purple-salt", 1, 2, 2, 1],
    "Nullo": [8, "nullo-salt", 1, 2, 0, 0]
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
    18: {'Name': 'Woodular Shrine', 'Image': 'woodular-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 12, 'ValueIncrement': 3},
    19: {'Name': 'Isaccian Shrine', 'Image': 'isaccian-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 12, 'ValueIncrement': 3},
    20: {'Name': 'Crystal Shrine', 'Image': 'crystal-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 20, 'ValueIncrement': 4},
    21: {'Name': 'Pantheon Shrine', 'Image': 'pantheon-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 10, 'ValueIncrement': 2},
    22: {'Name': 'Clover Shrine', 'Image': 'clover-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 15, 'ValueIncrement': 3},
    23: {'Name': 'Summereading Shrine', 'Image': 'summereading-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 6, 'ValueIncrement': 1},
    24: {'Name': 'Crescent Shrine', 'Image': 'crescent-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 50, 'ValueIncrement': 10},
    25: {'Name': 'Undead Shrine', 'Image': 'undead-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 5, 'ValueIncrement': 1},
    26: {'Name': 'Primordial Shrine', 'Image': 'primordial-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 1, 'ValueIncrement': 0.1},
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
dnSkullRequirementList = [0, 25000, 100000, 250000, 500000, 1000000, 5000000, 100000000, 1000000000]
dnSkullValueList = [0, 1, 2, 3, 4, 5, 7, 10, 20]
reversed_dnSkullRequirementList = dnSkullRequirementList[::-1]
reversed_dnSkullValueList = dnSkullValueList[::-1]
dnSkullValueToNameDict = {
    0: "None",
    1: "Normal Skull",
    2: "Copper Skull",
    3: "Iron Skull",
    4: "Gold Skull",
    5: "Platinum Skull",
    7: "Dementia Skull",
    10: "Lava Skull",
    20: "Eclipse Skull"
}
dnNextSkullNameDict = {
    0: "Normal Skull",
    1: "Copper Skull",
    2: "Iron Skull",
    3: "Gold Skull",
    4: "Platinum Skull",
    5: "Dementia Skull",
    7: "Lava Skull",
    10: "Eclipse Skull",
    20: "Finished!"
}
apocableMapIndexDict = {
    0: [30, 9, 38, 69, 120, 166],  #Barbarian only, not in regular DeathNote
    1: [1, 2, 14, 17, 16, 13, 18, 31, 19, 24, 26, 27, 28, 8, 15],
    2: [51, 52, 53, 57, 58, 59, 60, 62, 63, 64, 65],
    3: [101, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117],
    4: [151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163],
    5: [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213],
    6: [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264]
}
dnBasicMapsCount = sum([len(v) for k, v in apocableMapIndexDict.items() if k > 0])
dnAllApocMapsCount = dnBasicMapsCount + len(apocableMapIndexDict[0])
apocAmountsList = [100000, 1000000, 100000000, 1000000000, 1000000000000]
apocNamesList = ["ZOW", "CHOW", "MEOW", "WOW", "64bitOverflow"]
apocDifficultyNameList = [
    'Basic W1 Enemies', 'Basic W2 Enemies', 'Basic W3 Enemies', 'Basic W4 Enemies', 'Basic W5 Enemies', 'Basic W6 Enemies',
    'Easy Extras', 'Medium Extras', 'Difficult Extras', 'Insane', 'Impossible'
]
trappingQuestsRequirementList = [
    {"QuestName": "Frogecoin to the MOON!",         'RequiredItems': {"Critter1": 100,   "Critter1A": 1}},
    {"QuestName": "Yet another Cartoon Reference",  'RequiredItems': {"Critter2": 250,   "Critter2A": 1}},
    {"QuestName": "Small Stingers, Big Owie",       'RequiredItems': {"Critter3": 500,   "Critter3A": 2}},
    {"QuestName": "The Mouse n the Molerat",        'RequiredItems': {"Critter4": 1000,  "Critter4A": 2}},
    {"QuestName": "Happy Tree Friend",              'RequiredItems': {"Critter5": 1500,  "Critter5A": 3}},
    {"QuestName": "Noot Noot!",                     'RequiredItems': {"Critter6": 2500,  "Critter6A": 4}},
    {"QuestName": "Bunny you Should Say That!",     'RequiredItems': {"Critter7": 4000,  "Critter7A": 6}},
    {"QuestName": "Rollin' Thunder",                'RequiredItems': {"Critter8": 8000,  "Critter8A": 10}},
    {"QuestName": "Glitter Critter",                'RequiredItems': {"Critter8A": 30,   "Critter6A": 60,    "Critter3A": 200}}
]
trapset_images = {
    0: 'cardboard-traps',
    1: 'silkskin-traps',
    2: 'wooden-traps',
    3: 'natural-traps',
    4: 'steel-traps',
    5: 'meaty-traps',
    6: 'royal-traps',
    7: 'egalitarian-traps',
    8: 'forbidden-traps',
    9: 'containment-of-the-zrgyios'
}

def getSkullNames(mkValue: int) -> str:
    try:
        return dnSkullValueToNameDict.get(mkValue, f"UnknownSkull{mkValue}")
    except Exception as reason:
        return f"Unexpected Input '{mkValue}' received: {reason}"

def getNextSkullNames(mkValue: int) -> str:
    try:
        return dnNextSkullNameDict.get(mkValue, f"UnknownSkull{mkValue}")
    except Exception as reason:
        return f"Unexpected Input received: {reason}"

def getEnemyNameFromMap(inputMap: str) -> str:
    mapNametoEnemyNameDict = {
        # W1 Maps
        "Spore Meadows": "Green Mushroom",
        "Froggy Fields": "Frog",
        "Valley of the Beans": "Bored Bean",
        "Birch Enclave": "Red Mushroom",
        "Jungle Perimeter": "Slime",
        "The Base of the Bark": "Stick",
        "Hollowed Trunk": "Nutto",
        "Where the Branches End": "Wood Mushroom",
        "Winding Willows": "Baby Boa",
        "Vegetable Patch": "Carrotman",
        "Forest Outskirts": "Glublin",
        "Encroaching Forest Villa": "Wode Board",
        "Tucked Away": "Gigafrog",
        "Poopy Sewers": "Poop",
        "Rats Nest": "Rat",
        "The Roots": "Special - Single Nutto at WorshipTD map",
        "The Office": "Special - Poops surrounding Dr.Def",
        "Meel's Crypt": "Special- Boop",

        # W2 Maps
        "Jar Bridge": "Sandy Pot",
        "The Mimic Hole": "Mimic",
        "Dessert Dunes": "Crabcake",
        "The Grandioso Canyon": "Mafioso",
        "Shifty Sandbox": "Sand Castle",
        "Pincer Plateau": "Pincermin",
        "Slamabam Straightaway": "Mashed Potato",
        "The Ring": "Tyson",
        "Up Up Down Down": "Moonmoon",
        "Sands of Time": "Sand Giant",
        "Djonnuttown": "Snelbie",
        "Mummy Memorial": "Special- Invisible Green Mushroom inside King Doot's map",

        # W3 Maps
        "Steep Sheep Ledge": "Sheepie",
        "Snowfield Outskirts": "Frost Flake",
        "The Stache Split": "Sir Stache",
        "Refrigeration Station": "Bloque",
        "Mamooooth Mountain": "Mamooth",
        "Rollin' Tundra": "Snowmen",
        "Signature Slopes": "Penguin",
        "Thermonuclear Climb": "Thermister",
        "Waterlogged Entrance": "Quenchie",
        "Cryo Catacombs": "Cryosnake",
        "Overpass of Sound": "Bop Box",
        "Crystal Basecamp": "Neyeptune",
        "Wam Wonderland": "Dedotated Ram",
        "Hell Hath Frozen Over": "Bloodbone",
        "Equinox Valley": "Special- AFK only Dedotated Ram",

        # W4 Maps
        "Spaceway Raceway": "Purp Mushroom",
        "TV Outpost": "TV",
        "Donut Drive-In": "Donut",
        "Outskirts of Fallstar Isle": "Demon Genie",
        "Mountainous Deugh": "Soda Can",
        "Wurm Highway": "Flying Worm",
        "Jelly Cube Bridge": "Gelatinous Cuboid",
        "Cocoa Tunnel": "Choccie",
        "Standstill Plains": "Biggole Wurm",
        "Shelled Shores": "Clammie",
        "The Untraveled Octopath": "Octodar",
        "Flamboyant Bayou": "Flombeige",
        "Enclave of Eyes": "Stilted Seeker",
        "The Rift": "Rift Monsters",

        # W5 Maps
        "Naut Sake Perimeter": "Suggma",
        "Niagrilled Falls": "Maccie",
        "The Killer Roundabout": "Mister Brightside",
        "Cracker Jack Lake": "Cheese Nub",
        "The Great Molehill": "Stiltmole",
        "Erruption River": "Molti",
        "Mount Doomish": "Purgatory Stalker",
        "OJ Bay": "Citringe",
        "Lampar Lake": "Lampar",
        "Spitfire River": "Fire Spirit",
        "Miner Mole Outskirts": "Biggole Mole",
        "Crawly Catacombs": "Crawler",
        "The Worm Nest": "Tremor Wurm",

        # W6 Maps
        "Gooble Goop Creek": "Sprout Spirit",
        "Picnic Bridgeways": "Ricecake",
        "Irrigation Station": "River Spirit",
        "Troll Playground": "Baby Troll",
        "Edge of the Valley": "Woodlin Spirit",
        "Bamboo Laboredge": "Bamboo Spirit",
        "Lightway Path": "Lantern Spirit",
        "Troll Broodnest": "Mama Troll",
        "Above the Clouds": "Leek Spirit",
        "Sleepy Skyline": "Ceramic Spirit",
        "Dozey Dogpark": "Skydoggie Spirit",
        "Yolkrock Basin": "Royal Egg",
        "Chieftain Stairway": "Minichief Spirit",
        "Emperor's Castle Doorstep": "Samurai Guardian",
    }
    try:
        return mapNametoEnemyNameDict.get(inputMap, f"UnknownMap:{inputMap}")
    except Exception as reason:
        return f"Unexpected Input received: {reason}"


###WORLD 4 CONSTS###
tomepct = {
  50: 10270,
  25: 19718,
  10: 23709,
  5: 24862,
  1: 26292,
  0.5: 26680,
  0.1: 27227,
}
maxCookingTables = 10  # Last verified as of v2.26
maxMealCount = 67  # Last verified as of v2.26
maxMealLevel = 110  # Last verified as of v2.26
cookingCloseEnough = 1500

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

riftRewardsDict = {
    5: {'Name': 'Trap Box Vacuum', 'Shorthand': "TrapBoxVacuum"},
    10: {'Name': 'Infinite Stars', 'Shorthand': "InfiniteStars"},
    15: {'Name': 'Skill Mastery', 'Shorthand': "SkillMastery"},
    20: {'Name': 'Eclipse Skulls', 'Shorthand': "EclipseSkulls"},
    25: {'Name': 'Stamp Mastery', 'Shorthand': "StampMastery"},
    30: {'Name': 'Eldritch Artifact', 'Shorthand': "EldritchArtifacts"},
    35: {'Name': 'Vial Mastery', 'Shorthand': "VialMastery"},
    40: {'Name': 'Construct Mastery', 'Shorthand': "ConstructionMastery"},
    45: {'Name': 'Ruby Cards', 'Shorthand': "RubyCards"},
    50: {'Name': 'Killroy Prime', 'Shorthand': "KillroyPrime"},
    55: {'Name': 'Sneaking Mastery', 'Shorthand': "SneakingMastery"},
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
    12: {
        'Name': 'Grand Martial of Shinytown',
        'BonusText': "Boosts the rate at which shiny pets level up from being in the fenceyard. This will help you rack up those 100+ Day requirements!",
        'BonusValue': 5,
        'MaxLevel': 300,
        'MaxValue': 1500,
        'UnlockLevel': 80,
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

shinyDaysList = [
    0, 3, 11, 33, 85,
    200, 448, 964, 2013, 4107,
    8227, 16234, 31633, 60989, 116522,
    220874, 415802, 778022, 1447955, 2681786,
]

def getShinyLevelFromDays(days: float) -> int:
    shinyLevel = 0
    for requirement in shinyDaysList:
        if float(days) > requirement:
            shinyLevel += 1
        else:
            break
    return shinyLevel

def getDaysToNextShinyLevel(days: float) -> float:
    shinyLevel = getShinyLevelFromDays(days)
    if shinyLevel >= len(shinyDaysList):
        return 0
    else:
        try:
            daysRemaining = shinyDaysList[shinyLevel] - float(days)
            return daysRemaining
        except Exception as reason:
            logger.warning(f"With shinyLevel of {shinyLevel}, Defaulting Shiny days Remaining to 0. Reason: {reason}")
            return 0


breedabilityDaysList = [
    0.0000,
    2.9722,
    25.5910,
    230.7881,
    2445.8520,
    30113.1432,
    421857.0285,
    6615176.2308,
    114686626.8729,
    2177232407.5082,
]
breedabilityHearts = [1 + pow(x, 1.25) for x in range(0, 10)]

def getBreedabilityMultiFromDays(days: float) -> float:
    if not isinstance(days, float):
        try:
            days = float(days)
        except:
            logger.warning(f"Expected days to be float type, got {type(days)}: {days}. Using 0 days instead.")
            days = 0
    result = 1 + math.log(max(1, pow(days+1, 0.725)))
    #logger.debug(f"getBreedabilityMultiFromDays: Given {days} days, Breedability Multi = {result}")
    return result

def getBreedabilityHeartFromMulti(multi: float) -> str:
    result = 0
    for reqIndex, requirement in enumerate(breedabilityHearts):
        if multi >= requirement:
            result += 1
        else:
            break
    return f"breedability-heart-{result}"


###World 5 Caverns CONSTS###
def getCavernResourceImage(resource_number: int):
    try:
        if int(resource_number) <= 9:
            resource_image = f'well-sediment-{resource_number}'
        elif int(resource_number) <= 19:
            resource_image = f'harp-note-{int(resource_number) - 10}'
        else:
            resource_image = ''
    except Exception as e:
        logger.exception(f"Error parsing resource type for resource {resource_number}")
        resource_image = ''
    return resource_image


HolesInfo = [
    "57 57 228 -29 183 0 216 -150 96 -219 255 -45 175 -28 257 -36 176 -67 216 -150 273 -35 184 -66 216 -150 24 -75 180 -54 220 -43 173 -60 232 95 216 -150 254 -49 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0".split(" "),
    "0 0 8 0 0 7 0 0 0 0 10 2 2 4 3 6 2 5 1 6 0 0 0 0 0 0 0 0 0 0".split(" "),
    "289 208 253 244 324 244 289 282 219 282 358 282 253 321 324 321 289 357".split(" "),
    "497 210 443 210 432 264 454 318 486 264 551 210 540 264 562 318 551 372 508 318 443 372 497 372".split(" "),
    "698 207 751 214 769 258 716 251 663 244 681 288 734 295 752 339 699 332 646 325 664 369 717 376".split(" "),
    "289 208 253 244 324 244 289 282 219 282 358 252 253 321 324 321 289 357".split(" "),
    "497 210 443 210 432 264 454 318 486 264 551 210 540 264 562 318 551 372 508 318 443 372 497 372".split(" "),
    "698 207 751 214 769 258 716 251 663 244 681 288 734 295 752 339 699 332 646 325 664 329 717 376".split(" "),
    ["12", "21"],
    ["12", "11", "12", "32"],
    "12 2 12 21 12 41".split(" "),
    "10 6 3 24 21 19 14 37".split(" "),
    ["13", "13"],
    ["3", "13", "24", "13"],
    "13 5 2 22 24 22".split(" "),
    "3 3 24 3 3 24 24 24".split(" "),
    ["12", "12"],
    ["5", "5", "18", "20"],
    "3 7 21 7 12 21".split(" "),
    "12 1 1 12 23 12 12 23".split(" "),
    "Explorer_@___@_Each_LV_of_this_villager_unlocks_a_new_cavern!_@___@_Invest_opals_to_increase_their_XP/hr_using_that_blue_button! Engineer_@___@_Each_LV_unlocks_3_new_schematics_to_create!_@_Every_5_LVs_unlocks_an_additional_schematic!__@___ Conjuror_@___@_Each_LV_gives_+1_Majik_Point_to_put_into_permanent_bonuses! Measurer_@___@_Each_LV_gives_a_new_bonus_to_upgrade!_The_multi_goes_up_as_you_increase_its_IdleOn_stat,_shown_in_parenthesis!__@___ Librarian Elder ??? ???".split(" "),
    "0 50 500 9000 125000 1500000 20000000 100000000 500000000 2000000000.0".split(" "),  #21 Well Sediment bars
    "讽 论 许 讲 议 训".split(" "),
    "316 639 291 372 409 533 264 409 400 600 240 400 390 556 217 382 393 567 180 331 400 580 190 390 334 620 198 390 443 502 286 372 340 640 116 295 390 556 217 382 0 0 0 0 439 507 251 380 390 556 217 382 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 316 639 294 425 390 556 217 382 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0".split(" "),
    "THE_MOTHERLODE THE_UNDYING_HIVE THE_EVERTREE THE_BOTTOMLESS_TRENCH MONUMENT_OF_BRAVERY MONUMENT_OF_JUSTICE MONUMENT_OF_WISDOM MONUMENT_OF_COMPASSION".split(" "),
    ["Mining_Efficency_needed:", "Catching_Efficency_needed:", "Choppin'_Efficency_needed:", "Fishing_Efficency_needed:"],
    ["Motherlode", "Bug14", "MotherlodeTREE", "MotherlodeFISH"],
    ["LAYER_", "HIVE_", "TRUNK_", "DEPTH_"],
    "BIGGER_BITE Hounds_now_have_a_base_attack_value_of_{ ELUSIVE_INSTINCT Hounds_now_require_{_Accuracy_for_100%_hit_chance CANINE_RECOVERY All_hounds_now_heal_{%_HP_every_3s BIGGER_BOW_WOW Hounds_have_a_10%_chance_to_spawn_BIG_with_{x_HP_and_DMG DOGGO_EMP_EFFECT Somehow_the_hounds_now_make_your_attacks_cost_{x_more_MP CURSED_HOWL Hounds_have_a_5%_chance_to_be_cursed,_causing_{x_more_Fear DEN_DESPAIR Start_with_your_fear_meter_filled_to_{% FAST_AND_DEADLY Hounds_cause_fear_{_seconds_faster_than_normal".split(" "),
    ["`@#$%^&*():;<,>.?{[}船般航舞窗皮白癖爬爆歧武歌歉款欺欧欣欢次斗文敲数敬散敢敞教敏情悚悔恼恰恭恨恤恢恒"],
    "1 80 300 750 2000 5000 10000 24000".split(" "),  #30 Monument Hours required to break layers
    "Swords_deal_{~}_damage +2_additional_Sword You_can_Re-Throw_5_swords_per_story +1_additional_Sword You_get_1_Retelling_per_story +1_additional_Sword +10_Re-Throws_per_story +1_additional_Sword Start_with_$_coins Start_with_2_Mental_Health You_can_Dismiss_1_case_per_story Start_with_1.5x_more_coins +1_Mental_Health_and_Dismissal Start_with_10_popularity Start_with_3x_more_coins +2_Mental_Health_and_Dismissals Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6".split(" "),
    "+{%|Mining|Efficiency }x_Bucket|Fill_Rate }x|Cooking_Speed +{%_EXP|Gain_for|Villagers }x|Gaming_Bits|Gain +{%_Chance|for_Bravery|Opals +{%_DMG|for_all|Characters }x_Bell_Ring|&_Ping_Rate +{%|All_Monument|AFK_Gain }x_Bravery|Bonuses_Multi +{%_Catching|Efficiency }x_Harp|Note_Gain }x_Artifact|Find_Chance +{%_EXP|Gain_for|Villagers }x|All_Summoning|Essence_Gain +{%_Chance|for_Justice|Opals +{%_Class|EXP_Gain +{%_more|daily_Lamp|Wishes +{%|All_Monument|AFK_Gain }x_Justice|Bonuses_Multi Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_3 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6".split(" "),  #32 Bravery win bonuses
    "DIRTY_NAPKIN LIL_BABY_SPIDER STRAW_SCARECROW DIM_NIGHTLIGHT BEDTIME_SHADOW THE_1[_OF_GERMS SLOW_ESCORT_NPC MONDAYS BROCCOLINI POP_SONG DOLL_TOY INSIDE_OUT_SOCK MILKLESS_CEREAL EXCESS_CALORIES SLIGHTLY_SHORT_LEG MUMBLE_RAPPER VENTRILAKWIST SPELLING_TEST_RESULT AIRPLANE_BABY SPECIFIC_CROW CLOWN ABSENCE_OF_CLOWNS DISCORD_CHAT_FLEX VIDEO_GAMES".split(" "),
    "Eww_gross_who_knows_where_that_thing_has_been AAAHH_KILL_IT_KILL_IT A_truly_intimidating_and_very_much_real_enemy_stood_before_me In_darkness_the_monsters_under_the_bed_thrive AAAAAAAAAHHHH_MONSTER If_the_sanitizer_couldn't_get_them_what_chance_do_I_have WHY_CANT_YOU_MOVE_FASTER_YOU_FIEND You_haven't_stopped_bothering_me_since_first_grade Terrible_taste_and_pretentious_name,_I_HATE_YOU I_don't_care_how_many_people_like_it,_it_sucks!!! The_lamest_of_all_toys,_action_figure_gang_for_life! I_nearly_lost_my_mind_fixing_you_every_day Truly_a_horrendous_sight_to_behold_on_weekend_morning Why_must_you_take_such_a_hideous_form_upon_my_body? You_FIEND,_you_ALWAYS_make_the_chair_wobble_uncontrolably What_are_you_even_SAYING??? Speaking_without_moving_your_mouth_should_be_illegal An_F?_Noooooooo! SHUT_UP_SHUT_UPPPPPP Grrr,_the_one_that_stole_my_food_Sunday_March_11th_2007... Huh?_I_wasn't_afriad_of_clowns,_I_loved_clowns! NOOOOOOOOOOOOOOOOoooooo! Terrible,_just_terrible... The_worst_media_form!_You_poison_our_youth! It's_been_a_while_since_the_last_update,_they_have_formed_an_army".split(" "),
    "So_you_as_well_have_an_undying_lust_for_battle,_I_wish_you_could've_fought_with_me_in_my_final_hour... Fighting_to_the_bitter_end,_we_really_did_make_the_best_of_this_test_known_as_life... A_weaker_gamer_would_have_run_at_some_point,_but_I'm_glad_to_know_at_least_you_would've_stayed_with_me! ..._and_when_the_dust_settled_there_were_no_bonuses_kept,_just_an_everlasting_idea_of_bravery. I_always_said_I'd_rather_live_by_what_I_live_by_than_die_when_I'm_fine So_there_you_have_it,_that's_the_story!_I_tried_so_hard,_and_got_so_far,_but,_well_you_know_how_it_ended... Ah_don't_feel_too_bad_for_me!_I'm_a_master_mental_gymnast,_I_already_see_the_loss_as_a_win! I..._lost?_I_guess_I_only_thought_about_the_good_times,_I_forgot_that's_how_it_ended... Wait_no_no,_that's_not_how_it_went..._I_must_have_been_thinking_about_a_friend,_I_would_never_have_lost_like_that! Well,_that's_my_story!_Standing_up_against_true_evil_with_honor,_bonuses_be_darned!".split(" "),
    "Maybe_when_I_was_younger,_before_I_came_to_understand_the_virtue_of_bravery... You_really_think_running_was_an_option?_To_abandon_the_fight,_all_for_a_few_bonuses? Huh,_well_uh,_I_never_actually_considered_running_away..._probably_why_I_have_a_monument_and_you_don't! No_no,_that's_not_how_MY_story_ended,_but_I_suppose_everyone_has_their_own_story_to_tell... Well_that's_not_how_MY_story_ended,_but_I_suppose_everyone_has_their_own_story_to_tell... No_wonder_I_was_left_to_fend_for_myself,_everyone_always_thinks_to_run_in_the_face_of_trouble... Ah,_you_didn't_think_I'd_want_to_risk_it_eh?_Even_just_one_more_fight? All_the_bonuses_in_the_world_wouldn't_have_convinced_me_of_running! The_bonuses_may_be_comforting_now,_but_I_wouldn't_be_able_to_live_with_a_guilty_conscience... Run_away?_Bah,_just_the_thought..._maybe_next_time_you'll_stand_by_me_'till_the_end! I_would_never_run,_but_go_ahead_and_keep_your_crummy_bonuses..._they're_worthless_compared_to_the_glory_of_battle! I'm_not_surprised_your_mind_thinks_to_flee..._you_weren't_the_only_one_who_left_me_to_perish! Ugh,_It's_always_about_bonuses_these_days..._no_one_is_in_it_for_the_glory_like_me! No_wonder_I_had_to_fight_alone,_all_you_gamers_think_about_is_running_away! I_think_I_had_one_more_fight_in_me,_but_that's_a_story_for_a_different_day... I_think_I_had_one_more_fight_in_me,_but_that's_a_story_for_a_different_day... I_couldn't_disagree_more,_but_I_know_bonuses_mean_so_much_to_so_many... You_would_rather_I_run_than_be_brave?_I_mean_yea,_you_get_to_keep_all_those_bonuses_forever..._but_still! You_would_rather_I_run_than_be_brave?_I_mean_yea,_you_get_to_keep_all_those_bonuses_forever..._but_still! You_would_rather_I_run_than_be_brave?_I_mean_yea,_you_get_to_keep_all_those_bonuses_forever..._but_still!".split(" "),
    "2 4 10 1 8 2 1 1 50 250 2 4 500 1 5 2 1 300 50 250 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0".split(" "),
    "3 2 5 0 4 1 6 7".split(" "),
    "1 4 6 11 16 21 26".split(" "),
    "0 1 58 59 2 12 3 52 15 16 14 26 24 4 57 42 17 56 49 32 27 13 5 18 55 45 43 39 33 37 41 6 28 19 60 25 23 29 53 50 34 40 7 20 46 38 47 48 54 44 61 35 8 21 30 9 51 36 22 10 31 11".split(" "),
    "Bravery Justice Wisdom Compassion Type5 Type6".split(" "),  #41 Monument Names
    "15000000000 100 1000000 300 150 1500 1 1 1 1 1 1".split(" "),
    ["lol"],
    ["렴련렛렘렐렌레렀럽럼"],
    "Creates_{_of_the_note_you're_tuned_to!_@_LV_bonus:_+}%_Harp_Note_Gain Has_a_{%_chance_of_finding_an_opal!_@_LV_bonus:_|x_Harp_Note_Gain Doesn't_do_anything..._but_its_LV_bonus_is_freakin'_epic!_@_LV_bonus:_|x_Harp_Power/hr Creates_{_of_the_tune,_and_notes_next_to_the_tune!_@_LV_bonus:_+}%_Harp_Note_Gain Gives_{_EXP_to_all_string_types!_@_LV_bonus:_+}%_String_EXP_Gain! Creates_{_of_every_note_you_know!_@_LV_bonus:_+}%_Harp_Note_Gain AijowfWE_wjioaef,_jopfweaj_waf_gtojigr_joifs!_@_LV_bonus:_+}%_omefw_jiowef".split(" "),
    ["렴련렛렘렐렌레"], "10 6 5 13 20 18 0".split(" "),
    "689 185 808 146 855 61 776 6 726 89 659 2 616 104 556 24 504 130 455 5 404 91 349 9".split(" "),
    "雕 雏 雇 雅 雄 难 隧 障 隐 随 陶 陵 陪".split(" "),
    "3 10 4 12 14 5 16 6 17 7 20 21 22".split(" "),  #50 = Measurement Resource Cost
    "誇 詳 話 詰 試 許 訪 討 計 触 i i i".split(" "),
    "3 4 6 8 1 7 2 8 3 0 4 7 3".split(" "),  #52 = Measurement scalar type matchup
    "GLOOMIE_KILLS CROPS_FOUND ACCOUNT_LV TOME_SCORE ALL_SKILL_LV IDK_YET DEATHNOTE_PTS HIGHEST_DMG SLAB_ITEMS IDK_YET 4 7 3".split(" "),  #53 = Measurement scalar types
    "+{%_VILLAGER|EXP_GAIN +{%_BRAVERY|SWORD_MAX_DMG +{%_BELL_RING|访_PING_RATE +{%_HARP|NOTE_GAIN +{%_DAILY|LAMP_WISHES +{%_BUCKET|FILL_RATE +{%_HARP|STRING_EXP +{%_VILLAGER|EXP_GAIN +{%_HARP|NOTE_GAIN +{%_MULTIKILL|PER_TIER i i i".split(" "),  #54 = Measurement bonuses
    "45TOT 2 10 6 80TOT 11 13 60TOT 30 40TOT 1 1 1".split(" "),
    "3 4 2 1 1 1 1 1 1".split(" "),
    "4 3 2 3 1 1 1 1 1 1 1 1".split(" "),
    "1 4 2 4 3 1 1 1 1 1 1 1".split(" "),
    "+{%_BUCKET|FILL_RATE 10 +{%_ALL|VILLAGER_EXP 0.5 +{%_HARP|NOTE_GAINS 10 +{%_DAILY|LAMP_WISHES 0.3".split(" "),  #59 Bell Ring Bonuses
    "+{%_Bell_Ring/hr +{%_Bell_Clean/hr +{%_Bell_Ring/hr +{%_Bell_Ping/hr +{%_Bell_Ring/hr +{%_Bell_Ring/hr".split(" "),  #60 Bell Clean Improvements
    "5 10 8 13 12 15".split(" "),  #61 Bell Improvement Modifiers
    "0|Can_I_has_{_coins_pwease?|c-1.h2|h-1|ch|coincheck 1|I_got_fined_{_coins_by_YOUR_LAWS_for_using_the_5_finger_discount!_Can_you_waive_this_fine?_I_really_don't_want_to_pay_it!|h1|c2.h-1|ch|no 2|Your_honor,_I_seek_an_investment_of_{_coins_in_order_to_grow_my_Student_Loans_company_and_acquire_new_victims._I_promise_your_money_will_double_by_next_time_you_see_me.|c-3.h-1|h2|c|coincheck 2|Good_afternoon,_I_represent_a_third_party_who_would_like_to_buy_your_popularity,_yes_ALL_of_it,_for_2_coins_per_pop._Would_you_be_interested_in_this?|_|h1|_|no 0|Hewwo_OwO_can_u_tell_everyone_they_are_stinky_heads?_Also_ummmmmmmm..._are_you_skibbidy??!?|h-1|h1|h|no 4|It's_a_heart_attack._You're_currently_in_the_hospital,_you'll_make_a_full_recovery_if_you_pay_{_coins_for_the_best_cardiologist.|c-5|m-1|c|coincheck 4|You're_in_a_coma._Yea,_car_crash_on_your_way_to_the_next_court_case._You'll_recover,_but_only_if_you_pay_{_coins_to_cover_the_doctor_fees.|c-4|m-1|c|coincheck 4|Snake_attack_during_a_weekend_hike._You_really_are_quite_the_extravert!_But,_the_venom_will_cause_quite_a_lot_of_stress_if_you_don't_buy_the_cure..._last_I_checked,_it_currently_goes_for_{_coins.|c-4|m-1|c|coincheck 4|Shark_attack_during_a_weekend_hike_in_the_ocean._You_REALLY_are_quite_the_extravert._But,_without_proper_care_that_wound_is_going_to_get_a_lot_worse!_It's_gonna_be_{_coins_for_full_medicare.|c-3|m-1|c|coincheck 4|Well_that_Stream_could_have_gone_better..._you're_a_Millennial_judge,_of_course_you_stream_in_your_free_time._Look,_unless_you_give_me_{_coins_to_wipe_your_memory,_you're_going_to_feel_REALLY_bad_for_a_long_time._Like,_really_bad.|c-4|m-1|c|coincheck 4|Uhhh..._hey...?_Why_am_I_here?_You_seem_fine._But,_since_I_AM_here,_I'm_a_bit_short_on_rent._Soooo_give_me_{_coins,_or_I'll_be_taking_1_mental_health_of_yours!|c-3|m-1|c|coincheck 4|Blocked_artery._Your_spouse_rushed_you_to_the_hospital_at_quite_the_pace,_you_should_say_thanks_if_you_ever_see_them_again!_The_bill_is_looking_to_be_about_{_coins,_are_you_ready_to_pay_up?|c-4|m-1|c|coincheck 4|Someone_you_rejected_is_putting_their_plot_into_action..._yea,_like,_right_now._Don't_be_too_surprised,_you're_really_not_that_popular._You_won't_come_out_unscathed_unless_you_pay_{_coins_to_hire_a_better_Bailiff.|c-6|m-1|c|coincheck 4|No_no,_I'm_not_here_for_you._It's..._well,_it's_Little_Timmy._After_that_3rd_rejection,_he_ran_home_crying_and_won't_come_out_of_his_room._It's_gonna_cost_you_{_coins_to_make_him_feel_better,_or_you_can_just_live_with_the_guilt.|c-8|m-1|c|coincheck 4|Uh_oh,_looks_like_your_bills_finally_got_the_better_of_you!_I_guess_managing_money_ain't_so_easy_after_all._Look,_if_you_give_me_}_popularity,_I'll_save_you_the_embarassment_of_an_empty_coffer.|h-1.c1|m-1|h|popcheck 4|You're_broke...?_AGAIN???_I_even_gave_you_a_coin_myself_last_time!_Nope,_you're_not_weaseling_your_way_out_of_this_one_you_sneaky_beaky._Approve,_reject,_dismiss,_I_don't_care,_I'm_taking_some_of_your_mental_with_me.|m-1|m-1|_|no 1|Good_going_judge,_your_STUPID_laws_just_got_me_arrested!_You_HAVE_to_pay_my_bail_of_{_coins,_you_OWE_me_for_enforcing_such_dumb_rules!!!|c-3.h1|h-1|ch|coincheck 1|Here_judge,_I_brought_the_{_coins_I_owe_for_my_previous_misdemeanors._Just_shake_my_hand_first,_I_promise_I_wont_do_anything_to_damage_your_mental_health!_Hehehe...|c5.m-1|_|c|no 3|Hey_pal,_how_we_doin'?_You_lookin'_for_some_extra_cash?_I_got_{_coins_on_me,_take_em!_Don't_ask_questions,_'specially_'bout_where_I_got_'em_from.|c3.h-1|h1|ch|no 3|Hey_friendo._Is_me_again,_what's_good?_I_got_a_huge_score,_and_wanted_to_share_some_of_it!_Here,_have_{_coins,_but_your_mental_health_will_take_a_hit_when_you_hear_the_news_tonight...|c7.m-1|h1|c|no 3|Aight,_check_it._I_ain't_done_no_dirty_tricks_this_time,_I_got_a_shiny_clean_coin_right_'ere,_just_for_you!_Seriously,_take_it!|c1|h-1|_|no 5|Retirement_is_important,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_it'll_cost_you_{_coins.|r1.c-2|_|c|coincheck 5|Retirement_is_the_key_to_happiness,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_it'll_cost_you_}_popularity.|r1.h-1|_|h|popcheck 6|Oh_boy,_I'm_in_the_Justice_Monument_minigame_again!_Wanna_trade_some_of_your_coins_for_my_popularity?_Also_it's_ok_if_you_don't_have_enough_coins,_I_have_plenty_of_popularity_to_go_around!|c-2.h1|h-1|ch|no 6|Hey_it's_me,_everyone's_favorite_wiggly_piece_of_paper!_I_really_want_to_help_the_next_guy,_can_you_PROMISE_me_you'll_Approve_the_next_case?_I'll_give_you_{_coins._Please?|c3|h-1|c|no 8|I've_been_watching_you_closely,_and_I_wanted_to_thank_you_for_everything_you've_done_for_the_community_with_a_gift_of_{_coins,_and_1_Retirement_Chest!|c5.r1|m-999|_|no 7|Mmmm_yeeees,_charmed_your_honor._Perchance_could_I_get_a_loan_of_all_your_money?_I_will_give_it_all_back_next_you_see_me,_and_you_would_make_me_one_very_happy_bean_oh_hohoho_yeeees!|h12|_|_|no 7|Huzzah,_it_is_I!_Would_you_like_to_buy_a_mental_health,_perchance?_I_doooo_have_the_greatest_mind_ever_to_grace_this_court!_All_it_will_cost_you_is..._HALF_of_all_your_coins!|m1|_|_|no 7|Hark,_I_have_returned_bearing_the_gift_of_a_Retirement_Chest,_albeit_only_if_you_can_solve_my_riddle._Tell_me_magistrate..._as_I_am_royalty,_what_action_to_me_speaks_loudest,_yet_not_at_all?|h-1|h-1|_|no 7|I_have_a_deeeelightful_proposition_for_you!_Every_time_you_Approve_a_case,_I_will_give_4_coins._However,_two_rejections_and_I_will_make_you_infinitely_unpopular._Any_Case_Dismissal_will_void_this_deal.|_|_|_|no 0|Can_u_subskwibe_to_my_yootoob_channel_pwease??_Is_free!!!|h1|h-2|h|no 3|Eyo_was_up_my_guy,_I_got_a_bit_of_a_deal_for_ya._{_coins,_but_you_can't_Approve_that_Little_Timmy_fella_next_you_see_him._Whatchu_think?|c3|_|c|no 0|I_stole_my_fwends_toy,_and_he_said_I_am_under_arrest._Can_I_be_free_pwease?_I_will_give_u_{_coins..._did_I_do_bribe_right?_Daddy_teached_it_to_me_today!|c1.h-1|h1|ch|no 5|Retirement_is_everything,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_I_want_1_mental_health..._unless_you're_down_to_your_last_one,_then_you_can_have_the_chest_free.|r1|_|_|no 6|Can_I_get_a_{_coin_loan_to_buy_my_next_kitchen_in_World_4?_I_play_the_game_too_you_know!_I'll_give_you_back_the_coins_plus_interest_next_time_you_see_me,_AND_you'll_have_my_gratitude!|c-2.h1|h-1|ch|coincheck 2|Greetings,_I_come_to_you_today_seeking_a_}_popularity_investment_since_my_last_company_spilled_some,_well,_accidentally_spilled..._look,_I_am_willing_to_offer_a_LOT_of_coins!|h-1.c3|h1|hc|popcheck 2|Greetings,_I_come_to_you_today_seeking_a_{_coin_investment_in_my_time_management_company._I_guarantee_you_a_250%_return,_but_it_will_take_15_court_cases_to_mature.|c-5|h1|c|coincheck 5|Retirement_is_the_top_priority,_trust_me!_I'll_give_you_1_retirement_chest_to_get_you_going,_but_I'll_be_taking_{_coins_and_}_popularity_whether_you_have_them_or_not!|r1.c-2.h-1|_|ch|no 3|Ok_dog_hear_me_out,_I_had_this_dope_idea_while_I_was_drying_out_yesterday..._a_reverse_bribe!_You_give_me_{_coins,_and_I'll_boost_your_popularity|c-1.h1|_|ch|coincheck 5|Retirement_is_the_number_one_source_of_all_things_good,_trust_me!_I'll_give_you_1_retirement_chest_completely_free_just_to_show_you_how_right_I_am!|r1|_|_|no 9|Sup._Heads_you_win_a_bunch_of_coins,_Tails_you_lose_some_coins._You_wanna_flip_for_it?|c3|_|c|no 9|Sup._Heads_you_dope_as_heck,_Tails_you_fail_the_vibe_check._You_wanna_flip_for_it?|h2|_|h|no 9|Sup._Heads_you_win_2_Retirement_Chests,_Tails_you_lose_1_Retirement_Chest._You_wanna_flip_for_it?|r2|_|_|no 2|Greetings,_I_have_a_fantastic_opportunity_for_you!_For_just_{_coins,_I_will_invest_in_a_crypto_coin_and_will_share_the_profits!_1_coin_returned_every_day_for_15_days!|c-6.h-1|h1|_|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.r1|h-1|c|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.h3|_|hc|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.m1|h-1|c|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.h2|_|c|coincheck 0|Can_u_make_today_a_holiday_so_school_is_no?|c-3.h2|_|ch|no 10|Eat_me_eat_me_eat_me!|h1|h-1|h|no 11|Can_you_make_it_legal_for_me_to_scare_people?_I'll_pay_you_handsomely,_but_I'll_keep_scaring_1_person_every_day,_FOooOooOREVER...|c6|h1|c|no 1|You_look_richer_than_the_guy_I_just_stole_from._Give_me_one_of_your_retirement_chests,_and_I'll_tell_all_the_other_Reanimated_Limbs_back_home_what_a_legend_you_are!|r-1.h4|h-1|h|chestcheck 5|Retirement_is_worth_considering,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_it'll_cost_you_{_coins.|r1.c-3|_|c|coincheck 2|Good_afternoon,_I_am_seeking_invesetment_in_my_new_Retirement_Hedgefund!_For_just_1_Retirement_Chest,_you_will_receive_royalties_of_2_coins_per_day_for_10_days!|r-1|h1|_|chestcheck 9|Sup._Heads_you_the_man_and_get_2_mental_health,_Tails_you_crazy_and_lose_1_mental_health._You_wanna_flip_for_it?|m2|_|_|no 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_around_I_grant_the_consumer_some_sort_of_Chest_Magnetizer_effect,_lasts_for_3_days_I_reckon...|c-1|_|c|coincheck 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_'round_I_grant_the_consumer_a_LOT_of_pop!|c-1.h1|_|ch|coincheck 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_'round_I_grant_the_consumer_2_dismissals,_but_I_am_known_in_the_state_of_Blunder_Hills_to_cause_mental_fatigue!|c-1.d2.m-1|_|c|coincheck 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_'round_I_grant_the_consumer_a_strange_ability_to_never_ever_become_unpopular!_Like,_ever!|c-1|_|c|coincheck 11|I'm_done_scaring_people..._I_thought_it_was_funny_for_a_while,_but_now_I_just_feel_bad._Can_you_reinstate_the_ban,_make_it_illegal_again?_I'll_pay_you!|c4.h1|_|c|no 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_I'm_just_a_normal_drink,_but_there's_a_1_in_4_chance_I'm_the_limited_edition_glass_all_the_internet_nerds_want_to_buy!|c-1|_|c|coincheck 7|Ohohoho_I_have_heard_the_stories_about_you_judge!_Oh_yes_indeed!_Gulp_gulp_gulp,_say_no_more!_Shall_we_keep_this_a_secret_between_us?_Oh_how_I_do_LOVE_secrets!|h2|h-4|h|no 1|You_are_SO_dumb,_forcing_me_here_whenever_I_break_your_dumb_rules._Can_you_just_make_me_above_the_law?_I'll_share_part_what_I_steal_every_time_you_see_me,_I'll_even_share_the_blame!|h-1|h2|_|no 3|Hey_buddy,_how's_the_grind_going?_Look,_I_got_{_coins_on_me,_and_you_can_have_them_all!!!_Only_thing_is,_for_3_days_you_won't_be_able_to_Approve_anything...|c7|_|c|no".split(" "),
    "Little_Timmy Reainmated_Hand Head_Honcho_of_Big_Biz_LLC Mister_Bribe The_Harbinger Retirement_Chester Scripticus Esquire_Bored_Bean The_Gratefulbinger Cool_Bird Chippy Ghost Grumblo Fizarre_Drink".split(" ")
]
caverns_cavern_names = {
    0: 'Camp',
    1: 'The Well',
    2: 'Motherlode',
    3: 'The Den',
    4: 'Bravery Monument',
    5: 'The Bell',
    6: 'The Harp',
    7: 'The Lamp',
    8: 'The Hive',
    9: 'Grotto',
    10: 'Justice Monument',
}
max_cavern = max(caverns_cavern_names.keys())
caverns_villagers = [
    {'Name': 'Polonai', 'Role': 'The Explorer', 'VillagerNumber': 1, 'UnlockedAtCavern': 0},
    {'Name': 'Kaipu', 'Role': 'The Engineer',   'VillagerNumber': 2, 'UnlockedAtCavern': 2},  #Motherlode
    {'Name': 'Cosmos', 'Role': 'The Conjuror',  'VillagerNumber': 3, 'UnlockedAtCavern': 5},  #The Bell
    {'Name': 'Minau', 'Role': 'The Measurer',   'VillagerNumber': 4, 'UnlockedAtCavern': 7},  #The Lamp
]
#Schematics stored in HolesBuildings function in source code
caverns_engineer_schematics = ["Opal_Dividends 0 0 6 1 Each_opal_invested_in_a_villager_now_gives_them_125_EXP/hr,_instead_of_100_EXP/hr_@_Also_worry_not,_you_can_reset_your_opals_later_at_Cavern_7".split(" "), "Better_Buckets 1 0 8 1 Increases_the_base_fill_rate_of_all_Well_Buckets_from_10/hr_to_15/hr._IMPORTANT:You_can_click_on_the_buckets_for_more_info!".split(" "), "Cavern_'Porting 0 0 60 1 All_teleports_to_this_map_are_free!_Also,_did_you_know_you_can_double-click_a_map_instead_of_pressing_the_Teleport_button?".split(" "), "2nd_Bucket! 1 0 130 1 Adds_another_bucket_at_the_Well!_You'll_need_to_expand_your_Gravel_bar_to_hold_the_130_needed_to_create_this!".split(" "), "3rd_Bucket! 1 1 850 1 Adds_another_bucket_at_the_Well!_Remember,_click_a_bucket_to_change_what_sediment_it_collects!_That's_how_you_get_this_gold_resource!".split(" "), "4th_Bucket! 1 2 3000 f Adds_yet_another_bucket_at_the_Well!".split(" "), "Five_Nights_at_Bucket 1 2 12500 f Adds_one_more_bucket_at_the_Well!_Five_buckets!!!_WOW!_That's_worth_writing_home_about!".split(" "), "6th_Bucket! 1 3 75000 f Adds_another_bucket_at_the_Well!_I_guess_5_wasn't_enough_for_a_go_getter_like_yourself!".split(" "), "7rth_Barckot?! 1 4 1 f Adds_another_bucket_at_the_Well!_You_DO_want_more_buckets,_right?".split(" "), "Last_Bucket! 1 5 1 f Adds_another_bucket_at_the_Well!_And_it's_the_last_one_too,_I_hope_your_bucket_lust_is_satiated!".split(" "), "9th_Bucket! 1 6 1 f Adds_another_bucket_at_the_Well!_Yea_apparently_there_were_a_few_more_of_these_left!".split(" "), "Bucket_Finale! 1 7 1 f Adds_another_bucket_at_the_Well!_And_yea_this_one_is_actually_the_last_one,_I_don't_think_an_11th_would_fit_on_screen!".split(" "), "Bar_Expand-o-rama 1 0 100 1 Adds_the_'Expand_Full_Bars'_toggle_to_the_Well!_Let_me_explain..._when_a_bar_is_full_of_sediment,_you_lose_half_of_the_sediment,_but_permanently_increase_the_max_by_1.50x!".split(" "), "UBER_Bar_Expand-o-rama-hala 1 0 28000 1 Allow_for_UBER_Full_Bar_Expansion,_which_means_you_can_expand_Well_Bars_beyond_the_previous_limit_of_14_times.".split(" "), "Expander_Extravaganza 1 1 350 1 Gives_all_your_buckets_+20%_Fill_Rate_per_bar_expansion_across_all_sediment_types!_This_includes_Uber_expansions_later!_@_Total_Bonus:_+{%".split(" "), "Motherlode_~_Bucket_Synergy 1 0 180 1 Gives_all_your_buckets_1.10x_fill_rate_per_Motherlode_Layer_you've_destroyed!_@_Total_Bonus:_{x".split(" "), "Green_Amplifier 1 1 250 1 Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Pink_Amplifier 1 2 3250 1 Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Yellow_Amplifier 1 0 10000 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Cyan_Amplifier 1 3 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Purple_Amplifier 1 13 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "White_Amplifier 1 6 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Dark_Amplifier 1 18 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Amplifier_Stackin' 1 2 10 f You_now_get_an_additional_+0.50x_Multiplier_at_the_Dawg_Den_for_every_10_total_charge_across_all_amplifiers!".split(" "), "The_Story_Changes_Over_Time... 1 1 600 1 Bravery_Swords_get_+1_minimum_DMG_and_+10_maximum_DMG_per_6_HR_of_AFK_time_at_the_Bravery_Monument!".split(" "), "First_Try,_I_swear! 1 0 10 f If_you_throw_the_LAST_bravery_sword_first,_and_it_kills_the_monster,_you_get_a_+10%_Sword_Max_DMG_bonus_for_the_rest_of_the_story._If_it_doesn't_kill,_this_bonus_resets_back_to_0%".split(" "), "Even_Better_Buckets 1 1 25 f Increases_the_base_fill_rate_of_all_Well_Buckets_from_15/hr_to_20/hr._Try_changing_your_bucket_to_remove_the_rocks,_once_you_remove_that_layer_you_can_collect_gold_dust!".split(" "), "Eee_String 2 10 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_by_plucking_it,_getting_+1_EXP_per_100%_Harp_Power!".split(" "), "Eff_String 2 12 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_by_plucking_it,_getting_+1_EXP_per_100%_Harp_Power!".split(" "), "Geez_String 2 14 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_just_like_any_other_string,_getting_+1_EXP_per_100%_Harp_Power!".split(" "), "Aye_String 2 16 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_just_like_any_other_string!".split(" "), "Bee_String 2 18 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_just_like_any_other_string!".split(" "), "Loaded_Harp 2 10 10 f Adds_+1_more_string_to_the_Harp,_ready_to_be_strummed_until_the_end_of_(the)_time_(signature)!".split(" "), "Packed_Harp 2 11 10 f Adds_+1_more_string_to_the_Harp,_you'll_find_it_right_next_to_all_your_other_strings!".split(" "), "Hefty_Harp 2 13 10 f Adds_+1_more_string_to_the_Harp,_it_even_makes_sound_when_strummed!_The_other_ones_do_too,_but_like,_this_one_does_too!_Just_incase_you_were_worried_it_wouldn't.".split(" "), "Multitudinal_Harp 2 15 10 f Adds_+9999_more_strings_to_the_Harp!_Haha_nah_just_+1_string,_figured_I'd_keep_you_on_your_toes!_If_I_tricked_you,_you_must_go_pluck_the_F_string.".split(" "), "Sumptuous_Harp 2 17 10 f Adds_+1_more_string_to_the_Harp..._all_these_strings_really_remind_me_of_string_cheese,_I_used_to_love_it!".split(" "), "Domino_Effect 2 4 10 f Strings_give_+20%_more_per_string_plucked_during_a_strum..._let_me_explain._Imagine_you_have_5_strings,_this_would_mean_the_final_string_you_pluck_would_be_worth_DOUBLE!".split(" "), "Variety_Effect 2 6 10 f Strings_give_+30%_more_for_each_unique_string_type_on_your_harp..._I_see_you_currently_have_$_different_strings_on_your_harp,_so_your_strings_are_all_worth_#%_more!".split(" "), "Stringy_Effect 2 3 10 f Strings_give_+15%_more._@_More_what,_you_ask?_More_everything!_They_give_more_String_EXP,_more_notes,_higher_chance_for_opal..._so_yea,_MORE!".split(" "), "Reroll_Keeper 1 5 10 f Each_unused_reroll_you_have_in_a_Bravery_Story_gives_+10%_Sword_Max_DMG._So_don't_be_all_loosey_goosey_with_those_rerolls!".split(" "), "Fractalfly_~_Harp_Synergy 2 13 10 f Boosts_your_Harp_Note_production_by_1.10x_per_Undying_Hive_Layer_you've_destroyed!_@_Total_Bonus:_{x".split(" "), "Double_Dinger_Ringer 1 3 10 f Ringing_the_Bell_now_has_a_+30%_chance_of_giving_+2_LV_to_a_bonus,_instead_of_just_+1_LV".split(" "), "RNG_Oxidizing_Layer 1 4 10 f When_you_Clean_the_Bell_and_FAIL_to_get_a_new_Improvement_Method,_the_success_chance_for_next_time_goes_up_by_1.25x._This_happens_every_fail,_and_resets_when_you_finally_succeed!".split(" "), "Gloomie_Mulch 0 14 10 f Gloomie_mushrooms_respawn_+10%_faster!_In_fact,_ALL_monsters_across_all_the_worlds_of_IdleOn_respawn_+10%_faster!".split(" "), "Improvement_Stackin' 1 12 10 f For_every_25_LVs_across_all_Improvement_Methods_upgrades_at_the_Bell,_all_your_Improvement_Method_bonuses_are_1.10x_higher!_@_Total_bonus:_}x".split(" "), "Gloomie_Lootie 0 6 10 f +5%_Drop_Rate_for_each_Colony_of_Gloomie_Mushrooms_defeated!_Drop_rate_here_as_in_like,_the_one_for_stuff_outside_of_the_Caverns._@_Total_Bonus:_+{%".split(" "), "Gloomie_Expie 0 15 10 f +25%_Class_EXP_gain_for_each_Colony_of_Gloomie_Mushrooms_defeated!_@_Total_Bonus:_+{%".split(" "), "Gloomie_Opie 0 16 10 f +10%_Villager_EXP_gain_for_each_Colony_of_Gloomie_Mushrooms_successfully_romanced..._or_defeated,_whichever_is_higher._@_Total_Bonus:_+{%".split(" "), "Motherlode_Trickledown 0 3 10 f +15%_All_Skill_Efficiency,_and_+10%_All_Skill_EXP_gain_per_Motherlode_Layer_you've_destroyed!".split(" "), "Fractalfly_Trickledown 0 15 10 f +15%_All_Skill_Efficiency,_and_+10%_All_Skill_EXP_gain_per_Undying_Hive_Layer_you've_destroyed!".split(" "), "Rift_Guy 3 0 10 f Hey_bet_you_weren't_expecting_to_see_me_here,_huh?_Well,_that's_just_how_it_goes_with_me,_it's_in_my_blood._It's_how_I_roll._Go_ahead,_create_me._Or_don't,_I'll_keep_being_me.".split(" "), "DNA_Rock_Tumbler 0 0 10 f Gives_you_a_+60%_chance_to_get_an_additional_Grey_Gene_when_trashing_a_pet_for_every_Power_of_10_Gravel_you_have._@_Total_Bonus:_+{%_Chance_for_extra_Gene".split(" "), "Final_Ballad_of_the_Snail 0 13 10 f Gives_you_a_1.04x_higher_success_chance_when_leveling_up_Snail_for_every_Power_of_10_Trebel_Notes_you_have._@_Total_Bonus:_{x_Snail_success_chance".split(" "), "Noise_Reduction_Therapy 0 15 10 f Gives_you_a_multiplicative_1.20x_Stealth_bonus_for_all_ninjas_for_every_Power_of_10_Quaver_Notes_you_have._@_Total_Bonus:_{x_Stealth".split(" "), "Tune_of_Artifaction 0 11 10 f Gives_you_+10%_Artifact_Find_Chance_for_every_Power_of_10_Natural_Notes_you_have._@_Total_Bonus:_+{%_Artifact_Find_Chance".split(" "), "Heavy_Redstone_Seasoning 0 2 10 f Gives_you_a_multiplicative_1.30x_Cooking_Speed_bonus_for_every_Power_of_10_Redstone_you_have._@_Total_Bonus:_{x_Cooking_Speed".split(" "), "True_Golden_Edge 0 1 10 f Gives_all_your_players_+20%_Damage_for_every_Power_of_10_Golddust_you_have._@_Total_Bonus:_+{%_Damage".split(" "), "Loadin'_some_'Lode 1 0 12 1 Gives_+5_Bucket_Fill_Rate_per_Power_of_10_Motherlode_Ore_mined._You_have_mined_#_so_far!_@_Total_Bonus:_+{/hr_Bucket_Fill_Rate".split(" "), "Hiring_the_Hounds_from_Beyond 1 0 30 1 Gives_+10_B.F.R._per_100_hounds_defeated_in_best_runs_of_each_class._尬__Beginner:!,_Warrior:#,_Archer:$,_Mage:%_@_Total_Bonus:_+{/hr_Bucket_Fill_Rate".split(" "), "Triple_Tap_Tinkle 1 6 10 f Ringing_the_Bell_now_has_another_+30%_chance_of_giving_+2_LV_to_a_bonus_instead_of_just_+1_LV._Also,_there's_a_new_+20%_chance_of_giving_+3_LV_instead_of_+2_or_+1!".split(" "), "Compound_Interest 2 12 600 f You_start_with_+1_more_Court_Coins_every_Power_of_2_HRs_of_AFK_time_at_the_Justice_Monument!_So_2Hrs_you_get_+1_coin,_4Hrs_you_get_+2_coins,_8Hrs_you_get_+3_coins,_and_so_on!".split(" ")]
caverns_engineer_schematics_unlock_order = [int(entry) for entry in HolesInfo[40]]
max_schematics = len(caverns_engineer_schematics)
released_schematics = 56  #Last confirmed as of v2.25 in n._customBlock_Holes when e == "SchematicsAvailable"
schematics_unlocking_buckets = ['2nd Bucket!', '3rd Bucket!', '4th Bucket!', 'Five Nights at Bucket', '6th Bucket!', '7rth Barckot?!', 'Last Bucket!', '9th Bucket!', 'Bucket Finale!']
schematics_unlocking_amplifiers = {
    'Bigger Bite': ['Hounds have higher base attack', '', 'den-amplifier-0'],
    'Elusive Instinct': ['Hounds require additional Accuracy', 'Green Amplifier', 'den-amplifier-1'],
    'Canine Recovery': ['Hounds regenerate HP', 'Pink Amplifier', 'den-amplifier-2'],
    'Bigger Bow Wow': ['Chance to spawn BIG Hounds with additional HP and DMG', 'Yellow Amplifier', 'den-amplifier-3'],
    'Doggo EMP Effect': ["Player's attacks cost higher MP", 'Cyan Amplifier', 'den-amplifier-4'],
    'Cursed Howl': ['Hounds have a chance to cause more Fear', 'Purple Amplifier', 'den-amplifier-5'],
    'Den Despair': ['Fear bar starts partially filled', 'White Amplifier', 'den-amplifier-6'],
    'Fast and Deadly': ['Hounds cause Fear faster', 'Dark Amplifier', 'den-amplifier-7']
}
schematics_unlocking_harp_strings = ['Loaded Harp', 'Packed Harp', 'Hefty Harp', 'Multitudinal Harp', 'Sumptuous Harp']
schematics_unlocking_harp_chords = ['Eee String', 'Eff String', 'Geez String', 'Aye String', 'Bee String']
max_buckets = 1 + len(schematics_unlocking_buckets)
sediment_names = ['Gravel', 'Goldust', 'Redstone', 'Mythril', 'Cobaltine', 'Brunite', 'Freezium', 'Sweetium', 'Rad Coral', 'Hyper Coral']
sediment_bars = [int(float(v)) for v in HolesInfo[21]]
max_sediments = len(sediment_names)
#Majiks stored in CosmoUpgrades in source code
caverns_conjuror_majiks = {
    "Hole": [
        {'Name':"Monumental Vibes", 'BonusPerLevel': 25, 'MaxLevel': 4, 'Scaling': 'value', 'Description': 'x stronger Monument Bonuses',},
        {'Name':"String is Strung", 'BonusPerLevel': 1, 'MaxLevel': 5, 'Scaling': 'add', 'Description': ' more Harp strings',},
        {'Name':"Wishy Washy", 'BonusPerLevel': 30, 'MaxLevel': 3, 'Scaling': 'add', 'Description': '% chance for additional Lamp wishes',},
        {'Name':"Hole Placeholder", 'BonusPerLevel': 1, 'MaxLevel': 2, 'Scaling': 'add', 'Description': " placeholder- Don't buy this",},
    ],
    "Village": [
        {'Name':"Opal Enthusiasm", 'BonusPerLevel': 30, 'MaxLevel': 5, 'Scaling': 'add', 'Description': '% Villager EXP per 10 Opals invested',},
        {'Name':"Contented Creator", 'BonusPerLevel': 1, 'MaxLevel': 4, 'Scaling': 'add', 'Description': '% Villager EXP per Schematic created',},
        {'Name':"Cosmo, Enhance!", 'BonusPerLevel': 10, 'MaxLevel': 3, 'Scaling': 'add', 'Description': '% Villager EXP, and unlocks Enhancing Conjuror Bonuses',},
        {'Name':"Lengthmeister", 'BonusPerLevel': 25, 'MaxLevel': 4, 'Scaling': 'value', 'Description': 'x higher Measurement Bonuses',},
        {'Name':"Village Placeholder", 'BonusPerLevel': 1, 'MaxLevel': 1, 'Scaling': 'add', 'Description': " placeholder- Don't buy this",},
    ],
    "IdleOn": [
        {'Name':"Pocket Divinity", 'BonusPerLevel': 1, 'MaxLevel': 2, 'Scaling': 'add', 'Description': ' account-wide Divinity links',},
        {'Name':"Beeg Beeg Forge", 'BonusPerLevel': 3, 'MaxLevel': 5, 'Scaling': 'multi', 'Description': 'x forge ore capacity',},
        {'Name':"Resource Bursting", 'BonusPerLevel': 100, 'MaxLevel': 3, 'Scaling': 'add', 'Description': '% multi-resource max',},
        {'Name':"Voter Integrity", 'BonusPerLevel': 6, 'MaxLevel': 5, 'Scaling': 'add', 'Description': '% larger Ballot bonus',},
        {'Name':"Weapon Relevancy", 'BonusPerLevel': 75, 'MaxLevel': 4, 'Scaling': 'add', 'Description': '% stronger Weapon Power',},
        {'Name':"IdleOn Placeholder", 'BonusPerLevel': 1, 'MaxLevel': 2, 'Scaling': 'add', 'Description': " placeholder- Don't buy this",},
    ]
}
max_majiks = 0
for majik_type, majiks in caverns_conjuror_majiks.items():
    for majik in majiks:
        max_majiks += majik['MaxLevel']
caverns_measurer_measurement_resources = HolesInfo[50]
caverns_measurer_scalar_matchup = HolesInfo[52]
caverns_measurer_scalars = HolesInfo[53]
caverns_measurer_measurements = HolesInfo[54]
max_measurements = sum(1 for measurement in caverns_measurer_measurements if measurement != 'i')  #i is a placeholder for not-implemented
caverns_measurer_measurement_names = [
    'Inches', 'Meters', 'Miles', 'Liters', 'Yards', 'Pixels',
    'Leagues', 'Nanometers', 'Sadness', 'Feet', 'Bababooey', 'Killermeters', 'Joules', 'TBD14'
]

for entry_index, entry in enumerate(caverns_measurer_measurements):
    try:
        caverns_measurer_measurements[entry_index] = [
            caverns_measurer_measurement_names[entry_index],
            entry.replace('|', ' ').replace('_', ' ').replace('+{%', '').replace('访', '&').title(),
            caverns_measurer_scalars[int(caverns_measurer_scalar_matchup[entry_index])].replace('_', ' ').title(),
            getCavernResourceImage(caverns_measurer_measurement_resources[entry_index])
        ]
    except:
        caverns_measurer_measurements[entry_index] = [
            f"UnknownUnit{entry_index}",
            entry.replace('|', ' ').replace('_', ' ').replace('+{%', '').replace('访', '&').title(),
            f"UnknownScalar{entry_index}",
            ''
        ]
monument_hours = [int(h) for h in HolesInfo[30]]  #[1, 80, 300, 750, 2000, 5000, 10000, 24000] as of 2.20
monument_names = [f"{monument_name} Monument" for monument_name in HolesInfo[41]]
released_monuments = 2  #Don't increase this without implementing a _parse_ function in models first
#Layer rewards are in HolesInfo[31], but I wanted to clean up the display a bit
monument_layer_rewards = {
    monument_names[0]: {
        monument_hours[0]: {'Description': 'Story Minigame unlocked with 3 Swords', 'Image': 'monument-basic-sword'},
        monument_hours[1]: {'Description': '+2 additional Swords', 'Image': 'monument-basic-sword'},
        monument_hours[2]: {'Description': 'You can Re-Throw 5 swords per story', 'Image': 'engineer-schematic-40'},
        monument_hours[3]: {'Description': '+1 additional Sword', 'Image': 'monument-basic-sword'},
        monument_hours[4]: {'Description': 'You get 1 Retelling per story', 'Image': 'measurement-1'},
        monument_hours[5]: {'Description': '+1 additional Sword', 'Image': 'monument-basic-sword'},
        monument_hours[6]: {'Description': '+10 Re-Throws per story', 'Image': 'engineer-schematic-40'},
        monument_hours[7]: {'Description': '+1 additional Sword', 'Image': 'monument-basic-sword'},
    },
    monument_names[1]: {
        monument_hours[0]: {'Description': 'Story Minigame unlocked with Coins', 'Image': 'justice-coin-1'},
        monument_hours[1]: {'Description': 'Start with +1 Mental Health', 'Image': 'justice-currency-2'},
        monument_hours[2]: {'Description': 'You can dismiss 1 case per story', 'Image': 'justice-currency-5'},
        monument_hours[3]: {'Description': 'Start with 1.5x more Coins', 'Image': 'justice-coin-2'},
        monument_hours[4]: {'Description': '+1 Mental Health and Dismissal', 'Image': 'justice-currency-6'},
        monument_hours[5]: {'Description': 'Start with +7 Popularity', 'Image': 'justice-currency-4'},
        monument_hours[6]: {'Description': 'Start with 3x more Coins', 'Image': 'justice-coin-3'},
        monument_hours[7]: {'Description': '+2 Mental Health and Dismissals', 'Image': 'justice-currency-6'},
    }
}
monument_bonuses_clean_descriptions = [d.replace('|', ' ').replace('_', ' ') for d in HolesInfo[32]]
monument_bonuses_scaling = [int(v) for v in HolesInfo[37]]
monument_bonuses = {
    monument_names[0]: {},
    monument_names[1]: {},
    #'Justice Monument': {},
    #'Wisdom Monument': {},
    #'Compassion Monument': {},
}
justice_monument_currencies = ['Mental Health', 'Coins', 'Popularity', 'Dismissals']
for i in range(0, 10*released_monuments):  #Final number is excluded in range. 10 for Bravery, 10 for Justice
    monument_name = monument_names[i//10]
    try:
        monument_bonuses[monument_name][i] = {
            'Description': monument_bonuses_clean_descriptions[i],
            'ScalingValue': monument_bonuses_scaling[i],
            'ValueType': 'Percent' if '{' in monument_bonuses_clean_descriptions[i] else 'Multi' if '}' in monument_bonuses_clean_descriptions[i] else 'Flat',
            'Image': f"{monument_name.lower().replace(' ', '-').replace('-monument', '')}-bonus-{i}",
        }
    except Exception as e:
        logger.exception(f"Couldn't parse {monument_name} bonus {i}: {e}")
        continue
bell_ring_images = ['well-bucket', 'opal', 'cavern-6', 'cavern-7']
bell_ring_bonuses = {}
for i in range(0, 4):
    bell_ring_bonuses[i] = {
        'Description': HolesInfo[59][i*2].replace('|', ' ').replace('_', ' ').title(),
        'ScalingValue': float(HolesInfo[59][i*2 + 1]),
        'Image': bell_ring_images[i]
    }
bell_clean_resources = ['coins', 'well-sediment-3', 'purple-bits', 'harp-note-4', 'particles', '']
bell_clean_improvements = {}
for i in range(0, 6):
    bell_clean_improvements[i] = {
        'Description': HolesInfo[60][i].replace('|', ' ').replace('_', ' '),
        'Image': (
            "bell-ring" if 'Ring' in HolesInfo[60][i] else
            'bell-ping' if 'Ping' in HolesInfo[60][i] else
            'bell-clean' if 'Clean' in HolesInfo[60][i] else
            ''
        ),
        'Resource': bell_clean_resources[i]}
harp_chord_effects = {
    'C': ['Generate the tuned Note', 'Harp Note Gain'],
    'D': ['Chance for an Opal', 'Harp Note Gain'],
    'E': ['Nothing', 'Harp Power/hr'],
    'F': ['Generate the tuned Note and both nearby Notes', 'Harp Note Gain'],
    'G': ['Generate EXP for all unlocked Chords', 'String EXP Gain'],
    'A': ['Generate every Note you have unlocked', 'Harp Note Gain'],
    'B': ['TBD', 'TBD'],
}
harp_notes = [
    'Crotchet Note', 'Natural Note', 'Bass Note', 'Treble Note', 'Eighth Note',
    'Quaver Note', 'Sharp Note', '(F)Clef Note', '(G)Clef Note', 'Sixteenth Note'
]
max_harp_notes = len(harp_notes)
#Taken from "LampBonuses" == e inside _customBlock_Holes function
#(a.engine.getGameAttribute("DNSM").h.HoleozDT = "25,10,8;15,40,10;20,35,12;1,1,1;2,2,2" last verified as of v2.23
lamp_world_wish_values = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [25, 10, 8],
    [15, 40, 10],
    [20, 35, 12],
    [1, 1, 1],
    [2, 2, 2]
]
#LampWishes = function () in source code, slightly cleaned up
lamp_wishes = [
    ["More Wishes", 1, 3, 1, "Unlock the next Wish Type"],
    ["Another Try", 6, 0, 0, "Reset Opals or Majik investments. Cost does not increase."],
    ["1000000 Opals", 2, 2, 1, "+1 Opal"],
    ["Bring Them Back", 2, 0, 0, "+12 AFK Hours to any unlocked Monument Cost does not increase."],
    ["World 4 Stuff", 1, .2, 1,
     f"+@% Cooking Speed, "
     f"+#% Shiny Pet LV Up & Breedability Rate, "
     f"+$% Lab EXP gain"],
    ["A Moderate Discount", 2, .5, 1, "15% discount on the next Engineer Schematic creation"],
    ["World 5 Things", 1, .2, 1,
     f"+@% Sailing Loot Value, "
     f"+#% Bits gain, "
     f"+$% Divinity Pts gain"],
    ["Infinite Resources", 1, .05, 1, "Well and Harp resource gain"],
    ["World 6 Majigers", 1, .2, 1,
     f"+@% Next Crop chance, "
     f"+#% Stealth for Ninja twins, "
     f"+$% All Essence gain"],
    ["Knowledge of Future", 999, 999, 1, "Not implemented"],
    ["World 7 Stuff", 999, 999, 1, "Not implemented"],
    ["World 8 Stuff", 999, 999, 1, "Not implemented"]
]

def getMaxEngineerLevel() -> int:
    max_engi_last_i_checked = 20  # Last checked on Justice Monument release 2.23
    if max_schematics > (1 + (max_engi_last_i_checked * 3) + (max_engi_last_i_checked // 5)):
        needed_level = 0
        unlocked_schematics = 0
        while unlocked_schematics < max_schematics:
            needed_level += 1
            unlocked_schematics = 1 + (needed_level * 3) + (needed_level // 5)
        logger.warning(f"Update consts.max_engi_last_i_checked! {needed_level} is needed to unlock {max_schematics}")
        return needed_level
    else:
        return max_engi_last_i_checked

def getVillagerEXPRequired(villager_index, villager_level):
    match villager_index:
        case 0:
            result = 10 * ((10 + 7 * pow(villager_level, 2.1)) * pow(2.1, villager_level) * (1 + .75 * max(0, villager_level - 4)) - 1.50)
        case 1:
            result = 30 * ((10 + 6 * pow(villager_level, 1.8)) * pow(1.57, villager_level))
        case 2:
            result = 50 * ((10 + 5 * pow(villager_level, 1.7)) * pow(1.4, villager_level))
        case 3:
            result = 120 * ((30 + 10 * pow(villager_level, 2)) * pow(2, villager_level))
        case _:
            result = 10 * pow(10, 20)
    return result

def getSedimentBarRequirement(sediment_index, sediment_level):
    result = 100 * pow(1.5, sediment_level) * ValueToMulti(sediment_bars[sediment_index])
    return result

def getWellOpalTrade(holes_11_9):
    # From looking at data, holes_11_9 is just the number of previously completed trades. Maybe it changes higher up at some point
    if holes_11_9 == 1:
        return 6
    elif holes_11_9 == 2:
        return 60
    else:
        result = (
            (1 + (3 * holes_11_9) + pow(holes_11_9, 2))
            * pow(3.5 + holes_11_9 / 10, holes_11_9)
        )
        return math.ceil(result) if 1e9 > result else math.floor(result)

def getMotherlodeResourceRequired(layers_destroyed: int):
    result = math.ceil(200 * pow(2.2, 1 + layers_destroyed))
    return result

def getMotherlodeEfficiencyRequired(layers_destroyed: int):
    result = math.ceil(9000 * pow(1.8, layers_destroyed))
    return result

def getDenOpalRequirement(current_opals: int):
    result = 12 * (150 + (30 + current_opals) * current_opals) * pow(1.5, current_opals)
    return round(result)

def getMonumentOpalChance(current_opals: int, opal_bonus_value: float = 1):
    result = (
        min(0.5, pow(0.5, current_opals))
        * ValueToMulti(opal_bonus_value)
    )
    return result

def getBellExpRequired(bell_index, current_uses: int):
    match bell_index:
        case 0:  #Ring
            result = (5 + 3 * current_uses) * pow(1.05, current_uses)
        case 1:  #Ping
            result = (10 + (10 * current_uses + pow(current_uses, 2.5))) * pow(1.75, current_uses)
        case 2:  #Clean
            result = 100 * pow(3, current_uses)
        case _:  #Renew falls into this else
            result = 250
    return result

def getBellImprovementBonus(i_index, i_level, schematic_stacks=0, schematic_owned=False):
    #"BellMethodsQTY" in source code
    # Yes, HolesInfo[61] only applies AFTER the schematic is purchased. Probably a bug in game but must be replicated here for accuracy.
    result = (
        2 * i_level * max(1, pow(1.1, schematic_stacks) * schematic_owned * float(HolesInfo[61][i_index]))
    )
    return result

def getGrottoKills(current_opals: int):
    result = 5000 * pow(3.4, current_opals)
    return result

def getHarpNoteUnlockCost(note_index):
    result = math.ceil(150 * pow(1 + note_index, 1.5) * pow(4.5, note_index))
    return result

def getWishCost(wish_index, wish_level):
    match wish_index:
        case 0:  #New Wish Type
            if 11 > wish_level:
                result = math.floor(1 + (2 * wish_level) + pow(wish_level, 2))
            else:
                result = 999999
        case 2:  #Opal
            result = math.floor(1 + (2 * wish_level) + pow(wish_level, 1.7))
        case _:  #Everything else
            result = math.floor(lamp_wishes[wish_index][1] + (wish_level * lamp_wishes[wish_index][2]))
    return result


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
captainBuffs = ['Boat Speed', 'Loot Value', 'Cloud Discover Rate', 'Artifact Find Chance', 'Rare Chest Chance', 'None']
goldrelic_multisDict = {
    0: 0,
    1: 2,
    2: 2.5,
    3: 3,
    4: 5
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
divinity_DivCostAfter3 = 40  # Last verified as of v2.12 Ballot
divinity_arctisBreakpoints = {
    12: { 60:  841,  61:  602,  62:  467,  63:  380,  64:  319,  65:  275,  66:  241},
    13: { 72:  841,  73:  647,  74:  525,  75:  441,  76:  379,  77:  332,  78:  295},
    14: { 85: 1331,  86:  986,  87:  782,  88:  648,  89:  522,  90:  481,  91:  425,  92:  381},
    15: {102: 1641, 103: 1246, 104: 1004, 105:  841, 106:  722, 107:  633, 108:  564, 109:  508, 110:  462},
    16: {122: 3601, 123: 2401, 124: 1801, 125: 1441, 126: 1201, 127: 1029, 128:  901, 129:  801, 130:  721},
    17: {150: 4441, 151: 3101, 152: 2383, 153: 1936, 154: 1631, 155: 1409, 156: 1241, 157: 1002},
    18: {188: 5983, 189: 4302, 190: 3361, 191: 2759, 192: 2341, 193: 2033, 194: 1798, 195: 1612},
    19: {244: 6041, 245: 4841, 246: 4041, 247: 3469, 248: 3041, 249: 2707, 250: 2441},
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
snailMaxRank = 25

def getDivinityNameFromIndex(inputValue: int) -> str:
    if inputValue == 0:
        return "Unlinked"
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
    {
        "Name": "Science Highlighter",
        "Bonus": "Adds a new bonus type to your crop scientist! Specifically '+1% Drop Rate' per Crop after 100! So having 105 crops would only give +5%",
        "CodeString": "L"
    },

]
gfood_codes = ["PeanutG", "ButterBar", *[f"FoodG{i}" for i in range(1, 14)]]
pristineCharmsList: list = [
    {'Name': 'Sparkle Log', 'Image': 'sparkle-log', 'Bonus': '1.20x Total DMG'},
    {'Name': 'Fruit Rolle', 'Image': 'fruit-rolle', 'Bonus': '+20% AGI'},
    {'Name': 'Glowing Veil', 'Image': 'glowing-veil', 'Bonus': '1.40x Artifact Find Chance'},
    {'Name': 'Cotton Candy', 'Image': 'cotton-candy-charm', 'Bonus': '1.15x Drop Rate'},
    {'Name': 'Sugar Bomb', 'Image': 'sugar-bomb', 'Bonus': '+20% STR'},
    {'Name': 'Gumm Eye', 'Image': 'gumm-eye', 'Bonus': '+20% LUK'},
    {'Name': 'Bubblegum Law', 'Image': 'bubblegum-law', 'Bonus': '1.25x Kill per Kill'},
    {'Name': 'Sour Wowzer', 'Image': 'sour-wowzer', 'Bonus': '+50% Sneaking EXP gain'},
    {'Name': 'Crystal Comb', 'Image': 'crystal-comb', 'Bonus': '1.30x Bigger Summoning Winner Bonuses'},
    {'Name': 'Rock Candy', 'Image': 'rock-candy', 'Bonus': '+50% Farming EXP gain'},
    {'Name': 'Lollipop Law', 'Image': 'lollipop-law', 'Bonus': '+20% WIS'},
    {'Name': 'Taffy Disc', 'Image': 'taffy-disc', 'Bonus': '1.50x Higher Overgrowth Chance'},
    {'Name': 'Stick of Chew', 'Image': 'stick-of-chew', 'Bonus': '1.30x All Essence Generation'},
    {'Name': 'Treat Sack', 'Image': 'treat-sack', 'Bonus': '1.40x Jade Coin gain'},
    {'Name': 'Gumm Stick', 'Image': 'gumm-stick', 'Bonus': '+50% Golden Food bonus'},
    {'Name': 'Lolly Flower', 'Image': 'lolly-flower', 'Bonus': '+25% Printer Output'},
    {'Name': 'Gumball Necklace', 'Image': 'gumball-necklace', 'Bonus': '1.40x Money from Monsters'},
    {'Name': 'Liqorice Rolle', 'Image': 'liqorice-rolle', 'Bonus': '1.25x Bigger Bonuses of Non Misc Stamps'},
]
sneakingGemstonesList: list[str] = [
    "Aquamarine", "Emerald", "Garnet", "Starite", "Topaz", "Moissanite"
]
sneakingGemstonesStatList: list[str] = [
    "Stealth", "Jade", "Door Damage", "Gold Charm Bonus", "Sneak EXP", "Gemstone Bonuses"
]
sneakingGemstonesFirstIndex = 233
sneakingGemstonesCount = len(sneakingGemstonesList)
sneakingGemstonesBaseValueDict = {"Aquamarine": 40, "Emerald": 15, "Garnet": 12, "Starite": 5, "Topaz": 10, "Moissanite": 3}
sneakingGemstonesMaxValueDict = {"Aquamarine": 10040, "Emerald": 5015, "Garnet": 2512, "Starite": 205, "Topaz": 1010, "Moissanite": 303}
maxFarmingCrops = 230  # Last verified as of 2.26 Death Bringer
maxFarmingValue = 10000  # Last verified as of 2.21 The Fixening
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
    18: {'Name': 'Overgrowth Superboost', 'UnlockLevel': 2000, 'Value': 1500},
    19: {'Name': 'Seed of Stats', 'UnlockLevel': 3500, 'Value': 5},
}
marketUpgradeList = [
    "Land Plots", "Stronger Vines", "Nutritious Soil", "Smarter Seeds",
    "Biology Boost", "Product Doubler", "More Beenz", "Rank Boost",
    "Overgrowth", "Evolution GMO", "Speed GMO", "OG Fertilizer",
    "EXP GMO", "Land Rank", "Value GMO", "Super GMO"]
#  Last verified from MarketInfo function as of 2.12, slightly tweaked for readability
marketUpgradeDetails = [
    "LAND_PLOTS {_extra_plots_of_land_to_plant_crops_in 0 2 2 2 0 20 1".split(" "),
    "STRONGER_VINES +{%_chance_for_+1_crop_when_fully_grown 1 0.18 2 1.13 3 500 2".split(" "),
    "NUTRITIOUS_SOIL +{%_growth_speed_for_all_land 7 0.15 3 1.12 8 500 1".split(" "),
    "SMARTER_SEEDS +{%_farming_EXP_gain_from_all_sources 21 0.14 6 1.1 14 500 3".split(" "),
    "BIOLOGY_BOOST +{%_chance_of_crop_evolution,_or_'next_crop'_chance 46 0.09 10 1.1 31 500 15".split(" "),
    "PRODUCT_DOUBLER +{%_chance_for_crops_to_be_worth_2x_when_collected 30 0.12 15 1.2 42 500 3".split(" "),
    "MORE_BEENZ +{%_magic_beans_gained_when_trading_in_crops 61 0.11 25 1.15 53 500 2".split(" "),
    "RANK_BOOST Plots_earn_+{%_more_Rank_XP_when_a_crop_is_collected 84 0.11 30 1.2 80 500 3".split(" "),
    "OVERGROWTH Unlocks_Overgrowth_(OG)._Each_OG_doubles_crop_value_~_EXP 2 0.10 10 1.1 19 1 1".split(" "),
    "EVOLUTION_GMO }x_crop_evolution_chance_per_crop_you_have_200_of 2 0.10 15 1.080 25 500 0.8".split(" "),
    "SPEED_GMO +{%_growth_speed_per_crop_you_have_1000_of 2 0.10 25 1.155 36 500 0.3".split(" "),
    "OG_FERTILIZER }x_higher_chance_for_Overgrowth_to_occur 2 0.10 40 1.060 48 500 1".split(" "),
    "EXP_GMO +{%_farming_EXP_gain_crop_you_have_2500_of 2 0.10 60 1.095 57 100 1".split(" "),
    "LAND_RANK Each_plot_now_gets_Rank_XP_when_a_crop_is_collected. 2 0.10 80 1.050 61 1 1".split(" "),
    "VALUE_GMO +{%_crop_value_per_crop_you_have_10k_of 2 0.10 150 1.125 95 500 0.02".split(" "),
    "SUPER_GMO +{%_all_'GMO'_bonuses_per_crop_you_have_100K_of 2 0.10 250 1.20 109 50 0.5".split(" "),
]
marketUpgradeFirstIndex = 2
marketUpgradeLastIndex = marketUpgradeFirstIndex + len(marketUpgradeList)
cropDepotDict = {
    # Scaling info inside _customBlock_FarmingStuffs, CropSCbonus
    0: {
        'EmporiumUnlockName': 'Reinforced Science Pencil',
        'BonusString': 'DMG',
        'funcType': 'add',
        'x1': 20,
        'x2': 0,
        'Image': 'depot-pencil',
    },
    1: {
        'EmporiumUnlockName': 'Science Pen',
        'BonusString': 'Gaming Evo',
        'funcType': 'pow',
        'x1': 1.02,
        'x2': 0,
        'Image': 'depot-pen',
    },
    2: {
        'EmporiumUnlockName': 'Science Marker',
        'BonusString': 'Jade Coin',
        'funcType': 'add',
        'x1': 8,
        'x2': 0,
        'Image': 'depot-marker',
    },
    3: {
        'EmporiumUnlockName': 'Science Featherpen',
        'BonusString': 'Meal Spd',
        'funcType': 'pow',
        'x1': 1.1,
        'x2': 0,
        'Image': 'depot-featherpen',
    },
    4: {
        'EmporiumUnlockName': 'Science Environmentally Sourced Pencil',
        'BonusString': 'Cash',
        'funcType': 'add',
        'x1': 15,
        'x2': 0,
        'Image': 'depot-green-pencil',
    },
    5: {
        'EmporiumUnlockName': 'Science Crayon',
        'BonusString': 'Pet Rate',
        'funcType': 'add',
        'x1': 7,
        'x2': 0,
        'Image': 'depot-crayon',
    },
    6: {
        'EmporiumUnlockName': 'Science Paintbrush',
        'BonusString': 'Base Critters',
        'funcType': 'add',
        'x1': 0.1,
        'x2': 0,
        'Image': 'depot-paintbrush',
    },
    7: {
        'EmporiumUnlockName': 'Science Highlighter',
        'BonusString': 'Drop Rate',
        'funcType': 'add',
        'x1': 1,
        'x2': 0,
        'Image': 'depot-highlighter',
    },

}
cropDict = {
#Basic
    #0: {'Name': '', 'Image': '', 'SeedName': 'Earthy', 'SeedCropIndex': None},
    1: {'Name': 'Apple', 'Image': 'apple-crop', 'SeedName': 'Basic', 'SeedCropIndex': 1},
    2: {'Name': 'Orange', 'Image': 'orange', 'SeedName': 'Basic', 'SeedCropIndex': 2},
    3: {'Name': 'Lemon', 'Image': 'lemon', 'SeedName': 'Basic', 'SeedCropIndex': 3},
    4: {'Name': 'Pear', 'Image': 'pear', 'SeedName': 'Basic', 'SeedCropIndex': 4},
    5: {'Name': 'Strawberry', 'Image': 'strawberry', 'SeedName': 'Basic', 'SeedCropIndex': 5},
    6: {'Name': 'Bananas', 'Image': 'bananas', 'SeedName': 'Basic', 'SeedCropIndex': 6},
    7: {'Name': 'Blueberry', 'Image': 'blueberry', 'SeedName': 'Basic', 'SeedCropIndex': 7},
    8: {'Name': 'Brown Grapes', 'Image': 'red-grapes', 'SeedName': 'Basic', 'SeedCropIndex': 8},
    9: {'Name': 'Red Pear', 'Image': 'red-pear', 'SeedName': 'Basic', 'SeedCropIndex': 9},
    10: {'Name': 'Pineapple', 'Image': 'pineapple', 'SeedName': 'Basic', 'SeedCropIndex': 10},
    11: {'Name': 'Lime', 'Image': 'lime', 'SeedName': 'Basic', 'SeedCropIndex': 11},
    12: {'Name': 'Raspberry', 'Image': 'raspberry', 'SeedName': 'Basic', 'SeedCropIndex': 12},
    13: {'Name': 'Fig', 'Image': 'fig', 'SeedName': 'Basic', 'SeedCropIndex': 13},
    14: {'Name': 'Peach', 'Image': 'peach', 'SeedName': 'Basic', 'SeedCropIndex': 14},
    15: {'Name': 'Purple Grapes', 'Image': 'purple-grapes', 'SeedName': 'Basic', 'SeedCropIndex': 15},
    16: {'Name': 'Yellow Pear', 'Image': 'yellow-pear', 'SeedName': 'Basic', 'SeedCropIndex': 16},
    17: {'Name': 'Watermelon', 'Image': 'watermelon', 'SeedName': 'Basic', 'SeedCropIndex': 17},
    18: {'Name': 'Green Grapes', 'Image': 'green-grapes', 'SeedName': 'Basic', 'SeedCropIndex': 18},
    19: {'Name': 'Dragon Fruit', 'Image': 'dragon-fruit', 'SeedName': 'Basic', 'SeedCropIndex': 19},
    20: {'Name': 'Mango', 'Image': 'mango', 'SeedName': 'Basic', 'SeedCropIndex': 20},
    21: {'Name': 'Gold Blueberry', 'Image': 'gold-blueberry', 'SeedName': 'Basic', 'SeedCropIndex': 21},
#Earthy
    22: {'Name': 'Carrot', 'Image': 'carrot', 'SeedName': 'Earthy', 'SeedCropIndex': 1},
    23: {'Name': 'Potato', 'Image': 'potato', 'SeedName': 'Earthy', 'SeedCropIndex': 2},
    24: {'Name': 'Beat', 'Image': 'beat', 'SeedName': 'Earthy', 'SeedCropIndex': 3},
    25: {'Name': 'Tomato', 'Image': 'tomato', 'SeedName': 'Earthy', 'SeedCropIndex': 4},
    26: {'Name': 'Artichoke', 'Image': 'artichoke', 'SeedName': 'Earthy', 'SeedCropIndex': 5},
    27: {'Name': 'Roma Tomato', 'Image': 'roma-tomato', 'SeedName': 'Earthy', 'SeedCropIndex': 6},
    28: {'Name': 'Butternut Squash', 'Image': 'butternut-squash', 'SeedName': 'Earthy', 'SeedCropIndex': 7},
    29: {'Name': 'Avocado', 'Image': 'avocado', 'SeedName': 'Earthy', 'SeedCropIndex': 8},
    30: {'Name': 'Red Pepper', 'Image': 'red-pepper', 'SeedName': 'Earthy', 'SeedCropIndex': 9},
    31: {'Name': 'Broccoli', 'Image': 'broccoli', 'SeedName': 'Earthy', 'SeedCropIndex': 10},
    32: {'Name': 'Radish', 'Image': 'radish', 'SeedName': 'Earthy', 'SeedCropIndex': 11},
    33: {'Name': 'Coconut', 'Image': 'coconut', 'SeedName': 'Earthy', 'SeedCropIndex': 12},
    34: {'Name': 'Sliced Tomato', 'Image': 'sliced-tomato', 'SeedName': 'Earthy', 'SeedCropIndex': 13},
    35: {'Name': 'Cashew', 'Image': 'cashew', 'SeedName': 'Earthy', 'SeedCropIndex': 14},
    36: {'Name': 'Turnip', 'Image': 'turnip', 'SeedName': 'Earthy', 'SeedCropIndex': 15},
    37: {'Name': 'Coffee Bean', 'Image': 'coffee-bean', 'SeedName': 'Earthy', 'SeedCropIndex': 16},
    38: {'Name': 'Pumpkin', 'Image': 'pumpkin', 'SeedName': 'Earthy', 'SeedCropIndex': 17},
    39: {'Name': 'Sliced Cucumber', 'Image': 'sliced-cucumber', 'SeedName': 'Earthy', 'SeedCropIndex': 18},
    40: {'Name': 'Eggplant', 'Image': 'eggplant-crop', 'SeedName': 'Earthy', 'SeedCropIndex': 19},
    41: {'Name': 'Lettuce', 'Image': 'lettuce', 'SeedName': 'Earthy', 'SeedCropIndex': 20},
    42: {'Name': 'Garlic', 'Image': 'garlic', 'SeedName': 'Earthy', 'SeedCropIndex': 21},
    43: {'Name': 'Green Beans', 'Image': 'green-beans', 'SeedName': 'Earthy', 'SeedCropIndex': 22},
    44: {'Name': 'Bell Pepper', 'Image': 'bell-pepper', 'SeedName': 'Earthy', 'SeedCropIndex': 23},
    45: {'Name': 'Corn', 'Image': 'corn-crop', 'SeedName': 'Earthy', 'SeedCropIndex': 24},
    46: {'Name': 'Gold Sliced Tomato', 'Image': 'gold-sliced-tomato', 'SeedName': 'Earthy', 'SeedCropIndex': 25},
#Bulbo
    47: {'Name': 'Daisy', 'Image': 'daisy', 'SeedName': 'Bulbo', 'SeedCropIndex': 1},
    48: {'Name': 'Flour', 'Image': 'flour', 'SeedName': 'Bulbo', 'SeedCropIndex': 2},
    49: {'Name': 'Stargazer Lily', 'Image': 'stargazer-lily', 'SeedName': 'Bulbo', 'SeedCropIndex': 3},
    50: {'Name': 'Rose', 'Image': 'rose', 'SeedName': 'Bulbo', 'SeedCropIndex': 4},
    51: {'Name': 'Sunflower', 'Image': 'sunflower', 'SeedName': 'Bulbo', 'SeedCropIndex': 5},
    52: {'Name': 'Blue Daisy', 'Image': 'blue-daisy', 'SeedName': 'Bulbo', 'SeedCropIndex': 6},
    53: {'Name': 'Red Rose', 'Image': 'red-rose', 'SeedName': 'Bulbo', 'SeedCropIndex': 7},
    54: {'Name': 'Tulip', 'Image': 'tulip', 'SeedName': 'Bulbo', 'SeedCropIndex': 8},
    55: {'Name': 'Pink Daisy', 'Image': 'pink-daisy', 'SeedName': 'Bulbo', 'SeedCropIndex': 9},
    56: {'Name': 'Cauliflower', 'Image': 'cauliflower', 'SeedName': 'Bulbo', 'SeedCropIndex': 10},
    57: {'Name': 'Cape Marguerite Daisy', 'Image': 'cape-marguerite-daisy', 'SeedName': 'Bulbo', 'SeedCropIndex': 11},
    58: {'Name': 'Papua Black Orchid', 'Image': 'papua-black-orchid', 'SeedName': 'Bulbo', 'SeedCropIndex': 12},
    59: {'Name': 'Muffin', 'Image': 'muffin', 'SeedName': 'Bulbo', 'SeedCropIndex': 13},
    60: {'Name': 'Black Rose', 'Image': 'black-rose', 'SeedName': 'Bulbo', 'SeedCropIndex': 14},
    61: {'Name': 'Golden Tulip', 'Image': 'golden-tulip', 'SeedName': 'Bulbo', 'SeedCropIndex': 15},
#Sushi
    62: {'Name': 'Sushi Crop 1', 'Image': 'sushi-crop-1', 'SeedName': 'Sushi', 'SeedCropIndex': 1},
    63: {'Name': 'Sushi Crop 2', 'Image': 'sushi-crop-2', 'SeedName': 'Sushi', 'SeedCropIndex': 2},
    64: {'Name': 'Sushi Crop 3', 'Image': 'sushi-crop-3', 'SeedName': 'Sushi', 'SeedCropIndex': 3},
    65: {'Name': 'Sushi Crop 4', 'Image': 'sushi-crop-4', 'SeedName': 'Sushi', 'SeedCropIndex': 4},
    66: {'Name': 'Sushi Crop 5', 'Image': 'sushi-crop-5', 'SeedName': 'Sushi', 'SeedCropIndex': 5},
    67: {'Name': 'Sushi Crop 6', 'Image': 'sushi-crop-6', 'SeedName': 'Sushi', 'SeedCropIndex': 6},
    68: {'Name': 'Sushi Crop 7', 'Image': 'sushi-crop-7', 'SeedName': 'Sushi', 'SeedCropIndex': 7},
    69: {'Name': 'Sushi Crop 8', 'Image': 'sushi-crop-8', 'SeedName': 'Sushi', 'SeedCropIndex': 8},
    70: {'Name': 'Sushi Crop 9', 'Image': 'sushi-crop-9', 'SeedName': 'Sushi', 'SeedCropIndex': 9},
    71: {'Name': 'Sushi Crop 10', 'Image': 'sushi-crop-10', 'SeedName': 'Sushi', 'SeedCropIndex': 10},
    72: {'Name': 'Sushi Crop 11', 'Image': 'sushi-crop-11', 'SeedName': 'Sushi', 'SeedCropIndex': 11},
    73: {'Name': 'Sushi Crop 12', 'Image': 'sushi-crop-12', 'SeedName': 'Sushi', 'SeedCropIndex': 12},
    74: {'Name': 'Sushi Crop 13', 'Image': 'sushi-crop-13', 'SeedName': 'Sushi', 'SeedCropIndex': 13},
    75: {'Name': 'Sushi Crop 14', 'Image': 'sushi-crop-14', 'SeedName': 'Sushi', 'SeedCropIndex': 14},
    76: {'Name': 'Sushi Crop 15', 'Image': 'sushi-crop-15', 'SeedName': 'Sushi', 'SeedCropIndex': 15},
    77: {'Name': 'Sushi Crop 16', 'Image': 'sushi-crop-16', 'SeedName': 'Sushi', 'SeedCropIndex': 16},
    78: {'Name': 'Sushi Crop 17', 'Image': 'sushi-crop-17', 'SeedName': 'Sushi', 'SeedCropIndex': 17},
    79: {'Name': 'Sushi Crop 18', 'Image': 'sushi-crop-18', 'SeedName': 'Sushi', 'SeedCropIndex': 18},
    80: {'Name': 'Sushi Crop 19', 'Image': 'sushi-crop-19', 'SeedName': 'Sushi', 'SeedCropIndex': 19},
    81: {'Name': 'Sushi Crop 20', 'Image': 'sushi-crop-20', 'SeedName': 'Sushi', 'SeedCropIndex': 20},
    82: {'Name': 'Sushi Crop 21', 'Image': 'sushi-crop-21', 'SeedName': 'Sushi', 'SeedCropIndex': 21},
    83: {'Name': 'Sushi Crop 22', 'Image': 'sushi-crop-22', 'SeedName': 'Sushi', 'SeedCropIndex': 22},
    84: {'Name': 'Sushi Crop 23', 'Image': 'sushi-crop-23', 'SeedName': 'Sushi', 'SeedCropIndex': 23},
#Mushie
    85:  {'Name': 'Mushroom 1', 'Image': 'mushroom-1', 'SeedName': 'Mushie', 'SeedCropIndex': 1},
    86:  {'Name': 'Mushroom 2', 'Image': 'mushroom-2', 'SeedName': 'Mushie', 'SeedCropIndex': 2},
    87:  {'Name': 'Mushroom 3', 'Image': 'mushroom-3', 'SeedName': 'Mushie', 'SeedCropIndex': 3},
    88:  {'Name': 'Mushroom 4', 'Image': 'mushroom-4', 'SeedName': 'Mushie', 'SeedCropIndex': 4},
    89:  {'Name': 'Mushroom 5', 'Image': 'mushroom-5', 'SeedName': 'Mushie', 'SeedCropIndex': 5},
    90:  {'Name': 'Mushroom 6', 'Image': 'mushroom-6', 'SeedName': 'Mushie', 'SeedCropIndex': 6},
    91:  {'Name': 'Mushroom 7', 'Image': 'mushroom-7', 'SeedName': 'Mushie', 'SeedCropIndex': 7},
    92:  {'Name': 'Mushroom 8', 'Image': 'mushroom-8', 'SeedName': 'Mushie', 'SeedCropIndex': 8},
    93:  {'Name': 'Mushroom 9', 'Image': 'mushroom-9', 'SeedName': 'Mushie', 'SeedCropIndex': 9},
    94:  {'Name': 'Mushroom 10', 'Image': 'mushroom-10', 'SeedName': 'Mushie', 'SeedCropIndex': 10},
    95:  {'Name': 'Mushroom 11', 'Image': 'mushroom-11', 'SeedName': 'Mushie', 'SeedCropIndex': 11},
    96:  {'Name': 'Mushroom 12', 'Image': 'mushroom-12', 'SeedName': 'Mushie', 'SeedCropIndex': 12},
    97:  {'Name': 'Mushroom 13', 'Image': 'mushroom-13', 'SeedName': 'Mushie', 'SeedCropIndex': 13},
    98:  {'Name': 'Mushroom 14', 'Image': 'mushroom-14', 'SeedName': 'Mushie', 'SeedCropIndex': 14},
    99:  {'Name': 'Mushroom 15', 'Image': 'mushroom-15', 'SeedName': 'Mushie', 'SeedCropIndex': 15},
    100: {'Name': 'Mushroom 16', 'Image': 'mushroom-16', 'SeedName': 'Mushie', 'SeedCropIndex': 16},
    101: {'Name': 'Mushroom 17', 'Image': 'mushroom-17', 'SeedName': 'Mushie', 'SeedCropIndex': 17},
    102: {'Name': 'Mushroom 18', 'Image': 'mushroom-18', 'SeedName': 'Mushie', 'SeedCropIndex': 18},
    103: {'Name': 'Mushroom 19', 'Image': 'mushroom-19', 'SeedName': 'Mushie', 'SeedCropIndex': 19},
    104: {'Name': 'Mushroom 20', 'Image': 'mushroom-20', 'SeedName': 'Mushie', 'SeedCropIndex': 20},
    105: {'Name': 'Mushroom 21', 'Image': 'mushroom-21', 'SeedName': 'Mushie', 'SeedCropIndex': 21},
    106: {'Name': 'Mushroom 22', 'Image': 'mushroom-22', 'SeedName': 'Mushie', 'SeedCropIndex': 22},
    107: {'Name': 'Mushroom 23', 'Image': 'mushroom-23', 'SeedName': 'Mushie', 'SeedCropIndex': 23},
#Normal Glassy
    108: {'Name': 'Glassy Bananas', 'Image': 'glassy-bananas', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 1},
    109: {'Name': 'Glassy Mango', 'Image': 'glassy-mango', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 2},
    110: {'Name': 'Glassy Mushroom', 'Image': 'glassy-mushroom', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 3},
    111: {'Name': 'Glassy Maki', 'Image': 'glassy-maki', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 4},
    112: {'Name': 'Glassy Broccoli', 'Image': 'glassy-broccoli', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 5},
    113: {'Name': 'Glassy Carrot', 'Image': 'glassy-carrot', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 6},
    114: {'Name': 'Glassy Tomato', 'Image': 'glassy-tomato', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 7},
    115: {'Name': 'Glassy Watermelon', 'Image': 'glassy-watermelon', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 8},
    116: {'Name': 'Glassy Shrimp', 'Image': 'glassy-shrimp', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 9},
    117: {'Name': 'Glassy Rose', 'Image': 'glassy-rose', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 10},
    118: {'Name': 'Glassy Lettuce', 'Image': 'glassy-lettuce', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 11},
    119: {'Name': 'Glassy Onigiri', 'Image': 'glassy-onigiri', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 12},
    120: {'Name': 'Glassy Corn', 'Image': 'glassy-corn', 'SeedName': 'Normal Glassy', 'SeedCropIndex': 13},
#Red Glassy
    121: {'Name': 'Red Glassy Bananas',     'Image': 'red-glassy-bananas', 'SeedName': 'Red Glassy',    'SeedCropIndex': 14},
    122: {'Name': 'Red Glassy Mango',       'Image': 'red-glassy-mango', 'SeedName': 'Red Glassy',      'SeedCropIndex': 15},
    123: {'Name': 'Red Glassy Broccoli',    'Image': 'red-glassy-broccoli', 'SeedName': 'Red Glassy',   'SeedCropIndex': 16},
    124: {'Name': 'Red Glassy Carrot',      'Image': 'red-glassy-carrot', 'SeedName': 'Red Glassy',     'SeedCropIndex': 17},
    125: {'Name': 'Red Glassy Tomato',      'Image': 'red-glassy-tomato', 'SeedName': 'Red Glassy',     'SeedCropIndex': 18},
    126: {'Name': 'Red Glassy Watermelon',  'Image': 'red-glassy-watermelon', 'SeedName': 'Red Glassy', 'SeedCropIndex': 19},
    127: {'Name': 'Red Glassy Shrimp',      'Image': 'red-glassy-shrimp', 'SeedName': 'Red Glassy',     'SeedCropIndex': 20},
    128: {'Name': 'Red Glassy Rose',        'Image': 'red-glassy-rose', 'SeedName': 'Red Glassy',       'SeedCropIndex': 21},
    129: {'Name': 'Red Glassy Onigiri',     'Image': 'red-glassy-corn', 'SeedName': 'Red Glassy',       'SeedCropIndex': 22},
    130: {'Name': 'Red Glassy Corn',        'Image': 'red-glassy-corn', 'SeedName': 'Red Glassy',       'SeedCropIndex': 23},
#Green Glassy
    131: {'Name': 'Green Glassy Bananas',     'Image': 'green-glassy-bananas', 'SeedName': 'Green Glassy',    'SeedCropIndex': 24},
    132: {'Name': 'Green Glassy Mango',       'Image': 'green-glassy-mango', 'SeedName': 'Green Glassy',      'SeedCropIndex': 25},
    133: {'Name': 'Green Glassy Broccoli',    'Image': 'green-glassy-broccoli', 'SeedName': 'Green Glassy',   'SeedCropIndex': 26},
    134: {'Name': 'Green Glassy Carrot',      'Image': 'green-glassy-carrot', 'SeedName': 'Green Glassy',     'SeedCropIndex': 27},
    135: {'Name': 'Green Glassy Tomato',      'Image': 'green-glassy-tomato', 'SeedName': 'Green Glassy',     'SeedCropIndex': 28},
    136: {'Name': 'Green Glassy Watermelon',  'Image': 'green-glassy-watermelon', 'SeedName': 'Green Glassy', 'SeedCropIndex': 29},
    137: {'Name': 'Green Glassy Shrimp',      'Image': 'green-glassy-shrimp', 'SeedName': 'Green Glassy',     'SeedCropIndex': 30},
    138: {'Name': 'Green Glassy Rose',        'Image': 'green-glassy-rose', 'SeedName': 'Green Glassy',       'SeedCropIndex': 31},
    139: {'Name': 'Green Glassy Onigiri',     'Image': 'green-glassy-corn', 'SeedName': 'Green Glassy',       'SeedCropIndex': 32},
    140: {'Name': 'Green Glassy Corn',        'Image': 'green-glassy-corn', 'SeedName': 'Green Glassy',       'SeedCropIndex': 33},
#White Glassy
    141: {'Name': 'White Glassy Bananas',     'Image': 'white-glassy-bananas', 'SeedName': 'White Glassy',    'SeedCropIndex': 34},
    142: {'Name': 'White Glassy Mango',       'Image': 'white-glassy-mango', 'SeedName': 'White Glassy',      'SeedCropIndex': 35},
    143: {'Name': 'White Glassy Broccoli',    'Image': 'white-glassy-broccoli', 'SeedName': 'White Glassy',   'SeedCropIndex': 36},
    144: {'Name': 'White Glassy Carrot',      'Image': 'white-glassy-carrot', 'SeedName': 'White Glassy',     'SeedCropIndex': 37},
    145: {'Name': 'White Glassy Tomato',      'Image': 'white-glassy-tomato', 'SeedName': 'White Glassy',     'SeedCropIndex': 38},
    146: {'Name': 'White Glassy Watermelon',  'Image': 'white-glassy-watermelon', 'SeedName': 'White Glassy', 'SeedCropIndex': 39},
    147: {'Name': 'White Glassy Shrimp',      'Image': 'white-glassy-shrimp', 'SeedName': 'White Glassy',     'SeedCropIndex': 40},
    148: {'Name': 'White Glassy Rose',        'Image': 'white-glassy-rose', 'SeedName': 'White Glassy',       'SeedCropIndex': 41},
    149: {'Name': 'White Glassy Onigiri',     'Image': 'white-glassy-corn', 'SeedName': 'White Glassy',       'SeedCropIndex': 42},
    150: {'Name': 'White Glassy Corn',        'Image': 'white-glassy-corn', 'SeedName': 'White Glassy',       'SeedCropIndex': 43},
#Purple Glassy
    151: {'Name': 'Purple Glassy Bananas',     'Image': 'purple-glassy-bananas', 'SeedName': 'Purple Glassy',    'SeedCropIndex': 44},
    152: {'Name': 'Purple Glassy Mango',       'Image': 'purple-glassy-mango', 'SeedName': 'Purple Glassy',      'SeedCropIndex': 45},
    153: {'Name': 'Purple Glassy Broccoli',    'Image': 'purple-glassy-broccoli', 'SeedName': 'Purple Glassy',   'SeedCropIndex': 46},
    154: {'Name': 'Purple Glassy Carrot',      'Image': 'purple-glassy-carrot', 'SeedName': 'Purple Glassy',     'SeedCropIndex': 47},
    155: {'Name': 'Purple Glassy Tomato',      'Image': 'purple-glassy-tomato', 'SeedName': 'Purple Glassy',     'SeedCropIndex': 48},
    156: {'Name': 'Purple Glassy Watermelon',  'Image': 'purple-glassy-watermelon', 'SeedName': 'Purple Glassy', 'SeedCropIndex': 49},
    157: {'Name': 'Purple Glassy Shrimp',      'Image': 'purple-glassy-shrimp', 'SeedName': 'Purple Glassy',     'SeedCropIndex': 50},
    158: {'Name': 'Purple Glassy Rose',        'Image': 'purple-glassy-rose', 'SeedName': 'Purple Glassy',       'SeedCropIndex': 51},
    159: {'Name': 'Purple Glassy Onigiri',     'Image': 'purple-glassy-corn', 'SeedName': 'Purple Glassy',       'SeedCropIndex': 52},
    160: {'Name': 'Purple Glassy Corn',        'Image': 'purple-glassy-corn', 'SeedName': 'Purple Glassy',       'SeedCropIndex': 53},
#Yellow Glassy
    161: {'Name': 'Yellow Glassy Bananas',     'Image': 'yellow-glassy-bananas', 'SeedName': 'Yellow Glassy',    'SeedCropIndex': 54},
    162: {'Name': 'Yellow Glassy Mango',       'Image': 'yellow-glassy-mango', 'SeedName': 'Yellow Glassy',      'SeedCropIndex': 55},
    163: {'Name': 'Yellow Glassy Broccoli',    'Image': 'yellow-glassy-broccoli', 'SeedName': 'Yellow Glassy',   'SeedCropIndex': 56},
    164: {'Name': 'Yellow Glassy Carrot',      'Image': 'yellow-glassy-carrot', 'SeedName': 'Yellow Glassy',     'SeedCropIndex': 57},
    165: {'Name': 'Yellow Glassy Tomato',      'Image': 'yellow-glassy-tomato', 'SeedName': 'Yellow Glassy',     'SeedCropIndex': 58},
    166: {'Name': 'Yellow Glassy Watermelon',  'Image': 'yellow-glassy-watermelon', 'SeedName': 'Yellow Glassy', 'SeedCropIndex': 59},
    167: {'Name': 'Yellow Glassy Shrimp',      'Image': 'yellow-glassy-shrimp', 'SeedName': 'Yellow Glassy',     'SeedCropIndex': 60},
    168: {'Name': 'Yellow Glassy Rose',        'Image': 'yellow-glassy-rose', 'SeedName': 'Yellow Glassy',       'SeedCropIndex': 61},
    169: {'Name': 'Yellow Glassy Onigiri',     'Image': 'yellow-glassy-corn', 'SeedName': 'Yellow Glassy',       'SeedCropIndex': 62},
    170: {'Name': 'Yellow Glassy Corn',        'Image': 'yellow-glassy-corn', 'SeedName': 'Yellow Glassy',       'SeedCropIndex': 63},
#Blue Glassy
    171: {'Name': 'Blue Glassy Bananas',     'Image': 'blue-glassy-bananas', 'SeedName': 'Blue Glassy',    'SeedCropIndex': 64},
    172: {'Name': 'Blue Glassy Mango',       'Image': 'blue-glassy-mango', 'SeedName': 'Blue Glassy',      'SeedCropIndex': 65},
    173: {'Name': 'Blue Glassy Broccoli',    'Image': 'blue-glassy-broccoli', 'SeedName': 'Blue Glassy',   'SeedCropIndex': 66},
    174: {'Name': 'Blue Glassy Carrot',      'Image': 'blue-glassy-carrot', 'SeedName': 'Blue Glassy',     'SeedCropIndex': 67},
    175: {'Name': 'Blue Glassy Tomato',      'Image': 'blue-glassy-tomato', 'SeedName': 'Blue Glassy',     'SeedCropIndex': 68},
    176: {'Name': 'Blue Glassy Watermelon',  'Image': 'blue-glassy-watermelon', 'SeedName': 'Blue Glassy', 'SeedCropIndex': 69},
    177: {'Name': 'Blue Glassy Shrimp',      'Image': 'blue-glassy-shrimp', 'SeedName': 'Blue Glassy',     'SeedCropIndex': 70},
    178: {'Name': 'Blue Glassy Rose',        'Image': 'blue-glassy-rose', 'SeedName': 'Blue Glassy',       'SeedCropIndex': 71},
    179: {'Name': 'Blue Glassy Onigiri',     'Image': 'blue-glassy-corn', 'SeedName': 'Blue Glassy',       'SeedCropIndex': 72},
    180: {'Name': 'Blue Glassy Corn',        'Image': 'blue-glassy-corn', 'SeedName': 'Blue Glassy',       'SeedCropIndex': 73},
#T08 Glassy
    181: {'Name': 'T08 Glassy Bananas',     'Image': 't08-glassy-bananas',      'SeedName': 'T08 Glassy', 'SeedCropIndex': 74},
    182: {'Name': 'T08 Glassy Mango',       'Image': 't08-glassy-mango',        'SeedName': 'T08 Glassy', 'SeedCropIndex': 75},
    183: {'Name': 'T08 Glassy Broccoli',    'Image': 't08-glassy-broccoli',     'SeedName': 'T08 Glassy', 'SeedCropIndex': 76},
    184: {'Name': 'T08 Glassy Carrot',      'Image': 't08-glassy-carrot',       'SeedName': 'T08 Glassy', 'SeedCropIndex': 77},
    185: {'Name': 'T08 Glassy Tomato',      'Image': 't08-glassy-tomato',       'SeedName': 'T08 Glassy', 'SeedCropIndex': 78},
    186: {'Name': 'T08 Glassy Watermelon',  'Image': 't08-glassy-watermelon',   'SeedName': 'T08 Glassy', 'SeedCropIndex': 79},
    187: {'Name': 'T08 Glassy Shrimp',      'Image': 't08-glassy-shrimp',       'SeedName': 'T08 Glassy', 'SeedCropIndex': 80},
    188: {'Name': 'T08 Glassy Rose',        'Image': 't08-glassy-rose',         'SeedName': 'T08 Glassy', 'SeedCropIndex': 81},
    189: {'Name': 'T08 Glassy Onigiri',     'Image': 't08-glassy-corn',         'SeedName': 'T08 Glassy', 'SeedCropIndex': 82},
    190: {'Name': 'T08 Glassy Corn',        'Image': 't08-glassy-corn',         'SeedName': 'T08 Glassy', 'SeedCropIndex': 83},
#T09 Glassy
    191: {'Name': 'T09 Glassy Bananas',     'Image': 't09-glassy-bananas',      'SeedName': 'T09 Glassy', 'SeedCropIndex': 84},
    192: {'Name': 'T09 Glassy Mango',       'Image': 't09-glassy-mango',        'SeedName': 'T09 Glassy', 'SeedCropIndex': 85},
    193: {'Name': 'T09 Glassy Broccoli',    'Image': 't09-glassy-broccoli',     'SeedName': 'T09 Glassy', 'SeedCropIndex': 86},
    194: {'Name': 'T09 Glassy Carrot',      'Image': 't09-glassy-carrot',       'SeedName': 'T09 Glassy', 'SeedCropIndex': 87},
    195: {'Name': 'T09 Glassy Tomato',      'Image': 't09-glassy-tomato',       'SeedName': 'T09 Glassy', 'SeedCropIndex': 88},
    196: {'Name': 'T09 Glassy Watermelon',  'Image': 't09-glassy-watermelon',   'SeedName': 'T09 Glassy', 'SeedCropIndex': 89},
    197: {'Name': 'T09 Glassy Shrimp',      'Image': 't09-glassy-shrimp',       'SeedName': 'T09 Glassy', 'SeedCropIndex': 90},
    198: {'Name': 'T09 Glassy Rose',        'Image': 't09-glassy-rose',         'SeedName': 'T09 Glassy', 'SeedCropIndex': 91},
    199: {'Name': 'T09 Glassy Onigiri',     'Image': 't09-glassy-corn',         'SeedName': 'T09 Glassy', 'SeedCropIndex': 92},
    200: {'Name': 'T09 Glassy Corn',        'Image': 't09-glassy-corn',         'SeedName': 'T09 Glassy', 'SeedCropIndex': 93},
#T10 Glassy
    201: {'Name': 'T10 Glassy Bananas',     'Image': 't10-glassy-bananas',      'SeedName': 'T10 Glassy', 'SeedCropIndex': 94},
    202: {'Name': 'T10 Glassy Mango',       'Image': 't10-glassy-mango',        'SeedName': 'T10 Glassy', 'SeedCropIndex': 95},
    203: {'Name': 'T10 Glassy Broccoli',    'Image': 't10-glassy-broccoli',     'SeedName': 'T10 Glassy', 'SeedCropIndex': 96},
    204: {'Name': 'T10 Glassy Carrot',      'Image': 't10-glassy-carrot',       'SeedName': 'T10 Glassy', 'SeedCropIndex': 97},
    205: {'Name': 'T10 Glassy Tomato',      'Image': 't10-glassy-tomato',       'SeedName': 'T10 Glassy', 'SeedCropIndex': 98},
    206: {'Name': 'T10 Glassy Watermelon',  'Image': 't10-glassy-watermelon',   'SeedName': 'T10 Glassy', 'SeedCropIndex': 99},
    207: {'Name': 'T10 Glassy Shrimp',      'Image': 't10-glassy-shrimp',       'SeedName': 'T10 Glassy', 'SeedCropIndex': 100},
    208: {'Name': 'T10 Glassy Rose',        'Image': 't10-glassy-rose',         'SeedName': 'T10 Glassy', 'SeedCropIndex': 101},
    209: {'Name': 'T10 Glassy Onigiri',     'Image': 't10-glassy-corn',         'SeedName': 'T10 Glassy', 'SeedCropIndex': 102},
    210: {'Name': 'T10 Glassy Corn',        'Image': 't10-glassy-corn',         'SeedName': 'T10 Glassy', 'SeedCropIndex': 103},
#T11 Glassy
    211: {'Name': 'T11 Glassy Bananas',     'Image': 't11-glassy-bananas',      'SeedName': 'T11 Glassy', 'SeedCropIndex': 104},
    212: {'Name': 'T11 Glassy Mango',       'Image': 't11-glassy-mango',        'SeedName': 'T11 Glassy', 'SeedCropIndex': 105},
    213: {'Name': 'T11 Glassy Broccoli',    'Image': 't11-glassy-broccoli',     'SeedName': 'T11 Glassy', 'SeedCropIndex': 106},
    214: {'Name': 'T11 Glassy Carrot',      'Image': 't11-glassy-carrot',       'SeedName': 'T11 Glassy', 'SeedCropIndex': 107},
    215: {'Name': 'T11 Glassy Tomato',      'Image': 't11-glassy-tomato',       'SeedName': 'T11 Glassy', 'SeedCropIndex': 108},
    216: {'Name': 'T11 Glassy Watermelon',  'Image': 't11-glassy-watermelon',   'SeedName': 'T11 Glassy', 'SeedCropIndex': 109},
    217: {'Name': 'T11 Glassy Shrimp',      'Image': 't11-glassy-shrimp',       'SeedName': 'T11 Glassy', 'SeedCropIndex': 110},
    218: {'Name': 'T11 Glassy Rose',        'Image': 't11-glassy-rose',         'SeedName': 'T11 Glassy', 'SeedCropIndex': 111},
    219: {'Name': 'T11 Glassy Onigiri',     'Image': 't11-glassy-corn',         'SeedName': 'T11 Glassy', 'SeedCropIndex': 112},
    220: {'Name': 'T11 Glassy Corn',        'Image': 't11-glassy-corn',         'SeedName': 'T11 Glassy', 'SeedCropIndex': 113},
#T12 Glassy
    221: {'Name': 'T12 Glassy Bananas',     'Image': 't12-glassy-bananas',      'SeedName': 'T12 Glassy', 'SeedCropIndex': 114},
    222: {'Name': 'T12 Glassy Mango',       'Image': 't12-glassy-mango',        'SeedName': 'T12 Glassy', 'SeedCropIndex': 115},
    223: {'Name': 'T12 Glassy Broccoli',    'Image': 't12-glassy-broccoli',     'SeedName': 'T12 Glassy', 'SeedCropIndex': 116},
    224: {'Name': 'T12 Glassy Carrot',      'Image': 't12-glassy-carrot',       'SeedName': 'T12 Glassy', 'SeedCropIndex': 117},
    225: {'Name': 'T12 Glassy Tomato',      'Image': 't12-glassy-tomato',       'SeedName': 'T12 Glassy', 'SeedCropIndex': 118},
    226: {'Name': 'T12 Glassy Watermelon',  'Image': 't12-glassy-watermelon',   'SeedName': 'T12 Glassy', 'SeedCropIndex': 119},
    227: {'Name': 'T12 Glassy Shrimp',      'Image': 't12-glassy-shrimp',       'SeedName': 'T12 Glassy', 'SeedCropIndex': 120},
    228: {'Name': 'T12 Glassy Rose',        'Image': 't12-glassy-rose',         'SeedName': 'T12 Glassy', 'SeedCropIndex': 121},
    229: {'Name': 'T12 Glassy Onigiri',     'Image': 't12-glassy-corn',         'SeedName': 'T12 Glassy', 'SeedCropIndex': 122},
    230: {'Name': 'T12 Glassy Corn',        'Image': 't12-glassy-corn',         'SeedName': 'T12 Glassy', 'SeedCropIndex': 123},
}
seed_base = {
    'Basic': 0.75,
    'Earthy': 0.63,
    'Bulbo': 0.3,
    'Sushi': 0.4,
    'Mushie': 0.2,
    'Glassy': 0.05,
}
crop_base = 0.3
def getCropEvoChance(overallSeedNumber: int) -> float:
    if cropDict[overallSeedNumber]['SeedCropIndex'] == 1:
        return 1
    else:
        try:
            if 'Glassy' in cropDict[overallSeedNumber]['SeedName']:
                return crop_base * pow(seed_base['Glassy'], cropDict[overallSeedNumber]['SeedCropIndex'] - 2)
            else:
                return crop_base * pow(seed_base[cropDict[overallSeedNumber]['SeedName']], cropDict[overallSeedNumber]['SeedCropIndex'] - 2)
        except:
            logger.warning(f"overallSeedNumber {overallSeedNumber} not found in cropDict, or SeedName not found in seed_base. Returning crop_base {crop_base}")
            return crop_base

def getRequiredCropNumber(upgrade, target_level):
    target_index = target_level - 1  #Formula uses the number of already purchased levels: x - 1
    result_number = 0
    match upgrade:
        case 'Land Plots':
            starting_value = 0
            scaling_value = 2
        case 'Stronger Vines':
            starting_value = 1
            scaling_value = 0.18
        case 'Nutritious Soil':
            starting_value = 7
            scaling_value = 0.15
        case 'Smarter Seeds':
            starting_value = 21
            scaling_value = 0.14
        case 'Biology Boost':
            starting_value = 46
            scaling_value = 0.09
        case 'Product Doubler':
            starting_value = 30
            scaling_value = 0.12
        case 'More Beenz':
            starting_value = 61
            scaling_value = 0.11
        case 'Rank Boost':
            starting_value = 84
            scaling_value = 0.11
        case _:
            starting_value = 0
            scaling_value = 0
    if upgrade == 'Land Plots':
        result_number = 1 + math.floor(
            starting_value + scaling_value * (target_index + scaling_value * math.floor(target_index / 3) + math.floor(target_index / 4))
        )
    else:
        result_number = 1 + math.floor(starting_value + scaling_value * target_index)

    return result_number

def getMoissaniteValue(moissaniteLevel: int):
    try:
        if moissaniteLevel > 0:
            return 3 + (300 * (moissaniteLevel / (moissaniteLevel+1000)))
        else:
            return 0
    except:
        return 0

def getGemstoneBoostedValue(gemstoneValue: float, moissaniteValue: float):
    if moissaniteValue > 0:
        moissaniteMulti = 1 + (moissaniteValue / 100)
        boostedValue = gemstoneValue * moissaniteMulti
        return boostedValue
    else:
        return gemstoneValue

def getGemstoneBaseValue(gemstoneName: str, gemstoneLevel: int):
    value = 0
    if gemstoneLevel > 0:
        if gemstoneName in sneakingGemstonesBaseValueDict:
            value = (
                sneakingGemstonesBaseValueDict[gemstoneName]
                + (
                    (sneakingGemstonesMaxValueDict[gemstoneName] - sneakingGemstonesBaseValueDict[gemstoneName])
                    * (gemstoneLevel / (gemstoneLevel + 1000))
                )
            )
        else:
            logger.warning(f"Unrecognized gemstoneName: '{gemstoneName}'. Returning default 0 value")
            value = 0
    return value

def getGemstonePercent(gemstoneName: str, gemstoneValue: float):
    try:
        return 100 * (gemstoneValue / sneakingGemstonesMaxValueDict[gemstoneName])
    except Exception as reason:
        logger.exception(f"Could not find max value for Gemstone: {gemstoneName} because: {reason}")
    pass


summoning_sanctuary_counts = [1]
for multi in range(3, 16):  #(3, 16) produces length of 14
    summoning_sanctuary_counts.append(multi * summoning_sanctuary_counts[-1])
#summoning_sanctuary_counts = [1, 3, 12, 60, 360, 2520, 20160, 181440, 1814400, 19958400, 239500800, 3113510400, 43589145600, 653837184000]
# Maps to the RewardID, 1 indexed because Lava
summoningRewards = [
    "Unknown",
    # Normal Rewards
    "x Total DMG", "x Jade Gain", "x Farming SPD", "x Artifact Find",
    " Lab Con Range", "x All Essence", "x Sneak EXP", "x Sigil SPD",
    "x Farming EXP", "% Drop Rate", "x Crop EVO", "% AFK Gains",
    "% Skill EXP", "x Construct SPD", "x Skill Effncy.", "x Cooking SPD",
    "x Gaming Bits", "x Shiny EXP", "% All Stat", " Library Max",
    # Endless Rewards
    "+ Stamp LV/day", "% Villager EXP", "% Ballot Bonus", "% Class EXP",
    "+ Equinox Max LV", "% Monument AFK", "x Meal Bonuses", "% for World 7 (Placeholder 1)", "% for World 7 (Placeholder 2)",
    "% for World 7 (Placeholder 3)", "% for World 7 (Placeholder 4)", "x Winner Bonuses"
]
summoning_rewards_that_dont_multiply_base_value = [
    summoningRewards[0],   #Placeholder
    summoningRewards[21],  #Stamp Levels
    summoningRewards[23],  #Ballot Bonus
    summoningRewards[25],  #Equinox Levels
    summoningRewards[32],  #Winner Bonuses
]
# Plenty of unknown values. HP, damage, speed, reward size, etc seem to require calculation 
summoningDict = {
    "White": {
        0: {
            "EnemyID": "Pet1", "Value2": 29, "Value3": 24, "Value4": 12, "OpponentName": "Pablo and his Plump Piggies",
            "RewardID": summoningRewards[1], "Value8": 0, "Image": "piggo", "RewardQTY": 8,
        },
        1: {
            "EnemyID": "Pet2", "Value2": 25, "Value3": 26, "Value4": 12, "OpponentName": "Gam3rPr0digy and their Boar Stampede",
            "RewardID": summoningRewards[2], "Value8": 1, "Image": "wild-boar", "RewardQTY": 15,
        },
        2: {
            "EnemyID": "Pet3", "Value2": 23, "Value3": 22, "Value4": 17, "OpponentName": "Donald and his Quacky Ducks",
            "RewardID": summoningRewards[3], "Value8": 2, "Image": "mallay", "RewardQTY": 3,
        },
        3: {
            "EnemyID": "Pet0", "Value2": 28, "Value3": 23, "Value4": 12, "OpponentName": "Sandy and her Nutty Squirrels",
            "RewardID": summoningRewards[6], "Value8": 3, "Image": "squirrel", "RewardQTY": 7,
        },
        4: {
            "EnemyID": "Pet4", "Value2": 30, "Value3": 25, "Value4": 18, "OpponentName": "Popo and their Largest of Mammalians",
            "RewardID": summoningRewards[4], "Value8": 5, "Image": "whale", "RewardQTY": 15,
        },
        5: {
            "EnemyID": "Pet6", "Value2": 34, "Value3": 21, "Value4": 18, "OpponentName": "Little Susie and her Bunny Family",
            "RewardID": summoningRewards[2], "Value8": 7, "Image": "bunny", "RewardQTY": 25,
        },
        6: {
            "EnemyID": "Pet5", "Value2": 26, "Value3": 29, "Value4": 14, "OpponentName": "MoveFan84 and his Famous Nacho Batallion",
            "RewardID": summoningRewards[1], "Value8": 13, "Image": "chippy", "RewardQTY": 12,
        },
        7: {
            "EnemyID": "Pet10", "Value2": 30, "Value3": 38, "Value4": 15, "OpponentName": "Ronaldo and his Cool Freakin' Birdz",
            "RewardID": summoningRewards[5], "Value8": 24, "Image": "cool-bird", "RewardQTY": 0.3,
        },
        8: {
            "EnemyID": "Pet11", "Value2": 34, "Value3": 30, "Value4": 16, "OpponentName": "Master Oogman and his Speedy Hedgehogs",
            "RewardID": summoningRewards[3], "Value8": 40, "Image": "hedgehog", "RewardQTY": 4,
        },
    },
    "Green": {
        0: {
            "EnemyID": "mushG", "Value2": 26, "Value3": 41, "Value4": 8, "OpponentName": "Jonesy and his Lil Mushies",
            "RewardID": summoningRewards[1], "Value8": 4, "Image": "green-mushroom", "RewardQTY": 15,
        },
        1: {
            "EnemyID": "mushR", "Value2": 20, "Value3": 38, "Value4": 13, "OpponentName": "Walter and his Lil Shrooms",
            "RewardID": summoningRewards[7], "Value8": 5, "Image": "red-mushroom", "RewardQTY": 10,
        },
        2: {
            "EnemyID": "frogG", "Value2": 27, "Value3": 18, "Value4": 9, "OpponentName": "Lex and her Hoppy Frogs",
            "RewardID": summoningRewards[2], "Value8": 6, "Image": "frog", "RewardQTY": 30,
        },
        3: {
            "EnemyID": "beanG", "Value2": 47, "Value3": 32, "Value4": 16, "OpponentName": "Bongo and his Lazy Beans",
            "RewardID": summoningRewards[1], "Value8": 8, "Image": "bored-bean", "RewardQTY": 16,
        },
        4: {
            "EnemyID": "slimeG", "Value2": 23, "Value3": 15, "Value4": 10, "OpponentName": "Sam and his Goopy Slimes",
            "RewardID": summoningRewards[5], "Value8": 10, "Image": "slime", "RewardQTY": 0.3,
        },
        5: {
            "EnemyID": "snakeG", "Value2": 33, "Value3": 24, "Value4": 14, "OpponentName": "Mika and his Itty Bitty Baby Boas",
            "RewardID": summoningRewards[2], "Value8": 12, "Image": "baby-boa", "RewardQTY": 35,
        },
        6: {
            "EnemyID": "carrotO", "Value2": 42, "Value3": 22, "Value4": 24, "OpponentName": "Guy Montag and his Walking Veggies",
            "RewardID": summoningRewards[3], "Value8": 15, "Image": "carrotman", "RewardQTY": 5,
        },
        7: {
            "EnemyID": "goblinG", "Value2": 38, "Value3": 34, "Value4": 16, "OpponentName": "Gork and his Ugly Glublins",
            "RewardID": summoningRewards[4], "Value8": 17, "Image": "glublin", "RewardQTY": 20,
        },
        8: {
            "EnemyID": "plank", "Value2": 44, "Value3": 21, "Value4": 21, "OpponentName": "Ed and his Stolen Planks",
            "RewardID": summoningRewards[8], "Value8": 19, "Image": "wode-board", "RewardQTY": 10,
        },
        9: {
            "EnemyID": "frogBIG", "Value2": 56, "Value3": 33, "Value4": 22, "OpponentName": "Gigachad and his Awesome Gigafrogs",
            "RewardID": summoningRewards[5], "Value8": 21, "Image": "gigafrog", "RewardQTY": 0.3,
        },
        10: {
            "EnemyID": "poopSmall", "Value2": 26, "Value3": 19, "Value4": 11, "OpponentName": "TP Pete Jr and his Battle Poops",
            "RewardID": summoningRewards[6], "Value8": 25, "Image": "poop", "RewardQTY": 15,
        },
        11: {
            "EnemyID": "ratB", "Value2": 31, "Value3": 19, "Value4": 13, "OpponentName": "Michael and his Rodents",
            "RewardID": summoningRewards[4], "Value8": 28, "Image": "rat", "RewardQTY": 15,
        },
        12: {
            "EnemyID": "branch", "Value2": 32, "Value3": 31, "Value4": 20, "OpponentName": "Kyle and his Branch Brigade",
            "RewardID": summoningRewards[3], "Value8": 31, "Image": "walking-stick", "RewardQTY": 4,
        },
        13: {
            "EnemyID": "acorn", "Value2": 42, "Value3": 25, "Value4": 17, "OpponentName": "Aaron and his Aacorn Gang",
            "RewardID": summoningRewards[6], "Value8": 39, "Image": "nutto", "RewardQTY": 20,
        },
        14: {
            "EnemyID": "mushW", "Value2": 26, "Value3": 37, "Value4": 13, "OpponentName": "Kip and his Lil Fungi",
            "RewardID": summoningRewards[1], "Value8": 50, "Image": "wood-mushroom", "RewardQTY": 19,
        },
    },
    "Yellow": {
        0: {
            "EnemyID": "jarSand", "Value2": 31, "Value3": 20, "Value4": 12, "OpponentName": "Karen and her Pots",
            "RewardID": summoningRewards[9], "Value8": 9, "Image": "sandy-pot", "RewardQTY": 5,
        },
        1: {
            "EnemyID": "mimicA", "Value2": 33, "Value3": 30, "Value4": 16, "OpponentName": "Jimmy and his Enthusiastic Mimics",
            "RewardID": summoningRewards[7], "Value8": 11, "Image": "mimic", "RewardQTY": 15,
        },
        2: {
            "EnemyID": "crabcake", "Value2": 35, "Value3": 43, "Value4": 21, "OpponentName": "Eugene and his Frosted Crabs",
            "RewardID": summoningRewards[10], "Value8": 14, "Image": "crabcake", "RewardQTY": 2,
        },
        3: {
            "EnemyID": "coconut", "Value2": 49, "Value3": 25, "Value4": 14, "OpponentName": "Nobby and his Gang of Nuts",
            "RewardID": summoningRewards[2], "Value8": 16, "Image": "mafioso", "RewardQTY": 40,
        },
        4: {
            "EnemyID": "sandcastle", "Value2": 32, "Value3": 17, "Value4": 17, "OpponentName": "Tiny Tim and his Cool Castles",
            "RewardID": summoningRewards[8], "Value8": 18, "Image": "sand-castle", "RewardQTY": 15,
        },
        5: {
            "EnemyID": "pincermin", "Value2": 39, "Value3": 54, "Value4": 26, "OpponentName": "Tira and her Shrewd Pincermen",
            "RewardID": summoningRewards[7], "Value8": 22, "Image": "pincermin", "RewardQTY": 25,
        },
        6: {
            "EnemyID": "potato", "Value2": 57, "Value3": 58, "Value4": 28, "OpponentName": "Misha and her Super Spuds",
            "RewardID": summoningRewards[3], "Value8": 26, "Image": "mashed-potato", "RewardQTY": 6,
        },
        7: {
            "EnemyID": "steak", "Value2": 55, "Value3": 37, "Value4": 23, "OpponentName": "Wlad and his Rootin' Tootin' Tysons",
            "RewardID": summoningRewards[5], "Value8": 30, "Image": "tyson", "RewardQTY": 0.3,
        },
        8: {
            "EnemyID": "moonman", "Value2": 27, "Value3": 29, "Value4": 22, "OpponentName": "Mac and his Many Moonmoons",
            "RewardID": summoningRewards[11], "Value8": 34, "Image": "moonmoon", "RewardQTY": 10,
        },
        9: {
            "EnemyID": "sandgiant", "Value2": 50, "Value3": 21, "Value4": 23, "OpponentName": "Sir Reginald and his Gentlemen Giants",
            "RewardID": summoningRewards[4], "Value8": 45, "Image": "sand-giant", "RewardQTY": 20,
        },
        10: {
            "EnemyID": "snailZ", "Value2": 42, "Value3": 26, "Value4": 25, "OpponentName": "Shelby and her Shelled Snelbies",
            "RewardID": summoningRewards[1], "Value8": 60, "Image": "snelbie", "RewardQTY": 25,
        },
    },
    "Blue": {
        0: {
            "EnemyID": "sheep", "Value2": 32, "Value3": 31, "Value4": 14, "OpponentName": "Paulie and his Sheepie Herd",
            "RewardID": summoningRewards[12], "Value8": 20, "Image": "sheepie", "RewardQTY": 1,
        },
        1: {
            "EnemyID": "flake", "Value2": 35, "Value3": 28, "Value4": 14, "OpponentName": "Dirk and his Celsius Flakes",
            "RewardID": summoningRewards[9], "Value8": 23, "Image": "frost-flake", "RewardQTY": 10,
        },
        2: {
            "EnemyID": "stache", "Value2": 30, "Value3": 19, "Value4": 14, "OpponentName": "Mr Harrison and his Mighty Staches",
            "RewardID": summoningRewards[6], "Value8": 27, "Image": "sir-stache", "RewardQTY": 30,
        },
        3: {
            "EnemyID": "bloque", "Value2": 40, "Value3": 27, "Value4": 12, "OpponentName": "Gibby and his Bloque Offensive",
            "RewardID": summoningRewards[1], "Value8": 29, "Image": "bloque", "RewardQTY": 30,
        },
        4: {
            "EnemyID": "mamoth", "Value2": 37, "Value3": 22, "Value4": 14, "OpponentName": "Esther and her Trampler Mamooths",
            "RewardID": summoningRewards[8], "Value8": 32, "Image": "mamooth", "RewardQTY": 15,
        },
        5: {
            "EnemyID": "snowball", "Value2": 33, "Value3": 26, "Value4": 20, "OpponentName": "Frosty and his Relatives",
            "RewardID": summoningRewards[13], "Value8": 35, "Image": "snowman", "RewardQTY": 10,
        },
        6: {
            "EnemyID": "penguin", "Value2": 52, "Value3": 24, "Value4": 22, "OpponentName": "The Accountant and his Trusty Penguins",
            "RewardID": summoningRewards[2], "Value8": 38, "Image": "penguin", "RewardQTY": 50,
        },
        7: {
            "EnemyID": "thermostat", "Value2": 43, "Value3": 39, "Value4": 25, "OpponentName": "Fermi and his Thermies",
            "RewardID": summoningRewards[4], "Value8": 41, "Image": "thermister", "RewardQTY": 20,
        },
        8: {
            "EnemyID": "glass", "Value2": 35, "Value3": 27, "Value4": 15, "OpponentName": "Kristen and her Chill Quenchies",
            "RewardID": summoningRewards[10], "Value8": 46, "Image": "quenchie", "RewardQTY": 3,
        },
        9: {
            "EnemyID": "snakeB", "Value2": 31, "Value3": 18, "Value4": 14, "OpponentName": "Rob and his Ice Cold Killer Snakes",
            "RewardID": summoningRewards[14], "Value8": 49, "Image": "cryosnake", "RewardQTY": 30,
        },
        10: {
            "EnemyID": "speaker", "Value2": 30, "Value3": 38, "Value4": 21, "OpponentName": "Lil Plump and his Dope Bops",
            "RewardID": summoningRewards[15], "Value8": 51, "Image": "bop-box", "RewardQTY": 10,
        },
        11: {
            "EnemyID": "eye", "Value2": 39, "Value3": 23, "Value4": 18, "OpponentName": "Nadia and her All Seeing Eyes",
            "RewardID": summoningRewards[7], "Value8": 54, "Image": "neyeptune", "RewardQTY": 30,
        },
        12: {
            "EnemyID": "ram", "Value2": 37, "Value3": 42, "Value4": 21, "OpponentName": "Shepherd and his Flock of Rams",
            "RewardID": summoningRewards[5], "Value8": 65, "Image": "dedotated-ram", "RewardQTY": 0.3,
        },
        13: {
            "EnemyID": "skele2", "Value2": 33, "Value3": 31, "Value4": 30, "OpponentName": "Brody and his Infamous Bloodbones",
            "RewardID": summoningRewards[11], "Value8": 74, "Image": "bloodbone", "RewardQTY": 15,
        },
    },
    "Purple": {
        0: {
            "EnemyID": "mushP", "Value2": 33, "Value3": 32, "Value4": 16, "OpponentName": "ProXD and his Mushrooms of Mischief",
            "RewardID": summoningRewards[16], "Value8": 33, "Image": "purp-mushroom", "RewardQTY": 50,
        },
        1: {
            "EnemyID": "w4a2", "Value2": 31, "Value3": 36, "Value4": 23, "OpponentName": "Tallie and her Rambunctious TVs",
            "RewardID": summoningRewards[9], "Value8": 36, "Image": "tv", "RewardQTY": 15,
        },
        2: {
            "EnemyID": "w4a3", "Value2": 37, "Value3": 37, "Value4": 21, "OpponentName": "Homer and his Epic Donuts",
            "RewardID": summoningRewards[1], "Value8": 37, "Image": "donut", "RewardQTY": 35,
        },
        3: {
            "EnemyID": "demonP", "Value2": 53, "Value3": 34, "Value4": 31, "OpponentName": "Nostalgo and his Genies of Olde",
            "RewardID": summoningRewards[3], "Value8": 42, "Image": "demon-genie", "RewardQTY": 6,
        },
        4: {
            "EnemyID": "w4b2", "Value2": 28, "Value3": 29, "Value4": 18, "OpponentName": "Dalia and her Hyperactive Drinks",
            "RewardID": summoningRewards[12], "Value8": 43, "Image": "soda-can", "RewardQTY": 2,
        },
        5: {
            "EnemyID": "w4b1", "Value2": 19, "Value3": 23, "Value4": 10, "OpponentName": "Werm and his Worms",
            "RewardID": summoningRewards[6], "Value8": 47, "Image": "flying-worm", "RewardQTY": 35,
        },
        6: {
            "EnemyID": "w4b3", "Value2": 36, "Value3": 36, "Value4": 22, "OpponentName": "JelloL0ver87 and his Beloved Gel Cubes",
            "RewardID": summoningRewards[8], "Value8": 52, "Image": "gelatinous-cuboid", "RewardQTY": 20,
        },
        7: {
            "EnemyID": "w4b4", "Value2": 46, "Value3": 32, "Value4": 28, "OpponentName": "Megacorp Representative and his Product",
            "RewardID": summoningRewards[13], "Value8": 56, "Image": "choccie", "RewardQTY": 15,
        },
        8: {
            "EnemyID": "w4b5", "Value2": 37, "Value3": 33, "Value4": 30, "OpponentName": "Werm's Stepsister and her Worms",
            "RewardID": summoningRewards[1], "Value8": 61, "Image": "biggole-wurm", "RewardQTY": 50,
        },
        9: {
            "EnemyID": "w4c1", "Value2": 26, "Value3": 26, "Value4": 14, "OpponentName": "DQ and their abandoned Clammies",
            "RewardID": summoningRewards[2], "Value8": 62, "Image": "clammie", "RewardQTY": 75,
        },
        10: {
            "EnemyID": "w4c2", "Value2": 19, "Value3": 24, "Value4": 10, "OpponentName": "Dee and her 'dars",
            "RewardID": summoningRewards[4], "Value8": 66, "Image": "octodar", "RewardQTY": 25,
        },
        11: {
            "EnemyID": "w4c3", "Value2": 33, "Value3": 30, "Value4": 24, "OpponentName": "Gordon and his Eloquent Flombeiges",
            "RewardID": summoningRewards[10], "Value8": 70, "Image": "flombeige", "RewardQTY": 5,
        },
        12: {
            "EnemyID": "w4c4", "Value2": 66, "Value3": 39, "Value4": 30, "OpponentName": "Giuseppe and his Power Tools",
            "RewardID": summoningRewards[14], "Value8": 78, "Image": "stilted-seeker", "RewardQTY": 60,
        },

    },
    "Red": {
        0: {
            "EnemyID": "w5a1", "Value2": 24, "Value3": 20, "Value4": 10, "OpponentName": "Jawz and his Hot Smokin Suggmas",
            "RewardID": summoningRewards[17], "Value8": 44, "Image": "suggma", "RewardQTY": 30,
        },
        1: {
            "EnemyID": "w5a2", "Value2": 20, "Value3": 28, "Value4": 12, "OpponentName": "Macdonald and his Homemade Maccies",
            "RewardID": summoningRewards[15], "Value8": 48, "Image": "maccie", "RewardQTY": 10,
        },
        2: {
            "EnemyID": "w5a3", "Value2": 43, "Value3": 36, "Value4": 29, "OpponentName": "Brandon and his Iconic Brightsides",
            "RewardID": summoningRewards[1], "Value8": 53, "Image": "mister-brightside", "RewardQTY": 40,
        },
        3: {
            "EnemyID": "w5a4", "Value2": 30, "Value3": 27, "Value4": 18, "OpponentName": "Lola and her Crazy Crackers",
            "RewardID": summoningRewards[5], "Value8": 55, "Image": "cheese-nub", "RewardQTY": 0.3,
        },
        4: {
            "EnemyID": "w5a5", "Value2": 32, "Value3": 32, "Value4": 28, "OpponentName": "Mr M and his Holey Moleys",
            "RewardID": summoningRewards[11], "Value8": 57, "Image": "stiltmole", "RewardQTY": 25,
        },
        5: {
            "EnemyID": "w5b1", "Value2": 20, "Value3": 27, "Value4": 11, "OpponentName": "The Don's Molto Bene Moltis",
            "RewardID": summoningRewards[16], "Value8": 59, "Image": "molti", "RewardQTY": 90,
        },
        6: {
            "EnemyID": "w5b2", "Value2": 22, "Value3": 27, "Value4": 18, "OpponentName": "Smoggy Shaman and their Scary Bones",
            "RewardID": summoningRewards[7], "Value8": 63, "Image": "purgatory-stalker", "RewardQTY": 30,
        },
        7: {
            "EnemyID": "w5b3", "Value2": 23, "Value3": 24, "Value4": 18, "OpponentName": "Thomas and his Halftime Breakforce",
            "RewardID": summoningRewards[18], "Value8": 69, "Image": "citringe", "RewardQTY": 25,
        },
        8: {
            "EnemyID": "w5b4", "Value2": 28, "Value3": 30, "Value4": 24, "OpponentName": "Larry and his Lava Lamps",
            "RewardID": summoningRewards[9], "Value8": 71, "Image": "lampar", "RewardQTY": 25,
        },
        9: {
            "EnemyID": "w5b5", "Value2": 31, "Value3": 31, "Value4": 28, "OpponentName": "OwO and their Spirit Army",
            "RewardID": summoningRewards[3], "Value8": 75, "Image": "fire-spirit", "RewardQTY": 7,
        },
        10: {
            "EnemyID": "w5b6", "Value2": 34, "Value3": 37, "Value4": 23, "OpponentName": "Briggs and his Mole Workforce",
            "RewardID": summoningRewards[6], "Value8": 79, "Image": "biggole-mole", "RewardQTY": 25,
        },
        11: {
            "EnemyID": "w5c1", "Value2": 21, "Value3": 22, "Value4": 11, "OpponentName": "Krepe and his Crawlies",
            "RewardID": summoningRewards[4], "Value8": 82, "Image": "crawler", "RewardQTY": 15,
        },
        12: {
            "EnemyID": "w5c2", "Value2": 34, "Value3": 25, "Value4": 22, "OpponentName": "Grinder23 and his Favorite Mobs",
            "RewardID": summoningRewards[10], "Value8": 84, "Image": "tremor-wurm", "RewardQTY": 10,
        },
    },
    "Cyan": {
        0: {
            "EnemyID": "w6a1", "Value2": 22, "Value3": 25, "Value4": 16, "OpponentName": "Spiffy Jr and their Whelming Liquids",
            "RewardID": summoningRewards[19], "Value8": 58, "Image": "sprout-spirit", "RewardQTY": 3,
        },
        1: {
            "EnemyID": "w6a2", "Value2": 27, "Value3": 34, "Value4": 19, "OpponentName": "iFarm and their 0cal Units",
            "RewardID": summoningRewards[2], "Value8": 64, "Image": "ricecake", "RewardQTY": 50,
        },
        2: {
            "EnemyID": "w6a3", "Value2": 35, "Value3": 39, "Value4": 27, "OpponentName": "Spiffy Sr and his Bigtime Liquids",
            "RewardID": summoningRewards[8], "Value8": 67, "Image": "river-spirit", "RewardQTY": 20,
        },
        3: {
            "EnemyID": "w6a4", "Value2": 33, "Value3": 27, "Value4": 22, "OpponentName": "Bart and his Trollsquad",
            "RewardID": summoningRewards[12], "Value8": 68, "Image": "baby-troll", "RewardQTY": 2,
        },
        4: {
            "EnemyID": "w6a5", "Value2": 36, "Value3": 35, "Value4": 29, "OpponentName": "Grunkle and their Rooted Whimsy",
            "RewardID": summoningRewards[14], "Value8": 72, "Image": "woodlin-spirit", "RewardQTY": 80,
        },
        5: {
            "EnemyID": "w6b1", "Value2": 46, "Value3": 36, "Value4": 34, "OpponentName": "Barb and her Overworked Blobs",
            "RewardID": summoningRewards[13], "Value8": 73, "Image": "bamboo-spirit", "RewardQTY": 20,
        },
        6: {
            "EnemyID": "w6b2", "Value2": 25, "Value3": 29, "Value4": 22, "OpponentName": "Lumi and her Bright Lights",
            "RewardID": summoningRewards[1], "Value8": 76, "Image": "lantern-spirit", "RewardQTY": 60,
        },
        7: {
            "EnemyID": "w6b3", "Value2": 36, "Value3": 33, "Value4": 26, "OpponentName": "Marge and her Troll Patrol",
            "RewardID": summoningRewards[16], "Value8": 77, "Image": "mama-troll", "RewardQTY": 120,
        },
        8: {
            "EnemyID": "w6b4", "Value2": 45, "Value3": 34, "Value4": 31, "OpponentName": "Lief and his Overzealous Leeks",
            "RewardID": summoningRewards[5], "Value8": 80, "Image": "leek-spirit", "RewardQTY": 0.3,
        },
        9: {
            "EnemyID": "w6c1", "Value2": 29, "Value3": 27, "Value4": 19, "OpponentName": "Seru and their Ceramic Entities",
            "RewardID": summoningRewards[15], "Value8": 81, "Image": "ceramic-spirit", "RewardQTY": 20,
        },
        10: {
            "EnemyID": "w6c2", "Value2": 38, "Value3": 33, "Value4": 27, "OpponentName": "Mr Walker and his Untiring Doggies",
            "RewardID": summoningRewards[17], "Value8": 83, "Image": "skydoggie-spirit", "RewardQTY": 50,
        },
        11: {
            "EnemyID": "w6d1", "Value2": 23, "Value3": 24, "Value4": 14, "OpponentName": "Duke of Yolk and his Subjects",
            "RewardID": summoningRewards[3], "Value8": 85, "Image": "royal-egg", "RewardQTY": 8,
        },
        12: {
            "EnemyID": "w6d2", "Value2": 27, "Value3": 31, "Value4": 16, "OpponentName": "Sorel and her Esteemed Sludge",
            "RewardID": summoningRewards[18], "Value8": 86, "Image": "minichief-spirit", "RewardQTY": 70,
        },
        13: {
            "EnemyID": "w6d3", "Value2": 42, "Value3": 41, "Value4": 32, "OpponentName": "Shinji and his Inevitable Army",
            "RewardID": summoningRewards[20], "Value8": 87, "Image": "samurai-guardian", "RewardQTY": 3,
        },
    },
}
summoning_endlessEnemies = {0: 'rift-spooker', 1: 'rift-slug', 2: 'rift-jocund', 3: 'rift-hivemind', 4: 'rift-stalker'}
summoning_endlessDict = {
    0: {"RewardID": summoningRewards[21], "RewardQTY": 1},
    1: {"RewardID": summoningRewards[22], "RewardQTY": 3},
    2: {"RewardID": summoningRewards[23], "RewardQTY": 1},
    3: {"RewardID": summoningRewards[24], "RewardQTY": 12},
    4: {"RewardID": summoningRewards[25], "RewardQTY": 1},
    5: {"RewardID": summoningRewards[27], "RewardQTY": 7},
    6: {"RewardID": summoningRewards[23], "RewardQTY": 2},
    7: {"RewardID": summoningRewards[22], "RewardQTY": 4},
    8: {"RewardID": summoningRewards[24], "RewardQTY": 15},
    9: {"RewardID": summoningRewards[29], "RewardQTY": 10},
    10: {"RewardID": summoningRewards[25], "RewardQTY": 1},
    11: {"RewardID": summoningRewards[26], "RewardQTY": 4},
    12: {"RewardID": summoningRewards[24], "RewardQTY": 18},
    13: {"RewardID": summoningRewards[23], "RewardQTY": 2},
    14: {"RewardID": summoningRewards[22], "RewardQTY": 4},
    15: {"RewardID": summoningRewards[32], "RewardQTY": 3},
    16: {"RewardID": summoningRewards[30], "RewardQTY": 20},
    17: {"RewardID": summoningRewards[31], "RewardQTY": 25},
    18: {"RewardID": summoningRewards[25], "RewardQTY": 2},
    19: {"RewardID": summoningRewards[24], "RewardQTY": 20},
    20: {"RewardID": summoningRewards[26], "RewardQTY": 5},
    21: {"RewardID": summoningRewards[29], "RewardQTY": 30},
    22: {"RewardID": summoningRewards[24], "RewardQTY": 24},
    23: {"RewardID": summoningRewards[22], "RewardQTY": 4},
    24: {"RewardID": summoningRewards[21], "RewardQTY": 1},
    25: {"RewardID": summoningRewards[23], "RewardQTY": 2},
    26: {"RewardID": summoningRewards[31], "RewardQTY": 2},
    27: {"RewardID": summoningRewards[28], "RewardQTY": 35},
    28: {"RewardID": summoningRewards[27], "RewardQTY": 9},
    29: {"RewardID": summoningRewards[24], "RewardQTY": 26},
    30: {"RewardID": summoningRewards[26], "RewardQTY": 5},
    31: {"RewardID": summoningRewards[22], "RewardQTY": 5},
    32: {"RewardID": summoningRewards[30], "RewardQTY": 40},
    33: {"RewardID": summoningRewards[25], "RewardQTY": 1},
    34: {"RewardID": summoningRewards[29], "RewardQTY": 45},
    35: {"RewardID": summoningRewards[28], "RewardQTY": 50},
    36: {"RewardID": summoningRewards[23], "RewardQTY": 2},
    37: {"RewardID": summoningRewards[26], "RewardQTY": 6},
    38: {"RewardID": summoningRewards[24], "RewardQTY": 30},
    39: {"RewardID": summoningRewards[32], "RewardQTY": 3},
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
summoningBattleCountsDict["Normal"] = sum(summoningBattleCountsDict.values())
max_summoning_upgrades = 70  #Last verified as of 2.22 The Fixening

###Master Classes###
# Last pulled from GrimoireUpg function in v2.26
grimoire_upgrades_list = ["Wraith_Damage_製_(Tap_for_more_info) 8 1.10 0 999999 1 0 0 0 +{_Base_Damage_in_Wraith_Form".split(" "), "Wraith_Accuracy 8 1.04 0 999999 1 1 0 0 +{_Base_Accuracy_in_Wraith_Form".split(" "), "Wraith_Defence 9 1.10 0 999999 1 5 0 0 +{_Base_Defence_in_Wraith_Form".split(" "), "Wraith_Health 10 1.07 0 999999 1 10 0 0 +{_Base_HP_in_Wraith_Form".split(" "), "Ribbon_Shelf 1000 1.30 0 1 1 25 0 0 Unlocks_Ribbons_for_Meals,_found_at_Le_Menu_in_W4".split(" "), "Ribbon_Winning_製 50 1.60 0 50 1 26 0 0 Get_+1_Daily_Ribbon,_+{%_chance_for_rare_quality".split(" "), "Wraith_Damage_II 25 1.11 0 999999 3 80 0 0 +{_Base_Damage_in_Wraith_Form".split(" "), "Wraith_of_all_Trades 50 1.18 0 999999 1 125 0 0 +{%_Accuracy,_Defence,_and_HP_in_Wraith_Form".split(" "), "Wraith_Destruction 70 1.15 0 999999 1 155 0 0 +{%_Total_Damage_in_Wraith_Form".split(" "), "Land_Rank_Database_Maxim 100 10 0 10 1 190 0 0 +{_Max_LV_for_5th_column_Land_Rank_upgrades".split(" "), "Wraith_Crits 150 1.25 0 40 1 220 0 0 +{%_Crit_Chance_in_Wraith_Form".split(" "), "Pure_Opals 1500 1.8 1 25 1 255 0 0 +{_Opals_to_give_to_your_Villagers_in_World_5".split(" "), "Wraith_Accuracy_II 200 1.06 0 999999 3 290 0 0 +{_Base_Accuracy_in_Wraith_Form".split(" "), "Knockout!_(#)_製 450 1.45 1 999999 1 330 0 0 +{%_Wraith_DMG_per_KO!_Target:$".split(" "), "Sacrifice_of_Harvest 300 1.04 0 999999 5 380 0 0 }x_higher_Crop_Evo_chance".split(" "), "Wraith_Defence_II 500 1.12 1 999999 1 425 0 0 +{_Base_Defence_in_Wraith_Form".split(" "), "Wraith_Damage_III 750 1.12 1 999999 15 470 0 0 +{_Base_Damage_in_Wraith_Form".split(" "), "Grey_Tome_Book 2000 1.25 1 150 1 500 0 0 }x_higher_bonuses_from_the_Tome".split(" "), "Femur_Hoarding 3500 1.15 1 999999 2 550 0 0 +{%_Wraith_DMG_per_POW_10_Femurs_owned".split(" "), "Wraith_Health_II 4000 1.07 1 999999 2 650 0 0 +{_Base_HP_in_Wraith_Form".split(" "), "Wraith_Strikeforce 5800 1.15 1 999999 2 770 0 0 +{%_Crit_DMG_in_Wraith_Form".split(" "), "Elimination!_(#)_製 6250 1.45 1 999999 1 900 0 0 +{%_Wraith_DMG_per_elim!_Target:$".split(" "), "Superior_Crop_Research 7500 1.25 0 200 1 1050 0 0 }x_higher_bonuses_from_the_Crop_Scientist".split(" "), "Bones_o'_Plenty 8000 1.20 1 999999 2 1250 0 0 +{%_Extra_Bones".split(" "), "Skull_of_Major_Experience_製 8500 1.03 1 999999 8 1475 0 0 +{%_Class_EXP_bonus_for_all_characters,_always!".split(" "), "Wraith_Accuracy_III 10500 1.07 2 999999 5 1700 0 0 +{_Base_Accuracy_in_Wraith_Form".split(" "), "Supreme_Head_Chef_Status 11000 1.40 1 20 1 1900 0 0 +{_Max_LV_for_all_Meals._Go_max_them!".split(" "), "Ribcage_Hoarding 12000 1.20 0 999999 1 2150 0 0 +{%_Wraith_DEF_per_POW_10_Ribcages_owned".split(" "), "Wraith_Destruction_II 13900 1.17 1 999999 3 2300 0 0 +{%_Total_Damage_in_Wraith_Form".split(" "), "Villager_Extraciricular 15000 1.15 2 999999 1 2500 0 0 }x_Villager_EXP_gain_in_World_5".split(" "), "Wraith_Defence_III 14500 1.11 2 999999 2 2800 0 0 +{_Base_Defence_in_Wraith_Form".split(" "), "Annihilation!_(#)_製 16500 1.55 2 999999 1 2900 0 0 +{%_Wraith_DMG_per_stack!_Target:$".split(" "), "Talents_for_Me,_not_for_Thee 18000 1.10 2 200 1 3150 0 0 +{_Talent_PTS_for_the_Death_Bringer_class_only".split(" "), "Wraith_Damage_IV 19750 1.13 2 999999 50 3300 0 0 +{_Base_Damage_in_Wraith_Form".split(" "), "Wraith_Health_III 21500 1.07 2 999999 3 3500 0 0 +{_Base_HP_in_Wraith_Form".split(" "), "Skull_of_Major_Damage_製 23000 1.04 2 999999 3 3750 0 0 +{%_Total_DMG_bonus_for_all_characters,_always!".split(" "), "Writhing_Grimoire 27000 1.20 1 50 1 4100 0 0 }x_higher_bonuses_from_most_Grimoire_upgrades".split(" "), "Wraith_Accuracy_IV 34000 1.08 2 999999 5 4200 0 0 +{_Base_Accuracy_in_Wraith_Form".split(" "), "Wraith_of_all_Trades_II 42000 1.06 3 999999 1 4500 0 0 +{%_Accuracy,_Defence,_and_HP_in_Wraith_Form".split(" "), "Skull_of_Major_Talent_製 50000 1.65 3 30 1 4600 0 0 +{_Talent_LVs_for_all_characters,_always!".split(" "), "Wraith_Defence_IV 57000 1.13 3 999999 3 4800 0 0 +{_Base_Defence_in_Wraith_Form".split(" "), "Cranium_Hoarding 63000 1.07 3 999999 1 5000 0 0 +{%_Wraith_Accuracy_per_POW_10_Craniums_owned".split(" "), "Wraith_Health_IV 75000 1.09 3 999999 5 5200 0 0 +{_Base_HP_in_Wraith_Form".split(" "), "Wraith_Destruction_III 85000 1.17 3 999999 5 5400 0 0 +{%_Total_Damage_in_Wraith_form".split(" "), "Skull_of_Major_Droprate_製 100000 1.08 3 999999 1 5600 0 0 +{%_Drop_Rate_bonus_for_all_characters,_always!".split(" "), "Ok_fine,_Talents_for_Thee_too 120000 1.15 3 999999 1 5850 0 0 +{_Talent_PTS_for_all_other_Master_Classes".split(" "), "Wraith_Damage_V 150000 1.15 2 999999 1 6200 0 0 +{_Base_Damage_in_Wraith_Form".split(" "), "Wraith_Accuracy_V 200000 1.10 2 999999 1 6500 0 0 +{_Base_Accuracy_in_Wraith_Form".split(" "), "Bovinae_Hoarding 300000 1.35 2 999999 1 6800 0 0 +{%_Extra_Bones_per_POW_10_Bovinae_owned".split(" "), "Wraith_Defence_V 500000 1.15 3 999999 1 7100 0 0 +{_Base_Defence_in_Wraith_Form".split(" "), "Wraith_Destruction_IV 600000 1.18 3 999999 8 7200 0 0 +{%_Total_Damage_in_Wraith_Form".split(" "), "Death_of_the_Atom_Price 750000 1.15 3 999999 1 7500 0 0 All_Atoms_are_+{%_cheaper_to_upgrade".split(" "), "Ripped_Page 1999999999 99999 1 1 1 7600 0 0 These_pages_are_missing...".split(" "), "Ripped_Page 1999999999 99999 1 1 1 7700 0 0 These_pages_are_missing...".split(" "), "Ripped_Page 1999999999 99999 1 1 1 7800 0 0 These_pages_are_missing...".split(" ")]
grimoire_dont_scale = [9, 11, 26, 36, 39, 17, 32, 45]  # Pulled from the start of GrimoireUpgBonus under _customBlock_Summoning in v2.27
grimoire_bones_list = ['Femurs', 'Ribcages', 'Craniums', 'Bovinae']
grimoire_stack_types = ['Knockout', 'Elimination', 'Annihiliation']

# Last pulled from RANDOlist[140] function in v2.26
grimoire_coded_stack_monster_order = "mushG frogG beanG slimeG snakeG carrotO goblinG plank frogBIG branch acorn jarSand mimicA crabcake coconut sandcastle pincermin poopSmall ratB potato steak moonman sandgiant snailZ sheep flake stache bloque mamoth snowball penguin thermostat glass snakeB speaker eye ram mushP w4a2 w4a3 demonP w4b2 w4b1 w4b3 w4b4 w4b5 w4c1 w4c2 w4c3 w4c4 w5a1 w5a2 w5a3 w5a4 w5a5 w5b1 w5b2 w5b3 w5b4 w5b5 w5b6 w5c1 w5c2 w5b6 w6a1 w6a2 w6a3 w6a4 w6a5 w6b1 w6b2 w6b3 w6b4 w6c1 w6c2 w6d1 w6d2 w6d3".split(" ")

# Last pulled from UpgradeVault function in v2.28 Valenslimes
vault_upgrades_list = ["Bigger_Damage 8 1.025 0 500 1 0 0 0 +{_Damage._Monsters_hate_this_upgrade! _".split(" "), "Natural_Talent_製_(Tap_for_Info) 14 1.15 0 200 1 7 0 0 +{_Talent_Points._Go_spend_them! _".split(" "), "Monster_Tax 10 1.05 0 500 2 13 0 0 +{%_Coins_dropped_by_Monsters. _".split(" "), "Wicked_Smart 15 1.20 0 500 2 36 0 0 +{%_Class_EXP_Gain. Leveling_up_gives_you_Talent_Pts!".split(" "), "Bullseye_製 25 1.15 0 200 1 54 0 0 +{_Accuracy._Useful_when_you_start_missing! _".split(" "), "Steel_Guard 40 1.30 0 100 1 65 0 0 +{_Defence._Useful_when_monsters_start_hurting! _".split(" "), "Evolving_Talent_製 60 1.18 0 200 1 75 0 0 +{_Talent_Points_for_Warrior,_Archer,_and_Mage! _".split(" "), "Massive_Whirl 777 1.10 0 1 2 83 0 0 Whirl_is_2x_as_big_and_can_hit_+{_more_monsters! _".split(" "), "Rapid_Arrows 777 1.10 0 1 1 85 0 0 Piercing_Arrow_fires_double_arrows! _".split(" "), "Dual_Fireballs 777 1.10 0 1 1 87 0 0 Fireball_casts_in_both_directions_at_the_same_time! _".split(" "), "Weapon_Craft_製 150 7.5 0 5 10 100 0 0 All_crafted_weapons_give_+{%_more_damage. Go_craft_a_new_weapon_at_the_Anvil_in_town!".split(" "), "Mining_Payday_製 200 1.28 1 40 2 115 0 0 +{%_Coins_per_POW_10_ores_mined. Go_make_a_2nd_player_to_go_mining_for_you!".split(" "), "Baby_on_Board_製 250 1.08 0 50 2 130 0 0 +{%_Class_EXP_Gain_for_your_Lowest_LV_Player _".split(" "), "Major_Discount 300 1.30 0 80 1 175 0 0 All_upgrades_in_the_Vault_are_{%_cheaper _".split(" "), "Bored_to_Death_製 300 4.50 1 10 5 190 0 0 +{%_Coins_from_Monsters_per_POW_10_Bean_Kills. _".split(" "), "Knockout!_製 1000 6 1 5 1 220 0 0 +{%_Total_Damage_per_Knockout! Current_Target:&____".split(" "), "Stamp_Bonanza 500 1.20 1 100 2 275 0 0 }x_higher_bonuses_from_Sword,_Heart, Target,_and_Shield_Stamps".split(" "), "Carry_Capacity_製 650 1.35 1 100 5 300 0 0 Can_carry_+{_more_resources_per_slot! Craft_Bags_at_the_anvil_to_boost_this_way_more!".split(" "), "Drops_for_Days 700 1.17 1 50 1 345 0 0 +{%_Drop_Rarity,_also_known_by_the IdleOn_community_as_Drop_Rate,_or_DR".split(" "), "Happy_Doggy_製 800 1.25 1 100 2 350 0 0 +{%_Dog_Happiness _".split(" "), "Slice_N_Dice_製 900 1.10 1 100 2 370 0 0 +{_Base_Damage_per_POW_10_Carrot_Kills. _".split(" "), "Go_Go_Secret_Owl_製 400 1.10 0 100 5 410 0 0 +{%_Feathers/sec_for_Orion_the_Horned_Owl _".split(" "), "Boss_Decimation 1150 1.12 1 25 1 460 0 0 +{%_Boss_Damage _".split(" "), "Sleepy_Time 1200 1.55 0 20 1 520 0 0 +{%_AFK_Gains_for_Fighting_and_Skilling _".split(" "), "Production_Revolution_製 1300 1.15 1 100 5 580 0 0 +{%_faster_Anvil_Production _".split(" "), "Statue_Bonanza 1500 1.28 1 50 2 630 0 0 }x_higher_bonuses_from_Power,_Speed, Mining,_and_Lumberbob_Statues".split(" "), "Beeg_Forge 1600 1.15 2 100 5 690 0 0 +{%_higher_Forge_Capacity _".split(" "), "Stick_Snapping_製 1800 1.13 1 50 1 750 0 0 +{%_Total_Damage_per_POW_10_Branch_Kills. _".split(" "), "Liquid_Knowledge 2000 1.06 0 100 1 830 0 0 +{%_Alchemy_EXP_Gain _".split(" "), "Bug_Knowledge 2100 1.06 1 100 1 910 0 0 +{%_Catching_EXP_Gain _".split(" "), "Fish_Knowledge 2200 1.06 2 100 1 1000 0 0 +{%_Fishing_EXP_Gain _".split(" "), "Dirty_Money_製 3000 1.10 2 25 2 1200 0 0 +{%_Coins_from_Monsters_per_POW_10_Poop_Kills _".split(" "), "Vault_Mastery 10000 1.65 2 50 1 1500 0 0 }x_higher_bonuses_from_most_Vault_Upgrades _".split(" ")]
vault_dont_scale = [1, 6, 7, 8, 9, 13, 32, 999]  # Pulled from the start of VaultUpgBonus under _customBlock_Summoning in v2.27
vault_stack_types = ['Knockout']

def decode_enemy_name(coded_name: str) -> str:
    decoded_name = coded_name  #In the event it isn't found, return the coded name
    for card_set in card_data:
        if coded_name in card_data[card_set]:
            #logger.debug(f"Target found! {coded_name} = {card_data[card_set][coded_name][0]}")
            decoded_name = f"{card_data[card_set][coded_name][0]}"
    if decoded_name == coded_name:
        logger.warning(f"Could not find decoded name for {coded_name}")
    return decoded_name

#logger.debug(f"{grimoire_decoded_stack_monster_order}")
###SLAB CONSTS###
#SlabItemSort last pulled from code in 2.28 Valenslimes
slabList = "Copper Iron Gold Plat Dementia Void Lustre Starfire Marble Dreadlo Godshard Motherlode CopperBar IronBar GoldBar PlatBar DementiaBar VoidBar LustreBar StarfireBar MarbleBar DreadloBar GodshardBar OakTree BirchTree JungleTree ForestTree ToiletTree PalmTree StumpTree SaharanFoal Tree7 AlienTree Tree8 Tree9 Tree11 Tree10 Tree12 Tree13 MotherlodeTREE Leaf1 Leaf2 Leaf3 Leaf4 Leaf5 Leaf6 Fish1 Fish2 Fish3 Fish4 Fish5 Fish6 Fish7 Fish8 Fish9 Fish10 Fish11 Fish12 Fish13 Fish14 Bug1 Bug2 Bug3 Bug4 Bug5 Bug6 Bug7 Bug8 Bug9 Bug11 Bug10 Bug12 Bug13 Bug14 Critter1 Critter1A Critter2 Critter2A Critter3 Critter3A Critter4 Critter4A Critter5 Critter5A Critter6 Critter6A Critter7 Critter7A Critter8 Critter8A Critter9 Critter9A Critter10 Critter10A Critter11 Critter11A Soul1 Soul2 Soul3 Soul4 Soul5 Soul6 Soul7 Refinery1 Refinery2 Refinery3 Refinery4 Refinery5 Refinery6 CraftMat1 CraftMat2 CraftMat3 CraftMat5 CraftMat6 CraftMat7 CraftMat9 CraftMat8 CraftMat10 CraftMat11 CraftMat12 CraftMat13 CraftMat14 OilBarrel1 OilBarrel2 OilBarrel3 OilBarrel4 OilBarrel5 OilBarrel6 OilBarrel7 PureWater PureWater2 Grasslands1 Grasslands2 Grasslands3 Grasslands4 Jungle1 Jungle2 Jungle3 Forest1 Forest2 Forest3 Sewers1 Sewers1b Sewers2 Sewers3 TreeInterior1 TreeInterior1b TreeInterior2 DesertA1 DesertA1b DesertA2 DesertA3 DesertA3b DesertB1 DesertB2 DesertB3 DesertB4 DesertC1 DesertC2 DesertC2b DesertC3 DesertC4 SnowA1 SnowA2 SnowA2a SnowA3 SnowA4 SnowB1 SnowB2 SnowB2a SnowB5 SnowB3 SnowB4 SnowC1 SnowC2 SnowC3 SnowC4 SnowC4a SnowC5 GalaxyA1 GalaxyA2 GalaxyA2b GalaxyA3 GalaxyA4 GalaxyB1 GalaxyB2 GalaxyB3 GalaxyB4 GalaxyB5 GalaxyC1 GalaxyC1b GalaxyC2 GalaxyC3 GalaxyC4 LavaA1 LavaA1b LavaA2 LavaA3 LavaA4 LavaA5 LavaA5b LavaB1 LavaB2 LavaB3 LavaB3b LavaB4 LavaB5 LavaB6 LavaC1 LavaC2 SpiA1 SpiA2 SpiA2b SpiA3 SpiA4 SpiA5 SpiB1 SpiB2 SpiB2b SpiB3 SpiB4 SpiC1 SpiC2 SpiD1 SpiD2 SpiD3 BabaYagaETC Hgg Quest17 Quest29 EfauntDrop1 EfauntDrop2 Chiz0 Chiz1 TrollPart KrukPart KrukPart2 EquipmentHats11 EquipmentHats12 EquipmentHats13 EquipmentHats14 EquipmentHats1 EquipmentHats15 EquipmentHats17 EquipmentHats20 EquipmentHats3 EquipmentHats16 EquipmentHats21 EquipmentHats18 EquipmentHats22 EquipmentHats28 EquipmentHats19 TestObj13 EquipmentHats41 EquipmentHats26 EquipmentHats52 EquipmentHats53 EquipmentHats54 EquipmentHats61 EquipmentHats58 EquipmentHats59 EquipmentHats60 EquipmentHats68 EquipmentHats70 EquipmentHats71 EquipmentHats74 EquipmentHats77 EquipmentHats83 EquipmentHats105 EquipmentHats106 EquipmentHats5 EquipmentHats6 EquipmentHats7 EquipmentHats8 EquipmentHats9 EquipmentHats10 EquipmentHats4Choppin EquipmentHats25 EquipmentHats107 EquipmentHats29 EquipmentHats39 EquipmentHats27 EquipmentHats30 EquipmentHats44 EquipmentHats2 EquipmentHats67 EquipmentHats64 EquipmentHats66 EquipmentHats79 EquipmentHats73 EquipmentHats51 EquipmentHatsBeg1 EquipmentHats56 EquipmentHats63 EquipmentHats85 EquipmentHats86 EquipmentHats87 EquipmentHats88 EquipmentHats42 EquipmentHats69 EquipmentHats108 EquipmentHats55 EquipmentHats75 EquipmentHats76 EquipmentHats65 EquipmentHats80 EquipmentHats81 EquipmentHats82 EquipmentHats78 EquipmentHats35 EquipmentHats38 EquipmentHats47 EquipmentHats48 EquipmentHats46 EquipmentHats33 EquipmentHats49 EquipmentHats50 EquipmentHats110 EquipmentHats113 EquipmentHats57 EquipmentHats45 EquipmentHats62 EquipmentHats32 EquipmentHats37 EquipmentHats89 EquipmentHats34 EquipmentHats109 EquipmentHats84 EquipmentHats31 EquipmentHats111 EquipmentHats112 EquipmentHats90 EquipmentHats91 EquipmentHats92 EquipmentHats93 EquipmentHats94 EquipmentHats95 EquipmentHats96 EquipmentHats97 EquipmentHats98 EquipmentHats99 EquipmentHats100 EquipmentHats101 EquipmentHats102 EquipmentHats103 EquipmentHats104 EquipmentPunching1 EquipmentPunching2 EquipmentPunching3 EquipmentPunching4 EquipmentPunching5 EquipmentPunching6 EquipmentPunching7 EquipmentPunching8 EquipmentPunching9 EquipmentPunching10 EquipmentPunching11 TestObj1 TestObj7 TestObj3 EquipmentSword1 EquipmentSword2 EquipmentSword3 EquipmentSword4 EquipmentSword5 EquipmentSword6 EquipmentSword7 EquipmentSword8 EquipmentSword9 EquipmentBows1 EquipmentBows3 EquipmentBows4 EquipmentBows5 EquipmentBows6 EquipmentBows7 EquipmentBows8 EquipmentBows9 EquipmentBows10 EquipmentBows11 EquipmentBows12 EquipmentBows13 EquipmentBows14 EquipmentWands1 EquipmentWands2 EquipmentWands5 EquipmentWands6 EquipmentWands3 EquipmentWands7 EquipmentWands8 EquipmentWands9 EquipmentWands10 EquipmentWands11 EquipmentWands12 EquipmentWands13 EquipmentShirts1 EquipmentShirts17 EquipmentShirts19 EquipmentShirts20 EquipmentShirts24 EquipmentShirts25 EquipmentShirts2 EquipmentShirts16 EquipmentShirts3 EquipmentShirts21 EquipmentShirts10 EquipmentShirts11 EquipmentShirts12 EquipmentShirts13 EquipmentShirts18 EquipmentShirts14 EquipmentShirts5 EquipmentShirts23 EquipmentShirts22 EquipmentShirts15 EquipmentShirts26 EquipmentShirts27 EquipmentShirts31 EquipmentShirts28 EquipmentShirts29 EquipmentShirts30 EquipmentShirts6 EquipmentShirts32 EquipmentShirts33 EquipmentShirts34 EquipmentShirts35 EquipmentShirts36 EquipmentShirts37 EquipmentShirts38 EquipmentPants1 EquipmentPants2 EquipmentPants3 EquipmentPants4 EquipmentPants17 EquipmentPants5 EquipmentPants6 EquipmentPants20 EquipmentPants21 EquipmentPants10 EquipmentPants15 EquipmentPants16 EquipmentPants18 EquipmentPants19 EquipmentPants22 EquipmentPants23 EquipmentPants9 EquipmentPants24 EquipmentPants25 EquipmentPants8 EquipmentPants26 EquipmentPants27 EquipmentPants29 EquipmentPants30 EquipmentShoes1 EquipmentShoes9 EquipmentShoes15 EquipmentShoes3 EquipmentShoes20 EquipmentShoes4 EquipmentShoes5 EquipmentShoes21 EquipmentShoes22 EquipmentShoes7 EquipmentShoes16 EquipmentShoes17 EquipmentShoes18 EquipmentShoes19 EquipmentShoes2 EquipmentShoes23 EquipmentShoes26 EquipmentShoes27 EquipmentShoes28 EquipmentShoes29 EquipmentShoes30 EquipmentShoes31 EquipmentShoes32 EquipmentShoes33 EquipmentShoes39 EquipmentShoes24 EquipmentShoes25 EquipmentShoes34 EquipmentShoes35 EquipmentShoes36 EquipmentShoes37 EquipmentShoes38 EquipmentPendant9 EquipmentPendant32 EquipmentPendant10 EquipmentPendant11 EquipmentPendant12 EquipmentPendant14 EquipmentPendant16 EquipmentPendant17 EquipmentPendant18 EquipmentPendant19 EquipmentPendant20 EquipmentPendant21 EquipmentPendant22 EquipmentPendant23 EquipmentPendant24 EquipmentPendant25 EquipmentPendant26 EquipmentPendant27 EquipmentPendant28 EquipmentPendant31 EquipmentPendant29 EquipmentPendant30 EquipmentRings2 EquipmentRings3 EquipmentRings6 EquipmentRings7 EquipmentRings11 EquipmentRings12 EquipmentRings13 EquipmentRings14 EquipmentRings15 EquipmentRings16 EquipmentRings21 EquipmentRings20 EquipmentRings19 EquipmentRingsFishing1 EquipmentRingsFishing2 EquipmentRingsFishing3 EquipmentRings22 EquipmentRings18 EquipmentRings36 EquipmentRings23 EquipmentRings24 EquipmentRings25 EquipmentRings26 EquipmentRings27 EquipmentRings28 EquipmentRings29 EquipmentRings35 EquipmentRings30 EquipmentRings33 EquipmentRings31 EquipmentRings32 EquipmentRings34 EquipmentRingsChat10 EquipmentRingsChat1 EquipmentRingsChat2 EquipmentRingsChat3 EquipmentRingsChat4 EquipmentRingsChat5 EquipmentRingsChat11 EquipmentRingsChat9 EquipmentRingsChat6 EquipmentCape0 EquipmentCape2 EquipmentCape3 EquipmentCape4 EquipmentCape5 EquipmentCape6 EquipmentCape7 EquipmentCape8 EquipmentCape9 EquipmentCape10 EquipmentCape11 EquipmentCape12 EquipmentCape13 EquipmentCape14 EquipmentCape15 EquipmentCape16 EquipmentKeychain0 EquipmentKeychain1 EquipmentKeychain2 EquipmentKeychain3 EquipmentKeychain4 EquipmentKeychain5 EquipmentKeychain6 EquipmentKeychain7 EquipmentKeychain8 EquipmentKeychain9 EquipmentKeychain10 EquipmentKeychain11 EquipmentKeychain12 EquipmentKeychain13 EquipmentKeychain14 EquipmentKeychain15 EquipmentKeychain16 EquipmentKeychain17 EquipmentKeychain18 EquipmentKeychain19 EquipmentKeychain20 EquipmentKeychain21 EquipmentKeychain22 EquipmentKeychain23 EquipmentKeychain24 EquipmentKeychain25 EquipmentKeychain26 EquipmentKeychain27 EquipmentKeychain28 EquipmentKeychain29 Trophy1 Trophy2 Trophy3 Trophy5 Trophy6 Trophy7 Trophy8 Trophy9 Trophy10 Trophy11 Trophy12 Trophy13 Trophy14 Trophy15 Trophy16 Trophy17 Trophy18 Trophy19 Trophy20 Trophy21 Trophy22 EquipmentNametag1 EquipmentNametag3 EquipmentNametag4 EquipmentNametag5 EquipmentNametag6b EquipmentNametag7 EquipmentNametag8 EquipmentNametag9 EquipmentNametag10 EquipmentNametag11 EquipmentNametag12 EquipmentNametag13 EquipmentNametag14 EquipmentNametag15 EquipmentGown1 EquipmentTools1 EquipmentTools2 EquipmentTools3 EquipmentTools5 EquipmentTools6 EquipmentTools7 EquipmentTools11 EquipmentTools8 EquipmentTools12 EquipmentTools9 EquipmentTools14 EquipmentTools15 EquipmentTools10 EquipmentTools13 EquipmentToolsHatchet0 EquipmentToolsHatchet3 EquipmentToolsHatchet1 EquipmentToolsHatchet2b EquipmentToolsHatchet2 EquipmentToolsHatchet4 EquipmentToolsHatchet5 EquipmentToolsHatchet7 EquipmentToolsHatchet6 EquipmentToolsHatchet8 EquipmentToolsHatchet9 EquipmentToolsHatchet12 EquipmentToolsHatchet10 EquipmentToolsHatchet11 FishingRod2 FishingRod3 FishingRod4 FishingRod5 FishingRod6 FishingRod7 FishingRod8 FishingRod9 FishingRod10 FishingRod11 FishingRod12 CatchingNet2 CatchingNet3 CatchingNet4 CatchingNet5 CatchingNet6 CatchingNet7 CatchingNet8 CatchingNet9 CatchingNet10 CatchingNet11 CatchingNet12 TrapBoxSet1 TrapBoxSet2 TrapBoxSet3 TrapBoxSet4 TrapBoxSet5 TrapBoxSet6 TrapBoxSet7 TrapBoxSet8 TrapBoxSet9 TrapBoxSet10 WorshipSkull1 WorshipSkull2 WorshipSkull3 WorshipSkull4 WorshipSkull5 WorshipSkull6 WorshipSkull7 WorshipSkull8 WorshipSkull9 WorshipSkull10 WorshipSkull11 DNAgun0 DNAgun1 DNAgun2 DNAgun3 FoodHealth1 FoodHealth3 FoodHealth2 Peanut FoodHealth4 FoodHealth6 FoodHealth7 FoodHealth10 FoodHealth9 FoodHealth11 FoodHealth13 FoodHealth12 FoodHealth14 FoodHealth15 FoodHealth16 FoodHealth17 FoodHealth5 FoodEvent8 Meatloaf FoodPotOr1 FoodPotOr2 FoodPotOr3 FoodPotOr4 FoodPotRe1 FoodPotRe2 FoodPotRe3 FoodPotRe4 FoodPotGr1 FoodPotGr2 FoodPotGr3 FoodPotGr4 FoodEvent7 FoodPotMana1 FoodPotMana2 FoodPotMana3 FoodPotMana4 FoodPotYe1 FoodPotYe2 FoodPotYe3 FoodPotYe4 FoodPotYe5 FoodEvent6 Pearl3 FoodMining1 FoodEvent1 Pearl2 FoodChoppin1 FoodEvent2 FoodFish1 FoodEvent3 Pearl1 FoodCatch1 FoodEvent4 FoodTrapping1 FoodWorship1 Bullet BulletB Bullet3 MidnightCookie FoodEvent5 PeanutG FoodG1 FoodG2 FoodG3 FoodG4 FoodG5 FoodG6 FoodG7 FoodG8 FoodG9 FoodG10 FoodG11 FoodG12 FoodG13 ButterBar rtt0 ResetFrag ResetCompleted ResetCompletedS ClassSwap ClassSwapB ResetBox Ht StonePremRestore StonePremStatswap Key1 Key2 Key3 Key4 Key5 TixCol SilverPen PremiumGem TalentPoint1 TalentPoint2 TalentPoint3 TalentPoint4 TalentPoint5 TalentPoint6 Gfoodcoupon ItemsCoupon1 ItemsCoupon2 ExpBalloon1 ExpBalloon2 ExpBalloon3 Pearl4 Pearl6 Pearl5 Quest30 Quest35 Quest36 Quest38 Quest39 Quest40 Quest42 Quest43 Quest44 Quest49 Quest50 Quest70 Quest71 Quest72 Quest73 Quest90 Quest75 Quest85 Quest88 Quest89 Quest91 Quest92 Quest76 Quest77 Quest79 Quest80 GemP30 Quest81 Quest82 Timecandy1 Timecandy2 Timecandy3 Timecandy4 Timecandy5 Timecandy6 Timecandy7 Timecandy8 Timecandy9 StoneWe StoneWeb StoneW1 StoneW2 StoneW3 StoneW3b StoneW6 StoneW4 StoneW5 StoneW7 StoneW8 StoneAe StoneAeB StoneA1 StoneA1b StoneA2 StoneA2b StoneA3 StoneA3b StoneA4 StoneA5 StoneA6 StoneA7 StoneTe StoneT1 StoneT1e StoneT1eb StoneT2 StoneT3 StoneT4 StoneT5 StoneT6 StoneT7 StoneHelm1 StoneHelm6 StoneHelm1b StoneHelm7 StoneZ1 StoneZ2 StoneZ3 StoneZ4 StonePremSTR StonePremAGI StonePremWIS StonePremLUK JobApplication SmithingHammerChisel SmithingHammerChisel2 SmithingHammerChisel3 BobJoePickle BallJoePickle BoneJoePickle Quest1 Crystal1 Crystal2 Crystal3 Crystal4 Crystal5 PeanutS Quest3 Quest4 Mayo Trash Trash2 Trash3 Quest5 Quest6 Quest7 Quest10 Quest11 Quest12 Quest13 Quest14 Quest15 Quest16 Quest18 Quest19 Quest20 Quest21 Quest22 Quest23 Quest24 Quest25 Quest26 Quest27 GoldricP1 GoldricP2 GoldricP3 Cutter Quest32 Quest33 Quest34 Quest37 Quest41 Quest45 Quest46 Quest47 Quest48 Quest28 Island1 Island0 Quest86 Quest87 Quest93 Quest51 Quest52 PalmTreeD Quest53 Quest54 Quest55 Quest56 Quest57 Quest58 Quest59 Quest60 Quest61 Quest62 Quest63 Quest64 Quest65 Quest66 Quest67 Whetstone Quest68 Quest69 Quest74 Quest78 Quest83 Quest84 Bone0 Bone1 Bone2 Bone3 BadgeG1 BadgeG2 BadgeG3 BadgeD1 BadgeD2 BadgeD3 NPCtoken1 NPCtoken2 NPCtoken3 NPCtoken5 NPCtoken6 NPCtoken4 NPCtoken9 NPCtoken10 NPCtoken11 NPCtoken13 NPCtoken7 Quest9 NPCtoken15 NPCtoken12 NPCtoken14 NPCtoken16 NPCtoken17 NPCtoken18 NPCtoken19 NPCtoken20 NPCtoken21 NPCtoken27 NPCtoken22 NPCtoken24 NPCtoken25 NPCtoken26 NPCtoken23 NPCtoken28 NPCtoken29 NPCtoken30 NPCtoken31 NPCtoken32 NPCtoken33 NPCtoken34 NPCtoken35 NPCtoken36 NPCtoken37 NPCtoken38 NPCtoken39 NPCtoken40 NPCtoken41 BadgeI1 BadgeI2 BadgeI3 EquipmentStatues1 EquipmentStatues2 EquipmentStatues3 EquipmentStatues4 EquipmentStatues5 EquipmentStatues6 EquipmentStatues7 EquipmentStatues8 EquipmentStatues9 EquipmentStatues10 EquipmentStatues11 EquipmentStatues12 EquipmentStatues13 EquipmentStatues14 EquipmentStatues15 EquipmentStatues16 EquipmentStatues17 EquipmentStatues18 EquipmentStatues19 EquipmentStatues20 EquipmentStatues21 EquipmentStatues22 EquipmentStatues23 EquipmentStatues24 EquipmentStatues25 EquipmentStatues26 EquipmentStatues27 EquipmentStatues28 EquipmentStatues29 EquipmentSmithingTabs2 EquipmentSmithingTabs3 EquipmentSmithingTabs4 EquipmentSmithingTabs5 EquipmentSmithingTabs6 SmithingRecipes1 SmithingRecipes2 SmithingRecipes3 SmithingRecipes4 SmithingRecipes5 SmithingRecipes6 TalentBook1 TalentBook2 TalentBook3 TalentBook4 TalentBook5 MaxCapBagT2 MaxCapBag1 MaxCapBag2 MaxCapBag3 MaxCapBag4 MaxCapBag5 MaxCapBagMi6 MaxCapBagMi7 MaxCapBagMi8 MaxCapBagMi9 MaxCapBagMi10 MaxCapBagMi11 MaxCapBagT1 MaxCapBag7 MaxCapBag9 MaxCapBagT3 MaxCapBagT4 MaxCapBagT5 MaxCapBagT6 MaxCapBagT7 MaxCapBagT8 MaxCapBagT9 MaxCapBagT10 MaxCapBagT11 MaxCapBag6 MaxCapBag8 MaxCapBag10 MaxCapBagF3 MaxCapBagF4 MaxCapBagF5 MaxCapBagF6 MaxCapBagF7 MaxCapBagF8 MaxCapBagF9 MaxCapBagF10 MaxCapBagF11 MaxCapBagM1 MaxCapBagM2 MaxCapBagM3 MaxCapBagM4 MaxCapBagM5 MaxCapBagM6 MaxCapBagM7 MaxCapBagM8 MaxCapBagM9 MaxCapBagM10 MaxCapBagM11 MaxCapBagM12 MaxCapBagFi1 MaxCapBagFi2 MaxCapBagFi3 MaxCapBagFi4 MaxCapBagFi5 MaxCapBagFi6 MaxCapBagFi7 MaxCapBagFi8 MaxCapBagFi9 MaxCapBagFi10 MaxCapBagFi11 MaxCapBagB1 MaxCapBagB2 MaxCapBagB3 MaxCapBagB4 MaxCapBagB5 MaxCapBagB6 MaxCapBagB7 MaxCapBagB8 MaxCapBagB9 MaxCapBagB10 MaxCapBagB11 MaxCapBagTr1 MaxCapBagTr3 MaxCapBagTr4 MaxCapBagTr5 MaxCapBagTr6 MaxCapBagTr7 MaxCapBagTr8 MaxCapBagTr9 MaxCapBagTr10 MaxCapBagS1 MaxCapBagS3 MaxCapBagS4 MaxCapBagS5 MaxCapBagS6 MaxCapBagS7 MaxCapBagS8 MaxCapBagS9 MaxCapBagS10 ObolBronze0 ObolSilver0 ObolGold0 ObolPlatinum0 ObolPink0 ObolBronze1 ObolSilver1 ObolGold1 ObolPlatinum1 ObolPink1 ObolBronze2 ObolSilver2 ObolGold2 ObolPlatinum2 ObolPink2 ObolBronze3 ObolSilver3 ObolGold3 ObolPlatinum3 ObolPink3 ObolBronzeDamage ObolSilverDamage ObolGoldDamage ObolPlatinumDamage ObolPinkDamage ObolSilverMoney ObolGoldMoney ObolBronzeMining ObolSilverMining ObolGoldMining ObolPlatinumMining ObolPinkMining ObolBronzeChoppin ObolSilverChoppin ObolGoldChoppin ObolPlatinumChoppin ObolPinkChoppin ObolBronzeFishing ObolSilverFishing ObolGoldFishing ObolPlatinumFishing ObolPinkFishing ObolBronzeCatching ObolSilverCatching ObolGoldCatching ObolPlatinumCatching ObolPinkCatching ObolSilverLuck ObolGoldLuck ObolPlatinumLuck ObolPinkLuck ObolBronzePop ObolSilverPop ObolGoldPop ObolPlatinumPop ObolPinkPop ObolBronzeKill ObolSilverKill ObolGoldKill ObolPlatinumKill ObolPinkKill ObolBronzeEXP ObolSilverEXP ObolGoldEXP ObolPlatinumEXP ObolPinkEXP ObolBronzeCard ObolSilverCard ObolGoldCard ObolPlatinumCard ObolPinkCard ObolBronzeDef ObolSilverDef ObolGoldDef ObolPlatinumDef ObolPinkDef ObolBronzeTrapping ObolSilverTrapping ObolGoldTrapping ObolPlatinumTrapping ObolPinkTrapping ObolBronzeCons ObolSilverCons ObolGoldCons ObolPlatinumCons ObolPinkCons ObolBronzeWorship ObolSilverWorship ObolGoldWorship ObolPlatinumWorship ObolPinkWorship ObolFrog ObolAmarokA ObolEfauntA ObolKnight ObolSlush ObolChizoarA ObolTroll ObolLava ObolKruk ObolHyper0 ObolHyper1 ObolHyper2 ObolHyper3 ObolHyperB0 ObolHyperB1 ObolHyperB2 ObolHyperB3 StampA1 StampA2 StampA3 StampA4 StampA5 StampA6 StampA7 StampA8 StampA9 StampA10 StampA11 StampA12 StampA13 StampA14 StampA15 StampA16 StampA17 StampA18 StampA19 StampA20 StampA21 StampA22 StampA23 StampA24 StampA25 StampA26 StampA27 StampA28 StampA29 StampA30 StampA31 StampA32 StampA33 StampA34 StampA35 StampA36 StampA37 StampA38 StampA39 StampA40 StampA41 StampA42 StampB1 StampB2 StampB3 StampB4 StampB5 StampB6 StampB7 StampB8 StampB9 StampB10 StampB11 StampB12 StampB13 StampB14 StampB15 StampB16 StampB17 StampB18 StampB19 StampB20 StampB21 StampB22 StampB23 StampB24 StampB25 StampB26 StampB27 StampB28 StampB29 StampB30 StampB31 StampB32 StampB33 StampB34 StampB35 StampB36 StampB37 StampB38 StampB39 StampB40 StampB41 StampB42 StampB43 StampB44 StampB45 StampB46 StampB47 StampB48 StampB49 StampB50 StampB51 StampB52 StampB53 StampB54 StampC1 StampC2 StampC3 StampC4 StampC5 StampC6 StampC7 StampC8 StampC9 StampC10 StampC11 StampC12 StampC13 StampC14 StampC15 StampC16 StampC17 StampC18 StampC19 StampC20 StampC21 StampC22 StampC23 InvBag1 InvBag2 InvBag3 InvBag4 InvBag5 InvBag6 InvBag7 InvBag8 InvBag100 InvBag101 InvBag102 InvBag103 InvBag104 InvBag105 InvBag106 InvBag107 InvBag108 InvBag109 InvBag110 InvBag111 InvStorage1 InvStorage2 InvStorage3 InvStorage4 InvStorage5 InvStorage6 InvStorage7 InvStorage8 InvStorage9 InvStorage10 InvStorage11 InvStorage12 InvStorage13 InvStorage14 InvStorage15 InvStorage16 InvStorage17 InvStorage18 InvStorage19 InvStorage20 InvStorage21 InvStorage22 InvStorage23 InvStorage24 InvStorage25 InvStorage26 InvStorage27 InvStorage28 InvStorageF InvStorageS InvStorageC InvStorageD InvStorageN InvStorageH InvStorageL Weight1 Weight2 Weight3 Weight4 Weight5 Weight6 Weight7 Weight8 Weight9 Weight10 Weight11 Weight12 Weight13 Weight14 Line1 Line2 Line3 Line4 Line5 Line6 Line7 Line8 Line9 Line10 Line11 Line12 Line13 Line14 Ladle PetEgg Genetic0 Genetic1 Genetic2 Genetic3 CardPack1 CardPack2 CardPack3 CardPack4 CardPack5 CardPack6 CardPack7 DungCredits2 Cash XP XPskill DungEnhancer0 DungEnhancer1 DungEnhancer2 DungRNG0 DungRNG1 DungRNG2 DungRNG3 DungRNG4 DungeonA1 DungeonA2 DungeonA3 DungeonA4 DungeonA5 DungeonA6 DungeonA7 DungeonA8 KeyFrag DungCredits1 LootDice Tree7D PlatD Fish1D Fish3D Cashb Dung3Ice FoodHealth1d FoodHealth2d FoodHealth3d DungWeaponPunchA1 DungWeaponPunchA2 DungWeaponPunchA3 DungWeaponPunchA4 DungWeaponPunchA5 DungWeaponPunchB1 DungWeaponPunchB2 DungWeaponPunchB3 DungWeaponPunchB4 DungWeaponPunchB5 DungWeaponPunchC1 DungWeaponPunchC2 DungWeaponPunchC3 DungWeaponPunchC4 DungWeaponPunchC5 DungWeaponPunchD1 DungWeaponPunchD2 DungWeaponPunchD3 DungWeaponPunchD4 DungWeaponPunchD5 DungWeaponPunchE1 DungWeaponPunchE2 DungWeaponPunchE3 DungWeaponPunchE4 DungWeaponPunchE5 DungWeaponPunchF1 DungWeaponPunchF2 DungWeaponPunchF3 DungWeaponPunchF4 DungWeaponPunchF5 DungWeaponSwordA1 DungWeaponSwordA2 DungWeaponSwordA3 DungWeaponSwordA4 DungWeaponSwordA5 DungWeaponSwordB1 DungWeaponSwordB2 DungWeaponSwordB3 DungWeaponSwordB4 DungWeaponSwordB5 DungWeaponSwordC1 DungWeaponSwordC2 DungWeaponSwordC3 DungWeaponSwordC4 DungWeaponSwordC5 DungWeaponSwordD1 DungWeaponSwordD2 DungWeaponSwordD3 DungWeaponSwordD4 DungWeaponSwordD5 DungWeaponSwordE1 DungWeaponSwordE2 DungWeaponSwordE3 DungWeaponSwordE4 DungWeaponSwordE5 DungWeaponSwordF1 DungWeaponSwordF2 DungWeaponSwordF3 DungWeaponSwordF4 DungWeaponSwordF5 DungWeaponBowA1 DungWeaponBowA2 DungWeaponBowA3 DungWeaponBowA4 DungWeaponBowA5 DungWeaponBowB1 DungWeaponBowB2 DungWeaponBowB3 DungWeaponBowB4 DungWeaponBowB5 DungWeaponBowC1 DungWeaponBowC2 DungWeaponBowC3 DungWeaponBowC4 DungWeaponBowC5 DungWeaponBowD1 DungWeaponBowD2 DungWeaponBowD3 DungWeaponBowD4 DungWeaponBowD5 DungWeaponBowE1 DungWeaponBowE2 DungWeaponBowE3 DungWeaponBowE4 DungWeaponBowE5 DungWeaponBowF1 DungWeaponBowF2 DungWeaponBowF3 DungWeaponBowF4 DungWeaponBowF5 DungWeaponWandA1 DungWeaponWandA2 DungWeaponWandA3 DungWeaponWandA4 DungWeaponWandA5 DungWeaponWandB1 DungWeaponWandB2 DungWeaponWandB3 DungWeaponWandB4 DungWeaponWandB5 DungWeaponWandC1 DungWeaponWandC2 DungWeaponWandC3 DungWeaponWandC4 DungWeaponWandC5 DungWeaponWandD1 DungWeaponWandD2 DungWeaponWandD3 DungWeaponWandD4 DungWeaponWandD5 DungWeaponWandE1 DungWeaponWandE2 DungWeaponWandE3 DungWeaponWandE4 DungWeaponWandE5 DungWeaponWandF1 DungWeaponWandF2 DungWeaponWandF3 DungWeaponWandF4 DungWeaponWandF5 DungEquipmentHats0 DungEquipmentHats1 DungEquipmentHats2 DungEquipmentHats3 DungEquipmentHats4 DungEquipmentShirt0 DungEquipmentShirt1 DungEquipmentShirt2 DungEquipmentShirt3 DungEquipmentShirt4 DungEquipmentPants0 DungEquipmentPants1 DungEquipmentPants2 DungEquipmentPants3 DungEquipmentPants4 DungEquipmentShoes0 DungEquipmentShoes1 DungEquipmentShoes2 DungEquipmentShoes3 DungEquipmentShoes4 DungEquipmentPendant0 DungEquipmentPendant1 DungEquipmentPendant2 DungEquipmentPendant3 DungEquipmentPendant4 DungEquipmentRings0 DungEquipmentRings1 DungEquipmentRings2 DungEquipmentRings3 DungEquipmentRings4".split(" ")

#This replacement dict is needed due to a restriction for the image mapping variable names not being able to start with a Number
slab_itemNameReplacementDict = {
    "Timecandy1": "time-candy-1-hr",
    "Timecandy2": "time-candy-2-hr",
    "Timecandy3": "time-candy-4-hr",
    "Timecandy4": "time-candy-12-hr",
    "Timecandy5": "time-candy-24-hr",
    "Timecandy6": "time-candy-72-hr",
    "EquipmentHats108": "third-anniversary-ice-cream-topper",
    "EquipmentNametag10": "third-anniversary-idleon-nametag",
}
dungeonDropsList = [
    "Quest51", "Quest52", "PalmTreeD", "Quest53", "Quest54", "Quest55",
    "DungCredits2", "Cash", "XP", "XPskill", "DungEnhancer0", "DungEnhancer1", "DungEnhancer2",
    "DungRNG0", "DungRNG1", "DungRNG2", "DungRNG3", "DungRNG4",
    "DungeonA1", "DungeonA2", "DungeonA3", "DungeonA4", "DungeonA5", "DungeonA6", "DungeonA7", "DungeonA8",
    "KeyFrag", "DungCredits1", "LootDice", "Tree7D", "PlatD", "Fish1D", "Fish3D", "Cashb", "Dung3Ice",
    "FoodHealth1d", "FoodHealth2d", "FoodHealth3d"
]
maxDungeonWeaponsAvailable = 23  #This is the value saved in the JSON, 0-23 = 24 total. Last verified in 2.12
dungeonWeaponsList = [
    "DungWeaponPunchA1", "DungWeaponPunchA2", "DungWeaponPunchA3", "DungWeaponPunchA4", "DungWeaponPunchA5", "DungWeaponPunchB1", "DungWeaponPunchB2", "DungWeaponPunchB3", "DungWeaponPunchB4", "DungWeaponPunchB5", "DungWeaponPunchC1", "DungWeaponPunchC2", "DungWeaponPunchC3", "DungWeaponPunchC4", "DungWeaponPunchC5", "DungWeaponPunchD1", "DungWeaponPunchD2", "DungWeaponPunchD3", "DungWeaponPunchD4", "DungWeaponPunchD5", "DungWeaponPunchE1", "DungWeaponPunchE2", "DungWeaponPunchE3", "DungWeaponPunchE4",  #"DungWeaponPunchE5", "DungWeaponPunchF1", "DungWeaponPunchF2", "DungWeaponPunchF3", "DungWeaponPunchF4", "DungWeaponPunchF5",
    "DungWeaponSwordA1", "DungWeaponSwordA2", "DungWeaponSwordA3", "DungWeaponSwordA4", "DungWeaponSwordA5", "DungWeaponSwordB1", "DungWeaponSwordB2", "DungWeaponSwordB3", "DungWeaponSwordB4", "DungWeaponSwordB5", "DungWeaponSwordC1", "DungWeaponSwordC2", "DungWeaponSwordC3", "DungWeaponSwordC4", "DungWeaponSwordC5", "DungWeaponSwordD1", "DungWeaponSwordD2", "DungWeaponSwordD3", "DungWeaponSwordD4", "DungWeaponSwordD5", "DungWeaponSwordE1", "DungWeaponSwordE2", "DungWeaponSwordE3", "DungWeaponSwordE4",  #"DungWeaponSwordE5", "DungWeaponSwordF1", "DungWeaponSwordF2", "DungWeaponSwordF3", "DungWeaponSwordF4", "DungWeaponSwordF5",
    "DungWeaponBowA1", "DungWeaponBowA2", "DungWeaponBowA3", "DungWeaponBowA4", "DungWeaponBowA5", "DungWeaponBowB1", "DungWeaponBowB2", "DungWeaponBowB3", "DungWeaponBowB4", "DungWeaponBowB5", "DungWeaponBowC1", "DungWeaponBowC2", "DungWeaponBowC3", "DungWeaponBowC4", "DungWeaponBowC5", "DungWeaponBowD1", "DungWeaponBowD2", "DungWeaponBowD3", "DungWeaponBowD4", "DungWeaponBowD5", "DungWeaponBowE1", "DungWeaponBowE2", "DungWeaponBowE3", "DungWeaponBowE4",  #"DungWeaponBowE5", "DungWeaponBowF1", "DungWeaponBowF2", "DungWeaponBowF3", "DungWeaponBowF4", "DungWeaponBowF5",
    "DungWeaponWandA1", "DungWeaponWandA2", "DungWeaponWandA3", "DungWeaponWandA4", "DungWeaponWandA5", "DungWeaponWandB1", "DungWeaponWandB2", "DungWeaponWandB3", "DungWeaponWandB4", "DungWeaponWandB5", "DungWeaponWandC1", "DungWeaponWandC2", "DungWeaponWandC3", "DungWeaponWandC4", "DungWeaponWandC5", "DungWeaponWandD1", "DungWeaponWandD2", "DungWeaponWandD3", "DungWeaponWandD4", "DungWeaponWandD5", "DungWeaponWandE1", "DungWeaponWandE2", "DungWeaponWandE3", "DungWeaponWandE4",  #"DungWeaponWandE5", "DungWeaponWandF1", "DungWeaponWandF2", "DungWeaponWandF3", "DungWeaponWandF4", #"DungWeaponWandF5",
]
maxDungeonArmorsAvailable = 3  #This is the value saved in the JSON, 0-3 = 4 total. Last verified in 2.12
dungeonArmorsList = [
    "DungEquipmentHats0", "DungEquipmentHats1", "DungEquipmentHats2", "DungEquipmentHats3",  #"DungEquipmentHats4",
    "DungEquipmentShirt0", "DungEquipmentShirt1", "DungEquipmentShirt2", "DungEquipmentShirt3",  #"DungEquipmentShirt4",
    "DungEquipmentPants0", "DungEquipmentPants1", "DungEquipmentPants2", "DungEquipmentPants3",  #"DungEquipmentPants4",
    "DungEquipmentShoes0", "DungEquipmentShoes1", "DungEquipmentShoes2", "DungEquipmentShoes3",  #"DungEquipmentShoes4",
]  #This list was pulled from the items.yaml file
maxDungeonJewelryAvailable = 3   #This is the value saved in the JSON, 0-3 = 4 total. Last verified in 2.12
dungeonJewelryList = [
    "DungEquipmentPendant0", "DungEquipmentPendant1", "DungEquipmentPendant2", "DungEquipmentPendant3",  #"DungEquipmentPendant4",
    "DungEquipmentRings0", "DungEquipmentRings1", "DungEquipmentRings2", "DungEquipmentRings3",  #"DungEquipmentRings4",
]  #This list was pulled from the items.yaml file

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
slab_QuestRewardsAllChars = {
    'EquipmentPants16': {
        "ItemName": "Adam's Leaf",
        "QuestGiver": "Sprout",
        "QuestName": "Justice Wears No Clothes",
        "QuestNameCoded": "Sprout2"
    },
    'EquipmentShirts17': {
        "ItemName": "MCR Tshirt",
        "QuestGiver": "Sprout",
        "QuestName": "Shoe Shopping with Sprout",
        "QuestNameCoded": "Sprout3"
    },
    'NPCtoken12': {
        "ItemName": "Sproutinald Token",
        "QuestGiver": "Sprout",
        "QuestName": "Frisbee Fanatic",
        "QuestNameCoded": "Sprout4"
    },
    'EquipmentRings12': {
        "ItemName": "Frisbee Ring",
        "QuestGiver": "Sprout",
        "QuestName": "Frisbee Fanatic",
        "QuestNameCoded": "Sprout4"
    },
    'MaxCapBagT1': {
        "ItemName": "Miniature Choppin Pouch",
        "QuestGiver": "Woodsman",
        "QuestName": "A noob's first swing",
        "QuestNameCoded": "Woodsman1"
    },
    'EquipmentToolsHatchet0': {
        "ItemName": "Old Hatchet",
        "QuestGiver": "Woodsman",
        "QuestName": "A noob's 2nd first swing",
        "QuestNameCoded": "Woodsman2"
    },
    'EquipmentHats4Choppin': {
        "ItemName": "Stump Prop",
        "QuestGiver": "Woodsman",
        "QuestName": "It's Just a Plank, Bro!",
        "QuestNameCoded": "Woodsman3"
    },
    'NPCtoken5': {
        "ItemName": "Woodsman Token",
        "QuestGiver": "Woodsman",
        "QuestName": "Exotic Pranks... I mean Logs!",
        "QuestNameCoded": "Woodsman4"
    },
    'CraftMat2': {
        "ItemName": "Crimson String",
        "QuestGiver": "Scripticus",
        "QuestName": "Hardcore Gamer Status, Here I Come!",
        "QuestNameCoded": "Scripticus2"
    },
    'EquipmentHats7': {
        "ItemName": "Red Headband",
        "QuestGiver": "Scripticus",
        "QuestName": "Gear Up, Gamer!",
        "QuestNameCoded": "Scripticus3"
    },
    'InvBag1': {
        "ItemName": "Inventory Bag A",
        "QuestGiver": "Scripticus",
        "QuestName": "Mr. Worldwide",
        "QuestNameCoded": "Scripticus4"
    },
    'EquipmentTools1': {
        "ItemName": "Junk Pickaxe",
        "QuestGiver": "Scripticus",
        "QuestName": "Certified Swinger, of Pickaxes of course!",
        "QuestNameCoded": "Scripticus6"
    },
    'MaxCapBagM1': {
        "ItemName": "Mini Materials Pouch",
        "QuestGiver": "Scripticus",
        "QuestName": "The Smithing Grind",
        "QuestNameCoded": "Scripticus7"
    },
    'InvBag2': {
        "ItemName": "Inventory Bag B",
        "QuestGiver": "Scripticus",
        "QuestName": "Warrior, Archer or Mage?",
        "QuestNameCoded": "Scripticus8"
    },
    'MaxCapBagM3': {
        "ItemName": "Small Material Pouch",
        "QuestGiver": "Scripticus",
        "QuestName": "Warrior, Archer or Mage?",
        "QuestNameCoded": "Scripticus8"
    },
    'InvBag3': {
        "ItemName": "Inventory Bag C",
        "QuestGiver": "Scripticus",
        "QuestName": "Stiltzcho, the Leaf Scout",
        "QuestNameCoded": "Scripticus9"
    },
    'Trophy6': {
        "ItemName": "Blunder Hero",
        "QuestGiver": "Scripticus",
        "QuestName": "Champion of the Grasslands",
        "QuestNameCoded": "Scripticus12"
    },
    'StoneA1b': {
        "ItemName": "Armor Upgrade Stone G",
        "QuestGiver": "Krunk",
        "QuestName": "The Scientific Method, According to a Rock",
        "QuestNameCoded": "Krunk2"
    },
    'InvStorage3': {
        "ItemName": "The Scientific Method, According to a Rock",
        "QuestGiver": "Krunk",
        "QuestName": "Storage Chest 3",
        "QuestNameCoded": "Krunk2"
    },
    'NPCtoken10': {
        "ItemName": "Krunk Token",
        "QuestGiver": "Krunk",
        "QuestName": "King of the Cavern",
        "QuestNameCoded": "Krunk3"
    },
    'OilBarrel4': {
        "ItemName": "Glumlee's Special Tutorial Oil",
        "QuestGiver": "Glumlee",
        "QuestName": "Learning to Swing",
        "QuestNameCoded": "Glumlee1"
    },
    'Quest1': {
        "ItemName": "Mining Certificate",
        "QuestGiver": "Glumlee",
        "QuestName": "Literally Burning your Money",
        "QuestNameCoded": "Glumlee3"
    },
    'MaxCapBagT2': {
        "ItemName": "Miniature Mining Pouch",
        "QuestGiver": "Glumlee",
        "QuestName": "Literally Burning your Money",
        "QuestNameCoded": "Glumlee3"
    },
    'NPCtoken6': {
        "ItemName": "Glumlee Token",
        "QuestGiver": "Glumlee",
        "QuestName": "He's Havin' a Bad Day",
        "QuestNameCoded": "Glumlee5"
    },
    'MaxCapBag6': {
        "ItemName": "Miniscule Food Pouch",
        "QuestGiver": "Picnic_Stowaway",
        "QuestName": "The Hungry Stowaway",
        "QuestNameCoded": "Picnic_Stowaway1"
    },
    'EquipmentPendant9': {
        "ItemName": "Little Wooden Katana",
        "QuestGiver": "Picnic_Stowaway",
        "QuestName": "Beating Up Frogs for some Sauce",
        "QuestNameCoded": "Picnic_Stowaway2"
    },
    'Quest9': {
        "ItemName": "Picnic Token",
        "QuestGiver": "Picnic_Stowaway",
        "QuestName": "A Midnight Snack",
        "QuestNameCoded": "Picnic_Stowaway11"
    },
    'Trophy1': {
        "ItemName": "King of Food",
        "QuestGiver": "Picnic_Stowaway",
        "QuestName": "King of Food",
        "QuestNameCoded": "Picnic_Stowaway12"
    },
    'StampA4': {
        "ItemName": "Tomahawk Stamp",
        "QuestGiver": "Hamish",
        "QuestName": "The Hamazing Plot Twist",
        "QuestNameCoded": "Hamish1"
    },
    'StampB6': {
        "ItemName": "Should We Tell Him?",
        "QuestGiver": "Hamish",
        "QuestName": "Choppin' Bag Stamp",
        "QuestNameCoded": "Hamish2"
    },
    'InvStorage1': {
        "ItemName": "Slime for Storage",
        "QuestGiver": "Hamish",
        "QuestName": "Storage Chest 1",
        "QuestNameCoded": "Hamish3"
    },
    'Quest5': {
        "ItemName": "Class Certificate",
        "QuestGiver": "Promotheus",
        "QuestName": "Three Right Answers",
        "QuestNameCoded": "Promotheus2"
    },
    'EquipmentHats29': {
        "ItemName": "Slovakian Scare",
        "QuestGiver": "Promotheus",
        "QuestName": "Alien Headband",
        "QuestNameCoded": "Promotheus3"
    },
    'InvBag4': {
        "ItemName": "Inventory Bag D",
        "QuestGiver": "Promotheus",
        "QuestName": "The Witcher, but not Really Inventory Bag D",
        "QuestNameCoded": "Promotheus4"
    },

    'Quest6': {
        "ItemName": "Scouting Report",
        "QuestGiver": "Stiltzcho",
        "QuestName": "Investigator by Day, Prankster by Night",
        "QuestNameCoded": "Stiltzcho3"
    },
    'EquipmentPendant11': {
        "ItemName": "Carrot Horror",
        "QuestGiver": "Stiltzcho",
        "QuestName": "Investigator by Day, Prankster by Night",
        "QuestNameCoded": "Stiltzcho3"
    },
    'NPCtoken4': {
        "ItemName": "Stiltzcho Token",
        "QuestGiver": "Stiltzcho",
        "QuestName": "Time Crime Season Finale",
        "QuestNameCoded": "Stiltzcho6"
    },
    'MaxCapBag10': {
        "ItemName": "Small Food Pouch",
        "QuestGiver": "Funguy",
        "QuestName": "Mushroom Munchies",
        "QuestNameCoded": "Funguy1"
    },
    'EquipmentRings13': {
        "ItemName": "Silver Stopwatch",
        "QuestGiver": "Funguy",
        "QuestName": "Partycrastination",
        "QuestNameCoded": "Funguy3"
    },
    'NPCtoken9': {
        "ItemName": "Funguy Token",
        "QuestGiver": "Funguy",
        "QuestName": "Wicked Party Cleanup",
        "QuestNameCoded": "Funguy5"
    },
    'StampC1': {
        "ItemName": "",
        "QuestGiver": "Tiki_Chief",
        "QuestName": "",
        "QuestNameCoded": "Tiki_Chief2"
    },
    'NPCtoken11': {
        "ItemName": "Questin Stamp",
        "QuestGiver": "Tiki_Chief",
        "QuestName": "Three Strikes, you're Out!",
        "QuestNameCoded": "Tiki_Chief4"
    },
    'NPCtoken13': {
        "ItemName": "Dog Bone Token",
        "QuestGiver": "Dog_Bone",
        "QuestName": "Bow Wow going Dow..n!",
        "QuestNameCoded": "Dog_Bone2"
    },
    'StampC6': {
        "ItemName": "Potion Stamp",
        "QuestGiver": "Papua_Piggea",
        "QuestName": "Stamp Collecting",
        "QuestNameCoded": "Papua_Piggea3"
    },
    'NPCtoken7': {
        "ItemName": "Papua Piggea Token",
        "QuestGiver": "Papua_Piggea",
        "QuestName": "This Little Piggy Felt Remorse",
        "QuestNameCoded": "Papua_Piggea4"
    },
    'StampA19': {
        "ItemName": "Polearm Stamp",
        "QuestGiver": "Papua_Piggea",
        "QuestName": "This Little Piggy Felt Remorse",
        "QuestNameCoded": "Papua_Piggea4"
    },
    'StampA9': {
        "ItemName": "Fist Stamp",
        "QuestGiver": "Mutton",
        "QuestName": "Beatboxing Starterpack",
        "QuestNameCoded": "Mutton1"
    },
    'InvStorage5': {
        "ItemName": "Storage Chest 5",
        "QuestGiver": "Mutton",
        "QuestName": "Beatboxing Starterpack",
        "QuestNameCoded": "Mutton1"
    },
    'StampA14': {
        "ItemName": "Manamoar Stamp",
        "QuestGiver": "Mutton",
        "QuestName": "Clout Chasin'",
        "QuestNameCoded": "Mutton2"
    },
    'StampA16': {
        "ItemName": "Scimitar Stamp",
        "QuestGiver": "Mutton",
        "QuestName": "Cross Platform Promotion",
        "QuestNameCoded": "Mutton3"
    },
    'StampC7': {
        "ItemName": "Golden Apple Stamp",
        "QuestGiver": "Mutton",
        "QuestName": "7 Figure Followers",
        "QuestNameCoded": "Mutton4"
    },
    'StampA26': {
        "ItemName": "Steve Sword",
        "QuestGiver": "Mutton",
        "QuestName": "7 Figure Followers",
        "QuestNameCoded": "Mutton4"
    },
    'StampB17': {
        "ItemName": "Fishing Rod Stamp",
        "QuestGiver": "Fishpaste",
        "QuestName": "'Accidental' Exploit",
        "QuestNameCoded": "Fishpaste971"
    },
    'NPCtoken22': {
        "ItemName": "Fishpaste Token",
        "QuestGiver": "Fishpaste",
        "QuestName": "Can you do the Can Can?",
        "QuestNameCoded": "Fishpaste972"
    },
    'Weight6': {
        "ItemName": "One Pound of Feathers",
        "QuestGiver": "Fishpaste",
        "QuestName": "Can you do the Can Can?",
        "QuestNameCoded": "Fishpaste972"
    },
    'StampC18': {
        "ItemName": "Talent S Stamp",
        "QuestGiver": "Fishpaste",
        "QuestName": "Can you do the Can Can?",
        "QuestNameCoded": "Fishpaste972"
    },
    'Weight2': {
        "ItemName": "Iron Hook",
        "QuestGiver": "Scubidew",
        "QuestName": "Don't Step to Me, Bro!",
        "QuestNameCoded": "Scubidew1"
    },
    # 'Weight2': {
    #     "ItemName": "Iron Hook",
    #     "QuestGiver": "Carpetiem",
    #     "QuestName": "Helping 100 times over",
    #     "QuestNameCoded": "Carpetiem4"
    # },
    'Weight3': {
        "ItemName": "Basic Bobber",
        "QuestGiver": "Scubidew",
        "QuestName": "Uncovering the Deep Sea State!!!",
        "QuestNameCoded": "Scubidew2"
    },
    'NPCtoken26': {
        "ItemName": "Scubidew Token",
        "QuestGiver": "Scubidew",
        "QuestName": "A Normal Quest.",
        "QuestNameCoded": "Scubidew3"
    },
    'Weight1': {
        "ItemName": "Wormie Weight",
        "QuestGiver": "Whattso",
        "QuestName": "Mopey Dick",
        "QuestNameCoded": "Whattso1"
    },
    'Line11': {
        "ItemName": "Scripticus Spoons",
        "QuestGiver": "Whattso",
        "QuestName": "The Whaley Hard Minigame",
        "QuestNameCoded": "Whattso2"
    },
    'Weight12': {
        "ItemName": "Triple Threat",
        "QuestGiver": "Whattso",
        "QuestName": "Bobbin' Bobbers",
        "QuestNameCoded": "Whattso3"
    },
    'NPCtoken18': {
        "ItemName": "Whattso Token",
        "QuestGiver": "Whattso",
        "QuestName": "Bobbin' Bobbers",
        "QuestNameCoded": "Whattso3"
    },
    'Line7': {
        "ItemName": "Electrical Wiring",
        "QuestGiver": "Whattso",
        "QuestName": "The Biggest Fish in the Sea...?",
        "QuestNameCoded": "Whattso4"
    },
    'Quest46': {
        "ItemName": "The Bobber Challenge Scroll",
        "QuestGiver": "Whattso",
        "QuestName": "The Biggest Fish in the Sea...?",
        "QuestNameCoded": "Whattso4"
    },
    'Quest20': {
        "ItemName": "Signed Arrest Warrant",
        "QuestGiver": "Bandit_Bob",
        "QuestName": "Bringing Bob's Boxes",
        "QuestNameCoded": "Bandit_Bob3"
    },
    'NPCtoken16': {
        "ItemName": "Bandit Bob Token",
        "QuestGiver": "Bandit_Bob",
        "QuestName": "The Desert Dungeon Prequest",
        "QuestNameCoded": "Bandit_Bob4"
    },
    'NPCtoken20': {
        "ItemName": "Carpetiem Token",
        "QuestGiver": "Carpetiem",
        "QuestName": "Helping 100 times over",
        "QuestNameCoded": "Carpetiem4"
    },
    'Line2': {
        "ItemName": "Silver Twine",
        "QuestGiver": "Carpetiem",
        "QuestName": "Helping 100 times over",
        "QuestNameCoded": "Carpetiem4"
    },
    'NPCtoken25': {
        "ItemName": "Djonnut Token",
        "QuestGiver": "Djonnut",
        "QuestName": "The Blue New World",
        "QuestNameCoded": "Djonnut3"
    },
    'Quest27': {
        "ItemName": "Bag o Nuts",
        "QuestGiver": "Goldric",
        "QuestName": "Dress to Impress",
        "QuestNameCoded": "Goldric5"
    },
    'NPCtoken21': {
        "ItemName": "Goldric Token",
        "QuestGiver": "Goldric",
        "QuestName": "Dont lay a finger on my Sheepies!!!",
        "QuestNameCoded": "Goldric6"
    },
    'EquipmentRingsFishing1': {
        "ItemName": "Shallow Watering",
        "QuestGiver": "Omar_Da_Ogar",
        "QuestName": "Helping Omar Again",
        "QuestNameCoded": "Omar_Da_Ogar2"
    },
    'EquipmentRingsFishing2': {
        "ItemName": "Oceanic Ring,",
        "QuestGiver": "Omar_Da_Ogar",
        "QuestName": "Helping Omar Some More",
        "QuestNameCoded": "Omar_Da_Ogar4"
    },
    'Pearl1': {
        "ItemName": "Aqua Pearl",
        "QuestGiver": "Omar_Da_Ogar",
        "QuestName": "Helping Omar Yet Again Deja Vu",
        "QuestNameCoded": "Omar_Da_Ogar5"
    },
    'EquipmentRingsFishing3': {
        "ItemName": "Deepwater Trench Ring",
        "QuestGiver": "Omar_Da_Ogar",
        "QuestName": "Helping Omar For The Final Time",
        "QuestNameCoded": "Omar_Da_Ogar6"
    },
    'NPCtoken15': {
        'ItemName': 'TP Pete Token',
        'QuestGiver': 'TP Pete',
        'QuestName': 'Fired for BS Reasons!',
        'QuestNameCoded': 'TP_Pete3'
    },
    'EquipmentRings6': {
        "ItemName": "Death Wish",
        "QuestGiver": "Meel",
        "QuestName": "Waitin' for the Cards to Drop",
        "QuestNameCoded": "Meel2"
    },
    'InvStorage11': {
        "ItemName": "Red Stuff Bad!",
        "QuestGiver": "Snake_Jar",
        "QuestName": "Storage Chest 11",
        "QuestNameCoded": "Snake_Jar2"
    },
    'EquipmentHats44': {
        "ItemName": "Jar",
        "QuestGiver": "Snake_Jar",
        "QuestName": "PSA. You Are Being Eaten!",
        "QuestNameCoded": "Snake_Jar3"
    },
    'NPCtoken17': {
        "ItemName": "Snake Jar Token",
        "QuestGiver": "Snake_Jar",
        "QuestName": "A Noob, served Medium Rare!",
        "QuestNameCoded": "Snake_Jar4"
    },
    'NPCtoken24': {
        "ItemName": "Loominadi Token",
        "QuestGiver": "Loominadi",
        "QuestName": "The Mummy of Mystery",
        "QuestNameCoded": "Loominadi4"
    },
    'Weight8': {
        "ItemName": "Literal Elephant",
        "QuestGiver": "Loominadi",
        "QuestName": "The Mummy of Mystery",
        "QuestNameCoded": "Loominadi4"
    },
    'StampB14': {
        "ItemName": "Brainstew Stamps",
        "QuestGiver": "Wellington",
        "QuestName": "Platforms in Disguise, Platsformers!",
        "QuestNameCoded": "Wellington1"
    },
    'StampA24': {
        "ItemName": "Arcane Stamp",
        "QuestGiver": "Wellington",
        "QuestName": "Platforms in Disguise, Platsformers!",
        "QuestNameCoded": "Wellington1"
    },
    'StampB20': {
        "ItemName": "Fly Intel Stamp",
        "QuestGiver": "Wellington",
        "QuestName": "Findin' Fingerprints",
        "QuestNameCoded": "Wellington2"
    },
    'StampB22': {
        "ItemName": "Holy Mackerel Stamp",
        "QuestGiver": "Wellington",
        "QuestName": "Findin' Fingerprints",
        "QuestNameCoded": "Wellington2"
    },
    'StampC14': {
        "ItemName": "Talent II Stamp",
        "QuestGiver": "Wellington",
        "QuestName": "You Can't Run, but you Can Hide",
        "QuestNameCoded": "Wellington3"
    },
    'NPCtoken23': {
        "ItemName": "Wellington Token",
        "QuestGiver": "Wellington",
        "QuestName": "Puzzles and Math, a Winning Combination!",
        "QuestNameCoded": "Wellington4"
    },
    'NPCtoken14': {
        "ItemName": "Dazey Token",
        "QuestGiver": "Dazey",
        "QuestName": "Literally Physics",
        "QuestNameCoded": "Dazey2"
    },
    'InvStorage4': {
        "ItemName": "Storage Chest 4",
        "QuestGiver": "Cowbo_Jones",
        "QuestName": "The Hatless Howerhouse!",
        "QuestNameCoded": "Cowbo_Jones2"
    },
    'InvBag5': {
        "ItemName": "Inventory Bag E",
        "QuestGiver": "Cowbo_Jones",
        "QuestName": "Bake Him Away, Toys",
        "QuestNameCoded": "Cowbo_Jones8"
    },
    'EquipmentHats30': {
        "ItemName": "Cowbo Galloneer",
        "QuestGiver": "Cowbo_Jones",
        "QuestName": "A Hat in Crime",
        "QuestNameCoded": "Cowbo_Jones9"
    },
    'InvBag6': {
        "ItemName": "Inventory Bag F",
        "QuestGiver": "Cowbo_Jones",
        "QuestName": "Commence Criminal Crimes!",
        "QuestNameCoded": "Cowbo_Jones10"
    },
    'InvBag8': {
        "ItemName": "Inventory Bag H",
        "QuestGiver": "Cowbo_Jones",
        "QuestName": "Oh No, not the Elderly!",
        "QuestNameCoded": "Cowbo_Jones13"
    },
    'NPCtoken19': {
        "ItemName": "Cowbo Jones Token",
        "QuestGiver": "Cowbo_Jones",
        "QuestName": "Tomb Raid",
        "QuestNameCoded": "Cowbo_Jones14"
    },
    'Trophy11': {
        "ItemName": "YumYum Sheriff",
        "QuestGiver": "Cowbo_Jones",
        "QuestName": "The New Sheriff",
        "QuestNameCoded": "Cowbo_Jones15"
    },
    'Trophy22': {
        "ItemName": "Gladiator",
        "QuestGiver": "Centurion",
        "QuestName": "Glorious Gladiator",
        "QuestNameCoded": "Centurion8"
    },
    'StampB4': {
        "ItemName": "Lil' Mining Baggy Stamp",
        "QuestGiver": "XxX_Cattleprod_XxX",
        "QuestName": "Peak Gaming",
        "QuestNameCoded": "XxX_Cattleprod_XxX1"
    },
    'StampB19': {
        "ItemName": "Catch Net Stamp",
        "QuestGiver": "XxX_Cattleprod_XxX",
        "QuestName": "Peak Gaming",
        "QuestNameCoded": "XxX_Cattleprod_XxX1"
    },
    'StampC2': {
        "ItemName": "Mason Jar Stamp",
        "QuestGiver": "XxX_Cattleprod_XxX",
        "QuestName": "Wait No, I meant Pathetic Gaming",
        "QuestNameCoded": "XxX_Cattleprod_XxX2"
    },
    'StampB18': {
        "ItemName": "Fishhead Stamp",
        "QuestGiver": "XxX_Cattleprod_XxX",
        "QuestName": "Wait No, I meant Pathetic Gaming",
        "QuestNameCoded": "XxX_Cattleprod_XxX2"
    },
    'StampA28': {
        "ItemName": "Stat Graph Stamp",
        "QuestGiver": "XxX_Cattleprod_XxX",
        "QuestName": "Ok, NOW it's Peak Gaming!",
        "QuestNameCoded": "XxX_Cattleprod_XxX3"
    },
    'NPCtoken32': {
        "ItemName": "Hoggi Token",
        "QuestGiver": "Hoggindaz",
        "QuestName": "Chizoar No More",
        "QuestNameCoded": "Hoggindaz9"
    },
    'Trophy15': {
        "ItemName": "Frost Prince",
        "QuestGiver": "Hoggindaz",
        "QuestName": "The Fresh Prince of the Tundra",
        "QuestNameCoded": "Hoggindaz10"
    },
    'Quest61': {
        "ItemName": "Bill Brr's Vote",
        "QuestGiver": "Bill_Brr",
        "QuestName": "Coin Shenanigans",
        "QuestNameCoded": "Bill_Brr4"
    },
    'NPCtoken37': {
        "ItemName": "Bill Brr Token",
        "QuestGiver": "Bill_Brr",
        "QuestName": "Hatin' on the Green One",
        "QuestNameCoded": "Bill_Brr7"
    },
    'NPCtoken33': {
        "ItemName": "Bellows Token",
        "QuestGiver": "Bellows",
        "QuestName": "Optometric Hoarder",
        "QuestNameCoded": "Bellows4"
    },
    'StampA22': {
        "ItemName": "Hermes Stamp",
        "QuestGiver": "Crystalswine",
        "QuestName": "Melting the Snakes",
        "QuestNameCoded": "Crystalswine4"
    },
    'NPCtoken38': {
        "ItemName": "Crystalswine Token",
        "QuestGiver": "Crystalswine",
        "QuestName": "Sunrunning to Chizoar",
        "QuestNameCoded": "Crystalswine5"
    },
    'StampA25': {
        "ItemName": "Avast Yar Stamp",
        "QuestGiver": "Crystalswine",
        "QuestName": "Global Warming",
        "QuestNameCoded": "Crystalswine6"
    },
    'Quest60': {
        "ItemName": "Yondergreens Vote",
        "QuestGiver": "Yondergreen",
        "QuestName": "Legislative Action",
        "QuestNameCoded": "Yondergreen4"
    },
    'NPCtoken36': {
        "ItemName": "Yondergreen Token",
        "QuestGiver": "Yondergreen",
        "QuestName": "Ad Solidarity Contract",
        "QuestNameCoded": "Yondergreen7"
    },

    'Quest59': {
        "ItemName": "Shuvelle's Vote",
        "QuestGiver": "Shuvelle",
        "QuestName": "Mayoral Movie Taste",
        "QuestNameCoded": "Shuvelle4"
    },
    'NPCtoken35': {
        "ItemName": "Shuvelle Token",
        "QuestGiver": "Shuvelle",
        "QuestName": "Dig Diggily Diggy Dig Dig Hole!",
        "QuestNameCoded": "Shuvelle7"
    },
    'NPCtoken31': {
        "ItemName": "Lonely Hunter Token",
        "QuestGiver": "Lonely_Hunter",
        "QuestName": "Opening Chests",
        "QuestNameCoded": "Lonely_Hunter3"
    },
    'ResetBox': {
        "ItemName": "Post Office Box Reseto Magnifico",
        "QuestGiver": "Lord_of_the_Hunt",
        "QuestName": "Untitled Quest",
        "QuestNameCoded": "Lord_of_the_Hunt10"
    },
    'Trophy10': {
        "ItemName": "Critter Baron",
        "QuestGiver": "Lord_of_the_Hunt",
        "QuestName": "To Trap or not to Trap",
        "QuestNameCoded": "Lord_of_the_Hunt11"
    },
    'StampA21': {
        "ItemName": "Buckler Stamp",
        "QuestGiver": "Snouts",
        "QuestName": "A Salty Fall",
        "QuestNameCoded": "Snouts1"
    },
    'StampA18': {
        "ItemName": "Feather Stamp",
        "QuestGiver": "Snouts",
        "QuestName": "Gravity VS Salt",
        "QuestNameCoded": "Snouts2"
    },
    'StampB26': {
        "ItemName": "Purp Froge Stamp",
        "QuestGiver": "Snouts",
        "QuestName": "Gravity VS Salt",
        "QuestNameCoded": "Snouts2"
    },
    'StampC15': {
        "ItemName": "Talent III Stamp",
        "QuestGiver": "Snouts",
        "QuestName": "Big Ol Chonker",
        "QuestNameCoded": "Snouts3"
    },
    'StampC20': {
        "ItemName": "Biblio Stamp",
        "QuestGiver": "Snouts",
        "QuestName": "Big Ol Chonker",
        "QuestNameCoded": "Snouts3"
    },
    'NPCtoken34': {
        "ItemName": "Snouts Token",
        "QuestGiver": "Snouts",
        "QuestName": "Mana Plox",
        "QuestNameCoded": "Snouts4"
    },
    'StampB42': {
        "ItemName": "Lab Tube Stamp",
        "QuestGiver": "Capital_P",
        "QuestName": "Right side wrong side!",
        "QuestNameCoded": "Capital_P1"
    },
    'StampC21': {
        "ItemName": "DNA Stamp",
        "QuestGiver": "Capital_P",
        "QuestName": "No room on the Dance Floor!",
        "QuestNameCoded": "Capital_P2"
    },
    'StampA30': {
        "ItemName": "Diamond Axe Stamp",
        "QuestGiver": "Capital_P",
        "QuestName": "Everybody move it move it!",
        "QuestNameCoded": "Capital_P3"
    },
    'StampB37': {
        "ItemName": "Cooked Meal Stamp",
        "QuestGiver": "Oinkin",
        "QuestName": "Filling the Menu",
        "QuestNameCoded": "Oinkin1"
    },
    'StampB40': {
        "ItemName": "Nest Eggs Stamp",
        "QuestGiver": "Oinkin",
        "QuestName": "Diner Deliverer",
        "QuestNameCoded": "Oinkin2"
    },
    'StampB39': {
        "ItemName": "Ladle Stamp",
        "QuestGiver": "Oinkin",
        "QuestName": "Recipe for Fattening Pastry",
        "QuestNameCoded": "Oinkin3"
    },
    'StampB43': {
        "ItemName": "Sailboat Stamp",
        "QuestGiver": "Pirate_Porkchop",
        "QuestName": "Bring me the Booty",
        "QuestNameCoded": "Pirate_Porkchop1"
    },
    'StampB45': {
        "ItemName": "Divine Stamp",
        "QuestGiver": "Pirate_Porkchop",
        "QuestName": "Sailing for some Sparks",
        "QuestNameCoded": "Pirate_Porkchop2"
    },
    'StampA34': {
        "ItemName": "Sashe Sidestamp",
        "QuestGiver": "Pirate_Porkchop",
        "QuestName": "Seeking Treasure Shrooms",
        "QuestNameCoded": "Pirate_Porkchop3"
    },
    'StampA36': {
        "ItemName": "Conjocharmo Stamp",
        "QuestGiver": "Pirate_Porkchop",
        "QuestName": "Ye finest treasure at once!",
        "QuestNameCoded": "Pirate_Porkchop4"
    },
    'StampB44': {
        "ItemName": "Gamejoy Stamp",
        "QuestGiver": "Poigu",
        "QuestName": "Think twice speak once",
        "QuestNameCoded": "Poigu1"
    },
    'StampB46': {
        "ItemName": "Multitool Stamp",
        "QuestGiver": "Poigu",
        "QuestName": "Speak from the heart not the mind",
        "QuestNameCoded": "Poigu2"
    },
    'Quest70': {
        "ItemName": "Phone Box",
        "QuestGiver": "Rift_Ripper",
        "QuestName": "Entering The Rift...",
        "QuestNameCoded": "Rift_Ripper1"
    },
    'Quest71': {
        "ItemName": "Gem Envelope",
        "QuestGiver": "Rift_Ripper",
        "QuestName": "Entering The Rift...",
        "QuestNameCoded": "Rift_Ripper1"
    },
    # 'Quest71': {
    #     "ItemName": "Gem Envelope",
    #     "QuestGiver": "Nebulyte",
    #     "QuestName": "Chizoar Slayer",
    #     "QuestNameCoded": "Nebulyte2"
    # },
    'Trophy17': {
        "ItemName": "One of the Divine",
        "QuestGiver": "Tired_Mole",
        "QuestName": "Divine Endeavor",
        "QuestNameCoded": "Tired_Mole3"
    },
    'SmithingHammerChisel3': {
        "ItemName": "Onyx Tools",
        "QuestGiver": "Monolith",
        "QuestName": "Onyx Statue Crafting",
        "QuestNameCoded": "Monolith2"
    },
    'Weight14': {
        "ItemName": "Fat Albert",
        "QuestGiver": "Royal_Worm",
        "QuestName": "A Royal Gift",
        "QuestNameCoded": "Royal_Worm6"
    },
    'Trophy19': {
        "ItemName": "Nebula Royal",
        "QuestGiver": "Royal_Worm",
        "QuestName": "Royal Bidding",
        "QuestNameCoded": "Royal_Worm9"
    },
    'StampB48': {
        "ItemName": "Crop Evo Stamp",
        "QuestGiver": "Hoov",
        "QuestName": "Sneak Dropout",
        "QuestNameCoded": "Hoov1"
    },
    'StampA40': {
        "ItemName": "Void Sword Stamp",
        "QuestGiver": "Hoov",
        "QuestName": "Stealth Check 1 2 3",
        "QuestNameCoded": "Hoov2"
    },
    'InvStorageN': {
        "ItemName": "Ninja Chest",
        "QuestGiver": "Hoov",
        "QuestName": "Sneak Registration",
        "QuestNameCoded": "Hoov4"
    },
    'StampB53': {
        "ItemName": "Triad Essence Stamp",
        "QuestGiver": "Sussy_Gene",
        "QuestName": "Goofin' Around",
        "QuestNameCoded": "Sussy_Gene1"
    },
    'StampB51': {
        "ItemName": "Summoner Stone Stamp",
        "QuestGiver": "Sussy_Gene",
        "QuestName": "Messin' Around",
        "QuestNameCoded": "Sussy_Gene2"
    },
    'StampA41': {
        "ItemName": "Void Axe Stamp",
        "QuestGiver": "Sussy_Gene",
        "QuestName": "Loiterin' Around",
        "QuestNameCoded": "Sussy_Gene3"
    },
}
slab_QuestRewardsOnce = {
    'Mayo': {
        "ItemName": "Mayonnaise Bottle",
        "QuestGiver": "Walupiggy",
        "QuestName": "Treasure Hunt 1",
        "QuestNameCoded": "Walupiggy1"
    },
    'Trash': {
        "ItemName": "Broken Weapon",
        "QuestGiver": "Walupiggy",
        "QuestName": "Treasure Hunt 2",
        "QuestNameCoded": "Walupiggy2"
    },
    'Trash2': {
        "ItemName": "Dried Paint Blob",
        "QuestGiver": "Walupiggy",
        "QuestName": "Treasure Hunt 3",
        "QuestNameCoded": "Walupiggy3"
    },
    'Trash3': {
        "ItemName": "Engraved Bullet",
        "QuestGiver": "Walupiggy",
        "QuestName": "Treasure Hunt 4",
        "QuestNameCoded": "Walupiggy4"
    },
    'Timecandy7': {
        "ItemName": "Steamy Time Candy",
        "QuestGiver": "Walupiggy",
        "QuestName": "Treasure Hunt 4",
        "QuestNameCoded": "Walupiggy4"
    },
    'Quest44': {
        "ItemName": "Goldegg Capsule",
        "QuestGiver": "Walupiggy",
        "QuestName": "Treasure Hunt 4",
        "QuestNameCoded": "Walupiggy4"
    },
    'CardPack1': {
        "ItemName": "Newbie Card Pack",
        "QuestGiver": "Walupiggy",
        "QuestName": "Treasure Hunt 4",
        "QuestNameCoded": "Walupiggy4"
    },
    'CardPack4': {
        "ItemName": "Dungeon Card Pack",
        "QuestGiver": "Worldo",
        "QuestName": "Odd Jobs for Cold Hard Cash",
        "QuestNameCoded": "Worldo1"
    },
    'CardPack5': {
        "ItemName": "Galaxy Card Pack",
        "QuestGiver": "Nebulyte",
        "QuestName": "Chizoar Slayer",
        "QuestNameCoded": "Nebulyte2"
    },
    'CardPack6': {
        "ItemName": "Smolderin Card Pack",
        "QuestGiver": "Nebulyte",
        "QuestName": "Oh Geez Lets Not Think About This One...",
        "QuestNameCoded": "Nebulyte3"
    },
    'PeanutS': {
        "ItemName": "Stone Peanut",
        "QuestGiver": "Bushlyte",
        "QuestName": "A Peanut Saved is a Peanut not Eaten!",
        "QuestNameCoded": "Bushlyte3"
    },
    'Trophy3': {
        "ItemName": "Club Member",
        "QuestGiver": "Rocklyte",
        "QuestName": "Becoming the Best Beginner",
        "QuestNameCoded": "Rocklyte3"
    },
    'Trophy13': {
        "ItemName": "Club Maestro",
        "QuestGiver": "Cactolyte",
        "QuestName": "Maestro! The Stro! Mman!",
        "QuestNameCoded": "Cactolyte4"
    },
    'EquipmentNametag4': {
        "ItemName": "Vman Nametag",
        "QuestGiver": "Nebulyte",
        "QuestName": "VMAN ACHIEVED!",
        "QuestNameCoded": "Nebulyte4"
    },
}
npc_tokens = [
    'NPCtoken5', 'NPCtoken6', 'NPCtoken4', 'NPCtoken9', 'NPCtoken10', 'NPCtoken11',
    'NPCtoken13', 'NPCtoken7', 'Quest9', 'NPCtoken15', 'NPCtoken12', 'NPCtoken14',
    'NPCtoken16', 'NPCtoken17', 'NPCtoken18', 'NPCtoken19', 'NPCtoken20', 'NPCtoken21',
    'NPCtoken27', 'NPCtoken22', 'NPCtoken24', 'NPCtoken25', 'NPCtoken26', 'NPCtoken23',
    'NPCtoken32', 'NPCtoken31', 'NPCtoken34', 'NPCtoken35', 'NPCtoken36', 'NPCtoken38',
    'NPCtoken33', 'NPCtoken37'
]
#vendorItems last pulled from code in 2.12. Search for: ShopNames = function ()
vendorItems = {
    "W1 Town": "FoodHealth1 FoodHealth3 FoodHealth2 CraftMat3 FoodPotMana1 FoodPotOr1 FoodPotRe1 FoodPotGr1 OilBarrel1 StoneW1 StoneA1 StoneT1 EquipmentRings7 EquipmentStatues1 SmithingHammerChisel StampA5 StampA6 StampA3 InvBag104 InvStorage2 InvStorage6 InvStorage7 Quest86 rtt0 ResetFrag".split(' '),
    "Tiki Shop": "FoodHealth3 FoodHealth2 FoodHealth5 FoodPotOr2 FoodPotYe1 StoneA2 StampA12 EquipmentPendant12 Quest37 InvBag105 InvStorage8 InvStorage12 rtt0 ResetFrag".split(' '),
    "W2 Town": "FoodHealth6 FoodHealth7 FoodHealth4 Quest19 BobJoePickle StoneW2 StoneA2 StoneT2 FoodPotOr2 FoodPotGr2 FoodPotRe2 InvBag106 InvStorage9 InvStorage10 InvStorage13 InvStorage15 SmithingHammerChisel2 StampC11 rtt0 ResetFrag Quest87".split(' '),
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

def find_vendor_name(item_codename):
    for vendor_name, sold_items in vendorItems.items():
        if item_codename in sold_items:
            return vendor_name
#anvilItems last pulled from code in 2.12. Search for: ItemToCraftNAME = function ()
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
