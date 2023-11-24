import progressionResults

#Stamp p1
def setStampLevels(inputJSON, inputIndex):
    totalStampLevels = 0
    totalStampLevels -= inputJSON["StampLv"][inputIndex]['length']
    for stamp in inputJSON["StampLv"][inputIndex].values():
        totalStampLevels += int(stamp)
    return totalStampLevels

#Stamp p2
def setMissingStamps(inputJSON, inputIndex):
    missingStamps = []
    for stamp, value in inputJSON["StampLvM"][inputIndex].items():
        if value == 0:
            missingStamps.append(stamp)
    return missingStamps

#Stamp p3
def setPriorityStamps(inputJSON):
    priorityStampsDict = {
        #'Golden Sixes' : inputJSON["StampLv"][0]['37'],
        'Pickaxe' : inputJSON["StampLv"][1]['0'],
        'Hatchet' : inputJSON["StampLv"][1]['1'],
        'Matty Bag' : inputJSON["StampLv"][1]['7'],
        'Drippy Drop' : inputJSON["StampLv"][1]['14'],
        'Bag o Heads' : inputJSON["StampLv"][1]['20'],
        'Bugsack' : inputJSON["StampLv"][1]['22'],
        'Ladle' : inputJSON["StampLv"][1]['38'],
        'Multitool' : inputJSON["StampLv"][1]['45'],
        'Mason Jar' : inputJSON["StampLv"][2]['1'],
        'Crystallin' : inputJSON["StampLv"][2]['2'],
        'Golden Apple' : inputJSON["StampLv"][2]['6'],
        'Card' : inputJSON["StampLv"][2]['8']
        }
    try:
        priorityStampsDict['Golden Sixes'] = inputJSON["StampLv"][0]['37']
    except:
        priorityStampsDict['Golden Sixes'] = 0
    try:
        priorityStampsDict['Stat Wallstreet'] = inputJSON["StampLv"][0]['37']
    except:
        priorityStampsDict['Stat Wallstreet'] = 0
    try:
        priorityStampsDict['Skelefish'] = inputJSON["StampLv"][1]['37']
    except:
        priorityStampsDict['Skelefish'] = 0
    return priorityStampsDict

