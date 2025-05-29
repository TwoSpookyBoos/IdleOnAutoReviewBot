import math

from consts.consts import ValueToMulti
from consts.consts_idleon import lavaFunc
from utils.logging import get_logger

logger = get_logger(__name__)

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
BEANSTACK_GOAL = 10**4
SUPER_BEANSTACK_GOAL = 10**5
pristine_charms_list: list = [
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
    {'Name': 'Glimmerchain', 'Image': 'glimmerchain', 'Bonus': '1.30x Extra Death Bringer Bones'},
    {'Name': 'Twinkle Taffy', 'Image': 'twinkle-taffy', 'Bonus': '1.30x Extra Wind Walker Dust'},
    {'Name': 'Jellypick', 'Image': 'jellypick', 'Bonus': '+20% Exalted Stamp bonus'},
    {'Name': 'Candy Cache', 'Image': 'candy-cache', 'Bonus': '1.40x Villager EXP'},
    {'Name': 'Mystery Fizz', 'Image': 'mystery-fizz', 'Bonus': '1.30x Extra 3rd Master Class resource'}
]
sneaking_gemstones_all_values = {
    #NjGem0 = "4 130 Aquamarine 40 Hold_down_to_add_this_Gemstone_to_your_collection._View_collection_and_bonuses_in_Ninja_Knowledge. 10000".split(" ")
    #Gem Index = digit at NjGem, 0 in this example
    #[2] = name
    #[3] = Base Value
    #[5] = Max Value
    #Add [3] and [5] for Max Value
    'Aquamarine': {
        'Stat': 'Stealth',
        'Base Value': 40,
        'Scaling Value': 10000,
        'Max Value': 10040,
        'Gem Index': 0,
        'OptlAcc Index': 233+0
    },
    'Malachite': {
        'Stat': 'Jade',
        'Base Value': 15,
        'Scaling Value': 5000,
        'Max Value': 5015,
        'Gem Index': 1,
        'OptlAcc Index': 233+1
    },
    'Garnet': {
        'Stat': 'Door Damage',
        'Base Value': 12,
        'Scaling Value': 2500,
        'Max Value': 2512,
        'Gem Index': 2,
        'OptlAcc Index': 233+2
    },
    'Starite': {
        'Stat': 'Gold Charm Bonus',
        'Base Value': 5,
        'Scaling Value': 200,
        'Max Value': 205,
        'Gem Index': 3,
        'OptlAcc Index': 233+3
    },
    'Topaz': {
        'Stat': 'Sneak EXP',
        'Base Value': 10,
        'Scaling Value': 1000,
        'Max Value': 1010,
        'Gem Index': 4,
        'OptlAcc Index': 233+4
    },
    'Moissanite': {
        'Stat': 'Gemstone Bonuses',
        'Base Value': 3,
        'Scaling Value': 300,
        'Max Value': 303,
        'Gem Index': 5,
        'OptlAcc Index': 233+5
    },
    'Emerald': {
        'Stat': 'Cheaper Upgrades',
        'Base Value': 1,
        'Scaling Value': 2500,
        'Max Value': 2501,
        'Gem Index': 6,
        'OptlAcc Index': 233+6
    },
    'Firefrost': {
        'Stat': 'Max Charm levels',
        'Base Value': 1,
        'Scaling Value': 30,
        'Max Value': 31,
        'Gem Index': 7,
        'OptlAcc Index': 233+7
    },
}

def getMoissaniteValue(moissaniteLevel: int):
    value = 0
    try:
        if moissaniteLevel > 0:
            value = (
                    sneaking_gemstones_all_values['Moissanite']['Base Value']
                    + (sneaking_gemstones_all_values['Moissanite']['Scaling Value'] * (moissaniteLevel / (moissaniteLevel + 1000)))
            )
        return value
    except:
        return value


def getGemstoneBoostedValue(gemstone_value: float, moissanite_value: float, talent_level: int):
    if moissanite_value > 0:
        moissanite_multi = ValueToMulti(moissanite_value)
        talent_level_multi = lavaFunc('decayMulti', max(0, talent_level), 3, 300)
        boostedValue = gemstone_value * moissanite_multi * talent_level_multi
        return boostedValue
    else:
        return gemstone_value


