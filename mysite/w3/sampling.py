import math
from flask import g as session_data

from models.models import AdviceSection, AdviceGroup, Advice
from models.models_util import get_companion_advice
from utils.safer_data_handling import safer_get
from utils.misc.has_companion import has_companion
from utils.text_formatting import notateNumber
from utils.logging import get_logger
from consts.consts_autoreview import ValueToMulti, break_you_best, build_subgroup_label, EmojiType, AdviceType
from consts.consts_idleon import skill_index_list, lavaFunc
from consts.consts_w5 import goldrelic_multis_dict
from consts.consts_w3 import max_printer_sample_rate
from consts.consts_w2 import max_vial_level, arcade_max_level
from consts.progression_tiers import sampling_progressionTiers, true_max_tiers

logger = get_logger(__name__)

def getSampleClass(materialName: str) -> str:
    if materialName == 'Oak Logs':
        return 'mage-icon'
    elif materialName == 'Copper Ore':
        return 'warrior-icon'
    elif materialName == 'Goldfish':
        return 'barbarian-icon'
    elif materialName == 'Fly':
        return 'bowman-icon'
    elif materialName == 'Spore Cap':
        return 'voidwalker-icon'
    else:
        return ''

def getPrinterSampleRateAdviceGroup() -> AdviceGroup:
    psr_Advices = {}

    #Account-Wide
    account_sum = 0.0
    vialBonus = session_data.account.alchemy_vials['Snow Slurry (Snow Ball)']['Value']
    account_sum += vialBonus
    account_sum += session_data.account.alchemy_bubbles['Sample It']['BaseValue']
    account_sum += 0.5 * session_data.account.saltlick.get('Printer Sample Size', 0)
    account_sum += 0.5 * session_data.account.merits[2][4]['Level']
    account_sum += session_data.account.family_bonuses['Maestro']['Value']
    stample_value = session_data.account.stamps['Stample Stamp'].total_value
    amplestample_value = session_data.account.stamps['Amplestample Stamp'].total_value
    account_sum += stample_value
    account_sum += amplestample_value
    account_sum += float(session_data.account.arcade.get(5, {}).get('Value', 0))
    account_sum += session_data.account.achievements['Saharan Skull']['Complete']
    #achievementStatus = session_data.account.achievements['Saharan Skull']['Complete']
    star_talent_one_point = lavaFunc('bigBase', 1, 10, 0.075)
    account_sum += star_talent_one_point

    account_subgroup = f'Account-Wide: +{account_sum:.2f}%'
    psr_Advices[account_subgroup] = []
    
    psr_Advices[account_subgroup].append(Advice(
        label=f"Snow Slurry {{{{ Vial|#vials }}}}: +{vialBonus:.2f}/30%",
        picture_class=session_data.account.alchemy_vials['Snow Slurry (Snow Ball)']['Image'],
        progression=session_data.account.alchemy_vials['Snow Slurry (Snow Ball)']['Level'],
        goal=max_vial_level
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"Sample It bubble: "
              f"+{session_data.account.alchemy_bubbles['Sample It']['BaseValue']:.2f}/10%",
        picture_class='sample-it',
        progression=session_data.account.alchemy_bubbles['Sample It']['Level'],
        goal=200,
        resource=session_data.account.alchemy_bubbles['Sample It']['Material']
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"{{{{ Salt Lick|#salt-lick }}}} bonus: "
              f"+{round(0.5 * session_data.account.saltlick['Printer Sample Size'], 2):g}/10%",
        picture_class='salt-lick',
        progression=session_data.account.saltlick['Printer Sample Size'],
        goal=20
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"W3 merit: "
              f"+{round(0.5 * session_data.account.merits[2][4]['Level'], 1):g}/{0.5 * session_data.account.merits[2][4]['MaxLevel']:.0f}%",
        picture_class='merit-2-4',
        progression=session_data.account.merits[2][4]['Level'],
        goal=session_data.account.merits[2][4]['MaxLevel']
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"Maestro Family Bonus:"
              f" {session_data.account.family_bonuses['Maestro']['Value']:.2f}/4.5% at"
              f" Class Level {session_data.account.family_bonuses['Maestro']['Level']}",
        picture_class='maestro-icon',
        progression=session_data.account.family_bonuses['Maestro']['Level'],
        goal=328
    ))
    psr_Advices[account_subgroup].append(session_data.account.stamps['Amplestample Stamp'].get_advice())
    psr_Advices[account_subgroup].append(session_data.account.stamps['Stample Stamp'].get_advice())
    psr_Advices[account_subgroup].append(Advice(
        label=f"Lab Bonus: Certified Stamp Book: "
              f"{'2/2x<br>(Already applied to Stamps above)' if session_data.account.labBonuses['Certified Stamp Book']['Enabled'] else '1/2x'}",
        picture_class='certified-stamp-book',
        progression=int(session_data.account.labBonuses['Certified Stamp Book']['Enabled']),
        goal=1
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Liqorice Rolle: "
              f"{'1.25/1.25x<br>(Already applied to Stamps above)' if session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained'] else '1/1.25x'}",
        picture_class=session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']),
        goal=1
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"{{{{Arcade|#arcade}}}} Bonus: "
              f"{session_data.account.arcade[5]['Value']:.2f}/"
              f"{session_data.account.arcade[5]['MaxValue']:.0f}%",
        picture_class=session_data.account.arcade[5]['Image'],
        progression=session_data.account.arcade[5]['Level'],
        goal=arcade_max_level + 1,
        resource=session_data.account.arcade[5]['Material']
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"W3 Achievement: Saharan Skull: {int(session_data.account.achievements['Saharan Skull']['Complete'])}/1%",
        picture_class='saharan-skull',
        progression=int(session_data.account.achievements['Saharan Skull']['Complete']),
        goal=1
    ))
    psr_Advices[account_subgroup].append(Advice(
        label=f"Star Talent: Printer Sampling: {star_talent_one_point:.3f}% at minimum level 1",
        picture_class='printer-sampling',
        progression=1,
        goal=1
    ))

    #Character-Specific
    character_sum = 0.0
    star_talent_diff_to_max = lavaFunc('bigBase', 100, 10, 0.075) - star_talent_one_point
    character_sum += star_talent_diff_to_max
    po_box_max = lavaFunc('decay', 400, 5, 200)
    character_sum += po_box_max
    squire_super_samples_max_book = lavaFunc('decay', session_data.account.library['MaxBookLevel'], 9, 75)
    character_subgroup = f"Character-Specific: Up to +{character_sum:.3f}% or +{character_sum + squire_super_samples_max_book:.2f}% for Squires"
    psr_Advices[character_subgroup] = []
    psr_Advices[character_subgroup].append(Advice(
        label=f"Star Talent: Printer Sampling: Additional {star_talent_diff_to_max:.2f}% at max level 100",
        picture_class='printer-sampling',
        progression=1,
        goal=1
    ))
    psr_Advices[character_subgroup].append(Advice(
        label=f"Post Office: Utilitarian Capsule: +3.33% at max 400 crates",
        picture_class='utilitarian-capsule'
    ))
    psr_Advices[character_subgroup].append(Advice(
        label=f"Squire only: Super Samples: +{squire_super_samples_max_book:.2f}% at max book level {session_data.account.library['MaxBookLevel']}",
        picture_class='super-samples'
    ))

    prayerSubgroup = 'Which Characters need Royal Sampler?'
    psr_Advices[prayerSubgroup] = []
    psr_Advices[prayerSubgroup].append(Advice(
        label=f"{{{{ Prayer|#prayers }}}}: Royal Sampler: {session_data.account.prayers['The Royal Sampler']['BonusString']}",
        picture_class='the-royal-sampler',
        progression=session_data.account.prayers['The Royal Sampler']['Level'],
        goal=20
    ))
    psr_Advices[prayerSubgroup].append(Advice(
        label=f"Character's Printer Sample Rate below is calculated WITHOUT the prayer's bonus.",
        picture_class='',
    ))
    complete_toons = 0  #Either above 90 and the prayer not worn, or below 90 and already wearing the prayer. Those are the 2 "no action needed" states
    for char in session_data.account.all_characters:
        character_total_psr = account_sum + star_talent_diff_to_max + char.po_boxes_invested['Utilitarian Capsule']['Bonus1Value']
        if char.sub_class == 'Squire':
            character_total_psr += squire_super_samples_max_book
        if max_printer_sample_rate > character_total_psr:
            short_by = max_printer_sample_rate - character_total_psr
            prayer_gain = min(short_by, session_data.account.prayers['The Royal Sampler']['BonusValue'])
            character_eval = (
                f"Keep prayer equipped for +{prayer_gain:.2f}% {EmojiType.THUMBSUP.value}"
                if 'The Royal Sampler' in char.equipped_prayers
                else f"{EmojiType.WARNING.value}Equip the Prayer for +{prayer_gain:.2f}%"
            ) + (f"<br>{char.po_boxes_invested['Utilitarian Capsule']['Level']}/"
                 f"{char.po_boxes_invested['Utilitarian Capsule']['Max Level']} PO Boxes invested")
            complete_toons += 1 if 'The Royal Sampler' in char.equipped_prayers else 0
        else:
            character_eval = (
                f"Prayer not needed{'. You may remove if desired.' if 'The Royal Sampler' in char.equipped_prayers else ', not worn.'}"
                f" {EmojiType.THUMBSUP.value}"
            )
            complete_toons += 1

        psr_Advices[prayerSubgroup].append(Advice(
            label=f"{char.character_name}: {character_eval}",
            picture_class=f"{char.class_name_icon}",
            progression=f"{character_total_psr:.1f}",
            goal=max_printer_sample_rate,
            unit="%"
        ))

    for group_name in psr_Advices:
        if group_name != prayerSubgroup:
            for advice in psr_Advices[group_name]:
                advice.mark_advice_completed()

    psrAdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Sources of Printer Sample Rate ({max_printer_sample_rate}% Hardcap)",
        post_string=(
            f"All possible values would total well over the 90% hardcap. Targets on infinite sources are where I'd recommend stopping."
            if complete_toons < session_data.account.character_count
            else ''
        ),
        advices=psr_Advices,
        informational=True,
        completed=complete_toons >= session_data.account.character_count
    )
    return psrAdviceGroup

