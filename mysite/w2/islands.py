from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.data_formatting import mark_advice_completed
from flask import g as session_data
from consts import islands_progressionTiers, break_you_best, maxTiersPerGroup, islands_fractal_rewards_dict

logger = get_logger(__name__)

def getTrashIslandAdviceGroup() -> AdviceGroup:
    trash_advices = []
    if session_data.account.islands['Trash Island']['Garbage Purchases'] < 6:
        trash_advices.append(Advice(
            label=f"Purchase 5 total levels into Garbage Generation",
            picture_class='garbage',
            progression=session_data.account.islands['Trash Island']['Garbage Purchases'],
            goal=6
        ))
    if not session_data.account.islands['Trash Island']['Unlock New Bribe Set']['Unlocked']:
        trash_advices.append(Advice(
            label=f"Unlock and Purchase the new {{{{ Bribes|#bribes}}}}",
            picture_class='bribes',
            progression=session_data.account.islands['Trash'],
            goal=session_data.account.islands['Trash Island']['Unlock New Bribe Set']['Cost']
        ))
    if session_data.account.islands['Trash Island']['Garbage Purchases'] < 9:
        trash_advices.append(Advice(
            label=f"Purchase 9 total levels into Garbage Generation",
            picture_class='garbage',
            progression=session_data.account.islands['Trash Island']['Garbage Purchases'],
            goal=9
        ))

    for stamp_name in ['Golden Sixes Stamp', 'Stat Wallstreet Stamp', 'Skelefish Stamp', 'Amplestample Stamp']:
        if not session_data.account.islands['Trash Island'][stamp_name]['Unlocked']:
            trash_advices.append(Advice(
                label=f"Purchase the {stamp_name[:-6]} {{{{ Stamp|#stamps }}}}",
                picture_class=stamp_name,
                progression=session_data.account.islands['Trash'],
                goal=session_data.account.islands['Trash Island'][stamp_name]['Cost']
            ))

    trash_advicegroup = AdviceGroup(
        tier='',
        pre_string='Informational- Trash Island shop priorities',
        advices=trash_advices,
        informational=True
    )
    return trash_advicegroup

def getFractalAdviceGroup() -> AdviceGroup:
    fractal_advices = []
    for hours, rewardDict in islands_fractal_rewards_dict.items():
        fractal_advices.append(Advice(
            label=rewardDict['Reward'],
            picture_class=rewardDict['Image'],
            progression=session_data.account.nothing_hours,
            goal=int(hours)
        ))

    for advice in fractal_advices:
        mark_advice_completed(advice)

    fractal_advicegroup = AdviceGroup(
        tier='',
        pre_string='Informational- Fractal Nothing hour rewards',
        advices=fractal_advices,
        informational=True
    )

    return fractal_advicegroup

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    islands_AdviceDict = {}
    infoTiers = 0
    max_tier = max(islands_progressionTiers.keys()) - infoTiers
    tier_Islands = 0

    # Assess Tiers
    for tierNumber, tierRequirements in islands_progressionTiers.items():
        subgroupName = f"To reach Tier {tierNumber}"
        for islandName in tierRequirements.get('Islands', []):
            if not session_data.account.islands[islandName]['Unlocked']:
                if subgroupName not in islands_AdviceDict and len(islands_AdviceDict) < maxTiersPerGroup:
                    islands_AdviceDict[subgroupName] = []
                if subgroupName in islands_AdviceDict:
                    islands_AdviceDict[subgroupName].append(Advice(
                        label=f"Unlock {islandName}",
                        picture_class=islandName
                    ))
        if subgroupName not in islands_AdviceDict and tier_Islands == tierNumber - 1:
            tier_Islands = tierNumber
    tiers_ag = AdviceGroup(
        tier=tier_Islands,
        pre_string="Unlock all Islands",
        advices=islands_AdviceDict
    )
    overall_SectionTier = min(max_tier + infoTiers, tier_Islands)
    return tiers_ag, overall_SectionTier, max_tier

def getIslandsAdviceSection() -> AdviceSection:
    highestFishingSkillLevel = max(session_data.account.all_skills["Fishing"])
    if highestFishingSkillLevel < 30:
        islands_AdviceSection = AdviceSection(
            name="Islands",
            tier="Not Yet Evaluated",
            header="Come back after reaching level 30 Fishing!",
            picture="wiki/Island_Expeditions_Boat.gif",
            unreached=True
        )
        return islands_AdviceSection

    #Advice Groups
    islands_AdviceGroupDict = {}
    islands_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    islands_AdviceGroupDict['Trash'] = getTrashIslandAdviceGroup()
    islands_AdviceGroupDict['Fractal'] = getFractalAdviceGroup()

    #Advice Section

    tier_section = f"{overall_SectionTier}/{max_tier}"
    islands_AdviceSection = AdviceSection(
        name="Islands",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Islands tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="wiki/Island_Expeditions_Boat.gif",
        groups=islands_AdviceGroupDict.values()
    )
    return islands_AdviceSection
