import math
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed, safer_get
from utils.text_formatting import notateNumber
from utils.logging import get_logger
from consts import (
    lavaFunc, ValueToMulti, break_you_best, skillIndexList,
    sampling_progressionTiers, goldrelic_multisDict, max_printer_sample_rate, arcade_max_level
)


logger = get_logger(__name__)

def getSampleClass(materialName: str) -> str:
    if materialName == "Oak Logs":
        return "mage-icon"
    elif materialName == "Copper Ore":
        return "warrior-icon"
    elif materialName == "Goldfish":
        return "barbarian-icon"
    elif materialName == "Fly":
        return "bowman-icon"
    elif materialName == "Spore Cap":
        return "voidwalker-icon"
    else:
        return ""

def getPrinterSampleRateAdviceGroup() -> AdviceGroup:
    psrAdvices = {}

    #Account-Wide
    account_sum = 0.0
    vialBonus = session_data.account.alchemy_vials['Snow Slurry (Snow Ball)']['Value']
    account_sum += vialBonus
    account_sum += session_data.account.alchemy_bubbles['Sample It']['BaseValue']
    account_sum += 0.5 * session_data.account.saltlick.get('Printer Sample Size', 0)
    account_sum += 0.5 * session_data.account.merits[2][4]['Level']
    account_sum += session_data.account.family_bonuses['Maestro']['Value']
    stample_baseValue = session_data.account.stamps['Stample Stamp']['Value']
    stampleValue = session_data.account.stamps['Stample Stamp']['Value']
    amplestample_baseValue = session_data.account.stamps['Amplestample Stamp']['Value']
    amplestampleValue = session_data.account.stamps['Amplestample Stamp']['Value']
    if session_data.account.labBonuses['Certified Stamp Book']['Enabled']:
        stampleValue *= 2
        amplestampleValue *= 2
    if session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']:
        stampleValue *= 1.25
        amplestampleValue *= 1.25
    account_sum += stampleValue
    account_sum += amplestampleValue
    account_sum += float(session_data.account.arcade.get(5, {}).get('Value', 0))
    account_sum += session_data.account.achievements['Saharan Skull']['Complete']
    #achievementStatus = session_data.account.achievements['Saharan Skull']['Complete']
    starTalentOnePoint = lavaFunc('bigBase', 1, 10, 0.075)
    account_sum += starTalentOnePoint

    accountSubgroup = f"Account-Wide: +{account_sum:.2f}%"
    psrAdvices[accountSubgroup] = []
    
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Snow Slurry {{{{ Vial|#vials }}}}: +{vialBonus:.2f}/30%",
        picture_class='snow-slurry',
        progression=session_data.account.alchemy_vials['Snow Slurry (Snow Ball)']['Level'],
        goal=13
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Sample It bubble: "
              f"+{session_data.account.alchemy_bubbles['Sample It']['BaseValue']:.2f}/10%",
        picture_class="sample-it",
        progression=session_data.account.alchemy_bubbles['Sample It']['Level'],
        goal=200,
        resource=session_data.account.alchemy_bubbles['Sample It']['Material']
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"{{{{ Salt Lick|#salt-lick }}}} bonus: "
              f"+{0.5 * session_data.account.saltlick.get('Printer Sample Size', 0)}/10%",
        picture_class="salt-lick",
        progression=session_data.account.saltlick.get('Printer Sample Size', 0),
        goal=20
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"W3 Printer Sample Rate merit: "
              f"+{0.5 * session_data.account.merits[2][4]['Level']}/{0.5 * session_data.account.merits[2][4]['MaxLevel']:.0f}%",
        picture_class="merit-2-4",
        progression=session_data.account.merits[2][4]["Level"],
        goal=session_data.account.merits[2][4]["MaxLevel"]
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Maestro Family Bonus: "
              f"{session_data.account.family_bonuses['Maestro']['Value']:.2f}/4.5% at Class Level {session_data.account.family_bonuses['Maestro']['Level']}",
        picture_class="maestro-icon",
        progression=session_data.account.family_bonuses['Maestro']['Level'],
        goal=328
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Amplestample Stamp base value: +{amplestample_baseValue:.3f}/2.581%"
              f"<br>After multipliers: {amplestampleValue:.3f}%",
        picture_class="amplestample-stamp",
        progression=session_data.account.stamps['Amplestample Stamp']['Level'],
        goal=32,
        resource=session_data.account.stamps['Amplestample Stamp']['Material'],
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Stample Stamp base value: +{stample_baseValue:.3f}/2.667%"
              f"<br>After multipliers: {stampleValue:.3f}%",
        picture_class="stample-stamp",
        progression=session_data.account.stamps['Stample Stamp']['Level'],
        goal=60,
        resource=session_data.account.stamps['Stample Stamp']['Material'],
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Lab Bonus: Certified Stamp Book: "
              f"{'2/2x<br>(Already applied to Stamps above)' if session_data.account.labBonuses['Certified Stamp Book']['Enabled'] else '1/2x'}",
        picture_class="certified-stamp-book",
        progression=int(session_data.account.labBonuses['Certified Stamp Book']['Enabled']),
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Liqorice Rolle: "
              f"{'1.25/1.25x<br>(Already applied to Stamps above)' if session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained'] else '1/1.25x'}",
        picture_class=session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']),
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"{{{{Arcade|#arcade}}}} Bonus: "
              f"{session_data.account.arcade[5]['Value']:.2f}/"
              f"{session_data.account.arcade[5]['MaxValue']:.0f}%",
        picture_class=session_data.account.arcade[5]['Image'],
        progression=session_data.account.arcade[5]['Level'],
        goal=arcade_max_level + 1,
        resource=session_data.account.arcade[5]['Material']
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"W3 Achievement: Saharan Skull: {int(session_data.account.achievements['Saharan Skull']['Complete'])}/1%",
        picture_class="saharan-skull",
        progression=int(session_data.account.achievements['Saharan Skull']['Complete']),
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Star Talent: Printer Sampling: {starTalentOnePoint:.3f}% at minimum level 1",
        picture_class='printer-sampling',
        progression=1,
        goal=1
    ))

    #Character-Specific
    character_sum = 0.0
    starTalentDiffToMax = lavaFunc('bigBase', 100, 10, 0.075) - starTalentOnePoint
    character_sum += starTalentDiffToMax
    poBoxMax = lavaFunc('decay', 400, 5, 200)
    character_sum += poBoxMax
    squireSuperSamplesMaxBook = lavaFunc('decay', session_data.account.library['MaxBookLevel'], 9, 75)
    characterSubgroup = f"Character-Specific: Up to +{character_sum:.3f}% or +{character_sum + squireSuperSamplesMaxBook:.2f}% for Squires"
    psrAdvices[characterSubgroup] = []
    psrAdvices[characterSubgroup].append(Advice(
        label=f"Star Talent: Printer Sampling: Additional {starTalentDiffToMax:.2f}% at max level 100",
        picture_class='printer-sampling',
        progression=1,
        goal=1
    ))
    psrAdvices[characterSubgroup].append(Advice(
        label=f"Post Office: Utilitarian Capsule: +3.33% at max 400 crates",
        picture_class='utilitarian-capsule'
    ))
    psrAdvices[characterSubgroup].append(Advice(
        label=f"Squire only: Super Samples: +{squireSuperSamplesMaxBook:.2f}% at max book level {session_data.account.library['MaxBookLevel']}",
        picture_class='super-samples'
    ))

    prayerSubgroup = f"Which Characters need Royal Sampler?"
    psrAdvices[prayerSubgroup] = []
    psrAdvices[prayerSubgroup].append(Advice(
        label=f"{{{{ Prayer|#prayers }}}}: Royal Sampler: {session_data.account.prayers['The Royal Sampler']['BonusString']}",
        picture_class='the-royal-sampler',
        progression=session_data.account.prayers['The Royal Sampler']['Level'],
        goal=20
    ))
    psrAdvices[prayerSubgroup].append(Advice(
        label=f"Character's Printer Sample Rate below is calculated WITHOUT the prayer's bonus.",
        picture_class='',
    ))
    complete_toons = 0  #Either above 90 and the prayer not worn, or below 90 and already wearing the prayer. Those are the 2 "no action needed" states
    for toon in session_data.account.safe_characters:
        characterTotalPSR = account_sum + starTalentDiffToMax + toon.po_boxes_invested['Utilitarian Capsule']['Bonus1Value']
        if toon.sub_class == 'Squire':
            characterTotalPSR += squireSuperSamplesMaxBook
        if max_printer_sample_rate > characterTotalPSR:
            shortBy = max_printer_sample_rate - characterTotalPSR
            prayerGain = min(shortBy, session_data.account.prayers['The Royal Sampler']['BonusValue'])
            characterEval = (
                f"Keep prayer equipped for +{prayerGain:.3f}% 👍"
                if 'The Royal Sampler' in toon.equipped_prayers
                else f"⚠️Equip the Prayer for +{prayerGain:.3f}%"

            ) + f"<br>{toon.po_boxes_invested['Utilitarian Capsule']['Level']}/400 PO Boxes invested"
            complete_toons += 1 if 'The Royal Sampler' in toon.equipped_prayers else 0
        else:
            characterEval = f"Prayer not needed{'. You may remove if desired.' if 'The Royal Sampler' in toon.equipped_prayers else ', not worn.'} 👍"
            complete_toons += 1

        psrAdvices[prayerSubgroup].append(Advice(
            label=f"{toon.character_name}: {characterEval}",
            picture_class=f"{toon.class_name_icon}",
            progression=f"{characterTotalPSR:.2f}",
            goal=max_printer_sample_rate,
            unit="%"
        ))

    for group_name in psrAdvices:
        if group_name != prayerSubgroup:
            for advice in psrAdvices[group_name]:
                mark_advice_completed(advice)

    psrAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of Printer Sample Rate ({max_printer_sample_rate}% Hardcap)",
        post_string=(
            f"All possible values would total well over the 90% hardcap. Targets on infinite sources are provided where I'd recommend stopping."
            if complete_toons < session_data.account.character_count
            else ''
        ),
        advices=psrAdvices,
        informational=True,
        completed=complete_toons >= session_data.account.character_count
    )
    return psrAdviceGroup

def getPrinterOutputAdviceGroup() -> AdviceGroup:
    # Calculate Multis for Labels
    # Skill Mastery
    sm_base = 4 * session_data.account.rift['SkillMastery']  # This isn't expressed anywhere in game, but is hard-coded in source code.
    sm_eligible_skills = len(skillIndexList) - 1  #-1 to exclude Combat
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
    gr_multi = ValueToMulti(gr_days * goldrelic_multisDict.get(gr_level, 0))

    supreme_wiring_max_days = 50
    supreme_wiring_days = min(supreme_wiring_max_days, safer_get(session_data.account.raw_optlacc_dict, 323, 0))
    supreme_wiring_value = (supreme_wiring_days * 2 * session_data.account.event_points_shop['Bonuses']['Supreme Wiring']['Owned'])
    supreme_wiring_multi = ValueToMulti(supreme_wiring_value)

    biggole_mole_max_days = 100
    biggole_mole_days = min(biggole_mole_max_days, safer_get(session_data.account.raw_optlacc_dict, 354, 0))
    biggole_mole_value = biggole_mole_days * 1 * session_data.account.companions['Biggole Mole']
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

    anyDKMaxBooked = False
    bestKotRBook = 0
    anyDKMaxLeveled = False
    bestKotRPresetLevel = 0
    for dk in session_data.account.dks:
        levels_above_max = dk.max_talents_over_books - session_data.account.library['MaxBookLevel']
        # Book level
        if dk.max_talents.get("178", 0) >= session_data.account.library['MaxBookLevel']:
            anyDKMaxBooked = True
        if dk.max_talents.get("178", 0) > bestKotRBook:
            bestKotRBook = dk.max_talents.get("178", 0)

        # Preset level
        if (
            dk.current_preset_talents.get("178", 0) >= session_data.account.library['MaxBookLevel']
            or dk.secondary_preset_talents.get("178", 0) >= session_data.account.library['MaxBookLevel']
        ):
            anyDKMaxLeveled = True
        if dk.current_preset_talents.get("178", 0) >= bestKotRPresetLevel:
            bestKotRPresetLevel = dk.current_preset_talents.get("178", 0) + levels_above_max
        if dk.secondary_preset_talents.get("178", 0) >= bestKotRPresetLevel:
            bestKotRPresetLevel = dk.secondary_preset_talents.get("178", 0) + levels_above_max

    talent_value = lavaFunc('decay', bestKotRPresetLevel, 5, 150)
    orb_kills = session_data.account.dk_orb_kills
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

    lab_multi_aw = 2 if session_data.account.companions['King Doot'] else 1
    lab_multi_cs = 2 if session_data.account.labBonuses['Wired In']['Enabled'] else 1

    harriep_multi_aw = 3 if session_data.account.companions['King Doot'] else 1
    harriep_multi_cs = 3 if session_data.account.divinity['Divinities'][4]['Unlocked'] else 1

    aw_multi = (
        1 * sm_multi * gr_multi * kotr_multi * charm_multi_active * ballot_multi_active
        * lab_multi_aw * harriep_multi_aw * supreme_wiring_multi * biggole_mole_multi * compass_moon_of_print_multi
    )
    aw_label = f"Account Wide: {aw_multi:.3f}x"
    cs_multi = lab_multi_cs * harriep_multi_cs
    cs_label = f"Character Specific: Up to {cs_multi}x"

    po_AdviceDict = {
        cs_label: [],
        aw_label: [],
    }

    # If Doot is not owned, these are Character Specific. Otherwise, they are account-wide
    po_AdviceDict[f"{cs_label if not session_data.account.companions['King Doot'] else aw_label}"].append(Advice(
        label=f"Lab Bonus: Wired In: {'2x (Thanks Doot!)' if session_data.account.companions['King Doot'] else '2x if connected to Lab/Arctis'}",
        picture_class='wired-in',
        progression=lab_multi_aw if session_data.account.companions['King Doot'] else '',
        goal=2,
        unit="x",
        completed=session_data.account.companions['King Doot']
    ))
    po_AdviceDict[f"{cs_label if not session_data.account.companions['King Doot'] else aw_label}"].append(Advice(
        label=f"{{{{ Divinity|#divinity }}}}: Harriep Major Link bonus: {'3x (Thanks Doot!)' if session_data.account.companions['King Doot'] else '3x if linked'}",
        picture_class='harriep',
        progression=harriep_multi_aw if session_data.account.companions['King Doot'] else '',
        goal=3,
        unit="x",
        completed=session_data.account.companions['King Doot']
    ))

    # Account Wide
    po_AdviceDict[aw_label].append(Advice(
        label=f"{{{{Rift|#rift}}}}: Skill Mastery unlocked: {sm_base}/4%"
              f"<br>Additional 1% per Skill at 750: {sm_bonus}/{sm_eligible_skills}%",
        picture_class='skill-mastery',
        progression=f"{sm_multi:.2f}",
        goal=ValueToMulti(4 + sm_eligible_skills),
        unit="x"
    ))

    po_AdviceDict[aw_label].append(Advice(
        label=f"""DK's King of the Remembered: {kotr_multi:.3f}x"""
              f"""{'<br>Not max booked!' if not anyDKMaxBooked else ''}"""
              f"""{'<br>Not max leveled in any preset!' if not anyDKMaxLeveled else ''}"""
              f"""{f"<br>({talent_value:.3f} talent * {pow10_kills:.3f} pow10 kills)" if anyDKMaxBooked and anyDKMaxLeveled else ''}""",
        picture_class="king-of-the-remembered",
        resource="orb-of-remembrance",
        progression=f"{kotr_multi:.3f}",
        unit="x"
    ))

    po_AdviceDict[aw_label].append(Advice(
        label=f"{{{{ Sailing|#sailing}}}}: Level {gr_level} Gold Relic:"
              f"<br>{gr_multi:.2f}x ({gr_days}/{gr_max_days} days)",
        picture_class="gold-relic",
        progression=gr_days,
        goal=gr_max_days
    ))

    po_AdviceDict[aw_label].append(Advice(
        label=f"{{{{ Event Shop|#event-shop}}}}: Supreme Wiring:"
              f"<br>{supreme_wiring_multi:.2f}x ({supreme_wiring_days}/{supreme_wiring_max_days} days)",
        picture_class='event-shop-4',
        progression=supreme_wiring_days,
        goal=supreme_wiring_max_days
    ))

    po_AdviceDict[aw_label].append(Advice(
        label=f"Companions: Biggole Mole: "
              f"<br>{biggole_mole_multi:.2f}x ({biggole_mole_days}/{biggole_mole_max_days} days)"
              f"{'<br>Note: May be inaccurate. Not all data contains Companions!' if not session_data.account.companions['Biggole Mole'] else ''}",
        picture_class='biggole-mole',
        progression=biggole_mole_days,
        goal=biggole_mole_max_days
    ))

    po_AdviceDict[aw_label].append(Advice(
        label=f"{{{{Compass|#the-compass}}}}: {mop['Path Name']}-{mop['Path Ordering']}: Moon of Print: "
              f"<br>{compass_moon_of_print_multi:.2f}x ({compass_moon_of_print_days}/{compass_moon_of_print_max_days} days)",
        picture_class=mop['Image'],
        progression=compass_moon_of_print_days,
        goal=compass_moon_of_print_max_days
    ))

    po_AdviceDict[aw_label].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Lolly Flower: {charm_multi_active}/{charm_multi}x",
        picture_class=session_data.account.sneaking['PristineCharms']['Lolly Flower']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Lolly Flower']['Obtained']),
        goal=1
    ))

    po_AdviceDict[aw_label].append(Advice(
        label=f"Weekly {{{{ Ballot|#bonus-ballot }}}}: {ballot_multi_active:.3f}/{ballot_multi:.3f}x"
              f"<br>(Buff {ballot_status})",
        picture_class="ballot-11",
        progression=int(ballot_active),
        goal=1,
        completed=True
    ))

    po_AdviceDict[cs_label].append(Advice(
        label="Blue Dot before your sample = Only 2x from Lab is active",
        picture_class="printer-blue"
    ))
    po_AdviceDict[cs_label].append(Advice(
        label="Yellow Star = Only 3x from Harriep is active",
        picture_class="printer-yellow"
    ))
    po_AdviceDict[cs_label].append(Advice(
        label="Purple Swirl = 6x total from Lab and Harriep",
        picture_class="printer-purple"
    ))

    for subgroup in po_AdviceDict:
        for advice in po_AdviceDict[subgroup]:
            mark_advice_completed(advice)

    po_AdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"""Info- Sources of Printer Output. """
                   f"""Grand Total: {aw_multi:.3f}{f" - {aw_multi * cs_multi:.3f}" if len(po_AdviceDict[cs_label]) > 0 else ''}x""",
        advices=po_AdviceDict,
        post_string="Please note: Printer Output multiplies resources printed each hour. It does NOT increase the size of taking a new sample.",
        informational=True
    )
    return po_AdviceGroup

