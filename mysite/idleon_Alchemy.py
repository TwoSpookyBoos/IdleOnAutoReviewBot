import json
from math import floor
from models import AdviceSection, AdviceGroup, Advice
from utils import pl, get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, getSpecificSkillLevelsList

logger = get_logger(__name__)

def getHighestAlchemyLevel(inputJSON, playerCount):
    alchemySkillLevelsList = getSpecificSkillLevelsList("Alchemy")
    highestAlchLevel = max(alchemySkillLevelsList)
    return highestAlchLevel

def getReadableVialNames(inputNumber):
    try:
        inputNumber = int(inputNumber)
    except:
        return f"Unknown Vial {inputNumber}"
    match inputNumber:
        case 0:
            return "Copper Corona (Copper Ore)"
        case 1:
            return "Sippy Splinters (Oak Logs)"
        case 2:
            return "Mushroom Soup (Spore Cap)"
        case 3:
            return "Spool Sprite (Thread)"
        case 4:
            return "Barium Mixture (Copper Bar)"
        case 5:
            return "Dieter Drink (Bean Slices)"
        case 6:
            return "Skinny 0 Cal (Snake Skin)"
        case 7:
            return "Thumb Pow (Trusty Nails)"
        case 8:
            return "Jungle Juice (Jungle Logs)"
        case 9:
            return "Barley Brew (Iron Bar)"
        case 10:
            return "Anearful (Glublin Ear)"
        case 11:
            return "Tea With Pea (Potty Rolls)"
        case 12:
            return "Gold Guzzle (Gold Ore)"
        case 13:
            return "Ramificoction (Bullfrog Horn)"
        case 14:
            return "Seawater (Goldfish)"
        case 15:
            return "Tail Time (Rats Tail)"
        case 16:
            return "Fly In My Drink (Fly)"
        case 17:
            return "Mimicraught (Megalodon Tooth)"
        case 18:
            return "Blue Flav (Platinum Ore)"
        case 19:
            return "Slug Slurp (Hermit Can)"
        case 20:
            return "Pickle Jar (BobJoePickle)"
        case 21:
            return "Fur Refresher (Floof Ploof)"
        case 22:
            return "Sippy Soul (Forest Soul)"
        case 23:
            return "Crab Juice (Crabbo)"
        case 24:
            return "Void Vial (Void Ore)"
        case 25:
            return "Red Malt (Redox Salts)"
        case 26:
            return "Ew Gross Gross (Mosquisnow)"
        case 27:
            return "The Spanish Sahara (Tundra Logs)"
        case 28:
            return "Poison Tincture (Poison Froge)"
        case 29:
            return "Etruscan Lager (Mamooth Tusk)"
        case 30:
            return "Chonker Chug (Dune Soul)"
        case 31:
            return "Bubonic Burp (Mousey)"
        case 32:
            return "Visible Ink (Pen)"
        case 33:
            return "Orange Malt (Explosive Salts)"
        case 34:
            return "Snow Slurry (Snow Ball)"
        case 35:
            return "Slowergy Drink (Frigid Soul)"
        case 36:
            return "Sippy Cup (Sippy Straw)"
        case 37:
            return "Bunny Brew (Bunny)"
        case 38:
            return "40-40 Purity (Contact Lense)"
        case 39:
            return "Shaved Ice (Purple Salt)"
        case 40:
            return "Goosey Glug (Honker)"
        case 41:
            return "Ball Pickle Jar (BallJoePickle)"
        case 42:
            return "Capachino (Purple Mush Cap)"
        case 43:
            return "Donut Drink (Half Eaten Donut)"
        case 44:
            return "Long Island Tea (Sand Shark)"
        case 45:
            return "Spook Pint (Squishy Soul)"
        case 46:
            return "Calcium Carbonate (Tongue Bone)"
        case 47:
            return "Bloat Draft (Blobfish)"
        case 48:
            return "Choco Milkshake (Crumpled Wrapper)"
        case 49:
            return "Pearl Seltzer (Pearler Shell)"
        case 50:
            return "Krakenade (Kraken)"
        case 51:
            return "Electrolyte (Condensed Zap)"
        case 52:
            return "Ash Agua (Suggma Ashes)"
        case 53:
            return "Maple Syrup (Maple Logs)"
        case 54:
            return "Hampter Drippy (Hampter)"
        case 55:
            return "Dreadnog (Dreadlo Bar)"
        case 56:
            return "Dusted Drink (Dust Mote)"
        case 57:
            return "Oj Jooce (Orange Slice)"
        case 58:
            return "Oozie Ooblek (Oozie Soul)"
        case 59:
            return "Venison Malt (Mongo Worm Slices)"
        case 60:
            return "Marble Mocha (Marble Ore)"
        case 61:
            return "Willow Sippy (Willow Logs)"
        case 62:
            return "Shinyfin Stew (Equinox Fish)"
        case 63:
            return "Dreamy Drink (Dream Particulate)"
        case 64:
            return "Ricecakorade (Rice Cake)"
        case 65:
            return "Ladybug Serum (Ladybug)"
        case 66:
            return "Flavorgil (Caulifish)"
        case 67:
            return "Greenleaf Tea (Leafy Branch)"
        case 68:
            return "Firefly Grog (Firefly)"
        case 69:
            return "Dabar Special (Godshard Bar)"
        case 70:
            return "Refreshment (Breezy Soul)"
        case 71:
            return "Gibbed Drink (Eviscerated Horn)"
        case 72:
            return "Ded Sap (Effervescent Log)"
        case 73:
            return "Royale Cola (Royal Headpiece)"
        case 74:
            return "Turtle Tisane (Tuttle)"
        case _:
            return f"Unknown Vial {inputNumber}"

