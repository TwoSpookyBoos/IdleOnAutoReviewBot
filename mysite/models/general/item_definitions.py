from dataclasses import dataclass
from typing import TypeVar


@dataclass
class ItemDefinition:
    name: str
    code_name: str
    type: str
    description: str
    amount: float | int | None

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

