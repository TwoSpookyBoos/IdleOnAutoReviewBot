from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from consts.w7.legend_talents import legend_talents_bonuses
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_index


class LegendTalent:
    def __init__(self, talents: "LegendTalents", name: str, info: dict, level: int):
        self.talents = talents
        self.name = name
        self.level = level
        self.max_level = info["Max Level"]
        self.image = info["Image"]
        self.display_order = info["Display Order"]
        self._base_value = info["Base Value"]
        self._bonus_template = info["Bonus"]
        self._description_template = info["Description"]

    @cached_property
    def value(self) -> float:
        return self._base_value * self.level

    @cached_property
    def _next_value(self) -> float:
        return self._base_value * (self.level + 1)

    @cached_property
    def description(self) -> str:
        return self._fill_template(self._description_template, self.value)

    @cached_property
    def bonus(self) -> str:
        return self._fill_template(self._bonus_template, self._next_value)

    def _fill_template(self, template: str, value: float) -> str:
        text = template
        if "{" in text:
            text = text.replace("{", f"{value}")
        if "}" in text:
            text = text.replace("}", f"{ValueToMulti(value)}")
        if "$" in text:
            if self.name == "Double Aint Enough":
                text = text.replace("$", f"{2 + value / 100}")
            elif self.name == "Super Talent Points":
                # Depends on: LegendTalents['Super Duper Talents'].value
                text = text.replace(
                    "$", f"{50 + self.talents['Super Duper Talents'].value}"
                )
            elif self.name == "Inevitable Builder":
                text = text.replace(" for a total bonus speed of $x", "")
            elif self.name == "6 O'Clock Crystals":
                text = text.replace("$ ", "")
            else:
                text = text.replace("$", f"{value}")
        return text

    def get_advice(self, link_to_section: bool = True) -> Advice:
        link = "{{ Legend Talent|#legend-talents }} - " if link_to_section else ""
        next_level_text = (
            f"<br>Next Lv: {self.bonus}" if self.level < self.max_level else ""
        )
        return Advice(
            label=f"{link}{self.name}: {self.description}{next_level_text}",
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
        )


class LegendTalents(dict[str, LegendTalent]):
    def __init__(self, raw_data: dict):
        levels: list[int] = safer_index(safe_loads(raw_data.get("Spelunk", [])), 18, [])
        for index, (name, info) in enumerate(legend_talents_bonuses.items()):
            self[name] = LegendTalent(self, name, info, safer_index(levels, index, 0))
