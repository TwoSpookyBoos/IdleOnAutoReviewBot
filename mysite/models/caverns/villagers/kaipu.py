from dataclasses import dataclass
from functools import cached_property

from consts.caverns.cavern import get_resource_image
from consts.consts_autoreview import EmojiType
from consts.idleon.caverns.villager.kaipu import available_schematics, schematics_data
from models.advice.advice import Advice
from models.caverns.villagers.villager import Villager
from utils.logging import get_logger

logger = get_logger(__name__)


class SchematicBonus:
    def __init__(self, index: int, data: dict, is_bought: bool):
        self.name = data["Name"]
        self._template: str = data["Template"]
        self.unlock_order = data["UnlockOrder"]
        self.bought = is_bought
        self.image = f"engineer-schematic-{index}"
        self.resource = get_resource_image(data["ResourceIndex"])

    @cached_property
    def level(self):
        if not self.bought:
            return 0
        from models.general.session_data import session_data

        match self.unlock_order:
            case 44:  # Gloomie Lootie
                return session_data.account.caverns["Caverns"]["Grotto"]["OpalsFound"]
            case 81:  # Sanctum of LOOT
                return session_data.account.caverns["Caverns"]["The Temple"][
                    "OpalsFound"
                ]
            case _:
                return 0

    @cached_property
    def value(self):
        match self.unlock_order:
            case 44:  # Gloomie Lootie
                return 5 * self.level
            case 81:  # Sanctum of LOOT
                return 20 * self.level
            case _:
                return 0

    def full_name(self, link_to_section: bool = True) -> str:
        schematic_text = "{{Schematic|#villagers}}" if link_to_section else "Schematic"
        return f"{schematic_text} #{self.unlock_order + 1} - {self.name}"

    def get_advice(self):
        description_only = self._template.split("<br>")[0]
        return Advice(
            label=f"{self.full_name(link_to_section=False)}:<br>{description_only}",
            picture_class=self.image,
            progression=int(self.bought),
            goal=1,
            resource=self.resource,
        )

    def get_bonus_advice(self):
        description = self._template.replace("{", f"{self.value}")
        return Advice(
            label=f"{self.full_name()}:<br>{description}",
            picture_class=self.image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
        )


@dataclass
class Schematic(dict[str, SchematicBonus]):
    bought: int = 0
    unlocked: int = 0


class Kaipu(Villager):
    def __init__(self, **kwargs):
        super().__init__(name="Kaipu", unlock_at=2, role="The Engineer", **kwargs)
        self.schematics = Schematic()

    def parse_feature(self, raw_caverns_list: list):
        raw_schematics_list = raw_caverns_list[13]
        try:
            self.schematics.bought = sum(raw_schematics_list)
        except Exception:
            self.schematics.bought = 0
            logger.warning("Can't sum raw_schematics_list")
        for index, schematic_info in enumerate(schematics_data):
            is_bought = raw_schematics_list[index] > 0
            bonus = SchematicBonus(index, schematic_info, is_bought)
            self.schematics[bonus.name] = bonus
        self.schematics.unlocked = min(
            available_schematics, 1 + (self.level * 3) + (self.level // 5)
        )

    def calculate_bonuses(self):
        pass

    @cached_property
    def max_useful_level(self) -> int:
        needed_level = 29
        unlocked_schematics = 1 + (needed_level * 3) + (needed_level // 5)
        while unlocked_schematics < available_schematics:
            needed_level += 1
            unlocked_schematics = 1 + (needed_level * 3) + (needed_level // 5)
        return needed_level

    def stat_advices(self) -> list[Advice]:
        max_level = available_schematics * 5 // 16
        advice_list = self.base_stat_advice(max_level)
        advice_list.append(
            Advice(
                label="Total Schematics unlocked by leveling Kaipu",
                picture_class="empty-schematic",
                progression=self.schematics.unlocked,
                goal=available_schematics,
            )
        )
        advice_list.append(
            Advice(
                label="Total Schematics purchased",
                picture_class="empty-schematic",
                progression=self.schematics.bought,
                goal=available_schematics,
            )
        )
        return advice_list

    def feature_advice(self) -> dict[str, list[Advice]] | None:
        return {
            "Unpurchased Schematics": [
                bonus.get_advice()
                for bonus in sorted(
                    self.schematics.values(), key=lambda value: value.unlock_order
                )
                if not bonus.bought and bonus.unlock_order < available_schematics
            ]
        }
