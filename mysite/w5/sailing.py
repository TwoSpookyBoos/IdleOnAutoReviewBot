from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import sailing_progressionTiers, numberOfArtifactTiers, numberOfArtifacts, nblbMaxBubbleCount, break_you_best

logger = get_logger(__name__)

def getSailingDelays() -> dict:
    delaysDict = {}
    # If Goharut is already unlocked, delay priority on Ashen Urn
    if session_data.account.divinity['Divinities'][5]['Unlocked']:
        delaysDict[3] = ["Ashen Urn"]
    # If Purrmep is already unlocked, delay priority on Jade Rock
    if session_data.account.divinity['Divinities'][7]['Unlocked']:
        delaysDict[5] = ["Jade Rock"]
    # If NBLB is already increasing the max number of bubbles (10 as of v2.11), delay Amberite
    if session_data.account.labBonuses['No Bubble Left Behind']['Value'] >= nblbMaxBubbleCount:
        delaysDict[4] = ["Amberite"]
        delaysDict[13] = ["Amberite"]
        delaysDict[16] = ["Amberite"]
    return delaysDict

def getSailingProgressionTierAdviceGroups():
    sailing_AdviceDict = {
        "IslandsDiscovered": {},
        "CaptainsAndBoats": {},
        "Artifacts": {}
    }
    sailing_AdviceGroupDict = {}
    info_tiers = 0
    max_tier = max(sailing_progressionTiers.keys()) - info_tiers
    tier_Islands = 0
    tier_CaptainsAndBoats = 0
    tier_Artifacts = 0
    total_artifacts = numberOfArtifactTiers * numberOfArtifacts
    delaysDict = getSailingDelays()
    golden_hampter_note = ''

    # Assess Tiers
    for tierNumber, tierRequirementsDict in sailing_progressionTiers.items():
        subgroupName = f"To Reach Tier {tierNumber}"
        # Islands
        if 'IslandsDiscovered' in tierRequirementsDict:
            if session_data.account.sailing['IslandsDiscovered'] < tierRequirementsDict['IslandsDiscovered']:
                shortBy = tierRequirementsDict['IslandsDiscovered'] - session_data.account.sailing['IslandsDiscovered']
                if subgroupName not in sailing_AdviceDict['IslandsDiscovered'] and len(sailing_AdviceDict['IslandsDiscovered']) < session_data.account.maxSubgroupsPerGroup:
                    sailing_AdviceDict['IslandsDiscovered'][subgroupName] = []
                if subgroupName in sailing_AdviceDict['IslandsDiscovered']:
                    sailing_AdviceDict['IslandsDiscovered'][subgroupName].append(Advice(
                        label=f"Discover {shortBy} more Island{pl(shortBy)}",
                        picture_class="cloud-discover-rate",
                        progression=session_data.account.sailing['IslandsDiscovered'],
                        goal=tierRequirementsDict['IslandsDiscovered']
                    ))
        if subgroupName not in sailing_AdviceDict['IslandsDiscovered'] and tier_Islands == tierNumber - 1:
            tier_Islands = tierNumber

        # Captains and Boats
        if 'CaptainsAndBoats' in tierRequirementsDict:
            if session_data.account.sailing['CaptainsOwned'] < tierRequirementsDict['CaptainsAndBoats']:
                shortBy = tierRequirementsDict['CaptainsAndBoats'] - session_data.account.sailing['CaptainsOwned']
                if subgroupName not in sailing_AdviceDict['CaptainsAndBoats'] and len(sailing_AdviceDict['CaptainsAndBoats']) < session_data.account.maxSubgroupsPerGroup - 1:
                    sailing_AdviceDict['CaptainsAndBoats'][subgroupName] = []
                if subgroupName in sailing_AdviceDict['CaptainsAndBoats']:
                    sailing_AdviceDict['CaptainsAndBoats'][subgroupName].append(Advice(
                        label=f"Hire {shortBy} more Captain{pl(shortBy)}",
                        picture_class="captain-0-idle",
                        progression=session_data.account.sailing['CaptainsOwned'],
                        goal=tierRequirementsDict['CaptainsAndBoats']
                    ))
            if session_data.account.sailing['BoatsOwned'] < tierRequirementsDict['CaptainsAndBoats']:
                shortBy = tierRequirementsDict['CaptainsAndBoats'] - session_data.account.sailing['BoatsOwned']
                if subgroupName not in sailing_AdviceDict['CaptainsAndBoats'] and len(sailing_AdviceDict['CaptainsAndBoats']) < session_data.account.maxSubgroupsPerGroup - 1:
                    sailing_AdviceDict['CaptainsAndBoats'][subgroupName] = []
                if subgroupName in sailing_AdviceDict['CaptainsAndBoats']:
                    sailing_AdviceDict['CaptainsAndBoats'][subgroupName].append(Advice(
                        label=f"Purchase {shortBy} more Boat{pl(shortBy)}",
                        picture_class="sailing-ship-tier-1",
                        progression=session_data.account.sailing['BoatsOwned'],
                        goal=tierRequirementsDict['CaptainsAndBoats']
                    ))
        if subgroupName not in sailing_AdviceDict['CaptainsAndBoats'] and tier_CaptainsAndBoats == tierNumber - 1:
            tier_CaptainsAndBoats = tierNumber

        # Outside requirement checks should be at the top of the list
        if session_data.account.sum_artifact_tiers < total_artifacts:
            if 'Eldritch' in tierRequirementsDict:
                if not session_data.account.rift['EldritchArtifacts']:
                    if subgroupName not in sailing_AdviceDict['Artifacts'] and len(sailing_AdviceDict['Artifacts']) < session_data.account.maxSubgroupsPerGroup:
                        sailing_AdviceDict['Artifacts'][subgroupName] = []
                    if subgroupName in sailing_AdviceDict['Artifacts']:
                        sailing_AdviceDict['Artifacts'][subgroupName].append(Advice(
                            label="Unlock Eldritch tier Artifacts by completing {{ Rift|#rift }} 30",
                            picture_class="eldritch-artifact",
                        ))
            if 'Sovereign' in tierRequirementsDict:
                if not session_data.account.sneaking['JadeEmporium']["Sovereign Artifacts"]['Obtained']:
                    if subgroupName not in sailing_AdviceDict['Artifacts'] and len(sailing_AdviceDict['Artifacts']) < session_data.account.maxSubgroupsPerGroup:
                        sailing_AdviceDict['Artifacts'][subgroupName] = []
                    if subgroupName in sailing_AdviceDict['Artifacts']:
                        sailing_AdviceDict['Artifacts'][subgroupName].append(Advice(
                            label="Purchase \"Sovereign Artifacts\" from the {{ Jade Emporium|#sneaking }} in W6",
                            picture_class="sovereign-artifacts",
                        ))
            if 'ExtraLanterns' in tierRequirementsDict:
                if not session_data.account.sneaking['JadeEmporium']['Brighter Lighthouse Bulb']['Obtained']:
                    if subgroupName not in sailing_AdviceDict['Artifacts'] and len(sailing_AdviceDict['Artifacts']) < session_data.account.maxSubgroupsPerGroup:
                        sailing_AdviceDict['Artifacts'][subgroupName] = []
                    if subgroupName in sailing_AdviceDict['Artifacts']:
                        sailing_AdviceDict['Artifacts'][subgroupName].append(Advice(
                            label="Purchase \"Brighter Lighthouse Bulb\" from the {{ Jade Emporium|#sneaking }} in W6",
                            picture_class="brighter-lighthouse-bulb",
                        ))
            # Golden Hampters
            if (
                #If Golden Hampters are not 10k Beanstacked and the player has a Chocolatey Chip to active farm them
                'Beanstacked' in tierRequirementsDict and
                not session_data.account.sneaking.get('Beanstalk', {}).get('FoodG10', {}).get('Beanstacked', False)
                and session_data.account.labChips.get('Chocolatey Chip', 0) > 0
                and session_data.account.highestWorldReached >= 6
                and tier_Artifacts >= tierNumber - 1
            ):
                golden_hampter_note = 'Reminder: Golden Hampters can be deposited to the Beanstalk in World 6!'
            # Artifacts
            if 'Artifacts' in tierRequirementsDict:
                for artifactName, artifactTier in tierRequirementsDict['Artifacts'].items():
                    if session_data.account.sailing['Artifacts'].get(artifactName, {}).get('Level', 0) < artifactTier:
                        if artifactName not in delaysDict.get(tierNumber, []):
                            if subgroupName not in sailing_AdviceDict['Artifacts'] and len(sailing_AdviceDict['Artifacts']) < session_data.account.maxSubgroupsPerGroup:
                                sailing_AdviceDict['Artifacts'][subgroupName] = []
                            if subgroupName in sailing_AdviceDict['Artifacts']:
                                sailing_AdviceDict['Artifacts'][subgroupName].append(Advice(
                                    label=artifactName,
                                    picture_class=artifactName,
                                    progression=session_data.account.sailing['Artifacts'].get(artifactName, {}).get('Level', 0),
                                    goal=artifactTier
                                ))
        if subgroupName not in sailing_AdviceDict['Artifacts'] and tier_Artifacts == tierNumber - 1:
            tier_Artifacts = tierNumber

    # Generate AdviceGroups
    sailing_AdviceGroupDict['IslandsDiscovered'] = AdviceGroup(
        tier=str(tier_Islands),
        pre_string=f"Land ho! Discover all Islands",
        advices=sailing_AdviceDict['IslandsDiscovered']
    )
    sailing_AdviceGroupDict['CaptainsAndBoats'] = AdviceGroup(
        tier=str(tier_CaptainsAndBoats),
        pre_string=f"Gather yer sea dogs! Hire captains and purchase boats",
        advices=sailing_AdviceDict['CaptainsAndBoats']
    )
    sailing_AdviceGroupDict['Artifacts'] = AdviceGroup(
        tier=str(tier_Artifacts),
        pre_string=f"Amass booty! Collect all artifacts",
        advices=sailing_AdviceDict['Artifacts'],
        post_string=golden_hampter_note
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Islands, tier_CaptainsAndBoats, tier_Artifacts)
    return sailing_AdviceGroupDict, overall_SectionTier, max_tier, max_tier + info_tiers

def getSailingAdviceSection() -> AdviceSection:
    highestSailingSkillLevel = max(session_data.account.all_skills.get("Sailing", [0]))
    if highestSailingSkillLevel < 1:
        sailing_AdviceSection = AdviceSection(
            name="Sailing",
            tier="0",
            pinchy_rating=0,
            header="Come back after unlocking the Sailing skill in W5!",
            picture="Sailing.png",
            unreached=True
        )
        return sailing_AdviceSection

    #Generate AdviceGroup
    sailing_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getSailingProgressionTierAdviceGroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    sailing_AdviceSection = AdviceSection(
        name="Sailing",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Sailing tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Sailing.png",
        groups=sailing_AdviceGroupDict.values()
    )

    return sailing_AdviceSection
