from flask import g as session_data
from consts import lavaFunc, sampling_progressionTiers, maxTiersPerGroup
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import notateNumber
from utils.logging import get_logger


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
    vialBonus = session_data.account.alchemy_vials.get('Snow Slurry (Snow Ball)', {}).get('Value', 0) * session_data.account.vialMasteryMulti
    if session_data.account.labBonuses.get("My 1st Chemistry Set", {}).get("Enabled", False):
        vialBonus *= 2
    account_sum += vialBonus
    account_sum += session_data.account.alchemy_bubbles['Sample It']['BaseValue']
    account_sum += 0.5 * session_data.account.saltlick.get('Printer Sample Size', 0)
    account_sum += 0.5 * session_data.account.merits[2][4]['Level']
    account_sum += session_data.account.family_bonuses['Maestro']['Value']
    stampleValue = session_data.account.stamps.get('Stample Stamp', {}).get('Value', 0)
    amplestampleValue = session_data.account.stamps.get('Amplestample Stamp', {}).get('Value', 0)
    if session_data.account.labBonuses.get("Certified Stamp Book", {}).get("Enabled", False):
        stampleValue *= 2
        amplestampleValue *= 2
    if session_data.account.sneaking.get("PristineCharms", {}).get("Liqorice Rolle", False):
        stampleValue *= 1.25
        amplestampleValue *= 1.25
    account_sum += stampleValue
    account_sum += amplestampleValue
    account_sum += float(session_data.account.arcade.get(5, {}).get('Value', 0))
    account_sum += session_data.account.achievements.get('Saharan Skull', False)
    achievementStatus = session_data.account.achievements.get('Saharan Skull', False)
    starTalentOnePoint = lavaFunc('bigBase', 1, 10, 0.075)
    account_sum += starTalentOnePoint

    accountSubgroup = f"Account-Wide: +{account_sum:.2f}%"
    psrAdvices[accountSubgroup] = []
    
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Snow Slurry vial: "
              f"+{vialBonus:.2f}%",
        picture_class='snow-slurry',
        progression=session_data.account.alchemy_vials.get('Snow Slurry (Snow Ball)', {}).get('Level', 0),
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
              f"+{0.5 * session_data.account.merits[2][4]['Level']}/{0.5 * session_data.account.merits[2][4]['MaxLevel']}%",
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
        label=f"Amplestample Stamp: +{amplestampleValue:.3f}/6.45%",
        picture_class="amplestample-stamp",
        progression=session_data.account.stamps.get("Amplestample Stamp", {}).get("Level", 0),
        goal=32,
        resource=session_data.account.stamps.get("Amplestample Stamp", {}).get("Material", 0),
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Stample Stamp: +{stampleValue:.3f}/6.667%",
        picture_class="stample-stamp",
        progression=session_data.account.stamps.get("Stample Stamp", {}).get("Level", 0),
        goal=60,
        resource=session_data.account.stamps.get("Stample Stamp", {}).get("Material", 0),
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Lab Bonus: Certified Stamp Book: "
              f"{'2/2x (Already applied)' if session_data.account.labBonuses.get('Certified Stamp Book', {}).get('Enabled', False) else '1/2x'}",
        picture_class="certified-stamp-book",
        progression=int(session_data.account.labBonuses.get("Certified Stamp Book", {}).get("Enabled", False)),
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Liqorice Rolle: "
              f"{'1.25/1.25x (Already applied)' if session_data.account.sneaking.get('PristineCharms', {}).get('Liqorice Rolle', False) else '1/1.25x'}",
        picture_class="liqorice-rolle",
        progression=int(session_data.account.sneaking.get("PristineCharms", {}).get("Liqorice Rolle", False)),
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Arcade Bonus: {session_data.account.arcade.get(5, {}).get('Value', ''):.2f}/2%",
        picture_class="arcade-bonus-5",
        progression=session_data.account.arcade.get(5, {}).get('Level', 0),
        goal=100
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"W3 Achievement: Saharan Skull: {1 if achievementStatus else 0}/1%",
        picture_class="saharan-skull",
        progression=1 if achievementStatus else 0,
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
        characterTotalPSR = account_sum + starTalentDiffToMax + toon.po_boxes_invested.get('Utilitarian Capsule', {}).get('Bonus1Value', 0)
        if toon.sub_class == 'Squire':
            characterTotalPSR += squireSuperSamplesMaxBook
        if 90 > characterTotalPSR:
            shortBy = 90 - characterTotalPSR
            prayerGain = min(shortBy, session_data.account.prayers['The Royal Sampler']['BonusValue'])
            characterEval = f"{'Keep prayer equipped' if 'The Royal Sampler' in toon.equipped_prayers else 'Equip prayer'} for +{prayerGain:.3f}%"
        else:
            characterEval = f"Prayer not needed{'. You may remove if desired.' if 'The Royal Sampler' in toon.equipped_prayers else ', not worn.'}"

        psrAdvices[prayerSubgroup].append(Advice(
            label=f"{toon.character_name}: {characterEval}",
            picture_class=f"{toon.class_name_icon}",
            progression=f"{characterTotalPSR:.2f}",
            goal=90,
            unit="%"
        ))

    for group_name in psrAdvices:
        if group_name != prayerSubgroup:
            for advice in psrAdvices[group_name]:
                mark_advice_completed(advice)

    psrAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of Printer Sample Rate (90% Hardcap)",
        advices=psrAdvices
    )
    return psrAdviceGroup

