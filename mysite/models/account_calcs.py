from consts.consts_autoreview import MultiToValue
from consts.w3.equinox import ribbon_cloud_dream_number
from models.general.golden_food import calculate_golden_food_multis
from utils.logging import get_logger

logger = get_logger(__name__)

def calculate_account(account):
    _calculate_wave_1(account)
    _calculate_wave_2(account)
    _calculate_wave_3(account)
    _calculate_wave_4(account)


def _calculate_wave_1(account):
    # These numbers are used by formulas in _calculate_wave_2, so must be calculated first
    _calculate_caverns_majiks(account)
    _calculate_w2_arcade(account)
    account.tesseract.calculate_upgrades()
    _calculate_w6_emperor(account)
    account.summoning.calculate_winner_bonus_multi(
        account.sneaking.pristine_charms["Crystal Comb"].value,
        account.gemshop.purchases["King Of All Winners"],
        account.merits[5][4],
        account.sailing.artifacts["The Winz Lantern"].level,
        account.achievements,
        account.armor_sets["GODSHARD SET"].total_value,
        account.gemshop.bundles["ban_i"].owned,
        account.emperor["Summoning Winner Bonuses"].value,
    )
    account.summoning.calculate_bonuses()
    _calculate_general_friend_bonuses(account)
    account.gallery.calculate_palette_bonuses(
        account.legend_talents['Picasso Gaming'].value
    )
    account.farming.calculate_exotic_market_bonus()

def _calculate_general_friend_bonuses(account):
    account.friend_bonuses.calculate_bonuses(
        account.companions,
        account.event_points_shop['Friendly Slot'].owned,
    )

def _calculate_caverns_majiks(account):
    have_doot = account.companions.has("King Doot")
    account.caverns.villagers["Cosmos"].calculate_bonuses(have_doot)


def _calculate_w6_emperor(account):
    # Dependency: _calculate_master_classes_tesseract_upgrades, sneaking, _calculate_w2_arcade, gemshop
    account.emperor.calculate_max_attempt(account.gemshop, account.sneaking.emporium)
    account.emperor.calculate_bonus_multi(account.arcade, account.tesseract)
    account.emperor.calculate_bonuses()


def _calculate_w2_arcade(account):
    account.arcade.calculate_values(account.companions)

def _calculate_w4_tome(account):
    # Dependency: _calculate_w4_meal_multi, bonus talent levels, meritocracy
    account.tome.calculate_live_talent_max(account.meals['Buncha Banana'].value)
    account.tome.calculate_star_talents(
        account.characters.safe,
        account.family_bonuses['Wizard'].value,
        account.stamps['Talent S Stamp'].total_value,
        account.guild_bonuses['Star Dazzle'].value,
        account.alchemy_p2w.sigils['Two Starz'],
        account.sailing.artifacts.chilled_yarn_multi,
        account.meritocracy[21].value,
        account.bribes['Star Scraper'],
        account.companions['Flying Worm'].bonus,
    )
    account.tome.calculate_score(account.manual_tome_score)


def _calculate_wave_2(account):
    _calculate_general(account)
    # Lab connections gate bonuses read all through wave 2
    _calculate_w5(account)
    _calculate_w4_lab(account)
    _calculate_master_classes(account)
    _calculate_w1(account)
    _calculate_w2(account)
    account.tesseract.calculate_tachyon_sources(
        account.characters.acs, account.lab_jewels, account.arcade, account.emperor,
        account.alchemy_bubbles, account.sneaking, account.gemshop, account.alchemy_vials,
        account.companions.has('Balloonfish')
    )
    _calculate_w3(account)
    _calculate_w4(account)
    _calculate_w7(account)

def _calculate_general(account):
    account.add_alert_list('General', account.item_filter.get_alerts(
        account.slab,
        account.stored_assets,
        account.all_assets,
        account.autoloot,
        account.equinox.dreams[17].completed,
    ))
    account.world_progress.calculate(account.achievements, account.death_note)
    _calculate_general_storage_slots(account)

def _calculate_general_storage_slots(account):
    account.storage.calculate_other_sources(
        account.event_points_shop, account.vault, account.construction_buildings, account.gemshop
    )


