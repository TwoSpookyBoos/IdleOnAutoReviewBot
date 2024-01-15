import json
import progressionResults

def getShinyLevelFromDays(days):
    shinyDaysList = [0, 3, 11, 33, 85, 200, 448, 964, 2013, 4107]
    highestExceeded = 0
    for requirement in shinyDaysList:
        if float(days) > requirement:
            highestExceeded += 1
    return highestExceeded

def getShinyExclusions(inputJSON):
    currentArtifactsCount = 30
    currentArtifactTiers = 3
    shinyExclusionsDict = {
        "Exclude-InfiniteStarSigns": True,
        "Exclude-ArtifactChance": False
        }

    #if Infinite Star Signs are unlocked, set False (as in False, the recommendation should NOT be excluded), otherwise default True
    try:
        highestCompletedRift = inputJSON["Rift"][0]
        if highestCompletedRift >= 11:
            shinyExclusionsDict["Exclude-InfiniteStarSigns"] = False
    except Exception as reason:
        print("Breeding.getShinyExclusions~ EXCEPTION Unable to retrieve highest rift level:",reason)

    #if all artifacts are Eldritch tier, append True (as in True, the recommendation SHOULD be excluded), otherwise False
    try:
        sum_sailingArtifacts = sum(json.loads(inputJSON["Sailing"])[3])
        if sum_sailingArtifacts == (currentArtifactsCount*currentArtifactTiers): #30 artifacts times 3 tiers each = 90 for v1.91
            shinyExclusionsDict["Exclude-ArtifactChance"] = True
    except Exception as reason:
        print("Breeding.getShinyExclusions~ EXCEPTION Unable to get Sailing Artifacts:",reason)

    return shinyExclusionsDict

def getTerritoryName(index):
    territoryNames = ["", "Grasslands", "Jungle", "Encroaching Forest", "Tree Interior", "Stinky Sewers", "Desert Oasis", "Beach Docks", "Coarse Mountains",
        "Twilight Desert", "The Crypt", "Frosty Peaks", "Tundra Outback", "Crystal Caverns", "Pristalle Lake", "Nebulon Mantle", "Starfield Skies",
        "Shores of Eternity", "Molten Bay", "Smokey Lake", "Wurm Catacombs"]
    try:
        return territoryNames[int(index)]
    except:
        return "Unknown Territory" + str(index)

