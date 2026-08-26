from functools import cached_property
from math import log2

from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from models.caverns.caves.monument_cavern import MonumentCavern


class JusticeMonument(MonumentCavern):
    ANCHOR = "glowshroom-tunnels"
    MAX_MENTAL_HEALTH = 1 + 1 + 1 + 2
    MAX_POPULARITY = 0 + 10
    MAX_DISMISSALS = 0 + 1 + 1 + 2

    def __init__(self):
        super().__init__(name="Justice Monument", cavern_number=10, monument_index=1)

    def parse(self, raw_caverns_list: list):
        super().parse(raw_caverns_list)
        self.mental_health = (
            1
            + (1 * (self.hours >= 80))
            + (1 * (self.hours >= 2000))
            + (2 * (self.hours >= 24000))
        )
        self.popularity = 3 + (7 * (self.hours >= 5000))
        self.dismissals = (
            0
            + (1 * (self.hours >= 300))
            + (1 * (self.hours >= 2000))
            + (2 * (self.hours >= 24000))
        )

    @cached_property
    def coins(self) -> int:
        # "J_StartCoins" in source. Last update v2.523
        from models.general.session_data import session_data

        compound_interest_bought = (
            session_data.account.caverns.villagers["Kaipu"]
            .schematics["Compound Interest"]
            .bought
        )
        schematic_bonus = 0
        if self.hours > 0:
            schematic_bonus = log2(self.hours) * compound_interest_bought
        return round(
            (5 + schematic_bonus)
            * (1 + (0.5 * (self.hours >= 750)) + (1.5 * (self.hours >= 10000)))
        )

    def advice_groups(self) -> dict[str, list[Advice]]:
        currencies = {
            "Mental Health": (self.mental_health, self.MAX_MENTAL_HEALTH),
            "Coins": (self.coins, EmojiType.INFINITY.value),
            "Popularity": (self.popularity, self.MAX_POPULARITY),
            "Dismissals": (self.dismissals, self.MAX_DISMISSALS),
        }
        return {
            "Cavern Stats": self._cavern_stats_advice(
                "AFK here to gain Monument Hours that empower your Rulings "
                "within the Story minigame"
            ),
            "Layer Stats": self._layer_stats_advice("justice-bonus-19"),
            "Currency Stats": [
                Advice(
                    label=f"{value}/{max_value} starting {name}",
                    picture_class=f"justice-currency-{idx + 2}",
                    progression=value,
                    goal=max_value,
                )
                for idx, (name, (value, max_value)) in enumerate(currencies.items())
            ],
            "Bonuses Stats": self._bonuses_stats_advice(),
        }