def getGemstoneBaseValue(gemstoneName: str, gemstoneLevel: int):
    value = 0
    if gemstoneLevel > 0:
        if gemstoneName in sneaking_gemstones_all_values:
            value = (
                    sneaking_gemstones_all_values[gemstoneName]['Base Value']
                    + (sneaking_gemstones_all_values[gemstoneName]['Scaling Value'] * (gemstoneLevel / (gemstoneLevel + 1000)))
            )
        else:
            logger.warning(f"Unrecognized gemstoneName: '{gemstoneName}'. Returning default 0 value")
    return value


def getGemstonePercent(gemstone_name: str, gemstone_value: float):
    try:
        return 100 * (gemstone_value / sneaking_gemstones_all_values[gemstone_name]['Max Value'])
    except Exception as reason:
        logger.exception(f"Could not find max value for Gemstone {gemstone_name} given value {gemstone_value} because: {reason}")
    pass



max_farming_crops = 230  # Last verified as of 2.26 Death Bringer
max_farming_value = 10000  # Last verified as of 2.21 The Fixening
max_land_rank_level = 11  #Base 1 + 10 from Grimoire
landrank_dict = {
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
market_upgrade_list = [
    "Land Plots", "Stronger Vines", "Nutritious Soil", "Smarter Seeds",
    "Biology Boost", "Product Doubler", "More Beenz", "Rank Boost",
    "Overgrowth", "Evolution GMO", "Speed GMO", "OG Fertilizer",
    "EXP GMO", "Land Rank", "Value GMO", "Super GMO"]

#  Last verified from MarketInfo function as of 2.12, slightly tweaked for readability
market_upgrade_details = [
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
market_upgrade_first_index = 2
market_upgrade_last_index = market_upgrade_first_index + len(market_upgrade_list)
crop_depot_dict = {
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
crop_dict = {
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
    if crop_dict[overallSeedNumber]['SeedCropIndex'] == 1:
        return 1
    else:
        try:
            if 'Glassy' in crop_dict[overallSeedNumber]['SeedName']:
                return crop_base * pow(seed_base['Glassy'], crop_dict[overallSeedNumber]['SeedCropIndex'] - 2)
            else:
                return crop_base * pow(seed_base[crop_dict[overallSeedNumber]['SeedName']], crop_dict[overallSeedNumber]['SeedCropIndex'] - 2)
        except:
            logger.warning(f"overallSeedNumber {overallSeedNumber} not found in cropDict, or SeedName not found in seed_base. Returning crop_base {crop_base}")
            return crop_base

def getRequiredCropNumber(upgrade, target_level):
    target_index = target_level - 1  #Formula uses the number of already purchased levels: x - 1
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


summoning_sanctuary_counts = [1]
for multi in range(3, 16):  #(3, 16) produces length of 14
    summoning_sanctuary_counts.append(multi * summoning_sanctuary_counts[-1])
#summoning_sanctuary_counts = [1, 3, 12, 60, 360, 2520, 20160, 181440, 1814400, 19958400, 239500800, 3113510400, 43589145600, 653837184000]
#summoning_upgrades last pulled from SummonUPG in source code in v2.34 Wisdom
summoning_upgrades = ["427 171 0 White_Essence_Champ 10 1.12 5 0 9999 -1 1 +{%_White_Essence_generated_per_hour_for_each_win_across_all_colours._@_Total_bonus:_+}%".split(" "), "374 158 0 Unit_Health 10 1.3 1 0 9999 0 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "479 145 0 Familiar 100 10 1 0 10 0 0 Summons_a_slime_familiar_to_chill_in_your_sanctuary,_generating_10_Summoning_EXP_every_hour._@_Cost_resets_in_|".split(" "), "391 113 0 Unit_Damage 20 1.35 1 0 9999 1 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "389 59 0 Green_Summoning 4000 1.2 10 0 9999 3 1 Unlocks_the_Green_Summoning_Stone,_and_begins_generating_Green_Essence._@_Also,_+{%_Green_Essence_per_hour".split(" "), "449 80 0 Mana_Generation 40 1.35 2 0 9999 3 1 During_competition,_mana_generation_is_+{%_higher_than_normal.".split(" "), "536 126 0 Familiar_Merging 2500 1.2 1 0 1 9 0 3_Slime_Familiars_merge_into_a_Vrumbi_Familiar_which_gives_4x_Summoning_Exp._4_Vrumbies_then_merge_and_give_5x_exp._This_repeats_many_times.".split(" "), "499 58 0 Dodge_Roll 80 1.3 1 0 30 5 0 All_your_units_get_a_+{%_chance_to_dodge_damage_when_colliding_with_an_enemy".split(" "), "554 66 0 Multi-Number_Cards 7500 1.5 1 0 1 7 0 There's_a_chance_cards_can_played_multiple_times,_indicated_by_the_number_in_the_top-left_corner._These_cards_also_come_with_a_smaller_cost!".split(" "), "356 226 1 Vrumbi 10 7.5 5 0 10 4 0 7%_chance_to_draw_a_Vrumbi_during_competition._They_have_1.5x_SPD,_2.0x_DMG,_and_+{%_Dodge_Chance".split(" "), "301 209 1 Unit_Wellness 25 1.3 2 0 9999 9 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "306 154 1 Green_Essence_Victor 50 1.12 1 0 9999 10 1 +{%_Green_Essence_generated_per_hour_for_each_Green_circuit_win._@_Total_bonus:_+}%".split(" "), "252 137 1 Powerful_Units 70 1.35 2 0 9999 11 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "274 86 1 Yellow_Summoning 15000 1.2 10 0 9999 12 1 Unlocks_the_Yellow_Summoning_Stone,_and_begins_generating_Yellow_Essence._@_Also,_+{%_Yellow_Essence_per_hour".split(" "), "200 152 1 Mana_Overflow 4000 1.5 1 0 1 12 0 During_competition,_when_your_mana_pool_is_full,_expand_max_mana_by_1.5x_and_boost_mana_generation_by_+15%".split(" "), "215 94 1 Spiked_Placement 250 1.4 4 0 9999 12 1 When_summoning_any_unit,_deal_{_damage_to_all_enemies_within_100_pixels_of_where_you_click..._You_don't_have_to_click_in_your_spawn!".split(" "), "169 62 1 Starting_Mana_frfr 750 1.6 1 0 9999 15 1 Start_each_competition_with_+{_more_mana".split(" "), "509 201 2 Bloomy 20 25 5 0 10 13 0 4%_chance_to_draw_a_Bloomy_during_competition._They_sit_in_the_backline_and_give_+{%_Mana_Generation_while_alive.".split(" "), "566 188 2 Yellow_Essence_Winnin' 50 1.12 5 0 9999 17 1 +{%_Yellow_Essence_generated_per_hour_for_each_Yellow_circuit_win._@_Total_bonus:_+}%".split(" "), "622 159 2 Luck_of_the_Draw 130 3 2 0 10 18 0 All_special_units_are_>x_more_likely_to_be_drawn_instead_of_slime.".split(" "), "607 106 2 Unit_Constitution 250 1.3 5 0 9999 19 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{%".split(" "), "661 70 2 Stronger_Units 525 1.35 4 0 9999 20 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "714 89 2 Slime_Cellsplit 900 1.15 1 0 30 21 0 When_spawning_any_unit_during_competition,_+{%_chance_to_also_spawn_an_exact_duplicate,_free_of_charge!".split(" "), "747 137 2 Blue_Summoning 50000 1.2 10 0 9999 22 1 Unlocks_the_Blue_Summoning_Stone,_and_begins_generating_Blue_Essence._@_Also,_+{%_Blue_Essence_per_hour".split(" "), "769 78 2 Re-Draw 2000 5 1 0 3 22 1 Unlocks_the_Re-Draw_button,_allowing_you_to_instantly_redraw_all_your_cards_for_a_cost..._but_you_get_the_first_{_for_free!".split(" "), "826 88 2 Another_Slot 10000 1.5 1 0 1 24 0 Adds_+1_Card_Slot,_letting_you_hold_more_cards_at_once!".split(" "), "367 295 3 Tonka 30 1.85 10 0 20 23 0 5%_chance_to_draw_a_Tonka_during_competition._They_have_0.75x_SPD,_0.75x_DMG,_and_8.0x_HP._Your_upgrades_here_boost_its_HP_by_a_further_+{%.".split(" "), "312 285 3 Blue_Essence_Ballin' 70 1.12 5 0 9999 26 1 +{%_Blue_Essence_generated_per_hour_for_each_Blue_circuit_win._@_Total_bonus:_+}%".split(" "), "258 300 3 Slime_Mitosis 200 1.5 1 0 30 27 0 When_spawning_any_unit_during_competition,_+{%_chance_to_also_spawn_an_exact_duplicate,_free_of_charge!".split(" "), "207 275 3 Manaranarr 450 1.5 2 0 9999 28 1 During_competition,_mana_generation_is_+{%_higher_than_normal.".split(" "), "220 224 3 Blue_Knowledge 750 1.15 1 0 9999 29 1 +{%_Blue_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "168 214 3 Beefier_Units 1500 1.35 6 0 9999 30 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "117 183 3 Jeweled_Cards 6000 170 6 0 3 31 1 {%_chance_to_draw_a_Jeweled_variant_of_any_card,_which_costs_2x_Mana_but_spawns_4x_Units!".split(" "), "62 208 3 Purple_Summoning 250000 1.2 10 0 9999 32 1 Unlocks_the_Purple_Summoning_Stone,_and_begins_generating_Purple_Essence._@_Also,_+{%_Purple_Essence_per_hour".split(" "), "78 129 3 Another_Slot 15000 1.5 1 0 1 32 0 Adds_+1_Card_Slot!_Or_as_an_AI_might_say,_this_upgrade_further_substantiates_the_incremental_improvement_to_the_quantity_of_cards_you_hold_by_1".split(" "), "58 77 3 Unit_Ache_Pea 5000 1.3 9 0 9999 34 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "530 263 4 Regalis 50 1.7 1 0 30 33 0 3%_chance_to_draw_a_Regalis_during_competition._They_spawn_a_Slime_Unit_every_1_sec._Upgrading_this_boosts_slime_unit_spawn_rate_by_+{%".split(" "), "588 238 4 Unit_Hitpoints 100 1.25 13 0 9999 36 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "644 228 4 Purp_Essence_Pumpin' 250 1.12 5 0 9999 37 1 +{%_Purple_Essence_generated_per_hour_for_each_Purple_circuit_win._@_Total_bonus:_+}%".split(" "), "693 256 4 Familiar_Skipping 600 1.25 1 0 100 38 0 When_summoning_a_Slime_Familiar,_there's_a_1_in_8_to_get_a_Vrumbi_instead_of_Slime,_and_1_in_50_to_get_a_Bloomy._Upgrading_this_boosts_this_chance_by_+{%".split(" "), "747 262 4 Purple_Knowledge 1000 1.15 1 0 9999 39 1 +{%_Purple_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "705 207 4 Final_Card 2000 2500 1 0 3 38 1 If_you_play_every_card_in_your_hand,_get_+{%_Mana_Regen_per_card_played._Playing_Multi-Number_cards_counts_multiple_times_for_this!".split(" "), "764 204 4 Mana_Dividends 4500 1.5 2 0 9999 41 1 During_competition,_mana_generation_is_+{%_higher_than_normal.".split(" "), "821 165 4 Brutal_Units 9000 1.25 5 0 9999 42 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{%".split(" "), "875 186 4 Red_Summoning 1000000 1.2 10 0 9999 43 1 Unlocks_the_Red_Summoning_Stone,_and_begins_generating_Red_Essence._@_Also,_+{%_Red_Essence_per_hour".split(" "), "404 353 5 Sparkie 75 1.75 5 0 30 44 0 5%_chance_to_draw_a_Sparkie_during_competition._They_have_3.0X_DMG_and_explode_on_death._Your_upgrades_here_boost_it's_DMG_by_a_further_+{%.".split(" "), "349 391 5 Red_Essence_Ragin' 200 1.15 5 0 9999 45 1 +{%_Red_Essence_generated_per_hour_for_each_Red_circuit_win._@_Total_bonus:_+}%".split(" "), "293 362 5 Seeing_Red 750 1.8 1 0 10 46 1 When_an_enemy_crosses_your_line_and_damages_you,_all_units_get_{%_DMG_for_the_rest_of_the_fight._This_stacks_every_time_an_enemy_crosses_your_line.".split(" "), "230 370 5 Slime_Duplication 2000 1.5 1 0 40 47 0 When_spawning_any_unit_during_competition,_+{%_chance_to_also_spawn_an_exact_duplicate,_free_of_charge!".split(" "), "164 377 5 Cost_Crashing 4000 1.25 1 0 9999 48 1 All_Summoning_upgrades_cost_}%_less_Essence.".split(" "), "146 322 5 Unit_Blood 8000 1.4 10 0 9999 49 1 Increases_the_HP_of_all_summoned_units_in_competition_by_a_brand_new_multiplier_of_+{%".split(" "), "100 276 5 Merciless_Units 15000 1.41 8 0 9999 50 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_a_brand_new_multiplier_of_+{%".split(" "), "48 302 5 Red_Knowledge 30000 1.52 1 0 9999 51 1 +{%_Red_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "108 391 5 Cyan_Summoning 3000000 1.21 10 0 9999 49 1 Unlocks_the_Cyan_Summoning_Stone,_and_begins_generating_Cyan_Essence._@_Also,_+{%_Cyan_Essence_per_hour".split(" "), "477 374 6 Cyan_Essence_King 150 1.15 5 0 9999 69 1 +{%_Cyan_Essence_generated_per_hour_for_each_Cyan_circuit_win._@_Total_bonus:_+}%".split(" "), "534 384 6 I_Frames 400 1.5 1 0 30 54 0 All_your_units_get_a_+{%_chance_to_dodge_damage_when_colliding_with_an_enemy".split(" "), "598 390 6 Units_of_Destruction 2000 1.43 10 0 9999 55 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{%".split(" "), "574 322 6 Cost_Deflation 1200 1.21 2 0 9999 69 1 All_Summoning_upgrades_cost_}%_less_Essence.".split(" "), "630 339 6 Cyan_Knowledge 5000 1.55 1 0 9999 57 1 +{%_Cyan_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "683 373 6 Undying_Units 10000 1.41 14 0 9999 58 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{%".split(" "), "739 385 6 DMG_Laundering 20000 1.79 1 0 9999 59 1 Boosts_the_DMG_of_all_summoned_units_by_+{%_for_every_100_total_summoning_upgrades_purchased._@_Total_bonus:_+}%".split(" "), "795 394 6 HP_Laundering 50000 1.78 1 0 9999 60 1 Boosts_the_HP_of_all_summoned_units_by_+{%_for_every_100_total_summoning_upgrades_purchased._@_Total_bonus:_+}%".split(" "), "736 320 6 Infinite_Essence 100000 1.35 5 0 9999 70 1 The_generation_of_all_essence_colours_is_increased_by_+{%_for_every_Endless_Summoning_victory_you_have._@_Total_bonus:_+}%".split(" "), "792 312 6 Infinite_Health 300000 1.38 2 0 9999 62 1 The_HP_of_all_summoned_units_is_increased_by_+{%_for_every_Endless_Summoning_victory_you_have._@_Total_bonus:_+}%".split(" "), "834 266 6 Infinite_Damage 600000 1.41 2 0 9999 63 1 The_DMG_of_all_summoned_units_is_increased_by_+{%_for_every_Endless_Summoning_victory_you_have._@_Total_bonus:_+}%".split(" "), "340 76 0 White_Knowledge 1500 1.15 1 0 9999 4 1 +{%_White_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "148 109 1 Green_Knowledge 1200 1.15 1 0 9999 16 1 +{%_Green_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "678 153 2 Yellow_Knowledge 300 1.15 1 0 9999 19 1 +{%_Yellow_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "874 122 2 Sharpened_Spikes 12000 1.65 1 0 20 25 1 Spike_damage_is_increased_by_{%_of_your_base_unit_damage._@_Total_Bonus_Spike_DMG:_+}".split(" "), "514 327 6 Guardio 100 3.5 8 0 30 53 0 4%_chance_to_draw_a_Guardio!_They_sit_in_midfield,_do_0_DMG,_have_12x_HP,_and_aren't_knocked_back._Your_upgrades_here_boost_its_HP_by_a_further_+{%.".split(" "), "680 315 6 Endless_Summoning 2500 1.55 1 0 1 58 0 Unlocks_the_Endless_Summoning_feature,_accessed_in_the_Top_Right_when_selecting_an_opponent!_Go_to_the_Summoner's_Table,_you_can't_miss_it!".split(" ")]
max_summoning_upgrades = len(summoning_upgrades)
summoning_doubler_recommendations = [
    'Brutal Units', 'DMG Laundering', 'Seeing Red', 'Sharpened Spikes',  #Unique damage multis
    'Final Card', 'Jeweled Cards',
    'Infinite Damage',  #90% of Group C
    'Mana Generation', 'Manaranarr', 'Mana Dividends',  #Mana Generation in battle
    'Beefier Units', 'Stronger Units', 'Powerful Units', 'Unit Damage',  #Rest of the base damage group
    'Units of Destruction', 'Merciless Units',  #Rest of Group C
    'Re-Draw', 'Starting Mana frfr', 'Infinite Essence'
]
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
summoning_match_colors = ['White', 'Green', 'Yellow', 'Blue', 'Purple', 'Red', 'Cyan']
summoningDict = {
    summoning_match_colors[0]: {
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
    summoning_match_colors[1]: {
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
    summoning_match_colors[2]: {
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
    summoning_match_colors[3]: {
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
    summoning_match_colors[4]: {
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
    summoning_match_colors[5]: {
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
    summoning_match_colors[6]: {
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
summoning_endless_challenge_types = [
    "Slow Motion (60% speed)", "Fast Forward (170% speed)", "Glass Cannon (1 HP)",
    "Zerg Surprise", "Extra Time (2x HP)", "Fair Play (No lane stacking)",
    "Invincibility", "Offsides Rule", "Triple Overtime (10x HP)",
    "Truce (No Mods)", "Uno Draw 7"
]
summoning_endlessDict = {
    0: {'RewardID': summoningRewards[21], 'RewardQTY': 1, 'Challenge': summoning_endless_challenge_types[4]},
    1: {'RewardID': summoningRewards[22], 'RewardQTY': 3, 'Challenge': summoning_endless_challenge_types[5]},
    2: {'RewardID': summoningRewards[23], 'RewardQTY': 1, 'Challenge': summoning_endless_challenge_types[1]},
    3: {'RewardID': summoningRewards[24], 'RewardQTY': 12, 'Challenge': summoning_endless_challenge_types[6]},
    4: {'RewardID': summoningRewards[25], 'RewardQTY': 1, 'Challenge': summoning_endless_challenge_types[4]},
    5: {'RewardID': summoningRewards[27], 'RewardQTY': 7, 'Challenge': summoning_endless_challenge_types[0]},
    6: {'RewardID': summoningRewards[23], 'RewardQTY': 2, 'Challenge': summoning_endless_challenge_types[5]},
    7: {'RewardID': summoningRewards[22], 'RewardQTY': 4, 'Challenge': summoning_endless_challenge_types[6]},
    8: {'RewardID': summoningRewards[24], 'RewardQTY': 15, 'Challenge': summoning_endless_challenge_types[7]},
    9: {'RewardID': summoningRewards[29], 'RewardQTY': 10, 'Challenge': summoning_endless_challenge_types[8]},
    10: {'RewardID': summoningRewards[25], 'RewardQTY': 1, 'Challenge': summoning_endless_challenge_types[3]},
    11: {'RewardID': summoningRewards[26], 'RewardQTY': 4, 'Challenge': summoning_endless_challenge_types[10]},
    12: {'RewardID': summoningRewards[24], 'RewardQTY': 18, 'Challenge': summoning_endless_challenge_types[2]},
    13: {'RewardID': summoningRewards[23], 'RewardQTY': 2, 'Challenge': summoning_endless_challenge_types[9]},
    14: {'RewardID': summoningRewards[22], 'RewardQTY': 4, 'Challenge': summoning_endless_challenge_types[7]},
    15: {'RewardID': summoningRewards[32], 'RewardQTY': 3, 'Challenge': summoning_endless_challenge_types[1]},
    16: {'RewardID': summoningRewards[30], 'RewardQTY': 20, 'Challenge': summoning_endless_challenge_types[6]},
    17: {'RewardID': summoningRewards[31], 'RewardQTY': 25, 'Challenge': summoning_endless_challenge_types[5]},
    18: {'RewardID': summoningRewards[25], 'RewardQTY': 2, 'Challenge': summoning_endless_challenge_types[2]},
    19: {'RewardID': summoningRewards[24], 'RewardQTY': 20, 'Challenge': summoning_endless_challenge_types[8]},
    20: {'RewardID': summoningRewards[26], 'RewardQTY': 5, 'Challenge': summoning_endless_challenge_types[3]},
    21: {'RewardID': summoningRewards[29], 'RewardQTY': 30, 'Challenge': summoning_endless_challenge_types[4]},
    22: {'RewardID': summoningRewards[24], 'RewardQTY': 24, 'Challenge': summoning_endless_challenge_types[10]},
    23: {'RewardID': summoningRewards[22], 'RewardQTY': 4, 'Challenge': summoning_endless_challenge_types[6]},
    24: {'RewardID': summoningRewards[21], 'RewardQTY': 1, 'Challenge': summoning_endless_challenge_types[1]},
    25: {'RewardID': summoningRewards[23], 'RewardQTY': 2, 'Challenge': summoning_endless_challenge_types[7]},
    26: {'RewardID': summoningRewards[31], 'RewardQTY': 2, 'Challenge': summoning_endless_challenge_types[2]},
    27: {'RewardID': summoningRewards[28], 'RewardQTY': 35, 'Challenge': summoning_endless_challenge_types[0]},
    28: {'RewardID': summoningRewards[27], 'RewardQTY': 9, 'Challenge': summoning_endless_challenge_types[6]},
    29: {'RewardID': summoningRewards[24], 'RewardQTY': 26, 'Challenge': summoning_endless_challenge_types[3]},
    30: {'RewardID': summoningRewards[26], 'RewardQTY': 5, 'Challenge': summoning_endless_challenge_types[5]},
    31: {'RewardID': summoningRewards[22], 'RewardQTY': 5, 'Challenge': summoning_endless_challenge_types[8]},
    32: {'RewardID': summoningRewards[30], 'RewardQTY': 40, 'Challenge': summoning_endless_challenge_types[9]},
    33: {'RewardID': summoningRewards[25], 'RewardQTY': 1, 'Challenge': summoning_endless_challenge_types[4]},
    34: {'RewardID': summoningRewards[29], 'RewardQTY': 45, 'Challenge': summoning_endless_challenge_types[6]},
    35: {'RewardID': summoningRewards[28], 'RewardQTY': 50, 'Challenge': summoning_endless_challenge_types[2]},
    36: {'RewardID': summoningRewards[23], 'RewardQTY': 2, 'Challenge': summoning_endless_challenge_types[1]},
    37: {'RewardID': summoningRewards[26], 'RewardQTY': 6, 'Challenge': summoning_endless_challenge_types[5]},
    38: {'RewardID': summoningRewards[24], 'RewardQTY': 30, 'Challenge': summoning_endless_challenge_types[10]},
    39: {'RewardID': summoningRewards[32], 'RewardQTY': 3, 'Challenge': summoning_endless_challenge_types[8]},
}
summoningBattleCountsDict = {k: len(v) for k, v in summoningDict.items()}
summoningBattleCountsDict['Normal'] = sum(summoningBattleCountsDict.values())
