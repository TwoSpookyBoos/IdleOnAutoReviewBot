from models.models import Advice, AdviceGroup, AdviceSection
from utils.logging import get_logger
from flask import g as session_data
from consts import maxMeals, maxMealLevel, cookingCloseEnough
from utils.text_formatting import pl

logger = get_logger(__name__)


def setCookingProgressionTier():
    cooking_AdviceDict = {
        "NextTier": [],
        "CurrentTier": [],
        "PlateLevels": [],
    }
    cooking_AdviceGroupDict = {}
    cooking_AdviceSection = AdviceSection(
        name="Cooking",
        tier="0",
        pinchy_rating=0,
        header="Best Cooking tier met: Not Yet Evaluated",
        picture="Cooking_Table.gif"
    )
    highestCookingSkillLevel = max(session_data.account.all_skills["Cooking"])
    if highestCookingSkillLevel < 1:
        cooking_AdviceSection.header = "Come back after unlocking the Cooking skill in World 4!"
        return cooking_AdviceSection

    tier_Cooking = 0
    #TODO: Really ought to be structured into proper tiers.. What were you smoking when you made this?
    infoTiers = 1
    max_tier = 6
    vmans = session_data.account.vmans
    atomFluoride = session_data.account.atom_collider['Atoms']['Fluoride - Void Plate Chef']['Level'] >= 1
    dchefLevel = session_data.account.alchemy_bubbles['Diamond Chef']['Level']

    #Assess Tiers
    if highestCookingSkillLevel >= 1:
        tier_Cooking = 1
    if tier_Cooking == 1 and dchefLevel >= 15:
        tier_Cooking = 2
    if tier_Cooking == 2 and len(vmans) > 0:
        tier_Cooking = 3
    if tier_Cooking == 3 and atomFluoride and session_data.account.cooking['PlayerTotalMealLevels'] >= 500:
        tier_Cooking = 4
    if tier_Cooking == 4 and session_data.account.cooking['MealsUnlocked'] >= maxMeals and session_data.account.cooking['MealsUnder30'] <= 0:
        tier_Cooking = 5
    if tier_Cooking == 5 and session_data.account.cooking['PlayerMaxPlateLvl'] >= maxMealLevel:
        tier_Cooking = 6
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        tier_Cooking = 6
    if session_data.account.cooking['MaxRemainingMeals'] == 0:
        tier_Cooking = 7

    #Generate NextTier Advice
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
                picture_class="turkey-a-la-thank",
                progression=session_data.account.cooking['PlayerTotalMealLevels'],
                goal=500
            ))
    # 4) if Atom Collider Fluoride upgrade owned and total plates over 500:
    elif tier_Cooking == 4:
        if session_data.account.cooking['MealsUnlocked'] < maxMeals:
            cooking_AdviceDict["NextTier"].append(Advice(
                label=f"Unlock the remaining {maxMeals - session_data.account.cooking['MealsUnlocked']} "
                      f"{pl(maxMeals-session_data.account.cooking['MealsUnlocked'], 'meal', 'meals')}",
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
            picture_class="turkey-a-la-thank",
            progression=session_data.account.cooking['PlayerMaxPlateLvl'],
            goal=maxMealLevel
        ))
    # 6) All basics + max plate levels
    elif tier_Cooking == 6:
        cooking_AdviceDict["NextTier"].append(Advice(
            label=f"Finish all {maxMeals} meals to level {maxMealLevel}",
            picture_class="turkey-a-la-thank",
            progression=session_data.account.cooking['PlayerTotalMealLevels'],
            goal=maxMeals * maxMealLevel,
        ))

    #Generate CurrentTier Advice
    if session_data.account.cooking['MealsUnlocked'] < maxMeals:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Unlock All Meals",
            picture_class="taste-test",
            progression=session_data.account.cooking['MealsUnlocked'],
            goal=maxMeals,
        ))
    if session_data.account.cooking['MealsUnder11'] > 0 and tier_Cooking >= 2:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All unlocked plates to 11 for Diamond Chef",
            picture_class="diamond-chef",
            progression=session_data.account.cooking['MealsUnlocked']-session_data.account.cooking['MealsUnder11'],
            goal=session_data.account.cooking['MealsUnlocked'],
        ))
    if session_data.account.cooking['MealsUnder30'] > 0 and tier_Cooking >= 3:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All unlocked plates to 30 for Fluoride",
            picture_class="fluoride",
            progression=session_data.account.cooking['MealsUnlocked']-session_data.account.cooking['MealsUnder30'],
            goal=session_data.account.cooking['MealsUnlocked'],
        ))
    if tier_Cooking <= 3:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All +% Meal Cooking Speed meals (Egg, Corndog, Cabbage, etc.)",
            picture_class="egg",
            progression="",
            goal="",
        ))

    if tier_Cooking < 4:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any fast meal to level (5% of your Daily Ladles or less)",
            picture_class="blood-marrow",
            progression="",
            goal="",
        ))
    # Elif they have Voidwalker and meals still to level, replace the generic "any faster meal" with the more specific Vman Blood Marrow note
    elif 4 <= tier_Cooking < max_tier:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any! Voidwalker's Blood Marrow buff scales with EVERY meal level!",
            picture_class="blood-marrow",
        ))
        anyVWMaxBooked = False
        bestBMBook = 0
        anyVWMaxLeveled = False
        bestBMPresetLevel = 0
        #59: {"Name": "Blood Marrow", "Tab": "Voidwalker"},
        #If Blood Marrow is not max booked, recommend booking it
        #If Blood Marrow is not leveled on either preset, recommend leveling it
        for vman in vmans:
            #Book level
            if vman.max_talents.get("59", 0) >= session_data.account.library['MaxBookLevel']:
                anyVWMaxBooked = True
            if vman.max_talents.get("59", 0) > bestBMBook:
                bestBMBook = vman.max_talents.get("59", 0)

            #Preset level
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

    #If not all meals are maxed
    if session_data.account.cooking['PlayerTotalMealLevels'] < session_data.account.cooking['MaxTotalMealLevels']:
        current_remainingMeals = session_data.account.cooking['CurrentRemainingMeals']
        current_maxMealLevel = session_data.account.cooking['PlayerMaxPlateLvl']
        max_remainingMeals = session_data.account.cooking['MaxRemainingMeals']

        if tier_Cooking < max_tier:
            if current_remainingMeals != max_remainingMeals:
                cooking_AdviceDict["CurrentTier"].append(Advice(
                    label=f"Info- Current possible: {session_data.account.cooking['MealsUnlocked']}/{maxMeals} meals, "
                          f"{current_maxMealLevel}/{maxMealLevel} plate levels ({current_remainingMeals} to go!)",
                    picture_class="turkey-a-la-thank",
                    progression=session_data.account.cooking['PlayerTotalMealLevels'],
                    goal=session_data.account.cooking['MealsUnlocked'] * current_maxMealLevel,
                ))

            cooking_AdviceDict["CurrentTier"].append(Advice(
                label=f"Info- Total Meal Levels ({max_remainingMeals} to go!)",
                picture_class="turkey-a-la-thank",
                progression=session_data.account.cooking['PlayerTotalMealLevels'],
                goal=maxMeals * maxMealLevel,
            ))

    #If any sources of max plate levels are missing
    if session_data.account.cooking['PlayerMissingPlateUpgrades']:
        for missingUpgrade in session_data.account.cooking['PlayerMissingPlateUpgrades']:
            cooking_AdviceDict["PlateLevels"].append(Advice(
               label=missingUpgrade[0],
               picture_class=missingUpgrade[1],
           ))

    # Generate Advice Groups
    if tier_Cooking < max_tier:
        next_ps = "To unlock the next Tier of Meal Priorities"
    else:
        next_ps = f"Informational- Finish Cooking"
    cooking_AdviceGroupDict["NextTier"] = AdviceGroup(
        tier=f"{tier_Cooking if tier_Cooking < max_tier else ''}",
        pre_string=next_ps,
        advices=cooking_AdviceDict["NextTier"],
        post_string="",
    )

    cooking_AdviceGroupDict["CurrentTier"] = AdviceGroup(
        tier="",
        pre_string=f"Meal priorities for your current tier",
        advices=cooking_AdviceDict["CurrentTier"],
        post_string="",
    )

    cooking_AdviceGroupDict["PlateLevels"] = AdviceGroup(
        tier="",
        pre_string=f"Each remaining upgrade gives +10 max plate levels",
        advices=cooking_AdviceDict["PlateLevels"],
        post_string="",
    )

    # Generate Advice Section
    overall_CookingTier = min(max_tier + infoTiers, tier_Cooking)
    tier_section = f"{overall_CookingTier}/{max_tier}"
    cooking_AdviceSection.tier = tier_section
    cooking_AdviceSection.pinchy_rating = overall_CookingTier
    cooking_AdviceSection.groups = cooking_AdviceGroupDict.values()
    if overall_CookingTier >= max_tier:
        cooking_AdviceSection.header = f"Best Cooking tier met: {tier_section}<br>You best ❤️"
        cooking_AdviceSection.complete = True
    else:
        cooking_AdviceSection.header = f"Best Cooking tier met: {tier_section}"

    return cooking_AdviceSection
