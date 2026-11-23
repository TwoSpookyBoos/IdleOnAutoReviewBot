from functools import cached_property
from math import prod

from consts.consts_autoreview import ValueToMulti
from consts.consts_w4 import (
    breeding_upgrades_dict,
    getBreedabilityHeartFromMulti,
    getBreedabilityMultiFromDays,
    getDaysToNextShinyLevel,
    getShinyLevelFromDays,
    max_breeding_territories,
    slot_unlock_waves_list,
    territory_names,
)
from consts.idleon.lava_func import lava_func
from consts.w4.breeding import (
    breeding_genetics,
    pet_species,
    shiny_base_max_level,
    shiny_bonus_names,
)
from models.advice.advice import Advice
from models.general.session_data import session_data
from models.w1.star_signs import get_infinite_star_sign_levels
from utils.all_talentsDict import all_talentsDict
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_get, safer_index

# "Arena Spirit" Beast Master talent
_arena_spirit_index = 370


class Pet:
    def __init__(
        self,
        world: int,
        info: dict,
        breeding: "Breeding",
        unlocked: bool,
        shiny_days: float,
        breedability_days: float,
    ):
        self.name: str = info["Name"]
        self.world: int = world
        self.breeding = breeding
        self.genetic: str = info["Genetic"]
        self.shiny_bonus: str = info["Shiny Bonus"]
        self.shiny_bonus_description: str = info["Shiny Description"]
        self.shiny_bonus_per_level: int = info["Shiny Value Per Level"]
        self.unlocked: bool = unlocked
        self.shiny_days: float = shiny_days
        self.breedability_days: float = breedability_days
        self.breedability_multi: float = getBreedabilityMultiFromDays(breedability_days)
        self.breedability_heart: str = getBreedabilityHeartFromMulti(
            self.breedability_multi
        )

    @cached_property
    def shiny_level(self) -> int:
        return min(
            self.breeding.max_shiny_level, getShinyLevelFromDays(self.shiny_days)
        )

    @cached_property
    def days_to_shiny_level(self) -> float:
        if self.shiny_level >= self.breeding.max_shiny_level:
            return 0
        return getDaysToNextShinyLevel(self.shiny_days)

    @cached_property
    def shiny_bonus_value(self) -> int:
        return self.shiny_bonus_per_level * self.shiny_level

    @cached_property
    def max_shiny_bonus_value(self) -> int:
        return self.shiny_bonus_per_level * self.breeding.max_shiny_level

    def get_shiny_level_advice(self, goal: int) -> Advice:
        label = f"{self.shiny_bonus}: {self.name}"
        if self.days_to_shiny_level > 0:
            label += f"<br>{self.days_to_shiny_level:,.2f} base days to level"
        return Advice(
            label=label,
            picture_class=self.name,
            progression=self.shiny_level,
            goal=goal,
        )

    def get_shiny_advice(self) -> Advice:
        description = self.shiny_bonus_description.replace(
            "{", f"{self.shiny_bonus_value}/{self.max_shiny_bonus_value}"
        )
        return Advice(
            label=f"{{{{ Breeding|#breeding }}}} - Shiny {self.name}: {description}",
            picture_class=self.name,
            progression=self.shiny_level,
            goal=self.breeding.max_shiny_level,
        )


class BreedingUpgrade:
    def __init__(self, index: int, info: dict, level: int):
        self.name: str = info["Name"]
        self.level: int = level
        self.max_level: int = info["MaxLevel"]
        self.value: float = info["BonusValue"] * level
        self._image: str = f"breeding-bonus-{index - 1}"

    def get_advice(self) -> Advice:
        return Advice(
            label=f"Breeding Upgrade - {self.name}: +{self.value}%",
            picture_class=self._image,
            progression=self.level,
            goal=self.max_level,
        )


