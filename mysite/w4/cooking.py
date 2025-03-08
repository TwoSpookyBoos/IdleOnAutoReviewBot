from models.models import Advice, AdviceGroup, AdviceSection
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import maxMealCount, maxMealLevel, cookingCloseEnough, break_you_best
from utils.text_formatting import pl

logger = get_logger(__name__)

def getCookingProgressionTiersAdviceGroups(highestCookingSkillLevel):
    cooking_AdviceDict = {
        "NextTier": [],
        "CurrentTier": [],
        "PlateLevels": [],
    }
    cooking_AdviceGroupDict = {}
    tier_Cooking = 0
    # TODO: Really ought to be structured into proper tiers.. What were you smoking when you made this?
    infoTiers = 1
    max_tier = 6
    vmans = session_data.account.vmans
    atomFluoride = session_data.account.atom_collider['Atoms']['Fluoride - Void Plate Chef']['Level'] >= 1
    dchefLevel = session_data.account.alchemy_bubbles['Diamond Chef']['Level']

    # Assess Tiers
    if highestCookingSkillLevel >= 1:
        tier_Cooking = 1
    if tier_Cooking == 1 and dchefLevel >= 15:
        tier_Cooking = 2
    if tier_Cooking == 2 and len(vmans) > 0:
        tier_Cooking = 3
    if tier_Cooking == 3 and atomFluoride and session_data.account.cooking['PlayerTotalMealLevels'] >= 500:
        tier_Cooking = 4
    if tier_Cooking == 4 and session_data.account.cooking['MealsUnlocked'] >= maxMealCount and session_data.account.cooking['MealsUnder30'] <= 0:
        tier_Cooking = 5
    if tier_Cooking == 5 and session_data.account.cooking['PlayerMaxPlateLvl'] >= maxMealLevel:
        tier_Cooking = 6
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        tier_Cooking = 6
    if session_data.account.cooking['MaxRemainingMeals'] == 0:
        tier_Cooking = 7

    # Generate NextTier Advice
    # 1) if cooking is unlocked at least
    if tier_Cooking == 1:
        cooking_AdviceDict["NextTier"].append(Advice(
            label="Unlock and level Diamond Chef bubble",
            picture_class="diamond-chef",
            progression=dchefLevel,
            goal=15
        ))
    # 2) if Diamond Chef owned and level 15+, Speed meal or Fastest to 11.
    elif tier_Cooking == 2:
        if len(vmans) == 0:
            cooking_AdviceDict["NextTier"].append(Advice(
                label="Unlock a Voidwalker",
                picture_class="voidwalker-icon"
            ))
    # 3) if Vman:
    elif tier_Cooking == 3:
        cooking_AdviceDict["NextTier"].append(Advice(
            label="Unlock Fluoride - Void Plate Chef in the Atom Collider",
            picture_class="fluoride"
        ))
        if session_data.account.cooking['PlayerTotalMealLevels'] < 500:
            cooking_AdviceDict["NextTier"].append(Advice(
                label="Reach 500+ total meal levels",
                picture_class=session_data.account.meals['Turkey a la Thank']['Image'],
                progression=session_data.account.cooking['PlayerTotalMealLevels'],
                goal=500
            ))
    # 4) if Atom Collider Fluoride upgrade owned and total plates over 500:
    elif tier_Cooking == 4:
        if session_data.account.cooking['MealsUnlocked'] < maxMealCount:
            cooking_AdviceDict["NextTier"].append(Advice(
                label=f"Unlock the remaining {maxMealCount - session_data.account.cooking['MealsUnlocked']} "
                      f"{pl(maxMealCount - session_data.account.cooking['MealsUnlocked'], 'meal', 'meals')}",
                picture_class="dharma-mesa-spice"
            ))
        if session_data.account.cooking['MealsUnder11'] > 0:
            cooking_AdviceDict["NextTier"].append(Advice(
                label=f"Level up the remaining {session_data.account.cooking['MealsUnder11']} unlocked "
                      f"{pl(session_data.account.cooking['MealsUnder11'], 'meal', 'meals')} to 11+ for Diamond Chef",
                picture_class="diamond-chef",
                progression=session_data.account.cooking['MealsUnlocked'] - session_data.account.cooking['MealsUnder11'],
                goal=session_data.account.cooking['MealsUnlocked']
            ))
        if session_data.account.cooking['MealsUnder30'] > 0:
            cooking_AdviceDict["NextTier"].append(Advice(
                label=f"Level up the remaining {session_data.account.cooking['MealsUnder30']} unlocked "
                      f"{pl(session_data.account.cooking['MealsUnder30'], 'meal', 'meals')} to 30+ for Fluoride",
                picture_class="fluoride",
                progression=session_data.account.cooking['MealsUnlocked'] - session_data.account.cooking['MealsUnder30'],
                goal=session_data.account.cooking['MealsUnlocked']
            ))
    # 5) All meals unlocked, all meals 30+
    elif tier_Cooking == 5:
        cooking_AdviceDict["NextTier"].append(Advice(
            label=f"Unlock max level {maxMealLevel} plates",
            picture_class=session_data.account.meals['Turkey a la Thank']['Image'],
            progression=session_data.account.cooking['PlayerMaxPlateLvl'],
            goal=maxMealLevel
        ))
    # 6) All basics + max plate levels
    elif tier_Cooking == 6:
        cooking_AdviceDict["NextTier"].append(Advice(
            label=f"Finish all {maxMealCount} meals to level {maxMealLevel}"
                  f"<br>{session_data.account.cooking['CurrentRemainingMeals']} remaining levels = "
                  f"{session_data.account.cooking['NMLBDays']} NMLB triggers to go!",
            picture_class=session_data.account.meals['Turkey a la Thank']['Image'],
            progression=session_data.account.cooking['PlayerTotalMealLevels'],
            goal=maxMealCount * maxMealLevel,
        ))

    # Generate CurrentTier Advice
    if session_data.account.cooking['MealsUnlocked'] < maxMealCount:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Unlock All Meals",
            picture_class="taste-test",
            progression=session_data.account.cooking['MealsUnlocked'],
            goal=maxMealCount,
        ))
    if session_data.account.cooking['MealsUnder11'] > 0 and tier_Cooking >= 2:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All unlocked plates to 11 for Diamond Chef",
            picture_class="diamond-chef",
            progression=session_data.account.cooking['MealsUnlocked'] - session_data.account.cooking['MealsUnder11'],
            goal=session_data.account.cooking['MealsUnlocked'],
        ))
    if session_data.account.cooking['MealsUnder30'] > 0 and tier_Cooking >= 3:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All unlocked plates to 30 for Fluoride",
            picture_class="fluoride",
            progression=session_data.account.cooking['MealsUnlocked'] - session_data.account.cooking['MealsUnder30'],
            goal=session_data.account.cooking['MealsUnlocked'],
        ))
    if tier_Cooking <= 3:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All +% Meal Cooking Speed meals (Egg, Corndog, Cabbage, etc.)",
            picture_class=session_data.account.meals['Egg']['Image'],
            completed=False
        ))

    if tier_Cooking < 4:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any fast meal to level (5% of your Daily Ladles or less)",
            picture_class="blood-marrow",
            completed=False
        ))
    # Elif they have Voidwalker and meals still to level, replace the generic "any faster meal" with the more specific Vman Blood Marrow note
    elif 4 <= tier_Cooking < max_tier:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any! Voidwalker's Blood Marrow buff scales with EVERY meal level!",
            picture_class="blood-marrow",
            completed=False
        ))
        anyVWMaxBooked = False
        bestBMBook = 0
        anyVWMaxLeveled = False
        bestBMPresetLevel = 0
        # 59: {"Name": "Blood Marrow", "Tab": "Voidwalker"},
        # If Blood Marrow is not max booked, recommend booking it
        # If Blood Marrow is not leveled on either preset, recommend leveling it
        for vman in vmans:
            # Book level
            if vman.max_talents.get("59", 0) >= session_data.account.library['MaxBookLevel']:
                anyVWMaxBooked = True
            if vman.max_talents.get("59", 0) > bestBMBook:
                bestBMBook = vman.max_talents.get("59", 0)

            # Preset level
            if (
                    vman.current_preset_talents.get("59", 0) >= session_data.account.library['MaxBookLevel']
                    or vman.secondary_preset_talents.get("59", 0) >= session_data.account.library['MaxBookLevel']
            ):
                anyVWMaxLeveled = True
            if vman.current_preset_talents.get("59", 0) >= bestBMPresetLevel:
                bestBMPresetLevel = vman.current_preset_talents.get("59", 0)
            if vman.secondary_preset_talents.get("59", 0) >= bestBMPresetLevel:
                bestBMPresetLevel = vman.secondary_preset_talents.get("59", 0)

        if session_data.account.cooking['MaxRemainingMeals'] > cookingCloseEnough:
            if not anyVWMaxBooked:
                session_data.account.alerts_AdviceDict['World 4'].append(Advice(
                    label="No Voidwalkers with {{ Blood Marrow|#cooking }} talent max booked!",
                    picture_class="beginner-talent-book",
                    progression=bestBMBook,
                    goal=session_data.account.library['MaxBookLevel']
                ))
            if not anyVWMaxLeveled:
                session_data.account.alerts_AdviceDict['World 4'].append(Advice(
                    label="No Voidwalkers with {{ Blood Marrow|#cooking }} talent maxed in any presets!",
                    picture_class="talent-preset-1",
                    progression=bestBMPresetLevel,
                    goal=session_data.account.library['MaxBookLevel']
                ))

    # If not all meals are maxed
    if session_data.account.cooking['PlayerTotalMealLevels'] < session_data.account.cooking['MaxTotalMealLevels']:
        current_remainingMeals = session_data.account.cooking['CurrentRemainingMeals']
        current_maxMealLevel = session_data.account.cooking['PlayerMaxPlateLvl']
        max_remainingMeals = session_data.account.cooking['MaxRemainingMeals']

        if tier_Cooking < max_tier:
            if current_remainingMeals != max_remainingMeals:
                cooking_AdviceDict["CurrentTier"].append(Advice(
                    label=f"Info- Current possible: {session_data.account.cooking['MealsUnlocked']}/{maxMealCount} meals, "
                          f"{current_maxMealLevel}/{maxMealLevel} plate levels"
                          f"<br>{current_remainingMeals} meal levels = {session_data.account.cooking['NMLBDays']} NMLB triggers to go!",
                    picture_class=session_data.account.meals['Turkey a la Thank']['Image'],
                    progression=session_data.account.cooking['PlayerTotalMealLevels'],
                    goal=session_data.account.cooking['MealsUnlocked'] * current_maxMealLevel,
                ))

            cooking_AdviceDict["CurrentTier"].append(Advice(
                label=f"Info- Total Meal Levels ({max_remainingMeals} to go!)",
                picture_class=session_data.account.meals['Turkey a la Thank']['Image'],
                progression=session_data.account.cooking['PlayerTotalMealLevels'],
                goal=maxMealCount * maxMealLevel,
            ))

    # If any sources of max plate levels are missing
    if session_data.account.cooking['PlayerMissingPlateUpgrades']:
        for missingUpgrade in session_data.account.cooking['PlayerMissingPlateUpgrades']:
            cooking_AdviceDict["PlateLevels"].append(Advice(
                label=missingUpgrade[0],
                picture_class=missingUpgrade[1],
                progression=missingUpgrade[2],
                goal=missingUpgrade[3]
            ))

    for advice in cooking_AdviceDict["NextTier"]:
        mark_advice_completed(advice)

    # Generate Advice Groups
    cooking_AdviceGroupDict["NextTier"] = AdviceGroup(
        tier=f"{tier_Cooking if tier_Cooking < max_tier else ''}",
        pre_string="To unlock the next Tier of Meal Priorities" if tier_Cooking < max_tier else "Informational- Finish Cooking",
        advices=cooking_AdviceDict["NextTier"],
        post_string="",
        informational=tier_Cooking >= max_tier
    )

    cooking_AdviceGroupDict["CurrentTier"] = AdviceGroup(
        tier="",
        pre_string=f"Meal priorities for your current tier",
        advices=cooking_AdviceDict["CurrentTier"],
        post_string="",
        informational=True
    )

    cooking_AdviceGroupDict["PlateLevels"] = AdviceGroup(
        tier="",
        pre_string=f"Remaining sources of max plate levels",
        advices=cooking_AdviceDict["PlateLevels"],
        post_string="",
        informational=True
    )
    overall_SectionTier = min(max_tier + infoTiers, tier_Cooking)
    return cooking_AdviceGroupDict, overall_SectionTier, max_tier, max_tier + infoTiers


