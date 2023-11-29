import json

def parseBank(inputJSON):
    consumablesList = []

    #Standard Time Candies: 1hr - 72hr
    guaranteedCandyHours = 0
    guaranteedCandyString = " * You have no guaranteed candy in your bank. Wow."
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
        guaranteedCandyString = " * You have " + str(guaranteedCandyHours) + " hours (" + "{:.2f}".format(guaranteedCandyHours/24) + " days) of guaranteed candy in your bank. Don't forget about them!"
    elif guaranteedCandyHours != 0:
        guaranteedCandyString = " * You have " + str(guaranteedCandyHours) + " hours (" + "{:.2f}".format(guaranteedCandyHours/24) + " days) of guaranteed candy in your bank."

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
        variableCandyString = (" * You have somewhere between " + "{:.2f}".format(variableCandyMinutesMin/60)
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
            case 0:
                return "Quest"
            case 1:
                return "Quest"
            case 2:
                return "Quest"
            case 3:
                return "Quest"
            case 4:
                return "Quest"
            case 5:
                return "Quest"
            case 7:
                return "Quest"
            case 6:
                return "Dropped"
            case 100:
                return "Dropped"
            case 101:
                return "Dropped"
            case 110:
                return "Dropped"
            case 104:
                return "Vendor"
            case 105:
                return "Vendor"
            case 106:
                return "Vendor"
            case 107:
                return "Vendor"
            case 108:
                return "Vendor"
            case 109:
                return "Vendor"
            case 20:
                return "GemShop"
            case 21:
                return "GemShop"
            case 22:
                return "GemShop"
            case 23:
                return "GemShop"
            case 24:
                return "GemShop"
            case 25:
                return "GemShop"
    except:
        return ("Unknown Bag " + inputBagNumber)

def parseInventoryBags(inputJSON, playerCount, fromPublicIEBool):
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
    if fromPublicIEBool == True:
        playerNames = inputJSON['playerNames']
        #print("Consumables.parseInventoryBags~",playerNames)
        counter = 0
        while counter < playerCount:
            playerBagDict[playerNames[counter]] = json.loads(inputJSON['InvBagsUsed_'+str(counter)]) #yet another string pretending to be a list of lists..
            counter += 1
    else:
        counter = 0
        while counter < playerCount:
            playerBagDict[counter+1] = json.loads(inputJSON['InvBagsUsed_'+str(counter)]) #yet another string pretending to be a list of lists..
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
        if sumBags == currentMaxBagsSum:
            playersWithMaxBags.append(player)
        else:
            playersMissingBags.append(player)
    #print(playerBagsByTypeDict)
    for player in playersMissingBags:
        advice_MissingBags += str(player) + " (" + str(playerBagsByTypeDict[player]['Total']) + "/"+ str(currentMaxBagsSum) + "), "
    if advice_MissingBags != "":
        advice_MissingBags = " * Collect more inventory bags: " + advice_MissingBags[:-2]
    #print(advice_MissingBags)
    return advice_MissingBags

def parseStorageChests(inputJSON):
    advice_MissingChests = ""
    currentMaxChestsSum = 40
    usedStorageChests = json.loads(inputJSON['InvStorageUsed'])
    #print(len(usedStorageChests), usedStorageChests)
    if len(usedStorageChests) != currentMaxChestsSum:
        advice_MissingChests = " * Collect more storage chests: " + str(len(usedStorageChests)) + "/" + str(currentMaxChestsSum)
    return advice_MissingChests

def parseConsumables(inputJSON, playerCount, fromPublicIEBool):
    bankList = parseBank(inputJSON)
    inventoryBagList = parseInventoryBags(inputJSON, playerCount, fromPublicIEBool)
    storageChestsList = parseStorageChests(inputJSON)
    consumablesList = [bankList, inventoryBagList, storageChestsList]
    #return bankList #until the other modules are ready, only return the bank list
    return consumablesList