from math import ceil

from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.data_formatting import mark_advice_completed
from flask import g as session_data
from consts import (farming_progressionTiers, break_you_best, maxTiersPerGroup, maxFarmingCrops, maxCharacters, max_VialLevel, maxMealLevel, stamp_maxes,
                    ValueToMulti, tomepct, getCropEvoChance, cropDict)
from utils.text_formatting import pl

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
        advices=cd_advices
    )

    return cd_ag

def getDayMarketAdviceGroup(farming) -> AdviceGroup:
    dm = {name:details for name, details in farming['MarketUpgrades'].items() if details['MarketType'] == 'Day'}
    dm_advices = [
        Advice(
            label=#f"{details['Level']}/{details['MaxLevel']} "
                  f"{name}: {details['Description']}",
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
        advices=dm_advices
    )
    return dm_ag

def getNightMarketAdviceGroup(farming) -> AdviceGroup:
    nm = {name:details for name, details in farming['MarketUpgrades'].items() if details['MarketType'] == 'Night'}
    nm_advices = [
        Advice(
            label=#f"{details['Level']}/{details['MaxLevel']} "
                  f"{name}: {details['Description']}",
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
        advices=nm_advices
    )
    return nm_ag

def getCropValueAdviceGroup(farming) -> AdviceGroup:
    val = farming['Value']
    mga = f"Multi Group A: {val['Doubler Multi']:.2f}"
    mgb = f"Multi Group B: {val['Mboost Sboost Multi']:.2f}"
    mgc = f"Multi Group C: {val['Pboost Ballot Multi Min']:.2f} to {val['Pboost Ballot Multi Max']:.2f}"
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
    value_advices[mgb].append(Advice(
        label=f"Production Megaboost: +{farming['LandRankDatabase']['Production Megaboost']['Value']:.3f}%",
        picture_class='production-megaboost',
        progression=farming['LandRankDatabase']['Production Megaboost']['Level']
    ))
    value_advices[mgb].append(Advice(
        label=f"Production Superboost: +{farming['LandRankDatabase']['Production Superboost']['Value']:.3f}%",
        picture_class='production-superboost',
        progression=farming['LandRankDatabase']['Production Superboost']['Level']
    ))

    #MGC
    value_advices[mgc].append(Advice(
        label=f"Lowest Land Rank: {farming.get('LandRankMinPlot', 0)}",
        picture_class=getLandRankImage(farming.get('LandRankMinPlot', 0)),
    ))
    value_advices[mgc].append(Advice(
        label=f"Highest Land Rank: {farming.get('LandRankMaxPlot', 0)}",
        picture_class=getLandRankImage(farming.get('LandRankMaxPlot', 0)),
    ))
    value_advices[mgc].append(Advice(
        label=f"Production Boost: +{farming['LandRankDatabase']['Production Boost']['Value']:,.3f}% per land rank."
              f"<br>Total on Lowest: +{farming['LandRankDatabase']['Production Boost']['Value'] * farming.get('LandRankMinPlot', 0):.3f}%"
              f"<br>Total on Highest: +{farming['LandRankDatabase']['Production Boost']['Value'] * farming.get('LandRankMaxPlot', 0):.3f}%",
        picture_class='production-boost',
        progression=farming['LandRankDatabase']['Production Boost']['Level']
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
        label=f"Total on Lowest ranked plot",
        picture_class='crop-scientist',
        progression=val['BeforeCapMin'],
        goal=100
    ))
    value_advices[final].append(Advice(
        label=f"Total on Highest ranked plot",
        picture_class='crop-scientist',
        progression=val['BeforeCapMax'],
        goal=100
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
        advices=value_advices
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
        resource=session_data.account.alchemy_bubbles['Cropius Mapper']['Material']
    ))
    evo_advices[alch].append(Advice(
        label=f"Crop Chapter: {session_data.account.alchemy_bubbles['Crop Chapter']['BaseValue']:.3}% per 2k Tome Points above 5k",
        picture_class='crop-chapter',
        progression=session_data.account.alchemy_bubbles['Crop Chapter']['Level'],
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
        label=f"Lowest Land Rank: {farming.get('LandRankMinPlot', 0)}",
        picture_class=getLandRankImage(farming.get('LandRankMinPlot', 0)),
    ))
    evo_advices[lr].append(Advice(
        label=f"Highest Land Rank: {farming.get('LandRankMaxPlot', 0)}",
        picture_class=getLandRankImage(farming.get('LandRankMaxPlot', 0)),
    ))
    evo_advices[lr].append(Advice(
        label=f"Evolution Boost: +{farming['LandRankDatabase']['Evolution Boost']['Value']:.3f}% per land rank."
              f"<br>Total on Lowest: +{farming['LandRankDatabase']['Evolution Boost']['Value'] * farming.get('LandRankMinPlot', 0):,.3f}%"
              f"<br>Total on Highest: +{farming['LandRankDatabase']['Evolution Boost']['Value'] * farming.get('LandRankMaxPlot', 0):,.3f}%",
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
                (tome_added < 3 and first_failed_key <= 8)
                or (tome_added < 5 and first_failed_key >= 9)
            ):
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
        advices=evo_advices
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
        advices=speed_advices
    )
    return speed_ag

def getBeanMultiAdviceGroup(farming) -> AdviceGroup:
    # Create subgroup labels
    total = f"Total: {farming['Bean']['Total Multi']}x"
    mga = f"Day Market: {farming['Bean']['mga']}x"
    mgb = f"Emporium + Achievement: {farming['Bean']['mgb']}x"
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
        advices=bm_advices
    )
    return bm_ag

def getOGAdviceGroup(farming):
    # Fun calculations
    ach_multi = ValueToMulti(15 * session_data.account.achievements['Big Time Land Owner']['Complete'])
    starsign_final_value = (
        15 * session_data.account.star_signs['O.G. Signalais']['Unlocked']
        * session_data.account.star_sign_extras['SilkrodeNanoMulti']
        * session_data.account.star_sign_extras['SeraphMulti']
    )
    ss_multi = ValueToMulti(starsign_final_value)
    nm_multi = ValueToMulti(farming['MarketUpgrades']['Og Fertilizer']['Value'])
    merit_multi = ValueToMulti(2 * session_data.account.merits[5][2]['Level'])
    lr_multi = (ValueToMulti(
        farming['LandRankDatabase']['Overgrowth Boost']['Value']
        + farming['LandRankDatabase']['Overgrowth Megaboost']['Value']
        + farming['LandRankDatabase']['Overgrowth Superboost']['Value']
    ))
    pristine_multi = ValueToMulti(50 * session_data.account.sneaking['PristineCharms']['Taffy Disc']['Obtained'])
    total_multi = ach_multi * ss_multi * nm_multi * merit_multi * lr_multi * pristine_multi

    # Create subgroup labels
    total = f"Total: {total_multi:,.3f}x"
    nm = f"Night Market: {nm_multi:.3f}x"
    lr = f"Land Rank Total: {lr_multi:,.3f}x"
    ss = f"Star Sign: {ss_multi:.2f}x"
    ach = f"Achievement: {ach_multi:.2f}x"
    merit = f"Merit: {merit_multi:.2f}x"
    pristine = f"Pristine Charm: {pristine_multi:.2f}x"

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
        label=f"Overgrowth Chance: {total_multi:,.3f}x",
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
              f"<br>Total Value if doubled: {starsign_final_value:.3f}%",
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
        advices=og_advices
    )
    return og_ag

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
        subgroupName = f"TESTING PURPOSES ONLY, TIERS NOT READY!"
        #subgroupName = f"To reach Tier {tierNumber}"
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
    farming_AdviceGroupDict['Evo'] = getEvoChanceAdviceGroup(farming)
    farming_AdviceGroupDict['Speed'] = getSpeedAdviceGroup(farming)
    farming_AdviceGroupDict['OG'] = getOGAdviceGroup(farming)
    farming_AdviceGroupDict['Value'] = getCropValueAdviceGroup(farming)
    farming_AdviceGroupDict['Bean'] = getBeanMultiAdviceGroup(farming)
    farming_AdviceGroupDict['Depot'] = getCropDepotAdviceGroup(farming)
    farming_AdviceGroupDict['Day'] = getDayMarketAdviceGroup(farming)
    farming_AdviceGroupDict['Night'] = getNightMarketAdviceGroup(farming)

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
