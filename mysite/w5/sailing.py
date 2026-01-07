from collections import defaultdict

from consts.consts_w2 import max_vial_level, max_NBLB
from consts.consts_w3 import totems_max_wave

from models.general.character import Character
from models.general.cards import Card
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data
from models.advice.generators.w5 import get_sailing_artifact_advice
from models.advice.generators.w7 import get_legend_talent_advice
from models.advice.generators.general import get_gem_shop_purchase_advice

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.text_formatting import pl
from utils.number_formatting import round_and_trim
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, build_subgroup_label, ValueToMulti
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
            if session_data.account.sailing['Islands Discovered'] < requirements['Islands Discovered']:
                shortBy = requirements['Islands Discovered'] - session_data.account.sailing['Islands Discovered']
                add_subgroup_if_available_slot(sailing_Advices['Islands Discovered'], subgroup_label)
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
                add_subgroup_if_available_slot(sailing_Advices['Captains And Boats'], subgroup_label)
                if subgroup_label in sailing_Advices['Captains And Boats']:
                    sailing_Advices['Captains And Boats'][subgroup_label].append(Advice(
                        label=f"Hire {shortBy} more Captain{pl(shortBy)}",
                        picture_class='captain-0-idle',
                        progression=session_data.account.sailing['CaptainsOwned'],
                        goal=requirements['Captains And Boats']
                    ))
            if session_data.account.sailing['BoatsOwned'] < requirements['Captains And Boats']:
                shortBy = requirements['Captains And Boats'] - session_data.account.sailing['BoatsOwned']
                add_subgroup_if_available_slot(sailing_Advices['Captains And Boats'], subgroup_label)
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
                    add_subgroup_if_available_slot(sailing_Advices['Artifacts'], subgroup_label)
                    if subgroup_label in sailing_Advices['Artifacts']:
                        sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                            label="Unlock Eldritch tier Artifacts by completing {{ Rift|#rift }} 30",
                            picture_class='eldritch-artifact',
                            progression=0,
                            goal=1
                        ))
            if 'Sovereign' in requirements:
                if not session_data.account.sneaking['JadeEmporium']["Sovereign Artifacts"]['Obtained']:
                    add_subgroup_if_available_slot(sailing_Advices['Artifacts'], subgroup_label)
                    if subgroup_label in sailing_Advices['Artifacts']:
                        sailing_Advices['Artifacts'][subgroup_label].append(Advice(
                            label="Purchase \"Sovereign Artifacts\" from the {{ Jade Emporium|#sneaking }} in W6",
                            picture_class='sovereign-artifacts',
                            progression=0,
                            goal=1
                        ))
            if 'ExtraLanterns' in requirements:
                if not session_data.account.sneaking['JadeEmporium']['Brighter Lighthouse Bulb']['Obtained']:
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
                            add_subgroup_if_available_slot(sailing_Advices['Artifacts'], subgroup_label)
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

