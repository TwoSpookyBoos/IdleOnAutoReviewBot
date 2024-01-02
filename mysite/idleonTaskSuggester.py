#idleonTaskSuggester.py
import re
import requests
import json
import datetime

#general.. stuff that makes this file too big if I include directly
import idleon_ProgressionTiers

#general autoreview
import idleon_Pinchy
import idleon_CombatLevels
import idleon_Consumables
import idleon_GemShop
import idleon_Greenstacks
import idleon_MaestroHands

#w1
import idleon_Stamps
import idleon_Bribes
import idleon_Smithing

#w2
import idleon_Alchemy
#import idleon_Obols

#w3
#import idleon_Sampling
import idleon_ConsRefinery
import idleon_ConsSaltLick
import idleon_ConsDeathNote
import idleon_ConsBuildings
import idleon_Worship
import idleon_Trapping

#w4
import idleon_Breeding

#Global variables


#Step 1: Retrieve data from public IdleonEfficiency website or from file
def getJSONfromAPI(url="https://scoli.idleonefficiency.com/raw-data"):
    result = re.search('https://(.*?).idleonefficiency.com', url)
    username = result.group(1)
    username = username.lower()
    #print("Searching for character data from: " + str(url[:-9]))
    if len(username) > 0:
        headers = {
        "Content-Type": "text/json",
        "method": "GET"
        }
    response = requests.get(f"https://cdn2.idleonefficiency.com/profiles/{username.lower()}.json", headers=headers)
    try:
        jsonvalue = response.json()
        parsed = jsonvalue
    except Exception as reason:
        print("idleonTaskSuggester.getJSONfromAPI~ Error retrieving data from IE!", response, reason)
        parsed = []
    #print("parsed is a ", type(parsed))
    return parsed

def getJSONfromText(rawJSON):
    parsed = []
    #print("idleonTaskSuggester.getJSONfromText~ Input type:", type(rawJSON))
    if isinstance(rawJSON, dict): #Console testing
        #Check to see if this is Toolbox JSON
        if "lastUpdated" in rawJSON:
            parsed = rawJSON["data"]
            parsed["charNames"] = rawJSON["charNames"]
            parsed["companion"] = rawJSON["companion"]
            return parsed
        else:
            try:
                jsonString = json.dumps(rawJSON)
                #print("idleonTaskSuggester.getJSONfromText~ Type after json.dumps (expecting str):", type(jsonString))
                parsed = json.loads(jsonString)
                #print("idleonTaskSuggester.getJSONfromText~ Type after json.loads (excepting dict):", type(parsed))
            except Exception as reason:
                print("idleonTaskSuggester.getJSONfromText~ Error parsing JSON data from console input!")
                print("idleonTaskSuggester.getJSONfromText~ Exception reason: ", reason)
                parsed = []
    elif isinstance(rawJSON, str): #Input from the actual website
        #Check to see if this is Toolbox JSON
            if rawJSON.find("lastUpdated") != -1:
                toolboxParsed = json.loads(rawJSON)
                parsed = toolboxParsed["data"]
                parsed["charNames"] = toolboxParsed["charNames"]
                parsed["companion"] = toolboxParsed["companion"]
            else:
                try:
                    parsed = json.loads(rawJSON)
                    #print("idleonTaskSuggester.getJSONfromText~ Type after json.loads (excepting dict):", type(parsed))
                except Exception as reason:
                    print("idleonTaskSuggester.getJSONfromText~ Error parsing JSON data from website input!")
                    print("idleonTaskSuggester.getJSONfromText~ Exception reason: ", reason)
                    parsed = []
    #print("parsed is a ", type(parsed))
    return parsed

