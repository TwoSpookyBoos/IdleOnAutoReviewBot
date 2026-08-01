from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, AdviceType
from consts.consts_w4 import max_meal_count, max_meal_plate_level, cooking_close_enough, meal_counts_by_world
from utils.text_formatting import pl

logger = get_logger(__name__)

def getCookingProgressionTiersAdviceGroups(highestCookingSkillLevel):
    cooking_Advices = {
        'NextTier': [],
        'CurrentTier': [],
        'PlateLevels': [],
    }
    cooking_AdviceGroupDict = {}
    tier_Cooking = 0
    # TODO: Really ought to be structured into proper tiers.. What were you smoking when you made this?
    optional_tiers = 1
    true_max = true_max_tiers['Cooking']
    max_tier = true_max - optional_tiers
    vmans = session_data.account.vmans
    atom_fluoride = session_data.account.atom_collider['Atoms']['Fluoride - Void Plate Chef']['Level'] >= 1
    dchef_level = session_data.account.alchemy_bubbles['Diamond Chef']['Level']
    cooking = session_data.account.cooking

    # Assess Tiers
    if highestCookingSkillLevel >= 1:
        tier_Cooking = 1
    if tier_Cooking == 1 and dchef_level >= 15:
        tier_Cooking = 2
    if tier_Cooking == 2 and len(vmans) > 0:
        tier_Cooking = 3
    if tier_Cooking == 3 and atom_fluoride and cooking['PlayerTotalMealLevels'] >= 500:
        tier_Cooking = 4
    if tier_Cooking == 4 and cooking['MealsUnlockedByWorld'][4] >= meal_counts_by_world[4]:
        tier_Cooking = 5
    if tier_Cooking == 5 and cooking['MealsUnlockedByWorld'][5] >= meal_counts_by_world[5]:
        tier_Cooking = 6
    if tier_Cooking == 6 and cooking['MealsUnlockedByWorld'][6] >= meal_counts_by_world[6]:
        tier_Cooking = 7
    if tier_Cooking == 7 and cooking['MealsUnlockedByWorld'][7] >= meal_counts_by_world[7]:
        tier_Cooking = 8
    if tier_Cooking == 8 and cooking['MealsUnlockedByWorld'][8] >= meal_counts_by_world[8]:
        tier_Cooking = 9
    if tier_Cooking == 9 and cooking['MealsUnder30'] <= 0:
        tier_Cooking = 10
    if tier_Cooking == 10 and cooking['PlayerMaxPlateLvl'] >= max_meal_plate_level:
        tier_Cooking = 11
    if cooking['MaxRemainingMeals'] < cooking_close_enough:
        tier_Cooking = 12
    if cooking['MaxRemainingMeals'] == 0:
        tier_Cooking = 13

    # Generate NextTier Advice
    # 0) if cooking isn't unlocked yet
    if tier_Cooking == 0:
        cooking_Advices['NextTier'].append(Advice(
            label="Unlock the Cooking skill in World 4 town",
            picture_class='cooking',
            progression=highestCookingSkillLevel,
            goal=1
        ))

    # 1) if cooking is unlocked at least
    elif tier_Cooking == 1:
        cooking_Advices['NextTier'].append(Advice(
            label="Unlock and level Diamond Chef bubble",
            picture_class="diamond-chef",
            progression=dchef_level,
            goal=15
        ))

    # 2) if Diamond Chef owned and level 15+, Speed meal or Fastest to 11.
    elif tier_Cooking == 2:
        if len(vmans) == 0:
            cooking_Advices['NextTier'].append(Advice(
                label="Unlock a Voidwalker",
                picture_class="voidwalker-icon"
            ))

    # 3) if Vman:
    elif tier_Cooking == 3:
        cooking_Advices['NextTier'].append(Advice(
            label="Unlock Fluoride - Void Plate Chef in the {{Atom Collider|#atom-collider}} from W3 Construction skill",
            picture_class='fluoride'
        ))
        if cooking['PlayerTotalMealLevels'] < 500:
            cooking_Advices['NextTier'].append(Advice(
                label="Reach 500+ total meal levels",
                picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                progression=cooking['PlayerTotalMealLevels'],
                goal=500
            ))

    # 4) if Atom Collider Fluoride upgrade owned and total plates over 500, but not all W4 meals unlocked:
    elif tier_Cooking == 4:
        if cooking['MealsUnlockedByWorld'][4] < meal_counts_by_world[4]:
            cooking_Advices['NextTier'].append(Advice(
                label=f"Unlock the remaining {meal_counts_by_world[4] - cooking['MealsUnlocked']} W4 meal"
                      f"{pl(meal_counts_by_world[4] - cooking['MealsUnlockedByWorld'][4])}",
                picture_class='nebulon-mantle-spice'
            ))

    # 5) if all W4 meals unlocked, but not all W5:
    elif tier_Cooking == 5:
        if cooking['MealsUnlockedByWorld'][5] < meal_counts_by_world[5]:
            cooking_Advices['NextTier'].append(Advice(
                label=f"Unlock the remaining {meal_counts_by_world[5] - cooking['MealsUnlocked']} W5 meal"
                      f"{pl(meal_counts_by_world[5] - cooking['MealsUnlockedByWorld'][5])}",
                picture_class='wurm-catacombs-spice'
            ))

    # 6) if all W5 meals unlocked, but not all W6:
    elif tier_Cooking == 6:
        if cooking['MealsUnlockedByWorld'][6] < meal_counts_by_world[6]:
            cooking_Advices['NextTier'].append(Advice(
                label=f"Unlock the remaining {meal_counts_by_world[6] - cooking['MealsUnlocked']} W6 meal"
                      f"{pl(meal_counts_by_world[6] - cooking['MealsUnlockedByWorld'][6])}",
                picture_class='dharma-mesa-spice'
            ))

    # 7) if all W6 meals unlocked, but not all W7:
    elif tier_Cooking == 7:
        if cooking['MealsUnlockedByWorld'][7] < meal_counts_by_world[7]:
            cooking_Advices['NextTier'].append(Advice(
                label=f"Unlock the remaining {meal_counts_by_world[7] - cooking['MealsUnlocked']} W7 meal"
                      f"{pl(meal_counts_by_world[7] - cooking['MealsUnlockedByWorld'][7])}",
                picture_class='dharma-mesa-spice'
            ))

    # 8) if all W7 meals unlocked, but not all W8:
    elif tier_Cooking == 8:
        if cooking['MealsUnlockedByWorld'][8] < meal_counts_by_world[8]:
            cooking_Advices['NextTier'].append(Advice(
                label=f"Unlock the remaining {meal_counts_by_world[8] - cooking['MealsUnlocked']} W8 meal"
                      f"{pl(meal_counts_by_world[8] - cooking['MealsUnlockedByWorld'][8])}",
                picture_class='dharma-mesa-spice'
            ))

    # 9) All W8 meals unlocked, but not all 11+ for Diamond Chef and 30+ for Flouride
    elif tier_Cooking == 9:
        if session_data.account.cooking['MealsUnder11'] > 0:
            cooking_Advices['NextTier'].append(Advice(
                label=f"Level up the remaining {session_data.account.cooking['MealsUnder11']} unlocked "
                      f"{pl(session_data.account.cooking['MealsUnder11'], 'meal', 'meals')} to 11+ for Diamond Chef",
                picture_class="diamond-chef",
                progression=session_data.account.cooking['MealsUnlocked'] - session_data.account.cooking['MealsUnder11'],
                goal=session_data.account.cooking['MealsUnlocked']
            ))
        if session_data.account.cooking['MealsUnder30'] > 0:
            cooking_Advices['NextTier'].append(Advice(
                label=f"Level up the remaining {session_data.account.cooking['MealsUnder30']} unlocked "
                      f"{pl(session_data.account.cooking['MealsUnder30'], 'meal', 'meals')} to 30+ for Fluoride",
                picture_class="fluoride",
                progression=session_data.account.cooking['MealsUnlocked'] - session_data.account.cooking['MealsUnder30'],
                goal=session_data.account.cooking['MealsUnlocked']
            ))

    # 10) All meals unlocked, all meals 30+, but max plate level is not unlocked yet
    elif tier_Cooking == 10:
        cooking_Advices['NextTier'].append(Advice(
            label=f"Unlock max level {max_meal_plate_level} plates",
            picture_class=session_data.account.meals['Turkey of Thank']['Image'],
            progression=cooking['PlayerMaxPlateLvl'],
            goal=max_meal_plate_level
        ))

    # 11) All basics + max plate levels
    #elif tier_Cooking == 11:
    else:
        cooking_Advices['NextTier'].append(Advice(
            label=f"Finish all {max_meal_count} meals to level {max_meal_plate_level}"
                  f"<br>{cooking['CurrentRemainingMeals']} remaining levels = "
                  f"{cooking['NMLBDays']} NMLB triggers to go!",
            picture_class=session_data.account.meals['Turkey of Thank']['Image'],
            progression=cooking['PlayerTotalMealLevels'],
            goal=max_meal_count * max_meal_plate_level,
        ))

    # Generate CurrentTier Advice
    if session_data.account.cooking['MealsUnlocked'] < max_meal_count:
        cooking_Advices["CurrentTier"].append(Advice(
            label="Work on unlocking all meals. Breakdowns by world below",
            picture_class='taste-test',
            progression=session_data.account.cooking['MealsUnlocked'],
            goal=max_meal_count,
        ))
    for world in range(0, 9):
        if session_data.account.highest_world_reached >= world and cooking['MealsUnlockedByWorld'][world] < meal_counts_by_world[world]:
            cooking_Advices["CurrentTier"].append(Advice(
                label=f"Unlock All W{world} Meals",
                picture_class='taste-test',
                progression=cooking['MealsUnlockedByWorld'][world],
                goal=meal_counts_by_world[world],
            ))

    if cooking['UnlockedMealsUnder11'] > 0 and tier_Cooking >= 2:
        cooking_Advices["CurrentTier"].append(Advice(
            label="All unlocked plates to 11 for Diamond Chef",
            picture_class="diamond-chef",
            progression=cooking['MealsUnlocked'] - cooking['UnlockedMealsUnder11'],
            goal=cooking['MealsUnlocked'],
        ))
    if cooking['UnlockedMealsUnder30'] > 0 and tier_Cooking >= 3:
        cooking_Advices["CurrentTier"].append(Advice(
            label="All unlocked plates to 30 for Fluoride",
            picture_class='fluoride',
            progression=cooking['MealsUnlocked'] - cooking['UnlockedMealsUnder30'],
            goal=cooking['MealsUnlocked'],
        ))
    if tier_Cooking <= 3:
        cooking_Advices["CurrentTier"].append(Advice(
            label="All +% Meal Cooking Speed meals (Egg, Corndog, Cabbage, etc.)",
            picture_class=session_data.account.meals['Egg']['Image'],
            completed=False
        ))

    if tier_Cooking < 4:
        cooking_Advices["CurrentTier"].append(Advice(
            label="Any fast meal to level (5% of your Daily Ladles or less)",
            picture_class='blood-marrow',
            completed=False
        ))
    # Elif they have Voidwalker and meals still to level, replace the generic "any faster meal" with the more specific Vman Blood Marrow note
    elif 4 <= tier_Cooking < max_tier:
        cooking_Advices["CurrentTier"].append(Advice(
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
                cooking_Advices["CurrentTier"].append(Advice(
                    label=f"{AdviceType.INFO.value} - Current possible: {cooking['MealsUnlocked']}/{max_meal_count} meals, "
                          f"{current_maxMealLevel}/{max_meal_plate_level} plate levels"
                          f"<br>{current_remainingMeals} meal levels = {cooking['NMLBDays']} NMLB triggers to go!",
                    picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                    progression=cooking['PlayerTotalMealLevels'],
                    goal=cooking['MealsUnlocked'] * current_maxMealLevel,
                ))

            cooking_Advices["CurrentTier"].append(Advice(
                label=f"{AdviceType.INFO.value} - Total Meal Levels ({max_remainingMeals:,} levels to go!)",
                picture_class=session_data.account.meals['Turkey of Thank']['Image'],
                progression=cooking['PlayerTotalMealLevels'],
                goal=max_meal_count * max_meal_plate_level,
            ))

    # If any sources of max plate levels are missing
    if cooking['PlayerMissingPlateUpgrades']:
        for missingUpgrade in cooking['PlayerMissingPlateUpgrades']:
            if isinstance(missingUpgrade, Advice):
                cooking_Advices['PlateLevels'].append(missingUpgrade)
            else:
                cooking_Advices['PlateLevels'].append(Advice(
                    label=missingUpgrade[0],
                    picture_class=missingUpgrade[1],
                    progression=missingUpgrade[2],
                    goal=missingUpgrade[3]
                ))

    for advice in cooking_Advices['NextTier']:
        advice.mark_advice_completed()

    # Generate Advice Groups
    cooking_AdviceGroupDict['NextTier'] = AdviceGroup(
        tier=tier_Cooking,
        pre_string='To unlock the next set of Meal Priorities' if tier_Cooking < max_tier else 'Max all Meals',
        advices=cooking_Advices['NextTier']
    )

    cooking_AdviceGroupDict['CurrentTier'] = AdviceGroup(
        tier='',
        pre_string='Meal priorities for your current tier',
        advices=cooking_Advices['CurrentTier'],
        informational=True
    )

    cooking_AdviceGroupDict['PlateLevels'] = AdviceGroup(
        tier='',
        pre_string='Remaining sources of max plate levels',
        advices=cooking_Advices["PlateLevels"],
        informational=True
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

    #Generate AdviceGroup
    cooking_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getCookingProgressionTiersAdviceGroups(highest_cooking_skill_level)
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
