from __future__ import annotations

from typing import TYPE_CHECKING

from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index

if TYPE_CHECKING:
    from models.w7.menagerie import Menagerie

# Liquid Shop item (`AlchemyDescription[5]` in source) that gives a Shell
LUMINOUS_SHELL_INDEX = 16


class MenagerieShells:
    """Shells ("Menagerie"[0][1] in source) and every place they come from.

    Ranking up spends them, so the save only holds the current amount.
    """

    def __init__(self, raw_data: dict, menagerie: Menagerie):
        self.menagerie = menagerie
        # "CauldronInfo"[10] in source: Liquid Shop purchases, never reset for this item
        purchases = safer_index(safe_loads(raw_data.get("CauldronInfo", [])), 10, {})
        if isinstance(purchases, dict):
            bought = purchases.get(str(LUMINOUS_SHELL_INDEX), 0)
        else:
            bought = safer_index(purchases, LUMINOUS_SHELL_INDEX, 0)
        self.liquid_shop_bought: int = round(safer_convert(bought, 0))

    def get_rank_advice(self) -> Advice:
        menagerie = self.menagerie
        return Advice(
            label=f"Shells needed for Menagerie Rank {menagerie.rank + 1}",
            picture_class="menagerie-shell",
            progression=menagerie.shells,
            goal=menagerie.shell_req,
        )

    def get_missions_advice(self) -> Advice:
        claimed = sum(mission.completions for mission in self.menagerie.missions)
        return Advice(
            label="Missions: +1 Shell per claim",
            picture_class="menagerie-mission-0",
            progression=claimed,
            goal=EmojiType.INFINITY.value,
        )

    def get_liquid_shop_advice(self) -> Advice:
        return Advice(
            label="Alchemy Liquid Shop: Luminous Shell<br>Its cost never resets",
            picture_class="menagerie-shell",
            progression=self.liquid_shop_bought,
            goal=EmojiType.INFINITY.value,
            resource="trench-seawater",
        )

    def get_advices(self) -> list[Advice]:
        from models.general.session_data import session_data

        account = session_data.account
        return [
            self.get_rank_advice(),
            self.get_missions_advice(),
            self.menagerie.jellyfish["Pink Jellyfish"].get_shell_advice(),
            account.coral_reef["Carnation Coral"].get_advice(),
            self.get_liquid_shop_advice(),
            account.event_points_shop["Menagerie Shell"].get_bonus_advice(),
        ]