def getReadableBubbleNames(inputNumber, color):
    try:
        inputNumber = int(inputNumber)
    except:
        return f"Unknown Bubble {color} {inputNumber}"
    match color:
        case "Orange":
            match inputNumber:
                case 0:
                    return "Roid Ragin"
                case 1:
                    return "Warriors Rule"
                case 2:
                    return "Hearty Diggy"
                case 3:
                    return "Wyoming Blood"
                case 4:
                    return "Reely Smart"
                case 5:
                    return "Big Meaty Claws"
                case 6:
                    return "Sploosh Sploosh"
                case 7:
                    return "Stronk Tools"
                case 8:
                    return "FMJ"
                case 9:
                    return "Bappity Boopity"
                case 10:
                    return "Brittley Spears"
                case 11:
                    return "Call Me Bob"
                case 12:
                    return "Carpenter"
                case 13:
                    return "Buff Boi Talent"
                case 14:
                    return "Orange Bargain"
                case 15:
                    return "Penny of Strength"
                case 16:
                    return "Multorange"
                case 17:
                    return "Dream of Ironfish"
                case 18:
                    return "Shimmeron"
                case 19:
                    return "Bite But Not Chew"
                case 20:
                    return "Spear Powah"
                case 21:
                    return "Slabi Orefish"
                case 22:
                    return "Gamer at Heart"
                case 23:
                    return "Slabi Strength"
                case 24:
                    return "Power Trione"
                case 25:
                    return "Farquad Force"
                case 26:
                    return "Endgame Eff I"
                case 27:
                    return "Tome Strength"
                case 28:
                    return "Essence Boost"
                case 29:
                    return "Crop Chapter"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"
        case "Green":
            match inputNumber:
                case 0:
                    return "Swift Steppin"
                case 1:
                    return "Archer or Bust"
                case 2:
                    return "Hammer Hammer"
                case 3:
                    return "Lil Big Damage"
                case 4:
                    return "Anvilnomics"
                case 5:
                    return "Quick Slap"
                case 6:
                    return "Sanic Tools"
                case 7:
                    return "Bug^2"
                case 8:
                    return "Shaquracy"
                case 9:
                    return "Cheap Shot"
                case 10:
                    return "Bow Jack"
                case 11:
                    return "Call Me Ash"
                case 12:
                    return "Cuz I Catch Em All"
                case 13:
                    return "Fast Boi Talent"
                case 14:
                    return "Green Bargain"
                case 15:
                    return "Dollar Of Agility"
                case 16:
                    return "Premigreen"
                case 17:
                    return "Fly in Mind"
                case 18:
                    return "Kill Per Kill"
                case 19:
                    return "Afk Expexp"
                case 20:
                    return "Bow Power"
                case 21:
                    return "Slabo Critterbug"
                case 22:
                    return "Sailor At Heart"
                case 23:
                    return "Slabo Agility"
                case 24:
                    return "Power Tritwo"
                case 25:
                    return "Quickdraw Quiver"
                case 26:
                    return "Essence Boost"
                case 27:
                    return "Endgame Eff II"
                case 28:
                    return "Tome Agility"
                case 29:
                    return "Stealth Chapter"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"
        case "Purple":
            match inputNumber:
                case 0:
                    return "Stable Jenius"
                case 1:
                    return "Mage is Best"
                case 2:
                    return "Hocus Choppus"
                case 3:
                    return "Molto Loggo"
                case 4:
                    return "Noodubble"
                case 5:
                    return "Name I Guess"
                case 6:
                    return "Le Brain Tools"
                case 7:
                    return "Cookin Roadkill"
                case 8:
                    return "Brewstachio"
                case 9:
                    return "All for Kill"
                case 10:
                    return "Matty Stafford"
                case 11:
                    return "Call Me Pope"
                case 12:
                    return "Gospel Leader"
                case 13:
                    return "Smart Boi Talent"
                case 14:
                    return "Purple Bargain"
                case 15:
                    return "Nickel Of Wisdom"
                case 16:
                    return "Severapurple"
                case 17:
                    return "Tree Sleeper"
                case 18:
                    return "Hyperswift"
                case 19:
                    return "Matrix Evolved"
                case 20:
                    return "Wand Pawur"
                case 21:
                    return "Slabe Logsoul"
                case 22:
                    return "Pious At Heart"
                case 23:
                    return "Slabe Wisdom"
                case 24:
                    return "Power Trithree"
                case 25:
                    return "Smarter Spells"
                case 26:
                    return "Endgame Eff III"
                case 27:
                    return "Essence Boost"
                case 28:
                    return "Tome Wisdom"
                case 29:
                    return "Essence Chapter"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"
        case "Yellow":
            match inputNumber:
                case 0:
                    return "Lotto Skills"
                case 1:
                    return "Droppin Loads"
                case 2:
                    return "Startue Exp"
                case 3:
                    return "Level Up Gift"
                case 4:
                    return "Prowesessary"
                case 5:
                    return "Stamp Tramp"
                case 6:
                    return "Undeveloped Costs"
                case 7:
                    return "Da Daily Drip"
                case 8:
                    return "Grind Time"
                case 9:
                    return "Laaarrrryyyy"
                case 10:
                    return "Cogs For Hands"
                case 11:
                    return "Sample It"
                case 12:
                    return "Big Game Hunter"
                case 13:
                    return "Ignore Overdues"
                case 14:
                    return "Yellow Bargain"
                case 15:
                    return "Mr Massacre"
                case 16:
                    return "Egg Ink"
                case 17:
                    return "Diamond Chef"
                case 18:
                    return "Card Champ"
                case 19:
                    return "Petting The Rift"
                case 20:
                    return "Boaty Bubble"
                case 21:
                    return "Big P"
                case 22:
                    return "Bit By Bit"
                case 23:
                    return "Gifts Abound"
                case 24:
                    return "Atom Split"
                case 25:
                    return "Cropius Mapper"
                case 26:
                    return "Essence Boost"
                case 27:
                    return "Hinge Buster"
                case 28:
                    return "Ninja Looter"
                case 29:
                    return "Lo Cost Mo Jade"
                case _:
                    return f"Unknown Bubble {color} {inputNumber}"

