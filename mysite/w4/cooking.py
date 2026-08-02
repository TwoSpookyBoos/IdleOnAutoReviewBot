from consts.progression_tiers import true_max_tiers, cooking_progressionTiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, AdviceType, build_subgroup_label
from consts.consts_w4 import max_meal_count, max_meal_plate_level, cooking_close_enough, meal_counts_by_world
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.text_formatting import pl

logger = get_logger(__name__)

def getCookingProgressionTiersAdviceGroups(highest_cooking_skill_level, cooking, dchef_level, vmans, challenge_account, atom_fluoride_level):
    cooking_Advices = {
        'Tiers': {}
    }
    cooking_AdviceGroupDict = {}
    tier_Cooking = 0
    optional_tiers = 1
    true_max = true_max_tiers['Cooking']
    max_tier = true_max - optional_tiers
    spice_images_by_world = {
        4: 'nebulon-mantle-spice',
        5: 'wurm-catacombs-spice',
        6: 'dharma-mesa-spice',
        7: 'murky-trenches-spice',
        8: ''
    }

    # Assess Tiers
    for tier_number, requirements in cooking_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        #Cooking level
        if highest_cooking_skill_level < requirements.get('CookingLevel', 0):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label="Unlock the Cooking skill in World 4 town",
                    picture_class='cooking',
                    progression=highest_cooking_skill_level,
                    goal=1
                ))

        #Diamond Chef level
        if dchef_level < requirements.get('DiamondChef', 0):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label="Unlock and level Diamond Chef bubble to at least 15",
                    picture_class='diamond-chef',
                    progression=dchef_level,
                    goal=15
                ))

        #Voidwalker created or troll/challenge account with no beginners
        if len(vmans) == 0 and not challenge_account:
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label="Unlock a Voidwalker",
                    picture_class="voidwalker-icon"
                ))

        #Fluoride atom level
        if atom_fluoride_level < requirements.get('Fluoride', 0):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label="Unlock Fluoride - Void Plate Chef in the {{Atom Collider|#atom-collider}} from W3 Construction skill",
                    picture_class='fluoride'
                ))

        #Total meal plate levels
        if cooking['PlayerTotalMealLevels'] < requirements.get('TotalMealLevels', 0):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Reach {requirements.get('TotalMealLevels', 0)}+ total meal levels",
                    picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                    progression=cooking['PlayerTotalMealLevels'],
                    goal=requirements.get('TotalMealLevels', 0)
                ))

        #Unlock all meals per world
        if requirements.get('AllMealsUnlockedByWorld', 0) > 0:
            world_number = requirements['AllMealsUnlockedByWorld']
            if cooking['MealsUnlockedByWorld'][world_number] < meal_counts_by_world[world_number]:
                add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
                if subgroup_label in cooking_Advices['Tiers']:
                    cooking_Advices['Tiers'][subgroup_label].append(Advice(
                        label=f"Unlock the remaining {meal_counts_by_world[world_number] - cooking['MealsUnlockedByWorld'][world_number]} W{world_number} meal"
                              f"{pl(meal_counts_by_world[world_number] - cooking['MealsUnlockedByWorld'][world_number])}",
                        picture_class=spice_images_by_world.get(world_number, ''),
                        progression=cooking['MealsUnlockedByWorld'][world_number],
                        goal=meal_counts_by_world[world_number]
                    ))

        # Unlocked meals under 11
        if cooking['UnlockedMealsUnder11'] > requirements.get('UnlockedMealsUnder11', 9999999999999):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Level up the remaining {cooking['UnlockedMealsUnder11']} meal"
                          f"{pl(cooking['UnlockedMealsUnder11'])} to 11+ for Diamond Chef",
                    picture_class='diamond-chef',
                    progression=cooking['MealsUnlocked'] - cooking['UnlockedMealsUnder11'],
                    goal=cooking['MealsUnlocked']
                ))

        # All meals under 11
        if cooking['MealsUnder11'] > requirements.get('TotalMealsUnder11', 9999999999999):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Level up the remaining {cooking['MealsUnder11']} meal"
                          f"{pl(cooking['MealsUnder11'])} to 11+ for Diamond Chef",
                    picture_class='diamond-chef',
                    progression=max_meal_count - cooking['MealsUnder11'],
                    goal=max_meal_count
                ))

        #Unlocked meals under 30
        if cooking['UnlockedMealsUnder30'] > requirements.get('UnlockedMealsUnder30', 9999999999999):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Level up the remaining {cooking['UnlockedMealsUnder30']} meal"
                          f"{pl(cooking['UnlockedMealsUnder30'])} to 30+ for Fluoride",
                    picture_class='fluoride',
                    progression=cooking['MealsUnlocked'] - cooking['UnlockedMealsUnder30'],
                    goal=cooking['MealsUnlocked']
                ))

        #All meals under 30
        if cooking['MealsUnder30'] > requirements.get('TotalMealsUnder30', 9999999999999):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Level up the remaining {cooking['MealsUnder30']} meal"
                          f"{pl(cooking['MealsUnder30'])} to 30+ for Fluoride",
                    picture_class='fluoride',
                    progression=max_meal_count - cooking['MealsUnder30'],
                    goal=max_meal_count
                ))

        #Max plate level for meals
        if cooking['PlayerMaxPlateLvl'] < requirements.get('MaxPlateLevel', 0):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Unlock max level {max_meal_plate_level} plates",
                    picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                    progression=cooking['PlayerMaxPlateLvl'],
                    goal=max_meal_plate_level
                ))

        #MaxRemainingMeals
        if cooking['MaxRemainingMeals'] > requirements.get('MaxRemainingMeals', 9999999999999):
            add_subgroup_if_available_slot(cooking_Advices['Tiers'], subgroup_label)
            if subgroup_label in cooking_Advices['Tiers']:
                cooking_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Finish all {max_meal_count} meals to level {max_meal_plate_level}"
                          f"<br>{cooking['CurrentRemainingMeals']} remaining levels = "
                          f"{cooking['NMLBDays']} NMLB triggers to go!",
                    picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                    progression=cooking['PlayerTotalMealLevels'],
                    goal=max_meal_count * max_meal_plate_level,
                ))

        # Final tier check
        if subgroup_label not in cooking_Advices['Tiers'] and tier_Cooking == tier_number - 1:
            tier_Cooking = tier_number

    

    # Generate Advice Groups
    cooking_AdviceGroupDict['Tiers'] = AdviceGroup(
        tier=tier_Cooking,
        pre_string='Progress Cooking',
        advices=cooking_Advices['Tiers']
    )

    


    overall_SectionTier = min(true_max, tier_Cooking)
    return cooking_AdviceGroupDict, overall_SectionTier, max_tier, true_max


