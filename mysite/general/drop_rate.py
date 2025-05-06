from models.models import Advice, AdviceGroup, AdviceSection
from consts import (
	lavaFunc, max_card_stars, maxFarmingCrops, max_land_rank_level, max_IndexOfSigils, stampsDict,
    class_kill_talents_dict, cards_max_level, numberOfArtifactTiers, sigilsDict, riftRewardsDict
)
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import notateNumber
from utils.logging import get_logger
from math import floor
from flask import g as session_data

logger = get_logger(__name__)
general = 'General'
w1 = 'World 1'
w2 = 'World 2'
w3 = 'World 3'
w4 = 'World 4'
w5 = 'World 5'
w6 = 'World 6'

# All of the cards that affect Drop Rate

drop_rate_cards = [
    'Emperor',
    'Minichief Spirit',
    'King Doot',
    'Mister Brightside',
    'Crystal Carrot',
    'Bop Box',
    'Mr Blueberry',
    'Giftmas Blobulyte',
    'Mimic'
]
passive_drop_rate_cards = [
    'Domeo Magmus',
    'Ancient Golem',
    'IdleOn Fourth Anniversary'
]

def get_drop_rate_account_advice_group() -> AdviceGroup:
    drop_rate_shiny_base = 1
    missing_companion_data_txt = ''
    if not session_data.account.companions['Companion Data Present']:
        missing_companion_data_txt = '<br>Note: Could be inaccurate. Companion data not found!'

    drop_rate_aw_advice = {
        general: [],
        w1: [],
        w2: [],
        w3: [],
        w4: [],
        w5: [],
        w6: []
    }

    #########################################
    # Account Wide
    #########################################

    # Global
    #########################################

    # Rift - Ruby Cards
    if not session_data.account.rift['RubyCards']:
        ruby_cards_rift_level = next(i for i, r in riftRewardsDict.items() if r['Shorthand'] == 'RubyCards')
        rift_level = session_data.account.rift['Level']
        drop_rate_aw_advice[general].append(Advice(
            label=f"Rift- Ruby Cards:"
                f"<br>+1 Max Card Level"
                f"<br>Note: increases the max card level for the cards below",
            picture_class='ruby-cards',
            progression=rift_level,
            goal=ruby_cards_rift_level
        ))

    # Cards - Drop Rate
    for card in session_data.account.cards:
        if card.name in passive_drop_rate_cards:
            drop_rate_aw_advice[general].append(card.getAdvice())

    # Guild Bonus - Gold Charm
    gold_charm_bonus = session_data.account.guild_bonuses['Gold Charm']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Guild Bonus- Gold Charm:"
              f"<br>+{gold_charm_bonus['Value']:g}/{gold_charm_bonus['MaxValue']:g}% Drop Rate",
        picture_class=gold_charm_bonus['Picture'],
        progression=gold_charm_bonus['Level'],
        goal=gold_charm_bonus['MaxLevel']
    ))

    # Upgrade Vault - Vault Mastery
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    vault_mastery_vault = session_data.account.vault['Upgrades']['Vault Mastery']
    vault_mastery_vault_level = vault_mastery_vault['Level']
    vault_mastery_vault_level_max = vault_mastery_vault['Max Level']
    vault_mastery_vault_value = 1 + (vault_mastery_vault_level * vault_mastery_vault['Value Per Level'])/100
    vault_mastery_vault_value_max = 1 + (vault_mastery_vault_level_max * vault_mastery_vault['Value Per Level'])/100
    if vault_mastery_vault_level < vault_mastery_vault_level_max:
        drop_rate_aw_advice[general].append(Advice(
            label=f"Upgrade Vault- Vault Mastery:"
                f"<br>x{vault_mastery_vault_value:g}/x{vault_mastery_vault_value_max:g} blue highlighted vault bonuses"
                f"<br>(increases the value of the Vault upgrade below)",
            picture_class=vault_mastery_vault['Image'],
            progression=vault_mastery_vault_level,
            goal=vault_mastery_vault_level_max
        ))
    # Upgrade Vault - Drops for Days
    drops_for_days_vault = session_data.account.vault['Upgrades']['Drops for Days']
    drops_for_days_vault_level_max = drops_for_days_vault['Max Level']
    drops_for_days_vault_value_max = vault_mastery_vault_value_max * drops_for_days_vault_level_max * drops_for_days_vault['Value Per Level']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Upgrade Vault- Drops for Days:"
              f"<br>+{drops_for_days_vault['Total Value']:g}/{drops_for_days_vault_value_max:g}% Drop Rate",
        picture_class=drops_for_days_vault['Image'],
        progression=drops_for_days_vault['Level'],
        goal=drops_for_days_vault_level_max
    ))

    # Seige Breaker - Talents -  Archlord of the Pirates
    sb_talent = session_data.account.class_kill_talents['Archlord of the Pirates']
    goalString = notateNumber("Basic", 1e6, 1)
    sb_dict = class_kill_talents_dict['Archlord of the Pirates']
    sb_talent_bonus_max = lavaFunc(sb_dict['FuncType'], max(1000000, sb_talent['Kills']), sb_dict['X1'], sb_dict['X2'])
    drop_rate_aw_advice[general].append(Advice(
        label=f"Siege Breaker Talents- Archlord of the Pirates:"
              f"<br>+{round(sb_talent['Value'], 3):g}/{round(sb_talent_bonus_max, 3):g}% Drop Rate MULTI",
        picture_class='archlord-of-the-pirates',
        progression=notateNumber("Match", sb_talent['Kills'], 2, '', goalString),
        goal=goalString,
        resource='pirate-flag'
    ))

    # TODO: Grimoire - Skull of Major Droprate

    # Companions - Crystal Custard
    has_crystal_custard_companion = session_data.account.companions['Crystal Custard']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Companions- Crystal Custard:"
              f"<br>+{100 if has_crystal_custard_companion else 0}/100% Drop Rate"
              f"{missing_companion_data_txt}",
        picture_class='crystal-custard',
        progression=int(has_crystal_custard_companion),
        goal=1
    ))

    # Companions - Quenchie
    has_quenchie_companion = session_data.account.companions['Quenchie']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Companions- Quenchie:"
              f"<br>+{15 if has_quenchie_companion else 0}/15% Drop Rate"
              f"{missing_companion_data_txt}",
        picture_class='quenchie',
        progression=int(has_quenchie_companion),
        goal=1
    ))

    # Companions - Mallay
    has_mallay_companion = session_data.account.companions['Mallay']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Companions- Mallay:"
              f"<br>x{1.30 if has_mallay_companion else 0}/x1.3 Drop Rate MULTI"
              f"{missing_companion_data_txt}",
        picture_class='mallay',
        progression=int(has_mallay_companion),
        goal=1
    ))

    # Gem Shop - Deathbringer Pack
    has_bundle_data = session_data.account.gemshop['Bundle Data Present']
    has_db_pack = next((b['Owned'] for b in session_data.account.gemshop['Bundles'].values() if b['Display'] == 'Deathbringer Pack'), False)
    db_pack_drop_rate_text = f"+{200 if has_db_pack else 0}/200% Drop Rate" if has_bundle_data \
                          else "+200% Drop Rate<br>Note: Could be inaccurate. Bundle data not found!"
    drop_rate_aw_advice[general].append(Advice(
        label=f"Gemshop- Deathbringer Pack:"
              f"<br>{db_pack_drop_rate_text}",
        picture_class='gem',
        progression=int(has_db_pack) if has_bundle_data else 'IDK',
        goal=1
    ))

    # Gem Shop - Island Explorer Pack
    has_island_explorer_pack = next((b['Owned'] for b in session_data.account.gemshop['Bundles'].values() if b['Display'] == 'Island Explorer Pack'), False)
    island_explorer_drop_rate_text = f"x{1.2 if has_island_explorer_pack else 0}/x1.2 Drop Rate MULTI" if has_bundle_data \
                                 else "x1.2 Drop Rate MULTI<br>Note: Could be inaccurate. Bundle data not found!"
    drop_rate_aw_advice[general].append(Advice(
        label=f"Gemshop- Island Explorer Pack:"
              f"<br>{island_explorer_drop_rate_text}",
        picture_class='gem',
        progression=int(has_island_explorer_pack) if session_data.account.gemshop['Bundle Data Present'] else 'IDK',
        goal=1
    ))

    # World 1
    #########################################

    # Owl Bonuses
    drop_rate_aw_advice[w1].append(Advice(
        label=f"Bonuses of Orion- Drop Rate:"
              f"<br>+{session_data.account.owl['Bonuses']['Drop Rate']['Value']}% Drop Rate",
        picture_class='the-great-horned-owl',
        progression=max(0, session_data.account.owl['MegaFeathersOwned']-10),
        resource='megafeather-9',
        goal='∞'
    ))

    # Lab Nodes- Certified Stamp Book
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    golden_sixes_buffs = []
    has_certified_stamp_book = session_data.account.labBonuses['Certified Stamp Book']['Enabled']
    if not has_certified_stamp_book:
        golden_sixes_buffs.append('Lab')
        drop_rate_aw_advice[w1].append(Advice(
            label="Lab Nodes- Certified Stamp Book:"
                  "<br>x2 Non Misc Stamp Bonuses"
                  "<br>Note: improves the stamp below",
            picture_class='certified-stamp-book',
            progression=0, # we're only showing if it's missing, so just assume 0
            goal=1
        ))
    # Pristine Charm- Ligorice Rolle
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    has_liqorice_rolle = session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']
    if not has_liqorice_rolle:
        golden_sixes_buffs.append('Pristine Charm')
        drop_rate_aw_advice[w1].append(Advice(
            label="Pristine Charms- Liqorice Rolle:"
                  "<br>x1.25 Non Misc Stamp Bonuses"
                  "<br>Note: improves the stamp below",
            picture_class='liqorice-rolle',
            progression=0, # we're only showing if it's missing, so just assume 0
            goal=1
        ))
    # Stamps - Golden Sixes
    golden_sixes_stamp = session_data.account.stamps['Golden Sixes Stamp']
    has_exalted_golden_sixes = golden_sixes_stamp['Exalted']
    if not has_exalted_golden_sixes:
        golden_sixes_buffs.append('Exalted Stamps')
    match len(golden_sixes_buffs):
        case 0:
            golden_sixes_addl_text = "Note: can be further increased by the Abomination Slayer XVII compass bonus"
        case 1:
            golden_sixes_addl_text = f"Note: can be increased by {golden_sixes_buffs[0]}"
        case 2:
            golden_sixes_addl_text = f"Note: can be increased by {golden_sixes_buffs[0]} and {golden_sixes_buffs[1]}"
        case 3:
            golden_sixes_addl_text = f"Note: can be increased by {golden_sixes_buffs[0]}, {golden_sixes_buffs[1]}, and {golden_sixes_buffs[2]}"
    abomination_slayer_17 = session_data.account.compass['Upgrades']['Abomination Slayer XVII']
    exalted_stamp_bonus_value = ((abomination_slayer_17['Level'] * abomination_slayer_17['Value Per Level'])/100)
    exalted_stamp_multi = 2 + exalted_stamp_bonus_value
    # The exalted multiplier is the only multiplier that actually changes the base value on the stamp, we have to add the other 2 manually
    golden_sixes_value = round(golden_sixes_stamp['Value'] * \
            (2 if has_certified_stamp_book else 1) * \
            (1.25 if has_liqorice_rolle else 1) \
        , 2)
    golden_sixes_stamp_data = stampsDict['Combat'][37]
    golden_sixes_base_max = lavaFunc(golden_sixes_stamp_data['funcType'], golden_sixes_stamp['Max'], golden_sixes_stamp_data['x1'], golden_sixes_stamp_data['x2'])
    golden_sixes_value_max = round((golden_sixes_base_max * 2 * 1.35 * exalted_stamp_multi), 2)
    drop_rate_aw_advice[w1].append(Advice(
        label=f"Stamps- Golden Sixes:"
              f"<br>+{golden_sixes_value:g}/{golden_sixes_value_max}%"
              f"<br>{golden_sixes_addl_text}",
        picture_class='golden-sixes-stamp',
        progression=golden_sixes_stamp['Level'],
        resource=golden_sixes_stamp['Material'],
        goal=golden_sixes_stamp['Max']
    ))

    # World 2
    #########################################

    # Arcade - Shop Bonuses
    has_reindeer_companion = session_data.account.companions['Reindeer']
    if not has_reindeer_companion:
        drop_rate_aw_advice[w2].append(Advice(
            label=f"Companions- Reindeer:"
                f"<br>x{2 if has_reindeer_companion else 0}/x2 Arcade Bonus MULTI"
                f"<br>Note: increases the Arcade Bonus value below"
                f"{missing_companion_data_txt}",
            picture_class='spirit-reindeer',
            progression=int(has_reindeer_companion),
            goal=1
        ))
    drop_rate_arcade_bonus_id = 27
    _, drop_rate_arcade  = list(session_data.account.arcade.items())[drop_rate_arcade_bonus_id]
    drop_rate_aw_advice[w2].append(Advice(
        label=f"Arcade Bonus- % Drop Rate:"
              f"<br>+{drop_rate_arcade['Value']}/{drop_rate_arcade['MaxValue']}%"
              f"{missing_companion_data_txt}",
        picture_class=drop_rate_arcade['Image'],
        progression=drop_rate_arcade['Level'],
        resource='arcade-gold-ball',
        goal=101
    ))

    # Obols - Family - Drop Rate
    obol_family_drop_rate = session_data.account.obols['BonusTotals']['%_DROP_CHANCE']
    obol_family_drop_rate_max = max(124, obol_family_drop_rate)
    drop_rate_aw_advice[w2].append(Advice(
        label=f"Obols- Family Obols:"
              f"<br>+{obol_family_drop_rate}/{obol_family_drop_rate_max}% Drop Rate",
        picture_class='hyper-six-obol',
        progression=obol_family_drop_rate,
        goal=124
    ))

    # Question: Maybe up the goal to 6930 for +39.6% at 99% or 2730 for a nice round +39%?
    # Alchemy - Bubbles - Dropin Loads
    dropin_loads_bubble = session_data.account.alchemy_bubbles['Droppin Loads']
    droppin_loads_value_breakpoints = [
        [280, 32, 80],
        [630, 36, 90],
        [1330, 38, 95],
        [6930, 39.6, 99]
    ]
    droppin_loads_next_breakpoint = next(
        (b for b in droppin_loads_value_breakpoints if b[0] > dropin_loads_bubble['Level']),
        None
    )
    droppin_loads_breakpoint_txt = ''
    if droppin_loads_next_breakpoint != None:
        droppin_loads_breakpoint_txt = f"<br>Next breakpoint: {droppin_loads_next_breakpoint[2]}% value at level {droppin_loads_next_breakpoint[0]}"
    drop_rate_aw_advice[w2].append(Advice(
        label=f"Alchemy Bubbles- Droppin Loads:"
              f"<br>+{round(dropin_loads_bubble['BaseValue'], 1):g}/{droppin_loads_value_breakpoints[-1][1]}% Drop Rate"
              f"{droppin_loads_breakpoint_txt}",
        picture_class='droppin-loads',
        progression=dropin_loads_bubble['Level'],
        resource=dropin_loads_bubble['Material'],
        goal=droppin_loads_value_breakpoints[-1][0]
    ))

    # Artifacts- Chilled Yarn
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    chilled_yarn_artifact_level = session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']
    chilled_yarn_value = 2 * chilled_yarn_artifact_level
    chilled_yarn_max = 2 * numberOfArtifactTiers
    if chilled_yarn_artifact_level < numberOfArtifactTiers:
        drop_rate_aw_advice[w2].append(Advice(
            label=f"Artifacts- Chilled Yarn:"
                  f"<br>x{chilled_yarn_value}/x{chilled_yarn_max} Sigil Bonuses"
                  f"<br>Note: improves the sigil below",
            picture_class='chilled-yarn',
            progression=chilled_yarn_value,
            goal=numberOfArtifactTiers
        ))
    # Alchemy - Sigils - Clover
    trove_sigil_level = session_data.account.alchemy_p2w['Sigils']['Trove']['Level']
    trove_sigil_value = sigilsDict['Trove']['Values'][trove_sigil_level-1] * chilled_yarn_value
    trove_sigil_value_max = sigilsDict['Trove']['Values'][max_IndexOfSigils-1] * chilled_yarn_max
    drop_rate_aw_advice[w2].append(Advice(
        label=f"Sigils- Clover Sigil:"
              f"<br>+{trove_sigil_value}/{trove_sigil_value_max}% Drop Rate",
        picture_class='trove',
        progression=trove_sigil_level,
        goal=max_IndexOfSigils
    ))

    # World 3
    #########################################

    # Equinox - Faux Jewels
    # Will show additional info if player is maxed out for their currently available levels
    faux_jewels_bonus = session_data.account.equinox_bonuses['Faux Jewels']
    faux_jewels_level = faux_jewels_bonus['CurrentLevel']
    drop_rate_aw_advice[w3].append(Advice(
        label=f"Equinox- Faux Jewels:"
              f"<br>+{5 * faux_jewels_level}% Drop Rate (+5% per level)"
              f"{'<br>Note: increase Faux Jewels max level with Endless Summoning' if faux_jewels_level == faux_jewels_bonus['PlayerMaxLevel'] else ''}",
        picture_class='faux-jewels',
        progression=faux_jewels_level,
         # This is technically infinite with Endless Summoning wins, but we'll just show what's currently unlocked with a note about ES
        goal=faux_jewels_bonus['FinalMaxLevel']
    ))

    # Construction - Shrine - Clover Shrine
    chaotic_chizoar_card = next(c for c in session_data.account.cards if c.name == 'Chaotic Chizoar')
    shrine_exta_bonus_text = ''
    if chaotic_chizoar_card.getStars() < (cards_max_level-1):
        drop_rate_aw_advice[w3].append(chaotic_chizoar_card.getAdvice())
        shrine_exta_bonus_text = '<br>Note: can be increased by getting more Chaotic Chizoar card stars'
    drop_rate_aw_advice[w3].append(Advice(
        label=f"Shrines- Clover Shrine:"
              f"<br>+{session_data.account.shrines['Clover Shrine']['Value']:g}% Drop Rate (15% base + 3% per level)"
              f"{shrine_exta_bonus_text}",
        picture_class='clover-shrine',
        progression=session_data.account.shrines['Clover Shrine']['Level'],
        goal='∞'
    ))

    # World 4
    #########################################

    # Breeding - Shiny Pets
    drop_rate_shiny_level = 0
    drop_rate_shiny_value = 0
    for name, shiny in session_data.account.breeding['Species'][1].items():
        if shiny['ShinyBonus'] == 'Drop Rate':
            drop_rate_shiny_level += shiny['ShinyLevel']
            drop_rate_shiny_value += drop_rate_shiny_base * shiny['ShinyLevel']
    drop_rate_aw_advice[w4].append(Advice(
        label=f"Breeding- Shiny Critters:"
              f"<br>+{drop_rate_shiny_value}% Drop Rate (+1% per critter level)",
        picture_class='breeding',
        progression=drop_rate_shiny_level,
        goal='∞'
    ))

    # Rift - Sneak Mastery 1
    sneak_mastery_level = session_data.account.sneaking['MaxMastery']
    drop_rate_aw_advice[w4].append(Advice(
        label=f"Rift- Sneaking Mastery:"
              f"<br>+{30 if (sneak_mastery_level > 0) else 0}/30% Drop Rate",
        picture_class='sneaking-mastery',
        progression=sneak_mastery_level,
        goal=1
    ))

    # World 5
    #########################################
    # Caverns - Schematics - Gloomie Lootie
    grotto_cavern = session_data.account.caverns['Caverns']['Grotto']
    gloomie_lootie_schematic = session_data.account.caverns['Schematics']['Gloomie Lootie']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"Engineer Schematics- Gloomie Lootie:"
              f"<br>+{5 * grotto_cavern['OpalsFound']}% Drop Rate (+5% per Cavern cleared)",
        picture_class=gloomie_lootie_schematic['Image'],
        progression=grotto_cavern['OpalsFound'] if gloomie_lootie_schematic['Purchased'] else 0,
        goal='∞'
    ))

    # Caverns - Schematics - Sanctum of LOOT
    temple_cavern = session_data.account.caverns['Caverns']['The Temple']
    sanctum_of_loot_schematic = session_data.account.caverns['Schematics']['Sanctum of LOOT']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"Engineer Schematics- Sanctum of LOOT:"
              f"<br>+{20 * temple_cavern['OpalsFound']}% Drop Rate (+20% per Sanctum cleared)",
        picture_class=sanctum_of_loot_schematic['Image'],
        progression=temple_cavern['OpalsFound'] if sanctum_of_loot_schematic['Purchased'] else 0,
        goal='∞'
    ))

    # Caverns - Schematics - Wisdom Monument
    wisdom_drop_rate_index = 26
    wisdom_monument_drop_rate = session_data.account.caverns['Caverns']['Wisdom Monument']['Bonuses'][wisdom_drop_rate_index]
    drop_rate_aw_advice[w5].append(Advice(
        label=f"Caverns- Wisdom Monument:"
              f"<br>+{wisdom_monument_drop_rate['Value']}% Drop Rate",
        picture_class='cavern-13',
        progression=wisdom_monument_drop_rate['Level'],
        goal='∞'
    ))

    # World 6
    #########################################

    # Achievements - Big Big Hampter
    drop_rate_aw_advice[w6].append(Advice(
        label='Achievements- Big Big Hampter:'
              '<br>+4% Drop Rate',
        picture_class='big-big-hampter',
        progression=1 if session_data.account.achievements['Big Big Hampter']['Complete'] else 0,
        goal=1
    ))

    # Achievements - Summoning GM
    drop_rate_aw_advice[w6].append(Advice(
        label='Achievements- Summoning GM:'
              '<br>+6% Drop Rate',
        picture_class='summoning-gm',
        progression=int(session_data.account.achievements['Summoning GM']['Complete']),
        goal=1
    ))

    # Farming - Crop Depot - Highlighter
    crops_unlocked = session_data.account.farming['CropsUnlocked']
    crops_highlighter_value = (crops_unlocked - 100) if (crops_unlocked > 100) else 0
    crops_highlighter_value_max = (maxFarmingCrops - 100)
    drop_rate_aw_advice[w6].append(Advice(
        label=f"Crop Depot- Highlighter:"
              f"<br>+{crops_highlighter_value}/{crops_highlighter_value_max}% Drop Rate"
              f"<br>{'Note: value only increases after 100 crops found' if (crops_unlocked <= 100) else ''}",
        picture_class='depot-highlighter',
        progression=crops_unlocked,
        goal=maxFarmingCrops
    ))

    # Farming - Land Rank - Seed of Loot
    # Will show additional info if the player does not have the current max number of available land rank levels
    seed_of_loot_land_rank = session_data.account.farming['LandRankDatabase']['Seed of Loot']
    seed_of_loot_value = seed_of_loot_land_rank['BaseValue'] * seed_of_loot_land_rank['Level']
    seed_of_loot_value_max = seed_of_loot_land_rank['BaseValue'] * max_land_rank_level
    drop_rate_aw_advice[w6].append(Advice(
        label=f"Land Ranks- Seed of Loot:"
              f"<br>+{seed_of_loot_value}/{seed_of_loot_value_max}% Drop Rate"
              f"{'<br>Note: increase Land Rank max with Death Bringer Grimoire' if seed_of_loot_land_rank['Level'] < max_land_rank_level else ''}",
        picture_class='seed-of-loot',
        progression=seed_of_loot_land_rank['Level'],
        goal=max_land_rank_level
    ))

    # Sneaking - Pristine Charm - Cotton Candy
    cotton_candy_obtained = session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']
    drop_rate_aw_advice[w6].append(Advice(
        label=f"Pristine Charms- Cotton Candy:"
              f"<br>{'x1.15' if cotton_candy_obtained else '0%'} Drop Rate MULTI",
        picture_class='cotton-candy-charm',
        progression=int(cotton_candy_obtained),
        goal=1
    ))

    # Sneaking - Beanstalk - Golden Cake
    cake_beanstalk_name ='FoodG13'
    cake_beanstalk = session_data.account.sneaking['Beanstalk'][cake_beanstalk_name]
    cake_beanstalk_level = int(cake_beanstalk['Beanstacked']) + int(cake_beanstalk['SuperBeanstacked'])
    if cake_beanstalk_level == 2:
        cake_beanstalk_bonus = '+6.67'
    elif cake_beanstalk_level == 1:
        cake_beanstalk_bonus = '+4.59'
    else:
        cake_beanstalk_bonus = '0%'
    drop_rate_aw_advice[w6].append(Advice(
        label=f"Beanstalk- Golden Cake:"
              f"<br>{cake_beanstalk_bonus}/6.67% Drop Rate"
              f"<br>Note: further increased by Golden Food bonuses",
        picture_class='golden-cake',
        progression=cake_beanstalk_level,
        goal=2
    ))

    # Summoning - Bonuses
    summoning_battles = session_data.account.summoning['Battles']
    yellow_3_drop_rate = 7 if summoning_battles['Yellow'] >= 3 else 0
    blue_9_drop_rate = 10.5 if summoning_battles['Blue'] >= 9 else 0
    purple_12_drop_rate = 17.5 if summoning_battles['Purple'] >= 12 else 0
    red_13_drop_rate = 35 if summoning_battles['Red'] >= 13 else 0
    summoning_drop_rate_base = yellow_3_drop_rate + blue_9_drop_rate + purple_12_drop_rate + red_13_drop_rate
    endless_summon_bonus_multi = .03 * ((floor(summoning_battles['Endless']/40) * 2) + (1 if summoning_battles['Endless'] % 40 > 16 else 0))
    other_summon_bonus_multi = (.01 if session_data.account.achievements['Regalis My Beloved']['Complete'] else 0) \
        + (.01 if session_data.account.achievements['Spectre Stars']['Complete'] else 0) \
        + (.25 * session_data.account.sailing['Artifacts']['The Winz Lantern']['Level']) \
        + (.01 * session_data.account.merits[5][4]['Level'])
    prisine_charm_summon_bonus_multi = 1.3 if session_data.account.sneaking['PristineCharms']['Crystal Comb']['Obtained'] else 1
    # The bonuses from endless summoning and everything else, except the pristine charm are addative. The charm is a multi
    total_summon_bonus_multi = (1 + endless_summon_bonus_multi + other_summon_bonus_multi) * prisine_charm_summon_bonus_multi
    summoning_drop_rate_value = round(summoning_drop_rate_base * total_summon_bonus_multi, 2)
    summoning_drop_rate_max = round((7 + 10.5 + 17.5 + 35) * total_summon_bonus_multi, 2)
    drop_rate_aw_advice[w6].append(Advice(
        label=f"Summoning Bonuses- Drop Rate:"
              f"<br>+{summoning_drop_rate_value:g}/{summoning_drop_rate_max:g} Drop Rate",
        picture_class='summoning',
        progression=int(session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']),
        goal='∞'
    ))

    for subgroup in drop_rate_aw_advice:
        for advice in drop_rate_aw_advice[subgroup]:
            mark_advice_completed(advice)

    drop_rate_ag = AdviceGroup(
        tier="",
        pre_string="Info- Account wide sources of Drop Rate",
        advices=drop_rate_aw_advice,
        informational=True,
    )
    return drop_rate_ag

def get_drop_rate_player_advice_group():
    bnn_cardset = []
    events_cardset = []
    for card in session_data.account.cards:
        if card.cardset == 'Bosses n Nightmares':
            bnn_cardset.append(card)
        if card.cardset == 'Events':
            events_cardset.append(card)

    drop_rate_pp_advice = {
        general: [],
        w1: [],
        w2: [],
        w3: [],
        w4: [],
        w5: [],
        w6: []
    }

    card_drop_rate = []
    for card in session_data.account.cards:
        if card.name in drop_rate_cards:
            card_drop_rate.append(card)
    card_drop_rate.sort(key=lambda c: c.getCurrentValue(), reverse=True)
    best_2_cards = 0
    for card in card_drop_rate:
        end_note = ''
        if best_2_cards < 2:
            end_note = f"Note: place in the {'TOP LEFT' if best_2_cards == 0 else 'BOTTOM RIGHT'} card slot"
            best_2_cards += 1
        print("END NOTE: " + end_note)
        drop_rate_pp_advice[general].append(card.getAdvice(optional_ending_note=end_note))

    # Card Sets - Bosses n Nightmares
    bnn_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in bnn_cardset)
    bnn_star, _ = divmod(bnn_stars_sum, len(bnn_cardset))
    bnn_star = min(bnn_star, max_card_stars)
    bnn_star_next = (bnn_star + 1) * len(bnn_cardset)
    drop_rate_pp_advice[general].append(Advice(
        label=f"Bosses n Nightmares- Card Set:"
              f"<br>+{6 * bnn_star}/{6 * (1 + max_card_stars)}% Drop Rate"
              f"<br>Cards until next set level {bnn_stars_sum}/{bnn_star_next}",
        picture_class='bosses-n-nightmares',
        progression=bnn_star,
        goal=6
    ))

    # Cards Sets - Events
    events_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in events_cardset)
    events_star, _ = divmod(events_stars_sum, len(events_cardset))
    events_star = min(events_star, max_card_stars)
    events_star_next = (events_star + 1) * len(events_cardset)
    drop_rate_pp_advice[general].append(Advice(
        label=f"Events- Card Set:"
              f"<br>+{7 * events_star}/{7 * (1 + max_card_stars)}% Drop Rate"
              f"<br>Cards until next set level {events_stars_sum}/{events_star_next}",
        picture_class='events',
        progression=events_star,
        goal=6
    ))

    drop_rate_ag = AdviceGroup(
        tier="",
        pre_string="Info- Player specific sources of Drop Rate",
        advices=drop_rate_pp_advice,
        informational=True,
    )
    return drop_rate_ag

