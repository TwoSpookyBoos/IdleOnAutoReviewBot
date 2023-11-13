import re
import requests
import json
#general
import progressionResults
import idleon_CombatLevels
import idleon_Consumables
#w1
import idleon_Stamps
import idleon_Bribes
import idleon_Smithing
#w2
import idleon_Alchemy
#w3
import idleon_ConsRefinery
import idleon_ConsSaltLick

#Global variables


#Step 1: Retrieve data from public IdleonEfficiency website or from file
def getJSONfromAPI(url="https://scoli.idleonefficiency.com/raw-data"):
    result = re.search('https://(.*?).idleonefficiency.com', url)
    username = result.group(1)
    username = username.lower()
    print("Searching for character data from: " + str(url[:-9]))
    if len(username) > 0:
        headers = {
        "Content-Type": "text/json",
        "method": "GET"
        }
    response = requests.get(f"https://cdn.idleonefficiency.com/profiles/{username.lower()}.json", headers=headers)
    try:
        jsonvalue = response.json()
        parsed = jsonvalue
    except Exception as reason:
        print("Error retrieving data from IE!")
        print(response, reason)
        parsed = []
    return parsed

def getJSONfromFILE(filename="jsonimport.json"):
  with open(filename,'r') as f:
    parsed = json.load(f)
  #print(parsed)
  return parsed

