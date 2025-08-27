from math import ceil, floor

from models.models import AdviceSection, AdviceGroup, Advice
from utils.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger
from utils.data_formatting import mark_advice_completed
from flask import g as session_data
from consts.consts_autoreview import break_you_best, ValueToMulti, build_subgroup_label, EmojiType
from consts.consts_general import max_characters
from consts.consts_w6 import max_farming_crops, max_farming_value, landrank_dict, crop_dict, getCropEvoChance, getRequiredCropNumber
from consts.consts_w4 import max_meal_level
from consts.consts_w2 import max_vial_level
from consts.consts_w1 import stamp_maxes
from consts.progression_tiers import farming_progressionTiers, true_max_tiers
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
    lab_note = f"<br>Note: Defaulted ON. Sorry {EmojiType.FROWN.value}"

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
            label=f"{{{{ Grimoire|#the-grimoire}}}}: Superior Crop Research: "
                  f"{round(session_data.account.grimoire['Upgrades']['Superior Crop Research']['Total Value'], 2):g}/3x",
            picture_class=session_data.account.grimoire['Upgrades']['Superior Crop Research']['Image'],
            progression=session_data.account.grimoire['Upgrades']['Superior Crop Research']['Level'],
            goal=session_data.account.grimoire['Upgrades']['Superior Crop Research']['Max Level'],
        ),
        Advice(
            label=f"Total Crops Discovered: {farming['CropsUnlocked']}/{max_farming_crops}",
            picture_class='crop-depot',
            progression=farming['CropsUnlocked'],
            goal=max_farming_crops
        ),
    ]
    for bonusIndex, bonusDetails in farming['Depot'].items():
        if bonusDetails['ScalingType'] == 'pow':
            scaling_label = f"{bonusDetails['ScalingNumber']}x {bonusDetails['BonusString']} per crop discovered, multiplicative"
            if bonusDetails['ValuePlus1'] > bonusDetails['Value']:
                scaling_label += f".<br>Next crop would increase total by {bonusDetails['ValuePlus1'] - bonusDetails['Value']:,.3f}"
        else:
            scaling_label = (f"+{bonusDetails['ScalingNumber']}{'%' if bonusDetails['BonusString'] != 'Base Critters' else ''}"
                             f" {bonusDetails['BonusString']} per crop discovered, additive")

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
        pre_string='Crop Depot bonuses',
        advices=cd_advices,
        informational=True
    )

    return cd_ag

def getDayMarketAdviceGroup(farming) -> AdviceGroup:
    dm = {name:details for name, details in farming['MarketUpgrades'].items() if details['MarketType'] == 'Day'}
    dm_advices = [
        Advice(
            label=f"{name}: {details['Description']}" + (
                  f"<br>Next level's crop: "
                  f"{crop_dict.get(getRequiredCropNumber(name, min(details['MaxLevel'], details['Level'] + 1)), {}).get('Name', '')}"
                  if details['Level'] < details['MaxLevel'] else ''
            ),
            picture_class='day-market',
            progression=details['Level'],
            goal=details['MaxLevel'],
            resource=(
                crop_dict.get(getRequiredCropNumber(name, details['Level'] + 1), {}).get('Image', '')
                if details['Level'] < details['MaxLevel'] else ''
            )
        )
        for name, details in dm.items()]

    for advice in dm_advices:
        mark_advice_completed(advice)

    dm_ag = AdviceGroup(
        tier='',
        pre_string='Day Market upgrades',
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
        pre_string='Night Market upgrades',
        advices=nm_advices,
        informational=True
    )
    return nm_ag