#Stamp p4
def getReadableStampName(stampNumber, stampType):
    #print("Fetching name for " + stampType + " stamp: " + stampNumber)
    match stampType:
        case "Combat":
            match stampNumber:
                case 0:
                    return "Sword Stamp"
                case 1:
                    return "Heart Stamp"
                case 2:
                    return "Mana Stamp"
                case 3:
                    return "Tomahawk Stamp"
                case 4:
                    return "Target Stamp"
                case 5:
                    return "Shield Stamp"
                case 6:
                    return "Longsword Stamp"
                case 7:
                    return "Kapow Stamp"
                case 8:
                    return "Fist Stamp"
                case 9:
                    return "Battleaxe Stamp"
                case 10:
                    return "Agile Stamp"
                case 11:
                    return "Vitality Stamp"
                case 12:
                    return "Book Stamp"
                case 13:
                    return "Manamoar Stamp"
                case 14:
                    return "Clover Stamp"
                case 15:
                    return "Scimitar Stamp"
                case 16:
                    return "Bullseye Stamp"
                case 17:
                    return "Feather Stamp"
                case 18:
                    return "Polearm Stamp"
                case 19:
                    return "Violence Stamp"
                case 20:
                    return "Buckler Stamp"
                case 21:
                    return "Hermes Stamp"
                case 22:
                    return "Sukka Foo"
                case 23:
                    return "Arcane Stamp"
                case 24:
                    return "Avast Yar Stamp"
                case 25:
                    return "Steve Sword"
                case 26:
                    return "Blover Stamp"
                case 27:
                    return "Stat Graph Stamp"
                case 28:
                    return "Gilded Axe Stamp"
                case 29:
                    return "Diamond Axe Stamp"
                case 30:
                    return "Tripleshot Stamp"
                case 31:
                    return "Blackheart Stamp"
                case 32:
                    return "Maxo Slappo Stamp"
                case 33:
                    return "Sashe Sidestamp"
                case 34:
                    return "Intellectostampo"
                case 35:
                    return "Conjocharmo Stamp"
                case 36:
                    return "Dementia Sword Stamp"
                case 37:
                    return "Golden Sixes Stamp"
                case 38:
                    return "Stat Wallstreet Stamp"
                case _:
                    return ("Unknown Combat stamp: " + str(stampNumber))
        case "Skill":
            match stampNumber:
                case 0:
                    return "Pickaxe Stamp"
                case 1:
                    return "Hatchet Stamp"
                case 2:
                    return  "Anvil Zoomer Stamp"
                case 3:
                    return "Lil' Mining Baggy Stamp"
                case 4:
                    return "Twin Ores Stamp"
                case 5:
                    return "Choppin' Bag Stamp"
                case 6:
                    return "Duplogs Stamp"
                case 7:
                    return "Matty Bag Stamp"
                case 8:
                    return "Smart Dirt Stamp"
                case 9:
                    return "Cool Diggy Tool Stamp"
                case 10:
                    return "High IQ Lumber Stamp"
                case 11:
                    return "Swag Swingy Tool Stamp"
                case 12:
                    return "Alch Go Brrr Stamp"
                case 13:
                    return "Brainstew Stamp"
                case 14:
                    return "Drippy Drop Stamp"
                case 15:
                    return "Droplots Stamp"
                case 16:
                    return "Fishing Rod Stamp"
                case 17:
                    return "Fishhead Stamp"
                case 18:
                    return "Catch Net Stamp"
                case 19:
                    return "Fly Intel Stamp"
                case 20:
                    return "Bag o Heads Stamp"
                case 21:
                    return "Holy Mackerel Stamp"
                case 22:
                    return "Bugsack Stamp"
                case 23:
                    return "Buzz Buzz Stamp"
                case 24:
                    return "Hidey Box Stamp"
                case 25:
                    return "Purp Froge Stamp"
                case 26:
                    return "Spikemouth Stamp"
                case 27:
                    return "Shiny Crab Stamp"
                case 28:
                    return "Gear Stamp"
                case 29:
                    return "Stample Stamp"
                case 30:
                    return "Saw Stamp"
                case 31:
                    return "Amplestample Stamp"
                case 32:
                    return "SpoOoky Stamp"
                case 33:
                    return "Flowin Stamp"
                case 34:
                    return "Prayday Stamp"
                case 35:
                    return "Banked Pts Stamp"
                case 36:
                    return "Cooked Meal Stamp"
                case 37:
                    return "Spice Stamp"
                case 38:
                    return "Ladle Stamp"
                case 39:
                    return "Nest Eggs Stamp"
                case 40:
                    return "Egg Stamp"
                case 41:
                    return "Lab Tube Stamp"
                case 42:
                    return "Sailboat Stamp"
                case 43:
                    return "Gamejoy Stamp"
                case 44:
                    return "Divine Stamp"
                case 45:
                    return "Multitool Stamp"
                case 46:
                    return "Skelefish Stamp"
                case _:
                    return ("Unknown Skill stamp: " + str(stampNumber))
        case "Misc":
            match stampNumber:
                case 0:
                    return "Questin Stamp"
                case 1:
                    return "Mason Jar Stamp"
                case 2:
                    return  "Crystallin"
                case 3:
                    return "Arcade Ball Stamp"
                case 4:
                    return "Gold Ball Stamp"
                case 5:
                    return "Potion Stamp"
                case 6:
                    return "Golden Apple Stamp"
                case 7:
                    return "Ball Timer Stamp"
                case 8:
                    return "Card Stamp"
                #case 9:
                #    return "Blue Hatchet Stamp"
                #case 10:
                #    return "Red Sword Stamp"
                #case 11:
                #    return "Blue Sword Stamp"
                case 12:
                    return "Talent I Stamp"
                case 13:
                    return "Talent II Stamp"
                case 14:
                    return "Talent III Stamp"
                case 15:
                    return "Talent IV Stamp"
                case 16:
                    return "Talent V Stamp"
                case 17:
                    return "Talent S Stamp"
                case 18:
                    return "Multikill Stamp"
                case 19:
                    return "Biblio Stamp"
                case 20:
                    return "DNA Stamp"
                case 21:
                    return "Refinery Stamp"
                case _:
                    return ("Unknown Misc stamp: " + str(stampNumber))