def getLastUpdatedTime(inputJSON):
    try:
        timeAwayDict = json.loads(inputJSON['TimeAway'])
        lastUpdatedTimeEpoch = timeAwayDict["GlobalTime"]
        lastUpdatedTimeUTC = datetime.datetime.utcfromtimestamp(lastUpdatedTimeEpoch)#.strftime('%Y-%m-%d %H:%M:%S')
        currentTimeUTC = datetime.datetime.utcnow()
        deltaTime = currentTimeUTC - lastUpdatedTimeUTC
        if deltaTime.days > 0:
            lastUpdatedString = "Save data last updated: " + lastUpdatedTimeUTC.strftime('%Y-%m-%d %H:%M:%S') + " UTC (" + str(deltaTime.days) + " days and " + "{:.1f}".format(deltaTime.seconds/3600) + " hours ago)"
        else:
            lastUpdatedString = "Save data last updated: " + lastUpdatedTimeUTC.strftime('%Y-%m-%d %H:%M:%S') + " UTC (" + "{:.1f}".format(deltaTime.seconds/3600) + " hours ago)"
        #print(lastUpdatedString)
        return lastUpdatedString
    except:
        return "Unable to parse last updated time, sorry :("

def getPlayerCountAndNames(inputJSON):
    playerCount = 0
    playerNames = []
    if "playerNames" in inputJSON.keys():
        #Present in Public IE and JSON copied from IE
        playerNames = inputJSON['playerNames']
        playerCount = len(playerNames)
        print("idleonTaskSuggester.getPlayerCountAndNames~ INFO From Public IE, found " + str(playerCount) + " characters: ", playerNames)
    elif "charNames" in inputJSON.keys():
        #Present in Toolbox JSON copies
        playerNames = inputJSON['charNames']
        playerCount = len(playerNames)
        print("idleonTaskSuggester.getPlayerCountAndNames~ INFO From Toolbox JSON, found " + str(playerCount) + " characters: ", playerNames)
    else:
        try:
            #this produces an unsorted list of names
            cogDataForNames = inputJSON['CogO']
            cogDataList = json.loads(cogDataForNames)
            for item in cogDataList:
                if item.startswith("Player_"):
                    playerCount +=1
                    playerNames.append(item[7:])
            print("idleonTaskSuggester.getPlayerCountAndNames~ INFO From IE JSON or Toolbox Raw Game JSON, found " + str(playerCount) + " characters: ", playerNames)
        except Exception as reason:
            print("idleonTaskSuggester.getPlayerCountAndNames~ EXCEPTION Couldn't load Cog data for this account to get the unsorted list of names. Oh well:", reason)

        #Produce a "sorted" list of generic Character names
        counter = 0
        playerNames = []
        while counter < playerCount:
            playerNames.append("Character"+str(counter+1))
            counter += 1
        #print("idleonTaskSuggester.getPlayerCountAndNames~ INFO Because that playerNames list was unsorted, replacing with generic list for deeper functions to use:", playerNames)

    #print(type(cogDataList))
    #print("Found this many character names:", playerCount)
    return [playerCount, playerNames]

def getRoastableStatus(playerNames):
    roastworthyBool = False
    roastworthyList = ["scoli", "weebgasm", "herusx", "rashaken", "trickzbunny", "redpaaaaanda"]
    for name in playerNames:
        if name.lower() in roastworthyList:
            roastworthyBool = True
    return roastworthyBool