def getBubbleColorFromName(inputName):
    match inputName:
        case "FMJ" | "Call Me Bob" | "Carpenter", "Shimmeron":
            return " (Orange"
        case "Hammer Hammer" | "Shaquracy":
            return " (Green"
        case "Cookin Roadkill", "All For Kill":
            return " (Purple"
        case "Prowesessary" | "Laaarrrryyyy" | "Startue Exp" | "Droppin Loads" | "Diamond Chef" | "Big P" | "Big Game Hunter" | "Mr Massacre" | "Grind Time":
            return " (Yellow"
        case _:
            return f" (Unknown- {inputName}"

def getSumUnlockedBubbles(colorDict, colorString):
    bubblesUnlocked = 0
    for bubble in colorDict:
        if not isinstance(colorDict[bubble], int):
            #logger.warning(f"Non-Integer Bubble value found. Attempting to convert: {colorString} {bubble} {type(colorDict[bubble])} {colorDict[bubble]}")
            try:
                colorDict[bubble] = int(round(float(colorDict[bubble])))
            except:
                logger.exception(f"Could not convert [{colorString} {bubble} {type(colorDict[bubble])} {colorDict[bubble]}] to int :( Setting bubble to level 0")
                colorDict[bubble] = 0
        if colorDict[bubble] > 0:
            bubblesUnlocked += 1
    return bubblesUnlocked

