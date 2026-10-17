from functools import cached_property
from math import floor

from consts.consts_autoreview import EmojiType, ValueToMulti
from consts.consts_w1 import (
    get_statue_type_index_from_name,
    statue_count,
    statue_type_count,
    statue_type_dict,
    statues_dict,
)
from consts.consts_w5 import max_sailing_artifact_level
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from models.general.character import Character
from models.general.event_shop import EventShopBonus
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.safer_data_handling import safe_loads, safer_convert, safer_index
from utils.text_formatting import kebab

logger = get_logger(__name__)

onyx_type_number = get_statue_type_index_from_name("Onyx")
zenith_type_number = get_statue_type_index_from_name("Zenith")
# Statue Bonanza applies to these
vault_statues = [statues_dict[i]["Name"] for i in [0, 1, 2, 6]]


class Statue:
    def __init__(self, info: dict, level: int, type_number: int):
        self.name: str = info["Name"]
        self.item_name: str = info["ItemName"]
        self.effect: str = info["Effect"]
        self.base_value: float = info["BaseValue"]
        self.farmer: str = info["Farmer"]
        self.resource: str = info["Resource"]
        self.level: int = level
        self.type_number: int = type_number
        self.type: str = statue_type_dict.get(type_number, "UnknownType")
        self.image: str = kebab(f"{self.type} {self.name}")
        self.value: float = self.base_value

    def calculate_value(self, multis: list[float]):
        self.value = self.base_value * self.level
        for multi in multis:
            self.value *= multi

    def get_advice(self) -> Advice:
        spacer = " " if not self.effect.startswith("%") else ""
        return Advice(
            label=f"Level {self.level} {self.type} {self.name}:"
            f"<br> +{round(self.value, 2):,g}{spacer}{self.effect}",
            picture_class=self.image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
            resource=self.resource,
        )


class Statues(dict[str, Statue]):
    def __init__(self, raw_data: dict, characters: list[Character]):
        super().__init__()
        # e.g. [2,2,2,...,0,0]
        raw_types = safe_loads(raw_data.get("StuG", []))
        if len(raw_types) != statue_count:
            raw_types += [0] * (statue_count - len(raw_types))
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        monolith_progress = parse_number(safer_index(raw_optlacc, 69, 0), 0)
        self.tome_drop_chance: int = safer_convert(safer_index(raw_optlacc, 200, 1), 1)
        self.onyx_unlocked: bool = (
            max(raw_types, default=0) >= onyx_type_number or monolith_progress >= 2
        )
        self.zenith_unlocked: bool = (
            max(raw_types, default=0) >= zenith_type_number or monolith_progress >= 3
        )

        # Normal statues level per character; Gold+ share across all
        levels = [0] * statue_count
        for char in characters:
            try:
                raw_char_statues = safe_loads(
                    raw_data.get(f"StatueLevels_{char.character_index}")
                )
                for index, raw_statue in enumerate(raw_char_statues):
                    if index >= statue_count:
                        logger.warning(
                            f"Statue index {index} missing from statues_dict"
                        )
                        continue
                    levels[index] = max(levels[index], raw_statue[0])
            except Exception as e:
                logger.warning(
                    f"Statue levels error, Character{char.character_index}: {e}"
                )

        for index, info in statues_dict.items():
            self[info["Name"]] = Statue(info, levels[index], raw_types[index])

        self.voodoo_multi: float = 1
        self.onyx_multi: float = 1
        self.zenith_multi: float = 1
        self.merit_multi: float = 1
        self.event_shop_multi: float = 1
        self.vault_multi: float = 1
        self.dragon_multi: float = 1

    @cached_property
    def maxed_count(self) -> int:
        return sum(statue.type_number >= statue_type_count for statue in self.values())

    @property
    def total_multi(self) -> float:
        return (
            self.voodoo_multi
            * self.onyx_multi
            * self.zenith_multi
            * self.dragon_multi
            * self.event_shop_multi
            * self.merit_multi
        )

    def calculate_values(
        self,
        voodoo_talent_levels: list[int],
        onyx_lantern_level: int,
        true_zen_value: float,
        meritocracy_value: float,
        smiley_statue_owned: bool,
        vault_multi: float,
    ):
        # Best Voodoo Statufication across Voodoo Masters
        voodoo = all_talentsDict[56]
        self.voodoo_multi = ValueToMulti(
            max(
                (
                    lava_func(voodoo["funcX"], level, voodoo["x1"], voodoo["x2"])
                    for level in voodoo_talent_levels
                ),
                default=0,
            )
        )
        self.onyx_multi = 2 + 0.3 * onyx_lantern_level
        self.zenith_multi = ValueToMulti(50 + floor(true_zen_value))
        self.merit_multi = ValueToMulti(meritocracy_value)
        self.event_shop_multi = ValueToMulti(30 * smiley_statue_owned)
        self.vault_multi = vault_multi

        # Dragon boosts every other statue, so goes first
        dragon = self["Dragon Statue"]
        dragon.calculate_value(self._statue_multis(dragon, []))
        self.dragon_multi = ValueToMulti(dragon.value)
        for statue in self.values():
            if statue is not dragon:
                statue.calculate_value(self._statue_multis(statue, [self.dragon_multi]))

    def get_voodoo_advice(self) -> Advice:
        return Advice(
            label=f"Voidwalker {{{{talent|#library}}}} - Voodoo Statufication: "
            f"{round(self.voodoo_multi, 2):g}x",
            picture_class="voodoo-statufication",
        )

    def get_onyx_advice(self, onyx_lantern_level: int) -> Advice:
        return Advice(
            label=f"Onyx base bonus: {2 * self.onyx_unlocked}/2x"
            f"<br>Total including {{{{The Onyx Lantern |  #sailing}}}}: "
            f"{round(self.onyx_multi, 1):g}/{2 + (0.3 * max_sailing_artifact_level)}x",
            picture_class="onyx-tools",
            progression=onyx_lantern_level,
            goal=max_sailing_artifact_level,
            resource="the-onyx-lantern",
        )

    def get_event_shop_advice(self, smiley_statue: EventShopBonus) -> Advice:
        return Advice(
            label=f"{{{{Event Shop|#event-shop}}}} - Smiley Statue: "
            f"{round(self.event_shop_multi, 2):g}/1.3x",
            picture_class=smiley_statue.image,
            progression=int(smiley_statue.owned),
            goal=1,
        )

    def get_dragon_advice(self) -> Advice:
        dragon = self["Dragon Statue"]
        return Advice(
            label=f"Level {dragon.level} Dragon Statue: "
            f"{round(self.dragon_multi, 3):g}x",
            picture_class=dragon.image,
        )

    def get_total_multi_advice(self) -> Advice:
        return Advice(
            label=f"Total Multi for all statues: {round(self.total_multi, 2):g}x"
            f"<br>Vault statues: {round(self.total_multi * self.vault_multi, 2):g}x",
            picture_class="town-marble",
        )

    def _statue_multis(self, statue: Statue, dragon: list[float]) -> list[float]:
        return [
            self.onyx_multi if statue.type_number >= onyx_type_number else 1,
            self.zenith_multi if statue.type_number >= zenith_type_number else 1,
            self.vault_multi if statue.name in vault_statues else 1,
            self.voodoo_multi,
            *dragon,
            self.event_shop_multi,
            self.merit_multi,
        ]
