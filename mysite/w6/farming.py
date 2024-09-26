from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.data_formatting import mark_advice_completed
from flask import g as session_data
from consts import farming_progressionTiers, break_you_best, maxFarmingCrops

logger = get_logger(__name__)

def getCropDepotAdviceGroup() -> AdviceGroup:
    lab_note = f"<br>Note: Most of Lab is defaulted ON until I figure out Lab parsing. Sorry 🙁"

    navette_value = session_data.account.labJewels['Pure Opal Navette']['Value'] * session_data.account.labJewels['Pure Opal Navette']['Enabled']
    navette_max = session_data.account.labJewels['Pure Opal Navette']['BaseValue']

    spelunker_multi = max(1, session_data.account.labBonuses['Spelunker Obol']['Value'])
    spelunker_max = session_data.account.labBonuses['Spelunker Obol']['BaseValue']

    rhombol_value = session_data.account.labJewels['Pure Opal Rhombol']['Value'] * session_data.account.labJewels['Pure Opal Rhombol']['Enabled']
    rhombol_max = session_data.account.labJewels['Pure Opal Rhombol']['BaseValue']
    rhombol_enhanced_max = rhombol_max * (spelunker_max + (navette_max/100))

    studies_value = max(1, 1 + ((session_data.account.labBonuses['Depot Studies PhD']['Value'] + rhombol_value) / 100))
    studies_max = 1 + (session_data.account.labBonuses['Depot Studies PhD']['BaseValue'] / 100)
    studies_enhanced_max_value = session_data.account.labBonuses['Depot Studies PhD']['BaseValue']

    lab_multi = max(1, 1 + ((session_data.account.labBonuses['Depot Studies PhD']['Value'] + rhombol_value) / 100))
    lab_max = max(1, 1 + ((studies_enhanced_max_value + rhombol_enhanced_max) / 100))
    cd_advices = [
        Advice(
            label=f"Lab Jewel: Pure Opal Navette: Increases the value of Spelunker Obol by +{navette_value/100:.1f}/{navette_max/100:.1f}"
                  f"<br>(Yes, this jewel is bugged)",
            picture_class='pure-opal-navette',
            progression=int(session_data.account.labJewels['Pure Opal Navette']['Enabled']),
            goal=1
        ),
        Advice(
            label=f"Lab Bonus: Spelunker Obol: Multiplies the value of Pure Opal Rhombol by {spelunker_multi:.1f}/{spelunker_max:.1f}x",
            picture_class='spelunker-obol',
            progression=int(session_data.account.labBonuses['Spelunker Obol']['Enabled']),
            goal=1
        ),
        Advice(
            label=f"Lab Jewel: Pure Opal Rhombol: Increases Depot Studies by +{rhombol_value:.0f}/{rhombol_max:.0f}",
            picture_class='pure-opal-rhombol',
            progression=int(session_data.account.labJewels['Pure Opal Rhombol']['Enabled']),
            goal=1
        ),
        Advice(
            label=f"Lab Bonus: Depot Studies PhD: {studies_value:.2f}/{studies_max:.2f}x",
            picture_class='depot-studies-phd',
            progression=int(session_data.account.labBonuses['Depot Studies PhD']['Enabled']),
            goal=1
        ),
        Advice(
            label=f"Final Lab multi: {lab_multi:.2f}/{lab_max:.2f}x"
                  f"{lab_note}",
            picture_class='laboratory',
            progression=f"{lab_multi:.2f}",
            goal=f"{lab_max:.2f}"
        ),
        Advice(
            label=f"Total Crops Discovered: {session_data.account.farming['CropsUnlocked']}/{maxFarmingCrops}",
            picture_class='crop-depot',
            progression=session_data.account.farming['CropsUnlocked'],
            goal=maxFarmingCrops
        ),
    ]
    for bonusIndex, bonusDetails in session_data.account.farming['Depot'].items():
        if bonusDetails['ScalingType'] == 'pow':
            scaling_label = f"{bonusDetails['ScalingNumber']}x {bonusDetails['BonusString']} per crop discovered, multiplicative"
            if bonusDetails['ValuePlus1'] > bonusDetails['Value']:
                scaling_label += f".<br>Next crop would increase total by {bonusDetails['ValuePlus1'] - bonusDetails['Value']:,.3f}"
        else:
            scaling_label = f"+{bonusDetails['ScalingNumber']}{'%' if bonusDetails['BonusString'] != 'Base Critters' else ''} {bonusDetails['BonusString']} per crop discovered, additive"

        cd_advices.append(Advice(
            label=f"{scaling_label}"
                  f"{'<br>Unlock via {{ Jade Emporium|#sneaking }}' if not bonusDetails['Unlocked'] else ''}",
            picture_class=bonusDetails['Image'],
            progression=f"{bonusDetails['Value']:,.2f}"
        ))

    for advice in cd_advices:
        mark_advice_completed(advice)

    cd_ag = AdviceGroup(
        tier='',
        pre_string='Informational- Crop Depot Bonuses and scaling',
        advices=cd_advices
    )

    return cd_ag