def setAlchemyVialsProgressionTier(inputJSON, progressionTiers, characterDict) -> AdviceSection:
    vial_AdviceDict = {
        "EarlyVials": {
            "Total Unlocked Vials": [],
            "Shaman's Virile Vials": []
        },
        "MaxVials": {
            "Total Maxed Vials": [],
            "Vials to max next": [],
        },
    }
    vial_AdviceGroupDict = {}
    vial_AdviceSection = AdviceSection(
        name="Vials",
        tier="Not Yet Evaluated",
        header="Best Vial tier met: Not Yet Evaluated",
        picture="Alchemy_Vial-level-1.png"
    )
    highestAlchemyLevel = getHighestAlchemyLevel(inputJSON, len(characterDict))
    if highestAlchemyLevel < 1:
        vial_AdviceSection.header = "Come back after unlocking the Alchemy skill in World 2!"
        return vial_AdviceSection

    max_IndexOfVials = 75
    manualVialsAdded = 0
    virileVialsList = []
    maxExpectedVV = max_IndexOfVials-4  # Exclude both pickle and both rare drop vials
    maxedVialsList = []
    unmaxedVialsList = []
    lockedVialsList = []

    try:
        alchemyVialsDict = inputJSON["CauldronInfo"][4]
        del alchemyVialsDict["length"]
        while len(alchemyVialsDict) < max_IndexOfVials:
            alchemyVialsDict[str(max_IndexOfVials-manualVialsAdded)] = 0
            manualVialsAdded += 1
    except:
        alchemyVialsDict = {}
        logger.exception("Unable to retrieve alchemyVialsDict from JSON. Creating an empty Dict.")

    unlockedVials = 0
    for vial in alchemyVialsDict:
        if alchemyVialsDict[vial] == 0:
            lockedVialsList.append(vial)
            unmaxedVialsList.append(getReadableVialNames(vial))
        else:
            unlockedVials += 1
            if alchemyVialsDict[vial] >= 4:
                virileVialsList.append(getReadableVialNames(vial))
            if alchemyVialsDict[vial] >= 13:
                maxedVialsList.append(getReadableVialNames(vial))
            elif alchemyVialsDict[vial] != 'length':
                unmaxedVialsList.append(getReadableVialNames(vial))

    if len(virileVialsList) < maxExpectedVV:
        vial_AdviceDict["EarlyVials"]["Shaman's Virile Vials"].append(
            Advice(label="Total level 4+ Vials", picture_class="vial-l4", progression=len(virileVialsList), goal=maxExpectedVV)
        )

    tier_TotalVialsUnlocked = 0
    tier_TotalVialsMaxed = 0
    overall_AlchemyVialsTier = 0
    max_tier = progressionTiers[-1][0]
    maxAdvicesPerGroup = 6

    if session_data.account.vial_mastery_unlocked:
        if len(maxedVialsList) < 27:
            advice_TrailingMaxedVials = " 27 is the magic number needed to get the Snake Skin vial to 100% chance to double deposited statues :D (This also requires Snake Skin itself be maxed lol)"
        else:
            advice_TrailingMaxedVials = " Thanks to the Vial Mastery bonus in W4's Rift, every maxed vial increases the bonus of EVERY vial you have unlocked!"
    else:
        advice_TrailingMaxedVials = ""

    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalVialsUnlocked
        #tier[2] = int TotalVialsMaxed
        #tier[3] = list ParticularVialsMaxed
        #tier[4] = str Notes

        #Total Vials Unlocked
        if tier_TotalVialsUnlocked == (tier[0]-1):  # Only check if they already met previous tier
            if unlockedVials >= tier[1]:
                tier_TotalVialsUnlocked = tier[0]
            else:
                vial_AdviceDict["EarlyVials"]["Total Unlocked Vials"].append(
                    Advice(label=f"Unlock more vial{pl(['Placeholder'] * (tier[1] - unlockedVials), '', 's')}", picture_class="vials",
                           progression=str(unlockedVials), goal=str(tier[1]))
                )

        #Total Vials Maxed
        if tier_TotalVialsMaxed == (tier[0]-1):  # Only check if they already met previous tier
            if len(maxedVialsList) >= tier[2]:
                tier_TotalVialsMaxed = tier[0]
            else:
                if tier_TotalVialsMaxed >= 20:
                    advice_TrailingMaxedVials += tier[4]
                vial_AdviceDict["MaxVials"]["Total Maxed Vials"].append(
                    Advice(label="Total Maxed Vials", picture_class="vial-max", progression=str(len(maxedVialsList)), goal=str(tier[2]))
                )

        #Particular Vials Maxed
        for requiredVial in tier[3]:
            if requiredVial in unmaxedVialsList:
                if len(vial_AdviceDict["MaxVials"]["Vials to max next"]) < maxAdvicesPerGroup:
                    vial_AdviceDict["MaxVials"]["Vials to max next"].append(
                        Advice(label=requiredVial, picture_class=requiredVial.split("(")[0].strip(), progression="", goal="")
                    )

    #Generate AdviceGroups
    vial_AdviceGroupDict["Total Unlocked Vials"] = AdviceGroup(
        tier=str(tier_TotalVialsUnlocked),
        pre_string="Early Vial Goals",
        post_string="",
        advices=vial_AdviceDict["EarlyVials"]
    )
    if len(vial_AdviceDict["EarlyVials"]["Total Unlocked Vials"]) > 0:
        vial_AdviceGroupDict["Total Unlocked Vials"].post_string = "For the most unlock chances per day, rapidly drop multiple stacks of items on the cauldron!"
    else:
        del vial_AdviceGroupDict["Total Unlocked Vials"].advices["Total Unlocked Vials"]

    vial_AdviceGroupDict["Total Maxed Vials"] = AdviceGroup(
        tier=str(tier_TotalVialsMaxed),
        pre_string="Late Vial Goals",
        post_string=advice_TrailingMaxedVials,
        advices=vial_AdviceDict["MaxVials"]  #["Total Maxed Vials"]
    )

    #Generate AdviceSection
    overall_AlchemyVialsTier = min(tier_TotalVialsUnlocked, tier_TotalVialsMaxed)  #, tier_ParticularVialsMaxed)
    tier_section = f"{overall_AlchemyVialsTier}/{max_tier}"
    vial_AdviceSection.tier = tier_section
    vial_AdviceSection.pinchy_rating = overall_AlchemyVialsTier
    vial_AdviceSection.groups = vial_AdviceGroupDict.values()
    if overall_AlchemyVialsTier == max_tier:
        vial_AdviceSection.header = f"Best Vial tier met: {tier_section}<br>You best ❤️"
    else:
        vial_AdviceSection.header = f"Best Vial tier met: {tier_section}"

    return vial_AdviceSection

