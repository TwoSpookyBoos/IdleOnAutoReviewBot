from math import ceil

from consts.consts_autoreview import break_you_best
from consts.consts_general import arbitrary_es_family_goal
from consts.idleon.consts_idleon import expected_talents_dict, current_world
from consts.consts_w2 import max_vial_level
from consts.consts_w3 import max_static_book_levels, max_scaling_book_levels, max_overall_book_levels, \
    library_subgroup_tiers, skill_talentsDict, combat_talentsDict, unbookable_talents_list
from consts.consts_w4 import max_meal_level, cooking_close_enough
from consts.consts_w5 import max_sailing_artifact_level
from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data
from models.advice.advice_group_tabbed import TabbedAdviceGroupTab, TabbedAdviceGroup
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.character import Character
from models.advice.generators.w6 import get_summoning_bonus_advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.misc.add_tabbed_advice_group_or_spread_advice_group_list import \
    add_tabbed_advice_group_or_spread_advice_group_list
from utils.text_formatting import kebab

logger = get_logger(__name__)

def getJeopardyGoal(start: int, interval: int, talentExceedsBookLevels: bool, max_talents_over_books: int):
    #Example1: Refinery Throttle starts 0, interval 8. talentExceedsBookLevels = True, so doNotExceed = max_talents_over_books.
    #Example2: Enhancement Eclipse starts 0, interval 25. talentExceedsBookLevels = False, so doNotExceed = account-wide max book level.
    if talentExceedsBookLevels:
        doNotExceed = max_talents_over_books
        optimal = interval * ((doNotExceed - start) // interval)
        try:
            #logger.debug(f"Given {start}, {interval}, {doNotExceed}, {talentExceedsBookLevels > 0}: optimal {optimal}: Returning {optimal - (doNotExceed - session_data.account.library['MaxBookLevel'])}")
            return int(optimal - (doNotExceed - session_data.account.library['MaxBookLevel']))
        except Exception as reason:
            logger.exception(f"Could not find optimal target level using start {start}, interval {interval}, doNotExceed {doNotExceed} because: {reason}")
            return doNotExceed
    else:
        doNotExceed = session_data.account.library['MaxBookLevel']
        optimal = interval * ((doNotExceed - start) // interval)
        try:
            return int(optimal)
        except Exception as reason:
            logger.exception(f"Could not find optimal target level using start {start}, interval {interval}, doNotExceed {doNotExceed} because: {reason}")
            return session_data.account.library['MaxBookLevel']

def getBookLevelAdviceGroup() -> AdviceGroup:
    bookLevelAdvices = {}

    #Static Sources
    staticSubgroup = f"Static Sources: +{session_data.account.library['StaticSum']}/{max_static_book_levels}"
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
        furyPostString = '. Eldritch Artifacts are unlocked by reaching {{ Rift|#rift }} 31'
    elif not session_data.account.sneaking.emporium["Sovereign Artifacts"].obtained and session_data.account.sailing['Artifacts']['Fury Relic']['Level'] == 3:
        furyPostString = '. Sovereign Artifacts unlock from {{ Jade Emporium|#sneaking }}'
    elif not session_data.account.spelunk.cave["Pebble Cove"].bonus_obtained and session_data.account.sailing['Artifacts']['Fury Relic']['Level'] == 4:
        furyPostString = '. Omnipotent Artifacts unlock from {{ Spelunking|#spelunking }}'
    else:
        furyPostString = ''
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"{{{{ Artifact|#sailing }}}}: Fury Relic: "
              f"+{25 * session_data.account.sailing['Artifacts']['Fury Relic']['Level']}/{25 * max_sailing_artifact_level}{furyPostString}",
        picture_class='fury-relic',
        progression=session_data.account.sailing['Artifacts']['Fury Relic']['Level'],
        goal=max_sailing_artifact_level
    ))

    #Scaling Sources
    scalingSubgroup = f"Scaling Sources: +{session_data.account.library['ScalingSum']}/{max_scaling_book_levels}"
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
    summoning = session_data.account.summoning
    summoning_library = summoning['Bonuses']['+{ Library Max']
    summoningSubgroup = f"Summoning: +{summoning_library['Value']}/{summoning_library['Max']}"

    bookLevelAdvices[summoningSubgroup] = []
    bookLevelAdvices[summoningSubgroup].append(get_summoning_bonus_advice('+{ Library Max'))

    for group_name in bookLevelAdvices:
        for advice in bookLevelAdvices[group_name]:
            advice.mark_advice_completed()

    bookLevelAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Sources of Max Book Levels ({session_data.account.library['MaxBookLevel']}/{max_overall_book_levels})",
        advices=bookLevelAdvices,
        completed=session_data.account.library['MaxBookLevel'] >= max_overall_book_levels
    )
    return bookLevelAdviceGroup

