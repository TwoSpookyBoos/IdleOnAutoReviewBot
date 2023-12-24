import json
import progressionResults

def getHighestAlchemyLevel(inputJSON, playerCount):
    highestAlchLevel = 0
    counter = 0
    while counter < playerCount:
        try:
            if highestAlchLevel < inputJSON['Lv0_'+str(counter)][5]:
                highestAlchLevel = inputJSON['Lv0_'+str(counter)][5]
        except Exception as reason:
            print("Alchemy~ EXCEPTION Could not retrieve alchemy level for playerCount of ",playerCount, reason)
        counter += 1
    #print("Alchemy~ OUTPUT highestAlchLevel:",highestAlchLevel)
    return highestAlchLevel

def getReadableVialNames(inputNumber):
    try:
        inputNumber = int(inputNumber)
    except:
        return ("Unknown Vial " + inputNumber)
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
        case _:
            return ("Unknown Vial " + inputNumber)

def getReadableBubbleNames(inputNumber, color):
    try:
        inputNumber = int(inputNumber)
    except:
        return ("Unknown Bubble " + str(color) + str(inputNumber))
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
                case _:
                    return ("Unknown Bubble " + str(color) + str(inputNumber))
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
                case _:
                    return ("Unknown Bubble " + str(color) + str(inputNumber))
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
                    return "All For Kill"
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
                case _:
                    return ("Unknown Bubble " + str(color) + str(inputNumber))
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
                case _:
                    return ("Unknown Bubble " + str(color) + str(inputNumber))

def getBubbleColorFromName(inputName):
    match inputName:
        case "FMJ" | "Call Me Bob" | "Carpenter":
            return str(" (Orange)")
        case "Hammer Hammer" | "Shaquracy":
            return str(" (Green)")
        case "Cookin Roadkill":
            return str(" (Purple)")
        case "Prowesessary" | "Laaarrrryyyy" | "Startue Exp" | "Droppin Loads" | "Diamond Chef" | "Big P" | "Big Game Hunter" | "Mr Massacre" | "Grind Time":
            return str(" (Yellow)")
        case _:
            return str(" (Unknown)")

