from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    break_you_best, infinity_string, grimoire_bones_list,
    # grimoire_progressionTiers
)
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    grimoire_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0  #max(grimoire_progressionTiers.keys(), default=0) - info_tiers
    tier_Grimoire = 0

    tiers_ag = AdviceGroup(
        tier=tier_Grimoire,
        pre_string="Progression Tiers",
        advices=grimoire_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Grimoire)
    return tiers_ag, overall_SectionTier, max_tier


def getGrimoireUpgradesAdviceGroup():
    upgrades_AdviceDict = {}

    #General Info
    upgrades_AdviceDict['General Info'] = []

    #Currencies
    upgrades_AdviceDict['Currencies'] = [
        Advice(
            label=f"{bone_name}: {notateNumber('Basic', session_data.account.grimoire[f'Bone{bone_index}'], 3)}",
            picture_class=f'grimoire-bone-{bone_index-1}'
        ) for bone_index, bone_name in enumerate(grimoire_bones_list, start=1)
    ]
    upgrades_AdviceDict['Currencies'].insert(0, Advice(
        label=f"Total Bones Collected: {notateNumber('Basic', session_data.account.grimoire['Total Bones Collected'], 3)}",
        picture_class='wraith-overlord'
    ))
    #Upgrades
    upgrades_AdviceDict['Upgrades'] = [
        Advice(
            label=(
                f"{upgrade_name}: {upgrade_details['Description']}"
                f"<br>Requires {upgrade_details['Unlock Requirement'] - session_data.account.grimoire['Total Upgrades']} more Upgrades to unlock"
                if not upgrade_details['Unlocked'] else
                f"{upgrade_name}: {upgrade_details['Description']}"
            ),
            picture_class=upgrade_details['Image'],
            progression=upgrade_details['Level'],
            goal=upgrade_details['Max Level'],
            resource=upgrade_details['Bone Image']
        ) for upgrade_name, upgrade_details in session_data.account.grimoire['Upgrades'].items()
    ]
    upgrades_AdviceDict['Upgrades'].insert(0, Advice(
        label=f"Total Grimoire Upgrades: {session_data.account.grimoire['Total Upgrades']:,}",
        picture_class='grimoire',
    ))

    for subgroup in upgrades_AdviceDict:
        for advice in upgrades_AdviceDict[subgroup]:
            mark_advice_completed(advice)

    upgrades_ag = AdviceGroup(
        tier='',
        pre_string="Grimoire Upgrades info",
        advices=upgrades_AdviceDict
    )
    upgrades_ag.remove_empty_subgroups()
    return upgrades_ag


def getGrimoireAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if 'Death Bringer' not in session_data.account.classes:
        grimoire_AdviceSection = AdviceSection(
            name="The Grimoire",
            tier="Not Yet Evaluated",
            header="Come back after unlocking a Death Bringer in World 6!",
            picture='customized/Wraith.gif',
            unrated=True,
            unreached=session_data.account.highestWorldReached < 6,
            completed=False
        )
        return grimoire_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    grimoire_AdviceGroupDict = {}
    grimoire_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    grimoire_AdviceGroupDict['Upgrades'] = getGrimoireUpgradesAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    grimoire_AdviceSection = AdviceSection(
        name="The Grimoire",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Death Bringer and Grimoire Information",  #tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Wraith.gif',
        groups=grimoire_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return grimoire_AdviceSection
