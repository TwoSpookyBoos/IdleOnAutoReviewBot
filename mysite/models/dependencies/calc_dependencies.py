from models.account_calcs import _calculate_caverns_gambit, _calculate_w6_summoning_winner_bonuses, \
    _calculate_w6_summoning_doublers, _calculate_w6_sneaking_gemstones, _calculate_w6_farming_og, \
    _calculate_w6_farming_markets, _calculate_w6_farming_land_ranks, _calculate_w6_farming_crop_value, \
    _calculate_w6_farming_crop_speed, _calculate_w6_farming_crop_evo, _calculate_w6_farming_crop_depot, \
    _calculate_w6_farming_bean_bonus, _calculate_w6_emperor, _calculate_w5_divinity_offering_costs, \
    _calculate_w5_account_wide_arctis, _calculate_w4_tome_bonuses, _calculate_w4_tome, _calculate_w4_meal_multi, \
    _calculate_w4_lab_bonuses, _calculate_w4_jewel_multi, _calculate_w4_cooking_max_plate_levels, \
    _calculate_w3_shrine_values, _calculate_w3_shrine_advices, _calculate_w3_library_max_book_levels, \
    _calculate_w3_equinox_max_levels, _calculate_w3_collider_cost_reduction, _calculate_w3_collider_base_costs, \
    _calculate_w3_collider_atoms, _calculate_w3_building_max_levels, _calculate_w3_armor_sets, _calculate_w2_vials, \
    _calculate_w2_sigils, _calculate_w2_postOffice, _calculate_w2_killroy, _calculate_w2_islands_trash, \
    _calculate_w2_cauldrons, _calculate_w2_ballot, _calculate_w2_arcade, _calculate_w1_upgrade_vault, \
    _calculate_w1_statues, _calculate_w1_starsigns, _calculate_w1_stamps, _calculate_w1_owl_bonuses, \
    _calculate_master_classes_tesseract_upgrades, _calculate_master_classes_tesseract_tachyon_sources, \
    _calculate_master_classes_grimoire_upgrades, _calculate_master_classes_grimoire_bone_sources, \
    _calculate_master_classes_compass_upgrades, _calculate_master_classes_compass_dust_sources, \
    _calculate_general_item_filter, _calculate_general_highest_world_reached, _calculate_general_crystal_spawn_chance, \
    _calculate_general_character_bonus_talent_levels, _calculate_general_alerts, _calculate_class_unique_kill_stacks, \
    _calculate_caverns_the_well, _calculate_caverns_the_harp, _calculate_caverns_the_bell, _calculate_caverns_studies, \
    _calculate_caverns_motherlode_layers, _calculate_caverns_monuments_justice, _calculate_caverns_monuments_bravery, \
    _calculate_caverns_monument_bonuses, _calculate_caverns_measurements_multis, _calculate_caverns_measurements_base, \
    _calculate_caverns_majiks, _calculate_caverns_jar_collectibles, _calculate_general_guild_bonuses
from models.models import Account


def calc_args(account: Account):
    return {
        _calculate_caverns_gambit: [account],
        _calculate_caverns_jar_collectibles: [account],
        _calculate_caverns_majiks: [account],
        _calculate_caverns_measurements_base: [account],
        _calculate_caverns_measurements_multis: [account],
        _calculate_caverns_monument_bonuses: [account],
        _calculate_caverns_monuments_bravery: [account],
        _calculate_caverns_monuments_justice: [account],
        _calculate_caverns_motherlode_layers: [account],
        _calculate_caverns_studies: [account],
        _calculate_caverns_the_bell: [account],
        _calculate_caverns_the_harp: [account],
        _calculate_caverns_the_well: [account],
        _calculate_class_unique_kill_stacks: [account],
        _calculate_general_alerts: [account],
        _calculate_general_character_bonus_talent_levels: [account],
        _calculate_general_crystal_spawn_chance: [account],
        _calculate_general_guild_bonuses: [account],
        _calculate_general_highest_world_reached: [account],
        _calculate_general_item_filter: [account],
        _calculate_master_classes_compass_dust_sources: [account],
        _calculate_master_classes_compass_upgrades: [account],
        _calculate_master_classes_grimoire_bone_sources: [account],
        _calculate_master_classes_grimoire_upgrades: [account],
        _calculate_master_classes_tesseract_tachyon_sources: [account],
        _calculate_master_classes_tesseract_upgrades: [account],
        _calculate_w1_owl_bonuses: [account],
        _calculate_w1_stamps: [account],
        _calculate_w1_starsigns: [account],
        _calculate_w1_statues: [account],
        _calculate_w1_upgrade_vault: [account],
        _calculate_w2_arcade: [account],
        _calculate_w2_ballot: [account],
        _calculate_w2_cauldrons: [account],
        _calculate_w2_islands_trash: [account],
        _calculate_w2_killroy: [account],
        _calculate_w2_postOffice: [account],
        _calculate_w2_sigils: [account],
        _calculate_w2_vials: [account],
        _calculate_w3_armor_sets: [account],
        _calculate_w3_building_max_levels: [account],
        _calculate_w3_collider_atoms: [account],
        _calculate_w3_collider_base_costs: [account],
        _calculate_w3_collider_cost_reduction: [account],
        _calculate_w3_equinox_max_levels: [account],
        _calculate_w3_library_max_book_levels: [account],
        _calculate_w3_shrine_advices: [account],
        _calculate_w3_shrine_values: [account],
        _calculate_w4_cooking_max_plate_levels: [account],
        _calculate_w4_jewel_multi: [account],
        _calculate_w4_lab_bonuses: [account],
        _calculate_w4_meal_multi: [account],
        _calculate_w4_tome: [account],
        _calculate_w4_tome_bonuses: [account],
        _calculate_w5_account_wide_arctis: [account],
        _calculate_w5_divinity_offering_costs: [account],
        _calculate_w6_emperor: [account],
        _calculate_w6_farming_bean_bonus: [account],
        _calculate_w6_farming_crop_depot: [account],
        _calculate_w6_farming_crop_evo: [account],
        _calculate_w6_farming_crop_speed: [account],
        _calculate_w6_farming_crop_value: [account],
        _calculate_w6_farming_land_ranks: [account],
        _calculate_w6_farming_markets: [account],
        _calculate_w6_farming_og: [account],
        _calculate_w6_sneaking_gemstones: [account],
        _calculate_w6_summoning_doublers: [account],
        _calculate_w6_summoning_winner_bonuses: [account],
    }