def getNightMarketCost(name, first_level, last_level=0):
    cost_multi = (
        max(.001, session_data.account.emperor['Bonuses'][2]['Total Value'])
    )
    total_cost = 0
    upgrade = session_data.account.farming['MarketUpgrades'][name]
    if first_level > last_level:
        last_level = first_level-1
    for level in range(first_level, last_level):
        total_cost += floor(upgrade['BaseCost'] * pow(upgrade['CostIncrement'], level)) * cost_multi
    return floor(total_cost) if 1e8 > total_cost else total_cost

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
    while value < max_farming_value and sum(upgrades) < available_points:
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
    mgd = f"Multi Group D: {val['Value GMO Current']:.2f}x"
    final = (
        f"Conclusion: You are "
        f"{'NOT ' if val['FinalMin'] < max_farming_value else 'over' if val['BeforeCapMin'] >= max_farming_value * 1.25 else ''}"
        f"capped on Lowest plots")
    value_advices = {
        final: [],
        mga: [],
        mgb: [],
        mgc: [],
        mgd: [],
    }
    #MGA
    value_advices[mga].append(Advice(
        label=f"Highest full 100 Product Doubler reached for guarantee: "
              f"{(farming['MarketUpgrades']['Product Doubler']['Value'] // 100) * 100:.0f}%",
        picture_class='day-market',
        progression=f"{farming['MarketUpgrades']['Product Doubler']['Value']:.0f}",
        goal=400,
        unit='%'
    ))

    #MGB
    #optimal_upgrades = getValueLRSuggies(farming) if farming['LandRankTotalRanks'] >= 5 else [-1, -1, -1]
    value_advices[mgb].append(Advice(
        label=f"Production Megaboost: +{farming['LandRankDatabase']['Production Megaboost']['Value']:.3f}%"
              f"{'<br>Unlocked at 250 total land ranks' if farming['LandRankTotalRanks'] < 250 else ''}",
        picture_class='production-megaboost',
        progression=farming['LandRankDatabase']['Production Megaboost']['Level'],
        #goal=optimal_upgrades[1] if optimal_upgrades[1] >= 0 else ''
    ))
    value_advices[mgb].append(Advice(
        label=f"Production Superboost: +{farming['LandRankDatabase']['Production Superboost']['Value']:.3f}%"
              f"{'<br>Unlocked at 1750 total land ranks' if farming['LandRankTotalRanks'] < 1750 else ''}",
        picture_class='production-superboost',
        progression=farming['LandRankDatabase']['Production Superboost']['Level'],
        #goal=optimal_upgrades[2] if optimal_upgrades[2] >= 0 else ''
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
        #goal=optimal_upgrades[0] if optimal_upgrades[0] >= 0 else ''
    ))
    ballot_active = session_data.account.ballot['CurrentBuff'] == 29
    if ballot_active:
        ballot_status = "is Active"
    elif not ballot_active and session_data.account.ballot['CurrentBuff'] != 0:
        ballot_status = "is Inactive"
    else:
        ballot_status = "status is not available in provided data"
    ballot_multi = ValueToMulti(session_data.account.ballot['Buffs'][29]['Value'])
    ballot_multi_active = max(1, ballot_multi * ballot_active)
    value_advices[mgc].append(Advice(
        label=f"Plus Weekly {{{{ Ballot|#bonus-ballot }}}}: {ballot_multi_active:.3f}/{ballot_multi:.3f}x"
              f"<br>(Buff {ballot_status})",
        picture_class='ballot-29',
        progression=int(ballot_active),
        goal=1
    ))

    value_advices[mgd].append(Advice(
        label=f"Night Market Value GMO: {farming['MarketUpgrades']['Value Gmo']['Description']}",
        picture_class='night-market',
        progression=farming['MarketUpgrades']['Value Gmo']['Level'],
        goal=farming['MarketUpgrades']['Value Gmo']['MaxLevel']
    ))

    #Final
    value_advices[final].append(Advice(
        label=f"Total on Lowest ranked plot"
              f"<br>Note: 10,000x is a HARD cap.",
        picture_class='crop-scientist',
        progression=f"{val['BeforeCapMin']:,.0f}",
        goal=f"{max_farming_value:,}"
    ))
    if val['BeforeCapMin'] < max_farming_value:
        value_advices[final].append(Advice(
            label=f"Total on Highest ranked plot",
            picture_class='crop-scientist',
            progression=f"{val['BeforeCapMax']:,.0f}",
            goal=f"{max_farming_value:,}"
        ))

    value_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Crop Value',
        advices=value_advices,
        informational=True,
        completed=val['BeforeCapMin'] >= max_farming_value
    )
    return value_ag

