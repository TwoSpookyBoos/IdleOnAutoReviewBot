from math import ceil

from flask import g as session_data
from consts import maxStaticBookLevels, maxScalingBookLevels, maxSummoningBookLevels, maxOverallBookLevels, skill_talentsDict, combat_talentsDict, currentWorld, \
    stamp_maxes, maxMealLevel, cookingCloseEnough, librarySubgroupTiers, break_you_best, arbitrary_es_family_goal, max_VialLevel
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger

logger = get_logger(__name__)

def getJeopardyGoal(start: int, interval: int, talentExceedsBookLevels: bool, max_talents_over_books: int):
    #Example1: Refinery Throttle starts 0, interval 8. talentExceedsBookLevels = True, so doNotExceed = max_talents_over_books.
    #Example2: Enhancement Eclipse starts 0, interval 25. talentExceedsBookLevels = False, so doNotExceed = account-wide max book level.
    if talentExceedsBookLevels:
        doNotExceed = max_talents_over_books
        optimal = interval * ((doNotExceed - start) // interval)
        try:
            #logger.debug(f"Given {start}, {interval}, {doNotExceed}, {talentExceedsBookLevels > 0}: optimal {optimal}: Returning {optimal - (doNotExceed - session_data.account.library['MaxBookLevel'])}")
            return optimal - (doNotExceed - session_data.account.library['MaxBookLevel'])
        except Exception as reason:
            logger.exception(f"Could not find optimal target level using start {start}, interval {interval}, doNotExceed {doNotExceed} because: {reason}")
            return doNotExceed
    else:
        doNotExceed = session_data.account.library['MaxBookLevel']
        optimal = interval * ((doNotExceed - start) // interval)
        try:
            return optimal
        except Exception as reason:
            logger.exception(f"Could not find optimal target level using start {start}, interval {interval}, doNotExceed {doNotExceed} because: {reason}")
            return session_data.account.library['MaxBookLevel']

def getBookLevelAdviceGroup() -> AdviceGroup:
    bookLevelAdvices = {}

    #Static Sources
    staticSubgroup = f"Static Sources: +{session_data.account.library['StaticSum']}/{maxStaticBookLevels}"
    bookLevelAdvices[staticSubgroup] = []

    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Construction: Talent Book Library built: "
              f"+{25 * (0 < session_data.account.construction_buildings['Talent Book Library']['Level'])}/25",
        picture_class="talent-book-library",
        progression=min(1, session_data.account.construction_buildings['Talent Book Library']['Level']),
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"W3 Achievement: Checkout Takeout: "
              f"+{5 * session_data.account.achievements['Checkout Takeout']['Complete']}/5",
        picture_class="checkout-takeout",
        progression=int(session_data.account.achievements['Checkout Takeout']['Complete']),
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"{{{{Atom Collider|#atom-collider }}}}: Oxygen: "
              f"+{10 * (0 < session_data.account.atom_collider['Atoms']['Oxygen - Library Booker']['Level'])}/10",
        picture_class="oxygen",
        progression=1 if 0 < session_data.account.atom_collider['Atoms']['Oxygen - Library Booker']['Level'] else 0,
        goal=1
    ))
    if not session_data.account.rift['EldritchArtifacts'] and session_data.account.sailing['Artifacts']['Fury Relic']['Level'] == 2:
        furyPostString = ". Eldritch Artifacts are unlocked by reaching {{ Rift|#rift }} 31"
    elif not session_data.account.sneaking['JadeEmporium']["Sovereign Artifacts"]['Obtained'] and session_data.account.sailing['Artifacts']['Fury Relic']['Level'] == 3:
        furyPostString = ". Sovereign Artifacts unlock from {{ Jade Emporium|#sneaking }}"
    else:
        furyPostString = ""
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"{{{{ Artifact|#sailing }}}}: Fury Relic: "
              f"+{25 * session_data.account.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0)}/100{furyPostString}",
        picture_class="fury-relic",
        progression=session_data.account.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0),
        goal=4
    ))

    #Scaling Sources
    scalingSubgroup = f"Scaling Sources: +{session_data.account.library['ScalingSum']}/{maxScalingBookLevels}"
    bookLevelAdvices[scalingSubgroup] = []

    bookLevelAdvices[scalingSubgroup].append(Advice(
        label=f"W3 Max Book level Merit: "
              f"+{2 * session_data.account.merits[2][2]['Level']}/10",
        picture_class="merit-2-2",
        progression=session_data.account.merits[2][2]["Level"],
        goal=session_data.account.merits[2][2]["MaxLevel"]
    ))
    bookLevelAdvices[scalingSubgroup].append(Advice(
        label=f"{{{{Salt Lick|#salt-lick }}}}: "
              f"+{2 * session_data.account.saltlick.get('Max Book', 0)}/20",
        picture_class="salt-lick",
        progression=session_data.account.saltlick.get('Max Book', 0),
        goal=10
    ))

    #Summoning Sources
    summoningSubgroup = f"Summoning Winner Bonus: +{session_data.account.library['SummoningSum']}/{maxSummoningBookLevels}"
    bookLevelAdvices[summoningSubgroup] = []
    cyan14beat = session_data.account.summoning['Battles']['Cyan'] >= 14
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"Summoning match Cyan14: "
              f"+{10.5 * cyan14beat}/10.5{'' if cyan14beat else '. No other multipliers apply until this is beaten.'}",
        picture_class="samurai-guardian",
        progression=1 if cyan14beat else 0,
        goal=1
    ))
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        bookLevelAdvices[summoningSubgroup].append(advice)
    bookLevelAdvices[summoningSubgroup].append(session_data.account.summoning['WinnerBonusesSummaryPartial'])

    for group_name in bookLevelAdvices:
        for advice in bookLevelAdvices[group_name]:
            mark_advice_completed(advice)

    bookLevelAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of Max Book Levels ({session_data.account.library['MaxBookLevel']}/{maxOverallBookLevels})",
        advices=bookLevelAdvices,
        informational=True,
        completed=True if session_data.account.library['MaxBookLevel'] >= maxOverallBookLevels else False
    )
    return bookLevelAdviceGroup

