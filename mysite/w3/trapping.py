from consts.consts import break_keep_it_up
from consts.consts_w2 import max_vial_level, getReadableVialNames, critter_vials_list
from consts.consts_w3 import max_trapping_critter_types, trapping_quests_requirement_list, trapset_images
from consts.progression_tiers_updater import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.data_formatting import safe_loads, mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)


def getCritterName(input_number):
    reversed_critter_index_list = ['Tuttle', 'Blobfish', 'Honker', 'Dung Beat', 'Bunny', 'Pingy', 'Owlio', 'Mousey', 'Scorpie', 'Crabbo', 'Froge', 'None']
    try:
        return reversed_critter_index_list[input_number]
    except:
        return f'UnknownCritter-{input_number}'

def getUnlockedCritterStatus():
    if session_data.account.sneaking['JadeEmporium']["New Critter"]['Obtained']:
        return [
            12,  # Index of the highest unlocked critter
            max_trapping_critter_types,  # Index of the highest critter possible
            'Tuttle',  # Name of the highest unlocked critter
            'None'  # Name of the next critter to be unlocked
        ]
    else:
        reversed_quest_critters = ['Blobfish', 'Honker', 'Dung Beat', 'Bunny', 'Pingy', 'Owlio', 'Mousey', 'Scorpie', 'Crabbo', 'Froge', 'None']
        reversedQuestIndexList = [
            'Blobbo2', 'Lord_of_the_Hunt10', 'Lord_of_the_Hunt9', 'Lord_of_the_Hunt8', 'Lord_of_the_Hunt7', 'Lord_of_the_Hunt6',
            'Lord_of_the_Hunt5', 'Lord_of_the_Hunt4', 'Lord_of_the_Hunt3', 'Lord_of_the_Hunt2'
        ]
        reversed_required_status_quest_index_list = [1,0,0,0,0,0,0,0,0,0,0]
        highest_critter = (len(reversed_quest_critters)-1)
        #Critters available to be trapped can be found by quest status, except for the current last critter of Tuttles
        #["QuestComplete_0"] through _9 are dictionaries.
        #Keys are "Lord_of_the_Hunt2" through 10. Values are 1 for completed, 0 for in progress I think, and -1 for not started.
        #1 = buy a trap set quest, irrelevant
        #Lord_of_the_Hunt2 = Froge
        #3 = Crabbo
        #4 = Scorpie
        #5 = Mousey
        #6 = Owlio
        #7 = Pingy
        #8 = Bunny
        #9 = Dung Beat
        #10 = Honker when quest is STARTED (value of 0 or 1)
        #11 = the trophy quest, irrelevant
        #Blobfish are unlocked after "Blobbo2" quest is completed (value of 1)

        quest_index = 0
        for character_index in range(0, session_data.account.character_count):
            try:
                char_quests = session_data.account.all_quests[character_index]
                for quest_index in range(0, len(reversedQuestIndexList)):
                    if (
                        char_quests[reversedQuestIndexList[quest_index]] >= reversed_required_status_quest_index_list[quest_index]
                        and quest_index < highest_critter
                    ):  #and the quest is better than what is already known to be the best
                        #print("Trapping.getUnlockedCritterStatus~ INFO New highest critter found on character", character_index, "! Changing from",highest_critter,"to",quest_index)
                        #logger.debug(f"New highest critter available from character {character_index}! Changing from {reversed_quest_critters[highest_critter]} to {reversed_quest_critters[quest_index]}")
                        highest_critter = quest_index
            except Exception as reason:
                logger.exception(f"Could not retrieve {reversedQuestIndexList[quest_index]} status on Character{character_index} because {reason}")
                #print("Trapping.getUnlockedCritterStatus~ EXCEPTION Could not retrieve quest status:", character_index, quest_index, reversedQuestIndexList[quest_index], reason)
            character_index += 1
            quest_index = 0
        #print("Trapping.getUnlockedCritterStatus~ OUTPUT highest_critter:",highest_critter, reversed_quest_critters[highest_critter])
        try:
            return [
                (len(reversed_quest_critters)-highest_critter),  # Index of the highest unlocked critter
                max_trapping_critter_types,  # Index of the highest critter possible
                reversed_quest_critters[highest_critter],  #Name of the highest unlocked critter
                getCritterName(highest_critter)  #Name of the next critter to be unlocked
            ]
        except:
            logger.exception(f"Unable to return highest_critter name in reversed_quest_critters at index {highest_critter}")
            return f'UnknownCritter-{highest_critter}'

