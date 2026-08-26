from functools import cached_property
from math import ceil, exp, floor, log

from consts.caverns.caves.gambit import (
    gambit_challenge_names,
    gambit_challenge_time_offset,
    gambit_pts_bonuses,
    gambit_pts_for_doublers,
    schematics_unlocking_gambit_challenges,
)
from consts.consts_autoreview import EmojiType, ValueToMulti
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_math_log
from utils.text_formatting import notateNumber


class GambitChallenge:
    def __init__(
        self,
        cavern: "Gambit",
        index: int,
        name: str,
        seconds: float,
        unlock_schematic: str | None,
    ):
        self.cavern = cavern
        self.index = index
        self.name = name
        self.seconds = seconds
        self.image = (
            "engineer-schematic-78"
            if index == 0
            else f"engineer-schematic-{88 + index}"
        )
        self._unlock_schematic = unlock_schematic

    @cached_property
    def unlocked(self) -> bool:
        if self._unlock_schematic is None:
            return True
        from models.general.session_data import session_data

        kaipu = session_data.account.caverns.villagers["Kaipu"]
        return kaipu.schematics[self._unlock_schematic].bought

    @cached_property
    def base_pts(self) -> float:
        # `GambitPts` in source. Last update v2.523.
        base_value = 100 if self.index == 0 else 200
        return base_value * (
            self.seconds + 3 * floor(self.seconds / 10) + 10 * floor(self.seconds / 60)
        )

    @property
    def time_display(self) -> str:
        return f"{self.seconds // 60:.0f}min {self.seconds % 60:.1f}sec"

    def get_advice(self) -> Advice:
        if self.unlocked:
            return Advice(
                label=(
                    f"{self.name}<br>{self.time_display} = "
                    f"{self.base_pts:,.2f} base points"
                ),
                picture_class=self.image,
            )
        assert self._unlock_schematic is not None
        from models.general.session_data import session_data

        schematic = session_data.account.caverns.villagers["Kaipu"].schematics[
            self._unlock_schematic
        ]
        return Advice(
            label=(
                f"Unlock {self.name} by purchasing"
                f"<br>{schematic.full_name()}"
            ),
            picture_class=self.image,
            resource=schematic.resource,
        )


class GambitBonus:
    def __init__(self, cavern: "Gambit", index: int, entry: dict):
        self.cavern = cavern
        self.index = index
        self.scaling_value = entry["ScalingValue"]
        self.scales_with_pts = entry["ScalesWithPts"]
        self.description = entry["Description"]
        self.pts_required = entry["PtsRequired"]
        self.image = f"gambit-bonus-{index}"
        self._raw_name = entry["Name"]

    @cached_property
    def unlocked(self) -> bool:
        return self.cavern.total_pts >= self.pts_required

    @cached_property
    def value(self) -> float:
        if not self.unlocked:
            return 0
        match self.index:
            case 0:
                total_pts = self.cavern.total_pts
                return max(
                    1 if total_pts > 0 else 0,
                    ceil(
                        safer_math_log(total_pts, 2)
                        - 8
                        + (safer_math_log(total_pts, "Lava") - 1)
                    ),
                )
            case 12:
                # Bonus 13 in-game: "2x Extra Bones on Deathbringer" == +100% Bones
                return 100
            case _:
                if self.scales_with_pts:
                    return self.scaling_value * safer_math_log(
                        self.cavern.total_pts, "Lava"
                    )
                return self.scaling_value

    @cached_property
    def name(self) -> str:
        name = self._raw_name
        display_value = self.value if self.unlocked else self.scaling_value
        if "{" in name:
            if self.index == 0 or not self.scales_with_pts:
                return name.replace("{", f"{display_value}")
            return name.replace("{", f"{display_value:.2f}")
        if "}" in name:
            return name.replace("}", f"{ValueToMulti(display_value):.3f}x")
        return name

    @cached_property
    def next_doubler_cost(self) -> int:
        # "GambitBonuses" when 0 == b in source. Last update v2.523.
        # count = log2(TotalPTS) - 8 + (log10(TotalPTS) - 1)
        # TotalPTS(count) = e^((count + 9) / (1 / log(2) + 1 / log(10)))
        try:
            return gambit_pts_for_doublers[int(self.value) + 1]
        except IndexError:
            return ceil(exp((self.value + 9) / (1 / log(2) + 1 / 2.30259)))

    def get_advice(self) -> Advice:
        suffix = f"{': ' if self.description else ''}{self.description}"
        if self.unlocked:
            label = f"{self.name}{suffix}"
        else:
            points_to_go = ceil(self.pts_required - self.cavern.total_pts)
            label = f"{self.name}{suffix}<br>{points_to_go:,.0f} points to Unlock"
        return Advice(
            label=label,
            picture_class=self.image,
            progression=int(self.unlocked) if not self.scales_with_pts else "",
            goal=1 if not self.scales_with_pts else EmojiType.INFINITY.value,
        )

    def get_bonus_advice(self) -> Advice | None:
        """Render this bonus for display outside the Gambit cavern's own advice
        groups. While locked, all bonuses share one format; once unlocked,
        wording differs per bonus. Returns None for a bonus with no external
        representation defined."""
        link = f"{{{{{self.cavern.pre_string()}|#underground-overgrowth}}}}"
        if not self.unlocked:
            points_to_go = ceil(self.pts_required - self.cavern.total_pts)
            return Advice(
                label=(
                    f"{link}: {self.name}<br>{points_to_go:,.0f} Gambit points "
                    "remaining to Unlock this bonus"
                ),
                picture_class=self.image,
                progression=0,
                goal=1,
            )
        match self.index:
            case 0:
                next_cost = self.next_doubler_cost
                notated_next_cost = notateNumber("Basic", next_cost, decimals=3)
                notated_pts = notateNumber(
                    "Match", self.cavern.total_pts, 3, matchString=notated_next_cost
                )
                return Advice(
                    label=(
                        f"{self.name} earned from {link}"
                        f"<br>Next Doubler at {notated_next_cost} Total Gambit PTS "
                        f"({next_cost - self.cavern.total_pts:,.0f} to go!)"
                    ),
                    picture_class=self.image,
                    progression=notated_pts,
                    goal=notated_next_cost,
                )
            case 12:
                return Advice(
                    label=f"{link}: Bonus 13: +100% Bones",
                    picture_class=self.image,
                    progression=1,
                    goal=1,
                )
            case _:
                return None


