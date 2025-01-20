from consts import deathNote_progressionTiers, cookingCloseEnough, break_you_best, apocDifficultyNameList, currentWorld, apocNamesList
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

def getAllKillsDisplaySubgroupedByWorldAdviceGroup():
    advices = {}
    ags = []
    apocName = apocNamesList[-1]
    difficultyName = apocDifficultyNameList[-2]
    #logger.debug(f"apocCharactersIndexList: {session_data.account.apocCharactersIndexList}")
    for characterIndex in session_data.account.apocCharactersIndexList:
        toon = session_data.account.all_characters[characterIndex]
        #logger.debug(f"Generating AdviceGroup for: {toon.character_name}")
        advices[toon.character_name] = {
            "Scattered Extras": [],
            "World 1": [],
            "World 2": [],
            "World 3": [],
            "World 4": [],
            "World 5": [],
            "World 6": [],
            #"World 7": [],
            #"World 8": [],
        }
        for enemy in toon.apoc_dict[apocName][difficultyName]:
            subgroupName = f"World {enemy[4]}" if enemy[4] != 0 else f"Scattered Extras"
            advices[toon.character_name][subgroupName].append(
                Advice(
                    label=enemy[0],
                    picture_class=enemy[3],
                    goal=f"{enemy[1]:,}"),
            )
    for toon_name, toon_advice_list in advices.items():
        ags.append(AdviceGroup(
            tier="",
            pre_string=f"Informational- All kills for {toon_name} without a filter. Have fun",
            advices=toon_advice_list,
            informational=True,
            completed=True
        ))
    return ags

