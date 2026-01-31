from consts.consts_autoreview import break_you_best, build_subgroup_label, EmojiType
from consts.consts_general import inventory_slots_max_usable
from consts.consts_item_data import ITEM_DATA
from consts.w1.stamps import stamp_types, unavailable_stamps_list, stamps_exalt_recommendations
from consts.consts_w2 import max_vial_level, max_sigil_level
from consts.consts_w3 import max_overall_book_levels
from consts.consts_w5 import max_sailing_artifact_level
from consts.w6.farming import max_farming_crops
from consts.progression_tiers import stamps_progressionTiers, true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.w7 import get_legend_talent_advice
from models.advice.generators.general import get_guild_bonus_advice, get_gem_shop_purchase_advice
from utils.logging import get_logger
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot

logger = get_logger(__name__)


def setMissingStamps():
    return [stampName for stampName, stampValues in session_data.account.stamps.items() if
            not stampValues.delivered and stampName not in unavailable_stamps_list]

def getStampExclusions() -> dict[str, bool]:
    exclusionsDict = {
        # Capacity
        'Matty Bag Stamp': False,  # Materials
        'Foods': False,  # Doesn't exist currently, placeholder
        "Lil' Mining Baggy Stamp": False,  # Mining Ores
        "Choppin' Bag Stamp": False,  # Choppin Logs
        'Bag o Heads Stamp': False,  # Fish
        'Bugsack Stamp': False,  # Catching Bugs
        'Critters': False,  # Doesn't exist currently, placeholder
        'Souls': False,  # Doesn't exist currently, placeholder
        'Mason Jar Stamp': False,  # All types, but less per level
        # Others
        'Triad Essence Stamp': False,  # Sussy Gene quests
        'Summoner Stone Stamp': False,
        'Void Axe Stamp': False,
        'Crop Evo Stamp': False,
    }
    if session_data.account.stamps['Crystallin'].level >= 270:  # Highest Crystallin in Tiers
        exclusionsDict['Matty Bag Stamp'] = True
    if session_data.account.stamps['Multitool Stamp'].level >= 220:  # Highest Multitool in Tiers
        exclusionsDict['Bugsack Stamp'] = True
        exclusionsDict['Bag o Heads Stamp'] = True
    if exclusionsDict['Matty Bag Stamp'] and exclusionsDict['Bugsack Stamp'] and exclusionsDict['Bag o Heads Stamp']:
        exclusionsDict['Mason Jar Stamp'] = True

    # If all summoning matches are finished, exclude the Sussy Gene stamps if not obtained
    if session_data.account.summoning['AllRegularBattlesWon']:
        exclusionsDict['Triad Essence Stamp'] = True if not session_data.account.stamps['Triad Essence Stamp'].delivered else False
        exclusionsDict['Summoner Stone Stamp'] = True if not session_data.account.stamps['Summoner Stone Stamp'].delivered else False
        exclusionsDict['Void Axe Stamp'] = True if not session_data.account.stamps['Void Axe Stamp'].delivered else False

    if session_data.account.farming.crops.unlocked >= max_farming_crops:
        exclusionsDict['Crop Evo Stamp'] = True

    return exclusionsDict

