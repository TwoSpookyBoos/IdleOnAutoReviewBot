from dataclasses import dataclass

from consts.caverns.cavern import get_resource_image
from consts.caverns.villager.minau import (
    max_measurements,
    measurement_scales_name,
    measurements_data,
)
from consts.caverns.villager.roles import villager_roles
from consts.consts_autoreview import EmojiType, ValueToMulti
from models.advice.advice import Advice
from models.caverns.villagers.villager import Villager
from utils.misc.next_break_point_tooltip import next_break_point_tooltip
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safer_convert, safer_math_log
from utils.text_formatting import notateNumber


@dataclass
class MeasurementScale:
    value: float
    index: int

    def __post_init__(self):
        # "MeasurementQTYfound" in source. Last update v2.497
        # Formula for multi in the source code, this is when 99 = i
        match self.index:
            case 0:
                # Gloomie kills
                value = notateNumber("Basic", self.value, 2)
                raw_multi = safer_math_log(self.value, "Lava")
            case 1:
                # Crops
                value = f"{self.value:,}"
                raw_multi = self.value / 14
            case 2:
                # Account Lv
                value = f"{self.value:,}"
                raw_multi = self.value / 500
            case 3:
                # Tome Score
                value = f"{self.value:,}"
                raw_multi = self.value / 2500
            case 4:
                # All Skill Lv
                value = f"{self.value:,}"
                raw_multi = self.value / 5000 + max(0.0, (self.value - 18000) / 1500)
            # index 5 Unimplemented default case handle it
            case 6:
                # Deathnote Pts
                value = f"{self.value:,}"
                raw_multi = self.value / 125
            case 7:
                # Highest Dmg
                value = notateNumber("Basic", self.value, 3)
                raw_multi = safer_math_log(self.value, "Lava") / 2
            case 8:
                # Slab Items
                value = f"{self.value:,}"
                raw_multi = self.value / 150
            case 9:
                # Studies Done
                value = f"{self.value:,}"
                raw_multi = self.value / 6
            case 10:
                # Golem Kills
                value = notateNumber("Basic", self.value, 2)
                raw_multi = max(0, safer_math_log(self.value, "Lava") - 2)
            case _:
                value = ""
                raw_multi = 0
        # "MeasurementMulti" in source. Last update v2.497
        if raw_multi < 5:
            self.as_multi = ValueToMulti(18 * raw_multi)
        else:
            self.as_multi = ValueToMulti(18 * raw_multi + 8 * (raw_multi - 5))
        self.scale_by = measurement_scales_name[self.index]
        self.display = f"{value} {self.scale_by}"


class MeasurementBonus:
    # "MeasurementBaseBonus" in source: base * L / (100 + L),
    # so it's the level giving half of the base
    _HALF_LEVEL = 100

    def __init__(self, index: int, data: dict, level: int):
        self.level = level
        self.value = 0
        self._number = index + 1
        self._base_value = data["BaseValue"]
        self._is_linear = data["IsLinear"]
        self._template = data["Template"]
        self._scale_index = data["ScaleIndex"]
        self._resource = get_resource_image(data["ResourceIndex"])
        self._image = f"measurement-{index}"
        self._majik_multi = 1

    def calculate_bonus(self, majik_multi: float, scale: list[MeasurementScale]):
        # "MeasurementBaseBonus" in source. Last update v2.497
        if self._is_linear:
            self.value = self._base_value * self.level
        else:
            self._current_percent = self.level / (self._HALF_LEVEL + self.level)
            self.value = self._base_value * self._current_percent
        self._majik_multi = majik_multi
        self.value *= majik_multi
        self._value_by_level = self.value
        self._scale = scale[self._scale_index]
        self.value *= self._scale.as_multi

    def get_advice(self):
        if self._is_linear:
            value_by_level = f"+{self._value_by_level:.0f}% {self._template}"
            progression = "Linear"
            goal = EmojiType.INFINITY.value
            unit = ""
            tooltip = ""
        else:
            bonus = self._format_bonus(self._value_by_level)
            value_by_level = f"{bonus} {self._template}"
            progression = f"{self._current_percent * 100:.2f}"
            goal = 100
            unit = "%"
            tooltip = next_break_point_tooltip(
                self._value_by_level,
                self._base_value * self._majik_multi,
                self._HALF_LEVEL,
                self._format_bonus,
            )
        return Advice(
            label=(
                f"Level {self.level}<br>"
                f"Base: {value_by_level}<br>"
                f"x{self._scale.as_multi:.3f} ({self._scale.display})<br>"
                f"Total: +{self.value:,.2f}%"
            ),
            picture_class=self._image,
            progression=progression,
            goal=goal,
            resource=self._resource,
            unit=unit,
            progression_tooltip=tooltip,
        )

    @staticmethod
    def _format_bonus(value: float) -> str:
        # Base bonus, without the scale, as in "Base:" of the label
        return f"+{round_and_trim(value)}%"

    def get_bonus_advice(self) -> Advice:
        return Advice(
            label=(
                f"{{{{ Caverns|#villagers }}}} - Measurement #{self._number}:<br>"
                f"+{self.value:.2f}% {self._template} "
                f"(scales with {self._scale.scale_by})"
            ),
            picture_class=self._image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
        )


@dataclass
class Measurements(list[MeasurementBonus]):
    unlocked: int = 0


class Minau(Villager):
    def __init__(self, **kwargs):
        super().__init__(
            name="Minau", unlock_at=7, role=villager_roles["Minau"], **kwargs
        )
        self.measurements = Measurements()
        self.gloomie_kills: float = 0

    def parse_feature(self, raw_caverns_list: list):
        self.gloomie_kills = self._get_gloomie_kills(raw_caverns_list)
        raw_measurements_level = raw_caverns_list[22]
        for index, data in enumerate(measurements_data):
            level = safer_convert(raw_measurements_level[index], 0)
            bonus = MeasurementBonus(index, data, level)
            self.measurements.append(bonus)

    def calculate_bonuses(
        self,
        *,
        lengthmeister_multi: float,
        crops_found: int,
        all_skills: dict[str, list[int]],
        tome_score: int,
        death_note,
        highest_dmg: float,
        slab_items: int,
        studies_done: int,
        golem_kills: float,
    ):
        scale_values = [
            self.gloomie_kills,
            crops_found,
            # Account Lv
            sum(all_skills["Combat"]) or 0,
            tome_score,
            # All Skill Lv
            sum(
                [
                    sum(skill_levels)
                    for skill, skill_levels in all_skills.items()
                    if skill != "Combat"
                ]
            ),
            # Unimplemented
            0,
            # Deathnote Pts
            sum([death_note.worlds[world].total_mk for world in death_note.worlds])
            + death_note.minibosses.total_mk,
            highest_dmg,
            slab_items,
            studies_done,
            golem_kills,
        ]
        self._scale = [
            MeasurementScale(value, index) for index, value in enumerate(scale_values)
        ]
        for bonus in self.measurements:
            bonus.calculate_bonus(lengthmeister_multi, self._scale)

    @staticmethod
    def _get_gloomie_kills(raw_holes):
        try:
            return safer_convert(raw_holes[11][28], 0.00) if raw_holes else 0
        except Exception:
            return 0

    def stat_advices(self) -> list[Advice]:
        max_level = max_measurements
        return self.base_stat_advice(max_level)

    def feature_advice(self) -> dict[str, list[Advice]] | None:
        return {
            "Measurement Stats": [
                measurement.get_advice() for measurement in self.measurements
            ]
        }