def _calculate_master_classes(account):
    account.grimoire.calculate_upgrades()
    # account.grimoire.calculate_bone_sources(...)  #Moved to wave3 as it relies on Caverns/Gambit
    account.compass.calculate_upgrades()
    account.compass.calculate_dust_sources(
        account.characters.wws, account.sneaking, account.all_assets, account.arcade, account.lab_jewels, account.emperor
    )

def _calculate_w1(account):
    account.vault.calculate(
        account.glimbo, account.research.grid, account.event_points_shop
    )
    _calculate_w1_starsigns(account)
    _calculate_w1_stamps(account)
    account.owl.calculate(account.legend_talents, account.companions)
    account.basketball.calculate()
    account.darts.calculate()

def _calculate_w1_starsigns(account):
    account.star_signs.calculate_seraph(
        account.tesseract.upgrades['Astrology Cultism'].level, account.characters.all_skills['Summoning']
    )
    account.star_signs.calculate_silkrode(account.lab_chips['Silkrode Nanochip'])


def _calculate_w1_stamps(account):
    # Dependency: legend talents
    account.stamps.calculate_total_values(
        [
            account.atom_collider['Aluminium - Stamp Supercharger'].value,
            account.sneaking.pristine_charms['Jellypick'].value,
            account.compass.upgrades['Abomination Slayer XVII'].total_value,
            MultiToValue(account.armor_sets['EMPEROR SET'].total_value),
            20 * account.event_points_shop['Extra Exaltedness'].owned,
            # "PaletteBonus"(23) in source. Last updated in v2.531.0
            account.gallery.exalted_palette_bonus,
            # "ExoticBonusQTY"(49) in source. Last updated in v2.531.0
            account.farming.exotic_market['EXALTED ELDOU'].value,
            # "Spelunk[4][3]" in source. Last updated in v2.531.0
            account.spelunk.exalt_stamp_bonus,
            account.legend_talents['Wowa Woowa'].value,
            # "RoG_BonusQTY"(17) in source. Last updated in v2.531.0
            account.sushi_station.get_milestone_bonus_value('Exalted Stamp Bonus'),
            # "RoG_BonusQTY"(50) in source. Last updated in v2.531.0
            account.jelly_operator.obstructions['Fancy Facet'].bonus_value / 100,
        ],
        account.lab_bonuses['Certified Stamp Book'].enabled,
        account.sneaking.pristine_charms['Liqorice Rolle'].value,
    )

def _calculate_w2(account):
    _calculate_w2_vials(account)
    _calculate_w2_sigils(account)
    _calculate_w2_prisma(account)
    _calculate_w2_ballot(account)
    _calculate_w2_islands_trash(account)
    _calculate_w2_killroy(account)

def _calculate_w2_vials(account):
    account.alchemy_vials.calculate_values(account.vault, account.rift, account.lab_bonuses)

def _calculate_w2_sigils(account):
    account.alchemy_p2w.sigils.calculate_precharge_levels(
        account.sneaking.emporium['Ionized Sigils'].obtained
    )

def _calculate_w2_prisma(account):
    account.alchemy_bubbles.calculate_prisma_multi(
        account.tesseract,
        account.arcade,
        account.sushi_station,
        account.jelly_operator,
        account.gallery,
        account.alchemy_p2w.sigils,
        account.farming.exotic_market,
        account.legend_talents,
        account.companions,
    )

def _calculate_w2_ballot(account):
    account.ballot.calculate_values(
        account.equinox.upgrades['Voter Rights'].level,
        account.caverns.villagers["Cosmos"].majiks.idleon['Voter Integrity'].value,
        account.summoning.bonuses["Ballot Bonus"].value,
        account.event_points_shop['Gilded Vote Button'].owned,
        account.event_points_shop['Royal Vote Button'].owned,
        account.companions['Mashed Potato'].bonus,
        account.companions['Crystal Cuttlefish'].bonus,
        account.legend_talents['Democracy FTW'].value,
    )

def _calculate_w2_islands_trash(account):
    account.islands.calculate_trash_shop(account.stamps, account.stored_assets, account.bribes)

