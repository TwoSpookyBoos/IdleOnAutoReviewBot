import math
from consts.consts_autoreview import ValueToMulti
from utils.logging import get_logger

logger = get_logger(__name__)


def getCavernResourceImage(resource_number: int):
    try:
        if int(resource_number) <= 9:
            resource_image = f'well-sediment-{resource_number}'
        elif int(resource_number) <= 19:
            resource_image = f'harp-note-{int(resource_number) - 10}'
        elif int(resource_number) <= 29:
            resource_image = f'jar-rupie-{int(resource_number) - 20}'
        else:
            resource_image = ''
    except:
        logger.exception(f"Error parsing resource type for resource {resource_number}")
        resource_image = ''
    return resource_image


HolesInfo = [
    "57 57 228 -29 183 0 216 -150 96 -219 255 -45 175 -28 257 -36 176 -67 216 -150 273 -35 184 -66 216 -150 24 -75 180 -114 220 -43 173 -60 232 95 216 -150 254 -49 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0".split(" "),
    "0 0 8 0 0 7 0 0 0 0 10 2 2 4 3 6 2 5 1 6 0 0 0 0 0 0 0 0 0 0".split(" "),
    "289 208 253 244 324 244 289 282 219 282 358 282 253 321 324 321 289 357".split(" "),
    "497 210 443 210 432 264 454 318 486 264 551 210 540 264 562 318 551 372 508 318 443 372 497 372".split(" "),
    "698 207 751 214 769 258 716 251 663 244 681 288 734 295 752 339 699 332 646 325 664 369 717 376".split(" "),
    "289 208 253 244 324 244 289 282 219 282 358 252 253 321 324 321 289 357".split(" "),
    "497 210 443 210 432 264 454 318 486 264 551 210 540 264 562 318 551 372 508 318 443 372 497 372".split(" "),
    "698 207 751 214 769 258 716 251 663 244 681 288 734 295 752 339 699 332 646 325 664 329 717 376".split(" "),
    ["12", "21"],
    ["12", "11", "12", "32"],
    "12 2 12 21 12 41".split(" "),
    "10 6 3 24 21 19 14 37".split(" "),
    ["13", "13"],
    ["3", "13", "24", "13"],
    "13 5 2 22 24 22".split(" "),
    "3 3 24 3 3 24 24 24".split(" "),
    ["12", "12"],
    ["5", "5", "18", "20"],
    "3 7 21 7 12 21".split(" "),
    "12 1 1 12 23 12 12 23".split(" "),
    "Explorer_@___@_Each_LV_of_this_villager_unlocks_a_new_cavern!_@___@_Invest_opals_to_increase_their_XP/hr_using_that_blue_button! Engineer_@___@_Each_LV_unlocks_3_new_schematics_to_create!_@_Every_5_LVs_unlocks_an_additional_schematic!__@___ Conjuror_@___@_Each_LV_gives_+1_Majik_Point_to_put_into_permanent_bonuses! Measurer_@___@_Each_LV_gives_a_new_bonus_to_upgrade!_The_multi_goes_up_as_you_increase_its_IdleOn_stat,_shown_in_parenthesis!__@___ Librarian_@___@_Send_them_to_study_specific_caverns_to_discover_powerful_bonuses!_Each_LV_boosts_his_study_rate_by_+5%___ Elder ??? ???".split(" "),
    "0 50 500 9000 125000 1500000 20000000 100000000 500000000 2000000000.0".split(" "),
    "讽 论 许 讲 议 训".split(" "),
    "316 639 291 372 409 533 264 409 400 600 240 400 390 556 217 382 393 567 180 331 400 580 190 390 334 620 198 390 443 502 286 372 340 640 116 295 390 556 217 382 385 560 185 340 439 507 251 380 390 556 217 382 142 818 164 358 345 614 75 294 0 0 0 0 0 0 0 0 316 639 294 425 390 556 217 382 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0".split(" "),
    "THE_MOTHERLODE THE_UNDYING_HIVE THE_EVERTREE THE_BOTTOMLESS_TRENCH MONUMENT_OF_BRAVERY MONUMENT_OF_JUSTICE MONUMENT_OF_WISDOM MONUMENT_OF_COMPASSION A A A A A".split(" "),
    ["Mining_Efficency_needed:", "Catching_Efficency_needed:", "Choppin'_Efficency_needed:", "Fishing_Efficency_needed:"],
    ["Motherlode", "Bug14", "MotherlodeTREE", "MotherlodeFISH"],
    ["LAYER_", "HIVE_", "TRUNK_", "DEPTH_"],
    "BIGGER_BITE Hounds_now_have_a_base_attack_value_of_{ ELUSIVE_INSTINCT Hounds_now_require_{_Accuracy_for_100%_hit_chance CANINE_RECOVERY All_hounds_now_heal_{%_HP_every_3s BIGGER_BOW_WOW Hounds_have_a_10%_chance_to_spawn_BIG_with_{x_HP_and_DMG DOGGO_EMP_EFFECT Somehow_the_hounds_now_make_your_attacks_cost_{x_more_MP CURSED_HOWL Hounds_have_a_5%_chance_to_be_cursed,_causing_{x_more_Fear DEN_DESPAIR Start_with_your_fear_meter_filled_to_{% FAST_AND_DEADLY Hounds_cause_fear_{_seconds_faster_than_normal".split(" "),
    ["`@#$%^&*():;<,>.?{[}船般航舞窗皮白癖爬爆歧武歌歉款欺欧欣欢次斗文敲数敬散敢敞教敏情悚悔恼恰恭恨恤恢恒"],
    "1 80 300 750 2000 5000 10000 24000".split(" "),
    "Swords_deal_{~}_damage +2_additional_Sword You_can_Re-Throw_5_swords_per_story +1_additional_Sword You_get_1_Retelling_per_story +1_additional_Sword +10_Re-Throws_per_story +1_additional_Sword Start_with_$_coins Start_with_2_Mental_Health You_can_Dismiss_1_case_per_story Start_with_1.5x_more_coins +1_Mental_Health_and_Dismissal Start_with_10_popularity Start_with_3x_more_coins +2_Mental_Health_and_Dismissals Start_with_#_Attempts Get_+2_Attempts_per_Board_Clear 1st_attempt_each_Board_reveals_row Start_with_4_Insta_Matches_per_story +4_additional_Starting_Attempts 4th_attempt_each_Board_reveals_square Get_+1_Attempts_per_Board_Clear +5_additional_Insta_Matches Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6".split(" "),
    "+{%|Mining|Efficiency }x_Bucket|Fill_Rate }x|Cooking_Speed +{%_EXP|Gain_for|Villagers }x|Gaming_Bits|Gain +{%_Chance|for_Bravery|Opals +{%_DMG|for_all|Characters }x_Bell_Ring|&_Ping_Rate +{%|All_Monument|AFK_Gain }x_Bravery|Bonuses_Multi +{%_Catching|Efficiency }x_Harp|Note_Gain }x_Artifact|Find_Chance +{%_EXP|Gain_for|Villagers }x|All_Summoning|Essence_Gain +{%_Chance|for_Justice|Opals +{%_Class|EXP_Gain +{%_more|daily_Lamp|Wishes +{%|All_Monument|AFK_Gain }x_Justice|Bonuses_Multi +{%_Choppin|Efficiency }x_Jar|Rupie_Value }x_Jade|Coin_Gain +{%_EXP|Gain_for|Villagers }x|Farming_Crop|Evo_Chance +{%_Chance|for_Wisdom|Opals +{%_Player|Drop_Rate +{%_Gambit|Points +{%|All_Monument|AFK_Gain }x_Wisdom|Bonuses_Multi Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_4 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_5 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6 Monument_6".split(" "),
    "DIRTY_NAPKIN LIL_BABY_SPIDER STRAW_SCARECROW DIM_NIGHTLIGHT BEDTIME_SHADOW THE_1[_OF_GERMS SLOW_ESCORT_NPC MONDAYS BROCCOLINI POP_SONG DOLL_TOY INSIDE_OUT_SOCK MILKLESS_CEREAL EXCESS_CALORIES SLIGHTLY_SHORT_LEG MUMBLE_RAPPER VENTRILAKWIST SPELLING_TEST_RESULT AIRPLANE_BABY SPECIFIC_CROW CLOWN ABSENCE_OF_CLOWNS DISCORD_CHAT_FLEX VIDEO_GAMES".split(" "),
    "Eww_gross_who_knows_where_that_thing_has_been AAAHH_KILL_IT_KILL_IT A_truly_intimidating_and_very_much_real_enemy_stood_before_me In_darkness_the_monsters_under_the_bed_thrive AAAAAAAAAHHHH_MONSTER If_the_sanitizer_couldn't_get_them_what_chance_do_I_have WHY_CANT_YOU_MOVE_FASTER_YOU_FIEND You_haven't_stopped_bothering_me_since_first_grade Terrible_taste_and_pretentious_name,_I_HATE_YOU I_don't_care_how_many_people_like_it,_it_sucks!!! The_lamest_of_all_toys,_action_figure_gang_for_life! I_nearly_lost_my_mind_fixing_you_every_day Truly_a_horrendous_sight_to_behold_on_weekend_morning Why_must_you_take_such_a_hideous_form_upon_my_body? You_FIEND,_you_ALWAYS_make_the_chair_wobble_uncontrolably What_are_you_even_SAYING??? Speaking_without_moving_your_mouth_should_be_illegal An_F?_Noooooooo! SHUT_UP_SHUT_UPPPPPP Grrr,_the_one_that_stole_my_food_Sunday_March_11th_2007... Huh?_I_wasn't_afraid_of_clowns,_I_loved_clowns! NOOOOOOOOOOOOOOOOoooooo! Terrible,_just_terrible... The_worst_media_form!_You_poison_our_youth! It's_been_a_while_since_the_last_update,_they_have_formed_an_army".split(" "),
    "So_you_as_well_have_an_undying_lust_for_battle,_I_wish_you_could've_fought_with_me_in_my_final_hour... Fighting_to_the_bitter_end,_we_really_did_make_the_best_of_this_test_known_as_life... A_weaker_gamer_would_have_run_at_some_point,_but_I'm_glad_to_know_at_least_you_would've_stayed_with_me! ..._and_when_the_dust_settled_there_were_no_bonuses_kept,_just_an_everlasting_idea_of_bravery. I_always_said_I'd_rather_live_by_what_I_live_by_than_die_when_I'm_fine So_there_you_have_it,_that's_the_story!_I_tried_so_hard,_and_got_so_far,_but,_well_you_know_how_it_ended... Ah_don't_feel_too_bad_for_me!_I'm_a_master_mental_gymnast,_I_already_see_the_loss_as_a_win! I..._lost?_I_guess_I_only_thought_about_the_good_times,_I_forgot_that's_how_it_ended... Wait_no_no,_that's_not_how_it_went..._I_must_have_been_thinking_about_a_friend,_I_would_never_have_lost_like_that! Well,_that's_my_story!_Standing_up_against_true_evil_with_honor,_bonuses_be_darned!".split(" "),
    "Maybe_when_I_was_younger,_before_I_came_to_understand_the_virtue_of_bravery... You_really_think_running_was_an_option?_To_abandon_the_fight,_all_for_a_few_bonuses? Huh,_well_uh,_I_never_actually_considered_running_away..._probably_why_I_have_a_monument_and_you_don't! No_no,_that's_not_how_MY_story_ended,_but_I_suppose_everyone_has_their_own_story_to_tell... Well_that's_not_how_MY_story_ended,_but_I_suppose_everyone_has_their_own_story_to_tell... No_wonder_I_was_left_to_fend_for_myself,_everyone_always_thinks_to_run_in_the_face_of_trouble... Ah,_you_didn't_think_I'd_want_to_risk_it_eh?_Even_just_one_more_fight? All_the_bonuses_in_the_world_wouldn't_have_convinced_me_of_running! The_bonuses_may_be_comforting_now,_but_I_wouldn't_be_able_to_live_with_a_guilty_conscience... Run_away?_Bah,_just_the_thought..._maybe_next_time_you'll_stand_by_me_'till_the_end! I_would_never_run,_but_go_ahead_and_keep_your_crummy_bonuses..._they're_worthless_compared_to_the_glory_of_battle! I'm_not_surprised_your_mind_thinks_to_flee..._you_weren't_the_only_one_who_left_me_to_perish! Ugh,_It's_always_about_bonuses_these_days..._no_one_is_in_it_for_the_glory_like_me! No_wonder_I_had_to_fight_alone,_all_you_gamers_think_about_is_running_away! I_think_I_had_one_more_fight_in_me,_but_that's_a_story_for_a_different_day... I_think_I_had_one_more_fight_in_me,_but_that's_a_story_for_a_different_day... I_couldn't_disagree_more,_but_I_know_bonuses_mean_so_much_to_so_many... You_would_rather_I_run_than_be_brave?_I_mean_yea,_you_get_to_keep_all_those_bonuses_forever..._but_still! You_would_rather_I_run_than_be_brave?_I_mean_yea,_you_get_to_keep_all_those_bonuses_forever..._but_still! You_would_rather_I_run_than_be_brave?_I_mean_yea,_you_get_to_keep_all_those_bonuses_forever..._but_still!".split(" "),
    "2 4 10 1 8 2 1 1 50 250 2 4 500 1 5 2 1 300 50 250 2 3 2 1 4 2 100 35 50 250 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0".split(" "),
    "3 2 5 0 4 1 6 7".split(" "),
    "1 4 6 11 16 21 26".split(" "),
    "0 1 58 59 2 12 3 52 15 16 14 26 24 4 57 42 17 56 49 32 27 13 5 18 55 45 43 39 33 37 41 6 28 19 60 25 23 29 53 50 34 40 7 20 46 38 47 48 54 44 61 35 8 21 30 9 62 71 80 69 79 63 85 74 81 36 89 64 90 76 70 87 91 65 78 72 86 66 92 22 73 82 67 10 75 77 83 93 11 68 88 84 51 31".split(" "),
    "Bravery Justice Wisdom Compassion Type5 Type6".split(" "),
    "15000000000 100 1000000 300 150 1500 1 1 1 1 1 1".split(" "),
    ["lol"],
    ["렴련렛렘렐렌레렀럽럼"],
    "Creates_{_of_the_note_you're_tuned_to!_@_LV_bonus:_+}%_Harp_Note_Gain Has_a_{%_chance_of_finding_an_opal!_@_LV_bonus:_|x_Harp_Note_Gain Doesn't_do_anything..._but_its_LV_bonus_is_freakin'_epic!_@_LV_bonus:_|x_Harp_Power/hr Creates_{_of_the_tune,_and_notes_next_to_the_tune!_@_LV_bonus:_+}%_Harp_Note_Gain Gives_{_EXP_to_all_string_types!_@_LV_bonus:_+}%_String_EXP_Gain! Creates_{_of_every_note_you_know!_@_LV_bonus:_+}%_Harp_Note_Gain AijowfWE_wjioaef,_jopfweaj_waf_gtojigr_joifs!_@_LV_bonus:_+}%_omefw_jiowef".split(" "),
    ["렴련렛렘렐렌레"],
    "10 6 5 13 20 18 0".split(" "),
    "689 185 808 146 855 61 776 6 726 89 659 2 616 104 556 24 504 130 455 5 404 91 349 9".split(" "),
    "雕 雏 雇 雅 雄 难 隧 障 隐 随 陶 陵 陪 雏 难 雄".split(" "),
    "3 10 4 12 14 5 16 6 17 7 20 21 23 24 26 29".split(" "),
    "誇 詳 話 詰 試 許 訪 討 計 触 樹 横 権 旗 標 旅".split(" "),
    "3 4 6 8 1 7 2 8 3 0 9 4 2 6 7 10".split(" "),
    "GLOOMIE_KILLS CROPS_FOUND ACCOUNT_LV TOME_SCORE ALL_SKILL_LV IDK_YET DEATHNOTE_PTS HIGHEST_DMG SLAB_ITEMS STUDIES_DONE GOLEM_KILLS 7 3".split(" "),
    "+{%_VILLAGER|EXP_GAIN +{%_BRAVERY|SWORD_MAX_DMG +{%_BELL_RING|访_PING_RATE +{%_HARP|NOTE_GAIN +{%_DAILY|LAMP_WISHES +{%_BUCKET|FILL_RATE +{%_HARP|STRING_EXP +{%_VILLAGER|EXP_GAIN +{%_HARP|NOTE_GAIN +{%_MULTIKILL|PER_TIER +{%_RUPIE|VALUE +{%_MONUMENT|AFK_RATE +{%_JAR|PRODUCE_SPD +{%_GAMBIT|POINTS +{%_RUPIE|VALUE +{%_DROP|RATE".split(" "),
    "45TOT 2 10 6 80TOT 11 13 60TOT 30 40TOT 10 5TOT 30TOT 10TOT 18 50TOT".split(" "),
    "3 4 2 4 1 1 1 1 1".split(" "),
    "4 3 2 3 4 3 1 1 1 1 1 1".split(" "),
    "1 4 2 4 3 4 1 1 1 1 1 1".split(" "),
    "+{%_BUCKET|FILL_RATE 10 +{%_ALL|VILLAGER_EXP 0.5 +{%_HARP|NOTE_GAINS 10 +{%_DAILY|LAMP_WISHES 0.3 +{%_EXTRA|RUPIE_CHANCE 0.5 +{%_DOUBLE|TORCH_CHANCE 2.0".split(" "),
    "+{%_Bell_Ring/hr +{%_Bell_Clean/hr +{%_Bell_Ring/hr +{%_Bell_Ping/hr +{%_Bell_Ring/hr +{%_Bell_Ring/hr".split(" "),
    "5 10 8 13 12 15".split(" "),
    "0|Can_I_has_{_coins_pwease?|c-1.h2|h-1|ch|coincheck 1|I_got_fined_{_coins_by_YOUR_LAWS_for_using_the_5_finger_discount!_Can_you_waive_this_fine?_I_really_don't_want_to_pay_it!|h1|c2.h-1|ch|no 2|Your_honor,_I_seek_an_investment_of_{_coins_in_order_to_grow_my_Student_Loans_company_and_acquire_new_victims._I_promise_your_money_will_double_by_next_time_you_see_me.|c-3.h-1|h2|c|coincheck 2|Good_afternoon,_I_represent_a_third_party_who_would_like_to_buy_your_popularity,_yes_ALL_of_it,_for_2_coins_per_pop._Would_you_be_interested_in_this?|_|h1|_|no 0|Hewwo_OwO_can_u_tell_everyone_they_are_stinky_heads?_Also_ummmmmmmm..._are_you_skibbidy??!?|h-1|h1|h|no 4|It's_a_heart_attack._You're_currently_in_the_hospital,_you'll_make_a_full_recovery_if_you_pay_{_coins_for_the_best_cardiologist.|c-5|m-1|c|coincheck 4|You're_in_a_coma._Yea,_car_crash_on_your_way_to_the_next_court_case._You'll_recover,_but_only_if_you_pay_{_coins_to_cover_the_doctor_fees.|c-4|m-1|c|coincheck 4|Snake_attack_during_a_weekend_hike._You_really_are_quite_the_extravert!_But,_the_venom_will_cause_quite_a_lot_of_stress_if_you_don't_buy_the_cure..._last_I_checked,_it_currently_goes_for_{_coins.|c-4|m-1|c|coincheck 4|Shark_attack_during_a_weekend_hike_in_the_ocean._You_REALLY_are_quite_the_extravert._But,_without_proper_care_that_wound_is_going_to_get_a_lot_worse!_It's_gonna_be_{_coins_for_full_medicare.|c-3|m-1|c|coincheck 4|Well_that_Stream_could_have_gone_better..._you're_a_Millennial_judge,_of_course_you_stream_in_your_free_time._Look,_unless_you_give_me_{_coins_to_wipe_your_memory,_you're_going_to_feel_REALLY_bad_for_a_long_time._Like,_really_bad.|c-4|m-1|c|coincheck 4|Uhhh..._hey...?_Why_am_I_here?_You_seem_fine._But,_since_I_AM_here,_I'm_a_bit_short_on_rent._Soooo_give_me_{_coins,_or_I'll_be_taking_1_mental_health_of_yours!|c-3|m-1|c|coincheck 4|Blocked_artery._Your_spouse_rushed_you_to_the_hospital_at_quite_the_pace,_you_should_say_thanks_if_you_ever_see_them_again!_The_bill_is_looking_to_be_about_{_coins,_are_you_ready_to_pay_up?|c-4|m-1|c|coincheck 4|Someone_you_rejected_is_putting_their_plot_into_action..._yea,_like,_right_now._Don't_be_too_surprised,_you're_really_not_that_popular._You_won't_come_out_unscathed_unless_you_pay_{_coins_to_hire_a_better_Bailiff.|c-6|m-1|c|coincheck 4|No_no,_I'm_not_here_for_you._It's..._well,_it's_Little_Timmy._After_that_3rd_rejection,_he_ran_home_crying_and_won't_come_out_of_his_room._It's_gonna_cost_you_{_coins_to_make_him_feel_better,_or_you_can_just_live_with_the_guilt.|c-8|m-1|c|coincheck 4|Uh_oh,_looks_like_your_bills_finally_got_the_better_of_you!_I_guess_managing_money_ain't_so_easy_after_all._Look,_if_you_give_me_}_popularity,_I'll_save_you_the_embarassment_of_an_empty_coffer.|h-1.c1|m-1|h|popcheck 4|You're_broke...?_AGAIN???_I_even_gave_you_a_coin_myself_last_time!_Nope,_you're_not_weaseling_your_way_out_of_this_one_you_sneaky_beaky._Approve,_reject,_dismiss,_I_don't_care,_I'm_taking_some_of_your_mental_with_me.|m-1|m-1|_|no 1|Good_going_judge,_your_STUPID_laws_just_got_me_arrested!_You_HAVE_to_pay_my_bail_of_{_coins,_you_OWE_me_for_enforcing_such_dumb_rules!!!|c-3.h1|h-1|ch|coincheck 1|Here_judge,_I_brought_the_{_coins_I_owe_for_my_previous_misdemeanors._Just_shake_my_hand_first,_I_promise_I_wont_do_anything_to_damage_your_mental_health!_Hehehe...|c5.m-1|_|c|no 3|Hey_pal,_how_we_doin'?_You_lookin'_for_some_extra_cash?_I_got_{_coins_on_me,_take_em!_Don't_ask_questions,_'specially_'bout_where_I_got_'em_from.|c3.h-1|h1|ch|no 3|Hey_friendo._Is_me_again,_what's_good?_I_got_a_huge_score,_and_wanted_to_share_some_of_it!_Here,_have_{_coins,_but_your_mental_health_will_take_a_hit_when_you_hear_the_news_tonight...|c7.m-1|h1|c|no 3|Aight,_check_it._I_ain't_done_no_dirty_tricks_this_time,_I_got_a_shiny_clean_coin_right_'ere,_just_for_you!_Seriously,_take_it!|c1|h-1|_|no 5|Retirement_is_important,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_it'll_cost_you_{_coins.|r1.c-2|_|c|coincheck 5|Retirement_is_the_key_to_happiness,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_it'll_cost_you_}_popularity.|r1.h-1|_|h|popcheck 6|Oh_boy,_I'm_in_the_Justice_Monument_minigame_again!_Wanna_trade_some_of_your_coins_for_my_popularity?_Also_it's_ok_if_you_don't_have_enough_coins,_I_have_plenty_of_popularity_to_go_around!|c-2.h1|h-1|ch|no 6|Hey_it's_me,_everyone's_favorite_wiggly_piece_of_paper!_I_really_want_to_help_the_next_guy,_can_you_PROMISE_me_you'll_Approve_the_next_case?_I'll_give_you_{_coins._Please?|c3|h-1|c|no 8|I've_been_watching_you_closely,_and_I_wanted_to_thank_you_for_everything_you've_done_for_the_community_with_a_gift_of_{_coins,_and_1_Retirement_Chest!|c5.r1|m-999|_|no 7|Mmmm_yeeees,_charmed_your_honor._Perchance_could_I_get_a_loan_of_all_your_money?_I_will_give_it_all_back_next_you_see_me,_and_you_would_make_me_one_very_happy_bean_oh_hohoho_yeeees!|h12|_|_|no 7|Huzzah,_it_is_I!_Would_you_like_to_buy_a_mental_health,_perchance?_I_doooo_have_the_greatest_mind_ever_to_grace_this_court!_All_it_will_cost_you_is..._HALF_of_all_your_coins!|m1|_|_|no 7|Hark,_I_have_returned_bearing_the_gift_of_a_Retirement_Chest,_albeit_only_if_you_can_solve_my_riddle._Tell_me_magistrate..._as_I_am_royalty,_what_action_to_me_speaks_loudest,_yet_not_at_all?|h-1|h-1|_|no 7|I_have_a_deeeelightful_proposition_for_you!_Every_time_you_Approve_a_case,_I_will_give_4_coins._However,_two_rejections_and_I_will_make_you_infinitely_unpopular._Any_Case_Dismissal_will_void_this_deal.|_|_|_|no 0|Can_u_subskwibe_to_my_yootoob_channel_pwease??_Is_free!!!|h1|h-2|h|no 3|Eyo_was_up_my_guy,_I_got_a_bit_of_a_deal_for_ya._{_coins,_but_you_can't_Approve_that_Little_Timmy_fella_next_you_see_him._Whatchu_think?|c3|_|c|no 0|I_stole_my_fwends_toy,_and_he_said_I_am_under_arrest._Can_I_be_free_pwease?_I_will_give_u_{_coins..._did_I_do_bribe_right?_Daddy_teached_it_to_me_today!|c1.h-1|h1|ch|no 5|Retirement_is_everything,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_I_want_1_mental_health..._unless_you're_down_to_your_last_one,_then_you_can_have_the_chest_free.|r1|_|_|no 6|Can_I_get_a_{_coin_loan_to_buy_my_next_kitchen_in_World_4?_I_play_the_game_too_you_know!_I'll_give_you_back_the_coins_plus_interest_next_time_you_see_me,_AND_you'll_have_my_gratitude!|c-2.h1|h-1|ch|coincheck 2|Greetings,_I_come_to_you_today_seeking_a_}_popularity_investment_since_my_last_company_spilled_some,_well,_accidentally_spilled..._look,_I_am_willing_to_offer_a_LOT_of_coins!|h-1.c3|h1|hc|popcheck 2|Greetings,_I_come_to_you_today_seeking_a_{_coin_investment_in_my_time_management_company._I_guarantee_you_a_250%_return,_but_it_will_take_15_court_cases_to_mature.|c-5|h1|c|coincheck 5|Retirement_is_the_top_priority,_trust_me!_I'll_give_you_1_retirement_chest_to_get_you_going,_but_I'll_be_taking_{_coins_and_}_popularity_whether_you_have_them_or_not!|r1.c-2.h-1|_|ch|no 3|Ok_dog_hear_me_out,_I_had_this_dope_idea_while_I_was_drying_out_yesterday..._a_reverse_bribe!_You_give_me_{_coins,_and_I'll_boost_your_popularity|c-1.h1|_|ch|coincheck 5|Retirement_is_the_number_one_source_of_all_things_good,_trust_me!_I'll_give_you_1_retirement_chest_completely_free_just_to_show_you_how_right_I_am!|r1|_|_|no 9|Sup._Heads_you_win_a_bunch_of_coins,_Tails_you_lose_some_coins._You_wanna_flip_for_it?|c3|_|c|no 9|Sup._Heads_you_dope_as_heck,_Tails_you_fail_the_vibe_check._You_wanna_flip_for_it?|h2|_|h|no 9|Sup._Heads_you_win_2_Retirement_Chests,_Tails_you_lose_1_Retirement_Chest._You_wanna_flip_for_it?|r2|_|_|no 2|Greetings,_I_have_a_fantastic_opportunity_for_you!_For_just_{_coins,_I_will_invest_in_a_crypto_coin_and_will_share_the_profits!_1_coin_returned_every_day_for_15_days!|c-6.h-1|h1|_|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.r1|h-1|c|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.h3|_|hc|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.m1|h-1|c|coincheck 12|Me_like_coin._Me_collect_coin!_You_give_me_{_coin,_I_give_you_random_gift!|c-1.h2|_|c|coincheck 0|Can_u_make_today_a_holiday_so_school_is_no?|c-3.h2|_|ch|no 10|Eat_me_eat_me_eat_me!|h1|h-1|h|no 11|Can_you_make_it_legal_for_me_to_scare_people?_I'll_pay_you_handsomely,_but_I'll_keep_scaring_1_person_every_day,_FOooOooOREVER...|c6|h1|c|no 1|You_look_richer_than_the_guy_I_just_stole_from._Give_me_one_of_your_retirement_chests,_and_I'll_tell_all_the_other_Reanimated_Limbs_back_home_what_a_legend_you_are!|r-1.h4|h-1|h|chestcheck 5|Retirement_is_worth_considering,_trust_me_I'd_know!_I'll_give_you_1_retirement_chest,_but_it'll_cost_you_{_coins.|r1.c-3|_|c|coincheck 2|Good_afternoon,_I_am_seeking_invesetment_in_my_new_Retirement_Hedgefund!_For_just_1_Retirement_Chest,_you_will_receive_royalties_of_2_coins_per_day_for_10_days!|r-1|h1|_|chestcheck 9|Sup._Heads_you_the_man_and_get_2_mental_health,_Tails_you_crazy_and_lose_1_mental_health._You_wanna_flip_for_it?|m2|_|_|no 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_around_I_grant_the_consumer_some_sort_of_Chest_Magnetizer_effect,_lasts_for_3_days_I_reckon...|c-1|_|c|coincheck 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_'round_I_grant_the_consumer_a_LOT_of_pop!|c-1.h1|_|ch|coincheck 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_'round_I_grant_the_consumer_2_dismissals,_but_I_am_known_in_the_state_of_Blunder_Hills_to_cause_mental_fatigue!|c-1.d2.m-1|_|c|coincheck 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_'round_I_grant_the_consumer_a_strange_ability_to_never_ever_become_unpopular!_Like,_ever!|c-1|_|c|coincheck 11|I'm_done_scaring_people..._I_thought_it_was_funny_for_a_while,_but_now_I_just_feel_bad._Can_you_reinstate_the_ban,_make_it_illegal_again?_I'll_pay_you!|c4.h1|_|c|no 13|I'm_not_a_free_drink,_{_coin_please!_My_effects?_Well,_this_time_I'm_just_a_normal_drink,_but_there's_a_1_in_4_chance_I'm_the_limited_edition_glass_all_the_internet_nerds_want_to_buy!|c-1|_|c|coincheck 7|Ohohoho_I_have_heard_the_stories_about_you_judge!_Oh_yes_indeed!_Gulp_gulp_gulp,_say_no_more!_Shall_we_keep_this_a_secret_between_us?_Oh_how_I_do_LOVE_secrets!|h2|h-4|h|no 1|You_are_SO_dumb,_forcing_me_here_whenever_I_break_your_dumb_rules._Can_you_just_make_me_above_the_law?_I'll_share_part_what_I_steal_every_time_you_see_me,_I'll_even_share_the_blame!|h-1|h2|_|no 3|Hey_buddy,_how's_the_grind_going?_Look,_I_got_{_coins_on_me,_and_you_can_have_them_all!!!_Only_thing_is,_for_3_days_you_won't_be_able_to_Approve_anything...|c7|_|c|no".split(" "),
    "Little_Timmy Reainmated_Hand Head_Honcho_of_Big_Biz_LLC Mister_Bribe The_Harbinger Retirement_Chester Scripticus Esquire_Bored_Bean The_Gratefulbinger Cool_Bird Chippy Ghost Grumblo Fizarre_Drink".split(" "),
    "21 14 8 3 3 3 3 0".split(" "),
    "Contains_a_random_basic_rupie Has_a_{%_chance_to_contain_an_Opal Has_a_{%_chance_to_contain_a_new_collectible Contains_a_random_decent_rupie Has_a_{%_chance_to_enchant_a_collectible_doubling_its_bonus Contains_a_white_rupee Contains_a_random_elegant_rupie Doubles_the_amount_of_rupies_from_the_next_jar_opened Contains_a_dark_rupie Contains_the_one_and_only_master_rupie".split(" "),
    "7 3 20 17 22 11 14 5 17 13".split(" "),
    "ABNORMAL_RUPIE|20|Filler|Rupies_found_are_worth_+{%_more._@_Current_Rupie_Value:$ SAPPHIRE_DROPLET|10|Filler|Jar_production_rate_is_+{%_faster. EFFERVESCENT_DIAMOND|20|Filler|}x_higher_chance_to_find_Opals_in_Tall_Jars. TORTOLE_ROCK|25|Filler|All_rupies_found_are_worth_a_whopping_}x_more! NATURAL_PEARL|15|Filler|All_villagers_gain_+{%_more_EXP. AMETHYST_HEARTSTONE|10|Filler|All_skilling_caverns_require_{%_less_Resources_to_get_opals! AMBER_SQUARE|25|Filler|Rupies_found_are_worth_+{%_more. VERDANT_THORNS|25|Filler|}x_higher_chance_to_find_new_Collectibles. VIOLENT_VIOLETS|20|Filler|All_buckets_get_}x_Bucket_Fill_Rate! BLUE_FABERGE_EGG|15|Filler|}x_higher_chance_to_enchant_a_Collectible SHADOW_PRISM|20|Filler|All_villagers_gain_+{%_more_EXP. BIG_BEEF_ROCK|25|Filler|}x_faster_Bell_Ring_Rate! EMERALD_ORE|30|Filler|All_villagers_gain_+{%_more_EXP. DAWN_PRISM|30|Filler|Rupies_found_are_worth_+{%_more. SWAMPSTONE|25|Filler|}x_higher_chance_to_find_Opals_in_Tall_Jars. FROST_SPIRESTONE|12|Filler|Jar_production_rate_is_+{%_faster. ROSEMERALD|10|Filler|}x_Faster_study_rate_for_villager_Bolaia BLOOD_GLASS|40|Filler|All_rupies_found_are_worth_a_whopping_}x_more! SUNRISE_DIAMOND|25|Filler|}x_higher_chance_to_enchant_a_Collectible MINCERAFT_GEM|20|Filler|+{%_Monument_AFK_Gain_rate. CRIMSON_SPADE|20|Filler|The_harp_produces_}x_more_Notes! STAINED_GLASSDROP|35|Filler|Rupies_found_are_worth_+{%_more. TABULA_RASASTONE|32|Filler|All_villagers_gain_+{%_more_EXP. DEEP_BLUE_SQUARE|1|Filler|+{%_Gambit_PTS EARTHBOUND_GEODE|15|Filler|Jar_production_rate_is_+{%_faster. INFERNO_DROPLET|40|Filler|}x_higher_chance_to_find_new_Collectibles. OCTOGONAL_GEM|30|Filler|}x_higher_chance_to_enchant_a_Collectible SOLARFANG|32|Filler|}x_higher_chance_to_find_Opals_in_Tall_Jars. MYSTIC_ORE|50|Filler|All_rupies_found_are_worth_a_whopping_}x_more! ARCANE_PRISM|38|Filler|All_villagers_gain_+{%_more_EXP. MURKY_FABREGE_EGG|1|Filler|+{%_Gambit_PTS CORPORE_ROCK|1|Filler|Boosts_a_future_cavern..._futuuure..! TWILIGHT_PRISM|1|Filler|Boosts_a_future_cavern..._futuuure..! TEWBALL_ORBSTONE|40|Filler|Rupies_found_are_worth_+{%_more. MAD_MUSCLE_ROCK|40|Filler|}x_higher_chance_to_enchant_a_Collectible SUNROOT_SPLINTERS|40|Filler|All_villagers_gain_+{%_more_EXP. TWISTED_RUPIE|75|Filler|}x_faster_Bell_Ring_Rate! OVERLOADED_RELIC|1|Filler|Boosts_a_future_cavern..._futuuure..! SUNBURST_PEARL|1|Filler|Boosts_a_future_cavern..._futuuure..! BLOODFANG_SPIRES|1|Filler|Boosts_a_future_cavern..._futuuure..!".split(" "),
    "THE_WELL MOTHERLODE THE_DEN BRAVERY THE_BELL THE_HARP THE_LAMP THE_HIVE GROTTO JUSTICE THE_JARS EVERTREE WISDOM GAMBIT TEMPLE".split(" "),
    "You_only_lose_25%_sediment_when_bar_expanding_instead_of_50%_Also,_+{%_Bucket_Fill_Rate_per_Bar_Expansion Every_layer_destroyed_lowers_the_resources_needed_to_destroy_other_skilling_caverns_by_{% Defeating_the_Golden_Hound_gives_a_}x_score_multi_and_spawns_another_Golden_Hound! Minimum_DMG_is_at_least_{%_of_Max,_and_you_now_skip_trivial_fights! Every_20th_Bell_Ring_gives_a_random_bonus_+{_LVs._Biiig_Ring_baby! All_strings_give_2x_EXP,_and_have_a_1%_chance_of_getting_a_massive_{x_EXP_multi Get_{_more_lamp_wishes_every_day._No,_you_can't_wish_to_change_this! Every_hive_harvested_lowers_the_resources_needed_to_destroy_other_skilling_caverns_by_{% Each_Gloomie_kill_counts_for_}x_more_toward_challenging_the_Monarch Justice_Reward_Multi_goes_up_100%_every_day_for_+14_more_days!_Also,_}x_chance_for_opal_reward! Double_click_to_choose_a_collectible_to_be_most_likely_enchanted!_Also,_}x_Enchantment_Chance! Every_trunk_whittled_lowers_the_resources_needed_to_destroy_other_skilling_caverns_by_{% If_you_end_a_round_with_no_instamatches,_you_get_one!_Also,_start_with_{_more_attempts! +{%_Total_Gambit_Points._Also,_50%_chance_to_not_use_up_your_daily_Gambit_attempt_when_starting_a_Gambit! There_is_an_extra_+{%_chance_to_get_double_torches_when_picking_them_up!".split(" "),
    "10 2 5 3 20 100 1 5 1 50 25 5 1 5 30".split(" "),
    "1|1|Press_the_star_button_in_a_summoning_upgrade_to_DOUBLE_it!_Get_more_Gambit_Points_to_get_more_doublers!_You_have_$_left,_and_can_reset_them_at_The_Lamp|{_Summoning_Doublers_梦(TAP_ME) 1|1|You_know_how_POW_10_works!_You'll_get_an_opal_at_10_total_score,_then_100,_then_1000,_then_10000,_etc...|1_Opal_per_POW_10_Points_梦 20|0|For_example,_having_a_party_of_4_people_would_give_1.80x_Flurbo_Gain_bonus|+{%_Flurbos_per_party_member_梦 25|1|This_bonus_INCREASES_the_more_Gambit_Points_you_have!|+{%_Resources_from_Caverns_梦 20|0|no|+{%_Upgrade_Stone_Success 25|1|This_bonus_INCREASES_the_more_Gambit_Points_you_have!|}_Essence_Gain_梦 35|0|For_example,_if_you_combined_two_T8_ribbons,_theres_a_35%_chance_for_a_T10_instead_of_T9.|{%_chance_for_2而_ribbon_combine_梦 10|1|This_bonus_INCREASES_the_more_Gambit_Points_you_have!|}_Coins_from_monsters_梦 100|1|This_includes_Owl_Feathers_and_Roo_Fish._Also,_this_bonus_INCREASES_the_more_Gambit_Points_you_have!|}_gains_from_clickers_梦 1|0|Trim_Slot_means_the_gold_Trimmed_Construction_slot,_and_Wiz_means_Wizard_Towers_in_Construction.|+1_Trim_Slot_and_+100_Wiz_Max_LV_梦 1|0|no|2而_extra_Snail_Mail_every_day 25|1|This_bonus_INCREASES_the_more_Gambit_Points_you_have!|}_Ninja_Stealth_梦 1|0|no|2而_Extra_Bones_on_Deathbringer 1|0|no|2而_daily_particle_bubble_upg 1|0|no|World_7_bonus..._what_will_it_be...? 1|0|no|World_7_bonus..._what_will_it_be...? 1|0|no|World_7_bonus..._what_will_it_be...? 1|0|no|World_7_bonus..._what_will_it_be...? 1|0|no|World_8_bonus..._what_will_it_be...?".split(" "),
    "15 16 17 26 27 28 14 18 25 29 37 39 24 30 8 19 2 13 4 6 5 38 23 35 31 41 36 40 3 7 12 20 1 9 34 42 11 21 22 32 0 10 33 43".split(" "),
    "15 16 17 26 27 28 25 29 14 18 5 38 4 6 37 39 13 19 24 30 3 7 36 40 12 20 23 31 2 8 35 41 1 9 34 42 11 21 22 32 0 10 33 43".split(" "),
    "13 14 15 16 17 18 19 27 4 6 26 28 12 20 3 7 24 25 29 30 5 38 11 21 2 8 1 9 36 40 23 31 22 32 37 39 35 41 0 10 34 42 33 43".split(" ")
]
caverns_cavern_names = {
    0: 'Camp',
    1: 'The Well',
    2: 'Motherlode',
    3: 'The Den',
    4: 'Bravery Monument',
    5: 'The Bell',
    6: 'The Harp',
    7: 'The Lamp',
    8: 'The Hive',
    9: 'Grotto',
    10: 'Justice Monument',
    11: 'The Jar',
    12: 'Evertree',
    13: 'Wisdom Monument',
    14: 'Gambit',
    15: 'The Temple'
}
max_cavern = max(caverns_cavern_names.keys())
caverns_villagers = [
    {'Name': 'Polonai', 'Role': 'The Explorer', 'VillagerNumber': 1, 'UnlockedAtCavern': 0},
    {'Name': 'Kaipu', 'Role': 'The Engineer',   'VillagerNumber': 2, 'UnlockedAtCavern': 2},  #Motherlode
    {'Name': 'Cosmos', 'Role': 'The Conjuror',  'VillagerNumber': 3, 'UnlockedAtCavern': 5},  #The Bell
    {'Name': 'Minau', 'Role': 'The Measurer',   'VillagerNumber': 4, 'UnlockedAtCavern': 7},  #The Lamp
    {'Name': 'Bolaia', 'Role': 'The Librarian', 'VillagerNumber': 5, 'UnlockedAtCavern': 12},  #Evertree
]
#Schematics stored in HolesBuildings function in source code, last confirmed as of v2.31
caverns_engineer_schematics = ["Opal_Dividends 0 0 6 1 Each_opal_invested_in_a_villager_now_gives_them_125_EXP/hr,_instead_of_100_EXP/hr_@_Also_worry_not,_you_can_reset_your_opals_later_at_Cavern_7".split(" "), "Better_Buckets 1 0 8 1 Increases_the_base_fill_rate_of_all_Well_Buckets_from_10/hr_to_15/hr._IMPORTANT:You_can_click_on_the_buckets_for_more_info!".split(" "), "Cavern_'Porting 0 0 60 1 All_teleports_to_this_map_are_free!_Also,_did_you_know_you_can_double-click_a_map_instead_of_pressing_the_Teleport_button?".split(" "), "2nd_Bucket! 1 0 130 1 Adds_another_bucket_at_the_Well!_You'll_need_to_expand_your_Gravel_bar_to_hold_the_130_needed_to_create_this!".split(" "), "3rd_Bucket! 1 1 850 1 Adds_another_bucket_at_the_Well!_Remember,_click_a_bucket_to_change_what_sediment_it_collects!_That's_how_you_get_this_gold_resource!".split(" "), "4th_Bucket! 1 2 3000 f Adds_yet_another_bucket_at_the_Well!".split(" "), "Five_Nights_at_Bucket 1 2 12500 f Adds_one_more_bucket_at_the_Well!_Five_buckets!!!_WOW!_That's_worth_writing_home_about!".split(" "), "6th_Bucket! 1 3 75000 f Adds_another_bucket_at_the_Well!_I_guess_5_wasn't_enough_for_a_go_getter_like_yourself!".split(" "), "7rth_Barckot?! 1 4 1 f Adds_another_bucket_at_the_Well!_You_DO_want_more_buckets,_right?".split(" "), "Last_Bucket! 1 5 1 f Adds_another_bucket_at_the_Well!_And_it's_the_last_one_too,_I_hope_your_bucket_lust_is_satiated!".split(" "), "9th_Bucket! 1 6 1 f Adds_another_bucket_at_the_Well!_Yea_apparently_there_were_a_few_more_of_these_left!".split(" "), "Bucket_Finale! 1 7 1 f Adds_another_bucket_at_the_Well!_And_yea_this_one_is_actually_the_last_one,_I_don't_think_an_11th_would_fit_on_screen!".split(" "), "Bar_Expand-o-rama 1 0 100 1 Adds_the_'Expand_Full_Bars'_toggle_to_the_Well!_Let_me_explain..._when_a_bar_is_full_of_sediment,_you_lose_half_of_the_sediment,_but_permanently_increase_the_max_by_1.50x!".split(" "), "UBER_Bar_Expand-o-rama-hala 1 0 28000 1 Allow_for_UBER_Full_Bar_Expansion,_which_means_you_can_expand_Well_Bars_beyond_the_previous_limit_of_14_times.".split(" "), "Expander_Extravaganza 1 1 350 1 Gives_all_your_buckets_+20%_Fill_Rate_per_bar_expansion_across_all_sediment_types!_This_includes_Uber_expansions_later!_@_Total_Bonus:_+{%".split(" "), "Motherlode_~_Bucket_Synergy 1 0 180 1 Gives_all_your_buckets_1.10x_fill_rate_per_Motherlode_Layer_you've_destroyed!_@_Total_Bonus:_{x".split(" "), "Green_Amplifier 1 1 250 1 Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Pink_Amplifier 1 2 3250 1 Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Yellow_Amplifier 1 0 10000 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Cyan_Amplifier 1 3 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Purple_Amplifier 1 13 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "White_Amplifier 1 6 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Dark_Amplifier 1 18 10 f Adds_a_new_Amplifier_stone_to_interact_with_at_the_Dawg_Den!".split(" "), "Amplifier_Stackin' 1 2 10 f You_now_get_an_additional_+0.50x_Multiplier_at_the_Dawg_Den_for_every_10_total_charge_across_all_amplifiers!".split(" "), "The_Story_Changes_Over_Time... 1 1 600 1 Bravery_Swords_get_+1_minimum_DMG_and_+10_maximum_DMG_per_6_HR_of_AFK_time_at_the_Bravery_Monument!".split(" "), "First_Try,_I_swear! 1 0 10 f If_you_throw_the_LAST_bravery_sword_first,_and_it_kills_the_monster,_you_get_a_+10%_Sword_Max_DMG_bonus_for_the_rest_of_the_story._If_it_doesn't_kill,_this_bonus_resets_back_to_0%".split(" "), "Even_Better_Buckets 1 1 25 f Increases_the_base_fill_rate_of_all_Well_Buckets_from_15/hr_to_20/hr._Try_changing_your_bucket_to_remove_the_rocks,_once_you_remove_that_layer_you_can_collect_gold_dust!".split(" "), "Eee_String 2 10 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_by_plucking_it,_getting_+1_EXP_per_100%_Harp_Power!".split(" "), "Eff_String 2 12 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_by_plucking_it,_getting_+1_EXP_per_100%_Harp_Power!".split(" "), "Geez_String 2 14 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_just_like_any_other_string,_getting_+1_EXP_per_100%_Harp_Power!".split(" "), "Aye_String 2 16 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_just_like_any_other_string!".split(" "), "Bee_String 2 18 10 f Permanently_unlocks_a_new_String_Type_for_the_Harp!_You_can_level_it_up_just_like_any_other_string!".split(" "), "Loaded_Harp 2 10 10 f Adds_+1_more_string_to_the_Harp,_ready_to_be_strummed_until_the_end_of_(the)_time_(signature)!".split(" "), "Packed_Harp 2 11 10 f Adds_+1_more_string_to_the_Harp,_you'll_find_it_right_next_to_all_your_other_strings!".split(" "), "Hefty_Harp 2 13 10 f Adds_+1_more_string_to_the_Harp,_it_even_makes_sound_when_strummed!_The_other_ones_do_too,_but_like,_this_one_does_too!_Just_incase_you_were_worried_it_wouldn't.".split(" "), "Multitudinal_Harp 2 15 10 f Adds_+9999_more_strings_to_the_Harp!_Haha_nah_just_+1_string,_figured_I'd_keep_you_on_your_toes!_If_I_tricked_you,_you_must_go_pluck_the_F_string.".split(" "), "Sumptuous_Harp 2 17 10 f Adds_+1_more_string_to_the_Harp..._all_these_strings_really_remind_me_of_string_cheese,_I_used_to_love_it!".split(" "), "Domino_Effect 2 4 10 f Strings_give_+20%_more_per_string_plucked_during_a_strum..._let_me_explain._Imagine_you_have_5_strings,_this_would_mean_the_final_string_you_pluck_would_be_worth_DOUBLE!".split(" "), "Variety_Effect 2 6 10 f Strings_give_+30%_more_for_each_unique_string_type_on_your_harp..._I_see_you_currently_have_$_different_strings_on_your_harp,_so_your_strings_are_all_worth_#%_more!".split(" "), "Stringy_Effect 2 3 10 f Strings_give_+15%_more._@_More_what,_you_ask?_More_everything!_They_give_more_String_EXP,_more_notes,_higher_chance_for_opal..._so_yea,_MORE!".split(" "), "Reroll_Keeper 1 5 10 f Each_unused_reroll_you_have_in_a_Bravery_Story_gives_+10%_Sword_Max_DMG._So_don't_be_all_loosey_goosey_with_those_rerolls!".split(" "), "Fractalfly_~_Harp_Synergy 2 13 10 f Boosts_your_Harp_Note_production_by_1.10x_per_Undying_Hive_Layer_you've_destroyed!_@_Total_Bonus:_{x".split(" "), "Double_Dinger_Ringer 1 3 10 f Ringing_the_Bell_now_has_a_+30%_chance_of_giving_+2_LV_to_a_bonus,_instead_of_just_+1_LV".split(" "), "RNG_Oxidizing_Layer 1 4 10 f When_you_Clean_the_Bell_and_FAIL_to_get_a_new_Improvement_Method,_the_success_chance_for_next_time_goes_up_by_1.25x._This_happens_every_fail,_and_resets_when_you_finally_succeed!".split(" "), "Gloomie_Mulch 0 14 10 f Gloomie_mushrooms_respawn_+10%_faster!_In_fact,_ALL_monsters_across_all_the_worlds_of_IdleOn_respawn_+10%_faster!".split(" "), "Improvement_Stackin' 1 12 10 f For_every_25_LVs_across_all_Improvement_Methods_upgrades_at_the_Bell,_all_your_Improvement_Method_bonuses_are_1.10x_higher!_@_Total_bonus:_}x".split(" "), "Gloomie_Lootie 0 6 10 f +5%_Drop_Rate_for_each_Colony_of_Gloomie_Mushrooms_defeated!_Drop_rate_here_as_in_like,_the_one_for_stuff_outside_of_the_Caverns._@_Total_Bonus:_+{%".split(" "), "Gloomie_Expie 0 15 10 f +25%_Class_EXP_gain_for_each_Colony_of_Gloomie_Mushrooms_defeated!_@_Total_Bonus:_+{%".split(" "), "Gloomie_Opie 0 16 10 f +10%_Villager_EXP_gain_for_each_Colony_of_Gloomie_Mushrooms_successfully_romanced..._or_defeated,_whichever_is_higher._@_Total_Bonus:_+{%".split(" "), "Motherlode_Trickledown 0 3 10 f +15%_All_Skill_Efficiency,_and_+10%_All_Skill_EXP_gain_per_Motherlode_Layer_you've_destroyed!".split(" "), "Fractalfly_Trickledown 0 15 10 f +15%_All_Skill_Efficiency,_and_+10%_All_Skill_EXP_gain_per_Undying_Hive_Layer_you've_destroyed!".split(" "), "Rift_Guy 3 0 10 f Hey_bet_you_weren't_expecting_to_see_me_here,_huh?_Well,_that's_just_how_it_goes_with_me,_it's_in_my_blood._It's_how_I_roll._Go_ahead,_create_me._Or_don't,_I'll_keep_being_me.".split(" "), "DNA_Rock_Tumbler 0 0 10 f Gives_you_a_+60%_chance_to_get_an_additional_Grey_Gene_when_trashing_a_pet_for_every_Power_of_10_Gravel_you_have._@_Total_Bonus:_+{%_Chance_for_extra_Gene".split(" "), "Final_Ballad_of_the_Snail 0 13 10 f Gives_you_a_1.04x_higher_success_chance_when_leveling_up_Snail_for_every_Power_of_10_Trebel_Notes_you_have._@_Total_Bonus:_{x_Snail_success_chance".split(" "), "Noise_Reduction_Therapy 0 15 10 f Gives_you_a_multiplicative_1.20x_Stealth_bonus_for_all_ninjas_for_every_Power_of_10_Quaver_Notes_you_have._@_Total_Bonus:_{x_Stealth".split(" "), "Tune_of_Artifaction 0 11 10 f Gives_you_+10%_Artifact_Find_Chance_for_every_Power_of_10_Natural_Notes_you_have._@_Total_Bonus:_+{%_Artifact_Find_Chance".split(" "), "Heavy_Redstone_Seasoning 0 2 10 f Gives_you_a_multiplicative_1.30x_Cooking_Speed_bonus_for_every_Power_of_10_Redstone_you_have._@_Total_Bonus:_{x_Cooking_Speed".split(" "), "True_Golden_Edge 0 1 10 f Gives_all_your_players_+20%_Damage_for_every_Power_of_10_Golddust_you_have._@_Total_Bonus:_+{%_Damage".split(" "), "Loadin'_some_'Lode 1 0 12 1 Gives_+5_Bucket_Fill_Rate_per_Power_of_10_Motherlode_Ore_mined._You_have_mined_#_so_far!_@_Total_Bonus:_+{/hr_Bucket_Fill_Rate".split(" "), "Hiring_the_Hounds_from_Beyond 1 0 30 1 Gives_+10_B.F.R._per_100_hounds_defeated_in_best_runs_of_each_class._尬__Beginner:!,_Warrior:#,_Archer:$,_Mage:%_@_Total_Bonus:_+{/hr_Bucket_Fill_Rate".split(" "), "Triple_Tap_Tinkle 1 6 10 f Ringing_the_Bell_now_has_another_+30%_chance_of_giving_+2_LV_to_a_bonus_instead_of_just_+1_LV._Also,_there's_a_new_+20%_chance_of_giving_+3_LV_instead_of_+2_or_+1!".split(" "), "Compound_Interest 2 12 600 f You_start_with_+1_more_Court_Coins_every_Power_of_2_HRs_of_AFK_time_at_the_Justice_Monument!_So_2Hrs_you_get_+1_coin,_4Hrs_you_get_+2_coins,_8Hrs_you_get_+3_coins,_and_so_on!".split(" "), "Big_Jar_Mach_II 3 20 10 1 Upgrades_the_main_jar,_doubling_the_base_value_of_every_rupie_you_find._So_if_you_see_2_red_rupies,_you_actually_got_4!".split(" "), "Big_Jar_Mach_III 3 21 10 f Upgrades_the_main_jar,_allowing_you_to_produce_2_jar_types_at_once!".split(" "), "Big_Jar_Mach_IV 3 22 10 f Upgrades_the_main_jar,_increasing_the_chance_for_multiple_rupies_in_a_jar_by_+50%".split(" "), "Big_Jar_Mach_V 3 24 10 f Upgrades_the_main_jar,_doubling_the_base_value_of_every_rupie_you_find_AGAIN!_If_2_red_rupies_gave_you_4_before,_now_it's_8!!!".split(" "), "Big_Jar_Mach_VI 3 25 10 f Upgrades_the_main_jar,_allowing_you_to_produce_3_jar_types_at_once!".split(" "), "Big_Jar_Mach_VII 3 27 10 f Upgrades_the_main_jar,_reducing_the_production_amount_required_to_make_jars_by_30%_so_you_can_make_them_faster!".split(" "), "Big_Jar_Mach_VIII 3 29 10 f Upgrades_the_main_jar,_doubling_the_base_value_of_every_rupie_you_find!_This_does_not_stack_with_the_other_ones..._just_kidding_it_totally_does!_ANOTHER_2x_RUPIES!!!".split(" "), "Break_All_Button 3 21 200 1 Adds_a_new_button_to_the_top_left_of_the_Jar,_allowing_you_to_break_all_jars_at_once!".split(" "), "Max_Monument_Rewards 1 24 10 f Monument_Reward_Multi_now_increases_at_the_normal_rate_of_+100%_daily_for_4_full_days!_Before_this_upgrade,_it_was_only_2_days...".split(" "), "Supergiant_Jars 3 20 25 1 Jars_now_COMBINE_to_save_space!_10_Jars_becomes_1_large_jar,_which_gives_10x_rewards._10_large_jars_become_1_giant_jar,_which_gives_100x_rewards._This_continues_forever!".split(" "), "Light_Speed 3 25 10 f Every_POW_10_white_rupies_you_own_increases_the_production_rate_of_jars_by_+10%_@_Total_Bonus:_+{%_Jar_Producton_Rate".split(" "), "Dark_Luck 3 27 10 f Every_POW_10_dark_rupies_you_own_increases_the_chance_of_enchanting_collectibles_from_the_Enchanted_Jar_by_1.10x_@_Total_Bonus:_{x_Enchantment".split(" "), "Jar_Production_Line 3 22 10 f The_requirement_to_make_a_jar_is_5%_lower_per_POW_10_jars_made_of_the_previous_type._For_example,_making_100_Simple_Jars_would_mean_Tall_jars_are_10%_quicker_to_make!".split(" "), "Advanced_Collection 3 28 10 f You_can_now_find_new_collectible_types_from_jars,_found_in_the_new_2nd_page_of_your_collection!_Go_collect_'em_all!".split(" "), "Collect_'Em_All 3 23 10 f Gives_a_1.02x_chance_to_find_a_new_collectible_for_every_digit_of_all_the_rupies_you_own._@_Total_Bonus:_{x_Collectible_Chance".split(" "), "Roaring_Flame 3 26 10 f +25%_chance_to_get_DOUBLE_the_Torches_from_Ancient_Golems_when_picking_them_up!".split(" "), "The_Sicilian 3 25 10 f +10%_Total_Gambit_Score".split(" "), "Evertree_Trickledown 3 20 400 1 +15%_All_Skill_Efficiency,_and_+10%_All_Skill_EXP_gain_per_Evertree_Trunk_you've_whittled!".split(" "), "Evertree_~_Rupie_Synergy 3 20 100 1 Boosts_overall_Rupie_value_by_1.10x_per_Evertree_Trunk_you've_whittled!_@_Total_Bonus:_{x".split(" "), "Rock_Smart 3 23 10 f Hmm..._let_me_think_about_this_some_more..._for_now,_I_will_give_you_+20%_Monument_AFK_gain...".split(" "), "Sanctum_of_LOOT 3 27 10 f +20%_Drop_Rate_for_each_Sanctum_of_Ancient_Golems_you've_cleared!_@_Total_Bonus:_+{%".split(" "), "Sanctum_of_EXP 3 28 10 f +40%_Class_EXP_for_each_Sanctum_of_Ancient_Golems_you've_cleared!_@_Total_Bonus:_+{%".split(" "), "Sanctum_of_DMG 3 29 10 f +100%_Total_Damage_for_each_Sanctum_of_Ancient_Golems_you've_cleared!_@_Total_Bonus:_+{%".split(" "), "Peer_Reviewed_Books 3 21 10 f Bolaia_now_get_+7%_Study_Rate_per_LV,_instead_of_the_previous_+5%_per_LV!".split(" "), "All_This_Ringing_in_my_Ears 3 25 10 f When_Ringing_the_Bell,_there_is_now_a_25%_chance_to_get_2x_more_LVs_than_you_otherwise_would_have_gotten!".split(" "), "Cutting_Edge_Research 3 24 10 f Bolaia_now_get_a_massive_+10%_Study_Rate_per_LV,_instead_of_the_previous_+7%_per_LV!".split(" "), "Billion_Dollar_Grant 3 29 1000000000 1 Bolaia_now_get_a_sumptuous_+15%_Study_Rate_per_LV,_instead_of_the_previous_+10%_per_LV!".split(" "), "Horsey_Gambit 3 22 10 f Unlocks_the_Horsey_challenge_in_the_Gambit_cavern.".split(" "), "Bishop_Gambit 3 24 10 f Unlocks_the_Bishop_challenge_in_the_Gambit_cavern.".split(" "), "Queen_Gambit 3 20 10 f Unlocks_the_Queen_challenge_in_the_Gambit_cavern.".split(" "), "Castle_Gambit 3 21 10 f Unlocks_the_Castle_challenge_in_the_Gambit_cavern.".split(" "), "Noob_Gambit 3 27 10 f Unlocks_the_Noob_challenge_in_the_Gambit_cavern.".split(" "), "NameNameName 3 24 10 f desc".split(" "), "NameNameName 3 24 10 f desc".split(" "), "NameNameName 3 24 10 f desc".split(" "), "NameNameName 3 24 10 f desc".split(" "), "NameNameName 3 24 10 f desc".split(" "), "NameNameName 3 24 10 f desc".split(" ")]
caverns_engineer_schematics_unlock_order = [int(entry) for entry in HolesInfo[40]]
max_schematics = len(caverns_engineer_schematics)
released_schematics = 93  #Last confirmed as of v2.32 in n._customBlock_Holes when e == "SchematicsAvailable"
schematics_unlocking_buckets = ['2nd Bucket!', '3rd Bucket!', '4th Bucket!', 'Five Nights at Bucket', '6th Bucket!', '7rth Barckot?!', 'Last Bucket!', '9th Bucket!', 'Bucket Finale!']
schematics_unlocking_amplifiers = {
    'Bigger Bite': ['Hounds have higher base attack', '', 'den-amplifier-0'],
    'Elusive Instinct': ['Hounds require additional Accuracy', 'Green Amplifier', 'den-amplifier-1'],
    'Canine Recovery': ['Hounds regenerate HP', 'Pink Amplifier', 'den-amplifier-2'],
    'Bigger Bow Wow': ['Chance to spawn BIG Hounds with additional HP and DMG', 'Yellow Amplifier', 'den-amplifier-3'],
    'Doggo EMP Effect': ["Player's attacks cost higher MP", 'Cyan Amplifier', 'den-amplifier-4'],
    'Cursed Howl': ['Hounds have a chance to cause more Fear', 'Purple Amplifier', 'den-amplifier-5'],
    'Den Despair': ['Fear bar starts partially filled', 'White Amplifier', 'den-amplifier-6'],
    'Fast and Deadly': ['Hounds cause Fear faster', 'Dark Amplifier', 'den-amplifier-7'],
}
schematics_unlocking_harp_strings = ['Loaded Harp', 'Packed Harp', 'Hefty Harp', 'Multitudinal Harp', 'Sumptuous Harp']
schematics_unlocking_harp_chords = ['Eee String', 'Eff String', 'Geez String', 'Aye String', 'Bee String']
max_buckets = 1 + len(schematics_unlocking_buckets)
sediment_names = ['Gravel', 'Goldust', 'Redstone', 'Mythril', 'Cobaltine', 'Brunite', 'Freezium', 'Sweetium', 'Rad Coral', 'Hyper Coral']
sediment_bars = [int(float(v)) for v in HolesInfo[21]]
max_sediments = len(sediment_names)

#Majiks stored partially in CosmoUpgrades in source code
#["25", "0", "Monumental_Vibes", "All_of_your_Monument_Bonuses_are_}x_higher!_9_out_of_10_monument_enjoyers_recommend_this_bonus!"]
#[0] = BonusPerLevel, [2] = Description. Idk where to get the scaling types and max levels, those are manual work.
#Scaling 'value' means additive with itself (a * level), then convert to multi
#Scaling 'multi' means multi with self (a ^ level), then convert to multi
#Scaling 'add' means additive with itself, leave it as that value
caverns_conjuror_majiks = {
    "Hole": [
        {'Name': 'Monumental Vibes', 'BonusPerLevel': 25, 'MaxLevel': 4, 'Scaling': 'value', 'Description': 'x stronger Monument Bonuses'},
        {'Name': 'String is Strung', 'BonusPerLevel': 1, 'MaxLevel': 5, 'Scaling': 'add', 'Description': ' more Harp strings'},
        {'Name': 'Wishy Washy', 'BonusPerLevel': 30, 'MaxLevel': 3, 'Scaling': 'add', 'Description': '% chance for additional Lamp wishes'},
        {'Name': 'Rupies Everywhere', 'BonusPerLevel': 35, 'MaxLevel': 5, 'Scaling': 'add', 'Description': '% chance for Jars to have multiple Rupees'},
        {'Name': 'Hole Placeholder', 'BonusPerLevel': 1, 'MaxLevel': 2, 'Scaling': 'add', 'Description': " placeholder- Don't buy this"},
    ],
    "Village": [
        {'Name': 'Opal Enthusiasm', 'BonusPerLevel': 30, 'MaxLevel': 5, 'Scaling': 'add', 'Description': '% Villager EXP per 10 Opals invested'},
        {'Name': 'Contented Creator', 'BonusPerLevel': 1, 'MaxLevel': 4, 'Scaling': 'add', 'Description': '% Villager EXP per Schematic created'},
        {'Name': 'Cosmo, Enhance!', 'BonusPerLevel': 10, 'MaxLevel': 3, 'Scaling': 'add', 'Description': '% Villager EXP, and unlocks Enhancing Conjuror Bonuses'},
        {'Name': 'Lengthmeister', 'BonusPerLevel': 25, 'MaxLevel': 4, 'Scaling': 'value', 'Description': 'x higher Measurement Bonuses'},
        {'Name': 'Study All Nighter', 'BonusPerLevel': 20, 'MaxLevel': 5, 'Scaling': 'add', 'Description': '% Study Rate for Bolaia!'},
        {'Name': 'Equal Spread', 'BonusPerLevel': 2, 'MaxLevel': 4, 'Scaling': 'value', 'Description': 'x villager exp per 5 opals invested in the villager with the LEAST opals!'},
        {'Name': 'Village Placeholder', 'BonusPerLevel': 1, 'MaxLevel': 1, 'Scaling': 'add', 'Description': " placeholder- Don't buy this"},
    ],
    "IdleOn": [
        {'Name': 'Pocket Divinity', 'BonusPerLevel': 1, 'MaxLevel': 2, 'Scaling': 'add', 'Description': ' account-wide Divinity links'},
        {'Name': 'Beeg Beeg Forge', 'BonusPerLevel': 3, 'MaxLevel': 5, 'Scaling': 'multi', 'Description': 'x forge ore capacity'},
        {'Name': 'Resource Bursting', 'BonusPerLevel': 100, 'MaxLevel': 3, 'Scaling': 'add', 'Description': '% multi-resource max'},
        {'Name': 'Voter Integrity', 'BonusPerLevel': 6, 'MaxLevel': 5, 'Scaling': 'add', 'Description': '% larger Ballot bonus'},
        {'Name': 'Weapon Relevancy', 'BonusPerLevel': 75, 'MaxLevel': 4, 'Scaling': 'add', 'Description': '% stronger Weapon Power'},
        {'Name': 'Equinox Maxim', 'BonusPerLevel': 12, 'MaxLevel': 5, 'Scaling': 'value', 'Description': 'x Equinox Bar Fill Rate'},
        {'Name': 'IdleOn Placeholder', 'BonusPerLevel': 1, 'MaxLevel': 2, 'Scaling': 'add', 'Description': " placeholder- Don't buy this",},
    ]
}
max_majiks = 0
total_placeholder_majiks = 0
for majik_type, majiks in caverns_conjuror_majiks.items():
    for majik in majiks:
        max_majiks += majik['MaxLevel']
        if 'placeholder' in majik['Description']:
            total_placeholder_majiks += majik['MaxLevel']

caverns_measurer_measurement_resources = HolesInfo[50]
caverns_measurer_scalar_matchup = HolesInfo[52]
caverns_measurer_scalars = HolesInfo[53]
caverns_measurer_measurements = HolesInfo[54]
caverns_measurer_HI55 = HolesInfo[55]
caverns_max_measurements = sum(1 for measurement in caverns_measurer_measurements if measurement != 'i')  #i is a placeholder for not-implemented
caverns_measurer_measurement_names = [
    'Inches', 'Meters', 'Miles', 'Liters', 'Yards',
    'Pixels', 'Leagues', 'Nanometers', 'Sadness', 'Feet',
    'Bababooey', 'Killermeters', 'Joules', 'Meters', 'Pixels',
    'Yards'
]
for entry_index, entry in enumerate(caverns_measurer_measurements):
    try:
        caverns_measurer_measurements[entry_index] = [
            caverns_measurer_measurement_names[entry_index],
            entry.replace('|', ' ').replace('_', ' ').replace('+{%', '').replace('访', '&').title(),
            caverns_measurer_scalars[int(caverns_measurer_scalar_matchup[entry_index])].replace('_', ' ').title(),
            getCavernResourceImage(caverns_measurer_measurement_resources[entry_index])
        ]
    except:
        caverns_measurer_measurements[entry_index] = [
            f"UnknownUnit{entry_index}",
            entry.replace('|', ' ').replace('_', ' ').replace('+{%', '').replace('访', '&').title(),
            f"UnknownScalar{entry_index}",
            ''
        ]

caverns_measurement_percent_goals = {
    # "MeasurementBaseBonus" in source code
    # =CosmosMulti * ScalingValue * (Level / (100 + Level))
    # Numbers calculated by Xythium https://docs.google.com/spreadsheets/d/1krMdc1cGhKLBVv7XFEBU4BUbatyLHggEwp7XN5a6gAc/edit?usp=sharing
    12: '10%', 25: '20%', 43: '30%', 67: '40%', 100: '50%', 150: '60%',
    234: '70%', 300: '75%', 400: '80%', 567: '85%', 900: '90%', 1900: '95%',
    2400: '96%', 3234: '97%', 4900: '98%', 9900: '99%'
}
caverns_librarian_studies = {}
for entry_index, entry in enumerate(HolesInfo[69]):
    caverns_librarian_studies[entry_index] = [
        HolesInfo[69][entry_index].replace('_', ' '),  #Description
        int(HolesInfo[70][entry_index])  #Scaling value
    ]

monument_hours = [int(h) for h in HolesInfo[30]]  #[1, 80, 300, 750, 2000, 5000, 10000, 24000] as of 2.31
monument_names = [f"{monument_name} Monument" for monument_name in HolesInfo[41]]
released_monuments = 3  #Don't increase this without implementing a _parse_ function in models first
monument_layer_rewards = {
    monument_names[0]: {
        monument_hours[0]: {'Description': 'Story Minigame unlocked with 3 Swords', 'Image': 'monument-basic-sword'},
        monument_hours[1]: {'Description': '+2 additional Swords', 'Image': 'monument-basic-sword'},
        monument_hours[2]: {'Description': 'You can Re-Throw 5 swords per story', 'Image': 'engineer-schematic-40'},
        monument_hours[3]: {'Description': '+1 additional Sword', 'Image': 'monument-basic-sword'},
        monument_hours[4]: {'Description': 'You get 1 Retelling per story', 'Image': 'measurement-1'},
        monument_hours[5]: {'Description': '+1 additional Sword', 'Image': 'monument-basic-sword'},
        monument_hours[6]: {'Description': '+10 Re-Throws per story', 'Image': 'engineer-schematic-40'},
        monument_hours[7]: {'Description': '+1 additional Sword', 'Image': 'monument-basic-sword'},
    },
    monument_names[1]: {
        monument_hours[0]: {'Description': 'Story Minigame unlocked with Coins', 'Image': 'justice-coin-1'},
        monument_hours[1]: {'Description': 'Start with +1 Mental Health', 'Image': 'justice-currency-2'},
        monument_hours[2]: {'Description': 'You can dismiss 1 case per story', 'Image': 'justice-currency-5'},
        monument_hours[3]: {'Description': 'Start with 1.5x more Coins', 'Image': 'justice-coin-2'},
        monument_hours[4]: {'Description': '+1 Mental Health and Dismissal', 'Image': 'justice-currency-6'},
        monument_hours[5]: {'Description': 'Start with +7 Popularity', 'Image': 'justice-currency-4'},
        monument_hours[6]: {'Description': 'Start with 3x more Coins', 'Image': 'justice-coin-3'},
        monument_hours[7]: {'Description': '+2 Mental Health and Dismissals', 'Image': 'justice-currency-6'},
    },
    monument_names[2]: {
        monument_hours[0]: {'Description': f'Start with # Attempts', 'Image': 'wisdom-attempts'},
        monument_hours[1]: {'Description': f'Get +2 Attempts per Board Clear', 'Image': 'wisdom-attempts'},
        monument_hours[2]: {'Description': f'1st attempt each Board reveals row', 'Image': 'wisdom-row'},
        monument_hours[3]: {'Description': f'Start with 4 Insta Matches per story', 'Image': 'wisdom-instamatch'},
        monument_hours[4]: {'Description': f'+4 additional Starting Attempts', 'Image': 'wisdom-attempts'},
        monument_hours[5]: {'Description': f'4th attempt each Board reveals square', 'Image': 'wisdom-square'},
        monument_hours[6]: {'Description': f'Get +1 Attempts per Board Clear', 'Image': 'wisdom-attempts'},
        monument_hours[7]: {'Description': f'+5 additional Insta Matches', 'Image': 'wisdom-instamatch'},
    },
}
monument_bonuses_clean_descriptions = [d.replace('|', ' ').replace('_', ' ') for d in HolesInfo[32]]
monument_bonuses_scaling = [int(v) for v in HolesInfo[37]]
monument_bonuses = {monument_names[entry]: {} for entry in range(0, released_monuments+1)}

#Layer rewards are in HolesInfo[31], but I wanted to clean up the display a bit
justice_monument_currencies = ['Mental Health', 'Coins', 'Popularity', 'Dismissals']
for i in range(0, 10 * released_monuments):  #Final number is excluded in range. 10 for Bravery, 10 for Justice
    monument_name = monument_names[i // 10]
    try:
        monument_bonuses[monument_name][i] = {
            'Description': monument_bonuses_clean_descriptions[i],
            'ScalingValue': monument_bonuses_scaling[i],
            'ValueType': 'Percent' if '{' in monument_bonuses_clean_descriptions[i] else 'Multi' if '}' in monument_bonuses_clean_descriptions[i] else 'Flat',
            'Image': f"{monument_name.lower().replace(' ', '-').replace('-monument', '')}-bonus-{i}",
        }
    except Exception as e:
        logger.exception(f"Couldn't parse {monument_name} bonus {i}: {e}")
        continue

bell_ring_images = ['well-bucket', 'opal', 'cavern-6', 'cavern-7', 'jar-rupie-0', 'temple-torch']
bell_ring_bonuses = {}
for i in range(0, 6):
    bell_ring_bonuses[i] = {
        'Description': HolesInfo[59][i * 2].replace('|', ' ').replace('_', ' ').title(),
        'ScalingValue': float(HolesInfo[59][i * 2 + 1]),
        'Image': bell_ring_images[i]
    }

bell_clean_resources = ['coins', 'well-sediment-3', 'purple-bits', 'harp-note-4', 'particles', 'jar-rupie-5']
bell_clean_improvements = {}
for i in range(0, 6):
    bell_clean_improvements[i] = {
        'Description': HolesInfo[60][i].replace('|', ' ').replace('_', ' '),
        'Image': (
            "bell-ring" if 'Ring' in HolesInfo[60][i] else
            'bell-ping' if 'Ping' in HolesInfo[60][i] else
            'bell-clean' if 'Clean' in HolesInfo[60][i] else
            ''
        ),
        'Resource': bell_clean_resources[i]
    }

harp_chord_effects = {
    'C': ['Generate the tuned Note', 'Harp Note Gain'],
    'D': ['Chance for an Opal', 'Harp Note Gain'],
    'E': ['Nothing', 'Harp Power/hr'],
    'F': ['Generate the tuned Note and both nearby Notes', 'Harp Note Gain'],
    'G': ['Generate EXP for all unlocked Chords', 'String EXP Gain'],
    'A': ['Generate every Note you have unlocked', 'Harp Note Gain'],
    'B': ['TBD', 'TBD'],
}
harp_notes = [
    'Crotchet Note', 'Natural Note', 'Bass Note', 'Treble Note', 'Eighth Note',
    'Quaver Note', 'Sharp Note', '(F)Clef Note', '(G)Clef Note', 'Sixteenth Note'
]
max_harp_notes = len(harp_notes)

#Taken from "LampBonuses" == e inside _customBlock_Holes function
#(a.engine.getGameAttribute("DNSM").h.HoleozDT = "25,10,8;15,40,10;20,35,12;1,1,1;2,2,2" last verified as of v2.23
lamp_world_wish_values = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [25, 10, 8],
    [15, 40, 10],
    [20, 35, 12],
    [1, 1, 1],
    [2, 2, 2]
]
#LampWishes = function () in source code, slightly cleaned up
lamp_wishes = [
    ["More Wishes", 1, 3, 1, "Unlock the next Wish Type"],
    ["Another Try", 6, 0, 0, "Reset Opals or Majik investments. Cost does not increase."],
    ["1000000 Opals", 2, 2, 1, "+1 Opal"],
    ["Bring Them Back", 2, 0, 0, "+12 AFK Hours to any unlocked Monument Cost does not increase."],
    ["World 4 Stuff", 1, .2, 1,
     f"+@% Cooking Speed, "
     f"+#% Shiny Pet LV Up & Breedability Rate, "
     f"+$% Lab EXP gain"],
    ["A Moderate Discount", 2, .5, 1, "15% discount on the next Engineer Schematic creation"],
    ["World 5 Things", 1, .2, 1,
     f"+@% Sailing Loot Value, "
     f"+#% Bits gain, "
     f"+$% Divinity Pts gain"],
    ["Infinite Resources", 1, .05, 1, "Well, Harp, and Jar resource gain"],
    ["World 6 Majigers", 1, .2, 1,
     f"+@% Next Crop chance, "
     f"+#% Stealth for Ninja twins, "
     f"+$% All Essence gain"],
    ["Knowledge of Future", 999, 999, 1, "Not implemented"],
    ["World 7 Stuff", 999, 999, 1, "Not implemented"],
    ["World 8 Stuff", 999, 999, 1, "Not implemented"]
]
caverns_jar_collectibles = [entry.split('|') for entry in HolesInfo[67]]
caverns_jar_collectibles_count = len(caverns_jar_collectibles)
caverns_jar_rupies = ['Red', 'Green', 'Blue', 'Yellow', 'Magenta', 'Turquoise', 'Orange', 'Ultramarine', 'Purple', 'Master', 'White', 'Dark']
caverns_jar_max_rupies = len(caverns_jar_rupies)
caverns_jar_jar_types = ['Simple', 'Tall', 'Ornate', 'Great', 'Enchanted', 'Artisan', 'Epic', 'Gilded', 'Ceremony', 'Heirloom']
caverns_jar_max_jar_types = len(caverns_jar_jar_types)
caverns_gambit_pts_bonuses = HolesInfo[71]
caverns_gambit_challenge_names = ["King's Gambit", "Horsey's Gambit", "Bishop's Gambit", "Queen's Gambit", "Rook's Gambit", "Noob's Gambit"]
schematics_unlocking_gambit_challenges = [None, 'Horsey Gambit', 'Bishop Gambit', 'Queen Gambit', 'Castle Gambit', 'Noob Gambit']
caverns_gambit_total_challenges = len(caverns_gambit_challenge_names)
caverns_gambit_pts_for_doublers = [
    0, 1, 206, 351, 598, 1018,
    1735, 2956, 5036, 8579, 14615,
    24899, 42419, 72267, 123118, 209749,
    357336, 608773, 1037131, 1766899, 3010163,
    5128238, 8736680, 14884170, 25357290, 43199731,
    73596854, 125382655, 213607095, 363909914, 619972035,
    1056210093, 1799403358, 3065538252, 5222578214, 8897401031,
    15157981722, 25823766860, 43994441151, 74950756128, 127689219300,
    217536654301, 370604474083, 631377165616, 1075640347430, 1832505545065,
    3121932512775, 5318653818304, 9061079418982, 15436831018131, 26298826096055
]


def getMaxEngineerLevel() -> int:
    max_engi_last_i_checked = 29  # Last checked on v2.32 Gambit
    if released_schematics > (1 + (max_engi_last_i_checked * 3) + (max_engi_last_i_checked // 5)):
        needed_level = 0
        unlocked_schematics = 0
        while unlocked_schematics < released_schematics:
            needed_level += 1
            unlocked_schematics = 1 + (needed_level * 3) + (needed_level // 5)
        logger.warning(f"Update consts.max_engi_last_i_checked! {needed_level} is needed to unlock all {released_schematics} released schematics")
        return needed_level
    else:
        return max_engi_last_i_checked


def getVillagerEXPRequired(villager_index, villager_level, game_version):
    #_customBlock_Holes."VillagerExpREQ"
    match villager_index:
        case 0:
            if villager_level == 1:
                result = 5
            else:
                result = (
                    10 * (
                        (10 + 7 * pow(villager_level, 2.1))
                        * pow(2.1, villager_level)
                        * (1 + .75 * max(0, villager_level - 4))
                        * pow(3.4, min(1, max(0, math.floor((1e5 + game_version) / 100247.3))) * max(0, villager_level - 12))
                    )
                    - 1.5
                )
        case 1:
            result = 30 * ((10 + 6 * pow(villager_level, 1.8)) * pow(1.57, villager_level))
        case 2:
            result = 50 * ((10 + 5 * pow(villager_level, 1.7)) * pow(1.4, villager_level))
        case 3:
            result = 120 * ((30 + 10 * pow(villager_level, 2)) * pow(2, villager_level))
        case 4:
            result = 500 * (10 + 5 * pow(villager_level, 1.3)) * pow(1.13, villager_level)
        case _:
            result = 10 * pow(10, 20)
    return result


def getSedimentBarRequirement(sediment_index, sediment_level):
    try:
        result = 100 * pow(1.5, sediment_level) * ValueToMulti(sediment_bars[sediment_index])
    except OverflowError:
        logger.exception(f"Overflow error calculating SedimentBarRequirement given {sediment_index = } and {sediment_level = }. Returning 1e100.")
        result = 1e100
    return result


def getWellOpalTrade(holes_11_9):
    # From looking at data, holes_11_9 is just the number of previously completed trades. Maybe it changes higher up at some point
    if holes_11_9 == 1:
        return 6
    elif holes_11_9 == 2:
        return 60
    else:
        result = (
            (1 + (3 * holes_11_9) + pow(holes_11_9, 2))
            * pow(3.5 + holes_11_9 / 10, holes_11_9)
        )
        return math.ceil(result) if 1e9 > result else math.floor(result)


def getMotherlodeEfficiencyRequired(layers_destroyed: int):
    result = math.ceil(9000 * pow(1.8, layers_destroyed))
    return result


def getDenOpalRequirement(current_opals: int):
    result = 12 * (150 + (30 + current_opals) * current_opals) * pow(1.5, current_opals)
    return round(result)


def getMonumentOpalChance(current_opals: int, opal_bonus_value: float = 1):
    result = (
        min(0.5, pow(0.5, current_opals))
        * ValueToMulti(opal_bonus_value)
    )
    return result


def getBellExpRequired(bell_index, current_uses: int):
    match bell_index:
        case 0:  #Ring
            result = (5 + 3 * current_uses) * pow(1.05, current_uses)
        case 1:  #Ping
            result = (10 + (10 * current_uses + pow(current_uses, 2.5))) * pow(1.75, current_uses)
        case 2:  #Clean
            result = 100 * pow(3, current_uses)
        case _:  #Renew falls into this else
            result = 250
    return result


def getBellImprovementBonus(i_index, i_level, schematic_stacks=0, schematic_owned=False):
    #"BellMethodsQTY" in source code
    # Yes, HolesInfo[61] only applies AFTER the schematic is purchased. Probably a bug in game but must be replicated here for accuracy.
    result = (
        2 * i_level * max(1, pow(1.1, schematic_stacks) * schematic_owned * float(HolesInfo[61][i_index]))
    )
    return result


def getGrottoKills(current_opals: int):
    result = 5000 * pow(3.4, current_opals)
    return result


def getHarpNoteUnlockCost(note_index):
    result = math.ceil(150 * pow(1 + note_index, 1.5) * pow(4.5, note_index))
    return result


def getWishCost(wish_index, wish_level):
    match wish_index:
        case 0:  #New Wish Type
            if 11 > wish_level:
                result = math.floor(1 + (2 * wish_level) + pow(wish_level, 2))
            else:
                result = 999999
        case 2:  #Opal
            result = math.floor(1 + (2 * wish_level) + pow(wish_level, 1.7))
        case _:  #Everything else
            result = math.floor(lamp_wishes[wish_index][1] + (wish_level * lamp_wishes[wish_index][2]))
    return result


def getSummoningDoublerPtsCost(current_doublers):
    try:
        pts_required = caverns_gambit_pts_for_doublers[current_doublers+1]
    except IndexError:
        #both functions using base e
        pts_required = math.ceil(math.exp((current_doublers + 9) / (1 / math.log(2) + 1 / math.log(10))))
    return pts_required
