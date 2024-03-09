import json
import progressionResults
import idleon_SkillLevels
from mysite.models import AdviceGroup, Advice, AdviceSection
from mysite.utils import get_logger


logger = get_logger(__name__)


def getEquinoxDreams(inputJSON) -> dict:
    try:
        rawDreams = json.loads(inputJSON["WeeklyBoss"])
    except Exception as reason:
        logger.error("Unable to access WeeklyBoss data from JSON: %s", reason)
        return dict(
            Dream3=False,
            Dream11=False,
            Dream23=False
        )

    results = dict(
        Dream3=rawDreams.get("d_2") == -1,
        Dream11=rawDreams.get("d_10") == -1,
        Dream23=rawDreams.get("d_22") == -1,
    )
    logger.debug("OUTPUT results: %s", results)

    return results


def parseCombatLevels(inputJSON, playerCount, playerNames):
    combatLevels = idleon_SkillLevels.getSpecificSkillLevelsList(inputJSON, playerCount, "Combat")
    equinox3_charactersUnder100 = {}
    equinox11_charactersUnder250 = {}
    equinox23_charactersUnder500 = {}

    for counter, playerLevel in enumerate(combatLevels):
        player_name = playerNames[counter]
        if playerLevel < 500:  # player under level 500, add to 1
            equinox23_charactersUnder500[player_name] = playerLevel
        if playerLevel < 250:  # player under level 250, add to 2
            equinox11_charactersUnder250[player_name] = playerLevel
        if playerLevel < 100:  # player under level 100, add to all 3
            equinox3_charactersUnder100[player_name] = playerLevel


    parsedCombatLevels = dict(
        sum_AccountLevel=sum(combatLevels),
        equinoxDict=dict(
            under100=equinox3_charactersUnder100,
            under250=equinox11_charactersUnder250,
            under500=equinox23_charactersUnder500,
        )
    )
    logger.info('%s', parsedCombatLevels["sum_AccountLevel"])
    # parsedCombatLevels['playerClasses'] = playerClasses
    return parsedCombatLevels


def setCombatLevelsProgressionTier(inputJSON, progressionTiers, playerCount, playerNames, playerClasses) -> progressionResults:
    parsedCombatLevels = parseCombatLevels(inputJSON, playerCount, playerNames)
    equinoxDreamStatus = getEquinoxDreams(inputJSON)

    total_combat_level = parsedCombatLevels['sum_AccountLevel']

    # Process tiers
    # tier[0] = int tier
    # tier[1] = int TotalAccountLevel
    # tier[2] = str TotalAccountLevel reward
    # tier[3] = int PlayerLevels
    # tier[4] = str PL reward
    # tier[5] = str notes
    next_tier = next((tier for tier in progressionTiers if total_combat_level < tier[1]), None)
    curr_tier = next((tier for tier in reversed(progressionTiers) if total_combat_level >= tier[1]), progressionTiers[0])

    overall_CombatLevelTier = curr_tier[0]

    advices = [
        Advice(label=next_tier[2], picture_class="total-level", progression=total_combat_level, goal=next_tier[1])
    ] if next_tier else []

    total_level_group = AdviceGroup(
        tier=overall_CombatLevelTier,
        pre_string=f"Increase the total family level to unlock the next reward",
        advices=advices
    )

    if len(parsedCombatLevels['equinoxDict']['under100']) > 0 and equinoxDreamStatus["Dream3"] is False:
        advice_PersonalLevels = "Level the following characters to 100+ to complete Equinox Dream 3"
        goal = 100

    elif len(parsedCombatLevels['equinoxDict']['under250']) > 0 and equinoxDreamStatus["Dream11"] is False:
        advice_PersonalLevels = "Level the following characters to 250+ to complete Equinox Dream 11 and unlock their Personal Sparkle Obol slot"
        goal = 250

    elif len(parsedCombatLevels['equinoxDict']['under500']) > 0 and equinoxDreamStatus["Dream23"] is False:
        advice_PersonalLevels = "Level the following characters to 500+ to complete Equinox Dream 23"
        goal = 500

    else:
        advice_PersonalLevels = f"Your family class level is {total_combat_level}. The last reward was back at 5k. Still... Pretty neat :)"
        goal = '∞'

    lvlup_advices = [
        Advice(label=character, picture_class=playerClasses[playerNames.index(character)] + '-icon', progression=level, goal=goal)
        for character, level in parsedCombatLevels['equinoxDict'].get(f'under{goal}', dict()).items()
    ]

    lvlup_group = AdviceGroup(
        tier="",
        pre_string=advice_PersonalLevels,
        advices=lvlup_advices,
    )

    max_tier = progressionTiers[-1][0]
    tier = f"{overall_CombatLevelTier}/{max_tier}"
    header = f"Optimal family class level tier met: {tier}. "

    if overall_CombatLevelTier == max_tier:
        header += f"Your family class level is {total_combat_level}, no more rewards for you. Do you, like, live off of genocidal energy or something? ... jk 💪💪💪"

    combat_section = AdviceSection(
        name="Combat Levels",
        tier=tier,
        header=header,
        picture="Family.png",
        groups=[total_level_group, lvlup_group],
        pinchy_rating=overall_CombatLevelTier
    )

    return combat_section
