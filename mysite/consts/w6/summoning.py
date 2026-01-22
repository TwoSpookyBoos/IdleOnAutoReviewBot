from consts.idleon.w6.summoning import summoning_battle_per_color_dict

summoning_regular_match_colors = [
    "White",
    "Green",
    "Yellow",
    "Blue",
    "Purple",
    "Red",
    "Cyan",
    "Teal",
]

summoning_regular_reward_indexes = sorted(
    set(
        [
            battle["RewardIndex"]
            for color in summoning_regular_match_colors
            for battle in summoning_battle_per_color_dict[color]
        ]
    )
)

summoning_not_multi_bonus_indexes = [
    21,  # Stamp Levels
    23,  # Ballot Bonus
    25,  # Equinox Levels
    32,  # Winner Bonuses
]

summoning_bonus_img = {
    # Regular
    "Total DMG": "ballot-0",
    "Jade Gain": "jade-coin",
    "All Essence": "summoning",
    "Farming SPD": "farming",
    "Artifact Find": "sailing",
    "Lab Con Range": "laboratory",
    "Sneak EXP": "sneaking",
    "Sigil SPD": "sigils",
    "Farming EXP": "farming",
    "Drop Rate": "vault-upgrade-18",
    "Crop EVO": "farming",
    "AFK Gains": "vault-upgrade-23",
    "Skill EXP": "meritocracy-10",
    "Construct SPD": "construction",
    "Skill Effncy.": "ballot-7",
    "Cooking SPD": "cooking",
    "Gaming Bits": "gaming",
    "Shiny EXP": "breeding",
    "All Stat": "ballot-2",
    "Library Max": "library",
    # Endless
    "Stamp LV/day": "event-shop-1",
    "Villager EXP": "bravery-bonus-3",
    "Ballot Bonus": "bonus-ballot",
    "Class EXP": "ballot-15",
    "Equinox Max LV": "equinox",
    "Meal Bonuses": "cooking",
    "Amber Gain": "spelunking-amber-0",
    "Monument AFK": "bravery-bonus-8",
    "Winner Bonuses": "endless-summoning",
    "for World 7 #1": "placeholder",
    "for World 7 #2": "placeholder",
    "Spelunk POW": "spelunking-tool-0",
}

summoning_sanctuary_counts = [1]
for multi in range(3, 16):  # (3, 16) produces length of 14
    summoning_sanctuary_counts.append(multi * summoning_sanctuary_counts[-1])

summoning_boss_info = {
    "White": {"Name": "Aether", "Location": "Bamboo Laboredge", "EnemyID": "babaMummy"},
    "Green": {"Name": "Grover", "Location": "Lightway Path", "EnemyID": "slimeB"},
    "Yellow": {"Name": "Shimmer", "Location": "Yolkrock Basin", "EnemyID": "mini6a"},
    "Blue": {"Name": "Freezer", "Location": "Equinox Valley", "EnemyID": "mini3a"},
    "Purple": {"Name": "Hexer", "Location": "Jelly Cube Bridge", "EnemyID": "mini4a"},
    "Red": {"Name": "Cinder", "Location": "Crawly Catacombs", "EnemyID": "mini5a"},
    "Cyan": {
        "Name": "Zephyer",
        "Location": "Emperor's Castle Doorstep",
        "EnemyID": "Boss6A",
    },
}

summoning_doubler_recommendations = [
    # Unique damage multis
    "Brutal Units",
    "DMG Laundering",
    "Seeing Red",
    "Sharpened Spikes",
    # 90% of Group C
    "Final Card",
    "Jeweled Cards",
    "Infinite Damage",
    # Mana Generation in battle
    "Mana Generation",
    "Manaranarr",
    "Mana Dividends",
    # Rest of the base damage group
    "Beefier Units",
    "Stronger Units",
    "Powerful Units",
    "Unit Damage",
    # Rest of Group C
    "Units of Destruction",
    "Merciless Units",
    "Re-Draw",
    "Starting Mana frfr",
    "Infinite Essence",
]
