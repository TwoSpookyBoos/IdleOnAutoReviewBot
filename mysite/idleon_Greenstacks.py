import json
import itemDecoder
from math import floor
import itertools

def getEquinoxDreams(inputJSON):
    try:
        rawDreams = json.loads(inputJSON["WeeklyBoss"])
    except Exception as reason:
        print("Greenstacks.getEquinoxDreams~ EXCEPTION Unable to access WeeklyBoss data from JSON:", reason)
    results = {
        "Dream1": False,
        "Dream12": False,
        "Dream29": False
        }
    if "d_0" in rawDreams:
        if rawDreams["d_0"] == -1:
            results["Dream1"] = True
    if "d_11" in rawDreams:
        if rawDreams["d_11"] == -1:
            results["Dream12"] = True
    if "d_28" in rawDreams:
        if rawDreams["d_28"] == -1:
            results["Dream29"] = True
    #print("Greenstacks.getEquinoxDreams~ OUTPUT results:", results)
    return results


def getPlayerItems(inputJSON, playerCount):
    storageNamesList = ["ChestOrder", "InventoryOrder_0", "InventoryOrder_1", "InventoryOrder_2", "InventoryOrder_3", "InventoryOrder_4", "InventoryOrder_5", "InventoryOrder_6", "InventoryOrder_7", "InventoryOrder_8", "InventoryOrder_9"]
    storageQuantityList = ["ChestQuantity", "ItemQTY_0", "ItemQTY_1", "ItemQTY_2", "ItemQTY_3", "ItemQTY_4", "ItemQTY_5", "ItemQTY_6", "ItemQTY_7", "ItemQTY_8", "ItemQTY_9"]
    if playerCount < 10:
        storageNamesList = storageNamesList[:-(10-playerCount)]
        storageQuantityList = storageQuantityList[:-(10-playerCount)]

    playerItemsDict = {}
    for locationIndex in range(0, len(storageNamesList)):
        try:
            locationItemNames = inputJSON[storageNamesList[locationIndex]]
            locationItemQuantities = inputJSON[storageQuantityList[locationIndex]]
        except Exception as reason:
            print("Greenstacks.getPlayerItems~ EXCEPTION Unable to access", storageNamesList[locationIndex], reason)
            locationItemNames = []
        for itemIndex in range(0, len(locationItemNames)):
            if locationItemNames[itemIndex] not in playerItemsDict:
                playerItemsDict[locationItemNames[itemIndex]] = locationItemQuantities[itemIndex]
            else:
                playerItemsDict[locationItemNames[itemIndex]] += locationItemQuantities[itemIndex]

    return playerItemsDict

def getMissableGStacks(inputJSON, playerCount):
    greenStackAmount = 10000000
    obtainedMissableGStacks = 0
    missedMissableGStacks = 0
    endangeredMissableGStacks = 0
    missedList = []
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
        "Corporatube Sub":      [0,"Quest22",   "Mutton4", "Mutton: 7 Figure Followers","https://idleon.wiki/wiki/Corporatube_Sub", "Active ES or time candy.",0],
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
                print("Greenstacks.getMissableGStacks~ EXCEPTION Unable to look in inputJSON[storageNamesList[listCounter]] while listCounter=", listCounter, "and playerCount=", playerCount, "because:", reason)
            listCounter += 1
        #after totaling up all instances of the quest, if less than a greenstack, see how many characters can still complete this quest
        if missableGStacksDict[questItem][0] < greenStackAmount:
            playerIndex = 0
            while playerIndex < playerCount:
                try:
                    if missableGStacksDict[questItem][2] in inputJSON["QuestComplete_"+str(playerIndex)]:
                        if json.loads(inputJSON["QuestComplete_"+str(playerIndex)])[missableGStacksDict[questItem][2]] != 1:
                            #print("GreenStacks.getMissableGStacks~ OUTPUT Character",playerIndex+1,"has not completed quest:",missableGStacksDict[questItem][2])
                            missableGStacksDict[questItem][6] += 1

                except Exception as reason:
                    print("Greenstacks.getMissableGStacks~ EXCEPTION Unable to check if Character", playerIndex+1, "has not completed quest:", missableGStacksDict[questItem][2], "because:", reason)
                playerIndex += 1
            if missableGStacksDict[questItem][6] == 0:
                missedMissableGStacks += 1
                missedList.append(missableGStacksDict[questItem][1])
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

    missedQuestItemsDict = {}
    missedQuestItemsDict["ItemNames"] = missedList
    missedQuestItemsDict["Advice"] = advice_EndangeredQuestGStacks
    return missedQuestItemsDict
    #return [advice_ObtainedQuestGStacks, advice_EndangeredQuestGStacks, advice_MissedQuestGStacks]

