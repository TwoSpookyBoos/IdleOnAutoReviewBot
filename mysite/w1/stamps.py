from consts.consts_w5 import max_sailing_artifact_level
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from consts.consts_autoreview import break_you_best, build_subgroup_label, EmojiType
from consts.consts_general import current_max_usable_inventory_slots
from consts.consts_w6 import max_farming_crops
from consts.consts_w3 import max_overall_book_levels
from consts.consts_w2 import max_vial_level, max_sigil_level
from consts.consts_w1 import stamp_types, unavailable_stamps_list, stamp_maxes, stamps_dict, stamps_exalt_recommendations, capacity_stamps
from consts.progression_tiers import stamps_progressionTiers, true_max_tiers
from flask import g as session_data

logger = get_logger(__name__)


def setMissingStamps():
    return [stampName for stampName, stampValues in session_data.account.stamps.items() if
            not stampValues['Delivered'] and stampName not in unavailable_stamps_list]

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
    if session_data.account.stamps['Crystallin']['Level'] >= 270:  # Highest Crystallin in Tiers
        exclusionsDict['Matty Bag Stamp'] = True
    if session_data.account.stamps['Multitool Stamp']['Level'] >= 220:  # Highest Multitool in Tiers
        exclusionsDict['Bugsack Stamp'] = True
        exclusionsDict['Bag o Heads Stamp'] = True
    if exclusionsDict['Matty Bag Stamp'] and exclusionsDict['Bugsack Stamp'] and exclusionsDict['Bag o Heads Stamp']:
        exclusionsDict['Mason Jar Stamp'] = True

    # If all summoning matches are finished, exclude the Sussy Gene stamps if not obtained
    if session_data.account.summoning['AllBattlesWon']:
        exclusionsDict['Triad Essence Stamp'] = True if not session_data.account.stamps['Triad Essence Stamp']['Delivered'] else False
        exclusionsDict['Summoner Stone Stamp'] = True if not session_data.account.stamps['Summoner Stone Stamp']['Delivered'] else False
        exclusionsDict['Void Axe Stamp'] = True if not session_data.account.stamps['Void Axe Stamp']['Delivered'] else False

    if session_data.account.farming['CropsUnlocked'] >= max_farming_crops:
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
    capacity_Advices['Stamps'].append(Advice(
        label="{{ Jade Emporium|#sneaking }}: Level Exemption",
        picture_class="level-exemption",
        progression=1 if session_data.account.sneaking['JadeEmporium']['Level Exemption']['Obtained'] else 0,
        goal=1
    ))
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
    capacity_Advices['Stamps'].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Liqorice Rolle: "
              f"{'1.25' if session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained'] else '1'}/1.25x",
        picture_class=session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']),
        goal=1
    ))
    for cap_stamp in capacity_stamps:
        capacity_Advices['Stamps'].append(Advice(
            label=f"{cap_stamp}: {round(session_data.account.stamps[cap_stamp]['Total Value'], 2):g}%",
            picture_class=cap_stamp,
            progression=session_data.account.stamps[cap_stamp]['Level'],
            goal=stamp_maxes[cap_stamp],
            resource=session_data.account.stamps[cap_stamp]['Material'],
        ))

    # Account-Wide
    capacity_Advices['Account Wide'].append(Advice(
        label=f"{{{{ Bribe|#bribes }}}}: Bottomless Bags: "
              f"{'5' if session_data.account.bribes['W4']['Bottomless Bags'] >= 1 else '0'}/5%",
        picture_class='bottomless-bags',
        progression=1 if session_data.account.bribes['W4']['Bottomless Bags'] >= 1 else 0,
        goal=1
    ))
    capacity_Advices['Account Wide'].append(Advice(
        label='Guild Bonus: Rucksack',
        picture_class='rucksack',
        progression=f"{session_data.account.guild_bonuses['Rucksack']['Level'] if session_data.account.guild_bonuses['Rucksack']['Level'] > 0 else 'IDK'}",
        goal=50
    ))
    capacity_Advices['Account Wide'].append(session_data.account.shrine_advices['Pantheon Shrine'])
    capacity_Advices['Account Wide'].append(session_data.account.shrine_advices['Chaotic Chizoar Card'])
    capacity_Advices['Account Wide'].append(Advice(
        label=f"{{{{ Gem Shop|#gem-shop }}}}: Carry Capacity: "
              f"{(25 * session_data.account.gemshop.get('Carry Capacity', 0))}%/250%",
        picture_class="carry-capacity",
        progression=session_data.account.gemshop.get('Carry Capacity', 0),
        goal=10
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
        label=f"{current_max_usable_inventory_slots} available {{{{ Inventory Slots|#storage }}}}",
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
            mark_advice_completed(advice)

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
    costReduction_Advices['Uncapped'].append(Advice(
        label="{{ Jade Emporium|#sneaking }}: Ionized Sigils",
        picture_class='ionized-sigils',
        progression=int(session_data.account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']),
        goal=1
    ))
    costReduction_Advices['Uncapped'].append(Advice(
        label=f"{{{{ Artifact|#sailing }}}}: Chilled Yarn increases sigil by {1 + session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']}x",
        picture_class='chilled-yarn',
        progression=session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'],
        goal=max_sailing_artifact_level
    ))

    for group_name in costReduction_Advices:
        for advice in costReduction_Advices[group_name]:
            mark_advice_completed(advice)

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
    gemshop = session_data.account.gemshop
    atom_collider = session_data.account.atom_collider
    pc = session_data.account.sneaking['PristineCharms']

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
    exalted_advice[boni].append(Advice(
        label=f"{{{{Pristine Charm|#sneaking}}}}: Jellypick: +{20 * pc['Jellypick']['Obtained']}/20%",
        picture_class='jellypick',
        progression=int(pc['Jellypick']['Obtained']),
        goal=1
    ))
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

    tot_available = compass['Upgrades']['Exalted Stamps']['Level'] + gemshop['Exalted Stamps']

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
    exalted_advice[tot].append(Advice(
        label=f"Exalted Stamps from Gem Shop (Limited Availability): {gemshop['Exalted Stamps']}",
        picture_class='exalted-stamps',
        progression=gemshop['Exalted Stamps'],
        goal=EmojiType.INFINITY.value
    ))

    exalted_advice[rec] = [
        Advice(
            label=f"{stamps[stamp_name]['StampType']}: {stamp_name}",
            picture_class=stamp_name,
            progression=0,
            goal=1
        ) for stamp_name in stamps_exalt_recommendations if not stamps[stamp_name]['Exalted'] and stamps[stamp_name]['Delivered']
    ]

    exalted_advice[cur] = [
        Advice(
            label=f"{stamp_details['StampType']}: {stamp_name}",
            picture_class=stamp_name,
            progression=1,
            goal=1
        ) for stamp_name, stamp_details in stamps.items() if stamp_details['Exalted']
    ]

    for subgroup in exalted_advice:
        for advice in exalted_advice[subgroup]:
            mark_advice_completed(advice)

    exalted_ag = AdviceGroup(
        tier='',
        pre_string='Exalted Stamps',
        advices=exalted_advice,
        informational=True
    )
    exalted_ag.remove_empty_subgroups()
    return exalted_ag

def getReadableStampName(stampNumber, stampType):
    # logger.debug(f"Fetching name for {stampType} + {stampNumber}")
    return stamps_dict.get(stampType, {}).get(stampNumber, f"Unknown{stampType}{stampNumber}")

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
            if (
                subgroup_label not in stamp_Advices['Stamp Levels']
                and len(stamp_Advices['Stamp Levels']) < session_data.account.max_subgroups
            ):
                stamp_Advices['Stamp Levels'][subgroup_label] = []
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
                    if (
                        subgroup_label not in stamp_Advices['Find Required']
                        and len(stamp_Advices['Find Required']) < session_data.account.max_subgroups
                    ):
                        stamp_Advices['Find Required'][subgroup_label] = []
                    if subgroup_label in stamp_Advices['Find Required']:
                        stamp_Advices['Find Required'][subgroup_label].append(Advice(
                            label=f"{stamp_type}: {required_stamp}, leveled with {player_stamps[required_stamp]['Material'].replace('-', ' ').title()}",
                            picture_class=required_stamp,
                            progression=0,
                            goal=1,
                            resource=player_stamps[required_stamp]['Material'],
                        ))
        if subgroup_label not in stamp_Advices['Find Required'] and tier_FindRequiredStamps >= tier_number - 1:
            tier_FindRequiredStamps = tier_number

        # SpecificStampLevels
        for stamp_name, required_level in requirements.get('Stamps', {}).get('Specific', {}).items():
            # if added_stamps.get(stamp_name, 0) >= required_level:
            #     continue  #Don't add the same stamp/level combo into multiple tiers
            if player_stamps[stamp_name]['Level'] < required_level:
                if (
                    (tier_number <= max_tier and exclusions_dict.get(stamp_name, False) == False)
                    or (tier_number > max_tier and player_stamps[stamp_name]['Delivered'])
                ):
                    if (
                        subgroup_label not in stamp_Advices['Specific']
                        and len(stamp_Advices['Specific']) < session_data.account.max_subgroups
                    ):
                        stamp_Advices['Specific'][subgroup_label] = []
                    if subgroup_label in stamp_Advices['Specific']:
                        added_stamps[stamp_name] = required_level
                        stamp_Advices['Specific'][subgroup_label].append(Advice(
                            label=f"{player_stamps[stamp_name]['StampType']}: {stamp_name}",
                            picture_class=stamp_name,
                            progression=player_stamps[stamp_name]['Level'],
                            goal=required_level,
                            resource=player_stamps[stamp_name]['Material'],
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
                        label=f"{player_stamps[required_stamp]['StampType']}: {required_stamp}",
                        picture_class=required_stamp,
                        resource=player_stamps[required_stamp]['Material'],
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