def setAlchemyVialsProgressionTier(inputJSON, progressionTiers):
    alchemyVialsDict = inputJSON["CauldronInfo"][4]
    try:
        del alchemyVialsDict["length"]
    except Exception as reason:
        print("Alchemy~ EXCPTION Unable to delete 'length' element from alchemyVialsDict:",reason)
    #print("Alchemy~ OUTPUT alchemyVialsDict:",len(alchemyVialsDict), alchemyVialsDict)
    try:
        highestCompletedRift = inputJSON["Rift"][0]
        if highestCompletedRift >= 35:
            advice_SnakeskinRiftVialMastery = " 27 is the magic number needed to get the Snake Skin vial to 100% chance to double deposited statues :D (This also requires Snake Skin itself be maxed lol)"
        else:
            advice_SnakeskinRiftVialMastery = ""
    except Exception as reason:
        print("Alchemy~ EXCEPTION Unable to retrieve highest rift level.",reason)
        highestCompletedRift = 0
    virileVialsList = []
    maxExpectedVV = 62 #Excludes both pickle vials
    maxedVialsList = []
    unmaxedVialsList = []
    lockedVialsList = []

    unlockedVials = 0
    for vial in alchemyVialsDict:
        if alchemyVialsDict[vial] == 0:
            lockedVialsList.append(vial)
        else:
            unlockedVials += 1
            if alchemyVialsDict[vial] >= 4:
                virileVialsList.append(getReadableVialNames(vial))
            if alchemyVialsDict[vial] >= 13:
                maxedVialsList.append(getReadableVialNames(vial))
            elif alchemyVialsDict[vial] != 'length':
                unmaxedVialsList.append(getReadableVialNames(vial))

    #print("Alchemy.setAlchemyVialsProgressionTier~ OUTPUT maxedVialsList:",len(maxedVialsList),maxedVialsList)
    #print("Alchemy.setAlchemyVialsProgressionTier~ OUTPUT virileVialsList:",len(virileVialsList),virileVialsList)
    tier_TotalVialsUnlocked = 0
    tier_TotalVialsMaxed = 0
    tier_ParticularVialsMaxed = 0
    overall_AlchemyVialsTier = 0
    advice_TotalVialsUnlocked = ""
    advice_TotalVialsMaxed = ""
    advice_ParticularVialsMaxed = ""
    advice_VirileVials = ""

    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalVialsUnlocked
        #tier[2] = int TotalVialsMaxed
        #tier[3] = list ParticularVialsMaxed
        #tier[4] = str Notes
        if tier_TotalVialsUnlocked == (tier[0]-1): #Only check if they already met previous tier
            if unlockedVials >= tier[1]:
                tier_TotalVialsUnlocked = tier[0]
            else:
                advice_TotalVialsUnlocked = "Tier " + str(tier_TotalVialsUnlocked) + "- Unlock some more vials: " + str(unlockedVials) + "/" + str(tier[1]) + tier[4] + "For the most unlock chances per day, rapidly drop multiple stacks of items on the cauldron!"
        if tier_TotalVialsMaxed == (tier[0]-1): #Only check if they already met previous tier
            if len(maxedVialsList) >= tier[2]:
                tier_TotalVialsMaxed = tier[0]
            else:
                if len(maxedVialsList) < 27 and highestCompletedRift >= 35:
                    advice_TotalVialsMaxed = "Tier " + str(tier_TotalVialsMaxed) + "- Max some more vials: " + str(len(maxedVialsList)) + "/" + str(tier[2]) + "." + advice_SnakeskinRiftVialMastery
                else:
                    advice_TotalVialsMaxed = "Tier " + str(tier_TotalVialsMaxed) + "- Max some more vials: " + str(len(maxedVialsList)) + "/" + str(tier[2]) + ". Thanks to the Vial Mastery bonus in W4's Rift, every maxed vial increases the bonus of EVERY vial you have unlocked!"
                    if tier_TotalVialsMaxed >= 20:
                        advice_TotalVialsMaxed += tier[4]
        if tier_ParticularVialsMaxed == (tier[0]-1): #Only check if they already met previous tier
            allRequirementsMet = True
            for requiredVial in tier[3]:
                #print("Looking for Vial ", requiredVial, " in " , unmaxedVialsList)
                if requiredVial in unmaxedVialsList:
                    allRequirementsMet = False
                    advice_ParticularVialsMaxed += requiredVial + ", "
            if allRequirementsMet == True:
                #print("Alch particular vial passed at tier",tier[0],tier[4])
                tier_ParticularVialsMaxed = tier[0]
            else:
                #print("Alch particular vial failed at tier",tier[0],tier[4])
                advice_ParticularVialsMaxed = "Tier " + str(tier_ParticularVialsMaxed) + "- Work on maxing these particular vial(s): " + advice_ParticularVialsMaxed[:-2] #strip off the final comma and space
    overall_AlchemyVialsTier = min(tier_TotalVialsUnlocked, tier_TotalVialsMaxed, tier_ParticularVialsMaxed)
    if len(virileVialsList) < maxExpectedVV:
        advice_VirileVials = "Informational- You have " + str(len(virileVialsList)) + "/" + str(maxExpectedVV) + " vials up to level 4, giving damage to Shaman's Virile Vials talent :)"
    advice_AlchemyVialsCombined = [
        "Best Alchemy-Vials tier met: " + str(overall_AlchemyVialsTier) + "/" + str(progressionTiers[-3][0]) + ". Recommended Alchemy-Vials actions:",
        advice_TotalVialsUnlocked,
        advice_TotalVialsMaxed,
        advice_ParticularVialsMaxed,
        advice_VirileVials]
    alchemyVialsPR = progressionResults.progressionResults(overall_AlchemyVialsTier,advice_AlchemyVialsCombined,"")
    return alchemyVialsPR