def parseJSONtoBreedingDict(inputJSON):
    breedingList = []
    try:
        breedingList = json.loads(inputJSON["Breeding"])
        #print("Breeding.parseJSON~ OUTPUT unlockedPets:", type(breedingList[1]), breedingList[1])
    except Exception as reason:
        print("Breeding.parseJSON~ EXCEPTION Could not load \"Breeding\" from JSON:", reason)
        return {}

    territoriesList = []
    try:
        territoriesList = json.loads(inputJSON["Territory"])
        #print("Breeding.parseJSON~ OUTPUT territoriesList:", type(territoriesList), territoriesList)
    except Exception as reason:
        print("Breeding.parseJSON~ EXCEPTION Could not load \"Territory\" from JSON:", reason)
        return {}

    arenaMaxWave = 0
    petSlotsUnlocked = 2
    try:
        arenaMaxWave = inputJSON["OptLacc"][89]
        slotUnlockWavesList = [2, 15, 50, 125]
        for requirement in slotUnlockWavesList:
            if arenaMaxWave > requirement:
                petSlotsUnlocked += 1
        #print("Breeding.parseJSON~ OUTPUT arenaMaxWave:", arenaMaxWave)
        #print("Breeding.parseJSON~ OUTPUT petSlotsUnlocked:", petSlotsUnlocked)
    except Exception as reason:
        print("Breeding.parseJSON~ EXCEPTION Could not load \"OptLacc\" from JSON to get Arena Max Wave:", reason)

    parsedBreedingDict = {}
    if breedingList != []:
        #Straight data grabs
        parsedBreedingDict = {
            "W1 Unlocked Count": breedingList[1][0],
            "W2 Unlocked Count": breedingList[1][1],
            "W3 Unlocked Count": breedingList[1][2],
            "W4 Unlocked Count": breedingList[1][3],
            "W5 Unlocked Count": breedingList[1][4],
            "W6 Unlocked Count": breedingList[1][5],
            "W7 Unlocked Count": breedingList[1][6],
            "W8 Unlocked Count": breedingList[1][7],
            "Abilities": {},
            "Species": {},
            "Shinies": {
                "W1 Shiny Days": breedingList[22],
                "W2 Shiny Days": breedingList[23],
                "W3 Shiny Days": breedingList[24],
                "W4 Shiny Days": breedingList[25],
                "W5 Shiny Days": breedingList[26],
                "W6 Shiny Days": breedingList[27],
                "W7 Shiny Days": breedingList[28],
                "W8 Shiny Days": breedingList[29],
                "Total Shiny Levels": {},
                "Grouped Bonus": {}
                },
            "Highest Arena Wave": arenaMaxWave,
            "Pet Slots Unlocked": petSlotsUnlocked
            }

        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"Shinies\"]:", parsedBreedingDict["Shinies"])
        #print("Breeding.parseJSON~ OUTPUT length of each [Shinies][WX Shiny Days]:",
        #    len(parsedBreedingDict["Shinies"]["W1 Shiny Days"]), len(parsedBreedingDict["Shinies"]["W2 Shiny Days"]),
        #    len(parsedBreedingDict["Shinies"]["W3 Shiny Days"]), len(parsedBreedingDict["Shinies"]["W4 Shiny Days"]),
        #    len(parsedBreedingDict["Shinies"]["W5 Shiny Days"]), len(parsedBreedingDict["Shinies"]["W6 Shiny Days"]),
        #    len(parsedBreedingDict["Shinies"]["W7 Shiny Days"]), len(parsedBreedingDict["Shinies"]["W8 Shiny Days"]), )

        #Data needing some logic behind it
        parsedBreedingDict["Total Unlocked Count"] = parsedBreedingDict["W1 Unlocked Count"] + parsedBreedingDict["W2 Unlocked Count"] + parsedBreedingDict["W3 Unlocked Count"] + parsedBreedingDict["W4 Unlocked Count"]
        # + parsedBreedingDict["W5 Unlocked Count"] + parsedBreedingDict["W6 Unlocked Count"] + parsedBreedingDict["W7 Unlocked Count"] + parsedBreedingDict["W8 Unlocked Count"]

        abilitiesList = ["Fighter", "Defender", "Forager", "Fleeter", "Breeder", "Special", "Mercenary", "Boomer", "Sniper", "Amplifier", "Tsar", "Rattler", "Cursory",
        "Fastidious", "Flashy", "Opticular", "Monolithic", "Alchemic", "Badumdum", "Defstone", "Targeter", "Looter", "Refiller", "Eggshell", "Lazarus", "Trasher", "Miasma",
        "Converter", "Heavyweight", "Fastihoop", "Ninja", "Superboomer", "Peapeapod", "Borger"]
        for ability in abilitiesList:
            parsedBreedingDict["Abilities"][ability] = False
        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"Abilities\"]:", parsedBreedingDict["Abilities"])

        shinyBonusList = ["Faster Shiny Pet Lv Up Rate", "Infinite Star Signs", "Total Damage", "Drop Rate", "Base Efficiency for All Skills",
            "Base WIS", "Base STR", "Base AGI", "Base LUK", "Class EXP", "Skill EXP",
            "Tab 1 Talent Pts", "Tab 2 Talent Pts", "Tab 3 Talent Pts", "Tab 4 Talent Pts", "Star Talent Pts",
            "Faster Refinery Speed", "Base Critter Per Trap", "Multikill Per Tier",
            "Bonuses from All Meals", "Line Width in Lab",
            "Higher Artifact Find Chance", "Sail Captain EXP Gain", "Lower Mininmum Travel Time for Sailing",
            "World 6...?"]
        for bonus in shinyBonusList:
            parsedBreedingDict["Shinies"]["Total Shiny Levels"][bonus] = 0

        speciesDict = {
            "W1 Unlocked Species": {
                "Green Mushroom": ["Fighter", parsedBreedingDict["W1 Unlocked Count"]>=1, "Faster Shiny Pet Lv Up Rate", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][0]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][0]],
                "Squirrel": ["Forager", parsedBreedingDict["W1 Unlocked Count"]>=2, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][1]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][1]],
                "Frog": ["Boomer", parsedBreedingDict["W1 Unlocked Count"]>=3, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][2]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][2]],
                "Bored Bean": ["Fleeter", parsedBreedingDict["W1 Unlocked Count"]>=4, "Faster Refinery Speed", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][3]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][3]],
                "Red Mushroom": ["Fighter", parsedBreedingDict["W1 Unlocked Count"]>=5, "Bonuses from All Meals", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][4]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][4]],
                "Slime": ["Cursory", parsedBreedingDict["W1 Unlocked Count"]>=6, "Drop Rate", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][5]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][5]],
                "Piggo": ["Amplifier", parsedBreedingDict["W1 Unlocked Count"]>=7, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][6]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][6]],
                "Baby Boa": ["Targeter", parsedBreedingDict["W1 Unlocked Count"]>=8, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][7]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][7]],
                "Carrotman": ["Mercenary", parsedBreedingDict["W1 Unlocked Count"]>=9, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][8]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][8]],
                "Glublin": ["Refiller", parsedBreedingDict["W1 Unlocked Count"]>=10, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][9]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][9]],
                "Wode Board": ["Miasma", parsedBreedingDict["W1 Unlocked Count"]>=11, "Faster Shiny Pet Lv Up Rate", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][10]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][10]],
                "Gigafrog": ["Amplifier", parsedBreedingDict["W1 Unlocked Count"]>=12, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][11]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][11]],
                "Wild Boar": ["Heavyweight", parsedBreedingDict["W1 Unlocked Count"]>=13, "Base AGI", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][12]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][12]],
                "Walking Stick": ["Refiller", parsedBreedingDict["W1 Unlocked Count"]>=14, "Base Critter Per Trap", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][13]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][13]],
                "Nutto": ["Borger", parsedBreedingDict["W1 Unlocked Count"]>=15, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][14]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][14]],
                "Poop": ["Tsar", parsedBreedingDict["W1 Unlocked Count"]>=16, "World 6...?", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][15]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][15]],
                "Rat": ["Monolithic", parsedBreedingDict["W1 Unlocked Count"]>=17, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W1 Shiny Days"][16]), parsedBreedingDict["Shinies"]["W1 Shiny Days"][16]]
                },
            "W2 Unlocked Species": {
                "Sandy Pot": ["Looter", parsedBreedingDict["W2 Unlocked Count"]>=1, "Class EXP", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][0]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][0]],
                "Mimic": ["Defender", parsedBreedingDict["W2 Unlocked Count"]>=2, "Tab 1 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][1]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][1]],
                "Crabcake": ["Fleeter", parsedBreedingDict["W2 Unlocked Count"]>=3, "Skill EXP", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][2]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][2]],
                "Mafioso": ["Forager", parsedBreedingDict["W2 Unlocked Count"]>=4, "Tab 2 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][3]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][3]],
                "Mallay": ["Opticular", parsedBreedingDict["W2 Unlocked Count"]>=5, "Line Width in Lab", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][4]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][4]],
                "Sand Castle": ["Defstone", parsedBreedingDict["W2 Unlocked Count"]>=6, "Base STR", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][5]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][5]],
                "Pincermin": ["Fighter", parsedBreedingDict["W2 Unlocked Count"]>=7, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][6]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][6]],
                "Mashed Potato": ["Amplifier", parsedBreedingDict["W2 Unlocked Count"]>=8, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][7]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][7]],
                "Tyson": ["Fastidious", parsedBreedingDict["W2 Unlocked Count"]>=9, "Higher Artifact Find Chance", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][8]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][8]],
                "Whale": ["Badumdum", parsedBreedingDict["W2 Unlocked Count"]>=10, "Faster Refinery Speed", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][9]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][9]],
                "Moonmoon": ["Mercenary", parsedBreedingDict["W2 Unlocked Count"]>=11, "Base WIS", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][10]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][10]],
                "Sand Giant": ["Rattler", parsedBreedingDict["W2 Unlocked Count"]>=12, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][11]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][11]],
                "Snelbie": ["Monolithic", parsedBreedingDict["W2 Unlocked Count"]>=13, "Tab 4 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][12]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][12]],
                "Dig Doug": ["Lazarus", parsedBreedingDict["W2 Unlocked Count"]>=14, "World 6...?", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][13]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][13]],
                "Beefie": ["Trasher", parsedBreedingDict["W2 Unlocked Count"]>=15, "Base LUK", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][14]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][14]],
                "Crescent Spud": ["Monolithic", parsedBreedingDict["W2 Unlocked Count"]>=16, "Faster Shiny Pet Lv Up Rate", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][15]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][15]],
                "Chippy": ["Eggshell", parsedBreedingDict["W2 Unlocked Count"]>=17, "World 6...?", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W2 Shiny Days"][16]), parsedBreedingDict["Shinies"]["W2 Shiny Days"][16]]
                },
            "W3 Unlocked Species": {
                "Sheepie": ["Sniper", parsedBreedingDict["W3 Unlocked Count"]>=1, "Bonuses from All Meals", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][0]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][0]],
                "Frost Flake": ["Ninja", parsedBreedingDict["W3 Unlocked Count"]>=2, "Tab 3 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][1]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][1]],
                "Sir Stache": ["Eggshell", parsedBreedingDict["W3 Unlocked Count"]>=3, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][2]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][2]],
                "Xylobone": ["Opticular", parsedBreedingDict["W3 Unlocked Count"]>=4, "Drop Rate", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][3]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][3]],
                "Bunny": ["Flashy", parsedBreedingDict["W3 Unlocked Count"]>=5, "Base LUK", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][4]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][4]],
                "Bloque": ["Alchemic", parsedBreedingDict["W3 Unlocked Count"]>=6, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][5]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][5]],
                "Mamooth": ["Looter", parsedBreedingDict["W3 Unlocked Count"]>=7, "Higher Artifact Find Chance", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][6]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][6]],
                "Snowman": ["Defstone", parsedBreedingDict["W3 Unlocked Count"]>=8, "Class EXP", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][7]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][7]],
                "Penguin": ["Fastidious", parsedBreedingDict["W3 Unlocked Count"]>=9, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][8]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][8]],
                "Thermister": ["Sniper", parsedBreedingDict["W3 Unlocked Count"]>=10, "Skill EXP", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][9]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][9]],
                "Quenchie": ["Boomer", parsedBreedingDict["W3 Unlocked Count"]>=11, "Faster Shiny Pet Lv Up Rate", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][10]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][10]],
                "Cryosnake": ["Eggshell", parsedBreedingDict["W3 Unlocked Count"]>=12, "Star Talent Pts", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][11]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][11]],
                "Mecho Mouse": ["Trasher", parsedBreedingDict["W3 Unlocked Count"]>=13, "Base STR", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][12]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][12]],
                "Bop Box": ["Converter", parsedBreedingDict["W3 Unlocked Count"]>=14, "Base WIS", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][13]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][13]],
                "Neyeptune": ["Lazarus", parsedBreedingDict["W3 Unlocked Count"]>=15, "World 6...?", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][14]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][14]],
                "Dedotated Ram": ["Amplifier", parsedBreedingDict["W3 Unlocked Count"]>=16, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][15]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][15]],
                "Bloodbone": ["Targeter", parsedBreedingDict["W3 Unlocked Count"]>=17, "World 6...?", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][16]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][16]],
                "Panda": ["Converter", parsedBreedingDict["W3 Unlocked Count"]>=18, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W3 Shiny Days"][17]), parsedBreedingDict["Shinies"]["W3 Shiny Days"][17]]
                },
            "W4 Unlocked Species": {
                "Purp Mushroom": ["Tsar", parsedBreedingDict["W4 Unlocked Count"]>=1, "World 6...?", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][0]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][0]],
                "TV": ["Rattler", parsedBreedingDict["W4 Unlocked Count"]>=2, "Sail Captain EXP Gain", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][1]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][1]],
                "Donut": ["Flashy", parsedBreedingDict["W4 Unlocked Count"]>=3, "World 6...?", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][2]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][2]],
                "Demon Genie": ["Superboomer", parsedBreedingDict["W4 Unlocked Count"]>=4, "Faster Refinery Speed", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][3]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][3]],
                "Flying Worm": ["Borger", parsedBreedingDict["W4 Unlocked Count"]>=5, "Base AGI", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][4]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][4]],
                "Dog": ["Peapeapod", parsedBreedingDict["W4 Unlocked Count"]>=6, "Lower Mininmum Travel Time for Sailing", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][5]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][5]],
                "Soda Can": ["Fastihoop", parsedBreedingDict["W4 Unlocked Count"]>=7, "Higher Artifact Find Chance", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][6]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][6]],
                "Gelatinous Cuboid": ["Flashy", parsedBreedingDict["W4 Unlocked Count"]>=8, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][7]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][7]],
                "Choccie": ["Superboomer", parsedBreedingDict["W4 Unlocked Count"]>=9, "Drop Rate", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][8]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][8]],
                "Biggole Wurm": ["Tsar", parsedBreedingDict["W4 Unlocked Count"]>=10, "Class EXP", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][9]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][9]],
                "Cool Bird": ["Borger", parsedBreedingDict["W4 Unlocked Count"]>=11, "Base STR", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][10]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][10]],
                "Clammie": ["Mercenary", parsedBreedingDict["W4 Unlocked Count"]>=12, "Skill EXP", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][11]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][11]],
                "Octodar": ["Cursory", parsedBreedingDict["W4 Unlocked Count"]>=13, "Base Critter Per Trap", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][12]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][12]],
                "Flombeige": ["Trasher", parsedBreedingDict["W4 Unlocked Count"]>=14, "Base AGI", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][13]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][13]],
                "Stilted Seeker": ["Borger", parsedBreedingDict["W4 Unlocked Count"]>=15, "Base WIS", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][14]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][14]],
                "Hedgehog": ["Peapeapod", parsedBreedingDict["W4 Unlocked Count"]>=16, "Base LUK", getShinyLevelFromDays(parsedBreedingDict["Shinies"]["W4 Shiny Days"][15]), parsedBreedingDict["Shinies"]["W4 Shiny Days"][15]]
                }
            }

        parsedBreedingDict["Species"] = speciesDict
        for world in speciesDict:
            #print("Breeding.parseJSON~ OUTPUT world in speciesDict:", world)
            for species in speciesDict[world]:
                #print("Breeding.parseJSON~ OUTPUT species in speciesDict:", species)
                if speciesDict[world][species][1] == True and parsedBreedingDict["Abilities"][speciesDict[world][species][0]] == False:
                    parsedBreedingDict["Abilities"][speciesDict[world][species][0]] = True
                if speciesDict[world][species][3] > 0:
                    #print("Breeding.parseJSON~ INFO From", species, ", increasing total level of", speciesDict[world][species][2], "by", speciesDict[world][species][3])
                    #print("Old value:", parsedBreedingDict["Shinies"]["Total Shiny Levels"][speciesDict[world][species][2]])
                    parsedBreedingDict["Shinies"]["Total Shiny Levels"][speciesDict[world][species][2]] += speciesDict[world][species][3]
                if speciesDict[world][species][2] in parsedBreedingDict["Shinies"]["Grouped Bonus"].keys():
                    parsedBreedingDict["Shinies"]["Grouped Bonus"][speciesDict[world][species][2]].append((species, speciesDict[world][species][3], speciesDict[world][species][4]))
                else:
                    parsedBreedingDict["Shinies"]["Grouped Bonus"][speciesDict[world][species][2]] = [(species, speciesDict[world][species][3], speciesDict[world][species][4])]
        for groupedBonus in parsedBreedingDict["Shinies"]["Grouped Bonus"]:
            parsedBreedingDict["Shinies"]["Grouped Bonus"][groupedBonus].sort(key = lambda x: float(x[2]))

        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"Abilities\"]:", parsedBreedingDict["Abilities"])
        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"Shinies\"][\"Total Shiny Levels\"]:", parsedBreedingDict["Shinies"]["Total Shiny Levels"])
        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"Shinies\"][\"Grouped Bonus\"]:", parsedBreedingDict["Shinies"]["Grouped Bonus"])
        #print("Breeding.parseJSON~ OUTPUT Sorted by lowest level per:", parsedBreedingDict["Shinies"]["Grouped Bonus"])

        parsedBreedingDict["Territories Unlocked Count"] = 0
        for territory in territoriesList:
            if territory[0] > 0: #This will only be above 0 for territories which have had a pet added and progress started
                parsedBreedingDict["Territories Unlocked Count"] += 1
        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"Territories Unlocked Count\"]:", parsedBreedingDict["Territories Unlocked Count"])
    else:
        return {}

    #for element in parsedBreedingDict:
        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"", element, "\"]:", parsedBreedingDict[element])
    return parsedBreedingDict

