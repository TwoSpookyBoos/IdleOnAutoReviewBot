from flask import g as session_data
from consts import lavaFunc
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger


logger = get_logger(__name__)

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
        label=f"Snow Slurry vial: +{vialBonus:.2f}%",
        picture_class='snow-slurry',
        progression=session_data.account.alchemy_vials.get('Snow Slurry (Snow Ball)', {}).get('Level', 0),
        goal=13
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Sample It bubble: +{session_data.account.alchemy_bubbles['Sample It']['BaseValue']:.2f}%",
        picture_class="sample-it",
        progression=session_data.account.alchemy_bubbles['Sample It']['Level'],
        goal=200,
        resource=session_data.account.alchemy_bubbles['Sample It']['Material']
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"{{{{ Salt Lick|#salt-lick }}}}: +{0.5 * session_data.account.saltlick.get('Printer Sample Size', 0)}%",
        picture_class="salt-lick",
        progression=session_data.account.saltlick.get('Printer Sample Size', 0),
        goal=20
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"W3 Printer Sample Rate merit: +{0.5 * session_data.account.merits[2][4]['Level']}%",
        picture_class="merit-2-4",
        progression=session_data.account.merits[2][4]["Level"],
        goal=session_data.account.merits[2][4]["MaxLevel"]
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Maestro Family Bonus: {session_data.account.family_bonuses['Maestro']['DisplayValue']} at Class Level {session_data.account.family_bonuses['Maestro']['Level']}",
        picture_class="maestro-icon",
        progression=session_data.account.family_bonuses['Maestro']['Level'],
        goal=328
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Amplestample Stamp: +{amplestampleValue:.3f}%",
        picture_class="amplestample-stamp",
        progression=session_data.account.stamps.get("Amplestample Stamp", {}).get("Level", 0),
        goal=32,
        resource=session_data.account.stamps.get("Amplestample Stamp", {}).get("Material", 0),
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Stample Stamp: +{stampleValue:.3f}%",
        picture_class="stample-stamp",
        progression=session_data.account.stamps.get("Stample Stamp", {}).get("Level", 0),
        goal=60,
        resource=session_data.account.stamps.get("Stample Stamp", {}).get("Material", 0),
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Lab Bonus: Certified Stamp Book: {'2x (Already applied)' if session_data.account.labBonuses.get('Certified Stamp Book', {}).get('Enabled', False) else '1x'}",
        picture_class="certified-stamp-book",
        progression=int(session_data.account.labBonuses.get("Certified Stamp Book", {}).get("Enabled", False)),
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Liqorice Rolle: {'1.25x (Already applied)' if session_data.account.sneaking.get('PristineCharms', {}).get('Liqorice Rolle', False) else '1x'}",
        picture_class="liqorice-rolle",
        progression=int(session_data.account.sneaking.get("PristineCharms", {}).get("Liqorice Rolle", False)),
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Arcade Bonus: {session_data.account.arcade.get(5, {}).get('Display', '')} {'(2% max)' if session_data.account.arcade.get(5, {}).get('Level', 0) < 100 else ''}",
        picture_class="arcade-bonus-5",
        progression=session_data.account.arcade.get(5, {}).get('Level', 0),
        goal=100
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"W3 Achievement: Saharan Skull: {1 if achievementStatus else 0}%",
        picture_class="saharan-skull",
        progression=1 if achievementStatus else 0,
        goal=1
    ))
    psrAdvices[accountSubgroup].append(Advice(
        label=f"Star Talent: Printer Sampling: {starTalentOnePoint:.3f}% at minimum level 1",
        picture_class='printer-sampling'
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
        picture_class='printer-sampling'
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
    sampling_AdviceDict = {}
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

    max_tier = 0
    tier_PrinterSampleRate = 0

    # Generate AdviceGroups
    sampling_AdviceGroupDict["PrinterSampleRate"] = getPrinterSampleRateAdviceGroup()

    # Generate AdviceSection
    overall_SamplingTier = min(max_tier, tier_PrinterSampleRate)  #Looks silly, but may get more evaluations in the future
    tier_section = f"{overall_SamplingTier}/{max_tier}"
    sampling_AdviceSection.tier = tier_section
    sampling_AdviceSection.pinchy_rating = overall_SamplingTier
    sampling_AdviceSection.groups = sampling_AdviceGroupDict.values()
    if overall_SamplingTier == max_tier:
        sampling_AdviceSection.header = f"Best Sampling tier met: {tier_section}<br>You best ❤️"
    else:
        sampling_AdviceSection.header = f"Best Sampling tier met: {tier_section}"
    return sampling_AdviceSection
