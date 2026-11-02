from collections.abc import Collection
from dataclasses import dataclass
from typing import TypeVar

from utils.number_formatting import round_and_trim


@dataclass
class ItemMiscBonus:
    effect: str
    value: int

    def __init__(self, effect, value):
        self.effect = effect.replace("_", " ").title()
        self.value = value

    def get_label(self, multi: float = 1) -> str:
        return f"+{round_and_trim(self.value * multi)}{self.effect}"


@dataclass
class ItemBonus:
    weapon_power: int = 0
    str: int = 0
    agi: int = 0
    wis: int = 0
    luk: int = 0
    defence: int = 0
    misc1: ItemMiscBonus | None = None
    misc2: ItemMiscBonus | None = None

    def get_misc_bonuses(
        self, stats: Collection[str] | None = None
    ) -> list[ItemMiscBonus]:
        """Non-empty misc bonuses, only `stats` (e.g. "% Drop Rate") if given."""
        return [
            misc
            for misc in (self.misc1, self.misc2)
            if misc and misc.effect != "0" and (stats is None or misc.effect in stats)
        ]

    def add_to(self, total: dict[str, float], multi: float):
        if multi == 0:
            return
        total[" Weapon Power"] += self.weapon_power * multi
        total[" STR"] += self.str * multi
        total[" AGI"] += self.agi * multi
        total[" WIS"] += self.wis * multi
        total[" LUK"] += self.luk * multi
        total[" Defence"] += self.defence * multi
        total[self.misc1.effect] += self.misc1.value * multi
        total[self.misc2.effect] += self.misc2.value * multi


@dataclass
class ItemDefinition:
    name: str
    code_name: str
    type: str
    description: str
    amount: float | int | None
    bonus: ItemBonus


@dataclass
class StampBonus:
    effect: str
    code_material: str
    scaling_type: str
    x1: int
    x2: int


@dataclass
class StampItemDefinition(ItemDefinition):
    stamp_bonus: StampBonus


ItemDef = TypeVar("ItemDef", bound=ItemDefinition | StampItemDefinition)


class ItemDefinitions(dict[str, ItemDef]):
    def get_item_from_codename(self, codename: str) -> ItemDef:
        return self[codename]

    def get_all_stamps(self) -> list[StampItemDefinition]:
        return [item for item in self.values() if isinstance(item, StampItemDefinition)]

    def get_capacity_stamps(self) -> list[StampItemDefinition]:
        return [stamp for stamp in self.get_all_stamps() if 'Carry Cap' in stamp.stamp_bonus.effect]

    def get_items_by_type(self, item_type: str) -> list[ItemDef]:
        return [item for item in self.values() if item.type == item_type]