def getPlacedTrapsDict():
    placed_traps = {}
    for character_index in range(0, session_data.account.character_count):
        try:
            placed_traps[character_index] = safe_loads(session_data.account.raw_data[f'PldTraps_{character_index}'])
        except:
            logger.exception(f"Unable to retrieve 'PldTraps_{character_index}'")
            placed_traps[character_index] = []
    return placed_traps

def getCharactersWithUnplacedTraps(trapping_levels, placed_traps):
    unused_traps = {}
    max_placable_traps_list = []
    trapset_level_requirement_list = [48,40,35,25,15,5,1]
    trapset_placable_count_list = [7,6,5,4,3,2,1]
    #Equipped trap set is in EquipOrder_0 through 9, standard character indexing again, dictionary of 1, element of 4. Stored as a string.
    #Required trap levels for each increased set that gives another slot:
    #Cardboard = Lv1, 1 slot
    #Silkskin = Lv5, 2 slots
    #Wooden = Lv15, 3 slots
    #Nature = Lv25, 4 slots
    #Steel = Lv35, 5 slots
    #Meaty = Lv40, 6 slots
    #Royal = LV48, 7 slots
    #Egalitarian Royal Traps do not give any extra slots, can be ignored.
    #Forbidden Traps do not give any extra slots, can be ignored.
    #Containment of the Zrgyios does not give any extra slots, can be ignored.

    #Step 1 = Get number of expected traps
    #Bonus trap slot comes from the Call Me Ash bubble, which is an Int stored at ["CauldronInfo"][1][11]. If it is level 1 or higher, the extra trap slot is always given. Does not need to be equipped.
    bonus_trap_slot = 0
    if session_data.account.alchemy_bubbles['Call Me Ash']['Level'] >= 1:
        bonus_trap_slot = 1

    for char in session_data.account.all_characters:
        for trap_list_index, requirement in enumerate(trapset_level_requirement_list):
            try:
                if (
                    len(max_placable_traps_list) <= char.character_index
                    and trapping_levels[char.character_index] >= trapset_level_requirement_list[trap_list_index]
                ):
                    max_placable_traps_list.append(trapset_placable_count_list[trap_list_index] + bonus_trap_slot)
            except:
                logger.exception(f'Unable to append to max_placable_traps_list')
        if len(max_placable_traps_list)-1 < char.character_index:
            max_placable_traps_list.append(0)

    #Step 2 = Get number of placed traps
    if len(placed_traps) > 0:
        for char_key in placed_traps:
            char_placed_traps = 0
            for trap_details in placed_traps[char_key]:
                if trap_details[0] != -1:
                    char_placed_traps += 1
            if max_placable_traps_list[char_key] - char_placed_traps > 0:
                unused_traps[char_key] = [str(char_placed_traps), str(max_placable_traps_list[char_key])]
    return unused_traps

def getSecretClassTrapStatus(placed_traps):
    secret_character_not_using_nature_traps_dict = {}
    for jman in session_data.account.jmans:
        if jman.trapping_level >= 25:  #the level required to wear Nature Traps
            for trap_details in placed_traps[jman.character_index]:
                if trap_details[0] != -1 and trap_details[5] != 3:
                    if jman.character_index in secret_character_not_using_nature_traps_dict.keys():
                        secret_character_not_using_nature_traps_dict[jman.character_index] += 1
                    else:
                        secret_character_not_using_nature_traps_dict[jman.character_index] = 1
    return secret_character_not_using_nature_traps_dict

