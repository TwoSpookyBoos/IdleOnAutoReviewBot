import progressionResults
import idleon_SkillLevels

def parseCombatLevels(inputJSON, playerCount, playerNames):
    counter = 0
    sum_AccountLevel = 0
    combatLevels = idleon_SkillLevels.getSpecificSkillLevelsList(inputJSON, playerCount, "Combat")
    playerLevels = {}
    equinoxDict = {}
    equinox3_charactersUnder100 = {}
    equinox11_charactersUnder250 = {}
    equinox23_charactersUnder500= {}
    parsedCombatLevels = {}

    counter = 0
    for playerLevel in combatLevels:
        if (playerLevel) < 100: #player under level 100, add to all 3
            equinox3_charactersUnder100[playerNames[counter]] = (playerLevel)
            equinox11_charactersUnder250[playerNames[counter]] = (playerLevel)
            equinox23_charactersUnder500[playerNames[counter]] = (playerLevel)
        elif (playerLevel) < 250: #player under level 250, add to 2
            equinox11_charactersUnder250[playerNames[counter]] = (playerLevel)
            equinox23_charactersUnder500[playerNames[counter]] = (playerLevel)
        elif (playerLevel) < 500: #player under level 500, add to 1
            equinox23_charactersUnder500[playerNames[counter]] = (playerLevel)
        sum_AccountLevel += playerLevel
        counter += 1

    equinoxDict['Characters Under 100'] = equinox3_charactersUnder100
    equinoxDict['Characters Under 250'] = equinox11_charactersUnder250
    equinoxDict['Characters Under 500'] = equinox23_charactersUnder500
    #print(sum_AccountLevel, playerLevels)
    parsedCombatLevels['sum_AccountLevel'] = sum_AccountLevel
    parsedCombatLevels['playerLevels'] = playerLevels
    parsedCombatLevels['equinoxDict'] = equinoxDict
    #parsedCombatLevels['playerClasses'] = playerClasses
    return parsedCombatLevels

def setCombatLevelsProgressionTier(inputJSON, progressionTiers, playerCount, playerNames):
    parsedCombatLevels = parseCombatLevels(inputJSON, playerCount, playerNames)
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
                advice_AccountLevels = "Tier " + str(tier_RequiredAccountLevels) + "- Current Family level: " + str(parsedCombatLevels['sum_AccountLevel']) + ". Next family reward at " + str(tier[1]) + " unlocks " + tier[2]
    if len(parsedCombatLevels['equinoxDict']['Characters Under 100']) > 0:
        advice_PersonalLevels = "Level the following characters to 100+ to complete Equinox Dream 3: "
        for character in parsedCombatLevels['equinoxDict']['Characters Under 100']:
            advice_PersonalLevels += str(character) + " (" + str(parsedCombatLevels['equinoxDict']['Characters Under 100'][character]) + "), "
        advice_PersonalLevels = advice_PersonalLevels[:-2] #remove the trailing comma and space
    elif len(parsedCombatLevels['equinoxDict']['Characters Under 250']) > 0:
        advice_PersonalLevels = "Level the following characters to 250+ to complete Equinox Dream 11 and unlock their Personal Sparkle Obol slot: "
        for character in parsedCombatLevels['equinoxDict']['Characters Under 250']:
            advice_PersonalLevels += str(character) + " (" + str(parsedCombatLevels['equinoxDict']['Characters Under 250'][character]) + "), "
        advice_PersonalLevels = advice_PersonalLevels[:-2] #remove the trailing comma and space
    elif len(parsedCombatLevels['equinoxDict']['Characters Under 500']) > 0:
        advice_PersonalLevels = "Level the following characters to 500+ to complete Equinox Dream 23: "
        for character in parsedCombatLevels['equinoxDict']['Characters Under 500']:
            advice_PersonalLevels += str(character) + " (" + str(parsedCombatLevels['equinoxDict']['Characters Under 500'][character]) + "), "
        advice_PersonalLevels = advice_PersonalLevels[:-2] #remove the trailing comma and space
    if advice_AccountLevels == "":
        advice_AccountLevels = "Your total family level is " + str(parsedCombatLevels['sum_AccountLevel']) + ". The last reward was back at 5k. Still... Pretty neat :)"
    advice_CombatLevelsCombined = [advice_AccountLevels, advice_PersonalLevels]
    #Print fun stuff

    #Generate and return the progressionResults
    overall_CombatLevelTier = min(progressionTiers[-1][-0], tier_RequiredAccountLevels)
    combatLevelsPR = progressionResults.progressionResults(overall_CombatLevelTier, advice_CombatLevelsCombined,"")
    return combatLevelsPR