def getPrinterOutputAdviceGroup() -> AdviceGroup:
    # Calculate Multis for Labels
    # Skill Mastery
    sm_base = 4 * session_data.account.rift['SkillMastery']  # This isn't expressed anywhere in game, but is hard-coded in source code.
    sm_eligible_skills = len(skill_index_list) - 1  #-1 to exclude Combat
    sm_bonus = sum([1 for skillName, skillLevels in session_data.account.all_skills.items() if skillName != "Combat" and sum(skillLevels) >= 750])
    sm_sum = sm_base + sm_bonus
    sm_multi = ValueToMulti(sm_sum)

    gr_level = session_data.account.sailing['Artifacts']['Gold Relic']['Level']
    gr_days = safer_get(session_data.account.raw_optlacc_dict, 125, 0)
    gr_max_days = (
        160 if gr_level == 4
        else 80 if gr_level == 3
        else 60 if gr_level == 2
        else 40
    )
    gr_multi = ValueToMulti(gr_days * goldrelic_multis_dict.get(gr_level, 0))

    supreme_wiring_max_days = 50
    supreme_wiring_days = min(supreme_wiring_max_days, safer_get(session_data.account.raw_optlacc_dict, 323, 0))
    supreme_wiring_value = (supreme_wiring_days * 2 * session_data.account.event_points_shop['Bonuses']['Supreme Wiring']['Owned'])
    supreme_wiring_multi = ValueToMulti(supreme_wiring_value)

    biggole_mole_max_days = 100
    biggole_mole_days = min(biggole_mole_max_days, safer_get(session_data.account.raw_optlacc_dict, 354, 0))
    biggole_mole_value = biggole_mole_days * 1 * has_companion('Biggole Mole')
    biggole_mole_multi = ValueToMulti(biggole_mole_value)

    mop = session_data.account.compass['Upgrades']['Moon of Print']
    compass_moon_of_print_max_days = 100
    compass_moon_of_print_days = min(compass_moon_of_print_max_days, safer_get(session_data.account.raw_optlacc_dict, 364, 0))
    compass_moon_of_print_value = (
        compass_moon_of_print_max_days
        * mop['Unlocked']
        * mop['Total Value']
    )
    compass_moon_of_print_multi = ValueToMulti(compass_moon_of_print_value)

    any_dk_max_booked = False
    best_kotr_book = 0
    any_dk_max_leveled = False
    best_kotr_preset_level = 0
    for dk in session_data.account.dks:
        levels_above_max = dk.max_talents_over_books - session_data.account.library['MaxBookLevel']
        # Book level
        if dk.max_talents.get("178", 0) >= session_data.account.library['MaxBookLevel']:
            any_dk_max_booked = True
        if dk.max_talents.get("178", 0) > best_kotr_book:
            best_kotr_book = dk.max_talents.get("178", 0)

        # Preset level
        if (
            dk.current_preset_talents.get("178", 0) >= session_data.account.library['MaxBookLevel']
            or dk.secondary_preset_talents.get("178", 0) >= session_data.account.library['MaxBookLevel']
        ):
            any_dk_max_leveled = True
        if dk.current_preset_talents.get("178", 0) >= best_kotr_preset_level:
            best_kotr_preset_level = dk.current_preset_talents.get("178", 0) + levels_above_max
        if dk.secondary_preset_talents.get("178", 0) >= best_kotr_preset_level:
            best_kotr_preset_level = dk.secondary_preset_talents.get("178", 0) + levels_above_max

    talent_value = lavaFunc('decay', best_kotr_preset_level, 5, 150)
    orb_kills = session_data.account.class_kill_talents['King of the Remembered']['Kills']
    pow10_kills = math.log(orb_kills,10) if orb_kills > 0 else 0
    kotr_multi = max(1, ValueToMulti(talent_value * pow10_kills))

    charm_multi = 1.25
    charm_multi_active = charm_multi if session_data.account.sneaking['PristineCharms']['Lolly Flower']['Obtained'] else 1

    ballot_active = session_data.account.ballot['CurrentBuff'] == 11
    if ballot_active:
        ballot_status = "is Active"
    elif not ballot_active and session_data.account.ballot['CurrentBuff'] != 0:
        ballot_status = "is Inactive"
    else:
        ballot_status = "status is not available in provided data"
    ballot_multi = ValueToMulti(session_data.account.ballot['Buffs'][11]['Value'])
    ballot_multi_active = max(1, ballot_multi * ballot_active)

    lab_multi_aw = 2 if has_companion('King Doot') else 1
    lab_multi_cs = 2 if session_data.account.labBonuses['Wired In']['Enabled'] else 1

    harriep_multi_aw = 3 if has_companion('King Doot') else 1
    harriep_multi_cs = 3 if session_data.account.divinity['Divinities'][4]['Unlocked'] else 1

    aw_multi = (
        1 * sm_multi * gr_multi * kotr_multi * charm_multi_active * ballot_multi_active
        * lab_multi_aw * harriep_multi_aw * supreme_wiring_multi * biggole_mole_multi * compass_moon_of_print_multi
    )
    aw_label = f"Account Wide: {aw_multi:.3f}x"
    cs_multi = lab_multi_cs * harriep_multi_cs
    cs_label = f"Character Specific: Up to {cs_multi}x"

    po_Advices = {
        cs_label: [],
        aw_label: [],
    }

    # If Doot is not owned, these are Character Specific. Otherwise, they are account-wide
    po_Advices[f"{cs_label if not has_companion('King Doot') else aw_label}"].append(Advice(
        label=f"Lab Bonus: Wired In: {'2x (Thanks Doot!)' if has_companion('King Doot') else '2x if connected to Lab/Arctis'}",
        picture_class='wired-in',
        progression=lab_multi_aw if has_companion('King Doot') else '',
        goal=2,
        unit='x',
        completed=has_companion('King Doot')
    ))
    po_Advices[f"{cs_label if not has_companion('King Doot') else aw_label}"].append(Advice(
        label=f"{{{{ Divinity|#divinity }}}}: Harriep Major Link bonus: {'3x (Thanks Doot!)' if has_companion('King Doot') else '3x if linked'}",
        picture_class='harriep',
        progression=harriep_multi_aw if has_companion('King Doot') else '',
        goal=3,
        unit='x',
        completed=has_companion('King Doot')
    ))

    # Account Wide
    po_Advices[aw_label].append(Advice(
        label=f"{{{{Rift|#rift}}}}: Skill Mastery unlocked: {sm_base}/4%"
              f"<br>Additional 1% per Skill at 750: {sm_bonus}/{sm_eligible_skills}%",
        picture_class='skill-mastery',
        progression=f"{sm_multi:.2f}",
        goal=f"{ValueToMulti(4 + sm_eligible_skills):.2f}",
        unit='x'
    ))

    max_booked_note = '<br>Not max booked!' if not any_dk_max_booked else ''
    max_preset_note = '<br>Not max leveled in any preset!' if not any_dk_max_leveled else ''
    breakdown = f'<br>({talent_value:.3f} talent * {pow10_kills:.3f} pow10 kills)' if any_dk_max_booked and any_dk_max_leveled else ''
    po_Advices[aw_label].append(Advice(
        label=f"DK's King of the Remembered: {kotr_multi:.3f}x"
              f"{max_booked_note}"
              f"{max_preset_note}"
              f"{breakdown}",
        picture_class='king-of-the-remembered',
        resource='orb-of-remembrance',
        progression=f"{kotr_multi:.3f}",
        unit='x'
    ))

    po_Advices[aw_label].append(Advice(
        label=f"{{{{ Sailing|#sailing}}}}: Level {gr_level} Gold Relic:"
              f"<br>{gr_multi:.2f}x ({gr_days}/{gr_max_days} days)",
        picture_class='gold-relic',
        progression=gr_days,
        goal=gr_max_days
    ))

    po_Advices[aw_label].append(Advice(
        label=f"{{{{ Event Shop|#event-shop}}}}: Supreme Wiring:"
              f"<br>{supreme_wiring_multi:.2f}x ({supreme_wiring_days}/{supreme_wiring_max_days} days)",
        picture_class='event-shop-4',
        progression=supreme_wiring_days,
        goal=supreme_wiring_max_days
    ))

    _, biggole_mole_advice = get_companion_advice('Biggole Mole')
    po_Advices[aw_label].append(biggole_mole_advice)

    po_Advices[aw_label].append(Advice(
        label=f"{{{{Compass|#the-compass}}}}: {mop['Path Name']}-{mop['Path Ordering']}: Moon of Print: "
              f"<br>{compass_moon_of_print_multi:.2f}x ({compass_moon_of_print_days}/{compass_moon_of_print_max_days} days)",
        picture_class=mop['Image'],
        progression=compass_moon_of_print_days,
        goal=compass_moon_of_print_max_days
    ))

    po_Advices[aw_label].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Lolly Flower: {charm_multi_active}/{charm_multi}x",
        picture_class=session_data.account.sneaking['PristineCharms']['Lolly Flower']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Lolly Flower']['Obtained']),
        goal=1
    ))

    po_Advices[aw_label].append(Advice(
        label=f"Weekly {{{{ Ballot|#bonus-ballot }}}}: {ballot_multi_active:.3f}/{ballot_multi:.3f}x"
              f"<br>(Buff {ballot_status})",
        picture_class='ballot-11',
        progression=int(ballot_active),
        goal=1,
        completed=True
    ))

    po_Advices[cs_label].append(Advice(
        label="Blue Dot before your sample = Only 2x from Lab is active",
        picture_class='printer-blue'
    ))
    po_Advices[cs_label].append(Advice(
        label="Yellow Star = Only 3x from Harriep is active",
        picture_class='printer-yellow'
    ))
    po_Advices[cs_label].append(Advice(
        label="Purple Swirl = 6x total from Lab and Harriep",
        picture_class='printer-purple'
    ))

    for subgroup in po_Advices:
        for advice in po_Advices[subgroup]:
            advice.mark_advice_completed()

    po_AdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Sources of Printer Output. "
                   f"Grand Total: {aw_multi:.3f}{f' - {aw_multi * cs_multi:.3f}' if len(po_Advices[cs_label]) > 0 else ''}x",
        advices=po_Advices,
        post_string="Printer Output multiplies resources printed each hour. It does NOT increase the size of taking a new sample.",
        informational=True
    )
    return po_AdviceGroup

