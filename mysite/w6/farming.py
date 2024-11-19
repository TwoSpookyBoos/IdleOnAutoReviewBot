from math import ceil, floor

from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.data_formatting import mark_advice_completed
from flask import g as session_data
from consts import (farming_progressionTiers, break_you_best, maxTiersPerGroup, maxFarmingCrops, maxCharacters, max_VialLevel, maxMealLevel, stamp_maxes,
                    ValueToMulti, tomepct, getCropEvoChance, cropDict, landrankDict, maxFarmingValue, infinity_string)
from utils.text_formatting import pl, notateNumber

logger = get_logger(__name__)

def getLandRankImage(level: int) -> str:
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

def getCropDepotAdviceGroup(farming) -> AdviceGroup:
    lab_note = f"<br>Note: Most of Lab is defaulted ON until I figure out Lab parsing. Sorry 🙁"

    navette_value = session_data.account.labJewels['Pure Opal Navette']['Value'] * session_data.account.labJewels['Pure Opal Navette']['Enabled']
    navette_max = session_data.account.labJewels['Pure Opal Navette']['BaseValue']

    spelunker_multi = max(1, session_data.account.labBonuses['Spelunker Obol']['Value'])
    spelunker_max = session_data.account.labBonuses['Spelunker Obol']['BaseValue']

    rhombol_value = session_data.account.labJewels['Pure Opal Rhombol']['Value'] * session_data.account.labJewels['Pure Opal Rhombol']['Enabled']
    rhombol_max = session_data.account.labJewels['Pure Opal Rhombol']['BaseValue']
    rhombol_enhanced_max = rhombol_max * (spelunker_max + (navette_max/100))

    studies_value = max(1, ValueToMulti(session_data.account.labBonuses['Depot Studies PhD']['Value'] + rhombol_value))
    studies_max = ValueToMulti(session_data.account.labBonuses['Depot Studies PhD']['BaseValue'])
    studies_enhanced_max_value = session_data.account.labBonuses['Depot Studies PhD']['BaseValue']

    lab_multi = max(1, ValueToMulti(session_data.account.labBonuses['Depot Studies PhD']['Value'] + rhombol_value))
    lab_max = max(1, ValueToMulti(studies_enhanced_max_value + rhombol_enhanced_max))
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
            label=f"Total Crops Discovered: {farming['CropsUnlocked']}/{maxFarmingCrops}",
            picture_class='crop-depot',
            progression=farming['CropsUnlocked'],
            goal=maxFarmingCrops
        ),
    ]
    for bonusIndex, bonusDetails in farming['Depot'].items():
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
        pre_string='Informational- Crop Depot bonuses',
        advices=cd_advices,
        informational=True
    )

    return cd_ag

def getDayMarketAdviceGroup(farming) -> AdviceGroup:
    dm = {name:details for name, details in farming['MarketUpgrades'].items() if details['MarketType'] == 'Day'}
    dm_advices = [
        Advice(
            label=f"{name}: {details['Description']}",
            picture_class='day-market',
            progression=details['Level'],
            goal=details['MaxLevel']
        )
        for name, details in dm.items()]

    for advice in dm_advices:
        mark_advice_completed(advice)

    dm_ag = AdviceGroup(
        tier='',
        pre_string=f"Informational- Day Market upgrades",
        advices=dm_advices,
        informational=True
    )
    return dm_ag

def getNightMarketAdviceGroup(farming) -> AdviceGroup:
    nm = {name:details for name, details in farming['MarketUpgrades'].items() if details['MarketType'] == 'Night'}
    nm_advices = [
        Advice(
            label=f"{name}: {details['Description']}",
            picture_class='night-market',
            progression=details['Level'],
            goal=details['MaxLevel']
        )
        for name, details in nm.items()]

    for advice in nm_advices:
        mark_advice_completed(advice)

    nm_ag = AdviceGroup(
        tier='',
        pre_string=f"Informational- Night Market upgrades",
        advices=nm_advices,
        informational=True
    )
    return nm_ag

def getNMCost(name, first_level, last_level=0):
    total_cost = 0
    upgrade = session_data.account.farming['MarketUpgrades'][name]
    if first_level > last_level:
        last_level = first_level-1
    #logger.info(f"Calculating cost for {name} {first_level} until but excluding {last_level}")
    for level in range(first_level, last_level):
        #logger.debug(f"Cost for {name} {level}: {floor(upgrade['BaseCost'] * pow(upgrade['CostIncrement'], level))}")
        total_cost += floor(upgrade['BaseCost'] * pow(upgrade['CostIncrement'], level))
    return total_cost

def val_m_s_boost(megaboost, superboost):
    return ValueToMulti(
        ((1.7 * 100 * megaboost) / (megaboost + 80))
        + ((1.7 * 600 * superboost) / (superboost + 80))
    )

def val_boost(minrank, b):
    return ValueToMulti(((1.7 * 5 * b) / (b + 80)) * minrank)

def getValueLRSuggies(farming):
    #names = ['Boost', 'Megaboost', 'Superboost']
    min_lr = max(farming['LandRankMinPlot'], floor(0.8 * farming['LandRankMinPlot']))
    value = farming['Value']['Doubler Multi']
    available_points = farming['LandRankTotalRanks']
    currently_invested = sum([
        farming['LandRankDatabase']['Production Boost']['Level'],
        farming['LandRankDatabase']['Production Megaboost']['Level'],
        farming['LandRankDatabase']['Production Superboost']['Level']
    ])
    upgrades = [0, 0, 0]
    #logger.debug(f"Starting Value of {value}, Minimum Land Rank of {min_lr}, and max {available_points} points")
    #i = 0
    while value < 100 and sum(upgrades) < available_points:
        #i += 1
        dValue = [
            val_boost(min_lr, upgrades[0] + 1) / val_boost(min_lr, upgrades[0]),
            val_m_s_boost(upgrades[1] + 1, upgrades[2]) / val_m_s_boost(upgrades[1], upgrades[2]) if available_points >= 250 else 1,
            val_m_s_boost(upgrades[1], upgrades[2] + 1) / val_m_s_boost(upgrades[1], upgrades[2]) if available_points >= 1750 else 1
        ]
        value *= max(dValue)
        upgrades[dValue.index(max(dValue))] += 1
        #logger.debug(f"Round {i}: {dValue}. Victor: {names[dValue.index(max(dValue))]}. Current: {upgrades}, {value:.4f}x")
    #logger.debug(f"{sum(upgrades)} upgrades: {upgrades}. Final Value: {value}")
    return upgrades

def getEvoLRSuggies(farming):
    pass

