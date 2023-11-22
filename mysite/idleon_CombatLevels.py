import progressionResults

def getHumanReadableClasses(classNumber):
    humanReadableClasses = {
        1:"Beginner",
        2:"Journeyman",
        3:"Maestro",
        4:"Voidwalker",
        7:"Warrior",
        8:"Barbarian",
        9:"Squire",
        10:"Blood Berserker",
        12:"Divine Knight",
        19:"Archer",
        20:"Bowman",
        21:"Hunter",
        22:"Siege Breaker",
        25:"Beast Master",
        31:"Mage",
        32:"Wizard",
        33:"Shaman",
        34:"Elemental Sorcerer",
        36:"Bubonic Conjuror",
        }
    try:
        return humanReadableClasses[classNumber]
    except:
        return "Unknown class: " + str(classNumber)

def parseCombatLevelsFromPublicIE(inputJSON, playerCount):
    counter = 0
    sum_AccountLevel = 0
    combatLevels = []
    playerLevels = {}
    playerClasses = {}
    equinoxDict = {}
    equinox3_charactersUnder100 = {}
    equinox11_charactersUnder250 = {}
    equinox23_charactersUnder500= {}
    parsedCombatLevels = {}
    while counter < playerCount: #playerCount is not 0 based
        try:
            combatLevels.append(inputJSON['Lv0_'+str(counter)][0])
            playerLevels[inputJSON["playerNames"][counter]] = (inputJSON['Lv0_'+str(counter)][0])
            playerClasses[inputJSON["playerNames"][counter]] = (inputJSON['CharacterClass_'+str(counter)])
            if (inputJSON['Lv0_'+str(counter)][0]) < 100: #player under level 100, add to all 3
                equinox3_charactersUnder100[inputJSON["playerNames"][counter]] = (inputJSON['Lv0_'+str(counter)][0])
                equinox11_charactersUnder250[inputJSON["playerNames"][counter]] = (inputJSON['Lv0_'+str(counter)][0])
                equinox23_charactersUnder500[inputJSON["playerNames"][counter]] = (inputJSON['Lv0_'+str(counter)][0])
            elif (inputJSON['Lv0_'+str(counter)][0]) < 250: #player under level 250, add to 2
                equinox11_charactersUnder250[inputJSON["playerNames"][counter]] = (inputJSON['Lv0_'+str(counter)][0])
                equinox23_charactersUnder500[inputJSON["playerNames"][counter]] = (inputJSON['Lv0_'+str(counter)][0])
            elif (inputJSON['Lv0_'+str(counter)][0]) < 500: #player under level 500, add to 1
                equinox23_charactersUnder500[inputJSON["playerNames"][counter]] = (inputJSON['Lv0_'+str(counter)][0])
            counter +=1
        except Exception as reason:
            print("CombatLevelsFromIE: Unable to access 'Lv0_" + str(counter) + "' when playerCount = " + str(playerCount), reason)
            counter +=1
    for playerLevel in combatLevels:
        sum_AccountLevel += playerLevel
    equinoxDict['Characters Under 100'] = equinox3_charactersUnder100
    equinoxDict['Characters Under 250'] = equinox11_charactersUnder250
    equinoxDict['Characters Under 500'] = equinox23_charactersUnder500
    #print(sum_AccountLevel, playerLevels)
    parsedCombatLevels['sum_AccountLevel'] = sum_AccountLevel
    parsedCombatLevels['playerLevels'] = playerLevels
    parsedCombatLevels['equinoxDict'] = equinoxDict
    parsedCombatLevels['playerClasses'] = playerClasses
    return parsedCombatLevels