class Breeding:
    def __init__(self, raw_data: dict):
        raw_breeding = safe_loads(raw_data.get("Breeding", []))
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        self.egg_slots: int = 3

        self.arena_max_wave: int = 0
        try:
            self.arena_max_wave = int(raw_optlacc[89])
        except (IndexError, TypeError, ValueError):
            pass
        self.pet_slots_unlocked: int = 2 + sum(
            self.arena_max_wave > requirement for requirement in slot_unlock_waves_list
        )

        raw_upgrades = safer_index(raw_breeding, 2, [])
        self.upgrades: dict[str, BreedingUpgrade] = {}
        for index, info in breeding_upgrades_dict.items():
            try:
                level = raw_upgrades[index]
                self.upgrades[info["Name"]] = BreedingUpgrade(index, info, level)
            except (IndexError, TypeError):
                upgrade = BreedingUpgrade(index, info, 0)
                upgrade.value = 0
                self.upgrades[info["Name"]] = upgrade

        self.highest_unlocked_territory: int = safer_get(
            dict(enumerate(raw_optlacc)), 85, 0
        )
        self.highest_unlocked_territory_name: str = territory_names[
            min(max_breeding_territories, self.highest_unlocked_territory)
        ]
        # Territory name to unlocked
        self.territories: dict[str, bool] = {
            territory_names[index + 1]: index < self.highest_unlocked_territory
            for index in range(max_breeding_territories)
        }

        raw_unlocked_counts = safer_index(raw_breeding, 1, [])
        unlocked_counts = {}
        self.total_unlocked_count: int = 0
        for index in range(8):
            try:
                unlocked_counts[index + 1] = raw_unlocked_counts[index]
                self.total_unlocked_count += raw_unlocked_counts[index]
            except (IndexError, TypeError):
                unlocked_counts[index + 1] = 0

        self.genetics: dict[str, bool] = {
            genetic: False for genetic in breeding_genetics
        }
        # Shiny bonus to its pets, in world order
        self.shiny_bonus_pets: dict[str, list[Pet]] = {
            bonus: [] for bonus in shiny_bonus_names
        }
        self.species: dict[int, dict[str, Pet]] = {}
        for world, world_pets in enumerate(pet_species, start=1):
            breedability_days = [
                safer_convert(entry, 0.0)
                for entry in safer_index(raw_breeding, world + 12, [])
            ]
            shiny_days = [
                safer_convert(entry, 0.0)
                for entry in safer_index(raw_breeding, world + 21, [])
            ]
            self.species[world] = {}
            for pet_index, info in enumerate(world_pets):
                pet = Pet(
                    world,
                    info,
                    self,
                    unlocked=unlocked_counts[world] > pet_index,
                    shiny_days=safer_index(shiny_days, pet_index, 0.0),
                    breedability_days=safer_index(breedability_days, pet_index, 0.0),
                )
                if pet.unlocked:
                    self.genetics[pet.genetic] = True
                self.species[world][pet.name] = pet
                self.shiny_bonus_pets[pet.shiny_bonus].append(pet)

    @cached_property
    def max_shiny_level(self) -> int:
        # "SpecialPassives" "Lv" in source. Last updated in v2.550.0
        unlocked = session_data.account.menagerie.unlocks[11].owned
        return shiny_base_max_level + 10 * int(unlocked)

    @cached_property
    def shiny_over_level(self) -> int:
        # "SpecialzOverLVL" in source: Shiny LVs above the base max. v2.550.0
        return sum(
            max(0, pet.shiny_level - shiny_base_max_level)
            for pets in self.species.values()
            for pet in pets.values()
        )

    @cached_property
    def shiny_over_level_multi(self) -> float:
        # "ShinySpdMulti" in source. Last updated in v2.550.0
        return ValueToMulti(10 * self.shiny_over_level)

    def get_shiny_over_level_advice(self) -> Advice:
        total_pets = sum(len(pets) for pets in self.species.values())
        max_over_level = (self.max_shiny_level - shiny_base_max_level) * total_pets
        label = (
            f"Shiny OverLV (Shiny LVs above {shiny_base_max_level}): "
            f"{round(self.shiny_over_level_multi, 2)}x"
        )
        if max_over_level == 0:
            label += "<br>Needs {{ Menagerie|#luminous-menagerie }} Unlock 12"
        return Advice(
            label=label,
            picture_class="menagerie-unlock-11",
            progression=self.shiny_over_level,
            goal=max(max_over_level, 10 * total_pets),
        )

    @cached_property
    def total_shiny_levels(self) -> dict[str, int]:
        return {
            bonus: sum(pet.shiny_level for pet in pets)
            for bonus, pets in self.shiny_bonus_pets.items()
        }

    @cached_property
    def total_shiny_level_count(self) -> int:
        # "SpecialPassives" "Lv" in source is at least 1, even for a pet with no shiny
        # progress. "ShinyBonusS" skips such pets (so `shiny_level` is 0 for them), but
        # the Tome's shiny levels count them as LV 1. Last updated in v2.550.0
        return sum(
            max(1, pet.shiny_level)
            for pets in self.species.values()
            for pet in pets.values()
        )

    @cached_property
    def total_shiny_bonus_values(self) -> dict[str, int]:
        return {
            bonus: sum(pet.shiny_bonus_value for pet in pets)
            for bonus, pets in self.shiny_bonus_pets.items()
        }

    def calculate_egg_slots(self, royal_egg_cap: int, merit_level: int):
        self.egg_slots += (
            royal_egg_cap + self.upgrades["Egg Capacity"].level + merit_level
        )

    @cached_property
    def _barley_lost_bonus(self) -> int:
        # Depends on: achievements['Barley Lost']
        return 5 * session_data.account.achievements["Barley Lost"].complete

    @cached_property
    def _power_bowower_bonus(self) -> float:
        # `StarSigns["59"]` in source is for the logged in character: the best one
        # Depends on: star_signs, characters
        account = session_data.account
        infinite_levels = get_infinite_star_sign_levels(
            self.total_shiny_bonus_values["Infinite Star Signs"]
        )
        power_bowower = account.star_signs["Power Bowower"]
        seraph_multi = account.star_signs.seraph_multi
        return max(
            (
                power_bowower.value_for(char, 30, infinite_levels, seraph_multi)
                for char in account.characters.safe
            ),
            default=0,
        )

    @cached_property
    def _arena_spirit_levels(self) -> tuple[int, int]:
        # "getbonus2"(2, 370, -1) in source, logged in as the best character.
        # Returns the level and that character's max talent level
        # Depends on: characters
        account = session_data.account
        best_level, best_char = max(
            (
                (account.get_best_talent_level(_arena_spirit_index, char), char)
                for char in account.characters.safe
            ),
            key=lambda pair: pair[0],
            default=(0, None),
        )
        if best_char is None or best_level <= 0:
            return 0, 0
        return best_level, best_char.max_talents_over_books

    @cached_property
    def _arena_spirit_bonus(self) -> float:
        talent = all_talentsDict[_arena_spirit_index]
        level, _ = self._arena_spirit_levels
        return lava_func(talent["funcY"], level, talent["y1"], talent["y2"])

    @cached_property
    def _pet_damage_multis(self) -> dict[str, float]:
        # "PetBonusDMG" in source. Last updated in v2.561.0
        # Not modelled yet: "PaletteBonus" 26 (Lilac Purple)
        # Depends on: sushi_station, alchemy_vials['Electrolyte (Condensed Zap)'],
        # achievements['Barley Lost'], meals['Croissant'], meals['Wedding Cake'],
        # characters, star_signs['Power Bowower'], arcade[30],
        # vault.upgrades['Pet Punchies']
        account = session_data.account
        sushi_milestone = account.sushi_station.milestones["Breeding Mob Damage"]
        return {
            "A": ValueToMulti(self.upgrades["Blooming Axe"].value),
            "B": self.shiny_over_level_multi,
            "C": ValueToMulti(sushi_milestone.unlocked_value),
            "D": ValueToMulti(
                account.alchemy_vials["Electrolyte (Condensed Zap)"].value
                + self._barley_lost_bonus
                + account.meals["Croissant"].value
                + account.meals["Wedding Cake"].value
                + self._arena_spirit_bonus
                + self._power_bowower_bonus
                + account.arcade[30].value
                + account.vault.upgrades["Pet Punchies"].total_value
            ),
        }

    @cached_property
    def pet_damage_multi(self) -> float:
        return round(prod(self._pet_damage_multis.values()), 2)

    def get_pet_damage_advices(self) -> dict[str, list[Advice]]:
        account = session_data.account
        multis = {group: round(m, 2) for group, m in self._pet_damage_multis.items()}
        total = self.pet_damage_multi
        sushi_milestone = account.sushi_station.milestones["Breeding Mob Damage"]
        return {
            f"Total: {total}x": [
                Advice(
                    label=f"Total Pet Damage bonus: {total}x",
                    picture_class="vault-upgrade-58",
                )
            ],
            f"Multi Group A: {multis['A']}x": [
                self.upgrades["Blooming Axe"].get_advice()
            ],
            f"Multi Group B: {multis['B']}x": [self.get_shiny_over_level_advice()],
            f"Multi Group C: {multis['C']}x": [sushi_milestone.get_advice()],
            f"Multi Group D: {multis['D']}x": [
                account.alchemy_vials["Electrolyte (Condensed Zap)"].get_advice(
                    full_name=False
                ),
                self._get_barley_lost_advice(),
                account.meals["Croissant"].get_bonus_advice(),
                account.meals["Wedding Cake"].get_bonus_advice(),
                self._get_arena_spirit_advice(),
                self._get_power_bowower_advice(),
                account.arcade[30].get_advice(),
                account.vault.get_upgrade_advice("Pet Punchies"),
            ],
        }

    def _get_barley_lost_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Achievement|#achievements }}}} - Barley Lost: "
            f"+{self._barley_lost_bonus}%",
            picture_class="barley-lost",
            progression=int(self._barley_lost_bonus > 0),
            goal=1,
        )

    def _get_arena_spirit_advice(self) -> Advice:
        level, goal_level = self._arena_spirit_levels
        return Advice(
            label=f"Beast Master Talent passive- Arena Spirit: "
            f"+{self._arena_spirit_bonus:.2f}%",
            picture_class="arena-spirit",
            progression=level,
            goal=goal_level,
        )

    def _get_power_bowower_advice(self) -> Advice:
        star_signs = session_data.account.star_signs
        unlocked = star_signs["Power Bowower"].unlocked
        if not unlocked:
            status = "Locked."
        elif self._power_bowower_bonus:
            status = f"+{round_and_trim(self._power_bowower_bonus)}%"
        else:
            # What `value_for` gives once it is equipped
            equipped_bonus = round_and_trim(30 * star_signs.seraph_multi)
            status = f"+{equipped_bonus}% if equipped"
        return Advice(
            label=f"{{{{ Star Sign|#star-signs }}}} -  Power Bowower: {status}",
            picture_class="power-bowower",
            progression=int(unlocked),
            goal=1,
        )
