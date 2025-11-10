from consts.consts_idleon import NinjaInfo
from utils.text_formatting import numberToLetter
from utils.number_formatting import parse_number

bribes_dict = {
    "W1": ["Insider Trading", "Tracking Chips", "Mandatory Fire Sale", "Sleeping On the Job", "Artificial Demand", "The Art of the Deal"],
    "W2": ["Overstock Regulations", "Double EXP Scheme", "Tagged Indicators", "Fossil Fuel Legislation", "Five Aces in the Deck", "Fake Teleport Tickets", "The Art of the Steal"],
    "W3": ["Counterfeit Telepassports", "Weighted Marbles", "Changing the Code", "Taxidermied Cog Pouches", "Guild VIP Fraud", "Library Double Agent", "The Art of the Fail"],
    "W4": ["Photoshopped Dmg Range", "Glitched Acc Formula", "Firewalled Defence", "Bottomless Bags", "AFKeylogging", "Guild GP Hack"],
    "Trash Island": ["The Art of the Bail", "Random Garbage", "Godlier Creation", "Fishermaster", "Muscles on Muscles", "Bottle Service", "Star Scraper"],
    "W6": ["The Art of the Grail", "Artifact Pilfering", "Forge Cap Smuggling", "Gold from Lead", "Nugget Fabrication", "Divine PTS Miscounting", "Loot Table Tampering", "The Art of the Flail"]
}

# See the end of `BribeDescriptions` in source. Last updated in v2.43 Nov 6
unpurchasable_bribes = ["The Art of the Flail"]
stamp_types = ['Combat', 'Skill', 'Misc']

# Last updated in v2.10
unavailable_stamps_list = [
    'Shiny Crab Stamp', 'Gear Stamp', 'SpoOoky Stamp', 'Prayday Stamp',  #Skill
    'Talent I Stamp', 'Talent V Stamp',  #Misc
]
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
    'Cavern Resource Stamp': 240,
    'Study Hall Stamp': 165
}
stamps_dict = {
    #addNewQuest("StampA1" -> desc_line1 has the scaling, and material
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
        42: {'Name': "Splosion Stamp", 'funcType': 'decay', 'x1': 50, 'x2': 200, 'Material': 'earl-tail'},
        43: {'Name': "Gud EXP Stamp", 'funcType': 'decay', 'x1': 5, 'x2': 200, 'Material': 'earl-tail'},
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
        54: {'Name': "Amber Stamp", 'funcType': 'decay', 'x1': 30, 'x2': 150, 'Material': 'spelunking-chapter-2'},
        55: {'Name': "Little Rock Stamp", 'funcType': 'decay', 'x1': 200, 'x2': 220, 'Material': 'spelunking-chapter-1'},
        56: {'Name': "Hardhat Stamp", 'funcType': 'decay', 'x1': 50, 'x2': 150, 'Material': 'spelunking-chapter-3'},
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
        23: {'Name': 'Cavern Resource Stamp', 'funcType': 'decay', 'x1': 100, 'x2': 250, 'Material': 'cooking-ladle'},
        24: {'Name': 'Study Hall Stamp', 'funcType': 'decay', 'x1': 30, 'x2': 160, 'Material': 'villager-statue'},
        25: {'Name': 'Kruker Stamp', 'funcType': 'add', 'x1': 1, 'x2': 0, 'Material': 'equinox-flesh'},
        26: {'Name': 'Corale Stamp', 'funcType': 'decay', 'x1': 10, 'x2': 150, 'Material': 'demonflesh'},
    }
}
capacity_stamps = ["Mason Jar Stamp", "Lil' Mining Baggy Stamp", "Choppin' Bag Stamp", "Matty Bag Stamp", "Bag o Heads Stamp", "Bugsack Stamp"]
stamps_exalt_recommendations = [
    'Crystallin', 'Mason Jar Stamp', 'Summoner Stone Stamp', 'Multitool Stamp',
    'Matty Bag Stamp', 'Golden Sixes Stamp', 'Drippy Drop Stamp', 'Gold Ball Stamp',
    'Refinery Stamp', 'Bugsack Stamp', 'Bag o Heads Stamp', "Lil' Mining Baggy Stamp", "Choppin' Bag Stamp",
    'Card Stamp', 'Divine Stamp', 'Golden Apple Stamp', 'Vendor Stamp', 'Study Hall Stamp', 'Cavern Resource Stamp',
]