def getCookingMealsAdviceGroup() -> AdviceGroup:
    meals_advice = [
        Advice(
            label=f"{meal_name}: {meal_values['Description']}"
                  f"<br>Tier {meal_values['RibbonTier']} Ribbon = {meal_values['RibbonMulti']:.3f}x multi",
            picture_class=meal_values['Image'],
            progression=meal_values['Level'],
            goal=max_meal_plate_level,
            resource=f"meal-ribbon-{meal_values['RibbonTier']}",
            informational=True
        ) for meal_name, meal_values in session_data.account.meals.items()
    ]
    for advice in meals_advice:
        advice.mark_advice_completed()

    meals_ag = AdviceGroup(
        tier='',
        pre_string='All Meal levels and ribbons',
        advices=meals_advice,
        informational=True
    )
    return meals_ag


def getCurrentTierStrategyAdviceGroup(cooking, dchef_level, atom_fluoride_level, tier_Cooking, max_tier, vmans):
    currenttier_Advices = []
    # Generate CurrentTier Advice
    if session_data.account.cooking['MealsUnlocked'] < max_meal_count:
        currenttier_Advices.append(Advice(
            label='Work on unlocking all meals. This may mean pushing maps and Breeding progress to unlock new spices!',
            picture_class='taste-test',
            progression=cooking['MealsUnlocked'],
            goal=max_meal_count,
        ))
    for world in range(0, 9):
        if session_data.account.highest_world_reached >= world and cooking['MealsUnlockedByWorld'][world] < meal_counts_by_world[world]:
            currenttier_Advices.append(Advice(
                label=f"Unlock All W{world} Meals",
                picture_class='taste-test',
                progression=cooking['MealsUnlockedByWorld'][world],
                goal=meal_counts_by_world[world],
            ))

    if cooking['UnlockedMealsUnder11'] > 0 and dchef_level >= 1:
        currenttier_Advices.append(Advice(
            label="Level all unlocked plates to 11+ for Diamond Chef bonus",
            picture_class='diamond-chef',
            progression=cooking['MealsUnlocked'] - cooking['UnlockedMealsUnder11'],
            goal=cooking['MealsUnlocked'],
        ))
    if cooking['UnlockedMealsUnder30'] > 0 and atom_fluoride_level > 0:
        currenttier_Advices.append(Advice(
            label="All unlocked plates to 30+ for Fluoride bonus",
            picture_class='fluoride',
            progression=cooking['MealsUnlocked'] - cooking['UnlockedMealsUnder30'],
            goal=cooking['MealsUnlocked'],
        ))
    if tier_Cooking <= 3:
        currenttier_Advices.append(Advice(
            label="All +% Meal Cooking Speed meals (Egg, Corndog, Cabbage, etc.)",
            picture_class=session_data.account.meals['Egg']['Image'],
            completed=False
        ))

    if tier_Cooking < 4:
        currenttier_Advices.append(Advice(
            label="Any fast meal to level (5% of your Daily Ladles or less)",
            picture_class='blood-marrow',
            completed=False
        ))
    # Elif they have Voidwalker and meals still to level, replace the generic "any faster meal" with the more specific Vman Blood Marrow note
    elif 4 <= tier_Cooking < max_tier:
        currenttier_Advices.append(Advice(
            label="Any! Voidwalker's Blood Marrow buff scales with EVERY meal level!",
            picture_class='blood-marrow',
            completed=False
        ))
        anyVWMaxBooked = False
        bestBMBook = 0
        anyVWMaxLeveled = False
        bestBMPresetLevel = 0
        # 59: {"Name": "Blood Marrow", "Tab": "Voidwalker"},
        # If Blood Marrow is not max booked, recommend booking it
        # _customBlock_TalentCalc and if (59 == d) in source. Last update v2.492
        # Math.min(1.012, 1 + k._customBlock_GetTalentNumber(1, 59) / 100)
        # 1 + ((2.1 * level) / (level + 220) / 100) = 1.012 => level = 293.33
        max_efficiency_level = min(294, session_data.account.library['MaxBookLevel'])
        # If Blood Marrow is not leveled on either preset, recommend leveling it
        for vman in vmans:
            # Book level
            if vman.max_talents.get('59', 0) >= max_efficiency_level:
                anyVWMaxBooked = True
            if vman.max_talents.get('59', 0) > bestBMBook:
                bestBMBook = vman.max_talents.get('59', 0)

            # Preset level
            if (
                    vman.current_preset_talents.get('59', 0) >= max_efficiency_level
                    or vman.secondary_preset_talents.get('59', 0) >= max_efficiency_level
            ):
                anyVWMaxLeveled = True
            if vman.current_preset_talents.get('59', 0) >= bestBMPresetLevel:
                bestBMPresetLevel = vman.current_preset_talents.get('59', 0)
            if vman.secondary_preset_talents.get('59', 0) >= bestBMPresetLevel:
                bestBMPresetLevel = vman.secondary_preset_talents.get('59', 0)

        if cooking['MaxRemainingMeals'] > cooking_close_enough:
            if not anyVWMaxBooked:
                session_data.account.alerts_Advices['World 4'].append(Advice(
                    label="No Voidwalkers with {{ Blood Marrow|#cooking }} talent max booked!",
                    picture_class="beginner-talent-book",
                    progression=bestBMBook,
                    goal=max_efficiency_level
                ))
            if not anyVWMaxLeveled:
                session_data.account.alerts_Advices['World 4'].append(Advice(
                    label="No Voidwalkers with {{ Blood Marrow|#cooking }} talent maxed in any presets!",
                    picture_class="talent-preset-1",
                    progression=bestBMPresetLevel,
                    goal=max_efficiency_level
                ))

    # If not all meals are maxed
    if cooking['PlayerTotalMealLevels'] < cooking['MaxTotalMealLevels']:
        current_remainingMeals = cooking['CurrentRemainingMeals']
        current_maxMealLevel = cooking['PlayerMaxPlateLvl']
        max_remainingMeals = cooking['MaxRemainingMeals']

        if tier_Cooking < max_tier:
            if current_remainingMeals != max_remainingMeals:
                currenttier_Advices.append(Advice(
                    label=f"{AdviceType.INFO.value} - Current possible: {cooking['MealsUnlocked']}/{max_meal_count} meals, "
                          f"{current_maxMealLevel}/{max_meal_plate_level} plate levels"
                          f"<br>{current_remainingMeals} meal levels = {cooking['NMLBDays']} NMLB triggers to go!",
                    picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                    progression=cooking['PlayerTotalMealLevels'],
                    goal=cooking['MealsUnlocked'] * current_maxMealLevel,
                ))

            currenttier_Advices.append(Advice(
                label=f"{AdviceType.INFO.value} - Total Meal Levels ({max_remainingMeals:,} levels to go!)",
                picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                progression=cooking['PlayerTotalMealLevels'],
                goal=max_meal_count * max_meal_plate_level,
            ))

    currenttier_ag = AdviceGroup(
        tier='',
        pre_string='Meal priorities for your current tier',
        advices=currenttier_Advices,
        informational=True
    )
    currenttier_ag.remove_empty_subgroups()
    return currenttier_ag