def getBonusLevelAdviceGroup() -> AdviceGroup:
    bonusLevelAdvices = {}

    #Account Wide
    account_subgroupName = f"Account Wide: +{session_data.account.bonus_talents_account_wide_sum}"
    bonusLevelAdvices[account_subgroupName] = []
    for bonusName, bonusValuesDict in session_data.account.bonus_talents.items():
        force_complete = None
        if bonusValuesDict.get('Label', '').startswith('ES Family Bonus'):
            if int(bonusValuesDict['Progression']) >= arbitrary_es_family_goal:
                force_complete = True
        bonusLevelAdvices[account_subgroupName].append(Advice(
            label=bonusValuesDict.get('Label', ''),
            picture_class=bonusValuesDict.get('Image', ''),
            progression=bonusValuesDict.get('Progression', ''),
            goal=bonusValuesDict.get('Goal', ''),
            complete=force_complete
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
                label=f"Symbols of Beyond: +{char.symbols_of_beyond}/{1 + session_data.account.library['MaxBookLevel']//20}",
                picture_class=symbols_image_name
            ))

        if char.class_name == 'Elemental Sorcerer':
            bonusLevelAdvices[subgroupName].append(Advice(
                label=f"ES Family Guy: +{char.family_guy_bonus}",
                picture_class='the-family-guy'
            ))

    for advice in bonusLevelAdvices[account_subgroupName]:
        mark_advice_completed(advice)
    if (
        int(session_data.account.bonus_talents['ES Family']['Progression']) >= arbitrary_es_family_goal and
        sum([1 for advice in bonusLevelAdvices[account_subgroupName] if advice.goal == "✔" or advice.goal == '']) >= len(bonusLevelAdvices[account_subgroupName])-1
    ):
        good_enough = True
    else:
        good_enough = False

    bonusLevelAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of bonus talent levels beyond book levels",
        advices=bonusLevelAdvices,
        informational=True,
        completed=good_enough
    )
    return bonusLevelAdviceGroup

