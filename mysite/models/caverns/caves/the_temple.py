from consts.consts_autoreview import ValueToMulti
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_convert, safer_math_log, safer_math_pow
from utils.text_formatting import notateNumber


class TheTemple(Cavern):
    def __init__(self):
        super().__init__(name="The Temple", cavern_number=15)

    def parse(self, raw_caverns_list: list):
        try:
            self.torches_owned = safer_convert(raw_caverns_list[11][56], 0.0)
        except Exception:
            self.torches_owned = 0.0
        try:
            self.illuminate = safer_convert(raw_caverns_list[11][57], 0)
        except Exception:
            self.illuminate = 0
        try:
            self.amplify = safer_convert(raw_caverns_list[11][59], 0)
        except Exception:
            self.amplify = 0
        try:
            self.current_kills = safer_convert(raw_caverns_list[11][63], 0.0)
        except Exception:
            self.current_kills = 0.0
        self.illuminate_multi = ValueToMulti(10 * self.illuminate)

    def _search_chance(
        self, torches_owned: float, torch_overwrite: bool = False
    ) -> float:
        # `TempleTorchBonuses` in source. Last update v2.523
        if torch_overwrite:
            spent_torches = max(5, torches_owned)
        else:
            spent_torches = max(5, torches_owned / 4)
        return (
            0.05
            * self.illuminate_multi
            * safer_math_pow(0.7, self.opals_found)
            * safer_math_log(spent_torches, 2)
        )

    def advice_groups(self) -> dict[str, list[Advice]]:
        from models.general.session_data import session_data

        cavern_stats = [
            self.objective_advice(
                "Fight Ancient Golems, collect Temple Torches, and Search for "
                "Centurions to collect Opals",
                resource="ancient-golem",
            ),
            Advice(
                label=(
                    "Bonus Objective- Collect Dragon Warrior "
                    "{{Statues|#statues}} from AFK kills."
                ),
                picture_class="dragon-warrior-statue",
            ),
        ]
        for stamp_name in ["Cavern Resource Stamp", "Study Hall Stamp"]:
            stamp = session_data.account.stamps[stamp_name]
            if not stamp.delivered:
                cavern_stats.append(
                    Advice(
                        label=(
                            f"Bonus Objective - Collect {stamp_name} from AFK "
                            f"kills, then level with {stamp.material.name}"
                        ),
                        picture_class=stamp_name,
                    )
                )
        cavern_stats.append(self.opals_found_advice())

        torches_owned_decimals = 3 if self.torches_owned >= 1000 else 0
        torches_owned_display = notateNumber(
            "Basic", self.torches_owned, torches_owned_decimals
        )

        return {
            "Cavern Stats": cavern_stats,
            "FAQs": [
                Advice(
                    label=(
                        "Statues from Active kills don't have their quantity "
                        "multiplied by Multikill. Farm them AFK instead."
                        "<br>Statues cannot be sampled."
                    ),
                    picture_class="dragon-warrior-statue",
                ),
                Advice(
                    label=(
                        "Respawn% from Amplify only works while Active! Your "
                        "AFK kills will not be increased."
                    ),
                    picture_class="temple-torch",
                ),
                Advice(
                    label=(
                        "Searching costs 25% of your Torches (minimum of 5). "
                        "Chance doesn't scale well, so search early and often!"
                    ),
                    picture_class="temple-torch",
                ),
            ],
            "Torch Stats": [
                Advice(
                    label=f"Torches owned: {torches_owned_display}",
                    picture_class="temple-torch",
                ),
                Advice(
                    label=(
                        f"{self.illuminate} Illuminations: "
                        f"{self.illuminate_multi}x Search chance"
                    ),
                    picture_class="temple-torch",
                ),
                Advice(
                    label=(
                        f"Sanctum {self.opals_found + 1} search odds"
                        f"<br>5 torches: {self._search_chance(5):.6%}"
                        f"<br>500 torches: {self._search_chance(500, True):.6%}"
                        f"<br>50K torches: {self._search_chance(50000, True):.6%}"
                    ),
                    picture_class="temple-torch",
                ),
                Advice(
                    label=(
                        f"{self.amplify} Amplifications: "
                        f"+{5 * self.amplify}% Respawn while Active"
                    ),
                    picture_class="temple-torch",
                ),
            ],
        }
