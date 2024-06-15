from typing import Dict

from flask import g as session_data
from consts import maxStaticBookLevels, maxScalingBookLevels, maxSummoningBookLevels, maxOverallBookLevels, skill_talentsDict, combat_talentsDict
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger

logger = get_logger(__name__)

def getBookLevelAdviceGroup() -> AdviceGroup:
    bookLevelAdvices = {}

    #Static Sources
    staticSubgroup = f"Static Sources: +{session_data.account.library['StaticSum']}/{maxStaticBookLevels}"
    bookLevelAdvices[staticSubgroup] = []

    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Construction: Talent Book Library built: +{25 * (0 < session_data.account.construction_buildings.get('Talent Book Library', 0))}",
        picture_class="talent-book-library",
        progression=min(1, session_data.account.construction_buildings.get('Talent Book Library', 0)),
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"W3 Achievement: Checkout Takeout: +{5 * (0 < session_data.account.achievements.get('Checkout Takeout', False))}",
        picture_class="checkout-takeout",
        progression=1 if session_data.account.achievements.get('Checkout Takeout', False) else 0,
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Atom Collider: Oxygen: +{10 * (0 < session_data.account.atoms.get('Oxygen - Library Booker', 0))}",
        picture_class="oxygen",
        progression=1 if 0 < session_data.account.atoms.get('Oxygen - Library Booker', 0) else 0,
        goal=1
    ))
    if not session_data.account.rift['EldritchArtifacts'] and session_data.account.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0) == 2:
        furyPostString = ". Eldritch Artifacts are unlocked by reaching {{ Rift|#rift }} 31"
    elif not session_data.account.sneaking['JadeEmporium']["Sovereign Artifacts"]['Obtained'] and session_data.account.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0) == 3:
        furyPostString = ". Sovereign Artifacts are unlocked from the {{ Jade Emporium|#sneaking }}"
    else:
        furyPostString = ""
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"{{{{ Artifact|#sailing }}}}: Fury Relic: +{25 * session_data.account.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0)}{furyPostString}",
        picture_class="fury-relic",
        progression=session_data.account.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0),
        goal=4
    ))

    #Scaling Sources
    scalingSubgroup = f"Scaling Sources: +{session_data.account.library['ScalingSum']}/{maxScalingBookLevels}"
    bookLevelAdvices[scalingSubgroup] = []

    bookLevelAdvices[scalingSubgroup].append(Advice(
        label=f"W3 Max Book level Merit: +{2 * session_data.account.merits[2][2]['Level']}",
        picture_class="merit-2-2",
        progression=session_data.account.merits[2][2]["Level"],
        goal=session_data.account.merits[2][2]["MaxLevel"]
    ))
    bookLevelAdvices[scalingSubgroup].append(Advice(
        label=f"{{{{Salt Lick|#salt-lick }}}}: +{2 * session_data.account.saltlick.get('Max Book', 0)}",
        picture_class="salt-lick",
        progression=session_data.account.saltlick.get('Max Book', 0),
        goal=10
    ))

    #Summoning Sources
    summoningSubgroup = f"Summoning Winner Bonus: +{session_data.account.library['SummoningSum']}/{maxSummoningBookLevels}"
    bookLevelAdvices[summoningSubgroup] = []
    cyan14beat = 'w6d3' in session_data.account.summoning['BattlesWon']
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"Summoning match Cyan14: +{10.5 * cyan14beat}{'' if cyan14beat else '. No other multipliers apply until this is beaten.'}",
        picture_class="samurai-guardian",
        progression=1 if cyan14beat else 0,
        goal=1
    ))
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        bookLevelAdvices[summoningSubgroup].append(advice)

    for group_name in bookLevelAdvices:
        for advice in bookLevelAdvices[group_name]:
            mark_advice_completed(advice)

    bookLevelAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of Max Book Levels ({session_data.account.library['MaxBookLevel']}/{maxOverallBookLevels})",
        advices=bookLevelAdvices
    )
    return bookLevelAdviceGroup

