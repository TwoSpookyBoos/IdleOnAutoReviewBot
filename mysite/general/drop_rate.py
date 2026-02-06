from consts.progression_tiers import true_max_tiers
from consts.consts_autoreview import ValueToMulti, EmojiType
from consts.idleon.lava_func import lava_func
from consts.consts_general import max_card_stars, cards_max_level, equipment_by_bonus_dict
from consts.consts_w5 import max_sailing_artifact_level
from consts.consts_w4 import rift_rewards_dict, shiny_days_list
from consts.consts_w3 import prayers_dict, approx_max_talent_level_non_es_non_star
from consts.consts_w2 import max_sigil_level, sigils_dict, po_box_dict, obols_max_bonuses_dict
from consts.consts_w1 import starsigns_dict, get_seraph_cosmos_multi, seraph_max, get_seraph_cosmos_summ_level_goal
from models.general.session_data import session_data

from models.general.assets import Asset
from models.general.character import Character
from models.advice.advice_group_tabbed import TabbedAdviceGroupTab, TabbedAdviceGroup
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.w6 import get_summoning_bonus_advice
from models.advice.generators.w7 import get_legend_talent_advice
from models.advice.generators.general import get_guild_bonus_advice, get_upgrade_vault_advice, get_companion_advice
from models.advice.generators.w2 import get_arcade_advice

from utils.misc.add_tabbed_advice_group_or_spread_advice_group_list import add_tabbed_advice_group_or_spread_advice_group_list
from utils.all_talentsDict import all_talentsDict
from utils.misc.has_companion import has_companion
from utils.text_formatting import notateNumber, kebab
from utils.logging import get_logger


logger = get_logger(__name__)

drop_rate_shiny_base = 1
infinite_star_sign_shiny_base = 2

