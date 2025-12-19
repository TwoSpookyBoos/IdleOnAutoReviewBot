
from consts.consts_autoreview import break_you_best
from consts.consts_w3 import max_possible_dreams
from consts.progression_tiers import equinox_progressionTiers, true_max_tiers

from models.models import AdviceSection, AdviceGroup, Advice, session_data
from utils.logging import get_logger
from utils.text_formatting import pl

logger = get_logger(__name__)

def getEquinoxProgressionTiersAdviceGroup():
    equinox_Advices = {
        'Dreams': {
            'Complete Dreams': [],
            'Unlock Equinox Bonuses': [],
        },
        'TotalUpgrades': {},
    }

    optional_tiers = 1
    true_max = true_max_tiers['Equinox']
    max_tier = true_max - optional_tiers  # 1 final info tier for completing all dreams

    playerRecommendedBonusTotal = sum([bonus['CurrentLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Recommended'])
    playerOptionalBonusTotal = sum([bonus['CurrentLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Optional'])
    recommendedBonusTotal = sum([bonus['FinalMaxLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Recommended'])
    optionalBonusTotal = sum([bonus['FinalMaxLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Optional'])

    # Dreams Completed
    remainingBonusesToBeUnlocked = []
    if session_data.account.total_dreams_completed >= max_possible_dreams:  # If the player has completed ALL possible dreams, set to max tier
        tier_TotalDreamsCompleted = max_tier + optional_tiers
    else:
        for bonusName, bonusValuesDict in session_data.account.equinox_bonuses.items():
            if bonusValuesDict['Unlocked'] == False:
                remainingBonusesToBeUnlocked.append(bonusName)
        # Otherwise set to max - 1 (for completing all dreams) - however many upgrades are remaining to be unlocked
        # 11 - 1 = t10 if all bonuses unlocked
        # 11 - 1 - 4 = t6 if 5 remaining bonuses to be unlocked
        tier_TotalDreamsCompleted = max_tier - len(session_data.account.remaining_equinox_dreams_unlocking_new_bonuses)
        for dream in session_data.account.remaining_equinox_dreams_unlocking_new_bonuses:
            equinox_Advices["Dreams"]["Complete Dreams"].append(Advice(
                label=f"Dream {dream}",
                picture_class="ballot-32",
            ))
        for lockedBonus in remainingBonusesToBeUnlocked:
            equinox_Advices["Dreams"]["Unlock Equinox Bonuses"].append(Advice(
                label=f"{lockedBonus} ({session_data.account.equinox_bonuses[lockedBonus]['Category']})",
                picture_class=lockedBonus,
                # goal=f"Dream {session_data.account.remaining_equinox_dreams_unlocking_new_bonuses[remainingBonusesToBeUnlocked.index(lockedBonus)]}"
            ))

        equinox_Advices["Dreams"]["Complete Dreams"].append(Advice(
            label=f"Complete all {max_possible_dreams} possible Dreams",
            picture_class="equinox-mirror",
            progression=session_data.account.total_dreams_completed,
            goal=max_possible_dreams
        ))

    # Recommended Upgrades
    recommendedSubgroupName = f"Recommended Upgrades: {playerRecommendedBonusTotal}/{recommendedBonusTotal}"
    if playerRecommendedBonusTotal < recommendedBonusTotal:
        equinox_Advices["TotalUpgrades"][recommendedSubgroupName] = []
        for bonusName in equinox_progressionTiers['Recommended']:
            if session_data.account.equinox_bonuses[bonusName]['CurrentLevel'] < session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel'] \
                    and session_data.account.equinox_bonuses[bonusName]['Unlocked'] == True:
                if len(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades']) > 0:
                    expandDreamMaxLevelEval = (f" (Increase max level by completing "
                                               f"Dream{pl(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])}: "
                                               f"{', '.join(str(dreamNumber) for dreamNumber in session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])})")
                else:
                    expandDreamMaxLevelEval = ""
                equinox_Advices["TotalUpgrades"][recommendedSubgroupName].append(Advice(
                    label=f"{bonusName}{expandDreamMaxLevelEval}",
                    picture_class=bonusName,
                    progression=session_data.account.equinox_bonuses[bonusName]['CurrentLevel'],
                    goal=session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel']
                ))
        if len(equinox_Advices["TotalUpgrades"][recommendedSubgroupName]) == 0:
            equinox_Advices["TotalUpgrades"][recommendedSubgroupName].append(Advice(
                label="Nothing good available :( Maybe wait for future unlocks!",
                picture_class="",
            ))

    # Optional Upgrades
    if playerOptionalBonusTotal < optionalBonusTotal:
        optionalSubgroupName = f"Optional Upgrades: {playerOptionalBonusTotal}/{optionalBonusTotal}"
        equinox_Advices["TotalUpgrades"][optionalSubgroupName] = []
        for bonusName in equinox_progressionTiers['Optional']:
            if session_data.account.equinox_bonuses[bonusName]['CurrentLevel'] < session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel'] \
                    and session_data.account.equinox_bonuses[bonusName]['Unlocked'] == True:
                if len(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades']) > 0:
                    expandDreamMaxLevelEval = (
                        f" (Increase max level by completing "
                        f"Dream{pl(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])}: "
                        f"{', '.join(str(dreamNumber) for dreamNumber in session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])})"
                    )
                else:
                    expandDreamMaxLevelEval = ""
                equinox_Advices["TotalUpgrades"][optionalSubgroupName].append(Advice(
                    label=f"{bonusName}{expandDreamMaxLevelEval}",
                    picture_class=bonusName,
                    progression=session_data.account.equinox_bonuses[bonusName]['CurrentLevel'],
                    goal=session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel']
                ))
        if len(equinox_Advices["TotalUpgrades"][optionalSubgroupName]) == 0:
            equinox_Advices["TotalUpgrades"][optionalSubgroupName].append(Advice(
                label="No unlocked, unmaxed Optional upgrades to list",
                picture_class="",
            ))

    # Generate AdviceGroups
    equinox_AdviceGroupDict = {}
    equinox_AdviceGroupDict["Complete Dreams"] = AdviceGroup(
        tier=f"{tier_TotalDreamsCompleted if tier_TotalDreamsCompleted < max_tier else ''}",
        pre_string=f"{'Informational- Complete all Equinox Dreams' if tier_TotalDreamsCompleted >= max_tier else 'Unlock more Equinox Bonuses'}",
        advices=equinox_Advices["Dreams"],
        post_string=f"{'New Bonuses unlock in a set order. They are not tied to certain Dreams.' if tier_TotalDreamsCompleted < max_tier else ''}",
        informational=True if tier_TotalDreamsCompleted >= max_tier else False
    )
    equinox_AdviceGroupDict["Complete Dreams"].remove_empty_subgroups()

    bonus_max_levels = session_data.account.summoning['Endless Bonuses'].get('+ Equinox Max LV', 0)
    equinox_AdviceGroupDict["BonusUpgrades"] = AdviceGroup(
        tier="",
        pre_string="Upgrade more Equinox Bonuses",
        post_string=f"+{bonus_max_levels} max levels from Endless Summoning already included" if bonus_max_levels > 0 else '',
        advices=equinox_Advices['TotalUpgrades'],
        informational=True,
        completed=recommendedSubgroupName not in equinox_Advices["TotalUpgrades"]
    )
    overall_SectionTier = min(max_tier + optional_tiers, tier_TotalDreamsCompleted)
    return equinox_AdviceGroupDict, overall_SectionTier, max_tier, max_tier + optional_tiers

def getEquinoxAdviceSection() -> AdviceSection:
    if not session_data.account.equinox_unlocked:
        equinox_AdviceSection = AdviceSection(
            name="Equinox",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Equinox in World 3!",
            picture="Equinox_Valley_Mirror.gif",
            unreached=True
        )
        return equinox_AdviceSection

    #Generate AdviceGroups
    equinox_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getEquinoxProgressionTiersAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    equinox_AdviceSection = AdviceSection(
        name="Equinox",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Equinox tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Equinox_Valley_Mirror.gif",
        groups=equinox_AdviceGroupDict.values()
    )
    return equinox_AdviceSection
