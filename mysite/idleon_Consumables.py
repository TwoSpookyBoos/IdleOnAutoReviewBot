import json

def parseBank(inputJSON):
    consumablesList = []

    #Standard Time Candies: 1hr - 72hr
    guaranteedCandyHours = 0
    guaranteedCandyString = "You have no guaranteed candy in your bank. Wow."
    if 'Timecandy1' in inputJSON["ChestOrder"]:
        TC1Index = inputJSON["ChestOrder"].index('Timecandy1')
        guaranteedCandyHours += 1*(inputJSON["ChestQuantity"][TC1Index])
    if 'Timecandy2' in inputJSON["ChestOrder"]:
        TC2Index = inputJSON["ChestOrder"].index('Timecandy2')
        guaranteedCandyHours += (2*inputJSON["ChestQuantity"][TC2Index])
    if 'Timecandy3' in inputJSON["ChestOrder"]:
        TC3Index = inputJSON["ChestOrder"].index('Timecandy3')
        guaranteedCandyHours += (4*inputJSON["ChestQuantity"][TC3Index])
    if 'Timecandy4' in inputJSON["ChestOrder"]:
        TC4Index = inputJSON["ChestOrder"].index('Timecandy4')
        guaranteedCandyHours += (12*inputJSON["ChestQuantity"][TC4Index])
    if 'Timecandy5' in inputJSON["ChestOrder"]:
        TC5Index = inputJSON["ChestOrder"].index('Timecandy5')
        guaranteedCandyHours += (24*inputJSON["ChestQuantity"][TC5Index])
    if 'Timecandy6' in inputJSON["ChestOrder"]:
        TC6Index = inputJSON["ChestOrder"].index('Timecandy6')
        guaranteedCandyHours += (72*inputJSON["ChestQuantity"][TC6Index])
    if guaranteedCandyHours >= 1000:
        guaranteedCandyString = "You have " + str(guaranteedCandyHours) + " hours (" + "{:.2f}".format(guaranteedCandyHours/24) + " days) of guaranteed candy in your bank. Don't forget about them!"
    elif guaranteedCandyHours != 0:
        guaranteedCandyString = "You have " + str(guaranteedCandyHours) + " hours (" + "{:.2f}".format(guaranteedCandyHours/24) + " days) of guaranteed candy in your bank."

    #Variable Time Candies: Steamy, Spooky, Cosmic
    variableCandyMinutesMin = 0
    variableCandyMinutesMax = 0
    if 'Timecandy7' in inputJSON["ChestOrder"]: #Steamy Time Candy: 10 minutes to 24hr
        TC7Index = inputJSON["ChestOrder"].index('Timecandy7')
        variableCandyMinutesMin += 10*(inputJSON["ChestQuantity"][TC7Index])
        variableCandyMinutesMax += 1440*(inputJSON["ChestQuantity"][TC7Index])
    if 'Timecandy8' in inputJSON["ChestOrder"]: #Spooky Time Candy: 20 minutes to 12hr
        TC8Index = inputJSON["ChestOrder"].index('Timecandy8')
        variableCandyMinutesMin += 20*(inputJSON["ChestQuantity"][TC8Index])
        variableCandyMinutesMax += 720*(inputJSON["ChestQuantity"][TC8Index])
    if 'Timecandy9' in inputJSON["ChestOrder"]: #Cosmic Time Candy: 5hr to 500hr
        TC9Index = inputJSON["ChestOrder"].index('Timecandy9')
        variableCandyMinutesMin += 300*(inputJSON["ChestQuantity"][TC9Index])
        variableCandyMinutesMax += 30000*(inputJSON["ChestQuantity"][TC9Index])
    if variableCandyMinutesMin != 0:
        variableCandyString = ("You have somewhere between " + "{:.2f}".format(variableCandyMinutesMin/60)
            + " - " + "{:.2f}".format(variableCandyMinutesMax/60) + " hours (" + "{:.2f}".format(variableCandyMinutesMin/1440)
            + " - " + "{:.2f}".format(variableCandyMinutesMax/1440) + " days) of variable candy in your bank.")
    else:
        variableCandyString = ""

    #Maybe Black / Divinity Pearls?
    consumablesList = [guaranteedCandyString, variableCandyString]
    #print(guaranteedCandyString)
    #print(variableCandyString)
    return consumablesList

