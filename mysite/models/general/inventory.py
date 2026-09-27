from consts.consts_general import inventory_bags_dict, inventory_other_sources_dict
from models.advice.advice import Advice
from models.general.character import Character
from models.general.models_consumables import Bag
from utils.logging import get_logger

logger = get_logger(__name__)


class InventorySource:
    def __init__(self, info: dict, owned: bool):
        self.description: str = info["Description"]
        self.max_slots: int = info["Max Slots"]
        self.owned: bool = owned
        self._image: str = info["Image"]
        self._resource: str = info.get("Resource", "")

    @property
    def owned_slots(self) -> int:
        return self.max_slots * self.owned

    def get_advice(self) -> Advice:
        return Advice(
            label=f"{self.description}: {self.owned_slots}/{self.max_slots} slots",
            picture_class=self._image,
            progression=int(self.owned),
            goal=1,
            resource=self._resource,
        )


class Inventory(dict[str, InventorySource]):
    """Account wide inventory slot sources"""

    def __init__(self):
        super().__init__()
        for name, info in inventory_other_sources_dict.items():
            self[name] = InventorySource(info, owned=name == "Default")

    @property
    def owned_slots(self) -> int:
        return sum(source.owned_slots for source in self.values())

    @property
    def max_slots(self) -> int:
        return sum(source.max_slots for source in self.values())

    def calculate_owned(
        self,
        characters: list[Character],
        autoloot: bool,
        secret_pouch: bool,
        eternal_hunter: bool,
    ):
        self["Autoloot"].owned = autoloot
        self["Secret Pouch"].owned = secret_pouch
        # Only on characters that logged in since claiming it
        self["Fourth Anni"].owned = any(
            char.character_name for char in characters if "112" in char.inventory_bags
        )
        self["bon_f"].owned = eternal_hunter

        unknown_bags = {
            f"{bag}: {slots}"
            for char in characters
            for bag, slots in char.inventory_bags.items()
            if int(bag) not in inventory_bags_dict
        }
        if unknown_bags:
            logger.warning(
                f"Unknown Inventory Bags found in JSON: {unknown_bags}. "
                f"Get these added to consts_general.inventory_bags_dict"
            )
        for char in characters:
            char.calculate_inventory_slots(self.owned_slots)

    @staticmethod
    def missing_bags(character: Character) -> list[Bag]:
        return [bag for bag in Bag if str(bag.value) not in character.inventory_bags]
