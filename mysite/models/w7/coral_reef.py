from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from consts.w7.coral_reef import coral_reef_bonus_data
from models.advice.advice import Advice
from models.general.session_data import session_data
from utils.safer_data_handling import (
    safe_loads,
    safer_convert,
    safer_index,
    safer_math_pow,
)


class CoralReefBonus:
    def __init__(self, index: int, info: dict, unlocked: bool, level: int):
        self.index = index
        self.name = info["Name"]
        self.description = info["Description"]
        self._base_max_level = info["Max Level"]
        self.image = f"coral-{index}"
        self.unlocked = unlocked
        self.level = level
        self.next_cost = int(
            info["Coefficient"] * safer_math_pow(info["Exponent Base"], self.level, 0)
        )

    @cached_property
    def max_level(self) -> int:
        match self.index:
            case 3:
                # Menagerie Unlock 10 rewrites `CoralReef[3][1]` 12 -> 15 in source
                owned = session_data.account.menagerie.unlocks[9].owned
                return self._base_max_level + 3 * int(owned)
            case _:
                return self._base_max_level

    def get_advice(self) -> Advice:
        unlock_or_upgrade_text = "Level up" if self.unlocked else "Unlock"
        next_level_cost_text = (
            f"<br>Next level costs {self.next_cost} corals"
            if self.unlocked and self.level < self.max_level
            else ""
        )
        return Advice(
            label=(
                f"{unlock_or_upgrade_text} {self.name}: {self.description}"
                f"{next_level_cost_text}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource="coral",
        )


class CoralReef(dict[str, CoralReefBonus]):
    def __init__(self, raw_data: dict):
        raw_spelunk = safe_loads(raw_data.get("Spelunk", []))
        self.town_corals = safer_convert(
            safer_index(safer_index(raw_spelunk, 4, []), 5, 0), 0
        )

        unlocked_reef_corals = safer_index(raw_spelunk, 12, [])
        coral_levels = safer_index(raw_spelunk, 13, [])

        for index, info in enumerate(coral_reef_bonus_data):
            unlocked = bool(safer_index(unlocked_reef_corals, index, False))
            level = safer_index(coral_levels, index, 0)
            bonus = CoralReefBonus(index, info, unlocked, level)
            self[bonus.name] = bonus

        self.total_level = sum(bonus.level for bonus in self.values())

    @cached_property
    def _daily_corals_multis(self) -> dict[str, float]:
        # `"ReefDayGains" == e` in source. Last updated in v2.46 Dec 7
        # Depends on: companions['Shellslug'], event_points_shop['Coolral'],
        # gemshop.purchases['More Coral'], coral_kid[5], dancing_coral[0], clam_work,
        # killroy.skull_shop['Daily Coral'], stamps['Corale Stamp'],
        # alchemy_vials['Scale On Ice (Scaled Fragment)'],
        # legend_talents['Coral Restoration'], arcade[57],
        # sneaking.emporium['Coral Conservationism'], cards['Demonblub'],
        # statues['Coral Statue']
        account = session_data.account
        multi_group_d_value = sum(
            (
                account.coral_kid[5].value,
                account.dancing_coral[0].value,
                account.clam_work.daily_corals_bonus,
                account.killroy.skull_shop["Daily Coral"].value,
                account.stamps["Corale Stamp"].total_value,
                account.alchemy_vials["Scale On Ice (Scaled Fragment)"].value,
                account.legend_talents["Coral Restoration"].value,
                account.arcade[57].value,
                account.sneaking.emporium["Coral Conservationism"].value,
                account.cards.named("Demonblub").getCurrentValue(),
                account.statues["Coral Statue"].value,
            )
        )
        return {
            "A": account.companions["Shellslug"].get_multi("Daily Corals"),
            "B": 1 + 0.3 * account.event_points_shop["Coolral"].owned,
            "C": 1 + 0.2 * account.gemshop.purchases["More Coral"].owned,
            "D": ValueToMulti(multi_group_d_value),
        }

    def get_daily_corals_advices(self) -> dict[str, list[Advice]]:
        account = session_data.account
        multis = self._daily_corals_multis
        base_daily_corals = 10
        total_daily_corals = (
            base_daily_corals * multis["A"] * multis["B"] * multis["C"] * multis["D"]
        )
        more_coral_advice = account.gemshop.purchases["More Coral"].get_advice(
            additional_text=f": x{multis['C']}/x3.0 Daily Corals"
        )
        coral_conservationism = account.sneaking.emporium["Coral Conservationism"]
        return {
            f"Total daily corals: {round(total_daily_corals, 2):g}": [],
            f"Base: {base_daily_corals}": [
                Advice(
                    label=f"Base daily corals: {base_daily_corals}",
                    picture_class="coral",
                    completed=True,
                )
            ],
            f"Multi Group A: x{round(multis['A'], 2):g}": [
                account.companions["Shellslug"].get_advice()
            ],
            f"Multi Group B: x{round(multis['B'], 2):g}": [
                account.event_points_shop["Coolral"].get_bonus_advice()
            ],
            f"Multi Group C: x{round(multis['C'], 2):g}": [more_coral_advice],
            f"Multi Group D: x{round(multis['D'], 2):g}": [
                account.coral_kid[5].get_advice(),
                account.dancing_coral[0].get_advice(),
                account.clam_work.get_daily_corals_advice(),
                account.killroy.skull_shop["Daily Coral"].get_bonus_advice(),
                account.stamps["Corale Stamp"].get_advice(),
                account.alchemy_vials["Scale On Ice (Scaled Fragment)"].get_advice(
                    additional_text=" Daily Corals",
                    full_name=False,
                    resource="scaled-fragment",
                ),
                account.legend_talents["Coral Restoration"].get_advice(),
                account.arcade[57].get_advice(),
                coral_conservationism.get_obtained_advice(),
                account.cards.named("Demonblub").getAdvice(),
                account.statues["Coral Statue"].get_advice(),
            ],
        }