def getCapacityAdviceGroup() -> AdviceGroup:
    capacity_Advices = {
        'Stamps': [],
        'Account Wide': [],
        'Character Specific': []
    }

    starsignBase = 0
    starsignBase += 30 * bool(session_data.account.star_signs['Mr No Sleep']['Unlocked'])
    starsignBase += 10 * bool(session_data.account.star_signs['Pack Mule']['Unlocked'])
    starsignBase += 5 * bool(session_data.account.star_signs['The OG Skiller']['Unlocked'])
    totalStarsignValue = starsignBase * session_data.account.star_sign_extras['SilkrodeNanoMulti'] * session_data.account.star_sign_extras['SeraphMulti']

    # Stamps
    capacity_Advices['Stamps'].append(
        session_data.account.sneaking.emporium['Level Exemption'].get_obtained_advice()
    )
    capacity_Advices['Stamps'].append(Advice(
        label=f"Lab: Certified Stamp Book: "
              f"{max(1, 2 * session_data.account.labBonuses['Certified Stamp Book']['Enabled'])}/2x",
        picture_class="certified-stamp-book",
        progression=int(session_data.account.labBonuses['Certified Stamp Book']['Enabled']),
        goal=1
    ))
    # I'm kinda doubting Lava ever fixes this bug, so hiding it
    # capacity_Advices['Stamps'].append(Advice(
    #     label="Lab Jewel: Pure Opal Navette (lol jk, this is bugged)",
    #     picture_class="pure-opal-navette",
    # ))
    capacity_Advices['Stamps'].append(
        session_data.account.sneaking.pristine_charms[
            'Liqorice Rolle'
        ].get_obtained_advice()
    )
    for cap_stamp in ITEM_DATA.get_capacity_stamps():
        capacity_Advices['Stamps'].append(session_data.account.stamps[cap_stamp.name].get_advice(link_to_section=False))

    # Account-Wide
    capacity_Advices['Account Wide'].append(Advice(
        label=f"{{{{ Bribe|#bribes }}}}: Bottomless Bags: "
              f"{'5' if session_data.account.bribes['W4']['Bottomless Bags'] >= 1 else '0'}/5%",
        picture_class='bottomless-bags',
        progression=1 if session_data.account.bribes['W4']['Bottomless Bags'] >= 1 else 0,
        goal=1
    ))
    capacity_Advices['Account Wide'].append(get_guild_bonus_advice('Rucksack'))
    capacity_Advices['Account Wide'].append(session_data.account.shrine_advices['Pantheon Shrine'])
    capacity_Advices['Account Wide'].append(session_data.account.shrine_advices['Chaotic Chizoar Card'])
    gemshop_carry_capacity = session_data.account.gemshop['Purchases']['Carry Capacity']
    capacity_Advices['Account Wide'].append(get_gem_shop_purchase_advice(
        purchase_name='Carry Capacity',
        link_to_section=True,
        secondary_label=f": +{25 * gemshop_carry_capacity['Owned']}/{25 * gemshop_carry_capacity['MaxLevel']}%"
    ))
    capacity_Advices['Account Wide'].append(session_data.account.star_sign_extras['SeraphAdvice'])

    # Character Specific
    capacity_Advices['Character Specific'].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    capacity_Advices['Character Specific'].append(Advice(
        label=f"Starsign: Mr No Sleep: {30 * session_data.account.star_signs['Mr No Sleep']['Unlocked']}/30% base",
        picture_class='mr-no-sleep',
        progression=int(session_data.account.star_signs['Mr No Sleep']['Unlocked']),
        goal=1
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label=f"Starsign: Pack Mule: {10 * session_data.account.star_signs['Pack Mule']['Unlocked']}/10% base",
        picture_class='pack-mule',
        progression=int(session_data.account.star_signs['Pack Mule']['Unlocked']),
        goal=1
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label=f"Starsign: The OG Skiller: {5 * session_data.account.star_signs['The OG Skiller']['Unlocked']}/5% base",
        picture_class='the-og-skiller',
        progression=int(session_data.account.star_signs['The OG Skiller']['Unlocked']),
        goal=1
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label=f"Total Starsign Value: {totalStarsignValue:.2f}%",
        picture_class='telescope',
    ))
    # This only checks if they are max booked, not if they are actually maxed in either of their presets
    best_jman_bag_book = max([jman.max_talents.get("78", 0) for jman in session_data.account.jmans], default=0)
    capacity_Advices['Character Specific'].append(Advice(
        label="Jman's Extra Bags talent (Materials only)",
        picture_class='extra-bags',
        progression=best_jman_bag_book,
        goal=max_overall_book_levels
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label=f"{inventory_slots_max_usable} available {{{{ Inventory Slots|#storage }}}}",
        picture_class='storage'
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label='Highest Type-Specific Capacity Bag crafted',
        picture_class='herculean-matty-pouch',
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label=f"{{{{ Prayer|#prayers }}}}: Ruck Sack: {session_data.account.prayers['Ruck Sack']['BonusValue']}/177%",
        picture_class='ruck-sack',
        progression=session_data.account.prayers['Ruck Sack']['Level'],
        goal=50
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label=f"{{{{ Prayer|#prayers }}}}: REMOVE ZERG RUSHOGEN ({session_data.account.prayers['Zerg Rushogen']['CurseString']})",
        picture_class='zerg-rushogen',
        progression=EmojiType.NO.value
    ))
    capacity_Advices['Character Specific'].append(Advice(
        label='Star Talent: Telekinetic Storage',
        picture_class="telekinetic-storage",
        progression=5 * session_data.account.merits[2][3]['Level'],
        goal=5 * session_data.account.merits[2][3]['MaxLevel']
    ))

    for group_name in capacity_Advices:
        for advice in capacity_Advices[group_name]:
            advice.mark_advice_completed()

    # Build the AdviceGroup
    capacity_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Sources of Carry Capacity',
        advices=capacity_Advices,
        informational=True
    )
    return capacity_AdviceGroup

