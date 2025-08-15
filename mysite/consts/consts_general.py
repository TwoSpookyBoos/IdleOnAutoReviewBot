from consts.consts_autoreview import EmojiType
from utils.logging import get_logger
logger = get_logger(__name__)


current_world = 6
max_characters = 10

# Greenstacks
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
            "Refinery1", "Refinery2", "Refinery3", "Refinery4", "Refinery5", "Refinery6"
        ]
    },
    1: {
        "Printable Skilling Resources": [
            "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", "PalmTree", "StumpTree", "SaharanFoal",
            "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",
            "Fish1", "Fish2", "Fish3",
            "Bug1", "Bug2"
        ]
    },
    2: {
        "Printable Skilling Resources": [
            "Tree7", "AlienTree", "Tree8", "Tree9", "Tree11",
            "Starfire", "Marble",
            "Fish4", "Fish5", "Fish6", "Fish7",
            "Bug3", "Bug4", "Bug5", "Bug6", "Bug7", "Bug8"
        ],
        "Other Skilling Resources": [
            "CraftMat1"
        ],
        "Vendor Shops": [
            "FoodHealth14", "FoodHealth15"
        ]
    },
    3: {
        "Base Monster Materials": [
            "Grasslands1", "Grasslands2", "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3"
        ],
        "Printable Skilling Resources": [
            "Tree10",
            "Dreadlo",
            "Fish8", "Fish9", "Fish10",
            "Bug9", "Bug11"
        ],
        "Other Skilling Resources": [
            "CraftMat5"
        ],
        "Vendor Shops": [
            "FoodHealth12", "FoodHealth13"
        ]
    },
    4: {
        "Base Monster Materials": [
            "Sewers1", "Sewers2", "TreeInterior1", "TreeInterior2"
        ],
        "Printable Skilling Resources": [
            "Tree12",
            "Godshard",
            "Fish11", "Fish12", "Fish13",
            'Bug10', "Bug12", "Bug13"
        ],
        "Other Skilling Resources": [
            "CraftMat6", "Soul1"
        ],
        "Vendor Shops": [
            "FoodHealth16", "FoodHealth17",
            "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4"
        ]
    },
    5: {
        "Base Monster Materials": [
            "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4",
            "SnowA1", "SnowA2", "SnowA3"
        ],
        "Printable Skilling Resources": [
            "Tree13"
        ],
        "Other Skilling Resources": [
            "CraftMat7", "CraftMat9",
            "Critter1", "Critter2",
            "Soul2"
        ]
    },
    6: {
        "Base Monster Materials": [
            "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4",
            "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1", "GalaxyB2"
        ],
        "Other Skilling Resources": [
            "CraftMat8", "CraftMat10",
            "Critter3", "Critter4",
            "Soul3"
        ]
    },
    7: {
        "Base Monster Materials": [
            "SnowA4", "SnowC5",
            "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2", "GalaxyC3", "GalaxyC4"
        ],
        "Crystal Enemy Drops": [
            "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1"
        ],
        "Other Skilling Resources": [
            "CraftMat11",
            "Critter5",
            "Soul4"
        ]
    },
    8: {
        "Base Monster Materials": [
            "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5",
            "SpiA1", "SpiA2",
        ],
        "Crystal Enemy Drops": [
            "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3"
        ],
        "Other Skilling Resources": [
            "CraftMat12",
            "Critter6", "Critter7",
            "Soul5"
        ]
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
            "Soul6"
        ]
    },
    10: {
        "Base Monster Materials": [
             "SpiD1", "SpiD2", "SpiD3"
        ],
        "Crystal Enemy Drops": [
            "Leaf2",
            "Leaf3",
            "FoodPotMana4", "Leaf4",
            "FoodPotYe5", "Leaf5",
            "Leaf6"
        ],
        "Other Skilling Resources": [
            "Soul7",
            "CopperBar", "IronBar", "GoldBar", "PlatBar", "DementiaBar", "VoidBar",
            "FoodMining1", "FoodFish1", "FoodCatch1", "Bullet", "BulletB"
        ],
        "Vendor Shops": [
            "OilBarrel6", "OilBarrel7"
        ]
    },
    11: {
        "Missable Quest Items": [
            "Quest3", "Quest4", "Quest7", "Quest12",
            "Quest14", "Quest22", "Quest23", "Quest24",
            "Quest32"
        ],
        "Crystal Enemy Drops": [
            "FoodPotOr1"
        ],
        "Other Skilling Resources": [
            "LustreBar", "StarfireBar", "DreadloBar", "MarbleBar", "GodshardBar",
            "Critter10", "Critter11"
        ],
        "Rare Drops": [
            'Quest78'
        ]
    },
    12: {
        "Missable Quest Items": [
            "GoldricP1", "GoldricP2", "GoldricP3", "Quest21"
        ],
        "Base Monster Materials": [
            "Sewers3"
        ],
        "Crystal Enemy Drops": [
            "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",
        ],
        "Other Skilling Resources": [
            "Peanut", "Quest68", "Bullet3", "FoodChoppin1"  #I really hate that the Slush Bucket is listed as Quest68
        ],
        "Rare Drops": [
            "FoodPotRe1"
        ]
    },
    13: {
        "Base Monster Materials": [
            "Quest15", "Hgg"
        ],
        "Crystal Enemy Drops": [
            "EquipmentStatues1", "EquipmentStatues5",  #Power and Health statues are still more common than W2 statues
            "EquipmentStatues10", "EquipmentStatues12", "EquipmentStatues13", "EquipmentStatues8", "EquipmentStatues11",  #W2 statues
            "EquipmentStatues18",  #W3 EhExPee statue
            "EquipmentStatues20", "EquipmentStatues21", "EquipmentStatues22",  # W4 Statues
            "rtt0",
            "StoneA1", "StoneW1", "StoneZ1", "StoneT1",
            "StoneZ2", "StoneT2",
            "PureWater",
            "FoodG9"
        ],
        "Other Skilling Resources": [
            "EquipmentSmithingTabs2",
            'EquipmentSmithingTabs3',
            "PeanutG"
        ],
        "Rare Drops": [
            "FoodPotMana3", "ButterBar", "EquipmentStatues9", "OilBarrel2", "FoodPotRe2", "FoodPotGr3", "FoodHealth9",
            'EquipmentStatues29',  # Villager Statues from Caverns
        ]
    },
    14: {
        "Crystal Enemy Drops": [
            "StoneW2", 'ResetFrag', "SilverPen",
            "EquipmentStatues23", "EquipmentStatues24", "EquipmentStatues25",  # W5 Statues
        ],
        "Other Skilling Resources": [
            "FoodTrapping1", "FoodWorship1",
            "Ladle"
        ],
        "Rare Drops": [
            'Sewers1b',  #W1 Golden Plop
            'DesertC2b', 'DesertA3b',  #W2 Ghost and Nuget Cake
            'SnowC4a', 'SnowB2a',  #W3 Black Lense and Ice Age 3
            'EfauntDrop1',
            'EquipmentStatues15',  #Bullseye
            'EquipmentStatues16', 'EquipmentStatues17', 'EquipmentStatues19',  # W3 Statues
            'EquipmentStatues30'  # Dragon Warrior Statues from Caverns
        ]
    },
    15: {
        'Crystal Enemy Drops': [
            'StoneA2'
        ],
        "Other Skilling Resources": [
            "Critter1A", "Critter2A", "Critter3A", "Critter4A", "Critter5A",
            "Critter6A", "Critter7A", "Critter8A", "Critter9A", "Critter10A",
            "Critter11A"
        ],
        'Rare Drops': [
            'DesertA1b',  #W2 Glass Shard
            'SnowA2a',  #W3 Yellow Snowflake
            'GalaxyC1b', 'GalaxyA2b',  #W4 Pearler Shell + Lost Batteries
            'LavaA1b', 'LavaA5b', 'LavaB3b', 'Key5'  # W5 Rare Drops
        ]
    }
}
missable_gstacks_dict = {
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
expected_stackables = {
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
        "StoneT2", "StoneZ2",  "StoneW2", "StoneA2",  # W2 upgrade stones and Mystery2
        "PureWater", "EquipmentStatues18",  #W3 Slow drops = Distilled Water + EhExPee Statue
        "EquipmentStatues20", "EquipmentStatues21", "EquipmentStatues22",  # W4 Statues
        "EquipmentStatues23", "EquipmentStatues24", "EquipmentStatues25", "FoodG9",  #W5 Slow drops = Golden W5 Sammy + Statues
        # "FoodG11", "FoodG12"  #W6 gold foods
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
        'EquipmentStatues15',  #Bullseye
        'EquipmentStatues16', 'EquipmentStatues17', 'EquipmentStatues19',  # W3 Statues not from Crystals
        "FoodPotMana3",  #Decent Mana Potion from Bloques
        "FoodHealth9",  #Yeti Ham from Bop Box
        "OilBarrel2",  # Slime Barrel, 1 in 3334
        'Sewers1b',  # W1 Golden Plop
        "DesertC2b", 'DesertA3b', 'DesertA1b',  # W2 Ghost, Nuget Cake, Glass Shard
        "Quest78", 'SnowC4a', 'SnowB2a', 'SnowA2a',  # W3 Equinox Mirror, Black Lense, Ice Age 3, Yellow Snowflake
        'GalaxyC1b', 'GalaxyA2b',  #W4 Pearler Shell, Lost Batteries
        'LavaA1b', 'LavaA5b', 'LavaB3b', 'Key5',  # W5 Rare Drops
        "EfauntDrop1",  # Basic Efaunt material
        # "Key2", "Key3",  # Efaunt and Chizoar keys
        'EquipmentStatues29', 'EquipmentStatues30',  # Villager and Dragon Warrior statues from Caverns
    ],
    "Cheater": [
        "TreeInterior1b", "BabaYagaETC", "JobApplication",  # W1 Rare Drops
        "MidnightCookie",  # W2 Rare Drops
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
        "EquipmentStatues6",  # Kachow
        "FoodG1", "FoodG2", "FoodG3", "FoodG4", "FoodG5", "FoodG6", "FoodG7", "FoodG8", "FoodG10",  # Gold Foods
        "ResetCompleted", "ResetCompletedS", "ClassSwap",
        "ClassSwapB", "ResetBox",
    ]
}
greenstack_amount = 10 ** 7
gstackable_codenames = [item for items in expected_stackables.values() for item in items]
gstackable_codenames_expected = [
    item for items in list(expected_stackables.values())[:-1] for item in items
]
gstacks_rated_items = []
quest_items_codenames = expected_stackables["Missable Quest Items"]
for dg in greenstack_item_difficulty_groups:
    for category in greenstack_item_difficulty_groups[dg]:
        for item_name in greenstack_item_difficulty_groups[dg][category]:
            gstacks_rated_items.append(item_name)