def setGStackProgressionTier(inputJSON, playerCount, progressionTiers):
    greenStackAmount = 10000000
    equinoxDreamsStatus = getEquinoxDreams(inputJSON)

    playerCombinedItems = getPlayerItems(inputJSON, playerCount)
    missedQuestItemsDict = getMissableGStacks(inputJSON, playerCount)
    expectedStackables = {
        "Missable Quest Items": [
            "Quest3", "Quest4", "Quest7", "Quest12", "Quest21", "Quest14", "Quest22", "Quest23", "Quest24", "GoldricP1", "GoldricP2", "GoldricP3", "Quest32"
            ],
        "Base Monster Materials": [
            "Grasslands1", "Grasslands2", "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3", "Sewers1", "Sewers2", "TreeInterior1", "TreeInterior2", #W1
            "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4", #W2
            "SnowA1", "SnowA2", "SnowA3", "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4", "SnowA4", "SnowC5", #W3
            "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1",  "GalaxyB2", "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2", "GalaxyC3", "GalaxyC4", #W4
            "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5", "LavaB6",  "LavaC1", "LavaC2", #W5
            "Sewers3", "Quest15", "Hgg" #Specialty Monster Materials
            ],
        "Crystal Enemy Drops": [
            "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1", #W1
            "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2", #W2
            "FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3", #W3
            "FoodPotMana4", "Leaf4", #W4
            "FoodPotYe5", "Leaf5", #W5
            "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14", #Standard statues
            "EquipmentStatues1", "EquipmentStatues5", #Plausible but time consuming
            "rtt0", "StoneZ1", "StoneT1", "StoneW1", "StoneA1" #W1 Slow drops
            ],
        "Printable Skilling Resources": [
            "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", #Tier1 Easy Logs
            "Copper", "Iron", "Gold", "Plat", "Dementia", #Tier1 Slow Ores
            "Fish1", "Fish2", "Fish3", #Tier1 Fish
            "Bug1", "Bug2", #Tier1 Bugs

            "PalmTree", "StumpTree", "SaharanFoal", "Tree7", #Tier1 Slow Logs
            "Void", "Lustre", #Tier1 Slow Ores

            "AlienTree", "Tree8", "Tree9", "Tree11", "Tree10", #Tier2 Logs
            "Starfire", "Marble", "Dreadlo", #Tier2 Ores
            "Fish4", "Fish5", "Fish6", "Fish7", "Fish8", #Tier2 Fish
            "Bug3", "Bug4", "Bug5", "Bug6", "Bug7", "Bug8", #Tier2 Bugs
            "Fish9", "Fish10", "Fish11", "Fish13", "Fish12", #Tier3 Fish
            "Bug9", "Bug11", "Bug10" #Tier3 Bugs
            ],
        "Other Skilling Resources": [
            "CraftMat1", "CraftMat5", "CraftMat6", "CraftMat7", "CraftMat8", "CraftMat9", "CraftMat10", "CraftMat11", #Tier1, 2, and 3 Anvil
            "Critter1", "Critter2", "Critter3", "Soul1", "CopperBar", #Tier3 Critters, Souls, Bars
            "CraftMat12", "CraftMat13", "Critter4", "Critter5", "Critter6", "Soul2", "IronBar", #Tier4 Anvil, Critters, Souls, Bars
            "CraftMat14", "Critter7", "Critter8", "Soul3", "GoldBar", #Tier5 Anvil, Critters, Souls, Bars
             "Critter9", "Critter10", "Soul4", "PlatBar", "FoodMining1", "FoodFish1", "FoodCatch1", #Tier6 Critters, Souls, Bars, and Crafted
            "Soul5", "DementiaBar", "Peanut", #Tier7 Souls, Bars, Crafted
            "Soul6", "VoidBar", "Bullet", "BulletB", #Tier8 Souls, Bars, Crafted
            "LustreBar", "Quest68", #Tier9 Bars, Crafted
            "StarfireBar", "Bullet3", "FoodChoppin1", #Tier10 Bars, Crafted
            "DreadloBar", "EquipmentSmithingTabs2", "Refinery1", #Tier11 Bars, Crafted, Salts
            "Critter1A", "Refinery2", "Critter2A", "Refinery3", "Critter3A", "Critter4A", "Critter5A", "Refinery4", "Critter6A", "Critter7A", "Critter8A", "Critter9A", "Critter10A" #Tier12 Salts, Shiny Critters
            ],
        "Vendor Shops": [
            "FoodHealth14", "FoodHealth15", "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4", "OilBarrel6", "FoodHealth4", "FoodHealth9", "FoodHealth11", "Quest19"
            #"FoodHealth4", "Quest19", #W2
            #"FoodHealth11", "FoodHealth9", "FoodPotGr3", #W3
            #"FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4", #W4
            #"OilBarrel6", "FoodHealth14", "FoodHealth15" #W5 shop
            ],
        "Misc": [
            "FoodPotMana3", "FoodPotGr3", "ButterBar", "FoodPotRe1", "FoodPotRe2",
            ],
        "Cheater": [
            "Refinery5", "Refinery6", #Purple and Nullo Salts
            "OilBarrel1", "OilBarrel2", "OilBarrel3", "OilBarrel4", "OilBarrel5", #Oil Barrels
            "PureWater", "PureWater2", #Alchemy waters
            "Godshard", "GodshardBar" #Unreleased
            "Quest1", "Quest2", "Quest5", "Quest6", "Quest8", "Quest10", "Quest11", "Quest13", "Quest16", "Quest17", "Quest18", "Quest20", "Quest25",
            "Quest26", "Quest27", "Quest28", "Quest29", "Quest30", "Quest31", "Quest33", "Quest34", "Quest36", "Quest37", "Quest38", "Quest39", "Quest40",
            "Quest41", "Quest42", "Quest43", "Quest44", "Quest45", "Quest46", "Quest47", "Quest48", "Quest49", "Quest50",  "Quest9",
            "Mayo", "Trash1", "Trash2", "Trash3",  #Treasure Hunt rewards
            "Meatloaf", "FoodHealth5", "FoodHealth8", "FoodPotYe3", "BobJoePickle", "BallJoePickle",
            "FoodEvent1", "FoodEvent2", "FoodEvent3", "FoodEvent4", "FoodEvent5", "FoodEvent6", "FoodEvent7", "FoodEvent8" #Event Foods
            "Pearl1", "Pearl2", "Pearl3", "Pearl4", "Pearl5", "Pearl6" #Skilling Speed Pearls, EXP pearls
            "ExpBalloon1", "ExpBalloon2", "ExpBalloon3", #Experience Balloons
            "Timecandy1", "Timecandy2", "Timecandy3", "Timecandy4", "Timecandy5", "Timecandy6", "Timecandy7", "Timecandy8", "Timecandy9" #Time Candies
            "Silver Pen", "Ladle", "PetEgg", "Whetstone", "Quest72", "Quest77", "Quest78" #Other Time Skips
            "EquipmentStatues6", "EquipmentStatues15", #Kachow and Bullseye
            "EquipmentStatues8", "EquipmentStatues9", "EquipmentStatues10", "EquipmentStatues11", "EquipmentStatues12", "EquipmentStatues13", #W2 Statues
            "EquipmentStatues16", "EquipmentStatues17", "EquipmentStatues18", "EquipmentStatues19", #W3 Statues
            "EquipmentStatues20", "EquipmentStatues21", "EquipmentStatues22", "EquipmentStatues23", "EquipmentStatues24", "EquipmentStatues25" #W4 and W5 Statues
            ]
        }
    #if len(missedQuestItemsDict["ItemNames"]) > 0:
        #for missedItem in missedQuestItemsDict["ItemNames"]:
           # del expectedStackables["Missable Quest Items"][missedItem]

    remainingToDoGStacksByTier = {}
    for tier in progressionTiers:
        remainingToDoGStacksByTier[tier] = {}

    uniqueGStacksDict = {}
    todoGStacks = {}
    expectedStackablesDecoded = {}
    for category in expectedStackables:
        uniqueGStacksDict[category] = {}
        todoGStacks[category] = {}
        expectedStackablesDecoded[category] = []
        for tier in remainingToDoGStacksByTier:
            remainingToDoGStacksByTier[tier][category] = {}
    uniqueGStacksDict["Unexpected"] = {}
    todoGStacks["Unexpected"] = {}
    remainingToDoGStacksByTier["Unexpected"] = {}

    #Look through the items the player has in their save data.
    for itemCategory in expectedStackables:
        for item in expectedStackables[itemCategory]:
            #If the player's item is one that is expected to be stackble, add it to the uniqueGStacksDict
            if item in playerCombinedItems:
                if playerCombinedItems[item] >= greenStackAmount:
                    uniqueGStacksDict[itemCategory][item] = playerCombinedItems[item]
                else: #Item found, but not gstacked
                    todoGStacks[itemCategory][item] = playerCombinedItems[item]
            else: #Player has 0 of this item, but it is in the expectedStackables
                    todoGStacks[itemCategory][item] = 0

    #Check for items the play has GStacked that I wasn't expecting
    expectedFlatList = []
    for itemCategory in expectedStackables:
        for item in expectedStackables[itemCategory]:
            expectedFlatList.append(item)
    for item in playerCombinedItems:
        if playerCombinedItems[item] >= greenStackAmount and item not in expectedFlatList:
            uniqueGStacksDict["Unexpected"][item] = playerCombinedItems[item]

    #Get count of max expected gstacks
    expectedStackablesCount = 0
    for itemCategory in expectedStackables:
        if len(expectedStackables[itemCategory]) > 0 and itemCategory != "Cheater":
            expectedStackablesCount += len(expectedStackables[itemCategory])

    #Get count allll the counts
    uniqueGStacksCount = 0
    todoGStacksCount = 0
    for itemCategory in uniqueGStacksDict:
        uniqueGStacksCount += len(uniqueGStacksDict[itemCategory])
        todoGStacksCount += len(todoGStacks[itemCategory])

    #print("Greenstacks.getUniqueGStacksInStorage~ Player has finished", uniqueGStacksCount, "out of max possible", expectedStackablesCount, "GStacks")
    if len(uniqueGStacksDict["Unexpected"]) > 0:
        print("Greenstacks.getUniqueGStacksInStorage~ FOUND UNEXPECTED GSTACKS!!", uniqueGStacksDict["Unexpected"])

    #Troubleshooting prints
    #for itemCategory in expectedStackables:
        #for item in range(0, len(expectedStackables[itemCategory])):
            #expectedStackablesDecoded[itemCategory].append(itemDecoder.getItemDisplayName(expectedStackables[itemCategory][item]))
    #print("Greenstacks.getUniqueGStacksInStorage~ Expected Stackables", len(expectedStackables[itemCategory]), itemCategory, expectedStackables[itemCategory])
    #print("Greenstacks.getUniqueGStacksInStorage~ Total Expected Stackables:", expectedStackablesCount)
    #print("Greenstacks.getUniqueGStacksInStorage~ Number of unique greenstacks found:", uniqueGStacksCount)
    #print("Greenstacks.getUniqueGStacksInStorage~ Gstacks:", uniqueGStacksCount, "Ungrouped:", len(uniqueGStacksDict["Unexpected"]), uniqueGStacksDict["Unexpected"], "Cheater:", len(uniqueGStacksDict["Cheater"]), uniqueGStacksDict["Cheater"])
    #print("Greenstacks.getUniqueGStacksInStorage~ Categories in expectedStackables:", expectedStackables.keys())
    #print("Greenstacks.getUniqueGStacksInStorage~ Categories in uniqueGStacksDict: ", uniqueGStacksDict.keys())
    #print("Greenstacks.getUniqueGStacksInStorage~ Categories in todoGStacks:", todoGStacks.keys())
    #print("Greenstacks.getUniqueGStacksInStorage~ Tiers in remainingToDoGStacksByTier:", remainingToDoGStacksByTier.keys())
    #print("Already missed:", missedQuestItemsDict)



    #tiers
    combinedAdvice = {}
    for tier in progressionTiers: #tier = int
        combinedAdvice[tier] = []
        for category in progressionTiers[tier]: #category = string
            #if category in todoGStacks:
            for requiredItem in progressionTiers[tier][category]: #requiredItem = string
                if requiredItem not in missedQuestItemsDict["ItemNames"]:
                    if requiredItem in todoGStacks[category]:
                        #print("Setting remainingToDoGStacksByTier[", category, "][", tier, "][", requiredItem, "] equal to: ", ((todoGStacks[category][requiredItem]/greenStackAmount)*100))
                        remainingToDoGStacksByTier[tier][category][itemDecoder.getItemDisplayName(requiredItem)] = floor((todoGStacks[category][requiredItem]/greenStackAmount)*100) #Display a percentage


    for tier in remainingToDoGStacksByTier:
        #print("Greenstacks.getUniqueGStacksInStorage~ remainingToDoGStacksByTier: Tier ", tier, "- ", remainingToDoGStacksByTier[tier])
        for category in remainingToDoGStacksByTier[tier]:
            if len(remainingToDoGStacksByTier[tier][category]) > 0:
                categoryAdvice = str(category + ": ")
                for item in remainingToDoGStacksByTier[tier][category]:
                    if categoryAdvice.endswith(": "):
                        categoryAdvice += item + " (" + str(remainingToDoGStacksByTier[tier][category][item]) + "%)"
                    elif categoryAdvice.endswith(")"):
                        categoryAdvice += ", " + item + " (" + str(remainingToDoGStacksByTier[tier][category][item]) + "%)"
                if categoryAdvice.endswith(")"):
                    combinedAdvice[tier].append(categoryAdvice)

    tiersToBeDeleted = []
    for tier in combinedAdvice:
        if len(combinedAdvice[tier]) == 0:
            tiersToBeDeleted.append(tier)
    for tier in tiersToBeDeleted:
        #print("Deleting tier", tier, "because it is empty.")
        del combinedAdvice[tier]

    dreamAdvice = "You currently have " + str(uniqueGStacksCount) + " out of max possible " + str(expectedStackablesCount) + " GStacks."
    if uniqueGStacksCount >= 200 or equinoxDreamsStatus["Dream29"] == True:
        dreamAdvice += " You best <3 (until Lava adds further Dream tasks) Other possible targets are still listed below."
        firstAdvice = dict(itertools.islice(combinedAdvice.items(), 3))
    elif uniqueGStacksCount >= 75 or equinoxDreamsStatus["Dream12"] == True:
        dreamAdvice += " Equinox Dream 29 requires 200. Aim for items up through Tier 10! There are a few extras included for flexibility."
        firstAdvice = dict(itertools.islice(combinedAdvice.items(), 3))
    elif uniqueGStacksCount >= 20 or equinoxDreamsStatus["Dream1"] == True:
        dreamAdvice += " Equinox Dream 12 requires 75. Aim for items up through Tier 2! There are a few extras included for flexibility."
        firstAdvice = dict(itertools.islice(combinedAdvice.items(), 2))
    elif uniqueGStacksCount < 20 and equinoxDreamsStatus["Dream1"] == False:
        dreamAdvice += " Equinox Dream 1 requires 20. Aim for items in Tier 1! There are a few extras included for flexibility."
        firstAdvice = dict(itertools.islice(combinedAdvice.items(), 1))

    #print("Dream Advice:", dreamAdvice)
    #for tier in first3Advice:
        #if tier != "":
            #print("GStack Advice:", tier, first3Advice[tier])

    return [dreamAdvice, missedQuestItemsDict["Advice"], firstAdvice]