def getDeathNoteProgressionTiersAdviceGroup():
    deathnote_AdviceDict = {
        "W1": [],
        "W2": [],
        "W3": [],
        "W4": [],
        "W5": [],
        "W6": [],
        "ZOW": {},
        "CHOW": {},
        "MEOW": {},
        "WOW": {}
    }
    infoTiers = 2
    max_tier = deathNote_progressionTiers[-1][0] - infoTiers
    worldIndexes = []
    tier_combo = {}
    for number in range(1, currentWorld + 1):
        worldIndexes.append(number)
        tier_combo[number] = 0
    tier_combo['ZOW'] = 0
    tier_combo['CHOW'] = 0
    tier_combo['MEOW'] = 0
    tier_combo['WOW'] = 0
    apocToNextTier = {
        'ZOW': 0,
        'CHOW': 0,
        'MEOW': 0,
        'WOW': 0
    }
    zowsForNextTier = 0
    chowsForNextTier = 0
    meowsForNextTier = 0
    wowsForNextTier = 0

    # Just shortening the paths
    apocCharactersIndexList = session_data.account.apocCharactersIndexList
    apocalypse_character_Index = session_data.account.apocalypse_character_Index
    fullDeathNoteDict = session_data.account.enemy_worlds

    highestZOWCount = 0
    highestZOWCountIndex = None
    highestCHOWCount = 0
    highestCHOWCountIndex = None
    highestWOWCount = 0
    highestWOWCountIndex = None
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
        if session_data.account.all_characters[barbIndex].apoc_dict['WOW']['Total'] > highestWOWCount:
            highestWOWCount = session_data.account.all_characters[barbIndex].apoc_dict['WOW']['Total']
            highestWOWCountIndex = barbIndex

    # Assess Tiers
    for tier in deathNote_progressionTiers:
        # tier[0] = int tier
        # tier[1] = int w1LowestSkull
        # tier[2] = int w2LowestSkull
        # tier[3] = int w3LowestSkull
        # tier[4] = int w4LowestSkull
        # tier[5] = int w5LowestSkull
        # tier[6] = int w6LowestSkull
        # tier[7] = int w7LowestSkull
        # tier[8] = int w8LowestSkull
        # tier[9] = int zowCount
        # tier[10] = int chowCount
        # tier[11] = int meowCount
        # tier[12] = int wowCount
        # tier[13] = str Notes

        # Basic Worlds
        for worldIndex in worldIndexes:
            if tier_combo[worldIndex] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
                if fullDeathNoteDict[worldIndex].lowest_skull_value >= tier[worldIndex]:
                    tier_combo[worldIndex] = tier[0]
                else:
                    for enemy in fullDeathNoteDict[worldIndex].lowest_skulls_dict[fullDeathNoteDict[worldIndex].lowest_skull_value]:
                        deathnote_AdviceDict[f"W{worldIndex}"].append(Advice(
                            label=enemy[0],
                            picture_class=enemy[3],
                            progression=enemy[2],
                            goal=100,
                            unit='%'
                        ))

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
                                deathnote_AdviceDict["ZOW"][difficultyName].append(Advice(
                                    label=enemy[0],
                                    picture_class=enemy[3],
                                    progression=enemy[2],
                                    goal=100,
                                    unit='%'
                                ))
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
                                deathnote_AdviceDict["CHOW"][difficultyName].append(Advice(
                                    label=enemy[0],
                                    picture_class=enemy[3],
                                    progression=enemy[2],
                                    goal=100,
                                    unit='%'
                                ))
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
                if apocalypse_character_Index is not None:
                    if session_data.account.all_characters[apocalypse_character_Index].apoc_dict['MEOW']['Total'] >= tier[11]:
                        tier_combo['MEOW'] = tier[0]
                    else:
                        meowsForNextTier = f"({session_data.account.all_characters[apocalypse_character_Index].apoc_dict['MEOW']['Total']}/{tier[11]})"
                        apocToNextTier['MEOW'] = tier[11] - session_data.account.all_characters[apocalypse_character_Index].apoc_dict['MEOW']['Total']
                        for difficultyName in apocDifficultyNameList:
                            if len(session_data.account.all_characters[apocalypse_character_Index].apoc_dict['MEOW'][difficultyName]) > 0:
                                if difficultyName not in deathnote_AdviceDict['MEOW']:
                                    deathnote_AdviceDict['MEOW'][difficultyName] = []
                                for enemy in session_data.account.all_characters[apocalypse_character_Index].apoc_dict['MEOW'][difficultyName]:
                                    deathnote_AdviceDict["MEOW"][difficultyName].append(Advice(
                                        label=enemy[0],
                                        picture_class=enemy[3],
                                        progression=enemy[2],
                                        goal=100,
                                        unit='%'
                                    ))
                else:
                    deathnote_AdviceDict["MEOW"] = [
                        Advice(
                            label="Create a Blood Berserker",
                            picture_class="blood-berserker-icon",
                            progression=0,
                            goal=1)
                    ]

        # WOW
        if tier_combo['WOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highestWOWCount >= tier[12]:
                tier_combo['WOW'] = tier[0]
            else:
                wowsForNextTier = f"({highestWOWCount}/{tier[12]})"
                if highestWOWCountIndex is not None:
                    apocToNextTier['WOW'] = tier[12] - highestWOWCount
                    for difficultyName in apocDifficultyNameList:
                        if len(session_data.account.all_characters[highestWOWCountIndex].apoc_dict['WOW'][difficultyName]) > 0:
                            if difficultyName not in deathnote_AdviceDict['WOW']:
                                deathnote_AdviceDict['WOW'][difficultyName] = []
                            for enemy in session_data.account.all_characters[highestWOWCountIndex].apoc_dict['WOW'][difficultyName]:
                                deathnote_AdviceDict["WOW"][difficultyName].append(Advice(
                                    label=enemy[0],
                                    picture_class=enemy[3],
                                    progression=enemy[2],
                                    goal=100,
                                    unit='%'
                                ))
                else:
                    deathnote_AdviceDict["WOW"] = [
                        Advice(
                            label="Create a Death Bringer",
                            picture_class="death-bringer-icon",
                            progression=0,
                            goal=1)
                    ]

    # If the player is basically finished with cooking, bypass the requirement while still showing the progress
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        if tier_combo['ZOW'] < max_tier + infoTiers:
            tier_combo['ZOW'] = max_tier + infoTiers
        if tier_combo['CHOW'] < max_tier + infoTiers:
            tier_combo['CHOW'] = max_tier + infoTiers
        if tier_combo['MEOW'] < max_tier + infoTiers:
            tier_combo['MEOW'] = max_tier + infoTiers
        if tier_combo['WOW'] < max_tier + infoTiers:
            tier_combo['WOW'] = max_tier + infoTiers

    # Generate Advice Groups
    deathnote_AdviceGroupDict = {}
    # Basic Worlds
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
            post_string="Aim for 12hrs or less (8k+ KPH) per enemy",
            informational=True if tier_combo['ZOW'] >= max_tier else False
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
            post_string="Aim for 12hrs or less (83k+ KPH) per enemy",
            informational=True if tier_combo['CHOW'] >= max_tier else False
        )
    else:
        deathnote_AdviceGroupDict['CHOW'] = AdviceGroup(
            tier=str(tier_combo['CHOW'] if tier_combo['CHOW'] < max_tier else ""),
            pre_string=f"CHOW Progress unavailable until a Blood Berserker is found in your account",
            advices=deathnote_AdviceDict['CHOW'],
        )

    # MEOW
    if apocalypse_character_Index is not None:
        deathnote_AdviceGroupDict['MEOW'] = AdviceGroup(
            tier=str(tier_combo['MEOW'] if tier_combo['MEOW'] < max_tier else ""),
            pre_string=f"{'Informational- You could complete' if tier_combo['MEOW'] >= max_tier else 'Complete'} {apocToNextTier['MEOW']} more"
                       f" Super CHOW{pl(apocToNextTier['MEOW'])} with {session_data.account.all_characters[apocalypse_character_Index].character_name} {meowsForNextTier}",
            advices=deathnote_AdviceDict['MEOW'],
            post_string=f"Aim for 24hrs or less (4m+ KPH) per enemy",
            informational=True if tier_combo['MEOW'] >= max_tier else False
        )
    else:
        deathnote_AdviceGroupDict['MEOW'] = AdviceGroup(
            tier=str(tier_combo['MEOW'] if tier_combo['MEOW'] < max_tier else ""),
            pre_string=f"Super CHOW Progress unavailable until a Blood Berserker is found in your account",
            advices=deathnote_AdviceDict['MEOW'],
        )

    # WOW
    if apocalypse_character_Index is not None:
        deathnote_AdviceGroupDict['WOW'] = AdviceGroup(
            tier=str(tier_combo['WOW'] if tier_combo['WOW'] < max_tier else ""),
            pre_string=f"{'Informational- You could complete' if tier_combo['WOW'] >= max_tier else 'Complete'} {apocToNextTier['WOW']} more"
                       f" WOW{pl(apocToNextTier['WOW'])} with {session_data.account.all_characters[apocalypse_character_Index].character_name} {wowsForNextTier}",
            advices=deathnote_AdviceDict['WOW'],
            informational=True if tier_combo['WOW'] >= max_tier else False
        )
    else:
        deathnote_AdviceGroupDict['WOW'] = AdviceGroup(
            tier=str(tier_combo['WOW'] if tier_combo['MEOW'] < max_tier else ""),
            pre_string=f"Super CHOW Progress unavailable until a Blood Berserker is found in your account",
            advices=deathnote_AdviceDict['WOW'],
        )

    if apocalypse_character_Index is not None:
        all_kills_ags = getAllKillsDisplaySubgroupedByWorldAdviceGroup()
        for ag in all_kills_ags:
            deathnote_AdviceGroupDict[ag.pre_string] = ag

    overall_SectionTier = min(
        max_tier + infoTiers, min(tier_combo.values())
        # tier_combo[1], tier_combo[2], tier_combo[3],
        # tier_combo[4], tier_combo[5], tier_combo[6],
        # tier_combo['ZOW'], tier_combo['CHOW'], tier_combo['MEOW'], tier_combo['WOW']
    )
    return deathnote_AdviceGroupDict, overall_SectionTier, max_tier


def getDeathNoteAdviceSection() -> AdviceSection:
    #highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if session_data.account.construction_buildings['Death Note']['Level'] < 1:
        deathnote_AdviceSection = AdviceSection(
            name="Death Note",
            tier="",
            header=f"Come back after unlocking the Death Note within the Construction skill in World 3!",
            picture="Construction_Death_Note.png",
            unreached=True
        )
        return deathnote_AdviceSection

    #Generate AdviceGroups
    deathnote_AdviceGroupDict, overall_SectionTier, max_tier = getDeathNoteProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    deathnote_AdviceSection = AdviceSection(
        name="Death Note",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Death Note tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Construction_Death_Note.png",
        groups=deathnote_AdviceGroupDict.values()
    )
    if len(session_data.account.bbCharactersIndexList) > 1:
        deathnote_AdviceSection.note = "Important! As of February 2024, Super CHOWs only give benefit if completed on your 2nd Blood Berserker regardless of the platform you play on."

    return deathnote_AdviceSection