def getProgressionTiersAdviceGroup():
    catchup = f"{AdviceType.OPT.value} - Catchup other samples to current tier"
    sampling_Advices = {
        'MaterialSamples': {
            catchup: [],
        },
    }
    sampling_AdviceGroupDict = {}
    optional_tiers = 0
    true_max = true_max_tiers['Sampling']
    max_tier = true_max - optional_tiers
    tier_MaterialSamples = 0
    all_samples = session_data.account.printer['AllSamplesSorted']

    # Assess tiers
    failed_materials_dict = {}
    for tier_number, tierRequirements in sampling_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, true_max, pre='Complete at least 1 goal')
        failed_materials_dict[tier_number] = {}
        # For each material in progressionTiers,
        #    Check if player's best sample of each material is less than tierRequirement
        #        Add failed requirements to failed_materials_dict
        for materialName, materialNumber in tierRequirements['Materials'].items():
            finalMaterialNumber = materialNumber if has_companion('King Doot') and tier_number >= 3 else materialNumber * tierRequirements[
                'NonDootDiscount']
            # logger.debug(f"Comparing {float(max(all_samples.get(materialName, [0])))} to {finalMaterialNumber}")
            try:
                if max(all_samples.get(materialName, [0])) < finalMaterialNumber:
                    failed_materials_dict[tier_number][materialName] = finalMaterialNumber
                    # logger.info(f"Tier{tier_number} failed on {materialName}: {max(all_samples.get(materialName, [0]))} < {finalMaterialNumber}")
            except Exception as reason:
                logger.exception(
                    f"Couldn't compare {type(max(all_samples.get(materialName, [0])))} {max(all_samples.get(materialName, [0]))} to T{tier_number} {materialName} {finalMaterialNumber}: {reason}")
                failed_materials_dict[tier_number][materialName] = finalMaterialNumber
        # If the player passed at least 1 requirement and tier_MaterialSamples already current, increase tier_MaterialSamples
        if len(failed_materials_dict[tier_number].keys()) < len(tierRequirements['Materials'].keys()) and tier_MaterialSamples == tier_number - 1:
            tier_MaterialSamples = tier_number
        if (
            0 < len(failed_materials_dict[tier_number].keys())  # At least 1 requirement was failed
            and subgroup_label not in sampling_Advices['MaterialSamples']  # The subgroup_label name doesn't already exist
            and len(sampling_Advices['MaterialSamples']) < session_data.account.max_subgroups + 1  # +1 to account for the catchup
            and tier_MaterialSamples < tier_number
        ):
            # Setup empty subgroup with subgroup_label as empty list to be added to
            sampling_Advices['MaterialSamples'][subgroup_label] = []

        # Finally, if that subgroup_label exists, populate with Advice
        if subgroup_label in sampling_Advices['MaterialSamples']:
            for materialName, materialNumber in failed_materials_dict[tier_number].items():
                goalString = notateNumber("Basic", materialNumber, 1)
                sampling_Advices['MaterialSamples'][subgroup_label].append(Advice(
                    label=f"{materialName}",
                    picture_class=materialName,
                    progression=notateNumber("Match", max(all_samples.get(materialName, [0])), 2, '', goalString),
                    goal=goalString,
                    resource=getSampleClass(materialName)
                ))

    # After evaluating all tiers, populate the catchup group
    for materialName, materialNumber in failed_materials_dict.get(tier_MaterialSamples, {}).items():
        goalString = notateNumber("Basic", materialNumber, 1)
        sampling_Advices['MaterialSamples'][catchup].append(Advice(
            label=f"{materialName}",
            picture_class=materialName,
            progression=notateNumber("Match", max(all_samples.get(materialName, [0])), 2, '', goalString),
            goal=goalString,
            resource=getSampleClass(materialName)
        ))

    # Generate AdviceGroups
    sampling_AdviceGroupDict["MaterialSamples"] = AdviceGroup(
        tier=tier_MaterialSamples,
        pre_string='Improve material samples',
        advices=sampling_Advices['MaterialSamples'],
        completed=all(['Optional' in subgroup_label for subgroup_label in sampling_Advices['MaterialSamples']])
    )
    sampling_AdviceGroupDict['MaterialSamples'].remove_empty_subgroups()

    overall_SectionTier = min(true_max, tier_MaterialSamples)
    return sampling_AdviceGroupDict, overall_SectionTier, max_tier,true_max

def getSamplingAdviceSection() -> AdviceSection:
    if session_data.account.construction_buildings['3D Printer']['Level'] < 1:
        sampling_AdviceSection = AdviceSection(
            name='Sampling',
            tier='Not Yet Evaluated',
            header='Come back after unlocking the 3D Printer within the Construction skill in World 3!',
            picture='3D_Printer.gif',
            unreached=True
        )
        return sampling_AdviceSection

    # Generate AdviceGroups
    sampling_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    sampling_AdviceGroupDict["PrinterSampleRate"] = getPrinterSampleRateAdviceGroup()
    sampling_AdviceGroupDict["PrinterOutput"] = getPrinterOutputAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    sampling_AdviceSection = AdviceSection(
        name='Sampling',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Sampling tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='3D_Printer.gif',
        groups=sampling_AdviceGroupDict.values(),
    )
    return sampling_AdviceSection