def getEvoChanceAdviceGroup(farming, highest_farming_level) -> AdviceGroup:
    #Create subgroup labels
    alch = f"Alchemy: {farming['Evo']['Alch Multi']:.3f}x"
    stamp = f"Stamps: {farming['Evo']['Stamp Multi']:.3f}x"
    meals = f"Meals: {farming['Evo']['Meals Multi']:.3f}x"
    farm = f"Markets: {farming['Evo']['Farm Multi']:.3g}x"
    lr = f"Land Ranks: {farming['Evo']['LR Multi']:,.3f}x"
    summon = f"Summoning: {farming['Evo']['Summon Multi']:,.3f}x"
    ss = f"Star Sign: {farming['Evo']['SS Multi']:.3f}x"
    lamp = f"Lamp Wish: {farming['Evo']['Wish Multi']:.3f}x"
    misc = f"Misc: {farming['Evo']['Misc Multi']:.3f}x"
    total = f"Total Evo Chance: {farming['Evo']['Subtotal Multi']:.3g}x"
    evo_advices = {
        total: [],
        alch: [],
        stamp: [],
        meals: [],
        farm: [],
        lr: [],
        summon: [],
        ss: [],
        lamp: [],
        misc: [],
    }
    #Add Advice lines
#Bubbles

    evo_advices[alch].append(Advice(
        label=f"Cropius Mapper: {farming['Evo']['Maps Opened']}/{max_characters * (len(session_data.account.enemy_maps[6]) - 1)} maps"
              f"<br>Total value: {farming['Evo']['Cropius Final Value']:.3f}%",
        picture_class='cropius-mapper',
        progression=session_data.account.alchemy_bubbles['Cropius Mapper']['Level'],
        goal=EmojiType.INFINITY.value,
        resource=session_data.account.alchemy_bubbles['Cropius Mapper']['Material']
    ))
    crop_chapter_stacks = max(0, (session_data.account.tome['Total Points'] - 5000) // 2000)
    evo_advices[alch].append(Advice(
        label=f"Crop Chapter: {session_data.account.alchemy_bubbles['Crop Chapter']['BaseValue']:.3}% per 2k Tome Points above 5k"
              f"<br>{session_data.account.tome['Total Points']:,} Tome Points = {crop_chapter_stacks} stacks"
              f"<br>Total: +{round(session_data.account.alchemy_bubbles['Crop Chapter']['BaseValue'] * crop_chapter_stacks, 3):g}%",
        picture_class='crop-chapter',
        progression=session_data.account.alchemy_bubbles['Crop Chapter']['Level'],
        goal=EmojiType.INFINITY.value,
        resource=session_data.account.alchemy_bubbles['Crop Chapter']['Material']
    ))
#Vial
    evo_advices[alch].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Flavorgil (Caulifish): {session_data.account.alchemy_vials['Flavorgil (Caulifish)']['BaseValue']:.2f}%"
              f"<br>Total Value after multis: {farming['Evo']['Vial Value']:.2f}%",
        picture_class="caulifish",
        progression=session_data.account.alchemy_vials['Flavorgil (Caulifish)']['Level'],
        goal=max_vial_level
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
              f"<br>Total Value after multis: {session_data.account.stamps['Crop Evo Stamp']['Total Value']:.2f}%",
        picture_class='crop-evo-stamp',
        progression=session_data.account.stamps['Crop Evo Stamp']['Level'],
        goal=stamp_maxes['Crop Evo Stamp'],
        resource=session_data.account.stamps['Crop Evo Stamp']['Material'],
    ))