gstack_rated_not_expected = [item for item in gstacks_rated_items if item not in gstackable_codenames_expected]
if len(gstack_rated_not_expected) > 0:
    logger.warning(f"Rated but not Expected Greenstacks found: {gstack_rated_not_expected}")
gstack_expected_not_rated = [item for item in gstackable_codenames_expected if item not in gstacks_rated_items]
if len(gstack_expected_not_rated) > 0:
    logger.warning(f"Expected but not Rated Greenstacks found: {gstack_expected_not_rated}")
gstack_unique_expected = set()
gstack_duplicate_expected = set()
for item_name in gstackable_codenames_expected:
    if item_name in gstack_unique_expected:
        gstack_duplicate_expected.add(item_name)
    else:
        gstack_unique_expected.add(item_name)
# if len(gstack_duplicate_expected) > 0:
# These 3 are expected as they're sold in Vendor Shops category + Rare Drops from enemies {'FoodPotGr3', 'FoodPotRe2', 'FoodHealth9'}
#     print(f"Reminder: Duplicate entries in GStack Expected list: {gstack_duplicate_expected}")

#Cards
max_card_stars = 5
key_cards = 'Cards0'
cards_max_level = 6
cardset_names = [
    "Blunder Hills", "Yum-Yum Desert", "Easy Resources",
    "Medium Resources", "Frostbite Tundra", "Hard Resources",
    "Hyperion Nebula", "Smolderin' Plateau", "Spirited Valley",
    "Dungeons", "Bosses n Nightmares", "Events"
]
card_raw_data = [
    [
        ["mushG", "A0", "5", "+{_Base_HP", "12"],
        ["mushR", "A1", "10", "+{_Base_LUK", "3"],
        ["frogG", "A2", "6", "+{_Base_MP", "10"],
        ["beanG", "A3", "7", "+{_Base_Damage", "7"],
        ["slimeG", "A4", "8", "+{_Base_WIS", "2"],
        ["snakeG", "A5", "9", "+{_Move_Spd", "1"],
        ["carrotO", "A6", "10", "+{_Base_AGI", "2"],
        ["goblinG", "A7", "10", "+{%_Total_HP", "2"],
        ["plank", "A8", "10", "+{_Base_STR", "2"],
        ["frogBIG", "A9", "10", "+{%_Card_Drop_Chance", "5"],
        ["poopSmall", "A10", "10", "+{%_Crystal_Mob_Spawn_Chance", "10"],
        ["ratB", "A11", "10", "+{%_Critical_Chance", "1"],
        ["branch", "A12", "10", "+{_Base_WIS", "5"],
        ["acorn", "A13", "10", "+{%_Money_from_Monsters", "5"],
        ["Crystal0", "A14", "3", "+{%_Total_Drop_Rate", "5"],
        ["mushW", "A16", "10", "+{%_Total_Accuracy", "5"]
    ],
    [
        ["jarSand", "B1", "10", "+{%_EXP_Conversion_from_Talent", "12"],
        ["mimicA", "B2", "10", "+{%_Total_Drop_Rate", "2"],
        ["crabcake", "B3", "10", "+{%_To_not_consume_Food", "5"],
        ["coconut", "B4", "10", "+{_Base_AGI", "5"],
        ["sandcastle", "B5", "10", "+{%_Total_Accuracy", "4"],
        ["pincermin", "B6", "10", "+{_Weapon_Power", "1"],
        ["potato", "B7", "10", "+{%_Critical_Damage", "3"],
        ["steak", "B8", "10", "+{_Base_STR", "5"],
        ["moonman", "B9", "10", "+{%_Monster_EXP_While_Active", "8"],
        ["sandgiant", "B10", "10", "+{%_Minimum_Damage", "2"],
        ["snailZ", "B11", "10", "+{%_Card_Drop_Chance", "8"],
        ["shovelR", "B12", "10", "+{_Base_LUK", "6"],
        ["Crystal1", "B13", "3", "+{%_EXP_from_monsters", "2"],
        ["Bandit_Bob", "B14", "1", "+{%_Money_from_Monsters", "1"],
        ["Blank", "A0", "10", "+{%", "3"],
        ["Blank", "A0", "10", "+{%", "3"]
    ],
    [
        ["Copper", "C1", "10", "+{_Base_accuracy", "4"],
        ["Iron", "C2", "10", "+{%_Total_Mining_Efficiency", "5"],
        ["Gold", "C3", "10", "+{%_Mining_EXP", "5"],
        ["ForgeA", "C16", "10", "+{%_Smithing_EXP_(Passive)", "4"],
        ["OakTree", "C4", "10", "+{_Base_Defence", "3"],
        ["BirchTree", "C5", "10", "+{%_Total_Choppin_Efficiency", "5"],
        ["JungleTree", "C6", "10", "+{%_Choppin_EXP", "5"],
        ["ForestTree", "C7", "10", "+{%_EXP_Conversion_from_Talent", "8"],
        ["Fish1", "C8", "10", "+{%_Total_MP", "3"],
        ["Fish2", "C9", "10", "+{%_Total_Fishing_Efficiency", "5"],
        ["Fish3", "C10", "10", "+{%_Fishing_EXP", "5"],
        ["Bug1", "C11", "10", "+{%_Monster_EXP_While_Active", "4"],
        ["Bug2", "C12", "10", "+{%_Total_Catching_Efficiency", "5"],
        ["Blank", "A0", "10", "+{%", "3"],
        ["Blank", "A0", "10", "+{%", "3"],
        ["Blank", "A0", "10", "+{%", "3"]
    ],
    [
        ["Plat", "D2", "10", "+{%_Mining_Away_Gains", "2"],
        ["Dementia", "D1", "10", "+{%_Mining_Speed", "4"],
        ["Void", "D3", "10", "+{%_Total_Mining_Efficiency", "6"],
        ["ForgeB", "D16", "10", "+{%_Smithing_EXP_(Passive)", "7"],
        ["PalmTree", "D7", "10", "+{%_Choppin_Away_Gains", "2"],
        ["ToiletTree", "D5", "10", "+{%_Choppin_Speed", "4"],
        ["StumpTree", "D6", "10", "+{%_Total_Accuracy", "3"],
        ["Fish4", "D11", "10", "+{%_Fishing_Away_Gains", "2"],
        ["Bug3", "D10", "10", "+{%_Catching_EXP", "5"],
        ["Bug4", "D9", "10", "+{%_Catching_Away_Gains", "2"],
        ["SoulCard1", "D17", "3", "+{%_Defence_from_Equipment", "3"],
        ["SoulCard2", "D18", "3", "+{_Starting_Pts_in_Worship", "4"],
        ["CritterCard1", "D19", "4", "+{%_Shiny_Critter_Chance", "3"],
        ["CritterCard2", "D20", "4", "+{%_Trapping_Efficiency", "5"],
        ["CritterCard3", "D21", "4", "+{%_Trapping_EXP", "5"],
        ["Blank", "A0", "10", "+{%", "3"]
    ],
    [
        ["sheep", "E0", "11", "+{%_Defence_from_Equipment", "3"],
        ["flake", "E1", "12", "+{_Base_STR", "7"],
        ["stache", "E2", "13", "+{%_Card_Drop_Chance", "9"],
        ["bloque", "E3", "14", "+{_Base_AGI", "7"],
        ["mamoth", "E4", "15", "+{%_Total_HP", "3.5"],
        ["snowball", "E5", "15", "+{%_Total_Damage", "3"],
        ["penguin", "E6", "15", "+{_Base_WIS", "7"],
        ["thermostat", "E7", "15", "+{%_Critical_Damage", "4"],
        ["glass", "E8", "17", "+{_Base_LUK", "7"],
        ["snakeB", "E9", "17", "+{%_MP_regen_rate", "5"],
        ["speaker", "E10", "17", "+{%_Total_Drop_Rate", "3.5"],
        ["eye", "E11", "17", "+{%_Total_Accuracy", "5"],
        ["ram", "E14", "20", "+{_Weapon_Power", "2"],
        ["skele", "E12", "15", "+{%_Critical_Chance", "1"],
        ["skele2", "E13", "15", "+{%_Total_Damage", "3"],
        ["Crystal2", "E15", "10", "+{%_EXP_from_monsters", "3"]
        ],
    [
        ["Lustre", "D4", "10", "+{%_Mining_Speed", "5"],
        ["Starfire", "F16", "12", "+{%_Mining_EXP", "8"],
        ["Dreadlo", "F29", "15", "+{%_Mining_Away_Gains", "3"],
        ["Godshard", "F39", "400", "+{%_Forge_Cap_and_SPD_(Passive)", "30"],
        ["SaharanFoal", "D8", "10", "+{%_Choppin_Away_Gains", "2.5"],
        ["Tree7", "F2", "10", "+{%_Choppin_Speed", "6"],
        ["AlienTree", "F13", "10", "+{%_Total_Choppin_Efficiency", "8"],
        ["Tree8", "F12", "10", "+{%_Choppin_Speed", "7"],
        ["Tree9", "F24", "12", "+{%_Choppin_Away_Gains", "3"],
        ["Tree10", "F25", "15", "+{%_Choppin_Speed", "8"],
        ["Tree12", "F34", "15", "+{%_Total_Choppin_Efficiency", "10"],
        ["Tree13", "F35", "15", "+{%_Choppin_Away_Gains", "4"],
        ["Fish5", "F20", "8", "+{%_Total_Fishing_Efficiency", "8"],
        ["Fish6", "F21", "10", "+{%_Fishing_Speed", "4"],
        ["Fish7", "F22", "10", "+{%_Fishing_EXP", "10"],
        ["Fish8", "F23", "10", "+{%_Fishing_Away_Gains", "3"],
        ["Bug5", "F8", "10", "+{%_Total_Catching_Efficiency", "7"],
        ["Bug6", "F9", "10", "+{%_Catching_Away_Gains", "2.5"],
        ["Bug7", "F14", "10", "+{%_Total_Catching_Efficiency", "8"],
        ["Bug8", "F15", "10", "+{%_Catching_Speed", "4"],
        ["Bug9", "F26", "12", "+{%_Total_Catching_Efficiency", "10"],
        ["Bug10", "F27", "15", "+{%_Catching_Away_Gains", "3"],
        ["Bug12", "F37", "15", "+{%_Total_Catching_Efficiency", "5"],
        ["Bug13", "F38", "15", "+{%_Catching_Speed", "5"],
        ["CritterCard4", "F4", "4", "+{%_Shiny_Critter_Chance", "5"],
        ["CritterCard5", "F5", "4", "+{%_EXP_from_monsters", "1.25"],
        ["CritterCard6", "F6", "5", "+{%_Shiny_Critter_Chance", "6"],
        ["CritterCard7", "F7", "6", "+{%_Skill_AFK_gain_rate", "1"],
        ["CritterCard8", "F17", "7", "+{%_Trapping_Efficiency", "7"],
        ["CritterCard9", "F18", "9", "+{%_Trapping_EXP", "8"],
        ["CritterCard10", "F19", "12", "+{%_Shiny_Critter_Chance", "8"],
        ["SoulCard3", "F3", "3", "+{_Starting_Pts_in_Worship", "6"],
        ["SoulCard4", "F10", "4", "+{%_Max_Charge", "7"],
        ["SoulCard5", "F11", "5", "+{%_Charge_Rate", "5"],
        ["SoulCard6", "F28", "7", "+{%_Max_Charge", "10"],
        ["SoulCard7", "F36", "7", "+{%_Charge_Rate", "7"],
        ["Fish9", "F30", "15", "+{%_Fishing_EXP", "15"],
        ["Fish10", "F31", "18", "+{%_Total_Fishing_Efficiency", "12"],
        ["Fish11", "F32", "24", "+{%_Fishing_Away_Gains", "3.5"],
        ["Fish12", "F33", "30", "+{%_Fishing_Speed", "7"]
    ],
    [
        ["mushP", "G1", "15", "+{%_Money_from_Monsters", "8"],
        ["w4a2", "G2", "17", "+{%_Breeding_EXP_(Passive)", "5"],
        ["w4a3", "G3", "18", "+{%_Defence_from_Equipment", "4"],
        ["demonP", "G4", "19", "+{%_Crystal_Mob_Spawn_Chance", "15"],
        ["w4b2", "G6", "20", "+{_Star_Talent_Pts_(Passive)", "5"],
        ["w4b1", "G5", "21", "+{_Base_WIS", "12"],
        ["w4b3", "G7", "22", "+{%_Lab_EXP_gain", "4"],
        ["w4b4", "G8", "23", "+{_Weapon_Power", "2.5"],
        ["w4b5", "G9", "24", "+{_Base_AGI", "12"],
        ["w4c1", "G10", "26", "+{%_Multikill_per_tier", "1.5"],
        ["w4c2", "G11", "27", "+{_Base_STR", "12"],
        ["w4c3", "G12", "28", "+{%_Critical_Chance_(Passive)", "1.5"],
        ["w4c4", "G13", "30", "+{%_All_Stat", "0.5"],
        ["Crystal3", "G14", "10", "+{px_Line_Width_(Passive)", "2"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"]
        ],
    [
        ["w5a1", "H1", "25", "+{%_Multikill_per_tier", "2"],
        ["w5a2", "H2", "28", "+{%_Defence_from_Equipment", "5"],
        ["w5a3", "H3", "32", "+{%_Total_Drop_Rate", "6"],
        ["w5a4", "H4", "35", "+{%_Skill_EXP_(Passive)", "5"],
        ["w5a5", "H5", "45", "+{%_Divinity_EXP_(Passive)", "6"],
        ["w5b1", "H6", "48", "+{%_Money_from_mobs_(Passive)", "7"],
        ["w5b2", "H7", "52", "+{_Weapon_Power_(Passive)", "1"],
        ["w5b3", "H8", "60", "+{%_Total_Damage", "4.5"],
        ["w5b4", "H9", "65", "+{%_EXP_from_monsters", "4"],
        ["w5b5", "H10", "70", "+{_Base_LUK", "15"],
        ["w5b6", "H11", "75", "+{%_Mining_Speed", "6"],
        ["w5c1", "H12", "80", "+{%_Sailing_Speed_(Passive)", "4"],
        ["w5c2", "H13", "100", "+{%_All_Stat", "1"],
        ["caveB", "H15", "5000", "+{%_Villager_EXP_(Passive)", "4"],
        ["caveC", "H16", "10000", "+{%_Total_Drop_Rate_(Passive)", "4"],
        ["Crystal4", "H14", "15", "+{%_Skill_Efficncy_(Passive)", "3"]
    ],
    [
        ["w6a1", "I1", "50", "+{%_Total_Damage", "5"],
        ["w6a2", "I2", "60", "+{%_DEF_from_Equips_(Passive)", "3"],
        ["w6a3", "I3", "75", "+{%_All_Stat", "1.5"],
        ["w6a4", "I4", "85", "+{%_Sneaking_EXP_(Passive)", "3"],
        ["w6a5", "I5", "100", "+{%_Multikill_per_tier", "3"],
        ["w6b1", "I6", "150", "+{%_Summoning_EXP_(Passive)", "3"],
        ["w6b2", "I7", "170", "+{%_Farming_EXP_(Passive)", "2"],
        ["w6b3", "I8", "200", "+{%_Skill_AFK_gain_rate", "2"],
        ["w6b4", "I9", "250", "+{%_Jade_Coin_gain_(Passive)", "4"],
        ["w6c1", "I10", "400", "+{%_Cooking_Spd_Multi_(Passive)", "5"],
        ["w6c2", "I11", "500", "+{_Base_LUK", "20"],
        ["w6d1", "I12", "900", "+{%_Fighting_AFK_(Passive)", "1"],
        ["w6d2", "I13", "1300", "+{%_Total_Drop_Rate", "8"],
        ["w6d3", "I14", "2500", "+{%_All_AFK_Gains(Passive)", "1.5"],
        ["Crystal5", "I15", "5000", "+{%_Sneaking_Stealth_(Passive)", "4"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"]
    ],
    [
        ["frogP", "X0", "1.5", "+{_Base_Dungeon_MP", "2"],
        ["frogD", "X1", "2", "+{%_Block_Chance", "2"],
        ["frogY", "X2", "2", "+{_Base_Dungeon_Damage", "1.5"],
        ["frogR", "X14", "2", "+{%_Dungeon_Card_Chance", "6"],
        ["frogW", "X15", "3", "+{%_Dungeon_Credits", "2.5"],
        ["frogGG", "X22", "5", "{%_to_start_with_RNG_orb_(Passive)", "20"],
        ["frogGR", "X3", "1.5", "{%_to_start_with_RNG_orb_(Passive)", "15"],
        ["frogGR2", "X4", "1.5", "+{%_Dungeon_Flurbos", "4"],
        ["frogGR3", "X5", "1.5", "+{%_Dungeon_Credits", "5"],
        ["frogGR4", "X21", "1", "+{%_Dungeon_Move_Speed", "7"],
        ["target", "X6", "2", "+{_Base_Dungeon_HP", "2"],
        ["rocky", "X7", "2", "+{%_Dungeon_Card_Chance", "8"],
        ["steakR", "X9", "2", "+{%_Dungeon_Money", "6"],
        ["totem", "X16", "2", "+{%_RNG_item_rarity", "10"],
        ["cactus", "X8", "2", "+{%_Dungeon_Boss_Dmg", "3"],
        ["potatoB", "X10", "5", "+{%_Dungeon_MP_regen", "5"],
        ["snakeZ", "X11", "1.5", "+{%_Dungeon_Drop_Rate", "4"],
        ["snakeZ2", "X12", "1.5", "+{%_Total_Dungeon_Dmg", "5"],
        ["snakeZ3", "X13", "1.5", "+{%_Dungeon_Flurbos", "5"],
        ["iceknight", "X17", "8", "+{%_Dungeon_MP_regen", "8"],
        ["iceBossZ", "X18", "2", "+{%_Dungeon_Card_Chance", "15"],
        ["iceBossZ2", "X19", "1.5", "+{%_Dungeon_Credits", "8"],
        ["iceBossZ3", "X20", "1.5", "+{%_Total_Dungeon_Dmg", "8"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"]
    ],
    [
        ["slimeB", "Z26", "2", "+{_Weapon_Power", "2"],
        ["babayaga", "Z0", "1.5", "+{%_Money_from_Monsters", "10"],
        ["poopBig", "Z1", "1.5", "+{%_Total_Damage", "5"],
        ["poopD", "A15", "1", "+{%_Fighting_AFK_gain_rate", "1"],
        ["wolfA", "Z2", "1.5", "+{%_Skill_AFK_gain_rate", "2.5"],
        ["wolfB", "Z4", "1.5", "+{%_Fighting_AFK_gain_rate", "2.5"],
        ["wolfC", "Z14", "10", "+{_Weapon_Power", "3"],
        ["babaHour", "Z5", "1.5", "+{%_Double_AFK_claim_chance", "3"],
        ["babaMummy", "Z6", "1.5", "+{%_Total_Drop_Rate", "6"],
        ["Boss2A", "Z3", "1.5", "+{%_EXP_from_monsters", "5"],
        ["Boss2B", "Z7", "1.5", "+{%_Skill_EXP", "3.75"],
        ["Boss2C", "Z15", "11", "+{_Star_Talent_Pts_(Passive)", "15"],
        ["mini3a", "Z12", "5", "+{%_Money_from_Monsters", "12"],
        ["Boss3A", "Z8", "1.5", "+{%_Cog_Build_Spd_(Passive)", "8"],
        ["Boss3B", "Z9", "1.5", "+{%_Shrine_Effects_(Passive)", "5"],
        ["Boss3C", "Z16", "12", "+{%_All_Stat", "1.5"],
        ["mini4a", "Z13", "5", "+{%_Cooking_EXP_gain", "6"],
        ["Boss4A", "Z10", "2", "+{%_Kitchen_Speed_(Passive)", "6"],
        ["Boss4B", "Z11", "2", "+{%_All_Skill_Efficiency", "10"],
        ["Boss4C", "Z17", "4", "+{%_Total_Damage", "7"],
        ["mini5a", "Z24", "4", "+{%_Total_Drop_Rate_(Passive)", "1.5"],
        ["Boss5A", "Z18", "3", "+{%_Sailing_Speed_(Passive)", "6"],
        ["Boss5B", "Z19", "4", "+{%_EXP_from_monsters", "8"],
        ["Boss5C", "Z20", "5", "+{%_Money_from_Monsters", "18"],
        ["mini6a", "Z25", "5", "+{%_Fighting_AFK_gain_rate", "2.5"],
        ["Boss6A", "Z21", "6", "+{%_Total_Drop_Rate", "12"],
        ["Boss6B", "Z22", "9", "+{%_Total_Damage_Multi", "8"],
        ["Boss6C", "Z23", "13", "+{%_Multikill_per_tier", "20"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"]
        ],
    [
        ["ghost", "Y0", "2", "+{%_Monster_EXP_While_Active", "3"],
        ["xmasEvent", "Y1", "1.5", "+{%_Total_Drop_Rate", "3"],
        ["xmasEvent2", "Y2", "1.5", "+{%_Money_from_Monsters", "3"],
        ["slimeR", "Y3", "2", "+{%_Defence_from_Equipment", "3"],
        ["loveEvent", "Y4", "1.5", "+{%_Total_HP", "5"],
        ["loveEvent2", "Y5", "1.5", "+{%_Boost_Food_Effect", "4"],
        ["loveEvent3", "Y15", "1.5", "+{%_EXP_from_monsters", "3"],
        ["sheepB", "Y6", "3", "+{%_MP_regen_rate", "3"],
        ["snakeY", "Y7", "3", "+{_Base_LUK", "3"],
        ["EasterEvent1", "Y8", "1.5", "+{%_Card_Drop_Chance", "1"],
        ["EasterEvent2", "Y9", "1.5", "+{%_Critical_Damage", "1"],
        ["shovelY", "Y13", "4", "+{_Base_Defence", "2"],
        ["crabcakeB", "Y10", "4", "+{%_Total_Drop_Rate", "3"],
        ["SummerEvent1", "Y11", "8", "+{%_Fishing_Away_Gains", "1"],
        ["SummerEvent2", "Y12", "8", "+{%_Catching_EXP", "4"],
        ["xmasEvent3", "Y14", "1", "+{%_Defence_from_Equipment", "3"],
        ["springEvent1", "Y16", "1", "+{%_Class_EXP_(Passive)", "2"],
        ["springEvent2", "Y17", "1", "+{%_All_Skill_EXP_(Passive)", "2"],
        ["fallEvent1", "Y18", "3", "+{_Star_Talent_Pts_(Passive)", "4"],
        ["anni4Event1", "Y19", "4", "+{%_Drop_Rate_(Passive)", "2"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"],
        ["Blank", "A0", "10", "+{%_Base_HP", "3"]
    ]
]
enemy_coded_names = {
    "Crystal0": "Crystal Carrot",
    "acorn": "Nutto",
    "beanG": "Bored Bean",
    "branch": "Walking Stick",
    "carrotO": "Carrotman",
    "frogBIG": "Gigafrog",
    "frogG": "Frog",
    "goblinG": "Glublin",
    "mushG": "Green Mushroom",
    "mushR": "Red Mushroom",
    "mushW": "Wood Mushroom",
    "plank": "Wode Board",
    "poopSmall": "Poop",
    "ratB": "Rat",
    "slimeG": "Slime",
    "snakeG": "Baby Boa",
    "Bandit_Bob": "Bandit Bob",
    "Crystal1": "Crystal Crabal",
    "coconut": "Mafioso",
    "crabcake": "Crabcake",
    "jarSand": "Sandy Pot",
    "mimicA": "Mimic",
    "moonman": "Moonmoon",
    "pincermin": "Pincermin",
    "potato": "Mashed Potato",
    "sandcastle": "Sand Castle",
    "sandgiant": "Sand Giant",
    "shovelR": "Dig Doug",
    "snailZ": "Snelbie",
    "steak": "Tyson",
    "BirchTree": "Bleach Logs",
    "Bug1": "Fly",
    "Bug2": "Butterfly",
    "Copper": "Copper Ore",
    "Fish1": "Goldfish",
    "Fish2": "Hermit Can",
    "Fish3": "Jellyfish",
    "ForestTree": "Forest Fibres",
    "ForgeA": "Fire Forge",
    "Gold": "Gold Ore",
    "Iron": "Iron Ore",
    "JungleTree": "Jungle Logs",
    "OakTree": "Oak Logs",
    "Bug3": "Sentient Cereal",
    "Bug4": "Fruitfly",
    "CritterCard1": "Froge",
    "CritterCard2": "Crabbo",
    "CritterCard3": "Scorpie",
    "Dementia": "Dementia Ore",
    "Fish4": "Bloach",
    "ForgeB": "Cinder Forge",
    "PalmTree": "Tropilogs",
    "Plat": "Platinum Ore",
    "SoulCard1": "Forest Soul",
    "SoulCard2": "Dune Soul",
    "StumpTree": "Veiny Logs",
    "ToiletTree": "Potty Rolls",
    "Void": "Void Ore",
    "Crystal2": "Crystal Cattle",
    "bloque": "Bloque",
    "eye": "Neyeptune",
    "flake": "Frost Flake",
    "glass": "Quenchie",
    "mamoth": "Mamooth",
    "penguin": "Penguin",
    "ram": "Dedotated Ram",
    "sheep": "Sheepie",
    "skele": "Xylobone",
    "skele2": "Bloodbone",
    "snakeB": "Cryosnake",
    "snowball": "Snowman",
    "speaker": "Bop Box",
    "stache": "Sir Stache",
    "thermostat": "Thermister",
    "AlienTree": "Alien Hive Chunk",
    "Bug10": "Dust Mote",
    "Bug12": "Ladybug",
    "Bug13": "Firefly",
    "Bug5": "Mosquisnow",
    "Bug6": "Flycicle",
    "Bug7": "Worker Bee",
    "Bug8": "Fairy",
    "Bug9": "Scarab",
    "CritterCard10": "Blobfish",
    "CritterCard4": "Mousey",
    "CritterCard5": "Owlio",
    "CritterCard6": "Pingy",
    "CritterCard7": "Bunny",
    "CritterCard8": "Dung Beat",
    "CritterCard9": "Honker",
    "Dreadlo": "Dreadlo Ore",
    "Fish10": "Shellfish",
    "Fish11": "Jumbo Shrimp",
    "Fish12": "Caulifish",
    "Fish5": "Skelefish",
    "Fish6": "Sand Shark",
    "Fish7": "Manta Ray",
    "Fish8": "Kraken",
    "Fish9": "Icefish",
    "Godshard": "Godshard Ore",
    "Lustre": "Lustre Ore",
    "SaharanFoal": "Tundra Logs",
    "SoulCard3": "Rooted Soul",
    "SoulCard4": "Frigid Soul",
    "SoulCard5": "Squishy Soul",
    "SoulCard6": "Oozie Soul",
    "SoulCard7": "Breezy Soul",
    "Starfire": "Starfire Ore",
    "Tree10": "Dandielogs",
    "Tree12": "Bamboo Logs",
    "Tree13": "Effervescent Logs",
    "Tree7": "Wispy Lumber",
    "Tree8": "Cubed Logs",
    "Tree9": "Maple Logs",
    "Crystal3": "Crystal Custard",
    "demonP": "Demon Genie",
    "mushP": "Purp Mushroom",
    "w4a2": "TV",
    "w4a3": "Donut",
    "w4b1": "Flying Worm",
    "w4b2": "Soda Can",
    "w4b3": "Gelatinous Cuboid",
    "w4b4": "Choccie",
    "w4b5": "Biggole Wurm",
    "w4c1": "Clammie",
    "w4c2": "Octodar",
    "w4c3": "Flombeige",
    "w4c4": "Stilted Seeker",
    "Crystal4": "Crystal Capybara",
    "w5a1": "Suggma",
    "w5a2": "Maccie",
    "w5a3": "Mister Brightside",
    "w5a4": "Cheese Nub",
    "w5a5": "Stiltmole",
    "w5b1": "Molti",
    "w5b2": "Purgatory Stalker",
    "w5b3": "Citringe",
    "w5b4": "Lampar",
    "w5b5": "Fire Spirit",
    "w5b6": "Biggole Mole",
    "w5c1": "Crawler",
    "w5c2": "Tremor Wurm",
    "caveB": "Gloomie Mushroom",
    "caveC": "Ancient Golem",
    "Crystal5": "Crystal Candalight",
    "w6a1": "Sprout Spirit",
    "w6a2": "Ricecake",
    "w6a3": "River Spirit",
    "w6a4": "Baby Troll",
    "w6a5": "Woodlin Spirit",
    "w6b1": "Bamboo Spirit",
    "w6b2": "Lantern Spirit",
    "w6b3": "Mama Troll",
    "w6b4": "Leek Spirit",
    "w6c1": "Ceramic Spirit",
    "w6c2": "Skydoggie Spirit",
    "w6d1": "Royal Egg",
    "w6d2": "Minichief Spirit",
    "w6d3": "Samurai Guardian",
    "cactus": "Cactopunk",
    "frogD": "Globohopper",
    "frogGG": "Eldritch Croaker",
    "frogGR": "Grandfrogger",
    "frogGR2": "Rotting Grandfrogger",
    "frogGR3": "Forlorn Grandfrogger",
    "frogGR4": "Vengeful Grandfrogger",
    "frogP": "Poisonic Frog",
    "frogR": "Lava Slimer",
    "frogW": "Chromatium Frog",
    "frogY": "King Frog",
    "iceBossZ": "Glaciaxus",
    "iceBossZ2": "Golden Glaciaxus",
    "iceBossZ3": "Caustic Glaciaxus",
    "iceknight": "Ice Guard",
    "potatoB": "Crescent Spud",
    "rocky": "Grumblo",
    "snakeZ": "Snakenhotep",
    "snakeZ2": "Enraged Snakenhotep",
    "snakeZ3": "Inevitable Snakenhotep",
    "steakR": "Beefie",
    "target": "Target",
    "totem": "Lazlo",
    "Boss2A": "Efaunt",
    "Boss2B": "Chaotic Efaunt",
    "Boss2C": "Gilded Efaunt",
    "Boss3A": "Chizoar",
    "Boss3B": "Chaotic Chizoar",
    "Boss3C": "Blighted Chizoar",
    "Boss4A": "Massive Troll",
    "Boss4B": "Chaotic Troll",
    "Boss4C": "Blitzkrieg Troll",
    "Boss5A": "Kattlekruk",
    "Boss5B": "Chaotic Kattlekruk",
    "Boss5C": "Sacrilegious Kattlekruk",
    "Boss6A": "Emperor",
    "Boss6B": "Chaotic Emperor",
    "Boss6C": "Sovereign Emperor",
    "babaHour": "Biggie Hours",
    "babaMummy": "King Doot",
    "babayaga": "Baba Yaga",
    "mini3a": "Dilapidated Slush",
    "mini4a": "Mutated Mush",
    "poopBig": "Dr Defecaus",
    "poopD": "Boop",
    "wolfA": "Amarok",
    "wolfB": "Chaotic Amarok",
    "wolfC": "Radiant Amarok",
    "mini5a": "Domeo Magmus",
    "mini6a": "Demented Spiritlord",
    "slimeB": "Glunko The Massive",
    "EasterEvent1": "Egggulyte",
    "EasterEvent2": "Egg Capsule",
    "SummerEvent1": "Coastiolyte",
    "SummerEvent2": "Summer Spirit",
    "crabcakeB": "Mr Blueberry",
    "fallEvent1": "Falloween Pumpkin",
    "ghost": "Ghost (Event)",
    "loveEvent": "Loveulyte",
    "loveEvent2": "Chocco Box",
    "loveEvent3": "Giant Rose",
    "sheepB": "Floofie",
    "shovelY": "Plasti Doug",
    "slimeR": "Valentslime",
    "snakeY": "Shell Snake",
    "springEvent1": "Bubbulyte",
    "springEvent2": "Spring Splendor",
    "xmasEvent": "Giftmas Blobulyte",
    "xmasEvent2": "Meaning of Giftmas",
    "xmasEvent3": "Golden Giftmas Box",
    "anni4Event1": "IdleOn 4th Anniversary",
}

#Inventory, Storage, Consumables
inventory_bags_dict = {
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
    112:8,
    113:1,
    114:1
}
storage_chests_dict = {
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
    106:16,
    107:16
}
current_max_usable_inventory_slots = 104  #As of v2.36 Charred Bones

#Gem Shop
gem_shop_dict = {
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
}
gem_shop_optlacc_dict = {
    'Dragonic Liquid Cauldron': [123, 4],
    'Equinox Pingy': [320, EmojiType.INFINITY.value],
    'Rupie Slug': [355, EmojiType.INFINITY.value],
    'Exalted Stamps': [366, EmojiType.INFINITY.value],
    'Lifetime Tickets': [382, EmojiType.INFINITY.value]
}
gem_shop_bundles_dict = {
    # Names of the bundles aren't stored, but descriptions can be found in Source Code: GemPopupBundleMessages = function ()
    'bun_a': 'Lava Supporter Pack',
    'bun_b': 'New Year Pack',
    'bun_c': 'Starter Pack',
    'bun_d': 'Easter Bundle',
    'bun_e': 'Totally Chill Pack',
    'bun_f': 'Summer Bundle',
    'bun_g': 'Dungeon Bundle',
    'bun_h': 'Giftmas Bundle',
    'bun_i': 'Auto-Loot Pack',
    'bun_j': 'Outta This World Pack',
    'bun_k': 'Eggscellent Pack',
    'bun_l': 'Super Hot Fire Pack',
    'bun_m': 'Gem Motherlode Pack',
    'bun_n': 'Riftwalker Pack',
    'bun_o': "Bloomin' Pet Pack",
    'bun_p': 'Island Explorer Pack',
    'bun_q': 'Equinox Pack',
    'bun_r': 'Calm Serenity Pack',
    'bun_s': 'Sacred Methods Pack',
    'bun_t': 'Timeless Pack',
    'bun_u': 'Ancient Echos Pack',
    'bun_v': 'Deathbringer Pack',
    'bun_w': 'Windwalker Pack',
    'bun_y': 'Valenslime Day Pack',
    'bun_z': 'Fallen Spirits Pet Pack',
    'bon_a': 'Storage Ram Pack',
    # No bon_b, yet as of 2.36.0
    'bon_c': 'Blazing Star Anniversary Pack',
    'bon_d': 'Midnight Tide Anniversary Pack',
    'bon_e': 'Lush Emerald Anniversary Pack',
    'bon_f': 'Eternal Hunter Pack',
    'bon_g': 'Gilded Treasure',
}  # As of 2.38.0

#Guild
guild_bonuses_dict = {
    'Guild Gifts': {'Image': 'guild-gifts', 'Max Level': 100, 'Max Value': 350, 'funcType': 'decay', 'x1': 700, 'x2': 100},
    'Stat Runes': {'Image': 'stat-runes', 'Max Level': 50, 'Max Value': 20, 'funcType': 'decay', 'x1': 40, 'x2': 50},
    'Rucksack': {'Image': 'rucksack', 'Max Level': 50, 'Max Value': 35, 'funcType': 'decay', 'x1': 70, 'x2': 50},
    'Power of Pow': {'Image': 'power-of-pow', 'Max Level': 50, 'Max Value': 5, 'funcType': 'decay', 'x1': 10, 'x2': 50},
    'REM Fighting': {'Image': 'rem-fighting', 'Max Level': 50, 'Max Value': 5, 'funcType': 'decay', 'x1': 10, 'x2': 50},
    'Make or Break': {'Image': 'make-or-break', 'Max Level': 50, 'Max Value': 15, 'funcType': 'decay', 'x1': 30, 'x2': 50},
    'Multi Tool': {'Image': 'multi-tool', 'Max Level': 50, 'Max Value': 15, 'funcType': 'decay', 'x1': 30, 'x2': 50},
    'Sleepy Skiller': {'Image': 'sleepy-skiller', 'Max Level': 50, 'Max Value': 5, 'funcType': 'decay', 'x1': 10, 'x2': 50},
    'Coin Supercharger': {'Image': 'coin-supercharger', 'Max Level': 100, 'Max Value': 16.667, 'funcType': 'decay', 'x1': 20, 'x2': 20},
    'Bonus GP for small guilds': {'Image': 'bonus-gp-for-small-guilds', 'Max Level': 50, 'Max Value': 0, 'funcType': 'special1', 'x1': 200, 'x2': 50},  # This value decreases to a min value of 0
    'Gold Charm': {'Image': 'gold-charm', 'Max Level': 50, 'Max Value': 20, 'funcType': 'decay', 'x1': 40, 'x2': 50},
    'Star Dazzle': {'Image': 'star-dazzle', 'Max Level': 50, 'Max Value': 60, 'funcType': 'decay', 'x1': 120, 'x2': 50},
    'C2 Card Spotter': {'Image': 'c2-card-spotter', 'Max Level': 50, 'Max Value': 30, 'funcType': 'decay', 'x1': 60, 'x2': 50},
    'Bestone': {'Image': 'bestone', 'Max Level': 50, 'Max Value': 8, 'funcType': 'decay', 'x1': 16, 'x2': 50},
    'Skilley Skillet': {'Image': 'skilley-skillet', 'Max Level': 200, 'Max Value': 18.75, 'funcType': 'decay', 'x1': 30, 'x2': 120},
    'Craps': {'Image': 'craps', 'Max Level': 50, 'Max Value': 14, 'funcType': 'decay', 'x1': 28, 'x2': 50},
    'Anotha One': {'Image': 'anotha-one', 'Max Level': 50, 'Max Value': 13, 'funcType': 'decay', 'x1': 26, 'x2': 50},
    'Wait A Minute': {'Image': 'wait-a-minute', 'Max Level': 0, 'Max Value': 0, 'funcType': 'add', 'x1': 1, 'x2': 0}
}

#Family Bonuses
family_bonus_class_tier_level_reductions = [9, 29, 69, 999]  #Character must be this high of a level to get bonuses
family_bonuses_dict = {
    #"Beginner": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Journeyman": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Luck', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Maestro": {'funcType': 'decay', 'x1': 6, 'x2': 100, 'Stat': 'Printer Sample Rate', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[1]},
    "Voidwalker": {'funcType': 'decay', 'x1': 5, 'x2': 250, 'Stat': 'Fighting AFK Gains', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[2]},
    #"Infinilyte": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    #"Rage Basics": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Warrior": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Strength', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Barbarian": {'funcType': 'decay', 'x1': 25, 'x2': 100, 'Stat': 'Weapon Power', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[1]},
    "Squire": {'funcType': 'decay', 'x1': 40, 'x2': 100, 'Stat': 'Total HP', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[1]},
    "Blood Berserker": {'funcType': 'decay', 'x1': 20, 'x2': 180, 'Stat': 'Total Damage', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[2]},
    #"Death Bringer": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Divine Knight": {'funcType': 'decay', 'x1': 50, 'x2': 150, 'Stat': 'Refinery Speed', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[2]},
    #"Royal Guardian": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    #"Calm Basics": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Archer": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Agility', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Bowman": {'funcType': 'decay', 'x1': 38, 'x2': 100, 'Stat': 'EXP when fighting monsters actively', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[1]},
    "Hunter": {'funcType': 'decay', 'x1': 30, 'x2': 100, 'Stat': 'Efficiency for all skills', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[1]},
    "Siege Breaker": {'funcType': 'decay', 'x1': 20, 'x2': 170, 'Stat': 'Faster Minimum Boat Travel Time', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[2]},
    #"Mayheim": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    #"Wind Walker": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Beast Master": {'funcType': 'decay', 'x1': 5, 'x2': 180, 'Stat': 'All Skill AFK Gains', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[2]},
    #"Savvy Basics": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Mage": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 5, 'Stat': 'Total Wisdom', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Wizard": {'funcType': 'intervalAdd', 'x1': 1, 'x2': 6, 'Stat': 'Star Talent Points', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[1]},
    "Shaman": {'funcType': 'decayMulti', 'x1': 0.4, 'x2': 100, 'Stat': 'Higher Bonuses from Golden Foods', 'PrePlus': False, 'PostDisplay': 'x', 'levelDiscount': family_bonus_class_tier_level_reductions[1]},
    "Elemental Sorcerer": {'funcType': 'decay', 'x1': 20, 'x2': 350, 'Stat': 'Lv For All Talents Above Lv 1', 'PrePlus': True, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[2]},
    #"Spiritual Monk": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
    "Bubonic Conjuror": {'funcType': 'decay', 'x1': 5, 'x2': 180, 'Stat': 'All Stat. STR, AGI, WIS, LUK.', 'PrePlus': True, 'PostDisplay': '%', 'levelDiscount': family_bonus_class_tier_level_reductions[2]},
    #"Arcane Cultist": {'funcType': 'decay', 'x1': 0, 'x2': 0, 'Stat': '', 'PrePlus': False, 'PostDisplay': '', 'levelDiscount': family_bonus_class_tier_level_reductions[0]},
}
esFamilyBonusBreakpointsList = [0, 88, 108, 131, 157, 186, 219, 258, 303, 356, 419, 497, 594, 719, 885, 1118, 1468, 2049, 3210, 6681, 1272447]
arbitrary_es_family_goal = esFamilyBonusBreakpointsList[13]  #719 fairly feasible in v2.12, 885 feels too tough atm
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
        return esFamilyBonusBreakpointsList[result + 1]
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
equipment_by_bonus_dict = {
    'DropRate': {
        # Weapons
        'Mittens of the Gods': {'Type': 'Fisticuffs', 'Limited': False, 'Misc1': {'Bonus': 'Damage', 'Value': 120}, 'Misc2': {'Bonus': 'DropRate', 'Value': 40}, 'Image': 'mittens-of-the-gods'},
        'Massive Godbreaker': {'Type': 'Spear', 'Limited': False, 'Misc1': {'Bonus': 'Damage', 'Value': 60}, 'Misc2': {'Bonus': 'DropRate', 'Value': 20}, 'Image': 'massive-godbreaker'},
        'Doublestring Godshooter': {'Type': 'Bow', 'Limited': False, 'Misc1': {'Bonus': 'Damage', 'Value': 60}, 'Misc2': {'Bonus': 'DropRate', 'Value': 20}, 'Image': 'doublestring-godshooter'},
        'Magnifique Godcaster': {'Type': 'Wand', 'Limited': False, 'Misc1': {'Bonus': 'Damage', 'Value': 60}, 'Misc2': {'Bonus': 'DropRate', 'Value': 20}, 'Image': 'magnifique-godcaster'},
        # Tools
        'Destroyer of the Mollo Gomme': {'Type': 'Pickaxe', 'Limited': False, 'Misc1': {'Bonus': 'MiningEff', 'Value': 35}, 'Misc2': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'destroyer-of-the-mollo-gomme'},
        'Annihilator of the Yggdrasil': {'Type': 'Hatchet', 'Limited': False, 'Misc1': {'Bonus': 'ChoppingEff', 'Value': 12}, 'Misc2': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'annihilator-of-the-yggdrasil'},
        'Angler of the Iliunne': {'Type': 'Rod', 'Limited': False, 'Misc1': {'Bonus': 'FishingEff', 'Value': 12}, 'Misc2': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'angler-of-the-iliunne'},
        'Wrangler of the Qoxzul': {'Type': 'Net', 'Limited': False, 'Misc1': {'Bonus': 'CatchingEff', 'Value': 12}, 'Misc2': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'wrangler-of-the-qoxzul'},
        'Containment of the Zrgyios': {'Type': 'Trap', 'Limited': False, 'Misc1': {'Bonus': 'AfkGain', 'Value': 4}, 'Misc2': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'containment-of-the-zrgyios'},
        # Helmets
        '3rd Anniversary Ice Cream Topper': {'Type': 'Helmet', 'Limited': True, 'Misc1': {'Bonus': 'MonsterXp', 'Value': 4}, 'Misc2': {'Bonus': 'DropRate', 'Value': 3}, 'Image': 'x3rd-anniversary-ice-cream-topper'},
        'Efaunt Helmet': {'Type': 'Helmet', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 5}, 'Image': 'efaunt-helmet'},
        'Skulled Helmet of the Divine': {'Type': 'Helmet', 'Limited': False, 'Misc1': {'Bonus': 'Damage', 'Value': 30}, 'Misc2': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'skulled-helmet-of-the-divine'},
        'Crown of the Gods': {'Type': 'Helmet', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 15}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 22}, 'Image': 'crown-of-the-gods'},
        'Emperor Kabuto': {'Type': 'Helmet', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 25}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 30}, 'Image': 'emperor-kabuto'},
        # Pendants
        'Chaotic Amarok Pendant': {'Type': 'Pendant', 'Limited': False, 'Misc1': {'Bonus': 'Damage', 'Value': 20}, 'Misc2': {'Bonus': 'DropRate', 'Value': 5}, 'Image': 'chaotic-amarok-pendant'},
        # Chests
        'Robe of the Gods': {'Type': 'Chest', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 30}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 16}, 'Image': 'robe-of-the-gods'},
        'Emperor Sokutai Ho': {'Type': 'Chest', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 40}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 25}, 'Image': 'emperor-sokutai-ho'},
        # Legs
        'Tatters of the Gods': {'Type': 'Legs', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 25}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 14}, 'Image': 'tatters-of-the-gods'},
        'Emperor Zubon': {'Type': 'Legs', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 35}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 20}, 'Image': 'emperor-zubon'},
        # Feet
        'Devious Slippers of the Divine': {'Type': 'Feet', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 15}, 'Misc2': {'Bonus': 'Damage', 'Value': 8}, 'Image': 'devious-slippers-of-the-divine'},
        'Drip of the Gods': {'Type': 'Feet', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 30}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 12}, 'Image': 'drip-of-the-gods'},
        'Emperor Geta': {'Type': 'Feet', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 40}, 'Misc2': {'Bonus': 'MultikillPerTier', 'Value': 20}, 'Image': 'emperor-geta'},
        # Premium Hats
        'Siege Captain Cap': {'Type': 'Premium Hat', 'Limited': True, 'Misc1': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'siege-captain-cap'},
        'Goldberry': {'Type': 'Premium Hat', 'Limited': True, 'Misc1': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'goldberry'},
        # Trophies
        'Lucky Lad': {'Type': 'Trophy', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 7}, 'Image': 'lucky-lad'},
        'Luckier Lad': {'Type': 'Trophy', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 50}, 'Misc2': {'Bonus': 'PercentLuck', 'Value': 5}, 'Image': 'luckier-lad'},
        'One of the Divine': {'Type': 'Trophy', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 42}, 'Misc2': {'Bonus': 'Damage', 'Value': 35}, 'Image': 'one-of-the-divine'},
        # Capes
        'Molten Cloak': {'Type': 'Cape', 'Limited': True, 'Misc1': {'Bonus': 'DropRate', 'Value': 30}, 'Image': 'molten-cloak'},
        'Gilded Emperor Wings': {'Type': 'Cape', 'Limited': False, 'Misc1': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'gilded-emperor-wings'},
        'Chains of the Gilded Vaultguard': {'Type': 'Cape', 'Limited': True, 'Misc1': {'Bonus': 'ClassExpMulti', 'Value': 100}, 'Misc2': {'Bonus': 'DropRateMulti', 'Value': 40}, 'Image': 'chains-of-the-gilded-vaultguard'},
        # Nametags
        '3rd Anniversary IdleOn Nametag': {'Type': 'Nametag', 'Limited': True, 'Misc1': {'Bonus': 'AfkGain', 'Value': 3}, 'Misc2': {'Bonus': 'DropRate', 'Value': 3}, 'Image': 'x3rd-anniversary-idleon-nametag'},
        'Balling Nametag': {'Type': 'Nametag', 'Limited': True, 'Misc1': {'Bonus': 'DropRate', 'Value': 40}, 'Image': 'balling-nametag'},
        'Aethermoon Nametag': {'Type': 'Nametag', 'Limited': True, 'Misc1': {'Bonus': 'AfkGain', 'Value': 80}, 'Misc2': {'Bonus': 'DropRate', 'Value': 10}, 'Image': 'aethermoon-nametag'},
        'Deadbones Nametag': {'Type': 'Nametag', 'Limited': True, 'Misc1': {'Bonus': 'DropRateMulti', 'Value': 25}, 'Misc2': {'Bonus': 'DropRate', 'Value': 35}, 'Image': 'deadbones-nametag'},
        'Treasure Nametag': {'Type': 'Nametag', 'Limited': True, 'Misc1': {'Bonus': 'DropRate', 'Value': 25}, 'Misc2': {'Bonus': 'Money', 'Value': 25}, 'Image': 'treasure-nametag'},
        # Attire
        'Cobalt Robe':    {'Type': 'Attire', 'Limited': True, 'Misc1': {'Bonus': 'Damage', 'Value': 100}, 'Misc2': {'Bonus': 'DropRate', 'Value': 60}, 'Image': 'cobalt-robe'},
        'Evergreen Robe': {'Type': 'Attire', 'Limited': True, 'Misc1': {'Bonus': 'ClassXp', 'Value': 100}, 'Misc2': {'Bonus': 'DropRate', 'Value': 75}, 'Image': 'evergreen-robe'},
        # Keychains
        'Relic Chain': {'Type': 'Keychain', 'Limited': False, 'Note': 'Relic can roll up to +16% total Drop Rate<br>All other Tier 2 keychains can only roll up to +8% Drop Rate', 'Misc1': {'Bonus': 'DropRate', 'Value': 16}, 'Image': 'relic-chain'}
    }
}

def decode_enemy_name(coded_name: str) -> str:
    decoded_name = enemy_coded_names.get(coded_name, f"Unknown-{coded_name}")
    if decoded_name.startswith('Unknown'):
        logger.warning(f"Unknown enemy code name: {coded_name}")
    return decoded_name
