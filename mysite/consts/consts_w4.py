import math

from utils.safer_data_handling import safer_math_pow
from utils.logging import get_logger
from utils.number_formatting import parse_number

logger = get_logger(__name__)

tomepct = {
    95: 765,
    90: 1221,
    80: 2217,
    70: 3676,
    60: 6368,
    50: 9859,
    25: 20303,
    10: 24903,
    5: 26691,
    1: 29154,
    0.5: 29717,
    0.1: 30559,
}
# Last pulled from Tome = function () in code in v2.35
tome_challenges = ["Stamp_Total_LV 10000 0 800 filler filler".split(" "), "Statue_Total_LV 2300 0 350 filler filler".split(" "), "Cards_Total_LV 1344 2 350 filler filler".split(" "), "Total_Talent_Max_LV_膛_(Tap_for_more_info) 12000 0 400 filler For_each_talent,_the_tome_counts_the_highest_Max_LV_out_of_all_your_players.".split(" "), "Unique_Quests_Completed_膛 323 2 300 filler Doing_the_same_quest_on_multiple_players_doesn't_count_for_this.".split(" "), "Account_LV 5500 0 900 filler filler".split(" "), "Total_Tasks_Completed 470 2 470 filler filler".split(" "), "Total_Achievements_Completed 266 2 750 filler filler".split(" "), "Most_Money_held_in_Storage 25 1 300 filler filler".split(" "), "Most_Spore_Caps_held_in_Inventory_at_once 9 1 200 filler filler".split(" "), "Trophies_Found 21 2 660 filler filler".split(" "), "Account_Skills_LV 15000 0 750 filler filler".split(" "), "Best_Spiketrap_Surprise_round 13 2 100 filler filler".split(" "), "Total_AFK_Hours_claimed 2000000 0 350 filler filler".split(" "), "DPS_Record_on_Shimmer_Island 20 1 350 filler filler".split(" "), "Star_Talent_Points_Owned 2500 0 200 filler filler".split(" "), "Average_kills_for_a_Crystal_Spawn_膛 30 3 350 filler In_other_words,_the_chance_for_a_crystal_mob_spawn_on_kill,_so_1_in_N.".split(" "), "Dungeon_Rank 30 0 250 filler filler".split(" "), "Highest_Drop_Rarity_Multi 40 0 350 1 filler".split(" "), "Constellations_Completed 49 2 300 filler filler".split(" "), "Most_DMG_Dealt_to_Gravestone_in_a_Weekly_Battle_膛 300000 0 200 filler Gravestone_appears_when_you_defeat_all_weekly_bosses._This_is_the_negative_number_shown_after.".split(" "), "Unique_Obols_Found 107 2 250 filler filler".split(" "), "Total_Bubble_LV 200000 0 1000 filler filler".split(" "), "Total_Vial_LV 962 2 500 filler filler".split(" "), "Total_Sigil_LV 72 2 250 filler filler".split(" "), "Jackpots_Hit_in_Arcade 1 0 50 filler filler".split(" "), "Post_Office_PO_Boxes_Earned 20000 0 300 filler filler".split(" "), "Highest_Killroy_Score_on_a_Warrior 3000 0 200 filler filler".split(" "), "Highest_Killroy_Score_on_an_Archer 3000 0 200 filler filler".split(" "), "Highest_Killroy_Score_on_a_Mage 3000 0 200 filler filler".split(" "), "Fastest_Time_to_kill_Chaotic_Efaunt_(in_Seconds) 10 3 200 filler filler".split(" "), "Largest_Oak_Log_Printer_Sample 9 1 400 filler filler".split(" "), "Largest_Copper_Ore_Printer_Sample 9 1 400 filler filler".split(" "), "Largest_Spore_Cap_Printer_Sample 9 1 300 filler filler".split(" "), "Largest_Goldfish_Printer_Sample 9 1 300 filler filler".split(" "), "Largest_Fly_Printer_Sample 9 1 300 filler filler".split(" "), "Best_Non_Duplicate_Goblin_Gorefest_Wave_膛 120 0 200 filler Non_Duplicate_means_you_can_only_place_1_of_each_Wizard_Type,_2_or_more_invalidates_the_attempt.".split(" "), "Total_Best_Wave_in_Worship 1000 0 300 filler filler".split(" "), "Total_Digits_of_all_Deathnote_Kills_膛 700 0 600 filler For_example,_1,520_kills_would_be_4_digits,_and_this_is_for_all_monster_types.".split(" "), "Equinox_Clouds_Completed 31 2 750 filler filler".split(" "), "Total_Refinery_Rank 120 0 450 filler filler".split(" "), "Total_Atom_Upgrade_LV 150 0 400 filler filler".split(" "), "Total_Construct_Buildings_LV 3000 0 600 filler filler".split(" "), "Most_Tottoise_in_Storage_膛 7 1 150 filler Tottoise_is_the_11th_Shiny_Critter_unlocked_from_the_Jade_Emporium_in_World_6".split(" "), "Most_Greenstacks_in_Storage_膛 150 0 600 filler Greenstack_is_when_you_have_10,000,000_or_more_of_a_single_item_in_your_Storage_Chest.".split(" "), "Rift_Levels_Completed 49 2 500 filler filler".split(" "), "Highest_Power_Pet 8 1 150 filler filler".split(" "), "Fastest_Time_reaching_Round_100_Arena_(in_Seconds) 50 3 180 filler filler".split(" "), "Total_Kitchen_Upgrade_LV 8000 0 200 filler filler".split(" "), "Total_Shiny_Pet_LV 750 0 250 filler filler".split(" "), "Total_Cooking_Meals_LV 5400 0 750 filler filler".split(" "), "Total_Pet_Breedability_LV 500 2 200 filler filler".split(" "), "Total_Lab_Chips_Owned 100 0 150 filler filler".split(" "), "Total_Colosseum_Score 10 1 200 filler filler".split(" "), "Most_Giants_Killed_in_a_Single_Week 25 0 250 filler filler".split(" "), "Total_Onyx_Statues 28 2 450 filler filler".split(" "), "Fastest_Time_to_Kill_200_Tremor_Wurms_(in_Seconds) 30 3 150 filler filler".split(" "), "Total_Boat_Upgrade_LV 10000 0 200 filler filler".split(" "), "God_Rank_in_Divinity 10 0 200 filler filler".split(" "), "Total_Gaming_Plants_Evolved 100000 0 200 filler filler".split(" "), "Total_Artifacts_Found_膛 132 2 800 filler Rarer_versions_of_an_artifact_count_for_more,_so_Ancient_would_count_as_2_Artifacts.".split(" "), "Gold_Bar_Sailing_Treasure_Owned 14 1 200 filler filler".split(" "), "Highest_Captain_LV 25 0 150 filler filler".split(" "), "Highest_Immortal_Snail_LV 25 2 150 filler filler".split(" "), "Best_Gold_Nugget 9 1 200 filler filler".split(" "), "Items_Found 1590 2 1000 filler filler".split(" "), "Most_Gaming_Bits_Owned 45 1 250 filler filler".split(" "), "Highest_Crop_OG 6 1 200 filler filler".split(" "), "Total_Crops_Discovered 120 2 350 filler filler".split(" "), "Total_Golden_Food_Beanstacks_膛 28 2 400 filler Supersized_Gold_Food_Beanstacks_count_as_2_Beanstacks.".split(" "), "Total_Summoning_Upgrades_LV 10000 0 200 filler filler".split(" "), "Total_Career_Summoning_Wins_膛 160 0 500 filler Rack_up_those_wins!_Endless_Summoning_wins_count_for_this_too,_of_course!".split(" "), "Ninja_Floors_Unlocked 12 2 250 filler filler".split(" "), "Familiars_Owned_in_Summoning_膛 600 0 150 filler Measured_in_terms_of_Grey_Slime,_so_a_Vrumbi_would_count_as_3,_Bloomy_as_12,_and_so_on.".split(" "), "Jade_Emporium_Upgrades_Purchased 38 2 500 filler filler".split(" "), "Total_Minigame_Highscore_膛 450 2 100 filler This_is_Choppin_game,_Mining_Cart_game,_Fishing_game,_Catching_Hoops_game,_and_Trapping_game".split(" "), "Total_Prayer_Upgrade_LV 673 2 200 filler filler".split(" "), "Total_Land_Rank_膛 5000 0 200 filler Land_Ranks_are_from_the_Farming_skill,_in_World_6._Unlocked_from_the_Night_Market!".split(" "), "Largest_Magic_Bean_Trade 1000 0 200 filler filler".split(" "), "Most_Balls_earned_from_LBoFaF_膛 1000 0 150 filler LBoFaF_means_Lava's_Ballpit_of_Fire_and_Fury,_the_bonus_round_in_Arcade".split(" "), "Total_Arcade_Gold_Ball_Shop_Upgrade_LV 3800 2 300 filler filler".split(" "), "Vault_Upgrade_bonus_LV 500 2 500 filler filler".split(" "), "Total_Gambit_Time_(in_Seconds)_膛 3600 0 400 filler Gambit_is_the_14th_Cavern_in_The_Hole.".split(" "), "Total_Digits_of_all_Cavern_Resources_膛 500 0 750 filler For_example,_if_you_had_1273_gravel_and_422_gold_dust,_thats_7_Digits._If_you_then_got_23_quaver_notes_from_harp,_thats_another_2_digits,_making_your_total_9_Digits.".split(" "), "Total_LV_of_Cavern_Villagers 200 0 350 filler filler".split(" "), "Megafeathers_Earned_from_Orion 12 0 100 filler filler".split(" "), "Megafish_Earned_from_Poppy 12 0 100 filler filler".split(" "), "Best_Bravery_Monument_Round_膛 50 0 250 filler Bravery_Monument_is_the_4th_Cavern_in_The_Hole._The_Hole_is_found_in_World_5.".split(" "), "Best_Justice_Monument_Round_膛 200 0 250 filler Justice_Monument_is_the_10th_Cavern_in_The_Hole._'Best_Round'_here_means_your_highest_Court_Case_reached_in_a_run.".split(" "), "Best_Wisdom_Monument_Round_膛 18 2 350 filler Wisdom_Monument_is_the_13th_Cavern_in_The_Hole.".split(" "), "Best_Deathbringer_Max_Damage_in_Wraith_Mode_膛 9 1 400 filler Deathbringer_is_the_Blood_Berserker's_Master_Class,_given_by_Masterius_NPC_in_World_6._You_need_to_open_your_grimoire_btw.".split(" "), "Best_Dawg_Den_score_膛 7 1 250 filler The_Dawg_Den_is_the_3rd_Cavern_in_The_Hole._The_Hole_is_found_in_World_5.".split(" "), "Total_Resource_Layers_Destroyed_膛 150 0 350 filler Destroying_Layers_includes_the_following_caverns..._Motherlode,_Eternal_Hive,_and_Evertree_Cavern,_with_more_added_later!".split(" "), "Total_Opals_Found 500 0 400 filler filler".split(" "), "Best_Pure_Memory_Round_Reached_膛 13 2 50 filler Yea_nah,_I_aint_snitchin'._This_is_a_SECRET_mode.".split(" "), "Spirited_Valley_Emperor_Boss_Kills_膛 100 2 400 filler This_counts_your_current_Showdown_for_the_Emperor_boss_in_World_6,_not_the_total_amount_of_kills.".split(" ")]
tome_challenges_count = len(tome_challenges)
# Formula last pulled from _customBlock_Summoning."TomeLvReq" in code in v2.35
def get_final_combat_level_required_for_tome() -> int:
    return 40 * tome_challenges_count + (5 * max(0, tome_challenges_count - 35) + 10 * max(0, tome_challenges_count - 60)) + 350