def setBreedingProgressionTier(inputJSON, progressionTiers):
    maxBreedingTier = max(progressionTiers.keys())
    tier_UnlockedTerritories = 0
    tier_MaxArenaWave = 0
    tier_ShinyLevels = 0
    overall_BreedingTier = 0
    advice_UnlockedTerritories = ""
    recommendedTerritoryCompsList = [ "",
        "Mercenary, Next Highest Power",
        "Mercenary, Cursory, Defender or Highest Power",
        "Rattler, Cursory, Refiller, Defender",
        "Rattler, Monolithic, Refiller, Defender, Refiller",
        "Rattler, Looter, Monolithic, Refiller, Defender, Refiller" ]
    recommendedArenaCompsList = [
        "Mercenary or Fighter, Next Highest Power",                 #2-pet comp used to beat Wave 3
        "Mercenary, Cursory, Defender or Highest Power",            #3-pet comp used to beat Wave 15
        "Rattler, Monolithic, Refiller, Borger or Defender",        #4-pet comp used to beat Wave 50
        "Rattler, Monolithic, Badumdum, Refiller, Borger",          #5-pet comp used to beat Wave 125
        "Rattler, Defender, Looter, Refiller, Badumdum, Borger"    #6-pet comp used to beat Wave 200
        ]
    advice_TerritoryComp = ""
    advice_ArenaComp = ""
    failedShinyRequirements = []
    failedShinyBonus = {}
    advice_ShinyLevels = ""
    advice_ShinyPets = []
    breedingDict = parseJSONtoBreedingDict(inputJSON)
    shinyExclusionsDict = getShinyExclusions(inputJSON)
    if breedingDict == {}:
        breedingPR = progressionResults.progressionResults(0, "Come back after unlocking Breeding in W4!", "")
        return breedingPR
    else:
        for tier in progressionTiers:
            if "Infinite Star Signs" in progressionTiers[tier]["Shinies"] and shinyExclusionsDict["Exclude-InfiniteStarSigns"] == True:
                progressionTiers[tier]["Shinies"]["Infinite Star Signs"] = 0
            if "Higher Artifact Find Chance" in progressionTiers[tier]["Shinies"] and shinyExclusionsDict["Exclude-ArtifactChance"] == True:
                progressionTiers[tier]["Shinies"]["Higher Artifact Find Chance"] = 0

            #print("Breeding.setBreedingProgressionTier~ INFO Starting review of Tier:", tier)
            #Unlocked Territories
            if tier_UnlockedTerritories >= (tier-1):
                if breedingDict["Territories Unlocked Count"] >= progressionTiers[tier]["TerritoriesUnlocked"]:
                    tier_UnlockedTerritories = tier
                    #print("Breeding.setBreedingProgressionTier~ INFO Territory requirement met!", breedingDict["Territories Unlocked Count"], ">=", progressionTiers[tier]["TerritoriesUnlocked"])
                else:
                    advice_UnlockedTerritories = ("Unlock more Spice Territories (" + str(breedingDict["Territories Unlocked Count"])
                        + "/" + str(progressionTiers[tier]["TerritoriesUnlocked"]) + " through " + getTerritoryName(progressionTiers[tier]["TerritoriesUnlocked"]) + ").")
                    #print("Breeding.setBreedingProgressionTier~ INFO Territory requirement failed for tier", tier, "because", breedingDict["Territories Unlocked Count"], "<", progressionTiers[tier]["TerritoriesUnlocked"])

            #Arena Waves to unlock Pet Slots
            if tier_MaxArenaWave >= (tier-1):
                if breedingDict["Highest Arena Wave"] >= progressionTiers[tier]["ArenaWaves"]:
                    tier_MaxArenaWave = tier
                else:
                    advice_ArenaComp = "Recommended team for Arena Wave " + str(progressionTiers[tier]["ArenaWaves"]) + " (from left to right): " + recommendedArenaCompsList[tier_MaxArenaWave]
                    #print("Breeding.setBreedingProgressionTier~ INFO Arena Wave requirement failed for tier", tier, "because", breedingDict["Highest Arena Wave"], "<", progressionTiers[tier]["ArenaWaves"])

            #Shinies
            if tier_ShinyLevels >= (tier-1):
                if len(progressionTiers[tier]["Shinies"]) == 0:
                    #free pass
                    tier_ShinyLevels = tier
                    #print("Breeding.setBreedingProgressionTier~ INFO Shiny requirement freebie!")
                else:
                    #if there are actual level requirements
                    allRequirementsMet = True
                    for requiredShinyBonusType in progressionTiers[tier]["Shinies"]:
                        if breedingDict["Shinies"]["Total Shiny Levels"][requiredShinyBonusType] < progressionTiers[tier]["Shinies"][requiredShinyBonusType]:
                            allRequirementsMet = False
                            failedShinyRequirements.append(requiredShinyBonusType + " (" + str(breedingDict["Shinies"]["Total Shiny Levels"][requiredShinyBonusType]) + "/" + str(progressionTiers[tier]["Shinies"][requiredShinyBonusType]) + ")")
                            failedShinyBonus[requiredShinyBonusType] = breedingDict["Shinies"]["Grouped Bonus"][requiredShinyBonusType]
                            #print("Breeding.setBreedingProgressionTier~ INFO Shiny requirement failed on tier", tier, "because", requiredShinyBonusType, breedingDict["Shinies"]["Total Shiny Levels"][requiredShinyBonusType], "<", progressionTiers[tier]["Shinies"][requiredShinyBonusType])
                    if allRequirementsMet == True:
                        tier_ShinyLevels = tier
                        #print("Breeding.setBreedingProgressionTier~ INFO Shiny requirement met!")
                    else:
                        if len(failedShinyRequirements) == 1:
                            advice_ShinyLevels = "Level the following Shiny bonus: " + failedShinyRequirements[0]
                        else:
                            advice_ShinyLevels = "Level the following Shiny bonuses: "
                            for failedRequirement in failedShinyRequirements:
                                advice_ShinyLevels += failedRequirement + ", "
                            advice_ShinyLevels = advice_ShinyLevels[:-2] #trim off final space and comma

                        advice_perShinyBonus = ""
                        for shinyBonus in failedShinyBonus:
                            #print("Breeding.setBreedingProgressionTier~ INFO shinyBonus:", shinyBonus)
                            advice_perShinyBonus = shinyBonus + " pets: "
                            for pet in failedShinyBonus[shinyBonus]:
                                #print("Breeding.setBreedingProgressionTier~ INFO pet:", pet)
                                advice_perShinyBonus += "Lv" + str(pet[1]) + " " + pet[0] + ", "
                            advice_perShinyBonus = advice_perShinyBonus[:-2] #trim off final space and comma
                            advice_ShinyPets.append(advice_perShinyBonus)
                        #advice_ShinyPets = "Shiny pets for each bonus, sorted by lowest whole level:"
                        #print("Breeding.setBreedingProgressionTier~ OUTPUT advice_ShinyPets:", advice_ShinyPets)

    #Pretty up advice statements
    overall_BreedingTier = min(maxBreedingTier, tier_UnlockedTerritories, tier_ShinyLevels)
    if overall_BreedingTier == maxBreedingTier:
        advice_UnlockedTerritories = "Fantastic job unlocking all of the spice territories!"
        advice_ShinyLevels = "You've got the basic Shiny levels down now. Choose to either futureproof by leveling the W6 buffs and Infinite Star Signs before release, or continue leveling already strong buffs for guaranteed value now."
        advice_ShinyPets = [
            "Best IMO: Faster Shiny Pet Lv Up Rate, Bonuses from All Meals, Base Efficiency for All Skills, Base Critter Per Trap",
            "Second best: Drop Rate, Multikill Per Tier, Total Damage, Base WIS, Base STR, Base AGI",
            "Futureproof: W6...?, Infinite Star Signs",
            "Middle of the pack, helpful to Lv5 at least: Base LUK, Faster Refinery Speed, Higher Artifact Find Chance",
            "Meh: Lower Mininmum Travel Time for Sailing, Sail Captain EXP Gain, Skill EXP",
            "Ignorable: Class EXP, Line Width in Lab"]
    else:
        if advice_UnlockedTerritories != "":
            advice_UnlockedTerritories = "Tier " + str(tier_UnlockedTerritories) + "- " + advice_UnlockedTerritories
            advice_TerritoryComp = "Recommend team for these Territory battles (from left to right): " + recommendedTerritoryCompsList[tier_UnlockedTerritories+1]
        else:
            advice_UnlockedTerritories = "Fantastic job unlocking all of the spice territories!"
        if advice_ShinyLevels != "":
            advice_ShinyLevels = "Tier " + str(tier_ShinyLevels) + "- " + advice_ShinyLevels

    advice_BreedingCombined = ["Best Breeding tier met: " + str(overall_BreedingTier) + "/" + str(maxBreedingTier) + ". Recommended Breeding actions:", advice_UnlockedTerritories, advice_TerritoryComp, advice_ArenaComp, advice_ShinyLevels, advice_ShinyPets]
    breedingPR = progressionResults.progressionResults(overall_BreedingTier,advice_BreedingCombined,"")
    return breedingPR