def setAlchemyBubblesProgressionTier(inputJSON, progressionTiers):
    currentlyAvailableBubblesIndex = 24
    tier_TotalBubblesUnlocked = 0
    orangeBubblesUnlocked = 0
    greenBubblesUnlocked = 0
    purpleBubblesUnlocked = 0
    yellowBubblesUnlocked = 0
    w1BubblesUnlocked = 0
    w2BubblesUnlocked = 0
    w3BubblesUnlocked = 0
    w4BubblesUnlocked = 0
    w5BubblesUnlocked = 0
    w6BubblesUnlocked = 0
    w7BubblesUnlocked = 0
    w8BubblesUnlocked = 0
    sum_TotalBubblesUnlocked = 0
    tier_OrangeSampleBubbles = 0
    tier_GreenSampleBubbles = 0
    tier_PurpleSampleBubbles = 0
    tier_UtilityBubbles = 0
    overall_alchemyBubblesTier = 0

    advice_TotalBubblesUnlocked = ""
    advice_OrangeSampleBubbles = ""
    advice_GreenSampleBubbles = ""
    advice_PurpleSampleBubbles = ""
    advice_UtilityBubbles = ""

    #Get the bubble data and remove the length element
    raw_orange_alchemyBubblesDict = inputJSON["CauldronInfo"][0]
    del raw_orange_alchemyBubblesDict['length']
    raw_green_alchemyBubblesDict = inputJSON["CauldronInfo"][1]
    del raw_green_alchemyBubblesDict['length']
    raw_purple_alchemyBubblesDict = inputJSON["CauldronInfo"][2]
    del raw_purple_alchemyBubblesDict['length']
    raw_yellow_alchemyBubblesDict = inputJSON["CauldronInfo"][3]
    del raw_yellow_alchemyBubblesDict['length']

    #Replace the bubble numbers with their names for readable evaluation against the the progression tiers
    named_all_alchemyBublesDict = {}
    for bubble in raw_orange_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBublesDict[getReadableBubbleNames(bubble, "Orange")] = raw_orange_alchemyBubblesDict[bubble]
    #print(named_all_alchemyBublesDict)
    for bubble in raw_orange_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBublesDict[getReadableBubbleNames(bubble, "Green")] = raw_green_alchemyBubblesDict[bubble]
    #print(named_all_alchemyBublesDict)
    for bubble in raw_purple_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBublesDict[getReadableBubbleNames(bubble, "Purple")] = raw_purple_alchemyBubblesDict[bubble]
    #print(named_all_alchemyBublesDict)
    for bubble in raw_yellow_alchemyBubblesDict:
        if int(bubble) <= currentlyAvailableBubblesIndex:
            named_all_alchemyBublesDict[getReadableBubbleNames(bubble, "Yellow")] = raw_yellow_alchemyBubblesDict[bubble]
    #print(named_all_alchemyBublesDict)

    #Sum up unlocked bubbles (level > 0)
    for bubble in raw_orange_alchemyBubblesDict:
        if raw_orange_alchemyBubblesDict[bubble] > 0:
            sum_TotalBubblesUnlocked += 1
            orangeBubblesUnlocked += 1
    for bubble in raw_green_alchemyBubblesDict:
        if raw_green_alchemyBubblesDict[bubble] > 0:
            sum_TotalBubblesUnlocked += 1
            greenBubblesUnlocked += 1
    for bubble in raw_purple_alchemyBubblesDict:
        if raw_purple_alchemyBubblesDict[bubble] > 0:
            sum_TotalBubblesUnlocked += 1
            purpleBubblesUnlocked += 1
    for bubble in raw_yellow_alchemyBubblesDict:
        if raw_yellow_alchemyBubblesDict[bubble] > 0:
            sum_TotalBubblesUnlocked += 1
            yellowBubblesUnlocked += 1

    bubbleUnlockListByWorld = ["placeholder",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #this will break if they've unlocked more than 100 bubbles lmao

    #orange
    worldCounter = 1
    while orangeBubblesUnlocked >= 5:
        #print("Alchemy-SamplingBubbles~ ",orangeBubblesUnlocked,worldCounter)
        bubbleUnlockListByWorld[worldCounter] += 5
        orangeBubblesUnlocked -= 5
        worldCounter += 1
    if orangeBubblesUnlocked > 0:
        bubbleUnlockListByWorld[worldCounter] += orangeBubblesUnlocked
        orangeBubblesUnlocked = 0
    #green
    worldCounter = 1
    while greenBubblesUnlocked >= 5:
        bubbleUnlockListByWorld[worldCounter] += 5
        greenBubblesUnlocked -= 5
        worldCounter += 1
    if greenBubblesUnlocked > 0:
        bubbleUnlockListByWorld[worldCounter] += greenBubblesUnlocked
        greenBubblesUnlocked = 0
    #purple
    worldCounter = 1
    while purpleBubblesUnlocked >= 5:
        bubbleUnlockListByWorld[worldCounter] += 5
        purpleBubblesUnlocked -= 5
        worldCounter += 1
    if purpleBubblesUnlocked > 0:
        bubbleUnlockListByWorld[worldCounter] += purpleBubblesUnlocked
        purpleBubblesUnlocked = 0
    #yellow
    worldCounter = 1
    while yellowBubblesUnlocked >= 5:
        bubbleUnlockListByWorld[worldCounter] += 5
        yellowBubblesUnlocked -= 5
        worldCounter += 1
    if yellowBubblesUnlocked > 0:
        bubbleUnlockListByWorld[worldCounter] += yellowBubblesUnlocked
        yellowBubblesUnlocked = 0
    #print(bubbleUnlockListByWorld)
    #print(sum_TotalBubblesUnlocked) #future world's pre-unlocked bubbles inflate this number

    #Clean up memory by deleting the raw dictionaries
    del raw_orange_alchemyBubblesDict
    del raw_green_alchemyBubblesDict
    del raw_purple_alchemyBubblesDict
    del raw_yellow_alchemyBubblesDict

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
        if tier_TotalBubblesUnlocked == (tier[0]-1): #Only check if they already met the previous tier
            if sum_TotalBubblesUnlocked >= tier[1]:
                tier_TotalBubblesUnlocked = tier[0]
            else:
                if tier[1] >= 160:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[8]) + "/20 of W8 bubbles with a final per-bubble cost of 986m per unlock attempt."
                elif tier[1] >= 140:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[7]) + "/20 of W7 bubbles with a final per-bubble cost of 197m per unlock attempt, and " + str(sum_TotalBubblesUnlocked) + "/160 total bubbles up to W8."
                elif tier[1] >= 120:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[6]) + "/20 of W6 bubbles with a final per-bubble cost of 37.3m per unlock attempt, and " + str(sum_TotalBubblesUnlocked) + "/160 total bubbles up to W8."
                elif tier[1] >= 100:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[5]) + "/20 of W5 bubbles, and " + str(sum_TotalBubblesUnlocked) + "/160 total bubbles up to W8."
                elif tier[1] >= 80:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[4]) + "/20 of W4 bubbles."
                elif tier[1] >= 60:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[3]) + "/20 of W3 bubbles."
                elif tier[1] >= 40:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[2]) + "/20 of W2 bubbles."
                else:
                    advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(bubbleUnlockListByWorld[1]) + "/20 of W1 bubbles."

                #advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked) + "- You have unlocked " + str(sum_TotalBubblesUnlocked) + "/" + str(tier[1]) + " of total bubbles. This can go up to 160 if you pre-unlock all the way up to W8 bubbles :o"

        #tier_OrangeSampleBubbles
        all_orangeRequirementsMet = True
        if tier_OrangeSampleBubbles == (tier[0]-1): #Only check if they already met the previous tier
            for requiredBubble in tier[2]:
                #requiredBubble = name of the bubble
                #tier[2][requiredBubble] = level of the bubble in the requirement
                #named_all_alchemyBublesDict[requiredBubble] = level of the player's bubble
                if named_all_alchemyBublesDict[requiredBubble] < tier[2][requiredBubble]:
                    all_orangeRequirementsMet = False
                    advice_OrangeSampleBubbles += requiredBubble + " to " + str(tier[2][requiredBubble]) + "+, "
            if all_orangeRequirementsMet == True:
                tier_OrangeSampleBubbles = tier[0]
            else:
                advice_OrangeSampleBubbles = "Tier " + str(tier_OrangeSampleBubbles) + "- Level the following Orange sample-boosting bubbles to " + progressionTiers[tier_OrangeSampleBubbles+1][6] + " of their maximum possible value: " + advice_OrangeSampleBubbles[:-2]

        #tier_GreenSampleBubbles
        all_greenRequirementsMet = True
        if tier_GreenSampleBubbles == (tier[0]-1): #Only check if they already met the previous tier
            for requiredBubble in tier[3]:
                #requiredBubble = name of the bubble
                #tier[2][requiredBubble] = level of the bubble in the requirement
                #named_all_alchemyBublesDict[requiredBubble] = level of the player's bubble

                if named_all_alchemyBublesDict[requiredBubble] < tier[3][requiredBubble]:
                    all_greenRequirementsMet = False
                    advice_GreenSampleBubbles += requiredBubble + " to " + str(tier[3][requiredBubble]) + "+, "
            if all_greenRequirementsMet == True:
                tier_GreenSampleBubbles = tier[0]
            else:
                advice_GreenSampleBubbles = "Tier " + str(tier_GreenSampleBubbles) + "- Level the following Green sample-boosting bubbles to " + progressionTiers[tier_GreenSampleBubbles+1][6] + " of their maximum possible value: " + advice_GreenSampleBubbles[:-2]

        #tier_PurpleSampleBubbles
        all_purpleRequirementsMet = True
        if tier_PurpleSampleBubbles == (tier[0]-1): #Only check if they already met the previous tier
            for requiredBubble in tier[4]:
                #requiredBubble = name of the bubble
                #tier[3][requiredBubble] = level of the bubble in the requirement
                #named_all_alchemyBublesDict[requiredBubble] = level of the player's bubble
                if named_all_alchemyBublesDict[requiredBubble] < tier[4][requiredBubble]:
                    all_purpleRequirementsMet = False
                    advice_PurpleSampleBubbles += requiredBubble + " to " + str(tier[4][requiredBubble]) + "+, "
            if all_purpleRequirementsMet == True:
                tier_PurpleSampleBubbles = tier[0]
            else:
                advice_PurpleSampleBubbles = "Tier " + str(tier_PurpleSampleBubbles) + "- Level the following Purple sample-boosting bubbles to " + progressionTiers[tier_PurpleSampleBubbles+1][6] + " of their maximum possible value: " + advice_PurpleSampleBubbles[:-2] + ". Purple bubbles are listed first as they are the highest priority due to Log samples being the largest producer of Atom Particles."

        #tier_UtilityBubbles
        all_utilityRequirementsMet = True
        if tier_UtilityBubbles == (tier[0]-1): #Only check if they already met the previous tier
            for requiredBubble in tier[5]:
                #requiredBubble = name of the bubble
                #tier[3][requiredBubble] = level of the bubble in the requirement
                #named_all_alchemyBublesDict[requiredBubble] = level of the player's bubble
                if named_all_alchemyBublesDict[requiredBubble] < tier[5][requiredBubble]:
                    all_utilityRequirementsMet = False
                    advice_UtilityBubbles += requiredBubble + getBubbleColorFromName(requiredBubble) + " to " + str(tier[5][requiredBubble]) + "+, "
            if all_utilityRequirementsMet == True:
                tier_UtilityBubbles = tier[0]
            else:
                advice_UtilityBubbles = "Informational Tier " + str(tier_UtilityBubbles) + "- Level the following Utility bubbles: " + advice_UtilityBubbles[:-2] + ". " + tier[7]
    if advice_UtilityBubbles == "":
        advice_UtilityBubbles = " " + progressionTiers[-1][7]
    overall_alchemyBubblesTier = min(tier_TotalBubblesUnlocked, tier_OrangeSampleBubbles, tier_GreenSampleBubbles, tier_PurpleSampleBubbles) # tier_UtilityBubbles not included
    #Generate advice
    advice_alchemyBubblesCombined = [
        "Best Alchemy-Bubbles tier met: " + str(overall_alchemyBubblesTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Alchemy-Bubbles actions:",
        advice_TotalBubblesUnlocked,
        advice_PurpleSampleBubbles, #Purple highest priority
        advice_OrangeSampleBubbles,
        advice_GreenSampleBubbles,
        advice_UtilityBubbles]
    alchemyBubblesPR = progressionResults.progressionResults(overall_alchemyBubblesTier, advice_alchemyBubblesCombined,"")
    return alchemyBubblesPR

def setAlchemyP2W(inputJSON, playerCount):
    highestAlchemyLevel = getHighestAlchemyLevel(inputJSON, playerCount)
    alchemyP2WList = []
    try:
        alchemyP2WList = json.loads(inputJSON["CauldronP2W"])
    except:
        return ["Unable to retrieve Alchemy-P2W data.", "Unable to retrieve Alchemy-P2W data."]
    bubbleCauldronSum = 0
    liquidCauldronSum = 0
    vialsSum = 0
    playerSum = 0
    p2wSum = 0
    liquidCauldronsUnlocked = 1

    if highestAlchemyLevel >= 120:
        liquidCauldronsUnlocked = 4 #includes Toxic HG
    elif highestAlchemyLevel >= 35:
        liquidCauldronsUnlocked = 3 #includes Trench Seawater
    elif liquidCauldronsUnlocked >= 20:
        liquidCauldronMax = 2 #includes Liquid Nitrogen
    else:
        liquidCauldronsUnlocked = 1 #only Water Droplets

    bubbleCauldronMax = 4*375 #4 cauldrons, 375 upgrades each
    liquidCauldronMax = 180*liquidCauldronsUnlocked
    vialsMax = 15+45 #15 attempts, 45 RNG


    bubbleCauldronSum = sum(alchemyP2WList[0])
    vialsSum = sum(alchemyP2WList[2])
    playerSum = sum(alchemyP2WList[3])
    for liquidEntry in alchemyP2WList[1]: #Liquids are different. Any locked liquid cauldrons are stored as -1 which would throw off a simple sum
        if liquidEntry != -1:
            liquidCauldronSum += liquidEntry


    p2wSum = bubbleCauldronSum + liquidCauldronSum + vialsSum + playerSum
    p2wMax = bubbleCauldronMax + liquidCauldronMax + vialsMax + (highestAlchemyLevel*2)
    print("Alchemy.setAlchemyP2W~ OUTPUT bubbleCauldronSum, liquidCauldronSum, vialsSum, playerSum:",bubbleCauldronSum, liquidCauldronSum, vialsSum, playerSum)
    print("Alchemy.setAlchemyP2W~ OUTPUT p2wSum, p2wMax, p2wTrueMax:",p2wSum, p2wMax)
    advice_alchemyP2WSums = ""
    advice_alchemyP2WBubbleCauldrons = ""
    advice_alchemyP2WLiquidCauldrons = ""
    advice_alchemyP2WVials = ""
    advice_alchemyP2WPlayer = ""
    advice_alchemyP2WCombined = []
    if p2wSum >= p2wMax:
        advice_alchemyP2WSums = "You've purchased all " + str(p2wMax) + " upgrades in Alchemy-P2W! You best <3"
    else:
        advice_alchemyP2WSums = "You've purchased " + str(p2wSum) + "/" + str(p2wMax) + " upgrades in Alchemy P2W. Try to purchase the basic updates before Mid W5, and Player upgrades after each level up!"
        if bubbleCauldronSum < bubbleCauldronMax:
            advice_alchemyP2WBubbleCauldrons += "Bubble Cauldron upgrades: " + str(bubbleCauldronSum) + "/" + str(bubbleCauldronMax)
        if liquidCauldronSum < liquidCauldronMax:
            advice_alchemyP2WLiquidCauldrons += "Liquid Cauldron upgrades: " + str(liquidCauldronSum) + "/" + str(liquidCauldronMax)
        if vialsSum < vialsMax:
            advice_alchemyP2WVials += "Vial upgrades: " + str(vialsSum) + "/" + str(vialsMax)
        if playerSum < highestAlchemyLevel*2:
            advice_alchemyP2WPlayer += "Player upgrades: " + str(playerSum) + "/" + str(highestAlchemyLevel*2)

    advice_alchemyP2WCombined = [advice_alchemyP2WBubbleCauldrons, advice_alchemyP2WLiquidCauldrons, advice_alchemyP2WVials, advice_alchemyP2WPlayer]
    #print(advice_alchemyP2WSums, advice_alchemyP2WCombined)
    return [advice_alchemyP2WSums, advice_alchemyP2WCombined]