max_cooking_tables = 10  # Last verified as of v2.34
max_meal_count = 67  # Last verified as of v2.34
max_meal_level = 110  # Last verified as of v2.34
max_cooking_ribbon = 23
cooking_close_enough = 300  # Last adjusted v2.34
cooking_meal_dict = {
    0:{"Name": "Turkey a la Thank", "Description": "Do I smell gratitude? Oh, no, that's colonialization...", "Effect": "+{% Total Damage", "BaseValue": 2},
    1:{"Name": "Egg", "Description": "It's just an egg.", "Effect": "+{% Meal Cooking Speed", "BaseValue": 5},
    2:{"Name": "Salad", "Description": "Yea uhm, could I get a burger, but hold the meat and buns?", "Effect": "+{% Cash from Monsters", "BaseValue": 3},
    3:{"Name": "Pie", "Description": "Cartoon characters with a fear of levitation HATE the smell of this!", "Effect": "+{% New Recipe Cooking Speed", "BaseValue": 5},
    4:{"Name": "Frenk Fries", "Description": "You're breeding pets in outer space, don't be shocked that there's no France!", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 5},
    5:{"Name": "Spaghetti", "Description": "Your mom made this. It's her spaghetti.", "Effect": "+{% Breeding EXP", "BaseValue": 4},
    6:{"Name": "Corn", "Description": "To think the government is subsidizing this... its bonus is terrible!!!", "Effect": "+{% Skill Efficiency", "BaseValue": 2},
    7:{"Name": "Garlic Bread", "Description": "The letter H ain't lookin' so good after eating a few of these...", "Effect": "+{% VIP Library Membership", "BaseValue": 4},
    8:{"Name": "Garlicless Bread", "Description": "Many revolutions in the world originate from an increase in the price of bread", "Effect": "+{% Lab EXP", "BaseValue": 2},
    9:{"Name": "Pizza", "Description": "Mama mia mahhh piiiiiiiizzza!!! Wait I already did that joke, replace this one", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 9},
    10:{"Name": "Apple", "Description": "Aw jeez Richard, I sure am hungry for apples!", "Effect": "+{ Base DEF", "BaseValue": 5},
    11:{"Name": "Pancakes", "Description": "Ohhh, they're called 'pan'cakes because they're like cakes made in a pan haha", "Effect": "+{Px Line Width in Lab Mainframe", "BaseValue": 2},
    12:{"Name": "Corndog", "Description": "Ohhh, they're called 'corn'dogs because... wait, why are they called corndogs?", "Effect": "+{% Meal Cooking Speed", "BaseValue": 12},
    13:{"Name": "Cabbage", "Description": "This is a MONUMENTALLY IMPORTANT vegetable, as well as upgrade.", "Effect": "+{% All Cooking Spd per 10 upgrade Lvs", "BaseValue": 5},
    14:{"Name": "Potato Pea Pastry", "Description": "Yuhhhh it's that Triple P threat! Look out for them P's bro!", "Effect": "+{% Lower Egg Incubator Time", "BaseValue": 1},
    15:{"Name": "Dango", "Description": "Look, I'm not sure what these are either, just go with it.", "Effect": "+{% Lower Kitchen Upgrade Costs", "BaseValue": 2},
    16:{"Name": "Sourish Fish", "Description": "Shhh stop saying they're sweet, you're gonna get me in trouble!", "Effect": "+{% VIP Library Membership", "BaseValue": 4},
    17:{"Name": "Octoplop", "Description": "They really did just plop an octopus on a plate and call it a day.", "Effect": "+{% Total Damage", "BaseValue": 2},
    18:{"Name": "Croissant", "Description": "Carl loves these!", "Effect": "+{% Pet Fighting Damage", "BaseValue": 1},
    19:{"Name": "Canopy", "Description": "...oh, you said 'Can of Pea's. You know, that does make a lot more sense.", "Effect": "+{% New Recipe Cooking Speed", "BaseValue": 10},
    20:{"Name": "Cannoli", "Description": "Ain't got no joke for this one, it's existence is enough of a joke.", "Effect": "+{% Points earned in Tower Defence", "BaseValue": 1},
    21:{"Name": "Cheese", "Description": "Sourced organically, straight from the moon!", "Effect": "+{% Cooking EXP", "BaseValue": 5},
    22:{"Name": "Sawdust", "Description": "'Id rather starve than eat that' - Angie, 2021", "Effect": "+{% Lab EXP", "BaseValue": 5},
    23:{"Name": "Eggplant", "Description": "Idk what you Zoomers are up to with those eggplant emojis, but I don't like it...", "Effect": "+{% Pet Breedability Speed in Fenceyard", "BaseValue": 5},
    24:{"Name": "Cheesy Bread", "Description": "Another bread meal? Wow so unoriginal, I'm glad I already left a 1 star rating.", "Effect": "+{% Total Accuracy", "BaseValue": 1},
    25:{"Name": "Wild Boar", "Description": "It's not really wild anymore is it, it looks kinda dead and roasted.", "Effect": "+{Px Line Width in Lab Mainframe", "BaseValue": 2},
    26:{"Name": "Donut", "Description": "Mmmmm... doooooooonut...", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 15},
    27:{"Name": "Riceball", "Description": "Dude it's just a ball of rice, like what do you want me to say about it?", "Effect": "+{% Skill Efficiency", "BaseValue": 3},
    28:{"Name": "Cauliflower", "Description": "The white part is called Curd! Hmm, time to recategorize this as an educational game!", "Effect": "+{% Basic Atk Speed", "BaseValue": 1},
    29:{"Name": "Durian Fruit", "Description": "This must have been in the room when Kurt said it smelled like 'teen spirit'...", "Effect": "+{% Lower Kitchen Upgrade costs", "BaseValue": 6},
    30:{"Name": "Orange", "Description": "The true arch-nemesis of rappers and poets alike.", "Effect": "+{% VIP Library Membership", "BaseValue": 3},
    31:{"Name": "Bunt Cake", "Description": "Bunt cake more like Punt cake because I'm kicking this trash straight to the garbage.", "Effect": "+{% Cash from Monsters", "BaseValue": 7},
    32:{"Name": "Chocolate Truffle", "Description": "I mean it's got a bite taken out of it, pretty gross.", "Effect": "+{% New Pet Breeding Odds", "BaseValue": 25},
    33:{"Name": "Leek", "Description": "Prowess lowers the efficiency needed when efficiency bar is orange in AFK info", "Effect": "+{% skilling prowess", "BaseValue": 2},
    34:{"Name": "Fortune Cookie", "Description": "It reads: 'Salvation lies not within enjoying video games, but from gitting gud at them'", "Effect": "+{% Faster Library checkout Speed", "BaseValue": 4},
    35:{"Name": "Pretzel", "Description": "I love pretzels, people really be sleepin' on the versatility they bring to the table!", "Effect": "+{% Lab EXP", "BaseValue": 7},
    36:{"Name": "Sea Urchin", "Description": "At least one person reading this has eating one of these. Oh, it's you? Good for you.", "Effect": "+{% Critters from traps", "BaseValue": 1},
    37:{"Name": "Mashed Potato", "Description": "This nutritious meal reminds me of the potato monster from that IdleOn video game!", "Effect": "+{% Cooking EXP", "BaseValue": 6},
    38:{"Name": "Mutton", "Description": "Yeap I tell you hwat Bobby, this is a real man's meal right here!", "Effect": "+{% Crit Chance", "BaseValue": 1},
    39:{"Name": "Wedding Cake", "Description": "Imagine getting married lol so cringe haha am I right??!?! High-five, fellow kids!", "Effect": "+{% Pet Fighting Damage", "BaseValue": 2},
    40:{"Name": "Eel", "Description": "The younger sibling of the Loch Ness Monster. He's real, but no one really cares.", "Effect": "+{% Line Width in Lab Mainframe", "BaseValue": 1},
    41:{"Name": "Whipped Cocoa", "Description": "Why is this being served on a plate? Was the cup not good enough for you??", "Effect": "+{% Skill Efficiency", "BaseValue": 4},
    42:{"Name": "Onion", "Description": "No, I'm not crying, this onion is just stimulating the lachrymal glands in my eyes.", "Effect": "+{% Total Damage", "BaseValue": 3},
    43:{"Name": "Soda", "Description": "Yea those red marks are grill marks, our chef doesn't know what he's doing.", "Effect": "+{% Meal Cooking Speed", "BaseValue": 20},
    44:{"Name": "Sushi Roll", "Description": "For something called a 'sushi roll', it isn't moving around very much.", "Effect": "+{% VIP Library Membership", "BaseValue": 7},
    45:{"Name": "Buncha Banana", "Description": "Straight from the island of Karjama! Or something like that, starts with a K at least.", "Effect": "+{ Max LVs for TP Pete Star Talent", "BaseValue": 4},
    46:{"Name": "Pumpkin", "Description": "According to the author of the Iliad, its value should peak right around January...", "Effect": "+{% Liquid Cap for liquids 1 and 2", "BaseValue": 2},
    47:{"Name": "Cotton Candy", "Description": "The most exquisite of fairground cuisine!", "Effect": "+{% Divinity EXP", "BaseValue": 2},
    48:{"Name": "Massive Fig", "Description": "This thing has gotta weigh at least 30!", "Effect": "+{% Total Damage", "BaseValue": 3},
    49:{"Name": "Head Chef Geustloaf", "Description": "How DARE you question the honorable Chef Geustloaf's cooking abilities!", "Effect": "+{% Bits Gained in Gaming", "BaseValue": 4},
    50:{"Name": "Kiwi Fruit", "Description": "Is there a reason these are so hard to cook? Aren't you just like... cutting it in half?", "Effect": "+{% Liquid Cap for liquids 3 and 4", "BaseValue": 2},
    51:{"Name": "Popped Corn", "Description": "Effectively no different than a normal bowl of popcorn, but it's still impressive!", "Effect": "+{% Sailing Speed", "BaseValue": 2},
    52:{"Name": "Double Cherry", "Description": "So like... why did the yellow circle want these again? This bonus is pretty bad.", "Effect": "+{% Meal Cooking Speed", "BaseValue": 30},
    53:{"Name": "Ratatouey", "Description": "Hey cmon man how should I know how to spell Ratatouille, there's no France remember?", "Effect": "+{% Lower Kitchen Upgrade costs", "BaseValue": 8},
    54:{"Name": "Giant Tomato", "Description": "It's big, it's large, it's round, it's red, and it'll fill you up thats for sure!", "Effect": "+{% Gaming EXP", "BaseValue": 5},
    55:{"Name": "Wrath Grapes", "Description": "I'd be angry too if I were a grape.", "Effect": "+{% Divinity EXP", "BaseValue": 4},
    56:{"Name": "Sausy Sausage", "Description": "Plump innit! Would go great with some momey milk!", "Effect": "+{% Bits Gained in Gaming", "BaseValue": 6},
    57:{"Name": "Seasoned Marrow", "Description": "You ate all the edible stuff around the bone? Why not try the stuff inside the bone!", "Effect": "+{% Farming EXP", "BaseValue": 3},
    58:{"Name": "Sticky Bun", "Description": "This frosting better be made of superglue or I'm suing for false advertising.", "Effect": "+{% All Summoning Essence Gain", "BaseValue": 5},
    59:{"Name": "Frazzleberry", "Description": "Big. Blue. Beautiful. Boing. Boat. Broom. Balls. Backgammon. Bort.", "Effect": "+{% Sneaking EXP", "BaseValue": 2},
    60:{"Name": "Misterloin Steak", "Description": "Make sure to paint on the grill marks to really give it that extra taste!", "Effect": "+{% Jade gain from Sneaking", "BaseValue": 6},
    61:{"Name": "Large Pohayoh", "Description": "Aye lad if thah ain't tha larjes' fookin' poh'ay'oh eyev evah seen wih me own eyes!", "Effect": "+{% Summoning EXP", "BaseValue": 2},
    62:{"Name": "Bill Jack Pepper", "Description": "It's Him.", "Effect": "+{% Crop Evolution Chance", "BaseValue": 5},
    63:{"Name": "Burned Marshmallow", "Description": "IMPORTANT, this bonus DOUBLES at Farming Lv 50. Triples at Farming Lv 100, and so on!", "Effect": "+{% Meal Cooking Speed", "BaseValue": 40},
    64:{"Name": "Yumi Peachring", "Description": "Don't disrespect the ring. All hail the ring.", "Effect": "+{% All Golden Food bonus", "BaseValue": 2},
    65:{"Name": "Plumpcakes", "Description": "Ohhh, they're called 'plump'cakes because they're dummy thicc can I get an amen!", "Effect": "+{% Total Damage", "BaseValue": 6},
    66:{"Name": "Nyanborgir", "Description": "It's the greatest meal ever! Bonus DOUBLES at Summoning Lv 50, Triples at 100, etc", "Effect": "+{% Crop Evolution Chance", "BaseValue": 9},
}
rift_rewards_dict = {
    5: {'Name': 'Trap Box Vacuum', 'Shorthand': "TrapBoxVacuum"},
    10: {'Name': 'Infinite Stars', 'Shorthand': "InfiniteStars"},
    15: {'Name': 'Skill Mastery', 'Shorthand': "SkillMastery"},
    20: {'Name': 'Eclipse Skulls', 'Shorthand': "EclipseSkulls"},
    25: {'Name': 'Stamp Mastery', 'Shorthand': "StampMastery"},
    30: {'Name': 'Eldritch Artifact', 'Shorthand': "EldritchArtifacts"},
    35: {'Name': 'Vial Mastery', 'Shorthand': "VialMastery"},
    40: {'Name': 'Construct Mastery', 'Shorthand': "ConstructionMastery"},
    45: {'Name': 'Ruby Cards', 'Shorthand': "RubyCards"},
    50: {'Name': 'Killroy Prime', 'Shorthand': "KillroyPrime"},
    55: {'Name': 'Sneaking Mastery', 'Shorthand': "SneakingMastery"},
}
lab_chips_dict = {
    0: {"Name": "Grounded Nanochip", "Description": "+{% Total Defence", "Effect": "Boosts total defence", "Material": "Copper", "MaterialCost": 20000, "Meal": "Meal0", "MealCost": 100, "Spice": "Spice0", "SpiceCost": 100, "Value10": 0, "EffectID": "def", "BaseValue": 10},
    1: {"Name": "Grounded Motherboard", "Description": "+{% Move Speed if total is less than 170%", "Effect": "Boosts total movement speed", "Material": "OakTree", "MaterialCost": 30000, "Meal": "Meal1", "MealCost": 100, "Spice": "Spice0", "SpiceCost": 100, "Value10": 0, "EffectID": "move", "BaseValue": 30},
    2: {"Name": "Grounded Software", "Description": "+{% Total Accuracy", "Effect": "Boosts total accuracy", "Material": "Fish1", "MaterialCost": 20000, "Meal": "Meal3", "MealCost": 100, "Spice": "Spice1", "SpiceCost": 100, "Value10": 0, "EffectID": "acc", "BaseValue": 10},
    3: {"Name": "Grounded Processor", "Description": "+{% Drop Rate if total is less than 5.00x", "Effect": "Boosts total drop rate", "Material": "DesertA1", "MaterialCost": 10000, "Meal": "Meal4", "MealCost": 100, "Spice": "Spice1", "SpiceCost": 100, "Value10": 0, "EffectID": "dr", "BaseValue": 60},
    4: {"Name": "Potato Chip", "Description": "+{% Basic Attack spd. *Can Only Equip 1 per player*", "Effect": "Boosts attack speed", "Material": "Bug1", "MaterialCost": 20000, "Meal": "Meal6", "MealCost": 100, "Spice": "Spice2", "SpiceCost": 100, "Value10": 1, "EffectID": "atkspd", "BaseValue": 20},
    5: {"Name": "Conductive Nanochip", "Description": "+{% Lab EXP Gain", "Effect": "Boosts lab exp gain", "Material": "StumpTree", "MaterialCost": 100000, "Meal": "Meal9", "MealCost": 100, "Spice": "Spice3", "SpiceCost": 100, "Value10": 0, "EffectID": "labexp", "BaseValue": 30},
    6: {"Name": "Conductive Motherboard", "Description": "+{% Line Width within Mainframe", "Effect": "Boosts mainframe line width", "Material": "Gold", "MaterialCost": 100000, "Meal": "Meal12", "MealCost": 100, "Spice": "Spice4", "SpiceCost": 100, "Value10": 0, "EffectID": "linewidth", "BaseValue": 12},
    7: {"Name": "Conductive Software", "Description": "+{% Fighting AFK Gain Rate *Can Only Equip 1 per player*", "Effect": "Boosts Fighting AFK gain rate", "Material": "Critter2", "MaterialCost": 10000, "Meal": "Meal15", "MealCost": 100, "Spice": "Spice4", "SpiceCost": 100, "Value10": 1, "EffectID": "fafk", "BaseValue": 15},
    8: {"Name": "Conductive Processor", "Description": "+{% Skilling AFK Gain Rate *Can Only Equip 1 per player*", "Effect": "Boosts Skilling AFK gain Rate", "Material": "Bug5", "MaterialCost": 100000, "Meal": "Meal18", "MealCost": 100, "Spice": "Spice5", "SpiceCost": 100, "Value10": 1, "EffectID": "safk", "BaseValue": 15},
    9: {"Name": "Chocolatey Chip", "Description": "{% chance to spawn a crystal mob when one dies. *Can Only Equip 1 per player*", "Effect": "Chance for Crystal Mob revival", "Material": "CraftMat8", "MaterialCost": 200000, "Meal": "Meal21", "MealCost": 100, "Spice": "Spice6", "SpiceCost": 100, "Value10": 1, "EffectID": "crys", "BaseValue": 75},
    10: {"Name": "Galvanic Nanochip", "Description": "+{% Monster Respawn Rate", "Effect": "Boosts Mob respawn rate", "Material": "SnowC1", "MaterialCost": 100000, "Meal": "Meal24", "MealCost": 100, "Spice": "Spice7", "SpiceCost": 100, "Value10": 0, "EffectID": "resp", "BaseValue": 10},
    11: {"Name": "Galvanic Motherboard", "Description": "+{% Total Skilling Efficiency for all skills", "Effect": "Boosts skilling efficiency", "Material": "Fish5", "MaterialCost": 250000, "Meal": "Meal27", "MealCost": 100, "Spice": "Spice8", "SpiceCost": 100, "Value10": 0, "EffectID": "toteff", "BaseValue": 20},
    12: {"Name": "Galvanic Software", "Description": "+{% Total Damage", "Effect": "Boosts total damage", "Material": "Dementia", "MaterialCost": 300000, "Meal": "Meal29", "MealCost": 100, "Spice": "Spice9", "SpiceCost": 100, "Value10": 0, "EffectID": "dmg", "BaseValue": 10},
    13: {"Name": "Galvanic Processor", "Description": "+{ Base Efficiency for all skills", "Effect": "Boosts base skilling efficiency", "Material": "GalaxyB2", "MaterialCost": 100000, "Meal": "Meal31", "MealCost": 100, "Spice": "Spice10", "SpiceCost": 100, "Value10": 0, "EffectID": "eff", "BaseValue": 250},
    14: {"Name": "Wood Chip", "Description": "+{% Multikill per Damage Tier for all worlds", "Effect": "Boosts multikill", "Material": "Tree8", "MaterialCost": 250000, "Meal": "Meal33", "MealCost": 100, "Spice": "Spice11", "SpiceCost": 100, "Value10": 0, "EffectID": "mkill", "BaseValue": 15},
    15: {"Name": "Silkrode Nanochip", "Description": "Doubles the bonuses of all active Star Signs. *Can Only Equip 1 per player*", "Effect": "Bolsters active star signs", "Material": "CraftMat10", "MaterialCost": 2000000, "Meal": "Meal35", "MealCost": 100, "Spice": "Spice12", "SpiceCost": 100, "Value10": 1, "EffectID": "star", "BaseValue": 1},
    16: {"Name": "Silkrode Motherboard", "Description": "Doubles MISC bonuses of currently equipped Trophy. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped trophy", "Material": "Soul5", "MaterialCost": 2000000, "Meal": "Meal37", "MealCost": 100, "Spice": "Spice13", "SpiceCost": 100, "Value10": 1, "EffectID": "troph", "BaseValue": 1},
    17: {"Name": "Silkrode Software", "Description": "Doubles MISC bonuses of keychain equipped in the upper keychain slot. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped keychain", "Material": "Bug8", "MaterialCost": 2000000, "Meal": "Meal39", "MealCost": 100, "Spice": "Spice13", "SpiceCost": 100, "Value10": 1, "EffectID": "key1", "BaseValue": 1},
    18: {"Name": "Silkrode Processor", "Description": "Doubles MISC bonuses of currently equipped Pendant. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped pendant", "Material": "Critter10", "MaterialCost": 2000000, "Meal": "Meal41", "MealCost": 100, "Spice": "Spice14", "SpiceCost": 100, "Value10": 1, "EffectID": "pend", "BaseValue": 1},
    19: {"Name": "Poker Chip", "Description": "Your weapon gives 1.{x more Weapon Power. *Can Only Equip 1 per player*", "Effect": "Bolsters equipped Weapon", "Material": "CraftMat14", "MaterialCost": 2000000, "Meal": "Meal43", "MealCost": 100, "Spice": "Spice14", "SpiceCost": 100, "Value10": 1, "EffectID": "weppow", "BaseValue": 25},
    20: {"Name": "Omega Nanochip", "Description": "Doubles bonus of card equipped in top left slot. *Can Only Equip 1 per player*", "Effect": "Bolsters an equipped card", "Material": "Bug8", "MaterialCost": 10000000, "Meal": "Meal45", "MealCost": 100, "Spice": "Spice15", "SpiceCost": 100, "Value10": 1, "EffectID": "card1", "BaseValue": 1},
    21: {"Name": "Omega Motherboard", "Description": "Doubles bonus of card equipped in bottom right slot. *Can Only Equip 1 per player*", "Effect": "Bolsters an equipped card", "Material": "Fish8", "MaterialCost": 10000000, "Meal": "Meal47", "MealCost": 100, "Spice": "Spice16", "SpiceCost": 100, "Value10": 1, "EffectID": "card2", "BaseValue": 1},
}
lab_bonuses_dict = {
    0: {"Name": "Animal Farm", "Description": "+1% Total Damage for every different species you have bred within Pet Breeding. You just need to breed the pet type one time for it to count! @ - @ Total Bonus: {%", "BaseValue": 1, "Coordinates": [91, 90], "Value4": 90, "Value5": 0},
    1: {"Name": "Wired In", "Description": "All Uploaded Players print 2x more resources from their section of the 3D Printer. The displayed amount will NOT appear doubled, just to avoid confusion as to what your actual base Sampling Rate is, but it will be displayed in blue.", "BaseValue": 2, "Coordinates": [250, 90], "Value4": 90, "Value5": 1},
    2: {"Name": "Gilded Cyclical Tubing", "Description": "All refinery cycles occur 3x faster. Faster cycles means more salts!", "BaseValue": 3, "Coordinates": [356, 90], "Value4": 90, "Value5": 1},
    3: {"Name": "No Bubble Left Behind", "Description": "Every 24 hours, your 3 lowest level Alchemy Bubbles gets +1 Lv. This only applies to bubbles Lv 5 or higher, so it's more like 'your lowest level bubble that is at least level 5'. ALSO, it only works on the first 15 bubbles of each colour! @ Doesn't trigger on days that you don't login.", "BaseValue": 1, "Coordinates": [450, 90], "Value4": 90, "Value5": 0},
    4: {"Name": "Killer's Brightside", "Description": "All monster kills count for 2x more than normal for things like opening portals and Death Note. Doesn't increase resource drops or exp gain.", "BaseValue": 2, "Coordinates": [538, 90], "Value4": 90, "Value5": 1},
    5: {"Name": "Shrine World Tour", "Description": "If a shrine is placed within town, instead of in a monster map, it will act as though it is placed in EVERY map in that entire world!", "BaseValue": 1, "Coordinates": [651, 90], "Value4": 90, "Value5": 0},
    6: {"Name": "Viaduct of the Gods", "Description": "All alchemy liquids have x5 higher max capacity. However, you regenerate alchemy liquids -30% slower.", "BaseValue": 5, "Coordinates": [753, 90], "Value4": 90, "Value5": 1},
    7: {"Name": "Certified Stamp Book", "Description": "All Stamps, except for MISC tab stamps, give DOUBLE the bonus.", "BaseValue": 2, "Coordinates": [824, 90], "Value4": 90, "Value5": 1},
    8: {"Name": "Spelunker Obol", "Description": "1.50x higher effects from all active Jewels within the Mainframe, and gives you +50% rememberance of the game Idle Skilling. @ This bonus always has a 80px connection range no matter what!", "BaseValue": 1.5, "Coordinates": [945, 90], "Value4": 90, "Value5": 1},
    9: {"Name": "Fungi Finger Pocketer", "Description": "+2% extra cash from monsters for every 1 million Green Mushroom kills your account has, which can be viewed at Death Note. @ - @ Total Bonus: {%", "BaseValue": 2, "Coordinates": [990, 90], "Value4": 90, "Value5": 0},
    10: {"Name": "My 1st Chemistry Set", "Description": "All Vials in Alchemy give DOUBLE the bonus. The bonus description will reflect this doubling.", "BaseValue": 2, "Coordinates": [1177, 90], "Value4": 90, "Value5": 1},
    11: {"Name": "Unadulterated Banking Fury", "Description": "+2% Total Damage for each 'green stack' of resources in your bank. A 'green stack' is a stack in your Storage Chest with 10 million or more items, since the number turns Green after 10M! @ - @ Total Bonus: {%", "BaseValue": 2, "Coordinates": [1300, 90], "Value4": 90, "Value5": 0},
    12: {"Name": "Sigils of Olden Alchemy", "Description": "Allows you to level up Alchemy Sigils by assigning players in alchemy, at a base rate of 1 sigil xp per hour. @ Sigils can be leveled up just twice: Once to unlock their bonus, and once more to boost their bonus. Their bonuses are passive, and apply to all characters always.", "BaseValue": 1, "Coordinates": [400, 90], "Value4": 90, "Value5": 0},
    13: {"Name": "Viral Connection", "Description": "All mainframe bonuses and jewels have a 50% larger connection range, unless it states otherwise. @ This bonus always has a 80px connection range no matter what!", "BaseValue": 50, "Coordinates": [1430, 90], "Value4": 90, "Value5": 0},
    14: {"Name": "Artifact Attraction", "Description": "Artifact find chance is 1.5x higher! If you've found all artifacts at max rarity, then this bonus changes to 1,000x artifact find chance!", "BaseValue": 50, "Coordinates": [1530, 90], "Value4": 90, "Value5": 0},
    15: {"Name": "Slab Sovereignty", "Description": "All bonuses given by the Slab are 1.25x higher!", "BaseValue": 25, "Coordinates": [1630, 90], "Value4": 90, "Value5": 0},
    16: {"Name": "Spiritual Growth", "Description": "Boosts EXP multi for all three World 6 skills by +50%!", "BaseValue": 50, "Coordinates": [1790, 90], "Value4": 90, "Value5": 0},
    17: {"Name": "Depot Studies PhD", "Description": "All bonuses given at the Crop Depot are 1.30x higher!", "BaseValue": 30, "Coordinates": [1950, 90], "Value4": 90, "Value5": 0},
}
lab_jewels_source_info = ["76 134 90 Meal_cooking_is_}x_faster._This_bonus_is_applied_TWICE_if_all_3_purple_jewels_are_active. Boosts_Meal_Cooking_speed Quest66 5 Meal1 2000 Spice0 200 Amethyst_Rhinestone 1.5".split(" "), "164 412 90 'Animal_Farm'_mainframe_bonus_gives_an_additional_+}%_per_species._If_Animal_Farm_is_not_active,_then_this_does_nothing. Bolsters_'Animal_Farm' Quest35 5 Meal3 2000 Spice1 200 Purple_Navette 0.5".split(" "), "163 218 90 All_players_get_+}%_Lab_EXP_gain. Boosts_Lab_EXP_gain Timecandy1 10 Meal5 2000 Spice2 200 Purple_Rhombol 40".split(" "), "246 110 90 Construction_slot_1_is_now_trimmed_up,_and_has_}x_building_Speed._Also_trims_slot_2_if_all_4_blue_jewels_are_active. Trims_up_a_construction_slot Quest15 10 Meal7 5000 Spice3 400 Sapphire_Rhinestone 3".split(" "), "277 394 90 All_players_get_+}%_All_Stat._STR,_AGI,_WIS,_and_LUCK_to_boot. Boosts_all_stats TreeInterior1b 25 Meal9 5000 Spice4 400 Sapphire_Navette 3".split(" "), "470 294 90 Even_if_this_jewel_is_off,_all_players_within_a_150px_radius_of_this_jewel,_shown_by_the_circle,_have_+25%_Line_Width._@_Also_gives_+}%_Breeding_EXP,_but_only_when_active. Emits_a_'Line_Width'_Aura Sewers1b 30 Meal11 5000 Spice5 400 Sapphire_Rhombol 25".split(" "), "490 112 90 Every_24_hours,_the_}_lowest_level_Kitchen_Upgrades_across_all_owned_kitchens_gain_+1_Lv. Automatically_levels_up_kitchens Quest38 2 Meal13 5000 Spice6 400 Sapphire_Pyramite 2".split(" "), "552 163 90 'No_Bubble_Left_Behind'_mainframe_bonus_gives_+}_levels_instead_of_+1,_and_does_so_for_the_lowest_4_bubbles_instead_of_3. Bolsters_'No_Bubble_Left_Behind' DesertA1b 50 Meal15 10000 Spice7 1500 Pyrite_Rhinestone 2".split(" "), "646 407 90 All_players_get_}x_'non-consume'_chance,_and_raises_the_max_chance_from_90%_to_98%,_allowing_for_longer_AFK_with_food. Boosts_'non-consume'_chance EquipmentPants19 2 Meal17 10000 Spice8 1500 Pyrite_Navette 3".split(" "), "680 319 90 All_mainframe_bonuses_and_jewels_have_a_}%_larger_connection_range,_except_for_this_jewel._This_jewel_has_an_80px_connection_range_no_matter_what! Boosts_mainframe_connection_range DesertA3b 50 Meal19 10000 Spice9 1500 Pyrite_Rhombol 30".split(" "), "847 105 90 All_players_deal_1.}x_more_damage._This_bonus_is_applied_TWICE_if_all_4_Orange_Jewels_are_active. Boosts_player_damage DesertC2b 50 Meal21 10000 Spice10 1500 Pyrite_Pyramite 10".split(" "), "998 404 90 }%_reduced_incubation_egg_time._Mo_eggs_mo_problems_tho,_fo_sho. Reduces_egg_incubation_time BabaYagaETC 1 Meal23 25000 Spice11 5000 Emerald_Rhinestone 28".split(" "), "1079 233 90 All_players_have_}_higher_base_efficiency_in_all_skills,_and_+10%_skill_action_speed._This_bonus_is_applied_TWICE_if_all_5_Green_Jewels_are_active. Boosts_player_efficiency SnowA2a 80 Meal25 25000 Spice12 5000 Emerald_Navette 200".split(" "), "1085 121 90 'Fungi_Finger_Pocketer'_mainframe_bonus_gives_an_additional_+}%_cash_bonus_per_million_mushroom_kills Bolsters_'Fungi_Finger_Pocketer' SnowB2a 120 Meal27 25000 Spice13 5000 Emerald_Rhombol 1".split(" "), "1167 390 90 Meal_cooking_is_}%_faster_for_every_25_total_upgrade_levels_across_all_kitchens._@_Total_Bonus:_{%_speed Boosts_Meal_Cooking_speed SnowC4a 150 Meal29 25000 Spice14 5000 Emerald_Pyramite 1".split(" "), "1300 208 90 Special_Pets_in_the_Fenceyard_level_up_their_Passive_Bonuses_+}%_faster Boosts_Pet_Passive_level_up_rate GalaxyA2b 200 Meal31 25000 Spice15 5000 Emerald_Ulthurite 30".split(" "), "1365 100 90 All_meals_now_give_a_1.}x_higher_bonus!_Go_ahead_and_check_it_out_at_the_Dinner_Menu!_@_Doesn't_apply_to_the_meal_that_gives_Line_Width_bonus. Bolsters_meals GalaxyC1b 300 Meal33 100000 Spice15 10000 Black_Diamond_Rhinestone 16".split(" "), "1389 408 90 'Unadulterated_Banking_Fury'_gives_an_additional_+}%_Total_Damage_per_greened_stack. Bolsters_'Unadulterated_Banking_Fury' Critter10A 10000 Meal35 100000 Spice16 10000 Black_Diamond_Ulthurite 1".split(" "), "1619 203 90 'Slab_Sovereignty'_gives_an_additional_}%_boost_to_all_Slab_Bonuses! Bolsters_'Slab_Sovereignty' SpiA1 3000000 Meal53 1000000 Spice20 10000 Pure_Opal_Rhinestone 20".split(" "), "1846 410 80 +}%_higher_effects_from_all_active_bonuses_and_jewels_within_the_Mainframe,_except_for_Spelunker_Obol._@_This_is_a_multiplier,_so_+10%_would_be_1.10x,_ya_feel_me?_@_This_bonus_always_has_a_80px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 Pure_Opal_Navette 10".split(" "), "2040 96 90 'Depot_Studies_PhD'_gives_an_additional_}%_boost_to_all_Crop_Depot_bonuses! Bolsters_'Depot_Studies_PhD' Critter11A 5000 Meal62 100000000 Spice22 10000 Pure_Opal_Rhombol 10".split(" "), "1815 96 100 +}%_extra_Deathbringer_Bones._@_This_bonus_always_has_a_100px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 Deadly_Wrath_Jewel 50".split(" "), "1728 421 100 +}%_extra_Windwalker_Dust._@_This_bonus_always_has_a_100px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 North_Winds_Jewel 50".split(" "), "2042 410 100 +}%_extra_Arcane_Cultist_Tachyons._@_This_bonus_always_has_a_100px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 Eternal_Energy_Jewel 50".split(" ")]
lab_jewels_dict = {
    index: {
        'Name': data[11].replace('_', ' '),
        'Description': data[3].replace('_', ' '),
        'BaseValue': parse_number(data[12])
    } for index, data in enumerate(lab_jewels_source_info)}