def getCropValueAdviceGroup(farming) -> AdviceGroup:
    val = farming['Value']
    mga = f"Multi Group A: {val['Doubler Multi']:.2f}x"
    mgb = f"Multi Group B: {val['Mboost Sboost Multi']:.2f}x"
    mgc = f"Multi Group C: {val['Pboost Ballot Multi Min']:.2f}x to {val['Pboost Ballot Multi Max']:.2f}x"
    final = f"Conclusion: You are {'NOT ' if val['FinalMin'] < 100 else 'over' if val['BeforeCapMin'] >= 125 else ''}capped on Lowest plots"
    value_advices = {
        final: [],
        mga: [],
        mgb: [],
        mgc: [],
    }
    #MGA
    value_advices[mga].append(Advice(
        label=f"Highest full 100 Product Doubler reached for guarantee: "
              f"{(farming['MarketUpgrades']['Product Doubler']['Value'] // 100) * 100:.0f}%",
        picture_class='day-market',
        progression=f"{farming['MarketUpgrades']['Product Doubler']['Value']:.0f}",
        goal=300
    ))

    #MGB
    optimal_upgrades = getValueLRSuggies(farming) if farming['LandRankTotalRanks'] >= 5 else [-1, -1, -1]
    value_advices[mgb].append(Advice(
        label=f"Production Megaboost: +{farming['LandRankDatabase']['Production Megaboost']['Value']:.3f}%"
              f"{'<br>Unlocked at 250 total land ranks' if farming['LandRankTotalRanks'] < 250 else ''}",
        picture_class='production-megaboost',
        progression=farming['LandRankDatabase']['Production Megaboost']['Level'],
        goal=optimal_upgrades[1] if optimal_upgrades[1] >= 0 else ''
    ))
    value_advices[mgb].append(Advice(
        label=f"Production Superboost: +{farming['LandRankDatabase']['Production Superboost']['Value']:.3f}%"
              f"{'<br>Unlocked at 1750 total land ranks' if farming['LandRankTotalRanks'] < 1750 else ''}",
        picture_class='production-superboost',
        progression=farming['LandRankDatabase']['Production Superboost']['Level'],
        goal=optimal_upgrades[2] if optimal_upgrades[2] >= 0 else ''
    ))

    #MGC
    min_lr = max(farming['LandRankMinPlot'], floor(0.8 * farming['LandRankMinPlot']))
    if farming['LandRankMinPlot'] < floor(0.8 * farming['LandRankMinPlot']):
        llr_note = '80% of Max'
    else:
        llr_note = 'Lowest'
    value_advices[mgc].append(Advice(
        label=f"{llr_note} Land Rank: {min_lr}",
        picture_class=getLandRankImage(min_lr),
    ))
    value_advices[mgc].append(Advice(
        label=f"Highest Land Rank: {farming['LandRankMaxPlot']}",
        picture_class=getLandRankImage(farming['LandRankMaxPlot']),
    ))
    value_advices[mgc].append(Advice(
        label=f"Production Boost: +{farming['LandRankDatabase']['Production Boost']['Value']:,.3f}% per land rank."
              f"<br>Total on Lowest: +{farming['LandRankDatabase']['Production Boost']['Value'] * farming['LandRankMinPlot']:.3f}%"
              f"<br>Total on Highest: +{farming['LandRankDatabase']['Production Boost']['Value'] * farming['LandRankMaxPlot']:.3f}%",
        picture_class='production-boost',
        progression=farming['LandRankDatabase']['Production Boost']['Level'],
        goal=optimal_upgrades[0] if optimal_upgrades[0] >= 0 else ''
    ))
    ballot_active = session_data.account.ballot['CurrentBuff'] == 29
    if ballot_active:
        ballot_status = "is Active"
    elif not ballot_active and session_data.account.ballot['CurrentBuff'] != "Unknown":
        ballot_status = "is Inactive"
    else:
        ballot_status = "status is not available in provided data"
    ballot_multi = ValueToMulti(session_data.account.ballot['Buffs'][29]['Value'])
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
        label=f"Total on Lowest ranked plot"
              f"<br>Note: 100x is a HARD cap. Going above is pointless.",
        picture_class='crop-scientist',
        progression=val['BeforeCapMin'],
        goal=maxFarmingValue
    ))
    if val['BeforeCapMin'] < maxFarmingValue:
        value_advices[final].append(Advice(
            label=f"Total on Highest ranked plot",
            picture_class='crop-scientist',
            progression=val['BeforeCapMax'],
            goal=maxFarmingValue
        ))
    value_advices[final].append(Advice(
        label=f"Lava hasn't implemented Night Market Value GMO 😭",
        picture_class='night-market',
        progression="Lava",
        goal="Pls"
    ))

    value_ag = AdviceGroup(
        tier='',
        pre_string="Informational- Sources of Crop Value",
        advices=value_advices,
        informational=True,
        completed=val['BeforeCapMin']>=maxFarmingValue
    )
    return value_ag

def getEvoChanceAdviceGroup(farming) -> AdviceGroup:
    #Create subgroup labels
    alch = f"Alchemy without Crop Chapter: {farming['Evo']['Alch Multi']:.3f}x"
    stamp = f"Stamps: {farming['Evo']['Stamp Multi']:.3f}x"
    meals = f"Meals: {farming['Evo']['Meals Multi']:.3f}x"
    farm = f"Markets: {farming['Evo']['Farm Multi']:.3g}x"
    lr = f"Land Ranks: {farming['Evo']['LR Multi']:,.3f}x"
    summon = f"Summoning: {farming['Evo']['Summon Multi']:,.3f}x"
    ss = f"Star Sign: {farming['Evo']['SS Multi']:.3f}x"
    misc = f"Misc: {farming['Evo']['Misc Multi']:.3f}x"
    total = f"Subtotal before Crop Chapter Bubble: {farming['Evo']['Subtotal Multi']:.3g}x"
    evo_advices = {
        total: [],
        alch: [],
        stamp: [],
        meals: [],
        farm: [],
        lr: [],
        summon: [],
        ss: [],
        misc: [],
    }
    #Add Advice lines
#Bubbles

    evo_advices[alch].append(Advice(
        label=f"Cropius Mapper: {farming['Evo']['Maps Opened']}/{maxCharacters * (len(session_data.account.enemy_maps[6])-1)} maps"
              f"<br>Total value: {farming['Evo']['Cropius Final Value']:.3f}%",
        picture_class='cropius-mapper',
        progression=session_data.account.alchemy_bubbles['Cropius Mapper']['Level'],
        goal=infinity_string,
        resource=session_data.account.alchemy_bubbles['Cropius Mapper']['Material']
    ))
    evo_advices[alch].append(Advice(
        label=f"Crop Chapter: {session_data.account.alchemy_bubbles['Crop Chapter']['BaseValue']:.3}% per 2k Tome Points above 5k",
        picture_class='crop-chapter',
        progression=session_data.account.alchemy_bubbles['Crop Chapter']['Level'],
        goal=infinity_string,
        resource=session_data.account.alchemy_bubbles['Crop Chapter']['Material']
    ))