def parseCombatLevelsFromDirectJSON(inputJSON, playerCount):
    counter = 0
    sum_AccountLevel = 0
    combatLevels = []
    playerLevels = {}
    playerClasses = {}
    equinoxDict = {}
    equinox3_charactersUnder100 = {}
    equinox11_charactersUnder250 = {}
    equinox23_charactersUnder500= {}
    parsedCombatLevels = {}
    while counter < playerCount: #playerCount is not 0 based
        try:
            combatLevels.append(inputJSON['Lv0_'+str(counter)][0])
            playerLevels[counter+1] = (inputJSON['Lv0_'+str(counter)][0])
            #playerClasses[inputJSON["playerNames"][counter]] = (inputJSON['CharacterClass_'+str(counter)])
            if (inputJSON['Lv0_'+str(counter)][0]) < 100: #player under level 100, add to all 3
                equinox3_charactersUnder100[counter+1] = (inputJSON['Lv0_'+str(counter)][0])
                equinox11_charactersUnder250[counter+1] = (inputJSON['Lv0_'+str(counter)][0])
                equinox23_charactersUnder500[counter+1] = (inputJSON['Lv0_'+str(counter)][0])
            elif (inputJSON['Lv0_'+str(counter)][0]) < 250: #player under level 250, add to 2
                equinox11_charactersUnder250[counter+1] = (inputJSON['Lv0_'+str(counter)][0])
                equinox23_charactersUnder500[counter+1] = (inputJSON['Lv0_'+str(counter)][0])
            elif (inputJSON['Lv0_'+str(counter)][0]) < 500: #player under level 500, add to 1
                equinox23_charactersUnder500[counter+1] = (inputJSON['Lv0_'+str(counter)][0])
            counter +=1
        except Exception as reason:
            print("CombatLevelsFromJSON: Unable to access 'Lv0_" + str(counter) + "' when playerCount = " + str(playerCount), reason)
            counter +=1
    for playerLevel in combatLevels:
        sum_AccountLevel += playerLevel
    equinoxDict['Characters Under 100'] = equinox3_charactersUnder100
    equinoxDict['Characters Under 250'] = equinox11_charactersUnder250
    equinoxDict['Characters Under 500'] = equinox23_charactersUnder500
    #print(sum_AccountLevel, playerLevels)
    parsedCombatLevels['sum_AccountLevel'] = sum_AccountLevel
    parsedCombatLevels['playerLevels'] = playerLevels
    parsedCombatLevels['equinoxDict'] = equinoxDict
    parsedCombatLevels['playerClasses'] = playerClasses
    return parsedCombatLevels

def setCombatLevelsProgressionTier(inputJSON, progressionTiers, playerCount, fromPublicIEBool):
    if fromPublicIEBool == True:
        parsedCombatLevels = parseCombatLevelsFromPublicIE(inputJSON, playerCount)
    else:
        parsedCombatLevels = parseCombatLevelsFromDirectJSON(inputJSON, playerCount)
    tier_RequiredAccountLevels = 0
    tier_RequiredPersonalLevels = 0
    overall_CombatLevelTier = 0
    advice_AccountLevels = ""
    advice_PersonalLevels = ""
    advice_CombatLevelsCombined = ""
    #Process tiers
    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalAccountLevel
        #tier[2] = str TotalAccountLevel reward
        #tier[3] = int PlayerLevels
        #tier[4] = str PL reward
        #tier[5] = str notes
        if tier_RequiredAccountLevels == (tier[0]-1): #Only check if they already met previous tier
            if parsedCombatLevels['sum_AccountLevel'] >= tier[1]:
                tier_RequiredAccountLevels = tier[0]
            else:
                advice_AccountLevels = "*Current Family level: " + str(parsedCombatLevels['sum_AccountLevel']) + ". Next family reward at " + str(tier[1]) + " unlocks " + tier[2]
    if len(parsedCombatLevels['equinoxDict']['Characters Under 100']) > 0:
        advice_PersonalLevels = "*Level the following characters to 100+ to complete Equinox Dream 3: "
        for character in parsedCombatLevels['equinoxDict']['Characters Under 100']:
            advice_PersonalLevels += str(character) + " (" + str(parsedCombatLevels['equinoxDict']['Characters Under 100'][character]) + "), "
        advice_PersonalLevels = advice_PersonalLevels[:-2] #remove the trailing comma and space
    elif len(parsedCombatLevels['equinoxDict']['Characters Under 250']) > 0:
        advice_PersonalLevels = "*Level the following characters to 250+ to complete Equinox Dream 11 and unlock their Personal Sparkle Obol slot: "
        for character in parsedCombatLevels['equinoxDict']['Characters Under 250']:
            advice_PersonalLevels += str(character) + " (" + str(parsedCombatLevels['equinoxDict']['Characters Under 250'][character]) + "), "
        advice_PersonalLevels = advice_PersonalLevels[:-2] #remove the trailing comma and space
    elif len(parsedCombatLevels['equinoxDict']['Characters Under 500']) > 0:
        advice_PersonalLevels = "*Level the following characters to 500+ to complete Equinox Dream 23: "
        for character in parsedCombatLevels['equinoxDict']['Characters Under 500']:
            advice_PersonalLevels += str(character) + " (" + str(parsedCombatLevels['equinoxDict']['Characters Under 500'][character]) + "), "
        advice_PersonalLevels = advice_PersonalLevels[:-2] #remove the trailing comma and space
    advice_CombatLevelsCombined = [advice_AccountLevels, advice_PersonalLevels]
    #Print fun stuff

    #Generate and return the progressionResults
    overall_CombatLevelTier = min(progressionTiers[-1][-0], tier_RequiredAccountLevels)
    combatLevelsPR = progressionResults.progressionResults(overall_CombatLevelTier, advice_CombatLevelsCombined,"")
    return combatLevelsPR