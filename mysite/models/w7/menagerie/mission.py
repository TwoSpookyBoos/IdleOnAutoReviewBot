from __future__ import annotations

from functools import cached_property
from math import ceil, floor
from typing import TYPE_CHECKING

from models.advice.advice import Advice
from utils.safer_data_handling import safer_math_log
from utils.text_formatting import notateNumber

if TYPE_CHECKING:
    from models.w7.menagerie import Menagerie


class MenagerieMission:
    def __init__(self, index: int, info: dict, completions: int, menagerie: Menagerie):
        self.index = index
        self.description = info["Description"]
        self.progress_label = info["Progress Label"]
        self.completions = completions
        self.menagerie = menagerie
        # "Cost" 0 in source
        self.goal = floor(info["Goal Base"] + info["Goal Increment"] * completions)

    @property
    def visible(self) -> bool:
        # "UpgUnlocked" 0 in source
        return self.index < self.menagerie.visible_missions

    @cached_property
    def progress(self) -> float | None:
        # "MissionProg" in source. Last updated in v2.550.0
        from models.general.session_data import session_data

        account = session_data.account
        challenges = account.tome.challenges
        match self.index:
            case 0:
                return sum(character.combat_level for character in account.characters)
            case 1:
                return account.sneaking.unlocked_mastery
            case 2:
                return account.spelunk.total_depths
            case 3:
                return account.farming.crops.unlocked
            case 4:
                return account.summoning.endless.total_win
            case 5:
                return account.worship.total_waves
            case 6:
                return account.divinity.god_rank
            case 7:
                return account.meals["Turkey of Thank"].level
            case 8:
                return account.clam_work.level
            case 9:
                return account.minehead.opponents_defeated
            case 10:
                return account.sushi_station.unique_sushi
            case 11:
                return account.jelly_operator.obstructions_defeated
            case 13:
                return account.glimbo.total_trades
            case 14:
                return account.the_button.total_clicks
            case 15:
                return challenges[112].quantity
            case 16:
                return account.tome.score
            case 17:
                return account.research.grid.totals.crowns_reclaimed
            case 18:
                return account.sailing.artifacts.total_tiers
            case 19:
                return len(account.slab)
            case 20:
                sample = account.printer.first_slot_values.get("Copper", 0)
                return ceil(safer_math_log(sample, "Lava")) if sample else 0
            case 21:
                return account.greenstacks.count
            case 22:
                return account.emperor.last_showdown
            case 23:
                return challenges[92].quantity
            case 24:
                return floor(safer_math_log(account.gaming.bits_owned, "Lava"))
            case 25:
                return account.owl.mega_feathers_owned - 9
            case 26:
                return round(challenges[86].quantity - 11)
            case 27:
                return round(challenges[108].quantity - 11)
            case 28:
                return account.gallery.total_palette_level
            case 29:
                return challenges[96].quantity
            case 31:
                return challenges[24].quantity
            case 32:
                return account.killroy.prime_kills
            case _:
                # TODO: not tracked yet
                #  12 "TotalOpalsEarned": a dozen opal bonuses on top of Holes[7]
                #  30 "OverkillQTY" 7: Deathnote bosses page
                return None

    def _format(self, value: float) -> str:
        # "$" missions show NotateNumber(10^value), "{" ones show CommaNotation(value)
        if "$" in self.description:
            return notateNumber("Basic", 10**value, 2)
        return f"{round(value):,}"

    @property
    def claimable(self) -> bool:
        # "CanClaim" 0 in source, limited to missions the player can see
        return self.visible and self.progress is not None and self.progress >= self.goal

    def _title(self) -> str:
        goal = self._format(self.goal)
        description = self.description.replace("{", goal).replace("$", goal)
        return f"Mission {self.index + 1}: {description}"

    def get_advice(self) -> Advice:
        label = self._title()
        progress = self.progress
        if progress is None:
            label += f"<br>{self.progress_label}: not tracked yet"
        if not self.visible:
            label += "<br>Needs more Mission slots"
        elif self.claimable:
            label += "<br>Ready to claim!"
        return Advice(
            label=label,
            picture_class=f"menagerie-mission-{self.index}",
            progression="" if progress is None else round(progress),
            goal=self.goal,
        )

    def get_claim_alert(self) -> Advice | None:
        if not self.claimable:
            return None
        return Advice(
            label=f"Claim {{{{ Menagerie|#luminous-menagerie }}}} {self._title()}",
            picture_class=f"menagerie-mission-{self.index}",
        )