def getCheckoutSpeedAdviceGroup(anyBookAdvice) -> AdviceGroup:
    checkoutSpeedAdvices = []

    # Meal
    checkoutSpeedAdvices.append(Advice(
        label=f"Meal: Fortune Cookie: {session_data.account.meals['Fortune Cookie']['Value']:.1f}%",
        picture_class="fortune-cookie",
        progression=session_data.account.meals["Fortune Cookie"]["Level"],
        goal=maxMealLevel 
    ))

    # Atom
    checkoutSpeedAdvices.append(Advice(
        label=f"""Oxygen - Library Booker: {2*session_data.account.atom_collider['Atoms']["Oxygen - Library Booker"]['Level']}/60%""",
        picture_class="oxygen",
        progression=session_data.account.atom_collider['Atoms']["Oxygen - Library Booker"]['Level'],
        goal=20 + (10 * session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked'])
    ))

    # Tower
    checkoutSpeedAdvices.append(Advice(
        label=f"Talent Book Library building: {((session_data.account.construction_buildings['Talent Book Library']['Level']-1) * 5)}/{session_data.account.construction_buildings['Talent Book Library']['MaxLevel']*5}%",
        picture_class="talent-book-library",
        progression=session_data.account.construction_buildings['Talent Book Library']['Level'],
        goal=session_data.account.construction_buildings['Talent Book Library']['MaxLevel']
    ))

    # Bubble
    checkoutSpeedAdvices.append(Advice(
        label=f"Ignore Overdues bubble: {session_data.account.alchemy_bubbles['Ignore Overdues']['BaseValue']:.1f}/100%",
        picture_class="ignore-overdues",
        progression=session_data.account.alchemy_bubbles['Ignore Overdues']['Level'],
        resource=session_data.account.alchemy_bubbles['Ignore Overdues']['Material']
    ))

    # Vial
    vialBonus = (
        session_data.account.alchemy_vials['Chonker Chug (Dune Soul)']['Value']
        * session_data.account.vialMasteryMulti
        * session_data.account.labBonuses["My 1st Chemistry Set"]["Value"]
    )
    checkoutSpeedAdvices.append(Advice(
        label=f"Chonker Chug vial: +{vialBonus:.1f}%",
        picture_class='chonker-chug',
        progression=session_data.account.alchemy_vials['Chonker Chug (Dune Soul)']['Level'],
        goal=max_VialLevel
    ))

    # Stamp
    checkoutSpeedAdvices.append(Advice(
        label=f"Stamp: Biblio Stamp: +{session_data.account.stamps['Biblio Stamp']['Level']}%",
        picture_class="biblio-stamp",
        progression=session_data.account.stamps["Biblio Stamp"]['Level'],
        goal=stamp_maxes["Biblio Stamp"],
        resource=session_data.account.stamps["Biblio Stamp"]['Material'],
    ))

    # Superbit
    gaming_level = max(session_data.account.all_skills["Gaming"])
    checkoutSpeedAdvices.append(Advice(
        label=f"Superbit: Library Checkouts: +1% per Gaming Level",
        picture_class="green-bits",
        progression=gaming_level if session_data.account.gaming['SuperBits']['Library Checkouts']['Unlocked'] else 0
    ))

    # Achievement
    checkoutSpeedAdvices.append(Advice(
        label=f"W3 Achievement: Checkout Takeout: +{30 * session_data.account.achievements['Checkout Takeout']['Complete']}%",
        picture_class="checkout-takeout",
        progression=int(session_data.account.achievements['Checkout Takeout']['Complete']),
        goal=1
    ))
    
    for advice in checkoutSpeedAdvices:
        mark_advice_completed(advice)

    checkoutSpeedAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of Checkout Speed",
        advices=checkoutSpeedAdvices,
        informational=True,
        completed=not anyBookAdvice
    )

    return checkoutSpeedAdviceGroup