def getUnmaxedCritterVialStatus():
    unmaxed_critter_vials_count = 0
    for vial_name in critter_vials_list:
        if session_data.account.alchemy_vials[vial_name]['Level'] < max_vial_level:
            unmaxed_critter_vials_count += 1
    return unmaxed_critter_vials_count != 0

def getStaticCritterTrapAdviceList(highest_trapset: int) -> dict[str, list[Advice]]:
    advices = {
        'Efficiency for Manually Claimed traps': [],
    }
    if highest_trapset >= 6:
        listIndexManualAdvice = 6
    elif highest_trapset >= 5:
        listIndexManualAdvice = 5
    else:
        listIndexManualAdvice = 0

    if highest_trapset >= 6:
        listIndexVaccuumAdvice = 6
    elif highest_trapset >= 5:
        listIndexVaccuumAdvice = 5
    elif highest_trapset >= 2:
        listIndexVaccuumAdvice = 2
    else:
        listIndexVaccuumAdvice = 0

    manualCritterTrapsDict = {
        0: [["Cardboard 20 Minutes", "Cardboard 1 Hour", "Cardboard 8 Hours", "Cardboard 20 Hours"], ["3x/hr", "2x/hr", "1.25x/hr", "1x/hr"]],
        5: [["Cardboard 20 Minutes", "Meaty 1 Hour", "Meaty 10 Hours", "Cardboard 8 Hours", "Cardboard 20 Hours"], ["3x/hr", "3x/hr", "1.5x/hr", "1.25x/hr", "1x/hr"]],
        6: [["Royal 20 Minutes", "Royal 1 Hour", "Royal 10 Hours", "Royal 40 Hours"], ["6x/hr", "4x/hr", "2.1x/hr", "1.75x/hr"]]
    }
    vaccuumCritterTrapsDict = {
        0: [["Cardboard 20 Hours"], ["0.83x/hr"]],
        2: [["Wooden 5 Days", "Cardboard 20 Hours"], ["1.67x/hr", "0.83x/hr"]],
        5: [["Wooden 5 Days", "Meaty 8 Days", "Cardboard 20 Hours"],["1.67x/hr", "1.15x/hr", "0.83x/hr"]],
        6: [["Wooden 5 Days", "Royal 40 Hours", "Meaty 8 Days", "Royal 10 Hours"], ["1.67x/hr", "1.46x/hr", "1.15x/hr", "0.88x/hr"]]
    }

    for counter in range(0, len(manualCritterTrapsDict[listIndexManualAdvice][0])):
        advices["Efficiency for Manually Claimed traps"].append(Advice(
            label=manualCritterTrapsDict[listIndexManualAdvice][0][counter],
            picture_class=f"{manualCritterTrapsDict[listIndexManualAdvice][0][counter].lower().split(' ')[0]}-traps",
            progression=manualCritterTrapsDict[listIndexManualAdvice][1][counter]
        ))

    if session_data.account.rift['TrapBoxVacuum']:
        advices["Efficiency for Rift's Daily traps"] = []
        for counter in range(0, len(vaccuumCritterTrapsDict[listIndexVaccuumAdvice][0])):
            advices["Efficiency for Rift's Daily traps"].append(Advice(
                label=vaccuumCritterTrapsDict[listIndexVaccuumAdvice][0][counter],
                picture_class=f"{vaccuumCritterTrapsDict[listIndexVaccuumAdvice][0][counter].lower().split(' ')[0]}-traps",
                progression=vaccuumCritterTrapsDict[listIndexVaccuumAdvice][1][counter]
            ))

    return advices

