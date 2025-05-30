from consts.consts_general import gstack_unique_expected, max_card_stars, cardset_names
from consts.consts_w2 import max_maxable_vials
from consts.consts_w4 import get_final_combat_level_required_for_tome
from consts.progression_tiers import vials_progressionTiers, greenstack_progressionTiers, combatLevels_progressionTiers
from consts.progression_tiers_updater import true_max_tiers
from utils.logging import get_logger

logger = get_logger(__name__)


try:
    assert max_maxable_vials == vials_progressionTiers[true_max_tiers['Vials']]['Maxed']
except AssertionError:
    logger.exception(f"Max number of Maxable Vials not in sync between variable {max_maxable_vials} and tier {vials_progressionTiers[-1][2]}")

try:
    assert greenstack_progressionTiers[5]['Required Stacks'] == len(gstack_unique_expected)
except AssertionError:
    logger.exception(f"Total number of Expected GStacks not in sync between tier {greenstack_progressionTiers[5]['Required Stacks']} and list {len(gstack_unique_expected)}")

try:
    assert true_max_tiers['Cards'] == len(cardset_names) * (max_card_stars + 1)
except AssertionError:
    logger.exception(f"Total number of Card Set stars out of sync between tier {true_max_tiers['Cards']} and variables {len(cardset_names) * (max_card_stars + 1)}")

# try:
#     assert get_final_combat_level_required_for_tome() < combatLevels_progressionTiers[-2][1]
# except AssertionError:
#     logger.exception(f"Total Account Level for Tome out of sync between "
#                      f"variable {get_final_combat_level_required_for_tome()} and "
#                      f"tier {combatLevels_progressionTiers[-2][1]}")