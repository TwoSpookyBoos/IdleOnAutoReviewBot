import json
from models.models import Advice, AdviceGroup, AdviceSection
from utils.logging import get_logger
from flask import g as session_data
from consts import maxCookingTables, maxMeals
from utils.text_formatting import pl

logger = get_logger(__name__)

def parseJSON():
    emptyTable = [0]*11  #Some tables only have 10 fields, others have 11. Scary.
    emptyCooking = [emptyTable for table in range(maxCookingTables)]
    rawCooking = session_data.account.raw_data.get("Cooking", emptyCooking)
    if isinstance(rawCooking, str):
        rawCooking = json.loads(rawCooking)
    for sublistIndex, value in enumerate(rawCooking):
        while len(rawCooking[sublistIndex]) < 11:
            rawCooking[sublistIndex].append(0)

    emptyMeal = [0]*maxMeals
    # Meals contains 4 lists of lists. The first 3 are as long as the number of plates. The 4th is general shorter.
    emptyMeals = [emptyMeal for meal in range(4)]
    rawMeals = session_data.account.raw_data.get("Meals", emptyMeals)
    if isinstance(rawMeals, str):
        rawMeals = json.loads(rawMeals)
    for sublistIndex, value in enumerate(rawMeals):
        while len(rawMeals[sublistIndex]) < maxMeals:
            rawMeals[sublistIndex].append(0)

    return [rawCooking, rawMeals]

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
        cooking_AdviceSection.header = "Come back after unlocking Cooking!"
        return cooking_AdviceSection

    tier_Cooking = 0
    max_tier = 4

    playerCookingList, playerMealsList = parseJSON()
    playerTotalMealLevels = sum(playerMealsList[0])
    voidwalkers = [toon for toon in session_data.account.all_characters if toon.elite_class == "Voidwalker"]

    try:
        atomFlouride = session_data.account.raw_data.get("Atoms", [0,0,0,0,0])[5] >= 1
    except:
        logger.exception(f"Unable to retrieve Atom Collider Flouride level. Defaulting to 0.")
        atomFlouride = False

    try:
        dchefLevel = session_data.account.raw_data.get("CauldronInfo")[3][17]
    except:
        logger.exception(f"Unable to retrieve Diamond Chef bubble level. Defaulting to 0.")
        dchefLevel = 0

    #Assess Tiers and Generate Advice
    # 4) if Vman and total plates over 500: Fastest Any level
        # If any under 11, those first
        # Elif any under 30, those next
        # Else whatever plate is fastest to level, with slightly more preference to Speed meals. Maybe a 1.2x buffer or something?
    if len(voidwalkers) > 0 and playerTotalMealLevels >= 500:
        tier_Cooking = 4
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Use IE or IT's Cooking section with the sort set to 'Least Time to Cook Next'",
            picture_class="",
            progression="",
            goal="",
        ))
    # 3) if Atom Collider Flouride upgrade owned: Fastest to 30 or Speed Meal or Fastest to 11.
    elif atomFlouride:
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
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Fastest out of: Fastest to 11, Fastest to 30, any Speed meals",
            picture_class="",
            progression="",
            goal="",
        ))
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any ol' meal is good here to prep for the next tier",
            picture_class="",
            progression="",
            goal="",
        ))
        # 2) If Diamond Chef owned and level 5+, Speed meal or Fastest to 11.
    elif dchefLevel >= 5:
        tier_Cooking = 2
        cooking_AdviceDict["NextTier"].append(Advice(
            label="Unlock Fluoride - Void Plate Chef in the Atom Collider",
            picture_class=""
        ))
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Fastest out of: Fastest to 11, any Speed meals",
            picture_class="",
            progression="",
            goal="",
        ))
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Any ol' meal is okay here to start prepping for future tiers",
            picture_class="",
            progression="",
            goal="",
        ))
    # 1) Fastest Speed Meal
    else:
        tier_Cooking = 1
        cooking_AdviceDict["NextTier"].append(Advice(
            label="Unlock and level Diamond Chef bubble",
            picture_class="diamond-chef",
            progression=dchefLevel,
            goal=5
        ))
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label="Focus on Meal Speed meals with the least time remaining to level",
            picture_class="",
            progression="",
            goal="",
        ))

    # Generate Advice Groups
    cooking_AdviceGroupDict["NextTier"] = AdviceGroup(
        tier=str(tier_Cooking),
        pre_string="To unlock the next Tier of Meal Priorities",
        advices=cooking_AdviceDict["NextTier"],
        post_string="",
    )

    cooking_AdviceGroupDict["CurrentTier"] = AdviceGroup(
        tier=str(tier_Cooking),
        pre_string=f"Focus on the Fastest Meals {pl(cooking_AdviceDict['CurrentTier'], 'of this type', 'of these types')}",
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
