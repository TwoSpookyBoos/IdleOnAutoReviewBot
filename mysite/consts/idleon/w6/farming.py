from consts.idleon.consts_idleon import NinjaInfo

from utils.number_formatting import parse_number


# MarketInfo in source. Last update v2.48 14 Jan 2026
MarketInfo = ["LAND_PLOTS You_get_{_extra_plots_of_land_to_plant_crops_in 0 2 2 2 0 20 1".split(" "),"STRONGER_VINES +{%_chance_for_+1_crop_when_fully_grown 1 0.18 2 1.13 3 500 2".split(" "),"NUTRITIOUS_SOIL +{%_growth_speed_for_all_land 7 0.15 3 1.12 8 500 1".split(" "),"SMARTER_SEEDS +{%_farming_EXP_gain_from_all_sources 21 0.14 6 1.1 14 500 3".split(" "),"BIOLOGY_BOOST +{%_chance_of_crop_evolution,_or_'next_crop'_chance 46 0.09 10 1.1 31 500 15".split(" "),"PRODUCT_DOUBLER +{%_chance_for_crops_to_be_worth_2x_when_collected 30 0.12 15 1.2 42 500 3".split(" "),"MORE_BEENZ +{%_magic_beans_gained_when_trading_in_crops 61 0.11 25 1.15 53 500 2".split(" "),"RANK_BOOST Plots_earn_+{%_more_Rank_XP_when_a_crop_is_collected 84 0.11 30 1.2 80 500 3".split(" "),"OVERGROWTH Unlocks_Overgrowth_(OG)._Each_OG_doubles_crop_value_~_EXP 2 0.10 10 1.1 19 1 1".split(" "),"EVOLUTION_GMO }x_crop_evolution_chance_per_crop_you_have_200_of 2 0.10 15 1.080 25 500 0.8".split(" "),"SPEED_GMO +{%_growth_speed_per_crop_you_have_1000_of 2 0.10 25 1.155 36 500 0.3".split(" "),"OG_FERTILIZER }x_higher_chance_for_Overgrowth_to_occur 2 0.10 40 1.060 48 500 1".split(" "),"EXP_GMO +{%_farming_EXP_gain_crop_you_have_2500_of 2 0.10 60 1.095 57 100 1".split(" "),"LAND_RANK Each_plot_now_gets_Rank_XP_when_a_crop_is_collected. 2 0.10 80 1.050 61 1 1".split(" "),"VALUE_GMO +{%_crop_value_per_per_crop_you_have_10000_of 2 0.10 150 1.125 95 500 0.02".split(" "),"SUPER_GMO +{%_all_'GMO'_bonuses_per_crop_you_have_100K 2 0.10 250 1.20 109 50 0.5".split(" "),] # fmt: skip # noqa

market_info = [
    {
        "Name": market_item[0].replace("_", " ").title(),
        "Description": market_item[1].replace("_", " "),
        "UpgradeCropIndexStart": parse_number(market_item[2]),
        "UpgradeCropIndexScale": parse_number(market_item[3]),
        "BaseCost": parse_number(market_item[4]),
        "CostIncrement": parse_number(market_item[5]),
        "UnlockRequirement": parse_number(market_item[6]),
        "MaxLevel": parse_number(market_item[7]),
        "BonusPerLevel": parse_number(market_item[8]),
    }
    for market_item in MarketInfo
]