def getCostReductionAdviceGroup() -> AdviceGroup:
    costReduction_Advices = {
        'Vials': [],
        'Uncapped': []
    }

    costReduction_Advices['Vials'].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Blue Flav (Platinum Ore): {session_data.account.alchemy_vials['Blue Flav (Platinum Ore)']['Value']:.2f}%",
        picture_class='platinum-ore',
        progression=session_data.account.alchemy_vials['Blue Flav (Platinum Ore)']['Level'],
        goal=max_vial_level
    ))
    costReduction_Advices['Vials'].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Venison Malt (Mongo Worm Slices): {session_data.account.alchemy_vials['Venison Malt (Mongo Worm Slices)']['Value']:.2f}%",
        picture_class='mongo-worm-slices',
        progression=session_data.account.alchemy_vials['Venison Malt (Mongo Worm Slices)']['Level'],
        goal=max_vial_level
    ))

    totalVialReduction = session_data.account.alchemy_vials['Blue Flav (Platinum Ore)']['Value'] + session_data.account.alchemy_vials['Venison Malt (Mongo Worm Slices)']['Value']
    costReduction_Advices['Vials'].append(Advice(
        label='Total Vial reduction (90% hardcap)',
        picture_class='vial-1',
        progression=f"{totalVialReduction:.2f}",
        goal=90,
        unit="%"
    ))

    if (
        session_data.account.alchemy_p2w['Sigils']['Envelope Pile']['PrechargeLevel']
        > session_data.account.alchemy_p2w['Sigils']['Envelope Pile']['Level']
    ):
        envelope_pile_precharged = ' (Precharged)'
    else:
        envelope_pile_precharged = ''
    costReduction_Advices['Uncapped'].append(Advice(
        label=f"Sigil: Envelope Pile{envelope_pile_precharged}",
        picture_class='envelope-pile',
        progression=session_data.account.alchemy_p2w['Sigils']['Envelope Pile']['PrechargeLevel'],
        goal=max_sigil_level
    ))
    costReduction_Advices['Uncapped'].append(
        session_data.account.sneaking.emporium['Ionized Sigils'].get_obtained_advice()
    )
    costReduction_Advices['Uncapped'].append(Advice(
        label=f"{{{{ Artifact|#sailing }}}}: Chilled Yarn increases sigil by {1 + session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']}x",
        picture_class='chilled-yarn',
        progression=session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'],
        goal=max_sailing_artifact_level
    ))

    for group_name in costReduction_Advices:
        for advice in costReduction_Advices[group_name]:
            advice.mark_advice_completed()

    # Build the AdviceGroup
    costReduction_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Sources of Stamp Cost Reduction',
        advices=costReduction_Advices,
        informational=True
    )
    return costReduction_AdviceGroup

