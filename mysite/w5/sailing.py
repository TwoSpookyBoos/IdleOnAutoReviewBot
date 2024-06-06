from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import safe_loads
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import numberOfArtifacts, numberOfArtifactTiers, sailing_progressionTiers, sailingDict, artifactTiers, maxTiersPerGroup

logger = get_logger(__name__)

def setSailingProgressionTier():
    sailing_AdviceDict = {
        "Islands": [],
        "CaptainsAndBoats": [],
        "Artifacts": {}
    }
    sailing_AdviceGroupDict = {}
    sailing_AdviceSection = AdviceSection(
        name="Sailing",
        tier="0",
        pinchy_rating=0,
        header="Best Sailing tier met: Not Yet Evaluated",
        picture="Sailing.png"
    )
    #highestSailingSkillLevel = max(session_data.account.all_skills.get("Sailing", [0]))
    highestSailingSkillLevel = 100
    if highestSailingSkillLevel < 1:
        sailing_AdviceSection.header = "Come back after unlocking the Sailing skill in W5!"
        return sailing_AdviceSection

    tier_Islands = 0
    tier_Artifacts = 0
    max_tier = max(sailing_progressionTiers.keys())

    # Assess Tiers
    for islandIndex, islandValuesDict in sailingDict.items():
        # Discover all islands
        if not session_data.account.sailing['Islands'][islandValuesDict['Name']].get('Discovered', False):
            sailing_AdviceDict['Islands'].append(Advice(
                label=f"{islandValuesDict['Name']}: {islandValuesDict['Distance']} roundtrip Distance",
                picture_class=islandValuesDict['NormalTreasure'],
                progression=0,
                goal=1
            ))
        # Lowest 2 artifact tiers missing any artifacts
        for artifactIndex, artifactValuesDict in islandValuesDict['Artifacts'].items():
            for artifactTierIndex, artifactTierName in enumerate(artifactTiers):
                if session_data.account.sailing['Artifacts'].get(artifactValuesDict['Name']).get('Level') < artifactTierIndex+1:
                    if artifactTierName not in sailing_AdviceDict['Artifacts'] and len(sailing_AdviceDict['Artifacts']) < maxTiersPerGroup-1:
                        sailing_AdviceDict['Artifacts'][artifactTierName] = []
                        if artifactTierName == "Eldritch" and not session_data.account.eldritch_artifacts_unlocked:
                            sailing_AdviceDict['Artifacts']["Eldritch"].append(Advice(
                                label=f"Unlock Eldritch Artifacts by completing W4 Rift 30",
                                picture_class='eldritch-artifact',
                                progression=0,
                                goal=1
                            ))
                            break
                        elif artifactTierName == "Sovereign" and "Sovereign Artifacts" not in session_data.account.jade_emporium_purchases:
                            sailing_AdviceDict['Artifacts']["Sovereign"].append(Advice(
                                label=f"Unlock Sovereign Artifacts from W6 Jade Emporium",
                                picture_class='sovereign-artifacts',
                                progression=0,
                                goal=1
                            ))
                            break
                    if artifactTierName in sailing_AdviceDict['Artifacts']:
                        sailing_AdviceDict['Artifacts'][artifactTierName].append(Advice(
                            label=f"{islandValuesDict['Name']}: {artifactValuesDict['Name']}",
                            picture_class=artifactValuesDict['Name'],
                            progression=session_data.account.sailing['Artifacts'].get(artifactValuesDict['Name']).get('Level'),
                            goal=artifactTierIndex+1
                        ))

    # Generate AdviceGroups
    sailing_AdviceGroupDict['Islands'] = AdviceGroup(
        tier=str(tier_Islands),
        pre_string="Discover all Islands",
        advices=sailing_AdviceDict['Islands']
    )
    sailing_AdviceGroupDict['Artifacts'] = AdviceGroup(
        tier=str(tier_Artifacts),
        pre_string="Collect all artifacts",
        advices=sailing_AdviceDict['Artifacts']
    )

    # Generate AdviceSection
    overall_SailingTier = min(max_tier, tier_Artifacts)
    tier_section = f"{overall_SailingTier}/{max_tier}"
    sailing_AdviceSection.tier = tier_section
    sailing_AdviceSection.pinchy_rating = overall_SailingTier
    sailing_AdviceSection.groups = sailing_AdviceGroupDict.values()
    if overall_SailingTier == max_tier:
        sailing_AdviceSection.header = f"Best Sailing tier met: {tier_section}<br>You best ❤️"
    else:
        sailing_AdviceSection.header = f"Best Sailing tier met: {tier_section}"

    return sailing_AdviceSection
