from dataclasses import dataclass
from typing import TypeVar


@dataclass
class ItemMiscBonus:
    effect: str
    value: int

    def __init__(self, effect, value):
        self.effect = effect.replace("_", " ").title()
        self.value = value


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
        return next(item for code, item in self.items() if code == codename)

    def get_all_stamps(self) -> list[StampItemDefinition]:
        return [item for item in self.values() if isinstance(item, StampItemDefinition)]

    def get_capacity_stamps(self) -> list[StampItemDefinition]:
        return [stamp for stamp in self.get_all_stamps() if 'Carry Cap' in stamp.stamp_bonus.effect]

    def get_items_by_type(self, item_type: str) -> list[ItemDef]:
        return [item for item in self.values() if item.type == item_type]