def getCharacterBooksAdviceGroups() -> dict:
    character_adviceDict = {}
    character_AdviceGroupDict = {}


    for toon in session_data.account.safe_characters:
        character_adviceDict[toon.character_name] = {}
        talentNumbersAdded = []

        #Skilling
        for skillName in skill_talentsDict.keys():
            for talentNumber, talentDetailsDict in skill_talentsDict[skillName].items():
                if skillName == "Utility" or skillName in toon.specialized_skills:
                    goal_level = talentDetailsDict.get('Optimal', 9999) if talentDetailsDict.get('Optimal', 9999) < session_data.account.library[
                        'MaxBookLevel'] else session_data.account.library['MaxBookLevel']
                    if 0 < toon.max_talents.get(str(talentNumber), 0) < goal_level and talentNumber not in talentNumbersAdded:
                        if 'Skilling' not in character_adviceDict[toon.character_name]:
                            character_adviceDict[toon.character_name]['Skilling'] = []
                        character_adviceDict[toon.character_name]['Skilling'].append(Advice(
                            label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                            picture_class=talentDetailsDict['Name'],
                            progression=toon.max_talents.get(str(talentNumber), 0),
                            goal=goal_level
                        ))
                        talentNumbersAdded.append(talentNumber)

        #Combat / Other
        for className in combat_talentsDict.keys():
            if className == toon.class_name:  #Only check recommendations for their CURRENT class
                for talentNumber, talentDetailsDict in combat_talentsDict[className].items():
                    goal_level = talentDetailsDict.get('Optimal', 9999) if talentDetailsDict.get('Optimal', 9999) < session_data.account.library[
                        'MaxBookLevel'] else session_data.account.library['MaxBookLevel']
                    if 0 < toon.max_talents.get(str(talentNumber), 0) < goal_level and talentNumber not in talentNumbersAdded:
                        if 'Combat' not in character_adviceDict[toon.character_name]:
                            character_adviceDict[toon.character_name]['Combat'] = []
                        character_adviceDict[toon.character_name]['Combat'].append(Advice(
                            label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                            picture_class=talentDetailsDict['Name'],
                            progression=toon.max_talents.get(str(talentNumber), 0),
                            goal=goal_level
                        ))
                        talentNumbersAdded.append(talentNumber)

        #Create AdviceGroup before moving on to next character
        character_AdviceGroupDict[toon.character_name] = AdviceGroup(
            tier="",
            pre_string=f"Priority Checkouts for {toon.character_name} the {toon.class_name}",
            advices=character_adviceDict[toon.character_name]
        )

    return character_AdviceGroupDict

def getSkillingBooksAdviceGroup() -> dict:
    skill_adviceDict = {}
    skill_AdviceGroupDict = {}

    #Group by Skill
    for skillName in skill_talentsDict.keys():
        skill_adviceDict[skillName] = {}
        for talentNumber, talentDetailsDict in skill_talentsDict[skillName].items():
            for toon in session_data.account.safe_characters:
                if skillName == "Utility" or skillName in toon.specialized_skills:
                    goal_level = talentDetailsDict.get('Optimal', 9999) if talentDetailsDict.get('Optimal', 9999) < session_data.account.library[
                        'MaxBookLevel'] else session_data.account.library['MaxBookLevel']
                    if 0 < toon.max_talents.get(str(talentNumber), 0) < goal_level:
                        if talentDetailsDict['Name'] not in skill_adviceDict[skillName]:
                            skill_adviceDict[skillName][talentDetailsDict['Name']] = [Advice(
                                label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                picture_class=talentDetailsDict['Name']
                            )]
                        skill_adviceDict[skillName][talentDetailsDict['Name']].append(Advice(
                            label=toon.character_name,
                            picture_class=toon.class_name_icon,
                            progression=toon.max_talents.get(str(talentNumber), 0),
                            goal=goal_level
                        ))
        skill_AdviceGroupDict[skillName] = AdviceGroup(
            tier="",
            pre_string=f"Priority Checkouts for {skillName}",
            advices=skill_adviceDict[skillName]
        )

    return skill_AdviceGroupDict

def setLibraryProgressionTier() -> AdviceSection:
    library_AdviceDict = {
        "MaxBookLevels": [],
        "PriorityCheckouts": {}
    }
    library_AdviceGroupDict = {}
    library_AdviceSection = AdviceSection(
        name="Library",
        tier="Not Yet Evaluated",
        header="",
        picture="Library.png",
    )

    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        library_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return library_AdviceSection

    max_tier = 0
    tier_bookLevels = 0

    # Generate AdviceGroups
    library_AdviceGroupDict["MaxBookLevels"] = getBookLevelAdviceGroup()
    characterCheckouts = getCharacterBooksAdviceGroups()
    for characterName, characterAG in characterCheckouts.items():
        library_AdviceGroupDict[characterName] = characterAG

    # Generate AdviceSection
    overall_SamplingTier = min(max_tier, tier_bookLevels)  # Looks silly, but may get more evaluations in the future
    tier_section = f"{overall_SamplingTier}/{max_tier}"
    library_AdviceSection.tier = tier_section
    library_AdviceSection.pinchy_rating = overall_SamplingTier
    library_AdviceSection.groups = library_AdviceGroupDict.values()
    if overall_SamplingTier == max_tier:
        library_AdviceSection.header = f"Best Library tier met: {tier_section}<br>You best ❤️"
    else:
        library_AdviceSection.header = f"Best Library tier met: {tier_section}"
    return library_AdviceSection