def getBonusLevelAdviceGroup() -> AdviceGroup:
    bonusLevelAdvices = {}

    #Account Wide
    account_subgroupName = f"Account Wide: +{session_data.account.sum_account_wide_bonus_talents}"
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
        arctis_current = arctis_max if session_data.account.divinity['AccountWideArctis'] or char.isArctisLinked() else 0

        char_bonus_levels = int(char.max_talents_over_books - session_data.account.sum_account_wide_bonus_talents - session_data.account.library['MaxBookLevel'])
        subgroupName = f"{char.character_name} the {char.class_name}: +{char_bonus_levels}"
        bonusLevelAdvices[subgroupName] = []

        #Character Specific 1 - Arctis link
        bonusLevelAdvices[subgroupName].append(Advice(
            label=f"{{{{ Divinity|#divinity}}}}: Arctis Minor Link: +{arctis_current}/{arctis_max}",
            picture_class='arctis',
        ))

        #Character Specific 2 - Symbols of Beyond talent
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

        #Character Specific 3 - ES Family Guy
        if char.class_name == 'Elemental Sorcerer':
            bonusLevelAdvices[subgroupName].append(Advice(
                label=f"ES Family Guy: +{char.family_guy_bonus}",
                picture_class='the-family-guy'
            ))

        #Character Specific 4 - Final total
        character_final = (
            session_data.account.library['MaxBookLevel']
            + session_data.account.sum_account_wide_bonus_talents
            + char_bonus_levels
        )
        bonusLevelAdvices[subgroupName].append(Advice(
            label=f"Final talent level: {char.max_talents_over_books}",
            picture_class='ui-talents',
        ))

    for advice in bonusLevelAdvices[account_subgroupName]:
        advice.mark_advice_completed()
    if (
        int(session_data.account.bonus_talents['ES Family']['Progression']) >= arbitrary_es_family_goal and
        sum([1 for advice in bonusLevelAdvices[account_subgroupName] if advice.goal == "✔" or advice.goal == '']) >= len(bonusLevelAdvices[account_subgroupName])-1
    ):
        good_enough = True
    else:
        good_enough = False

    bonusLevelAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Sources of bonus talent levels beyond book levels",
        advices=bonusLevelAdvices,
        informational=True,
        completed=good_enough
    )
    return bonusLevelAdviceGroup