def calc_dependencies():
    return {
        _calculate_caverns_gambit: [_calculate_caverns_measurements_base],
        _calculate_caverns_jar_collectibles: [],
        _calculate_caverns_majiks: [],
        _calculate_caverns_measurements_base: [_calculate_caverns_majiks],
        _calculate_caverns_measurements_multis: [_calculate_caverns_measurements_base],
        _calculate_caverns_monument_bonuses: [_calculate_caverns_majiks],
        _calculate_caverns_monuments_bravery: [_calculate_caverns_measurements_base],
        _calculate_caverns_monuments_justice: [],
        _calculate_caverns_motherlode_layers: [],
        _calculate_caverns_studies: [],
        _calculate_caverns_the_bell: [],
        _calculate_caverns_the_harp: [],
        _calculate_caverns_the_well: [],
        _calculate_class_unique_kill_stacks: [_calculate_general_character_bonus_talent_levels],
        _calculate_general_alerts: [],
        _calculate_general_character_bonus_talent_levels: [_calculate_w3_armor_sets, _calculate_w5_account_wide_arctis, _calculate_w3_library_max_book_levels],
        _calculate_general_crystal_spawn_chance: [_calculate_w1_stamps],
        _calculate_general_guild_bonuses: [],
        _calculate_general_highest_world_reached: [],
        _calculate_general_item_filter: [],
        _calculate_master_classes_compass_dust_sources: [_calculate_master_classes_compass_upgrades],
        _calculate_master_classes_compass_upgrades: [],
        _calculate_master_classes_grimoire_bone_sources: [_calculate_master_classes_grimoire_upgrades],
        _calculate_master_classes_grimoire_upgrades: [],
        _calculate_master_classes_tesseract_tachyon_sources: [_calculate_master_classes_tesseract_upgrades],
        _calculate_master_classes_tesseract_upgrades: [],
        _calculate_w1_owl_bonuses: [],
        _calculate_w1_stamps: [_calculate_master_classes_compass_upgrades, _calculate_w3_armor_sets],
        _calculate_w1_starsigns: [],
        _calculate_w1_statues: [_calculate_w1_upgrade_vault],
        _calculate_w1_upgrade_vault: [],
        _calculate_w2_arcade: [],
        _calculate_w2_ballot: [_calculate_caverns_majiks],
        _calculate_w2_cauldrons: [],
        _calculate_w2_islands_trash: [],
        _calculate_w2_killroy: [],
        _calculate_w2_postOffice: [],
        _calculate_w2_sigils: [],
        _calculate_w2_vials: [_calculate_w1_upgrade_vault],
        _calculate_w3_armor_sets: [],
        _calculate_w3_building_max_levels: [],
        _calculate_w3_collider_atoms: [],
        _calculate_w3_collider_base_costs: [_calculate_master_classes_compass_upgrades],
        _calculate_w3_collider_cost_reduction: [_calculate_w1_stamps, _calculate_master_classes_grimoire_upgrades],
        _calculate_w3_equinox_max_levels: [],
        _calculate_w3_library_max_book_levels: [_calculate_w6_summoning_winner_bonuses],
        _calculate_w3_shrine_advices: [],
        _calculate_w3_shrine_values: [],
        _calculate_w4_cooking_max_plate_levels: [],
        _calculate_w4_jewel_multi: [],
        _calculate_w4_lab_bonuses: [],
        _calculate_w4_meal_multi: [_calculate_w3_armor_sets],
        _calculate_w4_tome: [],
        _calculate_w4_tome_bonuses: [_calculate_w3_armor_sets],
        _calculate_w5_account_wide_arctis: [],
        _calculate_w5_divinity_offering_costs: [],
        _calculate_w6_emperor: [],
        _calculate_w6_farming_bean_bonus: [],
        _calculate_w6_farming_crop_depot: [_calculate_master_classes_grimoire_upgrades],
        _calculate_w6_farming_crop_evo: [_calculate_w2_vials, _calculate_w1_stamps, _calculate_w6_summoning_winner_bonuses, _calculate_w1_starsigns],
        _calculate_w6_farming_crop_speed: [_calculate_w6_summoning_winner_bonuses, _calculate_w2_vials],
        _calculate_w6_farming_crop_value: [],
        _calculate_w6_farming_land_ranks: [_calculate_general_character_bonus_talent_levels],
        _calculate_w6_farming_markets: [],
        _calculate_w6_farming_og: [_calculate_w1_starsigns],
        _calculate_w6_sneaking_gemstones: [_calculate_general_character_bonus_talent_levels],
        _calculate_w6_summoning_doublers: [_calculate_caverns_gambit],
        _calculate_w6_summoning_winner_bonuses: [_calculate_w3_armor_sets, _calculate_w6_emperor],
    }