def getBagType(inputBagNumber):
    try:
        inputBagNumber = int(inputBagNumber)
        match inputBagNumber:
            case 0 | 1 | 2 | 3 | 4 | 5 | 7:
                return "Quest"
            case 6 | 100 | 101 | 110:
                return "Dropped"
            case 104 | 105 | 106 | 107 | 108 | 109:
                return "Vendor"
            case 20 | 21 | 22 | 23 | 24 | 25:
                return "GemShop"
    except:
        return "Unknown Bag " + inputBagNumber

def parseInventoryBagsCount(inputJSON, playerCount, playerNames):
    advice_MissingBags = ""
    currentMaxQuestBags = 7 #As of v1.91
    currentMaxDroppedBags = 4 #As of v1.91
    currentMaxCraftedBags = 4 #As of v1.91
    currentMaxVendorBags = 5 #As of v1.91
    currentMaxGemShopBags = 6 #As of v1.91
    currentMaxBagsSum = currentMaxQuestBags + currentMaxDroppedBags + currentMaxCraftedBags + currentMaxVendorBags + currentMaxGemShopBags
    playerBagDict = {}
    playerBagsByTypeDict = {}
    playersWithMaxBags = []
    playersMissingBags = []

    counter = 0
    while counter < playerCount:
        try:
            playerBagDict[playerNames[counter]] = json.loads(inputJSON['InvBagsUsed_'+str(counter)]) #yet another string pretending to be a list of lists..
        except Exception as reason:
            print("Consumables.parseInventoryBagsCount~ EXCEPTION Unable to retrieve Inventory Bags Used for: ", playerNames[counter], "because:", reason)
        counter += 1

    #print(playerBagDict)
    for player, bagList in playerBagDict.items():
        #print(type(player), player)
        #print(type(bagList), bagList)
        questBags = 0
        droppedBags = 0
        vendorBags = 0
        gemshopBags = 0
        sumBags = 0
        for bag in bagList:
            thisBag = getBagType(bag)
            #print(bag, thisBag)
            sumBags += 1
            match thisBag:
                case "Quest":
                    questBags += 1
                case "Dropped":
                    droppedBags += 1
                case "Vendor":
                    vendorBags += 1
                case "GemShop":
                    gemshopBags += 1
        playerBagsByTypeDict[player] = {
            "Quest":questBags,
            "Dropped":droppedBags,
            "Vendor":vendorBags,
            "GemShop":gemshopBags,
            "Total":sumBags
            }
        if sumBags >= currentMaxBagsSum:
            playersWithMaxBags.append(player)
        else:
            playersMissingBags.append(player)
    #print(playerBagsByTypeDict)
    for player in playersMissingBags:
        advice_MissingBags += str(player) + " (" + str(playerBagsByTypeDict[player]['Total']) + "/"+ str(currentMaxBagsSum) + "), "
    if advice_MissingBags != "":
        advice_MissingBags = "Collect more inventory bags: " + advice_MissingBags[:-2]
    #print(advice_MissingBags)
    return advice_MissingBags

