import re

from consts.idleon.w3.equinox import DreamChallenge, DreamUpg
from utils.text_formatting import kebab

# Levels start at Dream[2]
equinox_upgrade_level_offset = 2
# "Grid_Bonus",86 gate in "CloudsTask" in source. Last updated in v2.528.0
equinox_first_nightmare = 37
# "UpgMaxLV" in source. Last updated in v2.528.0
equinox_summoning_max_level_upgrades = [
    'Matching Scims', 'Slow Roast Wiz', 'Metal Detector', 'Faux Jewels',
    'Food Lust', 'Equinox Symbols', 'Voter Rights', 'Nonstop Studies',
]
equinox_superbit_max_level_upgrades = [
    'Matching Scims', 'Slow Roast Wiz', 'Metal Detector', 'Faux Jewels',
    'Food Lust', 'Equinox Symbols', 'Voter Rights',
]
equinox_superbit_max_levels = 10
# { becomes value/max value
equinox_bonus_descriptions = {
    'Liquidvestment': '{% of excess liquid invested into Decant levels',
    'Matching Scims': '+{% Damage multi',
    'Slow Roast Wiz': '+{% Worship tower damage per second',
    'Laboratory Fuse': '+{ px Lab connection range',
    'Metal Detector': '+{% nugget size per small nugget',
    'Faux Jewels': '+{% Drop Rate',
    'Food Lust': '{ max stacks of cheaper Meal upgrades',
    'Equinox Symbols': '+{ All Talent LVs',
    'Voter Rights': '+{% Ballot Bonus',
    'Nonstop Studies': '+{% Research EXP multi',
}

_unlock_reward = 'Unlock_next_Equinox_upgrade'
_max_level_reward = re.compile(r"^\+(\d+)_Max_LV_for_(?:Equinox_Upgrade_)?'([^']+)'")

equinox_dreams = [
    {
        'Number': index + 1,
        'Display Name': (
            f"Nightmare {index + 2 - equinox_first_nightmare}" if index + 1 >= equinox_first_nightmare
            else f"Dream {index + 1}"
        ),
        'Nightmare': index + 1 >= equinox_first_nightmare,
    }
    for index in range(len(DreamChallenge))
]
# Dream 77's Killroy Prime challenge isn't completable yet
equinox_impossible_dreams = [77]
equinox_possible_dream_count = len(DreamChallenge) - len(equinox_impossible_dreams)
equinox_unlock_dreams = [
    index + 1 for index, (_, _, reward, _) in enumerate(DreamChallenge) if reward == _unlock_reward
]

_max_level_increases: dict[str, dict[int, int]] = {}
for index, (_, _, reward, _) in enumerate(DreamChallenge):
    if match := _max_level_reward.match(reward):
        _max_level_increases.setdefault(match[2].replace('_', ' '), {})[index + 1] = int(match[1])

equinox_upgrades = []
for unlock_order, (raw_name, _, base_max_level, value_per_level) in enumerate(DreamUpg):
    if value_per_level == 'Filler':
        continue
    name = raw_name.replace('_', ' ')
    increases = _max_level_increases.get(name, {})
    equinox_upgrades.append({
        'Name': name,
        'Unlock Order': unlock_order,
        'Base Max Level': int(base_max_level),
        'Final Max Level': int(base_max_level) + sum(increases.values()),
        'Max Level Increases': increases,
        'Value Per Level': int(value_per_level),
        'Summoning Expands': name in equinox_summoning_max_level_upgrades,
        'Superbit Expands': name in equinox_superbit_max_level_upgrades,
        'Description': equinox_bonus_descriptions.get(name, ''),
        'Image': kebab(name),
    })