def getTalentExclusions() -> list:
    talentExclusions = []

    #If over 2100 lab, you have all jewels from Jade Emporium and lab levels no longer matter
    if sum(session_data.account.all_skills['Lab']) > 2100:
        talentExclusions.extend([537, 538])
        # 537: {"Name": "Essence Transferral", "Tab": "Bubonic Conjuror"},
        # 538: {"Name": "Upload Squared", "Tab": "Bubonic Conjuror"},

    #If you can reach max book of 200, the Bubo Aura build really takes off. Priority for damage from Poison falls off a cliff.
    if max([toon.max_talents_over_books for toon in session_data.account.safe_characters if toon.class_name == "Bubonic Conjuror"], default=0) >= 200:
        talentExclusions.append(525)
        #525: {"Name": "Chemical Warfare", "Tab": "Bubonic Conjuror"},

    #If you have less than 5 God Ranks, exclude ES damage per God rank
    if session_data.account.divinity['GodRank'] < 4:
        talentExclusions.append(507)

    #Elite Account-Wides don't stack, can be excluded if already maxed on one character
    for talentNumber, className in {
        148: "Blood Berserker",     #148: {"Name": "Overflowing Ladle", "Tab": "Blood Berserker"},
        176: "Divine Knight",       #176: {"Name": "One Thousand Hours Played", "Tab": "Divine Knight"},
        177: "Divine Knight",       #177: {"Name": "Bitty Litty", "Tab": "Divine Knight"},
        178: "Divine Knight",       #178: {"Name": "King of the Remembered", "Tab": "Divine Knight"},
        326: "Siege Breaker",       #326: {"Name": "Expertly Sailed", "Tab": "Siege Breaker"},
        327: "Siege Breaker",       #327: {"Name": "Captain Peptalk", "Tab": "Siege Breaker"},
        328: "Siege Breaker",       #328: {"Name": "Archlord Of The Pirates", "Tab": "Siege Breaker"},
        310: "Hunter",              #310: {"Name": "Eagle Eye", "Tab": "Hunter"},
        311: "Hunter",              #311: {"Name": "Invasive Species", "Tab": "Hunter"},
        372: "Beast Master",        #372: {"Name": "Shining Beacon of Egg", "Tab": "Beast Master"},
        373: "Beast Master",        #373: {"Name": "Curviture Of The Paw", "Tab": "Beast Master"},
        505: "Elemental Sorcerer",  #505: {"Name": "Polytheism", "Tab": "Elemental Sorcerer"},
        506: "Elemental Sorcerer",  #506: {"Name": "Shared Beliefs", "Tab": "Elemental Sorcerer"},
        507: "Elemental Sorcerer",  #507: {"Name": "Gods Chosen Children", "Tab": "Elemental Sorcerer"},
        508: "Elemental Sorcerer",  #508: {"Name": "Wormhole Emperor", "Tab": "Elemental Sorcerer"},
        536: "Bubonic Conjuror",    #536: {"Name": "Green Tube", "Tab": "Bubonic Conjuror"},
    }.items():
        if max([toon.max_talents.get(str(talentNumber), 0)
               for toon in session_data.account.safe_characters
               if className in toon.all_classes], default=0) == session_data.account.library['MaxBookLevel']:
            talentExclusions.append(talentNumber)

    #Exclude Siege Breaker > Plunder Ye Deceased if they have a Vman. Level 50 in Enhance Eclipse spawns Plunders often enough to not need the extra time.
    if "Voidwalker" in session_data.account.classes:
        talentExclusions.append(319)

    #If cooking is basically finished thanks to NMLB, exclude Cooking talents
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        talentExclusions.extend([148, 146, 147])
        # 148: {"Name": "Overflowing Ladle", "Tab": "Blood Berserker"},
        # 146: {"Name": "Apocalypse Chow", "Tab": "Blood Berserker"},
        # 147: {"Name": "Waiting to Cool", "Tab": "Blood Berserker"},

    #If all bubbles for current max world are unlocked, exclude Shaman's Bubble Breakthrough
    if session_data.account.alchemy_cauldrons['NextWorldMissingBubbles'] > currentWorld:
        talentExclusions.extend([492, 493])
        #492: {"Name": "Bubble Breakthrough", "Tab": "Shaman"},
        #493: {"Name": "Sharing Some Smarts", "Tab": "Shaman"},

    #If the final Gaming Superbit is owned, exclude DK Gaming
    if session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked']:
        talentExclusions.extend([175, 176, 177])
        #175: {"Name": "Undying Passion", "Tab": "Divine Knight"},
        #176: {"Name": "One Thousand Hours Played", "Tab": "Divine Knight"},
        #177: {"Name": "Bitty Litty", "Tab": "Divine Knight"},

    return talentExclusions

