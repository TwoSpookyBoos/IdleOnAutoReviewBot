from collections import defaultdict

from consts.consts_w2 import max_NBLB

from models.general.cards import Card
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.text_formatting import pl
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_w5 import max_sailing_artifact_level, sailing_artifacts_count
from consts.consts_w4 import max_nblb_bubbles
from consts.progression_tiers import sailing_progressionTiers, true_max_tiers

logger = get_logger(__name__)

def getSailingDelays() -> dict:
    delaysDict = {}
    # If Goharut is already unlocked, delay priority on Ashen Urn
    if session_data.account.divinity[5].unlocked:
        delaysDict[3] = ['Ashen Urn']
    # If Purrmep is already unlocked, delay priority on Jade Rock
    if session_data.account.divinity[7].unlocked:
        delaysDict[5] = ['Jade Rock']
    # If NBLB is already increasing the max number of bubbles (10 as of v2.11), delay Amberite
    if session_data.account.lab_bonuses['No Bubble Left Behind'].value >= max_nblb_bubbles:
        delaysDict[4] = ['Amberite']
        delaysDict[13] = ['Amberite']
        delaysDict[16] = ['Amberite']
    return delaysDict

def get_sailing_progression_tier_advicegroups():
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
            if session_data.account.sailing.islands_discovered < requirements['Islands Discovered']:
                shortBy = requirements['Islands Discovered'] - session_data.account.sailing.islands_discovered
                add_subgroup_if_available_slot(sailing_Advices['Islands Discovered'], subgroup_label)
                if subgroup_label in sailing_Advices['Islands Discovered']:
                    sailing_Advices['Islands Discovered'][subgroup_label].append(Advice(
                        label=f"Discover {shortBy} more Island{pl(shortBy)}",
                        picture_class='cloud-discover-rate',
                        progression=session_data.account.sailing.islands_discovered,
                        goal=requirements['Islands Discovered']
                    ))
        if subgroup_label not in sailing_Advices['Islands Discovered'] and tier_Islands == tier_number - 1:
            tier_Islands = tier_number

        # Captains and Boats
        if 'Captains And Boats' in requirements:
            if session_data.account.sailing.captains_owned < requirements['Captains And Boats']:
                shortBy = requirements['Captains And Boats'] - session_data.account.sailing.captains_owned
                add_subgroup_if_available_slot(sailing_Advices['Captains And Boats'], subgroup_label)
                if subgroup_label in sailing_Advices['Captains And Boats']:
                    sailing_Advices['Captains And Boats'][subgroup_label].append(Advice(
                        label=f"Hire {shortBy} more Captain{pl(shortBy)}",
                        picture_class='captain-0-idle',
                        progression=session_data.account.sailing.captains_owned,
                        goal=requirements['Captains And Boats']
                    ))
            if session_data.account.sailing.boats_owned < requirements['Captains And Boats']:
                shortBy = requirements['Captains And Boats'] - session_data.account.sailing.boats_owned
                add_subgroup_if_available_slot(sailing_Advices['Captains And Boats'], subgroup_label)
                if subgroup_label in sailing_Advices['Captains And Boats']:
                    sailing_Advices['Captains And Boats'][subgroup_label].append(Advice(
                        label=f"Purchase {shortBy} more Boat{pl(shortBy)}",
                        picture_class='sailing-ship-tier-1',
                        progression=session_data.account.sailing.boats_owned,
                        goal=requirements['Captains And Boats']
                    ))
        if subgroup_label not in sailing_Advices['Captains And Boats'] and tier_CaptainsAndBoats == tier_number - 1:
            tier_CaptainsAndBoats = tier_number

        # Outside requirement checks should be at the top of the list
        if session_data.account.sailing.artifacts.total_tiers < total_artifacts:
            if 'Eldritch' in requirements:
                if not session_data.account.rift['EldritchArtifact'].unlocked:
                    add_subgroup_if_available_slot(sailing_Advices['Artifacts'], subgroup_label)
                    if subgroup_label in sailing_Advices['Artifacts']:
                        sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                            label="Unlock Eldritch tier Artifacts by completing {{ Rift|#rift }} 30",
                            picture_class='eldritch-artifact',
                            progression=0,
                            goal=1
                        ))
            if 'Sovereign' in requirements:
                if not session_data.account.sneaking.emporium["Sovereign Artifacts"].obtained:
                    add_subgroup_if_available_slot(sailing_Advices['Artifacts'], subgroup_label)
                    if subgroup_label in sailing_Advices['Artifacts']:
                        sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                            label="Purchase \"Sovereign Artifacts\" from the {{ Jade Emporium|#sneaking }} in W6",
                            picture_class='sovereign-artifacts',
                            progression=0,
                            goal=1
                        ))
            if 'ExtraLanterns' in requirements:
                if not session_data.account.sneaking.emporium['Brighter Lighthouse Bulb'].obtained:
                    add_subgroup_if_available_slot(sailing_Advices['Artifacts'], subgroup_label)
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
                'Beanstacked' in requirements
                and session_data.account.beanstalk["Golden Hampter Gummy Candy"].tier < 1
                and session_data.account.lab_chips['Chocolatey Chip'].owned
                and session_data.account.world_progress.highest_reached >= 6
                and tier_Artifacts >= tier_number - 1
            ):
                golden_hampter_note = 'Reminder: Golden Hampters can be deposited to the Beanstalk in World 6!'
            # Artifacts
            if 'Artifacts' in requirements:
                for artifact_name, artifact_tier in requirements['Artifacts'].items():
                    if session_data.account.sailing.artifacts[artifact_name].level < artifact_tier:
                        if artifact_name not in delays_dict.get(tier_number, []):
                            add_subgroup_if_available_slot(sailing_Advices['Artifacts'], subgroup_label)
                            if subgroup_label in sailing_Advices['Artifacts']:
                                sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                                    label=artifact_name,
                                    picture_class=artifact_name,
                                    progression=session_data.account.sailing.artifacts[artifact_name].level,
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