def getStaticShinyTrapAdviceList(highest_trapset: int) -> dict[str, list[Advice]]:
    advices = {
        'Shiny Chance Multi for Manually Claimed traps': []
    }
    num_of_vaccuum_suggestions = 2
    #"The highest Shiny chance increasing traps are: Royal 20min, Royal 1hr, Silkskin 20min, Silkskin 1hr, and Royal 10hrs."
    shiny_traps_label_list = ["Royal 20 Minutes", "Royal 1 Hour", "Silkskin 20 Minutes", "Silkskin 1 Hour", "Royal 10 Hours", "Silkskin 20 Hours", "Royal 40 Hours"]
    shiny_traps_item_name_list = ["royal-traps", "royal-traps", "silkskin-traps", "silkskin-traps", "royal-traps", "silkskin-traps", "royal-traps"]
    shiny_traps_required_trap_index_list = [6, 6, 1, 1, 6, 1, 6]
    shiny_traps_eff_per_hour_list = ["12x/hr", "8x/hr", "3x/hr", "2.1x/hr", "3.8x/hr", "1.25x/hr", "2.6x/hr"]
    for counter in range(0, len(shiny_traps_label_list) - num_of_vaccuum_suggestions):
        if highest_trapset >= shiny_traps_required_trap_index_list[counter]:
            advices['Shiny Chance Multi for Manually Claimed traps'].append(Advice(
                label=shiny_traps_label_list[counter],
                picture_class=shiny_traps_item_name_list[counter],
                progression=shiny_traps_eff_per_hour_list[counter]
            ))

    if session_data.account.rift['TrapBoxVacuum']:
        advices["Shiny Chance Multi for Rift's Daily traps"] = []
        for counter in range(len(shiny_traps_label_list) - num_of_vaccuum_suggestions, len(shiny_traps_label_list)):
            if highest_trapset >= shiny_traps_required_trap_index_list[counter]:
                advices["Shiny Chance Multi for Rift's Daily traps"].append(Advice(
                    label=shiny_traps_label_list[counter],
                    picture_class=shiny_traps_item_name_list[counter],
                    progression=shiny_traps_eff_per_hour_list[counter]
                ))
    return advices

def getStaticEXPTrapAdviceList(highest_trapset) -> dict[str, list[Advice]]:
    advices = {
        'Best Experience for Manually Claimed traps': []
    }
    num_of_vaccuum_suggestions = 1
    # The highest EXP traps are: Nature 8hrs and Nature 20hrs.
    exp_traps_label_list = ['Natural 8 Hours', 'Natural 20 Hours']
    exp_traps_item_name_list = ['natural-traps', 'natural-traps']
    exp_traps_required_trap_index_list = [3, 3]
    exp_traps_eff_per_hour_list = ['5x/hr', '3.12x/hr']
    for counter in range(0, len(exp_traps_label_list) - num_of_vaccuum_suggestions):
        if highest_trapset >= exp_traps_required_trap_index_list[counter]:
            advices['Best Experience for Manually Claimed traps'].append(Advice(
                label=exp_traps_label_list[counter],
                picture_class=exp_traps_item_name_list[counter],
                progression=exp_traps_eff_per_hour_list[counter]
            ))

    if session_data.account.rift['TrapBoxVacuum']:
        advices["Best Experience for Rift's Daily traps"] = []
        for counter in range(len(exp_traps_label_list) - num_of_vaccuum_suggestions, len(exp_traps_label_list)):
            if highest_trapset >= exp_traps_required_trap_index_list[counter]:
                advices["Best Experience for Rift's Daily traps"].append(
                    Advice(label=exp_traps_label_list[counter], picture_class=exp_traps_item_name_list[counter], progression=exp_traps_eff_per_hour_list[counter],
                           goal="", unit=""))
    return advices

