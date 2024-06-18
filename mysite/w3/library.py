from math import ceil
from flask import g as session_data
from consts import maxStaticBookLevels, maxScalingBookLevels, maxSummoningBookLevels, maxOverallBookLevels, skill_talentsDict, combat_talentsDict
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger

logger = get_logger(__name__)

def getJeopardyGoal(start: int, interval: int, doNotExceed: int):
    try:
        return interval * (doNotExceed-start // interval)
    except Exception as reason:
        logger.exception(f"Could not find optimal target level using start {start}, interval {interval}, doNotExceed {doNotExceed} because: {reason}")
        return doNotExceed

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
        furyPostString = ". Sovereign Artifacts unlock from {{ Jade Emporium|#sneaking }}"
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

def getBonusLevelAdviceGroup() -> AdviceGroup:
    bonusLevelAdvices = {}

    #Account Wide
    account_subgroupName = f"Account Wide: +{session_data.account.bonus_talents_account_wide_sum}"
    bonusLevelAdvices[account_subgroupName] = []
    for bonusName, bonusValuesDict in session_data.account.bonus_talents.items():
        bonusLevelAdvices[account_subgroupName].append(Advice(
            label=bonusValuesDict.get('Label', ''),
            picture_class=bonusValuesDict.get('Image', ''),
            progression=bonusValuesDict.get('Progression', ''),
            goal=bonusValuesDict.get('Goal', ''),
        ))

    #Character Specific
    for char in session_data.account.safe_characters:
        arctis_max = ceil(15 * session_data.account.alchemy_bubbles['Big P']['BaseValue'] * (char.divinity_level / (char.divinity_level + 60)))
        arctis_current = arctis_max if session_data.account.doot_owned or char.divinity_link == "Arctis" or char.current_polytheism_link == "Arctis" or char.secondary_polytheism_link == "Arctis" else 0

        char_bonus_levels = arctis_current + char.symbols_of_beyond
        char_bonus_levels += char.family_guy_bonus if char.class_name == "Elemental Sorcerer" else 0
        subgroupName = f"{char.character_name} the {char.class_name}: +{char_bonus_levels}"
        bonusLevelAdvices[subgroupName] = []

        bonusLevelAdvices[subgroupName].append(Advice(
            label=f"{{{{ Divinity|#divinity}}}}: Arctis Minor Link: +{arctis_current}/{arctis_max}",
            picture_class='arctis',
        ))
        if char.base_class == 'Warrior':
            symbols_image_name = 'symbols-of-beyond-r'
        elif char.base_class == 'Archer':
            symbols_image_name = 'symbols-of-beyond-g'
        elif char.base_class == 'Mage':
            symbols_image_name = 'symbols-of-beyond-p'
        else:
            symbols_image_name = ''  #Journeyman doesn't get a Symbols talent
        if symbols_image_name:
            bonusLevelAdvices[subgroupName].append(Advice(
                label=f"Symbols of Beyond: +{char.symbols_of_beyond}",
                picture_class=symbols_image_name
        ))

        if char.class_name == 'Elemental Sorcerer':
            bonusLevelAdvices[subgroupName].append(Advice(
                label=f"ES Family Guy: +{char.family_guy_bonus}",
                picture_class='the-family-guy'
            ))

    bonusLevelAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of bonus talent levels beyond book levels",
        advices=bonusLevelAdvices
    )
    return bonusLevelAdviceGroup

def getCharacterBooksAdviceGroups() -> dict:
    character_adviceDict = {}
    character_AdviceGroupDict = {}

    for toon in session_data.account.safe_characters:
        character_adviceDict[toon.character_name] = {}
        talentNumbersAdded = []

        #Skilling
        for skillName in skill_talentsDict.keys():
            for rating in skill_talentsDict[skillName]:
                subgroupName = f"Skilling - {rating} Priority"
                if subgroupName not in character_adviceDict[toon.character_name]:
                    character_adviceDict[toon.character_name][subgroupName] = []
                if skill_talentsDict[skillName][rating]:   # Trying to .items() on an empty dict gets angy- This should prevent that.
                    for talentNumber, talentDetailsDict in skill_talentsDict[skillName][rating].items():
                        if skillName == "Utility" or skillName in toon.specialized_skills:
                            jeopardy_goal_level = 9999
                            hardcap_level = talentDetailsDict.get('Hardcap', 9999)
                            if 'Optimal' in talentDetailsDict:
                                if talentDetailsDict['Optimal'][2]:  #Lists whether this talent goes beyond book levels or not
                                    jeopardy_goal_level = getJeopardyGoal(
                                        talentDetailsDict['Optimal'][0],
                                        talentDetailsDict['Optimal'][1],
                                        toon.max_talents_over_books)
                                else:
                                    jeopardy_goal_level = getJeopardyGoal(
                                        talentDetailsDict['Optimal'][0],
                                        talentDetailsDict['Optimal'][1],
                                        session_data.account.library['MaxBookLevel'])
                            goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
                            if 0 < toon.max_talents.get(str(talentNumber), 0) < goal_level and talentNumber not in talentNumbersAdded:
                                character_adviceDict[toon.character_name][subgroupName].append(Advice(
                                    label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                    picture_class=talentDetailsDict['Name'],
                                    progression=toon.max_talents.get(str(talentNumber), 0),
                                    goal=goal_level
                                ))
                                talentNumbersAdded.append(talentNumber)

        #Combat / Other
        # for className in combat_talentsDict.keys():
        #     for rating in combat_talentsDict[className]:
        #         subgroupName = f"Combat - {rating} Priority"
        #         if className == toon.class_name:  #Only check recommendations for their CURRENT class
        #             if combat_talentsDict[className][rating]:  # Trying to .items() on an empty dict gets angy- This should prevent that.
        #                 for talentNumber, talentDetailsDict in combat_talentsDict[className][rating].items():
        #                     jeopardy_goal_level = 9999
        #                     hardcap_level = talentDetailsDict.get('Hardcap', 9999)
        #                     if talentDetailsDict.get('Optimal', None):
        #                         if talentDetailsDict['Optimal'][2]:
        #                             jeopardy_goal_level = getJeopardyGoal(
        #                                 talentDetailsDict['Optimal'][0],
        #                                 talentDetailsDict['Optimal'][1],
        #                                 session_data.account.library['MaxBookLevel'])
        #                         else:
        #                             jeopardy_goal_level = getJeopardyGoal(
        #                                 talentDetailsDict['Optimal'][0],
        #                                 talentDetailsDict['Optimal'][1],
        #                                 toon.max_talents_over_books)
        #                     goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
        #                     if 0 < toon.max_talents.get(str(talentNumber), 0) < goal_level and talentNumber not in talentNumbersAdded:
        #                         if subgroupName not in character_adviceDict[toon.character_name]:
        #                             character_adviceDict[toon.character_name][subgroupName] = []
        #                         character_adviceDict[toon.character_name][subgroupName].append(Advice(
        #                             label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
        #                             picture_class=talentDetailsDict['Name'],
        #                             progression=toon.max_talents.get(str(talentNumber), 0),
        #                             goal=goal_level
        #                         ))
        #                         talentNumbersAdded.append(talentNumber)

        #Create AdviceGroup before moving on to next character
        character_AdviceGroupDict[toon.character_name] = AdviceGroup(
            tier="",
            pre_string=f"Priority Checkouts for {toon.character_name} the {toon.class_name}",
            advices=character_adviceDict[toon.character_name]
        )

    #Remove any empty subgroups
    for ag in character_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

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
    library_AdviceGroupDict["BonusLevels"] = getBonusLevelAdviceGroup()
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
