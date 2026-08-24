from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_convert, safer_math_pow
from utils.text_formatting import notateNumber


class Grotto(Cavern):
    def __init__(self):
        super().__init__(name="Grotto", cavern_number=9)

    def parse(self, raw_caverns_list: list):
        try:
            self.current_kills = safer_convert(raw_caverns_list[11][27], 0)
        except Exception:
            self.current_kills = 0
        self.kills_required = self._kills_required()
        self.kills_remaining = max(0, self.kills_required - self.current_kills)

    def _kills_required(self) -> float:
        # `getGrottoKills` in source; scales with Opals Found in the Grotto.
        return 5000 * safer_math_pow(3.4, self.opals_found)

    def alert_advice(self) -> Advice | None:
        """For display outside Grotto's own advice_groups(), as an alert when
        the Monarch is ready to be challenged."""
        if self.current_kills < 0.99 * self.kills_required:
            return None
        return Advice(
            label="Challenge {{ The Monarch|#glowshroom-tunnels }}!",
            picture_class="gloomie-mushroom",
        )

    def advice_groups(self) -> dict[str, list[Advice]]:
        target_string = notateNumber("Basic", self.kills_required, 2)
        current_string = notateNumber(
            "Match", self.current_kills, 2, matchString=target_string
        )
        return {
            "Cavern Stats": [
                Advice(
                    label=(
                        "Opal Objective- Kill enough Gloomie Mushrooms to "
                        "summon and defeat a Monarch."
                    ),
                    picture_class=self.image,
                    resource="gloomie-mushroom",
                ),
                Advice(
                    label=(
                        "Bonus Objective- Collect Villager "
                        "{{Statues|#statues}} from AFK kills."
                    ),
                    picture_class="villager-statue",
                ),
                self.opals_found_advice(),
            ],
            "FAQs": [
                Advice(
                    label=(
                        "Mushroom HP does NOT increase after defeating a "
                        "Monarch.<br>The number of kills required and the "
                        "Monarch's HP will increase."
                    ),
                    picture_class="gloomie-mushroom",
                ),
                Advice(
                    label=(
                        "Statues from Active kills don't have their quantity "
                        "multiplied by Multikill. Farm them AFK instead."
                        "<br>Statues cannot be sampled."
                    ),
                    picture_class="villager-statue",
                ),
            ],
            "Colony Stats": [
                Advice(
                    label=(
                        f"Kills before Monarch: "
                        f"{notateNumber('Basic', self.kills_remaining, 2)}"
                    ),
                    picture_class="gloomie-mushroom",
                    progression=current_string,
                    goal=target_string,
                ),
            ],
        }