def getCheckoutSpeedAdviceGroup(anyBookAdvice) -> AdviceGroup:
    speed_Advices = []

    # Meal
    speed_Advices.append(Advice(
        label=f"{{{{ Meal|#cooking }}}}: Fortune Cookie: {session_data.account.meals['Fortune Cookie']['Description']}",
        picture_class=session_data.account.meals['Fortune Cookie']['Image'],
        progression=session_data.account.meals['Fortune Cookie']['Level'],
        goal=max_meal_level
    ))

    # Atom
    speed_Advices.append(Advice(
        label=f"Oxygen - Library Booker: {2*session_data.account.atom_collider['Atoms']['Oxygen - Library Booker']['Level']}/60%",
        picture_class='oxygen',
        progression=session_data.account.atom_collider['Atoms']["Oxygen - Library Booker"]['Level'],
        goal=20 + (10 * session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked'])
    ))

    # Tower
    speed_Advices.append(Advice(
        label=f"Talent Book Library building: {((session_data.account.construction_buildings['Talent Book Library']['Level']-1) * 5)}/"
              f"{session_data.account.construction_buildings['Talent Book Library']['MaxLevel']*5}%",
        picture_class='talent-book-library',
        progression=session_data.account.construction_buildings['Talent Book Library']['Level'],
        goal=session_data.account.construction_buildings['Talent Book Library']['MaxLevel']
    ))

    # Bubble
    speed_Advices.append(Advice(
        label=f"Ignore Overdues bubble: {session_data.account.alchemy_bubbles['Ignore Overdues']['BaseValue']:.1f}/100%",
        picture_class='ignore-overdues',
        progression=session_data.account.alchemy_bubbles['Ignore Overdues']['Level'],
        resource=session_data.account.alchemy_bubbles['Ignore Overdues']['Material']
    ))

    # Vial
    vialBonus = session_data.account.alchemy_vials['Chonker Chug (Dune Soul)']['Value']
    speed_Advices.append(Advice(
        label=f"Chonker Chug vial: +{vialBonus:.1f}%",
        picture_class=session_data.account.alchemy_vials['Chonker Chug (Dune Soul)']['Image'],
        progression=session_data.account.alchemy_vials['Chonker Chug (Dune Soul)']['Level'],
        goal=max_vial_level
    ))

    # Stamp
    speed_Advices.append(session_data.account.stamps['Biblio Stamp'].get_advice())

    # Superbit
    gaming_level = max(session_data.account.all_skills['Gaming'])
    speed_Advices.append(Advice(
        label='Superbit: Library Checkouts: +1% per Gaming Level',
        picture_class='green-bits',
        progression=gaming_level if session_data.account.gaming['SuperBits']['Library Checkouts']['Unlocked'] else 0
    ))

    # Achievement
    speed_Advices.append(Advice(
        label=f"W3 Achievement: Checkout Takeout: +{30 * session_data.account.achievements['Checkout Takeout']['Complete']}%",
        picture_class='checkout-takeout',
        progression=int(session_data.account.achievements['Checkout Takeout']['Complete']),
        goal=1
    ))
    
    for advice in speed_Advices:
        advice.mark_advice_completed()

    checkoutSpeedAdviceGroup = AdviceGroup(
        tier='',
        pre_string='Sources of Checkout Speed',
        advices=speed_Advices,
        informational=True,
        completed=not anyBookAdvice
    )

    return checkoutSpeedAdviceGroup

def getTalentExclusions() -> list:
    talentExclusions = []

    #If over 2100 lab, you have all jewels from Jade Emporium and lab levels no longer matter
    if sum(session_data.account.all_skills['Laboratory']) > 2100:
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
        59: "Voidwalker",           #Blood Marrow
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
        204: "Death Bringer",       #Ribbon Winning
        205: "Death Bringer",       #Mass Irrigation
        206: "Death Bringer",       #Agricultural 'Preciation
        207: "Death Bringer",       #Dank Ranks
        208: "Death Bringer",       #Wraith Overlord
        209: "Death Bringer",       #Apocalypse Wow
    }.items():
        if max([toon.max_talents.get(str(talentNumber), 0)
               for toon in session_data.account.safe_characters
               if className in toon.all_classes], default=0) == session_data.account.library['MaxBookLevel']:
            talentExclusions.append(talentNumber)

    #Exclude Siege Breaker > Plunder Ye Deceased if they have a Vman. Level 50 in Enhance Eclipse spawns Plunders often enough to not need the extra time.
    if "Voidwalker" in session_data.account.classes:
        talentExclusions.append(319)

    #If cooking is basically finished thanks to NMLB, exclude Cooking talents
    if session_data.account.cooking['MaxRemainingMeals'] < cooking_close_enough:
        talentExclusions.extend([148, 146, 147, 59])
        # 148: {"Name": "Overflowing Ladle", "Tab": "Blood Berserker"},
        # 146: {"Name": "Apocalypse Chow", "Tab": "Blood Berserker"},
        # 147: {"Name": "Waiting to Cool", "Tab": "Blood Berserker"},
        #  59: Blood Marrow

    #If all bubbles for current max world are unlocked, exclude Shaman's Bubble Breakthrough
    if session_data.account.alchemy_cauldrons['NextWorldMissingBubbles'] > current_world:
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

