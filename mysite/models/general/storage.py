from functools import cached_property

from consts.consts_general import (
    storage_building_slots_per_level,
    storage_chests_dict,
    storage_chests_item_slots_max,
    storage_event_shop_slots,
    storage_gem_shop_slots,
    storage_vault_upgrades,
)
from models.advice.advice import Advice
from models.general.event_shop import EventShop
from models.general.gem_shop import GemShop
from models.general.models_consumables import StorageChest
from models.w3.buildings import Buildings
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads

logger = get_logger(__name__)


class StorageSource:
    def __init__(
        self,
        source: str,
        owned_slots: int,
        max_slots: int,
        label: str = "",
        image: str = "",
        progression: int = 0,
        goal: int = 0,
        resource: str = "",
    ):
        self.source: str = source
        self.owned_slots: int = owned_slots
        self.max_slots: int = max_slots
        self._label: str = label
        self._image: str = image
        self._progression: int = progression
        self._goal: int = goal
        self._resource: str = resource

    def get_advice(self) -> Advice:
        return Advice(
            label=self._label,
            picture_class=self._image,
            progression=self._progression,
            goal=self._goal,
            resource=self._resource if self.owned_slots < self.max_slots else "",
        )


class Storage(dict[str, StorageSource]):
    """Non-chest storage sources, by name"""

    def __init__(self, raw_data: dict):
        super().__init__()
        raw_used_chests = safe_loads(raw_data.get("InvStorageUsed", {}))
        if not isinstance(raw_used_chests, dict):
            raw_used_chests = {}
        unknown_chests = [
            f"{key}:{value}"
            for key, value in raw_used_chests.items()
            if int(key) not in storage_chests_dict
        ]
        if unknown_chests:
            logger.warning(
                f"Unknown Storage Chest found in JSON: {unknown_chests}. "
                f"Get these added to consts_general.storage_chests_dict"
            )
        self.used_chests: list[StorageChest] = [
            chest for chest in StorageChest if str(chest.value) in raw_used_chests
        ]
        self.missing_chests: list[StorageChest] = [
            chest for chest in StorageChest if str(chest.value) not in raw_used_chests
        ]

    @cached_property
    def used_chest_slots(self) -> int:
        return sum(storage_chests_dict.get(chest.value) for chest in self.used_chests)

    @property
    def other_slots_owned(self) -> int:
        return sum(source.owned_slots for source in self.values())

    @property
    def other_slots_max(self) -> int:
        return sum(source.max_slots for source in self.values())

    @property
    def total_slots_owned(self) -> int:
        return self.used_chest_slots + self.other_slots_owned

    @property
    def total_slots_max(self) -> int:
        return storage_chests_item_slots_max + self.other_slots_max

    def calculate_other_sources(
        self,
        event_points_shop: EventShop,
        vault,
        construction_buildings: Buildings,
        gemshop: GemShop,
    ):
        for name, slots in storage_event_shop_slots.items():
            bonus = event_points_shop[name]
            self[name] = StorageSource(
                source="Event Shop",
                owned_slots=slots * bonus.owned,
                max_slots=slots,
                label=f"{{{{ Event Shop|#event-shop }}}} - {name}: {slots} slots",
                image=bonus.image,
                progression=int(bonus.owned),
                goal=1,
                resource="event-point",
            )
        for name in storage_vault_upgrades:
            upgrade = vault.upgrades[name]
            # Advice comes from Vault.get_upgrade_advice
            self[name] = StorageSource(
                source="Vault",
                owned_slots=upgrade.value_per_level * upgrade.level,
                max_slots=upgrade.value_per_level * upgrade.max_level,
            )
        for name, slots_per_level in storage_building_slots_per_level.items():
            building = construction_buildings[name]
            owned_slots = slots_per_level * (building.level - 1)
            self[name] = StorageSource(
                source="Construction Building",
                owned_slots=owned_slots,
                max_slots=slots_per_level * (building.max_level - 1),
                label=f"{{{{ Construction Building|#buildings }}}} - {name}: "
                f"{owned_slots} total slots",
                image=building.image,
                progression=building.level,
                goal=building.max_level,
            )
        for name, slots in storage_gem_shop_slots.items():
            purchase = gemshop.purchases[name]
            owned_slots = slots * purchase.owned
            max_slots = slots * purchase.max_level
            self[name] = StorageSource(
                source="Gem Shop",
                owned_slots=owned_slots,
                max_slots=max_slots,
                label=f"{{{{ Gem Shop|#gem-shop }}}} - {name} "
                f"({purchase.subsection}): {owned_slots}/{max_slots} total slots",
                image=name,
                progression=purchase.owned,
                goal=purchase.max_level,
                resource="gem",
            )
