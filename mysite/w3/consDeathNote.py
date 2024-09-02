from consts import deathNote_progressionTiers, cookingCloseEnough, break_you_best, apocDifficultyNameList, currentWorld
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

def setConsDeathNoteProgressionTier():
    deathnote_AdviceDict = {
        "W1": [],
        "W2": [],
        "W3": [],
        "W4": [],
        "W5": [],
        "W6": [],
        "ZOW": {},
        "CHOW": {},
        "MEOW": {}
    }

    deathnote_AdviceGroupDict = {}
    deathnote_AdviceSection = AdviceSection(
        name="Death Note",
        tier="",
        header="Recommended Death Note actions",
        picture="Construction_Death_Note.png"
    )
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        deathnote_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return deathnote_AdviceSection
    elif session_data.account.construction_buildings['Death Note']['Level'] < 1:
        deathnote_AdviceSection.header = "Come back after unlocking the Death Note within the Construction skill in World 3!"
        return deathnote_AdviceSection

    # Just shortening the paths
    apocCharactersIndexList = session_data.account.apocCharactersIndexList
    bbCharactersIndexList = session_data.account.bbCharactersIndexList
    meowBBIndex = session_data.account.meowBBIndex
    fullDeathNoteDict = session_data.account.enemy_worlds

    infoTiers = 2
    max_tier = deathNote_progressionTiers[-1][0] - infoTiers  #Final 2 tiers are info only
    overall_DeathNoteTier = 0
    worldIndexes = []
    tier_combo = {}
    for number in range(1, currentWorld + 1):
        worldIndexes.append(number)
        tier_combo[number] = 0
    tier_combo['ZOW'] = 0
    tier_combo['CHOW'] = 0
    tier_combo['MEOW'] = 0
    apocToNextTier = {
        'ZOW': 0,
        'CHOW': 0,
        'MEOW': 0
    }
    zowsForNextTier = 0
    chowsForNextTier = 0
    meowsForNextTier = 0

    highestZOWCount = 0
    highestZOWCountIndex = None
    highestCHOWCount = 0
    highestCHOWCountIndex = None
    for barbIndex in apocCharactersIndexList:
        if highestZOWCountIndex is None:
            highestZOWCountIndex = barbIndex
        if highestCHOWCountIndex is None:
            highestCHOWCountIndex = barbIndex
        if session_data.account.all_characters[barbIndex].apoc_dict['ZOW']['Total'] > highestZOWCount:
            highestZOWCount = session_data.account.all_characters[barbIndex].apoc_dict['ZOW']['Total']
            highestZOWCountIndex = barbIndex
        if session_data.account.all_characters[barbIndex].apoc_dict['CHOW']['Total'] > highestCHOWCount:
            highestCHOWCount = session_data.account.all_characters[barbIndex].apoc_dict['CHOW']['Total']
            highestCHOWCountIndex = barbIndex

    #assess tiers
    for tier in deathNote_progressionTiers:
        #tier[0] = int tier
        #tier[1] = int w1LowestSkull
        #tier[2] = int w2LowestSkull
        #tier[3] = int w3LowestSkull
        #tier[4] = int w4LowestSkull
        #tier[5] = int w5LowestSkull
        #tier[6] = int w6LowestSkull
        #tier[7] = int w7LowestSkull
        #tier[8] = int w8LowestSkull
        #tier[9] = int zowCount
        #tier[10] = int chowCount
        #tier[11] = int meowCount
        #tier[12] = str Notes

        # Basic Worlds
        for worldIndex in worldIndexes:
            if tier_combo[worldIndex] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
                if fullDeathNoteDict[worldIndex].lowest_skull_value >= tier[worldIndex]:
                    tier_combo[worldIndex] = tier[0]
                else:
                    for enemy in fullDeathNoteDict[worldIndex].lowest_skulls_dict[fullDeathNoteDict[worldIndex].lowest_skull_value]:
                        deathnote_AdviceDict[f"W{worldIndex}"].append(
                            Advice(
                                label=enemy[0],
                                picture_class=enemy[3],
                                progression=f"{enemy[2]}%")
                        )

        # ZOW
        if tier_combo['ZOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highestZOWCount >= tier[9]:
                tier_combo['ZOW'] = tier[0]
            else:
                zowsForNextTier = f"({highestZOWCount}/{tier[9]})"
                if highestZOWCountIndex is not None:
                    apocToNextTier['ZOW'] = tier[9] - highestZOWCount
                    for difficultyName in apocDifficultyNameList:
                        if len(session_data.account.all_characters[highestZOWCountIndex].apoc_dict['ZOW'][difficultyName]) > 0:
                            if difficultyName not in deathnote_AdviceDict['ZOW']:
                                deathnote_AdviceDict['ZOW'][difficultyName] = []
                            for enemy in session_data.account.all_characters[highestZOWCountIndex].apoc_dict['ZOW'][difficultyName]:
                                deathnote_AdviceDict["ZOW"][difficultyName].append(
                                    Advice(
                                        label=enemy[0],
                                        picture_class=enemy[3],
                                        progression=f"{enemy[2]}%"),
                                )
                else:
                    deathnote_AdviceDict["ZOW"] = [
                        Advice(
                            label="Create a Barbarian",
                            picture_class="barbarian-icon",
                            progression=0,
                            goal=1)
                    ]
        # CHOW
        if tier_combo['CHOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highestCHOWCount >= tier[10]:
                tier_combo['CHOW'] = tier[0]
            else:
                chowsForNextTier = f"({highestCHOWCount}/{tier[10]})"
                if highestCHOWCountIndex is not None:
                    apocToNextTier['CHOW'] = tier[10] - highestCHOWCount
                    for difficultyName in apocDifficultyNameList:
                        if len(session_data.account.all_characters[highestCHOWCountIndex].apoc_dict['CHOW'][difficultyName]) > 0:
                            if difficultyName not in deathnote_AdviceDict['CHOW']:
                                deathnote_AdviceDict['CHOW'][difficultyName] = []
                            for enemy in session_data.account.all_characters[highestCHOWCountIndex].apoc_dict['CHOW'][difficultyName]:
                                deathnote_AdviceDict["CHOW"][difficultyName].append(
                                    Advice(
                                        label=enemy[0],
                                        picture_class=enemy[3],
                                        progression=f"{enemy[2]}%"),
                                    )
                else:
                    deathnote_AdviceDict["CHOW"] = [
                        Advice(
                            label="Create a Blood Berserker",
                            picture_class="blood-berserker-icon",
                            progression=0,
                            goal=1)
                    ]
        # MEOW
        if tier_combo['MEOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if tier[11] == 0:
                tier_combo['MEOW'] = tier[0]
            else:
                if meowBBIndex is not None:
                    if session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW']['Total'] >= tier[11]:
                        tier_combo['MEOW'] = tier[0]
                    else:
                        meowsForNextTier = f"({session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW']['Total']}/{tier[11]})"
                        apocToNextTier['MEOW'] = tier[11] - session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW']['Total']
                        for difficultyName in apocDifficultyNameList:
                            if len(session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW'][difficultyName]) > 0:
                                if difficultyName not in deathnote_AdviceDict['MEOW']:
                                    deathnote_AdviceDict['MEOW'][difficultyName] = []
                                for enemy in session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW'][difficultyName]:
                                    deathnote_AdviceDict["MEOW"][difficultyName].append(
                                        Advice(
                                            label=enemy[0],
                                            picture_class=enemy[3],
                                            progression=f"{enemy[2]}%"),
                                        )
                else:
                    deathnote_AdviceDict["MEOW"] = [
                        Advice(
                            label="Create a Blood Berserker",
                            picture_class="blood-berserker-icon",
                            progression=0,
                            goal=1)
                    ]

    #If the player is basically finished with cooking, bypass the requirement while still showing the progress
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        if tier_combo['ZOW'] < max_tier + infoTiers:
            tier_combo['ZOW'] = max_tier + infoTiers
        if tier_combo['CHOW'] < max_tier + infoTiers:
            tier_combo['CHOW'] = max_tier + infoTiers
        if tier_combo['MEOW'] < max_tier + infoTiers:
            tier_combo['MEOW'] = max_tier + infoTiers

    #Generate Advice Groups
    #Basic Worlds
    for worldIndex in worldIndexes:
        deathnote_AdviceGroupDict[f"W{worldIndex}"] = AdviceGroup(
            tier=str(tier_combo[worldIndex]),
            pre_string=f"Kill more W{worldIndex} enemies to reach a minimum skull of {fullDeathNoteDict[worldIndex].next_lowest_skull_name}",
            advices=deathnote_AdviceDict[f"W{worldIndex}"],
            post_string=""
        )

    # ZOW
    if highestZOWCountIndex is not None:
        deathnote_AdviceGroupDict['ZOW'] = AdviceGroup(
            tier=str(tier_combo['ZOW'] if tier_combo['ZOW'] < max_tier else ""),
            pre_string=f"{'Informational- You could complete' if tier_combo['ZOW'] >= max_tier else 'Complete'} {apocToNextTier['ZOW']} more"
                       f" ZOW{pl(apocToNextTier['ZOW'])} with {session_data.account.all_characters[highestZOWCountIndex].character_name} {zowsForNextTier}",
            advices=deathnote_AdviceDict['ZOW'],
            post_string="Aim for 12hrs or less (8k+ KPH) per enemy"
        )
    else:
        deathnote_AdviceGroupDict['ZOW'] = AdviceGroup(
            tier=str(tier_combo['ZOW'] if tier_combo['ZOW'] < max_tier else ""),
            pre_string=f"ZOW Progress unavailable until a Barbarian is found in your account",
            advices=deathnote_AdviceDict['ZOW'],
        )

    # CHOW
    if highestCHOWCountIndex is not None:
        deathnote_AdviceGroupDict['CHOW'] = AdviceGroup(
            tier=str(tier_combo['CHOW'] if tier_combo['CHOW'] < max_tier else ""),
            pre_string=f"{'Informational- You could complete' if tier_combo['CHOW'] >= max_tier else 'Complete'} {apocToNextTier['CHOW']} more"
                       f" CHOW{pl(apocToNextTier['CHOW'])} with {session_data.account.all_characters[highestCHOWCountIndex].character_name} {chowsForNextTier}",
            advices=deathnote_AdviceDict['CHOW'],
            post_string="Aim for 12hrs or less (83k+ KPH) per enemy"
        )
    else:
        deathnote_AdviceGroupDict['CHOW'] = AdviceGroup(
            tier=str(tier_combo['CHOW'] if tier_combo['CHOW'] < max_tier else ""),
            pre_string=f"CHOW Progress unavailable until a Blood Berserker is found in your account",
            advices=deathnote_AdviceDict['CHOW'],
        )

    # MEOW
    if meowBBIndex is not None:
        deathnote_AdviceGroupDict['MEOW'] = AdviceGroup(
            tier=str(tier_combo['MEOW'] if tier_combo['MEOW'] < max_tier else ""),
            pre_string=f"{'Informational- You could complete' if tier_combo['MEOW'] >= max_tier else 'Complete'} {apocToNextTier['MEOW']} more"
                       f" Super CHOW{pl(apocToNextTier['MEOW'])} with {session_data.account.all_characters[meowBBIndex].character_name} {meowsForNextTier}",
            advices=deathnote_AdviceDict['MEOW'],
            post_string=f"Aim for 24hrs or less (4m+ KPH) per enemy"
        )
    else:
        deathnote_AdviceGroupDict['MEOW'] = AdviceGroup(
            tier=str(tier_combo['MEOW'] if tier_combo['MEOW'] < max_tier else ""),
            pre_string=f"Super CHOW Progress unavailable until a Blood Berserker is found in your account",
            advices=deathnote_AdviceDict['MEOW'],
        )

    #Generate Advice Section
    if len(bbCharactersIndexList) > 1:
        deathnote_AdviceSection.note = "Important! As of February 2024, Super CHOWs only give benefit if completed on your 2nd Blood Berserker regardless of the platform you play on."
    overall_DeathNoteTier = min((max_tier + infoTiers), tier_combo[1], tier_combo[2], tier_combo[3],
                                tier_combo[4], tier_combo[5], tier_combo[6],
                                tier_combo['ZOW'], tier_combo['CHOW'], tier_combo['MEOW'])  #tier_zows, tier_chows, tier_meows

    tier_section = f"{overall_DeathNoteTier}/{max_tier}"
    deathnote_AdviceSection.tier = tier_section
    deathnote_AdviceSection.pinchy_rating = overall_DeathNoteTier
    deathnote_AdviceSection.groups = deathnote_AdviceGroupDict.values()
    if overall_DeathNoteTier >= max_tier:
        deathnote_AdviceSection.header = f"Best Death Note tier met: {tier_section}{break_you_best}"
        deathnote_AdviceSection.complete = True
    else:
        deathnote_AdviceSection.header = f"Best Death Note tier met: {tier_section}"

    return deathnote_AdviceSection