def getDayMarketAdviceGroup() -> AdviceGroup:
    dm = {name:details for name, details in session_data.account.farming['MarketUpgrades'].items() if details['MarketType'] == 'Day'}
    dm_advices = [
        Advice(
            label=f"{details['Level']}/{details['MaxLevel']} {name}: {details['Description']}",
            picture_class='day-market'
        )
        for name, details in dm.items()]

    dm_ag = AdviceGroup(
        tier='',
        pre_string=f"Informational- Day Market upgrades",
        advices=dm_advices
    )
    return dm_ag

def getNightMarketAdviceGroup() -> AdviceGroup:
    nm = {name:details for name, details in session_data.account.farming['MarketUpgrades'].items() if details['MarketType'] == 'Night'}
    nm_advices = [
        Advice(
            label=f"{details['Level']}/{details['MaxLevel']} {name}: {details['Description']}",
            picture_class='night-market'
        )
        for name, details in nm.items()]

    dm_ag = AdviceGroup(
        tier='',
        pre_string=f"Informational- Night Market upgrades",
        advices=nm_advices
    )
    return dm_ag

def setFarmingProgressionTier():
    farming_AdviceDict = {
    }
    farming_AdviceGroupDict = {}
    farming_AdviceSection = AdviceSection(
        name="Farming",
        tier="0",
        pinchy_rating=0,
        header="Best Farming tier met: Not Yet Evaluated",
        picture="wiki/FarmCropBean.png",
        complete=False
    )
    highestFarmingSkillLevel = max(session_data.account.all_skills["Farming"])
    if highestFarmingSkillLevel < 1:
        farming_AdviceSection.header = "Come back after unlocking the Farming skill in W6!"
        return farming_AdviceSection

    infoTiers = 0
    max_tier = max(farming_progressionTiers.keys(), default=0) - infoTiers
    tier_Farming = 0

    farming_AdviceGroupDict['Depot'] = getCropDepotAdviceGroup()
    farming_AdviceGroupDict['Day'] = getDayMarketAdviceGroup()
    farming_AdviceGroupDict['Night'] = getNightMarketAdviceGroup()

    overall_FarmingTier = min(max_tier + infoTiers, tier_Farming)
    tier_section = f"{overall_FarmingTier}/{max_tier}"
    farming_AdviceSection.pinchy_rating = overall_FarmingTier
    farming_AdviceSection.tier = tier_section
    farming_AdviceSection.groups = farming_AdviceGroupDict.values()
    if overall_FarmingTier >= max_tier:
        farming_AdviceSection.header = f"Best Farming tier met: {tier_section}{break_you_best}️"
        farming_AdviceSection.complete = True
    else:
        farming_AdviceSection.header = f"Best Farming tier met: {tier_section}"

    return farming_AdviceSection
