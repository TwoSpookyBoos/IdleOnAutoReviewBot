from collections import Counter

from consts.progression_tiers import breeding_progressionTiers
from consts.w4.breeding import (
    shiny_bonus_exclusions,
    shiny_bonus_names,
    shiny_bonus_tier,
)


def test_shiny_bonus_tier_covers_every_shiny_bonus_once():
    tiered = Counter(
        bonus for bonuses in shiny_bonus_tier.values() for bonus in bonuses
    )
    assert tiered == Counter(shiny_bonus_names)


def test_breeding_tiers_use_known_shiny_bonuses():
    used = {
        bonus
        for tier in breeding_progressionTiers.values()
        for bonus in [*tier.get("Shinies", {}), *tier.get("Max Shinies", [])]
    }
    assert used <= set(shiny_bonus_names)


def test_shiny_bonus_exclusions_use_known_shiny_bonuses():
    assert set(shiny_bonus_exclusions) <= set(shiny_bonus_names)
