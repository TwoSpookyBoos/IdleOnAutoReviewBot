import json

def getCardSetReview(inputJSON):
    cardRequirementsDict = {
        "Blunder Hills": {
            "mushG": ["Green Mushroom",5,15,25,80,2295],
            "mushR": ["Red Mushroom",10,30,50,160,4590],
            "frogG": ["Frog",6,18,30,96,2754],
            "beanG": ["Bored Bean",7,21,35,112,3213],
            "slimeG": ["Slime", 8,24,40,128,3672],
            "snakeG": ["Baby Boa",9,27,45,144,4131],
            "carrot0": ["Carrot",10,30,50,160,4590],
            "goblinG": ["Goblin",10,30,50,160,4590],
            "plank": ["Plank",10,30,50,160,4590],
            "frogBIG": ["Giga Frog",10,30,50,160,4590],
            "poopSmall": ["Poop",10,30,50,160,4590],
            "ratB": ["Rat",10,30,50,160,4590],
            "branch": ["Stick",10,30,50,160,4590],
            "acorn": ["Acorn",10,30,50,160,4590],
            "Crystal0": ["Crystal Carrot",3,9,15,48,1377],
            "mushW": ["Wood Mushroom",10,30,50,160,4590]
        },
        "Yum-Yum Desert": {
            "jarSand": ["Sandy Pot",10,30,50,160,4590],
            "mimicA": ["Mimic",10,30,50,160,4590],
            "crapcake": ["Crabcake",10,30,50,160,4590],
            "coconut": ["Mafioso",10,30,50,160,4590],
            "sandcastle": ["Sandcastle",10,30,50,160,4590],
            "pincermin": ["Pincermin",10,30,50,160,4590],
            "potato": ["Mashed Potato",10,30,50,160,4590],
            "moonman": ["Moonman",10,30,50,160,4590],
            "sandgiant": ["Sand Giant",10,30,50,160,4590],
            "snailZ": ["Snelbie",10,30,50,160,4590],
            "shovelR": ["Dig Doug",10,30,50,160,4590],
            "Crystal1": ["Crystal Crabal",3,9,15,48,1377],
            "Bandit_Bob": ["Bandit Bob",1,3,5,16,459]
        },
        "Easy Resources": {
            "Copper": ["Copper Ore",10,30,50,160,4590],
            "Iron": ["Iron Ore",10,30,50,160,4590],
            "Gold": ["Gold Ore",10,30,50,160,4590],
            "ForgeA": ["Fire Forge",10,30,50,160,4590],
            "OakTree": ["Oak Logs",10,30,50,160,4590],
            "BirchTree": ["Bleach Logs",10,30,50,160,4590],
            "JungleTree": ["Jungle Logs",10,30,50,160,4590],
            "ForestTree": ["Forest Fibres",10,30,50,160,4590],
            "Fish1": ["Goldfish",10,30,50,160,4590],
            "Fish2": ["Hermit Can",10,30,50,160,4590],
            "Fish3": ["Jellyfish",10,30,50,160,4590],
            "Bug1": ["Fly",10,30,50,160,4590],
            "Bug2": ["Butterfly",10,30,50,160,4590]
        },
        "Medium Resources": {
    		"Plat": ["Platinum Ore",10,30,50,160,4590],
            "Dementia": ["Dementia Ore",10,30,50,160,4590],
            "Void": ["Void Ore",10,30,50,160,4590],
            "ForgeB": ["Cinder Forges",10,30,50,160,4590],
            "PalmTree": ["Tropilogs",10,30,50,160,4590],
            "ToiletTree": ["Potty Rolls",10,30,50,160,4590],
            "StumpTree": ["Veiny Logs",10,30,50,160,4590],
            "Fish4": ["Bloach",10,30,50,160,4590],
            "Bug3": ["Senient Cereal",10,30,50,160,4590],
            "Bug4": ["Fruitfly",10,30,50,160,4590],
            "SoulCard1": ["Forest Soul",39,15,48,1377],
            "SoulCard2": ["Dune Soul",39,15,48,1377],
            "CritterCard1": ["Froge",4,12,20,64,1836],
            "CritterCard2": ["Crabbo",4,12,20,64,1836],
            "CritterCard3": ["Scorpie",4,12,20,64,1836]
        },
        "Frostbite Tundra": {
            "sheep": ["Sheepie",11,33,55,176,5049],
            "flake": ["Snow Flake",12,36,60,192,5508],
            "stache": ["Stache",13,39,65,208,5967],
            "bloque": ["Bloque",14,42,70,224,6426],
            "mamoth": ["Mammoth",15,24,75,240,6885],
            "snowball": ["Snowball",15,45,75,240,6885],
            "penguin": ["Penguin",15,45,75,240,6885],
            "thermostat": ["Thermo",15,45,75,240,6885],
            "glass": ["Quenchie",17,51,85,272,7803],
            "snakeB": ["CryoSnake",17,51,85,272,7803],
            "speaker": ["Bop Box",17,51,85,272,7803],
            "eye": ["Neptuneye",17,51,85,272,7803],
            "ram": ["Dedotated Ram",20,60,100,320,9180],
            "skele": ["Xylobone",15,45,75,240,6885],
            "skele2": ["Bloodbones",15,45,75,240,6885],
            "Crystal2": ["Crystal Cattle",10,30,50,160,4590]
        },
        "Hard Resources": {
            "Lustre": ["Lustre Ore",10,30,50,160,4590],
            "Starfire": ["Starfire Ore",12,36,60,192,5508],
            "Dreadlo": ["Dreadlo Ore",15,45,75,240,6885],
            "SaharanFoal": ["Tundra Logs",10,30,50,160,4590],
            "Tree7": ["Wispy Lumber",10,30,50,160,4590],
            "AlienTree": ["Alien Hive Chunk",10,30,50,160,4590],
            "Tree8": ["Cubed Logs",10,30,50,160,4590],
            "Tree9": ["Maple Logs",12,36,60,192,5508],
            "Tree10": ["Dandielogs",15,45,75,240,6885],
            "Fish5": ["Skelefish",8,24,40,128,3672],
            "Fish6": ["Sand Shark",10,30,50,160,4590],
            "Fish7": ["Manta Ray",10,30,50,160,4590],
            "Fish8": ["Kraken",10,30,50,160,4590],
            "Bug5": ["Mosquisnow",10,30,50,160,4590],
            "Bug6": ["Flycicle",10,30,50,160,4590],
            "Bug7": ["Worker Bee",10,30,50,160,4590],
            "Bug8": ["Fairy",10,30,50,160,4590],
            "Bug9": ["Scarab",12,36,60,192,5508],
            "Bug10": ["Dust Mote",15,45,75,240,6885],
            "CritterCard4": ["Mousey",4,12,20,64,1836],
            "CritterCard5": ["Owlio",4,12,20,64,1836],
            "CritterCard6": ["Pingy",5,15,25,80,2295],
            "CritterCard7": ["Bunny",6,18,30,96,2754],
            "CritterCard8": ["Dung Beat",7,21,35,112,3213],
            "CritterCard9": ["Honker",9,27,45,144,4131],
            "CritterCard10": ["Blobfish",12,36,60,192,],
            "SoulCard3": ["Rooted Soul",3,9,15,48,1377],
            "SoulCard4": ["Frigid Soul",4,12,20,64,1836],
            "SoulCard5": ["Squishy Soul",5,15,25,80,2295],
            "SoulCard6": ["Oozie Soul",7,21,35,112,3213],
            "Fish9": ["Icefish",15,45,75,240,6885],
            "Fish10": ["Shellfish",18,54,90,288,8262],
            "Fish11": ["Jumbo Shrimp",24,72,120,384,11016],
            "Fish12": ["Caulifish",30,90,150,480,13770],
        },
        "Hyperion Nebula": {
            "mushP": ["Purple Mushroom",15,45,75,240,6885],
            "w4a2": ["TVs",17,51,85,272,7803],
            "w4a3": ["Donuts",18,54,90,288,8262],
            "demonP": ["Demon Genies",19,57,95,304,8721],
            "w4b2": ["Soda Cans",20,60,100,320,9180],
            "w4b1": ["Flying Worm",21,63,105,336,9639],
            "w4b3": ["Gelatinous Cuboid",22,66,110,352,10098],
            "w4b4": ["Choccie",23,69,115,368,10557],
            "w4b5": ["Biggole Worm",24,72,120,384,11016],
            "w4c1": ["Clammie",26,78,130,416,11934],
            "w4c2": ["Octodar",27,81,135,432,12393],
            "w4c3": ["Floms",28,84,140,448,12852],
            "w4c4": ["Stilted Seeker",30,90,150,480,13770],
            "Crystal3": ["Crystal Custard", 10,30,50,160,4590]
        },
        "Smolderin' Plateau": {
            "w5a1": ["Suggma",25,75,125,400,11475],
            "w5a2": ["Maccie",28,84,140,448,12852],
            "w5a3": ["Mister Brightside",32,96,160,512,14688],
            "w5a4": ["Cheese Nub",35,105,175,560,16065],
            "w5a5": ["Stiltmole",45,135,225,720,20655],
            "w5b1": ["Molti",48,144,240,768,22032],
            "w5b2": ["Puragtory Stalker",52,156,260,832,23868],
            "w5b3": ["Citringe",60,180,300,960,27540],
            "w5b4": ["Lampar",65,195,325,1040,29835],
            "w5b5": ["Fire Spirit",70,2210,350,1120,32130],
            "w5b6": ["Biggole Mole",75,225,375,1200,34425],
            "w5c1": ["Crawler",80,240,400,1280,36720],
            "w5c2": ["Tremor Wurms",100,300,500,1600,45900],
            "Crystal4": ["Crystal Capybara",15,45,75,240,6885]
        },
        "Dungeons": {
            "frogP": ["Poisonic Frog",2,4,8,24,688],
            "frogD": ["Globohopper",2,6,10,32,918],
            "frogY": ["King Frog",2,6,10,32,918],
            "frogR": ["Lava Slimer",2,6,10,32,918],
            "frogW": ["Chromatium Frog",3,9,15,48,1377],
            "frogGG": ["Eldritch Croaker",5,15,25,80,2295],
            "frogGR": ["Grandfrogger",2,4,8,24,688],
            "frogGR2": ["Rotting Grandfrogger",2,4,8,24,688],
            "frogGR3": ["Forlorn Grandfrogger",2,4,8,24,688],
            "frogGR4": ["Vengeful Grandfrogger",1,3,5,16,459],
            "target": ["Target Card",2,6,10,32,918],
            "rocky": ["Grumblo",2,6,10,32,918],
            "steakR": ["Beefie",2,6,10,32,918],
            "totem": ["Lazlo",2,6,10,32,918],
            "cactus": ["Cactopunk",2,6,10,32,918],
            "potatoB": ["Crescent Spud",5,15,25,80,2295],
            "snakeZ": ["Snakenhotep",2,4,8,24,688],
            "snakeZ2": ["Enraged Snakenhotep",2,4,8,24,688],
            "snakeZ3": ["Inevitable Snakenhotep",2,4,8,24,688],
            "iceknight": ["Ice Guard",8,24,40,128,3672],
            "iceBossZ": ["Glaciaxus",2,6,10,32,918],
            "iceBossZ2": ["Golden Glaciaxus",2,4,8,24,688],
            "iceBossZ3": ["Caustic Glaciaxus",2,4,8,24,688]
        },
        "Bosses n Nightmares": {
            "babayaga": ["Baba Yaga",2,4,8,24,688],
            "poopBig": ["Dr Defecaus",2,4,8,24,688],
            "poopD": ["Boop",1,3,5,16,459],
            "wolfA": ["Amarok",2,4,8,24,688],
            "wolfB": ["Chaotic Amarok",2,4,8,24,688],
            "wolfC": ["Radiant Amarok",10,30,50,160,4590],
            "babaHour": ["Biggie Hours",2,4,8,24,688],
            "babaMummy": ["King Doot",2,4,8,24,688],
            "Boss2A": ["Efaunt",2,4,8,24,688],
            "Boss2B": ["Chaotic Efaunt",2,4,8,24,688],
            "Boss2C": ["Gilded Efaunt",11,33,55,176,5049],
            "mini3a": ["Dilapidated Slush",5,15,25,80,2295],
            "Boss3A": ["Chizoar",2,4,8,24,688],
            "Boss3B": ["Chaotic Chizoar",2,4,8,24,16],
            "Boss3C": ["Blighted Chizoar",12,36,60,192,5508],
            "mini4a": ["Mutated Mush",5,15,25,90,2295],
            "Boss4A": ["Massive Troll",2,6,10,32,918],
            "Boss4B": ["Chaotic Troll",2,6,10,32,918],
            "Boss4C": ["Blitzkrieg Troll",4,12,20,64,1836],
            "Boss5A": ["Kattlecruk",3,9,15,48,1377],
            "Boss5B": ["Chaotic Kattlecruk",4,12,20,64,1836],
            "Boss5C": ["Sacrilegious Kattlecruk",5,15,25,80,2295]
        },
        "Events": {
            "ghost": ["Ghost (Event)",2,6,10,32,918],
            "xmasEvent": ["Giftmas Blobulyte",2,4,8,24,688],
            "xmasEvent2": ["Meaning of Giftmas",2,4,8,24,688],
            "slimeR": ["Valentslime",2,6,10,32,918],
            "loveEvent": ["Loveulyte",2,4,8,24,688],
            "loveEvent2": ["Chocco Box",2,4,8,24,688],
            "loveEvent3": ["Giant Rose",2,4,8,24,688],
            "sheepB": ["Floofie",3,9,15,48,1377],
            "snakeY": ["Shell Snake",3,9,15,48,1377],
            "EasterEvent1": ["Egggulyte",2,4,8,24,688],
            "EasterEvent2": ["Egg Capsule",2,4,8,24,688],
            "shovelY": ["Plasti Doug",4,12,20,64,1836],
            "crabcakeB": ["Mr Blueberry",4,12,20,64,1836],
            "SummerEvent1": ["Coastiolyte",8,24,40,128,3672],
            "SummerEvent2": ["Summer Spirit",8,24,40,128,3672],
            "xmasEvent3": ["Golden Giftmas",1,3,5,16,459],
            "springEvent1": ["Bubbulyte",1,3,5,16,459],
            "springEvent2": ["Spring Splendor",1,3,5,16,459],
            "fallEvent1": ["Falloween Pumpkin",3,9,15,48,1377]
        }
    }
    rawCardsData = inputJSON["Cards0"]
    playerCardsToNextLevelDict = {
        }
    print("Cards.getCardSetReview~ INFO rawCardsData:", type(rawCardsData))

    #Build playerCard cardSets
    for cardSet in cardRequirementsDict:
        playerCardsToNextLevelDict[cardSet] = {"Total": 0}
        for card in cardRequirementsDict[cardSet]:
            playerCardsToNextLevelDict[cardSet][card] = {
                "CardName": cardRequirementsDict[card][0],
                "CardsToNextLevel": 1,
                "CardLevel": 0,
                "NextLevelName": "Normal"}

    for card in rawCardsData:
        #card {"stache":18612}
        for cardSet in cardRequirementsDict:
            #cardSet "Frostbite Tundra": {"stache": {...}, ...}
            if card in cardRequirementsDict[cardSet]:
                #if card already Ruby:
                if rawCardsData[cardSet][card] >= cardRequirementsDict[card][5]:
                    playerCardsToNextLevelDict[cardSet][card]["CardsToNextLevel"] = 0
                    playerCardsToNextLevelDict[cardSet][card]["NextLevelName"] = "None"
                    playerCardsToNextLevelDict[cardSet][card]["CardLevel"] = 6
                    playerCardsToNextLevelDict[cardSet]["Total"] += 6
                #if card already Platinum:
                elif rawCardsData[cardSet][card] >= cardRequirementsDict[card][4]:
                    playerCardsToNextLevelDict[cardSet][card]["CardsToNextLevel"] = cardRequirementsDict[card][5]-rawCardsData[cardSet][card]
                    playerCardsToNextLevelDict[cardSet][card]["NextLevelName"] = "Ruby"
                    playerCardsToNextLevelDict[cardSet][card]["CardLevel"] = 5
                    playerCardsToNextLevelDict[cardSet]["Total"] += 5
                #if card already Gold:
                elif rawCardsData[cardSet][card] >= cardRequirementsDict[card][3]:
                    playerCardsToNextLevelDict[cardSet][card]["CardsToNextLevel"] = cardRequirementsDict[card][4]-rawCardsData[cardSet][card]
                    playerCardsToNextLevelDict[cardSet][card]["NextLevelName"] = "Platinum"
                    playerCardsToNextLevelDict[cardSet][card]["CardLevel"] = 4
                    playerCardsToNextLevelDict[cardSet]["Total"] += 4
                #if card already Silver:
                elif rawCardsData[cardSet][card] >= cardRequirementsDict[card][2]:
                    playerCardsToNextLevelDict[cardSet][card]["CardsToNextLevel"] = cardRequirementsDict[card][3]-rawCardsData[cardSet][card]
                    playerCardsToNextLevelDict[cardSet][card]["NextLevelName"] = "Gold"
                    playerCardsToNextLevelDict[cardSet][card]["CardLevel"] = 3
                    playerCardsToNextLevelDict[cardSet]["Total"] += 3
                #if card already Bronze:
                elif rawCardsData[cardSet][card] >= cardRequirementsDict[card][1]:
                    playerCardsToNextLevelDict[cardSet][card]["CardsToNextLevel"] = cardRequirementsDict[card][2]-rawCardsData[cardSet][card]
                    playerCardsToNextLevelDict[cardSet][card]["NextLevelName"] = "Silver"
                    playerCardsToNextLevelDict[cardSet][card]["CardLevel"] = 2
                    playerCardsToNextLevelDict[cardSet]["Total"] += 2
                #if card already Normal:
                elif rawCardsData[cardSet][card] >= 1:
                    playerCardsToNextLevelDict[cardSet][card]["CardsToNextLevel"] = cardRequirementsDict[card][1]-rawCardsData[cardSet][card]
                    playerCardsToNextLevelDict[cardSet][card]["NextLevelName"] = "Bronze"
                    playerCardsToNextLevelDict[cardSet][card]["CardLevel"] = 1
                    playerCardsToNextLevelDict[cardSet]["Total"] += 1

    for cardSet in playerCardsToNextLevelDict:
        print("Cards.getCardSetReview~ OUTPUT CardSet Totals:", cardSet, playerCardsToNextLevelDict[cardSet]["Total"])
