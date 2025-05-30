from consts.consts_w1 import stamp_maxes, capacity_stamps, stamps_dict, unavailable_stamps_list, tiered_stamps, ordered_tiers_stamps, remaining_stamps
from consts.consts_w3 import max_trapping_critter_types, dreams_that_unlock_new_bonuses, library_subgroup_tiers, old_library_subgroup_tiers
from consts.consts_w6 import gfood_codes
from consts.progression_tiers import stamps_progressionTiers, combatLevels_progressionTiers, secret_class_progressionTiers, achievements_progressionTiers, \
    greenstack_progressionTiers, vault_progressionTiers, bribes_progressionTiers, smithing_progressionTiers, statues_progressionTiers, \
    starsigns_progressionTiers, owl_progressionTiers, bubbles_progressionTiers, vials_progressionTiers, sigils_progressionTiers, post_office_progression_tiers, \
    islands_progressionTiers, sampling_progressionTiers, salt_lick_progression_tiers, deathNote_progressionTiers, atoms_progressionTiers, \
    prayers_progressionTiers, breeding_progressionTiers, rift_progressionTiers, divinity_progressionTiers, sailing_progressionTiers, gaming_progressionTiers, \
    farming_progressionTiers

def finalize_progression_tiers():
    update_w1_stamps()

def update_w1_stamps():
    # In the 3rd to last tier, set every Capacity Stamp to its max from stamp_maxes
    stamps_progressionTiers[max(stamps_progressionTiers) - 2]['Stamps']['Specific'] = {stampName: stamp_maxes[stampName] for stampName in capacity_stamps}
    for tier in stamps_progressionTiers:
        for requiredStamp in stamps_progressionTiers[tier].get('Stamps', {}).get('Specific', []):
            if requiredStamp not in capacity_stamps and requiredStamp != 'Crop Evo Stamp':
                tiered_stamps.add(requiredStamp)
    for stampType in stamps_dict:
        for stamp in stamps_dict[stampType].values():
            if stamp['Name'] not in unavailable_stamps_list and stamp['Name'] not in capacity_stamps:
                if stamp['Name'] in tiered_stamps:
                    ordered_tiers_stamps.append(stamp['Name'])
                else:
                    remaining_stamps.append(stamp['Name'])

    # In the 2nd to last tier, set every previously required stamp to its max from stamp_maxes
    stamps_progressionTiers[max(stamps_progressionTiers) - 1]['Stamps']['Specific'] = {stamp: stamp_maxes[stamp] for stamp in ordered_tiers_stamps}

    # In the last tier, set every stamp not covered by the previous 2 to its max from stamp_maxes
    stamps_progressionTiers[max(stamps_progressionTiers)]['Stamps']['Specific'] = {stamp: stamp_maxes[stamp] for stamp in remaining_stamps}


true_max_tiers = {
    # General
    'Achievements': max(achievements_progressionTiers.keys()),
    'Active': 0,
    'Cards': 72,  #12 sets * 6 stars
    'Combat Levels': combatLevels_progressionTiers[-1][0],
    'Consumables': 0,
    'Drop Rate': 0,
    'Event Shop': 0,
    'Gem Shop': 0,
    'Greenstacks': max(greenstack_progressionTiers.keys()),
    'Endangered Greenstacks': 1,
    'Secret Class Path': max(secret_class_progressionTiers.keys()),

    # Master Classes
    'Grimoire': 0,
    'Compass': 0,

    # World 1
    'Bribes': max(bribes_progressionTiers.keys()),
    'Owl': max(owl_progressionTiers.keys()),
    'Smithing': max(smithing_progressionTiers.keys()),
    'Stamps': max(stamps_progressionTiers.keys()),
    'Star Signs': max(starsigns_progressionTiers.keys()),
    'Statues': max(statues_progressionTiers.keys()),
    'Upgrade Vault': max(vault_progressionTiers.keys()),

    # World 2
    'Bubbles': bubbles_progressionTiers[-1][0],
    'Pay2Win': 1,
    'Sigils': max(sigils_progressionTiers.keys()),
    'Vials': max(vials_progressionTiers.keys()),
    'Arcade': 0,
    'Bonus Ballot': 0,
    'Islands': max(islands_progressionTiers.keys()),
    'Killroy': 0,
    'Post Office': max(post_office_progression_tiers.keys()),

    # World 3
    'Armor Sets': 7,
    'Atom Collider': max(atoms_progressionTiers.keys()),
    'Buildings': 0,
    'Death Note': deathNote_progressionTiers[-1][0],
    'Equinox': len(dreams_that_unlock_new_bonuses) + 1,
    'Library': len(library_subgroup_tiers),
    'Library Characters': len(old_library_subgroup_tiers),
    'Refinery': 1,  #Pass or Fail
    'Salt Lick': max(salt_lick_progression_tiers.keys()),
    'Sampling': max(sampling_progressionTiers.keys()),
    'Trapping': max_trapping_critter_types,
    'Prayers': max(prayers_progressionTiers.keys()),

    # World 4
    'Breeding': max(breeding_progressionTiers.keys()),
    'Cooking': 6+1,  #TODO
    'Rift': max(rift_progressionTiers.keys()),

    # World 5
    'Divinity': max(divinity_progressionTiers.keys()),
    'Gaming': max(gaming_progressionTiers.keys()),
    'Sailing': max(sailing_progressionTiers.keys()),
    'Slab': 0,

    # Caverns
    'Glowshroom Tunnels': 0,
    'Shallow Caverns': 0,
    'Underground Overgrowth': 0,
    'Villagers': 0,

    # World 6
    'Beanstalk': len(gfood_codes) * 2,
    'Farming': max(farming_progressionTiers.keys()),
    'Sneaking': 0,
    'Summoning': 0
}
