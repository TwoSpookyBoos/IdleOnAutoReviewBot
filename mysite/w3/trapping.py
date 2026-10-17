from consts.consts_autoreview import break_keep_it_up
from consts.consts_w3 import max_trapping_critter_types, trapping_quests_requirement_list, trapset_images
from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)


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

    if session_data.account.rift['TrapBoxVacuum'].unlocked:
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

    if session_data.account.rift['TrapBoxVacuum'].unlocked:
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

    if session_data.account.rift['TrapBoxVacuum'].unlocked:
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
    trapping = session_data.account.trapping
    optional_tiers = 0
    true_max = true_max_tiers['Trapping']
    max_tier = true_max - optional_tiers

    highest_wearable_trapset = trapping.highest_wearable_trapset
    placed_traps = trapping.placed_traps
    unplaced_traps = trapping.unplaced_traps
    secret_character_not_using_nature_traps_dict = trapping.non_nature_traps

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
    tier_unlockCritters = trapping.unlocked_critters
    if not trapping.all_critters_unlocked:
        trapping_Advices['UnlockCritters'].append(Advice(
                label=agd_unlockcritters_post_strings[tier_unlockCritters],
                picture_class=trapping.next_critter,
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
        advice.mark_advice_completed()

    # UnusedTraps
    if len(unplaced_traps) > 0:
        for character_index in unplaced_traps:
            trapping_Advices['UnplacedTraps'].append(Advice(
                label=session_data.account.characters[character_index].character_name,
                picture_class=session_data.account.characters[character_index].class_name_icon,
                progression=unplaced_traps[character_index][0],
                goal=unplaced_traps[character_index][1]
            ))

    # BeginnerNatures
    if len(secret_character_not_using_nature_traps_dict) > 0:
        for character_index in secret_character_not_using_nature_traps_dict:
            trapping_Advices['BeginnerNatures'].append(Advice(
                label=session_data.account.characters[character_index].character_name,
                picture_class=session_data.account.characters[character_index].class_name_icon,
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
        for trap_index, trap in enumerate(placed_traps[character_index]):
            if trap.placed:
                if trap.trapset not in good_trap_dict:  # Bad trap sets don't appear in good_trap_dict
                    bad_trap_details[trap_index] = trap
                elif trap.duration not in good_trap_dict[trap.trapset]:  # Bad trap set + duration combos don't appear in good_trap_dict
                    bad_trap_details[trap_index] = trap
                elif int(trap.trapset) == 2 and int(trap.duration) == 432000 and int(trap.exp_variant) != 0:
                    # Using a 5day Wooden Trap that isn't the 0exp variety. Would be better using Royal/Natures in this scenario.
                    bad_trap_details[trap_index] = trap
        if len(bad_trap_details) > 0:
            non_meta_trap_dict[character_index] = len(bad_trap_details)
            non_meta_trap_details[character_index] = bad_trap_details

    for character_index in non_meta_trap_dict:
        subgroup_label = (
            f"{session_data.account.characters[character_index].character_name}: "
            f"{non_meta_trap_dict[character_index]} inefficient traps"
        )
        trapping_Advices['NonMetaTraps'][subgroup_label] = []
        for trap_index, trap in non_meta_trap_details[character_index].items():
            if trap.duration >= 259200:
                #There are some 30, 40, 44, 60hr traps that the game displays as Hours rather than Days so only use Days if >= 3 days
                time = f"{trap.duration / 86400:.0f} day"
            elif trap.duration >= 3600:
                time = f"{trap.duration / 3600:.0f} hour"
            else:
                time = f"{trap.duration / 60:.0f} minutes"
            trap_name = trapset_images.get(trap.trapset, '').replace('-', ' ').title()
            trapping_Advices["NonMetaTraps"][subgroup_label].append(Advice(
                label=f"Trap {trap_index+1}: {time} {trap_name}"
                      f"{' (Only the 200x Critter version is good)' if trap_name == 'Wooden Traps' and trap.duration == 432000 else ''}",
                picture_class=trapset_images.get(trap.trapset, ''),
                completed=False
            ))

    # if len(trapping_Advices["NonMetaTraps"]) > 0:  #Several requests came in to always show this information
    trapping_Advices['CritterTraps'] = getStaticCritterTrapAdviceList(highest_wearable_trapset)
    trapping_Advices['ShinyTraps'] = getStaticShinyTrapAdviceList(highest_wearable_trapset)
    trapping_Advices['EXPTraps'] = getStaticEXPTrapAdviceList(highest_wearable_trapset)

    # Generate Advice Groups

    trapping_AdviceGroups['UnlockCritters'] = AdviceGroup(
        tier=tier_unlockCritters,
        pre_string=f"{pl((['UnlockRemaining'] * (max_trapping_critter_types - tier_unlockCritters)), 'Unlock the final Critter type', 'Continue unlocking new Critter types')}",
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
        completed=min([vman.trapping_level for vman in session_data.account.characters.vmans], default=0) >= 120 or len(trapping_Advices['BeginnerNatures']) == 0
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
    trapping_levels_list = session_data.account.characters.all_skills['Trapping']
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