#Vial
    evo_advices[alch].append(Advice(
        label="Lab: My 1st Chemistry Set: "
              f"{max(1, 2 * session_data.account.labBonuses['My 1st Chemistry Set']['Enabled'])}/2x",
        picture_class="my-1st-chemistry-set",
        progression=int(session_data.account.labBonuses['My 1st Chemistry Set']['Enabled']),
        goal=1
    ))
    evo_advices[alch].append(Advice(
        label=f"{{{{ Rift|#rift }}}}: Vial Mastery: {session_data.account.vialMasteryMulti:.2f}x",
        picture_class="vial-mastery",
        progression=f"{1 if session_data.account.rift['VialMastery'] else 0}",
        goal=1
    ))
    evo_advices[alch].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Flavorgil (Caulifish): {session_data.account.alchemy_vials['Flavorgil (Caulifish)']['Value']:.2f}%"
              f"<br>Total Value after multis: {farming['Evo']['Vial Value']:.2f}%",
        picture_class="caulifish",
        progression=session_data.account.alchemy_vials['Flavorgil (Caulifish)']['Level'],
        goal=max_VialLevel
    ))

#Stamp
    evo_advices[stamp].append(Advice(
        label=f"Lab: Certified Stamp Book: "
              f"{max(1, 2 * session_data.account.labBonuses['Certified Stamp Book']['Enabled'])}/2x",
        picture_class="certified-stamp-book",
        progression=int(session_data.account.labBonuses['Certified Stamp Book']['Enabled']),
        goal=1
    ))
    evo_advices[stamp].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Liqorice Rolle: "
              f"{max(1, 1.25 * session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained'])}/1.25x",
        picture_class=session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']),
        goal=1
    ))
    evo_advices[stamp].append(Advice(
        label=f"Crop Evo {{{{ Stamp|#stamps}}}}: {session_data.account.stamps['Crop Evo Stamp']['Value']:.0f}%"
              f"<br>Total Value after multis: {farming['Evo']['Stamp Value']:.2f}%",
        picture_class='crop-evo-stamp',
        progression=session_data.account.stamps['Crop Evo Stamp']['Level'],
        goal=stamp_maxes['Crop Evo Stamp'],
        resource=session_data.account.stamps['Crop Evo Stamp']['Material'],
    ))

#Meals
    evo_advices[meals].append(Advice(
        label=f"Meal: Bill Jack Pepper"
              f"<br>Total Value after multis: {session_data.account.meals['Bill Jack Pepper']['Value']:,.3f}%",
        picture_class="bill-jack-pepper",
        progression=session_data.account.meals['Bill Jack Pepper']['Level'],
        goal=maxMealLevel
    ))

    evo_advices[meals].append(Advice(
        label=f"Highest Summoning level: {max(session_data.account.all_skills['Summoning'], default=0)}"
              f"<br>Provides a {farming['Evo']['Nyan Stacks']}x multi to Nyanborgir",
        picture_class='summoning'
    ))
    evo_advices[meals].append(Advice(
        label=f"Meal: Nyanborgir"
              f"<br>Total Value after multis: {session_data.account.meals['Nyanborgir']['Value'] * farming['Evo']['Nyan Stacks']:,.3f}%",
        picture_class="nyanborgir",
        progression=session_data.account.meals['Nyanborgir']['Level'],
        goal=maxMealLevel
    ))

#Day Market
    evo_advices[farm].append(Advice(
        label=f"Day Market: Biology Boost: {farming['MarketUpgrades']['Biology Boost']['Value']:.0f}/"
              f"{farming['MarketUpgrades']['Biology Boost']['BonusPerLevel'] * farming['MarketUpgrades']['Biology Boost']['MaxLevel']}%",
        picture_class="day-market",
        progression=farming['MarketUpgrades']['Biology Boost']['Level'],
        goal=farming['MarketUpgrades']['Biology Boost']['MaxLevel']
    ))

#Night Market
    evo_advices[farm].append(Advice(
        label=f"Night Market: Super Gmo: {farming['MarketUpgrades']['Super Gmo']['Value']:.0f}/"
              f"{farming['MarketUpgrades']['Super Gmo']['BonusPerLevel'] * farming['MarketUpgrades']['Super Gmo']['MaxLevel']}%"
              f"<br>{farming['CropStacks']['Super Gmo']} stacks = {farming['MarketUpgrades']['Super Gmo']['StackedValue']}x",
        picture_class="night-market",
        progression=farming['MarketUpgrades']['Super Gmo']['Level'],
        goal=farming['MarketUpgrades']['Super Gmo']['MaxLevel']
    ))
    evo_advices[farm].append(Advice(
        label=f"Night Market: Evolution Gmo: {farming['MarketUpgrades']['Evolution Gmo']['Value']:.0f}/"
              f"{farming['MarketUpgrades']['Evolution Gmo']['BonusPerLevel'] * farming['MarketUpgrades']['Evolution Gmo']['MaxLevel']}%"
              f"<br>{farming['CropStacks']['Evolution Gmo']} stacks = {farming['MarketUpgrades']['Evolution Gmo']['StackedValue']:.3g}x",
        picture_class="night-market",
        progression=farming['MarketUpgrades']['Evolution Gmo']['Level'],
        goal=farming['MarketUpgrades']['Evolution Gmo']['MaxLevel']
    ))

#LAND RANKS
    evo_advices[lr].append(Advice(
        label=f"Lowest Land Rank: {farming['LandRankMinPlot']}",
        picture_class=getLandRankImage(farming['LandRankMinPlot']),
    ))
    evo_advices[lr].append(Advice(
        label=f"Highest Land Rank: {farming['LandRankMaxPlot']}",
        picture_class=getLandRankImage(farming['LandRankMaxPlot']),
    ))
    evo_advices[lr].append(Advice(
        label=f"Evolution Boost: +{farming['LandRankDatabase']['Evolution Boost']['Value']:.3f}% per land rank."
              f"<br>Total on Lowest: +{farming['LandRankDatabase']['Evolution Boost']['Value'] * farming['LandRankMinPlot']:,.3f}%"
              f"<br>Total on Highest: +{farming['LandRankDatabase']['Evolution Boost']['Value'] * farming['LandRankMaxPlot']:,.3f}%",
        picture_class='evolution-boost',
        progression=farming['LandRankDatabase']['Evolution Boost']['Level']
    ))
    evo_advices[lr].append(Advice(
        label=f"Evolution Megaboost: +{farming['LandRankDatabase']['Evolution Megaboost']['Value']:,.3f}%",
        picture_class='evolution-megaboost',
        progression=farming['LandRankDatabase']['Evolution Megaboost']['Level']
    ))
    evo_advices[lr].append(Advice(
        label=f"Evolution Superboost: +{farming['LandRankDatabase']['Evolution Superboost']['Value']:,.3f}%",
        picture_class='evolution-superboost',
        progression=farming['LandRankDatabase']['Evolution Superboost']['Level']
    ))
    evo_advices[lr].append(Advice(
        label=f"Evolution Ultraboost: +{farming['LandRankDatabase']['Evolution Ultraboost']['Value']:,.3f}%",
        picture_class='evolution-ultraboost',
        progression=farming['LandRankDatabase']['Evolution Ultraboost']['Level']
    ))

