from consts.consts_w1 import statues_dict

# `ArmoryUpg`. Re-verified 2026-08-29 against a same-day balance patch.
royal_armory_upgrades_list = ["Resource_Grades_製 1 1.00 0 1 1 0 0 0 Whenever_an_'Empty'_resource_gets_refilled,_it_gets_+1_Grade!_@_Each_Grade_means_+50%_Max_Resources_and_+$%_Collection_Rate!".split(" "), "Perfect_Purification 1 1.30 0 300 1 1 0 0 All_your_Purified_Maps_now_get_a_$x_bonus_to_Collection_Rate,_instead_of_the_standard_2x_bonus.".split(" "), "Kingdom_Expansion_2 1 1.00 0 1 1 4 0 0 Allows_you_to_expand_the_kingdom_into_World_2,_allowing_you_to_build_Outposts_and_collect_Resources!".split(" "), "Kingdom_Expansion_3 1 1.00 0 1 1 10 0 0 Allows_you_to_expand_the_kingdom_into_World_3,_allowing_you_to_build_Outposts_and_collect_Resources!".split(" "), "Kingdom_Expansion_4 1 1.00 0 1 1 15 0 0 Allows_you_to_expand_the_kingdom_into_World_4,_allowing_you_to_build_Outposts_and_collect_Resources!".split(" "), "Kingdom_Expansion_5 1 1.00 0 1 1 16 0 0 Allows_you_to_expand_the_kingdom_into_World_5,_allowing_you_to_build_Outposts_and_collect_Resources!".split(" "), "Kingdom_Expansion_6 1 1.00 1 1 1 25 0 0 Allows_you_to_expand_the_kingdom_into_World_6,_allowing_you_to_build_Outposts_and_collect_Resources!".split(" "), "Kingdom_Expansion_7 1 1.00 2 1 1 40 0 0 Allows_you_to_expand_the_kingdom_into_World_7,_allowing_you_to_build_Outposts_and_collect_Resources!".split(" "), "Kingdom_Expansion_8 1 1.00 1 1 1 45 0 0 Allows_you_to_expand_the_kingdom_into_World_8,_allowing_you_to_build_Outposts_and_collect_Resources!".split(" "), "Blunder_Outpost_PTS_製 1 1.50 2 999999 1 50 0 0 All_of_your_Outposts_in_World_1_get_+{_PTS_to_spend_on_upgrades!".split(" "), "Yumyum_Outpost_PTS 1 1.55 1 999999 1 70 0 0 All_of_your_Outposts_in_World_2_get_+{_PTS_to_spend_on_upgrades!".split(" "), "Tundra_Outpost_PTS 1 1.60 2 999999 1 75 0 0 All_of_your_Outposts_in_World_3_get_+{_PTS_to_spend_on_upgrades!".split(" "), "Hyperion_Outpost_PTS 1 1.65 2 999999 1 80 0 0 All_of_your_Outposts_in_World_4_get_+{_PTS_to_spend_on_upgrades!".split(" "), "Plateau_Outpost_PTS 1 1.70 2 999999 1 100 0 0 All_of_your_Outposts_in_World_5_get_+{_PTS_to_spend_on_upgrades!".split(" "), "Valley_Outpost_PTS 1 1.80 2 999999 1 101 0 0 All_of_your_Outposts_in_World_6_get_+{_PTS_to_spend_on_upgrades!".split(" "), "Shimmerfin_Outpost_PTS 1 1.90 3 999999 1 115 0 0 All_of_your_Outposts_in_World_7_get_+{_PTS_to_spend_on_upgrades!".split(" "), "World_8_Outpost_PTS 1 2.00 4 999999 1 140 0 0 All_of_your_Outposts_in_World_8_get_+{_PTS_to_spend_on_upgrades!".split(" "), "Peacetime_Milita_製 1 1.00 5 1 1 170 0 0 Militia_Units_now_also_give_$_EXP/hr_to_their_Outpost's_highest_Rank,_giving_them_a_use_beyond_clearing_new_maps!".split(" "), "Global_Decree_-_RG 1 3.50 10 999999 5 200 0 0 Each_Resource_Grade_(RG)_gives_all_outposts_+{%_Collection_Rate._@_Total_Bonus:+$%".split(" "), "Wonderful_Workers 1 2.10 10 999999 10 230 0 0 Each_Worker_Unit_now_gives_+$%_Collection_Rate_bonus_to_their_outpost,_instead_of_the_standard_+50%_bonus.".split(" "), "Tremendous_Traders 1 2.10 5 999999 20 260 0 0 Each_Trader_Unit_now_gives_$_EXP/hr_toward_their_Outpost's_Trading_Rank.".split(" "), "Great_Guards 1 15.0 10 10 5 270 0 0 Each_Guard_Unit_now_increases_the_connection_range_of_their_Outpost_by_+$px".split(" "), "Super_Surveyors 1 1.90 11 999999 15 280 0 0 Each_Surveyor_Unit_now_gives_$_EXP/hr_toward_their_Outpost's_Intel_Rank.".split(" "), "Mighty_Militia 1 1.20 11 999999 25 300 0 0 Each_Militia_Unit_now_clears_away_$_Monsters/hr_in_Uncontrolled_Maps.".split(" "), "Charismatic_Commanders 1 3.50 11 999999 5 320 0 0 Each_Commander_Unit_now_gives_$_EXP/hr_toward_their_Outpost's_Command_Rank.".split(" "), "Kingsman_Knights 1 5.00 12 999999 5 340 0 0 Each_Knight_Unit_now_gives_$_EXP/hr_toward_their_Outpost's_Military_Rank.".split(" "), "Passionate_Priests 1 2.10 12 999999 10 380 0 0 Each_Priest_Unit_now_gives_$_EXP/hr_toward_their_Outpost's_Purity_Rank.".split(" "), "Trader_Profession 1 1.00 10 1 1 400 0 0 Unlocks_the_Trader_profession,_who_level_up_their_Outpost's_Trading_Rank!_Swap_professions_via_'Upgrade_Outposts'_button.".split(" "), "Guard_Profession 1 1.00 13 1 1 420 0 0 Unlocks_the_Guard_profession,_who_boost_their_Outpost's_connection_range!_Swap_professions_via_'Upgrade_Outposts'_button.".split(" "), "Surveyor_Profession 1 1.00 13 1 1 450 0 0 Unlocks_the_Surveyor_profession,_who_level_up_their_Outpost's_Intel_Rank!_Swap_professions_via_'Upgrade_Outposts'_button.".split(" "), "Collect_Resources_Tool 0 1.00 14 1 1 480 0 0 Adds_a_new_button_to_the_World_Map!_When_enabled,_you_can_click_and_drag_on_your_Outposts_to_connect_them_to_Resources!".split(" "), "Upgrade_Outposts_Tool 0 1.00 13 1 1 520 0 0 Adds_a_new_button_to_the_World_Map!_When_enabled,_you_can_click_on_any_Outpost_and_spend_its_PTS_on_upgrades!".split(" "), "Move_Units_Tool 0.1 1.00 14 1 1 560 0 0 Adds_a_new_button_to_the_World_Map!_When_enabled,_you_can_click_and_drag_Movable_Units_to_change_which_Outpost_they're_stationed_at!".split(" "), "Rat_Breeding_Protocol_I 1 100 15 10 10 590 0 0 Verminous_Rats,_found_in_the_cellar_dungeon_of_the_Royal_Castle,_respawn_+{%_faster.".split(" "), "Rat_Breeding_Protocol_II 1 1.95 14 100 1 630 0 0 Boosts_the_respawn_rate_of_Verminous_Rats_by_a_further_+{%".split(" "), "Anti-Rodent_Power_Move_I 1 1.20 15 999999 5 660 0 0 Boosts_the_base_damage_you_deal_within_the_Royal_Castle_by_+{".split(" "), "Anti-Rodent_Power_Move_II 1 1.25 15 999999 2 710 0 0 Boosts_the_total_damage_you_deal_within_the_Royal_Castle_by_+{%".split(" "), "Parchment_of_Enchantment_製 1 1.00 20 1 1 750 0 0 Verminous_Rats_now_have_a_1_in_$_chance_to_drop_Parchments_of_Enchantment,_which_are_used_to_upgrade_Royal_Statues!".split(" "), "Parchment_Surplus 1 1.10 20 999999 1 800 0 0 Boosts_the_drop_rate_of_Parchments_of_Enchantment_by_+{%".split(" "), "Parchment_Doubleprint 1 1.85 20 100 1 850 0 0 Whenever_you_pick_up_Parchments_of_Enchantment,_there_is_a_$%_chance_to_get_DOUBLE!_So_like,_two_of_them!".split(" "), "Parchment_Recycling 1 3.20 21 50 1 900 0 0 When_using_Parchments_of_Enchantment_to_upgrade_Royal_Statues,_there_is_a_$%_chance_they_are_not_used_up._Free_Usage!".split(" "), "Royal_Marble 1 6.00 22 50 1 950 0 0 Mobs_in_maps_with_outposts_have_a_1_in_$_chance_to_drop_special_Marble_items,_which_are_used_to_unlock_the_Royal_Statues!".split(" "), "Support_Camps 1 1000000000.0 21 3 1 1000 0 0 You_can_modify_{_Outposts_per_World_into_Support_Camps._Connects_to_other_outposts,_givin'_$".split(" "), "Super_Support 1 2.10 21 100 1 1100 0 0 Support_Camps_give_}x_higher_boosts_to_their_connected_Outposts!".split(" "), "Savage_Strongholds 1 1000000000.0 22 3 1 1200 0 0 You_can_now_modify_{_Outpost_per_World_into_Savage_Strongholds!_They_remove_$x_more_resources,_but_you_don't_keep_any!".split(" "), "Royal_Reverence .1 100 23 20 1 1300 0 0 All_Royal_Statues_give_}x_higher_bonuses!".split(" "), "Royal_Talent_Points_I_製 .2 1.13 22 200 1 1350 0 0 +{_Talent_PTS_for_the_Royal_Guardian_class.".split(" "), "Royal_Talent_Points_II 1 1.22 22 200 1 1400 0 0 +{_Talent_PTS_for_the_Royal_Guardian_class.".split(" "), "Royal_Talent_Points_III 1 1.70 23 200 1 1450 0 0 +{_Talent_PTS_for_the_Royal_Guardian_class.".split(" "), "Royal_Talent_Points_IV 1 2.00 23 200 1 1500 0 0 +{_Talent_PTS_for_the_Royal_Guardian_class.".split(" "), "Global_Decree_-_OL 1 1.95 23 100 1 1550 0 0 Each_Outpost_LV_(OL)_gives_all_outposts_+{%_Collection_Rate._@_Total_Bonus:+$%".split(" "), "Global_Decree_-_PM 1 4.25 24 40 25 1600 0 0 Each_Purified_Map_(PM)_gives_all_outposts_+{%_Collection_Rate._@_Total_Bonus:+$%".split(" "), "Experiential_Triumph 1 1.90 25 100 2 1650 0 0 Every_100_Class_LVs_of_your_Royal_Guardian_over_1000_gives_all_outposts_+{%_Collection_Rate._Total_Bonus:+$%".split(" "), "Tip-Top_'sources_製 1 750 26 10 1 1700 0 0 +{%_Collection_Rate_for_every_POW_10_'Top_of_List'_Resources_you_own.___Total_Bonus:+{%".split(" "), "Guardian_Loyalty 1 1.00 26 1 1 1750 0 0 bro_no_way_no_howw".split(" "), "Talent_Reattainment 1 1.75 30 300 1 1800 0 0 Your_'All_Talent_LVs'_bonuses_now_apply_to_Royal_Guardian_talents,_but_only_up_to_+{_LVs.".split(" "), "Super_Talent_Unban 1 1.00 30 1 1 1850 0 0 You_can_now_'Make_Super'_your_Royal_Guardian_talents.".split(" "), "Greater_Education 1 1.00 31 1 1 1900 0 0 Unlock_the_3rd_upgrade_options_for_all_outposts_across_all_worlds!".split(" "), "Solo_Militia_Status 0.1 1.16 31 1000 4 1950 0 0 Active_kills_now_count_towards_clearing_monsters_to_build_outposts!_@_Also,_each_kill_has_a_{%_chance_to_count_as_extra!".split(" "), "Orblet_Pittance 1 3.50 32 100 1 2000 0 0 Adds_a_new_{%_chance_for_the_Orb_of_Verisimilitude_to_drop_a_3rd_orblet_every_1000_kills!".split(" "), "Blunder_Hills_Militia 0.25 10 33 10 1 2050 0 0 Recruits_a_new_Militia_unit_in_World_1,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "Yumyum_Desert_Militia 1 20 32 10 1 2100 0 0 Recruits_a_new_Militia_unit_in_World_2,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "Frostbite_Tundra_Militia 1 30 33 10 1 2150 0 0 Recruits_a_new_Militia_unit_in_World_3,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "Hyperion_Nebula_Militia 1 60 34 10 1 2250 0 0 Recruits_a_new_Militia_unit_in_World_4,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "Smouldering_Plateau_Militia 1 80 35 10 1 2300 0 0 Recruits_a_new_Militia_unit_in_World_5,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "Spirited_Valley_Militia 1 100 35 10 1 2400 0 0 Recruits_a_new_Militia_unit_in_World_6,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "Shimmerfin_Deep_Militia 1 150 36 10 1 2500 0 0 Recruits_a_new_Militia_unit_in_World_7,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "World_8_Militia 1 4000 36 10 1 2600 0 0 Recruits_a_new_Militia_unit_in_World_8,_which_clear_away_monsters_at_a_rate_of_$/hr_so_you_can_build_more_outposts!".split(" "), "Kingdom_Sovereignty .25 4.00 37 36 1 2700 0 0 Recruits_new_Movable_Unit_every_time_you_buy_this_upgrade!_@_Next_Unit:_$".split(" "), "Super_Savagery 1 2.30 9 100 4 2800 0 0 Savage_Strongholds_remove_}x_more_resources_than_before!".split(" "), "Resource_Replenish 1 1.05 9 1000 1 8800 0 0 All_'Empty'_resources_get_refilled_every_day._@_Also,_+{%_Collection_Rate_for_all_Outposts.".split(" "), "Trading_Rank 1 10000000.0 9 6 1 8800 0 0 Each_Trading_Rank_of_an_Outpost_gives_+1_PTS_for_Upgrades.$".split(" "), "Intel_Rank 1 1000000.0 9 5 10 8800 0 0 Each_Intel_Rank_of_an_Outpost_boosts_the_EXP_gain_of_all_its_Ranks_by_+{%".split(" "), "Command_Rank_製 1 1000000.0 9 5 25 8800 0 0 Each_Command_Rank_of_an_Outpost_adds_a_permanent_stationary_unit,_and_boosts_the_outpost's_Collection_Rate_by_+{%".split(" "), "Military_Rank 1 1000000.0 9 5 2 8800 0 0 Each_Military_Rank_of_an_Outpost_boosts_its_connection_range_by_+{px".split(" "), "Purity_Rank 1 1.00 9 1 1 8800 0 0 Achieving_a_PURITY_Rank_of_1_means_that_Outpost_and_Map_are_Purified._Click_the_膛_button_to_see_Purified_Bonuses.".split(" "), "Farmer_Joe 1 1.80 9 100 5 8800 0 0 Joe_will_tend_to_your_Equinox_Valley,_giving_+{%_Equinox_Bar_Fill_rate_and_spending_full_bars_on_the_upgrade_of_your_choice!".split(" "), "State-Wide_Propoganda 1 2.20 9 100 10 8800 0 0 Boost_EXP/hr_of_your_chosen_Rank_Type_by_}x,_which_can_be_freely_changed_with_the_arrows_above.".split(" "), "Statue_Flair 1 1.00 9 1 1 8800 0 0 Unlock_the_Statue_Flair_system,_letting_you_spend_Marble_to_boost_normal_Statues_over_at_the_Statue_Man_in_W1_Town!".split(" "), "Compounding_Outposting 1 17 9 1 1 8800 0 0 Pick_a_stat_to_boost!_More_outposts_built_means_bigger_boost!_@_Currently_giving_$".split(" "), "Prismatic_Guardian 1 2.50 9 100 1 8800 0 0 Instantly_gain_1_Prisma_Bubble_Fragment!_Spend_these_in_Alchemy_to_boost_your_bubbles!".split(" "), "Weekly_Skull_Stipend 1 2.10 9 100 2 8800 0 0 Start_each_week_with_{_Killroy_Skulls_over_in_W2_town!".split(" "), "Ribbonic_Guardian 1 20 9 20 3 8800 0 0 There's_a_{%_chance_for_each_of_the_Ribbons_you_earn_each_day_is_+1_Tier_higher!".split(" ")]

# `CustomLists.h.Research[43]` - display-order permutation (tree slot -> real ArmoryUpg index).
royal_armory_research43 = [int(v) for v in "30 46 58 31 9 41 70 37 78 35 27 71 20 60 32 19 79 2 61 57 23 0 47 10 80 28 21 68 73 24 50 56 38 81 42 43 3 62 18 11 52 36 29 72 22 76 44 69 48 74 25 17 33 39 4 63 12 75 26 77 53 49 40 1 51 82 59 45 55".split(" ")]

# `RoyalG[1][materialIdx]` - which royal-armory-resource-N icon an upgrade's material is.
royal_armory_resource_indices = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25, 26, 30, 31, 32, 33, 34, 35, 36, 37]

# Slot N's own upgrade's `[6]` field is NOT its real unlock requirement - the gate counts entries
# meeting their own requirement, so slot N's real threshold is the (N+1)-th smallest of all 83.
royal_armory_slot_unlock_thresholds = sorted(int(_row[6]) for _row in royal_armory_upgrades_list)

# Account-independent per-upgrade data, derived once from royal_armory_upgrades_list/royal_armory_research43
# above, in real tree-slot order. RoyalArmory.__init__ only needs to merge this with the one thing that
# varies per account: level (RoyalG[2][Index]).
royal_armory_upgrades = []
for _slot, _real_index in enumerate(royal_armory_research43):
    _upgrade_values = royal_armory_upgrades_list[_real_index]
    _clean_name = _upgrade_values[0].replace('製', '').replace('_', ' ').rstrip()
    # Genuine game quirk: the material spent is `ArmoryUpg[slot][3]` - the raw shelf slot, not the
    # upgrade actually shown there. Decoupled from every other field on this row.
    _cost_resource_values = royal_armory_upgrades_list[_slot]
    _resource_index = int(_cost_resource_values[3])
    royal_armory_upgrades.append({
        "Name": _clean_name,
        "Index": _real_index,
        "Slot": _slot,
        "Image": f"royal-armory-upgrade-{_slot}",
        "Cost Base": float(_upgrade_values[1]),
        "Cost Increment": float(_upgrade_values[2]),
        "Resource Index": _resource_index,
        # A handful of far-future upgrades reference a resource index whose icon isn't published yet.
        "Resource Image": f"royal-armory-resource-{_resource_index}" if _resource_index in royal_armory_resource_indices else 'placeholder',
        "Max Level": int(_upgrade_values[4]),
        "Value Per Level": int(_upgrade_values[5]),
        "Unlock Requirement": royal_armory_slot_unlock_thresholds[_slot],
        "Description": _upgrade_values[9].replace('_', ' '),
    })

# 8 chance-based "Royal Statue" unlock/enhance slots (`RGshard0`-`RGshard7`, `RoyalG[0]` levels) -
# separate from the W1 Statues Statue Flair boosts.
royal_armory_statue_names = [
    'Heracles the Mighty', 'Plutus the Prosperous', 'Ymir the Frostborne', 'Minerva the Resolute',
    'Hephaestus the Unbroken', 'Odin the Shrouded', 'Neptune the Unforgiving', 'Statue #8 (unreleased)',
]
# `StatueUpgOdds` for an unbuilt statue (idx 0-7): `1/[this]` chance per Marble spent.
royal_armory_statue_unlock_odds_denom = [25, 50, 100, 250, 500, 1000, 2500, 10000]
# Statues 6 and 7 (Neptune, Statue #8) aren't live in-game yet - no real marble art published for
# either. Only the first N are shown to players.
royal_armory_statues_released = 6
# The statue's own artwork. Statue 7 has no image since it's unreleased.
royal_armory_statue_images = [
    'royal-statue-0', 'royal-statue-1', 'royal-statue-2', 'royal-statue-3',
    'royal-statue-4', 'royal-statue-5', 'royal-statue-6', 'placeholder',
]
# `StatueBon`: bonus = (base + increment * max(0, tier-1)) * (1 + Royal Reverence's own bonus/100).
# Only statues 0-3 have a confirmed effect name in `Research[40]` (4-7 are unwritten placeholders).
royal_armory_statue_bonus_names = ['Total Damage', 'Drop Rate', 'Extra Kills', 'Class EXP', None, None, None, None]
royal_armory_statue_bonus_base = [200, 50, 30, 300, 10, 10, 10, 10]
royal_armory_statue_bonus_increment = [15, 5, 3, 20, 3, 3, 3, 3]
# Build material per statue (`RGshard{idx}`). Only 6 of 8 marbles published so far.
royal_armory_statue_marble_images = [
    'leafy-marble', 'sandy-marble', 'frosty-marble', 'sparkly-marble', 'toasty-marble', 'wispy-marble',
    'placeholder', 'placeholder',
]

# "Statue Flair" boosts the EXISTING W1 Statues via a separate levels array (`RoyalG[22]`)
# This bonus doesnt affect statue potency, only potency of submitting statues
royal_armory_statue_flair_names = [
    'No Flair', 'Common Flair', 'Grand Flair', 'Superior Flair',
    'Elegant Flair', 'Illustrious Flair', 'Mesmerizing Flair',
]
royal_armory_statue_flair_max_level = 3

# OrbletMarket
royal_armory_orblet_market_list = ["EMULSION 2 50 5 1 1 {%_chance_to_get_1M_statues_worth_of_Statue_EXP_when_a_Zenith_Cluster_is_formed!".split(" "), "HYDRATION 3 1.08 200 5 1 +{%_Resource_Collection_for_all_Outposts".split(" "), "TALENTED 5 1.120 100 1 1 +{_Talent_Points_for_Royal_Guardians".split(" "), "FULL_CLEAR 10 1.250 50 1 4 +{%_extra_kills_for_Clearing_Mobs_in_order_to_build_new_outposts!".split(" "), "GLORIFICATION 25 1.250 50 4 1 $".split(" "), "INTERVENE 20 1.125 100 1 1 }x_higher_chance_for_Regal_Intervention_to_trigger!".split(" "), "STRONK_RANK 50 1.200 50 5 1 All_kingdom_units_generate_Rank_EXP_+{%_faster".split(" "), "BARGAIN 100 1.50 25 10 1 All_Masterclass_upgrades_cost_+{%_less_than_before".split(" "), "LONG_RANGE 200 1.105 20 1 1 All_Outposts_get_+{px_longer_connection_range".split(" "), "PARCHMORE 500 1.150 100 1 1 +{%_Parchment_of_Enchantment_Drop_Rate_from_Verminous_Rats".split(" ")]

# `GLORIFICATION` (slot 4) isn't a leveled upgrade - it's a flat "spend 1 Orblet, 10% Glorify chance".
royal_armory_orblet_market_glorification_index = 4

# Account-independent per-slot data, derived once from royal_armory_orblet_market_list above.
# RoyalArmory.__init__ only needs to merge this with the one thing that varies per account: level
# (RoyalG[23][Index]).
royal_armory_orblet_market_upgrades = []
for _index, _slot_values in enumerate(royal_armory_orblet_market_list):
    royal_armory_orblet_market_upgrades.append({
        "Name": _slot_values[0].replace('_', ' ').title(),
        "Index": _index,
        "Cost Base": int(_slot_values[1]),
        "Cost Increment": float(_slot_values[2]),
        "Max Level": int(_slot_values[3]),
        "Value Per Level": int(_slot_values[4]),
        "Description": ' '.join(_slot_values[6:]).replace('_', ' '),
    })
