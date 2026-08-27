from models.advice.advice import Advice
from models.caverns.caves.monument_cavern import MonumentCavern


class WisdomMonument(MonumentCavern):
    ANCHOR = "underground-overgrowth"

    def __init__(self):
        super().__init__(name="Wisdom Monument", cavern_number=13, monument_index=2)

    def advice_groups(self) -> dict[str, list[Advice]]:
        return {
            "Cavern Stats": self._cavern_stats_advice(
                "AFK here to gain Monument Hours"
            ),
            "Layer Stats": self._layer_stats_advice("wisdom-icon"),
            "Bonuses Stats": self._bonuses_stats_advice(),
        }
