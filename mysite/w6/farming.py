from math import ceil, floor

from consts.consts_autoreview import break_you_best, ValueToMulti, build_subgroup_label, EmojiType
from consts.consts_w2 import max_vial_level
from consts.consts_w4 import max_meal_level
from consts.idleon.consts_idleon import max_characters
from consts.idleon.w6.farming import landrank_list
from consts.progression_tiers import farming_progressionTiers, true_max_tiers
from consts.w6.farming import max_farming_crops, max_farming_value, crop_evo_breakpoint_list

from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.w6 import get_summoning_bonus_advice
from models.w6.farming import Farming

from utils.logging import get_logger
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.number_formatting import round_and_trim
from utils.text_formatting import pl, notateNumber

logger = get_logger(__name__)


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
        farming.crops.get_discovery_advice()
    ]
    for bonus in farming.depot.values():
        cd_advices.append(bonus.get_bonus_advice(False))

    for advice in cd_advices:
        advice.mark_advice_completed()

    cd_ag = AdviceGroup(
        tier='',
        pre_string='Crop Depot bonuses',
        advices=cd_advices,
        informational=True
    )

    return cd_ag

def getMarketAdviceGroup(farming) -> AdviceGroup:
    advice_section = {
        "Day Market": [
            upgrade.get_bonus_advice(True)
            for upgrade in farming.market.values()
            if upgrade.is_day
        ],
        "Night Market": [
            upgrade.get_bonus_advice(True)
            for upgrade in farming.market.values()
            if not upgrade.is_day
        ],
    }

    for advice_list in advice_section.values():
        for advice in advice_list:
            advice.mark_advice_completed()

    dm_ag = AdviceGroup(
        tier='',
        pre_string='Market upgrades',
        advices=advice_section,
        informational=True
    )
    return dm_ag


def getRankDatabaseAdviceGroup(farming) -> AdviceGroup:
    advice_list = [
        upgrade.get_bonus_advice(False) for upgrade in farming.land_rank.values()
    ]
    for advice in advice_list:
        advice.mark_advice_completed()
    return AdviceGroup(
        tier='',
        pre_string='Rank Database',
        advices=advice_list,
        informational=True
    )


def val_m_s_boost(megaboost, superboost):
    return ValueToMulti(
        ((1.7 * 100 * megaboost) / (megaboost + 80))
        + ((1.7 * 600 * superboost) / (superboost + 80))
    )

def val_boost(minrank, b):
    return ValueToMulti(((1.7 * 5 * b) / (b + 80)) * minrank)

def getValueLRSuggies(farming):
    #names = ['Boost', 'Megaboost', 'Superboost']
    min_lr = max(farming.land_rank.min_level, floor(0.8 * farming.land_rank.max_level))
    value = farming.multi['Value']['Doubler Multi']
    available_points = farming.land_rank.total_level
    currently_invested = sum([
        farming.land_rank['Production Boost'].level,
        farming.land_rank['Production Megaboost'].level,
        farming.land_rank['Production Superboost'].level
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
    val = farming.multi['Value']
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
              f"{(farming.market['Product Doubler'].value // 100) * 100:.0f}%",
        picture_class='day-market',
        progression=f"{farming.market['Product Doubler'].value:.0f}",
        goal=400,
        unit='%'
    ))

    #MGB
    #optimal_upgrades = getValueLRSuggies(farming) if farming['LandRankTotalRanks'] >= 5 else [-1, -1, -1]
    # TODO: use optimal level as level_goal=optimal_upgrades[1] if # optimal_upgrades[1] >= 0 else None
    value_advices[mgb].append(
        farming.land_rank['Production Megaboost'].get_bonus_advice(False)
    )
    # TODO: use optimal level as level_goal=optimal_upgrades[2] if # optimal_upgrades[2] >= 0 else None
    value_advices[mgb].append(
        farming.land_rank['Production Superboost'].get_bonus_advice(False)
    )

    #MGC
    # TODO: use optimal level optimal_upgrades[0] if optimal_upgrades[0] >= 0 else None
    value_advices[mgc].extend(
        farming.land_rank.get_bonus_with_land_rank_advice("Production Boost")
    )

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

    value_advices[mgd].append(farming.market['Value Gmo'].get_bonus_advice())

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

