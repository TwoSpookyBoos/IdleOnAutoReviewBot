from consts.consts_w1 import stamp_maxes
from consts.consts_w2 import max_vial_level
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_w5 import max_sailing_artifact_level, sailing_artifacts_count
from consts.consts_w4 import max_nblb_bubbles, max_meal_level
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

def getSailingSpeedAdviceGroup() -> AdviceGroup:
    speed_advices = []

    registered_slab_count = len(session_data.account.registered_slab)

    ad_tablet_level = session_data.account.sailing['Artifacts']['10 AD Tablet']['Level']
    ad_tablet_bonus_percent = 4 * ad_tablet_level * (registered_slab_count - 500) / 10

    speed_advices.append(Advice(
        label=f"{{{{ Sailing|#sailing }}}}: Level {ad_tablet_level} 10 AD Tablet: +{ad_tablet_bonus_percent}%",
        picture_class='10-ad-tablet',
        progression=session_data.account.sailing['Artifacts']['10 AD Tablet']['Level'],
        goal=3
    ))

    cards = ['Crawler', 'Kattlekruk']
    for card_name in cards:
        speed_advices.append(next(c for c in session_data.account.cards if c.name == card_name).getAdvice())

    goharut = next((divinity for divinity in session_data.account.divinity['Divinities'].values() if divinity.get('Name') == 'Goharut'), None)
    speed_advices.append(Advice(
        label=f"{goharut.get('Name')} Blessing: +{4 * goharut.get('BlessingLevel')}%",
        picture_class=goharut.get('Name'),
        progression=goharut.get('BlessingLevel'),
        goal=100,
        resource=goharut.get('BlessingMaterial')
    ))

    purrmep = next((divinity for divinity in session_data.account.divinity['Divinities'].values() if divinity.get('Name') == 'Purrmep'), None)
    anyone_linked_to_purrmep: bool = False
    for char in session_data.account.safe_characters:
        if char.divinity_link == "Purrmep":
            anyone_linked_to_purrmep = True
            break

    speed_advices.append(Advice(
        label=f"At least one {purrmep.get('Name')} Minor Link: +50%",
        picture_class=purrmep.get('Name'),
        progression=1 if anyone_linked_to_purrmep else 0,
        goal=1
    ))

    speed_advices.append(Advice(
        label=f"{purrmep.get('Name')} Blessing: +{3 * purrmep.get('BlessingLevel')}%",
        picture_class=purrmep.get('Name'),
        progression=purrmep.get('BlessingLevel'),
        goal=100,
        resource=purrmep.get('BlessingMaterial')
    ))

    bagur = next((divinity for divinity in session_data.account.divinity['Divinities'].values() if divinity.get('Name') == 'Bagur'), None)
    speed_advices.append(Advice(
        label=f"{bagur.get('Name')} Blessing: +{5 * bagur.get('BlessingLevel')}%",
        picture_class=bagur.get('Name'),
        progression=bagur.get('BlessingLevel'),
        goal=100,
        resource=bagur.get('BlessingMaterial')
    ))

    has_msa_sailing = session_data.account.gaming['SuperBits']['MSA Sailing']['Unlocked']
    total_worship_waves = sum([totem['Waves'] for totem in session_data.account.worship['Totems'].values()])
    speed_advices.append(Advice(
        label=f"MSA Sailing: +{has_msa_sailing * total_worship_waves / 10}% (+0.1% per wave in Worship)",
        picture_class="worship",
        progression=total_worship_waves,
        goal=len(session_data.account.worship['Totems'].keys()) * 300,
    ))

    boaty_bubble = session_data.account.alchemy_bubbles['Boaty Bubble']
    speed_advices.append(Advice(
        label=f"{{{{ Alchemy Bubbles|#bubbles }}}} - Boaty Bubble: +{round(boaty_bubble['BaseValue'], 2)}/135%",
        picture_class='boaty-bubble',
        progression=boaty_bubble['Level'],
        resource=boaty_bubble['Material'],
    ))

    popped_corn = session_data.account.meals['Popped Corn']
    speed_advices.append(Advice(
        label=f"{{{{ Meal|#cooking }}}} - Popped Corn: {popped_corn['Description']}",
        picture_class=popped_corn['Image'],
        progression=popped_corn['Level'],
        goal=max_meal_level
    ))

    has_skill_mastery = session_data.account.rift['SkillMastery']
    total_sailing_level = sum(session_data.account.all_skills['Sailing'])

    speed_advices.append(Advice(
        label=f"{{{{ Rift|#rift }}}} - Sailing Skill Mastery > 200: +{has_skill_mastery * 15}%",
        picture_class="skill-mastery",
        progression=total_sailing_level,
        goal=200
    ))

    sailboat_stamp = session_data.account.stamps['Sailboat Stamp']
    speed_advices.append(Advice(
        label=f"Sailboat Stamp: {round(sailboat_stamp['Total Value'], 2):g}%",
        picture_class='Sailboat Stamp',
        progression=sailboat_stamp['Level'],
        goal=stamp_maxes['Sailboat Stamp'],
        resource=sailboat_stamp['Material'],
    ))

    oj_jooce_vial = session_data.account.alchemy_vials['Oj Jooce (Orange Slice)']
    speed_advices.append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Oj Jooce: {oj_jooce_vial['Value']:.2f}%",
        picture_class='orange-slice',
        progression=oj_jooce_vial['Level'],
        goal=max_vial_level
    ))

    for advice in speed_advices:
        mark_advice_completed(advice)

    sailingSpeedAdviceGroup = AdviceGroup(
        tier='',
        pre_string='Sources of Sailing Speed',
        advices=speed_advices,
        informational=True,
    )

    return sailingSpeedAdviceGroup

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

    sailing_AdviceGroupDict["SailingSpeed"] = getSailingSpeedAdviceGroup()

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