#Step 2: Set either Default or Custom progression tiers
def setDefaultTiers():
    defaultTiers = {}
    defaultTiers['Bribes'] = [
        #int tier, int w1purchased, int w2purchased, int w3purchased, int w4purchased, int trashIslandpurchased, str notes
        [0, 0, 0, 0, 0, 0, ""],
        [1, 6, 0, 0, 0, 0, "by end of W1."],
        [2, 6, 7, 0, 0, 0, "by end of W2."],
        [3, 6, 7, 7, 0, 0, "by end of W3."],
        [4, 6, 7, 7, 6, 0, "by end of W4."],
        [5, 6, 7, 7, 6, 7, "by end of W5, after unlocking the Bribe from Trash Island."], #The 8th bribe in w5 can't be purchased yet
        ]
    defaultTiers['Stamps'] = [
        #int Tier, int Total Stamp Level, str Required combat stamps, str Required Skill stamps, str Required Misc stamps, dict Specific stamp levels, str Notes
        [0, 0, "", "", "", {}, "Just level up any stamp you can afford!"],
        [1, 50, "", "", "", {}, "Just level up any stamp you can afford!"],
        [2, 100, "", "", "", {}, "Just level up any stamp you can afford!"],
        [3, 150, "2,3,4,5,11", "2,5", "", {}, "W1 town and W1 Tiki shop both sell stamps!"],
        [4, 200, "13,14", "3,16,18", "17", {}, "Expected progression roughly near the end of World 2. Some of these required stamps are drops from enemies or quest rewards. Use the Wiki to find their sources!"],
        [5, 250, "7,9,16", "7,14,15", "0", {'Pickaxe':25,'Hatchet':25}, ""],
        [6, 300, "17,18,20", "4,6,25", "5", {}, ""],
        [7, 400, "10,12,19", "8,9", "", {'Pickaxe':35,'Hatchet':35}, ""],
        [8, 500, "15,21", "10,17,23", "14,19", {'Drippy Drop':30}, ""],
        [9, 600, "27", "11,24,26", "1,2", {'Mason Jar':12}, ""],
        [10, 700, "22,26", "12,20,22", "18", {'Drippy Drop':40,'Matty Bag':50}, ""],
        [11, 800, "28,30", "29,30,37,40", "", {'Pickaxe':45,'Hatchet':45,'Mason Jar':24,}, ""],
        [12, 900, "23,24", "13,46", "8", {'Drippy Drop':50}, ""],
        [13, 1000, "31", "19,21,36", "13", {'Pickaxe':55,'Hatchet':55,'Card':50}, ""],
        [14, 1500, "", "33,35,39", "21", {'Matty Bag':100,'Crystallin':60}, ""],
        [15, 2000, "25,29", "41", "6,20", {'Pickaxe':65,'Hatchet':65,'Card':100}, ""],
        [16, 2500, "32,33,34", "38,42", "15", {'Golden Apple':28}, ""],
        [17, 3000, "36", "43,44,45", "", {'Bugsack':80,'Bag o Heads':80},  ""],
        [18, 3500, "", "", "", {'Pickaxe':75,'Hatchet':75,'Drippy Drop':90,'Crystallin':100}, ""],
        [19, 4000, "", "", "", {'Matty Bag':150}, ""],
        [20, 4500, "", "", "", {'Card':150,'Ladle':100}, ""],
        [21, 5000, "", "", "", {'Pickaxe':85,'Hatchet':85,'Mason Jar':52,'Golden Apple':40}, ""],
        [22, 5500, "", "", "", {'Bugsack':120,'Bag o Heads':120}, ""],
        [23, 6000, "35", "", "", {'Matty Bag':200,'Crystallin':150}, ""],
        [24, 6500, "", "", "", {'Drippy Drop':100,'Ladle':150}, ""],
        [25, 7000, "", "", "", {'Pickaxe':95,'Hatchet':95,'Golden Apple':60,'Multitool':100}, ""],
        [26, 7500, "", "", "", {'Ladle':200}, ""],
        [27, 8000, "", "", "", {'Matty Bag':280,'Multitool':150}, ""],
        [28, 8500, "", "", "", {'Pickaxe':105,'Hatchet':105,'Mason Jar':88,'Crystallin':200,'Bugsack':152,'Bag o Heads':152,}, ""],
        [29, 9000, "", "", "", {'Drippy Drop':110,'Matty Bag':310}, ""],
        [30, 9500, "", "", "", {'Card':200,'Crystallin':250}, ""],
        [31, 10000, "", "", "", {'Golden Apple':80}, "Guaranteed daily Gilded Stamp at 10k"],
        [32, 10000, "", "", "", {'Mason Jar':124}, ""],
        [33, 10000, "", "", "", {'Bugsack':184,'Bag o Heads':184}, ""],
        [34, 10000, "", "", "", {'Golden Apple':100,'Multitool':210}, ""],
        [35, 10000, "37", "", "", {'Golden Sixes':170}, ""],
        [36, 10000, "38", "31", "", {'Golden Sixes':190}, ""]
        ]
    defaultTiers['Smithing'] = [
        #int tier, int Cash Points Purchased, int Monster Points Purchased, int Forge Totals, str Notes
        [0,0,0,0,""],
        [1,100,85,60,"all W1 enemies."],
        [2,200,150,120,"early W2 enemies."],
        [3,300,225,180,"all W2 enemies."],
        [4,400,350,240,"most W3 enemies."],
        [5,500,500,291,"early W4 enemies."],
        [6,600,700,291,"all W4 enemies."]
        ]
    defaultTiers['Alchemy Bubbles'] = []
    defaultTiers['Alchemy Vials'] = [
        #int tier, int TotalVialsUnlocked, int TotalVialsMaxed, list ParticularVials, str Notes
        [0, 10, 0, [], ""],
        [1, 14, 0, [], ". This is the number of vials requiring an unlock roll of 75 or less. "],
        [2, 19, 0, [], ". This is the number of vials requiring an unlock roll of 85 or less. "],
        [3, 27, 0, [], ". This is the number of vials requiring an unlock roll of 90 or less. "],
        [4, 33, 0, [], ". This is the number of vials requiring an unlock roll of 95 or less. "],
        [5, 38, 0, [], ". This is the number of vials requiring an unlock roll of 98 or less. "],
        [6, 51, 0, [], ". This is all vials up through W4, excluding the Arcade Pickle. "],
        [7, 63, 4, ['Copper Corona (Copper Ore)', 'Sippy Splinters (Oak Logs)', 'Jungle Juice (Jungle Logs)', 'Tea With Pea (Potty Rolls)'], ". This is all vials up through W5, excluding the Arcade Pickle. "],
        [8, 63, 8, ['Gold Guzzle (Gold Ore)', 'Seawater (Goldfish)', 'Fly In My Drink (Fly)', 'Blue Flav (Platinum Ore)'], ""],
        [9, 63, 12, ['Slug Slurp (Hermit Can)', 'Void Vial (Void Ore)', 'Ew Gross Gross (Mosquisnow)', 'The Spanish Sahara (Tundra Logs)'], ""],
        [10, 63, 16, ['Long Island Tea (Sand Shark)', 'Maple Syrup (Maple Logs)', 'Marble Mocha (Marble Ore)', 'Willow Sippy (Willow Logs)'], ""],
        [11, 63, 20, ['Mushroom Soup (Spore Cap)', 'Dieter Drink (Bean Slices)', 'Skinny 0 Cal (Snake Skin)', 'Shinyfin Stew (Equinox Fish)'], ""],
        [12, 63, 24, ['Anearful (Glublin Ear)', 'Ramificoction (Bullfrog Horn)', 'Tail Time (Rats Tail)', 'Dreamy Drink (Dream Particulate)'], ""],
        [13, 63, 28, ['Mimicraught (Megalodon Tooth)', 'Fur Refresher (Floof Ploof)', 'Etruscan Lager (Mamooth Tusk)', 'Dusted Drink (Dust Mote)'], ""],
        [14, 63, 32, ['Sippy Soul (Forest Soul)', 'Visible Ink (Pen)', 'Snow Slurry (Snow Ball)', 'Sippy Cup (Sippy Straw)'], ""],
        [15, 63, 36, ['Crab Juice (Crabbo)', 'Chonker Chug (Dune Soul)', 'Bubonic Burp (Mousey)', '40-40 Purity (Contact Lense)'], ""],
        [16, 63, 40, ['Capachino (Purple Mush Cap)', 'Donut Drink (Half Eaten Donut)', 'Calcium Carbonate (Tongue Bone)', 'Krakenade (Kraken)'], ""],
        [17, 63, 44, ['Spool Sprite (Thread)', 'Choco Milkshake (Crumpled Wrapper)', 'Electrolyte (Condensed Zap)', 'Ash Agua (Suggma Ashes)'], ""],
        [18, 63, 48, ['Thumb Pow (Trusty Nails)', 'Slowergy Drink (Frigid Soul)', 'Bunny Brew (Bunny)', 'Oj Jooce (Orange Slice)'], ""],
        [19, 63, 52, ['Goosey Glug (Honker)', 'Spook Pint (Squishy Soul)', 'Bloat Draft (Blobfish)', 'Venison Malt (Mongo Worm Slices)'], ""],
        [20, 63, 56, ['Barium Mixture (Copper Bar)', 'Barley Brew (Iron Bar)', ' (Poison Tincture)', 'Oozie Ooblek (Oozie Soul)'], ""],
        [21, 63, 60, ['Red Malt (Redox Salts)', 'Orange Malt (Explosive Salts)', 'Shaved Ice (Purple Salt)', 'Dreadnog (Dreadlo Bar)'], ""],
        [22, 63, 64, ['Pickle Jar (BobJoePickle)', 'Ball Pickle Jar (BallJoePickle)', 'Pearl Seltzer (Pearler Shell)', 'Hampter Drippy (Hampter)'], ""]
        ]
    defaultTiers['Construction Printer'] = []
    defaultTiers['Construction Refinery'] = [
        #int tier, dict Tab1 Ranks, dict Tab2 Ranks, dict Tab3, dict All-tab AutoRefine, int W3Merits purchased, str Notes
        [0,  {'Red Rank':0, 'Orange Rank':0, 'Blue Rank':0},    {'Green Rank':0, 'Purple Rank':0, 'Nullo Rank':0},    {}, {}, 0,""],
        [1,  {'Red Rank':1, 'Orange Rank':0, 'Blue Rank':0},    {'Green Rank':2, 'Purple Rank':0, 'Nullo Rank':0},    {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 0, ""],
        [2,  {'Red Rank':6, 'Orange Rank':3, 'Blue Rank':1},    {'Green Rank':2, 'Purple Rank':0, 'Nullo Rank':0},    {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 2, ""],
        [3,  {'Red Rank':8, 'Orange Rank':4, 'Blue Rank':2},    {'Green Rank':6, 'Purple Rank':3, 'Nullo Rank':1},    {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [4,  {'Red Rank':11, 'Orange Rank':6, 'Blue Rank':3},   {'Green Rank':8, 'Purple Rank':4, 'Nullo Rank':2},    {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [5,  {'Red Rank':14, 'Orange Rank':8, 'Blue Rank':4},   {'Green Rank':11, 'Purple Rank':6, 'Nullo Rank':3},   {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [6,  {'Red Rank':16, 'Orange Rank':9, 'Blue Rank':5},   {'Green Rank':14, 'Purple Rank':8, 'Nullo Rank':4},   {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [7,  {'Red Rank':19, 'Orange Rank':11, 'Blue Rank':6},  {'Green Rank':17, 'Purple Rank':10, 'Nullo Rank':5},  {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [8,  {'Red Rank':21, 'Orange Rank':12, 'Blue Rank':7},  {'Green Rank':19, 'Purple Rank':11, 'Nullo Rank':6},  {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [9,  {'Red Rank':24, 'Orange Rank':14, 'Blue Rank':8},  {'Green Rank':21, 'Purple Rank':12, 'Nullo Rank':7},  {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [10, {'Red Rank':28, 'Orange Rank':16, 'Blue Rank':9},  {'Green Rank':24, 'Purple Rank':14, 'Nullo Rank':8},  {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [11, {'Red Rank':33, 'Orange Rank':19, 'Blue Rank':11}, {'Green Rank':28, 'Purple Rank':16, 'Nullo Rank':9},  {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [12, {'Red Rank':33, 'Orange Rank':19, 'Blue Rank':12}, {'Green Rank':29, 'Purple Rank':17, 'Nullo Rank':10}, {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [13, {'Red Rank':37, 'Orange Rank':21, 'Blue Rank':12}, {'Green Rank':29, 'Purple Rank':17, 'Nullo Rank':11}, {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [14, {'Red Rank':40, 'Orange Rank':23, 'Blue Rank':13}, {'Green Rank':36, 'Purple Rank':21, 'Nullo Rank':12}, {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [15, {'Red Rank':45, 'Orange Rank':26, 'Blue Rank':15}, {'Green Rank':40, 'Purple Rank':23, 'Nullo Rank':13}, {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [16, {'Red Rank':45, 'Orange Rank':26, 'Blue Rank':15}, {'Green Rank':42, 'Purple Rank':24, 'Nullo Rank':14}, {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, ""],
        [17, {'Red Rank':22}, {}, {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, "Optionally, you can start letting the Combustion Tab salts always rank up after Red reaches Rank 22."],
        [18, {'Red Rank':22}, {'Green Rank':22}, {}, {'Red AutoRefine':0, 'Green AutoRefine':0}, 5, "Optionally, you can start letting the Combustion Tab salts always rank up after Green reaches Rank 22."],
        [19, {}, {}, {}, {'Sum AutoRefine':0}, 5, "Be cautious: This method of always ranking up all salts will get you to the Rank 22+ holy land faster, but will often leave you dry without salts for days or weeks at a time."],
        ]
    defaultTiers['Construction Salt Lick'] = [
        [0, {}, ""],
        [1, {'Obol Storage':8}, "Froges"],
        [2, {'Printer Sample Size':20}, "Red Salts"],
        [3, {'Refinery Speed':10}, "Orange Salts"],
        [4, {'Max Book':10}, "Blue Salts"],
        [5, {'Movespeed':25}, "Blue Souls"],
        [6, {'TD Points':10}, "Green Salts"],
        [7, {'Multikill':10}, "Purple Salts"],
        [8, {'EXP':100}, "Yellow Souls"],
        [9, {'Alchemy Liquids':100}, "Mouseys"],
        [10, {'Damage':250}, "Pingys"]
        ]
    defaultTiers['Construction Death Note'] = []
    defaultTiers['Construction Buildings'] = []
    defaultTiers['Construction Atom Collider'] = []
    defaultTiers['Combat Levels'] = [
        #int tier, int TotalAccountLevel, str TAL reward, int PlayerLevels, str PL reward, str notes
        [0, 0, "", 0, "", ""],
        [1, 8, "Character 2", 25, "Personal - Circle Obol Slot 2", ""],
        [2, 30, "Character 3", 32, "Personal - Square Obol Slot 1", ""],
        [3, 60, "Character 4 and Family - Circle Obol Slot 1", 40, "Personal - Circle Obol Slot 3", ""],
        [4, 80, "Family - Circle Obol Slot 2", 48, "Personal - Circle Obol Slot 4", ""],
        [5, 100, "Family - Circle Obol Slot 3", 60, "Personal - Square Obol Slot 2", ""],
        [6, 130, "Character 5", 70, "Personal - Circle Obol Slot 5", ""],
        [7, 160, "Family - Circle Obol Slot 4", 80, "Personal - Circle Obol Slot 6", ""],
        [8, 200, "Family - Square Obol Slot 1", 90, "Personal - Square Obol Slot 3", ""],
        [9, 225, "Character 6", 98, "Personal - Circle Obol Slot 7", ""],
        [10, 250, "Family - Circle Obol Slot 5", 105, "Personal - Hexagon Obol Slot 1", ""],
        [11, 330, "Character 7", 112, "Personal - Circle Obol Slot 8", ""],
        [12, 350, "Family - Circle Obol Slot 6", 120, "Personal - Square Obol Slot 4", ""],
        [13, 400, "Family - Circle Obol Slot 7 and Family - Hexagon Obol Slot 1", 130, "Personal - Circle Obol Slot 9", ""],
        [14, 470, "Character 8 and Family - Circle Obol Slot 8", 140, "Personal - Square Obol Slot 5", ""],
        [15, 600, "Character 9", 150, "Vman Quest, if class = Mman", ""],
        [16, 650, "Family - Sparkle Obol Slot 1", 152, "Personal - Circle Obol Slot 10", ""],
        [17, 700, "Family - Square Obol Slot 2", 180, "Personal - Hexagon Obol Slot 2", ""],
        [18, 875, "Family - Circle Obol Slot 9", 190, "Personal - Square Obol Slot 6", ""],
        [19, 900, "Character 10 and Family - Hexagon Obol Slot 2", 210, "Personal - Circle Obol Slot 12", ""],
        [20, 1150, "Family - Square Obol Slot 3", 250, "Personal - Sparkle Obol Slot 1 and Credit towards Equinox Dream 11", ""],
        [21, 1200, "Family - Sparkle Obol Slot 2", 425, "Able to equip The Divine Scarf", ""],
        [22, 1250, "Family - Circle Obol Slot 10", 450, "Able to equip One of the Divine Trophy", ""],
        [23, 1500, "Family - Circle Obol Slot 11", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500."],
        [24, 1750, "Family - Hexagon Obol Slot 3", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [25, 2000, "Family - Square Obol Slot 4", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [26, 2100, "Family - Circle Obol Slot 12", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [27, 2500, "Family - Sparkle Obol Slot 3", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [28, 3000, "Family - Hexagon Obol Slot 4", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [29, 5000, "Family - Sparkle Obol Slot 4", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [30, 5000, "As of v1.91, the last Family reward was at 5000! You're temporarily finished :)", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        ]
    return defaultTiers

def setCustomTiers(filename="input.csv"):
    return

def main(inputCharacterName="scoli"):
    #Step 1: Retrieve data from public IdleonEfficiency website or from file
    if True == True:
        inputCharacterName = str.strip(inputCharacterName.replace(" ", "_")) #IE expects underscores instead of spaces in names
        parsedJSON = getJSONfromAPI("https://" + inputCharacterName + ".idleonefficiency.com/raw-data")
    else:
        parsedJSON = getJSONfromFILE(filename)
    if parsedJSON == []:
        errorStatement = "Unable to retrieve data for this character name. Please check your spelling and make sure you have uploaded your account publicly."
        errorList = [errorStatement,errorStatement,errorStatement,errorStatement,errorStatement,errorStatement,errorStatement,errorStatement,errorStatement,errorStatement]
        errorListofLists = [[errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList], #general placeholder
        [errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList], #w1 placeholder
        [errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList], #w2 placeholder
        [errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList], #w3 placeholder
        [errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList], #w4 placeholder
        [errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList,errorList]] #w5 placeholder
        return errorListofLists
    #Step 2: Set either Default or Custom progression tiers
    if True == True:
        progressionTiers = setDefaultTiers()
    else:
        progressionTiers = setCustomTiers(filename)

    #Step 3: Send that data off to all the different analyzers
    playerCount = len(parsedJSON["playerNames"]) #not 0 based
    #print("Number of unlocked characters: " + str(playerCount))
    #print("## General Account AutoReview")
    combatLevelsPR = idleon_CombatLevels.setCombatLevelsProgressionTier(parsedJSON, progressionTiers['Combat Levels'], playerCount)
    print(combatLevelsPR.nTR)
    consumablesList = idleon_Consumables.parseConsumables(parsedJSON, playerCount)
    print(consumablesList)
    #generalObolsPR =
    #print("## World 1 AutoReview")
    stampPR = idleon_Stamps.setStampProgressionTier(parsedJSON, progressionTiers['Stamps'])
    print(stampPR.nTR)
    bribesPR = idleon_Bribes.setBribesProgressionTier(parsedJSON, progressionTiers['Bribes'])
    print(bribesPR.nTR)
    smithingPR = idleon_Smithing.setSmithingProgressionTier(parsedJSON, progressionTiers['Smithing'], playerCount)
    print(smithingPR.nTR)
    #print("## World 2 AutoReview")
    #alchBubblesPR = idleon_Alchemy.setAlchemyBubblesProgressionTier(parsedJSON, progressionTiers['Alchemy Bubbles'])
    #print(alchBubblesPR.nTR)
    alchVialsPR = idleon_Alchemy.setAlchemyVialsProgressionTier(parsedJSON, progressionTiers['Alchemy Vials'])
    print(alchVialsPR.nTR)
    #print("## World 3 AutoReview")
    #consPrinterPR =
    #print(consRefineryPR.nTR)
    consRefineryPR = idleon_ConsRefinery.setConsRefineryProgressionTier(parsedJSON, progressionTiers['Construction Refinery'])
    print(consRefineryPR.nTR)
    consSaltLickPR = idleon_ConsSaltLick.setConsSaltLickProgressionTier(parsedJSON, progressionTiers['Construction Salt Lick'])
    print(consSaltLickPR.nTR)
    #consDeathNotePR =
    #consBuildingsPR =
    #consAtomColliderPR =
    #worshipTotemsPR =
    #worshipPrayersPR =
    #trappingPR =
    #print("## World 4 AutoReview")
    #cookingPR =
    #labPR =
    #breedingPR =
    #print("## World 5 AutoReview")
    #sailingPR =
    #gamingPR =
    #divinityPR =

    generalList = [["Searching for character data from: https://" + inputCharacterName.lower() + ".idleonefficiency.com"], combatLevelsPR.nTR, consumablesList] #len(combatLevelsPR.nTR) = 2, len(consumablesList) = 2
    w1list = [stampPR.nTR, bribesPR.nTR, smithingPR.nTR] #len(stampPR) = 4, len(bribesPR.nTR) = 2, len(smithingPR.nTR) = 4
    w2list = [["Alchemy Bubbles coming soon!"],alchVialsPR.nTR] #len(alchBubblesPR.nTR) = 0, len(alchVialsPR.nTR) = 0
    w3list = [["Construction 3D Printer coming soon!"], consRefineryPR.nTR, consSaltLickPR.nTR, ["Construction Death Note coming soon!"],
        ["Construction Buildings coming soon!"], ["Construction Atom Collider coming soon!"], ["Worship Totems coming soon!"], ["Worship Prayers coming soon!"], ["Trapping coming soon!"]] #len(consRefineryPR.nTR) = 5, len(consSaltLickPR.nTR) = 2
    w4list = [["Cooking coming soon!"],["Breeding coming soon!"],["Lab coming soon!"]]
    w5list = [["Sailing coming soon!"],["Gaming coming soon!"],["Divinity coming soon!"]]
    return [generalList, w1list, w2list, w3list, w4list, w5list]

main("Cupquake")