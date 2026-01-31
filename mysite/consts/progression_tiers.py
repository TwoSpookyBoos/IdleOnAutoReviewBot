from consts.consts_w3 import dreams_that_unlock_new_bonuses, library_subgroup_tiers, old_library_subgroup_tiers, max_trapping_critter_types
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)

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
    [31, 4000, f'{{{{Advice For Money|#advice-for-money}}}} - Unlock \"Advice On Life And Death\"', None, None, None],
    [32, 4300, f'{{{{Advice For Money|#advice-for-money}}}} - Unlock \"Advice On Being Tired\"', None, None, None],
    [32, 4600, f'{{{{Advice For Money|#advice-for-money}}}} - Unlock \"Advice On Sleeping\"', None, None, None],
    [33, 4855, "Unlock all Tome challenges", 500, "Credit towards Equinox Dream 23", ""],
    [34, 5000, "Family - Sparkle Obol Slot 4", 500, "Credit towards Equinox Dream 23", ""],
    [35, 5050, f'{{{{Advice For Money|#advice-for-money}}}} - Unlock \"Advice On Murder One\"', None, None, None],
    [36, 5600, f'{{{{Advice For Money|#advice-for-money}}}} - Unlock \"Advice On Being Smart\"', None, None, None],
    [37, 6250, f'{{{{Advice For Money|#advice-for-money}}}} - Unlock \"Advice On Materialism\"', None, None, None],
]
secret_class_progressionTiers = {
    0: {},
    1: {
        'Required Class': 'Journeyman'
    },
    2: {
        'Required Class': 'Maestro'
    },
    3: {
        'Required Class': 'Voidwalker'
    },
    4: {
        'No Catchup Needed': True
    }
}
gemShop_progressionTiers = [
    # int tier, str tierName, dict recommendedPurchases, str notes
    [0, "", {}, ""],
    [1, "S", {
        'Infinity Hammer': 1, 'Bleach Liquid Cauldrons': 1, 'Crystal 3D Printer': 1, 'Richelin Kitchen': 1, 'Divinity Sparkie': 1, 'Instagrow Generator': 1,
        'Extra Card Slot': 4},
     ""],
    [2, "A", {
        'Item Backpack Space': 1, 'Storage Chest Space': 2, 'Carry Capacity': 2, 'Weekly Dungeon Boosters': 1,
        'Bleach Liquid Cauldrons': 2, 'Zen Cogs': 2, 'Tower Building Slots': 1,
        'Royal Egg Cap': 3, 'Souped Up Tube': 1,
        'Chest Sluggo': 2, 'Divinity Sparkie': 2, 'Lava Sprouts': 1,
        'Conjuror Pts': 1,
        'Instagrow Generator': 3, 'Shroom Familiar': 1, 'Plot Of Land': 2},
     ""],
    [3, "B", {
        'Item Backpack Space': 2, 'Storage Chest Space': 4, 'Carry Capacity': 4, 'Weekly Dungeon Boosters': 2, 'Food Slot': 1,
        'Bleach Liquid Cauldrons': 3, 'More Sample Spaces': 2, 'Zen Cogs': 4, 'Tower Building Slots': 2,
        'Royal Egg Cap': 5, 'Fenceyard Space': 2, 'Chest Sluggo': 6,
        'Parallel Villagers The Engineer': 1, 'Parallel Villagers The Conjuror': 1, 'Conjuror Pts': 3,
        'Plot Of Land': 4, 'Instagrow Generator': 5},
     ""],
    [4, "C", {
        'Item Backpack Space': 3, 'Storage Chest Space': 8, 'Carry Capacity': 6, 'Weekly Dungeon Boosters': 3, 'Food Slot': 2,
        'Bleach Liquid Cauldrons': 4, 'More Sample Spaces': 4, 'Tower Building Slots': 4,
        'Fenceyard Space': 4, 'Chest Sluggo': 9,
        'Parallel Villagers The Explorer': 1, 'Parallel Villagers The Measurer': 1, 'Parallel Villagers The Librarian': 1, 'Resource Boost': 2, 'Conjuror Pts': 6,
        'Plot Of Land': 6, 'Shroom Familiar': 2, 'Instagrow Generator': 7},
     ""],
    [5, "D", {
        'Item Backpack Space': 4, 'Carry Capacity': 8,
        'Ivory Bubble Cauldrons': 4, 'More Sample Spaces': 6, 'Zen Cogs': 8,
        'Souped Up Tube': 3, 'Fenceyard Space': 6, 'Chest Sluggo': 12,
        'Resource Boost': 4, 'Conjuror Pts': 12, 'Opal': 8,
        'Plot Of Land': 8, 'Instagrow Generator': 8,
    },
     ""],
    [6, "Practical Max", {
        'Item Backpack Space': 6, 'Storage Chest Space': 12, 'Carry Capacity': 10, 'More Storage Space': 10, 'Card Presets': 1,
        'Brimstone Forge Slot': 16,
        'Fluorescent Flaggies': 2, 'Burning Bad Books': 4,
        'Golden Sprinkler': 1, 'Divinity Sparkie': 6, 'Lava Sprouts': 6,
        'Resource Boost': 10, 'Conjuror Pts': 12, 'Opal': 20,
        'Parallel Villagers The Engineer': 1, 'Parallel Villagers The Conjuror': 1, 'Parallel Villagers The Explorer': 1, 'Parallel Villagers The Measurer': 1,
        'Plot Of Land': 12, 'Shroom Familiar': 6,
    },
     "I wouldn't recommend going any further as of v2.26."],
    [7, "True Max",
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
        'Crystal 3D Printer': 1, 'More Sample Spaces': 6, 'Burning Bad Books': 4, 'Prayer Slots': 4,
        'Zen Cogs': 8, 'Cog Inventory Space': 20, 'Tower Building Slots': 4, 'Fluorescent Flaggies': 6,
        #World 4
        'Royal Egg Cap': 5, 'Richelin Kitchen': 10, 'Souped Up Tube': 5, 'Pet Storage': 12, 'Fenceyard Space': 6,
        #World 5
        'Chest Sluggo': 12, 'Divinity Sparkie': 6, 'Golden Sprinkler': 4, 'Lava Sprouts': 6,
        #Caverns
        'Resource Boost': 10, 'Conjuror Pts': 12, 'Opal': 60,
        #World 6
        'Plot Of Land': 12, 'Shroom Familiar': 6, 'Instagrow Generator': 8,
     },
     "This final tier is for the truly depraved. Many of these bonuses are very weak or outright useless."]
]
greenstack_progressionTiers = {
    1: {'Dream Number': 1, 'Required Stacks': 20},
    2: {'Dream Number': 12, 'Required Stacks': 75},
    3: {'Dream Number': 29, 'Required Stacks': 200},
    4: {'Required Stacks': 250},
    5: {'Required Stacks': 320}
}
achievements_progressionTiers = {
    0: {},
    1: {
        'EZ Access': {
            'Platinum 200G': {'World': 1, 'Reward': 'W1 Key', 'Rating': ''},
            'Half a Mill-log': {'World': 1, 'Reward': 'W1 Colo and Shops', 'Rating': ''},
            'Super Cereal': {'World': 2, 'Reward': 'W2 Colo and Shops', 'Rating': ''},
            'Skill Master': {'World': 2, 'Reward': 'W2 Key', 'Rating': ''},
            'Cool Score!': {'World': 3, 'Reward': 'W3 Colo and Shop', 'Rating': ''},
        },
        'Monster Respawn': {},
        'Recipes': {
            'Based Roots': {'World': 1, 'Reward': 'Acorn Hat', 'Rating': ''},
        },
        'Dungeon RNG Items': {
            '2 Tons of Iron': {'World': 1, 'Reward': 'Golden Dice', 'Rating': ''},
            'House Flipper': {'World': 1, 'Reward': 'Horn of the Foal', 'Rating': ''},
            "Croakin' Froge": {'World': 3, 'Reward': 'Plump Dice', 'Rating': ''},
        },
        'Other Nice Rewards': {
            # 'Golden Fly': {'World': 2, 'Reward': '5% Catching Efficiency', 'Rating': ''},
            'Cog in the System': {'World': 3, 'Reward': '5% cons build speed', 'Rating': ''},
        },
    },
    2: {
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
    3: {
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
    4: {
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
bribes_progressionTiers = {
    1: {
        'W1': [
            "Insider Trading", "Tracking Chips", "Mandatory Fire Sale",
            "Sleeping On the Job", "Artificial Demand", "The Art of the Deal"
        ],
    },
    2: {
        'W2': [
            "Overstock Regulations", "Double EXP Scheme", "Tagged Indicators",
            "Fossil Fuel Legislation", "Five Aces in the Deck", "Fake Teleport Tickets",
            "The Art of the Steal"
        ],
    },
    3: {
        'W3': [
            "Counterfeit Telepassports", "Weighted Marbles", "Changing the Code",
            "Taxidermied Cog Pouches", "Guild VIP Fraud", "Library Double Agent",
            "The Art of the Fail"
        ],
    },
    4: {
        'W4': [
            "Photoshopped Dmg Range", "Glitched Acc Formula", "Firewalled Defence",
            "Bottomless Bags", "AFKeylogging", "Guild GP Hack"
        ],
    },
    5: {
        'Trash Island': [
            "The Art of the Bail",
            "Random Garbage", "Godlier Creation", "Fishermaster",
            "Muscles on Muscles", "Bottle Service", "Star Scraper"
        ],
    },
    6: {
        'W6': [
            "The Art of the Grail",
            "Artifact Pilfering", "Forge Cap Smuggling", "Gold from Lead",
            "Nugget Fabrication", "Divine PTS Miscounting", "Loot Table Tampering",
            #  "The Art of the Flail"  #Cannot be purchased as of 2.36
        ]
    },

}
stamps_progressionTiers = {
    0: {'Total Stamp Levels': 0, 'Stamps': {}},
    1: {'Total Stamp Levels': 50, 'Stamps': {}},
    2: {'Total Stamp Levels': 100, 'Stamps': {}},
    3: {'Total Stamp Levels': 150, 'Stamps': {
        "Combat": ["Mana Stamp", "Tomahawk Stamp", "Target Stamp", "Shield Stamp", "Vitality Stamp"],
        "Skill": ["Choppin' Bag Stamp"],
        "Misc": ["Vendor Stamp"]}},
    4: {'Total Stamp Levels': 200, 'Stamps': {
        "Skill": ["Lil' Mining Baggy Stamp"],
        'Not Recommended': ["Clover Stamp"]}},
    5: {'Total Stamp Levels': 250, 'Stamps': {
        "Skill": ["Anvil Zoomer Stamp", "Matty Bag Stamp"],
        'Not Recommended': ["Kapow Stamp"]}},
    6: {'Total Stamp Levels': 300, 'Stamps': {}},
    7: {'Total Stamp Levels': 400, 'Stamps': {
        "Skill": ["Fishing Rod Stamp", "Catch Net Stamp"],
        "Specific": {'Pickaxe Stamp': 35, 'Hatchet Stamp': 35}}},
    8: {'Total Stamp Levels': 500, 'Stamps': {
        "Skill": ["Drippy Drop Stamp"],
        "Specific": {'Drippy Drop Stamp': 30},
        'Not Recommended': ["Hermes Stamp", "Talent III Stamp"]}},
    9: {'Total Stamp Levels': 600, 'Stamps': {}},
    10: {'Total Stamp Levels': 700, 'Stamps': {
        "Combat": [
            "Fist Stamp", "Manamoar Stamp", "Longsword Stamp",
            "Battleaxe Stamp", "Scimitar Stamp", "Bullseye Stamp",
            "Buckler Stamp"
        ],
        "Skill": ["Twin Ores Stamp", "Duplogs Stamp", "Cool Diggy Tool Stamp", "Swag Swingy Tool Stamp", "Alch Go Brrr Stamp",
                  "Droplots Stamp", "Bugsack Stamp", "Hidey Box Stamp", "Spikemouth Stamp", "Purp Froge Stamp"],
        "Misc": ["Crystallin", "Talent S Stamp"]},
        "Specific": {'Drippy Drop Stamp': 40, 'Matty Bag Stamp': 30}
    },
    11: {'Total Stamp Levels': 800, 'Stamps': {
         "Skill": ["Stample Stamp", "Spice Stamp", "Egg Stamp"],
         "Misc": ["Mason Jar Stamp", "Sigil Stamp"],
         "Specific": {'Pickaxe Stamp': 45, 'Hatchet Stamp': 45, 'Mason Jar Stamp': 12}}},
    12: {'Total Stamp Levels': 1000, 'Stamps': {
        "Skill": ["Bag o Heads Stamp", "Skelefish Stamp" "Cooked Meal Stamp"],
        "Misc": ["Card Stamp"],
        "Specific": {
            'Drippy Drop Stamp': 50,
            'Pickaxe Stamp': 55, 'Hatchet Stamp': 55, 'Card Stamp': 50
        },
        'Not Recommended': [
            "Saw Stamp", "Agile Stamp", "Book Stamp", "Smart Dirt Stamp", "High IQ Lumber Stamp", "Fishhead Stamp",
            "Polearm Stamp", "Biblio Stamp"
        ]
    }},
    13: {'Total Stamp Levels': 2500, 'Stamps': {
        "Skill": ["Banked Pts Stamp", "Nest Eggs Stamp", "Ladle Stamp", "Sailboat Stamp"],
        "Misc": ["Refinery"],
        "Specific": {
            'Matty Bag Stamp': 100, 'Crystallin': 60,
            'Pickaxe Stamp': 65, 'Hatchet Stamp': 65, 'Card Stamp': 100,
        },
        'Not Recommended': ["Stat Graph Stamp", "Brainstew Stamps", "Arcane Stamp", "Fly Intel Stamp", "Holy Mackerel Stamp", "Talent II Stamp",
                     "Gilded Axe Stamp", "Avast Yar Stamp", "Blackheart Stamp", "Lab Tube Stamp", "DNA Stamp"]
    }},
    14: {'Total Stamp Levels': 4000, 'Stamps': {
        "Combat": ["Sashe Sidestamp"],
        "Skill": ["Gamejoy Stamp", "Divine Stamp"],
        "Specific": {
            'Bugsack Stamp': 80, 'Bag o Heads Stamp': 80, 'Pickaxe Stamp': 75, 'Hatchet Stamp': 75,
            'Drippy Drop Stamp': 85, 'Crystallin': 100,
        },
        'Not Recommended': ["Feather Stamp", "Steve Sword", "Diamond Axe Stamp", "Questin Stamp"],
    }},
    15: {'Total Stamp Levels': 5500, 'Stamps': {
        "Combat": ["Tripleshot Stamp", "Maxo Slappo Stamp"],
        "Skill": ["Crop Evo Stamp", "Buzz Buzz Stamp"],
        "Misc": ["Potion Stamp", "Golden Apple Stamp"],
        "Specific": {
            'Matty Bag Stamp': 150, 'Card Stamp': 150, 'Ladle Stamp': 100, 'Potion Stamp': 20,
            'Pickaxe Stamp': 85, 'Hatchet Stamp': 85, 'Mason Jar Stamp': 52, 'Golden Apple Stamp': 40, 'Crop Evo Stamp': 20,
        },
        'Not Recommended': ["Void Sword Stamp", "Multikill Stamp",]
    }},
    16: {'Total Stamp Levels': 7500, 'Stamps': {
        "Combat": ["Violence Stamp", "Intellectostampo", "Dementia Sword Stamp"],
        "Skill": ["Multitool Stamp", "Flowin Stamp", "Sneaky Peeky Stamp", "Jade Mint Stamp", "White Essence Stamp"],
        "Misc": ["Forge Stamp"],
        "Specific": {
            'Matty Bag Stamp': 200, 'Crystallin': 150,
            'Bugsack Stamp': 120, 'Bag o Heads Stamp': 120, 'Multitool Stamp': 100,
            'Drippy Drop Stamp': 100, 'Potion Stamp': 40, 'Golden Apple Stamp': 60,
            'Pickaxe Stamp': 95, 'Hatchet Stamp': 95, 'Ladle Stamp': 180, 'Forge Stamp': 100
        },
        'Not Recommended': ["Blover Stamp"]
    }},
    17: {'Total Stamp Levels': 9200, 'Stamps': {
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
    18: {'Total Stamp Levels': 11000, 'Stamps': {
        "Specific": {
            'Mason Jar Stamp': 88, 'Matty Bag Stamp': 280, 'Crystallin': 250,
            'Golden Apple Stamp': 100,
        }
    }},
    19: {'Total Stamp Levels': 13000, 'Stamps': {
        "Combat": ["Golden Sixes Stamp", "Stat Wallstreet Stamp"],
        "Skill": ["Amplestample Stamp", "Triad Essence Stamp", "Summoner Stone Stamp"],
        "Specific": {
            'Golden Sixes Stamp': 120,
            'Maxo Slappo Stamp': 98, 'Sashe Sidestamp': 98, 'Intellectostampo': 98,
            'Mason Jar Stamp': 92, "Matty Bag Stamp": 320, 'Crystallin': 260,
            'Triad Essence Stamp': 80
        },
        'Not Recommended': ["Sukka Foo", "Void Axe Stamp"]
    }},
    20: {'Stamps': {
        "Specific": {
            "Mason Jar Stamp": 96, "Matty Bag Stamp": 380, 'Crystallin': 270,
            "Lil' Mining Baggy Stamp": 280, 'Summoner Stone Stamp': 120, 'Drippy Drop Stamp': 155,
            "Choppin' Bag Stamp": 300, 'Intellectostampo': 161, 'Maxo Slappo Stamp': 133,
            'Cool Diggy Tool Stamp': 280, 'Swag Swingy Tool Stamp': 360, 'Golden Apple Stamp': 112,
            'Hatchet Stamp': 295, 'Pickaxe Stamp': 255,
            'Sashe Sidestamp': 126,  'Conjocharmo Stamp': 170,
            'Captalist Stats Stamp': 140,
            'Anvil Zoomer Stamp': 125, 'Skelefish Stamp': 32, 'Fishing Rod Stamp': 120, 'Catch Net Stamp': 120, 'Divine Stamp': 120,
            'White Essence Stamp': 104, 'Triad Essence Stamp': 112, 'Dark Triad Essence Stamp': 96, 'Nest Eggs Stamp': 240,
        },
    }},
    21: {'Stamps': {"Specific": {},}},  # Info tier for Capacity stamps, populated later from stamp_maxes
    22: {'Stamps': {"Specific": {},}},  # Info tier for all other previously tiered stamps, populated later from stamp_maxes
    23: {'Stamps': {"Specific": {},}},  # Info tier for all non-tiered stamps, populated later from stamp_maxes
}
smithing_progressionTiers = {
    1: {
        'Cash Points': 20,
        'Monster Points': 85,
        'Forge Total': 60,
        'Resource': 'bullfrog-horn'
    },
    2: {
        'Cash Points': 60,
        'Monster Points': 150,
        'Forge Total': 120,
        'Resource': 'pincer-arm'
    },
    3: {
        'Cash Points': 100,
        'Monster Points': 225,
        'Forge Total': 180,
        'Resource': 'shrapshell'
    },
    4: {
        'Cash Points': 150,
        'Monster Points': 350,
        'Forge Total': 240,
        'Resource': 'sippy-straw'
    },
    5: {
        'Cash Points': 200,
        'Monster Points': 500,
        'Forge Total': 291,
        'Resource': 'bottle-cap'
    },
    6: {
        'Cash Points': 600,
        'Monster Points': 700,
        'Forge Total': 291,
        'Resource': 'condensed-zap'
    }
}
owl_bonuses_of_orion = {
    'Class XP': {'BaseValue': 5},
    'Base Damage': {'BaseValue': 10},
    'Total Damage': {'BaseValue': 2},
    'Skill XP': {'BaseValue': 4},
    'Drop Rate': {'BaseValue': 1},
    'All Stat': {'BaseValue': 2}
}
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
        "Ol Reliable Statue": 20, "Exp Statue": 20, "Anvil Statue": 20, "Cauldron Statue": 20,
        "Beholder Statue": 20,
        "Pecunia Statue": 20, "Mutton Statue": 20, "Egg Statue": 20,
    },},
    2: {"MinStatueTypeNumber": 1, "MinStatueType": "Gold", 'SpecificTypes': [
        'Power Statue', 'Speed Statue', 'Mining Statue', 'Feasty Statue', 'Health Statue', 'Kachow Statue', 'Lumberbob Statue',
        'Thicc Skin Statue', 'Oceanman Statue', 'Ol Reliable Statue', 'Exp Statue', 'Anvil Statue', 'Cauldron Statue',
        'Beholder Statue', 'Bullseye Statue',
        'Box Statue', 'Twosoul Statue', 'EhExPee Statue', 'Seesaw Statue',
        'Pecunia Statue', 'Mutton Statue', 'Egg Statue',
        'Battleaxe Statue', 'Spiral Statue', 'Boat Statue',
        'Compost Statue', 'Stealth Statue', 'Essence Statue'
    ],},
    3: {"MinStatueTypeNumber": 2, "MinStatueType": "Onyx", 'SpecificTypes': [
        'Power Statue', 'Speed Statue', 'Mining Statue', 'Feasty Statue', 'Health Statue', 'Lumberbob Statue',
        'Ol Reliable Statue', 'Exp Statue', 'Anvil Statue', 'Cauldron Statue',
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
        'Oceanman Statue': 40, 'Ol Reliable Statue': 40, 'Exp Statue': 40, 'Anvil Statue': 40, 'Cauldron Statue': 40,
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
    11: {
        "MinStatueTypeNumber": 2,
        "MinStatueType": "Onyx",
        'SpecificTypes': ['Villager Statue', 'Dragon Statue'],
        'SpecificLevels': {
            'Mining Statue': 280, 'Feasty Statue': 280, 'Lumberbob Statue': 280, 'Villager Statue': 100, 'Dragon Statue': 150,
        },
    },
}
vault_progressionTiers = {
    1: {
        'Include': [
            'Bigger Damage', 'Massive Whirl', 'Rapid Arrows', 'Dual Fireballs', 'Weapon Craft', 'Mining Payday',
            'Baby on Board', 'Bored to Death', 'Stamp Bonanza', 'Drops for Days', 'Slice N Dice', 'Go Go Secret Owl',
            'Boss Decimation', 'Sleepy Time', 'Production Revolution', 'Statue Bonanza', 'Stick Snapping', 'Liquid Knowledge',
            'Bug Knowledge', 'Fish Knowledge', 'Dirty Money', "Schoolin' the Fish", 'Straight to Storage', 'Bubble Money',
            'Drip Drip Drip', 'Active Learning', 'Bug Power En Masse', 'Vial Overtune', 'Daily Mailbox', 'Duplicate Entries'
        ]
    },
    2: {
        'Include': [
            'Major Discount', 'Monster Tax', 'Recipe for Profit', 'Stunning Talent', 'All Armoured Up', 'Buildie Sheepie'
        ]  #This list generated from Acecow's alt account when they first entered World 6 and may need to be adjusted in the future
    },
    3: {
        'Exclude': [
            'Bullseye', 'Wicked Smart', 'Kitchen Dream-mare', 'Teh TOM', 'Cooking Knowledge',  #Too Expensive
            'Beeg Forge',  #Having too large of Ore capacity can be annoying. Not maxing this is one way player's have chosen to keep capacity down
            'Card Retirement'  #Passive cards cannot be doubled. I don't care, but some people like the option
        ]  #You're probably going to regret doing an exclude after Vault3 gets added, RIP
    }
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
     {'FMJ': 5, 'Shaquracy': 5, 'Prowesessary': 7, 'Hammer Hammer': 6},
     "10% max value",
     "MINIMUM recommended Utility bubbles for finishing W2. Prowess hard-caps at 2x."],
    [2, 20,
     {'Roid Ragin': 25, 'Warriors Rule': 13, 'Hearty Diggy': 25, 'Wyoming Blood': 13, 'Sploosh Sploosh': 13, 'Stronk Tools': 18},
     {'Swift Steppin': 25, 'Archer Or Bust': 13, 'Sanic Tools': 18, 'Bug^2': 13},
     {'Stable Jenius': 25, 'Mage Is Best': 13, 'Hocus Choppus': 25, 'Molto Loggo': 13, 'Le Brain Tools': 18},
     {'FMJ': 10, 'Shaquracy': 10, 'Prowesessary': 15, 'Hammer Hammer': 14, "Name I Guess": 10},
     "20% max value",
     "MINIMUM recommended Utility bubbles for starting W3. Prowess hard-caps at 2x."],
    [3, 40,
     {'Roid Ragin': 67, 'Warriors Rule': 34, 'Hearty Diggy': 67, 'Wyoming Blood': 20, 'Sploosh Sploosh': 20, 'Stronk Tools': 47},
     {'Swift Steppin': 67, 'Archer Or Bust': 34, 'Sanic Tools': 47, 'Bug^2': 20},
     {'Stable Jenius': 67, 'Mage Is Best': 34, 'Hocus Choppus': 67, 'Molto Loggo': 20, 'Le Brain Tools': 47},
     {'FMJ': 15, 'Shaquracy': 15, 'Prowesessary': 40, 'Hammer Hammer': 41, 'All For Kill': 25, "Name I Guess": 20},
     "40% max value",
     "MINIMUM recommended Utility bubbles for starting W4. Prowess hard-caps at 2x."],
    [4, 60,
     {'Roid Ragin': 100, 'Warriors Rule': 50, 'Hearty Diggy': 100, 'Wyoming Blood': 30, 'Sploosh Sploosh': 30, 'Stronk Tools': 70},
     {'Swift Steppin': 100, 'Archer Or Bust': 50, 'Sanic Tools': 70, 'Bug^2': 30},
     {'Stable Jenius': 100, 'Mage Is Best': 50, 'Hocus Choppus': 100, 'Molto Loggo': 30, 'Le Brain Tools': 70},
     {'FMJ': 20, 'Shaquracy': 20, 'Prowesessary': 60, 'Hammer Hammer': 65, 'All For Kill': 67, "Name I Guess": 30},
     "50% max value",
     "MINIMUM recommended Utility bubbles for starting W5. Prowess hard-caps at 2x, which you should be reaching now!"],
    [5, 80,
     {'Roid Ragin': 150, 'Warriors Rule': 75, 'Hearty Diggy': 150, 'Wyoming Blood': 45, 'Sploosh Sploosh': 45, 'Stronk Tools': 105, 'Multorange': 45},
     {'Swift Steppin': 150, 'Archer Or Bust': 75, 'Bug^2': 45, 'Premigreen': 45, },
     {'Stable Jenius': 150, 'Mage Is Best': 75, 'Molto Loggo': 45, 'Le Brain Tools': 105, 'Severapurple': 45, },
     {'FMJ': 30, 'Shaquracy': 30, 'Hammer Hammer': 100, 'All For Kill': 100, "Name I Guess": 40},
     "60% max value",
     "MINIMUM recommended Utility bubbles for starting W6 push. Keep watch of your No Bubble Left Behind list (from W4 Lab) to keep cheap/easy bubbles off when possible!"],
    [6, 100,
     {'Roid Ragin': 234, 'Warriors Rule': 117, 'Hearty Diggy': 234, 'Wyoming Blood': 70, 'Sploosh Sploosh': 70, 'Stronk Tools': 164, 'Multorange': 70,
      'Dream Of Ironfish': 70},
     {'Swift Steppin': 234, 'Archer Or Bust': 117, 'Bug^2': 70, 'Premigreen': 70, 'Fly In Mind': 94},
     {'Stable Jenius': 234, 'Mage Is Best': 117, 'Molto Loggo': 70, 'Le Brain Tools': 164, 'Severapurple': 70},
     {'All For Kill': 150, "Name I Guess": 100},
     "70% max value",
     ""],
    [7, 120,
     {'Roid Ragin': 400, 'Warriors Rule': 200, 'Hearty Diggy': 400, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 280, 'Multorange': 120},
     {'Swift Steppin': 400, 'Archer Or Bust': 200, 'Bug^2': 120},
     {'Stable Jenius': 400, 'Mage Is Best': 200, 'Hocus Choppus': 400, 'Molto Loggo': 120, 'Le Brain Tools': 280, 'Severapurple': 120, 'Tree Sleeper': 160},
     {'Laaarrrryyyy': 150, 'Hammer Hammer': 150, 'Cookin Roadkill': 105, 'All For Kill': 167},
     "80% max value",
     "Larry at 150 = 72% chance for +2 levels. Somewhere around level 125-150, this bubble should pass 100m Dementia Ore cost and be available to level with Boron upgrades from the W3 Atom Collider in Construction.  It should be, in my opinion, the ONLY Utility Bubble you spend these daily clicks on until it reaches 501. If you cannot afford the Particles needed to level Larry, invest into Sampling Bubbles."],
    [8, 0,
     {'Roid Ragin': 567, 'Warriors Rule': 284, 'Hearty Diggy': 567, 'Stronk Tools': 397, 'Multorange': 170, 'Dream Of Ironfish': 170},
     {'Swift Steppin': 567},
     {'Stable Jenius': 567, 'Mage Is Best': 284, 'Hocus Choppus': 567, 'Le Brain Tools': 397, 'Severapurple': 170, 'Tree Sleeper': 227},
     {'Hammer Hammer': 180},
     "85% max value",
     ""],
    [9, 0,
     {'Roid Ragin': 740, 'Warriors Rule': 450, 'Hearty Diggy': 900, 'Stronk Tools': 630, 'Multorange': 270, 'Dream Of Ironfish': 270},
     {'Swift Steppin': 740, 'Archer Or Bust': 450, 'Premigreen': 270},
     {'Stable Jenius': 740, 'Mage Is Best': 450, 'Hocus Choppus': 900, 'Le Brain Tools': 630, 'Severapurple': 270, 'Tree Sleeper': 360},
     {'Laaarrrryyyy': 501, 'Cookin Roadkill': 630, 'Startue Exp': 240, 'Hammer Hammer': 300,
      'Droppin Loads': 280, 'Buff Boi Talent': 100, 'Fast Boi Talent': 100, 'Smart Boi Talent': 100},
     "90% max value",
     ""],
    [10, 0,
     {'Roid Ragin': 840, 'Warriors Rule': 950, 'Multorange': 570},
     {'Swift Steppin': 840},
     {'Stable Jenius': 840, 'Mage Is Best': 950,  'Severapurple': 570},
     {'Laaarrrryyyy': 900, 'Big P': 540, 'Call Me Bob': 1000, 'Carpenter': 450, 'Big Game Hunter': 270, 'Mr Massacre': 450, "Grind Time": 500},
     "95% max value",
     ""],
    [11, 0,
     {'Roid Ragin': 900},
     {'Swift Steppin': 900},
     {'Stable Jenius': 900},
     {
        'Cropius Mapper': 630, 'Buff Boi Talent': 200, 'Fast Boi Talent': 200, 'Smart Boi Talent': 200,  #Old t19
        'Call Me Bob': 3000, 'Big Game Hunter': 570, 'Mr Massacre': 950, 'Lo Cost Mo Jade': 760, 'Cookin Roadkill': 1330, 'Big P': 940, 'Laaarrrryyyy': 1900,  #Old t20
        'Essence Boost-Orange': 400, 'Essence Boost-Green': 400, 'Carpenter': 950, 'Diamond Chef': 890  #Old t21
     },
     "98% max value",
     ""],
    [12, 0,
     {'Roid Ragin': 1000},
     {'Swift Steppin': 1000},
     {'Stable Jenius': 1000},
     {
        'Big P': 1440, 'Call Me Bob': 5000, 'Nickel Of Wisdom': 120, "Penny Of Strength": 120, "Dollar Of Agility": 120,
        'Buff Boi Talent': 300, 'Fast Boi Talent': 300, 'Smart Boi Talent': 300,
        'Droppin Loads': 1330, 'Startue Exp': 1140, "Grind Time": 5000
     },
     "99% max value",
     ""],
    [13, 0,
     {  #'Roid Ragin': 9000,
      'Slabi Orefish': 540, 'Slabi Strength': 540,  # 'Endgame Eff I': 540,
      'Tome Strength': 540},
     {  #'Swift Steppin': 9000,
      'Sanic Tools': 630,
      'Slabo Critterbug': 540, 'Slabo Agility': 540,  # 'Endgame Eff II': 540,
      'Tome Agility': 540},
     {  #'Stable Jenius': 9000,
      'Slabe Logsoul': 540, 'Slabe Wisdom': 540, 'Endgame Eff III': 540},  # 'Tome Wisdom': 540},
     {'Nickel Of Wisdom': 270, "Penny Of Strength": 270, "Dollar Of Agility": 270, 'Card Champ': 360},
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
     {'Nickel Of Wisdom': 570, "Penny Of Strength": 570, "Dollar Of Agility": 570, 'Card Champ': 760,},
     "95% catchup",
     ""],
    [15, 160,
     {'Roid Ragin': 10000, 'Warriors Rule': 4950, 'Hearty Diggy': 9900, 'Stronk Tools': 6930, 'Multorange': 2970, 'Dream Of Ironfish': 2970,
      'Slabi Orefish': 5940, 'Slabi Strength': 5940, 'Tome Strength': 5940},  #'Endgame Eff I': 5940,
     {'Swift Steppin': 10000, 'Archer Or Bust': 4950, 'Sanic Tools': 6930, 'Premigreen': 2970, 'Fly In Mind': 3960,
      'Slabo Critterbug': 5940, 'Slabo Agility': 5940, 'Endgame Eff II': 5940, 'Tome Agility': 5940},
     {'Stable Jenius': 10000, 'Mage Is Best': 4950, 'Hocus Choppus': 9900, 'Le Brain Tools': 6930, 'Severapurple': 2970, 'Tree Sleeper': 3960,
      'Slabe Logsoul': 5940, 'Slabe Wisdom': 5940, 'Endgame Eff III': 5940, 'Tome Wisdom': 5940},
     {'Cookin Roadkill': 6930, 'Call Me Bob': 10000, 'Carpenter': 4950, 'Nickel Of Wisdom': 2970, "Penny Of Strength": 2970, "Dollar Of Agility": 2970,
      'Droppin Loads': 6930, 'Startue Exp': 5940, 'Laaarrrryyyy': 9900, 'Big Game Hunter': 2970, 'Mr Massacre': 4950, 'Big P': 5940,
      'Hammer Hammer': 10000, "Grind Time": 10000, 'Buff Boi Talent': 800, 'Fast Boi Talent': 800, 'Smart Boi Talent': 800,
      'Card Champ': 3960,
      'Essence Chapter': 4950, 'Quickdraw Quiver': 5940, 'Smarter Spells': 5940, 'Ninja Looter': 5940, 'Crop Chapter': 4950
      },
     "99% catchup",
     ""],
]
vials_progressionTiers = {
    1: {
        'Unlocked': 7,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is the number of vials requiring an unlock roll of 75 or less. "
    },
    2: {
        'Unlocked': 14,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is the number of vials requiring an unlock roll of 85 or less. "
    },
    3: {
        'Unlocked': 19,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is the number of vials requiring an unlock roll of 90 or less. "
    },
    4: {
        'Unlocked': 27,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is the number of vials requiring an unlock roll of 95 or less. "
    },
    5: {
        'Unlocked': 33,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is the number of vials requiring an unlock roll of 98 or less. "
    },
    6: {
        'Unlocked': 38,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is all vials up through W4, excluding the Arcade Pickle. "
    },
    7: {
        'Unlocked': 51,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is all vials up through W5, excluding the Arcade Pickle. "
    },
    8: {
        'Unlocked': 63,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is all vials up through W5, excluding the Arcade Pickle. "
    },
    9: {
        'Unlocked': 67,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is all vials up through W5, excluding the Arcade Pickle. "
    },
    10: {
        'Unlocked': 70,
        'Maxed': 0,
        'Recommended': [],
        'Notes': "This is all vials up through W5, excluding the Arcade Pickle. "
    },
    11: {
        'Unlocked': 70,
        'Maxed': 4,
        'Recommended': ['Copper Corona (Copper Ore)', 'Sippy Splinters (Oak Logs)', 'Jungle Juice (Jungle Logs)', 'Tea With Pea (Potty Rolls)'],
        'Notes': "This is the first half of W6, excluding the Arcade Pickle. "
    },
    12: {
        'Unlocked': 70,
        'Maxed': 8,
        'Recommended': ['Gold Guzzle (Gold Ore)', 'Seawater (Goldfish)', 'Fly In My Drink (Fly)', 'Blue Flav (Platinum Ore)'],
        'Notes': ''
    },
    13: {
        'Unlocked': 72,
        'Maxed': 12,
        'Recommended': ['Slug Slurp (Hermit Can)', 'Void Vial (Void Ore)', 'Ew Gross Gross (Mosquisnow)', 'The Spanish Sahara (Tundra Logs)'],
        'Notes': ''
    },
    14: {
        'Unlocked': 72,
        'Maxed': 16,
        'Recommended': ['Mushroom Soup (Spore Cap)', 'Maple Syrup (Maple Logs)', 'Marble Mocha (Marble Ore)', 'Skinny 0 Cal (Snake Skin)'],
        'Notes': ''
    },
    15: {
        'Unlocked': 72,
        'Maxed': 20,
        'Recommended': ['Long Island Tea (Sand Shark)', 'Anearful (Glublin Ear)', 'Willow Sippy (Willow Logs)', 'Dieter Drink (Bean Slices)'],
        'Notes': ''
    },
    16: {
        'Unlocked': 72,
        'Maxed': 24,
        'Recommended': ['Shinyfin Stew (Equinox Fish)', 'Ramificoction (Bullfrog Horn)', 'Tail Time (Rats Tail)', 'Dreamy Drink (Dream Particulate)'],
        'Notes': ''
    },
    17: {
        'Unlocked': 72,
        'Maxed': 28,
        'Recommended': ['Mimicraught (Megalodon Tooth)', 'Fur Refresher (Floof Ploof)', 'Etruscan Lager (Mamooth Tusk)', 'Dusted Drink (Dust Mote)'],
        'Notes': ''
    },
    18: {
        'Unlocked': 72,
        'Maxed': 32,
        'Recommended': ['Ded Sap (Effervescent Logs)', 'Sippy Soul (Forest Soul)', 'Visible Ink (Pen)', 'Snow Slurry (Snow Ball)'],
        'Notes': ''
    },
    19: {
        'Unlocked': 72,
        'Maxed': 36,
        'Recommended': ['Sippy Cup (Sippy Straw)', 'Goosey Glug (Honker)', 'Crab Juice (Crabbo)', 'Chonker Chug (Dune Soul)'],
        'Notes': ''
    },
    20: {
        'Unlocked': 72,
        'Maxed': 40,
        'Recommended': ['40-40 Purity (Contact Lense)', 'Ladybug Serum (Ladybug)', 'Bubonic Burp (Mousey)', 'Capachino (Purple Mush Cap)'],
        'Notes': ''
    },
    21: {
        'Unlocked': 72,
        'Maxed': 44,
        'Recommended': ['Donut Drink (Half Eaten Donut)', 'Krakenade (Kraken)', 'Calcium Carbonate (Tongue Bone)', 'Spool Sprite (Thread)'],
        'Notes': ''
    },
    22: {
        'Unlocked': 72,
        'Maxed': 48,
        'Recommended': ['Choco Milkshake (Crumpled Wrapper)', 'Electrolyte (Condensed Zap)', 'Ash Agua (Suggma Ashes)', 'Oj Jooce (Orange Slice)'],
        'Notes': ''
    },
    23: {
        'Unlocked': 72,
        'Maxed': 52,
        'Recommended': ['Thumb Pow (Trusty Nails)', 'Slowergy Drink (Frigid Soul)', 'Bunny Brew (Bunny)', 'Flavorgil (Caulifish)'],
        'Notes': ''
    },
    24: {
        'Unlocked': 72,
        'Maxed': 56,
        'Recommended': ['Spook Pint (Squishy Soul)', 'Firefly Grog (Firefly)', 'Barium Mixture (Copper Bar)', 'Bloat Draft (Blobfish)'],
        'Notes': ''
    },
    25: {
        'Unlocked': 72,
        'Maxed': 60,
        'Recommended': ['Barley Brew (Iron Bar)', 'Oozie Ooblek (Oozie Soul)', 'Ricecakorade (Rice Cake)', 'Greenleaf Tea (Leafy Branch)'],
        'Notes': ''
    },
    26: {
        'Unlocked': 72,
        'Maxed': 65,
        'Recommended': [
            'Venison Malt (Mongo Worm Slices)', 'Gibbed Drink (Eviscerated Chunk)', 'Royale Cola (Royal Headpiece)',
            'Refreshment (Breezy Soul)', 'Turtle Tisane (Tuttle)'
        ],
        'Notes': ''
    },
    27: {
        'Unlocked': 72,
        'Maxed': 69,
        'Recommended': ['Red Malt (Redox Salts)', 'Orange Malt (Explosive Salts)', 'Dreadnog (Dreadlo Bar)', 'Dabar Special (Godshard Bar)'],
        'Notes': ''
    },
    # 28: {
    #     'Unlocked': 73,
    #     'Maxed': 73,
    #     'Recommended': ['Poison Tincture (Poison Froge)', 'Shaved Ice (Purple Salt)', 'Pearl Seltzer (Pearler Shell)', 'Hampter Drippy (Hampter)'],
    #     'Notes': 'Currently considered impossible'
    # },
    # 29: {
    #     'Unlocked': 75,
    #     'Maxed': 75,
    #     'Recommended': ['Pickle Jar (BobJoePickle)', 'Ball Pickle Jar (BallJoePickle)'],
    #     'Notes': 'Currently considered impossible'
    # },
}
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
post_office_progression_tiers = {
    0: {},
    1: {
        'Class Specific': {
            # STR
            'Death Bringer': {
                'Deaths Storage Unit': 400,
                'Magician Starterpack': 400,
            },
            'Blood Berserker': {
                'Chefs Essentials': 400,
            },
            'Barbarian': {
                'Sealed Fishheads': 400,
                'Utilitarian Capsule': 400,
            },
            'Divine Knight': {
                'Gaming Lootcrate': 800,
                'Non Predatory Loot Box': 400,
                'Magician Starterpack': 400,
            },
            'Squire': {
                'Construction Container': 400,
                'Dwarven Supplies': 400,
                'Utilitarian Capsule': 400,
            },
            'Warrior': {
                'Carepack From Mum': 400,
                'Locally Sourced Organs': 400,
                'Gaming Lootcrate': 800,
                'Dwarven Supplies': 400,  #Barbarian prioritizes this lower than Squire as it focuses on Cooking+Fishing first
            },

            # WIS
            'Elemental Sorcerer': {
                'Magician Starterpack': 400,
            },
            'Wizard': {
                'Crate of the Creator': 400
            },
            'Bubonic Conjuror': {
                'Magician Starterpack': 400,
                'Potion Package': 400,
                'Non Predatory Loot Box': 400,
                'Science Spare Parts': 400,
            },
            'Shaman': {},
            'Mage': {
                'Taped Up Timber': 400,
                'Utilitarian Capsule': 400,
                'Carepack From Mum': 400,
                'Box of Gosh': 800,
            },

            # AGI
            'Wind Walker': {},
            'Beast Master': {
                'Non Predatory Loot Box': 400,
            },
            'Hunter': {
                'Trapping Lockbox': 400,
            },
            'Siege Breaker': {
                'Non Predatory Loot Box': 400,
            },
            'Bowman': {
                'Bug Hunting Supplies': 400,
            },
            'Archer': {
                'Magician Starterpack': 400,
                'Utilitarian Capsule': 400,
                'Carepack From Mum': 400,
                'Blacksmith Box': 400,
                "Scurvy C'arr'ate": 800
            },

            # LUK
            'Voidwalker': {
                'Non Predatory Loot Box': 400,
            },
            'Maestro': {
                'Non Predatory Loot Box': 400,
                'Magician Starterpack': 400,
            },
            'Journeyman': {
                'Non Predatory Loot Box': 400,
                'Utilitarian Capsule': 400,
                'Carepack From Mum': 400,
            },
        }
    },
    2: {
        'Myriad': False  #Everything else not specified in Tier 1, except Myriad
    },
    3: {
        'Myriad': True  #Just Myriad
    },
}

###WORLD 3 PROGRESSION TIERS###
salt_lick_progression_tiers = {
    1: {
        'Upgrade': 'Obol Storage',
        'Level': 8,
        'Material': 'Froge'
    },
    2: {
        'Upgrade': 'Printer Sample Size',
        'Level': 20,
        'Material': 'Redox Salts'
    },
    3: {
        'Upgrade': 'Max Book',
        'Level': 10,
        'Material': 'Spontaneity Salts'
    },
    4: {
        'Upgrade': 'TD Points',
        'Level': 10,
        'Material': 'Dioxide Synthesis'
    },
    5: {
        'Upgrade': 'Multikill',
        'Level': 10,
        'Material': 'Purple Salt'
    },
    6: {
        'Upgrade': 'EXP',
        'Level': 100,
        'Material': 'Dune Soul'
    },
    7: {
        'Upgrade': 'Alchemy Liquids',
        'Level': 100,
        'Material': 'Mousey'
    },
    8: {
        'Upgrade': 'Damage',
        'Level': 250,
        'Material': 'Pingy'
    },
    9: {
        'Upgrade': 'Refinery Speed',
        'Level': 100,
        'Material': 'Explosive Salts'
    },

}
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
    [16, 20, 10, 10, 10, 10, 0,     0, 0,   15, 15, 15, 0, ""],
    [17, 20, 20, 10, 10, 10, 1,     0, 0,   26, 26, 26, 0, ""],
    [18, 20, 20, 20, 10, 10, 2,     0, 0,   40, 40, 40, 0, ""],
    [19, 20, 20, 20, 20, 10, 3,     0, 0,   53, 53, 53, 0, "Aim for Super CHOWs in 24hrs each (4m+ KPH)"],
    [20, 20, 20, 20, 20, 20, 4,     0, 0,   66, 66, 66, 0, ""],
    [21, 20, 20, 20, 20, 20, 10,    0, 0,   73, 73, 73, 0, ""],
    [22, 20, 20, 20, 20, 20, 20,    0, 0,   80, 80, 80, 80, ""],
    [23, 20, 20, 20, 20, 20, 20,    0, 0,   84, 84, 83, 82, ""],
    [24, 20, 20, 20, 20, 20, 20,    0, 0,   86, 86, 86, 85, ""]
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
prayers_progressionTiers = {
    1: {
        'The Royal Sampler': 1
    },
    2: {
        'Skilled Dimwit': 20
    },
    3: {
        'Balance of Pain': 11
    },
    4: {
        'Skilled Dimwit': 35,
        'Balance of Pain': 20
    },
    5: {
        'Midas Minded': 20
    },
    6: {
        'Skilled Dimwit': 50,
        'Midas Minded': 50,
        'Balance of Pain': 30
    },
    7: {
        'Shiny Snitch': 50,
        'Zerg Rushogen': 20,
        'Jawbreaker': 50,
        'Ruck Sack': 50
    },
}
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
            "Neon - Damage N' Cheapener": 30,
            'Fluoride - Void Plate Chef': 30,
        },
    },
    14: {
        'Atoms': {
            'Aluminium - Stamp Supercharger': 50,
            "Neon - Damage N' Cheapener": 50,
            'Hydrogen - Stamp Decreaser': 45,
            'Helium - Talent Power Stacker': 13,
            'Lithium - Bubble Insta Expander': 50,
            'Boron - Particle Upgrader': 50,
            'Nitrogen - Construction Trimmer': 50,
            'Carbon - Wizard Maximizer': 50,  #Questionable
            'Oxygen - Library Booker': 50,  #Questionable
            'Fluoride - Void Plate Chef': 50,  #Questionable
            'Magnesium - Trap Compounder': 50  #Questionable
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
armor_sets_progressionTiers = {
    1: {
        'Unlocked': True
    },
    2: {
        'Sets': ['COPPER SET', 'IRON SET', 'GOLD SET', 'PLATINUM SET', 'DEMENTIA SET', 'AMAROK SET']
    },
    3: {
        'Sets': ['VOID SET', 'EFAUNT SET', 'CHIZOAR SET']
    },
    4: {
        'Sets': ['LUSTRE SET', 'DIABOLICAL SET', 'TROLL SET', 'MAGMA SET']
    },
    5: {
        'Sets': ['KATTLEKRUK SET', 'MARBIGLASS SET', 'GODSHARD SET']
    },
    6: {
        'Sets': ['EMPEROR SET', 'PREHISTORIC SET']
    },
    7: {
        'Sets': ['SECRET SET']
    }
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
    },
    13: {
        'Max Shinies': [
            'Bonuses from All Meals', 'Drop Rate', 'Summoning EXP',
            'Base Efficiency for All Skills', 'Multikill Per Tier', 'Faster Refinery Speed'
        ]
    },
    14: {
        'Max Shinies': [
            'Farming EXP', 'Lower Minimum Travel Time for Sailing', 'Sail Captain EXP Gain',
            'Higher Artifact Find Chance', 'Skill EXP', 'Base Critter Per Trap'
        ]
    },
    15: {
        'Max Shinies': [
            'Faster Shiny Pet Lv Up Rate', 'Base WIS', 'Base STR', 'Base AGI', 'Base LUK',
            'Infinite Star Signs', 'Total Damage',
            'Tab 4 Talent Pts', 'Tab 3 Talent Pts', 'Tab 2 Talent Pts', 'Tab 1 Talent Pts',
            'Class EXP', 'Line Width in Lab'
        ]
    },

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
        'Islands Discovered': 1,
        'Captains And Boats': 3,
        'Artifacts': {
            'Moai Head': 1,
            'Fauxory Tusk': 1
        }
    },
    2: {
        'Islands Discovered': 4,
        'Captains And Boats': 5,
        'Artifacts': {
            'Gold Relic': 1,
            '10 AD Tablet': 2,
            'Fauxory Tusk': 2
        }
    },
    3: {
        'Islands Discovered': 5,
        'Captain And Boats': 9,
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
        'Islands Discovered': 6,
        'Captain And Boats': 10,
        'Artifacts': {
            'Amberite': 2,
            'Gold Relic': 2,
        }
    },
    5: {
        'Islands Discovered': 7,
        'Captain And Boats': 11,
        'Artifacts': {
            'Jade Rock': 2,
        }
    },
    6: {
        'Islands Discovered': 8,
        'Captain And Boats': 12,
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
        'Islands Discovered': 9,
        'Captain And Boats': 13,
        'Artifacts': {
            'Fury Relic': 2,
        },
    },
    8: {
        'Islands Discovered': 12,
        'Captain And Boats': 15,
        'Artifacts': {
            'Crystal Steak': 2,
        }
    },
    9: {
        'Islands Discovered': 14,
        'Captain And Boats': 17,
        'Artifacts': {
            'Socrates': 2,
        }
    },
    10: {
        'Islands Discovered': 15,
        'Captain And Boats': 19,
        'Artifacts': {
            'Cloud Urn': 1,
            'Weatherbook': 1,
            'Trilobite Rock': 1,
            'Opera Mask': 1,
        }
    },
    11: {
        'Captain And Boats': 20,
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
        },
        'Beanstacked': True,
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
        #'SuperBeanstacked': True
    },
    19: {
        'Artifacts': {
            #These last 2 are worthless, but get them anyway.
            'Giants Eye': 4,
            'Dreamcatcher': 4,
        },
    }
}
gaming_progressionTiers = {
    0: {}
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
            'CropIndex': [10, 28]  #10 = Basic/Lime, 28 = Earthy/Avocado
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
            'CropIndex': [20, 40, 54, 71],  #20 = Basic/Golden Blueberry, 40 = Earthy/Lettuce, 54 = Bulbo/Pink Daisy, 71 = Sushi/11
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
            'CropIndex': [45, 60, 83, 103, 118],  #45 = Earthy/Gold Sliced Tomato, 60 = Bulbo/Golden Tulip, 83 = Sushi/Max, 103 = Mushie/20, 118 = Normal Glassy/Onigiri
            'Stacks': ['Evolution Gmo', 'Speed Gmo'],
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
            'CropIndex': [106, 122],  #106 = Mushie/Final, 121 = Red Glassy/Mango
            'Stacks': ['Evolution Gmo', 'Speed Gmo'],
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
            'CropIndex': [125],  #125 at end of 1k stacking, before 100k stacking
            'Stacks': ['Evolution Gmo', 'Speed Gmo', 'Value Gmo'],
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
            'CropIndex': [126],
            'Stacks': ['Evolution Gmo', 'Speed Gmo', 'Value Gmo', 'Super Gmo'],
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
            'Stacks': ['Evolution Gmo', 'Speed Gmo', 'Value Gmo', 'Super Gmo'],
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
            'Stacks': ['Evolution Gmo', 'Speed Gmo', 'Value Gmo', 'Super Gmo'],
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
            'Stacks': ['Evolution Gmo', 'Speed Gmo', 'Value Gmo', 'Super Gmo'],
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
            'Stacks': ['Evolution Gmo', 'Speed Gmo', 'Value Gmo', 'Super Gmo'],
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
beanstalk_progressionTiers = {
    0: {},
    1: {
        '10k': [
            'Golden Peanut', 'Golden Jam', 'Golden Kebabs', 'Golden Meat Pie',
            'Golden Nomwich', 'Golden Ham', 'Golden Ribs', 'Golden Cheese',
            'Golden Grilled Cheese Nomwich', 'Golden Hampter Gummy Candy',
            'Golden Nigiri', 'Golden Dumpling'
        ]
    },
    2: {
        '10k': [
             'Golden Bread', 'Golden Cake'
        ],
        'Tier Unlocked': 2,
    },
    3: {
        '100k': [
            'Golden Peanut', 'Golden Jam', 'Golden Kebabs', 'Golden Meat Pie',
            'Golden Ham', 'Golden Ribs', 'Golden Cheese',
            'Golden Grilled Cheese Nomwich', 'Golden Hampter Gummy Candy',
            'Golden Nigiri', 'Golden Dumpling'
        ]
    },
    4: {
        '100k': [
            'Golden Cake'
        ]
    },
    5: {
        '10k': [
            'Butter Bar', 'Golden Nomwich'
        ],
        '100k': [
            'Butter Bar', 'Golden Nomwich', 'Golden Bread'
        ]
    },
    6: {
        '1M': [
            'Golden Peanut', 'Butter Bar', 'Golden Jam', 'Golden Kebabs',
            'Golden Meat Pie', 'Golden Nomwich', 'Golden Ham', 'Golden Bread',
            'Golden Ribs', 'Golden Cheese', 'Golden Grilled Cheese Nomwich',
            'Golden Hampter Gummy Candy', 'Golden Nigiri', 'Golden Dumpling',
            'Golden Cake', 'Golden Saltwater Taffy'
        ],
        'Tier Unlocked': 3,
    },
}

###TRUE MAX TIERS###
true_max_tiers = {
    # General
    'Achievements': max(achievements_progressionTiers.keys()),
    'Active': 0,
    'Cards': 91,  #13 sets * 7 stars
    'Combat Levels': combatLevels_progressionTiers[-1][0],
    'Consumables': 0,
    'Drop Rate': 0,
    'Event Shop': 0,
    'Gem Shop': 0,
    'Greenstacks': max(greenstack_progressionTiers.keys()),
    'Endangered Greenstacks': 1,
    'Secret Class Path': max(secret_class_progressionTiers.keys()),

    # Master Classes
    'Grimoire': 0,
    'Compass': 0,
    'Tesseract': 0,

    # World 1
    'Bribes': max(bribes_progressionTiers.keys()),
    'Owl': max(owl_progressionTiers.keys()),
    'Smithing': max(smithing_progressionTiers.keys()),
    'Stamps': max(stamps_progressionTiers.keys()),
    'Star Signs': max(starsigns_progressionTiers.keys()),
    'Statues': max(statues_progressionTiers.keys()),
    'Upgrade Vault': max(vault_progressionTiers.keys()),

    # World 2
    'Bubbles': bubbles_progressionTiers[-1][0],
    'Pay2Win': 1,
    'Sigils': max(sigils_progressionTiers.keys()),
    'Vials': max(vials_progressionTiers.keys()),
    'Arcade': 0,
    'Bonus Ballot': 0,
    'Islands': max(islands_progressionTiers.keys()),
    'Killroy': 0,
    'Post Office': max(post_office_progression_tiers.keys()),

    # World 3
    'Armor Sets': 7,
    'Atom Collider': max(atoms_progressionTiers.keys()),
    'Buildings': 0,
    'Death Note': deathNote_progressionTiers[-1][0],
    'Equinox': len(dreams_that_unlock_new_bonuses) + 1,
    'Library': len(library_subgroup_tiers),
    'Library Characters': len(old_library_subgroup_tiers),
    'Refinery': 1,  #Pass or Fail
    'Salt Lick': max(salt_lick_progression_tiers.keys()),
    'Sampling': max(sampling_progressionTiers.keys()),
    'Trapping': max_trapping_critter_types,
    'Prayers': max(prayers_progressionTiers.keys()),

    # World 4
    'Breeding': max(breeding_progressionTiers.keys()),
    'Cooking': 6+1,  #TODO
    'Rift': max(rift_progressionTiers.keys()),

    # World 5
    'Divinity': max(divinity_progressionTiers.keys()),
    'Gaming': max(gaming_progressionTiers.keys()),
    'Sailing': max(sailing_progressionTiers.keys()),
    'Slab': 0,

    # Caverns
    'Glowshroom Tunnels': 0,
    'Shallow Caverns': 0,
    'Underground Overgrowth': 0,
    'Villagers': 0,

    # World 6
    'Beanstalk': max(beanstalk_progressionTiers.keys()),
    'Farming': max(farming_progressionTiers.keys()),
    'Sneaking': 0,
    'Summoning': 0,
    'Emperor': 0
}