#Stamp meta
def setStampProgressionTier(inputJSON, progressionTiers):
    totalCombatStampLevels = setStampLevels(inputJSON, 0)
    totalSkillStampLevels = setStampLevels(inputJSON, 1)
    totalMiscStampLevels = setStampLevels(inputJSON, 2)
    totalAllStampLevels = totalCombatStampLevels + totalSkillStampLevels + totalMiscStampLevels
    missingCombatStamps = setMissingStamps(inputJSON, 0)
    missingSkillStamps = setMissingStamps(inputJSON, 1)
    missingMiscStamps = setMissingStamps(inputJSON, 2)
    playerPriorityStamps = setPriorityStamps(inputJSON)
    tier_StampLevels = 0
    tier_RequiredCombatStamps = 0
    tier_RequiredSkillStamps = 0
    tier_RequiredMiscStamps = 0
    tier_RequiredSpecificStamps = 0
    advice_StampLevels = ""
    advice_CollectStamps = ""
    advice_SpecificStamps = ""
    advice_CombinedStamps = ""
    for tier in progressionTiers:
        #TotalLevelStamps
        if tier_StampLevels == (tier[0]-1):
            if totalAllStampLevels >= tier[1]: #int
                tier_StampLevels = tier[0]
            else:
                advice_StampLevels = tier[1]
        #CombatStamps
        if tier_RequiredCombatStamps == (tier[0]-1): #Only check if they already met previous tier
            allCombatStamps = True
            splitRequiredCombatStamps = tier[2].split(",") #string of numbers, no spaces
            for rStamp in splitRequiredCombatStamps:
                #print(rStamp, missingCombatStamps, (rStamp in missingCombatStamps))
                if rStamp in missingCombatStamps:
                    allCombatStamps = False
                    advice_CollectStamps += (getReadableStampName(int(rStamp), "Combat") + ", ")
            if  allCombatStamps == True:
                tier_RequiredCombatStamps = tier[0]
        #SkillStamps
        if tier_RequiredSkillStamps == (tier[0]-1): #Only check if they already met previous tier
            allSkillStamps = True
            splitRequiredSkillStamps = tier[3].split(",") #string of numbers, no spaces
            for rStamp in splitRequiredSkillStamps:
                #print(rStamp, missingSkillStamps, (rStamp in missingSkillStamps))
                if rStamp in missingSkillStamps:
                    allSkillStamps = False
                    advice_CollectStamps += (getReadableStampName(int(rStamp), "Skill") + ", ")
            if  allSkillStamps == True:
                tier_RequiredSkillStamps = tier[0]
        #MiscStamps
        if tier_RequiredMiscStamps == (tier[0]-1): #Only check if they already met previous tier
            allMiscStamps = True
            splitRequiredMiscStamps = tier[4].split(",") #string of numbers, no spaces
            for rStamp in splitRequiredMiscStamps:
                if rStamp in missingMiscStamps:
                    allMiscStamps = False
                    advice_CollectStamps += (getReadableStampName(int(rStamp), "Misc") + ", ")
            if allMiscStamps == True:
                    tier_RequiredMiscStamps = tier[0]
        #SpecificStampLevels
        if tier_RequiredSpecificStamps == (tier[0]-1): #Only check if they already met previous tier
            requiredSpecificStamps = tier[5] #dictionary
            allSpecificStamps = True
            for key, value in requiredSpecificStamps.items():
                #print(tier[0], playerPriorityStamps[key], requiredSpecificStamps[key], playerPriorityStamps[key] >= requiredSpecificStamps[key])
                if playerPriorityStamps[key] < requiredSpecificStamps[key]:
                    allSpecificStamps = False
                    advice_SpecificStamps += (str(key) + " to " + str(value) + "+, ")
            if allSpecificStamps == True:
                tier_RequiredSpecificStamps = tier[0]
    overall_StampTier = min(tier_StampLevels, tier_RequiredCombatStamps, tier_RequiredSkillStamps, tier_RequiredMiscStamps, tier_RequiredSpecificStamps)
    #Generate advice statement
    if advice_StampLevels != "":
        advice_StampLevels = ("*Improve your total stamp levels to " + str(advice_StampLevels) + "+")
    if advice_CollectStamps != "":
        advice_CollectStamps = ("*Collect the following stamp(s): " + str(advice_CollectStamps[:-2]))
    if advice_SpecificStamps != "":
        advice_SpecificStamps = ("*Improve these high-priority stamp(s): "+ str(advice_SpecificStamps[:-2]))
    #Print out all the final stamp info
    #print("Stamp levels: "
    #    + str(totalCombatStampLevels) + ", "
    #    + str(totalSkillStampLevels) + ", "
    #    + str(totalMiscStampLevels) + ", "
    #    + str(totalAllStampLevels) + " total.")
    #print("Missing combat stamps: " + str(missingCombatStamps))
    #print("Missing skill stamps: " + str(missingSkillStamps))
    #print("Missing misc stamps: " + str(missingMiscStamps))
    #print("Tier of total stamp levels: " + str(tier_StampLevels))
    #print("Tier of required combat stamps: " + str(tier_RequiredCombatStamps))
    #print("Tier of required skill stamps: " + str(tier_RequiredSkillStamps))
    #print("Tier of required misc stamps: " + str(tier_RequiredMiscStamps))
    #print("Tier of required specific stamps: " + str(tier_RequiredSpecificStamps))
    #print (tier_StampLevels, tier_RequiredCombatStamps, tier_RequiredSkillStamps, tier_RequiredMiscStamps, tier_RequiredSpecificStamps, overall_StampTier)
    if advice_StampLevels == "" and advice_CollectStamps == "" and advice_SpecificStamps == "":
        advice_CombinedStamps = [
            "Best Stamp tier met: " + str(overall_StampTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended stamp actions:", "", "", "*You've reached the end of the recommendations. Let me know what important stamps you're aiming for next!"]
    else:
        advice_CombinedStamps = [
            "Best Stamp tier met: " + str(overall_StampTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended stamp actions:",
            advice_StampLevels,
            advice_CollectStamps,
            advice_SpecificStamps]
    #print(advice_CombinedStamps)
    stampPR = progressionResults.progressionResults(overall_StampTier, advice_CombinedStamps, "")
    return stampPR