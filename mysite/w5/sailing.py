from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_w5 import max_sailing_artifact_level, sailing_artifacts_count
from consts.consts_w4 import max_nblb_bubbles
from consts.progression_tiers import sailing_progressionTiers, true_max_tiers

logger = get_logger(__name__)

def getSailingDelays() -> dict:
    delaysDict = {}
    # If Goharut is already unlocked, delay priority on Ashen Urn
    if session_data.account.divinity['Divinities'][5]['Unlocked']:
        delaysDict[3] = ['Ashen Urn']
    # If Purrmep is already unlocked, delay priority on Jade Rock
    if session_data.account.divinity['Divinities'][7]['Unlocked']:
        delaysDict[5] = ['Jade Rock']
    # If NBLB is already increasing the max number of bubbles (10 as of v2.11), delay Amberite
    if session_data.account.labBonuses['No Bubble Left Behind']['Value'] >= max_nblb_bubbles:
        delaysDict[4] = ['Amberite']
        delaysDict[13] = ['Amberite']
        delaysDict[16] = ['Amberite']
    return delaysDict

def getSailingProgressionTierAdviceGroups():
    sailing_Advices = {
        'Islands Discovered': {},
        'Captains And Boats': {},
        'Artifacts': {}
    }
    sailing_AdviceGroups = {}
    optional_tiers = 0
    true_max = true_max_tiers['Sailing']
    max_tier = true_max - optional_tiers
    tier_Islands = 0
    tier_CaptainsAndBoats = 0
    tier_Artifacts = 0
    total_artifacts = max_sailing_artifact_level * sailing_artifacts_count
    delays_dict = getSailingDelays()
    golden_hampter_note = ''

    # Assess Tiers
    for tier_number, requirements in sailing_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        # Islands
        if 'Islands Discovered' in requirements:
            if session_data.account.sailing['Islands Discovered'] < requirements['Islands Discovered']:
                shortBy = requirements['Islands Discovered'] - session_data.account.sailing['Islands Discovered']
                if (
                    subgroup_label not in sailing_Advices['Islands Discovered']
                    and len(sailing_Advices['Islands Discovered']) < session_data.account.max_subgroups
                ):
                    sailing_Advices['Islands Discovered'][subgroup_label] = []
                if subgroup_label in sailing_Advices['Islands Discovered']:
                    sailing_Advices['Islands Discovered'][subgroup_label].append(Advice(
                        label=f"Discover {shortBy} more Island{pl(shortBy)}",
                        picture_class='cloud-discover-rate',
                        progression=session_data.account.sailing['Islands Discovered'],
                        goal=requirements['Islands Discovered']
                    ))
        if subgroup_label not in sailing_Advices['Islands Discovered'] and tier_Islands == tier_number - 1:
            tier_Islands = tier_number

        # Captains and Boats
        if 'Captains And Boats' in requirements:
            if session_data.account.sailing['CaptainsOwned'] < requirements['Captains And Boats']:
                shortBy = requirements['Captains And Boats'] - session_data.account.sailing['CaptainsOwned']
                if (
                    subgroup_label not in sailing_Advices['Captains And Boats']
                    and len(sailing_Advices['Captains And Boats']) < session_data.account.max_subgroups
                ):
                    sailing_Advices['Captains And Boats'][subgroup_label] = []
                if subgroup_label in sailing_Advices['Captains And Boats']:
                    sailing_Advices['Captains And Boats'][subgroup_label].append(Advice(
                        label=f"Hire {shortBy} more Captain{pl(shortBy)}",
                        picture_class='captain-0-idle',
                        progression=session_data.account.sailing['CaptainsOwned'],
                        goal=requirements['Captains And Boats']
                    ))
            if session_data.account.sailing['BoatsOwned'] < requirements['Captains And Boats']:
                shortBy = requirements['Captains And Boats'] - session_data.account.sailing['BoatsOwned']
                if (
                    subgroup_label not in sailing_Advices['Captains And Boats']
                    and len(sailing_Advices['Captains And Boats']) < session_data.account.max_subgroups
                ):
                    sailing_Advices['Captains And Boats'][subgroup_label] = []
                if subgroup_label in sailing_Advices['Captains And Boats']:
                    sailing_Advices['Captains And Boats'][subgroup_label].append(Advice(
                        label=f"Purchase {shortBy} more Boat{pl(shortBy)}",
                        picture_class='sailing-ship-tier-1',
                        progression=session_data.account.sailing['BoatsOwned'],
                        goal=requirements['Captains And Boats']
                    ))
        if subgroup_label not in sailing_Advices['Captains And Boats'] and tier_CaptainsAndBoats == tier_number - 1:
            tier_CaptainsAndBoats = tier_number

        # Outside requirement checks should be at the top of the list
        if session_data.account.sum_artifact_tiers < total_artifacts:
            if 'Eldritch' in requirements:
                if not session_data.account.rift['EldritchArtifacts']:
                    if (
                        subgroup_label not in sailing_Advices['Artifacts']
                        and len(sailing_Advices['Artifacts']) < session_data.account.max_subgroups
                    ):
                        sailing_Advices['Artifacts'][subgroup_label] = []
                    if subgroup_label in sailing_Advices['Artifacts']:
                        sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                            label="Unlock Eldritch tier Artifacts by completing {{ Rift|#rift }} 30",
                            picture_class='eldritch-artifact',
                            progression=0,
                            goal=1
                        ))
            if 'Sovereign' in requirements:
                if not session_data.account.sneaking['JadeEmporium']["Sovereign Artifacts"]['Obtained']:
                    if subgroup_label not in sailing_Advices['Artifacts'] and len(sailing_Advices['Artifacts']) < session_data.account.max_subgroups:
                        sailing_Advices['Artifacts'][subgroup_label] = []
                    if subgroup_label in sailing_Advices['Artifacts']:
                        sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                            label="Purchase \"Sovereign Artifacts\" from the {{ Jade Emporium|#sneaking }} in W6",
                            picture_class='sovereign-artifacts',
                            progression=0,
                            goal=1
                        ))
            if 'ExtraLanterns' in requirements:
                if not session_data.account.sneaking['JadeEmporium']['Brighter Lighthouse Bulb']['Obtained']:
                    if subgroup_label not in sailing_Advices['Artifacts'] and len(sailing_Advices['Artifacts']) < session_data.account.max_subgroups:
                        sailing_Advices['Artifacts'][subgroup_label] = []
                    if subgroup_label in sailing_Advices['Artifacts']:
                        sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                            label="Purchase \"Brighter Lighthouse Bulb\" from the {{ Jade Emporium|#sneaking }} in W6",
                            picture_class='brighter-lighthouse-bulb',
                            progression=0,
                            goal=1
                        ))
            # Golden Hampters
            if (
                #If Golden Hampters are not 10k Beanstacked and the player has a Chocolatey Chip to active farm them
                'Beanstacked' in requirements and
                not session_data.account.sneaking.get('Beanstalk', {}).get('FoodG10', {}).get('Beanstacked', False)
                and session_data.account.labChips.get('Chocolatey Chip', 0) > 0
                and session_data.account.highest_world_reached >= 6
                and tier_Artifacts >= tier_number - 1
            ):
                golden_hampter_note = 'Reminder: Golden Hampters can be deposited to the Beanstalk in World 6!'
            # Artifacts
            if 'Artifacts' in requirements:
                for artifact_name, artifact_tier in requirements['Artifacts'].items():
                    if session_data.account.sailing['Artifacts'].get(artifact_name, {}).get('Level', 0) < artifact_tier:
                        if artifact_name not in delays_dict.get(tier_number, []):
                            if subgroup_label not in sailing_Advices['Artifacts'] and len(sailing_Advices['Artifacts']) < session_data.account.max_subgroups:
                                sailing_Advices['Artifacts'][subgroup_label] = []
                            if subgroup_label in sailing_Advices['Artifacts']:
                                sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                                    label=artifact_name,
                                    picture_class=artifact_name,
                                    progression=session_data.account.sailing['Artifacts'].get(artifact_name, {}).get('Level', 0),
                                    goal=artifact_tier
                                ))
        if subgroup_label not in sailing_Advices['Artifacts'] and tier_Artifacts == tier_number - 1:
            tier_Artifacts = tier_number

    # Generate AdviceGroups
    sailing_AdviceGroups['Islands Discovered'] = AdviceGroup(
        tier=tier_Islands,
        pre_string='Land ho! Discover all Islands',
        advices=sailing_Advices['Islands Discovered']
    )
    sailing_AdviceGroups['Captains And Boats'] = AdviceGroup(
        tier=tier_CaptainsAndBoats,
        pre_string='Gather yer sea dogs! Hire captains and purchase boats',
        advices=sailing_Advices['Captains And Boats']
    )
    sailing_AdviceGroups['Artifacts'] = AdviceGroup(
        tier=tier_Artifacts,
        pre_string='Amass booty! Collect all artifacts',
        advices=sailing_Advices['Artifacts'],
        post_string=golden_hampter_note
    )
    overall_SectionTier = min(true_max, tier_Islands, tier_CaptainsAndBoats, tier_Artifacts)
    return sailing_AdviceGroups, overall_SectionTier, max_tier, true_max

def getSailingAdviceSection() -> AdviceSection:
    highest_sailing_level = max(session_data.account.all_skills['Sailing'])
    if highest_sailing_level < 1:
        sailing_AdviceSection = AdviceSection(
            name='Sailing',
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking the Sailing skill in W5!',
            picture='Sailing.png',
            unreached=True
        )
        return sailing_AdviceSection

    #Generate AdviceGroup
    sailing_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getSailingProgressionTierAdviceGroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    sailing_AdviceSection = AdviceSection(
        name='Sailing',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Sailing tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Sailing.png',
        groups=sailing_AdviceGroupDict.values()
    )

    return sailing_AdviceSection