#Meals
    evo_advices[meals].append(Advice(
        label=f"{{{{ Meal|#cooking }}}}: Bill Jack Pepper: {session_data.account.meals['Bill Jack Pepper']['Description']}",
        picture_class=session_data.account.meals['Bill Jack Pepper']['Image'],
        progression=session_data.account.meals['Bill Jack Pepper']['Level'],
        goal=max_meal_level
    ))

    evo_advices[meals].append(Advice(
        label=f"Highest Summoning level: {max(session_data.account.all_skills['Summoning'], default=0)}"
              f"<br>Provides a {farming['Evo']['Nyan Stacks']}x multi to Nyanborgir",
        picture_class='summoning'
    ))
    evo_advices[meals].append(Advice(
        label=f"{{{{ Meal|#cooking }}}}: Nyanborgir: {session_data.account.meals['Nyanborgir']['Description']}"
              f"<br>After {farming['Evo']['Nyan Stacks']} Summoning Level stack{pl(farming['Evo']['Nyan Stacks'])}:"
              f" {session_data.account.meals['Nyanborgir']['Value'] * farming['Evo']['Nyan Stacks']:,.3f}%",
        picture_class=session_data.account.meals['Nyanborgir']['Image'],
        progression=session_data.account.meals['Nyanborgir']['Level'],
        goal=max_meal_level
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
    evo_advices[summon].extend(session_data.account.summoning['WinnerBonusesSummaryRest'])

#Star Sign
    evo_advices[ss].append(session_data.account.star_sign_extras['SeraphAdvice'])
    evo_advices[ss].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    evo_advices[ss].append(Advice(
        label=f"Highest Farming level: {highest_farming_level}",
        picture_class='farming'
    ))

    evo_advices[ss].append(Advice(
        label=f"{{{{ Starsign|#star-signs }}}}: Cropiovo Minor: {3 * session_data.account.star_signs['Cropiovo Minor']['Unlocked']:.0f}/3% per farming level."
              f"<br>Total Value if doubled: {farming['Evo']['Starsign Final Value']:,.3f}%",
        picture_class='cropiovo-minor',
        progression=int(session_data.account.star_signs['Cropiovo Minor']['Unlocked']),
        goal=1
    ))
# Lamp
    lamp_cavern = session_data.account.caverns['Caverns']['The Lamp']
    evo_advices[lamp].append(Advice(
        label=f"{{{{Lamp|#glowshroom-tunnels}}}} Wish: {lamp_cavern['WishTypes'][8]['Name']}: +{lamp_cavern['WishTypes'][8]['BonusList'][0]}%",
        picture_class=f"cavern-{lamp_cavern['CavernNumber']}",
        progression=lamp_cavern['WishTypes'][8]['BonusList'][0],
        goal=EmojiType.INFINITY.value
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
        10:160,
        11:170,
        12:180,
        13:190,
        14:200,
        15:210,
        16:220,
        17:230
    }.items():
        final_crops[k] = [crop_dict[v]['SeedName'], ceil(1 / getCropEvoChance(v)), crop_dict[v]['Image']]
    subtotal_final_glassy_percent = farming['Evo']['Subtotal Multi'] / final_crops[max(final_crops.keys())][1]
    final_glassy_completed = subtotal_final_glassy_percent >= 1
    if final_glassy_completed:
        first_failed_goal = final_crops[max(final_crops.keys())][1]
        first_failed_key = max(final_crops.keys())
        prog_percent = min(1, farming['Evo']['Subtotal Multi'] / final_crops[first_failed_key][1]) * 100
        evo_advices[total].append(Advice(
            label=f"Final {final_crops[first_failed_key][0]} chance"
                  f"<br>{first_failed_goal:.3g} for 100% chance",
            picture_class=final_crops[first_failed_key][2],
            progression=f"{round(prog_percent, 2):g}",
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
                    label=f"Final {v[0]} chance"
                          f"<br>{first_failed_goal:.3g} for 100% chance",
                    picture_class=v[2],
                    progression=f"{min(1, prog_percent):.2%}",
                    goal="100%"
                ))
                break

    for category in evo_advices.values():
        for advice in category:
            mark_advice_completed(advice)

    evo_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Crop Evolution Chance',
        advices=evo_advices,
        informational=True,
        completed=session_data.account.farming['CropsUnlocked'] >= max_farming_crops
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
    speed_advices[summon].extend(session_data.account.summoning['WinnerBonusesSummaryRest'])

#Vial and Market
    # Vial
    speed_advices[vm].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Ricecakorade (Rice Cake): {session_data.account.alchemy_vials['Ricecakorade (Rice Cake)']['BaseValue']:.2f}%"
              f"<br>Total Value after multis: {farming['Speed']['Vial Value']:.2f}%",
        picture_class="rice-cake",
        progression=session_data.account.alchemy_vials['Ricecakorade (Rice Cake)']['Level'],
        goal=max_vial_level
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
        pre_string='Sources of Farming Speed',
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
        label=f"More Beenz: {farming['MarketUpgrades']['More Beenz']['Description']}",
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
        pre_string='Sources of Magic Bean Bonus',
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
        pre_string='Sources of Overgrowth',
        advices=og_advices,
        informational=True
    )
    return og_ag

def getLRExclusions(farming, highestFarmingSkillLevel):
    exclusions = []
    if farming['LandRankTotalRanks'] >= 1400:
        exclusions.extend([v['Name'] for v in landrank_dict.values() if not v['Name'].startswith('Seed')])
    else:
        if max_farming_crops-1 in farming['Crops']:
            exclusions.extend([v['Name'] for v in landrank_dict.values() if v['Name'].startswith('Evolution')])
        if farming['Value']['FinalMin'] >= max_farming_value/100:
            exclusions.extend([v['Name'] for v in landrank_dict.values() if v['Name'].startswith('Production')])
        if farming['LandRankMinPlot'] >= 120:
            exclusions.extend([v['Name'] for v in landrank_dict.values() if v['Name'].startswith('Soil Exp')])
        if highestFarmingSkillLevel >= 300:
            exclusions.extend([v['Name'] for v in landrank_dict.values() if v['Name'].startswith('Farmtastic')])
    #logger.debug(f"Land Rank Exclusions: {exclusions}")
    return exclusions

def getProgressionTiersAdviceGroup(farming, highest_farming_level):
    farming_Advices = {
        'Tiers': {},
    }

    optional_tiers = 1
    true_max = true_max_tiers['Farming']
    max_tier = true_max - optional_tiers
    tier_All = 0

    multis = ['Evolution Gmo', 'Og Fertilizer']
    one_point_landranks = ['Seed of Stealth', 'Seed of Loot', 'Seed of Damage', 'Seed of Stats']
    lr_exclusions = getLRExclusions(farming, highest_farming_level)

    #Assess Tiers
    for tier_number, requirements in farming_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        advice_types_added = set()

        #Farming Level
        if highest_farming_level < requirements.get('Farming Level', 0):
            add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
            if subgroup_label in farming_Advices['Tiers']:
                advice_types_added.add('Farming Level')
                farming_Advices['Tiers'][subgroup_label].append(Advice(
                    label='Raise Farming skill level',
                    picture_class='farming',
                    progression=highest_farming_level,
                    goal=requirements.get('Farming Level', 0)
                ))

        # Unlock Crops
        if farming['CropsUnlocked'] < requirements.get('Crops Unlocked', 0):
            add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
            if subgroup_label in farming_Advices['Tiers']:
                advice_types_added.add('Crops Unlocked')
                shortby = requirements.get('Crops Unlocked', 0) - farming['CropsUnlocked']
                farming_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Unlock {shortby} more crop type{pl(shortby)}",
                    picture_class='crop-depot',
                    progression=farming['CropsUnlocked'],
                    goal=requirements.get('Crops Unlocked', 0)
                ))

        # Stats
        if 'Stats' in requirements:
            requiredStats = requirements['Stats']
            if 'Value' in requiredStats:
                if farming['Value']['FinalMin'] < requiredStats['Value']:
                    add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                    if subgroup_label in farming_Advices['Tiers']:
                        advice_types_added.add('Value Stat')
                        farming_Advices['Tiers'][subgroup_label].append(Advice(
                            label=f"Reach {requiredStats['Value']}x total Value",
                            picture_class='',
                            progression=f"{farming['Value']['FinalMin']:.0f}",
                            goal=requiredStats['Value']
                        ))

        #Day Market
        for r_name, r_level in requirements.get('Day Market', {}).items():
            if farming['MarketUpgrades'][r_name]['Level'] < r_level:
                add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                if subgroup_label in farming_Advices['Tiers']:
                    advice_types_added.add('Day Market')
                    material_crop_number = getRequiredCropNumber(r_name, r_level)
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label=f"{r_name}: "
                              f"{farming['MarketUpgrades'][r_name]['Value']:.4g}/{farming['MarketUpgrades'][r_name]['BonusPerLevel'] * r_level:.4g}"
                              f"{'%' if r_name != 'Land Plots' else ''}"
                              f"<br>Final level's crop: {crop_dict.get(material_crop_number, {}).get('Name', '')}",
                        picture_class='day-market',
                        progression=farming['MarketUpgrades'][r_name]['Level'],
                        goal=r_level,
                        resource=crop_dict.get(material_crop_number, {}).get('Image', '')
                    ))

        # Land Ranks - Database Upgrades
        lr_this_tier = []
        for set_number, set_requirements in requirements.get('Land Ranks', {}).items():
            for r_name, r_level in set_requirements.items():
                if farming['LandRankDatabase'][r_name]['Level'] < r_level and r_name not in lr_exclusions:
                    add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                    if subgroup_label in farming_Advices['Tiers']:
                        if r_name in one_point_landranks:
                            current = farming['LandRankDatabase'][r_name]['Value']
                            target = farming['LandRankDatabase'][r_name]['BaseValue']
                        else:
                            current = farming['LandRankDatabase'][r_name]['Value']
                            target = (1.7 * farming['LandRankDatabase'][r_name]['BaseValue'] * r_level) / (r_level + 80)
                        lr_this_tier.append([r_name, r_level, current, target])

        for lrIndex, lrAdvice in enumerate(lr_this_tier):
            if lrIndex+1 < len(lr_this_tier):
                safe_to_add = lr_this_tier[lrIndex][0] != lr_this_tier[lrIndex+1][0]
                if safe_to_add:
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label=f"{lrAdvice[0]}: {lrAdvice[2]:.4g}/{lrAdvice[3]:.4g}%",
                        picture_class=lrAdvice[0],
                        progression=farming['LandRankDatabase'][lrAdvice[0]]['Level'],
                        goal=lrAdvice[1]
                    ))
            else:
                farming_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"{lrAdvice[0]}: {lrAdvice[2]:.4g}/{lrAdvice[3]:.4g}%",
                    picture_class=lrAdvice[0],
                    progression=farming['LandRankDatabase'][lrAdvice[0]]['Level'],
                    goal=lrAdvice[1]
                ))

        # Suggestions
        if subgroup_label in farming_Advices['Tiers']:
            if requirements.get('Suggestions', {}):
                suggies = requirements['Suggestions']
                if 'Evolution' in suggies.get('Stacks', []):
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label='Evolution GMO stacks (200 crops)',
                        picture_class='night-market',
                        progression=session_data.account.farming['CropStacks']['Evolution Gmo'],
                        goal=requirements['Crops Unlocked'],
                    ))
                if 'Speed' in suggies.get('Stacks', []):
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label='Speed GMO stacks (1k crops)',
                        picture_class='night-market',
                        progression=session_data.account.farming['CropStacks']['Speed Gmo'],
                        goal=requirements['Crops Unlocked'],
                    ))
                if 'Value' in suggies.get('Stacks', []):
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label='Value GMO stacks (10k crops)',
                        picture_class='night-market',
                        progression=session_data.account.farming['CropStacks']['Value Gmo'],
                        goal=requirements['Crops Unlocked'],
                    ))
                if 'Super' in suggies.get('Stacks', []):
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label='Super GMO stacks (100k crops)',
                        picture_class='night-market',
                        progression=session_data.account.farming['CropStacks']['Super Gmo'],
                        goal=requirements['Crops Unlocked'],
                    ))
                if 'Speed' in suggies:
                    if farming['Speed']['Total Multi'] < suggies['Speed'][1]:
                        farming_Advices['Tiers'][subgroup_label].append(Advice(
                            label=f"Suggestion: {suggies['Speed'][0]} to {suggies['Speed'][1]}x Speed",
                            picture_class='crop-scientist',
                            progression=f"{farming['Speed']['Total Multi']:.2f}" if farming['Speed']['Total Multi'] < 10 else f"{farming['Speed']['Total Multi']:.0f}",
                            goal=f"{suggies['Speed'][1]}"
                        ))
                if 'OG' in suggies:
                    if farming['OG']['Total Multi'] < suggies['OG'][1]:
                        farming_Advices['Tiers'][subgroup_label].append(Advice(
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
                            farming_Advices['Tiers'][subgroup_label].append(Advice(
                                label=f"Suggestion: {low_target} to {target}x Evo Chance",
                                picture_class='crop-scientist',
                                progression=notateNumber(
                                    'Match',
                                    farming['Evo']['Subtotal Multi'],
                                    2 if farming['Evo']['Subtotal Multi'] < 10 else 0,
                                    '',
                                    target
                                ),
                                goal=target
                            ))
                    if 'CropIndex' in suggies:
                        for cropIndex in suggies['CropIndex']:
                            if cropIndex-1 not in farming['Crops']:
                                crop = crop_dict.get(cropIndex, {'Name': f"UnknownCrop{cropIndex}", 'Image': '', 'SeedName': 'UnknownSeed', 'SeedCropIndex': 0})
                                farming_Advices['Tiers'][subgroup_label].append(Advice(
                                    label=f"Suggestion: {crop['Name']} ({crop['SeedName']} #{crop['SeedCropIndex']})",
                                    picture_class=crop['Image'],
                                    progression=farming['CropCountsPerSeed'][crop['SeedName'] if not crop['SeedName'].endswith('Glassy') else 'Glassy'],
                                    goal=crop['SeedCropIndex']
                                ))
                if 'No Trade' in suggies:
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label=suggies['No Trade'],
                        picture_class='crop-transfer-ticket',
                        progression=EmojiType.NO.value,
                        goal=EmojiType.NO.value,
                    ))

        #Night Market
        total_magic_bean_cost = 0
        total_nm_entries = 0
        for r_name, r_level in requirements.get('Night Market', {}).items():
            if farming['MarketUpgrades'][r_name]['Level'] < r_level:
                add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                if subgroup_label in farming_Advices['Tiers']:
                    if r_name in multis:
                        current = ValueToMulti(farming['MarketUpgrades'][r_name]['Value'])
                        target = ValueToMulti(farming['MarketUpgrades'][r_name]['BonusPerLevel'] * r_level)
                    else:
                        current = farming['MarketUpgrades'][r_name]['Value']
                        target = farming['MarketUpgrades'][r_name]['BonusPerLevel'] * r_level
                    upgrade_cost = getNightMarketCost(r_name, farming['MarketUpgrades'][r_name]['Level'], r_level)
                    farming_Advices['Tiers'][subgroup_label].append(Advice(
                        label=f"{r_name}: "
                              f"{current:.4g}/{target:.4g}"
                              f"{'x' if r_name in multis else '%' if r_name != 'Overgrowth' and r_name != 'Land Rank' else ''}"
                              f"<br>Total Magic Bean cost: {upgrade_cost:,}",
                        picture_class='night-market',
                        progression=farming['MarketUpgrades'][r_name]['Level'],
                        goal=r_level,
                        resource='magic-bean'
                    ))
                    total_magic_bean_cost += upgrade_cost
                    total_nm_entries += 1
        if total_nm_entries > 1:
            target = notateNumber('Basic', total_magic_bean_cost, 2)
            farming_Advices['Tiers'][subgroup_label].append(Advice(
                label='Grand Total Magic Bean Cost remaining in this Tier',
                picture_class='magic-bean',
                progression=f"{notateNumber('Match', farming['MagicBeans'], 2, '', target)}",  #Does not include the value of their current trade
                goal=target,
                resource='magic-bean'
            ))

        #Alchemy Bubbles
        if 'Alchemy Bubbles' in requirements:
            for r_name, r_level in requirements['Alchemy Bubbles'].items():
                if r_level > session_data.account.alchemy_bubbles[r_name]['Level']:
                    add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                    if subgroup_label in farming_Advices['Tiers']:
                        advice_types_added.add('Alchemy Bubbles')
                        farming_Advices['Tiers'][subgroup_label].append(Advice(
                            label=f'Level {r_name} to 99% value',
                            picture_class=r_name,
                            progression=session_data.account.alchemy_bubbles[r_name]['Level'],
                            goal=r_level,
                            resource=session_data.account.alchemy_bubbles[r_name]['Material']
                        ))

        #Final tier check
        if subgroup_label not in farming_Advices['Tiers'] and tier_All == tier_number - 1:
            tier_All = tier_number

    #Generate AdviceGroups
    farming_AdviceGroups = {}
    farming_AdviceGroups['Tiers'] = AdviceGroup(
        tier=tier_All,
        pre_string='Continue Farming',
        advices=farming_Advices['Tiers'],
    )
    overall_SectionTier = min(true_max, tier_All)
    return farming_AdviceGroups, overall_SectionTier, max_tier, true_max