depot_bonus = NinjaInfo[31]
# scaling info from "CropSCbonus" in _customBlock_FarmingStuffs in source.
# Last update v2.48 14 Jan 2026
crop_depot_list = [
    {
        "EmporiumUnlockName": "Reinforced Science Pencil",
        "Name": "Pencil",
        "Bonus": depot_bonus[0].replace("_", " "),
        "funcType": "add",
        "x1": 20,
        "x2": 0,
        "Image": "depot-pencil",
    },
    {
        "EmporiumUnlockName": "Science Pen",
        "Name": "Pen",
        "Bonus": depot_bonus[1].replace("_", " "),
        "funcType": "pow",
        "x1": 1.02,
        "x2": 0,
        "Image": "depot-pen",
    },
    {
        "EmporiumUnlockName": "Science Marker",
        "Name": "Marker",
        "Bonus": depot_bonus[2].replace("_", " "),
        "funcType": "add",
        "x1": 8,
        "x2": 0,
        "Image": "depot-marker",
    },
    {
        "EmporiumUnlockName": "Science Featherpen",
        "Name": "Featherpen",
        "Bonus": depot_bonus[3].replace("_", " "),
        "funcType": "pow",
        "x1": 1.1,
        "x2": 0,
        "Image": "depot-featherpen",
    },
    {
        "EmporiumUnlockName": "Science Environmentally Sourced Pencil",
        "Name": "Environmentally Sourced Pencil",
        "Bonus": depot_bonus[4].replace("_", " "),
        "funcType": "add",
        "x1": 15,
        "x2": 0,
        "Image": "depot-green-pencil",
    },
    {
        "EmporiumUnlockName": "Science Crayon",
        "Name": "Crayon",
        "Bonus": depot_bonus[5].replace("_", " "),
        "funcType": "add",
        "x1": 7,
        "x2": 0,
        "Image": "depot-crayon",
    },
    {
        "EmporiumUnlockName": "Science Paintbrush",
        "Name": "Paintbrush",
        "Bonus": depot_bonus[6].replace("_", " "),
        "funcType": "add",
        "x1": 0.1,
        "x2": 0,
        "Image": "depot-paintbrush",
    },
    {
        "EmporiumUnlockName": "Science Highlighter",
        "Name": "Highlighter",
        "Bonus": depot_bonus[7].replace("_", " "),
        "funcType": "add",
        "x1": 1,
        "x2": 0,
        "Image": "depot-highlighter",
    },
    {
        "EmporiumUnlockName": "Science Fancy Pen",
        "Name": "Fancy Pen",
        "Bonus": depot_bonus[8].replace("_", " "),
        "funcType": "add",
        "x1": 5,
        "x2": 0,
        "Image": "depot-fancy-pen",
    },
]

landrank_list = [
    {
        "Name": name.replace("_", " "),
        "Description": NinjaInfo[35][index].replace("_", " "),
        "UnlockLevel": parse_number(NinjaInfo[37][index]),
        "Base Value": parse_number(NinjaInfo[36][index]),
    }
    for index, name in enumerate(NinjaInfo[34])
]

# SeedInfo in source. Last updated v2.48 Giftmas Event
SeedInfo = ["BASIC 0 0 20 1 0.30 0.75".split(" "),"EARTHY 1 21 45 10 0.12 0.63".split(" "),"BULBO 2 46 60 25 0.04 0.3".split(" "),"SUSHI 3 61 83 50 0.01 0.4".split(" "),"MUSHIE 4 84 106 80 0.003 0.2".split(" "),"GLASSY 5 107 229 120 0.0005 0.05".split(" "),"MEDAL 6 230 279 120 0.000069420 0.003".split(" ")] # fmt: skip # noqa
seed_dict = {
    info[0].title(): {
        "CropIndexStart": parse_number(info[2]),
        "CropIndexEnd": parse_number(info[3]),
        "EvoBase": parse_number(info[5]),
        "EvoCoefficient": parse_number(info[6]),
    }
    for info in SeedInfo
}