def getLibraryProgressionTiersAdviceGroups_priorities():
    category_advices = {
        library_subgroup_tiers[0]: []
    }
    category_advices.update({
        v:{
            f"{char.character_name} the {char.class_name}":[] for char in session_data.account.all_characters
        } for v in library_subgroup_tiers[1:-1]  #Account-Wide Priorities and VIP are not addressed per character
    })
    category_advices[library_subgroup_tiers[-1]] = []
    category_advice_groups = {}

    optional_tiers = 2
    true_max = true_max_tiers['Library']
    max_tier = true_max - optional_tiers
    anyBookAdvice = False

    talentExclusions = getTalentExclusions()

    #Account-Wide, highest priority talents after increasing talent book levels
    awp = library_subgroup_tiers[0]
    account_wide_talent_prios = {
        43:  [0, 'Maestro'],   #Maestro- Right Hand of Action
        56:  [0, 'Voidwalker'],   #Vman- Voodoo Statue
        57:  [0, 'Voidwalker'],   #Vman- Species Epoch
        58:  [0, 'Voidwalker'],   #Vman- Master of the System
        59:  [0, 'Voidwalker'],   #Vman- Blood Marrow
        178: [0, 'Divine Knight'],  #DK- King of the Remembered
        328: [0, 'Siege Breaker'],  #SB- Archlord Of The Pirates
        310: [0, 'Hunter'],  #Hunter- Eagle Eye
    }
    for talentNumber in account_wide_talent_prios:
        #Record max level across all characters
        if talentNumber in talentExclusions:
            account_wide_talent_prios[talentNumber][0] = session_data.account.library['MaxBookLevel']
        else:
            account_wide_talent_prios[talentNumber][0] = max([toon.max_talents.get(str(talentNumber), 0) for toon in session_data.account.safe_characters], default=0)
        #If less than max book level
        if (
            account_wide_talent_prios[talentNumber][1] in session_data.account.classes
            and account_wide_talent_prios[talentNumber][0] < session_data.account.library['MaxBookLevel']
        ):
            category_advices[awp].append(Advice(
                label=f"Max {all_talentsDict.get(talentNumber, {}).get('name', f'Unknown{talentNumber}')} on any {account_wide_talent_prios[talentNumber][1]}",
                picture_class=all_talentsDict.get(talentNumber, {}).get('name', f'Unknown{talentNumber}'),
                progression=account_wide_talent_prios[talentNumber][0],
                goal=session_data.account.library['MaxBookLevel']
            ))

    #Character Specific
    for char in session_data.account.safe_characters:
        char_banner = f"{char.character_name} the {char.class_name}"
        talentNumbersAdded = []

        #Skilling
        for skillName in skill_talentsDict.keys():
            for rating in skill_talentsDict[skillName]:
                subgroupName = f"Skilling - {rating} Priority"
                if skill_talentsDict[skillName][rating]:   # Trying to .items() on an empty dict gets angy- This should prevent that.
                    for talent_number, talentDetailsDict in skill_talentsDict[skillName][rating].items():
                        if (
                                (skillName == "Utility" or skillName in char.specialized_skills)
                                and talent_number in char.expected_talents
                                and talent_number not in talentExclusions
                                and talent_number not in talentNumbersAdded
                        ):
                            jeopardy_goal_level = 9999
                            hardcap_level = talentDetailsDict.get('Hardcap', 9999)
                            if 'Optimal' in talentDetailsDict:
                                jeopardy_goal_level = getJeopardyGoal(
                                    talentDetailsDict['Optimal'][0],
                                    talentDetailsDict['Optimal'][1],
                                    talentDetailsDict['Optimal'][2],
                                    char.max_talents_over_books)
                            #logger.debug(f"{char.character_name} {skillName} {rating} {talentDetailsDict['Name']}: min({session_data.account.library['MaxBookLevel']}, {jeopardy_goal_level}, {hardcap_level}) = {min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)}")
                            goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
                            if char.max_talents.get(str(talent_number), 0) < goal_level:
                                category_advices[subgroupName][char_banner].append(
                                    Advice(
                                        label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                        picture_class=talentDetailsDict['Name'],
                                        progression=char.max_talents.get(str(talent_number), 0),
                                        goal=goal_level
                                    )
                                )
                                talentNumbersAdded.append(talent_number)

        #Combat / Other
        for className in combat_talentsDict.keys():
            for rating in combat_talentsDict[className]:
                subgroupName = f"Combat - {rating} Priority"
                if className == char.class_name:  #Only check recommendations for their CURRENT class
                    if combat_talentsDict[className][rating]:  # Trying to .items() on an empty dict gets angy- This should prevent that.
                        for talent_number, talentDetailsDict in combat_talentsDict[className][rating].items():
                            if (
                                    talent_number in char.expected_talents
                                    and talent_number not in talentExclusions
                                    and talent_number not in talentNumbersAdded
                            ):
                                jeopardy_goal_level = 9999
                                hardcap_level = talentDetailsDict.get('Hardcap', 9999)
                                if 'Optimal' in talentDetailsDict:
                                    jeopardy_goal_level = getJeopardyGoal(
                                        talentDetailsDict['Optimal'][0],
                                        talentDetailsDict['Optimal'][1],
                                        talentDetailsDict['Optimal'][2],
                                        char.max_talents_over_books)
                                goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
                                if char.max_talents.get(str(talent_number), 0) < goal_level:
                                    category_advices[subgroupName][char_banner].append(
                                        Advice(
                                            label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                            picture_class=talentDetailsDict['Name'],
                                            progression=char.max_talents.get(str(talent_number), 0),
                                            goal=goal_level
                                        )
                                    )
                                    talentNumbersAdded.append(talent_number)

        #ALL Unmaxed Talents
        subgroupName = library_subgroup_tiers[-2]  #'ALL Unmaxed Talents'
        for talent_number in char.expected_talents:
            if talent_number not in unbookable_talents_list:
                if char.max_talents.get(str(talent_number), 0) < session_data.account.library['MaxBookLevel']:
                    category_advices[subgroupName][char_banner].append(
                        Advice(
                            label=f"{all_talentsDict.get(talent_number, {}).get('subClass', 'Unknown')}: {all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}')}",
                            picture_class=all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}'),
                            progression=char.max_talents.get(str(talent_number), 0),
                            goal=session_data.account.library['MaxBookLevel']
                        )
                    )
                    talentNumbersAdded.append(talent_number)

        if talentNumbersAdded:
            anyBookAdvice = True

    # Account-wide Star Talents
    subgroupName = library_subgroup_tiers[-1]  #'VIP'
    for talent_number in expected_talents_dict[subgroupName]:
        try:
            if session_data.account.safe_characters[0].max_talents.get(str(talent_number), 0) < session_data.account.library['MaxBookLevel']:
                category_advices[subgroupName].append(
                    Advice(
                        label=f"{all_talentsDict.get(talent_number, {}).get('subClass', 'Unknown')}: "
                              f"{all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}')}",
                        picture_class=all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}'),
                        progression=session_data.account.safe_characters[0].max_talents.get(str(talent_number), 0),
                        goal=session_data.account.library['MaxBookLevel']
                    )
                )
        except:
            logger.exception(f"Unable to review Star Talent {talent_number} on Character 0")

    #Create the AdviceGroups
    for category in category_advices:
        category_advice_groups[category] = AdviceGroup(
            tier=1 + library_subgroup_tiers.index(category),
            pre_string=f"{category}",
            advices=category_advices[category]
        )

    #Remove any empty subgroups
    for ag in category_advice_groups.values():
        ag.remove_empty_subgroups()

    #Remove any empty AdviceGroups
    category_advice_groups = {k:v for k,v in category_advice_groups.items() if v.advices}

    category_tier = 0
    for category_name in library_subgroup_tiers:
        if category_name not in category_advice_groups:
            category_tier += 1
        else:
            break  #Don't give credit for completing tier X before tier X-1

    overall_SectionTier = min(max_tier + optional_tiers, category_tier)
    return category_advice_groups, overall_SectionTier, max_tier, anyBookAdvice

