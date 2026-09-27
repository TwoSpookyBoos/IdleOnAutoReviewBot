from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from consts.consts_w3 import atoms_list, collider_storage_limit_list
from models.advice.advice import Advice
from models.master_classes.compass import CompassUpgrade
from utils.safer_data_handling import safe_loads, safer_get, safer_math_pow


class Atom:
    def __init__(self, info: list, level: int):
        self.name: str = info[0]
        self.image: str = self.name.split(" - ")[0]
        self.level: int = level
        self.max_level: int = 20
        self.value_per_level: float = info[4]
        self.base_cost_to_upgrade: float = 0
        self.discounted_cost_to_upgrade: float = 0
        self.base_cost_to_max: float = 0
        self.discounted_cost_to_max: float = 0
        self._cost_increment: float = info[1]
        self._cost_exponent: float = info[2]
        self._cost_base: float = info[3]
        self._description_template: str = info[5]

    @cached_property
    def value(self) -> float:
        return self.level * self.value_per_level

    @cached_property
    def description(self) -> str:
        description = self._description_template
        if "{" in description:
            description = description.replace("{", f"{self.value}")
        if "}" in description:
            description = description.replace("}", f"{ValueToMulti(self.value):.3f}")
        return description

    def cost_at_level(self, level: int) -> float:
        return (self._cost_base + (self._cost_increment * level)) * safer_math_pow(
            self._cost_exponent, level
        )

    def calculate_costs(self, cost_reduction_multi: float):
        if self.level >= self.max_level:
            return
        self.base_cost_to_upgrade = self.cost_at_level(self.level)
        for level in range(self.level, self.max_level):
            self.base_cost_to_max += self.cost_at_level(level)
        self.discounted_cost_to_upgrade = (
            self.base_cost_to_upgrade * cost_reduction_multi
        )
        self.discounted_cost_to_max = self.base_cost_to_max * cost_reduction_multi

    def get_advice(self, additional_text: str = "") -> Advice:
        return Advice(
            label=f"{self.name}: {self.description}{additional_text}"
            f"<br>({self.value_per_level} per level)",
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
        )

    def get_tier_advice(self, goal: int) -> Advice:
        return Advice(
            label=self.name,
            picture_class=self.image,
            progression=self.level,
            goal=goal,
        )


class AtomCollider(dict[str, Atom]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.on: bool = safer_get(raw_optlacc, 132, False)
        self.magnesium_days: int = safer_get(raw_optlacc, 363, 0)
        try:
            self.storage_limit: int = collider_storage_limit_list[
                safer_get(raw_optlacc, 133, -1)
            ]
        except IndexError:
            self.storage_limit: int = collider_storage_limit_list[-1]
        try:
            self.particles = raw_data.get("Divinity", {})[39]
        except (IndexError, KeyError, TypeError):
            self.particles = "Unknown"

        raw_atoms = safe_loads(raw_data.get("Atoms", []))
        for index, info in enumerate(atoms_list):
            try:
                level = int(raw_atoms[index])
            except (IndexError, TypeError, ValueError):
                level = 0
            self[info[0]] = Atom(info, level)

        self.cost_reduction_raw: float = 1
        self.cost_reduction_multi: float = 1
        self.cost_discount: float = 0

    def calculate_max_levels(
        self,
        isotope_discovery: bool,
        atomic_potential_upgrade: CompassUpgrade,
        higgs_boson: bool,
    ):
        atomic_potential = (
            atomic_potential_upgrade.total_value
            if atomic_potential_upgrade.level > 0
            else 0
        )
        for atom in self.values():
            if isotope_discovery:
                atom.max_level += 10
            if atomic_potential:
                atom.max_level += atomic_potential
            if higgs_boson:
                atom.max_level += 20

    def calculate_costs(
        self,
        merit_level: int,
        collider_building_level: int,
        atom_redux: bool,
        atom_split_value: float,
        atomic_stamp_value: float,
        grimoire_value: float,
        compass_value: float,
    ):
        # Max was removed after DB and WW both introduced near-infinite scaling sources
        cost_reduction_raw = ValueToMulti(
            7 * merit_level
            + (collider_building_level / 10)
            + 1 * self["Neon - Damage N' Cheapener"].level
            + 10 * atom_redux
            + atom_split_value
            + atomic_stamp_value
            + grimoire_value
            + compass_value
        )
        self.cost_reduction_raw = cost_reduction_raw
        self.cost_reduction_multi = 1 / cost_reduction_raw
        self.cost_discount = (1 - (1 / cost_reduction_raw)) * 100
        for atom in self.values():
            atom.calculate_costs(self.cost_reduction_multi)