# MarketExoticInfo in source. Last update 2.48 Giftmas event
MarketExoticInfo=["SPROUTLUCK_I }x_crop_evolution_chance 3 500 1 2".split(" "),"SPROUTLUCK_II }x_crop_evolution_chance 5 600 1 2".split(" "),"SPROUTLUCK_III }x_crop_evolution_chance 6 700 1 2".split(" "),"SPROUTLUCK_IV }x_crop_evolution_chance 7 800 1 2".split(" "),"GENEOLOGY_I +{%_crop_evolution_chance_per_Farming_LV_above_50 9 6 1 2".split(" "),"GENEOLOGY_II +{%_crop_evolution_chance_per_Farming_LV_above_100 11 12 1 2".split(" "),"GENEOLOGY_III +{%_crop_evolution_chance_per_Farming_LV_above_150 13 20 1 2".split(" "),"GENEOLOGY_IV +{%_crop_evolution_chance_per_Farming_LV_above_200 15 28 1 2".split(" "),"GENEOLOGY_V +{%_crop_evolution_chance_per_Farming_LV_above_250 16 50 1 2".split(" "),"STABLEROOT_I +{%_Land_Rank_EXP_gain_for_all_plots 17 350 1 2".split(" "),"STABLEROOT_II +{%_Land_Rank_EXP_gain_for_all_plots 18 250 1 2".split(" "),"STABLEROOT_III +{%_Land_Rank_EXP_gain_for_all_plots 20 400 1 2".split(" "),"VIGOUROOT_I }x_Land_Rank_EXP_gain_for_all_plots 21 100 1 2".split(" "),"VIGOUROOT_II }x_Land_Rank_EXP_gain_for_all_plots 23 130 1 2".split(" "),"PLUMP_DATABASE +{%_higher_bonuses_from_the_Land_Rank_Database 24 60 1 2".split(" "),"DATADIGGING +$_higher_max_LV_for_5th_column_of_Land_Rank_Database 25 5 1 2".split(" "),"LEGUMIOSO_I +{%_Extra_Beans_from_Legumulyte 27 250 1 2".split(" "),"LEGUMIOSO_II +{%_Extra_Beans_from_Legumulyte 29 350 1 2".split(" "),"LEGUMIOSO_III +{%_Extra_Beans_from_Legumulyte 30 420 1 2".split(" "),"LARGUMES_I }x_more_Beans_from_Lugumulyte 31 90 1 2".split(" "),"LARGUMES_II }x_more_Beans_from_Lugumulyte 32 130 1 2".split(" "),"FARMER_BRAIN +{%_Farming_EXP_gain_on_all_characters 33 300 1 2".split(" "),"FARMER_KNOWHOW }x_Farming_EXP_gain_on_all_characters 34 120 1 2".split(" "),"STALK_VALUE_I +{%_higher_Crop_Value_max_cap 36 50 1 2".split(" "),"STALK_VALUE_II +{%_higher_Crop_Value_max_cap 37 70 1 2".split(" "),"STALK_VALUE_III +{%_higher_Crop_Value_max_cap 38 120 1 2".split(" "),"EVERGROW_I }x_Overgrowth_Chance_for_all_crops 40 100 1 2".split(" "),"EVERGROW_II }x_Overgrowth_Chance_for_all_crops 41 150 1 2".split(" "),"DOUBLE_PETAL_I +{%_chance_for_crops_to_be_worth_2x_when_harvested 42 50 1 2".split(" "),"DOUBLE_PETAL_II +{%_chance_for_crops_to_be_worth_2x_when_harvested 44 70 1 2".split(" "),"GOGOGROW +{%_Growth_Speed_for_all_land_plots 45 50 1 2".split(" "),"BOUNTIFUL_I +{%_chance_for_+1_crop_when_fully_grown 46 50 1 2".split(" "),"BOUNTIFUL_II +{%_chance_for_+1_crop_when_fully_grown 48 60 1 2".split(" "),"BOUNTIFUL_III +{%_chance_for_+1_crop_when_fully_grown 50 70 1 2".split(" "),"BETTER_DAY_I +{%_cheaper_Day_Market_upgrades 51 40 1 2".split(" "),"BETTER_DAY_II +{%_cheaper_Day_Market_upgrades 53 55 1 2".split(" "),"BETTER_NIGHT_I +{%_cheaper_Night_Market_upgrades 54 40 1 2".split(" "),"BETTER_NIGHT_II +{%_cheaper_Night_Market_upgrades 56 55 1 2".split(" "),"BETTER_EXOTIC +{%_extra_LVs_when_buying_Exotic_Upgrades 58 70 1 2".split(" "),"FREEXOTIC +{%_chance_to_save_a_purchase_when_buying_Exotic 60 30 1 2".split(" "),"SCIENTERRIFIC +{%_higher_bonuses_from_Crop_Scientist 62 20 1 2".split(" "),"BRIAR_PATCH +{%_Total_Damage_@_(Not_Farming_Related) 64 1 0 2".split(" "),"GRAVEL_POUND }x_Total_Spelunking_POW_@_(Not_Farming_Related) 66 300 1 2".split(" "),"SAP_SURGE }x_Amber_found_in_Spelunking_@_(Not_Farming_Related) 67 500 1 2".split(" "),"4_LEAF_CLOVER +{%_Palette_Luck_in_Gaming_@_(Not_Farming_Related) 69 150 1 2".split(" "),"5_LEAF_CLOVER }x_Artifact_Find_Chance_@_(Not_Farming_Related) 79 30 1 2".split(" "),"BUD_COURIER +{%_chance_for_2x_Snail_Mail_@_(Not_Farming_Related) 71 35 1 2".split(" "),"STUDIOUS_SPORE +{%_Spelunking_EXP_Gain_@_(Not_Farming_Related) 73 200 1 2".split(" "),"PRISMA_PETAL +{%_Prisma_Bubble_Bonus_@_(Not_Farming_Related) 75 2 1 2".split(" "),"EXALTED_ELDOU +{%_Exalted_Stamp_Bonus_@_(Not_Farming_Related) 77 2 1 2".split(" "),"INTELLEAF +{%_Class_EXP_@_(Not_Farming_Related) 78 300 1 2".split(" "),"GRAPEVINE }x_Villager_EXP_gain_@_(Not_Farming_Related) 81 70 1 2".split(" "),"HOLLOW_TRUNK }x_Jar_Collectibles_Chance_@_(Not_Farming_Related) 83 200 1 2".split(" "),"BONEMEAL_SOIL +{%_Deathbringer_Bones_@_(Not_Farming_Related) 85 160 1 2".split(" "),"FORCE_OF_NAUTRE +{%_Windwalker_Dust_@_(Not_Farming_Related) 86 160 1 2".split(" "),"PURPLE_GRASS +{%_Arcane_Cultist_Tachyons_@_(Not_Farming_Related) 87 160 1 2".split(" "),"POTENT_HEMLOCK +{%_Kill_per_Kill_@_(Not_Farming_Related) 88 35 1 2".split(" "),"GOLD_FIGLEAF +{%_Gold_Balls_gained_in_Arcade_@_(Not_Farming_Related) 89 10 1 2".split(" "),"SNAPEGRASS }x_Jade_Gain_in_Sneaking_@_(Not_Farming_Related) 91 1500 1 2".split(" "),"POMMELION_SEED +{%_Drop_Rate_@_(Not_Farming_Related) 92 25 1 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 93 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 94 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 95 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 96 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 97 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 98 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 99 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 100 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 101 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 102 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 104 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 106 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 108 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 110 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 112 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 113 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 114 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 116 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 118 1 0 2".split(" "),"NAME_MAGNI +{%_everything_is_awesome_evrythn_is_cool_when_u_r_tem 119 1 0 2".split(" ")] # fmt: skip # noqa

exotic_market_info = [
    {
        "Name": name.replace("_", " "),
        "Description": description.replace("_@_", " ")
        .replace("_", " ")
        .replace(" (Not Farming Related)", ""),
        "CostCropIndex": parse_number(crop_index),
        "Coefficient": parse_number(max_value),
        "ScalingType": parse_number(scaling_type),
    }
    for name, description, crop_index, max_value, scaling_type, _ in MarketExoticInfo
    if name != "NAME_MAGNI"
]