def getExaltedAdviceGroup() -> AdviceGroup:
    rec = 'Remaining Recommended Exalts'
    cur = 'Current Exalts'
    tot = 'Available Exalts'
    boni = 'Sources of Exalt Bonus'
    exalted_advice = {
        boni: [],
        tot: [],
        rec: [],
        cur: []
    }

    stamps = session_data.account.stamps
    compass = session_data.account.compass
    gemshop = session_data.account.gemshop['Purchases']
    atom_collider = session_data.account.atom_collider

    exalted_advice[boni].append(Advice(
        label=f"Total Exalted Bonus: {session_data.account.exalted_stamp_multi:.2f}x",
        picture_class='exalted-stamps'
    ))
    exalted_advice[boni].append(Advice(
        label='Base Value: +100%',
        picture_class='exalted-stamps'
    ))
    exalted_advice[boni].append(Advice(
        label=(
            f"{{{{Atom Collider|#atom-collider}}}}: Aluminium: "
            f"+{atom_collider['Atoms']['Aluminium - Stamp Supercharger']['Level'] * atom_collider['Atoms']['Aluminium - Stamp Supercharger']['Value per Level']}"
            f"/{atom_collider['Atoms']['Aluminium - Stamp Supercharger']['MaxLevel'] * atom_collider['Atoms']['Aluminium - Stamp Supercharger']['Value per Level']}%"
        ),
        picture_class='aluminium',
        progression=session_data.account.atom_collider['Atoms']['Aluminium - Stamp Supercharger']['Level'],
        goal=session_data.account.atom_collider['Atoms']['Aluminium - Stamp Supercharger']['MaxLevel'],
        resource='particles'
    ))
    exalted_advice[boni].append(
        session_data.account.sneaking.pristine_charms['Jellypick'].get_obtained_advice()
    )
    emp_set = session_data.account.armor_sets['Sets']['EMPEROR SET']
    exalted_advice[boni].append(Advice(
        label=f"{{{{Armor Set|#armor-sets}}}}: Emperor Set: {emp_set['Description']}",
        picture_class=emp_set['Image'],
        progression=int(emp_set['Owned']),
        goal=1
    ))

    compass_abs = compass['Upgrades']['Abomination Slayer XVII']
    exalted_advice[boni].append(Advice(
        label=f"{{{{Compass|#the-compass}}}}: {compass_abs['Path Name']}-{compass_abs['Path Ordering']}: "
              f"<br>Abomination Slayer XVII: +{compass_abs['Total Value']}/{compass_abs['Max Level']}%",
        picture_class=compass_abs['Image'] if compass_abs['Unlocked'] else 'placeholder',
        progression=compass_abs['Level'],
        goal=compass_abs['Max Level'],
        resource=compass_abs['Dust Image']
    ))

    extra_exaltedness = session_data.account.event_points_shop['Bonuses']['Extra Exaltedness']
    extra_exaltedness_value = 20
    exalted_advice[boni].append(Advice(
        label=f"{{{{Event Shop|#event-shop}}}}: Extra Exaltedness: +{extra_exaltedness_value * extra_exaltedness['Owned']}/{extra_exaltedness_value}%",
        picture_class='event-shop-18'
    ))

    exalted_advice[boni].append(get_legend_talent_advice('Wowa Woowa'))

    tot_available = compass['Upgrades']['Exalted Stamps']['Level'] + gemshop['Exalted Stamps']['Owned'] + int(extra_exaltedness['Owned'])

    exalted_advice[tot].append(Advice(
        label=f"Total Exalted Stamps spent: {compass['Total Exalted']}/{tot_available}",
        picture_class='exalted-stamps',
        progression=compass['Total Exalted'],
        goal=tot_available
    ))
    exalted_advice[tot].append(Advice(
        label=f"Exalted Stamps from Wind Walker {{{{Compass|#the-compass}}}}: {compass['Upgrades']['Exalted Stamps']['Level']}",
        picture_class=compass['Upgrades']['Exalted Stamps']['Image'],
        progression=compass['Upgrades']['Exalted Stamps']['Level'],
        goal=compass['Upgrades']['Exalted Stamps']['Max Level']
    ))
    gemshop_exalted_stamps = gemshop['Exalted Stamps']
    exalted_advice[tot].append(Advice(
        label=f"Exalted Stamps from Gem Shop ({gemshop_exalted_stamps['Subsection']}): {gemshop_exalted_stamps['Owned']}",
        picture_class='exalted-stamps',
        progression=gemshop_exalted_stamps['Owned'],
        goal=gemshop_exalted_stamps['MaxLevel']
    ))

    exalted_advice[rec] = [
        Advice(
            label=f"{stamps[stamp_name].stamp_type}: {stamp_name}",
            picture_class=stamp_name,
            progression=0,
            goal=1
        ) for stamp_name in stamps_exalt_recommendations if not stamps[stamp_name].exalted and stamps[stamp_name].delivered
    ]

    exalted_advice[cur] = [
        Advice(
            label=f"{stamp_details.stamp_type}: {stamp_name}",
            picture_class=stamp_name,
            progression=1,
            goal=1
        ) for stamp_name, stamp_details in stamps.items() if stamp_details.exalted
    ]

    for subgroup in exalted_advice:
        for advice in exalted_advice[subgroup]:
            advice.mark_advice_completed()

    exalted_ag = AdviceGroup(
        tier='',
        pre_string='Exalted Stamps',
        advices=exalted_advice,
        informational=True
    )
    exalted_ag.remove_empty_subgroups()
    return exalted_ag