def setAlchemyBubblesProgressionTier(inputJSON, progressionTiers, characterDict) -> AdviceSection:
    bubbles_AdviceDict = {
        "TotalBubblesUnlocked": [],
        "PurpleSampleBubbles": {},
        "OrangeSampleBubbles": {},
        "GreenSampleBubbles": {},
        "UtilityBubbles": {}
    }
    bubbles_AdviceGroupDict = {}
    bubbles_AdviceSection = AdviceSection(
        name="Bubbles",
        tier="Not Yet Evaluated",
        header="Best Bubbles tier met: Not Yet Evaluated. Recommended Bubbles actions:",
        picture="Alchemy_Bubble_all.gif"
    )
    highestAlchemyLevel = getHighestAlchemyLevel(inputJSON, len(characterDict))
    if highestAlchemyLevel < 1:
        bubbles_AdviceSection.header = "Come back after unlocking the Alchemy skill in World 2!"
        return bubbles_AdviceSection

    currentlyAvailableBubblesIndex = 29
    tier_TotalBubblesUnlocked = 0
    orangeBubblesUnlocked = 0
    greenBubblesUnlocked = 0
    purpleBubblesUnlocked = 0
    yellowBubblesUnlocked = 0
    sum_TotalBubblesUnlocked = 0
    tier_OrangeSampleBubbles = 0
    tier_GreenSampleBubbles = 0
    tier_PurpleSampleBubbles = 0
    tier_UtilityBubbles = 0
    max_tier = progressionTiers[-1][0]
    overall_alchemyBubblesTier = 0
    adviceCountsDict = {"PurpleSampleBubbles": 0, "OrangeSampleBubbles": 0, "GreenSampleBubbles": 0, "UtilityBubbles": 0}

    #Get the bubble data and remove the length element
    raw_orange_alchemyBubblesDict = inputJSON["CauldronInfo"][0]
    del raw_orange_alchemyBubblesDict['length']
    raw_green_alchemyBubblesDict = inputJSON["CauldronInfo"][1]
    del raw_green_alchemyBubblesDict['length']
    raw_purple_alchemyBubblesDict = inputJSON["CauldronInfo"][2]
    del raw_purple_alchemyBubblesDict['length']
    raw_yellow_alchemyBubblesDict = inputJSON["CauldronInfo"][3]
    del raw_yellow_alchemyBubblesDict['length']

    #Replace the bubble numbers with their names for readable evaluation against the progression tiers
    named_all_alchemyBubblesDict = {}
    for bubble in raw_orange_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Orange")] = int(raw_orange_alchemyBubblesDict[bubble])
    for bubble in raw_green_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Green")] = int(raw_green_alchemyBubblesDict[bubble])
    for bubble in raw_purple_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Purple")] = int(raw_purple_alchemyBubblesDict[bubble])
    for bubble in raw_yellow_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Yellow")] = int(raw_yellow_alchemyBubblesDict[bubble])

    #Sum up unlocked bubbles (level > 0)
    orangeBubblesUnlocked = getSumUnlockedBubbles(raw_orange_alchemyBubblesDict, "Orange")
    greenBubblesUnlocked = getSumUnlockedBubbles(raw_green_alchemyBubblesDict, "Green")
    purpleBubblesUnlocked = getSumUnlockedBubbles(raw_purple_alchemyBubblesDict, "Purple")
    yellowBubblesUnlocked = getSumUnlockedBubbles(raw_yellow_alchemyBubblesDict, "Yellow")
    sum_TotalBubblesUnlocked += orangeBubblesUnlocked + greenBubblesUnlocked + purpleBubblesUnlocked + yellowBubblesUnlocked

    bubbleUnlockListByWorld = [20,0,0,0,0,0,0,0,0]
    combined_BubblesList = [orangeBubblesUnlocked, greenBubblesUnlocked, purpleBubblesUnlocked, yellowBubblesUnlocked]
    for bubbleColorCount in combined_BubblesList:
        worldCounter = 1
        while bubbleColorCount >= 5 and worldCounter <= len(bubbleUnlockListByWorld)-1:
            bubbleUnlockListByWorld[worldCounter] += 5
            bubbleColorCount -= 5
            worldCounter += 1
        if bubbleColorCount > 0 and worldCounter <= len(bubbleUnlockListByWorld)-1:
            bubbleUnlockListByWorld[worldCounter] += bubbleColorCount
            bubbleColorCount = 0
    nextWorldMissingBubbles = 0
    for world in range(0, len(bubbleUnlockListByWorld)):
        if bubbleUnlockListByWorld[world] == 20:
            nextWorldMissingBubbles += 1

    #Assess tiers
    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalBubblesUnlocked
        #tier[2] = dict {OrangeSampleBubbles}
        #tier[3] = dict {GreenSampleBubbles}
        #tier[4] = dict {PurpleSampleBubbles}
        #tier[5] = dict {UtilityBubbles}
        #tier[6] = str BubbleValuePercentage
        #tier[7] = str Notes

        #tier_TotalBubblesUnlocked
        if tier_TotalBubblesUnlocked == (tier[0]-1):  # Only check if they already met the previous tier
            if sum_TotalBubblesUnlocked >= tier[1]:
                tier_TotalBubblesUnlocked = tier[0]
            else:
                advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked)
                advice_TotalBubblesUnlocked += "- You have unlocked " + str(bubbleUnlockListByWorld[nextWorldMissingBubbles]) + "/20 of W" + str(nextWorldMissingBubbles) + " bubbles."
                bubbleUnlockCountList = [orangeBubblesUnlocked, greenBubblesUnlocked, purpleBubblesUnlocked, yellowBubblesUnlocked]
                colorList = ["Orange", "Green", "Purple", "Yellow"]
                imagenameList = ["cauldron-o", "cauldron-g", "cauldron-p", "cauldron-y"]
                for counter in range(0, len(bubbleUnlockCountList)):
                    if bubbleUnlockCountList[counter] < (5 * nextWorldMissingBubbles):
                        bubbles_AdviceDict["TotalBubblesUnlocked"].append(
                            Advice(
                                label=f"{colorList[counter]} Bubbles Unlocked",
                                picture_class=imagenameList[counter],
                                progression=str(bubbleUnlockCountList[counter] - (5 * (nextWorldMissingBubbles - 1))),
                                goal=5)
                        )

        #tier_OrangeSampleBubbles
        all_orangeRequirementsMet = True
        for requiredBubble in tier[2]:
            #requiredBubble = name of the bubble
            #tier[2][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict[requiredBubble] = level of the player's bubble
            if named_all_alchemyBubblesDict[requiredBubble] < tier[2][requiredBubble]:
                all_orangeRequirementsMet = False
                if len(bubbles_AdviceDict["OrangeSampleBubbles"]) < maxTiersPerGroup:
                    adviceCountsDict["OrangeSampleBubbles"] += 1
                    if f"To reach Tier {tier[0]} ({tier[6]} max value)" not in bubbles_AdviceDict["OrangeSampleBubbles"]:
                        bubbles_AdviceDict["OrangeSampleBubbles"][f"To reach Tier {tier[0]} ({tier[6]} max value)"] = []
                    bubbles_AdviceDict["OrangeSampleBubbles"][f"To reach Tier {tier[0]} ({tier[6]} max value)"].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict[requiredBubble]),
                            goal=str(tier[2][requiredBubble]))
                    )
        if tier_OrangeSampleBubbles == (tier[0]-1) and all_orangeRequirementsMet == True:  # Only update if they already met the previous tier
            tier_OrangeSampleBubbles = tier[0]

        #tier_GreenSampleBubbles
        all_greenRequirementsMet = True
        for requiredBubble in tier[3]:
            #requiredBubble = name of the bubble
            #tier[2][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict[requiredBubble] = level of the player's bubble
            if named_all_alchemyBubblesDict[requiredBubble] < tier[3][requiredBubble]:
                all_greenRequirementsMet = False
                if len(bubbles_AdviceDict["GreenSampleBubbles"]) < maxTiersPerGroup:
                    adviceCountsDict["GreenSampleBubbles"] += 1
                    if f"To reach Tier {tier[0]} ({tier[6]} max value)" not in bubbles_AdviceDict["GreenSampleBubbles"]:
                        bubbles_AdviceDict["GreenSampleBubbles"][f"To reach Tier {tier[0]} ({tier[6]} max value)"] = []
                    bubbles_AdviceDict["GreenSampleBubbles"][f"To reach Tier {tier[0]} ({tier[6]} max value)"].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict[requiredBubble]),
                            goal=str(tier[3][requiredBubble]))
                    )
        if tier_GreenSampleBubbles == (tier[0]-1) and all_greenRequirementsMet == True:  # Only update if they already met the previous tier
            tier_GreenSampleBubbles = tier[0]

        #tier_PurpleSampleBubbles
        all_purpleRequirementsMet = True
        for requiredBubble in tier[4]:
            #requiredBubble = name of the bubble
            #tier[3][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict[requiredBubble] = level of the player's bubble
            if named_all_alchemyBubblesDict[requiredBubble] < tier[4][requiredBubble]:
                all_purpleRequirementsMet = False
                if len(bubbles_AdviceDict["PurpleSampleBubbles"]) < maxTiersPerGroup:
                    adviceCountsDict["PurpleSampleBubbles"] += 1
                    if f"To reach Tier {tier[0]} ({tier[6]} max value)" not in bubbles_AdviceDict["PurpleSampleBubbles"]:
                        bubbles_AdviceDict["PurpleSampleBubbles"][f"To reach Tier {tier[0]} ({tier[6]} max value)"] = []
                    bubbles_AdviceDict["PurpleSampleBubbles"][f"To reach Tier {tier[0]} ({tier[6]} max value)"].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict[requiredBubble]),
                            goal=str(tier[4][requiredBubble]))
                    )
        if tier_PurpleSampleBubbles == (tier[0]-1) and all_purpleRequirementsMet == True:  # Only update if they already met the previous tier
            tier_PurpleSampleBubbles = tier[0]

        #tier_UtilityBubbles
        all_utilityRequirementsMet = True
        for requiredBubble in tier[5]:
            #requiredBubble = name of the bubble
            #tier[3][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict[requiredBubble] = level of the player's bubble
            if named_all_alchemyBubblesDict[requiredBubble] < tier[5][requiredBubble]:
                all_utilityRequirementsMet = False
                if len(bubbles_AdviceDict["UtilityBubbles"]) < maxTiersPerGroup:
                    adviceCountsDict["UtilityBubbles"] += 1
                    if f"To reach Tier {tier[0]}" not in bubbles_AdviceDict["UtilityBubbles"]:
                        bubbles_AdviceDict["UtilityBubbles"][f"To reach Tier {tier[0]}"] = []
                    bubbles_AdviceDict["UtilityBubbles"][f"To reach Tier {tier[0]}"].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict[requiredBubble]),
                            goal=str(tier[5][requiredBubble]))
                    )
        if tier_UtilityBubbles == (tier[0]-1) and all_utilityRequirementsMet == True:
            tier_UtilityBubbles = tier[0]

    overall_alchemyBubblesTier = min(max_tier, tier_TotalBubblesUnlocked, tier_OrangeSampleBubbles, tier_GreenSampleBubbles, tier_PurpleSampleBubbles, tier_UtilityBubbles)

    #Generate AdviceGroups
    agdNames = ["TotalBubblesUnlocked", "OrangeSampleBubbles", "GreenSampleBubbles", "PurpleSampleBubbles", "UtilityBubbles"]
    agdTiers = [tier_TotalBubblesUnlocked, tier_OrangeSampleBubbles, tier_GreenSampleBubbles, tier_PurpleSampleBubbles, tier_UtilityBubbles]
    agdPre_strings = [
        f"Continue unlocking W{nextWorldMissingBubbles} bubbles",
        f"Level Orange sample-boosting bubbles",
        f"Level Green sample-boosting bubbles",
        f"Level Purple sample-boosting bubbles",
        f"Level Utility bubbles",
    ]
    agdPost_strings = [
        "", "", "",
        "Choppin Log samples are the largest producers of Atom Particles and should be given priority.",
        "",
    ]
    if tier_UtilityBubbles == max_tier:
        agdPost_strings.append(progressionTiers[tier_UtilityBubbles][7])
    else:
        agdPost_strings.append(progressionTiers[tier_UtilityBubbles+1][7])
    for counter in range(0, len(agdNames)):
        bubbles_AdviceGroupDict[agdNames[counter]] = AdviceGroup(
            tier=agdTiers[counter],
            pre_string=agdPre_strings[counter],
            post_string="",  #agdPost_strings[counter],
            advices=bubbles_AdviceDict[agdNames[counter]]
        )

    #Generate AdviceSection
    tier_section = f"{overall_alchemyBubblesTier}/{max_tier}"
    bubbles_AdviceSection.tier = tier_section
    bubbles_AdviceSection.pinchy_rating = overall_alchemyBubblesTier
    if overall_alchemyBubblesTier == max_tier:
        bubbles_AdviceSection.header = f"Best Bubbles tier met: {tier_section}<br>You best ❤️"
    else:
        bubbles_AdviceSection.header = f"Best Bubbles tier met: {tier_section}"
        bubbles_AdviceSection.groups = bubbles_AdviceGroupDict.values()
    return bubbles_AdviceSection