def get_drop_rate_account_advice_group() -> tuple[AdviceGroup, dict]:
    companion_data_missing = not session_data.account.companions['Companion Data Present']
    bundle_data_missing = not session_data.account.gemshop['Bundle Data Present']
    missing_bundle_data_txt = '<br>Note: Could be inaccurate. Bundle data not found!' if bundle_data_missing else ''
    passive_drop_rate_cards = [
        'Domeo Magmus',
        'Ancient Golem',
        'IdleOn 4th Anniversary'
    ]

    general = 'General'
    mc = 'Master Classes'
    w1 = 'World 1'
    w2 = 'World 2'
    w3 = 'World 3'
    w4 = 'World 4'
    w5 = 'World 5'
    w6 = 'World 6'
    w7 = 'World 7'
    special = 'Special bonuses'
    drop_rate_aw_advice = {
        general: [],
        mc: [],
        w1: [],
        w2: [],
        w3: [],
        w4: [],
        w5: [],
        w6: [],
        w7: [],
        special: []
    }

    #########################################
    # Account Wide
    #########################################

    # General
    #########################################
    general_bonus = 0
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
            general_bonus += card.getCurrentValue()

    # Cards - Shrine Effect - to boost Clover Shrine
    chaotic_chizoar_card = next(c for c in session_data.account.cards if c.name == 'Chaotic Chizoar')
    if chaotic_chizoar_card.getStars() < (cards_max_level - 1):
        drop_rate_aw_advice[general].append(chaotic_chizoar_card.getAdvice(optional_ending_note="Increases Clover Shrine effect. See character-specific sections"))

    # Guild Bonus - Gold Charm
    drop_rate_aw_advice[general].append(get_guild_bonus_advice('Gold Charm'))
    general_bonus += session_data.account.guild_bonuses['Gold Charm']['Value']

    # Upgrade Vault - Vault Mastery
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    vault_mastery_vault = session_data.account.vault['Upgrades']['Vault Mastery']
    if vault_mastery_vault['Level'] < vault_mastery_vault['Max Level']:
        drop_rate_aw_advice[general].append(get_upgrade_vault_advice('Vault Mastery', additional_info_text=f"<br>(increases the value of the Vault upgrade below)"))

    # Upgrade Vault - Drops for Days
    drop_rate_aw_advice[general].append(get_upgrade_vault_advice('Drops for Days'))
    general_bonus += session_data.account.vault['Upgrades']['Drops for Days']['Total Value']

    # Companions - Crystal Custard
    crystal_custard_value, crystal_custard_advice = get_companion_advice('Crystal Custard')
    drop_rate_aw_advice[general].append(crystal_custard_advice)
    general_bonus += crystal_custard_value

    # Companions - Quenchie
    quenchie_value, quenchie_advice = get_companion_advice('Quenchie')
    drop_rate_aw_advice[general].append(quenchie_advice)
    general_bonus += quenchie_value

    # Gem Shop - Deathbringer Pack
    has_db_pack = session_data.account.gemshop['Bundles']['bun_v']['Owned']
    db_pack_value = 200 if has_db_pack else 0
    drop_rate_aw_advice[general].append(Advice(
        label=f"Gemshop- Deathbringer Pack:"
              f"<br>+{db_pack_value}/200% Drop Rate"
              f"{missing_bundle_data_txt}",
        picture_class='gem',
        progression=int(has_db_pack) if not bundle_data_missing else 'IDK',
        goal=1
    ))
    general_bonus += db_pack_value

    drop_rate_aw_advice[f"{general} - +{round(general_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(general)

    # Master Classes
    #########################################
    master_classes_bonus = 0
    # Grimoire - Skull of Major Droprate
    skull_drop_rate_grimoire = session_data.account.grimoire['Upgrades']['Skull of Major Droprate']
    skull_drop_rate_grimoire_upgrades_unlock = skull_drop_rate_grimoire['Unlock Requirement'] - session_data.account.grimoire['Total Upgrades']
    skull_drop_rate_grimoire_value = skull_drop_rate_grimoire['Total Value']
    drop_rate_aw_advice[mc].append(Advice(
        label=f"{{{{Grimoire|#the-grimoire}}}}- Skull of Major Droprate:"
              f"<br>+{round(skull_drop_rate_grimoire_value, 1):g}% Drop Rate"
              f"{f'<br>Requires {skull_drop_rate_grimoire_upgrades_unlock} more upgrades to unlock' if skull_drop_rate_grimoire_upgrades_unlock > 0 else ''}",
        picture_class=skull_drop_rate_grimoire['Image'],
        progression=skull_drop_rate_grimoire['Level'],
        goal=skull_drop_rate_grimoire['Max Level']
    ))
    master_classes_bonus += skull_drop_rate_grimoire_value

    drop_rate_aw_advice[f"{mc} - +{round(master_classes_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(mc)

    # World 1
    #########################################
    world_1_bonus = 0

    # Owl Bonuses
    owl_bonus = session_data.account.owl['Bonuses']['Drop Rate']['Value']
    drop_rate_aw_advice[w1].append(Advice(
        label=f"{{{{ Owl|#owl }}}}- Drop Rate:"
              f"<br>+{owl_bonus}% Drop Rate",
        picture_class='the-great-horned-owl',
        progression=max(0, session_data.account.owl['MegaFeathersOwned'] - 10),
        resource='megafeather-9',
        goal=EmojiType.INFINITY.value
    ))
    world_1_bonus += owl_bonus

    # Lab Nodes- Certified Stamp Book
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    golden_sixes_buffs = []
    has_certified_stamp_book = session_data.account.labBonuses['Certified Stamp Book']['Enabled']
    if not has_certified_stamp_book:
        golden_sixes_buffs.append('Laboratory')
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
    liqorice_rolle = session_data.account.sneaking.pristine_charms['Liqorice Rolle']
    if not liqorice_rolle.obtained:
        golden_sixes_buffs.append('Pristine Charm')
        drop_rate_aw_advice[w1].append(liqorice_rolle.get_obtained_advice())
    # Stamps - Golden Sixes
    golden_sixes_stamp = session_data.account.stamps['Golden Sixes Stamp']
    if not golden_sixes_stamp.exalted:
        golden_sixes_buffs.append('Exalting the stamp')
    if len(golden_sixes_buffs) == 0:
        golden_sixes_addl_text = f"Note: Can be further increased by Exalted {{{{Stamp|#stamps}}}} bonuses"
    else:
        golden_sixes_addl_text = f"Note: Can be increased by " + ", ".join(golden_sixes_buffs)

    golden_sixes_bonus = golden_sixes_stamp.total_value
    drop_rate_aw_advice[w1].append(golden_sixes_stamp.get_advice(additional_text=f"<br>{golden_sixes_addl_text}"))
    world_1_bonus += golden_sixes_bonus

    drop_rate_aw_advice[f"{w1} - +{round(world_1_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w1)

    # World 2
    #########################################
    world_2_bonus = 0

    # Arcade - Shop Bonuses
    has_reindeer_companion = has_companion('Spirit Reindeer')
    if not has_reindeer_companion:
        _, reindeer_advice = get_companion_advice('Spirit Reindeer')
        drop_rate_aw_advice[w2].append(reindeer_advice)

    drop_rate_aw_advice[w2].append(get_arcade_advice(27))
    world_2_bonus += session_data.account.arcade[27]['Value']

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
    world_2_bonus += obols_family_drop_rate

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
    droppin_loads_value = dropin_loads_bubble['BaseValue'] # TODO: this currently does not account for Prismatic Bubbles. Should either be auto-fixed once those are implemented, or might need to swap 'BaseValue' for 'PrismaticValue' or whatever we come up with
    drop_rate_aw_advice[w2].append(Advice(
        label=f"{{{{ Alchemy Bubbles|#bubbles }}}}- Droppin Loads:"
              f"<br>+{round(droppin_loads_value, 1):g}/{droppin_loads_value_breakpoints[-1][1]}% Drop Rate"
              f"{droppin_loads_breakpoint_txt}",
        picture_class='droppin-loads',
        progression=dropin_loads_bubble['Level'],
        resource=dropin_loads_bubble['Material'],
        goal=droppin_loads_value_breakpoints[-1][0]
    ))
    world_2_bonus += droppin_loads_value

    # Artifacts- Chilled Yarn
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    chilled_yarn_artifact_level = session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']
    chilled_yarn_multi = ValueToMulti(100 * session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'])
    chilled_yarn_max = ValueToMulti(100 * max_sailing_artifact_level)
    if chilled_yarn_artifact_level < max_sailing_artifact_level:
        drop_rate_aw_advice[w2].append(Advice(
            label=f"{{{{ Artifacts|#artifacts }}}}- Chilled Yarn:"
                  f"<br>{round(chilled_yarn_multi, 1):g}/{round(chilled_yarn_max, 1):g}x Sigil Bonuses"
                  f"<br>Note: Improves the sigil below",
            picture_class='chilled-yarn',
            progression=chilled_yarn_artifact_level,
            goal=max_sailing_artifact_level
        ))
    # Alchemy - Sigils - Trove
    trove_sigil_level = session_data.account.alchemy_p2w['Sigils']['Trove']['Level']
    trove_sigil_value = sigils_dict['Trove']['Values'][trove_sigil_level] * chilled_yarn_multi
    trove_sigil_value_max = sigils_dict['Trove']['Values'][max_sigil_level] * chilled_yarn_max
    drop_rate_aw_advice[w2].append(Advice(
        label=f"{{{{ Sigils|#sigils }}}}- Trove Sigil:"
              f"<br>+{trove_sigil_value}/{trove_sigil_value_max}% Drop Rate",
        picture_class='trove',
        progression=trove_sigil_level,
        goal=max_sigil_level
    ))
    world_2_bonus += trove_sigil_value

    ballot_active = session_data.account.ballot['CurrentBuff'] == 27
    if ballot_active:
        ballot_status = 'is Active'
    elif not ballot_active and session_data.account.ballot['CurrentBuff'] != 0:
        ballot_status = 'is Inactive'
    else:
        ballot_status = 'status is not available in provided data'
    ballot_value = session_data.account.ballot['Buffs'][27]['Value']
    ballot_value_active = ballot_value * ballot_active
    drop_rate_aw_advice[w2].append(Advice(
        label=f"Weekly {{{{ Ballot|#bonus-ballot }}}}: +{round(ballot_value_active, 2)}/{round(ballot_value, 2)}% Drop Rate"
              f"<br>(Buff {ballot_status})",
        picture_class='ballot-27',
        progression=int(ballot_active),
        goal=1,
        completed=True
    ))
    world_2_bonus += ballot_value_active

    drop_rate_aw_advice[f"{w2} - +{round(world_2_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w2)

    # World 3
    #########################################
    world_3_bonus = 0

    # Equinox - Faux Jewels
    # Will show additional info if player is maxed out for their currently available levels
    faux_jewels_bonus = session_data.account.equinox_bonuses['Faux Jewels']
    faux_jewels_level = faux_jewels_bonus['CurrentLevel']
    faux_jewels_max_current = max(faux_jewels_bonus['FinalMaxLevel'], faux_jewels_bonus['PlayerMaxLevel'])
    faux_jewels_at_current_max = faux_jewels_level == faux_jewels_bonus['PlayerMaxLevel'] and faux_jewels_bonus['PlayerMaxLevel'] != 0
    faux_jewels_value = 5 * faux_jewels_level
    drop_rate_aw_advice[w3].append(Advice(
        label=f"{{{{ Equinox|#equinox }}}}- Faux Jewels:"
              f"<br>+{faux_jewels_value}/{5 * faux_jewels_max_current}% Drop Rate (+5% per level)"
              f"{'<br>Note: Increase Faux Jewels max level with {{Endless Summoning|#summoning}}' if faux_jewels_at_current_max else ''}",
        picture_class='faux-jewels',
        progression=faux_jewels_level,
        # This is technically infinite with Endless Summoning wins, but we'll just show what's currently unlocked with a note about ES
        goal=faux_jewels_max_current
    ))
    world_3_bonus += faux_jewels_value

    efaunt_set = session_data.account.armor_sets['Sets']['EFAUNT SET']
    drop_rate_aw_advice[w3].append(Advice(
        label=f"{{{{Set bonus|#armor-sets}}}}- Efaunt Set:"
              f"<br>{efaunt_set['Description']}",
        picture_class=efaunt_set['Image'],
        progression=int(efaunt_set['Owned']),
        goal=1
    ))
    world_3_bonus += efaunt_set['Total Value']

    drop_rate_aw_advice[f"{w3} - +{round(world_3_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w3)

    # World 4
    #########################################
    world_4_bonus = 0

    # Breeding - Shiny Pets
    for world in session_data.account.breeding['Species']:
        for shiny_name, shiny_details in session_data.account.breeding['Species'][world].items():
            if shiny_details['ShinyBonus'] == 'Drop Rate':
                shiny_value = shiny_details['ShinyLevel']
                drop_rate_aw_advice[w4].append(Advice(
                    label=f"{{{{ Breeding|#breeding }}}}- Shiny {shiny_name}:"
                          f"<br>+{shiny_value}/{len(shiny_days_list)}% Drop Rate",
                    picture_class=shiny_name,
                    progression=shiny_details['ShinyLevel'],
                    goal=len(shiny_days_list)
                ))
                world_4_bonus += shiny_value

    # The Tome
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    grey_tome_book = session_data.account.grimoire['Upgrades']['Grey Tome Book']
    if grey_tome_book['Level'] < grey_tome_book['Max Level']:
        upgrades_to_unlock = grey_tome_book['Unlock Requirement'] - session_data.account.grimoire['Total Upgrades']
        drop_rate_aw_advice[w4].append(Advice(
            label=f"{{{{Grimoire|#the-grimoire}}}}- Grey Tome Book:"
                  f"<br>{round(grey_tome_book['Total Value'], 1):g}x higher bonus from Tome Red Pages"
                  f"{f'<br>Requires {upgrades_to_unlock} more upgrades to unlock' if upgrades_to_unlock > 0 else ''}",
            picture_class=session_data.account.grimoire['Upgrades']['Grey Tome Book']['Image'],
            progression=grey_tome_book['Level'],
            goal=grey_tome_book['Max Level']
        ))
    troll_set = session_data.account.armor_sets['Sets']['TROLL SET']
    if not troll_set['Owned']:
        drop_rate_aw_advice[w4].append(Advice(
            label=f"{{{{Set bonus|#armor-sets}}}}- Troll Set:"
                  f"<br>{troll_set['Description']}"
                  f"<br>Note: Increases the Tome bonus below",
            picture_class=troll_set['Image'],
            progression=int(troll_set['Owned']),
            goal=1
        ))
    tome_drop_rate_value = session_data.account.tome['Bonuses']['Drop Rarity']['Total Value']
    drop_rate_aw_advice[w4].append(Advice(
        label=f"""Tome- Red Pages:"""
              f"""<br>+{round(tome_drop_rate_value, 1):g}% Drop Rate"""
              f"""<br>{f'Unknown, sorry {EmojiType.FROWN.value}' if not session_data.account.tome['Data Present'] else ''}"""
              f"""{f"{session_data.account.tome['Total Points']:,}" if session_data.account.tome['Data Present'] else ''} Total Tome Points"""
              f"""<br>Increases every 100 points over 8000""",
        picture_class='red-tome-pages',
        progression=session_data.account.tome['Red Pages Unlocked'],
        goal=1
    ))
    world_4_bonus += tome_drop_rate_value

    drop_rate_aw_advice[f"{w4} - +{round(world_4_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w4)

    # World 5
    #########################################
    world_5_bonus = 0

    # Caverns - Measurments - Yards
    caverns_measurements_yards = session_data.account.caverns['Measurements'][15]
    caverns_measurements_yards_value = caverns_measurements_yards['Value']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Caverns|#villagers }}}}- Measurement 16:"
              f"<br>+{round(caverns_measurements_yards_value, 1):g}% Drop Rate (scales with {caverns_measurements_yards['ScalesWith']})",
        picture_class=caverns_measurements_yards['Image'],
        progression=caverns_measurements_yards['Level'],
        goal=EmojiType.INFINITY.value
    ))
    world_5_bonus += caverns_measurements_yards_value

    # Caverns - Schematics - Gloomie Lootie
    grotto_cavern = session_data.account.caverns['Caverns']['Grotto']
    gloomie_lootie_schematic = session_data.account.caverns['Schematics']['Gloomie Lootie']
    gloomie_lootie_schematic_value = 5 * grotto_cavern['OpalsFound']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Caverns|#villagers }}}}- Schematic {gloomie_lootie_schematic['UnlockOrder']}: Gloomie Lootie:"
              f"<br>+{gloomie_lootie_schematic_value}% Drop Rate (+5% per Cavern cleared)",
        picture_class=gloomie_lootie_schematic['Image'],
        progression=grotto_cavern['OpalsFound'] if gloomie_lootie_schematic['Purchased'] else 0,
        goal=EmojiType.INFINITY.value
    ))
    world_5_bonus += gloomie_lootie_schematic_value

    # Caverns - Schematics - Sanctum of LOOT
    temple_cavern = session_data.account.caverns['Caverns']['The Temple']
    sanctum_of_loot_schematic = session_data.account.caverns['Schematics']['Sanctum of LOOT']
    sanctum_of_loot_schematic_value = 20 * temple_cavern['OpalsFound']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Caverns|#villagers }}}}- Schematic {sanctum_of_loot_schematic['UnlockOrder']}: Sanctum of LOOT:"
              f"<br>+{sanctum_of_loot_schematic_value}% Drop Rate (+20% per Sanctum cleared)",
        picture_class=sanctum_of_loot_schematic['Image'],
        progression=temple_cavern['OpalsFound'] if sanctum_of_loot_schematic['Purchased'] else 0,
        goal=EmojiType.INFINITY.value
    ))
    world_5_bonus += sanctum_of_loot_schematic_value

    # Caverns - Wisdom Monument
    wisdom_drop_rate_index = 26
    wisdom_monument_drop_rate = session_data.account.caverns['Caverns']['Wisdom Monument']['Bonuses'][wisdom_drop_rate_index]
    wisdom_monument_drop_rate_value = wisdom_monument_drop_rate['Value']
    drop_rate_aw_advice[w5].append(Advice(
        label=f"{{{{ Cavern 13|#underground-overgrowth }}}}- Wisdom Monument:"
              f"<br>+{round(wisdom_monument_drop_rate_value, 1):g}% Drop Rate",
        picture_class='cavern-13',
        progression=wisdom_monument_drop_rate['Level'],
        goal=EmojiType.INFINITY.value
    ))
    world_5_bonus += wisdom_monument_drop_rate_value

    drop_rate_aw_advice[f"{w5} - +{round(world_5_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w5)

    # World 6
    #########################################
    world_6_bonus = 0.0

    # Achievements - Big Big Hampter
    big_hampter_completed = session_data.account.achievements['Big Big Hampter']['Complete']
    big_hampter_value = 4 if big_hampter_completed else 0
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Achievements|#achievements }}}}- Big Big Hampter:"
              f"<br>+{big_hampter_value}/4% Drop Rate",
        picture_class='big-big-hampter',
        progression=int(big_hampter_completed),
        goal=1
    ))
    world_6_bonus += big_hampter_value

    # Achievements - Summoning GM
    summoning_gm_completed = session_data.account.achievements['Summoning GM']['Complete']
    summoning_gm_value = 6 if summoning_gm_completed else 0
    drop_rate_aw_advice[w6].append(Advice(
        label=f"{{{{ Achievements|#achievements }}}}- Summoning GM:"
              f"<br>+{summoning_gm_value}/6% Drop Rate",
        picture_class='summoning-gm',
        progression=int(summoning_gm_completed),
        goal=1
    ))
    world_6_bonus += summoning_gm_value

    # Farming - Crop Depot - Highlighter
    highlighter = session_data.account.farming.depot["Highlighter"]
    drop_rate_aw_advice[w6].append(highlighter.get_bonus_advice())
    world_6_bonus += highlighter.value

    # Farming - Land Rank - Seed of Loot
    seed_of_loot_land_rank = session_data.account.farming.land_rank['Seed of Loot']
    drop_rate_aw_advice[w6].append(seed_of_loot_land_rank.get_bonus_advice())
    world_6_bonus += seed_of_loot_land_rank.value

    secret_set = session_data.account.armor_sets['Sets']['SECRET SET']
    if not secret_set['Owned']:
        drop_rate_aw_advice[w6].append(Advice(
            label=f"{{{{Set bonus|#armor-sets}}}}- Secret Set:"
                  f"<br>{secret_set['Description']}"
                  f"<br>Note: Increases Golden Food bonus below",
            picture_class=secret_set['Image'],
            progression=int(secret_set['Owned']),
            goal=1
        ))

    # Sneaking - Beanstalk - Golden Cake
    cake_beanstalk = session_data.account.beanstalk['Golden Cake']
    drop_rate_aw_advice[w6].append(cake_beanstalk.get_bonus_advice())
    world_6_bonus += cake_beanstalk.bonus_value

    # Summoning - Bonuses
    drop_rate_aw_advice[w6].append(get_summoning_bonus_advice('+{% Drop Rate'))
    world_6_bonus += session_data.account.summoning['Bonuses']['+{% Drop Rate']['Value']

    emperor_bonus = session_data.account.emperor["Drop Rate"]
    drop_rate_aw_advice[w6].append(emperor_bonus.get_bonus_advice())
    world_6_bonus += emperor_bonus.value

    drop_rate_aw_advice[f"{w6} - +{round(world_6_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w6)

    # World 7
    #########################################
    world_7_bonus = 0

    # Legend Talents: Greatest Drop Party Ever
    drop_rate_aw_advice[w7].append(get_legend_talent_advice('Greatest Drop Party Ever'))
    world_7_bonus += session_data.account.legend_talents['Talents']['Greatest Drop Party Ever']['Value']

    drop_rate_aw_advice[f"{w7} - +{round(world_7_bonus, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w7)

    # Special bonuses. Dependent on character-specific bonuses as they are applied afterwards
    #########################################
    drop_rate_aw_advice[special].append(Advice(
        label="These bonuses are applied after the flat account-wide and character-specific bonuses in the shown order.",
        picture_class=""
    ))

    # Siege Breaker - Talents -  Archlord of the Pirates
    sb_talent = session_data.account.class_kill_talents['Archlord of the Pirates']
    goal_string = notateNumber('Basic', 1e6, 2)
    sb_talent_bonus_max = lava_func(sb_talent['funcType'], approx_max_talent_level_non_es_non_star, sb_talent['x1'], sb_talent['x2']) * sb_talent['Kill Stacks']
    sb_talent_multi = ValueToMulti(sb_talent['Total Value'])
    drop_rate_aw_advice[special].append(Advice(
        label=f"Siege Breaker talent- Archlord of the Pirates:"
              f"<br>Level {sb_talent['Highest Preset Level']}/{approx_max_talent_level_non_es_non_star} with your current kills gives"
              f"<br>{round(sb_talent_multi, 5):g}/{round(ValueToMulti(sb_talent_bonus_max), 5):g}x Drop Rate MULTI",
        picture_class='archlord-of-the-pirates',
        progression=notateNumber('Match', sb_talent['Kills'], 2, '', goal_string),
        goal=goal_string,
        resource='pirate-flag'
    ))

    # Rift - Sneak Mastery 1
    sneak_mastery_level = session_data.account.sneaking.unlocked_mastery
    sneak_mastery_value = 30 if (sneak_mastery_level > 0) else 0
    drop_rate_aw_advice[special].append(Advice(
        label=f"{{{{ Rift|#rift }}}}- Sneaking Mastery:"
              f"<br>+{sneak_mastery_value}/30% Drop Rate",
        picture_class='sneaking-mastery',
        progression=min(1, sneak_mastery_level),
        goal=1
    ))

    # Gem Shop - Island Explorer Pack
    has_island_explorer_pack = session_data.account.gemshop['Bundles']['bun_p']['Owned']
    island_explorer_multi = 1.2 if has_island_explorer_pack else 1
    drop_rate_aw_advice[special].append(Advice(
        label=f"Gemshop- Island Explorer Pack:"
              f"<br>{island_explorer_multi}/1.2x Drop Rate MULTI"
              f"{missing_bundle_data_txt}",
        picture_class='gem',
        progression=int(has_island_explorer_pack) if not bundle_data_missing else 'IDK',
        goal=1
    ))

    # Map-specific: DR Bonus from Arcane Cultist's Overwhelming Energy Talent
    drop_rate_aw_advice[special].append(Advice(
        label=f"Map-specific: Drop Rate MULTI from Arcane Cultist's 'Overwhelming Energy' talent. See character-specific sections",
        picture_class=f"overwhelming-energy"
    ))

    # Sneaking - Pristine Charm - Cotton Candy
    cotton_candy = session_data.account.sneaking.pristine_charms["Cotton Candy"]
    cotton_candy_multi = cotton_candy.value
    drop_rate_aw_advice[special].append(cotton_candy.get_obtained_advice())

    drop_rate_aw_advice[special].append(Advice(
        label=f"Character-specific: Drop Rate MULTI from Equipment. See character-specific sections",
        picture_class=f"drop-rate"
    ))

    # Companions - Mallay
    mallay_multi, mallay_advice = get_companion_advice('Mallay')
    drop_rate_aw_advice[special].append(mallay_advice)

    # Still need to pop to keep the order, even if we don't change the key/label
    drop_rate_aw_advice[special] = drop_rate_aw_advice.pop(special)

    for subgroup in drop_rate_aw_advice:
        for advice in drop_rate_aw_advice[subgroup]:
            advice.mark_advice_completed()

    total_flat_value = general_bonus + master_classes_bonus + world_1_bonus + world_2_bonus + world_3_bonus + world_4_bonus + world_5_bonus + world_6_bonus
    account_wide_advice_group = AdviceGroup(
        tier='',
        pre_string=f"Account wide sources of Drop Rate (+{round(total_flat_value, 1)}%)",
        post_string="Note: External DR bonus modifiers are included in Values shown, but only listed if missing or not maxed.",
        advices=drop_rate_aw_advice,
        informational=True,
    )

    account_wide_bonuses = {
        'total_flat_value': total_flat_value,
        'siege_breaker_multi': sb_talent_multi,
        'sneak_mastery_value': sneak_mastery_value,
        'island_explorer_multi': island_explorer_multi,
        'cotton_candy_multi': cotton_candy_multi,
        'mallay_multi': mallay_multi
    }

    return account_wide_advice_group, account_wide_bonuses


def process_star_sign(name, drop_rate, picture_class, character, infinite_star_sign_levels, silkroad_chip_equipped, silkroad_chip_starsign_mod, star_signs_advice):
    starsign = session_data.account.star_signs[name]
    infinite_unlocked = starsign['Index'] <= infinite_star_sign_levels
    equipped = (starsign['Index'] - 1) in character.equipped_star_signs
    silkroad_chip_owned = session_data.account.star_sign_extras['DoublerOwned']
    boosted = silkroad_chip_equipped and infinite_unlocked
    ac_level = session_data.account.tesseract['Upgrades']['Astrology Cultism']['Level']
    seraph_cosmos_starsign_mod = get_seraph_cosmos_multi(ac_level, character.summoning_level)

    passive_value = drop_rate * seraph_cosmos_starsign_mod
    boosted_value = drop_rate * seraph_cosmos_starsign_mod * silkroad_chip_starsign_mod

    active_value = passive_value if not boosted else boosted_value

    text = (
        f"<br>+{round(active_value, 1):g}% Drop Rate {'(PASSIVE)' if infinite_unlocked and not boosted else ''}"
        f"{'<br>Not being boosted by Silkrode Nanochip. Equip the Lab Chip!' if infinite_unlocked and silkroad_chip_owned and not boosted else ''}"
    )

    if infinite_unlocked and silkroad_chip_equipped:
        max_boosted_for_this_character = True
    elif (equipped or infinite_unlocked) and not silkroad_chip_owned:
        max_boosted_for_this_character = True
    else:
        max_boosted_for_this_character = False

    star_signs_advice.append(Advice(
        label=f"{{{{ Star Signs|#star-signs }}}}- {name}:{text}",
        picture_class=picture_class,
        progression=int(active_value > 0 and max_boosted_for_this_character),
        goal=1
    ))
    return active_value

def invalid_weapon_type(base_class, slot):
    if base_class == 'Warrior':
        return slot in ['Bow', 'Wand', 'Fisticuffs']
    if base_class == 'Archer':
        return slot in ['Spear', 'Wand', 'Fisticuffs']
    if base_class == 'Mage':
        return slot in ['Spear', 'Bow', 'Fisticuffs']
    if base_class in ['Journeyman', 'Beginner'] :
        return slot in ['Spear', 'Bow', 'Wand']
    logger.warning(f'Provided unknown base_class: {base_class}')
    return True


def get_drop_rate_player_advice_groups(account_wide_bonuses: dict) -> TabbedAdviceGroup:
    tabbed_advices: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]] = {}

    # All non-passive cards that affect Drop Rate
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

    acquired_drop_rate_cards = []
    for card in session_data.account.cards:
        if card.name in drop_rate_cards:
            acquired_drop_rate_cards.append(card)
    bnn_cardset = []
    events_cardset = []
    for card in session_data.account.cards:
        if card.cardset == 'Bosses n Nightmares':
            bnn_cardset.append(card)
        if card.cardset == 'Events':
            events_cardset.append(card)

    legend_talent_multi = ValueToMulti(session_data.account.legend_talents['Talents']['Flopping a Full House']['Value'])
    for index, character in enumerate(session_data.account.all_characters):
        # Drop Rate from LUK
        dr_from_luk_advice: list[Advice] = []
        luk = character.main_stats['LUK']
        if luk < 1e3:
            dr_from_luk = (((luk + 1) ** 0.37) - 1) / 40
        else:
            dr_from_luk = 0.5 * ((luk - 1e3) / (luk + 2500)) + 0.297
        dr_from_luk *= 1.4
        dr_from_luk *= 100  # x100 because DR from Luck is calculated as an additive Multi, but we just want to display flat % (0.09 -> +9% flat)
        dr_from_luk_advice.append(Advice(
            label=f"Drop Rate from the 'LUK' Stat: +{round(dr_from_luk, 2)}%",
            picture_class='luk'
        ))

        # Non-passive Drop Rate cards
        card_advice: list[Advice] = []
        card_bonus = 0
        best_2_cards = 0
        for card in sorted(acquired_drop_rate_cards, key=lambda c: c.getCurrentValue(), reverse=True):
            end_note = ''
            if best_2_cards < 2:
                if best_2_cards == 0 and session_data.account.labChips['Omega Nanochip'] > 0:
                    end_note = 'Note: Place in TOP LEFT card slot and equip Omega Nanochip Lab Chip'
                elif best_2_cards != 0 and session_data.account.labChips['Omega Motherboard'] > 0:
                    end_note = 'Note: Place in BOT RIGHT card slot and equip Omega Motherboard Lab Chip'
                best_2_cards += 1
            equipped = card.codename in character.equipped_cards_codenames
            starting_note = ""
            if equipped:
                card_bonus += card.getCurrentValue(optional_character=character)
                starting_note = f'(EQUIPPED {EmojiType.CHECK.value}) '
                equipped_slot = character.equipped_cards_codenames.index(card.codename)
                if (equipped_slot == 0 and "Omega Nanochip" in character.equipped_card_doublers) or (equipped_slot == 7 and "Omega Motherboard" in character.equipped_card_doublers):
                    starting_note = f'(DOUBLED {EmojiType.CHECK.value}{EmojiType.CHECK.value}) '
            card_advice.append(card.getAdvice(optional_character=character, optional_starting_note=starting_note, optional_ending_note=end_note))
        card_bonus *= legend_talent_multi
        card_advice.append(get_legend_talent_advice('Flopping a Full House'))

        # Card Sets - Bosses n Nightmares
        cardset_advice: list[Advice] = []
        cardset_bonus = 0
        bnn_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in bnn_cardset)
        bnn_star, _ = divmod(bnn_stars_sum, len(bnn_cardset))
        bnn_star = min(bnn_star, max_card_stars)
        bnn_star_next = (bnn_star + 1) * len(bnn_cardset)
        if bnn_stars_sum == bnn_star_next:
            bnn_star += 1
        bnn_value = 6 * bnn_star
        bnn_equipped = character.equipped_cardset == 'Bosses n Nightmares'
        cardset_advice.append(Advice(
            label=f"{f'(EQUIPPED {EmojiType.CHECK.value}) ' if bnn_equipped else ''} {{{{ Card Sets|#cards }}}}- Bosses n Nightmares:"
                  f"<br>+{bnn_value}/{6 * (1 + max_card_stars)}% Drop Rate"
                  + (f"<br>Cards until next set level {bnn_stars_sum}/{bnn_star_next}" if bnn_stars_sum < bnn_star_next else '')
            ,
            picture_class='bosses-n-nightmares',
            progression=bnn_star,
            goal=6
        ))
        if bnn_equipped:
            cardset_bonus = bnn_value

        # Cards Sets - Events
        events_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in events_cardset)
        events_star, _ = divmod(events_stars_sum, len(events_cardset))
        events_star = min(events_star, max_card_stars)
        events_star_next = (events_star + 1) * len(events_cardset)
        if events_stars_sum == events_star_next:
            events_star += 1
        events_value = 7 * events_star
        events_equipped = character.equipped_cardset == 'Events'
        cardset_advice.append(Advice(
            label=f"{f'(EQUIPPED {EmojiType.CHECK.value}) ' if events_equipped else ''} {{{{ Card Sets|#cards }}}}- Events:"
                  f"<br>+{events_value}/{7 * (1 + max_card_stars)}% Drop Rate"
                  + (f"<br>Cards until next set level {events_stars_sum}/{events_star_next}" if events_stars_sum < events_star_next else ''),
            picture_class='events',
            progression=events_star,
            goal=6
        ))
        if events_equipped:
            cardset_bonus = events_value

        # Equipment - Flat Drop Rate
        equipment_advice, equipment_bonus = get_equipment_advice_for_stat(
            character,
            'DropRate',
            '%_DROP_CHANCE',
            'Drop Rate',
            'Drop Rate - '
        )

        # Equipment - Drop Rate Multi
        equipment_multi_advice, equipment_multi_bonus = get_equipment_advice_for_stat(
            character,
            'DropRateMulti',
            '%_DROP_CHANCE_MULTI',
            'Drop Rate Multi',
            'Drop Rate Multi - '
        )
        equipment_multi_bonus_as_mult = ValueToMulti(equipment_multi_bonus)

        # Star Signs
        star_signs_advice: list[Advice] = []
        star_signs_bonus = 0

        # Lab Chips - Silkrode Nanochip
        # Modifier for Star Signs below, must be equipped so we always show
        silkroad_chip_equipped = 'Silkrode Nanochip' in character.equipped_lab_chips
        silkroad_chip_starsign_mod = 2 if silkroad_chip_equipped else 1
        star_signs_advice.append(Advice(
            label=f"Lab Chips- Silkrode Nanochip: 2x Passive Star Sign Bonuses while equipped",
            picture_class='silkrode-nanochip',
            progression=int(silkroad_chip_equipped),
            goal=1
        ))

        # Seraph Cosmos
        # Always shown because the modifier can grow based on Summoning levels
        ac_level = session_data.account.tesseract['Upgrades']['Astrology Cultism']['Level']
        seraph_cosmos_starsign_mod = get_seraph_cosmos_multi(ac_level, character.summoning_level)
        next_multi_goal = get_seraph_cosmos_summ_level_goal(ac_level, character.summoning_level)
        next_level_note = (
            f"<br>{character.summoning_level}/{next_multi_goal} summoning levels toward next multi increase."
            if seraph_cosmos_starsign_mod < seraph_max
            else ''
        )
        star_signs_advice.append(Advice(
            label=f"{{{{ Star Signs|#star-signs }}}}- Seraph Cosmos:"
                  f"<br>{round(seraph_cosmos_starsign_mod, 3):g}/{seraph_max}x Passive Star Sign Bonuses"
                  f"{next_level_note}",
            picture_class='seraph-cosmos',
            progression=int(session_data.account.star_signs['Seraph Cosmos']['Unlocked']),
            goal=1
        ))

        # Add up Infinite Star Sign levels
        infinite_star_sign_levels = session_data.account.breeding['Total Shiny Levels']['Infinite Star Signs'] * 2 + 5

        # Passive Star Signs are skipped by infinite star signs. The easiest way to account for this is to
        # just +1 the total ISS for each passive that WOULD have been counted. Then we can just compare index to ISS
        i = 1
        while i < min(len(starsigns_dict), infinite_star_sign_levels):
            infinite_star_sign_levels += int(starsigns_dict[i]['Passive'])
            i += 1

        # Star Sign - Pirate Booty
        star_signs_bonus += process_star_sign(
            "Pirate Booty", 5, "pack-mule",
            character,
            infinite_star_sign_levels,
            silkroad_chip_equipped,
            silkroad_chip_starsign_mod,
            star_signs_advice
        )

        # Star Sign - Druipi Major
        star_signs_bonus += process_star_sign(
            "Druipi Major", 12, "killian-maximus",
            character,
            infinite_star_sign_levels,
            silkroad_chip_equipped,
            silkroad_chip_starsign_mod,
            star_signs_advice
        )

        # Post Office - Non Predatory Loot Box
        post_office_advice: list[Advice] = []
        post_office_bonus = 0

        nplb_name = 'Non Predatory Loot Box'
        nplb = next(b for b in po_box_dict.values() if b['Name'] == nplb_name)
        nplb_dr_max_value = lava_func(
            funcType=nplb['1_funcType'],
            level=nplb['Max Level'],
            x1=nplb['1_x1'],
            x2=nplb['1_x2']
        )
        char_nplb = character.po_boxes_invested[nplb_name]

        post_office_advice.append(Advice(
            label=f"{{{{ Post Office|#post-office }}}}- {nplb_name}:"
                  f"<br>+{round(char_nplb['Bonus1Value'], 1):g}/{round(nplb_dr_max_value, 1):g}% Drop Rate",
            picture_class=nplb_name,
            progression=char_nplb['Level'],
            goal=char_nplb['Max Level']
        ))
        post_office_bonus += char_nplb['Bonus1Value']

        # Prayers - Midas Minded
        prayer_advice: list[Advice] = []
        prayer_bonus = 0

        midas_minded_name = 'Midas Minded'
        midas_minded_data = next(p for p in prayers_dict.values() if p['Name'] == midas_minded_name)
        midas_minded_bonus_max = lava_func(
            funcType=midas_minded_data['bonus_funcType'],
            level=midas_minded_data['MaxLevel'],
            x1=midas_minded_data['bonus_x1'],
            x2=midas_minded_data['bonus_x2']
        )
        midas_minded_curse_max = lava_func(
            funcType=midas_minded_data['curse_funcType'],
            level=midas_minded_data['MaxLevel'],
            x1=midas_minded_data['curse_x1'],
            x2=midas_minded_data['curse_x2']
        )

        midas_minded_equipped = midas_minded_name in character.equipped_prayers
        midas_minded_equip_notice = "" if midas_minded_equipped else "<br>Equip the prayer to gain its bonus!"
        midas_minded_prayer = session_data.account.prayers[midas_minded_name]
        midas_mind_completed = (midas_minded_prayer['Level'] == midas_minded_data['MaxLevel']) and midas_minded_equipped
        prayer_advice.append(Advice(
            label=f"{{{{ Prayers|#prayers }}}} - {midas_minded_name}:"
                  f"<br>+{round(midas_minded_prayer['BonusValue'], 1):g}/{round(midas_minded_bonus_max, 1):g}% Drop Rate Bonus | "
                  f"+{round(midas_minded_prayer['CurseValue'], 1):g}/{round(midas_minded_curse_max, 1):g}% Max HP for Monsters CURSE."
                  f"{midas_minded_equip_notice}",
            picture_class=midas_minded_name,
            progression=midas_minded_prayer['Level'],
            goal=midas_minded_data['MaxLevel'],
            completed=midas_mind_completed
        ))
        prayer_bonus += midas_minded_prayer['BonusValue'] * midas_minded_equipped

        # Obols - Personal
        obol_advice: list[Advice] = []
        obol_bonus = 0
        player_obol_drop_rate = character.obols.get('Total%_DROP_CHANCE', 0)
        player_obol_drop_rate_max = obols_max_bonuses_dict['PlayerDropRateTrue']
        obol_advice.append(Advice(
            label=f"Obols- Personal Obols:"
                  f"<br>+{player_obol_drop_rate}/{player_obol_drop_rate_max}% Drop Rate"
                  f"<br>Note: Includes Rare and Hyper Obols, each rerolled with +1% DR",
            picture_class='dementia-obol-of-infinisixes',
            progression=player_obol_drop_rate,
            goal=player_obol_drop_rate_max
        ))
        obol_bonus += player_obol_drop_rate

        # Shrines - Clover Shrine
        shrine_advice: list[Advice] = []
        shrine_bonus = 0

        chaotic_chizoar_card = next(c for c in session_data.account.cards if c.name == 'Chaotic Chizoar')
        shrine_extra_bonus_text = ''
        if chaotic_chizoar_card.getStars() < (cards_max_level - 1):
            shrine_extra_bonus_text = '<br>Note: Can be increased by getting more Chaotic Chizoar card stars'

        if session_data.account.sailing['Artifacts']['Moai Head']['Level'] > 0:
            clover_shrine_affects_character = True
        else:
            char_map = character.current_map_index
            char_world = (char_map // 50) + 1

            shrine_data = session_data.account.shrines['Clover Shrine']
            shrine_map = shrine_data['MapIndex']
            shrine_world = (shrine_map // 50) + 1

            if session_data.account.labBonuses['Shrine World Tour']['Enabled']:
                clover_shrine_affects_character = char_world == shrine_world
            else:
                clover_shrine_affects_character = char_map == shrine_map

        clover_shrine_value = session_data.account.shrines['Clover Shrine']['Value']
        shrine_advice.append(Advice(
            label=f"{f'(ACTIVE {EmojiType.CHECK.value}) ' if clover_shrine_affects_character else ''} Shrines- Clover Shrine:"
                  f"<br>+{round(clover_shrine_value, 1):g}% Drop Rate "
                  f"{shrine_extra_bonus_text}",
            picture_class='clover-shrine',
            progression=session_data.account.shrines['Clover Shrine']['Level'],
            goal=EmojiType.INFINITY.value
        ))
        shrine_bonus += clover_shrine_value * clover_shrine_affects_character

        # Talents
        talent_advice: list[Advice] = []
        talent_bonus = 0

        # Talents - Special Talent: Boss Battle Spillover
        bbs_index = 655
        boss_battle_spillover = all_talentsDict[bbs_index]
        char_boss_battle_spillover_level = character.current_preset_talents.get(str(bbs_index), 0)
        boss_battle_spillover_value_per_tier = lava_func(
            funcType=boss_battle_spillover['funcX'],
            level=char_boss_battle_spillover_level,
            x1=boss_battle_spillover['x1'],
            x2=boss_battle_spillover['x2']
        )
        boss_battle_spillover_value_per_tier_max = lava_func(
            funcType=boss_battle_spillover['funcX'],
            level=100,
            x1=boss_battle_spillover['x1'],
            x2=boss_battle_spillover['x2']
        )
        boss_battle_spillover_value = boss_battle_spillover_value_per_tier * session_data.account.weekly_boss_kills
        boss_battle_spillover_value_max = boss_battle_spillover_value_per_tier_max * 5
        talent_advice.append(Advice(
            label=f"Special Talent - Boss Battle Spillover:"
                  f"<br>+{round(boss_battle_spillover_value, 1)}%/{boss_battle_spillover_value_max}% Drop Rate" 
                  f"{'<br>Can be increased by defeating more weekly boss difficulties!' if session_data.account.weekly_boss_kills < 5 else ''}",
            picture_class='boss-battle-spillover',
            progression=char_boss_battle_spillover_level,
            goal=100,
            completed=boss_battle_spillover_value == boss_battle_spillover_value_max
        ))
        talent_bonus += boss_battle_spillover_value

        # Talent - Archer: Robbinghood
        if character.base_class == 'Archer':
            robbinghood_index = 279
            robbinghood = all_talentsDict[robbinghood_index]
            char_robbinghood_level = character.current_preset_talents.get(str(robbinghood_index), 0)
            if char_robbinghood_level > 0:
                char_robbinghood_level += character.total_bonus_talent_levels
            robbinghood_value = lava_func(
                funcType=robbinghood['funcX'],
                level=char_robbinghood_level,
                x1=robbinghood['x1'],
                x2=robbinghood['x2']
            )
            robbinghood_value_max = lava_func(
                funcType=robbinghood['funcX'],
                level=character.max_talents_over_books,
                x1=robbinghood['x1'],
                x2=robbinghood['x2']
            )
            talent_advice.append(Advice(
                label=f"Archer Talent - Robbinghood:"
                      f"<br>+{round(robbinghood_value, 1)}%/{round(robbinghood_value_max, 1)}% Drop Rate",
                picture_class='robbinghood',
                progression=char_robbinghood_level,
                goal=character.max_talents_over_books,
                completed=robbinghood_value == robbinghood_value_max
            ))
            talent_bonus += robbinghood_value

        # Talent - Journeyman: Curse Of Mr Looty Booty
        if character.base_class == 'Journeyman':
            looty_booty_index = 24
            looty_booty = all_talentsDict[looty_booty_index]
            char_looty_booty_level = character.current_preset_talents.get(str(looty_booty_index), 0)
            if char_looty_booty_level > 0:
                char_looty_booty_level += character.total_bonus_talent_levels
            looty_booty_value = lava_func(
                funcType=looty_booty['funcX'],
                level=char_looty_booty_level,
                x1=looty_booty['x1'],
                x2=looty_booty['x2']
            )
            looty_booty_value_max = lava_func(
                funcType=looty_booty['funcX'],
                level=character.max_talents_over_books,
                x1=looty_booty['x1'],
                x2=looty_booty['x2']
            )
            talent_advice.append(Advice(
                label=f"Journeyman Talent - Curse Of Mr Looty Booty:"
                      f"<br>+{round(looty_booty_value, 1)}%/{round(looty_booty_value_max, 1)}% Drop Rate",
                picture_class='curse-of-mr-looty-booty',
                progression=char_looty_booty_level,
                goal=character.max_talents_over_books,
                completed=looty_booty_value == looty_booty_value_max
            ))
            talent_bonus += looty_booty_value

        # Wrap Up
        character_specific_advice = {
            f'Luck - +{round(dr_from_luk, 2)}% Drop Rate': dr_from_luk_advice,
            f'Cards - +{round(card_bonus, 1)}% Drop Rate': card_advice,
            f'Card Set - +{round(cardset_bonus, 1)}% Drop Rate': cardset_advice,
            f'Equipment Drop Rate - Total: +{round(equipment_bonus, 1)}% Drop Rate': [],
            **equipment_advice,
            f'Equipment Drop Rate Multi - Total: x{round(equipment_multi_bonus_as_mult, 2)} Drop Rate': [],
            **equipment_multi_advice,
            f'Star Signs - +{round(star_signs_bonus, 1)}% Drop Rate': star_signs_advice,
            f'Post Office - +{round(post_office_bonus, 1)}% Drop Rate': post_office_advice,
            f'Prayers - +{round(prayer_bonus, 1)}% Drop Rate': prayer_advice,
            f'Obols - +{round(obol_bonus, 1)}% Drop Rate': obol_advice,
            f'Shrines - +{round(shrine_bonus, 1)}% Drop Rate': shrine_advice,
            f'Talents - +{round(talent_bonus, 1)}% Drop Rate': talent_advice,
        }
        character_specific_flat_bonus = dr_from_luk + card_bonus + cardset_bonus + equipment_bonus + star_signs_bonus + post_office_bonus + prayer_bonus + obol_bonus + shrine_bonus + talent_bonus
        total_bonus = account_wide_bonuses['total_flat_value'] + character_specific_flat_bonus

        final_value = 100  # Base (x1.00)
        final_value += total_bonus
        final_value *= account_wide_bonuses['siege_breaker_multi']
        final_value += account_wide_bonuses['sneak_mastery_value']
        final_value *= account_wide_bonuses['island_explorer_multi']
        # TODO: Arcane Cultist Map-specific Bonus
        final_value *= account_wide_bonuses['cotton_candy_multi']
        final_value *= equipment_multi_bonus_as_mult
        final_value *= account_wide_bonuses['mallay_multi']

        for subgroup in character_specific_advice.values():
            for advice in subgroup:
                advice.mark_advice_completed()

        tabbed_advices[character.character_name] = (
            TabbedAdviceGroupTab(kebab(character.class_name_icon), str(index + 1)),
            AdviceGroup(
                tier='',
                pre_string=f"Character-specific sources of Drop Rate for {character.character_name} the {character.class_name}"
                           f"<br>Character-specific Drop Rate: +{round(character_specific_flat_bonus, 2)}%"
                           f"<br>Total Drop Rate, including account-wide bonuses and multis: x{round(final_value / 100, 2)}",
                advices=character_specific_advice,
                informational=True
            )
        )
    return TabbedAdviceGroup(tabbed_advices)


def get_equipment_advice_for_stat(character: Character, stat: str, stat_codename: str, stat_human_readable_format: str, advice_group_prefix: str):
    equipment_advice: dict[str, list[Advice]] = {}
    equipment_bonus = 0
    equipment_dict: dict[str, list] = {}

    motherboard_equipped = "Silkrode Motherboard" in character.equipped_lab_chips
    software_equipped = "Silkrode Software" in character.equipped_lab_chips
    processor_equipped = "Silkrode Processor" in character.equipped_lab_chips

    for equipment_name, equipment_data in equipment_by_bonus_dict[stat].items():
        is_keychain = equipment_data['Type'] == 'Keychain'
        misc1 = equipment_data.get('Misc1', {})
        misc2 = equipment_data.get('Misc2', {})
        equipment_drop_rate_base = ((misc1.get('Bonus', '') == stat) * misc1.get('Value', 0)) + ((misc2.get('Bonus', '') == stat) * misc2.get('Value', 0))
        equipped_equipment: list[Asset | None] = [equipment for equipment in character.equipment.equips if equipment_name == equipment.name] + [tool for tool in character.equipment.tools if equipment_name == tool.name]
        if not equipped_equipment:
            equipped_equipment = [None] # So the loop below is executed once
            if is_keychain:
                equipped_equipment = [None, None] # So the loop below is executed twice
        if len(equipped_equipment) == 1 and is_keychain:
            equipped_equipment.append(None) # So the loop below is executed twice

        for index, item in enumerate(equipped_equipment):
            equipped_equipment_bonus = 0
            slot = equipment_data.get('Type')
            can_be_boosted = slot in ['Trophy', 'Keychain', 'Pendant'] and index == 0
            is_boosted = (motherboard_equipped and slot == 'Trophy' or
                          software_equipped and is_keychain and index == 0 or
                          processor_equipped and slot == 'Pendant')
            if item is not None:
                misc1 = item.stats.get('misc_1_txt', None)
                misc2 = item.stats.get('misc_2_txt', None)
                if misc1 == stat_codename:
                    equipped_equipment_bonus += item.stats['misc_1_val']
                if misc2 == stat_codename:
                    equipped_equipment_bonus += item.stats['misc_2_val']
                if equipped_equipment_bonus == 0:
                    equipped_equipment_bonus += equipment_drop_rate_base
            if is_boosted:
                equipped_equipment_bonus *= 2
            equipment_bonus += equipped_equipment_bonus

            if advice_group_prefix + slot not in equipment_dict.keys():
                equipment_dict[advice_group_prefix + slot] = []

            equipment_dict[advice_group_prefix + slot].append({
                'Name': equipment_name,
                'Slot': slot,
                stat: equipped_equipment_bonus if is_keychain else equipment_drop_rate_base,
                'Image': equipment_data['Image'],
                'EquippedAndMaxed': int(((not is_boosted) and equipped_equipment_bonus >= equipment_drop_rate_base) or (is_boosted and equipped_equipment_bonus >= 2 * equipment_drop_rate_base)), # >= because the gem shop can sell items with boosted stats, if you have those you're fine
                'Limited': equipment_data.get('Limited', False),
                'Note': equipment_data.get('Note', ''),
                'Can be boosted': can_be_boosted
            })

    for slot, equipment_list in equipment_dict.items():
        if invalid_weapon_type(character.base_class, slot[len(advice_group_prefix):]):
            continue
        if slot not in equipment_advice.keys():
            equipment_advice[slot] = []

        if "Trophy" in slot:
            equipment_advice[slot].append(Advice(
                label=f"Lab Chips - Silkrode Motherboard"
                      f"<br>Doubles Misc. Bonuses of equipped Trophy",
                picture_class='silkrode-motherboard',
                progression=int(motherboard_equipped),
                goal=1
            ))

        if "Keychain" in slot:
            equipment_advice[slot].append(Advice(
                label=f"Lab Chips - Silkrode Software"
                      f"<br>Doubles Misc. Bonuses of (upper) equipped Keychain",
                picture_class='silkrode-software',
                progression=int(software_equipped),
                goal=1
            ))

        if "Pendant" in slot:
            equipment_advice[slot].append(Advice(
                label=f"Lab Chips - Silkrode Processor"
                      f"<br>Doubles Misc. Bonuses of equipped Pendant",
                picture_class='silkrode-processor',
                progression=int(processor_equipped),
                goal=1
            ))

        for index, equipment in enumerate(equipment_list):
            if motherboard_equipped and equipment['Slot'] == 'Trophy' and equipment['Can be boosted']:
                equipment[stat] *= 2
                equipment['Note'] += f"<br>Boosted by Silkrode Motherboard"
            if software_equipped and equipment['Slot'] == 'Keychain' and equipment['Can be boosted']:
                # We don't mult by 2 here because it's already handled in the parsing of the "real" stats. Only Keychains have variable Drop Rate so we have to handle it there.
                equipment['Note'] += f"<br>Boosted by Silkrode Software"
            if processor_equipped and equipment['Slot'] == 'Pendant' and equipment['Can be boosted']:
                equipment[stat] *= 2
                equipment['Note'] += f"<br>Boosted by Silkrode Processor"

            equipment_advice[slot].append(Advice(
                label=f"{equipment['Name']}{' (Limited availability)' if equipment['Limited'] else ''}:"
                      f"<br>+{equipment[stat]}% {stat_human_readable_format}"
                      f"{'<br>' + equipment['Note'] if equipment['Note'] else ''}",
                picture_class=equipment['Image'],
                progression=equipment['EquippedAndMaxed'],
                goal=1
            ))
            if equipment['EquippedAndMaxed'] and index != len(equipment_list) - 1 and equipment['Name'] != equipment_list[index + 1]['Name']:
                # Don't check items that come after the equipped item because they are worse than the equipped item
                break
    return equipment_advice, equipment_bonus


def get_progression_tiers_advice_group() -> tuple[AdviceGroup, int, int, int]:
    template_advice_dict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Drop Rate']
    max_tier = true_max - optional_tiers
    tier_DropRate = 0

    # Assess Tiers
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
    account_wide_advice_group, account_wide_bonuses = get_drop_rate_account_advice_group()
    drop_rate_advice_group_dict['Account'] = account_wide_advice_group
    player_specific_advice: TabbedAdviceGroup = get_drop_rate_player_advice_groups(account_wide_bonuses)
    add_tabbed_advice_group_or_spread_advice_group_list(drop_rate_advice_group_dict, player_specific_advice, 'Player')

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
