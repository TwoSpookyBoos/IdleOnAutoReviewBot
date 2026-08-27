from consts.idleon.caverns.cavern import HolesInfo
from utils.number_formatting import parse_number

# CosmoUpgrades in source. Last update v2.494
CosmoUpgrades = [[["25","0","Monumental_Vibes","All_of_your_Monument_Bonuses_are_}x_higher!_9_out_of_10_monument_enjoyers_recommend_this_bonus!"],["1","0","String_is_Strung","Adds_{_more_string_to_your_harp,_cluck_it_with_pride!_Err,_pluck_it._I'm_not_a_chicken_that_was_just_a_typo!!"],["30","0","Wishy_Washy","+{%_chance_to_get_an_additional_Wish_every_day_at_the_Lamp!"],["35","0","Rupies_Everywhere","Increases_the_chance_for_jars_to_have_multiple_rupies_by_+{%"],["10","0","Confused_Bonus","Don't_conjure_this..._it_does_nothing_yet!_Wait_for_future_updates,_where_this_bonus_and_more_will_be_added!"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],],[["30","0","Opal_Enthusiasm","Every_10th_opal_invested_in_a_villager_boosts_their_own_exp_gain_by_+{%"],["1","0","Contented_Creator","+{%_villager_exp_gain_per_schematic_created._@_Total_Bonus:_+|%"],["10","0","Cosmo,_Enhance!","You_can_now_enhance_conjuror_bonuses!_Also,_uh,_+{%_villager_exp_gain,_why_not?"],["25","0","Lengthmeister","All_measurement_bonuses_are_}x_higher!_Inchredible!_Meterrific!_Footastic!_Yards!!!!"],["20","0","Study_All_Nighter","+{%_Study_Rate_for_Bolaia!"],["2","0","Equal_Spread","+{%_villager_exp_per_5_opals_invested_in_the_villager_with_the_LEAST_opals!_@_Total_Bonus:_+$%"],["10","0","Confused_Bonus","Don't_conjure_this..._it_does_nothing_yet!_Wait_for_future_updates,_where_this_bonus_and_more_will_be_added!"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],],[["1","0","Pocket_Divinity","Get_the_link_bonuses_from_this_god:_@_Y_@_Z"],["2","0","Beeg_Beeg_Forge","Increase_the_forge_capacity_by_{x"],["100","0","Resource_Bursting","Increase_the_max_Multi-Ore_by_{%_but_not_just_for_ore..._for_ALL_resources!_Multi-fish,_Multi-everything!"],["6","0","Voter_Integrity","Get_+{%_Ballot_Box_bonus_multiplier!_This_way_you_can_be_even_MORE_emotionally_invested_in_the_vote_outcome!"],["75","0","Weapon_Relevancy","The_effect_Weapon_Power_has_on_DMG_is_{%_higher."],["12","0","Equinox_Maxim","Increases_the_Equinox_Bar_Fill_Rate_by_a_multiplicative_+{%"],["10","0","Confused_Bonus","Don't_conjure_this..._it_does_nothing_yet!_Wait_for_future_updates,_where_this_bonus_and_more_will_be_added!"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"],["10","0","Confused_Bonus","Who_am_I_to_tell_you_what_bonus_I_give?"]]]  # fmt: skip # noqa

majiks = [
    [
        {
            "BaseValue": parse_number(data[0]),
            "Name": data[2].replace("_", " "),
            "Template": data[3].split("_@_")[0].replace("_", " "),
            "MaxEnchantLevel": parse_number(HolesInfo[56 + type_index][majik_index]),
        }
        for majik_index, data in enumerate(majiks_bonuses)
        if data[2] != "Confused_Bonus"
    ]
    for type_index, majiks_bonuses in enumerate(CosmoUpgrades)
]
