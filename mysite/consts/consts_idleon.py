import math
from flask import g as session_data
from consts.generated.monster_data import monster_data
from utils.number_formatting import parse_number
from utils.safer_data_handling import safer_math_pow
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)

# Last updated in v2.43 Nov 6. Make sure to manually turn any `.split("")` into `.split(" ")`
RANDOlist = ["mushG frogG beanG poopSmall ratB slimeG snakeG carrotO branch acorn goblinG plank frogBIG mushR mushW".split(" "), "jarSand mimicA crabcake shovelR coconut sandcastle pincermin potato steak moonman sandgiant snailZ".split(" "), "20 24 21 25 22 26 41 42 72 73 74 75 76 77 78 79 52 45 49 37 39 46 53 54 55".split(" "), "5 6 7 42 43 8 9 10 11 12 13 14 15 4 25 26 27 59 45 49 46 50 47 51 52 53 54 55 28 29 30 31 32 33 34 35 56 57 36 37".split(" "), "STR AGI WIS LUK UQ1val UQ2val Defence Weapon_Power".split(" "), "bloque flake speaker penguin eye mamoth snakeB glass stache snowball thermostat sheep sheep".split(" "), "0 7 14 22 30 37 44 51".split(" "), "Cardboard_Boxes Silkskin_Boxes Wooden_Crates Natural_Crates Steel_Trapper Meaty_Trapper Royal_Trapper".split(" "), "310 17 394 17 478 17 562 17 268 86 352 86 436 86 520 86 604 86 226 157 310 157 394 157 478 157 562 157 268 228 352 228 436 228 520 228 604 228 226 299 310 299 394 299 478 299 562 299 646 299".split(" "), "1 60 85 110 150 170 200 250 9999 9999 9999 9999 9999 9999 999 999 999 999 999 999 999".split(" "), "Goblin_Gorefest Wakawaka_War Acorn_Assault Frosty_Firefight Clash_of_Cans Tower_Defence_6 Tower_Defence_7".split(" "), ["0", "14", "39", "69"], ["30", "200", "1500", "10000"], "3 200 2250 12000 25000 60000 100000 150000 50000000 5 100 700 5000 40000 125000 400000 1000000 3500000 10 250 1000 7500 40000 200000 2000000 7000000 60000000".split(" "), "Build_this_space_to_unlock_the_3D_Printer. Build_this_space_to_unlock_the_Library._Wow!_What_a_game_changer! Build_this_space_to_get_your_very_own_Death_Note_thingy._Anime_doesn't_actually_exist_around_here,_so_wipe_that_smirk_off_your_face! Build_this_space_to_unlock_a_way_to_unlock_other_bonuses_using_Salt!_Its_almost_like_you're_Summoning_more_bonuses_with_Salt,_so_you_can_speedrun_the_game_faster! Build_this_space_to_get_more_Storage_Chest_slots!_I_KNOW_RIGHT?_It's_about_time!! Build_this_space_to_make_upgrading_other_Buildings_way_easier._Ok,_maybe_just_easier,_not_'way_easier'. Build_this_space_to_remotely_place,_collect_and_remove_Critter_Traps_to_and_from_any_location!_This_done_changin'_the_Trap_Game_fo'_real_yo! Build_this_space_to_harness_the_power_of_Automation!_Good_thing_you're_a_gamer,_thats_a_job_that_robots_will_never_replace. Build_this_space_because_it's_the_last_one..._I_mean_what_else_are_you_gonna_do? Build_this_space_to_get_your_first_Wizard_Defender._This_one_will_zap_nearby_monsters_as_they_run_by! Build_this_space_to_get_your_second_Wizard_Defender._This_one_will_throw_exploding_fireballs_toward_monsters,_which_explode!_Did_I_mention_the_fireballs_EXPLODE! Build_this_space_to_get_your_third_Wizard_Defender._This_one_will_roll_a_boulder_at_the_monsters,_squashing_them_into_inedible_pancakes! Build_this_space_to_get_your_fourth_Wizard_Defender._This_one_will_freeze_monsters..._pretty_cool,_right? Build_this_space_to_get_your_fifth_Wizard_Defender._This_one_will_smite_the_monsters_for_their_sins!_I_mean,_sure,_you're_the_one_murdering_them,_but_they're_monsters! Build_this_space_to_get_your_sixth_Wizard_Defender._This_one_will_rock_and_roll_all_night,_and_party_every_day!_I_don't_know_how_he_got_his_wizarding_license,_but_he_did_and_now_that's_your_problem! Build_this_space_to_get_your_seventh_Wizard_Defender._This_one_will_summon_giant_eyeballs,_which_boop_into_enemies!_Eye_think_you're_gonna_love_this_one! Build_this_space_to_get_your_eigth_Wizard_Defender._This_one_is_real_smelly._That's_his_thing,_he_stinks. Build_this_space_to_get_your_last_Wizard_Defender._This_one_is_crazy_good..._kinda_makes_all_the_other_tower_wizards_pointless. Build_this_space_to_get_your_first_Shrine._You_can_place_it_anywhere_in_the_game,_and_it_will_boost_all_characters_in_that_map!_This_one_boosts_damage! Build_this_space_to_get_your_second_Shrine._This_one_is_full_of_life,_as_well_as_pulmonary_veins_and_arteries. Build_this_space_to_get_your_third_Shrine!_This_one_is_a_bit_of_a_brain_bender,_it's_kinda_like_a_shrine_for_shrines. Build_this_space_to_get_your_fourth_Shrine._This_one's_for_all_you_institutional_bankers_out_there!_I'm_sure_I_speak_for_everyone_born_after_2008_when_I_say,_you're_the_best! Build_this_space_to_get_your_fifth_Shrine._This_one_is_green. Build_this_space_to_get_your_sixth_Shrine._This_one_is_a_pile_of_books,_which_will_somehow_give_you_a_boost_even_though_we_both_know_you_don't_read. Build_this_space_to_get_your_seventh_Shrine._This_one_is_practically_worthless,_and_will_be_forgotten_about_within_a_week_of_being_unlocked. Build_this_space_to_get_your_eigth_Shrine!_Dang,_we're_close_to_the_end,_I'm_gonna_miss_vaguely_describing_upcoming_shrines_to_you!_Anyway,_this_one's_spooky_and_scary. Build_this_space_to_get_your_last_Shrine._Yep,_definitely_the_last_one._No_need_to_look_for_a_10th_shrine_anywhere..._yet...".split(" "), "sheep flake stache ram bloque mamoth snowball penguin thermostat glass snakeB speaker eye skele2".split(" "), "10 11 12 23 75 86 87 266 267 446 447 79".split(" "), "InvStorage31 InvStorage32 InvStorage33 InvStorage34 InvStorage35 InvStorage36 InvStorage37 InvStorage38 InvStorage39 InvStorage40 InvStorage41 InvStorage42 InvBag21 InvBag22 InvBag23 InvBag24 InvBag25 InvBag26 EquipmentHats31 EquipmentHats32 EquipmentHats33 EquipmentHats34 EquipmentHats35 EquipmentHats36 EquipmentHats37 EquipmentHats38 EquipmentHats40 EquipmentHats43 EquipmentHats46 EquipmentHats47 EquipmentHats48 EquipmentHats49 EquipmentHats50 EquipmentHats45 EquipmentHats57 EquipmentHats62 Quest28 EquipmentRingsChat1 EquipmentRingsChat2 EquipmentRingsChat3 EquipmentRingsChat4 EquipmentRingsChat5 EquipmentRingsChat6 EquipmentRingsChat8 EquipmentRingsChat9 LockedInvSpace null Blank TestObj4 TestObj5 TestObj8 TestObj9 TestObj10 EquipmentWeapons1 TestObj2 EquipmentWands4 ExpSmith1 Starlight AlienTreetutorial EquipmentWeapons2 Secretstone InvStorage99 COIN EXP FillerMaterial DungWeaponBow1 DungWeaponWand1 DungWeaponSword1 TestObj15 TestObj16 TestObj14 EquipmentCape1 EquipmentHats72 Spice0 Spice6 Spice9 SailTr10 SailTr12 SailTr14 SailTr21 SailTr25 SailTr29 Bits EquipmentHatsBeg1 EquipmentShirts8 EquipmentShirts9 EquipmentPants11 EquipmentPants14 EquipmentShoes6 EquipmentShoes8 EquipmentShoes13 EquipmentPendant1 EquipmentPendant2 EquipmentPendant3 EquipmentPendant4 EquipmentPendant5 EquipmentPendant6 EquipmentPendant7 EquipmentPendant8 Trophy4 DoubleAFKtix ObolFrag DeliveryBox EquipmentHats23 EquipmentHats24 Quest8 CraftMat15 CraftMat16 CraftMat17 NPCtoken8 EquipmentShirts4 EquipmentPants12 EquipmentShoes10 EquipmentShoes11 EquipmentShoes12 EquipmentShoes14 EquipmentPendant13 EquipmentPendant15 EquipmentRings1 FoodHealth8 FishingRod1 CatchingNet1 MaxCapBagFi0 MaxCapBagB0 MaxCapBagTr0 MaxCapBagTr2 MaxCapBagS0 MaxCapBagS2 ObolPlatinumSpeed StampC10 StampC11 StampC12 EquipmentShirts7 EquipmentPants7 EquipmentPants13 EquipmentRings4 EquipmentRings5 EquipmentRings8 EquipmentRings9 EquipmentRings10 IceMountains2 InvBag9 Quest31 GemP25".split(" "), "50 50 200 800 3000 8000 14000 20000 30000 40000 50000 65000 80000 100000 200000 300000 400000 500000 600000 700000 800000 900000 1000000 1000000 1000000 1000000".split(" "), "Stiltzcho Builder_Bird Bushlyte Dazey Dog_Bone Egggulyte Funguy Giftmas_Blobulyte Glumlee Grasslands_Gary Hamish Krunk Loveulyte Meel Mutton Mr_Pigibank Papua_Piggea Picnic_Stowaway Promotheus Rocklyte Scripticus Sprout Stiltzcho Telescope Tiki_Chief Town_Marble TP_Pete Typhoon Woodsman Toadstall Falloween_Pumpkin Bubbulyte Coastiolyte".split(" "), "Bandit_Bob Walupiggy Cactolyte Carpetiem Centurion Clown Constructor_Crow Cowbo_Jones Desert_Davey Djonnut Fishpaste97 Goldric Loominadi Obol_Altar Omar_Da_Ogar Postboy_Pablob Scubidew Snake_Jar Speccius Wellington Whattso XxX_Cattleprod_XxX Gangster_Gus".split(" "), "Bellows Bill_Brr Carpenter_Cardinal Crystalswine Hoggindaz Iceland_Irwin Lonely_Hunter Lord_of_the_Hunt Shuvelle Snouts Worldo Yondergreen Worldo".split(" "), "ObolSilver0 7 ObolSilver1 14 ObolSilver2 21 ObolSilver3 28 ObolSilverCard 32 ObolSilverCatching 37 ObolSilverChoppin 42 ObolSilverFishing 47 ObolSilverMining 52 ObolSilverCons 53 ObolSilverWorship 54 ObolSilverTrapping 55 ObolSilverDamage 60 ObolSilverDef 64 ObolSilverEXP 65 ObolSilverLuck 66 ObolSilverMoney 67 ObolGold0 70 ObolGold1 73 ObolGold2 76 ObolGold3 78 ObolGoldMoney 79 ObolGoldCard 80 ObolGoldKill 82 ObolGoldChoppin 84 ObolGoldMining 86 ObolGoldLuck 88 ObolGoldCatching 90 ObolGoldFishing 92 ObolGoldEXP 93 ObolGoldDef 95 ObolGoldPop 96 ObolGoldDamage 200".split(" "), "ObolGold0 7 ObolGold1 14 ObolGold2 21 ObolGold3 28 ObolGoldMoney 32 ObolGoldCard 34 ObolGoldKill 36 ObolGoldChoppin 41 ObolGoldMining 46 ObolGoldLuck 47 ObolGoldCatching 52 ObolGoldFishing 57 ObolGoldCons 58 ObolGoldWorship 59 ObolGoldTrapping 60 ObolGoldDamage 63 ObolGoldEXP 64 ObolGoldDef 65 ObolPlatinum0 67 ObolPlatinum1 69 ObolPlatinum2 71 ObolPlatinum3 73 ObolPlatinumCard 74 ObolPlatinumCatching 76 ObolPlatinumChoppin 78 ObolPlatinumDamage 81 ObolPlatinumDef 82 ObolPlatinumEXP 83 ObolPlatinumFishing 85 ObolPlatinumKill 86 ObolPlatinumMining 88 ObolPlatinumPop 89 ObolPlatinumLuck 90 ObolPink0 91 ObolPink1 92 ObolPink2 93 ObolPink3 94 ObolPinkCard 94.5 ObolPinkCatching 95 ObolPinkDamage 96 ObolPinkDef 95.5 ObolPinkEXP 97 ObolPinkFishing 98 ObolPinkKill 98.4 ObolPinkLuck 99.2 ObolPinkMining 99.8 ObolPinkPop 200".split(" "), "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60".split(" "), "Key1_x1.png Key2_x1.png Key3_x1.png Key4_x1.png TixCol_x1.png MGp.png rtt0_x1.png ObolFrag_x1.png PremiumGem_x1.png PachAcc.png Libz.png Quest89_x1.png Key5_x1.png".split(" "), "NPCtoken5 NPCtoken6 NPCtoken4 NPCtoken9 NPCtoken10 NPCtoken11 NPCtoken13 NPCtoken7 Quest9 NPCtoken15 NPCtoken12 NPCtoken14 NPCtoken16 NPCtoken17 NPCtoken18 NPCtoken19 NPCtoken20 NPCtoken21 NPCtoken27 NPCtoken22 NPCtoken24 NPCtoken25 NPCtoken26 NPCtoken23 NPCtoken32 NPCtoken31 NPCtoken34 NPCtoken35 NPCtoken36 NPCtoken38 NPCtoken33 NPCtoken37".split(" "), "365 232 113 8 0 263 252 237".split(" "), ["DungCredits1", "DungCredits2"], "0 4 10 18 28 40 70 110 160 230 320 470 670 940 1310 1760 2400 3250 4000 5000 6160 8000 10000 12500 15000 18400 21000 25500 30500 36500 45400 52000 61000 72500 85000 110000 125000 145000 170000 200000 250000 275000 325000 400000 490000 600000 725000 875000 1000000 1200000 1500000 3000000 5000000 10000000 20000000 30000000 40000000 50000000 60000000 80000000 100000000 999999999 999999999 999999999 999999999 999999999 1999999999 1999999999 1999999999 1999999999 1999999999".split(" "), "51 189 5 0 112 189 5 0 173 189 5 0 51 292 10 1 112 292 10 1 173 292 10 1 33 395 15 2 86 395 15 2 139 395 15 2 192 395 15 2 305 189 20 3 374 189 20 3 260 292 25 4 313 292 25 4 366 292 25 4 419 292 25 4 278 395 30 5 339 395 30 5 400 395 30 5 505 189 35 6 566 189 35 6 627 189 35 6 532 292 40 7 601 292 40 7 487 395 50 8 540 395 50 8 593 395 50 8 646 395 50 8".split(" "), "a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" "), "0 1 3 2 4 5 0 1 1 1 3 0 2 0 4 1 5 1".split(" "), "0 1 3 2 4 5 6 7".split(" "), "897 9 918 37 912 95 557 942 933 102 932 184 914 204 903 266 929 271 613 515 591 478 536 516 318 515 291 485 250 479 230 515 185 512 171 484 131 479".split(" "), "915 59 915 59 916 227 627 483 574 499 261 500 200 479 139 497".split(" "), "1 2 3 4 5 6 7 8".split(" "), "DungWeaponPunch DungWeaponSword DungWeaponBow DungWeaponWand DungEquipmentHats DungEquipmentShirt DungEquipmentPants DungEquipmentShoes DungEquipmentPendant DungEquipmentRings".split(" "), "10 11 12 13 14 19 20 21 22 23 24 26 27 29 30 31 8 7 100 101 102".split(" "), ["DungCredits1", "DungCredits2"], "Iron 75 CopperBar 50 JungleTree 50 BirchTree 60 Fish1 50 Fish2 50 Gold 75 Bug1 125 Bug2 150".split(" "), "Dementia 80 PalmTree 120 StumpTree 100 Fish3 100 Fish4 100 Gold 75 PlatBar 20 Bug3 150 Bug5 100".split(" "), "16 50 90 85 75 60".split(" "), "15 30 46 90 91 105 106 115 120 121 270 271 285 286 300 301 450 451 453 460 465 466 467 480 481 482 495 496 497 135 136 137 165 360 316 317 315 361 362 363 525 526 527".split(" "), ["636", "638", "633", "637", "640"], "0 1 2 3 4 5 6 7 25 26".split(" "), "8 9 10 11 12 13 14 15 16".split(" "), "17 18 19 20 21 22 23 24 27 28".split(" "), "2 7 9 11 17 16 4 5 3 7 12 20 19 16 4 5 7 18 13 21 23 16 4 5 7 14 16 5 24 22 25 26 28".split(" "), "0 3 5 8 10 13 15 19 20 23 27 31 33 37 41 45 48 50 53 56 58 60 63 66 70".split(" "), "1 .20 .10 .05 .02 .01 .004 .001 .0005 .0003".split(" "), "_ _ _ _ _ _ _ _ _ _ BarCook.png BarBreed.png BarLab.png BarB2.png BarDiv.png BarR2.png BarB5.png BarB2.png BarB4.png BarSpel.png BarSpel.png BarSpel.png".split(" "), "1 16 28 51 55 57 63 70 101 108 110 116".split(" "), "2 5 8 12 15 20 25 35 50 65 80 100 125 150 175 200".split(" "), "2 3 4 7 11 15 20 35 60 100 170 300 500 800 1250 1700 2550 3000 4000 5000 7000 9000 12500 17500 25000 35000 45000 60000 100000 150000 200000 350000 600000 1200000 1500000 1900000 2500000 3500000 5000000 7000000 10000000 15000000 25000000 50000000 65000000 80000000 125000000 150000000 160000000 200000000 250000000 350000000 400000000 500000000 600000000 800000000 1000000000 1250000000 1500000000 1800000000 2000000000 3000000000 5000000000 8000000000 12000000000 18000000000 25000000000 40000000000 60000000000 75000000000 90000000000".split(" "), "0 2 7 3 0 12 21 9 20 1 6 3 22 2 15 26 19 0 9 13 8 28 30 18 23 6 15 22 14 11 17 21 33 19 16 13 8 10 7 23 11 14 25 16 31 24 33 32 29 14 27 31 25 24 10 33 6 9 12 16 20 23 25 27 33 32 26 2 2 2 2".split(" "), "0 2 7 0 3 12 21 2 7 9 1 3 20 6 12 22 21 15 0 9 23 1 19 20 2 13 6 8 22 15 18 23 14 21 19 11 13 8 17 7 18 16 14 1 10 20 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11".split(" "), "1 10 30 75 125 500 1000 999999".split(" "), "Gobo Oinkin Capital_P Blobbo Nebula_Neddy Eliteus Rift_Ripper Nebulyte Monolith Royal_Worm".split(" "), "5 5 15 5 1 15 5 1 1".split(" "), "105 110 111 113 130 131 134 137 138 142 143 144 146 149 152 153 154 155 156 157 159 161 164 165 166 167 168 171 174 178 179 180 182 183".split(" "), "WORLD_7_v1.00;NEW_UPDATE_PATCH_NOTES_@_*NEW_WORLD:_World_7_is_HERE!_Defeat_The_Emperor_boss_at_the_end_of_World_6_to_unlock!_@_*NEW_MAP:_Explore_through_12_maps_full_of_monsters,_resources,_secrets,_and_new_NPCs!_@_*NEW_SKILL:_Spelunking!_Level_up_by_exploring_caves_found_throughout_World_7,_then_delve_down_tunnels_to_find_amber_and_defeat_Lore_Bosses_to_unlock_new_content_for_the_rest_of_IdleOn!_@_*TOWN_FEATURES:_Rescue_fishies_to_boost_your_Coral_Reef_for_game_changing_bonuses,_and_spend_Legendary_Talent_PTS_earned_by_leveling_up_at_Whallamus!_@_*THE_GALLERY:_Codfrey_will_give_you_bonuses_from_all_the_Trophies_and_Nametags_you've_ever_found!_The_new_Replica_items_in_the_Town_Shop_let_you_mix_and_match_Trophies_and_Nametags_however_you_like!_@_*NEW_CONTENT:_Gaming_Palette,_Exotic_and_Medal_Farming,_Duperbits,_Teal_Summoning,_Ethereal_Sigils,_Mini_Ninja_Knowledge,_Killroy_Upgrades,_and_SO_much_more..._(Many_of_these_are_unlocked_via_Spelunking)_@_*SO_MANY_MORE_THINGS_SERIOUSLY_YOU_GUYS!!!_Click_Discord_button_up_there_for_full_patch_notes!;*Le Monde 6 est arriv\u00e9, avec tout ce que vous pourriez souhaiter ! De nouveaux monstres, de nouvelles comp\u00e9tences, de nouvelles cartes, de nouveaux tampons, de nouvelles bulles, de nouvelles fioles, de nouvelles statues, de nouveaux \u00e9quipements, tellement de nouveaut\u00e9s ! @ *Vous pouvez d\u00e9couvrir le Monde 6 vous-m\u00eame, \u00e0 la place, ces notes de mise \u00e0 jour concernent tous les changements de cette mise \u00e0 jour non li\u00e9s au Monde 6. @ *Nouvel affichage des pi\u00e8ces ajout\u00e9 ! Collectez 100 pi\u00e8ces Godshard pour voir ce que je veux dire ! @ *Le succ\u00e8s Trial by Time peut d\u00e9sormais \u00eatre compl\u00e9t\u00e9 \u00e0 n'importe quelle vitesse de d\u00e9placement. @ *Mise \u00e0 l'\u00e9chelle du bonus ajust\u00e9e sur la 6\u00e8me bulle de chaque couleur. C'est un buff pour toute personne en dessous du niveau de bulle 300, sinon c'est un nerf. @ * Correction du probl\u00e8me o\u00f9 les archers glissaient lorsqu'ils essayaient de combattre des foules prot\u00e9g\u00e9es. @ *Les attaques au canon de Siege Breaker apparaissent d\u00e9sormais derri\u00e8re lui.;*Welt 6 ist da, mit allem, was Sie sich nur w\u00fcnschen k\u00f6nnen! Neue Monster, neue F\u00e4higkeiten, neue Karten, neue Stempel, neue Blasen, neue Fl\u00e4schchen, neue Statuen, neue Ausr\u00fcstung, so viel neues Zeug! @ *Sie k\u00f6nnen Welt 6 selbst entdecken. Stattdessen gelten diese Patchnotizen f\u00fcr alle \u00c4nderungen in diesem Update, die nicht mit Welt 6 zusammenh\u00e4ngen. @ *Neue M\u00fcnzanzeige hinzugef\u00fcgt! Sammle 100 Godshard-M\u00fcnzen, um zu sehen, was ich meine! @ *Die Errungenschaft \u201ePr\u00fcfung durch Zeit\u201c kann jetzt bei jeder Bewegungsgeschwindigkeit abgeschlossen werden. @ *Bonusskalierung f\u00fcr die 6. Blase jeder Farbe angepasst. Es ist ein Buff f\u00fcr alle unter Bubble Lv 300, andernfalls ist es ein Nerf. @ *Das Problem wurde behoben, bei dem Bogensch\u00fctzen herumrutschten, wenn sie versuchten, gegen abgeschirmte Mobs zu k\u00e4mpfen. @ *Die Kanonenangriffe von Belagerungsbrecher erscheinen jetzt hinter ihm.;*\uc6d0\ud558\ub294 \ubaa8\ub4e0 \uac83\uc744 \uac16\ucd98 \uc6d4\ub4dc 6\uc774 \ub3c4\ucc29\ud588\uc2b5\ub2c8\ub2e4! \uc0c8\ub85c\uc6b4 \ubaac\uc2a4\ud130, \uc0c8\ub85c\uc6b4 \uae30\uc220, \uc0c8\ub85c\uc6b4 \uc9c0\ub3c4, \uc0c8\ub85c\uc6b4 \uc6b0\ud45c, \uc0c8\ub85c\uc6b4 \uac70\ud488, \uc0c8\ub85c\uc6b4 \uc57d\ubcd1, \uc0c8\ub85c\uc6b4 \uc870\uac01\uc0c1, \uc0c8\ub85c\uc6b4 \uc7a5\ube44, \ub108\ubb34\ub098 \ub9ce\uc740 \uc0c8\ub85c\uc6b4 \uac83\ub4e4! @ *\uc6d4\ub4dc 6\ub97c \uc9c1\uc811 \ubc1c\uacac\ud558\uc2e4 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \ub300\uc2e0 \uc774 \ud328\uce58 \ub178\ud2b8\ub294 \uc6d4\ub4dc 6\uacfc \uad00\ub828\ub418\uc9c0 \uc54a\uc740 \uc774\ubc88 \uc5c5\ub370\uc774\ud2b8\uc758 \ubaa8\ub4e0 \ubcc0\uacbd \uc0ac\ud56d\uc5d0 \ub300\ud55c \uac83\uc785\ub2c8\ub2e4. @ *\uc0c8\ub85c\uc6b4 \ucf54\uc778 \ud45c\uc2dc\uac00 \ucd94\uac00\ub418\uc5c8\uc2b5\ub2c8\ub2e4! 100\uac1c\uc758 \uac13\uc0e4\ub4dc \ub3d9\uc804\uc744 \ubaa8\uc544 \ubb34\uc2a8 \ub73b\uc778\uc9c0 \uc54c\uc544\ubcf4\uc138\uc694! @ *\uc774\uc81c \ubaa8\ub4e0 \uc774\ub3d9 \uc18d\ub3c4\uc5d0\uc11c \uc2dc\uac04\ubcc4 \uc2dc\ud5d8 \uc5c5\uc801\uc744 \uc644\ub8cc\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4. @ *\uac01 \uc0c9\uc0c1\uc758 6\ubc88\uc9f8 \ubc84\ube14\uc5d0 \ub300\ud55c \ubcf4\ub108\uc2a4 \uc2a4\ucf00\uc77c\ub9c1\uc744 \uc870\uc815\ud588\uc2b5\ub2c8\ub2e4. \ubc84\ube14 Lv 300 \ubbf8\ub9cc\uc778 \uc0ac\ub78c\uc5d0\uac8c\ub294 \ubc84\ud504\uc774\uace0, \uadf8\ub807\uc9c0 \uc54a\uc73c\uba74 \ub108\ud504\uc785\ub2c8\ub2e4. @ *\ubc29\uc5b4\ub9c9\uc774 \uc788\ub294 \ubab9\uacfc \uc2f8\uc6b8 \ub54c \uad81\uc218\uac00 \ubbf8\ub044\ub7ec\uc9c0\ub294 \ubb38\uc81c\ub97c \uc218\uc815\ud588\uc2b5\ub2c8\ub2e4. @ *Siege Breaker\uc758 \ub300\ud3ec \uacf5\uaca9\uc774 \uc774\uc81c \uadf8\uc758 \ub4a4\uc5d0\uc11c \uc0dd\uc131\ub429\ub2c8\ub2e4.;*\u3042\u306a\u305f\u304c\u671b\u3080\u3059\u3079\u3066\u304c\u63c3\u3063\u305f\u30ef\u30fc\u30eb\u30c9 6 \u304c\u5230\u7740\u3057\u307e\u3057\u305f!\u65b0\u3057\u3044\u30e2\u30f3\u30b9\u30bf\u30fc\u3001\u65b0\u3057\u3044\u30b9\u30ad\u30eb\u3001\u65b0\u3057\u3044\u30de\u30c3\u30d7\u3001\u65b0\u3057\u3044\u30b9\u30bf\u30f3\u30d7\u3001\u65b0\u3057\u3044\u30d0\u30d6\u30eb\u3001\u65b0\u3057\u3044\u5c0f\u74f6\u3001\u65b0\u3057\u3044\u5f6b\u50cf\u3001\u65b0\u3057\u3044\u88c5\u5099\u306a\u3069\u3001\u65b0\u3057\u3044\u3082\u306e\u304c\u305f\u304f\u3055\u3093\u3042\u308a\u307e\u3059\u3002 @ *\u30ef\u30fc\u30eb\u30c9 6 \u306f\u3054\u81ea\u8eab\u3067\u767a\u898b\u3059\u308b\u3053\u3068\u304c\u3067\u304d\u307e\u3059\u3002\u4ee3\u308f\u308a\u306b\u3001\u3053\u308c\u3089\u306e\u30d1\u30c3\u30c1\u30ce\u30fc\u30c8\u306f\u3001\u30ef\u30fc\u30eb\u30c9 6 \u306b\u95a2\u4fc2\u3057\u306a\u3044\u3053\u306e\u30a2\u30c3\u30d7\u30c7\u30fc\u30c8\u306e\u3059\u3079\u3066\u306e\u5909\u66f4\u3092\u5bfe\u8c61\u3068\u3057\u3066\u3044\u307e\u3059\u3002 @ *\u65b0\u3057\u3044\u30b3\u30a4\u30f3\u306e\u8868\u793a\u304c\u8ffd\u52a0\u3055\u308c\u307e\u3057\u305f\u3002 Godshard \u30b3\u30a4\u30f3\u3092 100 \u679a\u96c6\u3081\u3066\u3001\u79c1\u306e\u8a00\u3063\u3066\u3044\u308b\u610f\u5473\u3092\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002 @ *Trial by Time \u30a2\u30c1\u30fc\u30d6\u30e1\u30f3\u30c8\u306f\u4efb\u610f\u306e\u79fb\u52d5\u901f\u5ea6\u3067\u5b8c\u4e86\u3067\u304d\u308b\u3088\u3046\u306b\u306a\u308a\u307e\u3057\u305f\u3002 @ *\u5404\u8272\u306e 6 \u756a\u76ee\u306e\u30d0\u30d6\u30eb\u306e\u30dc\u30fc\u30ca\u30b9 \u30b9\u30b1\u30fc\u30ea\u30f3\u30b0\u3092\u8abf\u6574\u3057\u307e\u3057\u305f\u3002\u30d0\u30d6\u30ebLv 300\u4ee5\u4e0b\u306e\u4eba\u306b\u3068\u3063\u3066\u306f\u30d0\u30d5\u3067\u3059\u304c\u3001\u305d\u3046\u3067\u306a\u3044\u5834\u5408\u306f\u30ca\u30fc\u30d5\u3067\u3059\u3002 @ *\u5c04\u624b\u304c\u30b7\u30fc\u30eb\u30c9\u3055\u308c\u305fMob\u3068\u6226\u304a\u3046\u3068\u3059\u308b\u3068\u6ed1\u308a\u56de\u308b\u554f\u984c\u3092\u4fee\u6b63\u3057\u307e\u3057\u305f\u3002 @ *Siege Breaker \u306e\u5927\u7832\u653b\u6483\u304c\u5f7c\u306e\u80cc\u5f8c\u306b\u51fa\u73fe\u3059\u308b\u3088\u3046\u306b\u306a\u308a\u307e\u3057\u305f\u3002;*\u4e16\u754c 6 \u5df2\u7ecf\u5230\u6765\uff0c\u62e5\u6709\u60a8\u60f3\u8981\u7684\u4e00\u5207\uff01\u65b0\u602a\u7269\u3001\u65b0\u6280\u80fd\u3001\u65b0\u5730\u56fe\u3001\u65b0\u5370\u7ae0\u3001\u65b0\u6ce1\u6ce1\u3001\u65b0\u74f6\u5b50\u3001\u65b0\u96d5\u50cf\u3001\u65b0\u88c5\u5907\uff0c\u8fd9\u4e48\u591a\u65b0\u4e1c\u897f\uff01 @ *\u60a8\u53ef\u4ee5\u81ea\u5df1\u53d1\u73b0\u4e16\u754c 6\uff0c\u76f8\u53cd\uff0c\u8fd9\u4e9b\u8865\u4e01\u8bf4\u660e\u9002\u7528\u4e8e\u672c\u6b21\u66f4\u65b0\u4e2d\u4e0e\u4e16\u754c 6 \u65e0\u5173\u7684\u6240\u6709\u66f4\u6539\u3002@ *\u6dfb\u52a0\u4e86\u65b0\u786c\u5e01\u663e\u793a\uff01\u6536\u96c6 100 \u4e2a\u795e\u788e\u7247\u786c\u5e01\u5c31\u660e\u767d\u6211\u7684\u610f\u601d\u4e86\uff01 @ *\u65f6\u95f4\u5ba1\u5224\u6210\u5c31\u73b0\u5728\u53ef\u4ee5\u4ee5\u4efb\u4f55\u79fb\u52a8\u901f\u5ea6\u5b8c\u6210\u3002 @ *\u8c03\u6574\u4e86\u6bcf\u79cd\u989c\u8272\u7684\u7b2c\u516d\u4e2a\u6c14\u6ce1\u7684\u5956\u91d1\u6bd4\u4f8b\u3002\u5bf9\u4e8e 300 \u7ea7\u4ee5\u4e0b\u7684\u6ce1\u6ce1\u6765\u8bf4\u662f\u4e00\u4e2a buff\uff0c\u5426\u5219\u5c31\u662f nerf\u3002 @ *\u4fee\u590d\u4e86\u5f13\u7bad\u624b\u5728\u8bd5\u56fe\u5bf9\u6297\u5c4f\u853d\u5c0f\u602a\u65f6\u4f1a\u6ed1\u52a8\u7684\u95ee\u9898\u3002 @ *\u653b\u57ce\u8005\u7684\u5927\u70ae\u653b\u51fb\u73b0\u5728\u5728\u4ed6\u8eab\u540e\u4ea7\u751f\u3002".split(";"), "Pet0 Pet1 Pet3 Pet2 Pet7 w4b4 Pet10 Pet5 Pet8 Pet11 PetNA".split(" "), "0 2 7 13 22 31 38 48 54 62 62".split(" "), "TestObj16 TestObj5 TestObj8 TestObj14 TestObj15 EquipmentWeapons1 Trophy4 EquipmentCape1 EquipmentWeapons2 EquipmentRingsChat8 EquipmentHats72 EquipmentNametag2 EquipmentGown0 TrophyReplica4 EquipmentNametagReplica2".split(" "), "babayaga babaHour poopBig babaMummy mini3a mini4a iceBossZ iceBossZ2 iceBossZ3 snakeZ snakeZ2 snakeZ3 frogGR frogGR2 frogGR3 Meteor".split(" "), "BLOOD_BERSERKER DEATH_BRINGER DIVINE_KNIGHT ROYAL_GUARDIAN SIEGE_BREAKER MAYHEIM WIND_WALKER BEAST_MASTER ELEMENTAL_SORCERER SPIRITUAL_MONK ARCANE_CULTIST BUBONIC_CONJUROR FILLER MINING SMITHING CHOPPING FISHING ALCHEMY BUG_CATCHING TRAPPING CONSTRUCTION WORSHIP COOKING BREEDING LABORATORY SAILING DIVINITY GAMING FARMING SNEAKING SUMMONING".split(" "), "_ DEATH_BRINGER _ ROYAL_GUARDIAN _ MAYHEIM WIND_WALKER _ _ SPIRITUAL_MONK ARCANE_CULTIST _ FILLER MINING SMITHING CHOPPING FISHING ALCHEMY BUG_CATCHING TRAPPING CONSTRUCTION WORSHIP COOKING BREEDING LABORATORY SAILING DIVINITY GAMING FARMING SNEAKING SUMMONING".split(" "), "GrasslandsA GrasslandsB SewerA TreeInteriorA GrasslandsC SewerB JungleA GrasslandsD TreeInteriorB JungleB JungleC ForestA ForestB ForestC TreeInteriorC".split(" "), "zDesertCalmA zDesertCalmB zDesertCalmC zDesertMildA zDesertMildB zDesertMildC zDesertMildD zDesertNightA zDesertNightB zDesertNightC zDesertNightD".split(" "), "ySnowA1 ySnowA2 ySnowA3 ySnowB1 ySnowB2 ySnowB3 ySnowB4 ySnowB5 ySnowC1 ySnowC2 ySnowC3 ySnowC4 ySnowD1".split(" "), "xSpaceA1 xSpaceA2 xSpaceA3 xSpaceA4 xSpaceB1 xSpaceB2 xSpaceB3 xSpaceB4 xSpaceB5 xSpaceC1 xSpaceC2 xSpaceC3 xSpaceC4".split(" "), "wLavaA1 wLavaA2 wLavaA3 wLavaA4 wLavaA5 wLavaB1 wLavaB2 wLavaB3 wLavaB4 wLavaB5 wLavaB6 wLavaC1 wLavaC2".split(" "), "Oh_hi_again_cutie..._how_you_doing? Heyyyyy..._so_uhm,_yea..._about_that... Oh,_it's_you..._huh.... Well_well_well_look_who_came_back!_I_knew_you_couldn't_resist_me! Great_timing!_I_just_finished_work,_I_dropped_351_new_players_off_at_world_1_# My_my..._you_look_just_as_handsome_as_the_day_we_first_met! Ew,_the_noob_is_back_|_@_Haha_just_kidding_you're_still_a_cutie. Oh_how_long_I've_been_waiting_for_you_to_return... Aha!_I_knew_you_wouldn't_forget_about_me! I_knew_what_we_had_between_us_was_special,_I'm_glad_you_felt_the_same_way...".split(" "), "Kill_all_monsters_in_under_25_seconds!_Tick_tock,_times_running_out!! Defeat_10_monsters_without_hurting_a_green_mushroom! Yahtzee!!!!_You_need_a_6,_or_it's_gonna_be_all_over_baby! Oh_no,_the_energy_orbs_are_coming!_Hehehe_don't_get_zapped! I'm_gonna_close_my_eyes_and_count_to_10._You_better_be_climbing_when_I_open_them! Defeat_5_monsters_within_20_seconds!_Yeah_yeah_move_them_feet!! Ok_uhhmm..._how_about_a_classic_coin_flip?_Look_right_for_heads,_look_left_for_tails! Hmmm..._now_kill_the_monster_closest_to_the_middle_of_the_screen! 'Yawn'..._Uh,_do_100_lines_of_damage_before_I_get_bored_and_self_heal! WHAT?_Who_let_all_these_shrooms_in??!?_Haha_jk_jk_it_was_obviously_me._Ya_got_35_seconds... I_sure_love_my_soda,_it'd_be_a_real_shame_if_any_were_to_get_spilled..._anyway,_go_kill_that_crab_hehe!    ".split(" "), "Aaaaarrrggghhh...._aauuguauauauauauau..._I'm_ded...._hehehehe OOF_OUCHIE!_I'm_gonna_need_an_ice_pack_for_this_one..._pfft_hahahaha!! Awww_ya_got_me_^_hahaha_\\ Oh_jeez,_Lava_ain't_gonna_be_happy_when_I_tell_him_that_you_made_it_this_Far..._erm,_I_mean_dying_noises!!!_Gahh_I'm_dead!! Golly!_You_done_killed_me!_Shucks,_guess_you_get_all_this_loot_now_since_I'm_dead_and_all_that_lol ..._@_I'd_congratulate_you_for_killing_me,_but_I_think_Lava_told_me_that_playing_dead_means_not_talking,_so_I_won't_say_anything... Oh_no_I'm_dead_etc_etc_yada_yada..._ugh_when_is_my_shift_over... Oof_there_goes_my_HP_bar,_guess_you_finally_vanquished_IdleOn's_'FINAL'_Boss...._tehehehe Wow_what_a_fight!_Here,_you_deserve_these_great_items,_after_all_I_am_the_final_boss_and_you_did_kill_me_once_and_for_all_#".split(" "), "0 1 6 7 8 9 11 12 19 28 29 30 31 32 filler filler".split(" "), ["ObolAmarokA", "ObolEfauntA", "ObolChizoarA", "ObolSlush", "ObolTroll"], "96 137 168 159 57 258 247 160 113 308 197 315 325 205 280 330".split(" "), "Slargon Pirate_Porkchop Muhmuguh Poigu Lava_Larry Tired_Mole".split(" "), "Lafu_Shi Hoov Woodlin_Elder Tribal_Shaman Legumulyte Potti Sussy_Gene Spirit_Sungmin Masterius".split(" "), ["Meteor", "rocky", "iceknight", "snakeZ", "frogGR"], ["EquipmentHats78", "EquipmentRingsChat10"], ["EquipmentToolsHatchet11"], ["EquipmentHats79", "ObolKnight"], ["EquipmentTools13"], ["ObolFrog"], "w5a1 w5a2 w5a3 w5a4 w5a5 w5b1 w5b2 w5b3 w5b4 w5b5 w5b6 w5c1 w5c2 Copper Iron Gold Plat Dementia Void Lustre Starfire Dreadlo Godshard FishSmall FishMed Bug2 FishBig w6a1 w6a2 w6a3 w6a4 w6a5 w6b1 w6b2 w6b3 w6b4 w6c1 w6c2 w6d1 w6d2 w6d3 rift1 rift2 rift3 rift4 rift5 w7a1 w7a2 w7a3 w7a4 w7a5 w7a6 w7a7 w7a8 w7a9 w7a10 w7a11 w7a12".split(" "), "6 7 5 6 6 3 10 15 8 5 7 6 6 0 9 0 3 0 7 11 8 4 3 1 5 5 0 7 8 3 -1 10 2 5 5 10 4 4 2 2 0 1 3 10 0 5 5 3 2 4 4 0 5 4 6 0 -2 5 2 5 6 6 12 3 10 0 0 4 8 2 1 3 9 0".split(" "), "7 6 4 -1 9 4 3 5 6 9 5 1 7 0 2 0 6 0 7 4 1 0 -4 3 5 2 6 6 2 -1 -3 7 1 2 2 10 -3 0 3 4 0 1 -1 4 0 2 -1 0 0 -1 3 0 1 1 8 -6 -2 -3 -5 6 0 0 9 3 9 0 0 9 8 -4 4 2 11 0".split(" "), "0 16 3 5 15 20 0 1 3 4 10 22 2 3 11 19 16 6 5 22 21 20 7 12 15 3 8 0 23 9 22 4 21 5 1 13 3 2 24 16 14 17 25 6 4 15 24 7 18 21 5 3 0 9 24 1 6 2 4 23 16 24 25 7 5 8 9 20 16 1".split(" "), "+{%_Drop_Rate +{%_Class_EXP +{%_Skill_EXP +{_Infinite_Star_Signs +{%_Multikill_Per_Tier +{%_Total_Damage +{_Base_STR +{_Base_AGI +{_Base_WIS +{_Base_LUK +{_Tab_1_Talent_Pts +{_Tab_2_Talent_Pts +{_Tab_3_Talent_Pts +{_Tab_4_Talent_Pts +{_Star_Talent_Pts +{%_Faster_Refinery_Speed +{%_Faster_Shiny_Pet_Lv_Up_Rate +{%_Sail_Captain_EXP_Gain +{%_Lower_Minimum_Travel_Time_for_Sailing +{%_Line_Width_in_Lab +{%_Bonuses_from_All_Meals +{%_Higher_Artifact_Find_Chance +{_Base_Efficiency_for_All_Skills +{_Base_Critters_per_Trap +{%_Farming_EXP_gain +{%_Summoning_EXP_gain".split(" "), "1 1 2 2 1 1 2 2 2 2 2 2 2 2 2 2 3 3 1 1 1 2 20 1 1 1".split(" "), "test2;test2 Copy;dez;Beach;testi;testorama;des;Beach2".split(";"), "42 318 497 79 146 362 43 536 165 35".split(" "), "30 185 237 346 238 414 398 412 178 660 879 889 731 867 724 500 501 568 68 382 255 31 554 666 724 514".split(" "), "113 208 113 89 23 191 229 212 172 64 119 88 185 22 155 145 210 111 18 20 40 80 23 43 204 228".split(" "), "9999999 172800 86400 57600 43200 28800 14400 7200 3600".split(" "), "w6a1 w6a1 w6a3 w6a4 w6a4 w6a5 w6b1 w6b2 w6b3 w6b4 w6c1 w6d3 w6d1 w6d2 w6a2".split(" "), "vSpiritA1 vSpiritA2 vSpiritA3 vSpiritA4 vSpiritA5 vSpiritB1 vSpiritB2 vSpiritB3 vSpiritB4 vSpiritC1 vSpiritC2 vSpiritD1 vSpiritD2 vSpiritD3".split(" "), "\u00c2 \u00e2 \u0153 \u0178 \u00d4 \u00d6 \u00f4 \u00c9 \u00c8 \u00c7 \u0152 \u0152\u00e2 \u0152\u0153 \u0152\u0178".split(" "), "Gemstone_Ninja_Knowledge_{_+30%_DROP_RARITY New_Gold_Charms_added_{_+10%_ALL_STAT Bargain_Ninja_Knowledge_{_+5_All_Talent_LV +30_Max_LV_for_Sneaking_Items_{_1.10#_DMG_MULTI Centurion_Ninja_Knowledge_{_+10%_DAILY_CORAL Haha_yea_there's_no_bonus_here_yet. Haha_yea_there's_no_bonus_here_yet. Haha_yea_there's_no_bonus_here_yet.".split(" "), "{}%_Stealth_@_for_all_Ninjas {}%_Jade_@_Gain {}%_Damage_@_to_Doors +}%_Gold_@_Charm_Bonus {}%_Sneak_@_EXP_Gain {}%_Bonuses_@_from_Gemstones $%_Cheaper_@_Upgrades {}_Higher_@_Charm_LVs".split(" "), "Mega-Rare_Drop Rare_Drop LockedInvSpace Blank InvStorage99 GemP16 GemP25 GemP19 GemP9 GemP10 InvBag21 InvBag22 InvBag23 InvBag24 InvBag25 InvBag26 InvStorage31 InvStorage32 InvStorage33 InvStorage34 InvStorage35 InvStorage36 InvStorage37 InvStorage38 InvStorage39 InvStorage40 InvStorage41 InvStorage42 GemP35 EquipmentHats43 Quest31 EquipmentHats36".split(" "), "mushG frogG beanG slimeG snakeG carrotO goblinG plank frogBIG branch acorn jarSand mimicA crabcake coconut sandcastle pincermin poopSmall ratB potato steak moonman sandgiant snailZ sheep flake stache bloque mamoth snowball penguin thermostat glass snakeB speaker eye ram mushP w4a2 w4a3 demonP w4b2 w4b1 w4b3 w4b4 w4b5 w4c1 w4c2 w4c3 w4c4 w5a1 w5a2 w5a3 w5a4 w5a5 w5b1 w5b2 w5b3 w5b4 w5b5 w5b6 w5c1 w5c2 w5b6 w6a1 w6a2 w6a3 w6a4 w6a5 w6b1 w6b2 w6b3 w6b4 w6c1 w6c2 w6d1 w6d2 w6d3".split(" "), "3 2 4 5 106 8 12 6 7 107 118 10 110 116 9 113 11 114 109 108 117 115 112 111".split(" "), "14 17 119 18 120 16 15 21 122 124 19 123 20 121 22 129 125 130 134 128 127 133 24 25 132 131 23 135 26 136 126".split(" "), "28 29 139 35 137 30 142 34 140 141 32 145 31 37 138 38 146 33 144 36 148 147 150 149 39 143".split(" "), "42 41 43 44 45 154 151 47 152 49 48 155 46 52 50 157 53 158 153 56 51 156 164 55 163 57 162 159 167 54 161 58 166 160 165 168 169 59".split(" "), "60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105".split(" "), ["\u62f3", "\u62d6", "\u62d2", "\u62c7", "\u62c5"], "\u62a2 \u62a0 \u626f \u626d \u626b \u6258 \u6253 \u624d \u624b".split(" "), "mushG frogG beanG slimeG snakeG carrotO goblinG plank frogBIG branch acorn mushW poopSmall ratB poopD Crystal0 jarSand mimicA crabcake coconut sandcastle pincermin potato steak moonman sandgiant snailZ Crystal1 sheep flake stache bloque mamoth snowball penguin thermostat glass snakeB speaker eye ram skele2 skele rockS Crystal2 mushP w4a2 w4a3 demonP w4b2 w4b1 w4b3 w4b4 w4b5 w4c1 w4c2 w4c3 w4c4 Crystal3 w5a1 w5a2 w5a3 w5a4 w5a5 w5b1 w5b2 w5b3 w5b4 w5b5 w5b6 w5c1 w5c2 caveA caveB caveC Crystal4 w6a1 w6a2 w6a3 w6a4 w6a5 w6b1 w6b2 w6b3 w6b4 w6c1 w6c2 w6d1 w6d2 w6d3 Crystal5 reindeer mushR shovelR slimeB babayaga poopBig babaHour babaMummy mini3a mini4a mini5a mini6a ghost slimeR sheepB snakeY crabcakeB shovelY Meteor frogGR rocky snakeZ iceknight ChestA1 ChestB1 ChestC1 ChestA2 ChestB2 ChestC2 ChestA3 ChestB3 ChestC3 ChestA4 ChestB4 ChestC4 ChestA5 ChestB5 ChestC5 ChestA6 ChestB6 ChestC6".split(" "), "COPPER_SET IRON_SET AMAROK_SET GOLD_SET PLATINUM_SET EFAUNT_SET DEMENTIA_SET VOID_SET CHIZOAR_SET LUSTRE_SET DIABOLICAL_SET TROLL_SET SECRET_SET MAGMA_SET KATTLEKRUK_SET MARBIGLASS_SET GODSHARD_SET EMPEROR_SET PREHISTORIC_SET".split(" "), ["Snootie", "Sad_Urie", "Bloo_Radley", "Toobus_Goobus"]]

# `ClassNames` in source. Last updated in v2.43 Nov 10.
# Note that this includes skills and various placeholders
ClassNames = "0 BEGINNER JOURNEYMAN MAESTRO VOIDWALKER INFINILYTE RAGE_BASICS WARRIOR BARBARIAN SQUIRE BLOOD_BERSERKER NOPE DIVINE_KNIGHT NOPE DEATH_BRINGER FILLER ROYAL_GUARDIAN FILLER CALM_BASICS ARCHER BOWMAN HUNTER SIEGE_BREAKER NOPE NOPE BEAST_MASTER FILLER FILLER FILLER WIND_WALKER SAVVY_BASICS MAGE WIZARD SHAMAN ELEMENTAL_SORCERER SPIRITUAL_MONK BUBONIC_CONJUROR NOPE FILLER FILLER ARCANE_CULTIST FILLER MINING SMITHING CHOPPING FISHING ALCHEMY BUG_CATCHING TRAPPING CONSTRUCTION WORSHIP COOKING BREEDING LABORATORY SAILING DIVINITY GAMING FARMING SNEAKING SUMMONING SPELUNKING".split(" ")
classes_dict = {index:name.replace('_', ' ').title() for index, name in enumerate(ClassNames) if index < 41}
skill_index_list = ['Combat'] + [name.replace('_', ' ').replace('BUG ', '').title() for name in ClassNames[42:]]
empty_skill_list = [0] * len(skill_index_list)
balloonable_skills_list = [
    "Mining", "Smithing", "Chopping",
    "Fishing", "Alchemy", "Catching",
    "Trapping", "Worship",
    "Cooking",  #"Laboratory" isn't balloonable, oddly enough. You can pearl it though
]
pearlable_skills_list = [
    "Mining", "Smithing", "Chopping",
    "Fishing", "Alchemy", "Catching",
    "Trapping", "Worship",
    "Cooking", "Laboratory",
]

current_world = 7
max_characters = 10

expected_talents_dict = {
    'Beginner': [
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
    ],
    'Journeyman': [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        75, 76, 77, 78, 79,
        #Plus the 3 rows from Journeyman Tab2
        15, 16, 17, 18, 19,  #Top row
        20, 21, 22, 23, 24,  #Middle row
        25, 26, 27, 28, 29  #Bottom row
    ],
    'Maestro': [
        30, 31, 32, 33, 34,
        35, 36, 37, 38, 39,
        40, 41, 42, 43, 44
    ],
    'Voidwalker': [
        45, 46, 47, 48, 49,
        50, 51, 52, 53, 54,
        55, 56, 57, 58, 59
    ],
    #"Infinilyte": [],

    'Warrior': [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        85, 86, 87, 88, 89,
        #Plus the 3 rows from Warrior Tab2
        90, 91, 92, 93, 94,
        95, 96, 97, 98, 99,
        100, 101, 102, 103, 104
    ],
    'Barbarian': [
        105, 106, 107, 108, 109,
        110, 111, 112, 81, 114,
        115, 116, 117, 118, 119
    ],
    'Squire': [
        120, 121, 122, 123, 124,
        125, 111, 127, 81, 129,
        130, 131, 132, 133, 119
    ],
    'Blood Berserker': [
        135, 136, 137, 138, 139,
        140, 141, 142, 143, 144,
        145, 146, 147, 148, 149
    ],
    'Death Bringer': [
        195, 196, 197, 198, 199,
        200, 201, 202, 203, 204,
        205, 206, 207, 208, 209
    ],
    'Divine Knight': [
        165, 166, 167, 168, 169,
        170, 141, 142, 143, 144,
        175, 176, 177, 178, 149
    ],
    #"Royal Guardian": [],

    'Archer': [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        263, 266, 267, 268, 269,
        #Plus the 3 rows from Archer Tab2
        270, 271, 272, 273, 274,
        284, 276, 277, 278, 279,
        280, 281, 282, 283, 265
    ],
    'Bowman': [
        285, 286, 287, 288, 289,
        290, 291, 292, 293, 294,
        295, 296, 297, 298, 299
    ],
    'Hunter': [
        300, 301, 302, 303, 304,
        305, 291, 307, 293, 309,
        310, 311, 312, 313, 299
    ],
    'Siege Breaker': [
        360, 316, 317, 318, 319,
        320, 366, 367, 368, 144,
        325, 326, 327, 328, 374
    ],
    #"Mayheim": [],
    'Beast Master': [
        315, 361, 362, 363, 364,
        365, 366, 367, 368, 144,
        370, 371, 372, 373, 374
    ],
    'Wind Walker': [
        420, 421, 422, 423, 424,
        425, 426, 427, 428, 429,
        430, 431, 432, 433, 434
    ],

    'Mage': [
        #All 3 rows from Tab1
        0, 1, 8, 9, 5,
        10, 11, 12, 13, 6,
        445, 446, 447, 448, 449,
        #Plus the 3 rows from Mage Tab2
        450, 451, 452, 453, 454,
        455, 456, 457, 458, 459,
        460, 461, 462, 464, 463  #Not a typo, 464 is before 463
    ],
    'Wizard': [
        465, 466, 467, 468, 469,
        470, 486, 472, 488, 474,
        475, 476, 477, 478, 494
    ],
    'Shaman': [
        480, 481, 482, 483, 484,
        485, 486, 487, 488, 489,
        490, 491, 492, 493, 494
    ],
    'Elemental Sorcerer': [
        495, 496, 497, 498, 499,
        500, 531, 532, 533, 144,
        505, 506, 507, 508, 539
    ],
    #"Spiritual Monk": [],
    'Bubonic Conjuror': [
        525, 526, 527, 528, 529,
        530, 531, 532, 533, 144,
        535, 536, 537, 538, 539
    ],
    'Arcane Cultist': [
        585, 586, 587, 588, 589,
        590, 591, 592, 593, 594,
        595, 596, 597, 598, 599,
    ],
    'VIP': [
        641, 642, 643, 644, 645
    ],
}
base_crystal_chance = 0.0005  # 1 in 2000
max_crystal_chance = 0.1  #10% last updated in v2.45 Nov 15. Any extra crystal spawn chance above this increases loot and killcount, but not spawns

# `CompanionDB` in source. Last updated in v2.48 Dec 10
companions_info = [
    "babaMummy All_Divinities_from_World_5_count_as_Active 1 -53 -22 -14 2000 140".split(" "),
    "rift2 +25_Lv_for_all_Talents 25 -31 6 -14 450 130".split(" "),
    "ram You_can_use_Storage_Chest_anywhere_in_Quickref 1 -26 16 -19 150 125".split(" "),
    "Crystal3 {100%_Drop_Rate_and_Exp_from_monsters 100 -19 20 -8 150 120".split(" "),
    "sheep All_big_bubbles_in_Alchemy_count_as_equipped 1 -6 0 -11 10 110".split(" "),
    "w5b1 {5%_All_Skill_Efficiency 5 0 0 -5 10 110".split(" "),
    "beanG {5%_AFK_Gains_Rate_for_Fighting_and_Skills 5 -9 0 -22 10 110".split(" "),
    "slimeG +25%_Golden_Balls_earned_in_Arcade_for_Upgrades 1 17 0 -1 5 100".split(" "),
    "jarSand +15_Base_All_Stats_(STR/AGI/WIS/LUK) 15 5 0 -3 5 100".split(" "),
    "bloque +20%_All_Skill_EXP 20 1 0 -17 5 100".split(" "),
    "frogG +10%_Total_Damage 10 12 0 -5 5 100".split(" "),
    "slimeBz Only_100_of_these_exist_in_IdleOn... 10 -48 0 -30 1 10".split(" "),
    "caveC 10x_Total_Damage 9 -44 0 -35 1000 150".split(" "),
    "w6d3 3x_Villager_EXP_and_+25_Opals 1 -29 0 -19 250 130".split(" "),
    "rift3 2x_Kills_for_Opening_Portals_and_Deathnote 1 -21 0 -16 250 135".split(" "),
    "w6b4 3.50x_faster_Equinox_Bar_Fill_Rate 2.5 -23 0 -19 100 120".split(" "),
    "Crystal4 1.75x_Lab_EXP_and_Divinity_EXP_Gain .75 -21 0 -5 100 120".split(" "),
    "w5b6 3d_Printer_samples_grow_{1%/day_for_100_days 1 -17 0 -15 100 120".split(" "),
    "frogBIG {25%_Carry_Capacity_for_all_item_types 25 -13 0 -29 10 110".split(" "),
    "potato {5%_Ballot_Bonus_Multi_(World_2_feature) 5 -46 0 -25 10 110".split(" "),
    "w4b1 {30_Talent_Points_for_all_classes 30 -1 0 -5 10 110".split(" "),
    "frogP +15%_Defence 15 10 0 -5 5 100".split(" "),
    "glass +15%_Drop_Rate 15 -2 0 -5 5 100".split(" "),
    "mushG +15%_Accuracy 15 -8 0 -5 5 100".split(" "),
    "Pet10 4x_Coins_from_Mobs 3 -10 0 -13 500 100".split(" "),
    "Pet12 {50%_AFK_Gains 50 3 0 -20 500 100".split(" "),
    "Pet3 1.30x_Drop_Rate .3 -1 0 0 500 100".split(" "),
    "reindeer 2.00x_Gold_Ball_Shop_Bonuses 1 -40 0 -33 500 135".split(" "),
    "w7d1 {30%_AFK_gains_for_World_7_skills,_and_{1_World_Class_Showcase_Slot_(Grade_4) 30 -30 0 -48 500 200".split(" "),
    "Pet0 1.50x_Kills_for_Opening_Portals_and_Deathnote .5 6 0 -8 100 80".split(" "),
    "Pet1 2x_Friend_Bonuses,_{2_Friend_Bonus_Slots,_Auto_Loot,_Storage_Quickref_Usage,_Infinite_Teleporting 1 4 0 -5 100 100".split(" "),
    "Pet2 Bababooey! 3 2 0 -8 100 15".split(" "),
    "Pet4 2x_Class_EXP_gain_and_2x_All_Skill_EXP_gain 1 -2 0 -13 100 120".split(" "),
    "Pet5 2x_Total_Damage,_and_2x_Class_EXP_gain 1 -2 0 -10 100 15".split(" "),
    "Pet6 3x_Class_EXP_gain 2 2 0 -9 100 15".split(" "),
    "Pet8 2x_Refinery_Salts_produced_(affects_POW_produced_in_Refinery) 1 -5 0 -13 100 15".split(" "),
    "Pet11 {200%_Gold_Balls_gained_from_the_Arcade, 200 -4 0 -11 100 15".split(" "),
    "w7e1 10x_Class_EXP_and_{10_Legend_Talent_PTS 1 -10 20 -33 1000 150".split(" "),
    "w7a5 4x_Masterclass_drops_(Bones/Dust/Tachyon) 3 -54 0 -15 250 140".split(" "),
    "w7a8 +50%_Meritocracy_Bonus_Multi_(World_7_feature) 50 -15 30 -7 250 130".split(" "),
    "w7a4 1.75x_Daily_Reef_Coral_(World_7_feature) .75 -10 20 -19 100 120".split(" "),
    "Crystal6 {40%_Ballot_Bonus_Multi_(World_2_feature) 40 -17 0 -14 100 120".split(" "),
    "w7a3 {1_Grade_for_2_Gallery_Showcases_(World_7_feature) 2 -9 28 -17 100 120".split(" "),
    "w7a7 1.25x_Artifact_Find_chance_(World_5_feature) .25 -4 0 -19 10 110".split(" "),
    "w7a10 {1_Friend_Bonus_slot 1 -9 0 -15 10 110".split(" "),
    "w7a1 1.50x_Coins_from_monsters .50 6 0 -5 10 110".split(" "),
    "coconut +15%_faster_Alchemy_Brew_Speed 15 -4 0 -24 5 100".split(" "),
    "snakeG +10%_Class_EXP 10 3 0 -9 5 100".split(" "),
    "mushP +5%_Golden_Food_bonus 5 -10 0 -11 5 100".split(" "),
    "bubba {30%_Gallery_Bonus_Multi_(World_7_feature) 30 -29 0 -37 5 100".split(" "),
]

companions_data = {
    monster_data[companion[0]]['Name']: {
        'Id': index,
        'Image': '-'.join(monster_data[companion[0]]['Name'].lower().split(' ')),
        'Code': companion[0],
        'Description': companion[1].replace('_', ' ').replace('{', '+'),
        'Value': float(companion[2]) + (1 * companion[2].startswith('.')),
        # Placeholder: companion[3],
        # Placeholder: companion[4],
        # Placeholder: companion[5],
        # Placeholder: companion[6],
    } for index ,companion in enumerate(companions_info)
}

# `NinjaInfo` in source. Last updated in v2.43 Nov 10. Make sure to manually turn any `.split("")` into `.split(" ")`
NinjaInfo = ["0 0 0 0 0 0 0 0 0 0 0 0".split(" "), "0 0 13 19 21 22 10 21 17 15 8 18".split(" "), "0 0 0 0 0 0 0 0 0 0 0 0".split(" "), "1 150 800 5000 25000 200000 1500000 20000000 100000000 2000000000.0 40000000000.0 45000000000000.0".split(" "), "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 0 1 2 4 2 1 0 -1 -7 -5 -3 -3 -5 -7 -5 -3 -3 -5 -7 0 -1 -1 0 -1 0 0 0 0 0 0 0 0 0 -1 -1 0 0 -1 -1 -1 -1 -1 0 -1 -2 0 2 1 0 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 0 2 2 2 2 0 0 0 1 1 1 2 3 5 10 7 7 7 7 7 7 7 7".split(" "), "0 0 -1 -1 0 1 0 -1 0 0 -1 -1 0 0 -1 -1 1 0 0 0 2 1 1 2 4 3 3 3 3 2 1 0 0 -1 -2 -1 0 0 -1 -2 -1 0 5 5 4 4 5 5 5 5 6 2 1 2 6 5 0 -1 -1 -1 -1 0 1 1 0 -1 -2 -2 -1 1 0 -1 -1 -1 2 2 1 1 1 2 3 2 2 2 3 3 3 3 2 2 0 1 2 5 4 5 8 22 21 21 21 21 21 21 21 21".split(" "), "0 200 650 150 350 720 180 600 760 300 170 650".split(" "), "0 2 3 4 4 5 6 6 6 7 10 11".split(" "), "0 10 60 750 3000 17000 80000 500000 1500000 7000000 30000000 200000000.0".split(" "), "0.01 15 80 500 2500 8000 40000 170000 800000 3000000 10000000 20000000.0".split(" "), "0 100 300 1500 6000 17500 60000 170000 800000 4000000 15000000 60000000.0".split(" "), "25 40 150 1150 2000 14000 25000 170000 200000 2250000 5000000 25000000.0".split(" "), ["NjItem2", "0.001", "NjItem0", "0.10"], "NjItem0 0.05 NjTr0 0.2 NjTr8 0.3 NjItem1 0.05 NjItem14 0.03 NjWep0 0.15".split(" "), "NjItem5 0.04 NjTr15 0.15 NjTr13 0.17 NjTr5 0.2 NjWep1 0.15".split(" "), "NjItem3 0.02 NjItem11 0.04 NjTr7 0.17 NjTr9 0.2 NjWep5 0.15".split(" "), "NjItem9 0.03 NjItem10 0.01 NjTr10 0.17 NjTr4 0.2 NjWep2 0.15".split(" "), "NjItem12 0.04 NjTr14 0.17 NjTr11 0.2 NjWep6 0.15".split(" "), "NjItem4 0.03 NjTr18 0.17 NjTr1 0.2 NjWep3 0.15".split(" "), "NjItem13 0.02 NjTr2 0.17 NjGl0 0.08 NjTr6 0.2 NjWep7 0.15".split(" "), "NjItem6 0.005 NjTr12 0.17 NjTr16 0.23 NjWep4 0.15".split(" "), "NjItem7 0.001 NjGl1 0.05 NjTr17 0.21 NjWep8 0.15".split(" "), "NjItem8 0.0005 NjGl2 0.04 NjTr3 0.2".split(" "), ["NjItem2", "0.0001", "NjTr19", "0.2"], "0 12 5 8 22 27 18 1 17 24 19 25 13 16 26 7 9 23 14 20 28 2 3 15 10 11 6 21 35 30 34 37 29 31 32 4 36 33 38 39 40 41 42 43 44 45 46 47 48 49".split(" "), "14 1530 105 90 0 50 Artifact_Attraction Artifact_find_chance_is_1.5x_higher!_If_you've_found_all_artifacts_at_max_rarity,_then_this_bonus_changes_to_1,000x_artifact_find_chance!".split(" "), "15 1630 365 90 0 25 Slab_Sovereignty All_bonuses_given_by_the_Slab_are_1.25x_higher!".split(" "), "16 1790 250 90 0 50 Spiritual_Growth Boosts_EXP_multi_for_all_three_World_6_skills_by_+50%!".split(" "), "17 1950 195 90 0 30 Depot_Studies_PhD All_bonuses_given_at_the_Crop_Depot_are_1.30x_higher!".split(" "), "41 6 PeanutG 12 292 ButterBar 34 52 FoodG1 97 179 FoodG2 28 221 FoodG3 100 52 FoodG4 42 148 FoodG5 121 213 FoodG6 94 135 FoodG7 4 174 FoodG8 95 287 FoodG9 -2 246 FoodG10 78 236 FoodG11 85 10 FoodG12 63 101 FoodG13 51 267 FoodG14 61 196 FoodG15".split(" "), "slimeB poopBig babayaga babaHour babaMummy mini3a mini4a mini5a mini6a".split(" "), "+{%_DMG }x_Gaming_Evo +{%_Jade }x_Meal_Spd +{%_Cash +{%_Pet_Rate +{_Critters +{%_DR +{%_Spelunky".split(" "), "5 11 3 65 22 0 2 1 7 4 6 81 8 9 53 10 107 12 106 75 13 14 80 79 25 15 16 17 18 19 21 23 24 26 27 28 29 85 86 30 31 32 33 34 35 37 36 76 38 54 40 41 42 39 44 50 48 46 47 49 51 52 45 55 60 57 61 62 66 59 64 63 58 56 93 84 83 92 91 87 88 89 82 94 68 69 67 77 78 72 74 99 71 70 73 96 20 43 90 100 101 95 97 103 104 98 102 105".split(" "), "+{%_DMG +{%_Skill_Eff +{%_Drop_Rarity +{%_STR +{%_AGI +{%_WIS".split(" "), "Evolution_Boost Production_Boost Soil_Exp_Boost Evolution_Megaboost Seed_of_Stealth Farmtastic_Boost Soil_Exp_Megaboost Overgrowth_Boost Production_Megaboost Seed_of_Loot Evolution_Superboost Overgrowth_Megaboost Farmtastic_Megaboost Soil_Exp_Superboost Seed_of_Damage Evolution_Ultraboost Farmtastic_Superboost Production_Superboost Overgrowth_Superboost Seed_of_Stats".split(" "), "Increases_next_crop_chance_by_+{%_per_rank_of_the_land_plot Boosts_value_of_crops_harvested_by_+{%_per_rank_of_the_land_plot Each_land_gains_+{%_extra_Rank_EXP_per_rank_of_the_previous_land Increases_next_crop_chance_by_+{%_multiplicatively! Increases_the_Stealth_of_all_Ninja_Twins_by_+{%_per_Farming_LV Increases_Farming_Skill_EXP_gained_by_+{% All_plots_of_land_gain_+{%_more_Rank_EXP Increases_chance_for_Overgrowth_by_+{% Increases_the_amount_of_crops_harvested_by_+{% Increases_the_Drop_Rarity_of_all_characters_by_+{% Increases_next_crop_chance_by_+{%_multiplicatively! Increases_chance_for_Overgrowth_by_+{% Increases_Farming_Skill_EXP_gained_by_+{% All_plots_of_land_gain_+{%_more_Rank_EXP Gives_a_+{%_Total_Damage_bonus_to_all_characters Increases_next_crop_chance_by_+{%_multiplicatively! Increases_Farming_Skill_EXP_gained_by_+{% Increases_the_amount_of_crops_harvested_by_+{% Increases_chance_for_Overgrowth_by_+{% Gives_a_+{%_All_Stat_bonus_to_your_characters".split(" "), "250 5 25 600 2 90 200 120 100 10 3000 340 110 520 20 40000 220 600 1500 5".split(" "), "1 5 20 30 60 80 125 180 250 400 500 600 700 900 1200 1300 1500 1750 2000 3500".split(" "), "All_your_characters_deal_}x_more_damage_to_enemies 25 0 All_your_characters_deal_}x_more_damage_to_enemies 25 0 Increases_STR_AGI_WIS_and_LUK_for_all_characters_by_+{% 15 0 Increases_Defence_and_Accuracy_by_+{%_for_all_characters 30 0 Logging_in_each_day_gives_+{_more_GP_to_your_guild_than_you_normally_do 30 0 }x_Kill_per_Kill,_making_monster_kills_worth_more_for_portals_and_Deathnote 20 0 +{%_AFK_gain_for_both_fighting_and_skills_for_all_characters 15 0 Boosts_all_Mining_EXP_gain_and_Mining_Efficiency_by_+{% 42 0 Boosts_all_Fishing_EXP_gain_and_Fishing_Efficiency_by_+{% 50 0 Boosts_all_Choppin'_EXP_gain_and_Choppin'_Efficiency_by_+{% 38 0 Boosts_all_Catching_EXP_gain_and_Catching_Efficiency_by_+{% 46 0 Increases_the_amount_of_resources_produced_by_the_3D_Printer_by_}x 20 3 Boosts_liquid_generation_rate_for_all_Alchemy_liquids_by_+{% 25 0 Boosts_all_Cooking_EXP_gain_and_Cooking_Speed_by_+{% 63 4 Boosts_Dungeon_Credit_and_Dungeon_Flurbo_gain_by_}x 50 0 All_your_characters_gain_+{%_more_Class_EXP_from_monsters 60 0 Speeds_up_Egg_Incubation_time_and_Breeding_EXP_gain_by_+{% 50 4 Boosts_Sigil_EXP_gain_by_}x,_still_requires_Sigils_active_in_Lab 80 4 Boosts_Construction_Build_Rate_and_Construction_EXP_gain_by_+{% 40 3 Boosts_Shrine_EXP_gain_by_a_staggering_}x 53 3 Boosts_Artifact_Find_chance_in_Sailing_by_}x 31 5 Boosts_New_Species_chance_when_using_DNA_in_Gaming_by_}x 80 5 Find_+{%_more_Gold_Nuggets_when_digging_with_the_Shovel_in_Gaming 75 5 Boosts_Divinity_PTS_gain_by_}x_and_Divinity_EXP_Gain_by_+{% 60 5 Boosts_Sailing_Captain_EXP_gain_and_Sailing_Speed_by_}x 50 5 Boosts_Sneaking_Stealth_by_}x_and_EXP_Gain_by_+{%_for_all_your_Ninja_Twins 65 6 Boosts_bonuses_from_all_Golden_Food_by_+{% 30 0 Increases_Drop_Rate_for_all_your_characters_by_+{% 38 0 Boosts_Summoning_EXP_gain_by_+{%_and_all_Essence_gained_by_}x 40 6 Boosts_Crop_Value,_and_Farming_EXP_gain,_AND_Next_Crop_Chance_by_+{% 40 6 Increases_Trapping_EXP_gain_and_Worship_EXP_gain_by_+{% 54 3 Increases_Lab_EXP_gain_by_+{% 90 4 Boosts_Equinox_Bar_Fill_rate_by_}x 40 3 Boosts_Refinery_Cycle_Speed_by_+{% 50 3 Increases_cash_earned_from_monsters_by_+{% 52 0".split(" "), "Golden_Tome_@_Adds_a_new_DMG_Multi_bonus_type_to_the_Tome_in_World_4 25 Stamp_Stack_@_Get_+3_Stamp_LVs_every_day_for_a_random_Stamp 30 Bubble_Broth_@_Get_+5_LVs_for_a_random_Alchemy_Bubble_every_day 20 Equinox_Enhancement_@_Get_1.5x_faster_Bar_Fill_Rate_in_Equinox_Valley_in_World_3 15 Supreme_Wiring_@_+2%_Printer_Output_per_day,_taking_new_sample_resets_this 45 Sleepy_Joe_Armstrong_@_+20%_AFK_Gains_for_all_things_IdleOn_related 25 Village_Encouragement_@_All_Villagers_in_World_5_Camp_get_1.25x_EXP_Gain 30 Gilded_Vote_Button_@_Get_+17%_higher_Ballot_Bonus_Multi_from_Voting 35 Extra_Page_@_Get_+1_more_Filter_Page._Find_it_on_the_left_side_of_Cards 20 Coin_Stacking_@_Get_a_1.50x_multiplier_to_ALL_coin_gain,_and_profit_big_time! 15 Storage_Chest_@_Get_+12_storage_slots_for_your_storage_chest 15 Storage_Vault_@_Get_+16_storage_slots_for_your_storage_chest 32 Secret_Pouch_@_Get_+3_Inventory_slots_for_your_Items_Backpack 27 Ribbon_Connoisseur_@_Get_+3_more_ribbons_every_day_for_your_Ribbon_Shelf 35 Golden_Square_@_Get_+1_Trimmed_Construction_slot,_which_has_3x_speed! 23 Summoning_Star_@_Get_+10_Summoning_Doublers,_used_on_Summoning_Upgrades! 30 Royal_Vote_Button_@_Get_+30%_higher_Ballot_Bonus_Multi_instead_of_+17% 25 Extra_Page_@_Get_+1_more_Filter_Page._Find_it_on_the_left_side_of_Cards 22 Extra_Exaltedness_@_Get_+1_Exalted_Stamp_use,_and_+20%_Exalt_Bonus. 35 Smiley_Statue_@_All_statues_give_1.30x_higher_bonuses,_forever! 30 Government_Subsidy_@_Get_1.60x_more_coins_from_defeating_monsters! 17 Automated_Mail_@_Get_+5_Boxes_at_the_Post_Office_every_day_you_play! 15 Friendly_Slot_@_Adds_+1_more_slot_for_your_Friend_Bonuses_in_Codex! 12 Fossil_Meritocracy_@_Get_+20%_higher_Meritocracy_Bonus_in_World_7 45 Bonus_Points_@_You_now_earn_1.5x_PTS_for_the_Hoops_and_Darts_shops! 20 Coolral_@_Boosts_daily_gain_for_the_Coral_Reef_in_W7_by_1.30x 30 Plain_Showcase_@_Get_+1_more_trophy_slot_for_the_Gallery_in_World_7 35".split(" "), "ForestBOSS zDesertNightZboss ySnowCBOSS xSpaceaaTown wLavaCBOSS vSpiritCBOSS ySnowD3 xSpaceRift".split(" "), "Multiplies_everything_in_the_game_by_1.00x 0 0 Multiplies_all_Gaming_Bits_gained_by_}x 700 0 Multiplies_your_chance_to_get_Double_Snail_Mail_each_day_by_}x 150 0 Kattlekruk_gives_}x_more_Bubble_LVs_than_normal_each_day 200 0 Multiplies_how_many_Shiny_Critters_you_get_from_Trapping_by_}x 400 0 Multiplies_your_Total_Damage_dealt_to_monsters_by_}x 200 0 Multiplies_all_the_Jade_your_ninja_twins_find_by_}x 900 0 Multiplies_your_Monument_Reward_Multi_by_}x 200 0 Multiplies_your_total_Palette_Luck_in_Gaming_by_}x 200 0 The_Bonus_Ballo..._ugh,_THAT_guy..._the_Bonus_Ballot's_stuff_is_like_}x_more_or_whatever... 100 0 Multiplies_Skill_EXP_gain_by_}x 125 0 You_get_}x_more_Ribbons_added_to_your_Ribbon_Shelf_every_day 100 0 Multiplies_Feather_and_Fish_production_Rate_by_}x_for_your_friends_Orion_and_Poppy 9900 0 Your_Beryllium_atom_creates_}x_more_PO_Boxes_each_day_while_still_using_up_just_1_Silver_Pen 200 0 All_material_costs_for_upgrading_Stamp_Max_LV_are_}x_lower 100 0 You're_guaranteed_}x_more_Crystal_Mobs_than_normal_to_start_each_day 900 0 Get_}x_more_Worship_PTS_while_playing_Tower_Defence 100 0 Stamina_Regeneration_Rate_in_Spelunking_is_}x_faster 200 0 Multiplies_the_chance_for_Killroy_Skulls_to_drop_by_}x 200 0 When_you_claim_48hrs_or_less_of_AFK_gains_on_a_Masterclass,_you_get_}x_more_AFK_items 200 0 All_of_your_Vials_give_}x_higher_bonuses_than_normal 50 0 All_of_your_Sigils_give_}x_higher_bonuses_than_normal 40 0 All_of_your_Starsigns_give_}x_higher_bonuses_than_normal 60 0 All_of_your_Slab_give_}x_higher_bonuses_than_normal 30 0 Your_Brain_Coral_gives_}x_more_daily_LVs_for_your_Grind_Time_bubble 200 0 All_masterclasses_find_}x_more_Bones,_Dust,_and_Tachyons 200 0 All_of_your_Statue_give_}x_higher_bonuses_than_normal 50 0 Multiplies_Class_EXP_gain_by_}x 150 0".split(" ")]


def getAllSkillLevelsDict(inputJSON, playerCount):
    allSkillsDict = {
        'Skills': {skill: [] for skill in skill_index_list}
    }
    for characterIndex in range(0, playerCount):
        if characterIndex not in allSkillsDict:
            allSkillsDict[characterIndex] = {}
        try:
            characterSkillList = [parse_number(skill_level) for skill_level in inputJSON[f'Lv0_{characterIndex}']]
        except:
            characterSkillList = empty_skill_list
            logger.exception(f"Could not retrieve LV0_{characterIndex} from JSON. Setting character to all 0s for levels")
        for skillCounter in range(0, len(skill_index_list)):
            try:
                allSkillsDict[characterIndex][skill_index_list[skillCounter]] = characterSkillList[skillCounter]
                allSkillsDict['Skills'][skill_index_list[skillCounter]].append(characterSkillList[skillCounter])
            except:
                allSkillsDict[characterIndex][skill_index_list[skillCounter]] = 0
                allSkillsDict['Skills'][skill_index_list[skillCounter]].append(0)
                logger.exception(f"Unable to retrieve Lv0_{characterIndex}'s Skill level for {skill_index_list[skillCounter]}")
    return allSkillsDict


def getHumanReadableClasses(classNumber):
    return classes_dict.get(classNumber, f"Unknown class: {classNumber}")


def getSpecificSkillLevelsList(desiredSkill: str | int) -> list[int]:
    if isinstance(desiredSkill, str):
        try:
            return session_data.account.all_skills[desiredSkill]
        except:
            logger.exception(f"Could not retrieve skill data for {desiredSkill}")
            return empty_skill_list
    elif isinstance(desiredSkill, int):
        try:
            return session_data.account.all_skills[skill_index_list[desiredSkill]]
        except:
            logger.exception(f"Could not find Index for desiredSkill of {desiredSkill}")
            return empty_skill_list

def lavaFunc(funcType: str, level: int, x1: int | float, x2: int | float, roundResult=False):
    match funcType:
        case 'add':
            if x2 != 0:
                result = (((x1 + x2) / x2 + 0.5 * (level - 1)) / (x1/x2)) * level * x1
            else:
                result = level * x1
        case 'decay':
            result = (level * x1) / (level + x2)
        case 'intervalAdd':
            result = x1 + math.floor(level / x2)
        case 'decayMulti':
            result = 1 + (level * x1) / (level + x2)
        case 'bigBase':
            result = x1 + x2 * level
        case 'pow':
            result = safer_math_pow(x1, level)
        case _:
            result = 0
    if roundResult:
        return round(result)
    else:
        return result