def getLibraryProgressionTiersAdviceGroups():
    character_adviceDict = {}
    character_AdviceGroupDict = {}
    info_tiers = 0
    max_tier = len(librarySubgroupTiers) - 1
    anyBookAdvice = False

    talentExclusions = getTalentExclusions()
    char_tiers = {}

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
                        if (
                                (skillName == "Utility" or skillName in toon.specialized_skills)
                                and talentNumber in toon.expected_talents
                                and talentNumber not in talentExclusions
                                and talentNumber not in talentNumbersAdded
                        ):
                            jeopardy_goal_level = 9999
                            hardcap_level = talentDetailsDict.get('Hardcap', 9999)
                            if 'Optimal' in talentDetailsDict:
                                jeopardy_goal_level = getJeopardyGoal(
                                    talentDetailsDict['Optimal'][0],
                                    talentDetailsDict['Optimal'][1],
                                    talentDetailsDict['Optimal'][2],
                                    toon.max_talents_over_books)
                            #logger.debug(f"{toon.character_name} {skillName} {rating} {talentDetailsDict['Name']}: min({session_data.account.library['MaxBookLevel']}, {jeopardy_goal_level}, {hardcap_level}) = {min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)}")
                            goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
                            if toon.max_talents.get(str(talentNumber), 0) < goal_level:
                                character_adviceDict[toon.character_name][subgroupName].append(
                                    Advice(
                                        label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                        picture_class=talentDetailsDict['Name'],
                                        progression=toon.max_talents.get(str(talentNumber), 0),
                                        goal=goal_level
                                    )
                                )
                                talentNumbersAdded.append(talentNumber)

        #Combat / Other
        for className in combat_talentsDict.keys():
            for rating in combat_talentsDict[className]:
                subgroupName = f"Combat - {rating} Priority"
                if subgroupName not in character_adviceDict[toon.character_name]:
                    character_adviceDict[toon.character_name][subgroupName] = []
                if className == toon.class_name:  #Only check recommendations for their CURRENT class
                    if combat_talentsDict[className][rating]:  # Trying to .items() on an empty dict gets angy- This should prevent that.
                        for talentNumber, talentDetailsDict in combat_talentsDict[className][rating].items():
                            if (
                                    talentNumber in toon.expected_talents
                                    and talentNumber not in talentExclusions
                                    and talentNumber not in talentNumbersAdded
                            ):
                                jeopardy_goal_level = 9999
                                hardcap_level = talentDetailsDict.get('Hardcap', 9999)
                                if 'Optimal' in talentDetailsDict:
                                    jeopardy_goal_level = getJeopardyGoal(
                                        talentDetailsDict['Optimal'][0],
                                        talentDetailsDict['Optimal'][1],
                                        talentDetailsDict['Optimal'][2],
                                        toon.max_talents_over_books)
                                goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
                                if toon.max_talents.get(str(talentNumber), 0) < goal_level:
                                    character_adviceDict[toon.character_name][subgroupName].append(
                                        Advice(
                                            label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                            picture_class=talentDetailsDict['Name'],
                                            progression=toon.max_talents.get(str(talentNumber), 0),
                                            goal=goal_level
                                        )
                                    )
                                    talentNumbersAdded.append(talentNumber)

        #Create AdviceGroup before moving on to next character
        char_tier = 0
        for subgroupname in character_adviceDict[toon.character_name]:
            if char_tier == librarySubgroupTiers.index(subgroupname)-1 and len(character_adviceDict[toon.character_name][subgroupname]) == 0:
                char_tier = librarySubgroupTiers.index(subgroupname)
            else:
                break
        char_tiers[toon.character_name] = char_tier

        character_AdviceGroupDict[toon.character_name] = AdviceGroup(
            tier=char_tier,
            pre_string=f"Priority Checkouts for {toon.character_name} the {toon.class_name}",
            advices=character_adviceDict[toon.character_name]
        )
        if talentNumbersAdded:
            anyBookAdvice = True

    #Remove any empty subgroups
    for ag in character_AdviceGroupDict.values():
        ag.remove_empty_subgroups()
    overall_SectionTier = min(max_tier, min(char_tiers.values(), default=0))
    return character_AdviceGroupDict, overall_SectionTier, max_tier, anyBookAdvice

def getLibraryAdviceSection() -> AdviceSection:
    if session_data.account.construction_buildings['Talent Book Library']['Level'] < 1:
        library_AdviceSection = AdviceSection(
            name="Library",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Talent Book Library within the Construction skill in World 3!",
            picture="Library.png",
            unrated=True,
            unreached=True
        )
        return library_AdviceSection

    # Generate AdviceGroups
    library_AdviceGroupDict, overall_SectionTier, max_tier, anyBookAdvice = getLibraryProgressionTiersAdviceGroups()
    library_AdviceGroupDict["MaxBookLevels"] = getBookLevelAdviceGroup()
    library_AdviceGroupDict["BonusLevels"] = getBonusLevelAdviceGroup()
    library_AdviceGroupDict["CheckoutSpeed"] = getCheckoutSpeedAdviceGroup(anyBookAdvice)

    # Generate Alerts
    if (
        session_data.account.library['BooksReady'] >= 40
        and session_data.account.construction_buildings['Automation Arm']['Level'] >= 5
        and anyBookAdvice
    ):
        session_data.account.alerts_AdviceDict['World 3'].append(Advice(
            label=f"{session_data.account.library['BooksReady'] // 20} perfect {{{{ checkouts|#library }}}} available",
            picture_class="talent-book-library"
        ))

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    library_AdviceSection = AdviceSection(
        name="Library",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Library tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Library.png",
        groups=library_AdviceGroupDict.values(),
        unrated=True
    )
    return library_AdviceSection