# Passive Starsigns do not consume an Infinite Star Sign point and are the 3 big signs you can't align to.
# Last updated in v2.43 Nov 10
passive_starsigns = ['Chronus_Cosmos', 'Hydron_Cosmos', 'Seraph_Cosmos']

# `StarSigns` in source. Last updated in v2.43 Nov 10
StarSigns = [["The_Buff_Guy", "+1%_Total_Damage", "+3_STR", "_"], ["Flexo_Bendo", "+2%_Movement_Speed", "+3_AGI", "_"], ["The_Book_Worm", "+1%_Class_EXP_Gain", "+3_WIS", "_"], ["The_Fuzzy_Dice", "+3_Talent_Points", "+3_LUK", "_"], ["Dwarfo_Beardus", "+5%_Mining_Efficency", "+20%_Multi-Ore_Chance", "_"], ["Hipster_Logger", "+5%_Chop_Efficiency", "+20%_Multi-Log_Chance", "_"], ["Pie_Seas", "+5%_Fishin_Efficency", "+20%_Multi-Fish_Odds", "_"], ["Shoe_Fly", "+5%_Catch_Efficiency", "+20%_Multi-Bug_Chance", "_"], ["Blue_Hedgehog", "+4%_Movement_Speed", "+0.0001%_Ring_Drop", "_"], ["Gum_Drop", "+15%_to_get_a_Time", "Candy_when_claiming", "8+_Hour_AFK_gains"], ["Activelius", "+15%_Class_EXP_when", "fighting_actively", "_"], ["Pack_Mule", "+10%_Carry_Cap", "_", "_"], ["Ned_Kelly", "+6%_Defence", "+2_Weapon_Power", "_"], ["Robinhood", "+4%_Accuracy", "+2%_Movement_Speed", "+1_Cant_Trade_GME"], ["Pirate_Booty", "+5%_Drop_Rate", "_", "_"], ["Muscle_Man", "+8_STR", "_", "_"], ["Fast_Frog", "+8_AGI", "_", "_"], ["Smart_Stooge", "+8_WIS", "_", "_"], ["Lucky_Larry", "+8_LUK", "_", "_"], ["Silly_Snoozer", "+2%_Fight_AFK_Gain", "_", "_"], ["The_Big_Comatose", "+2%_Skill_AFK_Gain", "_", "_"], ["Miniature_Game", "+30%_minigame_reward", "_", "_"], ["Mount_Eaterest", "+10%_chance_to_not", "consume_food", "+15%_All_Food_Effect"], ["Bob_Build_Guy", "+10%_Speed_in_Town", "Skills", "_"], ["The_Big_Brain", "+3%_Class_EXP_gain", "_", "_"], ["The_OG_Skiller", "+5%_Carry_Cap", "+1%_Skill_AFK_gain", "+2%_All_Skill_Prowess"], ["Grim_Reaper", "+2%_Mob_Respawn_rate", "_", "_"], ["The_Fallen_Titan", "+3%_Boss_Damage", "+4%_Crit_Chance", "_"], ["The_Forsaken", "-80%_Total_HP", "-50%_Defence", "+6%_Fight_AFK_Gain"], ["Mr_No_Sleep", "-6%_AFK_Gain", "+30%_Carry_Cap", "_"], ["Sir_Savvy", "+3%_Skill_EXP_gain", "_", "_"], ["All_Rounder", "+4_All_Stats", "_", "_"], ["Fatty_Doodoo", "-3%_Movement_Speed", "+5%_Defence", "+2%_Total_Damage"], ["Chronus_Cosmos", "All_characters_can", "now_align_with_2", "Star_Signs_at_once"], ["All_Rounderi", "+1%_All_Stat", "i.e._STR/AGI/WIS/LUK", "_"], ["Centaurii", "+10%_Accuracy", "_", "_"], ["Murmollio", "+10%_Defence", "_", "_"], ["Strandissi", "+3%_STR", "_", "_"], ["Agitagi", "+3%_AGI", "_", "_"], ["Wispommo", "+3%_WIS", "_", "_"], ["Lukiris", "+3%_LUK", "_", "_"], ["Pokaminni", "+15%_Card_Drop", "(Outside_of_Dungeons)", "_"], ["Gor_Bowzor", "+12%_Boss_Damage", "_", "_"], ["Hydron_Cosmos", "All_characters_can", "now_align_with_3", "Star_Signs_at_once"], ["Trapezoidburg", "+20%_Critters/Trap", "+10%_Trap_Efficiency", "_"], ["Sawsaw_Salala", "+25%_Construct_Exp", "_", "_"], ["Preys_Bea", "+15%_Worship_Efficiency", "+15%_Worship_EXP", "_"], ["Cullingo", "+15%_Total_Multikill", "_", "_"], ["Gum_Drop_Major", "+40%_to_get_a_Time", "Candy_when_claiming", "40+_Hour_AFK_gains"], ["Grim_Reaper_Major", "+4%_Mob_Respawn_rate", "(If_Lv&60)", "_"], ["Sir_Savvy_Major", "+6%_Skill_EXP_gain", "(If_Lv&70)", "_"], ["The_Bulwark", "+20%_Total_Damage", "-12%_Movement_Speed", "_"], ["Big_Brain_Major", "+6%_Class_EXP_gain", "(If_Lv&80)", "_"], ["The_Fiesty", "+6%_Total_Damage", "_", "_"], ["The_Overachiever", "+15%_Total_Damage", "-7%_Fight_AFK_Gain", "_"], ["Comatose_Major", "+4%_Skill_AFK_Gain", "(If_Lv&90)", "_"], ["S._Snoozer_Major", "+4%_Fight_AFK_Gain", "(If_Lv&100)", "_"], ["Breedabilli", "+35%_Breedable_Spd", "+15%_Shiny_Pet_LV_spd", "_"], ["Gordonius_Major", "+15%_Cooking_SPD", "(Multiplicative!)", "_"], ["Power_Bowower", "+30%_Pet_DMG_for", "Breeding_Skill", "_"], ["Scienscion", "+20%_Lab_EXP_Gain", "_", "_"], ["Artifosho", "+15%_Artifact_Find", "Chance", "(Multiplicative)"], ["Divividov", "+30%_Divinity_EXP", "_", "_"], ["C._Shanti_Minor", "+20%_Sailing_SPD", "_", "_"], ["Muscle_Magnus", "+50_STR", "_", "_"], ["Cropiovo_Minor", "+3%_Crop_Evo", "chance_per_Farming_LV", "_"], ["Fabarmi", "+20%_Farming_EXP", "_", "_"], ["O.G._Signalais", "+15%_OG_Chance", "_", "_"], ["Lightspeed_Frog", "+50_AGI", "_", "_"], ["Beanbie_Major", "+20%_Golden_Food", "bonuses", "_"], ["Damarian_Major", "+25%_Total_Damage", "_", "_"], ["Lotto_Larrinald", "+50_LUK", "_", "_"], ["Intellostooge", "+50_WIS", "_", "_"], ["S._Tealio", "+12%_Ninja_Twin", "Stealth", "_"], ["Sneekee_E._X.", "+15%_Sneaking_EXP", "_", "_"], ["Jadaciussi", "+10%_Jade_Gain", "(Multiplicative!)", "_"], ["Druipi_Major", "+12%_Drop_Rarity", "_", "_"], ["Sumo_Magno", "+20%_Summoning_EXP", "_", "_"], ["Killian_Maximus", "+3%_Multikill_Per_Tier", "_", "_"], ["Seraph_Cosmos", "All_characters_now_get", "1.10x_Star_Sign_bonuses", "per_20_Summoning_LV"], ["Glimmer_of_Beyond", "This_star_sign_is", "unreachable_for_now...", "_"], ["Fillerz48", "_", "_", "_"], ["Fillerz49", "_", "_", "_"], ["Fillerz50", "_", "_", "_"], ["Fillerz51", "_", "_", "_"], ["Fillerz52", "_", "_", "_"], ["Fillerz53", "_", "_", "_"], ["Fillerz54", "_", "_", "_"], ["Fillerz55", "_", "_", "_"], ["Fillerz56", "_", "_", "_"], ["Fillerz57", "_", "_", "_"], ["Fillerz58", "_", "_", "_"], ["Fillerz59", "_", "_", "_"], ["Fillerz32", "_", "_", "_"]]
starsigns_dict = {
    index: {
        'Name': name.replace('_', ' '),
        'Passive': name in passive_starsigns,
        'Bonus1': bonus1.replace('_', ' '),
        'Bonus2': bonus2.replace('_', ' '),
        'Bonus3': bonus3.replace('_', ' '),
    }
    for index, (name, bonus1, bonus2, bonus3) in enumerate(StarSigns) if not name.startswith("Fillerz")
}