def getLibraryProgressionTiersAdviceGroups_characters():
    # This was a very lazy fix to get back to the previous state
    old_librarySubgroupTiers = [
        '', 'Skilling - High Priority', 'Skilling - Medium Priority', 'Skilling - Low Priority', 'Skilling - Lowest Priority',
        'Combat - High Priority', 'Combat - Medium Priority', 'Combat - Low Priority', 'ALL Unmaxed Talents'
    ]
    character_Advices = {}
    character_AdviceGroups = {}
    optional_tiers = 1
    true_max = true_max_tiers['Library Characters']
    max_tier = true_max - 1 - optional_tiers
    anyBookAdvice = False

    talent_exclusions = getTalentExclusions()
    char_tiers = {}

    #Account-Wide, highest priority talents after increasing talent book levels
    awp = 'Account Wide Priorities'
    account_wide_talent_prios = {
        # 32:  0,   #Maestro- Printer Go Brr
        43:  [0, 'Maestro'],   #Maestro- Right Hand of Action
        56:  [0, 'Voidwalker'],   #Vman- Voodoo Statue
        57:  [0, 'Voidwalker'],   #Vman- Species Epoch
        58:  [0, 'Voidwalker'],   #Vman- Master of the System
        59:  [0, 'Voidwalker'],   #Vman- Blood Marrow
        178: [0, 'Divine Knight'],  #DK- King of the Remembered
        328: [0, 'Siege Breaker'],  #SB- Archlord Of The Pirates
        310: [0, 'Hunter'],  #Hunter- Eagle Eye
        432: [0, 'Wind Walker'],  #WW- Generational Gemstones
        # 373: 0,  #BM- Curviture Of The Paw
        # 508: 0,  #ES- Wormhole Emperor
    }
    for talent_number in account_wide_talent_prios:
        #Record max level across all characters
        if talent_number in talent_exclusions:
            account_wide_talent_prios[talent_number][0] = session_data.account.library['MaxBookLevel']
        else:
            account_wide_talent_prios[talent_number][0] = max([toon.max_talents.get(str(talent_number), 0) for toon in session_data.account.safe_characters], default=0)
        #If less than max book level
        if (
            account_wide_talent_prios[talent_number][1] in session_data.account.classes
            and account_wide_talent_prios[talent_number][0] < session_data.account.library['MaxBookLevel']
        ):
            if awp not in character_Advices:
                character_Advices[awp] = []
            character_Advices[awp].append(
                Advice(
                    label=f"Max {all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}')} on any {account_wide_talent_prios[talent_number][1]}",
                    picture_class=all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}'),
                    progression=account_wide_talent_prios[talent_number][0],
                    goal=session_data.account.library['MaxBookLevel']
                )
            )
    character_AdviceGroups[awp] = AdviceGroup(
        tier=0,
        pre_string=f"Account-Wide Priority Checkouts after new max Book levels",
        advices=character_Advices.get(awp, [])
    )

    #Character Specific
    character_specific_advices = {}
    character_specific_advice_groups: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]] = {}
    for index, char in enumerate(session_data.account.safe_characters): #type: int, Character
        character_specific_advices[char.character_name] = {}
        talentNumbersAdded = []

        #Skilling
        for skillName in skill_talentsDict.keys():
            for rating in skill_talentsDict[skillName]:
                subgroup_label = f"Skilling - {rating} Priority"
                if subgroup_label not in character_specific_advices[char.character_name]:
                    character_specific_advices[char.character_name][subgroup_label] = []
                if skill_talentsDict[skillName][rating]:   # Trying to .items() on an empty dict gets angy- This should prevent that.
                    for talent_number, talentDetailsDict in skill_talentsDict[skillName][rating].items():
                        if (
                                (skillName == "Utility" or skillName in char.specialized_skills)
                                and talent_number in char.expected_talents
                                and talent_number not in talent_exclusions
                                and talent_number not in talentNumbersAdded
                        ):
                            jeopardy_goal_level = 9999
                            hardcap_level = talentDetailsDict.get('Hardcap', 9999)
                            if 'Optimal' in talentDetailsDict:
                                jeopardy_goal_level = getJeopardyGoal(
                                    talentDetailsDict['Optimal'][0],
                                    talentDetailsDict['Optimal'][1],
                                    talentDetailsDict['Optimal'][2],
                                    char.max_talents_over_books)
                            #logger.debug(f"{char.character_name} {skillName} {rating} {talentDetailsDict['Name']}: min({session_data.account.library['MaxBookLevel']}, {jeopardy_goal_level}, {hardcap_level}) = {min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)}")
                            goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
                            if char.max_talents.get(str(talent_number), 0) < goal_level:
                                character_specific_advices[char.character_name][subgroup_label].append(
                                    Advice(
                                        label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                        picture_class=talentDetailsDict['Name'],
                                        progression=char.max_talents.get(str(talent_number), 0),
                                        goal=goal_level
                                    )
                                )
                                talentNumbersAdded.append(talent_number)

        #Combat / Other
        for className in combat_talentsDict.keys():
            for rating in combat_talentsDict[className]:
                subgroup_label = f"Combat - {rating} Priority"
                if subgroup_label not in character_specific_advices[char.character_name]:
                    character_specific_advices[char.character_name][subgroup_label] = []
                if className == char.class_name:  #Only check recommendations for their CURRENT class
                    if combat_talentsDict[className][rating]:  # Trying to .items() on an empty dict gets angy- This should prevent that.
                        for talent_number, talentDetailsDict in combat_talentsDict[className][rating].items():
                            if (
                                    talent_number in char.expected_talents
                                    and talent_number not in talent_exclusions
                                    and talent_number not in talentNumbersAdded
                            ):
                                jeopardy_goal_level = 9999
                                hardcap_level = talentDetailsDict.get('Hardcap', 9999)
                                if 'Optimal' in talentDetailsDict:
                                    jeopardy_goal_level = getJeopardyGoal(
                                        talentDetailsDict['Optimal'][0],
                                        talentDetailsDict['Optimal'][1],
                                        talentDetailsDict['Optimal'][2],
                                        char.max_talents_over_books)
                                goal_level = min(session_data.account.library['MaxBookLevel'], jeopardy_goal_level, hardcap_level)
                                if char.max_talents.get(str(talent_number), 0) < goal_level:
                                    character_specific_advices[char.character_name][subgroup_label].append(
                                        Advice(
                                            label=f"{talentDetailsDict['Tab']}: {talentDetailsDict['Name']}",
                                            picture_class=talentDetailsDict['Name'],
                                            progression=char.max_talents.get(str(talent_number), 0),
                                            goal=goal_level
                                        )
                                    )
                                    talentNumbersAdded.append(talent_number)

        #Everything Else
        subgroup_label = old_librarySubgroupTiers[-1]
        if subgroup_label not in character_specific_advices[char.character_name]:
            character_specific_advices[char.character_name][subgroup_label] = []
        for talent_number in char.expected_talents:
            if talent_number not in unbookable_talents_list:
                if char.max_talents.get(str(talent_number), 0) < session_data.account.library['MaxBookLevel']:
                    character_specific_advices[char.character_name][subgroup_label].append(
                        Advice(
                            label=f"{all_talentsDict.get(talent_number, {}).get('subClass', 'Unknown')}: {all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}')}",
                            picture_class=all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}'),
                            progression=char.max_talents.get(str(talent_number), 0),
                            goal=session_data.account.library['MaxBookLevel']
                        )
                    )
                    talentNumbersAdded.append(talent_number)

        #Create AdviceGroup before moving on to next character
        char_tier = 0
        for subgroup_name in character_specific_advices[char.character_name]:
            if char_tier == old_librarySubgroupTiers.index(subgroup_name)-1 and len(character_specific_advices[char.character_name][subgroup_name]) == 0:
                char_tier = old_librarySubgroupTiers.index(subgroup_name)
            else:
                break
        char_tiers[char.character_name] = char_tier

        character_specific_advice_groups[char.character_name] = (
            TabbedAdviceGroupTab(kebab(char.class_name_icon), str(index + 1)),
            AdviceGroup(
                tier=char_tier,
                pre_string=f"Priority Checkouts for {char.character_name} the {char.class_name}",
                advices=character_specific_advices[char.character_name])
        )

        if talentNumbersAdded:
            anyBookAdvice = True

    character_specific_tabbed_advice_group = TabbedAdviceGroup(character_specific_advice_groups)
    add_tabbed_advice_group_or_spread_advice_group_list(character_AdviceGroups, character_specific_tabbed_advice_group, "Character Priorities")

    # Account-wide Star Talents
    awt = "VIP Star Talents"
    subgroup_label = "VIP"
    character_Advices[awt] = {subgroup_label: []}
    for talent_number in expected_talents_dict[subgroup_label]:
        try:
            # logger.debug(
            #     f"Star Talent {talent_number} "
            #     f"({all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}')}) on Character 0: "
            #     f"{session_data.account.safe_characters[0].max_talents.get(str(talent_number), 0)}"
            # )
            if session_data.account.safe_characters[0].max_talents.get(str(talent_number), 0) < session_data.account.library['MaxBookLevel']:
                character_Advices[awt][subgroup_label].append(
                    Advice(
                        label=f"{all_talentsDict.get(talent_number, {}).get('subClass', 'Unknown')}: "
                              f"{all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}')}",
                        picture_class=all_talentsDict.get(talent_number, {}).get('name', f'Unknown{talent_number}'),
                        progression=session_data.account.safe_characters[0].max_talents.get(str(talent_number), 0),
                        goal=session_data.account.library['MaxBookLevel']
                    )
                )
        except:
            logger.exception(f"Unable to review Star Talent {talent_number} on Character 0")

    # Create AdviceGroup before moving on to characters
    character_AdviceGroups[awt] = AdviceGroup(
        tier='',
        pre_string=f"Account-Wide VIP Star Talents",
        advices=character_Advices[awt]
    )

    #Remove any empty subgroups
    for group in character_AdviceGroups.values():
        group.remove_empty_subgroups()
    overall_SectionTier = min(max_tier + optional_tiers, min(char_tiers.values(), default=0))
    return character_AdviceGroups, overall_SectionTier, max_tier, anyBookAdvice


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
    library_AdviceGroups, overall_SectionTier, max_tier, any_book_advice = (
        getLibraryProgressionTiersAdviceGroups_characters()
        if session_data.account.library_group_characters else
        getLibraryProgressionTiersAdviceGroups_priorities()
    )
    library_AdviceGroups["MaxBookLevels"] = getBookLevelAdviceGroup()
    library_AdviceGroups["BonusLevels"] = getBonusLevelAdviceGroup()
    library_AdviceGroups["CheckoutSpeed"] = getCheckoutSpeedAdviceGroup(any_book_advice)

    # Generate Alerts
    if (
        session_data.account.library['BooksReady'] >= 40
        and session_data.account.construction_buildings['Automation Arm']['Level'] >= 5
        and any_book_advice
    ):
        # For future reference, since this comes up from time to time. The amount of checkouts stored in the JSON is only updated when the player
        # walks into town. AutoReview makes no effort to view the TimeAway value for Library and estimate book speed to fill the gap
        session_data.account.alerts_Advices['World 3'].append(Advice(
            label=f"{session_data.account.library['BooksReady'] // 20} perfect {{{{ checkouts|#library }}}} available",
            picture_class='talent-book-library'
        ))

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    library_AdviceSection = AdviceSection(
        name='Library',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Library tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Library.png',
        groups=library_AdviceGroups.values(),
        unrated=True
    )
    return library_AdviceSection