def getEvoChanceAdviceGroup(farming: Farming, highest_farming_level) -> AdviceGroup:
    summoning_evo = session_data.account.summoning['Bonuses']['<x Crop EVO']['Value']
    evo_multi = farming.multi['Evo']
    #Create subgroup labels
    alch = f"Alchemy: {evo_multi['Alch Multi']:.3f}x"
    stamp = f"Stamps: {evo_multi['Stamp Multi']:.3f}x"
    meals = f"Meals: {evo_multi['Meals Multi']:.3f}x"
    farm = f"Markets: {evo_multi['Farm Multi']:.3g}x"
    lr = f"Land Ranks: {evo_multi['LR Multi']:,.3f}x"
    summon = f"Summoning: {round_and_trim(summoning_evo)}x"
    ss = f"Star Sign: {evo_multi['SS Multi']:.3f}x"
    lamp = f"Lamp Wish: {evo_multi['Wish Multi']:.3f}x"
    misc = f"Misc: {evo_multi['Misc Multi']:.3f}x"
    total = f"Total Evo Chance: {evo_multi['Subtotal Multi']:.3g}x"
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
        label=f"Cropius Mapper: {evo_multi['Maps Opened']}/{max_characters * (len(session_data.account.enemy_maps[6]) - 1)} maps"
              f"<br>Total value: {evo_multi['Cropius Final Value']:.3f}%",
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
              f"<br>Total Value after multis: {evo_multi['Vial Value']:.2f}%",
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
    evo_advices[stamp].append(
        session_data.account.sneaking.pristine_charms[
            'Liqorice Rolle'
        ].get_obtained_advice()
    )
    evo_advices[stamp].append(session_data.account.stamps['Crop Evo Stamp'].get_advice())

#Meals
    evo_advices[meals].append(Advice(
        label=f"{{{{ Meal|#cooking }}}}: Bill Jack Pepper: {session_data.account.meals['Bill Jack Pepper']['Description']}",
        picture_class=session_data.account.meals['Bill Jack Pepper']['Image'],
        progression=session_data.account.meals['Bill Jack Pepper']['Level'],
        goal=max_meal_level
    ))

    evo_advices[meals].append(Advice(
        label=f"Highest Summoning level: {max(session_data.account.all_skills['Summoning'], default=0)}"
              f"<br>Provides a {evo_multi['Nyan Stacks']}x multi to Nyanborgir",
        picture_class='summoning'
    ))
    evo_advices[meals].append(Advice(
        label=f"{{{{ Meal|#cooking }}}}: Nyanborgir: {session_data.account.meals['Nyanborgir']['Description']}"
              f"<br>After {evo_multi['Nyan Stacks']} Summoning Level stack{pl(evo_multi['Nyan Stacks'])}:"
              f" {session_data.account.meals['Nyanborgir']['Value'] * evo_multi['Nyan Stacks']:,.3f}%",
        picture_class=session_data.account.meals['Nyanborgir']['Image'],
        progression=session_data.account.meals['Nyanborgir']['Level'],
        goal=max_meal_level
    ))

#Day Market
    evo_advices[farm].append(
        farming.market['Biology Boost'].get_bonus_advice()
    )

#Night Market
    evo_advices[farm].append(farming.market['Super Gmo'].get_bonus_advice())
    evo_advices[farm].append(
        farming.market['Evolution Gmo'].get_bonus_advice()
    )

#LAND RANKS
    evo_advices[lr].extend(
        farming.land_rank.get_bonus_with_land_rank_advice("Evolution Boost")
    )
    evo_advices[lr].append(
        farming.land_rank["Evolution Megaboost"].get_bonus_advice(False)
    )
    evo_advices[lr].append(
        farming.land_rank["Evolution Superboost"].get_bonus_advice(False)
    )
    evo_advices[lr].append(
        farming.land_rank['Evolution Ultraboost'].get_bonus_advice(False)
    )