###################################################WIP##########################
def parseInventoryBagSlots(inputJSON, playerCount, playerNames):
    advice_MissingBagSlots = ""
    currentMaxInventorySlots = 83 #As of v1.91
    currentMaxUsableInventorySlots = 80 #As of v1.91
    playerBagDict = {}
    playerBagSlotsDict = {}
    playersWithMaxBagSlots = []
    playersMissingBagSlots = []
    w1MeritLevelUnlocked = 0
    w1MeritMaxDict = {
        "1": 1, #Inventory Bag B
        "2": 1, #Inventory Bag C
        "4": 2, #Inventory Bag E
        "5": 2, #Inventory Bag F
        "7": 2  #Inventory Bag H
        }
    w1MeritDict = {}

    #W1 Merit applies bags BCEFH if your 1st character has it
    try:
        w1MeritLevelUnlocked = json.loads(inputJSON["TaskZZ2"])[0][0]
        print("Consumables.parseInventoryBagSlots~ OUTPUT w1MeritLevelUnlocked", w1MeritLevelUnlocked)
    except Exception as reason:
        print("Consumables.parseInventoryBagSlots~ EXCEPTION Unable to retrieve number of levels purchased for W1 Bag Merit: ", reason)
    if w1MeritLevelUnlocked >= 5:
        w1MeritDict = w1MeritMaxDict
    else:
        if w1MeritLevelUnlocked >= 1:
            w1MeritDict["1"] = 1
        if w1MeritLevelUnlocked >= 2:
            w1MeritDict["2"] = 1
        if w1MeritLevelUnlocked >= 3:
            w1MeritDict["4"] = 2
        if w1MeritLevelUnlocked >= 4:
            w1MeritDict["5"] = 2

    counter = 0
    while counter < playerCount:
        try:
            playerBagDict[playerNames[counter]] = json.loads(inputJSON['InvBagsUsed_'+str(counter)]) #yet another string pretending to be a list of lists..
        except Exception as reason:
            print("Consumables.parseInventoryBagSlots~ EXCEPTION Unable to retrieve Inventory Bags Used for: ", playerNames[counter], "because:", reason)
        counter += 1

    #If the merit is purchased, but player1 doesn't have the bag, nobody else gets it :(
    bagsToBeRemoved = []
    #print("Consumables.parseInventoryBagSlots~ OUTPUT w1MeritDict before comparing to Character1", w1MeritDict)
    for key in w1MeritDict:
        if key not in playerBagDict[playerNames[0]]:
            bagsToBeRemoved.append(key)
    for bag in bagsToBeRemoved:
        del w1MeritDict[bag]
    #print("Consumables.parseInventoryBagSlots~ OUTPUT w1MeritDict after comparing to Character1", w1MeritDict)
    for player in playerBagDict:
        playerBagDict[player].update(w1MeritDict)
        #print("Consumables.parseInventoryBagSlots~ INFO w1MeritDict added to playerBagDict for", player, ": ", w1MeritDict)


    for player, bagList in playerBagDict.items():
        sumSlots = 0
        for bag in bagList:
            sumSlots += int(bagList[bag])
        playerBagSlotsDict[player] = {"Total":sumSlots}
        if sumSlots == currentMaxUsableInventorySlots:
            playersWithMaxBagSlots.append(player)
        else:
            playersMissingBagSlots.append(player)
    print("Consumables.parseInventoryBagSlots~ OUTPUT playerBagDict: ", playerBagDict)
    print("Consumables.parseInventoryBagSlots~ OUTPUT playersMissingBagSlots", playersMissingBagSlots)
    for player in playersMissingBagSlots:
        advice_MissingBagSlots += str(player) + " (" + str(playerBagSlotsDict[player]['Total']) + "/"+ str(currentMaxUsableInventorySlots) + "), "
    if advice_MissingBagSlots != "":
        advice_MissingBagSlots = "Collect more inventory slots: " + advice_MissingBagSlots[:-2]
    print("Consumables.parseInventoryBagSlots~ OUTPUT advice_MissingBagSlots", advice_MissingBagSlots)
    return advice_MissingBagSlots
###################################################WIP##########################

def parseStorageChests(inputJSON):
    advice_MissingChests = ""
    currentMaxChestsSum = 44  # As of v2.0
    usedStorageChests = json.loads(inputJSON['InvStorageUsed'])
    #print(len(usedStorageChests), usedStorageChests)
    if len(usedStorageChests) < currentMaxChestsSum:
        advice_MissingChests = "Collect more storage chests: " + str(len(usedStorageChests)) + "/" + str(currentMaxChestsSum)
    return advice_MissingChests

def parseConsumables(inputJSON, playerCount, playerNames):
    bankList = parseBank(inputJSON)
    inventoryBagsList = parseInventoryBagsCount(inputJSON, playerCount, playerNames)
    #inventorySlotsList = parseInventoryBagSlots(inputJSON, playerCount, playerNames)
    storageChestsList = parseStorageChests(inputJSON)
    consumablesList = [bankList, inventoryBagsList, storageChestsList]
    #return bankList #until the other modules are ready, only return the bank list
    return consumablesList