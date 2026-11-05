from collections import Counter

from consts.progression_tiers import breeding_progressionTiers
from consts.w4.breeding import (
    pet_species,
    shiny_bonus_exclusions,
    shiny_bonus_names,
    shiny_bonus_tier,
)
from models.w4.breeding import Breeding

SHINY_DAYS = 5.0
BREEDABILITY_DAYS = 7.0


def _raw_breeding(extra_pets: int = 0, extra_worlds: int = 0) -> dict:
    # Save with `extra_pets` more (or, if negative, fewer) pets per world and
    # `extra_worlds` more (or fewer) worlds than the code
    world_sizes = [len(world_pets) for world_pets in pet_species]
    if extra_worlds < 0:
        world_sizes = world_sizes[:extra_worlds]
    world_sizes += [10] * extra_worlds
    counts = [size + extra_pets for size in world_sizes]
    raw = [[] for _ in range(len(counts) + 22)]
    raw[1] = counts
    for world, count in enumerate(counts, start=1):
        raw[world + 12] = [BREEDABILITY_DAYS] * count
        raw[world + 21] = [SHINY_DAYS] * count
    return {"Breeding": raw}


def _pets(breeding: Breeding) -> list:
    return [pet for pets in breeding.species.values() for pet in pets.values()]


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


def test_save_with_fewer_pets_than_code_defaults_missing_pets():
    breeding = Breeding(_raw_breeding(extra_pets=-1))
    for world, world_pets in enumerate(pet_species, start=1):
        pets = list(breeding.species[world].values())
        assert len(pets) == len(world_pets)
        *known, missing = pets
        for pet in known:
            assert pet.unlocked
            assert pet.shiny_days == SHINY_DAYS
            assert pet.breedability_days == BREEDABILITY_DAYS
        assert not missing.unlocked
        assert missing.shiny_days == 0
        assert missing.breedability_days == 0
        assert missing.breedability_heart == "breedability-heart-1"


def test_save_with_more_pets_than_code_ignores_extra_pets():
    breeding = Breeding(_raw_breeding(extra_pets=3))
    for world, world_pets in enumerate(pet_species, start=1):
        assert len(breeding.species[world]) == len(world_pets)
    for pet in _pets(breeding):
        assert pet.unlocked
        assert pet.shiny_days == SHINY_DAYS
        assert pet.breedability_days == BREEDABILITY_DAYS


def test_save_without_breeding_data_defaults_all_pets():
    breeding = Breeding({})
    pets = _pets(breeding)
    assert len(pets) == sum(len(world_pets) for world_pets in pet_species)
    for pet in pets:
        assert not pet.unlocked
        assert pet.shiny_days == 0
        assert pet.breedability_days == 0
    assert not any(breeding.genetics.values())


def test_save_with_fewer_worlds_than_code_defaults_missing_world():
    breeding = Breeding(_raw_breeding(extra_worlds=-1))
    *known_worlds, missing_world = breeding.species.values()
    assert len(breeding.species) == len(pet_species)
    for pet in (pet for pets in known_worlds for pet in pets.values()):
        assert pet.unlocked
        assert pet.shiny_days == SHINY_DAYS
        assert pet.breedability_days == BREEDABILITY_DAYS
    assert len(missing_world) == len(pet_species[-1])
    for pet in missing_world.values():
        assert not pet.unlocked
        assert pet.shiny_days == 0
        assert pet.breedability_days == 0


def test_save_with_more_worlds_than_code_ignores_extra_worlds():
    breeding = Breeding(_raw_breeding(extra_worlds=1))
    assert len(breeding.species) == len(pet_species)
    for pet in _pets(breeding):
        assert pet.unlocked
        assert pet.shiny_days == SHINY_DAYS
        assert pet.breedability_days == BREEDABILITY_DAYS
