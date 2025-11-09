import re

from utils.text_formatting import numeralList, numberToLetter

artifact_tiers = ['Base', 'Ancient', 'Eldritch', 'Sovereign']
max_sailing_artifact_level = len(artifact_tiers)

# `_customBlock_Sailing -> "MaxChests"` in source. Last updated in v2.43
# Seems to be clamped to 34 by `Math.min`
max_sailing_chests = 34

sailing_artifacts_list = [
    'Moai Head', 'Maneki Kat', 'Ruble Cuble', 'Fauxory Tusk', 'Gold Relic',
    'Genie Lamp', 'Silver Ankh', 'Emerald Relic', 'Fun Hippoete', 'Arrowhead',
    '10 AD Tablet', 'Ashen Urn', 'Amberite', 'Triagulon', 'Billcye Tri',
    'Frost Relic', 'Chilled Yarn', 'Causticolumn', 'Jade Rock', 'Dreamcatcher',
    'Gummy Orb', 'Fury Relic', 'Cloud Urn', 'Weatherbook', 'Giants Eye',
    'Crystal Steak', 'Trilobite Rock', 'Opera Mask', 'Socrates', 'The True Lantern',
    'The Onyx Lantern', 'The Shim Lantern', 'The Winz Lantern'
]
sailing_artifacts_count = len(sailing_artifacts_list)
sailing_dict = {
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
captain_buffs = ['Boat Speed', 'Loot Value', 'Cloud Discover Rate', 'Artifact Find Chance', 'Rare Chest Chance', 'None']
goldrelic_multis_dict = {
    0: 0,
    1: 2,
    2: 2.5,
    3: 3,
    4: 5
}
divinity_divinities_dict = {
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
divinity_offerings_dict = {
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
divinity_styles_dict = {
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
div_level_reasons_dict = {
    0: "",
    2: "to activate Doot",
    40: "to unlock the TranQi Style.",
    50: "to unlock the Multitool Stamp from Poigu's quest."
}
divinity_DivCostAfter3 = 40  # Last verified as of v2.12 Ballot
divinity_arctis_breakpoints = {
    12: { 60:  841,  61:  602,  62:  467,  63:  380,  64:  319,  65:  275,  66:  241},
    13: { 72:  841,  73:  647,  74:  525,  75:  441,  76:  379,  77:  332,  78:  295},
    14: { 85: 1331,  86:  986,  87:  782,  88:  648,  89:  522,  90:  481,  91:  425,  92:  381},
    15: {102: 1641, 103: 1246, 104: 1004, 105:  841, 106:  722, 107:  633, 108:  564, 109:  508, 110:  462},
    16: {122: 3601, 123: 2401, 124: 1801, 125: 1441, 126: 1201, 127: 1029, 128:  901, 129:  801, 130:  721},
    17: {150: 4441, 151: 3101, 152: 2383, 153: 1936, 154: 1631, 155: 1409, 156: 1241, 157: 1002},
    18: {188: 5983, 189: 4302, 190: 3361, 191: 2759, 192: 2341, 193: 2033, 194: 1798, 195: 1612},
    19: {244: 6041, 245: 4841, 246: 4041, 247: 3469, 248: 3041, 249: 2707, 250: 2441},
    20: {332: 6731, 333: 5817, 334: 5123, 335: 4579, 336: 4141, 337: 3780, 338: 3478}
}

def _parse_gaming_superbits(raw_game_data):
    name_counts = {}

    gaming_superbits_dict = {}
    for idx, (bonus_text, base, exp, name) in enumerate(raw_game_data):
        name = name.replace("_", " ").replace("|", " ")
        bonus_text = (re.sub("_+Total_Bonus.*$", "", bonus_text, flags=re.IGNORECASE)
                      .replace("\u20a3", " Bits")
                      .replace("_", " ")
                      .replace("(}).", "")
                      .strip())
        cost = int(base) * 10 ** int(exp)

        name_num = name_counts.get(name, 0) + 1
        name_counts[name] = name_num
        if name_num > 1:
            name += " " + numeralList[name_num-1]

        gaming_superbits_dict[name] = {
            "BonusText": bonus_text,
            "Cost": cost,
            "CodeString": numberToLetter(idx)
        }

    return gaming_superbits_dict

# `GamingUpg = function()` in source. Last updated in v2.43 Nov 6 (World 7)
gaming_superbits_dict = _parse_gaming_superbits([["x1.03\u20a3_per_Achievement_you've_unlocked_(}).___Total_bonus:_x{\u20a3","1","9","Bits_Per|Achievement"],["+1_Max_Evolution_for_all_plants._This_is_20x_rarer_than_normal_evolutions","3","10","Plant|evo"],["All_obols_give_+40%_more_STR/AGI/WIS/LUK_than_what_they_say_they_do!","2","12","obol_stat|booster"],["MSA_now_gives_+1%_bonus_Sailing_Speed_per_10_total_Waves","5","16","MSA|Sailing"],["+20%_chance_for_+1_more_bubble_boosted_by_No_Bubble_Left_Behind","1","22","Moar|Bubbles"],["+1_Max_Evolution_for_all_plants._This_one_is_5000x_rarer_than_normal","3","44","Plant|evo"],["+5_Max_HP_for_Worship_Totem_during_Tower_Defence_summon_battle","2","11","Worship|Totem_HP"],["Unlock_the_Totalizer_for_the_Miniature_Soul_Apparatus_(MSA)_in_World_3","5","13","MSA|Totalizer"],["All_shrines_level_up_+50%_faster_than_normal","5","14","Shrine|Speed"],["If_no_Prayers_equipped,_get_1/5th_bonus_of_all_prayers,_and_no_curses","3","17","No_more|Praying"],["+15%_chance_for_Double_Exp_whenever_claiming_AFK_gains","2","23","Double|Exp"],["MSA_now_gives_+1%_bonus_Class_EXP_per_10_total_Waves","4","38","MSA|Class_EXP"],["+1%_Library_Checkout_Speed_per_Gaming_Lv.___Total_Bonus:_+{%_Spd","4","19","Library|Checkouts"],["MSA_now_gives_+10%_bonus_Meal_Cooking_speed_per_10_total_Waves","2","20","MSA|Mealing"],["All_spice_claimed,_either_manually_or_automatically,_is_worth_1.5x_more.","4","25","Spice|Is_Nice"],["+10_Max_HP_for_Worship_Totem_during_Tower_Defence_summon_battle","4","31","Worship|Totem_HPr"],["MSA_now_gives_+1%_bonus_Skill_Exp_per_10_total_Waves","4","41","MSA|Skill_EXP"],["All_spice_claimed,_either_manually_or_automatically,_is_worth_2x_more.","5","47","Spice|Is_Nicer"],["+1_Max_Evolution_for_all_plants._This_one_is_250x_rarer_than_normal","2","27","Plant|evo"],["Your_lowest_Leveled_character_gets_1.5x_Class_EXP","4","29","Noobie|Gains"],["MSA_now_gives_+50%_Bits_for_Gaming_per_10_total_Waves","5","33","MSA|Big_Bits"],["All_atom_upgrading_is_now_10%_cheaper","2","36","Atom|Redux"],["+30%_chance_for_+1_more_bubble_boosted_by_No_Bubble_Left_Behind","4","45","Even_Moar|Bubbles"],["All_atoms_now_have_+10_Max_LV","2","50","Isotope|Discovery"],["1.01x_Class_EXP_per_Spelunk_Discovery.___________Total_Bonus:_{x_EXP","5","51","Classy|Discoveries"],["Adds_a_new_bonus_to_The_Slab:_+%_Total_Spelunking_POW","2","53","Slabby|Spelunking"],["1.02x_Artifact_chance_per_Spelunk_Discovery.__________Total_Bonus:_{x","6","55","Artifacto|Discoveries"],["MSA_now_gives_+1%_Spelunking_POW_per_10_total_Waves","6","58","MSA|Spelunking"],["+20%_Palette_Luck_per_Snail_LV_over_25.________Total_Bonus:_+{%_Luck","6","65","Lucky|Snail"],["The_Immortal_Snail_now_has_+10_Max_LV","5","71","Snail|Genesis"],["The_Immortal_Snail_now_has_+5_Max_LV","3","52","Snail|Omega"],["Monument_reward_multi_increases_normally_for_+10_more_days","9","54","Monument|Infimulti"],["1.05x_Collectible_chance_per_Spelunk_Discovery._______Total_Bonus:_{x","8","57","Jar_Jar|Collectible"],["Collect_Ultimate_Cogs_while_there_are_5+_left_to_get_a_Jewel_Cog_(1/day)","2","59","Jewel|Cogs"],["Adds_a_new_bonus_to_slab_when_W7_Skill_2_comes_out","3","67","Slabby|Something"],["+10_Max_LV_for_Equinox_upgrades","4","73","Equinox|Unending"],["Can_use_Spelunking_tools_you_don't_have_enough_stamina_for","6","58","Any_tool|Any_time"],["The_Squirrel_now_has_a_new_3rd_upgrade_to_spend_acorns_on","7","61","Squirrel|Triad"],["+1%_Palette_Luck_per_Total_Colour_LVs.__________Total_Bonus:_+{%_Luck","6","64","Colourful|Luck"],["If_no_Prayers_equipped,_get_2/5th_bonus_of_all_prayers,_and_no_curses","2","69","Prayers|Begone"],["The_Immortal_Snail_now_has_+10_Max_LV","5","70","Snail|Zenith"],["Adds_a_new_bonus_to_slab_when_W7_Skill_3_comes_out","7","76","Slabby|Something"],["+1_Palette_Colour_Slot,_and_2x_total_Palette_Luck!","3","60","Bigger|Palette"],["Bolaia_studies_ALSO_adjacent_caverns,_not_just_the_selected_one!","6","63","Peripheral|Vision"],["MSA_will_give_a_bonus_for_W7_skill_2_when_released...","1","68","MSA|Something"],["+3%_Palette_Luck_per_Gaming_LV_over_200._______Total_Bonus:_+{%_Luck","3","72","Gamer|Luck"],["MSA_will_give_a_bonus_for_W7_skill_3_when_released...","6","74","MSA|Something"],["+1_LV_for_all_Talents_per_100_Class_LV_over_500.______Total_Bonus:_+{_LV","8","78","Timmy|Talented"]])
snail_max_rank = 25 # TODO: Remove as this is not constant


def getDivinityNameFromIndex(inputValue: int) -> str:
    if inputValue == 0:
        return "Unlinked"
    return divinity_divinities_dict.get(inputValue, {"Name": f"UnknownDivinity{inputValue}"}).get("Name")


def getOfferingNameFromIndex(inputValue):
    return divinity_offerings_dict.get(inputValue, {"Name": f"UnknownOffering{inputValue}"}).get("Name")


def getStyleNameFromIndex(inputValue: int) -> str:
    return divinity_styles_dict.get(inputValue, {"Name": f"UnknownStyle{inputValue}"}).get("Name")


###SLAB CONSTS###
#SlabItemSort last pulled from code in v2.37 Wind Walker class
slab_list = "Copper Iron Gold Plat Dementia Void Lustre Starfire Marble Dreadlo Godshard Motherlode CopperBar IronBar GoldBar PlatBar DementiaBar VoidBar LustreBar StarfireBar MarbleBar DreadloBar GodshardBar OakTree BirchTree JungleTree ForestTree ToiletTree PalmTree StumpTree SaharanFoal Tree7 AlienTree Tree8 Tree9 Tree11 Tree10 Tree12 Tree13 MotherlodeTREE Leaf1 Leaf2 Leaf3 Leaf4 Leaf5 Leaf6 Fish1 Fish2 Fish3 Fish4 Fish5 Fish6 Fish7 Fish8 Fish9 Fish10 Fish11 Fish12 Fish13 Fish14 Bug1 Bug2 Bug3 Bug4 Bug5 Bug6 Bug7 Bug8 Bug9 Bug11 Bug10 Bug12 Bug13 Bug14 Critter1 Critter1A Critter2 Critter2A Critter3 Critter3A Critter4 Critter4A Critter5 Critter5A Critter6 Critter6A Critter7 Critter7A Critter8 Critter8A Critter9 Critter9A Critter10 Critter10A Critter11 Critter11A Soul1 Soul2 Soul3 Soul4 Soul5 Soul6 Soul7 Refinery1 Refinery2 Refinery3 Refinery4 Refinery5 Refinery6 CraftMat1 CraftMat2 CraftMat3 CraftMat5 CraftMat6 CraftMat7 CraftMat9 CraftMat8 CraftMat10 CraftMat11 CraftMat12 CraftMat13 CraftMat14 OilBarrel1 OilBarrel2 OilBarrel3 OilBarrel4 OilBarrel5 OilBarrel6 OilBarrel7 PureWater PureWater2 Grasslands1 Grasslands2 Grasslands3 Grasslands4 Jungle1 Jungle2 Jungle3 Forest1 Forest2 Forest3 Sewers1 Sewers1b Sewers2 Sewers3 TreeInterior1 TreeInterior1b TreeInterior2 DesertA1 DesertA1b DesertA2 DesertA3 DesertA3b DesertB1 DesertB2 DesertB3 DesertB4 DesertC1 DesertC2 DesertC2b DesertC3 DesertC4 SnowA1 SnowA2 SnowA2a SnowA3 SnowA4 SnowB1 SnowB2 SnowB2a SnowB5 SnowB3 SnowB4 SnowC1 SnowC2 SnowC3 SnowC4 SnowC4a SnowC5 GalaxyA1 GalaxyA2 GalaxyA2b GalaxyA3 GalaxyA4 GalaxyB1 GalaxyB2 GalaxyB3 GalaxyB4 GalaxyB5 GalaxyC1 GalaxyC1b GalaxyC2 GalaxyC3 GalaxyC4 LavaA1 LavaA1b LavaA2 LavaA3 LavaA4 LavaA5 LavaA5b LavaB1 LavaB2 LavaB3 LavaB3b LavaB4 LavaB5 LavaB6 LavaC1 LavaC2 SpiA1 SpiA2 SpiA2b SpiA3 SpiA4 SpiA5 SpiB1 SpiB2 SpiB2b SpiB3 SpiB4 SpiC1 SpiC2 SpiD1 SpiD2 SpiD3 BabaYagaETC Hgg Quest17 Quest29 EfauntDrop1 EfauntDrop2 Chiz0 Chiz1 TrollPart KrukPart KrukPart2 EmpPart EquipmentHats11 EquipmentHats12 EquipmentHats13 EquipmentHats14 EquipmentHats1 EquipmentHats15 EquipmentHats17 EquipmentHats20 EquipmentHats3 EquipmentHats16 EquipmentHats21 EquipmentHats18 EquipmentHats22 EquipmentHats28 EquipmentHats19 TestObj13 EquipmentHats41 EquipmentHats26 EquipmentHats52 EquipmentHats53 EquipmentHats54 EquipmentHats61 EquipmentHats58 EquipmentHats59 EquipmentHats60 EquipmentHats68 EquipmentHats70 EquipmentHats71 EquipmentHats74 EquipmentHats77 EquipmentHats83 EquipmentHats105 EquipmentHats106 EquipmentHats119 EquipmentHats5 EquipmentHats6 EquipmentHats7 EquipmentHats8 EquipmentHats9 EquipmentHats10 EquipmentHats4Choppin EquipmentHats25 EquipmentHats107 EquipmentHats29 EquipmentHats39 EquipmentHats27 EquipmentHats30 EquipmentHats44 EquipmentHats2 EquipmentHats67 EquipmentHats64 EquipmentHats66 EquipmentHats79 EquipmentHats73 EquipmentHats51 EquipmentHatsBeg1 EquipmentHats56 EquipmentHats63 EquipmentHats85 EquipmentHats86 EquipmentHats87 EquipmentHats88 EquipmentHats42 EquipmentHats69 EquipmentHats108 EquipmentHats121 EquipmentHats55 EquipmentHats75 EquipmentHats76 EquipmentHats65 EquipmentHats80 EquipmentHats81 EquipmentHats82 EquipmentHats78 EquipmentHats35 EquipmentHats38 EquipmentHats47 EquipmentHats48 EquipmentHats46 EquipmentHats116 EquipmentHats33 EquipmentHats49 EquipmentHats50 EquipmentHats110 EquipmentHats113 EquipmentHats117 EquipmentHats24 EquipmentHats114 EquipmentHats115 EquipmentHats120 EquipmentHats57 EquipmentHats45 EquipmentHats62 EquipmentHats32 EquipmentHats37 EquipmentHats89 EquipmentHats34 EquipmentHats109 EquipmentHats84 EquipmentHats31 EquipmentHats111 EquipmentHats112 EquipmentHats118 EquipmentHats90 EquipmentHats91 EquipmentHats92 EquipmentHats93 EquipmentHats94 EquipmentHats95 EquipmentHats96 EquipmentHats97 EquipmentHats98 EquipmentHats99 EquipmentHats100 EquipmentHats101 EquipmentHats102 EquipmentHats103 EquipmentHats104 EquipmentPunching1 EquipmentPunching2 EquipmentPunching3 EquipmentPunching4 EquipmentPunching5 EquipmentPunching6 EquipmentPunching7 EquipmentPunching8 EquipmentPunching9 EquipmentPunching10 EquipmentPunching11 TestObj1 TestObj7 TestObj3 EquipmentSword1 EquipmentSword2 EquipmentSword3 EquipmentSword4 EquipmentSword5 EquipmentSword6 EquipmentSword7 EquipmentSword8 EquipmentSword9 EquipmentBows1 EquipmentBows3 EquipmentBows4 EquipmentBows5 EquipmentBows6 EquipmentBows7 EquipmentBows8 EquipmentBows9 EquipmentBows10 EquipmentBows11 EquipmentBows12 EquipmentBows13 EquipmentBows14 EquipmentWands1 EquipmentWands2 EquipmentWands5 EquipmentWands6 EquipmentWands3 EquipmentWands7 EquipmentWands8 EquipmentWands9 EquipmentWands10 EquipmentWands11 EquipmentWands12 EquipmentWands13 EquipmentShirts1 EquipmentShirts17 EquipmentShirts19 EquipmentShirts20 EquipmentShirts24 EquipmentShirts25 EquipmentShirts2 EquipmentShirts16 EquipmentShirts3 EquipmentShirts21 EquipmentShirts10 EquipmentShirts11 EquipmentShirts12 EquipmentShirts13 EquipmentShirts18 EquipmentShirts14 EquipmentShirts5 EquipmentShirts23 EquipmentShirts22 EquipmentShirts15 EquipmentShirts26 EquipmentShirts27 EquipmentShirts31 EquipmentShirts28 EquipmentShirts29 EquipmentShirts30 EquipmentShirts6 EquipmentShirts32 EquipmentShirts33 EquipmentShirts34 EquipmentShirts35 EquipmentShirts36 EquipmentShirts37 EquipmentShirts38 EquipmentShirts39 EquipmentPants1 EquipmentPants2 EquipmentPants3 EquipmentPants4 EquipmentPants17 EquipmentPants5 EquipmentPants6 EquipmentPants20 EquipmentPants21 EquipmentPants10 EquipmentPants15 EquipmentPants16 EquipmentPants18 EquipmentPants19 EquipmentPants22 EquipmentPants23 EquipmentPants9 EquipmentPants24 EquipmentPants25 EquipmentPants8 EquipmentPants26 EquipmentPants27 EquipmentPants29 EquipmentPants30 EquipmentPants31 EquipmentShoes1 EquipmentShoes9 EquipmentShoes15 EquipmentShoes3 EquipmentShoes20 EquipmentShoes4 EquipmentShoes5 EquipmentShoes21 EquipmentShoes22 EquipmentShoes7 EquipmentShoes16 EquipmentShoes17 EquipmentShoes18 EquipmentShoes19 EquipmentShoes2 EquipmentShoes23 EquipmentShoes26 EquipmentShoes27 EquipmentShoes28 EquipmentShoes29 EquipmentShoes30 EquipmentShoes31 EquipmentShoes32 EquipmentShoes33 EquipmentShoes39 EquipmentShoes24 EquipmentShoes25 EquipmentShoes34 EquipmentShoes35 EquipmentShoes36 EquipmentShoes37 EquipmentShoes38 EquipmentShoes40 EquipmentPendant9 EquipmentPendant32 EquipmentPendant10 EquipmentPendant11 EquipmentPendant12 EquipmentPendant14 EquipmentPendant16 EquipmentPendant17 EquipmentPendant18 EquipmentPendant19 EquipmentPendant20 EquipmentPendant21 EquipmentPendant22 EquipmentPendant23 EquipmentPendant24 EquipmentPendant25 EquipmentPendant26 EquipmentPendant27 EquipmentPendant28 EquipmentPendant31 EquipmentPendant29 EquipmentPendant30 EquipmentPendant33 EquipmentRings2 EquipmentRings3 EquipmentRings6 EquipmentRings7 EquipmentRings11 EquipmentRings12 EquipmentRings13 EquipmentRings14 EquipmentRings15 EquipmentRings16 EquipmentRings21 EquipmentRings20 EquipmentRings19 EquipmentRingsFishing1 EquipmentRingsFishing2 EquipmentRingsFishing3 EquipmentRings22 EquipmentRings18 EquipmentRings36 EquipmentRings23 EquipmentRings24 EquipmentRings25 EquipmentRings26 EquipmentRings27 EquipmentRings28 EquipmentRings29 EquipmentRings35 EquipmentRings30 EquipmentRings33 EquipmentRings31 EquipmentRings32 EquipmentRings34 EquipmentRings37 EquipmentRingsChat10 EquipmentRingsChat1 EquipmentRingsChat2 EquipmentRingsChat3 EquipmentRingsChat4 EquipmentRingsChat5 EquipmentRingsChat11 EquipmentRingsChat9 EquipmentRingsChat6 EquipmentCape3 EquipmentCape4 EquipmentCape5 EquipmentCape6 EquipmentCape13 EquipmentCape17 EquipmentCape0 EquipmentCape2 EquipmentCape7 EquipmentCape8 EquipmentCape9 EquipmentCape10 EquipmentCape11 EquipmentCape12 EquipmentCape14 EquipmentCape15 EquipmentCape16 EquipmentCape18 EquipmentKeychain0 EquipmentKeychain1 EquipmentKeychain2 EquipmentKeychain3 EquipmentKeychain4 EquipmentKeychain5 EquipmentKeychain6 EquipmentKeychain7 EquipmentKeychain8 EquipmentKeychain9 EquipmentKeychain10 EquipmentKeychain11 EquipmentKeychain12 EquipmentKeychain13 EquipmentKeychain14 EquipmentKeychain15 EquipmentKeychain16 EquipmentKeychain17 EquipmentKeychain18 EquipmentKeychain19 EquipmentKeychain20 EquipmentKeychain21 EquipmentKeychain22 EquipmentKeychain23 EquipmentKeychain24 EquipmentKeychain25 EquipmentKeychain26 EquipmentKeychain27 EquipmentKeychain28 EquipmentKeychain29 Trophy1 Trophy2 Trophy3 Trophy5 Trophy6 Trophy7 Trophy8 Trophy9 Trophy10 Trophy11 Trophy12 Trophy13 Trophy14 Trophy15 Trophy16 Trophy17 Trophy18 Trophy19 Trophy20 Trophy21 Trophy22 Trophy23 EquipmentNametag1 EquipmentNametag3 EquipmentNametag4 EquipmentNametag5 EquipmentNametag6b EquipmentNametag7 EquipmentNametag8 EquipmentNametag9 EquipmentNametag10 EquipmentNametag11 EquipmentNametag12 EquipmentNametag13 EquipmentNametag14 EquipmentNametag15 EquipmentNametag16 EquipmentNametag17 EquipmentNametag18 EquipmentNametag19 EquipmentNametag20 EquipmentNametag21 EquipmentGown1 EquipmentGown2 EquipmentGown3 EquipmentGown4 EquipmentTools1 EquipmentTools2 EquipmentTools3 EquipmentTools5 EquipmentTools6 EquipmentTools7 EquipmentTools11 EquipmentTools8 EquipmentTools12 EquipmentTools9 EquipmentTools14 EquipmentTools15 EquipmentTools10 EquipmentTools13 EquipmentToolsHatchet0 EquipmentToolsHatchet3 EquipmentToolsHatchet1 EquipmentToolsHatchet2b EquipmentToolsHatchet2 EquipmentToolsHatchet4 EquipmentToolsHatchet5 EquipmentToolsHatchet7 EquipmentToolsHatchet6 EquipmentToolsHatchet8 EquipmentToolsHatchet9 EquipmentToolsHatchet12 EquipmentToolsHatchet10 EquipmentToolsHatchet11 FishingRod2 FishingRod3 FishingRod4 FishingRod5 FishingRod6 FishingRod7 FishingRod8 FishingRod9 FishingRod10 FishingRod11 FishingRod12 CatchingNet2 CatchingNet3 CatchingNet4 CatchingNet5 CatchingNet6 CatchingNet7 CatchingNet8 CatchingNet9 CatchingNet10 CatchingNet11 CatchingNet12 TrapBoxSet1 TrapBoxSet2 TrapBoxSet3 TrapBoxSet4 TrapBoxSet5 TrapBoxSet6 TrapBoxSet7 TrapBoxSet8 TrapBoxSet9 TrapBoxSet10 WorshipSkull1 WorshipSkull2 WorshipSkull3 WorshipSkull4 WorshipSkull5 WorshipSkull6 WorshipSkull7 WorshipSkull8 WorshipSkull9 WorshipSkull10 WorshipSkull11 DNAgun0 DNAgun1 DNAgun2 DNAgun3 FoodHealth1 FoodHealth3 FoodHealth2 Peanut FoodHealth4 FoodHealth6 FoodHealth7 FoodHealth10 FoodHealth9 FoodHealth11 FoodHealth13 FoodHealth12 FoodHealth14 FoodHealth15 FoodHealth16 FoodHealth17 FoodHealth5 FoodEvent8 Meatloaf FoodPotOr1 FoodPotOr2 FoodPotOr3 FoodPotOr4 FoodPotRe1 FoodPotRe2 FoodPotRe3 FoodPotRe4 FoodPotGr1 FoodPotGr2 FoodPotGr3 FoodPotGr4 FoodEvent7 FoodPotMana1 FoodPotMana2 FoodPotMana3 FoodPotMana4 FoodPotYe1 FoodPotYe2 FoodPotYe3 FoodPotYe4 FoodPotYe5 FoodEvent6 Pearl3 FoodMining1 FoodEvent1 Pearl2 FoodChoppin1 FoodEvent2 FoodFish1 FoodEvent3 Pearl1 FoodCatch1 FoodEvent4 FoodTrapping1 FoodWorship1 Bullet BulletB Bullet3 MidnightCookie FoodEvent5 PeanutG FoodG1 FoodG2 FoodG3 FoodG4 FoodG5 FoodG6 FoodG7 FoodG8 FoodG9 FoodG10 FoodG11 FoodG12 FoodG13 ButterBar rtt0 ResetFrag ResetCompleted ResetCompletedS ClassSwap ClassSwapB ClassSwapC ResetBox Ht StonePremRestore StonePremStatswap Key1 Key2 Key3 Key4 Key5 TixCol SilverPen PremiumGem TalentPoint1 TalentPoint2 TalentPoint3 TalentPoint4 TalentPoint5 TalentPoint6 Gfoodcoupon ItemsCoupon1 ItemsCoupon2 ExpBalloon1 ExpBalloon2 ExpBalloon3 Pearl4 Pearl6 Pearl5 Quest30 Quest35 Quest36 Quest38 Quest39 Quest40 Quest42 Quest43 Quest44 Quest49 Quest50 Quest70 Quest71 Quest72 Quest73 Quest90 Quest94 Quest75 Quest85 Quest88 Quest89 Quest91 Quest92 Quest76 Quest77 Quest79 Quest80 GemP36 GemP30 Quest81 Quest82 Quest95 Quest96 Quest97 Quest101 Timecandy1 Timecandy2 Timecandy3 Timecandy4 Timecandy5 Timecandy6 Timecandy7 Timecandy8 Timecandy9 StoneWe StoneWeb StoneW1 StoneW2 StoneW3 StoneW3b StoneW6 StoneW4 StoneW5 StoneW7 StoneW8 StoneAe StoneAeB StoneA1 StoneA1b StoneA2 StoneA2b StoneA3 StoneA3b StoneA4 StoneA5 StoneA6 StoneA7 StoneTe StoneT1 StoneT1e StoneT1eb StoneT2 StoneT3 StoneT4 StoneT5 StoneT6 StoneT7 StoneHelm1 StoneHelm6 StoneHelm1b StoneHelm7 StoneZ1 StoneZ2 StoneZ3 StoneZ4 StonePremSTR StonePremAGI StonePremWIS StonePremLUK JobApplication SmithingHammerChisel SmithingHammerChisel2 SmithingHammerChisel3 BobJoePickle BallJoePickle BoneJoePickle Quest1 Crystal1 Crystal2 Crystal3 Crystal4 Crystal5 PeanutS Quest3 Quest4 Mayo Trash Trash2 Trash3 Quest5 Quest6 Quest7 Quest10 Quest11 Quest12 Quest13 Quest14 Quest15 Quest16 Quest18 Quest19 Quest20 Quest21 Quest22 Quest23 Quest24 Quest25 Quest26 Quest27 GoldricP1 GoldricP2 GoldricP3 Cutter Quest32 Quest33 Quest34 Quest37 Quest41 Quest45 Quest46 Quest47 Quest48 Quest28 Island1 Island0 Quest86 Quest87 Quest93 Quest98 Quest100 Quest51 Quest52 PalmTreeD Quest53 Quest54 Quest55 Quest56 Quest57 Quest58 Quest59 Quest60 Quest61 Quest62 Quest63 Quest64 Quest65 Quest66 Quest67 Whetstone Quest68 Quest69 Quest74 Quest78 Quest83 Quest84 Bone0 Bone1 Bone2 Bone3 Dust0 Dust1 Dust2 Dust3 Dust4 Tach0 Tach1 Tach2 Tach3 Tach4 Tach5 Quest99 BadgeG1 BadgeG2 BadgeG3 BadgeD1 BadgeD2 BadgeD3 NPCtoken1 NPCtoken2 NPCtoken3 NPCtoken5 NPCtoken6 NPCtoken4 NPCtoken9 NPCtoken10 NPCtoken11 NPCtoken13 NPCtoken7 Quest9 NPCtoken15 NPCtoken12 NPCtoken14 NPCtoken16 NPCtoken17 NPCtoken18 NPCtoken19 NPCtoken20 NPCtoken21 NPCtoken27 NPCtoken22 NPCtoken24 NPCtoken25 NPCtoken26 NPCtoken23 NPCtoken28 NPCtoken29 NPCtoken30 NPCtoken31 NPCtoken32 NPCtoken33 NPCtoken34 NPCtoken35 NPCtoken36 NPCtoken37 NPCtoken38 NPCtoken39 NPCtoken40 NPCtoken41 BadgeI1 BadgeI2 BadgeI3 EquipmentStatues1 EquipmentStatues2 EquipmentStatues3 EquipmentStatues4 EquipmentStatues5 EquipmentStatues6 EquipmentStatues7 EquipmentStatues8 EquipmentStatues9 EquipmentStatues10 EquipmentStatues11 EquipmentStatues12 EquipmentStatues13 EquipmentStatues14 EquipmentStatues15 EquipmentStatues16 EquipmentStatues17 EquipmentStatues18 EquipmentStatues19 EquipmentStatues20 EquipmentStatues21 EquipmentStatues22 EquipmentStatues23 EquipmentStatues24 EquipmentStatues25 EquipmentStatues26 EquipmentStatues27 EquipmentStatues28 EquipmentStatues29 EquipmentStatues30 EquipmentSmithingTabs2 EquipmentSmithingTabs3 EquipmentSmithingTabs4 EquipmentSmithingTabs5 EquipmentSmithingTabs6 SmithingRecipes1 SmithingRecipes2 SmithingRecipes3 SmithingRecipes4 SmithingRecipes5 SmithingRecipes6 TalentBook1 TalentBook2 TalentBook3 TalentBook4 TalentBook5 MaxCapBagT2 MaxCapBag1 MaxCapBag2 MaxCapBag3 MaxCapBag4 MaxCapBag5 MaxCapBagMi6 MaxCapBagMi7 MaxCapBagMi8 MaxCapBagMi9 MaxCapBagMi10 MaxCapBagMi11 MaxCapBagT1 MaxCapBag7 MaxCapBag9 MaxCapBagT3 MaxCapBagT4 MaxCapBagT5 MaxCapBagT6 MaxCapBagT7 MaxCapBagT8 MaxCapBagT9 MaxCapBagT10 MaxCapBagT11 MaxCapBag6 MaxCapBag8 MaxCapBag10 MaxCapBagF3 MaxCapBagF4 MaxCapBagF5 MaxCapBagF6 MaxCapBagF7 MaxCapBagF8 MaxCapBagF9 MaxCapBagF10 MaxCapBagF11 MaxCapBagM1 MaxCapBagM2 MaxCapBagM3 MaxCapBagM4 MaxCapBagM5 MaxCapBagM6 MaxCapBagM7 MaxCapBagM8 MaxCapBagM9 MaxCapBagM10 MaxCapBagM11 MaxCapBagM12 MaxCapBagFi1 MaxCapBagFi2 MaxCapBagFi3 MaxCapBagFi4 MaxCapBagFi5 MaxCapBagFi6 MaxCapBagFi7 MaxCapBagFi8 MaxCapBagFi9 MaxCapBagFi10 MaxCapBagFi11 MaxCapBagB1 MaxCapBagB2 MaxCapBagB3 MaxCapBagB4 MaxCapBagB5 MaxCapBagB6 MaxCapBagB7 MaxCapBagB8 MaxCapBagB9 MaxCapBagB10 MaxCapBagB11 MaxCapBagTr1 MaxCapBagTr3 MaxCapBagTr4 MaxCapBagTr5 MaxCapBagTr6 MaxCapBagTr7 MaxCapBagTr8 MaxCapBagTr9 MaxCapBagTr10 MaxCapBagS1 MaxCapBagS3 MaxCapBagS4 MaxCapBagS5 MaxCapBagS6 MaxCapBagS7 MaxCapBagS8 MaxCapBagS9 MaxCapBagS10 ObolBronze0 ObolSilver0 ObolGold0 ObolPlatinum0 ObolPink0 ObolBronze1 ObolSilver1 ObolGold1 ObolPlatinum1 ObolPink1 ObolBronze2 ObolSilver2 ObolGold2 ObolPlatinum2 ObolPink2 ObolBronze3 ObolSilver3 ObolGold3 ObolPlatinum3 ObolPink3 ObolBronzeDamage ObolSilverDamage ObolGoldDamage ObolPlatinumDamage ObolPinkDamage ObolSilverMoney ObolGoldMoney ObolBronzeMining ObolSilverMining ObolGoldMining ObolPlatinumMining ObolPinkMining ObolBronzeChoppin ObolSilverChoppin ObolGoldChoppin ObolPlatinumChoppin ObolPinkChoppin ObolBronzeFishing ObolSilverFishing ObolGoldFishing ObolPlatinumFishing ObolPinkFishing ObolBronzeCatching ObolSilverCatching ObolGoldCatching ObolPlatinumCatching ObolPinkCatching ObolSilverLuck ObolGoldLuck ObolPlatinumLuck ObolPinkLuck ObolBronzePop ObolSilverPop ObolGoldPop ObolPlatinumPop ObolPinkPop ObolBronzeKill ObolSilverKill ObolGoldKill ObolPlatinumKill ObolPinkKill ObolBronzeEXP ObolSilverEXP ObolGoldEXP ObolPlatinumEXP ObolPinkEXP ObolBronzeCard ObolSilverCard ObolGoldCard ObolPlatinumCard ObolPinkCard ObolBronzeDef ObolSilverDef ObolGoldDef ObolPlatinumDef ObolPinkDef ObolBronzeTrapping ObolSilverTrapping ObolGoldTrapping ObolPlatinumTrapping ObolPinkTrapping ObolBronzeCons ObolSilverCons ObolGoldCons ObolPlatinumCons ObolPinkCons ObolBronzeWorship ObolSilverWorship ObolGoldWorship ObolPlatinumWorship ObolPinkWorship ObolFrog ObolAmarokA ObolEfauntA ObolKnight ObolSlush ObolChizoarA ObolTroll ObolLava ObolKruk ObolEmp ObolHyper0 ObolHyper1 ObolHyper2 ObolHyper3 ObolHyperB0 ObolHyperB1 ObolHyperB2 ObolHyperB3 StampA1 StampA2 StampA3 StampA4 StampA5 StampA6 StampA7 StampA8 StampA9 StampA10 StampA11 StampA12 StampA13 StampA14 StampA15 StampA16 StampA17 StampA18 StampA19 StampA20 StampA21 StampA22 StampA23 StampA24 StampA25 StampA26 StampA27 StampA28 StampA29 StampA30 StampA31 StampA32 StampA33 StampA34 StampA35 StampA36 StampA37 StampA38 StampA39 StampA40 StampA41 StampA42 StampB1 StampB2 StampB3 StampB4 StampB5 StampB6 StampB7 StampB8 StampB9 StampB10 StampB11 StampB12 StampB13 StampB14 StampB15 StampB16 StampB17 StampB18 StampB19 StampB20 StampB21 StampB22 StampB23 StampB24 StampB25 StampB26 StampB27 StampB28 StampB29 StampB30 StampB31 StampB32 StampB33 StampB34 StampB35 StampB36 StampB37 StampB38 StampB39 StampB40 StampB41 StampB42 StampB43 StampB44 StampB45 StampB46 StampB47 StampB48 StampB49 StampB50 StampB51 StampB52 StampB53 StampB54 StampC1 StampC2 StampC3 StampC4 StampC5 StampC6 StampC7 StampC8 StampC9 StampC10 StampC11 StampC12 StampC13 StampC14 StampC15 StampC16 StampC17 StampC18 StampC19 StampC20 StampC21 StampC22 StampC23 InvBag1 InvBag2 InvBag3 InvBag4 InvBag5 InvBag6 InvBag7 InvBag8 InvBag100 InvBag101 InvBag102 InvBag103 InvBag104 InvBag105 InvBag106 InvBag107 InvBag108 InvBag113 InvBag114 InvBag109 InvBag110 InvBag111 InvBag112 InvStorage1 InvStorage2 InvStorage3 InvStorage4 InvStorage5 InvStorage6 InvStorage7 InvStorage8 InvStorage9 InvStorage10 InvStorage11 InvStorage12 InvStorage13 InvStorage14 InvStorage15 InvStorage16 InvStorage17 InvStorage18 InvStorage19 InvStorage20 InvStorage21 InvStorage22 InvStorage23 InvStorage24 InvStorage25 InvStorage26 InvStorage27 InvStorage28 InvStorageF InvStorageS InvStorageC InvStorageD InvStorageN InvStorageH InvStorageL InvStorageZ Weight1 Weight2 Weight3 Weight4 Weight5 Weight6 Weight7 Weight8 Weight9 Weight10 Weight11 Weight12 Weight13 Weight14 Line1 Line2 Line3 Line4 Line5 Line6 Line7 Line8 Line9 Line10 Line11 Line12 Line13 Line14 Ladle PetEgg Genetic0 Genetic1 Genetic2 Genetic3 CardPack1 CardPack2 CardPack3 CardPack4 CardPack5 CardPack6 CardPack7 EquipmentBowsTempest0 EquipmentBowsTempest1 EquipmentBowsTempest2 EquipmentBowsTempest3 EquipmentBowsTempest4 EquipmentRingsTempest0 EquipmentRingsTempest1 EquipmentRingsTempest2 EquipmentRingsTempest3 EquipmentRingsTempest4 EquipmentRingsTempest5 EquipmentRingsTempest6 EquipmentRingsTempest7 EquipmentRingsTempest8 StoneTempestB0 StoneTempestB1 StoneTempestB2 StoneTempestR0 StoneTempestR1 StoneTempestR2 WWcoin EquipmentWandsArc0 EquipmentRingsArc0 DungCredits2 Cash XP XPskill DungEnhancer0 DungEnhancer1 DungEnhancer2 DungRNG0 DungRNG1 DungRNG2 DungRNG3 DungRNG4 DungeonA1 DungeonA2 DungeonA3 DungeonA4 DungeonA5 DungeonA6 DungeonA7 DungeonA8 KeyFrag DungCredits1 LootDice Tree7D PlatD Fish1D Fish3D Cashb Dung3Ice FoodHealth1d FoodHealth2d FoodHealth3d DungWeaponPunchA1 DungWeaponPunchA2 DungWeaponPunchA3 DungWeaponPunchA4 DungWeaponPunchA5 DungWeaponPunchB1 DungWeaponPunchB2 DungWeaponPunchB3 DungWeaponPunchB4 DungWeaponPunchB5 DungWeaponPunchC1 DungWeaponPunchC2 DungWeaponPunchC3 DungWeaponPunchC4 DungWeaponPunchC5 DungWeaponPunchD1 DungWeaponPunchD2 DungWeaponPunchD3 DungWeaponPunchD4 DungWeaponPunchD5 DungWeaponPunchE1 DungWeaponPunchE2 DungWeaponPunchE3 DungWeaponPunchE4 DungWeaponPunchE5 DungWeaponPunchF1 DungWeaponPunchF2 DungWeaponPunchF3 DungWeaponPunchF4 DungWeaponPunchF5 DungWeaponSwordA1 DungWeaponSwordA2 DungWeaponSwordA3 DungWeaponSwordA4 DungWeaponSwordA5 DungWeaponSwordB1 DungWeaponSwordB2 DungWeaponSwordB3 DungWeaponSwordB4 DungWeaponSwordB5 DungWeaponSwordC1 DungWeaponSwordC2 DungWeaponSwordC3 DungWeaponSwordC4 DungWeaponSwordC5 DungWeaponSwordD1 DungWeaponSwordD2 DungWeaponSwordD3 DungWeaponSwordD4 DungWeaponSwordD5 DungWeaponSwordE1 DungWeaponSwordE2 DungWeaponSwordE3 DungWeaponSwordE4 DungWeaponSwordE5 DungWeaponSwordF1 DungWeaponSwordF2 DungWeaponSwordF3 DungWeaponSwordF4 DungWeaponSwordF5 DungWeaponBowA1 DungWeaponBowA2 DungWeaponBowA3 DungWeaponBowA4 DungWeaponBowA5 DungWeaponBowB1 DungWeaponBowB2 DungWeaponBowB3 DungWeaponBowB4 DungWeaponBowB5 DungWeaponBowC1 DungWeaponBowC2 DungWeaponBowC3 DungWeaponBowC4 DungWeaponBowC5 DungWeaponBowD1 DungWeaponBowD2 DungWeaponBowD3 DungWeaponBowD4 DungWeaponBowD5 DungWeaponBowE1 DungWeaponBowE2 DungWeaponBowE3 DungWeaponBowE4 DungWeaponBowE5 DungWeaponBowF1 DungWeaponBowF2 DungWeaponBowF3 DungWeaponBowF4 DungWeaponBowF5 DungWeaponWandA1 DungWeaponWandA2 DungWeaponWandA3 DungWeaponWandA4 DungWeaponWandA5 DungWeaponWandB1 DungWeaponWandB2 DungWeaponWandB3 DungWeaponWandB4 DungWeaponWandB5 DungWeaponWandC1 DungWeaponWandC2 DungWeaponWandC3 DungWeaponWandC4 DungWeaponWandC5 DungWeaponWandD1 DungWeaponWandD2 DungWeaponWandD3 DungWeaponWandD4 DungWeaponWandD5 DungWeaponWandE1 DungWeaponWandE2 DungWeaponWandE3 DungWeaponWandE4 DungWeaponWandE5 DungWeaponWandF1 DungWeaponWandF2 DungWeaponWandF3 DungWeaponWandF4 DungWeaponWandF5 DungEquipmentHats0 DungEquipmentHats1 DungEquipmentHats2 DungEquipmentHats3 DungEquipmentHats4 DungEquipmentShirt0 DungEquipmentShirt1 DungEquipmentShirt2 DungEquipmentShirt3 DungEquipmentShirt4 DungEquipmentPants0 DungEquipmentPants1 DungEquipmentPants2 DungEquipmentPants3 DungEquipmentPants4 DungEquipmentShoes0 DungEquipmentShoes1 DungEquipmentShoes2 DungEquipmentShoes3 DungEquipmentShoes4 DungEquipmentPendant0 DungEquipmentPendant1 DungEquipmentPendant2 DungEquipmentPendant3 DungEquipmentPendant4 DungEquipmentRings0 DungEquipmentRings1 DungEquipmentRings2 DungEquipmentRings3 DungEquipmentRings4".split(" ")

dungeon_drops_list = [
    "Quest51", "Quest52", "PalmTreeD", "Quest53", "Quest54", "Quest55",
    "DungCredits2", "Cash", "XP", "XPskill", "DungEnhancer0", "DungEnhancer1", "DungEnhancer2",
    "DungRNG0", "DungRNG1", "DungRNG2", "DungRNG3", "DungRNG4",
    "DungeonA1", "DungeonA2", "DungeonA3", "DungeonA4", "DungeonA5", "DungeonA6", "DungeonA7", "DungeonA8",
    "KeyFrag", "DungCredits1", "LootDice", "Tree7D", "PlatD", "Fish1D", "Fish3D", "Cashb", "Dung3Ice",
    "FoodHealth1d", "FoodHealth2d", "FoodHealth3d"
]
max_dungeon_weapons_available = 23  #This is the value saved in the JSON, 0-23 = 24 total. Last verified in 2.12
dungeon_weapons_list = [
    "DungWeaponPunchA1", "DungWeaponPunchA2", "DungWeaponPunchA3", "DungWeaponPunchA4", "DungWeaponPunchA5", "DungWeaponPunchB1", "DungWeaponPunchB2", "DungWeaponPunchB3", "DungWeaponPunchB4", "DungWeaponPunchB5", "DungWeaponPunchC1", "DungWeaponPunchC2", "DungWeaponPunchC3", "DungWeaponPunchC4", "DungWeaponPunchC5", "DungWeaponPunchD1", "DungWeaponPunchD2", "DungWeaponPunchD3", "DungWeaponPunchD4", "DungWeaponPunchD5", "DungWeaponPunchE1", "DungWeaponPunchE2", "DungWeaponPunchE3", "DungWeaponPunchE4",  #"DungWeaponPunchE5", "DungWeaponPunchF1", "DungWeaponPunchF2", "DungWeaponPunchF3", "DungWeaponPunchF4", "DungWeaponPunchF5",
    "DungWeaponSwordA1", "DungWeaponSwordA2", "DungWeaponSwordA3", "DungWeaponSwordA4", "DungWeaponSwordA5", "DungWeaponSwordB1", "DungWeaponSwordB2", "DungWeaponSwordB3", "DungWeaponSwordB4", "DungWeaponSwordB5", "DungWeaponSwordC1", "DungWeaponSwordC2", "DungWeaponSwordC3", "DungWeaponSwordC4", "DungWeaponSwordC5", "DungWeaponSwordD1", "DungWeaponSwordD2", "DungWeaponSwordD3", "DungWeaponSwordD4", "DungWeaponSwordD5", "DungWeaponSwordE1", "DungWeaponSwordE2", "DungWeaponSwordE3", "DungWeaponSwordE4",  #"DungWeaponSwordE5", "DungWeaponSwordF1", "DungWeaponSwordF2", "DungWeaponSwordF3", "DungWeaponSwordF4", "DungWeaponSwordF5",
    "DungWeaponBowA1", "DungWeaponBowA2", "DungWeaponBowA3", "DungWeaponBowA4", "DungWeaponBowA5", "DungWeaponBowB1", "DungWeaponBowB2", "DungWeaponBowB3", "DungWeaponBowB4", "DungWeaponBowB5", "DungWeaponBowC1", "DungWeaponBowC2", "DungWeaponBowC3", "DungWeaponBowC4", "DungWeaponBowC5", "DungWeaponBowD1", "DungWeaponBowD2", "DungWeaponBowD3", "DungWeaponBowD4", "DungWeaponBowD5", "DungWeaponBowE1", "DungWeaponBowE2", "DungWeaponBowE3", "DungWeaponBowE4",  #"DungWeaponBowE5", "DungWeaponBowF1", "DungWeaponBowF2", "DungWeaponBowF3", "DungWeaponBowF4", "DungWeaponBowF5",
    "DungWeaponWandA1", "DungWeaponWandA2", "DungWeaponWandA3", "DungWeaponWandA4", "DungWeaponWandA5", "DungWeaponWandB1", "DungWeaponWandB2", "DungWeaponWandB3", "DungWeaponWandB4", "DungWeaponWandB5", "DungWeaponWandC1", "DungWeaponWandC2", "DungWeaponWandC3", "DungWeaponWandC4", "DungWeaponWandC5", "DungWeaponWandD1", "DungWeaponWandD2", "DungWeaponWandD3", "DungWeaponWandD4", "DungWeaponWandD5", "DungWeaponWandE1", "DungWeaponWandE2", "DungWeaponWandE3", "DungWeaponWandE4",  #"DungWeaponWandE5", "DungWeaponWandF1", "DungWeaponWandF2", "DungWeaponWandF3", "DungWeaponWandF4", #"DungWeaponWandF5",
]
max_dungeon_armors_available = 3  #This is the value saved in the JSON, 0-3 = 4 total. Last verified in 2.12
dungeon_armors_list = [
    "DungEquipmentHats0", "DungEquipmentHats1", "DungEquipmentHats2", "DungEquipmentHats3",  #"DungEquipmentHats4",
    "DungEquipmentShirt0", "DungEquipmentShirt1", "DungEquipmentShirt2", "DungEquipmentShirt3",  #"DungEquipmentShirt4",
    "DungEquipmentPants0", "DungEquipmentPants1", "DungEquipmentPants2", "DungEquipmentPants3",  #"DungEquipmentPants4",
    "DungEquipmentShoes0", "DungEquipmentShoes1", "DungEquipmentShoes2", "DungEquipmentShoes3",  #"DungEquipmentShoes4",
]  #This list was pulled from the items.yaml file
max_dungeon_jewelry_available = 3   #This is the value saved in the JSON, 0-3 = 4 total. Last verified in 2.12
dungeon_jewelry_list = [
    "DungEquipmentPendant0", "DungEquipmentPendant1", "DungEquipmentPendant2", "DungEquipmentPendant3",  #"DungEquipmentPendant4",
    "DungEquipmentRings0", "DungEquipmentRings1", "DungEquipmentRings2", "DungEquipmentRings3",  #"DungEquipmentRings4",
]  #This list was pulled from the items.yaml file
reclaimable_quest_items = {
    "CraftMat2": {
        "ItemName": "Crimson String",
        "QuestGiver": "Scripticus",
        "QuestName": "Hardcore Gamer Status, Here I Come!",
        "QuestNameCoded": "Scripticus2"
    },
    "EquipmentTools1": {
        "ItemName": "Junk Pickaxe",
        "QuestGiver": "Glumlee",
        "QuestName": "Literally Burning Your Money",
        "QuestNameCoded": "Glumlee3"
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
slab_quest_rewards_all_chars = {
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
    "EquipmentTools1": {
        "ItemName": "Junk Pickaxe",
        "QuestGiver": "Glumlee",
        "QuestName": "Literally Burning Your Money",
        "QuestNameCoded": "Glumlee3"
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
slab_quest_rewards_once = {
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
ShopNames = ["FoodHealth1 FoodHealth3 FoodHealth2 CraftMat3 FoodPotMana1 FoodPotOr1 FoodPotRe1 FoodPotGr1 OilBarrel1 StoneW1 StoneA1 StoneT1 EquipmentRings7 EquipmentStatues1 SmithingHammerChisel StampA5 StampA6 StampA3 InvBag104 InvStorage2 InvStorage6 InvStorage7 Quest86 rtt0 ResetFrag".split(" "), "FoodHealth3 FoodHealth2 FoodHealth5 FoodPotOr2 FoodPotYe1 StoneA2 StampA12 EquipmentPendant12 Quest37 InvBag105 InvStorage8 InvStorage12 rtt0 ResetFrag".split(" "), "FoodHealth6 FoodHealth7 FoodHealth4 Quest19 BobJoePickle StoneW2 StoneA2 StoneT2 FoodPotOr2 FoodPotGr2 FoodPotRe2 InvBag106 InvStorage9 InvStorage10 InvStorage13 InvStorage15 SmithingHammerChisel2 StampC11 rtt0 ResetFrag Quest87".split(" "), "Line1 Weight1 Line5 Weight5 Weight10 Line10 Weight11 StoneT1 StoneT2 StampB8 StampA15 NPCtoken27 ResetFrag".split(" "), "FoodHealth10 FoodHealth9 FoodHealth11 TrapBoxSet1 WorshipSkull1 StoneW3 StoneA3 StoneT3 FoodPotOr3 FoodPotGr3 FoodPotRe3 InvBag107 InvStorage16 InvStorage17 InvStorage18 InvStorage19 InvStorage20 InvStorage21 rtt0 ResetFrag Quest57 Quest67 Whetstone".split(" "), "Quest65 Quest66 FoodHealth13 FoodHealth12 DNAgun0 StoneW4 StoneA4 StoneT4 FoodPotOr4 FoodPotGr4 FoodPotRe4 FoodPotYe4 InvBag108 StampB41 StampB38 StampC12 Quest83".split(" "), "FoodHealth14 FoodHealth15 OilBarrel6 StoneW5 StoneA5 StoneT5 StampC22 InvBag113 Quest84".split(" "), "BoneJoePickle Quest80 FoodHealth16 FoodHealth17 OilBarrel7 StoneW8 StoneA7 StoneT7 StampC10 InvBag114 InvStorage26 InvStorage27 InvStorage28".split(" ")]
vendor_items = {
    "W1 Town": ShopNames[0],
    "Tiki Shop": ShopNames[1],
    "W2 Town": ShopNames[2],
    "Faraway Piers": ShopNames[3],
    "W3 Town": ShopNames[4],
    "W4 Town": ShopNames[5],
    "W5 Town": ShopNames[6],
    "W6 Town": ShopNames[7]
}  #vendor_items last pulled from code in 2.35. Search for: ShopNames = function ()
vendors = {
    "W2 Town": "Crystal1",
    "Faraway Piers": "Crystal1",
    "W3 Town": "Crystal2",
    "W4 Town": "Crystal3",
    "W5 Town": "Crystal4",
    "W6 Town": "Crystal5"
}

anvil_items = {
    "Anvil Tab I": "EquipmentPunching1 TestObj1 EquipmentBows1 EquipmentWands1 EquipmentHats1 EquipmentShirts1 EquipmentPants1 EquipmentShoes9 EquipmentTools2 MaxCapBag1 EquipmentToolsHatchet3 MaxCapBag7 EquipmentHats15 EquipmentPunching2 MaxCapBag8 MaxCapBagM2 EquipmentHats17 EquipmentShirts11 EquipmentPants2 EquipmentShoes1 EquipmentHats20 EquipmentHats3 EquipmentHats16 EquipmentHats21 TestObj7 EquipmentBows3 EquipmentWands2 EquipmentRings2 EquipmentTools3 MaxCapBag2 EquipmentToolsHatchet1 MaxCapBag9 EquipmentHats18 EquipmentShirts12 EquipmentPants3 EquipmentSmithingTabs2 EquipmentShirts2 EquipmentPendant10 EquipmentShoes15 EquipmentRings3 EquipmentHats8 FoodMining1 FoodChoppin1 EquipmentShoes7 EquipmentShirts10 EquipmentShirts20 OilBarrel5 EquipmentRings14 EquipmentPants15 EquipmentPants18 Peanut PeanutG InvBag102 EquipmentShirts25 EquipmentShirts24 EquipmentShirts3 BadgeG1 BadgeG2 BadgeG3 EquipmentHats67 NPCtoken1 NPCtoken2 NPCtoken3 EquipmentRings26 EquipmentHats22 EquipmentShirts18 EquipmentPants17 EquipmentShoes20 EquipmentPants22 EquipmentPants23 FillerMaterial EquipmentPendant17 FishingRod2 MaxCapBagFi1 CatchingNet2 MaxCapBagB1 FishingRod3 MaxCapBagFi2 CatchingNet3 MaxCapBagB2 TrapBoxSet2 MaxCapBagTr1 WorshipSkull2 MaxCapBagS1".split(" "),
    "Anvil Tab II": "EquipmentHats28 EquipmentShirts13 EquipmentPants4 EquipmentShoes3 EquipmentPunching3 TestObj3 EquipmentBows5 EquipmentWands5 EquipmentTools5 MaxCapBag3 EquipmentToolsHatchet2 MaxCapBagT3 FishingRod4 MaxCapBagFi3 CatchingNet4 MaxCapBagB3 EquipmentRings11 EquipmentPendant16 MaxCapBagF3 MaxCapBagM4 EquipmentHats19 EquipmentShirts14 EquipmentPants5 EquipmentShoes4 EquipmentPendant26 EquipmentSword1 EquipmentBows6 EquipmentWands6 EquipmentTools6 MaxCapBag4 EquipmentToolsHatchet4 MaxCapBagT4 FishingRod5 MaxCapBagFi4 CatchingNet5 MaxCapBagB4 MaxCapBagF4 MaxCapBagM5 FillerMaterial EquipmentSmithingTabs3 Quest13 Quest35 Bullet BulletB EquipmentHats64 TestObj13 EquipmentHats41 EquipmentHats26 FillerMaterial EquipmentShirts5 EquipmentShirts23 EquipmentShirts22 EquipmentShoes16 EquipmentShoes18 EquipmentShoes19 EquipmentShoes17 FoodFish1 FoodCatch1 Quest36 InvBag103 EquipmentHats52 EquipmentShirts26 EquipmentPants20 EquipmentShoes21 EquipmentRings16 EquipmentRings27 EquipmentPendant27 FillerMaterial TrapBoxSet3 MaxCapBagTr3 WorshipSkull3 MaxCapBagS3 BadgeD1 BadgeD2 BadgeD3 ResetCompletedS NPCtoken28 NPCtoken29 NPCtoken30 FillerMaterial".split(" "),
    "Anvil Tab III": "EquipmentHats53 EquipmentShirts15 EquipmentPants6 EquipmentShoes5 EquipmentPunching4 EquipmentSword2 EquipmentBows7 EquipmentWands3 EquipmentTools7 MaxCapBag5 EquipmentToolsHatchet5 MaxCapBagT5 FishingRod6 MaxCapBagFi5 CatchingNet6 MaxCapBagB5 TrapBoxSet4 MaxCapBagTr4 WorshipSkull4 MaxCapBagS4 EquipmentRings28 EquipmentRings29 MaxCapBagF5 MaxCapBagM6 EquipmentHats54 EquipmentShirts27 EquipmentPants21 EquipmentShoes22 EquipmentPunching5 EquipmentSword3 EquipmentBows8 EquipmentWands7 EquipmentTools11 MaxCapBagMi6 EquipmentToolsHatchet7 MaxCapBagT6 FishingRod7 MaxCapBagFi6 CatchingNet7 MaxCapBagB6 TrapBoxSet5 MaxCapBagTr5 WorshipSkull5 MaxCapBagS5 MaxCapBagF6 MaxCapBagM7 Trophy20 EquipmentSmithingTabs4 EquipmentHats61 EquipmentHats58 EquipmentHats59 EquipmentHats60 EquipmentShirts31 EquipmentShirts28 EquipmentShirts29 EquipmentShirts30 FoodTrapping1 FoodWorship1 InvBag109 EquipmentHats66 BadgeI1 BadgeI2 BadgeI3 Quest68 NPCtoken39 NPCtoken40 NPCtoken41 EquipmentPendant25 EquipmentHats68 EquipmentShirts6 EquipmentPants9 EquipmentShoes23".split(" "),
    "Anvil Tab IV": "EquipmentHats70 EquipmentShirts32 EquipmentPants24 EquipmentShoes24 EquipmentPunching6 EquipmentSword4 EquipmentBows9 EquipmentWands8 EquipmentTools8 MaxCapBagMi7 EquipmentToolsHatchet6 MaxCapBagT7 FishingRod8 MaxCapBagFi7 CatchingNet8 MaxCapBagB7 TrapBoxSet6 MaxCapBagTr6 WorshipSkull6 MaxCapBagS6 EquipmentShoes26 EquipmentShoes27 EquipmentShoes28 EquipmentShoes29 EquipmentShoes31 EquipmentShoes33 MaxCapBagF7 MaxCapBagM8 EquipmentHats71 EquipmentShirts33 EquipmentPants25 EquipmentShoes25 EquipmentPunching7 EquipmentSword5 EquipmentBows10 EquipmentWands9 EquipmentTools12 MaxCapBagMi8 EquipmentToolsHatchet8 MaxCapBagT8 FishingRod9 MaxCapBagFi8 CatchingNet9 MaxCapBagB8 TrapBoxSet7 MaxCapBagTr7 WorshipSkull7 MaxCapBagS7 MaxCapBagF8 MaxCapBagM9 FillerMaterial EquipmentSmithingTabs5 InvBag111 DNAgun1 DNAgun2 DNAgun3 EquipmentRings30 FillerMaterial FillerMaterial FillerMaterial EquipmentHats74 EquipmentShirts34 EquipmentPants8 EquipmentShoes34".split(" "),
    "Anvil Tab V": "EquipmentHats77 EquipmentShirts35 EquipmentPants26 EquipmentShoes35 EquipmentPunching8 EquipmentSword6 EquipmentBows11 EquipmentWands10 EquipmentTools9 MaxCapBagMi9 EquipmentToolsHatchet9 MaxCapBagT9 FishingRod10 MaxCapBagFi9 CatchingNet10 MaxCapBagB9 TrapBoxSet8 MaxCapBagTr8 WorshipSkull9 MaxCapBagS8 MaxCapBagF9 MaxCapBagM10 Bullet3 EquipmentSmithingTabs6 EquipmentHats83 EquipmentShirts36 EquipmentPants27 EquipmentShoes36 EquipmentPunching9 EquipmentSword7 EquipmentBows12 EquipmentWands11 EquipmentPendant30 EquipmentHats107 EquipmentShoes39 EquipmentRings35".split(" "),
    "Anvil Tab VI": "EquipmentHats105 EquipmentShirts37 EquipmentPants29 EquipmentShoes37 EquipmentPunching10 EquipmentSword8 EquipmentBows13 EquipmentWands12 EquipmentTools14 MaxCapBagMi10 EquipmentToolsHatchet12 MaxCapBagT10 FishingRod11 MaxCapBagFi10 CatchingNet11 MaxCapBagB10 TrapBoxSet9 MaxCapBagTr9 WorshipSkull10 MaxCapBagS9 MaxCapBagF10 MaxCapBagM11 EquipmentRings36 FillerMaterial EquipmentHats106 EquipmentShirts38 EquipmentPants30 EquipmentShoes38 EquipmentPunching11 EquipmentSword9 EquipmentBows14 EquipmentWands13 EquipmentTools15 MaxCapBagMi11 EquipmentToolsHatchet10 MaxCapBagT11 FishingRod12 MaxCapBagFi11 CatchingNet12 MaxCapBagB11 TrapBoxSet10 MaxCapBagTr10 WorshipSkull11 MaxCapBagS10 MaxCapBagF11 MaxCapBagM12 FoodG13 EquipmentSmithingTabs7".split(" ")
}  #anvil_items last pulled from code in 2.12. Search for: ItemToCraftNAME = function ()
anvil_tabs = {
    "Anvil Tab II": "EquipmentSmithingTabs2",
    "Anvil Tab III": "EquipmentSmithingTabs3",
    "Anvil Tab IV": "EquipmentSmithingTabs4",
    "Anvil Tab V":"EquipmentSmithingTabs5",
    "Anvil Tab VI": "EquipmentSmithingTabs6",
    #"Anvil Tab VII": "EquipmentSmithingTabs7",
}

def find_vendor_name(item_codename):
    for vendor_name, sold_items in vendor_items.items():
        if item_codename in sold_items:
            return vendor_name


filter_recipes = {
    "Lucky Lad": ["Luckier Lad"],
    "Beginner Recipe": [
        "Copper Band", "Iron Boots", "Steel Band", "Goo Galoshes", "Fur Shirt", "Dooble Goopi", "Bleached Designer Wode Patch Pants",
        "Serrated Rex Ring", "Fishing Overalls", "Bandito Pantaloon",
        "Blue Tee", "Peanut", "Golden Peanut",  #IDK about including these. They're technically from quests, but maybe they count too? :shrug:
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