def get_sailing_speed_advicegroup() -> AdviceGroup:
    # "BoatSpeed" in source. Last updated in v2.49 Dec 24 2025
    # Multi Group A -- Purrmep Minor Link, Cards, Bubble
    purrmep = next((divinity for divinity in session_data.account.divinity['Divinities'].values() if divinity.get('Name') == 'Purrmep'))
    purrmep_base_max_minor_bonus = 50
    char_linked_to_purrmep: Character | None = None
    for char in session_data.account.safe_characters:
        if char.divinity_link == 'Purrmep':
            char_linked_to_purrmep = char
            break

    crawler: Card = next(card for card in session_data.account.cards if card.name == 'Crawler')
    kattlekruk: Card = next(card for card in session_data.account.cards if card.name == 'Kattlekruk')

    boaty_bubble = session_data.account.alchemy_bubbles['Boaty Bubble']

    big_p = session_data.account.alchemy_bubbles['Big P']

    purrmep_minor_bonus = 0
    if char_linked_to_purrmep is not None:
        purrmep_minor_bonus = char_linked_to_purrmep.divinity_level / (60 + char_linked_to_purrmep.divinity_level) * big_p['BaseValue'] * purrmep_base_max_minor_bonus

    multi_group_a = 1 + (purrmep_minor_bonus + 4 * crawler.level + 6 * kattlekruk.level + boaty_bubble['BaseValue']) / 125
    multi_group_a = round(multi_group_a, 2)

    # Multi Group B -- Goharut Blessing
    goharut = next((divinity for divinity in session_data.account.divinity['Divinities'].values() if divinity.get('Name') == 'Goharut'))

    multi_group_b = ValueToMulti(4 * goharut['BlessingLevel'])
    multi_group_b = round(multi_group_b, 2)

    # Multi Group C -- Purrmep Blessing
    multi_group_c = ValueToMulti(3 * purrmep['BlessingLevel'])
    multi_group_c = round(multi_group_c, 2)

    # Multi Group D -- Ballot Bonus

    sailing_ballot_buff_index, sailing_ballot_buff = next(
        (i, buff) for i, buff in session_data.account.ballot['Buffs'].items()
        if 'Sailing Speed' in buff['Description']
    )
    is_current_ballot_buff = session_data.account.ballot['CurrentBuff'] == sailing_ballot_buff_index
    sailing_ballot_buff_mult = ValueToMulti(is_current_ballot_buff * sailing_ballot_buff['Value'])

    multi_group_d = sailing_ballot_buff_mult
    multi_group_d = round(multi_group_d, 2)

    # Multi Group E -- All other bonuses
    bagur = next((divinity for divinity in session_data.account.divinity['Divinities'].values() if divinity.get('Name') == 'Bagur'), None)

    ad_tablet_level = session_data.account.sailing['Artifacts']['10 AD Tablet']['Level']
    registered_slab_count = len(session_data.account.registered_slab)
    lab_bonus_slab_sovereignty = session_data.account.labBonuses['Slab Sovereignty']
    lab_bonus_slab_sovereignty_mult = ValueToMulti(lab_bonus_slab_sovereignty['Value']) * lab_bonus_slab_sovereignty['Enabled']
    ad_tablet_bonus_percent = ((4 * ad_tablet_level * ((registered_slab_count - 500) // 10)) * lab_bonus_slab_sovereignty_mult) if registered_slab_count >= 500 else 0

    sailboat_stamp = session_data.account.stamps['Sailboat Stamp']

    boat_statue = session_data.account.statues['Boat Statue']

    popped_corn = session_data.account.meals['Popped Corn']

    oj_jooce_vial = session_data.account.alchemy_vials['Oj Jooce (Orange Slice)']

    has_skill_mastery: bool = session_data.account.rift['SkillMastery']
    total_sailing_level = sum(session_data.account.all_skills['Sailing'])

    has_msa_sailing: bool = session_data.account.gaming['SuperBits']['MSA Sailing']['Unlocked']
    total_worship_waves = sum([totem['Waves'] for totem in session_data.account.worship['Totems'].values()])

    c_shanti_minor = session_data.account.star_signs['C. Shanti Minor']

    multi_group_e = 1 + (
            5 * bagur['BlessingLevel'] +
            ad_tablet_bonus_percent +
            sailboat_stamp.total_value +
            (boat_statue['Type'] != 'Normal') * boat_statue['Value'] +
            popped_corn['Value'] +
            oj_jooce_vial['Value'] +
            has_skill_mastery * (total_sailing_level > 200) * 15 +
            has_msa_sailing * (total_worship_waves // 10) +
            c_shanti_minor['Unlocked'] * 20
    ) / 125
    multi_group_e = round(multi_group_e, 2)

    # Multi Group F -- Davey Jones Bonus + Legend Talents
    # "DaveyJonesBonus" in source. Last updated in v2.49 Dec 24 2025
    multi_group_f = ValueToMulti(
        50 * session_data.account.gemshop['Purchases']['Davey Jones Training']['Owned']
        + session_data.account.legend_talents['Talents']['Davey Jones Returns']['Value']
    )
    multi_group_f = round_and_trim(multi_group_f)

    multi_total = round(multi_group_a * multi_group_b * multi_group_c * multi_group_d * multi_group_e * multi_group_f, 2)

    speed_advices = {
        f'Total: {multi_total}x': [
            Advice(
                label=f'Total Sailing Speed bonus: {multi_total}x',
                picture_class='sailing',
            )
        ],
        f'Multi Group A: {multi_group_a}x': [
            Advice(
                label=f"Anyone Minor Linked to {purrmep.get('Name')}: +{purrmep_minor_bonus:.2f}%",
                picture_class=purrmep.get('Name'),
                progression=int(char_linked_to_purrmep is not None),
                goal=1
            ),
            crawler.getAdvice(),
            kattlekruk.getAdvice(),
            Advice(
                label=f"{{{{ Alchemy Bubbles|#bubbles }}}} - Boaty Bubble: +{boaty_bubble['BaseValue']:.2f}/135%",
                picture_class='boaty-bubble',
                resource=boaty_bubble['Material'],
                progression=boaty_bubble['Level'],
                goal=max_NBLB
            )
        ],
        f'Multi Group B: {multi_group_b}x': [
            Advice(
                label=f"{goharut.get('Name')} Blessing: +{4 * goharut.get('BlessingLevel')}%",
                picture_class=goharut.get('Name'),
                progression=goharut.get('BlessingLevel'),
                goal=100,
                resource=goharut.get('BlessingMaterial')
            )
        ],
        f'Multi Group C: {multi_group_c}x': [
            Advice(
                label=f"{purrmep.get('Name')} Blessing: +{3 * purrmep.get('BlessingLevel')}%",
                picture_class=purrmep.get('Name'),
                progression=purrmep.get('BlessingLevel'),
                goal=100,
                resource=purrmep.get('BlessingMaterial')
            )
        ],
        f'Multi Group D: {multi_group_d}x': [
            Advice(
                label=f"Weekly Ballot: {round(sailing_ballot_buff_mult, 2)}x/{round(ValueToMulti(sailing_ballot_buff['Value']), 2)}x"
                      f"<br>(Buff {'is Active' if is_current_ballot_buff else 'is Inactive'})",
                picture_class=sailing_ballot_buff['Image'],
                progression=int(is_current_ballot_buff),
                goal=1
            )
        ],
        f'Multi Group E: {multi_group_e}x': [
            Advice(
                label=f"{bagur.get('Name')} Blessing: +{5 * bagur.get('BlessingLevel')}%",
                picture_class=bagur.get('Name'),
                progression=bagur.get('BlessingLevel'),
                goal=100,
                resource=bagur.get('BlessingMaterial')
            ),
            Advice(
                label=f'{{{{ Sailing|#sailing }}}}: Level {ad_tablet_level} 10 AD Tablet: +{ad_tablet_bonus_percent}%',
                picture_class='10-ad-tablet',
                progression=session_data.account.sailing['Artifacts']['10 AD Tablet']['Level'],
                goal=max_sailing_artifact_level
            ),
            session_data.account.stamps['Sailboat Stamp'].get_advice(),
            Advice(
                label=f"Level {boat_statue['Level']} Boat Statue: +{(boat_statue['Type'] != 'Normal') * boat_statue['Value']:.2f}% {'(must be at least gold)' if boat_statue['Type'] == 'Normal' else ''}",
                picture_class=boat_statue['Image'],
            ),
            Advice(
                label=f"{{{{ Meal|#cooking }}}} - Popped Corn: {popped_corn['Description']}",
                picture_class=popped_corn['Image'],
                progression=popped_corn['Level'],
                goal=max_meal_level
            ),
            Advice(
                label=f"{{{{ Vial|#vials }}}}: Oj Jooce: +{oj_jooce_vial['Value']:.2f}%",
                picture_class='orange-slice',
                progression=oj_jooce_vial['Level'],
                goal=max_vial_level
            ),
            Advice(
                label=f"{{{{ Rift|#rift }}}} - Sailing Skill Mastery > 200: {'+15%' if has_skill_mastery and total_sailing_level >= 200 else 'Locked.'}",
                picture_class='skill-mastery',
                progression=has_msa_sailing * total_sailing_level,
                goal=200
            ),
            Advice(
                label=f'MSA Sailing: +{has_msa_sailing * total_worship_waves // 10}% (+1% per 10 waves in Worship)',
                picture_class='worship',
                progression=total_worship_waves,
                goal=len(session_data.account.worship['Totems'].keys()) * totems_max_wave,
            ),
            Advice(
                label=f"{{{{ Star Signs|#star-signs }}}} - C. Shanti Minor: {'+20% if equipped' if c_shanti_minor['Unlocked'] else 'Locked.'}",
                picture_class='c-shanti-minor',
                progression=int(c_shanti_minor['Unlocked']),
                goal=1
            )
        ],
        f'Multi Group F: {multi_group_f}x': [
            get_gem_shop_purchase_advice(purchase_name='Davey Jones Training', link_to_section=True),
            get_legend_talent_advice('Davey Jones Returns')
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
    for artifact_name, details in session_data.account.sailing['Artifacts'].items():
        arti_advices[details['Island']].append(get_sailing_artifact_advice(artifact_name, False, False))

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