#SUMMONING
    evo_advices[summon].append(get_summoning_bonus_advice('<x Crop EVO'))
#Star Sign
    evo_advices[ss].append(session_data.account.star_sign_extras['SeraphAdvice'])
    evo_advices[ss].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    evo_advices[ss].append(Advice(
        label=f"Highest Farming level: {highest_farming_level}",
        picture_class='farming'
    ))

    evo_advices[ss].append(Advice(
        label=f"{{{{ Starsign|#star-signs }}}}: Cropiovo Minor: {3 * session_data.account.star_signs['Cropiovo Minor']['Unlocked']:.0f}/3% per farming level."
              f"<br>Total Value if doubled: {evo_multi['Starsign Final Value']:,.3f}%",
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
        label=f"Skill Mastery at 200 Farming: +{1.15 * evo_multi['Skill Mastery Bonus Bool'] * session_data.account.rift['SkillMastery']}/1.15x",
        picture_class='farming',
        progression=evo_multi['Total Farming Levels'],
        goal=200
    ))

    evo_advices[misc].append(Advice(
        label=f"Weekly Ballot: {evo_multi['Ballot Multi Current']:.3f}/{evo_multi['Ballot Multi Max']:.3f}x"
              f"<br>(Buff {evo_multi['Ballot Status']})",
        picture_class='ballot-29',
        progression=int(evo_multi['Ballot Active']),
        goal=1
    ))

#Total
    first_crop_index = crop_evo_breakpoint_list[0]
    target_evo_crop = (
        first_crop_index, ceil(1 / farming.crops.evo_chance(first_crop_index))
    )
    for crop_index in crop_evo_breakpoint_list[1:]:
        crop_evo_chance = ceil(1 / farming.crops.evo_chance(crop_index))
        if evo_multi['Subtotal Multi'] > crop_evo_chance:
            # Found crop for that we have enough evo chance, use previous as
            # target
            break
        target_evo_crop = crop_index, crop_evo_chance
    if target_evo_crop is not None:
        crop_index, crop_evo_chance = target_evo_crop
        precent = evo_multi['Subtotal Multi'] / crop_evo_chance
        evo_advices[total].append(
            farming.crops.get_crop_evo_advice(crop_index, crop_evo_chance, precent)
        )

    for category in evo_advices.values():
        for advice in category:
            advice.mark_advice_completed()

    evo_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Crop Evolution Chance',
        advices=evo_advices,
        informational=True,
        completed=session_data.account.farming.crops.unlocked >= max_farming_crops
    )
    return evo_ag


def getSpeedAdviceGroup(farming) -> AdviceGroup:
    summoning_speed = session_data.account.summoning['Bonuses']['<x Farming SPD']['Value']
    # Create subgroup labels
    total = f"Total: {farming.multi['Speed']['Total Multi']:,.3f}x"
    summon = f"Summoning: {round_and_trim(summoning_speed)}x"
    vm = f"Vial + Day Market: {farming.multi['Speed']['VM Multi']:,.3f}x"
    nm = f"Night Market: {farming.multi['Speed']['NM Multi']:,.3f}x"
    speed_advices = {
        total: [],
        summon: [],
        vm: [],
        nm: [],
    }
#Advices
#Total
    speed_advices[total].append(Advice(
        label=f"Farming Speed Multi: {farming.multi['Speed']['Total Multi']:,.3f}x",
        picture_class='crop-scientist'
    ))
#Summoning
    speed_advices[summon].append(get_summoning_bonus_advice('<x Farming SPD'))