#SUMMONING
    #Battles
    for color, battlesList in farming['Evo']['Summ Battles'].items():
        for battle in battlesList:
            beat = session_data.account.summoning['Battles'][color] >= battle
            evo_advices[summon].append(Advice(
                label=f"Summoning match {color}{battle}: "
                      f"{beat * session_data.account.summoning['BattleDetails'][color][battle]['RewardBaseValue']}"
                      f"/{session_data.account.summoning['BattleDetails'][color][battle]['RewardBaseValue']}"
                      f"{'.<br>Not yet beaten.' if not beat else ''}",
                picture_class=session_data.account.summoning["BattleDetails"][color][battle]['Image'],
                progression=int(session_data.account.summoning['Battles'][color] >= battle),
                goal=1
            ))

    #Winner Bonus Increases
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        evo_advices[summon].append(advice)

#Star Sign
    evo_advices[ss].append(session_data.account.star_sign_extras['SeraphAdvice'])
    evo_advices[ss].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    evo_advices[ss].append(Advice(
        label=f"Highest Farming level: {max(session_data.account.all_skills['Farming'], default=0)}",
        picture_class='farming'
    ))

    evo_advices[ss].append(Advice(
        label=f"{{{{ Starsign|#star-signs }}}}: Cropiovo Minor: {3 * session_data.account.star_signs['Cropiovo Minor']['Unlocked']:.0f}/3% per farming level."
              f"<br>Total Value if doubled: {farming['Evo']['Starsign Final Value']:,.3f}%",
        picture_class='cropiovo-minor',
        progression=int(session_data.account.star_signs['Cropiovo Minor']['Unlocked']),
        goal=1
    ))

# MISC
    # Achievement
    evo_advices[misc].append(Advice(
        label=f"""W6 Achievement: Lil' Overgrowth: {1.05 * session_data.account.achievements["Lil' Overgrowth"]['Complete']:.2f}/1.05x""",
        picture_class='lil-overgrowth',
        progression=int(session_data.account.achievements["Lil' Overgrowth"]['Complete']),
        goal=1
    ))
    #Killroy
    evo_advices[misc].append(Advice(
        label=f"Killroy Skull Shop: {session_data.account.killroy_skullshop['Crop Multi']:.3f}x"
              f"<br>1 purchase: +{session_data.account.killroy_skullshop['Crop Multi Plus 1'] - session_data.account.killroy_skullshop['Crop Multi']:.3f}x",
        picture_class='killroy-crop-evolution',
        progression=session_data.account.killroy_skullshop['Crop Purchases'],
    ))
    #Skill Mastery
    # Verify Skill Mastery itself is unlocked from The Rift
    evo_advices[misc].append(Advice(
        label="{{ Rift|#rift }} 16: Skill Mastery unlocked",
        picture_class='skill-mastery',
        progression=int(session_data.account.rift['SkillMastery']),
        goal=1
    ))
    # Account-wide total farming levels of 200 needed to unlock the bonus
    evo_advices[misc].append(Advice(
        label=f"Skill Mastery at 200 Farming: +{1.15 * farming['Evo']['Skill Mastery Bonus Bool'] * session_data.account.rift['SkillMastery']}/1.15x",
        picture_class='farming',
        progression=farming['Evo']['Total Farming Levels'],
        goal=200
    ))

    evo_advices[misc].append(Advice(
        label=f"Weekly Ballot: {farming['Evo']['Ballot Multi Current']:.3f}/{farming['Evo']['Ballot Multi Max']:.3f}x"
              f"<br>(Buff {farming['Evo']['Ballot Status']})",
        picture_class='ballot-29',
        progression=int(farming['Evo']['Ballot Active']),
        goal=1
    ))

