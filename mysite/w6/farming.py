from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.data_formatting import mark_advice_completed
from flask import g as session_data
from consts import farming_progressionTiers, break_you_best, maxTiersPerGroup, maxFarmingCrops
from utils.text_formatting import pl

logger = get_logger(__name__)

def getLandRankImage(level: int):
    if level >= 100:
        return 'landrank-7'
    elif level >= 75:
        return 'landrank-6'
    elif level >= 50:
        return 'landrank-5'
    elif level >= 25:
        return 'landrank-4'
    elif level >= 10:
        return 'landrank-3'
    elif level >= 5:
        return 'landrank-2'
    else:
        return 'landrank-1'


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
            label=f"Lab Jewel: Pure Opal Rhombol: Increases Depot Studies by +.{rhombol_value:.0f}/.{rhombol_max:.0f}",
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

def getCropValueAdviceGroup():
    val = session_data.account.farming['Value']
    mga = f"Multi Group A: {val['Doubler Multi']:.2f}"
    mgb = f"Multi Group B: {val['Mboost Sboost Multi']:.2f}"
    mgc = f"Multi Group C: {val['Pboost Ballot Multi']:.2f}"
    final = f"Conclusion: You are {'NOT capped' if val['Final'] < 100 else ''}{'overcapped' if val['BeforeCap'] > 120 else ''}"
    value_advices = {
        mga: [],
        mgb: [],
        mgc: [],
        final: [],
    }
    #MGA
    value_advices[mga].append(Advice(
        label=f"Highest full 100 Product Doubler reached for guarantee: "
              f"{(session_data.account.farming['MarketUpgrades']['Product Doubler']['Value'] // 100) * 100:.0f}%",
        picture_class='day-market',
        progression=f"{session_data.account.farming['MarketUpgrades']['Product Doubler']['Value']:.0f}",
        goal=300
    ))

    #MGB
    value_advices[mgb].append(Advice(
        label=f"Land Rank: Production Megaboost",
        picture_class='production-megaboost',
        progression=f"{session_data.account.farming['LandRankDatabase']['Production Megaboost']['Value']:.3f}"
    ))
    value_advices[mgb].append(Advice(
        label=f"Land Rank: Production Superboost",
        picture_class='production-superboost',
        progression=f"{session_data.account.farming['LandRankDatabase']['Production Superboost']['Value']:.3f}"
    ))

    #MGC
    value_advices[mgc].append(Advice(
        label=f"Minimum Land Rank: {session_data.account.farming.get('LandRankMinPlot', 0)}",
        picture_class=getLandRankImage(session_data.account.farming.get('LandRankMinPlot', 0)),
    ))
    value_advices[mgc].append(Advice(
        label=f"Land Rank: Production Boost: {session_data.account.farming['LandRankDatabase']['Production Boost']['Value']:.3f} per land rank."
              f"<br>Total: {session_data.account.farming['LandRankDatabase']['Production Boost']['Value'] * session_data.account.farming.get('LandRankMinPlot', 0):.3f}",
        picture_class='production-boost',
    ))
    ballot_active = session_data.account.ballot['CurrentBuff'] == 29
    if ballot_active:
        ballot_status = "is Active"
    elif not ballot_active and session_data.account.ballot['CurrentBuff'] != "Unknown":
        ballot_status = "is Inactive"
    else:
        ballot_status = "status is not available in provided data"
    ballot_multi = 1 + (session_data.account.ballot['Buffs'][29]['Value'] / 100)
    ballot_multi_active = max(1, ballot_multi * ballot_active)
    value_advices[mgc].append(Advice(
        label=f"Plus Weekly Ballot: {ballot_multi_active:.3f}/{ballot_multi:.3f}x"
              f"<br>(Buff {ballot_status})",
        picture_class='ballot-29',
        progression=int(ballot_active),
        goal=1
    ))

    #Final
    value_advices[final].append(Advice(
        label=f"Total before hidden 100x cap",
        picture_class='',
        progression=val['BeforeCap'],
        goal=100
    ))
    value_advices[final].append(Advice(
        label=f"Hey wait, what about Night Market Value GMO??"
              f"<br>Sorry mate, Lava hasn't implemented it 😭",
        picture_class='night-market',
        progression="Lava",
        goal="Pls"
    ))

    value_ag = AdviceGroup(
        tier='',
        pre_string="Informational- Sources of Crop Value",
        advices=value_advices
    )
    return value_ag


