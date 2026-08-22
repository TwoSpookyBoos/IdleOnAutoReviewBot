from functools import cached_property

from consts.caverns.caves.the_den import schematics_unlocking_amplifiers
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_math_pow


class TheDen(Cavern):
    def __init__(self):
        super().__init__(name="The Den", cavern_number=3)

    def parse(self, raw_caverns_list: list):
        try:
            self.high_score = round(float(raw_caverns_list[11][8]))
        except Exception:
            self.high_score = 0

    @cached_property
    def _schematics(self):
        from models.general.session_data import session_data

        return session_data.account.caverns_.villagers["Kaipu"].schematics

    def _next_opal_score(self) -> int:
        result = (
            12
            * (150 + (30 + self.opals_found) * self.opals_found)
            * safer_math_pow(1.5, self.opals_found)
        )
        return round(result)

    def _amplifier_advice(
        self,
        index: int,
        amp_name: str,
        description: str,
        unlock_schematic: str,
        image: str,
    ) -> Advice:
        schematics = self._schematics
        unlocked = unlock_schematic == "" or schematics[unlock_schematic].bought
        if unlocked:
            label = f"{amp_name}: {description}"
            resource = ""
        else:
            schematic = schematics[unlock_schematic]
            label = (
                f"Unlock Amplifier {index + 1} by purchasing"
                f"<br>{schematic.full_name()}"
            )
            resource = schematic.resource
        return Advice(label=label, picture_class=image, resource=resource)

    def advice_groups(self) -> dict[str, list[Advice]]:
        next_opal_score = self._next_opal_score()

        return {
            "Cavern Stats": [
                self.objective_advice(
                    "Fight increasingly difficult Dawgs, using Amplifiers to "
                    "increase score",
                    resource="dawg-den-dawgs",
                ),
                self.opals_found_advice(),
                Advice(
                    label=(
                        f"High Score: {self.high_score:,}"
                        f"<br>Next Opal:  {next_opal_score:,}"
                    ),
                    picture_class="my-first-trophy",
                    progression=f"{100 * (self.high_score / next_opal_score):.1f}",
                    goal=100,
                    unit="%",
                ),
            ],
            "Amplifier Stats": [
                self._amplifier_advice(
                    index, amp_name, description, unlock_schematic, image
                )
                for index, (
                    amp_name,
                    (description, unlock_schematic, image),
                ) in enumerate(schematics_unlocking_amplifiers.items())
            ],
        }