#Total
    final_crops = {}
    for k, v in {
        1: 21,
        2: 46,
        3: 61,
        4: 84,
        5: 107,
        6: 120,
        7: 130,
        8: 140,
        9: 150,
        10:160
    }.items():
        final_crops[k] = [cropDict[v]['SeedName'],  ceil(1 / getCropEvoChance(v)),  cropDict[v]['Image']]
    subtotal_purple_glassy_percent = farming['Evo']['Subtotal Multi'] / final_crops[max(final_crops.keys())][1]
    purple_glassy_completed = subtotal_purple_glassy_percent >= 1
    first_failed_goal = 0
    first_failed_key = 0
    if purple_glassy_completed:
        first_failed_goal = final_crops[max(final_crops.keys())][1]
        first_failed_key = max(final_crops.keys())
        prog_percent = farming['Evo']['Subtotal Multi'] / final_crops[first_failed_key][1]
        evo_advices[total].append(Advice(
            label=f"Final {final_crops[first_failed_key][0]} chance"
                  f"<br>{first_failed_goal:.3g} for 100% chance",
            picture_class=final_crops[first_failed_key][2],
            progression=f"{min(1, prog_percent):.2%}",
            #goal=f"{first_failed_goal:.3g}"
        ))
    else:
        #Find the first crop with a failed requirement
        for k, v in final_crops.items():
            if farming['Evo']['Subtotal Multi'] < v[1]:
                first_failed_key = k
                first_failed_goal = v[1]
                prog_percent = farming['Evo']['Subtotal Multi'] / final_crops[first_failed_key][1]
                evo_advices[total].append(Advice(
                    label=f"Final {v[0]} chance with 0 stacks of Crop Chapter"
                          f"<br>{first_failed_goal:.3g} for 100% chance",
                    picture_class=v[2],
                    progression=f"{min(1, prog_percent):.3%}",
                    #goal=f"{v[1]:.3g}"
                ))
                break
        #Show chance including Crop Chapter for 50%, 25%, and 10% tome
        tome_added = 0
        for threshold, points in tomepct.items():
            crop_chapter_stacks = max(1, (points - 5000)//2000)
            crop_chapter_multi = ValueToMulti(session_data.account.alchemy_bubbles['Crop Chapter']['BaseValue'] * crop_chapter_stacks)
            total_multi = farming['Evo']['Subtotal Multi'] * crop_chapter_multi
            prog_percent = min(1, total_multi / first_failed_goal)
            completed = prog_percent >= 1 or purple_glassy_completed
            if not completed and (
                (tome_added < 3 and first_failed_key <= 6)
                or (tome_added < 5 and first_failed_key >= 7)
            ) and crop_chapter_multi > 1:
                evo_advices[total].append(Advice(
                    label=f"{threshold}% tome = {crop_chapter_stacks} stacks"
                          f"<br>Bubble Multi: {crop_chapter_multi:.3f}x"
                          f"<br>Grand Total: {total_multi:.3g}",
                    picture_class='blue-tome-pages',
                    progression=f"{prog_percent:.2%}",
                    #goal=f"{first_failed_goal:.3g}"
                ))
                tome_added += 1

    for category in evo_advices.values():
        for advice in category:
            mark_advice_completed(advice)

    evo_ag = AdviceGroup(
        tier='',
        pre_string="Informational- Sources of Crop Evolution Chance",
        advices=evo_advices,
        informational=True,
        completed=session_data.account.farming['CropsUnlocked'] >= maxFarmingCrops
    )
    return evo_ag

def getSpeedAdviceGroup(farming) -> AdviceGroup:
    # Create subgroup labels
    total = f"Total: {farming['Speed']['Total Multi']:,.3f}x"
    summon = f"Summoning: {farming['Speed']['Summon Multi']:,.3f}x"
    vm = f"Vial + Day Market: {farming['Speed']['VM Multi']:,.3f}x"
    nm = f"Night Market: {farming['Speed']['NM Multi']:,.3f}x"
    speed_advices = {
        total: [],
        summon: [],
        vm: [],
        nm: [],
    }
#Advices
#Total
    speed_advices[total].append(Advice(
        label=f"Farming Speed Multi: {farming['Speed']['Total Multi']:,.3f}x",
        picture_class='crop-scientist'
    ))
#Summoning
    #Battles
    for color, battlesList in farming['Speed']['Summ Battles'].items():
        for battle in battlesList:
            beat = session_data.account.summoning['Battles'][color] >= battle
            speed_advices[summon].append(Advice(
                label=f"Summoning match {color}{battle}: "
                      f"{beat * session_data.account.summoning['BattleDetails'][color][battle]['RewardBaseValue']}"
                      f"/{session_data.account.summoning['BattleDetails'][color][battle]['RewardBaseValue']}"
                      f"{'.<br>Not yet beaten.' if not beat else ''}",
                picture_class=session_data.account.summoning["BattleDetails"][color][battle]['Image'],
                progression=int(session_data.account.summoning['Battles'][color] >= battle),
                goal=1
            ))
    # Winner Bonus Increases
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        speed_advices[summon].append(advice)

#Vial and Market
    # Vial
    speed_advices[vm].append(Advice(
        label="Lab: My 1st Chemistry Set: "
              f"{max(1, 2 * session_data.account.labBonuses['My 1st Chemistry Set']['Enabled'])}/2x",
        picture_class="my-1st-chemistry-set",
        progression=int(session_data.account.labBonuses['My 1st Chemistry Set']['Enabled']),
        goal=1
    ))
    speed_advices[vm].append(Advice(
        label=f"{{{{ Rift|#rift }}}}: Vial Mastery: {session_data.account.vialMasteryMulti:.2f}x",
        picture_class="vial-mastery",
        progression=f"{1 if session_data.account.rift['VialMastery'] else 0}",
        goal=1
    ))
    speed_advices[vm].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Ricecakorade (Rice Cake): {session_data.account.alchemy_vials['Ricecakorade (Rice Cake)']['Value']:.2f}%"
              f"<br>Total Value after multis: {farming['Speed']['Vial Value']:.2f}%",
        picture_class="rice-cake",
        progression=session_data.account.alchemy_vials['Ricecakorade (Rice Cake)']['Level'],
        goal=max_VialLevel
    ))
    # Day Market
    speed_advices[vm].append(Advice(
        label=f"Day Market: Nutritious Soil: {farming['MarketUpgrades']['Nutritious Soil']['Value']:.0f}/"
              f"{farming['MarketUpgrades']['Nutritious Soil']['BonusPerLevel'] * farming['MarketUpgrades']['Biology Boost']['MaxLevel']}%",
        picture_class="day-market",
        progression=farming['MarketUpgrades']['Nutritious Soil']['Level'],
        goal=farming['MarketUpgrades']['Nutritious Soil']['MaxLevel']
    ))
#Night Market
    speed_advices[nm].append(Advice(
        label=f"Night Market: Super Gmo: {farming['MarketUpgrades']['Super Gmo']['Value']:.0f}/"
              f"{farming['MarketUpgrades']['Super Gmo']['BonusPerLevel'] * farming['MarketUpgrades']['Super Gmo']['MaxLevel']}%"
              f"<br>{farming['CropStacks']['Super Gmo']} stacks = {farming['MarketUpgrades']['Super Gmo']['StackedValue']}x",
        picture_class="night-market",
        progression=farming['MarketUpgrades']['Super Gmo']['Level'],
        goal=farming['MarketUpgrades']['Super Gmo']['MaxLevel']
    ))
    speed_advices[nm].append(Advice(
        label=f"Night Market: Speed Gmo: {farming['MarketUpgrades']['Speed Gmo']['Value']:.0f}/"
              f"{farming['MarketUpgrades']['Evolution Gmo']['BonusPerLevel'] * farming['MarketUpgrades']['Speed Gmo']['MaxLevel']}%"
              f"<br>{farming['CropStacks']['Speed Gmo']} stacks = {farming['MarketUpgrades']['Speed Gmo']['StackedValue']:.4g}x",
        picture_class="night-market",
        progression=farming['MarketUpgrades']['Speed Gmo']['Level'],
        goal=farming['MarketUpgrades']['Speed Gmo']['MaxLevel']
    ))

    for category in speed_advices.values():
        for advice in category:
            mark_advice_completed(advice)

    speed_ag = AdviceGroup(
        tier='',
        pre_string="Informational- Sources of Farming Speed",
        advices=speed_advices,
        informational=True
    )
    return speed_ag