#Vial and Market
    # Vial
    speed_advices[vm].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Ricecakorade (Rice Cake): {session_data.account.alchemy_vials['Ricecakorade (Rice Cake)']['BaseValue']:.2f}%"
              f"<br>Total Value after multis: {farming.multi['Speed']['Vial Value']:.2f}%",
        picture_class="rice-cake",
        progression=session_data.account.alchemy_vials['Ricecakorade (Rice Cake)']['Level'],
        goal=max_vial_level
    ))
    # Day Market
    speed_advices[vm].append(
        farming.market['Nutritious Soil'].get_bonus_advice()
    )
#Night Market
    speed_advices[nm].append(farming.market['Super Gmo'].get_bonus_advice())
    speed_advices[nm].append(farming.market['Speed Gmo'].get_bonus_advice())

    for category in speed_advices.values():
        for advice in category:
            advice.mark_advice_completed()

    speed_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Farming Speed',
        advices=speed_advices,
        informational=True
    )
    return speed_ag

def getBeanMultiAdviceGroup(farming) -> AdviceGroup:
    # Create subgroup labels
    total = f"Total: {farming.multi['Bean']['Total Multi']:.2f}x"
    mga = f"Day Market: {farming.multi['Bean']['mga']:.2f}x"
    mgb = f"Emporium + Achievement: {farming.multi['Bean']['mgb']:.2f}x"
    bm_advices = {
        total: [],
        mga: [],
        mgb: []
    }

    #Total
    bm_advices[total].append(Advice(
        label=f"Magic Beans Bonus: {farming.multi['Bean']['Total Multi']:,.3f}x",
        picture_class='crop-scientist'
    ))

    #Day Market - More Beenz
    bm_advices[mga].append(farming.market['More Beenz'].get_bonus_advice())
    #Emporium - Deal Sweetening
    bm_advices[mgb].append(
        session_data.account.sneaking.emporium['Deal Sweetening'].get_obtained_advice()
    )
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
            advice.mark_advice_completed()

    bm_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Magic Bean Bonus',
        advices=bm_advices,
        informational=True
    )
    return bm_ag

def getOGAdviceGroup(farming):
    # Create subgroup labels
    total = f"Total: {farming.multi['OG']['Total Multi']:,.3f}x"
    nm = f"Night Market: {farming.multi['OG']['NM Multi']:.3f}x"
    lr = f"Land Rank Total: {farming.multi['OG']['LR Multi']:,.3f}x"
    ss = f"Star Sign: {farming.multi['OG']['SS Multi']:.2f}x"
    ach = f"Achievement: {farming.multi['OG']['Ach Multi']:.2f}x"
    merit = f"Merit: {farming.multi['OG']['Merit Multi']:.2f}x"
    pristine = f"Pristine Charm: {farming.multi['OG']['Pristine Multi']:.2f}x"

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
        label=f"Overgrowth Chance: {farming.multi['OG']['Total Multi']:,.3f}x",
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
              f"<br>Total Value if doubled: {farming.multi['OG']['Starsign Final Value']:.3f}%",
        picture_class='og-signalais',
        progression=int(session_data.account.star_signs['O.G. Signalais']['Unlocked']),
        goal=1
    ))
#Night Market
    og_advices[nm].append(farming.market['Og Fertilizer'].get_bonus_advice())
#Merit
    og_advices[merit].append(Advice(
        label=f"W6 Taskboard Merit: +{2 * session_data.account.merits[5][2]['Level']}/30%",
        picture_class='merit-5-2',
        progression=session_data.account.merits[5][2]['Level'],
        goal=15
    ))
#Land Rank
    og_advices[lr].append(
        farming.land_rank['Overgrowth Boost'].get_bonus_advice(False)
    )
    og_advices[lr].append(
        farming.land_rank['Overgrowth Megaboost'].get_bonus_advice(False)
    )
    og_advices[lr].append(
        farming.land_rank['Overgrowth Superboost'].get_bonus_advice(False)
    )

    # Pristine Charm
    og_advices[pristine].append(
        session_data.account.sneaking.pristine_charms[
            'Taffy Disc'
        ].get_obtained_advice()
    )

    for category in og_advices.values():
        for advice in category:
            advice.mark_advice_completed()

    og_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Overgrowth',
        advices=og_advices,
        informational=True
    )
    return og_ag

