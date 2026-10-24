from consts.consts_autoreview import ValueToMulti
from consts.consts_w4 import (
    breeding_genetics_list,
    breeding_shiny_bonus_list,
    breeding_species_dict,
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
from models.advice.advice import Advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_get, safer_index

logger = get_logger(__name__)


class Pet:
    def __init__(self, world: int, info: dict):
        self.name: str = info["Name"]
        self.world: int = world
        self.genetic: str = info["Genetic"]
        self.shiny_bonus: str = info["ShinyBonus"]
        self.unlocked: bool = False
        self.shiny_level: int = 0
        self.days_to_shiny_level: float = 0
        self.breedability_days: float = 0.0
        self.breedability_multi: float = 1
        self.breedability_heart: str = "breedability-heart-1"

    def parse(self, unlocked: bool, shiny_days: float, breedability_days: float):
        self.unlocked = unlocked
        self.shiny_level = getShinyLevelFromDays(shiny_days)
        self.days_to_shiny_level = getDaysToNextShinyLevel(shiny_days)
        self.breedability_days = breedability_days
        self.breedability_multi = getBreedabilityMultiFromDays(breedability_days)
        self.breedability_heart = getBreedabilityHeartFromMulti(self.breedability_multi)


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
            genetic: False for genetic in breeding_genetics_list
        }
        self.total_shiny_levels: dict[str, int] = {
            bonus: 0 for bonus in breeding_shiny_bonus_list
        }
        # Shiny bonus to its pets, soonest to level first
        self.shiny_bonus_pets: dict[str, list[Pet]] = {
            bonus: [] for bonus in breeding_shiny_bonus_list
        }
        self.species: dict[int, dict[str, Pet]] = {}
        for world, world_pets in breeding_species_dict.items():
            breedability_days = [
                safer_convert(entry, 0.0)
                for entry in safer_index(raw_breeding, world + 12, [])
            ]
            shiny_days = [
                safer_convert(entry, 0.0)
                for entry in safer_index(raw_breeding, world + 21, [])
            ]
            self.species[world] = {}
            for pet_index, info in world_pets.items():
                pet = Pet(world, info)
                try:
                    pet.parse(
                        unlocked_counts[world] > pet_index,
                        shiny_days[pet_index],
                        breedability_days[pet_index],
                    )
                    self.total_shiny_levels[pet.shiny_bonus] += pet.shiny_level
                    if pet.unlocked:
                        self.genetics[pet.genetic] = True
                except Exception:
                    logger.exception(f"Failed to parse breeding pet {pet.name}")
                    pet = Pet(world, info)
                self.species[world][pet.name] = pet
                self.shiny_bonus_pets[pet.shiny_bonus].append(pet)

        for pets in self.shiny_bonus_pets.values():
            pets.sort(key=lambda pet: float(pet.days_to_shiny_level))

    def calculate_egg_slots(self, royal_egg_cap: int, merit_level: int):
        self.egg_slots += (
            royal_egg_cap + self.upgrades["Egg Capacity"].level + merit_level
        )

    def calculate_pet_damage(
        self,
        *,
        electrolyte_vial: float,
        barley_lost: bool,
        croissant: float,
        wedding_cake: float,
        characters: list,
        power_bowower_unlocked: bool,
        arcade_bonus: float,
        vault_pet_punchies: float,
    ):
        self.pet_damage_multi_a = ValueToMulti(self.upgrades["Blooming Axe"].value)
        self.barley_lost = barley_lost
        self.barley_lost_bonus = int(barley_lost) * 5
        talent = next(
            t for t in all_talentsDict.values() if t["name"] == "Arena Spirit"
        )
        self.arena_spirit_level = 0
        self.arena_spirit_goal_level = 0
        for char in characters:
            try:
                level = (
                    char.current_preset_talents[str(talent["skillIndex"])]
                    + char.total_bonus_talent_levels
                )
            except KeyError:
                continue
            if level > self.arena_spirit_level:
                self.arena_spirit_level = level
                self.arena_spirit_goal_level = char.max_talents_over_books
        self.arena_spirit_bonus = lava_func(
            talent["funcY"], self.arena_spirit_level, talent["y1"], talent["y2"]
        )
        self.power_bowower_unlocked = power_bowower_unlocked
        self.power_bowower_bonus = int(power_bowower_unlocked) * 30
        self.pet_damage_multi_b = ValueToMulti(
            electrolyte_vial
            + self.barley_lost_bonus
            + croissant
            + wedding_cake
            + self.arena_spirit_bonus
            + self.power_bowower_bonus
            + arcade_bonus
            + vault_pet_punchies
        )
        self.pet_damage_multi = round(
            self.pet_damage_multi_a * self.pet_damage_multi_b, 2
        )

    def get_pet_damage_advice(self) -> Advice:
        return Advice(
            label=f"Total Pet Damage bonus: {self.pet_damage_multi}x",
            picture_class="vault-upgrade-58",
        )

    def get_barley_lost_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Achievement|#achievements }}}} - Barley Lost: "
            f"+{self.barley_lost_bonus}%",
            picture_class="barley-lost",
            progression=int(self.barley_lost),
            goal=1,
        )

    def get_arena_spirit_advice(self) -> Advice:
        return Advice(
            label=f"Beast Master Talent passive- Arena Spirit: "
            f"+{self.arena_spirit_bonus:.2f}%",
            picture_class="arena-spirit",
            progression=self.arena_spirit_level,
            goal=self.arena_spirit_goal_level,
        )

    def get_power_bowower_advice(self) -> Advice:
        status = "+30% if equipped" if self.power_bowower_unlocked else "Locked."
        return Advice(
            label=f"{{{{ Star Sign|#star-signs }}}} -  Power Bowower: {status}",
            picture_class="power-bowower",
            progression=int(self.power_bowower_unlocked),
            goal=1,
        )