def get_sailing_speed_advicegroup() -> AdviceGroup:
    sailing = session_data.account.sailing
    divinity = session_data.account.divinity
    purrmep = divinity.named('Purrmep')
    goharut = divinity.named('Goharut')
    bagur = divinity.named('Bagur')
    crawler: Card = next(card for card in session_data.account.cards if card.name == 'Crawler')
    kattlekruk: Card = next(card for card in session_data.account.cards if card.name == 'Kattlekruk')
    boaty_bubble = session_data.account.alchemy_bubbles['Boaty Bubble']
    multi_total = sailing.speed_multi

    speed_advices = {
        f'Total: {multi_total}x': [sailing.get_speed_advice()],
        f'Multi Group A: {sailing.speed_multi_a}x': [
            sailing.get_purrmep_minor_advice(),
            crawler.getAdvice(),
            kattlekruk.getAdvice(),
            boaty_bubble.get_bonus_advice(goal=max_NBLB)
        ],
        f'Multi Group B: {sailing.speed_multi_b}x': [
            goharut.get_blessing_advice(f": +{sailing.goharut_bonus}%")
        ],
        f'Multi Group C: {sailing.speed_multi_c}x': [
            purrmep.get_blessing_advice(f": +{sailing.purrmep_blessing_bonus}%")
        ],
        f'Multi Group D: {sailing.speed_multi_d}x': [sailing.get_ballot_advice()],
        f'Multi Group E: {sailing.speed_multi_e}x': [
            bagur.get_blessing_advice(f": +{sailing.bagur_bonus}%"),
            sailing.get_ad_tablet_advice(),
            session_data.account.stamps['Sailboat Stamp'].get_advice(),
            sailing.get_boat_statue_advice(),
            session_data.account.meals['Popped Corn'].get_bonus_advice(),
            session_data.account.alchemy_vials['Oj Jooce (Orange Slice)'].get_advice(full_name=False),
            sailing.get_skill_mastery_advice(),
            sailing.get_msa_advice(session_data.account.worship.max_total_waves),
            sailing.get_c_shanti_advice(),
        ],
        f'Multi Group F: {sailing.speed_multi_f}x': [
            session_data.account.gemshop.purchases['Davey Jones Training'].get_advice(),
            session_data.account.legend_talents['Davey Jones Returns'].get_advice()
        ]
    }

    for subgroup in speed_advices:
        for advice in speed_advices[subgroup]:
            advice.mark_advice_completed()

    sailingSpeedAdviceGroup = AdviceGroup(
        tier='',
        pre_string='Sources of Sailing Speed',
        advices=speed_advices,
        informational=True,
    )

    return sailingSpeedAdviceGroup

def get_sailing_artifacts_advicegroup() -> AdviceGroup:
    arti_advices = defaultdict(list)
    for artifact in session_data.account.sailing.artifacts.values():
        arti_advices[artifact.island].append(artifact.get_advice(link_to_section=False))

    for island_name in arti_advices:
        for advice in arti_advices[island_name]:
            advice.mark_advice_completed()

    arti_ag = AdviceGroup(
        tier='',
        pre_string='Artifact Bonuses',
        advices=arti_advices,
        informational=True
    )
    return arti_ag

def get_sailing_advicesection() -> AdviceSection:
    highest_sailing_level = max(session_data.account.characters.all_skills['Sailing'])
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
    sailing_AdviceGroupDict, overall_SectionTier, max_tier, true_max = get_sailing_progression_tier_advicegroups()
    sailing_AdviceGroupDict['SailingSpeed'] = get_sailing_speed_advicegroup()
    sailing_AdviceGroupDict['Artifacts Info'] = get_sailing_artifacts_advicegroup()

    # Generate AdviceSection
    tier_section = f'{overall_SectionTier}/{max_tier}'
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