class Gambit(Cavern):
    def __init__(self):
        super().__init__(name="Gambit", cavern_number=14)

    def parse(self, raw_caverns_list: list):
        self.challenges: dict[str, GambitChallenge] = {}
        for index, name in enumerate(gambit_challenge_names):
            try:
                seconds = raw_caverns_list[11][index + gambit_challenge_time_offset]
            except Exception:
                seconds = 0
            self.challenges[name] = GambitChallenge(
                cavern=self,
                index=index,
                name=name,
                seconds=seconds,
                unlock_schematic=schematics_unlocking_gambit_challenges[index],
            )

        self.bonuses: dict[int, GambitBonus] = {
            index: GambitBonus(self, index, entry)
            for index, entry in enumerate(gambit_pts_bonuses)
        }

    @cached_property
    def base_pts(self) -> float:
        return sum(challenge.base_pts for challenge in self.challenges.values())

    @cached_property
    def pts_multi(self) -> float:
        from models.general.session_data import session_data

        account = session_data.account
        return ValueToMulti(
            account.caverns.villagers["Minau"].measurements[13].value
            + account.caverns.villagers["Bolaia"].studies[13].value
            + (
                10
                * account.caverns.villagers["Kaipu"].schematics["The Sicilian"].bought
            )
            + account.caverns.caves["Wisdom Monument"].bonuses["Gambit Points"].value
            + account.caverns.caves["The Jar"].collectibles["Deep Blue Square"].value
            + account.caverns.caves["The Jar"].collectibles["Murky Fabrege Egg"].value
        )

    @cached_property
    def total_pts(self) -> float:
        return self.base_pts * self.pts_multi

    def advice_groups(self) -> dict[str, list[Advice]]:
        return {
            "Cavern Stats": [
                self.objective_advice(
                    "Survive as long as possible against various Summoning challenges"
                ),
                self.opals_found_advice(),
            ],
            "FAQs": [
                Advice(
                    label=(
                        "Your opponent does not have a health bar, and there is "
                        "no reward for your units reaching the right edge."
                    ),
                    picture_class="engineer-schematic-78",
                ),
            ],
            "Challenge Stats": [
                Advice(
                    label=f"Base Points: {self.base_pts:,.2f}",
                    picture_class="gambit-king-stone",
                ),
                Advice(
                    label=f"Points Multi: {self.pts_multi:,.2f}x",
                    picture_class="measurement-13",
                ),
                Advice(
                    label=f"Total Points: {self.total_pts:,.2f}",
                    picture_class="gambit-king-gold",
                ),
                *[challenge.get_advice() for challenge in self.challenges.values()],
            ],
            "Bonuses": [bonus.get_advice() for bonus in self.bonuses.values()],
        }
