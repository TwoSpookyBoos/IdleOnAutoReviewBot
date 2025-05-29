from consts.progression_tiers_updater import true_max_tiers
from models.models import Advice, AdviceGroup, AdviceSection
from consts.consts import ValueToMulti, EmojiType
from consts.consts_idleon import lavaFunc
from consts.consts_general import max_card_stars, cards_max_level, equipment_by_bonus_dict
from consts.consts_w6 import max_farming_crops, max_land_rank_level
from consts.consts_w5 import max_sailing_artifact_level
from consts.consts_w4 import rift_rewards_dict, shiny_days_list
from consts.consts_w3 import buildings_dict, prayers_dict, approx_max_talent_level_non_es
from consts.consts_w2 import max_sigil_level, sigils_dict, po_box_dict, obols_max_bonuses_dict
from consts.consts_w1 import stamp_maxes, starsigns_dict
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import notateNumber
from utils.logging import get_logger
from math import floor, ceil
from flask import g as session_data

logger = get_logger(__name__)


drop_rate_shiny_base = 1
infinite_star_sign_shiny_base = 2

def get_drop_rate_account_advice_group() -> AdviceGroup:
    missing_companion_data_txt = '<br>Note: Could be inaccurate. Companion data not found!' if not session_data.account.companions['Companion Data Present'] else ''
    missing_companion_data = not session_data.account.companions['Companion Data Present']
    missing_bundle_data_txt = '<br>Note: Could be inaccurate. Bundle data not found!' if not session_data.account.gemshop['Bundle Data Present'] else ''
    missing_bundle_data = not session_data.account.gemshop['Bundle Data Present']
    passive_drop_rate_cards = [
        'Domeo Magmus',
        'Ancient Golem',
        'IdleOn Fourth Anniversary'
    ]

    general = 'General'
    mc = 'Master Classes'
    w1 = 'World 1'
    w2 = 'World 2'
    w3 = 'World 3'
    w4 = 'World 4'
    w5 = 'World 5'
    w6 = 'World 6'
    drop_rate_aw_advice = {
        general: [],
        mc: [],
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
        ruby_cards_rift_level = next(i for i, r in rift_rewards_dict.items() if r['Shorthand'] == 'RubyCards')
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
              f"<br>+{round(gold_charm_bonus['Value'], 2):g}/{round(gold_charm_bonus['Max Value'], 2):g}% Drop Rate",
        picture_class=gold_charm_bonus['Image'],
        progression=gold_charm_bonus['Level'],
        goal=gold_charm_bonus['Max Level']
    ))

    # Upgrade Vault - Vault Mastery
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    vault_mastery_vault = session_data.account.vault['Upgrades']['Vault Mastery']
    vault_mastery_vault_value_max = ValueToMulti(vault_mastery_vault['Max Level'] * vault_mastery_vault['Value Per Level'])
    if vault_mastery_vault['Level'] < vault_mastery_vault['Max Level']:
        drop_rate_aw_advice[general].append(Advice(
            label=f"{{{{ Upgrade Vault|#upgrade-vault }}}}- Vault Mastery:"
                  f"<br>{round(vault_mastery_vault['Total Value'], 2):g}/{round(vault_mastery_vault_value_max, 2):g}x blue highlighted vault bonuses"
                  f"<br>(increases the value of the Vault upgrade below)",
            picture_class=vault_mastery_vault['Image'],
            progression=vault_mastery_vault['Level'],
            goal=vault_mastery_vault['Max Level']
        ))
    # Upgrade Vault - Drops for Days
    drops_for_days_vault = session_data.account.vault['Upgrades']['Drops for Days']
    drops_for_days_vault_level_max = drops_for_days_vault['Max Level']
    drops_for_days_vault_value_max = vault_mastery_vault_value_max * drops_for_days_vault_level_max * drops_for_days_vault['Value Per Level']
    drop_rate_aw_advice[general].append(Advice(
        label=f"{{{{ Upgrade Vault|#upgrade-vault }}}}- Drops for Days:"
              f"<br>+{round(drops_for_days_vault['Total Value'], 2):g}/{round(drops_for_days_vault_value_max, 2):g}% Drop Rate",
        picture_class=drops_for_days_vault['Image'],
        progression=drops_for_days_vault['Level'],
        goal=drops_for_days_vault_level_max
    ))

    # Siege Breaker - Talents -  Archlord of the Pirates
    sb_talent = session_data.account.class_kill_talents['Archlord of the Pirates']
    goal_string = notateNumber('Basic', 1e6, 2)
    sb_talent_bonus_max = lavaFunc(sb_talent['funcType'], approx_max_talent_level_non_es, sb_talent['x1'], sb_talent['x2']) * sb_talent['Kill Stacks']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Siege Breaker talent- Archlord of the Pirates:"
              f"<br>Level {sb_talent['Highest Preset Level']}/{approx_max_talent_level_non_es} with your current kills gives"
              f"<br>{round(ValueToMulti(sb_talent['Total Value']), 5):g}/{round(ValueToMulti(sb_talent_bonus_max), 5):g}x Drop Rate MULTI",
        picture_class='archlord-of-the-pirates',
        progression=notateNumber('Match', sb_talent['Kills'], 2, '', goal_string),
        goal=goal_string,
        resource='pirate-flag'
    ))

    # Companions - Crystal Custard
    has_crystal_custard_companion = session_data.account.companions['Crystal Custard']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Companions- Crystal Custard:"
              f"<br>+{100 if has_crystal_custard_companion else 0}/100% Drop Rate"
              f"{missing_companion_data_txt}",
        picture_class='crystal-custard',
        progression=int(has_crystal_custard_companion) if not missing_companion_data else 'IDK',
        goal=1
    ))

    # Companions - Quenchie
    has_quenchie_companion = session_data.account.companions['Quenchie']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Companions- Quenchie:"
              f"<br>+{15 if has_quenchie_companion else 0}/15% Drop Rate"
              f"{missing_companion_data_txt}",
        picture_class='quenchie',
        progression=int(has_quenchie_companion) if not missing_companion_data else 'IDK',
        goal=1
    ))

    # Companions - Mallay
    has_mallay_companion = session_data.account.companions['Mallay']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Companions- Mallay:"
              f"<br>{1.3 if has_mallay_companion else 0}/1.3x Drop Rate MULTI"
              f"{missing_companion_data_txt}",
        picture_class='mallay',
        progression=int(has_mallay_companion) if not missing_companion_data else 'IDK',
        goal=1
    ))

    # Gem Shop - Deathbringer Pack
    has_db_pack = session_data.account.gemshop['Bundles']['bun_v']['Owned']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Gemshop- Deathbringer Pack:"
              f"<br>+{200 if has_db_pack else 0}/200% Drop Rate"
              f"{missing_bundle_data_txt}",
        picture_class='gem',
        progression=int(has_db_pack) if not missing_bundle_data else 'IDK',
        goal=1
    ))

    # Gem Shop - Island Explorer Pack
    has_island_explorer_pack = session_data.account.gemshop['Bundles']['bun_p']['Owned']
    drop_rate_aw_advice[general].append(Advice(
        label=f"Gemshop- Island Explorer Pack:"
              f"<br>{1.2 if has_island_explorer_pack else 0}/1.2x Drop Rate MULTI"
              f"{missing_bundle_data_txt}",
        picture_class='gem',
        progression=int(has_island_explorer_pack) if not missing_bundle_data else 'IDK',
        goal=1
    ))

    # Master Classes
    #########################################
    # Grimoire - Skull of Major Droprate
    skull_drop_rate_grimoire = session_data.account.grimoire['Upgrades']['Skull of Major Droprate']
    skull_drop_rate_grimoire_upgrades_unlock = skull_drop_rate_grimoire['Unlock Requirement'] - session_data.account.grimoire['Total Upgrades']
    drop_rate_aw_advice[mc].append(Advice(
        label=f"{{{{Grimoire|#the-grimoire}}}}- Skull of Major Droprate:"
              f"<br>+{round(skull_drop_rate_grimoire['Total Value'], 1):g}% Drop Rate"
              f"{f'<br>Requires {skull_drop_rate_grimoire_upgrades_unlock} more upgrades to unlock' if skull_drop_rate_grimoire_upgrades_unlock > 0 else ''}",
        picture_class=skull_drop_rate_grimoire['Image'],
        progression=skull_drop_rate_grimoire['Level'],
        goal=skull_drop_rate_grimoire['Max Level']
    ))

    # World 1
    #########################################

    # Owl Bonuses
    drop_rate_aw_advice[w1].append(Advice(
        label=f"{{{{ Owl|#owl }}}}- Drop Rate:"
              f"<br>+{session_data.account.owl['Bonuses']['Drop Rate']['Value']}% Drop Rate",
        picture_class='the-great-horned-owl',
        progression=max(0, session_data.account.owl['MegaFeathersOwned']-10),
        resource='megafeather-9',
        goal=EmojiType.INFINITY.value
    ))

    # Lab Nodes- Certified Stamp Book
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    golden_sixes_buffs = []
    has_certified_stamp_book = session_data.account.labBonuses['Certified Stamp Book']['Enabled']
    if not has_certified_stamp_book:
        golden_sixes_buffs.append('Lab')
        drop_rate_aw_advice[w1].append(Advice(
            label=f"{{{{ Lab Nodes|#lab }}}}- Certified Stamp Book:"
                  "<br>x2 Non-Misc Stamp Bonuses"
                  "<br>Note: Improves the stamp below",
            picture_class='certified-stamp-book',
            progression=int(has_certified_stamp_book),
            goal=1
        ))
    # Pristine Charm- Liqorice Rolle
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    has_liqorice_rolle = session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']
    if not has_liqorice_rolle:
        golden_sixes_buffs.append('Pristine Charm')
        drop_rate_aw_advice[w1].append(Advice(
            label="Pristine Charms- Liqorice Rolle:"
                  f"<br>{1.25 if has_liqorice_rolle else 0}/1.25x Non Misc Stamp Bonuses"
                  "<br>Note: improves the stamp below",
            picture_class='liqorice-rolle',
            progression=int(has_liqorice_rolle),
            goal=1
        ))
    # Stamps - Golden Sixes
    golden_sixes_stamp = session_data.account.stamps['Golden Sixes Stamp']
    if not golden_sixes_stamp['Exalted']:
        golden_sixes_buffs.append('Exalting the stamp')
    if len(golden_sixes_buffs) == 0:
        golden_sixes_addl_text = f"Note: Can be further increased by Exalted {{{{Stamp|#stamps}}}} bonuses"
    else:
        golden_sixes_addl_text = f"Note: Can be increased by " + ", ".join(golden_sixes_buffs)

    drop_rate_aw_advice[w1].append(Advice(
        label=f"{{{{ Stamps|#stamps }}}}- Golden Sixes:"
              f"<br>+{round(golden_sixes_stamp['Total Value'], 2):g}% Drop Rate"
              f"<br>{golden_sixes_addl_text}",
        picture_class='golden-sixes-stamp',
        progression=golden_sixes_stamp['Level'],
        resource=golden_sixes_stamp['Material'],
        goal=stamp_maxes['Golden Sixes Stamp'] if golden_sixes_stamp['Delivered'] else 1
    ))

    # World 2
    #########################################

    # Arcade - Shop Bonuses
    has_reindeer_companion = session_data.account.companions['Reindeer']
    if not has_reindeer_companion:
        drop_rate_aw_advice[w2].append(Advice(
            label=f"Companions- Reindeer:"
                  f"<br>{2 if has_reindeer_companion else 0}/2x Arcade Bonus MULTI"
                  f"<br>Note: Increases the Arcade Bonus value below"
                  f"{missing_companion_data_txt}",
            picture_class='spirit-reindeer',
            progression=int(has_reindeer_companion) if not missing_companion_data else 'IDK',
            goal=1
        ))

    drop_rate_arcade = session_data.account.arcade[27]
    drop_rate_aw_advice[w2].append(Advice(
        label=f"{{{{ Arcade|#arcade }}}}- Drop Rate:"
              f"<br>+{drop_rate_arcade['Value']:g}/{drop_rate_arcade['MaxValue']:g}% Drop Rate"
              f"{missing_companion_data_txt}",
        picture_class=drop_rate_arcade['Image'],
        progression=drop_rate_arcade['Level'],
        resource='arcade-gold-ball',
        goal=101
    ))

    # Obols - Family - Drop Rate
    obols_family_drop_rate = session_data.account.obols['BonusTotals'].get('Total%_DROP_CHANCE', 0)
    obols_family_drop_rate_max = obols_max_bonuses_dict['FamilyDropRateTrue']
    obols_family_note = '<br>Note: Includes Rare and Hyper Obols, each rerolled with +1% DR'
    drop_rate_aw_advice[w2].append(Advice(
        label=f"Obols- Family Obols:"
              f"<br>+{obols_family_drop_rate}/{obols_family_drop_rate_max}% Drop Rate"
              f"{obols_family_note}",
        picture_class='hyper-six-obol',
        progression=obols_family_drop_rate,
        goal=obols_family_drop_rate_max
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
    droppin_loads_breakpoint_txt = (
        f"<br>Next breakpoint: {droppin_loads_next_breakpoint[2]}% value at level {droppin_loads_next_breakpoint[0]}"
        if droppin_loads_next_breakpoint is not None else ''
    )
    drop_rate_aw_advice[w2].append(Advice(
        label=f"{{{{ Alchemy Bubbles|#bubbles }}}}- Droppin Loads:"
              f"<br>+{round(dropin_loads_bubble['BaseValue'], 2):g}/{droppin_loads_value_breakpoints[-1][1]}% Drop Rate"
              f"{droppin_loads_breakpoint_txt}",
        picture_class='droppin-loads',
        progression=dropin_loads_bubble['Level'],
        resource=dropin_loads_bubble['Material'],
        goal=droppin_loads_value_breakpoints[-1][0]
    ))

    # Artifacts- Chilled Yarn
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    chilled_yarn_artifact_level = session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']
    chilled_yarn_multi = ValueToMulti(100 * session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'])
    chilled_yarn_max = ValueToMulti(100 * max_sailing_artifact_level)
    if chilled_yarn_artifact_level < max_sailing_artifact_level:
        drop_rate_aw_advice[w2].append(Advice(
            label=f"{{{{ Artifacts|#artifacts }}}}- Chilled Yarn:"
                  f"<br>{round(chilled_yarn_multi, 2):g}/{round(chilled_yarn_max, 2):g}x Sigil Bonuses"
                  f"<br>Note: Improves the sigil below",
            picture_class='chilled-yarn',
            progression=chilled_yarn_artifact_level,
            goal=max_sailing_artifact_level
        ))
    # Alchemy - Sigils - Clover
    trove_sigil_level = session_data.account.alchemy_p2w['Sigils']['Trove']['Level']
    trove_sigil_value = sigils_dict['Trove']['Values'][trove_sigil_level - 1] * chilled_yarn_multi
    trove_sigil_value_max = sigils_dict['Trove']['Values'][max_sigil_level - 1] * chilled_yarn_max
    drop_rate_aw_advice[w2].append(Advice(
        label=f"{{{{ Sigils|#sigils }}}}- Clover Sigil:"
              f"<br>+{trove_sigil_value}/{trove_sigil_value_max}% Drop Rate",
        picture_class='trove',
        progression=trove_sigil_level,
        goal=max_sigil_level
    ))

    # World 3
    #########################################

    # Equinox - Faux Jewels
    # Will show additional info if player is maxed out for their currently available levels
    faux_jewels_bonus = session_data.account.equinox_bonuses['Faux Jewels']
    faux_jewels_level = faux_jewels_bonus['CurrentLevel']
    faux_jewels_max_current = max(faux_jewels_bonus['FinalMaxLevel'], faux_jewels_bonus['PlayerMaxLevel'])
    faux_jewels_at_current_max = faux_jewels_level == faux_jewels_bonus['PlayerMaxLevel'] and faux_jewels_bonus['PlayerMaxLevel'] != 0
    drop_rate_aw_advice[w3].append(Advice(
        label=f"{{{{ Equinox|#equinox }}}}- Faux Jewels:"
              f"<br>+{5 * faux_jewels_level}/{5 * faux_jewels_max_current}% Drop Rate (+5% per level)"
              f"{'<br>Note: Increase Faux Jewels max level with {{Endless Summoning|#summoning}}' if faux_jewels_at_current_max else ''}",
        picture_class='faux-jewels',
        progression=faux_jewels_level,
        # This is technically infinite with Endless Summoning wins, but we'll just show what's currently unlocked with a note about ES
        goal=faux_jewels_max_current
    ))

    # Construction - Shrine - Clover Shrine
    chaotic_chizoar_card = next(c for c in session_data.account.cards if c.name == 'Chaotic Chizoar')
    shrine_exta_bonus_text = ''
    if chaotic_chizoar_card.getStars() < (cards_max_level-1):
        drop_rate_aw_advice[w3].append(chaotic_chizoar_card.getAdvice())
        shrine_exta_bonus_text = '<br>Note: Can be increased by getting more Chaotic Chizoar card stars'
    drop_rate_aw_advice[w3].append(Advice(
        label=f"Shrines- Clover Shrine:"
              f"<br>+{round(session_data.account.shrines['Clover Shrine']['Value'], 2):g}% Drop Rate "
              f"({buildings_dict[22]['ValueBase']}% base + {buildings_dict[22]['ValueIncrement']}% per level)"
              f"{shrine_exta_bonus_text}",
        picture_class='clover-shrine',
        progression=session_data.account.shrines['Clover Shrine']['Level'],
        goal=EmojiType.INFINITY.value
    ))

    # World 4
    #########################################

    # Breeding - Shiny Pets
    for world in session_data.account.breeding['Species']:
        for shiny_name, shiny_details in session_data.account.breeding['Species'][world].items():
            if shiny_details['ShinyBonus'] == 'Drop Rate':
                drop_rate_aw_advice[w4].append(Advice(
                    label=f"{{{{ Breeding|#breeding }}}}- Shiny {shiny_name}: +{shiny_details['ShinyLevel']}/{len(shiny_days_list)}%",
                    picture_class=shiny_name,
                    progression=shiny_details['ShinyLevel'],
                    goal=len(shiny_days_list)
                ))

    # Rift - Sneak Mastery 1
    sneak_mastery_level = session_data.account.sneaking['MaxMastery']
    drop_rate_aw_advice[w4].append(Advice(
        label=f"{{{{ Rift|#rift }}}}- Sneaking Mastery:"
              f"<br>+{30 if (sneak_mastery_level > 0) else 0}/30% Drop Rate",
        picture_class='sneaking-mastery',
        progression=min(1, sneak_mastery_level),
        goal=1
    ))

    # The Tome
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    grey_tome_book = session_data.account.grimoire['Upgrades']['Grey Tome Book']
    if grey_tome_book['Level'] < grey_tome_book['Max Level']:
        upgrades_to_unlock = grey_tome_book['Unlock Requirement'] - session_data.account.grimoire['Total Upgrades']
        drop_rate_aw_advice[w4].append(Advice(
            label=f"{{{{Grimoire|#the-grimoire}}}}: Grey Tome Book:"
                  f"<br>{round(grey_tome_book['Total Value'], 2):g}x higher bonus from Tome Red Pages"
                  f"{f'<br>Requires {upgrades_to_unlock} more upgrades to unlock' if upgrades_to_unlock > 0 else ''}",
            picture_class=session_data.account.grimoire['Upgrades']['Grey Tome Book']['Image'],
            progression=grey_tome_book['Level'],
            goal=grey_tome_book['Max Level']
        ))
    drop_rate_aw_advice[w4].append(Advice(
        label=f"""Tome- Red Pages:"""
              f"""<br>+{round(session_data.account.tome['Bonuses']['Drop Rarity']['Total Value'], 3):g}% Drop Rate"""
              f"""<br>{'Unknown, sorry 🙁' if not session_data.account.tome['Data Present'] else ''}"""
              f"""{f"{session_data.account.tome['Total Points']:,}" if session_data.account.tome['Data Present'] else ''} Total Tome Points"""
              f"""<br>Increases every 100 points over 8000""",
        picture_class='red-tome-pages',
        progression=session_data.account.tome['Red Pages Unlocked'],
        goal=1
    ))

    # World 5
    #########################################

    # Caverns - Measurments - Yards
    caverns_measurements_yards = session_data.account.caverns['Measurements'][15]
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Caverns|#villagers }}}}: Measurement 15:"
              f"<br>+{round(caverns_measurements_yards['Value'], 1):g}% Drop Rate (scales with {caverns_measurements_yards['ScalesWith']})",
        picture_class=caverns_measurements_yards['Image'],
        progression=caverns_measurements_yards['Level'],
        goal=EmojiType.INFINITY.value
    ))

    # Caverns - Schematics - Gloomie Lootie
    grotto_cavern = session_data.account.caverns['Caverns']['Grotto']
    gloomie_lootie_schematic = session_data.account.caverns['Schematics']['Gloomie Lootie']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Caverns|#villagers }}}}: Schematic {gloomie_lootie_schematic['UnlockOrder']}: Gloomie Lootie:"
              f"<br>+{5 * grotto_cavern['OpalsFound']}% Drop Rate (+5% per Cavern cleared)",
        picture_class=gloomie_lootie_schematic['Image'],
        progression=grotto_cavern['OpalsFound'] if gloomie_lootie_schematic['Purchased'] else 0,
        goal=EmojiType.INFINITY.value
    ))

    # Caverns - Schematics - Sanctum of LOOT
    temple_cavern = session_data.account.caverns['Caverns']['The Temple']
    sanctum_of_loot_schematic = session_data.account.caverns['Schematics']['Sanctum of LOOT']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Caverns|#villagers }}}}: Schematic {sanctum_of_loot_schematic['UnlockOrder']}: Sanctum of LOOT:"
              f"<br>+{20 * temple_cavern['OpalsFound']}% Drop Rate (+20% per Sanctum cleared)",
        picture_class=sanctum_of_loot_schematic['Image'],
        progression=temple_cavern['OpalsFound'] if sanctum_of_loot_schematic['Purchased'] else 0,
        goal=EmojiType.INFINITY.value
    ))

    # Caverns - Wisdom Monument
    wisdom_drop_rate_index = 26
    wisdom_monument_drop_rate = session_data.account.caverns['Caverns']['Wisdom Monument']['Bonuses'][wisdom_drop_rate_index]
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Cavern 13|#underground-overgrowth }}}}: Wisdom Monument:"
              f"<br>+{round(wisdom_monument_drop_rate['Value'], 2):g}% Drop Rate",
        picture_class='cavern-13',
        progression=wisdom_monument_drop_rate['Level'],
        goal=EmojiType.INFINITY.value
    ))

    # World 6
    #########################################

    # Achievements - Big Big Hampter
    big_hampter_completed = session_data.account.achievements['Big Big Hampter']['Complete']
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Achievements|#achievements }}}}- Big Big Hampter:"
              f"<br>+{4 if big_hampter_completed else 0}/4% Drop Rate",
        picture_class='big-big-hampter',
        progression=int(big_hampter_completed),
        goal=1
    ))

    # Achievements - Summoning GM
    summoning_gm_completed = session_data.account.achievements['Summoning GM']['Complete']
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Achievements|#achievements }}}}- Summoning GM:"
              f"<br>+{6 if summoning_gm_completed else 0}/6% Drop Rate",
        picture_class='summoning-gm',
        progression=int(summoning_gm_completed),
        goal=1
    ))

    # Farming - Crop Depot - Highlighter
    crops_unlocked = session_data.account.farming['CropsUnlocked']
    highlighter = session_data.account.farming['Depot'][7]
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Farming Crop Depot|#farming }}}}- Highlighter:"
              f"<br>+{round(highlighter['Value'], 2):g}% Drop Rate"
              f"{'<br>Note: Value only increases after 100 crops found' if (crops_unlocked <= 100) else ''}",
        picture_class=highlighter['Image'],
        progression=crops_unlocked,
        goal=max_farming_crops
    ))

    # Farming - Land Rank - Seed of Loot
    # Will show additional info if the player does not have the current max number of available land rank levels
    seed_of_loot_land_rank = session_data.account.farming['LandRankDatabase']['Seed of Loot']
    seed_of_loot_value = seed_of_loot_land_rank['BaseValue'] * seed_of_loot_land_rank['Level']
    seed_of_loot_value_max = seed_of_loot_land_rank['BaseValue'] * max_land_rank_level
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Land Ranks|#farming }}}}- Seed of Loot:"
              f"<br>+{seed_of_loot_value}/{seed_of_loot_value_max}% Drop Rate"
              f"{f'<br>Note: Increase Land Rank max with Death Bringer {{{{ Grimoire|#the-grimoire }}}}' if seed_of_loot_land_rank['Level'] < max_land_rank_level else ''}",
        picture_class='seed-of-loot',
        progression=seed_of_loot_land_rank['Level'],
        goal=max_land_rank_level
    ))

    # Sneaking - Pristine Charm - Cotton Candy
    cotton_candy_obtained = session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Pristine Charms|#sneaking }}}}- Cotton Candy:"
              f"<br>{1.15 if cotton_candy_obtained else 0}/1.15x Drop Rate MULTI",
        picture_class='cotton-candy-charm',
        progression=int(cotton_candy_obtained),
        goal=1
    ))

    # Sneaking - Beanstalk - Golden Cake
    beanstack_requirements = [0, '10K', '100K']
    cake_beanstalk = session_data.account.sneaking['Beanstalk']['FoodG13']
    cake_beanstalk_level = int(cake_beanstalk['Beanstacked']) + int(cake_beanstalk['SuperBeanstacked'])
    if cake_beanstalk_level == 2:
        cake_beanstalk_bonus = '+6.67'
    elif cake_beanstalk_level == 1:
        cake_beanstalk_bonus = '+4.59'
    else:
        cake_beanstalk_bonus = '0'
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Beanstalk|#beanstalk }}}}- Golden Cake:"
              f"<br>{cake_beanstalk_bonus}/6.67% base Drop Rate from {beanstack_requirements[cake_beanstalk_level]} deposited"
              f"<br>Note: Further increased by Golden Food bonuses",
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
    other_summon_bonus_multi = (
        (.01 if session_data.account.achievements['Regalis My Beloved']['Complete'] else 0)
        + (.01 if session_data.account.achievements['Spectre Stars']['Complete'] else 0)
        + (.25 * session_data.account.sailing['Artifacts']['The Winz Lantern']['Level'])
        + (.01 * session_data.account.merits[5][4]['Level'])
    )
    prisine_charm_summon_bonus_multi = 1.3 if session_data.account.sneaking['PristineCharms']['Crystal Comb']['Obtained'] else 1
    # The bonuses from endless summoning and everything else, except the pristine charm are addative. The charm is a multi
    total_summon_bonus_multi = (1 + endless_summon_bonus_multi + other_summon_bonus_multi) * prisine_charm_summon_bonus_multi
    summoning_drop_rate_value = round(summoning_drop_rate_base * total_summon_bonus_multi, 2)
    summoning_drop_rate_max_base = 7 + 10.5 + 17.5 + 35
    summoning_drop_rate_max_modded = round(summoning_drop_rate_max_base * total_summon_bonus_multi, 2)
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Summoning Bonuses|#summoning }}}}- Drop Rate:"
              f"<br>+{summoning_drop_rate_value:g}/{summoning_drop_rate_max_modded:g}% Drop Rate"
              f"{f'<br>Note: Max value can be further increased with Endless Summoning wins' if summoning_drop_rate_value >= summoning_drop_rate_max_base else ''}",
        picture_class='summoning',
        progression=summoning_battles['Endless'],
        goal=EmojiType.INFINITY.value
    ))

    for subgroup in drop_rate_aw_advice:
        for advice in drop_rate_aw_advice[subgroup]:
            mark_advice_completed(advice)

    drop_rate_ag = AdviceGroup(
        tier='',
        pre_string="Account wide sources of Drop Rate",
        post_string="Note: External DR bonus modifiers are included in Values shown, but only listed if missing or not maxed.",
        advices=drop_rate_aw_advice,
        informational=True,
    )
    return drop_rate_ag

