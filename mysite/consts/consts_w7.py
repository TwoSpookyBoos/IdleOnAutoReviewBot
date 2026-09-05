from utils.logging import get_logger
from utils.number_formatting import parse_number

logger = get_logger(__name__)

# Last updated in v2.505 May 18
ZenithMarket = ["TRUE_ZEN 1 1.14 250 2 1 }x_higher_bonuses_from_Zenith_Statues".split(" ", ),"KRUK_BUBBLES 2 6 5 1 1 Adds_a_new_bubble_for_Kattlekruk_to_boost!".split(" ", ),"LAMP_BOOST 5 1.09 200 1 1 }x_higher_bonuses_from_The_Lamp_in_Caverns".split(" ", ),"DOUBLE_CLUSTER 8 1.17 100 5 1 +{%_chance_for_a_Double_Zenith_Cluster_drop".split(" ", ),"BUBBLE_BOOST 15 1.5 25 2 1 +{_daily_LVs_for_all_Kattlekruk_bubbles".split(" ", ),"SUPER_DUPERS 50 1.7 25 1 1 Super_Talents_get_+{_more_LVs".split(" "),"MOST_GRANDIOSE 250 1.25 50 4 1 }x_Grand_Discovery_Chance_in_Spelunking".split(" ", ),"GIGA_SYMBOLS 1000 1.15 100 1 1 }x_Sneaking_Symbol_success_chance".split(" ", ),"WOOZLE_WUZZLE 5000 1.125 30 1 1 +{%_EXP_Gain_for_the_Research_skill!".split(" ", ),"CLASSY_GOGO 25000 1.115 100 1 1 }x_Class_EXP_gain,_for_now...".split(" ", ), ]
zenith_market_upgrade_data = []
for upgrade in ZenithMarket:
    name, base_price, price_mult_per_level, max_level, bonus_per_level, _, description_template = upgrade
    zenith_market_upgrade_data.append({
        "Name": name.replace("_", " "),
        "Base Price": parse_number(base_price),
        "Price Mult per Level": parse_number(price_mult_per_level),
        "Max Level": parse_number(max_level),
        "Bonus per Level": parse_number(bonus_per_level),
        "Description Template": description_template.replace("_", " "),
    })