def setFarmingProgressionTier():
    farming_AdviceDict = {
        'Unlock Crops': {},
        'Day Market': {},
        'Night Market': {},
        'Land Ranks': {}
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
    tier_Unlock_Crops = 0
    tier_Day_Market = 0
    tier_Night_Market = 0
    tier_Land_Ranks = 0

    farming = session_data.account.farming
    multis = ['Evolution Gmo', 'Og Fertilizer']
    one_point_landranks = ['Seed of Stealth', 'Seed of Loot', 'Seed of Damage', 'Seed of Stats']

    #Assess Tiers
    for tierNumber, tierRequirements in farming_progressionTiers.items():
        subgroupName = f"To reach Tier {tierNumber}"
        #Unlock Crops
        if farming['CropsUnlocked'] < tierRequirements.get('Crops Unlocked', 0):
            if subgroupName not in farming_AdviceDict['Unlock Crops'] and len(farming_AdviceDict['Unlock Crops']) < maxTiersPerGroup:
                farming_AdviceDict['Unlock Crops'][subgroupName] = []
            if subgroupName in farming_AdviceDict['Unlock Crops']:
                shortby = tierRequirements.get('Crops Unlocked', 0) - farming['CropsUnlocked']
                farming_AdviceDict['Unlock Crops'][subgroupName].append(Advice(
                    label=f"Unlock {shortby} more crop type{pl(shortby)}",
                    picture_class='crop-depot',
                    progression=farming['CropsUnlocked'],
                    goal=tierRequirements.get('Crops Unlocked', 0)
                ))
        if subgroupName not in farming_AdviceDict['Unlock Crops'] and tier_Unlock_Crops == tierNumber - 1:
            tier_Unlock_Crops = tierNumber

        #Day Market
        for rName, rLevel in tierRequirements.get('Day Market', {}).items():
            if farming['MarketUpgrades'][rName]['Level'] < rLevel:
                if subgroupName not in farming_AdviceDict['Day Market'] and len(farming_AdviceDict['Day Market']) < maxTiersPerGroup:
                    farming_AdviceDict['Day Market'][subgroupName] = []
                if subgroupName in farming_AdviceDict['Day Market']:
                    farming_AdviceDict['Day Market'][subgroupName].append(Advice(
                        label=f"{rName}: "
                              f"{farming['MarketUpgrades'][rName]['Value']:.4g}/{farming['MarketUpgrades'][rName]['BonusPerLevel'] * rLevel:.4g}"
                              f"{'%' if rName != 'Land Plots' else ''}",
                        picture_class='day-market',
                        progression=farming['MarketUpgrades'][rName]['Level'],
                        goal=rLevel
                    ))
        if subgroupName not in farming_AdviceDict['Day Market'] and tier_Day_Market == tierNumber - 1:
            tier_Day_Market = tierNumber

        #Night Market
        for rName, rLevel in tierRequirements.get('Night Market', {}).items():
            if farming['MarketUpgrades'][rName]['Level'] < rLevel:
                if subgroupName not in farming_AdviceDict['Night Market'] and len(farming_AdviceDict['Night Market']) < maxTiersPerGroup:
                    farming_AdviceDict['Night Market'][subgroupName] = []
                if subgroupName in farming_AdviceDict['Night Market']:
                    if rName in multis:
                        current = 1 + (farming['MarketUpgrades'][rName]['Value'] / 100)
                        target = 1 + ((farming['MarketUpgrades'][rName]['BonusPerLevel'] * rLevel) / 100)
                    else:
                        current = farming['MarketUpgrades'][rName]['Value']
                        target = farming['MarketUpgrades'][rName]['BonusPerLevel'] * rLevel
                    farming_AdviceDict['Night Market'][subgroupName].append(Advice(
                        label=f"{rName}: "
                              f"{current:.4g}/{target:.4g}"
                              f"{'x' if rName in multis else '%'}",
                        picture_class='night-market',
                        progression=farming['MarketUpgrades'][rName]['Level'],
                        goal=rLevel
                    ))
        if subgroupName not in farming_AdviceDict['Night Market'] and tier_Night_Market == tierNumber - 1:
            tier_Night_Market = tierNumber

        #Land Ranks - Minimum Plot
        if farming['LandRankMinPlot'] < tierRequirements.get('LandRankMinPlot', 0):
            if subgroupName not in farming_AdviceDict['Land Ranks'] and len(farming_AdviceDict['Land Ranks']) < maxTiersPerGroup:
                farming_AdviceDict['Land Ranks'][subgroupName] = []
            if subgroupName in farming_AdviceDict['Land Ranks']:
                farming_AdviceDict['Land Ranks'][subgroupName].append(Advice(
                    label=f"Raise minimum Plot Land rank to {tierRequirements.get('LandRankMinPlot', 0)}",
                    picture_class=getLandRankImage(tierRequirements.get('LandRankMinPlot', 0)),
                    progression=farming['LandRankMinPlot'],
                    goal=tierRequirements.get('LandRankMinPlot', 0)
                ))
        #Land Ranks - Database Upgrades
        for rName, rLevel in tierRequirements.get('Land Ranks', {}).items():
            if farming['LandRankDatabase'][rName]['Level'] < rLevel:
                if subgroupName not in farming_AdviceDict['Land Ranks'] and len(farming_AdviceDict['Land Ranks']) < maxTiersPerGroup:
                    farming_AdviceDict['Land Ranks'][subgroupName] = []
                if subgroupName in farming_AdviceDict['Land Ranks']:
                    if rName in one_point_landranks:
                        current = farming['LandRankDatabase'][rName]['Value']
                        target = farming['LandRankDatabase'][rName]['BaseValue']
                    else:
                        current = farming['LandRankDatabase'][rName]['Value']
                        target = (1.7 * farming['LandRankDatabase'][rName]['BaseValue'] * rLevel) / (rLevel + 80)
                    farming_AdviceDict['Land Ranks'][subgroupName].append(Advice(
                        label=f"{rName}: {current:.4g}/{target:.4g}%",
                        picture_class=rName,
                        progression=farming['LandRankDatabase'][rName]['Level'],
                        goal=rLevel
                    ))
        if subgroupName not in farming_AdviceDict['Land Ranks'] and tier_Land_Ranks == tierNumber - 1:
            tier_Land_Ranks = tierNumber

    #Advice Groups
    farming_AdviceGroupDict['Unlock Crops'] = AdviceGroup(
        tier=tier_Unlock_Crops,
        pre_string="Continue unlocking unique crop types",
        advices=farming_AdviceDict['Unlock Crops']
    )
    farming_AdviceGroupDict['Day Market'] = AdviceGroup(
        tier=tier_Day_Market,
        pre_string="Continue leveling Day Market upgrades",
        advices=farming_AdviceDict['Day Market']
    )
    farming_AdviceGroupDict['Night Market'] = AdviceGroup(
        tier=tier_Night_Market,
        pre_string="Continue leveling Night Market upgrades",
        advices=farming_AdviceDict['Night Market']
    )
    farming_AdviceGroupDict['Land Ranks'] = AdviceGroup(
        tier=tier_Night_Market,
        pre_string="Continue leveling Land Rank Database upgrades",
        advices=farming_AdviceDict['Land Ranks']
    )
    farming_AdviceGroupDict['Value'] = getCropValueAdviceGroup()
    farming_AdviceGroupDict['Depot'] = getCropDepotAdviceGroup()
    farming_AdviceGroupDict['Day'] = getDayMarketAdviceGroup()
    farming_AdviceGroupDict['Night'] = getNightMarketAdviceGroup()

    #Advice Section
    overall_FarmingTier = min(max_tier + infoTiers, tier_Unlock_Crops, tier_Day_Market, tier_Night_Market, tier_Land_Ranks)
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
