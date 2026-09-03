from utils.logging import get_logger
from utils.number_formatting import parse_number

logger = get_logger(__name__)

# `CoralReef` in source. Last updated in v2.46 Dec 6
CoralReef = ["Every_day_you_play,_your_Grind_Time_bubble_gets_+{_LVs 15 10 1.25 243 0 274 22 324 19 31 171 389 _".split(" "), "Orange... 1 10 1.5 300 332 63 400 300 20 0 400 400 _".split(" "), "Adds_a_new_bonus_to_your_Tome's_Epilogue_in_World_4,_which_goes_up_with_your_Tome_Score! 10 15 1.65 236 328 248 350 309 25 0 479 381 _".split(" "), "Adds_a_new_mini_'Ninja_Knowledge'_upgrade,_level_it_up_with_your_Jade! 12 10 1.55 263 611 270 647 325 24 0 789 384 _".split(" "), "The_Gallery_gives_+{%_higher_bonuses,_@_and_has_+}_more_slots_for_Trophies 10 40 1.5 290 0 13 24 95 28 13 164 189 _".split(" "), "Blue... 1 10 1.5 300 615 52 400 300 20 0 400 400 _".split(" ")]
coral_reef_names = ['Brain Coral', 'Carnation Coral', 'Anemone Coral', 'Pillar Coral', 'Paragorgia Coral', 'Staghorn Coral']
coral_reef_bonuses = {
    coral_reef_names[index] : {
        'Description': decription.replace('_', ' ').replace('@', '').replace('+{', '').replace('+}', '').replace('%', ''),
        'Max Level': parse_number(max_level, -1),
        'Image': f'coral-{index}',
        'Coefficient': parse_number(coefficient, 0),
        'Exponent Base': parse_number(exponent_base, 0)
    }
    # all leftover `_` parts seem to be coordinates used when rendering
    for index, (decription, max_level, coefficient, exponent_base, _, _, _, _, _, _, _ ,_, _, _) in enumerate(CoralReef)
}

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