def get_drop_rate_player_advice_group():
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

    bnn_cardset = []
    events_cardset = []
    for card in session_data.account.cards:
        if card.cardset == 'Bosses n Nightmares':
            bnn_cardset.append(card)
        if card.cardset == 'Events':
            events_cardset.append(card)

    cards = 'Cards'
    eqp = 'Equipment'
    misc = 'Miscellaneous'
    drop_rate_pp_advice = {
        cards: [],
        eqp: [],
        misc: []
    }

    # Cards - Drop Rate
    # Considered just showing the best 8, either total or currently unlocked
    # But decided to just show all of them so new accounts can see what they don't have yet
    card_drop_rate = []
    for card in session_data.account.cards:
        if card.name in drop_rate_cards:
            card_drop_rate.append(card)
    best_2_cards = 0
    for card in sorted(card_drop_rate, key=lambda c: c.getCurrentValue(), reverse=True):
        end_note = ''
        if best_2_cards < 2:
            if best_2_cards == 0 and session_data.account.labChips['Omega Nanochip'] > 0:
                end_note = 'Note: Place in TOP LEFT card slot with Omega Nanochip Lab Chip'
            elif best_2_cards != 0 and session_data.account.labChips['Omega Motherboard'] > 0:
                end_note = 'Note: Place in BOT RIGHT card slot with Omega Motherboard Lab Chip'
            best_2_cards += 1
        drop_rate_pp_advice[cards].append(card.getAdvice(optional_ending_note=end_note))

    # Card Sets - Bosses n Nightmares
    bnn_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in bnn_cardset)
    bnn_star, _ = divmod(bnn_stars_sum, len(bnn_cardset))
    bnn_star = min(bnn_star, max_card_stars)
    bnn_star_next = (bnn_star + 1) * len(bnn_cardset)
    if bnn_stars_sum == bnn_star_next:
        bnn_star += 1
    drop_rate_pp_advice[cards].append(Advice(
        label=f"{{{{ Card Sets|#cards }}}}- Bosses n Nightmares:"
              f"<br>+{6 * bnn_star}/{6 * (1 + max_card_stars)}% Drop Rate"
              + (f"<br>Cards until next set level {bnn_stars_sum}/{bnn_star_next}" if bnn_stars_sum < bnn_star_next else '')
        ,
        picture_class='bosses-n-nightmares',
        progression=bnn_star,
        goal=6
    ))

    # Cards Sets - Events
    events_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in events_cardset)
    events_star, _ = divmod(events_stars_sum, len(events_cardset))
    events_star = min(events_star, max_card_stars)
    events_star_next = (events_star + 1) * len(events_cardset)
    if events_stars_sum == events_star_next:
        events_star += 1
    drop_rate_pp_advice[cards].append(Advice(
        label=f"{{{{ Card Sets|#cards }}}}- Events:"
              f"<br>+{7 * events_star}/{7 * (1 + max_card_stars)}% Drop Rate"
              + (f"<br>Cards until next set level {events_stars_sum}/{events_star_next}" if events_stars_sum < events_star_next else ''),
        picture_class='events',
        progression=events_star,
        goal=6
    ))

    drop_rate_equipment = {}
    for equipment_name, equipment_data in equipment_by_bonus_dict['DropRate'].items():
        equipment_drop_rate = 0
        if equipment_data.get('Misc1', False) and equipment_data['Misc1']['Bonus'] == 'DropRate':
            equipment_drop_rate = equipment_data['Misc1']['Value']
        elif equipment_data.get('Misc2', False) and equipment_data['Misc2']['Bonus'] == 'DropRate':
            equipment_drop_rate = equipment_data['Misc2']['Value']
        if not drop_rate_equipment.get(equipment_data['Type'], False):
            drop_rate_equipment[equipment_data['Type']] = []
        drop_rate_equipment[equipment_data['Type']].append({
            'Name': equipment_name,
            'Limited': equipment_data['Limited'],
            'Type': equipment_data['Type'],
            'Owned': next((a.amount > 0 for a in session_data.account.all_assets.values() if a.name == equipment_name), False),
            'Value': equipment_drop_rate,
            'Image': equipment_data['Image'],
            'Note': equipment_data.get('Note', '')
        })

    # Equipment - Drop Rate
    for slot_list in drop_rate_equipment.values():
        # Once the player has a piece of DR gear for a slot, it won't list _worse_ items for the same slot.
        # Each slot is already sorted best to worst so we just break out of the slot loop once we have an owned item
        # Because of the lack of availability, we'll show ALL limited items all the time. Even if something better is owned
        best_value = 0
        for equipment in sorted(slot_list, key=lambda e: e['Value'], reverse=True):
            if equipment['Value'] >= best_value:
                best_value = max(best_value, equipment['Value'] * equipment['Owned'])
                drop_rate_pp_advice[eqp].append(Advice(
                    label=f"{equipment['Type']}- {equipment['Name']}:"
                          f"<br>+{equipment['Value']}% Drop Rate{' (Limited availability)' if equipment['Limited'] else ''}"
                          f"{'<br>' + equipment['Note'] if equipment['Note'] else ''}",
                    picture_class=equipment['Image'],
                    progression=int(equipment['Owned']),
                    goal=1
                ))

    # Lab Chips - Silkrode Nanochip
    # Modifier for Star Signs below, must be equipped so we always show 
    silkroad_chip_owned = session_data.account.labChips['Silkrode Nanochip'] > 0
    silkroad_chip_starsign_mod = 2 if silkroad_chip_owned else 1
    drop_rate_pp_advice[misc].append(Advice(
        label=f"Lab Chips- Silkrode Nanochip:"
              f"<br>x2 Star Sign Bonuses while equipped"
              f"<br>Note: Improves the Star Signs below while they are equipped",
        picture_class='silkrode-nanochip',
        progression=int(silkroad_chip_owned),
        goal=1
    ))

    # Star Signs - Seraph Cosmos
    # Always shown because the modifier can grow based on Summoning levels
    saraph_cosmos_starsign_unlocked = session_data.account.star_signs['Seraph Cosmos']['Unlocked']
    saraph_cosmod_starsign_mod = (1.1 ** max(3, ceil((session_data.account.all_skills['Summoning'][0]+1)/20))) if saraph_cosmos_starsign_unlocked else 1.0
    drop_rate_pp_advice[misc].append(Advice(
        label=f"{{{{ Star Signs|#star-signs }}}}- Seraph Cosmos:"
              f"<br>x{round(saraph_cosmod_starsign_mod, 3)} Star Sign Bonuses (x1.10 per 20 Summoning levels)"
              f"<br>Note: Always improves the Star Signs below",
        picture_class='seraph-cosmos',
        progression=int(saraph_cosmos_starsign_unlocked),
        goal=1
    ))

    # Add up Infinite Star Sign levels
    infinite_star_sign_levels = session_data.account.breeding['Total Shiny Levels']['Infinite Star Signs']
    
    # Passive Star Signs are skipped by infinite star signs. The easiest way to account for this is to
    # just +1 the total ISS for each passive that WOULD have been counted. Then we can just compare index to ISS
    i = 1
    while i < min(len(starsigns_dict), infinite_star_sign_levels):
        infinite_star_sign_levels += int(starsigns_dict[i]['Passive'])
        i += 1

    # Star Sign - Pirate Booty
    pirate_booty_starsign = session_data.account.star_signs['Pirate Booty']
    pirate_booty_starsign_unlocked = pirate_booty_starsign['Unlocked']
    pirate_booty_infinite_unlocked = pirate_booty_starsign['Index'] <= infinite_star_sign_levels
    pirate_booty_starsign_value_nochip = 5 * saraph_cosmod_starsign_mod
    pirate_booty_starsign_value_chip = 5 * saraph_cosmod_starsign_mod * silkroad_chip_starsign_mod
    drop_rate_pp_advice[misc].append(Advice(
        label=f"{{{{ Star Signs|#star-signs }}}}- Pirate Booty:"
              f"<br>+{round(pirate_booty_starsign_value_nochip, 1):g}% Drop Rate {'PASSIVE' if pirate_booty_infinite_unlocked else 'if equipped'}"
              f"{f'<br>+{round(pirate_booty_starsign_value_chip, 1):g}% Drop Rate if equipped WITH Silkrode Lab Chip' if silkroad_chip_owned and pirate_booty_infinite_unlocked else ''}",
        picture_class='blue-hedgehog',
        progression=int(pirate_booty_starsign_unlocked),
        goal=1
    ))

    # Star Sign - Druipi Major
    druipi_majox_starsign = session_data.account.star_signs['Druipi Major']
    druipi_major_starsign_unlocked = druipi_majox_starsign['Unlocked']
    druipi_major_infinite_unlocked = druipi_majox_starsign['Index'] <= infinite_star_sign_levels
    druipi_major_starsign_value_nochip = 12 * saraph_cosmod_starsign_mod
    druipi_major_starsign_value_chip = 12 * saraph_cosmod_starsign_mod * silkroad_chip_starsign_mod
    drop_rate_pp_advice[misc].append(Advice(
        label=f"{{{{ Star Signs|#star-signs }}}}- Druipi Major:"
              f"<br>+{round(druipi_major_starsign_value_nochip, 1):g}% Drop Rate {'PASSIVE' if druipi_major_infinite_unlocked else 'if equipped'}"
              f"{f'<br>+{round(druipi_major_starsign_value_chip, 1):g}% Drop Rate if equipped WITH Silkrode Lab Chip' if silkroad_chip_owned and druipi_major_infinite_unlocked else ''}",
        picture_class='og-signalais',
        progression=int(druipi_major_starsign_unlocked),
        goal=1
    ))

    # Post Office - Non Predatory Loot Box
    nplb = next(b for b in po_box_dict.values() if b['Name'] == 'Non Predatory Loot Box')
    nplb_dr_max_value = lavaFunc(
        funcType=nplb['1_funcType'],
        level=nplb['Max Level'],
        x1=nplb['1_x1'],
        x2=nplb['1_x2']
    )
    nplb_all = [char.po_boxes_invested[nplb['Name']]['Level'] for char in session_data.account.all_characters]
    nplb_unmaxed = {char.character_name:char.po_boxes_invested[nplb['Name']]['Level'] for char in session_data.account.all_characters if char.po_boxes_invested['Non Predatory Loot Box']['Level'] < nplb['Max Level']}
    nplb_lowest = min(nplb_all, default=0)
    if nplb_lowest < nplb['Max Level']:
        drop_rate_pp_advice[misc].append(Advice(
            label=(
                f"{{{{ Post Office|#post-office }}}}- Non Predatory Loot Box:"
                f"<br>Up to +{round(nplb_dr_max_value, 2):g}% Drop Rate at {nplb['Max Level']} boxes invested"
                f"<br>Non-maxed boxes: {nplb_unmaxed}"
            ),
            picture_class=nplb['Name'],
            progression=nplb_lowest,
            goal=nplb['Max Level']
        ))
    else:
        drop_rate_pp_advice[misc].append(Advice(
            label=f"{{{{ Post Office|#post-office }}}}- Non Predatory Loot Box:"
                  f"<br>+{round(nplb_dr_max_value, 2):g}% Drop Rate",
            picture_class=nplb['Name'],
            progression=nplb_lowest,
            goal=nplb['Max Level']
        ))

    # Prayers - Midas Minded
    midas_minded_data = next(p for p in prayers_dict.values() if p['Name'] == 'Midas Minded')
    midas_minded_bonus_max = lavaFunc(
        funcType=midas_minded_data['bonus_funcType'],
        level=midas_minded_data['MaxLevel'],
        x1=midas_minded_data['bonus_x1'],
        x2=midas_minded_data['bonus_x2']
    )
    midas_minded_curse_max = lavaFunc(
        funcType=midas_minded_data['curse_funcType'],
        level=midas_minded_data['MaxLevel'],
        x1=midas_minded_data['curse_x1'],
        x2=midas_minded_data['curse_x2']
    )

    midas_minded_prayer = session_data.account.prayers['Midas Minded']
    drop_rate_pp_advice[misc].append(Advice(
        label=f"{{{{ Prayers|#prayers }}}}- Midas Minded:"
              f"<br>+{round(midas_minded_prayer['BonusValue'], 2):g}/{round(midas_minded_bonus_max, 2):g}% Drop Rate Bonus | "
              f"+{round(midas_minded_prayer['CurseValue'], 2):g}/{round(midas_minded_curse_max, 2):g}% Max HP for Monsters CURSE",
        picture_class='midas-minded',
        progression=midas_minded_prayer['Level'],
        goal=midas_minded_data['MaxLevel']
    ))

    # Obols - Personal
    best_obols = [None, 0]
    for char in session_data.account.all_characters:
        if best_obols[0] is None:
            best_obols[0] = char.character_name
        if char.obols.get('Total%_DROP_CHANCE', 0) > best_obols[1]:
            best_obols[0] = char.character_name
            best_obols[1] = char.obols.get('Total%_DROP_CHANCE', 0)
    player_obol_drop_rate_max = obols_max_bonuses_dict['PlayerDropRateTrue']
    drop_rate_pp_advice[misc].append(Advice(
        label=f"Obols- Personal Obols:"
              f"<br>+{best_obols[1]}/{player_obol_drop_rate_max}% Drop Rate on best ({best_obols[0]})"
              f"<br>Note: Includes Rare and Hyper Obols, each rerolled with +1% DR",
        picture_class='dementia-obol-of-infinisixes',
        progression=best_obols[1],
        goal=player_obol_drop_rate_max
    ))

    for subgroup in drop_rate_pp_advice:
        for advice in drop_rate_pp_advice[subgroup]:
            mark_advice_completed(advice)

    drop_rate_ag = AdviceGroup(
        tier='',
        pre_string="Player specific sources of Drop Rate",
        # post_string="Note: Non-limited equipment that is worse than what you already have for the slot is excluded",
        advices=drop_rate_pp_advice,
        informational=True,
    )
    return drop_rate_ag