def setAlchemyP2W(inputJSON, characterDict) -> AdviceSection:
    p2w_AdviceDict = {
        "Pay2Win": []
    }
    p2w_AdviceGroupDict = {}
    p2w_AdviceSection = AdviceSection(
        name="Pay2Win",
        tier="Not Yet Evaluated",
        header="Best P2W tier met: Not Yet Evaluated. Recommended P2W actions:",
        picture="pay2win.png"
    )
    highestAlchemyLevel = getHighestAlchemyLevel(inputJSON, len(characterDict))
    if highestAlchemyLevel < 1:
        p2w_AdviceSection.header = "Come back after unlocking the Alchemy skill in World 2!"
        return p2w_AdviceSection

    alchemyP2WList = json.loads(inputJSON["CauldronP2W"])
    bubbleCauldronSum = 0
    liquidCauldronSum = 0
    vialsSum = 0
    playerSum = 0
    p2wSum = 0
    liquidCauldronsUnlocked = 1

    if highestAlchemyLevel >= 80:
        liquidCauldronsUnlocked = 4  #includes Toxic HG
    elif highestAlchemyLevel >= 35:
        liquidCauldronsUnlocked = 3  # includes Trench Seawater
    elif highestAlchemyLevel >= 20:
        liquidCauldronsUnlocked = 2  # includes Liquid Nitrogen

    bubbleCauldronMax = 4 * 375  # 4 cauldrons, 375 upgrades each
    liquidCauldronMax = 180 * liquidCauldronsUnlocked
    vialsMax = 15 + 45  # 15 attempts, 45 RNG
    bubbleCauldronSum = sum(alchemyP2WList[0])
    vialsSum = sum(alchemyP2WList[2])
    playerSum = sum(alchemyP2WList[3])
    for liquidEntry in alchemyP2WList[1]:  # Liquids are different. Any locked liquid cauldrons are stored as -1 which would throw off a simple sum
        if liquidEntry != -1:
            liquidCauldronSum += liquidEntry

    p2wSum = bubbleCauldronSum + liquidCauldronSum + vialsSum + playerSum
    p2wMax = bubbleCauldronMax + liquidCauldronMax + vialsMax + (highestAlchemyLevel*2)
    p2wSumWithoutPlayer = bubbleCauldronSum + liquidCauldronSum + vialsSum
    p2wMaxWithoutPlayer = bubbleCauldronMax + liquidCauldronMax + vialsMax

    if p2wSumWithoutPlayer >= p2wMaxWithoutPlayer:
        p2w_AdviceSection.pinchy_rating = 1
        p2w_AdviceSection.tier = '1/1'
    else:
        p2w_AdviceSection.pinchy_rating = 0
        p2w_AdviceSection.tier = '0/1'

    if p2wSum >= p2wMax:
        p2w_AdviceSection.header = f"You've purchased all {p2wMax} upgrades in Alchemy-P2W! You best ❤️"
    else:
        if bubbleCauldronSum < bubbleCauldronMax:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Bubble Cauldron Upgrades", picture_class="cauldron-a", progression=str(bubbleCauldronSum), goal=str(bubbleCauldronMax))
            )
        if liquidCauldronSum < liquidCauldronMax:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Liquid Cauldron Upgrades", picture_class="bleach-liquid-cauldrons", progression=str(liquidCauldronSum),
                       goal=str(liquidCauldronMax))
            )
        if vialsSum < vialsMax:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Vial Upgrades", picture_class="vials", progression=str(vialsSum), goal=str(vialsMax))
            )
        if playerSum < highestAlchemyLevel*2:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Player Upgrades", picture_class="p2w-player", progression=str(playerSum), goal=str(highestAlchemyLevel * 2))
            )
    p2w_AdviceGroupDict["Pay2Win"] = AdviceGroup(
        tier="",
        pre_string="Remaining Pay2Win upgrades to purchase",
        post_string="",
        advices=p2w_AdviceDict["Pay2Win"]
    )

    #Generate AdviceSection
    tier_section = f"{p2wSum}/{p2wMax}"
    p2w_AdviceSection.tier = tier_section
    p2w_AdviceSection.groups = p2w_AdviceGroupDict.values()
    if p2wSum >= p2wMax:
        p2w_AdviceSection.header = f"You've purchased all {p2wMax} upgrades in Alchemy-P2W! You best ❤️"
    else:
        p2w_AdviceSection.header = f"You've purchased {tier_section} upgrades in Alchemy P2W. Try to purchase the basic upgrades before Mid W5, and Player upgrades after each level up!"
    return p2w_AdviceSection
