from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts import break_you_best  #killroy_progressionTiers,

logger = get_logger(__name__)

def getKillroyCurrentUpgradesAdviceGroup():
    current_advices = []
    for upgradeName, upgradeDict in session_data.account.killroy.items():
        logger.debug(f"{upgradeName} available? {upgradeDict['Available']}")
        current_advices.append(Advice(
            label=f"{upgradeName}"
                  f"{'<br>Complete ' if not upgradeDict['Available'] else ''}"
                  f"{upgradeDict['Remaining'] if not upgradeDict['Available'] else ''}"
                  f"{' more Killroy fights to unlock this upgrade' if not upgradeDict['Available'] else ''}",
            picture_class=upgradeDict['Image'],
            progression=upgradeDict['Upgrades']
        ))
    current_ag = AdviceGroup(
        tier="",
        pre_string="Informational- Current upgrades",
        advices=current_advices
    )

    return current_ag

def setKillroyProgressionTier():
    killroy_AdviceDict = {
    }
    killroy_AdviceGroupDict = {}
    killroy_AdviceSection = AdviceSection(
        name="Killroy",
        tier="0",
        pinchy_rating=0,
        header="Best Killroy tier met: Not Yet Evaluated",
        picture="",
        complete=False
    )
    # highestKillroySkillLevel = max(session_data.account.all_skills["KillroySkill"])
    # if highestKillroySkillLevel < 1:
    #     killroy_AdviceSection.header = "Come back after unlocking Killroy!"
    #     return killroy_AdviceSection

    infoTiers = 0
    max_tier = 0 #max(killroy_progressionTiers.keys(), default=0) - infoTiers
    tier_Killroy = 0

    killroy_AdviceGroupDict['Current'] = getKillroyCurrentUpgradesAdviceGroup()

    overall_KillroyTier = min(max_tier + infoTiers, tier_Killroy)
    tier_section = f"{overall_KillroyTier}/{max_tier}"
    killroy_AdviceSection.pinchy_rating = overall_KillroyTier
    killroy_AdviceSection.tier = tier_section
    killroy_AdviceSection.groups = killroy_AdviceGroupDict.values()
    if overall_KillroyTier >= max_tier:
        killroy_AdviceSection.header = f"Best Killroy tier met: {tier_section}{break_you_best}️"
        killroy_AdviceSection.complete = True
    else:
        killroy_AdviceSection.header = f"Best Killroy tier met: {tier_section}"

    return killroy_AdviceSection
