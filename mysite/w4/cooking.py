import json
from models.models import Advice, AdviceGroup, AdviceSection
from utils.logging import get_logger
from flask import g as session_data
from consts import maxCookingTables, maxMeals, maxMealLevel
from utils.text_formatting import pl

logger = get_logger(__name__)

def parseJSON():
    emptyTable = [0]*11  #Some tables only have 10 fields, others have 11. Scary.
    emptyCooking = [emptyTable for table in range(maxCookingTables)]
    rawCooking = session_data.account.raw_data.get("Cooking", emptyCooking)
    if isinstance(rawCooking, str):
        rawCooking = json.loads(rawCooking)
    for sublistIndex, value in enumerate(rawCooking):
        if isinstance(rawCooking[sublistIndex], list):
            while len(rawCooking[sublistIndex]) < 11:
                rawCooking[sublistIndex].append(0)

    emptyMeal = [0]*maxMeals
    # Meals contains 4 lists of lists. The first 3 are as long as the number of plates. The 4th is general shorter.
    emptyMeals = [emptyMeal for meal in range(4)]
    rawMeals = session_data.account.raw_data.get("Meals", emptyMeals)
    if isinstance(rawMeals, str):
        rawMeals = json.loads(rawMeals)
    for sublistIndex, value in enumerate(rawMeals):
        if isinstance(rawMeals[sublistIndex], list):
            while len(rawMeals[sublistIndex]) < maxMeals:
                rawMeals[sublistIndex].append(0)

    #Count the number of unlocked meals, unlocked meals under 11, and unlocked meals under 30
    mealsUnlocked = 0
    mealsUnder11 = 0
    mealsUnder30 = 0
    for mealLevel in rawMeals[0]:
        if mealLevel > 0:
            mealsUnlocked += 1
            if mealLevel < 11:
                mealsUnder11 += 1
            if mealLevel < 30:
                mealsUnder30 += 1

    return [rawCooking, rawMeals, mealsUnlocked, mealsUnder11, mealsUnder30]

def setCookingProgressionTier():
    cooking_AdviceDict = {
        "NextTier": [],
        "CurrentTier": [],
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
    max_tier = 5
    voidwalkers = [toon for toon in session_data.account.all_characters if toon.elite_class == "Voidwalker"]

    try:
        atomFlouride = session_data.account.raw_data.get("Atoms", [0,0,0,0,0])[5] >= 1
    except:
        logger.exception(f"Unable to retrieve Atom Collider Flouride level. Defaulting to 0.")
        atomFlouride = False

    try:
        dchefLevel = session_data.account.raw_data.get("CauldronInfo")[3]["17"]
    except:
        logger.exception(f"Unable to retrieve Diamond Chef bubble level. Defaulting to 0.")
        dchefLevel = 0

    playerCookingList, playerMealsList, mealsUnlocked, mealsUnder11, mealsUnder30 = parseJSON()
    playerTotalMealLevels = sum(playerMealsList[0])

    #Assess Tiers and Generate NextTier Advice
    # 5) All the basics complete
    if (mealsUnlocked == maxMeals and mealsUnder11 == 0 and mealsUnder30 == 0
            and len(voidwalkers) > 0 and playerTotalMealLevels >= 500
            and atomFlouride
            and dchefLevel >= 15):
        tier_Cooking = 5
    # 4) if Vman and total plates over 500:
    elif (len(voidwalkers) > 0 and playerTotalMealLevels >= 500
          and atomFlouride
          and dchefLevel >= 15):
        tier_Cooking = 4
    # 3) if Atom Collider Flouride upgrade owned:
    elif (atomFlouride
          and dchefLevel >= 15):
        tier_Cooking = 3
        if len(voidwalkers) == 0:
            cooking_AdviceDict["NextTier"].append(Advice(
                label="Unlock a Voidwalker",
                picture_class="voidwalker-icon"
            ))
        if playerTotalMealLevels < 500:
            cooking_AdviceDict["NextTier"].append(Advice(
                label="Reach 500+ total meal levels",
                picture_class="turkey-a-la-thank",
                progression=playerTotalMealLevels,
                goal=500
            ))
    # 2) if Diamond Chef owned and level 15+, Speed meal or Fastest to 11.
    elif dchefLevel >= 15:
        tier_Cooking = 2
        cooking_AdviceDict["NextTier"].append(Advice(
            label="Unlock Fluoride - Void Plate Chef in the Atom Collider",
            picture_class="flouride"
        ))
    # 1) if cooking is unlocked at least
    else:
        tier_Cooking = 1
        cooking_AdviceDict["NextTier"].append(Advice(
            label="Unlock and level Diamond Chef bubble",
            picture_class="diamond-chef",
            progression=dchefLevel,
            goal=15
        ))

    #Generate CurrentTier Advice
    if mealsUnlocked < maxMeals:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Unlock All Meals",
            picture_class="taste-test",
            progression=mealsUnlocked,
            goal=maxMeals,
        ))
    if mealsUnder11 > 0 and tier_Cooking >= 2:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All unlocked plates to 11 for Diamond Chef",
            picture_class="diamond-chef",
            progression=mealsUnlocked-mealsUnder11,
            goal=mealsUnlocked,
        ))
    if mealsUnder30 > 0 and tier_Cooking >= 3:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="All unlocked plates to 30 for Flouride",
            picture_class="flouride",
            progression=mealsUnlocked-mealsUnder30,
            goal=mealsUnlocked,
        ))
    if tier_Cooking <= 3:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="+% Meal Cooking Speed",
            picture_class="egg",
            progression="",
            goal="",
        ))
    if tier_Cooking >= 4:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any! Voidwalker's Blood Marrow buff scales with EVERY meal level!",
            picture_class="blood-marrow",
        ))
    else:  #tier_Cooking < max_tier:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any fast meal to level (5% of your Daily Ladles or less)",
            picture_class="blood-marrow",
            progression="",
            goal="",
        ))
    if playerTotalMealLevels < maxMeals * maxMealLevel:
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label=f"Info- Total Meal Levels ({(maxMeals * maxMealLevel)-playerTotalMealLevels} to go!)",
            picture_class="turkey-a-la-thank",
            progression=playerTotalMealLevels,
            goal=maxMeals * maxMealLevel,
        ))

    # Generate Advice Groups
    cooking_AdviceGroupDict["NextTier"] = AdviceGroup(
        tier=str(tier_Cooking),
        pre_string="To unlock the next Tier of Meal Priorities",
        advices=cooking_AdviceDict["NextTier"],
        post_string="",
    )

    cooking_AdviceGroupDict["CurrentTier"] = AdviceGroup(
        tier="",
        pre_string=f"Meal priorities for your current tier",
        advices=cooking_AdviceDict["CurrentTier"],
        post_string="",
    )

    # Generate Advice Section
    overall_CookingTier = min(max_tier, tier_Cooking)
    tier_section = f"{overall_CookingTier}/{max_tier}"
    cooking_AdviceSection.tier = tier_section
    cooking_AdviceSection.pinchy_rating = overall_CookingTier
    cooking_AdviceSection.groups = cooking_AdviceGroupDict.values()
    if overall_CookingTier == max_tier:
        cooking_AdviceSection.header = f"Best Cooking tier met: {tier_section}<br>You best ❤️"
    else:
        cooking_AdviceSection.header = f"Best Cooking tier met: {tier_section}"

    return cooking_AdviceSection
