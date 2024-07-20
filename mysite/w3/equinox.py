from flask import g as session_data
from consts import maxDreams, dreamsThatUnlockNewBonuses, equinox_progressionTiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.text_formatting import pl

logger = get_logger(__name__)

def setEquinoxProgressionTier() -> AdviceSection:
    equinox_AdviceDict = {
        "DreamsCompleted": [],
        "TotalUpgrades": {},
    }
    equinox_AdviceGroupDict = {}
    equinox_AdviceSection = AdviceSection(
        name="Equinox",
        tier="Not Yet Evaluated",
        header="Best Equinox tier met: Not Yet Evaluated",
        picture="Equinox_Valley_Mirror.gif"
    )

    if not session_data.account.equinox_unlocked:
        equinox_AdviceSection.header = "Come back after unlocking Equinox!"
        return equinox_AdviceSection

    infoTiers = 1
    max_tier = len(dreamsThatUnlockNewBonuses)  # 1 final info tier for completing all dreams
    playerRecommendedBonusTotal = sum([bonus['CurrentLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Recommended'])
    playerOptionalBonusTotal = sum([bonus['CurrentLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Optional'])
    recommendedBonusTotal = sum([bonus['FinalMaxLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Recommended'])
    optionalBonusTotal = sum([bonus['FinalMaxLevel'] for bonus in session_data.account.equinox_bonuses.values() if bonus['Category'] == 'Optional'])

    #Dreams Completed
    remainingBonusesToBeUnlocked = []
    if session_data.account.total_dreams_completed >= maxDreams:  #If the player has completed ALL dreams, set to max tier
        tier_TotalDreamsCompleted = max_tier + infoTiers
    else:
        for bonusName, bonusValuesDict in session_data.account.equinox_bonuses.items():
            if bonusValuesDict['Unlocked'] == False:
                remainingBonusesToBeUnlocked.append(bonusName)
        # Otherwise set to max - 1 (for completing all dreams) - however many upgrades are remaining to be unlocked
        # 11 - 1 = t10 if all bonuses unlocked
        # 11 - 1 - 4 = t6 if 5 remaining bonuses to be unlocked
        tier_TotalDreamsCompleted = max_tier - len(session_data.account.remaining_equinox_dreams_unlocking_new_bonuses)
        for lockedBonus in remainingBonusesToBeUnlocked:
            equinox_AdviceDict["DreamsCompleted"].append(Advice(
                label=f"{lockedBonus} ({session_data.account.equinox_bonuses[lockedBonus]['Category']})",
                picture_class=lockedBonus,
                goal=f"Dream {session_data.account.remaining_equinox_dreams_unlocking_new_bonuses[remainingBonusesToBeUnlocked.index(lockedBonus)]}"
            ))
        equinox_AdviceDict["DreamsCompleted"].append(Advice(
            label=f"Complete all {maxDreams} Dreams",
            picture_class="equinox-mirror",
            progression=session_data.account.total_dreams_completed,
            goal=maxDreams
        ))

    #Recommended Upgrades
    if playerRecommendedBonusTotal < recommendedBonusTotal:
        recommendedSubgroupName = f"Recommended Upgrades: {playerRecommendedBonusTotal}/{recommendedBonusTotal}"
        equinox_AdviceDict["TotalUpgrades"][recommendedSubgroupName] = []
        for bonusName in equinox_progressionTiers['Recommended']:
            if session_data.account.equinox_bonuses[bonusName]['CurrentLevel'] < session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel']\
                    and session_data.account.equinox_bonuses[bonusName]['Unlocked'] == True:
                if len(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades']) > 0:
                    expandDreamMaxLevelEval = (f" (Increase max level by completing "
                                               f"Dream{pl(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])}: "
                                               f"{', '.join(str(dreamNumber) for dreamNumber in session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])})")
                else:
                    expandDreamMaxLevelEval = ""
                equinox_AdviceDict["TotalUpgrades"][recommendedSubgroupName].append(Advice(
                    label=f"{bonusName}{expandDreamMaxLevelEval}",
                    picture_class=bonusName,
                    progression=session_data.account.equinox_bonuses[bonusName]['CurrentLevel'],
                    goal=session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel']
                ))
        if len(equinox_AdviceDict["TotalUpgrades"][recommendedSubgroupName]) == 0:
            equinox_AdviceDict["TotalUpgrades"][recommendedSubgroupName].append(Advice(
                label="Nothing good available :( Maybe wait for future unlocks!",
                picture_class="",
            ))

    # Optional Upgrades
    if playerOptionalBonusTotal < optionalBonusTotal:
        optionalSubgroupName = f"Optional Upgrades: {playerOptionalBonusTotal}/{optionalBonusTotal}"
        equinox_AdviceDict["TotalUpgrades"][optionalSubgroupName] = []
        for bonusName in equinox_progressionTiers['Optional']:
            if session_data.account.equinox_bonuses[bonusName]['CurrentLevel'] < session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel'] \
                    and session_data.account.equinox_bonuses[bonusName]['Unlocked'] == True:
                if len(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades']) > 0:
                    expandDreamMaxLevelEval = (f" (Increase max level by completing "
                                               f"Dream{pl(session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])}: "
                                               f"{', '.join(str(dreamNumber) for dreamNumber in session_data.account.equinox_bonuses[bonusName]['RemainingUpgrades'])})")
                else:
                    expandDreamMaxLevelEval = ""
                equinox_AdviceDict["TotalUpgrades"][optionalSubgroupName].append(Advice(
                    label=f"{bonusName}{expandDreamMaxLevelEval}",
                    picture_class=bonusName,
                    progression=session_data.account.equinox_bonuses[bonusName]['CurrentLevel'],
                    goal=session_data.account.equinox_bonuses[bonusName]['FinalMaxLevel']
                ))
        if len(equinox_AdviceDict["TotalUpgrades"][optionalSubgroupName]) == 0:
            equinox_AdviceDict["TotalUpgrades"][optionalSubgroupName].append(Advice(
                label="No unlocked, unmaxed Optional upgrades to list",
                picture_class="",
            ))

    # Generate AdviceGroups
    equinox_AdviceGroupDict["DreamsCompleted"] = AdviceGroup(
        tier=f"{tier_TotalDreamsCompleted if tier_TotalDreamsCompleted < max_tier else ''}",
        pre_string=f"{'Informational- ' if tier_TotalDreamsCompleted >= max_tier else ''}"
                   f"""{pl(maxDreams - session_data.account.total_dreams_completed,
                         'Complete the last Equinox Dream',
                         'Complete more Equinox Dreams')}""",
        advices=equinox_AdviceDict['DreamsCompleted']
    )

    equinox_AdviceGroupDict["BonusUpgrades"] = AdviceGroup(
        tier="",
        pre_string="Upgrade more Equinox Bonuses",
        advices=equinox_AdviceDict['TotalUpgrades']
    )

    # Generate AdviceSection

    overall_EquinoxTier = min(max_tier + infoTiers, tier_TotalDreamsCompleted)
    tier_section = f"{overall_EquinoxTier}/{max_tier}"
    equinox_AdviceSection.tier = tier_section
    equinox_AdviceSection.pinchy_rating = overall_EquinoxTier
    equinox_AdviceSection.groups = equinox_AdviceGroupDict.values()
    if overall_EquinoxTier >= max_tier:
        equinox_AdviceSection.header = f"Best Equinox tier met: {tier_section}<br>You best ❤️"
        equinox_AdviceSection.complete = True
    else:
        equinox_AdviceSection.header = f"Best Equinox tier met: {tier_section}"

    return equinox_AdviceSection