def getProgressionTiersAdviceGroup():
    catchup = "Info- Catchup other samples to current tier"
    sampling_AdviceDict = {
        "MaterialSamples": {
            catchup: [],
        },
    }
    sampling_AdviceGroupDict = {}
    infoTiers = 0
    max_tier = max(sampling_progressionTiers.keys()) - infoTiers
    tier_MaterialSamples = 0
    # highestSample = session_data.account.printer['HighestValue']
    allSamples = session_data.account.printer['AllSamplesSorted']

    # Assess tiers
    failedMaterialsDict = {}
    for tierNumber, tierRequirements in sampling_progressionTiers.items():
        subgroupName = f"Meet at least 1 sample size to reach {'Informational ' if tierNumber > max_tier else ''}Tier {tierNumber}"
        failedMaterialsDict[tierNumber] = {}
        # For each material in progressionTiers,
        #    Check if player's best sample of each material is less than tierRequirement
        #        Add failed requirements to failedMaterialsDict
        for materialName, materialNumber in tierRequirements['Materials'].items():
            finalMaterialNumber = materialNumber if session_data.account.companions['King Doot'] and tierNumber >= 3 else materialNumber * tierRequirements[
                'NonDootDiscount']
            # logger.debug(f"Comparing {float(max(allSamples.get(materialName, [0])))} to {finalMaterialNumber}")
            try:
                if max(allSamples.get(materialName, [0])) < finalMaterialNumber:
                    failedMaterialsDict[tierNumber][materialName] = finalMaterialNumber
                    # logger.info(f"Tier{tierNumber} failed on {materialName}: {max(allSamples.get(materialName, [0]))} < {finalMaterialNumber}")
            except Exception as reason:
                logger.exception(
                    f"Couldn't compare {type(max(allSamples.get(materialName, [0])))} {max(allSamples.get(materialName, [0]))} to T{tierNumber} {materialName} {finalMaterialNumber}: {reason}")
                failedMaterialsDict[tierNumber][materialName] = finalMaterialNumber
        # If the player passed at least 1 requirement and tier_MaterialSamples already current, increase tier_MaterialSamples
        if len(failedMaterialsDict[tierNumber].keys()) < len(tierRequirements['Materials'].keys()) and tier_MaterialSamples == tierNumber - 1:
            tier_MaterialSamples = tierNumber
        if (
            0 < len(failedMaterialsDict[tierNumber].keys())  # At least 1 requirement was failed
            and subgroupName not in sampling_AdviceDict['MaterialSamples']  # The subgroupName name doesn't already exist
            and len(sampling_AdviceDict['MaterialSamples']) < session_data.account.maxSubgroupsPerGroup + 1  # +1 to account for the catchup
            and tier_MaterialSamples < tierNumber
        ):
            # Setup empty subgroup with subgroupName as empty list to be added to
            sampling_AdviceDict['MaterialSamples'][subgroupName] = []

        # Finally, if that subgroupName exists, populate with Advice
        if subgroupName in sampling_AdviceDict['MaterialSamples']:
            for materialName, materialNumber in failedMaterialsDict[tierNumber].items():
                goalString = notateNumber("Basic", materialNumber, 1)
                sampling_AdviceDict['MaterialSamples'][subgroupName].append(Advice(
                    label=f"{materialName}",
                    picture_class=materialName,
                    progression=notateNumber("Match", max(allSamples.get(materialName, [0])), 2, '', goalString),
                    goal=goalString,
                    resource=getSampleClass(materialName)
                ))

    # After evaluating all tiers, populate the catchup group
    for materialName, materialNumber in failedMaterialsDict.get(tier_MaterialSamples, {}).items():
        goalString = notateNumber("Basic", materialNumber, 1)
        sampling_AdviceDict['MaterialSamples'][catchup].append(Advice(
            label=f"{materialName}",
            picture_class=materialName,
            progression=notateNumber("Match", max(allSamples.get(materialName, [0])), 2, '', goalString),
            goal=goalString,
            resource=getSampleClass(materialName)
        ))

    # Generate AdviceGroups
    sampling_AdviceGroupDict["MaterialSamples"] = AdviceGroup(
        tier=tier_MaterialSamples,
        pre_string="Improve material samples",
        advices=sampling_AdviceDict['MaterialSamples'],
        informational=all(['Info' in subgroupName for subgroupName in sampling_AdviceDict['MaterialSamples']]),
        completed=all(['Info' in subgroupName for subgroupName in sampling_AdviceDict['MaterialSamples']])
    )
    sampling_AdviceGroupDict["MaterialSamples"].remove_empty_subgroups()

    overall_SectionTier = min(max_tier + infoTiers, tier_MaterialSamples)  # Looks silly, but may get more evaluations in the future
    return sampling_AdviceGroupDict, overall_SectionTier, max_tier, max_tier + infoTiers

def getSamplingAdviceSection() -> AdviceSection:
    if session_data.account.construction_buildings['3D Printer']['Level'] < 1:
        sampling_AdviceSection = AdviceSection(
            name="Sampling",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the 3D Printer within the Construction skill in World 3!",
            picture="3D_Printer.gif",
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
        name="Sampling",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Sampling tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="3D_Printer.gif",
        groups=sampling_AdviceGroupDict.values(),
    )
    return sampling_AdviceSection