def getLRExclusions(farming, highestFarmingSkillLevel):
    exclusions = []
    if farming.land_rank.total_level >= 1400:
        exclusions.extend([v['Name'] for v in landrank_list if not v['Name'].startswith('Seed')])
    else:
        if max_farming_crops - 1 in farming.crops:
            exclusions.extend([v['Name'] for v in landrank_list if v['Name'].startswith('Evolution')])
        if farming.multi['Value']['FinalMin'] >= max_farming_value/100:
            exclusions.extend([v['Name'] for v in landrank_list if v['Name'].startswith('Production')])
        if farming.land_rank.min_level >= 120:
            exclusions.extend([v['Name'] for v in landrank_list if v['Name'].startswith('Soil Exp')])
        if highestFarmingSkillLevel >= 300:
            exclusions.extend([v['Name'] for v in landrank_list if v['Name'].startswith('Farmtastic')])
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
    cost_multi = max(.001, session_data.account.emperor["cheaper Farming Upgrades"].value)

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
        require_crop_unlock = requirements.get('Crops Unlocked', 0)
        if farming.crops.unlocked < require_crop_unlock:
            add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
            if subgroup_label in farming_Advices['Tiers']:
                advice_types_added.add('Crops Unlocked')
                farming_Advices['Tiers'][subgroup_label].append(
                    farming.crops.get_unlock_advice(require_crop_unlock)
                )

        # Stats
        if 'Stats' in requirements:
            requiredStats = requirements['Stats']
            if 'Value' in requiredStats:
                if farming.multi['Value']['FinalMin'] < requiredStats['Value']:
                    add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                    if subgroup_label in farming_Advices['Tiers']:
                        advice_types_added.add('Value Stat')
                        farming_Advices['Tiers'][subgroup_label].append(Advice(
                            label=f"Reach {requiredStats['Value']}x total Value",
                            picture_class='',
                            progression=f"{farming.multi['Value']['FinalMin']:.0f}",
                            goal=requiredStats['Value']
                        ))

        # Day Market
        # TODO: calculate all market cost and show total of each crop after
        for r_name, r_level in requirements.get('Day Market', {}).items():
            if farming.market[r_name].level < r_level:
                add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                if subgroup_label in farming_Advices['Tiers']:
                    advice_types_added.add('Day Market')
                    _, target_advice = farming.market[r_name].get_target_bonus(r_level, cost_multi)
                    farming_Advices['Tiers'][subgroup_label].append(target_advice)

        # Land Ranks - Database Upgrades
        lr_this_tier = []
        for set_number, set_requirements in requirements.get('Land Ranks', {}).items():
            for r_name, r_level in set_requirements.items():
                if farming.land_rank[r_name].level < r_level and r_name not in lr_exclusions:
                    add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                    if subgroup_label in farming_Advices['Tiers']:
                        upgrade = farming.land_rank[r_name]
                        lr_this_tier.append([upgrade, r_level])

        for lrIndex, lrAdvice in enumerate(lr_this_tier):
            if lrIndex+1 < len(lr_this_tier):
                safe_to_add = lr_this_tier[lrIndex][0] != lr_this_tier[lrIndex+1][0]
                if safe_to_add:
                    farming_Advices['Tiers'][subgroup_label].append(
                        lrAdvice[0].get_bonus_advice(False, lrAdvice[1])
                    )
            else:
                farming_Advices['Tiers'][subgroup_label].append(
                    lrAdvice[0].get_bonus_advice(False, lrAdvice[1])
                )

        # Suggestions
        if subgroup_label in farming_Advices['Tiers']:
            if requirements.get('Suggestions', {}):
                suggies = requirements['Suggestions']
                for name in suggies.get('Stacks', []):
                    farming_Advices['Tiers'][subgroup_label].append(
                        session_data.account.farming.crops.get_stack_progress_advice(name, requirements['Crops Unlocked'])
                    )
                if 'Speed' in suggies:
                    if farming.multi['Speed']['Total Multi'] < suggies['Speed'][1]:
                        farming_Advices['Tiers'][subgroup_label].append(Advice(
                            label=f"Suggestion: {suggies['Speed'][0]} to {suggies['Speed'][1]}x Speed",
                            picture_class='crop-scientist',
                            progression=f"{farming.multi['Speed']['Total Multi']:.2f}" if farming.multi['Speed']['Total Multi'] < 10 else f"{farming.multi['Speed']['Total Multi']:.0f}",
                            goal=f"{suggies['Speed'][1]}"
                        ))
                if 'OG' in suggies:
                    if farming.multi['OG']['Total Multi'] < suggies['OG'][1]:
                        farming_Advices['Tiers'][subgroup_label].append(Advice(
                            label=f"Suggestion: {suggies['OG'][0]} to {suggies['OG'][1]}x Overgrowth",
                            picture_class='crop-scientist',
                            progression=f"{farming.multi['OG']['Total Multi']:.2f}" if farming.multi['OG']['Total Multi'] < 10 else f"{farming.multi['OG']['Total Multi']:.0f}",
                            goal=f"{suggies['OG'][1]}"
                        ))
                if 'Crops Unlocked' in advice_types_added:
                    if 'EvoChance' in suggies:
                        if farming.multi['Evo']['Subtotal Multi'] < suggies['EvoChance'][1]:
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
                                    farming.multi['Evo']['Subtotal Multi'],
                                    2 if farming.multi['Evo']['Subtotal Multi'] < 10 else 0,
                                    '',
                                    target
                                ),
                                goal=target
                            ))
                    if 'CropIndex' in suggies:
                        for cropIndex in suggies['CropIndex']:
                            farming_Advices['Tiers'][subgroup_label].append(
                                farming.crops.get_crop_unlock_advice(cropIndex)
                            )

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
            if farming.market[r_name].level < r_level:
                add_subgroup_if_available_slot(farming_Advices['Tiers'], subgroup_label)
                if subgroup_label in farming_Advices['Tiers']:
                    upgrade_cost, target_advice = farming.market[r_name].get_target_bonus(r_level, cost_multi)
                    farming_Advices['Tiers'][subgroup_label].append(target_advice)
                    total_magic_bean_cost += upgrade_cost
                    total_nm_entries += 1
        if total_nm_entries > 1:
            target = notateNumber('Basic', total_magic_bean_cost, 2)
            farming_Advices['Tiers'][subgroup_label].append(Advice(
                label='Grand Total Magic Bean Cost remaining in this Tier',
                picture_class='magic-bean',
                progression=f"{notateNumber('Match', farming.magic_beans, 2, '', target)}",  #Does not include the value of their current trade
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
    farming_AdviceGroups['Tiers'].remove_empty_subgroups()
    overall_SectionTier = min(true_max, tier_All)
    return farming_AdviceGroups, overall_SectionTier, max_tier, true_max


def getCostDiscountAdviceGroup(farming) -> AdviceGroup:
    cost_Advices = []

    cost_Advices.append(
        session_data.account.emperor["cheaper Farming Upgrades"].get_bonus_advice()
    )

    for advice in cost_Advices:
        advice.mark_advice_completed()

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
    if farming.market['Overgrowth'].level >= 1:
        farming_AdviceGroupDict['OG'] = getOGAdviceGroup(farming)
    if farming.land_rank.total_level >= 1:
        farming_AdviceGroupDict['Value'] = getCropValueAdviceGroup(farming)
    if farming.magic_bean_unlocked:
        farming_AdviceGroupDict['Bean'] = getBeanMultiAdviceGroup(farming)
    if session_data.account.sneaking.emporium['Crop Depot Scientist'].obtained:
        farming_AdviceGroupDict['Depot'] = getCropDepotAdviceGroup(farming)
    farming_AdviceGroupDict['Market'] = getMarketAdviceGroup(farming)
    farming_AdviceGroupDict['Rank'] = getRankDatabaseAdviceGroup(farming)
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