def main(inputData="scoli"):
    bannedAccountsList = ["thedyl", "wooddyl", "3boyy", "4minez", "5arch5", "6knight6", "7maestro7", "bowboy8", "8barb8", "10es10", "favicon.ico", "robots.txt"]
    empty = ""
    emptyList = [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty]
    errorStatement = "Unable to retrieve data for this character name. Please check your spelling and make sure you have uploaded your account publicly."
    errorList = [errorStatement,empty,empty,empty,empty,empty,empty,empty,empty,empty]
    errorListofLists = [[errorList,empty,empty,empty,empty,empty,empty,empty,empty,empty], #general placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w1 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w2 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w3 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w4 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w5 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w6 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w7 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w8 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty] #pinchy placeholder
    ]
    banned = "This account has been banned from lookups."
    bannedList = [banned,empty,empty,empty,empty,empty,empty,empty,empty,empty]
    bannedListofLists = [[bannedList,empty,empty,empty,empty,empty,empty,empty,empty,empty], #general placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w1 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w2 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w3 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w4 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w5 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w6 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w7 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w8 placeholder
    [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty] #pinchy placeholder
    ]

    if isinstance(inputData, str):
        inputData = inputData.strip() #remove leading and trailing whitespaces

    #Step 1: Retrieve data from public IdleonEfficiency website or from file
    if len(inputData) < 16 and isinstance(inputData, str):
        #print("~~~~~~~~~~~~~~~ Starting up PROD main at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "for", inputData, "~~~~~~~~~~~~~~~")
        inputData = inputData.replace(" ", "_") #IE expects underscores instead of spaces in names
        #print("inputData:'" + inputData + "' found in the banned list?", (inputData in bannedAccountsList))
        if inputData.lower() in bannedAccountsList:
            print("idleonTaskSuggester~ PETTY BITCH MODE ACTIVATED. Banned name entered:", inputData)
            return bannedListofLists
        else:
            parsedJSON = getJSONfromAPI("https://" + inputData + ".idleonefficiency.com/raw-data")
            fromPublicIEBool = True
            ieLinkString = "Searching for character data from: https://" + inputData.lower() + ".idleonefficiency.com"
            ieLinkList = ["Searching for character data from: ", "https://" + inputData.lower() + ".idleonefficiency.com"]
    else:
        print("~~~~~~~~~~~~~~~ Starting up PROD main at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "for direct web JSON input.~~~~~~~~~~~~~~~")
        parsedJSON = getJSONfromText(inputData)
        fromPublicIEBool = False
        ieLinkString = "Searching for character data from direct JSON paste. "
        ieLinkList = ["Searching for character data from direct JSON paste. ", ""]
    if parsedJSON == []:
        return errorListofLists
        #raise ValueError(f"data for {inputData} not found")

    #Step 2: Set either Default or Custom progression tiers
    if True == True:
        progressionTiers = idleon_ProgressionTiers.setDefaultTiers()
    else:
        progressionTiers = idleon_ProgressionTiers.setCustomTiers(filename)

    #Step 3: Send that data off to all the different analyzers
    playerCountAndNamesList = getPlayerCountAndNames(parsedJSON)
    playerCount = playerCountAndNamesList[0]
    playerNames = playerCountAndNamesList[1]
    for name in playerNames:
        #print("Checking for name in bannedAccountsList:", name.lower(),  (name.lower() in bannedAccountsList))
        if name.lower() in bannedAccountsList:
            print("idleonTaskSuggester~ WARNING! PETTY BITCH MODE ACTIVATED. Banned name entered:", name)
            return bannedListofLists
    roastworthyBool = getRoastableStatus(playerNames)

    if ieLinkString.endswith("JSON paste. "):
        if playerNames[0] == "Character1":
            ieLinkString += "NO SORTED LIST OF CHARACTER NAMES FOUND IN DATA. REPLACING WITH GENERIC NUMBER ORDER."
            ieLinkList[1] = "NO SORTED LIST OF CHARACTER NAMES FOUND IN DATA. REPLACING WITH GENERIC NUMBER ORDER."
        else:
            ieLinkString += "First character name found: " + playerNames[0]
            ieLinkList[1] = "First character name found: " + playerNames[0]

    #General
    lastUpdatedTimeString = getLastUpdatedTime(parsedJSON)
    print("idleonTaskSuggester.main~ INFO lastUpdatedTimeString", lastUpdatedTimeString)
    combatLevelsPR = idleon_CombatLevels.setCombatLevelsProgressionTier(parsedJSON, progressionTiers['Combat Levels'], playerCount, playerNames)
    consumablesList = idleon_Consumables.parseConsumables(parsedJSON, playerCount, playerNames)
    gemShopPR = idleon_GemShop.setGemShopProgressionTier(parsedJSON, progressionTiers['Gem Shop'], playerCount)
    missableGStacksList = idleon_Greenstacks.getMissableGStacks(parsedJSON, playerCount)
    maestroHandsListOfLists = idleon_MaestroHands.getHandsStatus(parsedJSON, playerCount, playerNames)

    #World 1
    stampPR = idleon_Stamps.setStampProgressionTier(parsedJSON, progressionTiers['Stamps'])
    bribesPR = idleon_Bribes.setBribesProgressionTier(parsedJSON, progressionTiers['Bribes'])
    smithingPR = idleon_Smithing.setSmithingProgressionTier(parsedJSON, progressionTiers['Smithing'], playerCount)

    #World 2
    alchBubblesPR = idleon_Alchemy.setAlchemyBubblesProgressionTier(parsedJSON, progressionTiers['Alchemy Bubbles'])
    alchVialsPR = idleon_Alchemy.setAlchemyVialsProgressionTier(parsedJSON, progressionTiers['Alchemy Vials'])
    alchP2WList = idleon_Alchemy.setAlchemyP2W(parsedJSON, playerCount)
    #obolsPR = idleon_Obols.setObolsProgressionTier(parsedJSON, playerCount, progressionTiers['Obols'], fromPublicIEBool)

    #World 3
    #consPrinterPR =
    consRefineryPR = idleon_ConsRefinery.setConsRefineryProgressionTier(parsedJSON, progressionTiers['Construction Refinery'])
    consSaltLickPR = idleon_ConsSaltLick.setConsSaltLickProgressionTier(parsedJSON, progressionTiers['Construction Salt Lick'])
    consDeathNotePR = idleon_ConsDeathNote.setConsDeathNoteProgressionTier(parsedJSON, progressionTiers['Construction Death Note'], playerCount, playerNames)
    consBuildingsPR = idleon_ConsBuildings.setConsBuildingsProgressionTier(parsedJSON, progressionTiers['Construction Buildings Pre-Buffs'], progressionTiers['Construction Buildings Post-Buffs'], playerCount)
    #consAtomColliderPR =
    #worshipTotemsPR =
    worshipPrayersPR = idleon_Worship.setWorshipPrayersProgressionTier(parsedJSON, progressionTiers['Worship Prayers'])
    trappingPR = idleon_Trapping.setTrappingProgressionTier(parsedJSON, playerCount, playerNames)

    #World 4
    #cookingPR =
    #labPR =
    breedingPR = idleon_Breeding.setBreedingProgressionTier(parsedJSON, progressionTiers['Breeding'])
    #print("## World 5 AutoReview")
    #sailingPR =
    #gamingPR =
    #divinityPR =

    generalList = [[ieLinkString, lastUpdatedTimeString], combatLevelsPR.nTR, consumablesList, gemShopPR.nTR, missableGStacksList, maestroHandsListOfLists] #len(combatLevelsPR.nTR) = 2, len(consumablesList) = 2, len(gemShopPR.nTR) = 5, len(missableGStacksList) = 3, len(maestroHandsList) = 1
    w1list = [stampPR.nTR, bribesPR.nTR, smithingPR.nTR] #len(stampPR) = 4, len(bribesPR.nTR) = 2, len(smithingPR.nTR) = 4
    w2list = [alchBubblesPR.nTR,alchVialsPR.nTR,alchP2WList, emptyList] #len(alchBubblesPR.nTR) = 6, len(alchVialsPR.nTR) = 5
    #w2list = [alchBubblesPR.nTR,alchVialsPR.nTR,alchP2WList, obolsPR.nTR] #len(alchBubblesPR.nTR) = 6, len(alchVialsPR.nTR) = 4, len(obolsPR.nTR) = 4
    w3list = [["Construction 3D Printer coming soon!"], consRefineryPR.nTR, consSaltLickPR.nTR, consDeathNotePR.nTR, #len(consRefineryPR.nTR) = 5, len(consSaltLickPR.nTR) = 2, len(consDeathNotePR.nTR) = 12)
        consBuildingsPR.nTR, ["Construction Atom Collider coming soon!"], ["Worship Totems coming soon!"], worshipPrayersPR.nTR, trappingPR.nTR] #len(consBuildingsPR.nTR) = 8, len(trappingPR.nTR) = 9
    w4list = [breedingPR.nTR, [""], [""]]
    w5list = [[""], [""], [""]]
    #w4list = [["Cooking coming soon!"],["Breeding coming soon!"],["Lab coming soon!"]]
    #w5list = [["Sailing coming soon!"],["Gaming coming soon!"],["Divinity coming soon!"]]
    w6list = [["w6 mechanic 1 placeholder"], ["w6 mechanic 2 placeholder"], ["w6 mechanic 3 placeholder"]]
    w7list = [["w7 mechanic 1 placeholder"], ["w7 mechanic 2 placeholder"], ["w7 mechanic 3 placeholder"]]
    w8list = [["w8 mechanic 1 placeholder"], ["w8 mechanic 2 placeholder"], ["w8 mechanic 3 placeholder"]]
    biggoleProgressionTiersDict = {
        "Combat Levels":combatLevelsPR.cT,
        "Stamps":stampPR.cT,
        "Bribes":bribesPR.cT,
        "Smithing":smithingPR.cT,
        "Alchemy-Bubbles":alchBubblesPR.cT,
        "Alchemy-Vials":alchVialsPR.cT,
        "Construction Refinery":consRefineryPR.cT,
        "Construction Salt Lick":consSaltLickPR.cT,
        "Construction Death Note":consDeathNotePR.cT,
        "Worship Prayers":worshipPrayersPR.cT
        }
    pinchyList = idleon_Pinchy.setPinchyList(parsedJSON, playerCount, biggoleProgressionTiersDict)
    biggoleAdviceList = [generalList, w1list, w2list, w3list, w4list, w5list, w6list, w7list, w8list, pinchyList]
    biggoleAdviceDict = {
        "General": {
            "Pinchy": pinchyList,
            "IE Link": ieLinkList,
            "Last Updated": lastUpdatedTimeString,
            "Combat Levels": combatLevelsPR.nTR,
            "Consumables": consumablesList,
            "Gem Shop": gemShopPR.nTR,
            "Missable Greenstacks": missableGStacksList,
            "Maestro Hands": maestroHandsListOfLists
            },
        "World 1": {
            "Stamps": stampPR.nTR,
            "Bribes": bribesPR.nTR,
            "Smithing": smithingPR.nTR
            },
        "World 2": {
            "Alchemy Bubbles": alchBubblesPR.nTR,
            "Alchemy Vials": alchVialsPR.nTR,
            "Alchemy P2W": alchP2WList,
            #"Obols": emptyList
            },
        "World 3": {
            #"3D Printer": ["Construction 3D Printer coming soon!"],
            "Construction Refinery": consRefineryPR.nTR,
            "Construction Salt Lick": consSaltLickPR.nTR,
            "Construction Death Note": consDeathNotePR.nTR,
            "Construction Buildings": consBuildingsPR.nTR,
            #"Construction Atom Collider": ["Construction Atom Collider coming soon!"],
            #"Worship Totems": ["Worship Totems coming soon!"],
            "Worship Prayers": worshipPrayersPR.nTR,
            "Trapping": trappingPR.nTR},
        "World 4": {
            "Breeding": breedingPR.nTR},
        "World 5": {},
        "World 6": {},
        "World 7": {},
        "World 8": {}
        }

    #print("idleonTaskSuggester.main~ OUTPUT biggoleAdviceList: ", biggoleAdviceList)
    #print("idleonTaskSuggester.main~ OUTPUT biggoleAdviceDict: ", biggoleAdviceDict)
    #print("idleonTaskSuggester.main~ OUTPUT biggoleAdviceDict section: ", biggoleAdviceDict["General"]["IE Link"])
    return biggoleAdviceList