def get_progression_tiers_advice_group() -> tuple[AdviceGroup, int, int, int]:
    template_advice_dict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Drop Rate']
    max_tier = true_max - optional_tiers
    tier_DropRate = 0

    #Assess Tiers
    tiers_ag = AdviceGroup(
        tier=tier_DropRate,
        pre_string="Progression Tiers",
        advices=template_advice_dict['Tiers']
    )
    overall_section_tier = min(true_max, tier_DropRate)
    return tiers_ag, overall_section_tier, max_tier, true_max

def get_drop_rate_advice_section() -> AdviceSection:
    # Generate AdviceGroups
    drop_rate_advice_group_dict = {}
    drop_rate_advice_group_dict['Tiers'], overall_section_tier, max_tier, true_max = get_progression_tiers_advice_group()
    drop_rate_advice_group_dict['Account'] = get_drop_rate_account_advice_group()
    drop_rate_advice_group_dict['Player'] = get_drop_rate_player_advice_group()

    # Generate AdviceSection
    tier_section = f"{overall_section_tier}/{max_tier}"
    drop_rate_advice_section = AdviceSection(
        name='Drop Rate',
        tier=tier_section,
        pinchy_rating=overall_section_tier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Drop Rate Information',
        picture='data/VaultUpg18.png',
        groups=drop_rate_advice_group_dict.values(),
        unrated=True,
    )
    return drop_rate_advice_section
