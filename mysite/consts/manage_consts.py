# The purpose of this file is making updates to consts.
# This is "run" when the file is imported in flask_app.py so that it only runs once per deploy,
# instead of once per profile/data submit.

from consts import consts_w2, progression_tiers
from consts.consts_general import gstack_unique_expected, cardset_names, max_card_stars
from consts.consts_w1 import stamp_maxes, unavailable_stamps_list
from consts.consts_w2 import max_maxable_vials
from consts.consts_w4 import get_final_combat_level_required_for_tome
from consts.progression_tiers import stamps_progressionTiers, vials_progressionTiers, true_max_tiers, greenstack_progressionTiers, combatLevels_progressionTiers
from utils.item_data_utils import get_all_stamps, get_capacity_stamps
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)

def finalize_consts():
    finalize_general_greenstacks()
    finalize_general_cards()
    finalize_general_combat_levels()
    finalize_w1_stamps()
    finalize_w2_vials()

def finalize_general_greenstacks():
    try:
        assert greenstack_progressionTiers[5]['Required Stacks'] == len(gstack_unique_expected)
    except AssertionError:
        logger.error(
            f"Total number of Expected GStacks not in sync between "
            f"tier {greenstack_progressionTiers[5]['Required Stacks']} and "
            f"list {len(gstack_unique_expected)}"
        )
        greenstack_progressionTiers[5]['Required Stacks'] = max(greenstack_progressionTiers[5]['Required Stacks'], len(gstack_unique_expected))

def finalize_general_cards():
    try:
        assert true_max_tiers['Cards'] == len(cardset_names) * (max_card_stars + 1)
    except AssertionError:
        logger.error(
            f"Total number of Card Set stars out of sync between "
            f"tier {true_max_tiers['Cards']} and "
            f"variables {len(cardset_names) * (max_card_stars + 1)}"
        )
        true_max_tiers['Cards'] = max(true_max_tiers['Cards'], len(cardset_names) * (max_card_stars + 1))

def finalize_general_combat_levels():
    try:
        assert get_final_combat_level_required_for_tome() == combatLevels_progressionTiers[-2][1]
    except AssertionError:
        logger.error(
            f"Total Account Level for Tome out of sync between "
            f"variable {get_final_combat_level_required_for_tome()} and "
            f"tier {combatLevels_progressionTiers[-2][1]}"
        )
        progression_tiers.combatLevels_progressionTiers[-2][1] = get_final_combat_level_required_for_tome()


def finalize_w1_stamps():
    tiered_stamps = set()
    ordered_tiers_stamps = []
    remaining_stamps = []

    capacity_stamps = get_capacity_stamps()
    # In the 3rd to last tier, set every Capacity Stamp to its max from stamp_maxes
    stamps_progressionTiers[max(stamps_progressionTiers) - 2]['Stamps']['Specific'] = {stamp['Name']: stamp_maxes[stamp['Name']] for stamp in capacity_stamps}
    logger.debug(f"Successfully updated Stamp Tier {max(stamps_progressionTiers) - 2}")
    for tier in stamps_progressionTiers:
        if tier < max(stamps_progressionTiers) - 2:
            for required_stamp in stamps_progressionTiers[tier].get('Stamps', {}).get('Specific', []):
                if (
                        required_stamp not in capacity_stamps
                        and required_stamp != 'Crop Evo Stamp'
                ):
                    tiered_stamps.add(required_stamp)
    all_stamps = get_all_stamps()
    for stamp in all_stamps:
        if stamp['Name'] not in stamp_maxes and stamp['Name'] not in unavailable_stamps_list:
            logger.warning(f"No entry in stamp_maxes for: {stamp['Name']}")
        if stamp['Name'] not in unavailable_stamps_list and stamp['Name'] not in capacity_stamps:
            if stamp['Name'] in tiered_stamps:
                ordered_tiers_stamps.append(stamp['Name'])
            else:
                remaining_stamps.append(stamp['Name'])

    # In the 2nd to last tier, set every previously required stamp to its max from stamp_maxes
    stamps_progressionTiers[max(stamps_progressionTiers) - 1]['Stamps']['Specific'] = {stamp: stamp_maxes.get(stamp, 0) for stamp in ordered_tiers_stamps}
    logger.debug(f"Successfully updated Stamp Tier {max(stamps_progressionTiers) - 1}")

    # In the last tier, set every stamp not covered by the previous 2 to its max from stamp_maxes
    stamps_progressionTiers[max(stamps_progressionTiers)]['Stamps']['Specific'] = {stamp: stamp_maxes.get(stamp, 0) for stamp in remaining_stamps}
    logger.debug(f"Successfully updated Stamp Tier {max(stamps_progressionTiers)}")

def finalize_w2_vials():
    try:
        assert max_maxable_vials == vials_progressionTiers[true_max_tiers['Vials']]['Maxed']
    except AssertionError:
        logger.error(
            f"Max number of Maxable Vials not in sync between "
            f"variable {max_maxable_vials} and "
            f"tier {vials_progressionTiers[true_max_tiers['Vials']]['Maxed']}"
        )
        consts_w2.max_maxable_vials = max(max_maxable_vials, vials_progressionTiers[true_max_tiers['Vials']]['Maxed'])
        vials_progressionTiers[true_max_tiers['Vials']]['Maxed'] = max(max_maxable_vials, vials_progressionTiers[true_max_tiers['Vials']]['Maxed'])


finalize_consts()
