import json
from models.models import Advice, AdviceGroup, AdviceSection
from utils.data_formatting import safe_loads
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

    #Calculate the player's max plate level
    playerMaxPlateLvl = 30  #30 is the default starting point
    playerMissingPlateUpgrades = []
    #Sailing Artifact Increases
    rawSailing = safe_loads(session_data.account.raw_data.get("Sailing", [[],[],[],[]]))
    if len(rawSailing[3]) >= 17:
        causticolumn_level = rawSailing[3][17]
        playerMaxPlateLvl += 10 * int(causticolumn_level)
    else:
        causticolumn_level = 0
    if causticolumn_level < 1:
        playerMissingPlateUpgrades.append(("Normal Causticolumn Sailing Artifact", "causticolumn"))
    if causticolumn_level < 2:
        playerMissingPlateUpgrades.append(("Ancient Causticolumn Sailing Artifact", "causticolumn"))
    if causticolumn_level < 3:
        if session_data.account.eldritch_artifacts_unlocked:
            playerMissingPlateUpgrades.append(("Eldritch Causticolumn Sailing Artifact", "causticolumn"))
        else:
            playerMissingPlateUpgrades.append(("Eldritch Causticolumn Sailing Artifact. Eldritch Artifacts are unlocked by reaching Rift 31", "eldritch-artifact"))
    if causticolumn_level < 4:
        if "Sovereign Artifacts" in session_data.account.jade_emporium_purchases:
            playerMissingPlateUpgrades.append(("Sovereign Causticolumn Sailing Artifact", "causticolumn"))
        else:
            playerMissingPlateUpgrades.append(("Sovereign Causticolumn Sailing Artifact. Sovereign Artifacts are unlocked from the Jade Emporium", "sovereign-artifacts"))
    #Jade Emporium Increases
    if "Papa Blob's Quality Guarantee" not in session_data.account.jade_emporium_purchases:
        playerMissingPlateUpgrades.append(("Purchase \"Papa Blob's Quality Guarantee\" from the Jade Emporium", "papa-blobs-quality-guarantee"))
    else:
        playerMaxPlateLvl += 10
    if "Chef Geustloaf's Cutting Edge Philosophy" not in session_data.account.jade_emporium_purchases:
        playerMissingPlateUpgrades.append(("Purchase \"Chef Geustloaf's Cutting Edge Philosophy\" from the Jade Emporium", "chef-geustloafs-cutting-edge-philosophy"))
    else:
        playerMaxPlateLvl += 10

    return [rawCooking, rawMeals, mealsUnlocked, mealsUnder11, mealsUnder30, playerMaxPlateLvl, playerMissingPlateUpgrades]

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
    max_tier = 6
    voidwalkers = [toon for toon in session_data.account.all_characters if toon.elite_class == "Voidwalker"]

    try:
        atomFlouride = session_data.account.raw_data.get("Atoms", [0,0,0,0,0])[8] >= 1
    except:
        logger.exception(f"Unable to retrieve Atom Collider Flouride level. Defaulting to 0.")
        atomFlouride = False

    try:
        dchefLevel = session_data.account.raw_data.get("CauldronInfo")[3]["17"]
    except:
        logger.exception(f"Unable to retrieve Diamond Chef bubble level. Defaulting to 0.")
        dchefLevel = 0

    playerCookingList, playerMealsList, mealsUnlocked, mealsUnder11, mealsUnder30, playerMaxPlateLvl, playerMissingPlateUpgrades = parseJSON()
    playerTotalMealLevels = sum(playerMealsList[0])

    #Assess Tiers
    if highestCookingSkillLevel >= 1:
        tier_Cooking = 1
    if tier_Cooking == 1 and dchefLevel >= 15:
        tier_Cooking = 2
    if tier_Cooking == 2 and len(voidwalkers) > 0:
        tier_Cooking = 3
    if tier_Cooking == 3 and atomFlouride and playerTotalMealLevels >= 500:
        tier_Cooking = 4
    if tier_Cooking == 4 and mealsUnlocked >= maxMeals and mealsUnder30 <= 0:
        tier_Cooking = 5
    if tier_Cooking == 5 and playerMaxPlateLvl >= maxMealLevel:
        tier_Cooking = 6

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
        if len(voidwalkers) == 0:
            cooking_AdviceDict["NextTier"].append(Advice(
                label="Unlock a Voidwalker",
                picture_class="voidwalker-icon"
            ))
    # 3) if Vman:
    elif tier_Cooking == 3:
        cooking_AdviceDict["NextTier"].append(Advice(
            label="Unlock Fluoride - Void Plate Chef in the Atom Collider",
            picture_class="flouride"
        ))
        if playerTotalMealLevels < 500:
            cooking_AdviceDict["NextTier"].append(Advice(
                label="Reach 500+ total meal levels",
                picture_class="turkey-a-la-thank",
                progression=playerTotalMealLevels,
                goal=500
            ))
    # 4) if Atom Collider Flouride upgrade owned and total plates over 500:
    elif tier_Cooking == 4:
        if mealsUnlocked < maxMeals:
            cooking_AdviceDict["NextTier"].append(Advice(
                label=f"Unlock the remaining {maxMeals - mealsUnlocked} {pl(maxMeals-mealsUnlocked, 'meal', 'meals')}",
                picture_class="dharma-mesa-spice"
            ))
        if mealsUnder11 > 0:
            cooking_AdviceDict["NextTier"].append(Advice(
                label=f"Level up the remaining {mealsUnder11} unlocked {pl(mealsUnder11, 'meal', 'meals')} to 11+ for Diamond Chef",
                picture_class="diamond-chef",
                progression=mealsUnlocked - mealsUnder11,
                goal=mealsUnlocked
            ))
        if mealsUnder30 > 0:
            cooking_AdviceDict["NextTier"].append(Advice(
                label=f"Level up the remaining {mealsUnder30} unlocked {pl(mealsUnder30, 'meal', 'meals')} to 30+ for Flouride",
                picture_class="flouride",
                progression=mealsUnlocked - mealsUnder30,
                goal=mealsUnlocked
            ))
    # 5) All meals unlocked, all meals 30+
    elif tier_Cooking == 5:
        cooking_AdviceDict["NextTier"].append(Advice(
            label=f"Unlock max level {maxMealLevel} plates",
            picture_class="turkey-a-la-thank",
            progression=playerMaxPlateLvl,
            goal=maxMealLevel
        ))
    # 6) All basics + max plate levels
    #elif tier_Cooking == 6:
        # Finished, for now. Leaving this here for future use.
        # cooking_AdviceDict["NextTier"].append(Advice(
        #     label=f"",
        #     picture_class="",
        #     progression="",
        #     goal=""
        # ))

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
        remainingMeals = (maxMeals * maxMealLevel)-playerTotalMealLevels
        session_data.account.meals_remaining = remainingMeals
        cooking_AdviceDict["CurrentTier"].append(Advice(
            label=f"Info- Total Meal Levels ({remainingMeals} to go!)",
            picture_class="turkey-a-la-thank",
            progression=playerTotalMealLevels,
            goal=maxMeals * maxMealLevel,
        ))

    if playerMissingPlateUpgrades:
        for missingUpgrade in playerMissingPlateUpgrades:
            cooking_AdviceDict["PlateLevels"].append(Advice(
               label=missingUpgrade[0],
               picture_class=missingUpgrade[1],
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

    cooking_AdviceGroupDict["PlateLevels"] = AdviceGroup(
        tier="",
        pre_string=f"Each remaining upgrade gives +10 max plate levels",
        advices=cooking_AdviceDict["PlateLevels"],
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