def get_progression_tiers_advice_group() -> tuple[AdviceGroup, int, int, int]:
    template_advice_dict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0 - info_tiers
    tier_Active = 0

    #Assess Tiers
    tiers_ag = AdviceGroup(
        tier=tier_Active,
        pre_string="Progression Tiers",
        advices=template_advice_dict['Tiers']
    )
    overall_section_tier = min(max_tier + info_tiers, tier_Active)
    return tiers_ag, overall_section_tier, max_tier, max_tier + info_tiers

def get_drop_rate_advice_section() -> AdviceSection:
    # Generate AdviceGroups
    drop_rate_advice_group_dict = {}
    drop_rate_advice_group_dict['Tiers'], overall_section_tier, max_tier, true_max = get_progression_tiers_advice_group()
    drop_rate_advice_group_dict['Account'] = get_drop_rate_account_advice_group()
    drop_rate_advice_group_dict['Player'] = get_drop_rate_player_advice_group()

    # Generate AdviceSection

    tier_section = f"{overall_section_tier}/{max_tier}"
    drop_rate_advice_section = AdviceSection(
        name="Drop Rate",
        tier=tier_section,
        pinchy_rating=overall_section_tier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Drop Rate Information",
        picture='data/VaultUpg18.png',
        groups=drop_rate_advice_group_dict.values(),
        unrated=True,
    )
    return drop_rate_advice_section
