from consts.progression_tiers import true_max_tiers
from consts.general.drop_rate import (
    drop_rate_star_signs,
    drop_rate_companions,
    drop_rate_multi_codenames,
    flat_drop_rate_codenames,
    golden_food_stat,
)
from consts.idleon.w7.research import minehead_drop_rate_bonus_index
from consts.w3.equinox import drop_rate_dream_number
from consts.consts_autoreview import ValueToMulti, EmojiType
from consts.consts_general import cards_max_level, equipment_by_bonus_dict
from consts.consts_w5 import max_sailing_artifact_level
from consts.general.friend_bonuses import friend_bonus_drop_rate_index
from models.general.session_data import session_data

from models.general.assets import Asset
from models.general.character import Character
from models.advice.advice_group_tabbed import TabbedAdviceGroupTab, TabbedAdviceGroup
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup

from utils.misc.add_tabbed_advice_group_or_spread_advice_group_list import add_tabbed_advice_group_or_spread_advice_group_list
from utils.number_formatting import round_and_trim
from utils.text_formatting import kebab
from utils.logging import get_logger


logger = get_logger(__name__)

royal_guardian_family_goal = 800

def get_gallery_item_advice() -> list[Advice]:
    # Itemized Trophies/Nametags, account-wide (Gallery, not equip). Delegates the actual
    # advice rows to GalleryTrophy/GalleryNametag.get_bonus_advice() so they carry the real
    # podium/inventory multi or nametag level (not just whether the item is owned), filtered
    # down to just the Drop Rate/Drop Rate Multi lines since that's all this page cares about.
    gallery = session_data.account.gallery
    stats = {'DropRate', 'DropRateMulti'}

    order = []
    types: dict[str, str] = {}
    for stat in stats:
        for name, data in equipment_by_bonus_dict[stat].items():
            if data['Type'] not in ('Trophy', 'Nametag') or name in types:
                continue
            types[name] = data['Type']
            order.append(name)

    return [
        (gallery.trophy if types[name] == 'Trophy' else gallery.nametag)[name].get_bonus_advice(
            stats=stats, link_to_section=True
        )
        for name in order
    ]


