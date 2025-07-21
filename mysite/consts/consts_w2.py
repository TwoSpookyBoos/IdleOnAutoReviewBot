from utils.text_formatting import getItemDisplayName

max_index_of_vials = 75  # Last verified as of v2.29
max_vial_level = 13  # Last verified as of 2.29
max_maxable_vials = 69
vial_costs = [1, 100, 1000, 2500, 10e3, 50e3, 100e3, 500e3, 1e6, 5e6, 25e6, 100e6, 1e9]
max_implemented_bubble_index = 29  # Last verified as of v2.29
max_sigil_level = 3  # Last verified as of v2.29
min_NBLB = 2
max_NBLB = 1500
nblb_max_index = 24
nblb_skippable = [
    'Reely Smart', 'Bappity Boopity', 'Orange Bargain', 'Bite But Not Chew',  #Orange
    'Lil Big Damage', 'Anvilnomics', 'Cheap Shot', 'Green Bargain', 'Kill Per Kill',  #Green
    'Noodubble', 'Purple Bargain', 'Matrix Evolved',  #Purple
    'Yellow Bargain', 'Petting The Rift',  #Yellow
]
vials_dict = {
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
def getReadableVialNames(inputNumber):
    try:
        return f"{vials_dict[int(inputNumber)]['Name']} ({getItemDisplayName(vials_dict[int(inputNumber)]['Material'])})"
    except:
        return f"Unknown Vial {inputNumber}"


critter_vials_list = [
    getReadableVialNames(23),  #Crabbo
    getReadableVialNames(31),  #Mousey
    getReadableVialNames(37),  #Bunny
    getReadableVialNames(40),  #Honker
    getReadableVialNames(47),  #Blobfish
    getReadableVialNames(74),  #Tuttle
]
sigils_dict = {
    "Big Muscle":       {"Index": 0,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [2, 100, 50000], 'Values': [0, 10, 20, 40]},
    "Pumped Kicks":     {"Index": 2,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [3, 150, 60000], 'Values': [0, 10, 20, 40]},
    "Odd Litearture":   {"Index": 4,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [5, 200, 70000], 'Values': [0, 10, 20, 40]},
    "Good Fortune":     {"Index": 6,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [8, 300, 90000], 'Values': [0, 10, 20, 40]},
    "Plunging Sword":   {"Index": 8,  "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [15, 700, 100000], 'Values': [0, 75, 225, 1000]},
    "Wizardly Hat":     {"Index": 10, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [24, 1250, 130000], 'Values': [0, 10, 20, 30]},
    "Envelope Pile":    {"Index": 12, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [60, 2500, 160000], 'Values': [0, 10, 25, 40]},
    "Shiny Beacon":     {"Index": 14, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [120, 4000, 200000], 'Values': [0, 2, 2, 5]},
    "Metal Exterior":   {"Index": 16, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [250, 7000, 240000], 'Values': [0, 6, 12, 20]},
    "Two Starz":        {"Index": 18, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [500, 10000, 280000], 'Values': [0, 10, 25, 45]},
    "Pipe Gauge":       {"Index": 20, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [700, 12000, 320000], 'Values': [0, 10, 20, 30]},
    "Trove":            {"Index": 22, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [1300, 14000, 400000], 'Values': [0, 10, 20, 30]},
    "Pea Pod":          {"Index": 24, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [2100, 15000, 420000], 'Values': [0, 25, 50, 100]},
    "Tuft Of Hair":     {"Index": 26, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [3000, 25000, 450000], 'Values': [0, 3, 6, 10]},
    "Emoji Veggie":     {"Index": 28, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [4500, 33000, 480000], 'Values': [0, 10, 25, 40]},
    "VIP Parchment":    {"Index": 30, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [6300, 42000, 520000], 'Values': [0, 10, 25, 50]},
    "Dream Catcher":    {"Index": 32, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [7000, 50000, 560000], 'Values': [0, 1, 2, 4]},
    "Duster Studs":     {"Index": 34, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [8000, 60000, 600000], 'Values': [0, 3, 7, 15]},
    "Garlic Glove":     {"Index": 36, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [9000, 70000, 650000], 'Values': [0, 15, 25, 60]},
    "Lab Tesstube":     {"Index": 38, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [12000, 80000, 700000], 'Values': [0, 8, 20, 35]},
    "Peculiar Vial":    {"Index": 40, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [17000, 120000, 750000], 'Values': [0, 15, 25, 35]},
    "Loot Pile":        {"Index": 42, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [23000, 160000, 900000], 'Values': [0, 10, 20, 30]},
    "Div Spiral":       {"Index": 44, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [26000, 200000, 1200000], 'Values': [0, 10, 30, 50]},
    "Cool Coin":        {"Index": 46, "PlayerHours": 0, "Level": 0, "PrechargeLevel": 0, "Requirements": [30000, 250000, 2000000], 'Values': [0, 10, 30, 100]},
}
bubble_cauldron_color_list = ['Orange', 'Green', 'Purple', 'Yellow']
alchemy_liquids_list = ['Water Droplets', 'Liquid Nitrogen', 'Trench Seawater', 'Toxic Mercury']
alchemy_jobs_list = bubble_cauldron_color_list + alchemy_liquids_list + [k for k in sigils_dict.keys()]
bubbles_dict = {
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
def getReadableBubbleNames(inputNumber, color):
    try:
        return bubbles_dict[bubble_cauldron_color_list.index(color)][inputNumber]
    except:
        return f"Unknown {color} Bubble {inputNumber}"


atrisk_basic_bubbles = [
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
]  #Standard log, ore, fish, bug prints in W1-W3 bubbles
atrisk_advanced_bubbles = [
    'Warriors Rule', 'Big Meaty Claws', 'Call Me Bob', 'Brittley Spears', 'Buff Boi Talent', 'Orange Bargain',
    'Archer Or Bust', 'Quick Slap', 'Sanic Tools', 'Bow Jack', 'Cuz I Catch Em All', 'Green Bargain',
    'Mage Is Best', 'Hocus Choppus', 'Molto Loggo', 'Brewstachio', 'Call Me Pope', 'Smart Boi Talent', 'Purple Bargain',
    'Lotto Skills', 'Startue Exp', 'Level Up Gift', 'Grind Time', 'Cogs For Hands', 'Sample It', 'Big Game Hunter', 'Yellow Bargain',
]  #Advanced being anvil mats, monster mats, critters, souls in W1-W3 bubbles
atrisk_lithium_bubbles = [
    'Penny Of Strength',
    'Fly In Mind', 'Afk Expexp', 'Slabo Critterbug',
    'Nickel Of Wisdom', 'Severapurple', 'Hyperswift', 'Matrix Evolved', 'Slabe Logsoul',
    'Bit By Bit', 'Gifts Abound',
]  #Standard log, ore, fish, bug prints in W4+ bubbles
atrisk_lithium_advanced_bubbles = [
    'Multorange', 'Bite But Not Chew', 'Slabi Orefish', 'Gamer At Heart',
    'Premigreen', 'Sailor At Heart', 'Slabo Agility',
    'Tree Sleeper', 'Pious At Heart', 'Slabe Wisdom', 'Essence Boost-Purple',
    'Petting The Rift', 'Big P', 'Atom Split'
]  #Advanced being anvil mats, monster mats, critters, souls, sailing treasures in W4+ bubbles
arcade_bonuses = {
    # ArcadeShopInfo last pulled from code during v2.35 4th anniversary
    # ["+{_Base_Damage 1 0 add _ +{_Dmg".split(" "), "+{_Base_Defence 0.2 0 add _ +{_Def".split(" "), "+{%_Total_Accuracy 60 100 decay _ +{%_Acc".split(" "), "+{%_Mining_EXP_gain 60 100 decay % +{%_Min_EXP".split(" "), "+{%_Fishing_EXP_gain 60 100 decay % +{%_Fish_EXP".split(" "), "+{%_Sample_Size 4 100 decay % +{%_Size".split(" "), "+{%_AFK_Gains_Rate 4 100 decay % +{%_Rate".split(" "), "+{_Cap_for_all_Liquids 25 100 decay % +{_Cap".split(" "), "+{%_Multikill_per_Tier 10 100 decay % +{%_Multikill".split(" "), "+{%_Catching_EXP_gain 50 100 decay % +{%_Catch_EXP".split(" "), "+{%_Cash_from_Mobs 20 100 decay % +{%_Cash".split(" "), "+{%_Cash_from_Mobs 30 100 decay % +{%_Cash".split(" "), "+{%_Class_EXP_gain 20 100 decay % +{%_EXP".split(" "), "+{%_Shiny_Chance 100 100 decay % +{%_Chance".split(" "), "+{%_Trapping_EXP 50 100 decay % +{%_Trap_EXP".split(" "), "+{_Starting_TD_Pts 1 0 add _ +{_Worship_Pts".split(" "), "+{_Tab_1_Talent_Pt 1 10 intervalAdd _ +1_Pt_per_10_LVs".split(" "), "+{_Weapon_Power 0.07 0 add _ +{_Wep_POW".split(" "), "+{%_Skill_EXP_gain 20 100 decay % +{%_EXP".split(" "), "+{_Base_STR 1 0 add _ +{_STR".split(" "), "+{_Base_AGI 1 0 add _ +{_AGI".split(" "), "+{_Base_WIS 1 0 add _ +{_WIS".split(" "), "+{_Base_LUK 1 0 add _ +{_LUK".split(" "), "+{%_Trapping_Critters 30 100 decay % +{%_Critters".split(" "), "+{%_Worship_Souls 30 100 decay % +{%_Souls".split(" "), "+{%_Refinery_Speed 30 100 decay % +{%_Speed".split(" "), "+{%_Forge_Capacity 100 100 decay % +{%_Cap".split(" "), "+{%_Drop_Rate 30 100 decay % +{%_Drop".split(" "), "+{%_Cook_SPD_multi 40 100 decay % +{%_SPD".split(" "), "+{%_Lab_EXP_gain 30 100 decay % +{%_EXP".split(" "), "+{%_Breed_Pet_DMG 40 100 decay % +{%_DMG".split(" "), "+{%_Nugget_Regen 30 100 decay % +{%_Regen".split(" "), "+{%_Arti_Find 50 100 decay % +{%_Chance".split(" "), "+{%_Sailing_Loot 30 100 decay % +{%_Loot".split(" "), "+{%_W_Ess_gain 40 100 decay % +{%_W_Ess".split(" "), "+{%_Jade_gain 50 100 decay % +{%_Jade".split(" "), "+{%_Farming_EXP 30 100 decay % +{%_EXP".split(" "), "+{%_Divinity_EXP 40 100 decay % +{%_EXP".split(" "), "+{%_Villager_XP_multi 40 100 decay % +{%_XP_multi".split(" "), "+{%_Gold_Ball_Gain 1 0 add % +{%_Balls".split(" "), "+{%_Deathbringer_Bones 1 0 add % +{%_Bones".split(" "), "+{%_Equinox_Fill_Rate .75 0 add % +{%_Fill_Rate".split(" "), "+{%_Monument_AFK .5 0 add % +{%_AFK".split(" "), "+{%_Sigil_Speed 1 0 add % +{%_Speed".split(" "), "+{%_Construction_Build 2 0 add % +{%_Build_Rate".split(" "), "+{%_Burger 1 0 add % +{%_Burger".split(" "), "+{%_Total_Damage 2 0 add % +{%_Damage".split(" ")]
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
    40: {'Stat': 'Death Bringer Bones', 'x1': 1, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    41: {'Stat': 'Equinox Fill Rate', 'x1': 0.75, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    42: {'Stat': 'Monument AFK', 'x1': 0.50, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    43: {'Stat': 'Sigil Speed', 'x1': 1, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    44: {'Stat': 'Construction Build Rate', 'x1': 2, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    45: {'Stat': 'Burger (does nothing atm)', 'x1': 1, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    46: {'Stat': 'Total Damage', 'x1': 2, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    47: {'Stat': 'Wind Walker Dust', 'x1': 1, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    48: {'Stat': 'Medallion Chance', 'x1': 0.5, 'x2': 0, 'funcType': 'add', 'displayType': '%'},
    49: {'Stat': 'Breedability Rate', 'x1': 100, 'x2': 100, 'funcType': 'decay', 'displayType': '%'}
}
arcade_max_level = 100
post_office_tabs = ["Bob's Boxes", "Charlie's Crates"]
#po_box_dict last taken from code in 2.09: #PostOffUpgradeInfo = function ()
#Translate using the Post Office tab in AR spreadsheet
po_box_dict = {
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
max_po_box_before_myriad = sum([v['Max Level'] for v in po_box_dict.values() if v['Name'] != 'Myriad Crate'])
max_po_box_after_myriad = max_po_box_before_myriad + po_box_dict[20]['Max Level']
ballot_dict = {
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
fishing_toolkit_dict = {
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
obols_dict = {
    #Drop Rate
    "ObolBronzePop":    {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolBronzePop"), 'Base': {'LUK': 1, 'DEF': 1, '%_DROP_CHANCE': 2}},
    "ObolSilverPop":    {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolSilverPop"), 'Base': {'LUK': 3, 'DEF': 2, '%_DROP_CHANCE': 3}},
    "ObolHyper0":       {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolHyper0"), 'Base': {'WP': 1, '%_DROP_CHANCE': 4}},
    "ObolSilverLuck":   {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolSilverLuck"), 'Base': {'LUK': 2, '%_DROP_CHANCE': 5}},
    "ObolGoldLuck":     {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolGoldLuck"), 'Base': {'LUK': 3, '%_DROP_CHANCE': 7}},
    "ObolKnight":       {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolKnight"), 'Base': {'WP': 2, 'STR': 3, 'AGI': 3, 'WIS': 3, 'LUK': 3, 'DEF': 5, '%_DROP_CHANCE': 8}},
    "ObolHyperB0":      {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolHyper0"), 'Base': {'WP': 5, '%_DROP_CHANCE': 10}},
    "ObolPlatinumLuck": {"Shape": "Hexagon", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolPlatinumLuck"), 'Base': {'LUK': 5, '%_DROP_CHANCE': 10}},
    "ObolLava":         {"Shape": "Hexagon", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolLava"), 'Base': {'LUK': 10, '%_DROP_CHANCE': 14}},
    "ObolPinkLuck":     {"Shape": "Sparkle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolPinkLuck"), 'Base': {'LUK': 7, '%_DROP_CHANCE': 15}},

    #Card Drop Chance
    "ObolBronzeCard":   {"Shape":"Circle", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolBronzeCard"), "Base": {"%_CARD_DROP_CHANCE": 1}},
    "ObolSilverCard":   {"Shape": "Square", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolSilverCard"), "Base": {"%_CARD_DROP_CHANCE": 3, "STR": 1, "AGI": 1, "WIS": 1}},
    "ObolGoldCard":     {"Shape": "Hexagon", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolGoldCard"), "Base": {"%_CARD_DROP_CHANCE": 5, "STR": 2, "AGI": 2, "WIS": 2}},
    "ObolPlatinumCard": {"Shape": "Hexagon", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolPlatinumCard"), "Base": {"%_CARD_DROP_CHANCE": 7, "STR": 3, "AGI": 3, "WIS": 3}},
    "ObolPinkCard":     {"Shape": "Sparkle", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolPinkCard"), "Base": {"%_CARD_DROP_CHANCE": 10, "STR": 5, "AGI": 5, "WIS": 5, "WP": 1}},
}
obols_max_bonuses_dict = {
    'PlayerDropRatePractical': 134,         #12*4=48% circles, 6*8=48% squares,  2*11=22% hex, 1*16=16% sparkle
    'PlayerDropRateTrue': 172,              #12*5=60% circles, 6*11=66% squares, 2*15=30% hex, 1*16=16% sparkle
    'FamilyDropRatePractical': 188,         #12*4=48% circles, 4*8=32% squares,  4*11=44% hex, 4*16=64% sparkle
    'FamilyDropRateTrue': 228,              #12*5=60% circles, 4*11=44% squares, 4*15=60% hex, 4*16=64% sparkle

    'PlayerCardDropChancePractical': 75,    #12*2=24% circles, 6*4=24% square, 2*8=16% hex, 1*11=11% sparkle
    'PlayerCardDropChanceTrue': 75 ,        #12*2=24% circles, 6*4=24% square, 2*8=16% hex, 1*11=11% sparkle
    'FamilyCardDropChancePractical': 116,   #12*2=24% circles, 4*4=16% square, 4*8=32% hex, 4*11=44% sparkle
    'FamilyCardDropChanceTrue': 116         #12*2=24% circles, 4*4=16% square, 4*8=32% hex, 4*11=44% sparkle
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
    40e3: {'Reward': 'All Ninja twins get +2% Stealth per Sneaking level', 'Image': 'sneaking'},
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