def getBeanMultiAdviceGroup(farming) -> AdviceGroup:
    # Create subgroup labels
    total = f"Total: {farming['Bean']['Total Multi']:.2f}x"
    mga = f"Day Market: {farming['Bean']['mga']:.2f}x"
    mgb = f"Emporium + Achievement: {farming['Bean']['mgb']:.2f}x"
    bm_advices = {
        total: [],
        mga: [],
        mgb: []
    }

    #Total
    bm_advices[total].append(Advice(
        label=f"Magic Beans Bonus: {farming['Bean']['Total Multi']:,.3f}x",
        picture_class='crop-scientist'
    ))

    #Day Market - More Beenz
    bm_advices[mga].append(Advice(
        label=f"More Beenz: +{farming['MarketUpgrades']['More Beenz']['Value']:.0f}%",
        picture_class='day-market',
        progression=f"{farming['MarketUpgrades']['More Beenz']['Level']:.0f}",
        goal=f"{farming['MarketUpgrades']['More Beenz']['MaxLevel']:.0f}",
    ))
    #Emporium - Deal Sweetening
    bm_advices[mgb].append(Advice(
        label=f"{{{{ Jade Emporium|#sneaking }}}}: Deal Sweetening: "
              f"+{25 * session_data.account.sneaking['JadeEmporium']['Deal Sweetening']['Obtained']}/25%",
        picture_class='deal-sweetening',
        progression=int(session_data.account.sneaking['JadeEmporium']['Deal Sweetening']['Obtained']),
        goal=1
    ))
    #Achievement - Crop Flooding
    bm_advices[mgb].append(Advice(
        label=f"W6 Achievement: Crop Flooding: "
              f"+{5 * session_data.account.achievements['Crop Flooding']['Complete']}/5%",
        picture_class='crop-flooding',
        progression=int(session_data.account.achievements['Crop Flooding']['Complete']),
        goal=1
    ))

    for category in bm_advices.values():
        for advice in category:
            mark_advice_completed(advice)

    bm_ag = AdviceGroup(
        tier='',
        pre_string='Informational- Sources of Magic Bean Bonus',
        advices=bm_advices,
        informational=True
    )
    return bm_ag

def getOGAdviceGroup(farming):
    # Create subgroup labels
    total = f"Total: {farming['OG']['Total Multi']:,.3f}x"
    nm = f"Night Market: {farming['OG']['NM Multi']:.3f}x"
    lr = f"Land Rank Total: {farming['OG']['LR Multi']:,.3f}x"
    ss = f"Star Sign: {farming['OG']['SS Multi']:.2f}x"
    ach = f"Achievement: {farming['OG']['Ach Multi']:.2f}x"
    merit = f"Merit: {farming['OG']['Merit Multi']:.2f}x"
    pristine = f"Pristine Charm: {farming['OG']['Pristine Multi']:.2f}x"

    og_advices = {
        total: [],
        nm: [],
        lr: [],
        ss: [],
        ach: [],
        merit: [],
        pristine: [],
    }
#Total
    og_advices[total].append(Advice(
        label=f"Overgrowth Chance: {farming['OG']['Total Multi']:,.3f}x",
        picture_class='crop-scientist'
    ))
#Achievement- Big Time Land Owner = 1.15x
    og_advices[ach].append(Advice(
        label=f"W6 Achievement: Big Time Land Owner: "
              f"{ValueToMulti(15 * session_data.account.achievements['Big Time Land Owner']['Complete']):.2f}/1.15x",
        picture_class='big-time-land-owner',
        progression=int(session_data.account.achievements['Big Time Land Owner']['Complete']),
        goal=1
    ))
#Star Sign
    og_advices[ss].append(session_data.account.star_sign_extras['SeraphAdvice'])
    og_advices[ss].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    og_advices[ss].append(Advice(
        label=f"{{{{ Starsign|#star-signs }}}}: O.G. Signalais: {15 * session_data.account.star_signs['O.G. Signalais']['Unlocked']:.0f}/15%."
              f"<br>Total Value if doubled: {farming['OG']['Starsign Final Value']:.3f}%",
        picture_class='og-signalais',
        progression=int(session_data.account.star_signs['O.G. Signalais']['Unlocked']),
        goal=1
    ))
#Night Market
    og_advices[nm].append(Advice(
        label=f"Night Market: OG Fertilizer: {farming['MarketUpgrades']['Og Fertilizer']['Value']:.0f}/"
              f"{farming['MarketUpgrades']['Og Fertilizer']['BonusPerLevel'] * farming['MarketUpgrades']['Og Fertilizer']['MaxLevel']}%",
        picture_class="night-market",
        progression=farming['MarketUpgrades']['Og Fertilizer']['Level'],
        goal=farming['MarketUpgrades']['Og Fertilizer']['MaxLevel']
    ))
#Merit
    og_advices[merit].append(Advice(
        label=f"W6 Taskboard Merit: +{2 * session_data.account.merits[5][2]['Level']}/30%",
        picture_class='merit-5-2',
        progression=session_data.account.merits[5][2]['Level'],
        goal=15
    ))
#Land Rank
    og_advices[lr].append(Advice(
        label=f"Overgrowth Boost: +{farming['LandRankDatabase']['Overgrowth Boost']['Value']:,.3f}%",
        picture_class='overgrowth-boost',
        progression=farming['LandRankDatabase']['Overgrowth Boost']['Level']
    ))
    og_advices[lr].append(Advice(
        label=f"Overgrowth Megaboost: +{farming['LandRankDatabase']['Overgrowth Megaboost']['Value']:,.3f}%",
        picture_class='overgrowth-megaboost',
        progression=farming['LandRankDatabase']['Overgrowth Megaboost']['Level']
    ))
    og_advices[lr].append(Advice(
        label=f"Overgrowth Superboost: +{farming['LandRankDatabase']['Overgrowth Superboost']['Value']:,.3f}%",
        picture_class='overgrowth-superboost',
        progression=farming['LandRankDatabase']['Overgrowth Superboost']['Level']
    ))

#Pristine Charm
    og_advices[pristine].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Taffy Disc: "
              f"{ValueToMulti(50 * session_data.account.sneaking['PristineCharms']['Taffy Disc']['Obtained']):.2f}/1.50x",
        picture_class=session_data.account.sneaking['PristineCharms']['Taffy Disc']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Taffy Disc']['Obtained']),
        goal=1
    ))

    for category in og_advices.values():
        for advice in category:
            mark_advice_completed(advice)

    og_ag = AdviceGroup(
        tier='',
        pre_string='Informational- Sources of Overgrowth',
        advices=og_advices,
        informational=True
    )
    return og_ag