def _calculate_w2_killroy(account):
    account.killroy.calculate_available(account.equinox.upgrades['Shades of K'].level)


def _calculate_w3(account):
    _calculate_w3_refinery(account)
    _calculate_w3_building_max_levels(account)
    _calculate_w3_atom_collider(account)
    _calculate_w3_shrines(account)

def _calculate_w3_building_max_levels(account):
    # Gambit's +100 Tower levels is applied in _calculate_caverns
    account.construction_buildings.calculate_max_levels(
        account.rift['SkillMastery'].unlocked,
        sum(account.characters.all_skills['Construction']),
        account.atom_collider['Carbon - Wizard Maximizer'].level,
    )

def _calculate_w3_refinery(account):
    account.refinery.calculate(account.companions['Panda'].bonus, account.merits[2][6].level)

def _calculate_w3_atom_collider(account):
    account.atom_collider.calculate_max_levels(
        account.gaming.superbits['Isotope Discovery'].unlocked,
        account.compass.upgrades['Atomic Potential'],
        account.event_points_shop['Higgs Boson'].owned,
    )
    account.atom_collider.calculate_costs(
        account.merits[4][6].level,
        account.construction_buildings['Atom Collider'].level,
        account.gaming.superbits['Atom Redux'].unlocked,
        account.alchemy_bubbles['Atom Split'].base_value,
        account.stamps['Atomic Stamp'].total_value,
        account.grimoire.upgrades['Death of the Atom Price'].total_value,
        account.compass.upgrades['Atomic Cost Crash'].total_value,
    )

def _calculate_w3_shrines(account):
    account.shrines.calculate_values(
        next(c.getStars() for c in account.cards if c.name == 'Chaotic Chizoar')
    )


def _calculate_w4(account):
    _calculate_w4_cooking_max_plate_levels(account)
    _calculate_w4_lab_bonuses(account)

def _calculate_w4_cooking_max_plate_levels(account):
    account.cooking.calculate_max_plate_level(
        account.sailing.artifacts['Causticolumn'].level,
        account.rift['EldritchArtifact'].unlocked,
        account.sneaking.emporium,
        account.grimoire.upgrades['Supreme Head Chef Status'],
        account.spelunk.caves["Lunarheim"],
    )

def _calculate_w4_lab(account):
    # Seam: connections need sibling systems, and meals rerun when Black Diamond lights
    account.lab_mainframe.calculate(
        account.characters.safe,
        account.divinity.account_wide_arctis,
        account.gemshop.purchases['Souped Up Tube'].owned,
        account.sneaking.emporium,
        account.meals,
        next(card for card in account.cards if card.codename == 'Crystal3'),
        account.lab_chips['Conductive Motherboard'],
        account.breeding,
        account.merits[3][4].level,
        account.equinox.upgrades['Laboratory Fuse'].level
        + account.summoning.bonuses['Lab Con Range'].value,
        lambda: _calculate_w4_meal_multi(account),
    )

def _calculate_w4_meal_multi(account):
    account.meals.calculate_values(
        account.lab_jewels['Black Diamond Rhinestone'].active_value,
        account.breeding.total_shiny_levels['Bonuses from All Meals'],
        account.summoning.bonuses["Meal Bonuses"].as_multi,
        account.companions.get_multi('Wickerlight Spirit', 'Meal Bonus'),
        emperor_set=MultiToValue(account.armor_sets['EMPEROR SET'].total_value),
        cloud_73=account.equinox.dreams[ribbon_cloud_dream_number].completed,
        jelly_rog_60=account.jelly_operator.obstructions['Soldier Shiv'].bonus_value,
        max_summoning_level=max(account.characters.all_skills['Summoning'], default=0),
    )

def _calculate_w4_lab_bonuses(account):
    account.lab_bonuses.calculate_nblb(
        account.lab_jewels['Pyrite Rhinestone'].enabled,
        account.sailing.artifacts['Amberite'].level,
        account.gaming.superbits['Moar Bubbles'].unlocked,
        account.gaming.superbits['Even Moar Bubbles'].unlocked,
        account.merits[3][6].level,
    )

