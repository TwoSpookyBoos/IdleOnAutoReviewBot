from consts.idleon.w1.bribes import BribeDescriptions

bribes_dict = {
    "W1": ["Insider Trading", "Tracking Chips", "Mandatory Fire Sale", "Sleeping On the Job", "Artificial Demand", "The Art of the Deal"],
    "W2": ["Overstock Regulations", "Double EXP Scheme", "Tagged Indicators", "Fossil Fuel Legislation", "Five Aces in the Deck", "Fake Teleport Tickets", "The Art of the Steal"],
    "W3": ["Counterfeit Telepassports", "Weighted Marbles", "Changing the Code", "Taxidermied Cog Pouches", "Guild VIP Fraud", "Library Double Agent", "The Art of the Fail"],
    "W4": ["Photoshopped Dmg Range", "Glitched Acc Formula", "Firewalled Defence", "Bottomless Bags", "AFKeylogging", "Guild GP Hack"],
    "Trash Island": ["The Art of the Bail", "Random Garbage", "Godlier Creation", "Fishermaster", "Muscles on Muscles", "Bottle Service", "Star Scraper"],
    "W6": ["The Art of the Grail", "Artifact Pilfering", "Forge Cap Smuggling", "Gold from Lead", "Nugget Fabrication", "Divine PTS Miscounting", "Loot Table Tampering", "The Art of the Flail"]
}

# See the end of `BribeDescriptions = function` in source. Last updated in v2.528.0
unpurchasable_bribes = ["The Art of the Flail"]

# Default unit is %
bribe_units = {
    'Five Aces in the Deck': 'x',
    'Forge Cap Smuggling': 'x',
    'Loot Table Tampering': 'x',
    'Fossil Fuel Legislation': '',
    'Fake Teleport Tickets': '',
    'Counterfeit Telepassports': '',
    'Changing the Code': '',
    'Taxidermied Cog Pouches': '',
    'Guild VIP Fraud': '',
    'Library Double Agent': '',
    'Guild GP Hack': '',
    'Random Garbage': '',
    'Godlier Creation': '',
    'Fishermaster': '',
    'Star Scraper': '',
}

# Game names differ in casing, so pair by index
bribes = [
    {
        'Set': set_name,
        'Name': name,
        'Value': 0 if info[4] == 'BribeExpansion' else float(info[5]),
        'Unit': bribe_units.get(name, '%'),
        'Unpurchasable': name in unpurchasable_bribes,
    }
    for (set_name, name), info in zip(
        [(set_name, name) for set_name, names in bribes_dict.items() for name in names],
        BribeDescriptions
    )
]
