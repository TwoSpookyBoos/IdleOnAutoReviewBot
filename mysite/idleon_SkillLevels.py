humanReadableClasses = {
    1: "Beginner",
    2: "Journeyman",
    3: "Maestro",
    4: "Voidwalker",
    5: "Infinilyte",
    6: "Rage Basics",
    7: "Warrior",
    8: "Barbarian",
    9: "Squire",
    10: "Blood Berserker",
    11: "Death Bringer",
    12: "Divine Knight",
    13: "Royal Guardian",
    18: "Calm Basics",
    19: "Archer",
    20: "Bowman",
    21: "Hunter",
    22: "Siege Breaker",
    23: "Mayheim",
    24: "Wind Walker",
    25: "Beast Master",
    30: "Savvy Basics",
    31: "Mage",
    32: "Wizard",
    33: "Shaman",
    34: "Elemental Sorcerer",
    35: "Spiritual Monk",
    36: "Bubonic Conjuror",
    37: "Arcane Cultist"
}


def getHumanReadableClasses(classNumber):
    return humanReadableClasses.get(classNumber, f"Unknown class: {classNumber}")



def getSpecificSkillLevelsList(inputJSON, playerCount, desiredSkill):
    counter = 0
    skillLevelsList = []
    skillIndexList = ["Combat", "Mining", "Smithing", "Choppin", "Fishing", "Alchemy", "Catching", "Trapping",
                      "Construction", "Worship", "Cooking", "Breeding", "Lab", "Sailing", "Divinity", "Gaming",
                      "Farming", "Sneaking", "Summoning"]
    while counter < playerCount:  # playerCount is not 0 based
        if isinstance(desiredSkill, str):
            try:
                skillLevelsList.append(inputJSON['Lv0_' + str(counter)][skillIndexList.index(desiredSkill)])
            except Exception as reason:
                print("SkillLevels.getSpecificSkillLevelsList~ EXCEPTION Unable to access 'Lv0_", counter,
                      "' and desiredSkill=", desiredSkill, " when playerCount= ", playerCount, reason)
        elif isinstance(desiredSkill, int):
            try:
                skillLevelsList.append(inputJSON['Lv0_' + str(counter)][desiredSkill])
            except Exception as reason:
                print("SkillLevels.getSpecificSkillLevelsList~ EXCEPTION Unable to access 'Lv0_", counter,
                      "' and desiredSkill=", desiredSkill, " when playerCount= ", playerCount, reason)
        else:
            print("SkillLevels.getSpecificSkillLevelsList~ EXCEPTION desiredSkill is not a String or Int: ",
                  type(desiredSkill), desiredSkill)
        counter += 1
    return skillLevelsList


def getAllSkillLevelsDict(inputJSON, playerCount):
    characterCounter = 0
    skillCounter = 0

    # setup Dict
    allSkillsDict = {}
    skillIndexList = ["Combat", "Mining", "Smithing", "Choppin", "Fishing", "Alchemy", "Catching", "Trapping",
                      "Construction", "Worship", "Cooking", "Breeding", "Lab", "Sailing", "Divinity", "Gaming",
                      "Farming", "Sneaking", "Summoning"]
    for playerCounter in range(0, playerCount):
        allSkillsDict[playerCounter] = {}
    while skillCounter < len(skillIndexList):
        allSkillsDict[skillIndexList[skillCounter]] = []
        skillCounter += 1
    # print("SkillLevels~ OUTPUT allSkillsDict:",allSkillsDict)

    while characterCounter < playerCount:  # playerCount is not 0 based
        skillCounter = 0
        while skillCounter < len(skillIndexList):
            # print("SkillLevels.getAllSkillLevelsDict~ OUTPUT allSkillsDict[skillIndexList[skillCounter]]",allSkillsDict[skillIndexList[skillCounter]])
            # print("SkillLevels.getAllSkillLevelsDict~ OUTPUT inputJSON['Lv0_'+str(characterCounter)][skillCounter]",inputJSON['Lv0_'+str(characterCounter)][skillCounter])
            try:
                characterSkillLevel = inputJSON['Lv0_' + str(characterCounter)][skillCounter]
                allSkillsDict[characterCounter][skillIndexList[skillCounter]] = characterSkillLevel
                allSkillsDict[skillIndexList[skillCounter]].append(inputJSON['Lv0_' + str(characterCounter)][skillCounter])
            except Exception as reason:
                allSkillsDict[skillIndexList[skillCounter]].append(0)
                print("SkillLevels.getAllSkillLevelsDict~ EXCEPTION Unable to access 'Lv0_", characterCounter,
                      "' and skillIndexList[skillCounter]=", skillIndexList[skillCounter], "when playerCount= ",
                      playerCount, reason)
            skillCounter += 1
        # print("SkillLevels.getAllSkillLevelsDict~ OUTPUT characterCounter increasing from",characterCounter,"to",characterCounter+1)
        characterCounter += 1
    # print("SkillLevels.getAllSkillLevelsDict~ OUTPUT allSkillsDict:",allSkillsDict)
    return allSkillsDict