def getCostDiscountAdviceGroup(farming) -> AdviceGroup:
    cost_Advices = []

    cost_Advices.append(
        Advice(
            label=f"{{{{Emperor Showdowns|#emperor}}}}: {session_data.account.emperor['Bonuses'][2]['Description']}"
                  f"<br>{session_data.account.emperor['Bonuses'][2]['Scaling']}",
            picture_class='the-emperor',
            progression=session_data.account.emperor['Bonuses'][2]['Wins'],
            goal=EmojiType.INFINITY.value
        )
    )

    for advice in cost_Advices:
        mark_advice_completed(advice)

    cost_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Cost Discount for Day and Night Market',
        advices=cost_Advices,
        informational=True
    )
    cost_ag.remove_empty_subgroups()
    return cost_ag


def getFarmingAdviceSection():
    highest_farming_level = max(session_data.account.all_skills['Farming'])
    if highest_farming_level < 1:
        farming_AdviceSection = AdviceSection(
            name='Farming',
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking the Farming skill in W6!',
            picture='wiki/FarmCropBean.png',
            unreached=True
        )
        return farming_AdviceSection

    farming = session_data.account.farming

    #Generate AdviceGroups
    farming_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup(farming, highest_farming_level)
    farming_AdviceGroupDict['Evo'] = getEvoChanceAdviceGroup(farming, highest_farming_level)
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
    farming_AdviceGroupDict['Cost'] = getCostDiscountAdviceGroup(farming)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    farming_AdviceSection = AdviceSection(
        name='Farming',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Farming tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='wiki/FarmCropBean.png',
        groups=farming_AdviceGroupDict.values()
    )
    return farming_AdviceSection
