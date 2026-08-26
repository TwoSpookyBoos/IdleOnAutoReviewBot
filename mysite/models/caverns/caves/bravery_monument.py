from functools import cached_property
from math import floor

from consts.consts_autoreview import ValueToMulti
from models.advice.advice import Advice
from models.caverns.caves.monument_cavern import MonumentCavern


class BraveryMonument(MonumentCavern):
    ANCHOR = "shallow-caverns"
    MAX_SWORDS = 8  # 3 + 2 + 1 + 1 + 1, under the game's own separate cap of 9
    MAX_RETHROWS = 5 + 10
    MAX_RETELLINGS = 1

    def __init__(self):
        super().__init__(name="Bravery Monument", cavern_number=4, monument_index=0)

    def parse(self, raw_caverns_list: list):
        super().parse(raw_caverns_list)
        self.sword_count = min(
            9,
            3
            + (2 * (self.hours >= 80))
            + (1 * (self.hours >= 750))
            + (1 * (self.hours >= 5000))
            + (1 * (self.hours >= 24000)),
        )
        self.rethrows = 0 + (5 * (self.hours >= 300)) + (10 * (self.hours >= 10000))
        self.retellings = 1 * (self.hours >= 2000)

    @cached_property
    def sword_min(self) -> float:
        from models.general.session_data import session_data

        story_schematic_bought = (
            session_data.account.caverns.villagers["Kaipu"]
            .schematics["The Story Changes Over Time..."]
            .bought
        )
        return 3 + (floor(self.hours / 6) * story_schematic_bought)

    @cached_property
    def sword_max(self) -> float:
        from models.general.session_data import session_data

        story_schematic_bought = (
            session_data.account.caverns.villagers["Kaipu"]
            .schematics["The Story Changes Over Time..."]
            .bought
        )
        minau_measurement = (
            session_data.account.caverns.villagers["Minau"].measurements[1].value
        )
        return (
            25 + (10 * floor(self.hours / 6) * story_schematic_bought)
        ) * ValueToMulti(minau_measurement)

    def advice_groups(self) -> dict[str, list[Advice]]:
        sword_range_label = (
            f"Per Sword: {round(self.sword_min):,} to {round(self.sword_max):,}"
            f"<br>All Swords: {round(self.sword_count * self.sword_min):,} to "
            f"{round(self.sword_count * self.sword_max):,}"
            f"<br>'Average' fight: "
            f"{round(self.sword_count * ((self.sword_max - self.sword_min) / 2)):,}"
        )
        return {
            "Cavern Stats": self._cavern_stats_advice(
                "AFK here to gain Monument Hours that empower your Attacks "
                "within the Story minigame"
            ),
            "Layer Stats": self._layer_stats_advice("bravery-bonus-9"),
            "Sword Stats": [
                Advice(
                    label=f"Total Swords: {self.sword_count}/{self.MAX_SWORDS}",
                    picture_class="monument-basic-sword",
                    progression=self.sword_count,
                    goal=self.MAX_SWORDS,
                ),
                Advice(
                    label=sword_range_label,
                    picture_class="monument-basic-sword",
                ),
                Advice(
                    label=(
                        f"{self.rethrows}/{self.MAX_RETHROWS} Sword Rethrows per Fight"
                    ),
                    picture_class="engineer-schematic-40",
                    progression=self.rethrows,
                    goal=self.MAX_RETHROWS,
                ),
                Advice(
                    label=(
                        f"{self.retellings}/{self.MAX_RETELLINGS} Retellings "
                        f"per Story attempt"
                    ),
                    picture_class="engineer-schematic-40",
                    progression=self.retellings,
                    goal=self.MAX_RETELLINGS,
                ),
            ],
            "Bonuses Stats": self._bonuses_stats_advice(),
        }
