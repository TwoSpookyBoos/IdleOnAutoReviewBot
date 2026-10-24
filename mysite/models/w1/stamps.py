from dataclasses import dataclass

from consts.consts_autoreview import EmojiType, ValueToMulti
from consts.consts_item_data import ITEM_DATA
from consts.idleon.lava_func import lava_func
from consts.w1.stamps import stamp_maxes, stamp_types
from models.general.item_definitions import ItemDefinition
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index
from utils.text_formatting import letterToNumber, numberToLetter

logger = get_logger(__name__)


@dataclass
class Stamp:
    name: str
    code_name: str
    effect: str
    delivered: bool
    level: int
    max_level: int
    material: ItemDefinition | None
    value: float
    stamp_type: str
    exalted: bool
    total_value: float = 0

    def get_advice(self, link_to_section: bool = True, additional_text: str = "", goal_override = ""):
        link_to_section_text = f"{{{{ Stamps|#stamps }}}} - " if link_to_section else ""
        effect_text = f" {self.effect}" if not self.effect.startswith('%') else self.effect
        unlock_text = "Unlock " if not self.delivered else ""
        body_text = f": +{round_and_trim(self.total_value)}{effect_text}{additional_text}" if self.delivered else ""
        return Advice(
            label=f"{link_to_section_text}{unlock_text}{self.name}{body_text}",
            resource=self.material.name,
            progression=self.level,
            goal=(goal_override if goal_override else stamp_maxes.get(self.name, EmojiType.INFINITY.value)) if self.delivered else 1,
            picture_class=self.name,
        )

def _raw_stamp_levels(raw_levels: list) -> dict[str, int]:
    # e.g. [{"0": 5, "1": 3, "length": 2}, ...] per stamp type
    return {
        f"Stamp{numberToLetter(type_index + 1).upper()}{int(key) + 1}": safer_convert(level, 0)
        for type_index, type_levels in enumerate(raw_levels)
        for key, level in type_levels.items()
        if key != "length"
    }


class Stamps(dict[str, Stamp]):
    def __init__(self, raw_data: dict, version: float):
        super().__init__()
        self.exalted_multi: float = 1
        levels = _raw_stamp_levels(safe_loads(raw_data.get("StampLv", [{}, {}, {}])))
        max_levels = _raw_stamp_levels(safe_loads(raw_data.get("StampLvM", [{}, {}, {}])))
        # Exalted stamps live in the Compass data
        raw_compass = safe_loads(raw_data.get("Compass", []))
        if not raw_compass:
            logger.warning(f"Exalted Stamp data not present{', as expected' if version < 264 else ''}.")
        raw_exalted = safer_index(raw_compass, 4, [])

        for definition in ITEM_DATA.get_all_stamps():
            stamp_codename = definition.code_name.split('Stamp')[1]
            stamp_type = stamp_types[letterToNumber(stamp_codename[0].lower()) - 1]
            exalted_key = (
                f"{numberToLetter(letterToNumber(stamp_codename[0].lower()) - 1)}"
                f"{int(stamp_codename[1:]) - 1}"
            )
            exalted = exalted_key in raw_exalted
            try:
                level = levels.get(definition.code_name, 0)
                max_level = max_levels.get(definition.code_name, 0)
                self[definition.name] = Stamp(
                    name=definition.name,
                    code_name=definition.code_name,
                    material=ITEM_DATA.get_item_from_codename(definition.stamp_bonus.code_material),
                    effect=definition.stamp_bonus.effect,
                    level=level,
                    max_level=max_level,
                    delivered=max_level > 0,
                    stamp_type=stamp_type,
                    value=lava_func(
                        definition.stamp_bonus.scaling_type,
                        level,
                        definition.stamp_bonus.x1,
                        definition.stamp_bonus.x2,
                    ),
                    exalted=exalted,
                )
            except Exception as e:
                logger.warning(f"Stamp Parse error at {stamp_type}: {e}. Defaulting to Undelivered")
                self[definition.name] = Stamp(
                    name=definition.name,
                    code_name=definition.code_name,
                    level=0,
                    max_level=0,
                    delivered=False,
                    stamp_type=stamp_type,
                    value=0,
                    exalted=exalted,
                    material=None,
                    effect="",
                )

    @property
    def total_levels(self) -> int:
        return sum(stamp.level for stamp in self.values())

    def calculate_total_values(
        self,
        exalted_sources: list[float],
        certified_stamp_book: bool,
        liqorice_rolle_value: float,
    ):
        # `"StampDoubler" == d` in source: base 100 plus every source. Last updated in v2.531.0
        self.exalted_multi = ValueToMulti(sum(exalted_sources, 100))
        for stamp in self.values():
            # Misc stamps skip the Lab and Pristine Charm doublers
            non_misc = stamp.stamp_type != 'Misc'
            stamp.total_value = (
                stamp.value
                * (2 if certified_stamp_book and non_misc else 1)
                * (ValueToMulti(liqorice_rolle_value) if non_misc else 1)
                * (self.exalted_multi if stamp.exalted else 1)
            )
