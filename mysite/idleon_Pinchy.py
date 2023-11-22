import json

def setPinchyList(inputJSON, playerCount, dictOfPRs):
    sortedResultsListofLists = [
        [], #[0] = w1/placeholder
        [],[],[], #[1] = early w2, [2] = mid w2, [3] = late w2
        [],[],[], #[4] = early w3, [5] = mid w3, [6] = late w3
        [],[],[], #[7] = early w4, [8] = mid w4, [9] = late w4
        [],[],[], #[10] = early w5, [11] = mid w5, [12] = late w5
        [],[],[], #[13] = Early W6 Prep, [14] = Solid W6 Prep, [15] = w6 waiting room
        [] #[16] = placeholder / max for v1.91
        ]
    progressionNamesList = ["W1", "Early W2", "Mid W2", "Late W2", "Early W3", "Mid W3", "Late W3", "Early W4", "Mid W4", "Late W4", "Early W5", "Mid W5", "Late W5", "Early W6 Prep", "Solid W6 Prep", "W6 Waiting Room", "Max for v1.91"]
    maxWorldTiers = len(sortedResultsListofLists)-1
    maxExpectedIndex = 13 #13 is the highest map evaluated, Tremor Wurms.
    progressionTiersVsWorlds = {
        #[0,0,0,0,0,0,0,0,0,0,0,0,0,99] #template
        "Combat Levels":[0,3,7,8,10,14,15,16,17,18,19,25,28,28,29,30,99],
        "Stamps":[0,2,3,4,5,6,8,9,10,11,13,15,18,25,31,36,99],
        "Bribes":[0,1,1,1,2,2,3,3,3,4,4,4,5,5,5,5,99],
        "Smithing":[0,0,0,0,0,0,1,2,3,4,5,6,6,6,6,6,99],
        "Alchemy-Bubbles":[0,0,1,1,2,2,3,3,4,4,5,5,6,9,12,21,99],
        "Alchemy-Vials":[0,0,0,0,0,0,1,2,3,4,5,6,7,13,16,20,99],
        "Construction Refinery":[0,0,0,0,1,1,1,2,2,3,3,4,5,8,10,16,99],
        "Construction Salt Lick":[0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,10,99],
        "Worship Prayers":[0,0,0,0,0,0,1,1,2,3,4,5,6,6,7,7,99]
        }
    for review in dictOfPRs:
        counter = 0
        prPlaced = False
        while counter < maxWorldTiers:
            if counter == maxWorldTiers-1 and prPlaced == False:
                #counter of 15 vs maxWorldTiers of 16 and still not placed
                if (dictOfPRs[review] >= progressionTiersVsWorlds[review][counter]):
                    #print("Placing",review,"into final tier because",dictOfPRs[review],">=",progressionTiersVsWorlds[review][counter])
                    sortedResultsListofLists[counter+1].append(review)
                else:
                    sortedResultsListofLists[counter].append(review)
            elif (dictOfPRs[review] >= progressionTiersVsWorlds[review][counter]) and (dictOfPRs[review] < progressionTiersVsWorlds[review][counter+1]):
                #print(review, dictOfPRs[review], progressionTiersVsWorlds[review][counter], progressionTiersVsWorlds[review][counter+1])
                sortedResultsListofLists[counter].append(review)
                prPlaced = True
            counter += 1
    #find lowest and highest index with an entry
    lowestIndex = maxWorldTiers
    highestIndex = 0
    counter = 0
    for index in sortedResultsListofLists:
        if len(index) > 0:
            if counter > highestIndex:
                highestIndex = counter
            if counter < lowestIndex:
                lowestIndex = counter
        counter += 1


    #find highest enemy killed or world unlocked to compare to
    #https://idleon.wiki/wiki/Portal_Requirements
    #W2 Sandy Pots = [51][0], starts at 250
    #W2 Mafiosos = [57][0], starts at 1200
    #W2 Tysons = [62][0], starts at 3000
    #W3 Sheepies = [101][0], starts at 1000
    #W3 Mamooths = [106][0], starts at 6000
    #W3 Quenchies = [110][0], starts at 18000
    #W4 Purp Mushroom = [151][0], starts at 5000
    #W4 Soda Can = [155][0], starts at 40000
    #W4 Clammies = [160][0], starts at 190000
    #W5 Suggma = [201][0], starts at 25000
    #W5 Stiltmole = [205][0], starts at 125000
    #W5 Fire Spirit = [210][0], starts at 3000000
    #W5 Tremor Wurms = [213][0], starts at 60000
    expectedIndex = 0
    playerCounter = 0
    while playerCounter < playerCount:
        if expectedIndex < maxExpectedIndex:
            playerKillsList = json.loads(inputJSON['KLA_'+str(playerCounter)]) #String pretending to be a list of lists yet again
            #print(type(playerKillsList), playerKillsList) #Expected to be a list
            if playerKillsList[213][0] < 60000:
                if expectedIndex < 13:
                    expectedIndex = 13
            elif playerKillsList[210][0] < 3000000:
                if expectedIndex < 12:
                    expectedIndex = 12
            elif playerKillsList[205][0] < 125000:
                if expectedIndex < 11:
                    expectedIndex = 11
            elif playerKillsList[201][0] < 25000:
                if expectedIndex < 10:
                    expectedIndex = 10
            elif playerKillsList[160][0] < 190000:
                if expectedIndex < 9:
                    expectedIndex = 9
            elif playerKillsList[155][0] < 40000:
                if expectedIndex < 8:
                    expectedIndex = 8
            elif playerKillsList[151][0] < 5000:
                if expectedIndex < 7:
                    expectedIndex = 7
            elif playerKillsList[110][0] < 18000:
                if expectedIndex < 6:
                    expectedIndex = 6
            elif playerKillsList[106][0] < 6000:
                if expectedIndex < 5:
                    expectedIndex = 5
            elif playerKillsList[101][0] < 1000:
                if expectedIndex < 4:
                    expectedIndex = 4
            elif playerKillsList[62][0] < 3000:
                if expectedIndex < 3:
                    expectedIndex = 3
            elif playerKillsList[57][0] < 1200:
                if expectedIndex < 2:
                    expectedIndex = 2
            elif playerKillsList[51][0] < 250:
                if expectedIndex < 1:
                    expectedIndex = 1
        playerCounter += 1

    #generate advice based on catchup
    if (lowestIndex >= expectedIndex):
        pinchyAdvice = "*Your lowest sections are roughly equal with (or better than!) your highest enemy map. Keep up the good work!"
    elif lowestIndex < highestIndex:
        if len(sortedResultsListofLists[lowestIndex]) == 1:
            pinchyAdvice = "*" + progressionNamesList[lowestIndex] + " rated section: "+ sortedResultsListofLists[lowestIndex][0] + ". You can find detailed advice below in the section's World."
        elif len(sortedResultsListofLists[lowestIndex]) >= 2:
            pinchyAdvice = "*" + progressionNamesList[lowestIndex] + " rated sections: "
            for item in sortedResultsListofLists[lowestIndex]:
                pinchyAdvice += item + ", "
            pinchyAdvice = pinchyAdvice[:-2] + ". You can find detailed advice below in the section's World." #trim off final comma and space
    elif (lowestIndex == highestIndex) and (highestIndex < expectedIndex):
        pinchyAdvice = "*All sections are roughly equal in terms of their expected progression. However, they're still behind based on your highest enemy map reached."

    #print(sortedResultsListofLists)
    #print("Lowest:",lowestIndex," (",progressionNamesList[lowestIndex],"), Highest:",highestIndex," (",progressionNamesList[highestIndex],"), Expected:",expectedIndex," (",progressionNamesList[expectedIndex],")")
    pinchyHeader = "Expected Progression, based on highest enemy map: " + progressionNamesList[expectedIndex] + "."
    pinchyMin = "Minimum Progression, based on weakest ranked review: " + progressionNamesList[lowestIndex] + "."
    #print(pinchyAdvice)
    return [pinchyHeader, pinchyMin, pinchyAdvice]