max_nblb_bubbles = 10
max_breeding_territories = 24  # as of w6 launch
breeding_last_arena_bonus_unlock_wave = 200
index_first_territory_assigned_pet = 28
slot_unlock_waves_list = [2, 15, 50, 125]
territory_names = [
    "", "Grasslands", "Jungle", "Encroaching Forest", "Tree Interior", "Stinky Sewers",
    "Desert Oasis", "Beach Docks", "Coarse Mountains", "Twilight Desert", "The Crypt",
    "Frosty Peaks", "Tundra Outback", "Crystal Caverns", "Pristalle Lake",
    "Nebulon Mantle", "Starfield Skies", "Shores of Eternity",
    "Molten Bay", "Smokey Lake", "Wurm Catacombs",
    "Spirit Fields", "Bamboo Forest", "Lullaby Airways", "Dharma Mesa"
]
breeding_upgrades_dict: dict[int, dict[str, str | int]] = {
    0: {
        'Name': 'No Upgrade Selected',
        'BonusText': "TAP AN UPGRADE ABOVE! Also, as a reward for reading this, I'll let you know that upgrading this 'nothing' bonus actually boosts breeding exp gain!!",
        'BonusValue': 2,
        'MaxLevel': 100,
        'MaxValue': 200,
        'UnlockLevel': 1,
    },
    1: {
        'Name': 'Genetic Splicing',
        'BonusText': "Unlocks the 1st Breeding Multiplier, Gene Boosting. Genes are found while fighting with the DNA Splicer tool purchased at the Town Shop.",
        'BonusValue': 4,
        'MaxLevel': 20,
        'MaxValue': 80,
        'UnlockLevel': 1,
    },
    2: {
        'Name': 'Egg Capacity',
        'BonusText': "Increases the maximum number of eggs your incubator can hold. The more eggs you currently hold, the rarer it is to get a new one.",
        'BonusValue': 1,
        'MaxLevel': 5,
        'MaxValue': 5,
        'UnlockLevel': 5,
    },
    3: {
        'Name': 'Breedability Pulse',
        'BonusText': "Unlocks the 2nd Breeding Multiplier, Breedability. Pets placed in the Fenceyard with the Breedable Gene increase this multi over time.",
        'BonusValue': 25,
        'MaxLevel': 10,
        'MaxValue': 250,
        'UnlockLevel': 10,
    },
    4: {
        'Name': 'Fence Extension',
        'BonusText': "Increases the number of slots in your Fence Yard, allowing for more pets to roam around, free range style!",
        'BonusValue': 1,
        'MaxLevel': 10,
        'MaxValue': 10,
        'UnlockLevel': 15,
    },
    5: {
        'Name': 'Rarity of the Egg',
        'BonusText': "Unlocks the 3rd Breeding Multi, Rarity. When the egg incubator is full, theres a chance to increase the rarity of another egg!",
        'BonusValue': 0,
        'MaxLevel': 10,
        'MaxValue': 3.5,
        'UnlockLevel': 20,
    },
    6: {
        'Name': 'Blooming Axe',
        'BonusText': "Forage pets contribute a fraction of their forage speed toward Fight Power. Now you no longer need at least 1 fighting pet!",
        'BonusValue': 6,
        'MaxLevel': 10,
        'MaxValue': 60,
        'UnlockLevel': 25,
    },
    7: {
        'Name': 'Pastpresent Brood',
        'BonusText': "Unlocks the 4th Breeding Multiplier, Pastpres. This increases based on the number of different pets discovered from the previous world.",
        'BonusValue': 0.15,
        'MaxLevel': 5,
        'MaxValue': 1.75,
        'UnlockLevel': 30,
    },
    8: {
        'Name': 'Paint Bucket',
        'BonusText': "Unlocks Shiny Pet Breeding. Shiny Pets come in 1 of 5 colours, and boost their Special Passive bonus when in the Fenceyard.",
        'BonusValue': 2,
        'MaxLevel': 100,
        'MaxValue': 201,
        'UnlockLevel': 40,
    },
    9: {
        'Name': 'Overwhelmed Golden Egg',
        'BonusText': "Your New Pet Chance is multiplied for every 100 kitchen upgrade levels across all kitchens! So 200 Lvs would apply it twice!!",
        'BonusValue': 0.02,
        'MaxLevel': 20,
        'MaxValue': 1.4,
        'UnlockLevel': 50,
    },
    10: {
        'Name': 'Failsafe Restitution Cloud',
        'BonusText': "Unlocks the 5th Breeding Multiplier, Failure. This increases every time you fail to get a pet, up to a max, and depletes when you succeed.",
        'BonusValue': 10,
        'MaxLevel': 25,
        'MaxValue': 250,
        'UnlockLevel': 60,
    },
    11: {
        'Name': 'Shattershell Iteration',
        'BonusText': "Every time you use up your last incubator egg, there is a chance to produce 2 more eggs immediately.",
        'BonusValue': 6,
        'MaxLevel': 10,
        'MaxValue': 60,
        'UnlockLevel': 70,
    },
    12: {
        'Name': 'Grand Martial of Shinytown',
        'BonusText': "Boosts the rate at which shiny pets level up from being in the fenceyard. This will help you rack up those 100+ Day requirements!",
        'BonusValue': 5,
        'MaxLevel': 300,
        'MaxValue': 1500,
        'UnlockLevel': 80,
    },

}
breeding_genetics_list: list[str] = [
    "Fighter", "Defender", "Forager", "Fleeter", "Breeder", "Special", "Mercenary", "Boomer",
    "Sniper", "Amplifier", "Tsar", "Rattler", "Cursory", "Fastidious", "Flashy", "Opticular",
    "Monolithic", "Alchemic", "Badumdum", "Defstone", "Targeter", "Looter", "Refiller", "Eggshell",
    "Lazarus", "Trasher", "Miasma", "Converter", "Heavyweight", "Fastihoop", "Ninja",
    "Superboomer", "Peapeapod", "Borger"
]
breeding_shiny_bonus_list: list[str] = [
    "Faster Shiny Pet Lv Up Rate",  #0
    "Infinite Star Signs",
    "Total Damage",  #2
    "Drop Rate",
    "Base Efficiency for All Skills",  #4
    "Base WIS",
    "Base STR",  #6
    "Base AGI",
    "Base LUK",  #8
    "Class EXP",
    "Skill EXP",  #10
    "Tab 1 Talent Pts",
    "Tab 2 Talent Pts",  #12
    "Tab 3 Talent Pts",
    "Tab 4 Talent Pts",  #14
    "Star Talent Pts",
    "Faster Refinery Speed",  #16
    "Base Critter Per Trap",
    "Multikill Per Tier",  #18
    "Bonuses from All Meals",
    "Line Width in Lab",  #20
    "Higher Artifact Find Chance",
    "Sail Captain EXP Gain",  #22
    "Lower Minimum Travel Time for Sailing",
    "Farming EXP",  #24
    "Summoning EXP"
]
breeding_species_dict: dict[int, dict] = {
    #Built using references to Genetics and ShinyBonus lists because I kept making typos + Wiki isn't consistent to copy/paste from
    1: {
        0: {
            'Name': 'Green Mushroom',
            'Genetic': breeding_genetics_list[0],  #Fighter
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate,
        },
        1: {
            'Name': 'Squirrel',
            'Genetic': breeding_genetics_list[2],  #Forager
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        2: {
            'Name': 'Frog',
            'Genetic': breeding_genetics_list[7],  #Boomer
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        3: {
            'Name': 'Bored Bean',
            'Genetic': breeding_genetics_list[3],  #Fleeter
            'ShinyBonus': breeding_shiny_bonus_list[16],  #Faster Refinery Speed
        },
        4: {
            'Name': 'Red Mushroom',
            'Genetic': breeding_genetics_list[0],  #Fighter
            'ShinyBonus': breeding_shiny_bonus_list[19],  #Bonuses from All Meals
        },
        5: {
            'Name': 'Slime',
            'Genetic': breeding_genetics_list[12],  #Cursory
            'ShinyBonus': breeding_shiny_bonus_list[3],  #Drop Rate
        },
        6: {
            'Name': 'Piggo',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        7: {
            'Name': 'Baby Boa',
            'Genetic': breeding_genetics_list[20],  #Targeter
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
        8: {
            'Name': 'Carrotman',
            'Genetic': breeding_genetics_list[6],  #Mercenary
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        9: {
            'Name': 'Glublin',
            'Genetic': breeding_genetics_list[22],  #Refiller
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        10: {
            'Name': 'Wode Board',
            'Genetic': breeding_genetics_list[26],  #Miasma
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate
        },
        11: {
            'Name': 'Gigafrog',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        12: {
            'Name': 'Wild Boar',
            'Genetic': breeding_genetics_list[28],  #Heavyweight
            'ShinyBonus': breeding_shiny_bonus_list[7],  #Base AGI
        },
        13: {
            'Name': 'Walking Stick',
            'Genetic': breeding_genetics_list[22],  #Refiller
            'ShinyBonus': breeding_shiny_bonus_list[17],  #Base Critter Per Trap
        },
        14: {
            'Name': 'Nutto',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        15: {
            'Name': 'Poop',
            'Genetic': breeding_genetics_list[10],  #Tsar
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        16: {
            'Name': 'Rat',
            'Genetic': breeding_genetics_list[16],  #Monolithic
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
    },
    2: {
        0: {
            'Name': 'Sandy Pot',
            'Genetic': breeding_genetics_list[21],  #Looter
            'ShinyBonus': breeding_shiny_bonus_list[9],  #Class EXP
        },
        1: {
            'Name': 'Mimic',
            'Genetic': breeding_genetics_list[1],  #Defender
            'ShinyBonus': breeding_shiny_bonus_list[11],  #Tab 1 Talent Pts
        },
        2: {
            'Name': 'Crabcake',
            'Genetic': breeding_genetics_list[3],  #Fleeter
            'ShinyBonus': breeding_shiny_bonus_list[10],  #Skill EXP
        },
        3: {
            'Name': 'Mafioso',
            'Genetic': breeding_genetics_list[2],  #Forager
            'ShinyBonus': breeding_shiny_bonus_list[12],  #Tab 2 Talent Pts
        },
        4: {
            'Name': 'Mallay',
            'Genetic': breeding_genetics_list[15],  #Opticular
            'ShinyBonus': breeding_shiny_bonus_list[20],  #Line Width in Lab
        },
        5: {
            'Name': 'Sand Castle',
            'Genetic': breeding_genetics_list[19],  #Defstone
            'ShinyBonus': breeding_shiny_bonus_list[6],  #Base STR
        },
        6: {
            'Name': 'Pincermin',
            'Genetic': breeding_genetics_list[0],  #Fighter
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        7: {
            'Name': 'Mashed Potato',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        8: {
            'Name': 'Tyson',
            'Genetic': breeding_genetics_list[13],  #Fastidious
            'ShinyBonus': breeding_shiny_bonus_list[21],  #Higher Artifact Find Chance
        },
        9: {
            'Name': 'Whale',
            'Genetic': breeding_genetics_list[18],  #Badumdum
            'ShinyBonus': breeding_shiny_bonus_list[16],  #Faster Refinery Speed
        },
        10: {
            'Name': 'Moonmoon',
            'Genetic': breeding_genetics_list[7],  #Mercenary
            'ShinyBonus': breeding_shiny_bonus_list[5],  #Base WIS
        },
        11: {
            'Name': 'Sand Giant',
            'Genetic': breeding_genetics_list[11],  #Rattler
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        12: {
            'Name': 'Snelbie',
            'Genetic': breeding_genetics_list[16],  #Monolithic
            'ShinyBonus': breeding_shiny_bonus_list[14],  #Tab 4 Talent Pts
        },
        13: {
            'Name': 'Dig Doug',
            'Genetic': breeding_genetics_list[24],  #Lazarus
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        14: {
            'Name': 'Beefie',
            'Genetic': breeding_genetics_list[25],  #Trasher
            'ShinyBonus': breeding_shiny_bonus_list[8],  #Base LUK
        },
        15: {
            'Name': 'Crescent Spud',
            'Genetic': breeding_genetics_list[16],  #Monolithic
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate
        },
        16: {
            'Name': 'Chippy',
            'Genetic': breeding_genetics_list[23],  #Eggshell
            'ShinyBonus': breeding_shiny_bonus_list[25],  #Summoning EXP
        },
    },
    3: {
        0: {
            'Name': 'Sheepie',
            'Genetic': breeding_genetics_list[8],  #Sniper
            'ShinyBonus': breeding_shiny_bonus_list[19],  #Bonuses from All Meals
        },
        1: {
            'Name': 'Frost Flake',
            'Genetic': breeding_genetics_list[30],  #Ninja
            'ShinyBonus': breeding_shiny_bonus_list[13],  #Tab 3 Talent Pts
        },
        2: {
            'Name': 'Sir Stache',
            'Genetic': breeding_genetics_list[23],  #Eggshell
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        3: {
            'Name': 'Xylobone',
            'Genetic': breeding_genetics_list[15],  #Opticular
            'ShinyBonus': breeding_shiny_bonus_list[3],  #Drop Rate
        },
        4: {
            'Name': 'Bunny',
            'Genetic': breeding_genetics_list[14],  #Flashy
            'ShinyBonus': breeding_shiny_bonus_list[8],  #Base LUK
        },
        5: {
            'Name': 'Bloque',
            'Genetic': breeding_genetics_list[17],  #Alchemic
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
        6: {
            'Name': 'Mamooth',
            'Genetic': breeding_genetics_list[21],  #Looter
            'ShinyBonus': breeding_shiny_bonus_list[21],  #Higher Artifact Find Chance
        },
        7: {
            'Name': 'Snowman',
            'Genetic': breeding_genetics_list[19],  #Defstone
            'ShinyBonus': breeding_shiny_bonus_list[9],  #Class EXP
        },
        8: {
            'Name': 'Penguin',
            'Genetic': breeding_genetics_list[13],  #Fastidious
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        9: {
            'Name': 'Thermister',
            'Genetic': breeding_genetics_list[8],  #Sniper
            'ShinyBonus': breeding_shiny_bonus_list[10],  #Skill EXP
        },
        10: {
            'Name': 'Quenchie',
            'Genetic': breeding_genetics_list[7],  #Boomer
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate
        },
        11: {
            'Name': 'Cryosnake',
            'Genetic': breeding_genetics_list[23],  #Eggshell
            'ShinyBonus': breeding_shiny_bonus_list[15],  #Star Talent Pts
        },
        12: {
            'Name': 'Mecho Mouse',
            'Genetic': breeding_genetics_list[25],  #Trasher
            'ShinyBonus': breeding_shiny_bonus_list[6],  #Base STR
        },
        13: {
            'Name': 'Bop Box',
            'Genetic': breeding_genetics_list[27],  #Converter
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        14: {
            'Name': 'Neyeptune',
            'Genetic': breeding_genetics_list[24],  #Lazarus
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        15: {
            'Name': 'Dedotated Ram',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
        16: {
            'Name': 'Bloodbone',
            'Genetic': breeding_genetics_list[20],  #Targeter
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        17: {
            'Name': 'Panda',
            'Genetic': breeding_genetics_list[27],  #Converter
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
    },
    4: {
        0: {
            'Name': 'Purp Mushroom',
            'Genetic': breeding_genetics_list[10],  #Tsar
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        1: {
            'Name': 'TV',
            'Genetic': breeding_genetics_list[11],  #Rattler
            'ShinyBonus': breeding_shiny_bonus_list[22],  #Sail Captain EXP Gain
        },
        2: {
            'Name': 'Donut',
            'Genetic': breeding_genetics_list[14],  #Flashy
            'ShinyBonus': breeding_shiny_bonus_list[25],  #Summoning EXP
        },
        3: {
            'Name': 'Demon Genie',
            'Genetic': breeding_genetics_list[31],  #Superboomer
            'ShinyBonus': breeding_shiny_bonus_list[16],  #Faster Refinery Speed
        },
        4: {
            'Name': 'Flying Worm',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[7],  #Base AGI
        },
        5: {
            'Name': 'Dog',
            'Genetic': breeding_genetics_list[32],  #Peapeapod
            'ShinyBonus': breeding_shiny_bonus_list[23],  #Lower Minimum Travel Time for Sailing
        },
        6: {
            'Name': 'Soda Can',
            'Genetic': breeding_genetics_list[29],  #Fastihoop
            'ShinyBonus': breeding_shiny_bonus_list[21],  #Higher Artifact Find Chance
        },
        7: {
            'Name': 'Gelatinous Cuboid',
            'Genetic': breeding_genetics_list[14],  #Flashy
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        8: {
            'Name': 'Choccie',
            'Genetic': breeding_genetics_list[31],  #Superboomer
            'ShinyBonus': breeding_shiny_bonus_list[3],  #Drop Rate
        },
        9: {
            'Name': 'Biggole Wurm',
            'Genetic': breeding_genetics_list[10],  #Tsar
            'ShinyBonus': breeding_shiny_bonus_list[9],  #Class EXP
        },
        10: {
            'Name': 'Cool Bird',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[6],  #Base STR
        },
        11: {
            'Name': 'Clammie',
            'Genetic': breeding_genetics_list[6],  #Mercenary
            'ShinyBonus': breeding_shiny_bonus_list[10],  #Skill EXP
        },
        12: {
            'Name': 'Octodar',
            'Genetic': breeding_genetics_list[12],  #Cursory
            'ShinyBonus': breeding_shiny_bonus_list[17],  #Base Critter Per Trap
        },
        13: {
            'Name': 'Flombeige',
            'Genetic': breeding_genetics_list[25],  #Trasher
            'ShinyBonus': breeding_shiny_bonus_list[7],  #Base AGI
        },
        14: {
            'Name': 'Stilted Seeker',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[5],  #Base WIS
        },
        15: {
            'Name': 'Hedgehog',
            'Genetic': breeding_genetics_list[32],  #Peapeapod
            'ShinyBonus': breeding_shiny_bonus_list[8],  #Base LUK
        },
    },
}
breeding_total_pets = sum([len(petValues) for worldIndex, petValues in breeding_species_dict.items()])
shiny_days_list = [
    0, 3, 11, 33, 85,
    200, 448, 964, 2013, 4107,
    8227, 16234, 31633, 60989, 116522,
    220874, 415802, 778022, 1447955, 2681786,
]


def getShinyLevelFromDays(days: float) -> int:
    shinyLevel = 0
    for requirement in shiny_days_list:
        if float(days) > requirement:
            shinyLevel += 1
        else:
            break
    return shinyLevel


def getDaysToNextShinyLevel(days: float) -> float:
    shinyLevel = getShinyLevelFromDays(days)
    if shinyLevel >= len(shiny_days_list):
        return 0
    else:
        try:
            daysRemaining = shiny_days_list[shinyLevel] - float(days)
            return daysRemaining
        except Exception as reason:
            logger.warning(f"With shinyLevel of {shinyLevel}, Defaulting Shiny days Remaining to 0. Reason: {reason}")
            return 0


breedabilityDaysList = [
    0.0000,
    2.9722,
    25.5910,
    230.7881,
    2445.8520,
    30113.1432,
    421857.0285,
    6615176.2308,
    114686626.8729,
    2177232407.5082,
]
breedabilityHearts = [1 + safer_math_pow(x, 1.25) for x in range(0, 10)]


def getBreedabilityMultiFromDays(days: float) -> float:
    if not isinstance(days, float):
        try:
            days = float(days)
        except:
            logger.warning(f"Expected days to be float type, got {type(days)}: {days}. Using 0 days instead.")
            days = 0
    result = 1 + math.log(max(1, safer_math_pow(days+1, 0.725)))
    #logger.debug(f"getBreedabilityMultiFromDays: Given {days} days, Breedability Multi = {result}")
    return result


def getBreedabilityHeartFromMulti(multi: float) -> str:
    result = 0
    for reqIndex, requirement in enumerate(breedabilityHearts):
        if multi >= requirement:
            result += 1
        else:
            break
    return f"breedability-heart-{result}"