def getCookingMealsAdviceGroup() -> AdviceGroup:
    meals_advice = [
        Advice(
            label=f"{meal_name}: {meal_values['Description']}"
                  f"<br>Tier {meal_values['RibbonTier']} Ribbon = {meal_values['RibbonMulti']:.3f}x multi",
            picture_class=meal_values['Image'],
            progression=meal_values['Level'],
            goal=maxMealLevel,
            resource=f"meal-ribbon-{meal_values['RibbonTier']}",
            informational=True
        ) for meal_name, meal_values in session_data.account.meals.items()
    ]
    for advice in meals_advice:
        mark_advice_completed(advice)

    meals_ag = AdviceGroup(
        tier='',
        pre_string="Info- All Meal levels and ribbons",
        advices=meals_advice,
        informational=True
    )
    return meals_ag


def getCookingAdviceSection() -> AdviceSection:
    highestCookingSkillLevel = max(session_data.account.all_skills["Cooking"])
    if highestCookingSkillLevel < 1:
        cooking_AdviceSection = AdviceSection(
            name="Cooking",
            tier="0",
            pinchy_rating=0,
            header="Come back after unlocking the Cooking skill in World 4!",
            picture="Cooking_Table.gif",
            unreached=True
        )
        return cooking_AdviceSection

    #Generate AdviceGroup
    cooking_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getCookingProgressionTiersAdviceGroups(highestCookingSkillLevel)
    cooking_AdviceGroupDict['AllMeals'] = getCookingMealsAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    cooking_AdviceSection = AdviceSection(
        name="Cooking",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Cooking tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Cooking_Table.gif",
        groups=cooking_AdviceGroupDict.values()
    )
    return cooking_AdviceSection
