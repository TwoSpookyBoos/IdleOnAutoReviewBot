from functools import cached_property
from math import ceil

from consts.caverns.caves.monuments import (
    monument_bonuses,
    monument_layer_rewards,
)
from consts.consts_autoreview import EmojiType, ValueToMulti
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_math_pow


class MonumentBonus:
    def __init__(
        self, cavern: "MonumentCavern", index: int, bonus_details: dict, level: int
    ):
        self.cavern = cavern
        self.index = index
        self.description = bonus_details["Description"]
        self.name = bonus_details["Description"].split(" ", 1)[1]
        self.scaling_value = bonus_details["ScalingValue"]
        self.value_type = bonus_details["ValueType"]
        self.image = bonus_details["Image"]
        self.level = level

    @cached_property
    def _result(self) -> tuple[float, float]:
        """Raw (value, base_value)."""
        cosmos_value = 0
        monument_bonus_multi = 0

        # "MonumentROGbonuses" in source. Last update v2.523
        if self.index != 9:
            from models.general.session_data import session_data

            cosmos_value = (
                session_data.account.caverns.villagers["Cosmos"]
                .majiks.hole["Monumental Vibes"]
                .value
            )
            monument_bonus_multi = self.cavern._bonus_at(9).value

        if self.scaling_value < 30:
            base_value = self.level * self.scaling_value
            value = base_value * ValueToMulti(cosmos_value + monument_bonus_multi)
        else:
            base_value = 0.1 * ceil(
                (self.level / (250 + self.level)) * 10 * self.scaling_value
            )
            value = 0.1 * ceil(
                (self.level / (250 + self.level))
                * 10
                * self.scaling_value
                * ValueToMulti(cosmos_value + monument_bonus_multi)
            )
        return value, base_value

    @property
    def value(self) -> float:
        return self._result[0]

    @property
    def base_value(self) -> float:
        return self._result[1]

    def get_advice(self) -> Advice:
        is_percent = self.value_type == "Percent"
        displayed_value = self.value if is_percent else ValueToMulti(self.value)
        placeholder = "{" if is_percent else "}"
        formatted_value = (
            f"{displayed_value:,.2f}" if is_percent else f"{displayed_value:,.3f}"
        )
        rendered_description = self.description.replace(placeholder, formatted_value)

        if self.scaling_value > 30:
            label = (
                f"Level {self.level}: {rendered_description}"
                f"<br>{self.base_value:.2f}/{self.scaling_value} max from Levels"
            )
            progression = f"{(self.base_value / self.scaling_value) * 100:.2f}"
            goal = 100
            unit = "%"
        else:
            per_level = (
                f"{self.scaling_value}%"
                if is_percent
                else f"{self.scaling_value / 100:.2f}x"
            )
            label = (
                f"Level {self.level}: {rendered_description}"
                f"<br>+{per_level} per level before multis"
            )
            progression = "Linear"
            goal = EmojiType.INFINITY.value
            unit = ""
        return Advice(
            label=label,
            picture_class=self.image,
            progression=progression,
            goal=goal,
            unit=unit,
        )

    def get_bonus_advice(self) -> Advice:
        """For display outside this monument's own advice_groups(), e.g. as a
        contributor to some other cross-cutting total."""
        is_percent = self.value_type == "Percent"
        displayed_value = self.value if is_percent else ValueToMulti(self.value)
        unit = "%" if is_percent else "x"
        return Advice(
            label=(
                f"{{{{ Cavern {self.cavern.cavern_number}|#{self.cavern.ANCHOR} }}}}"
                f"- {self.cavern.name}:"
                f"<br>+{displayed_value:.1f}{unit} {self.name}"
            ),
            picture_class=self.cavern.image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
        )


class MonumentCavern(Cavern):
    ANCHOR: str

    def __init__(self, name: str, cavern_number: int, monument_index: int):
        super().__init__(name=name, cavern_number=cavern_number)
        self.monument_index = monument_index

    def parse(self, raw_caverns_list: list):
        try:
            self.hours = int(raw_caverns_list[14][0 + 2 * self.monument_index])
        except Exception:
            self.hours = 0
        try:
            self.layers_cleared = int(raw_caverns_list[14][1 + 2 * self.monument_index])
        except Exception:
            self.layers_cleared = 0

        self.bonuses: dict[str, MonumentBonus] = {}
        for global_index, bonus_details in monument_bonuses[self.name].items():
            try:
                level = raw_caverns_list[15][global_index]
            except Exception:
                level = 0
            bonus = MonumentBonus(
                cavern=self,
                index=global_index % 10,
                bonus_details=bonus_details,
                level=level,
            )
            self.bonuses[bonus.name] = bonus

    def _bonus_at(self, index: int) -> MonumentBonus:
        return next(bonus for bonus in self.bonuses.values() if bonus.index == index)

    def _opal_chance(self) -> float:
        return min(0.5, safer_math_pow(0.5, self.opals_found)) * ValueToMulti(
            self._bonus_at(5).value
        )

    def _cavern_stats_advice(self, objective: str) -> list[Advice]:
        return [
            self.objective_advice(objective, resource="bravery-bonus-8"),
            self.opals_found_advice(),
            Advice(
                label=f"Chance for next Opal: {self._opal_chance():.2%}",
                picture_class="monument-basic-chest",
            ),
        ]

    def _layer_reward_advice(self, hour_requirement: int, layer_reward: dict) -> Advice:
        return Advice(
            label=f"{hour_requirement:,} hour bonus: {layer_reward['Description']}",
            picture_class=layer_reward["Image"],
            progression=self.hours,
            goal=hour_requirement,
        )

    def _layer_stats_advice(self, header_picture_class: str) -> list[Advice]:
        layer_rewards = monument_layer_rewards[self.name]
        return [
            Advice(
                label=f"Monument Hours: {self.hours:,.0f}",
                picture_class=header_picture_class,
            ),
            *[
                self._layer_reward_advice(hour_requirement, layer_reward)
                for hour_requirement, layer_reward in layer_rewards.items()
            ],
        ]

    def _bonuses_stats_advice(self) -> list[Advice]:
        from models.general.session_data import session_data

        monumental_vibes = session_data.account.caverns.villagers[
            "Cosmos"
        ].majiks.hole["Monumental Vibes"]
        return [
            monumental_vibes.get_advice(),
            *[bonus.get_advice() for bonus in self.bonuses.values()],
        ]
