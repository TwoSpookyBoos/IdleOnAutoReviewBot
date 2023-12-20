import json

def getMissableGStacks(inputJSON, playerCount):
    greenStackAmount = 10000000
    obtainedMissableGStacks = 0
    missedMissableGStacks = 0
    endangeredMissableGStacks = 0
    missableGStacksDict = {
        #template
        #"ItemName":[amount in storage, "SaveData Item Name", "SaveData Quest Name", "Human Readable Quest Name", "Wiki link to the item", "Recommended Class/Farming notes", number of characters will that quest uncompleted]
        #"":[0,"","","","","",0]
        "Dog Bone":             [0,"Quest12",   "Dog_Bone1", "Dog Bone: Why he Die???", "https://idleon.wiki/wiki/Dog_Bone", "Active ES or time candy.", 0],
        "Ketchup Bottle":       [0,"Quest3",    "Picnic_Stowaway2", "Picnic Stowaway: Beating Up Frogs for some Sauce", "https://idleon.wiki/wiki/Ketchup_Bottle", "Active ES or time candy.", 0],
        "Mustard Bottle":       [0,"Quest4",    "Picnic_Stowaway2", "Picnic Stowaway: Beating Up Frogs for some Sauce","https://idleon.wiki/wiki/Mustard_Bottle", "Active ES or time candy.",0],
        "Strange Rock":         [0,"Quest7",    "Stiltzcho2", "Stiltzcho: No Stone Unturned","https://idleon.wiki/wiki/Strange_Rock", "Active ES or time candy.",0],
        "Time Thingy":          [0,"Quest21",   "Funguy3", "Funguy: Partycrastination","https://idleon.wiki/wiki/Time_Thingy", "Active ES or time candy.",0],
        "Employment Statistics":[0,"Quest14",   "TP_Pete2", "TP Pete: The Rats are to Blame!","https://idleon.wiki/wiki/Employment_Statistics", "Active ES or time candy.",0],
        "Corporate Sub":        [0,"Quest22",   "Mutton4", "Mutton: 7 Figure Followers","https://idleon.wiki/wiki/Corporatube_Sub", "Active ES or time candy.",0],
        "Instablab Follower":   [0,"Quest23",   "Mutton4", "Mutton: 7 Figure Followers","https://idleon.wiki/wiki/Instablab_Follower", "Active ES or time candy.",0],
        "Cloudsound Follower":  [0,"Quest24",   "Mutton4", "Mutton: 7 Figure Followers","https://idleon.wiki/wiki/Cloudsound_Follower", "Active ES or time candy.",0],
        "Casual Confidante":    [0,"GoldricP1", "Goldric3", "Goldric: Only Winners have Portraits","https://idleon.wiki/wiki/Casual_Confidante", "Active ES or time candy.",0],
        "Triumphant Treason":   [0,"GoldricP2", "Goldric3", "Goldric: Only Winners have Portraits","https://idleon.wiki/wiki/Triumphant_Treason", "Active ES or time candy.",0],
        "Claiming Cashe":       [0,"GoldricP3", "Goldric3", "Goldric: Only Winners have Portraits","https://idleon.wiki/wiki/Claiming_Cashe", "Active ES or time candy.",0],
        "Monster Rating":       [0,"Quest32",   "XxX_Cattleprod_XxX3", "XxX_Cattleprod_XxX: Ok, NOW it's Peak Gaming!","https://idleon.wiki/wiki/Monster_Rating", "Monster Ratings can drop from Crystal enemies, making Divine Knight the better farmer for Monster Ratings.",0]
        }

    #Missable Quest items for GStacks
    advice_ObtainedQuestGStacks = ""
    advice_MissedQuestGStacks = ""
    advice_EndangeredQuestGStacks = ""
    storageNamesList = ["ChestOrder", "InventoryOrder_0", "InventoryOrder_1", "InventoryOrder_2", "InventoryOrder_3", "InventoryOrder_4", "InventoryOrder_5", "InventoryOrder_6", "InventoryOrder_7", "InventoryOrder_8", "InventoryOrder_9"]
    storageQuantityList = ["ChestQuantity", "ItemQTY_0", "ItemQTY_1", "ItemQTY_2", "ItemQTY_3", "ItemQTY_4", "ItemQTY_5", "ItemQTY_6", "ItemQTY_7", "ItemQTY_8", "ItemQTY_9"]
    if playerCount < 10:
        #print("GreenStacks.getMissableGStacks~ INFO Trimming storageNamesList by",10-playerCount,"because playerCount<10:",playerCount)
        storageNamesList = storageNamesList[:-(10-playerCount)]
        storageQuantityList = storageQuantityList[:-(10-playerCount)]

    for questItem in missableGStacksDict:
        listCounter = 0
        while listCounter < len(storageNamesList):
            try:
                if missableGStacksDict[questItem][1] in inputJSON[storageNamesList[listCounter]]:
                    missableGStacksDict[questItem][0] += inputJSON[storageQuantityList[listCounter]][inputJSON[storageNamesList[listCounter]].index(missableGStacksDict[questItem][1])]
            except Exception as reason:
                print("Greenstacks.getMissableGStacks~ EXCEPTION Unable to look in inputJSON[storageNamesList[listCounter]] while listCounter=",listCounter,"and playerCount=",playerCount,"because:",reason)
            listCounter += 1
        #after totaling up all instances of the quest, if less than a greenstack, see how many characters can still complete this quest
        if missableGStacksDict[questItem][0] < greenStackAmount:
            playerIndex = 0
            while playerIndex < playerCount:
                if missableGStacksDict[questItem][2] in inputJSON["QuestComplete_"+str(playerIndex)]:
                    if json.loads(inputJSON["QuestComplete_"+str(playerIndex)])[missableGStacksDict[questItem][2]] != 1:
                        #print("GreenStacks.getMissableGStacks~ OUTPUT Character",playerIndex+1,"has not completed quest:",missableGStacksDict[questItem][2])
                        missableGStacksDict[questItem][6] += 1
                playerIndex += 1
            if missableGStacksDict[questItem][6] == 0:
                missedMissableGStacks += 1
                advice_MissedQuestGStacks += questItem + ", "
            else:
                endangeredMissableGStacks += 1
                advice_EndangeredQuestGStacks += questItem + " (" + missableGStacksDict[questItem][3] + "), "
        else:
            advice_ObtainedQuestGStacks += questItem + ", "
            obtainedMissableGStacks += 1
    if advice_ObtainedQuestGStacks != "":
        if obtainedMissableGStacks == len(missableGStacksDict):
            advice_ObtainedQuestGStacks = "You have obtained all " + str(len(missableGStacksDict)) + " missable quest item Greensacks! Way to go, you best <3"
        else:
            advice_ObtainedQuestGStacks = "You have obtained " + str(obtainedMissableGStacks) + "/" + str(len(missableGStacksDict)) + " missable quest item Greenstacks: " + advice_ObtainedQuestGStacks[:-2] + "."
    if advice_MissedQuestGStacks != "":
        advice_MissedQuestGStacks = "You have already missed " + str(missedMissableGStacks) + "/" + str(len(missableGStacksDict)) + " missable quest item Greenstacks. You're locked out of these until you get more character slots :( " + advice_MissedQuestGStacks[:-2] + "."
    if advice_EndangeredQuestGStacks != "":
        advice_EndangeredQuestGStacks = "You can still obtain " + str(endangeredMissableGStacks) + "/" + str(len(missableGStacksDict)) + " missable quest item Greenstacks. Be sure not to turn in their quests until GStacking them: " + advice_EndangeredQuestGStacks[:-2] + "."


    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_ObtainedQuestGStacks:", advice_ObtainedQuestGStacks)
    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_EndangeredQuestGStacks:", advice_EndangeredQuestGStacks)
    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_MissedQuestGStacks:", advice_MissedQuestGStacks)
    return [advice_ObtainedQuestGStacks, advice_EndangeredQuestGStacks, advice_MissedQuestGStacks]