def getLRExclusions(farming, highestFarmingSkillLevel):
    exclusions = []
    if maxFarmingCrops-1 in farming['Crops']:
        exclusions.extend([v['Name'] for v in landrankDict.values() if v['Name'].startswith('Evolution')])
    if farming['Value']['FinalMin'] >= 100:
        exclusions.extend([v['Name'] for v in landrankDict.values() if v['Name'].startswith('Production')])
    if farming['LandRankMinPlot'] >= 100:
        exclusions.extend([v['Name'] for v in landrankDict.values() if v['Name'].startswith('Soil Exp')])
    if highestFarmingSkillLevel >= 300:
        exclusions.extend([v['Name'] for v in landrankDict.values() if v['Name'].startswith('Farmtastic')])
    #logger.debug(f"Land Rank Exclusions: {exclusions}")
    return exclusions

def getProgressionTiersAdviceGroup(farming, highestFarmingSkillLevel):
    farming_AdviceDict = {
        'Tiers': {},
    }
    farming_AdviceGroupDict = {}
    infoTiers = 0
    max_tier = max(farming_progressionTiers.keys(), default=0) - infoTiers
    tier_All = 0

    multis = ['Evolution Gmo', 'Og Fertilizer']
    one_point_landranks = ['Seed of Stealth', 'Seed of Loot', 'Seed of Damage', 'Seed of Stats']
    lr_exclusions = getLRExclusions(farming, highestFarmingSkillLevel)

    #Assess Tiers
    for tierNumber, tierRequirements in farming_progressionTiers.items():
        #subgroupName = f"TESTING PURPOSES ONLY, TIERS NOT READY!"
        subgroupName = f"To reach Tier {tierNumber}"
        advice_types_added = set()

        #Farming Level
        if highestFarmingSkillLevel < tierRequirements.get('Farming Level', 0):
            if subgroupName not in farming_AdviceDict['Tiers'] and len(farming_AdviceDict['Tiers']) < maxTiersPerGroup:
                farming_AdviceDict['Tiers'][subgroupName] = []
            if subgroupName in farming_AdviceDict['Tiers']:
                advice_types_added.add('Farming Level')
                farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                    label=f"Raise Farming skill level",
                    picture_class='farming',
                    progression=highestFarmingSkillLevel,
                    goal=tierRequirements.get('Farming Level', 0)
                ))

        # Unlock Crops
        if farming['CropsUnlocked'] < tierRequirements.get('Crops Unlocked', 0):
            if subgroupName not in farming_AdviceDict['Tiers'] and len(farming_AdviceDict['Tiers']) < maxTiersPerGroup:
                farming_AdviceDict['Tiers'][subgroupName] = []
            if subgroupName in farming_AdviceDict['Tiers']:
                advice_types_added.add('Crops Unlocked')
                shortby = tierRequirements.get('Crops Unlocked', 0) - farming['CropsUnlocked']
                farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                    label=f"Unlock {shortby} more crop type{pl(shortby)}",
                    picture_class='crop-depot',
                    progression=farming['CropsUnlocked'],
                    goal=tierRequirements.get('Crops Unlocked', 0)
                ))

        #Day Market
        for rName, rLevel in tierRequirements.get('Day Market', {}).items():
            if farming['MarketUpgrades'][rName]['Level'] < rLevel:
                if subgroupName not in farming_AdviceDict['Tiers'] and len(farming_AdviceDict['Tiers']) < maxTiersPerGroup:
                    farming_AdviceDict['Tiers'][subgroupName] = []
                if subgroupName in farming_AdviceDict['Tiers']:
                    advice_types_added.add('Day Market')
                    farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                        label=f"{rName}: "
                              f"{farming['MarketUpgrades'][rName]['Value']:.4g}/{farming['MarketUpgrades'][rName]['BonusPerLevel'] * rLevel:.4g}"
                              f"{'%' if rName != 'Land Plots' else ''}",
                        picture_class='day-market',
                        progression=farming['MarketUpgrades'][rName]['Level'],
                        goal=rLevel
                    ))

        # Land Ranks - Database Upgrades
        lr_this_tier = []
        for setNumber, setRequirements in tierRequirements.get('Land Ranks', {}).items():
            for rName, rLevel in setRequirements.items():
                if farming['LandRankDatabase'][rName]['Level'] < rLevel and rName not in lr_exclusions:
                    if subgroupName not in farming_AdviceDict['Tiers'] and len(farming_AdviceDict['Tiers']) < maxTiersPerGroup:
                        farming_AdviceDict['Tiers'][subgroupName] = []
                    if subgroupName in farming_AdviceDict['Tiers']:
                        if rName in one_point_landranks:
                            current = farming['LandRankDatabase'][rName]['Value']
                            target = farming['LandRankDatabase'][rName]['BaseValue']
                        else:
                            current = farming['LandRankDatabase'][rName]['Value']
                            target = (1.7 * farming['LandRankDatabase'][rName]['BaseValue'] * rLevel) / (rLevel + 80)
                        lr_this_tier.append([rName, rLevel, current, target])
                        # farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                        #     label=f"{rName}: {current:.4g}/{target:.4g}%",
                        #     picture_class=rName,
                        #     progression=farming['LandRankDatabase'][rName]['Level'],
                        #     goal=rLevel
                        # ))

        for lrIndex, lrAdvice in enumerate(lr_this_tier):
            if lrIndex+1 < len(lr_this_tier):
                safe_to_add = lr_this_tier[lrIndex][0] != lr_this_tier[lrIndex+1][0]
                if safe_to_add:
                    farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                        label=f"{lrAdvice[0]}: {lrAdvice[2]:.4g}/{lrAdvice[3]:.4g}%",
                        picture_class=lrAdvice[0],
                        progression=farming['LandRankDatabase'][lrAdvice[0]]['Level'],
                        goal=lrAdvice[1]
                    ))
            else:
                farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                    label=f"{lrAdvice[0]}: {lrAdvice[2]:.4g}/{lrAdvice[3]:.4g}%",
                    picture_class=lrAdvice[0],
                    progression=farming['LandRankDatabase'][lrAdvice[0]]['Level'],
                    goal=lrAdvice[1]
                ))

        # Suggestions
        if subgroupName in farming_AdviceDict['Tiers']:
            if tierRequirements.get('Suggestions', {}):
                suggies = tierRequirements['Suggestions']
                if 'Speed' in suggies:
                    if farming['Speed']['Total Multi'] < suggies['Speed'][1]:
                        farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                            label=f"Suggestion: {suggies['Speed'][0]} to {suggies['Speed'][1]}x Speed",
                            picture_class='crop-scientist',
                            progression=f"{farming['Speed']['Total Multi']:.2f}" if farming['Speed']['Total Multi'] < 10 else f"{farming['Speed']['Total Multi']:.0f}",
                            goal=f"{suggies['Speed'][1]}"
                        ))
                if 'OG' in suggies:
                    if farming['OG']['Total Multi'] < suggies['OG'][1]:
                        farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                            label=f"Suggestion: {suggies['OG'][0]} to {suggies['OG'][1]}x Overgrowth",
                            picture_class='crop-scientist',
                            progression=f"{farming['OG']['Total Multi']:.2f}" if farming['OG']['Total Multi'] < 10 else f"{farming['OG']['Total Multi']:.0f}",
                            goal=f"{suggies['OG'][1]}"
                        ))
                if 'Crops Unlocked' in advice_types_added:
                    if 'EvoChance' in suggies:
                        if farming['Evo']['Subtotal Multi'] < suggies['EvoChance'][1]:
                            low_target = notateNumber(
                                'Basic',
                                suggies['EvoChance'][0],
                                2 if suggies['EvoChance'][0] < 10 else 0
                            )
                            target = notateNumber(
                                'Basic',
                                suggies['EvoChance'][1],
                                2 if suggies['EvoChance'][1] < 10 else 0
                            )
                            match_letter = target[-1] if target[-1].isalpha() else ''
                            farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                                label=f"Suggestion: {low_target} to {target}x Evo Chance",
                                picture_class='crop-scientist',
                                progression=notateNumber(
                                    'Match',
                                    farming['Evo']['Subtotal Multi'],
                                    2 if farming['Evo']['Subtotal Multi'] < 10 else 0,
                                    match_letter
                                ),
                                goal=target
                            ))
                    if 'CropIndex' in suggies:
                        for cropIndex in suggies['CropIndex']:
                            if cropIndex-1 not in farming['Crops']:
                                crop = cropDict.get(cropIndex, {'Name': f"UnknownCrop{cropIndex}", 'Image': '', 'SeedName': 'UnknownSeed', 'SeedCropIndex': 0})
                                farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                                    label=f"Suggestion: {crop['Name']} ({crop['SeedName']} #{crop['SeedCropIndex']})",
                                    picture_class=crop['Image'],
                                    progression=farming['CropCountsPerSeed'][crop['SeedName'] if not crop['SeedName'].endswith('Glassy') else 'Glassy'],
                                    goal=crop['SeedCropIndex']
                                ))
                if 'No Trade' in suggies:
                    farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                        label=suggies['No Trade'],
                        picture_class='crop-transfer-ticket',
                        progression="❌",
                        goal="❌",
                    ))

        #Night Market
        total_magic_bean_cost = 0
        total_nm_entries = 0
        for rName, rLevel in tierRequirements.get('Night Market', {}).items():
            if farming['MarketUpgrades'][rName]['Level'] < rLevel:
                if subgroupName not in farming_AdviceDict['Tiers'] and len(farming_AdviceDict['Tiers']) < maxTiersPerGroup:
                    farming_AdviceDict['Tiers'][subgroupName] = []
                if subgroupName in farming_AdviceDict['Tiers']:
                    if rName in multis:
                        current = ValueToMulti(farming['MarketUpgrades'][rName]['Value'])
                        target = ValueToMulti(farming['MarketUpgrades'][rName]['BonusPerLevel'] * rLevel)
                    else:
                        current = farming['MarketUpgrades'][rName]['Value']
                        target = farming['MarketUpgrades'][rName]['BonusPerLevel'] * rLevel
                    upgrade_cost = getNMCost(rName, farming['MarketUpgrades'][rName]['Level'], rLevel)
                    farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                        label=f"{rName}: "
                              f"{current:.4g}/{target:.4g}"
                              f"{'x' if rName in multis else '%' if rName != 'Overgrowth' and rName != 'Land Rank' else ''}"
                              f"<br>Total Magic Bean cost: {upgrade_cost:,}",
                        picture_class='night-market',
                        progression=farming['MarketUpgrades'][rName]['Level'],
                        goal=rLevel,
                        resource='magic-bean'
                    ))
                    total_magic_bean_cost += upgrade_cost
                    total_nm_entries += 1
        if total_nm_entries > 1:
            target = notateNumber('Basic', total_magic_bean_cost, 2)
            match_letter = str(target[-1]) if target[-1].isalpha() else ''
            farming_AdviceDict['Tiers'][subgroupName].append(Advice(
                label=f"Grand Total Magic Bean Cost remaining in this Tier",
                picture_class='magic-bean',
                progression=f"{notateNumber('Match', farming['MagicBeans'], 2, match_letter)}",  #Does not include the value of their current trade
                goal=target,
                resource='magic-bean'
            ))

        #Final tier check
        if subgroupName not in farming_AdviceDict['Tiers'] and tier_All == tierNumber - 1:
            tier_All = tierNumber

    #Generate AdviceGroups
    farming_AdviceGroupDict['Tiers'] = AdviceGroup(
        tier=tier_All,
        pre_string="Continue farming",
        advices=farming_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + infoTiers, tier_All)
    return farming_AdviceGroupDict, overall_SectionTier, max_tier