def _calculate_w4_tome_bonuses(account):
    account.tome.calculate_bonuses(
        account.grimoire, account.armor_sets, account.event_points_shop
    )


def _calculate_w5(account):
    account.divinity.calculate(
        account.companions.has('King Doot')
        or 'Arctis' in account.caverns.villagers["Cosmos"].majiks.idleon["Pocket Divinity"].link
    )

def _calculate_caverns(account):
    # Minau measures Tome score, Gambit points read Minau
    account.caverns.villagers["Minau"].calculate_bonuses()
    account.construction_buildings.calculate_gambit_levels(
        account.caverns.caves['Gambit'].bonuses[9].unlocked
    )


def _calculate_w6_sneaking_gemstones(account):
    account.sneaking.calculate_gemstones_values(
        account.get_current_max_talent("Generational Gemstones")
    )


def _calculate_w6_sneaking_pristine_chance(account):
    # Dependency: _calculate_master_classes (Compass upgrades)
    account.sneaking.calculate_pristine_chance(
        account.compass.upgrades['Pristine Collector'].total_value
    )


def _calculate_w6_farming(account):
    # Runs in wave3 due to Land Rank multi from Talents
    farming = account.farming
    farming.calculate_market_bonus(
        account.gemshop.purchases['Plot Of Land'].owned, account.merits[5][2].level
    )
    farming.calculate_land_rank_bonus(account.get_current_max_talent("Dank Rank"))
    farming.calculate_crop_depot_bonus(
        account.lab_bonuses['Depot Studies PhD'], account.lab_jewels['Pure Opal Rhombol'],
        account.grimoire, account.vault, account.sneaking.emporium,
    )
    farming.calculate_crop_value_multi(account.ballot)
    # Dependency: Summoning regular battle
    farming.calculate_crop_evo_multi(
        account.characters,
        account.alchemy_bubbles,
        account.alchemy_vials,
        account.tome.score,
        account.stamps['Crop Evo Stamp'].total_value,
        account.meals,
        account.star_signs,
        account.characters.all_skills['Farming'],
        account.rift['SkillMastery'],
        account.ballot[29],
        account.achievements,
        account.killroy.skull_shop,
        account.caverns.caves['The Lamp'].wishes['World 6 Majigers'],
        account.summoning.bonuses,
    )
    farming.calculate_crop_speed(account.alchemy_vials, account.summoning.bonuses)
    farming.calculate_bean_bonus(
        account.sneaking.emporium['Deal Sweetening'].value, account.achievements
    )
    farming.calculate_og(
        account.achievements,
        account.star_signs,
        account.merits[5][2].level,
        account.sneaking.pristine_charms['Taffy Disc'].value,
    )


def _calculate_w6_summoning(account):
    account.summoning.calculate_doublers(
        account.caverns.caves["Gambit"].bonuses[0].value,
        account.event_points_shop["Summoning Star"].owned,
    )


def _calculate_wave_3(account):
    _calculate_w3_library_max_book_levels(account)
    _calculate_w3_equinox_max_levels(account)
    _calculate_general_character_bonus_talent_levels(account)
    _calculate_w4_tome(account)
    _calculate_w4_tome_bonuses(account)
    _calculate_caverns(account)
    _calculate_w6_summoning(account)
    _calculate_general_crystal_spawn_chance(account)
    _calculate_w6_sneaking_gemstones(account)
    _calculate_w6_sneaking_pristine_chance(account)
    account.grimoire.calculate_bone_sources(
        account.characters.dbs, account.sneaking, account.caverns, account.all_assets,
        account.arcade, account.lab_jewels, account.emperor
    )
    _calculate_class_unique_kill_stacks(account)
    _calculate_w6_farming(account)

def _calculate_w3_library_max_book_levels(account):
    # Dependency: Summoning regular battle
    account.library.calculate_max_book_levels(
        account.construction_buildings,
        account.achievements,
        account.atom_collider,
        account.sailing,
        account.merits,
        account.saltlick,
        account.summoning,
    )

