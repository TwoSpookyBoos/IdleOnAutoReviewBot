from consts import combatLevels_progressionTiers
from models.models import AdviceGroup, Advice, AdviceSection
from utils.logging import get_logger
from flask import g as session_data
from utils.data_formatting import safe_loads

logger = get_logger(__name__)


def getEquinoxDreams() -> dict:
    try:
        rawDreams = safe_loads(session_data.account.raw_data.get("WeeklyBoss", "{}"))
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
    # logger.debug("OUTPUT results: %s", results)

    return results


def parseCombatLevels():
    combatLevels = session_data.account.all_skills["Combat"]
    equinox3_charactersUnder100 = {}
    equinox11_charactersUnder250 = {}
    equinox23_charactersUnder500 = {}

    for counter, playerLevel in enumerate(combatLevels):
        if playerLevel < 500:  # player under level 500, add to 1
            equinox23_charactersUnder500[counter] = playerLevel
        if playerLevel < 250:  # player under level 250, add to 2
            equinox11_charactersUnder250[counter] = playerLevel
        if playerLevel < 100:  # player under level 100, add to all 3
            equinox3_charactersUnder100[counter] = playerLevel

    parsedCombatLevels = dict(
        sum_AccountLevel=sum(combatLevels),
        equinoxDict=dict(
            under100=equinox3_charactersUnder100,
            under250=equinox11_charactersUnder250,
            under500=equinox23_charactersUnder500,
        )
    )
    # logger.info('%s', parsedCombatLevels["sum_AccountLevel"])
    return parsedCombatLevels


def setCombatLevelsProgressionTier() -> AdviceSection:
    parsedCombatLevels = parseCombatLevels()
    equinoxDreamStatus = getEquinoxDreams()

    total_combat_level = parsedCombatLevels['sum_AccountLevel']

    # Process tiers
    # tier[0] = int tier
    # tier[1] = int TotalAccountLevel
    # tier[2] = str TotalAccountLevel reward
    # tier[3] = int PlayerLevels
    # tier[4] = str PL reward
    # tier[5] = str notes
    next_tier = next((tier for tier in combatLevels_progressionTiers if total_combat_level < tier[1]), None)
    curr_tier = next((tier for tier in reversed(combatLevels_progressionTiers) if total_combat_level >= tier[1]), combatLevels_progressionTiers[0])

    overall_CombatLevelTier = curr_tier[0]

    try:
        if 'Character' in next_tier[2]:
            character_or_obol = 'beginner-icon'
        elif 'Obol' in next_tier[2]:
            character_or_obol = 'silver-obol-of-pop-pop'
        else:
            character_or_obol = ''
    except:
        character_or_obol = ''
    advices = [
        Advice(
            label=next_tier[2],
            picture_class=character_or_obol,
            progression=total_combat_level,
            goal=next_tier[1])
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
        Advice(
            label=session_data.account.all_characters[characterIndex].character_name,
            picture_class=session_data.account.all_characters[characterIndex].class_name_icon,
            progression=level,
            goal=goal)
        for characterIndex, level in parsedCombatLevels['equinoxDict'].get(f'under{goal}', dict()).items() if session_data.account.equinox_unlocked
    ]

    lvlup_group = AdviceGroup(
        tier="",
        pre_string=advice_PersonalLevels,
        advices=lvlup_advices,
    )

    max_tier = combatLevels_progressionTiers[-1][0]
    tier = f"{overall_CombatLevelTier}/{max_tier}"
    header = f"Best Family class level tier met: {tier}. "

    if overall_CombatLevelTier == max_tier:
        header += f"<br>You best ❤️<br>Your Family class level is {total_combat_level}"
        #, no more rewards for you. Do you, like, live off of genocidal energy or something? ... jk 💪💪💪"

    combat_section = AdviceSection(
        name="Combat Levels",
        tier=tier,
        header=header,
        picture="Family.png",
        groups=[total_level_group, lvlup_group],
        pinchy_rating=overall_CombatLevelTier
    )

    return combat_section