def getPlateLevelsAdviceGroup(cooking):
    platelevels_Advices = []
    # If any sources of max plate levels are missing
    if cooking['PlayerMissingPlateUpgrades']:
        for missingUpgrade in cooking['PlayerMissingPlateUpgrades']:
            if isinstance(missingUpgrade, Advice):
                platelevels_Advices.append(missingUpgrade)
            else:
                platelevels_Advices.append(Advice(
                    label=missingUpgrade[0],
                    picture_class=missingUpgrade[1],
                    progression=missingUpgrade[2],
                    goal=missingUpgrade[3]
                ))

    platelevels_ag = AdviceGroup(
        tier='',
        pre_string='Remaining sources of max plate levels',
        advices=platelevels_Advices,
        informational=True
    )
    platelevels_ag.remove_empty_subgroups()
    return platelevels_ag


def getCookingAdviceSection() -> AdviceSection:
    highest_cooking_skill_level = max(session_data.account.all_skills['Cooking'])
    if highest_cooking_skill_level < 1:
        cooking_AdviceSection = AdviceSection(
            name='Cooking',
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking the Cooking skill in World 4!',
            picture='Cooking_Table.gif',
            unreached=True
        )
        return cooking_AdviceSection

    vmans = session_data.account.vmans
    challenge_account = session_data.account.no_beginners
    atom_fluoride_level = session_data.account.atom_collider['Atoms']['Fluoride - Void Plate Chef']['Level']
    dchef_level = session_data.account.alchemy_bubbles['Diamond Chef']['Level']
    cooking = session_data.account.cooking

    #Generate AdviceGroup
    cooking_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getCookingProgressionTiersAdviceGroups(
        highest_cooking_skill_level, cooking, dchef_level, vmans, challenge_account, atom_fluoride_level)
    cooking_AdviceGroupDict['CurrentTier'] = getCurrentTierStrategyAdviceGroup(
        cooking, dchef_level, atom_fluoride_level, overall_SectionTier, max_tier, vmans)
    cooking_AdviceGroupDict['PlateLevels'] = getPlateLevelsAdviceGroup(cooking)
    cooking_AdviceGroupDict['AllMeals'] = getCookingMealsAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    cooking_AdviceSection = AdviceSection(
        name='Cooking',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Cooking tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Cooking_Table.gif',
        groups=cooking_AdviceGroupDict.values()
    )
    return cooking_AdviceSection