def setSamplingProgressionTier() -> AdviceSection:
    catchup = "Info- Catchup other samples to current tier"
    sampling_AdviceDict = {
        "MaterialSamples": {
            catchup: [],
        },
    }
    sampling_AdviceGroupDict = {}
    sampling_AdviceSection = AdviceSection(
        name="Sampling",
        tier="Not Yet Evaluated",
        header="",
        picture="3D_Printer.gif",
    )

    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        sampling_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return sampling_AdviceSection
    elif session_data.account.construction_buildings['3D Printer']['Level'] < 1:
        sampling_AdviceSection.header = "Come back after unlocking the 3D Printer within the Construction skill in World 3!"
        return sampling_AdviceSection

    infoTiers = 0
    max_tier = max(sampling_progressionTiers.keys()) - infoTiers
    tier_MaterialSamples = 0
    #highestSample = session_data.account.printer['HighestValue']
    allSamples = session_data.account.printer['AllSamplesSorted']

    # Generate Alert Advice

    # Assess tiers
    failedMaterialsDict = {}
    for tierNumber, tierRequirements in sampling_progressionTiers.items():
        subgroupName = f"Meet at least 1 sample size to reach {'Informational ' if tierNumber > max_tier else ''}Tier {tierNumber}"
        failedMaterialsDict[tierNumber] = {}
        # For each material in progressionTiers,
        #    Check if player's best sample of each material is less than tierRequirement
        #        Add failed requirements to failedMaterialsDict
        for materialName, materialNumber in tierRequirements['Materials'].items():
            finalMaterialNumber = materialNumber if session_data.account.doot_owned and tierNumber >= 3 else materialNumber * tierRequirements['NonDootDiscount']
            if max(allSamples.get(materialName, [0])) < finalMaterialNumber:
                failedMaterialsDict[tierNumber][materialName] = finalMaterialNumber
                #logger.info(f"Tier{tierNumber} failed on {materialName}: {max(allSamples.get(materialName, [0]))} < {finalMaterialNumber}")
        # If the player passed at least 1 requirement and tier_MaterialSamples already current, increase tier_MaterialSamples
        if len(failedMaterialsDict[tierNumber].keys()) < len(tierRequirements.keys()) and tier_MaterialSamples == tierNumber - 1:
            tier_MaterialSamples = tierNumber
        if (
            0 < len(failedMaterialsDict[tierNumber].keys())  #At least 1 requirement was failed
            and subgroupName not in sampling_AdviceDict['MaterialSamples']  #The subgroupName name doesn't already exist
            and len(sampling_AdviceDict['MaterialSamples']) < maxTiersPerGroup  #Less than maxTiersPerGroup already exist
            and tier_MaterialSamples < tierNumber
        ):
            #Setup empty subgroup with subgroupName as empty list to be added to
            sampling_AdviceDict['MaterialSamples'][subgroupName] = []

        #Finally, if that subgroupName exists, populate with Advice
        if subgroupName in sampling_AdviceDict['MaterialSamples']:
            for materialName, materialNumber in failedMaterialsDict[tierNumber].items():
                goalLetter = notateNumber("Basic", materialNumber, 1)[-1]
                if goalLetter.isalpha():
                    sampling_AdviceDict['MaterialSamples'][subgroupName].append(Advice(
                        label=f"{materialName}",
                        picture_class=materialName,
                        progression=notateNumber("Match", max(allSamples.get(materialName, [0])), 2, goalLetter[-1]),
                        goal=notateNumber("Match", materialNumber, 1, goalLetter[-1]),
                        resource=getSampleClass(materialName)
                    ))
                else:
                    sampling_AdviceDict['MaterialSamples'][subgroupName].append(Advice(
                        label=f"{materialName}",
                        picture_class=materialName,
                        progression=notateNumber("Basic", max(allSamples.get(materialName, [0])), 1),
                        goal=notateNumber("Basic", materialNumber, 1),
                        resource=getSampleClass(materialName)
                    ))

    #After evaluating all tiers, populate the catchup group
    for materialName, materialNumber in failedMaterialsDict.get(tier_MaterialSamples, {}).items():
        goalLetter = notateNumber("Basic", materialNumber, 1)[-1]
        if goalLetter.isalpha():
            sampling_AdviceDict['MaterialSamples'][catchup].append(Advice(
                label=f"{materialName}",
                picture_class=materialName,
                progression=notateNumber("Match", max(allSamples.get(materialName, [0])), 2, goalLetter[-1]),
                goal=notateNumber("Match", materialNumber, 1, goalLetter[-1]),
                resource=getSampleClass(materialName)
            ))
        else:
            sampling_AdviceDict['MaterialSamples'][catchup].append(Advice(
                label=f"{materialName}",
                picture_class=materialName,
                progression=notateNumber("Basic", max(allSamples.get(materialName, [0])), 1),
                goal=notateNumber("Basic", materialNumber, 1),
                resource=getSampleClass(materialName)
            ))

    # Generate AdviceGroups
    sampling_AdviceGroupDict["MaterialSamples"] = AdviceGroup(
        tier=tier_MaterialSamples,
        pre_string="Improve material samples",
        advices=sampling_AdviceDict['MaterialSamples']
    )
    sampling_AdviceGroupDict["MaterialSamples"].remove_empty_subgroups()
    sampling_AdviceGroupDict["PrinterSampleRate"] = getPrinterSampleRateAdviceGroup()
    complete_toons = 0  # Either above 90 and the prayer not worn, or below 90 and already wearing the prayer. Those are the 2 "no action needed" states
    for entry in sampling_AdviceGroupDict["PrinterSampleRate"].advices['Which Characters need Royal Sampler?']:
        if "Keep prayer equipped" in entry.label or "Prayer not needed, not worn." in entry.label:
            complete_toons += 1

    # Generate AdviceSection
    overall_SamplingTier = min(max_tier + infoTiers, tier_MaterialSamples)  #Looks silly, but may get more evaluations in the future
    tier_section = f"{overall_SamplingTier}/{max_tier}"
    sampling_AdviceSection.tier = tier_section
    sampling_AdviceSection.pinchy_rating = overall_SamplingTier
    sampling_AdviceSection.groups = sampling_AdviceGroupDict.values()
    if overall_SamplingTier >= max_tier:
        sampling_AdviceSection.header = f"Best Sampling tier met: {tier_section}<br>You best ❤️"
        if complete_toons >= session_data.account.playerCount:  #Checks both the tier requirement and the Royal Sampler goodness
            sampling_AdviceSection.complete = True
    else:
        sampling_AdviceSection.header = f"Best Sampling tier met: {tier_section}"
    return sampling_AdviceSection
