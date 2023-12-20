import json
import idleon_SkillLevels

def getHandsStatus(inputJSON, playerCount, playerNames, fromPublicIEBool):
    skillsToReview_RightHand = ["Mining", "Choppin", "Fishing", "Catching", "Trapping", "Worship"]
    skillsToReview_LeftHand = ["Smithing"]
    handsClasses = [3,4,5,6] #Includes the placeholder numbers after Vman
    handsCharactersDict = {}
    characterClassesList = []
    classCounter = 0
    while classCounter < playerCount:
        characterClassesList.append(idleon_SkillLevels.getHumanReadableClasses(inputJSON['CharacterClass_'+str(classCounter)]))
        if inputJSON['CharacterClass_'+str(classCounter)] in handsClasses:
            if fromPublicIEBool:
                handsCharactersDict[classCounter] = [(playerNames[classCounter] + " the " + idleon_SkillLevels.getHumanReadableClasses(inputJSON['CharacterClass_'+str(classCounter)])), {}, {}]
            else:
                handsCharactersDict[classCounter] = ["Character"+str(classCounter+1) + " the " + idleon_SkillLevels.getHumanReadableClasses(inputJSON['CharacterClass_'+str(classCounter)]), {}, {}]
        classCounter += 1
    #print("MaestroHands.getHandsStatus~ OUTPUT characterClassesList:",characterClassesList)
    #print("MaestroHands.getHandsStatus~ OUTPUT handsCharactersDict:",handsCharactersDict)
    allSkillsDict = idleon_SkillLevels.getAllSkillLevelsDict(inputJSON, playerCount)
    for handsCharacter in handsCharactersDict: #int, the index of the character
        for skill in skillsToReview_LeftHand: #string, the name of the skill
            if allSkillsDict[skill][handsCharacter] < max(allSkillsDict[skill]):
                #print("MaestroHands.getHandsStatus~ INFO Increasing LeftHands counter by 1 for",handsCharactersDict[handsCharacter][0],"because their",skill,"level of",allSkillsDict[skill][handsCharacter],"is less than max of",max(allSkillsDict[skill]))
                handsCharactersDict[handsCharacter][1][skill] = " (" + str(allSkillsDict[skill][handsCharacter]) + "/" + str(max(allSkillsDict[skill])+1) + ")"
        for skill in skillsToReview_RightHand: #string, the name of the skill
            if allSkillsDict[skill][handsCharacter] < max(allSkillsDict[skill]):
                #print("MaestroHands.getHandsStatus~ INFO Increasing RightHands counter by 1 for",handsCharactersDict[handsCharacter][0],"because their",skill,"level of",allSkillsDict[skill][handsCharacter],"is less than max of",max(allSkillsDict[skill]))
                handsCharactersDict[handsCharacter][2][skill] = " (" + str(allSkillsDict[skill][handsCharacter]) + "/" + str(max(allSkillsDict[skill])+1) + ")"
    #print("MaestroHands.getHandsStatus~ OUTPUT handsCharactersDict:",handsCharactersDict)

    advice_LeftHands = []
    leftHandsString = ""
    advice_RightHands = []
    rightHandsString = ""
    for handsCharacter in handsCharactersDict:
        if len(handsCharactersDict[handsCharacter][1]) > 0: #if the character has at least 1 LeftHand skill they aren't first in
            leftHandsString = handsCharactersDict[handsCharacter][0] + " is not the highest level in " + str(len(handsCharactersDict[handsCharacter][1])) + "/" + str(len(skillsToReview_LeftHand)) + " Left Hand skills: "
            for skill in handsCharactersDict[handsCharacter][1]:
                leftHandsString += skill + handsCharactersDict[handsCharacter][1][skill] + ", "
        else:
            leftHandsString = handsCharactersDict[handsCharacter][0] + " is the highest level in all " + str(len(skillsToReview_LeftHand)) + " Left Hand skills! They best <3  "
        leftHandsString = leftHandsString[:-2]
        advice_LeftHands.append(leftHandsString)

        if len(handsCharactersDict[handsCharacter][2]) > 0: #if the character has at least 1 RightHand skill they aren't first in
            rightHandsString = handsCharactersDict[handsCharacter][0] + " is not the highest level in " + str(len(handsCharactersDict[handsCharacter][2])) + "/" + str(len(skillsToReview_RightHand)) + " Right Hand skills: "
            for skill in handsCharactersDict[handsCharacter][2]:
                rightHandsString += skill + handsCharactersDict[handsCharacter][2][skill] + ", "

        else:
            rightHandsString = handsCharactersDict[handsCharacter][0] + " is the highest level in all " + str(len(skillsToReview_RightHand)) + " Right Hand skills! They best <3  "
        rightHandsString = rightHandsString[:-2]
        advice_RightHands.append(rightHandsString)
    #print("MaestroHands.getHandsStatus~ OUTPUT advice_LeftHands:",advice_LeftHands)
    #print("MaestroHands.getHandsStatus~ OUTPUT advice_RightHands:",advice_RightHands)
    if advice_RightHands != []:
        return advice_RightHands
    else:
        return [""]