def setFarmingProgressionTier():
    highestFarmingSkillLevel = max(session_data.account.all_skills["Farming"])
    if highestFarmingSkillLevel < 1:
        farming_AdviceSection = AdviceSection(
            name="Farming",
            tier="0",
            pinchy_rating=0,
            header="Come back after unlocking the Farming skill in W6!",
            picture="wiki/FarmCropBean.png",
            unreached=True
        )
        return farming_AdviceSection

    farming = session_data.account.farming

    #Generate AdviceGroups
    farming_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceGroup(farming, highestFarmingSkillLevel)
    farming_AdviceGroupDict['Evo'] = getEvoChanceAdviceGroup(farming)
    farming_AdviceGroupDict['Speed'] = getSpeedAdviceGroup(farming)
    if farming['MarketUpgrades']['Overgrowth']['Level'] >= 1:
        farming_AdviceGroupDict['OG'] = getOGAdviceGroup(farming)
    if farming['LandRankTotalRanks'] >= 1:
        farming_AdviceGroupDict['Value'] = getCropValueAdviceGroup(farming)
    if farming['Mama Trolls Unlocked']:
        farming_AdviceGroupDict['Bean'] = getBeanMultiAdviceGroup(farming)
    if session_data.account.sneaking['JadeEmporium']['Crop Depot Scientist']['Obtained']:
        farming_AdviceGroupDict['Depot'] = getCropDepotAdviceGroup(farming)
    farming_AdviceGroupDict['Day'] = getDayMarketAdviceGroup(farming)
    farming_AdviceGroupDict['Night'] = getNightMarketAdviceGroup(farming)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    farming_AdviceSection = AdviceSection(
        name="Farming",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Farming tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="wiki/FarmCropBean.png",
        groups=farming_AdviceGroupDict.values()
    )
    return farming_AdviceSection