#1) If not all Pets unlocked, recommend next high priority
#2) If not all Arena Pet slots unlocked, or not all Territories unlocked, recommend what to aim for unlocking based on Abiltiy / meta teams.
    #2a) Possibly list sources of pet chance? Splicing and other dead dna bonsues, vial, stamp, meals, whatever else
    #2b) Maybe a recommended order to spend Dead DNA? Does such a list exist
#3) Spice collecting meta setups. I'm not sure I agree with all of them since I don't follow them.


#
#"Pets" : First 27 = fenceyard, rest = spicebattles
#["carrotO", #pet name/type as string
#4, #pet ability? 4 = Breedability, 5 = Shiny
#219.653862318461, #Pet power
#0] # Shiny color? I see 0 all on non-shinies. Shiny pets seem to be multiples of 60 up to 300.
#
#"PetsStored" for those in the inventory. Same data as within Pets.
#
#"Territory" seems to hold spice info
#[7130.1609064918075, #Progress toward next spice
#232, #Unknown, but seems to be increasing over time
#0, #Unknown
#"CookingSpice0", #Type of spice being collected, 0 through 19. Can be "Blank" even if unlocked.
#583, #Spices ready to be collected
#"Blank", #Unused / Placeholder
#0, #Unused / Placeholder
#"Blank", #Unused / Placeholder
#0] #Unused / Placeholder