forge_upgrades_dict = {
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


# `StatueInfo` in source. Last updated in v2.43 Nov 10
StatueInfo = [["POWER", "@BASE_DAMAGE", "30", "3"], ["SPEED", "%@MOVE_SPEED", "65", "0.1"], ["MINING", "@MINING_POWER", "280", "0.3"], ["FEASTY", "%@FOOD_EFFECT", "320", "1"], ["HEALTH", "@BASE_HEALTH", "0", "3"], ["KACHOW", "%@CRIT_DAMAGE", "-15", "0.4"], ["LUMBERBOB", "@CHOPPIN_POWER", "90", "0.3"], ["THICC_SKIN", "@BASE_DEFENCE", "210", "1"], ["OCEANMAN", "@FISHING_POWER", "115", "0.3"], ["OL_RELIABLE", "@CATCHIN_POWER", "45", "0.3"], ["EXP", "%@CLASS_EXP", "0", "0.1"], ["ANVIL", "%@PRODUCT_SPD", "165", "0.5"], ["CAULDRON", "%@ALCHEMY_EXP", "280", "0.5"], ["BEHOLDER", "%@CRIT_CHANCE", "300", "0.2"], ["BULLSEYE", "%@ACCURACY", "110", "0.8"], ["BOX", "@TRAPPIN_POWER", "180", "0.3"], ["TWOSOUL", "@WORSHIP_POWER", "260", "0.3"], ["EHEXPEE", "%@SKILL_EXP", "69", "0.1"], ["SEESAW", "%@CONS_EXP", "13", "0.5"], ["PECUNIA", "%@COINS", "50", "1"], ["MUTTON", "%@COOKING_EXP", "0", "0.3"], ["EGG", "%@BREEDING_EXP", "25", "0.4"], ["BATTLEAXE", "%@DAMAGE", "300", "0.2"], ["SPIRAL", "%@DIVINITY_EXP", "70", "1"], ["BOAT", "%@SAILING_SPD", "210", "0.5"], ["COMPOST", "%@FARMING_EXP", "75", "0.4"], ["STEALTH", "%@STEALTH", "185", "0.3"], ["ESSENCE", "%@WHITE_ESS", "160", "0.6"], ["VILLAGER", "%@VILLAGER_EXP", "120", "0.3"], ["DRAGON", "%@STATUES_BONUS", "270", "0.2"], ["SPELUNKY", "%@SPELUNK_EXP", "43", "0.2"], ["CORAL", "%@DAILY_CORAL", "181", "0.02"]]
statue_farming = {
    0:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    1:  {"Farmer": "W1-W3 Crystals with DK", "Resource": "w1-w3-crystals"},
    2:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    3:  {"Farmer": "W1-W3 Crystals with DK", "Resource": "w1-w3-crystals"},
    4:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    5:  {"Farmer": "Monolith Quest on All characters", "Resource": "monolith"},
    6:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    7:  {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    8:  {"Farmer": "AFK or Candy with Vman at W2 Bugs", "Resource": "fly-nest"},
    9:  {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    10: {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    11: {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    12: {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    13: {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    14: {"Farmer": "Active ES at Wood Mushroom or Candy at Nutto", "Resource": "wood-mushroom"},
    15: {"Farmer": "Candy or Active ES at Penguins", "Resource": "penguin"},
    16: {"Farmer": "Candy or Active ES at Quenchies", "Resource": "quenchie"},
    17: {"Farmer": "Crystals with DK at Bloodbones", "Resource": "bloodbone"},
    18: {"Farmer": "Candy or Active ES at Cryosnakes", "Resource": "cryosnake"},
    19: {"Farmer": "Crystals with DK at Clammies", "Resource": "clammie"},
    20: {"Farmer": "Crystals with DK at Clammies", "Resource": "clammie"},
    21: {"Farmer": "Crystals with DK at Clammies", "Resource": "clammie"},
    22: {"Farmer": "Crystals with DK at Tremor Wurms", "Resource": "tremor-wurm"},
    23: {"Farmer": "Crystals with DK at Tremor Wurms", "Resource": "tremor-wurm"},
    24: {"Farmer": "Crystals with DK at Tremor Wurms", "Resource": "tremor-wurm"},
    25: {"Farmer": "Crystals with DK at Minichiefs", "Resource": "minichief-spirit"},
    26: {"Farmer": "Crystals with DK at Minichiefs", "Resource": "minichief-spirit"},
    27: {"Farmer": "Crystals with DK at Minichiefs", "Resource": "minichief-spirit"},
    28: {"Farmer": "AFK {{Cavern 9|#villagers}}", "Resource": "gloomie-mushroom"},
    29: {"Farmer": "AFK {{Cavern 15|#villagers}}", "Resource": "ancient-golem"},
    30: {"Farmer": "W7 Crystals with DK", "Resource": ""},
    31: {"Farmer": "W7 Crystals with DK", "Resource": ""}
}
statues_dict = {
    index: {
        'Name': f"{name.replace('_', ' ').title()} Statue",
        'ItemName': f"EquipmentStatues{index+1}",
        'Effect': effect.replace('@', ' ').replace('_', ' ').strip().title(),
        'BaseValue': parse_number(basevalue),
        'Farmer': statue_farming.get(index, {}).get('Farmer', ''),
        'Resource': statue_farming.get(index, {}).get('Resource', ''),
    }
    for index, (name, effect, pos2, basevalue) in enumerate(StatueInfo)
}
statue_type_list = ['Normal', 'Gold', 'Onyx']
statue_count = len(statues_dict.keys())

# Found near end of `NinjaInfo` in source. Last updated in v2.43 Nov10
NinjaInfo_event_shop = NinjaInfo[39]
event_points_shop_dict = {
    NinjaInfo_event_shop[index].split('@')[0].replace('_', ' ').strip(): {
        'Cost': NinjaInfo_event_shop[index+1],
        'Code': numberToLetter(int(index/2)),
        'Image': f'event-shop-{int(index/2)}',
        'Description': NinjaInfo_event_shop[index].split('@')[1].replace('_', ' ').strip()
    }
    for index in range(0, len(NinjaInfo_event_shop), 2)
}