def get_drop_rate_account_advice_group() -> AdviceGroup:
    drop_rate = session_data.account.drop_rate
    general = 'General'
    mc = 'Master Classes'
    w1 = 'World 1'
    w2 = 'World 2'
    w3 = 'World 3'
    w4 = 'World 4'
    w5 = 'World 5'
    w6 = 'World 6'
    w7 = 'World 7'
    hatrack_group = 'World 3 - Hat Rack'
    gallery_group = 'World 7 - Gallery'
    companion_group = 'Companions'
    special = 'Special bonuses'
    drop_rate_aw_advice = {
        general: [],
        mc: [],
        w1: [],
        w2: [],
        w3: [],
        hatrack_group: [],
        w4: [],
        w5: [],
        w6: [],
        w7: [],
        gallery_group: [],
        companion_group: [],
        special: []
    }

    #########################################
    # Account Wide
    #########################################

    # General
    #########################################
    # Rift - Ruby Cards
    ruby_cards = session_data.account.rift['RubyCards']
    if not ruby_cards.unlocked:
        drop_rate_aw_advice[general].append(ruby_cards.get_advice(
            ":<br>+1 Max Card Level"
            "<br>Note: increases the max card level for the cards below"
        ))

    # Cards - Drop Rate
    for group, _ in drop_rate.passive_cards:
        drop_rate_aw_advice[general].extend(card.getAdvice() for card in group)

    # Cards - Shrine Effect - to boost Clover Shrine
    chaotic_chizoar_card = next(c for c in session_data.account.cards if c.name == 'Chaotic Chizoar')
    if chaotic_chizoar_card.getStars() < (cards_max_level - 1):
        drop_rate_aw_advice[general].append(chaotic_chizoar_card.getAdvice(optional_ending_note="Increases Clover Shrine effect. See character-specific sections"))

    # Guild Bonus - Gold Charm
    gold_charm = session_data.account.guild_bonuses['Gold Charm']
    drop_rate_aw_advice[general].append(gold_charm.get_advice())

    # Codex - Friend Bonus
    friend_bonuses = session_data.account.friend_bonuses
    if friend_bonus_drop_rate_index in friend_bonuses:
        friend_drop_rate = friend_bonuses[friend_bonus_drop_rate_index]
        drop_rate_aw_advice[general].append(friend_drop_rate.get_bonus_advice())

    # Upgrade Vault - Vault Mastery
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    vault_mastery_vault = session_data.account.vault.upgrades['Vault Mastery']
    if vault_mastery_vault.level < vault_mastery_vault.max_level:
        drop_rate_aw_advice[general].append(session_data.account.vault.get_upgrade_advice('Vault Mastery', additional_info_text=f"<br>(increases the value of the Vault upgrade below)"))

    # Upgrade Vault - Drops for Days
    drop_rate_aw_advice[general].append(session_data.account.vault.get_upgrade_advice('Drops for Days'))

    # Gem Shop - Deathbringer Pack
    drop_rate_aw_advice[general].append(drop_rate.get_deathbringer_pack_advice())

    drop_rate_aw_advice[f"{general} - +{round(drop_rate.general, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(general)

    # Master Classes
    #########################################
    # Grimoire - Skull of Major Droprate
    skull_drop_rate_grimoire = session_data.account.grimoire.upgrades['Skull of Major Droprate']
    drop_rate_aw_advice[mc].append(skull_drop_rate_grimoire.get_advice(session_data.account.grimoire.total_upgrades))

    # Royal Armory - Royal Statue
    drop_rate_aw_advice[mc].append(session_data.account.royal_armory.statues[1].get_advice())

    drop_rate_aw_advice[
        f"{mc} - +{round(drop_rate.master_classes, 1)}% Total Drop Rate, "
        f"x{round_and_trim(drop_rate.royal_statue_multi)} Drop Rate Multi"
    ] = drop_rate_aw_advice.pop(mc)

    # World 1
    #########################################

    # Owl Bonuses
    owl_drop_rate_bonus = session_data.account.owl.bonuses['Drop Rate']
    drop_rate_aw_advice[w1].append(owl_drop_rate_bonus.get_bonus_advice(
        progression=max(0, session_data.account.owl.mega_feathers_owned - 10),
        resource='megafeather-9',
        goal=EmojiType.INFINITY.value
    ))

    # Lab Nodes- Certified Stamp Book
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    golden_sixes_buffs = []
    certified_stamp_book = session_data.account.lab_bonuses['Certified Stamp Book']
    if not certified_stamp_book.enabled:
        golden_sixes_buffs.append('Laboratory')
        drop_rate_aw_advice[w1].append(certified_stamp_book.get_bonus_advice(
            "<br>Note: Improves the stamp below"
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

    drop_rate_aw_advice[w1].append(golden_sixes_stamp.get_advice(additional_text=f"<br>{golden_sixes_addl_text}"))

    drop_rate_aw_advice[f"{w1} - +{round(drop_rate.world_1, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w1)

    # World 2
    #########################################

    # Arcade - Shop Bonuses
    reindeer = session_data.account.companions['Spirit Reindeer']
    if not reindeer.owned:
        reindeer_advice = reindeer.get_advice()
        drop_rate_aw_advice[w2].append(reindeer_advice)

    drop_rate_aw_advice[w2].append(session_data.account.arcade[27].get_advice())

    # Obols - Family - Drop Rate
    drop_rate_aw_advice[w2].append(drop_rate.get_obols_family_advice())

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
        (b for b in droppin_loads_value_breakpoints if b[0] > dropin_loads_bubble.level),
        None
    )
    droppin_loads_breakpoint_txt = (
        f"<br>Next breakpoint: {droppin_loads_next_breakpoint[2]}% value at level {droppin_loads_next_breakpoint[0]}"
        if droppin_loads_next_breakpoint is not None else ''
    )
    drop_rate_aw_advice[w2].append(dropin_loads_bubble.get_bonus_advice(
        f" Drop Rate{droppin_loads_breakpoint_txt}",
        goal=droppin_loads_value_breakpoints[-1][0],
        cap=droppin_loads_value_breakpoints[-1][1]
    ))

    # Artifacts- Chilled Yarn
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    if drop_rate.chilled_yarn_level < max_sailing_artifact_level:
        drop_rate_aw_advice[w2].append(drop_rate.get_chilled_yarn_advice())
    # Alchemy - Sigils - Trove
    drop_rate_aw_advice[w2].append(drop_rate.get_trove_sigil_advice())

    drop_rate_aw_advice[w2].append(drop_rate.get_ballot_advice())

    drop_rate_aw_advice[f"{w2} - +{round(drop_rate.world_2, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w2)

    # World 3
    #########################################

    # Equinox - Faux Jewels
    # Will show additional info if player is maxed out for their currently available levels
    faux_jewels = session_data.account.equinox.upgrades['Faux Jewels']
    drop_rate_aw_advice[w3].append(faux_jewels.get_bonus_advice(
        '<br>Note: Increase Faux Jewels max level with {{Endless Summoning|#summoning}}'
        if faux_jewels.level == faux_jewels.max_level else ''
    ))

    efaunt_set = session_data.account.armor_sets['EFAUNT SET']
    drop_rate_aw_advice[w3].append(efaunt_set.get_bonus_advice())

    drop_rate_aw_advice[f"{w3} - +{round(drop_rate.world_3, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w3)

    # Hatrack, applied per character
    hat_rack = session_data.account.hat_rack
    if session_data.account.world_progress.highest_reached >= 3:
        drop_rate_aw_advice[hatrack_group].extend([
            hat_rack.get_bonus_advice('Drop Rate'),
            hat_rack.get_bonus_advice('Drop Rate Multi'),
        ])
    drop_rate_aw_advice[
        f"{hatrack_group} - +{round(drop_rate.hatrack, 1)}% Drop Rate, "
        f"x{round(ValueToMulti(drop_rate.hatrack_multi), 2)} Drop Rate Multi. "
        f"See character-specific sections"
    ] = drop_rate_aw_advice.pop(hatrack_group)

    # World 4
    #########################################

    # Breeding - Shiny Pets
    drop_rate_aw_advice[w4].extend(drop_rate.get_shiny_pet_advice())

    # The Tome
    # Temporary bonus line, disappears when maxed. Buffed value is included in the DR line below
    grey_tome_book = session_data.account.grimoire.upgrades['Grey Tome Book']
    if grey_tome_book.level < grey_tome_book.max_level:
        drop_rate_aw_advice[w4].append(grey_tome_book.get_advice(session_data.account.grimoire.total_upgrades))
    troll_set = session_data.account.armor_sets['TROLL SET']
    if not troll_set.owned:
        drop_rate_aw_advice[w4].append(troll_set.get_bonus_advice(
            additional_text="<br>Note: Increases the Tome bonus below"
        ))
    drop_rate_aw_advice[w4].append(session_data.account.tome.get_bonus_advice())

    drop_rate_aw_advice[f"{w4} - +{round(drop_rate.world_4, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w4)

    # World 5
    #########################################

    # Caverns - Measurments - Yards
    caverns_measurements_yards = session_data.account.caverns.villagers["Minau"].measurements[15]
    drop_rate_aw_advice[w5].append(caverns_measurements_yards.get_bonus_advice())

    # Caverns - Schematics - Gloomie Lootie
    gloomie_lootie_schematic = session_data.account.caverns.villagers["Kaipu"].schematics['Gloomie Lootie']
    drop_rate_aw_advice[w5].append(gloomie_lootie_schematic.get_bonus_advice())

    # Caverns - Schematics - Sanctum of LOOT
    sanctum_of_loot_schematic = session_data.account.caverns.villagers["Kaipu"].schematics['Sanctum of LOOT']
    drop_rate_aw_advice[w5].append(sanctum_of_loot_schematic.get_bonus_advice())

    # Caverns - Wisdom Monument
    wisdom_monument_drop_rate = session_data.account.caverns.caves['Wisdom Monument'].bonuses['Player Drop Rate']
    drop_rate_aw_advice[w5].append(wisdom_monument_drop_rate.get_bonus_advice())

    drop_rate_aw_advice[f"{w5} - +{round(drop_rate.world_5, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w5)

    # World 6
    #########################################

    # Achievements - Big Big Hampter
    drop_rate_aw_advice[w6].append(drop_rate.get_achievement_advice('Big Big Hampter'))

    # Achievements - Summoning GM
    drop_rate_aw_advice[w6].append(drop_rate.get_achievement_advice('Summoning GM'))

    # Farming - Crop Depot - Highlighter
    highlighter = session_data.account.farming.depot["Highlighter"]
    drop_rate_aw_advice[w6].append(highlighter.get_bonus_advice())

    # Farming - Land Rank - Seed of Loot
    seed_of_loot_land_rank = session_data.account.farming.land_rank['Seed of Loot']
    drop_rate_aw_advice[w6].append(seed_of_loot_land_rank.get_bonus_advice())

    # Farming - Exotic Market - Pommelion Seed
    pommelion_seed = session_data.account.farming.exotic_market['POMMELION SEED']
    drop_rate_aw_advice[w6].append(pommelion_seed.get_bonus_advice())

    secret_set = session_data.account.armor_sets['SECRET SET']
    if not secret_set.owned:
        drop_rate_aw_advice[w6].append(secret_set.get_bonus_advice(
            additional_text="<br>Note: Increases Golden Food bonus. "
                            "See character-specific sections"
        ))

    # Summoning - Bonuses
    summoinig_bonus = session_data.account.summoning.bonuses["Drop Rate"]
    drop_rate_aw_advice[w6].append(summoinig_bonus.get_bonus_advice())

    emperor_bonus = session_data.account.emperor["Drop Rate"]
    drop_rate_aw_advice[w6].append(emperor_bonus.get_bonus_advice())

    drop_rate_aw_advice[f"{w6} - +{round(drop_rate.world_6, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w6)

    # World 7
    #########################################

    # Legend Talents: Greatest Drop Party Ever
    drop_rate_aw_advice[w7].append(session_data.account.legend_talents['Greatest Drop Party Ever'].get_advice())

    # Spelunking - Shop - Golden Hardhat
    golden_hardhat = session_data.account.spelunk.shop['Golden Hardhat']
    drop_rate_aw_advice[w7].append(golden_hardhat.get_bonus_advice())

    # Research - Grid - Divine Design
    divine_design = session_data.account.research.grid['Divine Design']
    drop_rate_aw_advice[w7].append(divine_design.get_bonus_advice())

    # Gallery - Trophies & Nametags, applied per character
    if session_data.account.world_progress.highest_reached >= 7:
        drop_rate_aw_advice[gallery_group].extend(get_gallery_item_advice())

    drop_rate_aw_advice[f"{w7} - +{round(drop_rate.world_7, 1)}% Total Drop Rate"] = drop_rate_aw_advice.pop(w7)
    drop_rate_aw_advice[
        f"{gallery_group} - +{round(drop_rate.gallery, 1)}% Drop Rate, "
        f"x{round(ValueToMulti(drop_rate.gallery_multi), 2)} Drop Rate Multi. "
        f"See character-specific sections"
    ] = drop_rate_aw_advice.pop(gallery_group)

    # Companions
    #########################################
    companions = session_data.account.companions
    drop_rate_aw_advice[companion_group].extend(
        companions[name].get_advice() for name in drop_rate_companions
    )

    # Special bonuses. Dependent on character-specific bonuses as they are applied afterwards
    #########################################
    drop_rate_aw_advice[special].append(Advice(
        label="These bonuses are applied after the flat account-wide and character-specific bonuses in the shown order.",
        picture_class=""
    ))

    # Siege Breaker - Talents -  Archlord of the Pirates
    drop_rate_aw_advice[special].append(drop_rate.get_archlord_advice())

    # Rift - Sneak Mastery 1
    drop_rate_aw_advice[special].append(drop_rate.get_sneaking_mastery_advice())

    # Gem Shop - Island Explorer Pack
    drop_rate_aw_advice[special].append(drop_rate.get_island_explorer_pack_advice())

    # Map-specific: DR Bonus from Arcane Cultist's Overwhelming Energy Talent
    drop_rate_aw_advice[special].append(Advice(
        label=f"Map-specific: Drop Rate MULTI from Arcane Cultist's 'Overwhelming Energy' talent. See character-specific sections",
        picture_class=f"overwhelming-energy"
    ))

    # Sneaking - Pristine Charm - Cotton Candy
    drop_rate_aw_advice[special].append(
        session_data.account.sneaking.pristine_charms["Cotton Candy"].get_obtained_advice()
    )

    # Sushi Station + Jelly Operator
    sushi_milestone = session_data.account.sushi_station.milestones['Drop Rate']
    gold_bangle = session_data.account.jelly_operator.obstructions['Gold Bangle']
    drop_rate_aw_advice[special].append(sushi_milestone.get_advice())
    drop_rate_aw_advice[special].append(gold_bangle.get_advice())

    # Research - Glimbo
    research = session_data.account.research
    glimbo = research.grid['Glimbo Insider Trading Secrets']
    drop_rate_aw_advice[special].append(glimbo.get_bonus_advice())

    # Tome - Drop Rate Multi
    tome = session_data.account.tome
    drop_rate_aw_advice[special].append(tome.get_drop_rate_multi_advice())

    # Minehead
    minehead_bonus = session_data.account.minehead[minehead_drop_rate_bonus_index]
    drop_rate_aw_advice[special].append(minehead_bonus.get_bonus_advice())

    # Equinox - Dream cloud
    drop_rate_dream = session_data.account.equinox.dreams[drop_rate_dream_number]
    drop_rate_aw_advice[special].append(drop_rate_dream.get_bonus_advice())

    # Vials - Shipinabottle
    vials = session_data.account.alchemy_vials
    shipinabottle = vials['Shipinabottle (Pirate Ship Figurine)']
    vial_multi = ValueToMulti(shipinabottle.value)
    drop_rate_aw_advice[special].append(shipinabottle.get_advice(
        value_text=f"{round_and_trim(vial_multi, 3)}x Drop Rate MULTI", full_name=False
    ))

    drop_rate_aw_advice[special].append(Advice(
        label=f"Character-specific: Drop Rate MULTI from Equipment. See character-specific sections",
        picture_class=f"drop-rate"
    ))

    drop_rate_aw_advice[companion_group].append(companions['Mallay'].get_advice())
    drop_rate_aw_advice[
        f"{companion_group} - +{round(drop_rate.companions, 1)}% Drop Rate, x{round(drop_rate.companion_multi, 2)} Drop Rate Multi"
    ] = drop_rate_aw_advice.pop(companion_group)

    # Still need to pop to keep the order, even if we don't change the key/label
    drop_rate_aw_advice[special] = drop_rate_aw_advice.pop(special)

    for subgroup in drop_rate_aw_advice:
        for advice in drop_rate_aw_advice[subgroup]:
            advice.mark_advice_completed()

    account_wide_advice_group = AdviceGroup(
        tier='',
        pre_string=f"Account wide sources of Drop Rate (+{round(drop_rate.total_flat, 1)}%)",
        post_string="Note: External DR bonus modifiers are included in Values shown, but only listed if missing or not maxed.",
        advices=drop_rate_aw_advice,
        informational=True,
    )
    account_wide_advice_group.remove_empty_subgroups()
    return account_wide_advice_group


def invalid_weapon_type(base_class, slot):
    if base_class == 'Warrior':
        return slot in ['Bow', 'Wand', 'Fisticuffs']
    elif base_class == 'Archer':
        return slot in ['Spear', 'Wand', 'Fisticuffs']
    elif base_class == 'Mage':
        return slot in ['Spear', 'Bow', 'Fisticuffs']
    elif base_class in ['Journeyman', 'Beginner']:
        return slot in ['Spear', 'Bow', 'Wand']
    else:
        logger.warning(f'Provided unknown base_class: {base_class}')
    return True


def get_drop_rate_player_advice_groups() -> TabbedAdviceGroup:
    tabbed_advices: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]] = {}

    drop_rate = session_data.account.drop_rate
    royal_armory = session_data.account.royal_armory
    royal_guardian_family = session_data.account.family_bonuses['Royal Guardian']
    beanstalk = session_data.account.beanstalk
    for index, character in enumerate(session_data.account.characters):
        dr = drop_rate.characters[index]

        # Non-passive Drop Rate cards
        card_advice: list[Advice] = []
        best_2_cards = 0
        for card in drop_rate.flat_cards:
            end_note = ''
            if best_2_cards < 2:
                if best_2_cards == 0 and session_data.account.lab_chips['Omega Nanochip'].owned:
                    end_note = 'Note: Place in TOP LEFT card slot and equip Omega Nanochip Lab Chip'
                elif best_2_cards != 0 and session_data.account.lab_chips['Omega Motherboard'].owned:
                    end_note = 'Note: Place in BOT RIGHT card slot and equip Omega Motherboard Lab Chip'
                best_2_cards += 1
            equipped = card.codename in character.equipped_cards_codenames
            starting_note = ""
            if equipped:
                starting_note = f'(EQUIPPED {EmojiType.CHECK.value}) '
                equipped_slot = character.equipped_cards_codenames.index(card.codename)
                if (equipped_slot == 0 and "Omega Nanochip" in character.equipped_card_doublers) or (equipped_slot == 7 and "Omega Motherboard" in character.equipped_card_doublers):
                    starting_note = f'(DOUBLED {EmojiType.CHECK.value}{EmojiType.CHECK.value}) '
            card_advice.append(card.getAdvice(optional_character=character, optional_starting_note=starting_note, optional_ending_note=end_note))
        card_advice.append(session_data.account.legend_talents['Flopping a Full House'].get_advice())

        # Drop Rate Multi cards
        card_multi_advice: list[Advice] = []
        for card in drop_rate.multi_cards:
            starting_note = (
                f'(EQUIPPED {EmojiType.CHECK.value}) '
                if card.codename in character.equipped_cards_codenames else ''
            )
            card_multi_advice.append(card.getAdvice(
                optional_character=character, optional_starting_note=starting_note
            ))

        # Family Bonus - Royal Guardian
        family_advice = [
            royal_guardian_family.get_bonus_advice(royal_guardian_family_goal)
        ]

        # Card Sets
        cardset_advice = [
            dr.get_card_set_advice(name, progress)
            for name, progress in drop_rate.card_sets.items()
        ]

        # Equipment - Flat Drop Rate
        equipment_advice = get_equipment_advice_for_stat(
            character,
            'DropRate',
            flat_drop_rate_codenames,
            'Drop Rate',
            'Drop Rate - '
        )

        # Equipment - Drop Rate Multi
        equipment_multi_advice = get_equipment_advice_for_stat(
            character,
            'DropRateMulti',
            drop_rate_multi_codenames,
            'Drop Rate Multi',
            'Drop Rate Multi - '
        )
        showcase_headers = {
            (
                f'{name} - +{round(value, 1)}% Drop Rate, '
                f'+{round(multi_value, 1)}% Drop Rate Multi'
                f'{"" if active else " (not unlocked on this character)"}'
            ): []
            for name, world, active, value, multi_value in (
                ('Hat Rack', 3, character.hatrack_bonus_active, dr.hatrack, dr.hatrack_multi),
                ('Gallery', 7, character.gallery_bonus_active, dr.gallery, dr.gallery_multi),
            )
            if session_data.account.world_progress.highest_reached >= world
        }

        # Some slots (Cape, Nametag, Trophy) have items in both the flat Drop Rate and Drop Rate
        # Multi dicts, which used to show up as confusing duplicate sections (e.g. "Drop Rate -
        # Trophy" and "Drop Rate Multi - Trophy" side by side). Merge them into one section per
        # slot - each item's own label already says whether it's a flat bonus or a multi.
        equipment_advice_by_slot = merge_equipment_advice_by_slot(
            [('Drop Rate - ', equipment_advice), ('Drop Rate Multi - ', equipment_multi_advice)]
        )

        # Golden Food
        golden_food_advice = beanstalk.get_golden_food_bonus_advice(
            character, golden_food_stat
        )

        # Star Signs. Nanochip and Seraph modify the signs below
        star_signs_advice = [
            dr.get_silkrode_nanochip_advice(),
            dr.get_seraph_cosmos_advice(),
            *(
                dr.get_star_sign_advice(name, picture_class)
                for name, _, picture_class in drop_rate_star_signs
            ),
        ]
        star_signs_bonus = sum(dr.star_signs.values(), 0)

        talent_advice = [dr.get_boss_battle_spillover_advice()]
        if character.base_class == 'Archer':
            talent_advice.append(dr.get_robbinghood_advice())
        if character.base_class == 'Journeyman':
            talent_advice.append(dr.get_looty_booty_advice())

        # Talent - Royal Guardian: Graded Rate
        if dr.graded_rate > 0:
            talent_advice.append(royal_armory.get_graded_rate_advice(character))

        # Wrap Up
        character_specific_advice = {
            f'Luck - +{round(dr.luk, 2)}% Drop Rate': [dr.get_luk_advice()],
            f'Cards - +{round(dr.cards, 1)}% Drop Rate': card_advice,
            f'Card Set - +{round(dr.card_set, 1)}% Drop Rate': cardset_advice,
            f'Drop Rate Multi Cards - x{round_and_trim(dr.card_multi, 3)} Drop Rate':
                card_multi_advice,
            f'Family Bonus - x{round_and_trim(dr.family_multi, 3)} Drop Rate':
                family_advice,
            f'Equipment Drop Rate - Total: +{round(dr.equipment, 1)}% Drop Rate': [],
            (
                f'Equipment Drop Rate Multi - Total: '
                f'+{round(dr.equipment_multi, 1)}% Drop Rate Multi '
                f'(x{round(dr.equipment_multi_total, 2)} '
                f'with Gallery and Hat Rack)'
            ): [],
            **showcase_headers,
            f'Gown - x{round_and_trim(dr.gown_multi, 3)} Drop Rate': [],
            **equipment_advice_by_slot,
            f'Golden Food - +{round(dr.golden_food, 1)}% Drop Rate':
                golden_food_advice,
            f'Star Signs - +{round(star_signs_bonus, 1)}% Drop Rate': star_signs_advice,
            f'Post Office - +{round(dr.post_office, 1)}% Drop Rate': [dr.get_loot_box_advice()],
            f'Prayers - +{round(dr.prayers, 1)}% Drop Rate': [dr.get_midas_minded_advice()],
            f'Obols - +{round(dr.obols, 1)}% Drop Rate': [dr.get_obols_advice()],
            f'Shrines - +{round(dr.shrines, 1)}% Drop Rate': [dr.get_clover_shrine_advice()],
            f'Talents - +{round(dr.talents, 1)}% Drop Rate': talent_advice,
        }
        for subgroup in character_specific_advice.values():
            for advice in subgroup:
                advice.mark_advice_completed()

        tabbed_advices[character.character_name] = (
            TabbedAdviceGroupTab(kebab(character.class_name_icon), str(index + 1)),
            AdviceGroup(
                tier='',
                pre_string=f"Character-specific sources of Drop Rate for {character.character_name} the {character.class_name}"
                           f"<br>Character-specific Drop Rate: +{round(dr.flat_total, 2)}%"
                           f"<br>Total Drop Rate, including account-wide bonuses and multis: x{round(dr.total / 100, 2)}",
                advices=character_specific_advice,
                informational=True
            )
        )
    return TabbedAdviceGroup(tabbed_advices)


_lab_chip_picture_classes = {'silkrode-motherboard', 'silkrode-software', 'silkrode-processor'}


def merge_equipment_advice_by_slot(prefixed_equipment_advices: list[tuple[str, dict[str, list[Advice]]]]) -> dict[str, list[Advice]]:
    """Combine equipment advice dicts keyed by "{prefix}{Slot}" (e.g. "Drop Rate - Trophy",
    "Drop Rate Multi - Trophy") into one dict keyed by bare Slot (e.g. "Trophy"), so a slot that
    shows up under multiple stats gets a single section instead of one per stat.

    Some info rows (e.g. the Silkrode Motherboard chip note) get generated identically by each
    stat's pass, so exact duplicate labels within a slot are dropped. An item that contributes to
    both stats (e.g. Deadbones Nametag, listed under both Drop Rate and Drop Rate Multi) instead
    gets combined into a single row with one bare stat line per stat (e.g. "+35% Drop Rate" /
    "+25% Drop Rate Multi"), dropping each pass's Note since it only existed to cross-reference
    the other stat's value, which is now redundant once both lines are shown directly.
    """
    merged: dict[str, list[Advice]] = {}
    seen_chip_rows_by_slot: dict[str, set[tuple[str, str]]] = {}
    # Per slot, the already-emitted combined row for each (equipment name, occurrence) seen so
    # far - "occurrence" handles Keychains, where the same name can appear twice in one pass
    # (upper/lower slot) without those two rows being merged into each other.
    item_rows_by_slot: dict[str, dict[tuple[str, int], Advice]] = {}

    for prefix, equipment_advice in prefixed_equipment_advices:
        for slot_key, advices in equipment_advice.items():
            slot = slot_key.removeprefix(prefix)
            merged.setdefault(slot, [])
            seen_chip_rows = seen_chip_rows_by_slot.setdefault(slot, set())
            item_rows = item_rows_by_slot.setdefault(slot, {})
            name_occurrence_so_far: dict[str, int] = {}

            for advice in advices:
                if advice.picture_class in _lab_chip_picture_classes:
                    dedupe_key = (advice.label, advice.picture_class)
                    if dedupe_key in seen_chip_rows:
                        continue
                    seen_chip_rows.add(dedupe_key)
                    merged[slot].append(advice)
                    continue

                name = getattr(advice, 'equipment_name', None)
                if name is None:
                    # Not a recognized item row - pass through as-is
                    merged[slot].append(advice)
                    continue

                occurrence = name_occurrence_so_far.get(name, 0)
                name_occurrence_so_far[name] = occurrence + 1
                item_key = (name, occurrence)

                existing_row = item_rows.get(item_key)
                if existing_row is not None:
                    # Already have a row for this item from an earlier pass - rebuild the label
                    # from bare stat lines only (dropping both passes' Notes, since those only
                    # cross-referenced the other stat's value, which is redundant once merged).
                    existing_row.stat_lines.append(advice.stat_line)
                    limited_suffix = ' (Limited availability)' if existing_row.equipment_limited else ''
                    existing_row.label = f"{name}{limited_suffix}:" + ''.join(
                        f"<br>{line}" for line in existing_row.stat_lines
                    )
                else:
                    item_rows[item_key] = advice
                    merged[slot].append(advice)
    return merged


def get_equipment_advice_for_stat(
    character: Character,
    stat: str,
    stat_codenames: tuple[str, ...],
    stat_human_readable_format: str,
    advice_group_prefix: str
):
    equipment_advice: dict[str, list[Advice]] = {}
    equipment_dict: dict[str, list] = {}

    motherboard_equipped = "Silkrode Motherboard" in character.equipped_lab_chips
    software_equipped = "Silkrode Software" in character.equipped_lab_chips
    processor_equipped = "Silkrode Processor" in character.equipped_lab_chips
    motherboard_boosts_gallery = session_data.account.world_progress.highest_reached >= 7
    # Gallery/Hatrack take over these slots once open for this character
    showcased_types = (
        ('Trophy', 'Nametag') * character.gallery_bonus_active
        + ('Premium Hat',) * character.hatrack_bonus_active
    )

    if stat == 'DropRate':
        # Equipping the chip is per-character even though its effect is account-wide
        equipment_advice.setdefault(advice_group_prefix + 'Trophy', []).append(Advice(
            label=(
                "Lab Chips - Silkrode Motherboard<br>+10% Trophy Gallery Bonus Multi"
                if motherboard_boosts_gallery else
                "Lab Chips - Silkrode Motherboard<br>Doubles Misc. Bonuses of equipped Trophy"
            ),
            picture_class='silkrode-motherboard',
            progression=int(motherboard_equipped),
            goal=1
        ))

    for equipment_name, equipment_data in equipment_by_bonus_dict[stat].items():
        if equipment_data['Type'] in showcased_types:
            continue
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
                # Own misc lines only; chip doubling below, no gown multi
                equipped_equipment_bonus = character.equipment.get_item_misc_bonus(
                    item, stat_codenames
                )
            if is_boosted:
                equipped_equipment_bonus *= 2

            if advice_group_prefix + slot not in equipment_dict.keys():
                equipment_dict[advice_group_prefix + slot] = []

            equipment_dict[advice_group_prefix + slot].append({
                'Name': equipment_name,
                'Slot': slot,
                stat: equipped_equipment_bonus if is_keychain else equipment_drop_rate_base,
                'Image': equipment_data['Image'],
                'EquippedAndMaxed': int(
                    ((not is_boosted) and equipped_equipment_bonus >= equipment_drop_rate_base)
                    or (is_boosted and equipped_equipment_bonus >= 2 * equipment_drop_rate_base)
                ), # >= because the gem shop can sell items with boosted stats, if you have those you're fine
                'Limited': equipment_data.get('Limited', False),
                'Note': equipment_data.get('Note', ''),
                'Can be boosted': can_be_boosted
            })

    for slot, equipment_list in equipment_dict.items():
        if invalid_weapon_type(character.base_class, slot[len(advice_group_prefix):]):
            continue
        if slot not in equipment_advice.keys():
            equipment_advice[slot] = []

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

            # stat_line/detail_html are stashed separately so merge_equipment_advice_by_slot can
            # combine an item that contributes to both Drop Rate and Drop Rate Multi (e.g.
            # Deadbones Nametag) into a single row with one bare stat line per stat, instead of
            # two rows each also repeating a now-redundant Note about the other stat's value.
            stat_line = f"+{equipment[stat]}% {stat_human_readable_format}"
            detail_html = f"<br>{stat_line}{'<br>' + equipment['Note'] if equipment['Note'] else ''}"
            item_advice = Advice(
                label=f"{equipment['Name']}{' (Limited availability)' if equipment['Limited'] else ''}:{detail_html}",
                picture_class=equipment['Image'],
                progression=equipment['EquippedAndMaxed'],
                goal=1
            )
            item_advice.equipment_name = equipment['Name']
            item_advice.equipment_limited = equipment['Limited']
            item_advice.stat_line = stat_line
            item_advice.stat_lines = [stat_line]
            item_advice.detail_html = detail_html
            equipment_advice[slot].append(item_advice)
            if (
                equipment['EquippedAndMaxed']
                and index != len(equipment_list) - 1
                and equipment['Name'] != equipment_list[index + 1]['Name']
            ):
                # Don't check items that come after the equipped item because they are worse than the equipped item
                break
    return equipment_advice


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
    drop_rate_advice_group_dict['Account'] = get_drop_rate_account_advice_group()
    player_specific_advice: TabbedAdviceGroup = get_drop_rate_player_advice_groups()
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