def getProgressionTiersAdviceGroup():
    stamp_Advices = {
        'Stamp Levels': {},
        'Find Required': {},
        'Not Recommended': {},
        'Specific': {},
    }
    optional_tiers = 3
    true_max = true_max_tiers['Stamps']
    max_tier = true_max - optional_tiers
    tier_StampLevels = 0
    tier_FindRequiredStamps = 0
    tier_SpecificStamps = 0
    player_stamps = session_data.account.stamps
    missing_stamps_list = setMissingStamps()
    exclusions_dict = getStampExclusions()

    added_stamps = {}

    #Assess Tiers
    for tier_number, requirements in stamps_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        # TotalLevelStamps
        if session_data.account.stamp_totals.get('Total', 0) < requirements.get('Total Stamp Levels', 0):
            add_subgroup_if_available_slot(stamp_Advices['Stamp Levels'], subgroup_label)
            if subgroup_label in stamp_Advices['Stamp Levels']:
                stamp_Advices['Stamp Levels'][subgroup_label].append(Advice(
                    label='Total Stamp Levels',
                    picture_class='stat-graph-stamp',
                    progression=session_data.account.stamp_totals.get('Total', 0),
                    goal=requirements.get('Total Stamp Levels', 0)
                ))
        if subgroup_label not in stamp_Advices['Stamp Levels'] and tier_StampLevels >= tier_number - 1:
            tier_StampLevels = tier_number

        # Collect important Combat, Skill, and Misc stamps
        for stamp_type in stamp_types:
            for required_stamp in requirements.get('Stamps').get(stamp_type, []):
                if required_stamp in missing_stamps_list and exclusions_dict.get(required_stamp, False) == False:
                    add_subgroup_if_available_slot(stamp_Advices['Find Required'], subgroup_label)
                    if subgroup_label in stamp_Advices['Find Required']:
                        stamp_Advices['Find Required'][subgroup_label].append(Advice(
                            label=f"{stamp_type}: {required_stamp}, leveled with {player_stamps[required_stamp].material.name}",
                            picture_class=required_stamp,
                            progression=0,
                            goal=1,
                            resource=player_stamps[required_stamp].material.name,
                        ))
        if subgroup_label not in stamp_Advices['Find Required'] and tier_FindRequiredStamps >= tier_number - 1:
            tier_FindRequiredStamps = tier_number

        # SpecificStampLevels
        for stamp_name, required_level in requirements.get('Stamps', {}).get('Specific', {}).items():
            if added_stamps.get(stamp_name, 0) >= required_level:
                continue  #Don't add the same stamp/level combo into multiple tiers
            if player_stamps[stamp_name].level < required_level:
                if (
                    (tier_number <= max_tier and exclusions_dict.get(stamp_name, False) == False)
                    or (tier_number > max_tier and player_stamps[stamp_name].delivered)
                ):
                    add_subgroup_if_available_slot(stamp_Advices['Specific'], subgroup_label)
                    if subgroup_label in stamp_Advices['Specific']:
                        added_stamps[stamp_name] = required_level
                        stamp_Advices['Specific'][subgroup_label].append(Advice(
                            label=f"{player_stamps[stamp_name].stamp_type}: {stamp_name}",
                            picture_class=stamp_name,
                            progression=player_stamps[stamp_name].level,
                            goal=required_level,
                            resource=player_stamps[stamp_name].material.name,
                        ))

        if subgroup_label not in stamp_Advices['Specific'] and tier_SpecificStamps == tier_number - 1:
            tier_SpecificStamps = tier_number

        # Not Recommended
        for required_stamp in requirements.get('Stamps').get('Not Recommended', []):
            if required_stamp in missing_stamps_list and exclusions_dict.get(required_stamp, False) == False:
                subgroup_label = f"Previously Tier {tier_number}"
                if subgroup_label not in stamp_Advices['Not Recommended']:  # and len(stamp_Advices['Not Recommended']) < maxTiersPerGroup:
                    stamp_Advices['Not Recommended'][subgroup_label] = []
                if subgroup_label in stamp_Advices['Not Recommended']:
                    stamp_Advices['Not Recommended'][subgroup_label].append(Advice(
                        label=f"{player_stamps[required_stamp].stamp_type}: {required_stamp}",
                        picture_class=required_stamp,
                        resource=player_stamps[required_stamp].material.name,
                        informational=True,
                        completed=True
                    ))

    # Generate AdviceGroups
    stamp_AdviceGroupDict = {
        'Stamp Levels': AdviceGroup(
            tier=tier_StampLevels,
            pre_string='Improve your total stamp levels',
            advices=stamp_Advices['Stamp Levels'],
        ),
        'SpecificStamps': AdviceGroup(
            tier=tier_SpecificStamps,
            pre_string=f"Improve high-priority Stamps",
            advices=stamp_Advices['Specific'],
        ),
        'FindRequired': AdviceGroup(
            tier=tier_FindRequiredStamps,
            pre_string=f"Collect the following Stamps",
            advices=stamp_Advices['Find Required']
        ),
        'Not Recommended': AdviceGroup(
            tier='',
            pre_string="These stamps are not recommended to be turned in if you've purchased the Sacred Methods bundle",
            advices=stamp_Advices['Not Recommended'],
            informational=True
        )
    }
    overall_SectionTier = min(true_max, tier_StampLevels, tier_FindRequiredStamps, tier_SpecificStamps)
    return stamp_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getStampAdviceSection() -> AdviceSection:
    # Generate AdviceGroups
    stamp_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    stamp_AdviceGroupDict['Capacity'] = getCapacityAdviceGroup()
    stamp_AdviceGroupDict['CostReduction'] = getCostReductionAdviceGroup()
    stamp_AdviceGroupDict['Exalted'] = getExaltedAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    stamp_AdviceSection = AdviceSection(
        name='Stamps',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Stamp tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Stamps_Header.png',
        groups=stamp_AdviceGroupDict.values()
    )
    return stamp_AdviceSection