def getProgressionTiersAdviceGroup(trapping_levels_list: list[int]):
    trapping_Advices = {
        'UnlockCritters': [],
        'UnplacedTraps': [],
        'BeginnerNatures': [],
        'NonMetaTraps': {},
        'CritterTraps': [],
        'ShinyTraps': [],
        'EXPTraps': []
    }
    trapping_AdviceGroups = {}
    highestUnlockedCritter = getUnlockedCritterStatus()
    optional_tiers = 0
    true_max = true_max_tiers['Trapping']
    max_tier = true_max - optional_tiers

    highest_wearable_trapset = 0
    trapset_level_requirement_list = [1, 5, 15, 25, 35, 40, 48]
    for index in range(0, len(trapset_level_requirement_list)):
        if max(trapping_levels_list) >= trapset_level_requirement_list[index]:
            highest_wearable_trapset = index

    placed_traps = getPlacedTrapsDict()
    unplaced_traps = getCharactersWithUnplacedTraps(trapping_levels_list, placed_traps)
    secret_character_not_using_nature_traps_dict = getSecretClassTrapStatus(placed_traps)

    # UnlockCritters
    agd_unlockcritters_post_strings = [
        "",
        "Froge critters are unlocked after completing Lord of the Hunt's quest: Pelt for the Pelt God",
        "Crabbo critters are unlocked after completing Lord of the Hunt's quest: Frogecoin to the MOON!",
        "Scorpie critters are unlocked after completing Lord of the Hunt's quest: Yet another Cartoon Reference",
        "Mousey critters are unlocked after completing Lord of the Hunt's quest: Small Stingers, Big Owie",
        "Owlio critters are unlocked after completing Lord of the Hunt's quest: The Mouse n the Molerat",
        "Pingy critters are unlocked after completing Lord of the Hunt's quest: Happy Tree Friend",
        "Bunny critters are unlocked after completing Lord of the Hunt's quest: Noot Noot!",
        "Dung Beat critters are unlocked after completing Lord of the Hunt's quest: Bunny you Should Say That!",
        "Honker critters are unlocked after completing Lord of the Hunt's quest: Rollin' Thunder",
        "Blobfish critters are unlocked after completing Blobbo's quest: Glitter Critter",
        "Tuttle critters are unlocked in W6 Jade Emporium",
        ""
    ]
    tier_unlockCritters = highestUnlockedCritter[0]
    if tier_unlockCritters != max_trapping_critter_types:  # unlocked not equal to the max possible to unlock.
        trapping_Advices['UnlockCritters'].append(Advice(
                label=agd_unlockcritters_post_strings[highestUnlockedCritter[0]],
                picture_class=highestUnlockedCritter[3],
                progression=0,
                goal=1
        ))
        if 2 <= tier_unlockCritters < 11:  # Show only the quests with Critter requirement
            for required_item_code_name, required_quantity in trapping_quests_requirement_list[tier_unlockCritters - 2]['RequiredItems'].items():
                #logger.debug(f"required_item_code_name = {required_item_code_name}")
                item_asset = session_data.account.all_assets.get(required_item_code_name)
                trapping_Advices['UnlockCritters'].append(Advice(
                    label=item_asset.name,
                    picture_class=item_asset.name,
                    progression=item_asset.amount,
                    goal=required_quantity
                ))
    for advice in trapping_Advices['UnlockCritters']:
        mark_advice_completed(advice)

    # UnusedTraps
    if len(unplaced_traps) > 0:
        for character_index in unplaced_traps:
            trapping_Advices['UnplacedTraps'].append(Advice(
                label=session_data.account.all_characters[character_index].character_name,
                picture_class=session_data.account.all_characters[character_index].class_name_icon,
                progression=unplaced_traps[character_index][0],
                goal=unplaced_traps[character_index][1]
            ))

    # BeginnerNatures
    if len(secret_character_not_using_nature_traps_dict) > 0:
        for character_index in secret_character_not_using_nature_traps_dict:
            trapping_Advices['BeginnerNatures'].append(Advice(
                label=session_data.account.all_characters[character_index].character_name,
                picture_class=session_data.account.all_characters[character_index].class_name_icon,
                progression=secret_character_not_using_nature_traps_dict[character_index],
                goal=0
            ))

    # NonMetaTraps
    # hasUnmaxedCritterVial = getUnmaxedCritterVialStatus()
    good_trap_dict = {
        0: [1200, 3600, 28800, 72000],  # Cardboard Traps
        1: [1200, 3600, 28800, 72000],  # Silkskin Traps. 14400 is excluded.
        2: [432000],  # Wooden Traps. Only 5 days 0xp is good, and only if they still have Vials to complete
        3: [28800, 72000],  # Natural Traps. 8hr and 20hr are good, other options are bad.
        6: [1200, 3600, 36000, 144000, 604800]  # Royal Traps. All but the 28day are good.
    }
    if max(trapping_levels_list) < 48:
        good_trap_dict[5] = [3600, 36000, 108000]  # Before being able to wear Royals, Meaty traps give more critter efficiency than Cardboard
    non_meta_trap_dict = {}
    non_meta_trap_details = {}
    for character_index in placed_traps:
        bad_trap_details = {}
        for trap_index, trap_data in enumerate(placed_traps[character_index]):
            if trap_data[0] != -1:  # -1 is an unplaced trap
                if trap_data[5] not in good_trap_dict.keys():  # Bad trap sets don't appear in good_trap_dict
                    bad_trap_details[trap_index] = trap_data
                elif trap_data[6] not in good_trap_dict[trap_data[5]]:  # Bad trap set + duration combos don't appear in good_trap_dict
                    bad_trap_details[trap_index] = trap_data
                elif int(trap_data[5]) == 2 and int(trap_data[6]) == 432000 and int(trap_data[7]) != 0:
                    # Using a 5day Wooden Trap that isn't the 0exp variety. Would be better using Royal/Natures in this scenario.
                    bad_trap_details[trap_index] = trap_data
        if len(bad_trap_details) > 0:
            non_meta_trap_dict[character_index] = len(bad_trap_details)
            non_meta_trap_details[character_index] = bad_trap_details

    for character_index in non_meta_trap_dict:
        subgroup_label = (
            f"{session_data.account.all_characters[character_index].character_name}: "
            f"{non_meta_trap_dict[character_index]} inefficient traps"
        )
        trapping_Advices['NonMetaTraps'][subgroup_label] = []
        for trap_index, trap_details in non_meta_trap_details[character_index].items():
            if trap_details[6] >= 259200:
                #There are some 30, 40, 44, 60hr traps that the game displays as Hours rather than Days so only use Days if >= 3 days
                time = f"{trap_details[6] / 86400:.0f} day"
            elif trap_details[6] >= 3600:
                time = f"{trap_details[6] / 3600:.0f} hour"
            else:
                time = f"{trap_details[6] / 60:.0f} minutes"
            trap_name = trapset_images.get(trap_details[5], '').replace('-', ' ').title()
            trapping_Advices["NonMetaTraps"][subgroup_label].append(Advice(
                label=f"Trap {trap_index+1}: {time} {trap_name}"
                      f"{' (Only the 200x Critter version is good)' if trap_name == 'Wooden Traps' and trap_details[6] == 432000 else ''}",
                picture_class=trapset_images.get(trap_details[5], ''),
                completed=False
            ))

    # if len(trapping_Advices["NonMetaTraps"]) > 0:  #Several requests came in to always show this information
    trapping_Advices['CritterTraps'] = getStaticCritterTrapAdviceList(highest_wearable_trapset)
    trapping_Advices['ShinyTraps'] = getStaticShinyTrapAdviceList(highest_wearable_trapset)
    trapping_Advices['EXPTraps'] = getStaticEXPTrapAdviceList(highest_wearable_trapset)

    # Generate Advice Groups

    trapping_AdviceGroups['UnlockCritters'] = AdviceGroup(
        tier=highestUnlockedCritter[0],
        pre_string=f"{pl((['UnlockRemaining'] * (max_trapping_critter_types - highestUnlockedCritter[0])), 'Unlock the final Critter type', 'Continue unlocking new Critter types')}",
        advices=trapping_Advices['UnlockCritters'],
    )
    trapping_AdviceGroups['UnplacedTraps'] = AdviceGroup(
        tier='',
        pre_string=f"Place unused trap{pl(trapping_Advices['UnplacedTraps'])} (may require better Trap Set!)",
        advices=trapping_Advices['UnplacedTraps'],
        informational=True,
        completed=False
    )
    trapping_AdviceGroups['BeginnerNatures'] = AdviceGroup(
        tier='',
        pre_string=f"Place only Nature Traps on your Beginner{pl(trapping_Advices['BeginnerNatures'])}",
        advices=trapping_Advices['BeginnerNatures'],
        post_string=f"Nature EXP-only traps are recommended for Maestro's Right Hand of Action and Voidwalker's Species Epoch talents."
                    f" You will get ZERO critters from Nature Traps, but the bonus critters from those 2 talents more than make up for this loss!",
        informational=True,
        completed=min([vman.trapping_level for vman in session_data.account.vmans], default=0) >= 120 or len(trapping_Advices['BeginnerNatures']) == 0
    )
    trapping_AdviceGroups['NonMetaTraps'] = AdviceGroup(
        tier='',
        pre_string='Inefficient Trap Types or Durations',
        advices=trapping_Advices['NonMetaTraps'],
        informational=True
    )
    trapping_AdviceGroups['CritterTraps'] = AdviceGroup(
        tier='',
        pre_string='Best Critter-Focused traps from your available Trap Sets',
        advices=trapping_Advices['CritterTraps'],
        post_string='Set critter traps with your Hunter/BM/WW after maximizing Trapping Efficiency',
        informational=True,
        completed=len(trapping_Advices['NonMetaTraps']) == 0
    )
    trapping_AdviceGroups['ShinyTraps'] = AdviceGroup(
        tier='',
        pre_string='Best Shiny Chance-Focused traps from your available Trap Sets',
        advices=trapping_Advices['ShinyTraps'],
        post_string='Wear the Shiny Snitch prayer when Collecting. Shorter trap durations will earn more total Shiny Critters per day',
        informational=True,
        completed=len(trapping_Advices["NonMetaTraps"]) == 0
    )
    trapping_AdviceGroups["EXPTraps"] = AdviceGroup(
        tier='',
        pre_string='Best EXP-Focused traps from your available Trap Sets',
        advices=trapping_Advices['EXPTraps'],
        post_string='Set EXP traps with your Mman/Vman after maximizing Trapping EXP',
        informational=True,
        completed=len(trapping_Advices['NonMetaTraps']) == 0
    )
    overall_SectionTier = min(max_tier, tier_unlockCritters)
    return trapping_AdviceGroups, overall_SectionTier, max_tier

def getTrappingAdviceSection() -> AdviceSection:
    trapping_levels_list = session_data.account.all_skills['Trapping']
    if max(trapping_levels_list) < 1:
        trapping_AdviceSection = AdviceSection(
            name='Trapping',
            tier='0/0',
            header='Come back after unlocking the Trapping skill in World 3!',
            picture='Trapping_Cardboard_Traps.png',
            unreached=True
        )
        return trapping_AdviceSection

    #Generate AdviceGroups
    trapping_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceGroup(trapping_levels_list)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    trapping_AdviceSection = AdviceSection(
        name='Trapping',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Trapping tier met: {tier_section}{break_keep_it_up if overall_SectionTier >= max_tier else ''}",
        picture='Trapping_Cardboard_Traps.png',
        groups=trapping_AdviceGroupDict.values()
    )

    return trapping_AdviceSection
