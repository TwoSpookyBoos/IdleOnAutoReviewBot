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