def _calculate_w3_equinox_max_levels(account):
    account.equinox.calculate_max_levels(
        account.summoning.bonuses["Equinox Max LV"].value,
        account.gaming.superbits['Equinox Unending'].unlocked,
    )

def _calculate_general_character_bonus_talent_levels(account):
    account.library.calculate_bonus_talents(
        account.armor_sets, account.companions, account.family_bonuses, account.equinox,
        account.achievements, account.sneaking, account.grimoire, account.tesseract,
    )
    for char in account.characters.safe:
        char.calculate_bonus_talent_levels(
            account.library.account_wide_bonus_talents,
            account.divinity.account_wide_arctis or char.isArctisLinked(),
            account.alchemy_bubbles['Big P'].base_value,
            account.coral_kid[3].level,
            account.gaming.superbits['Timmy Talented'].unlocked,
            account.library.max_book_level,
            account.family_bonuses['Elemental Sorcerer'].value,
        )
        char.active_super_talents = account.spelunk.get_super_talents(
            char.character_index, char.active_talent_preset
        )
        # Character has no account access
        char.super_talent_levels = account.super_talent_levels

def _calculate_general_crystal_spawn_chance(account):
    account.crystal_spawn_chance.calculate(
        next(card for card in account.cards if card.name == 'Poop'),
        next(card for card in account.cards if card.name == 'Demon Genie'),
        account.lab_chips['Omega Nanochip'].owned + account.lab_chips['Omega Motherboard'].owned,
        account.stamps['Crystallin'].total_value,
        account.characters,
        account.shrines['Crescent Shrine'].value,
    )

def _calculate_class_unique_kill_stacks(account):
    account.class_kill_talents.calculate_values(
        account.characters.safe, account.get_best_talent_level
    )

def _calculate_wave_4(account):
    # Mostly stuff that relies on Talent Level calculations that happen in Wave 3
    _calculate_w1_statues(account)
    _calculate_w6_beanstalk(account)

def _calculate_w1_statues(account):
    account.statues.calculate_values(
        [char.max_talents.get('56', 0) for char in account.characters.vmans],
        account.sailing.artifacts['The Onyx Lantern'].level,
        account.zenith_market['TRUE ZEN'].value,
        account.meritocracy[26].value,
        account.event_points_shop['Smiley Statue'].owned,
        account.vault.upgrades['Statue Bonanza'].total_value,
    )


def _calculate_w6_beanstalk(account):
    # Dependency: Emporium
    account.beanstalk.calculate_unlocked_tier(account.sneaking.emporium)
    account.beanstalk.calculate_golden_food_multi(calculate_golden_food_multis(
        characters=account.characters,
        best_talent_level=account.get_best_talent_level,
        companions=account.companions,
        armor_sets=account.armor_sets,
        family_bonuses=account.family_bonuses,
        death_note=account.death_note,
        sigils=account.alchemy_p2w.sigils,
        artifacts=account.sailing.artifacts,
        meritocracy=account.meritocracy,
        star_signs=account.star_signs,
        breeding=account.breeding,
        tesseract=account.tesseract,
        cards=account.cards,
        achievements=account.achievements,
        jelly_operator=account.jelly_operator,
        stamps=account.stamps,
        meals=account.meals,
        bribes=account.bribes,
        pristine_charms=account.sneaking.pristine_charms,
        ballot=account.ballot,
        legend_talents=account.legend_talents,
        vault=account.vault,
        alchemy_bubbles=account.alchemy_bubbles,
    ))
    account.beanstalk.calculate_bonuses()


def _calculate_w7(account):
    account.spelunk.calculate_lore_bonus(account.sailing.artifacts["Pointagon"])
    account.advice_fish.calculate_bonuses()
    account.meritocracy.calculate_bonuses()
    account.zenith_market.calculate_bonuses()
    account.research.calculate_bonuses(account)
    account.glimbo.calculate_drop_rate_multi(account.research)
    account.sushi_station.calculate_bonuses()
    account.dancing_coral.calculate_bonuses()
    account.coral_kid.calculate_bonuses()
    account.jelly_operator.calculate_bonuses(account)
    account.gallery.calculate_bonuses(account)

