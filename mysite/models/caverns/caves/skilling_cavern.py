import math
from functools import cached_property

from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_convert, safer_math_pow
from utils.text_formatting import notateNumber


class SkillingCavern(Cavern):
    def __init__(
        self,
        name: str,
        cavern_number: int,
        offset: int,
        resource_type: str,
        resource_skill: str,
    ):
        super().__init__(name=name, cavern_number=cavern_number)
        self._offset = offset
        self.resource_type = resource_type
        self.resource_skill = resource_skill

    def parse(self, raw_caverns_list: list):
        try:
            self.resources_collected = safer_convert(
                raw_caverns_list[11][self._offset], 0.0
            )
        except Exception:
            self.resources_collected = 0
        try:
            self.layers_destroyed = safer_convert(
                raw_caverns_list[11][self._offset + 1], 0
            )
        except Exception:
            self.layers_destroyed = 0

    def _efficiency_required(self) -> int:
        return math.ceil(9000 * safer_math_pow(1.8, self.layers_destroyed))

    @cached_property
    def resources_remaining(self) -> float:
        from models.general.session_data import session_data

        discount = session_data.account.caverns.skilling_resource_discount
        base_requirement = math.ceil(
            200 * safer_math_pow(2.2, 1 + self.layers_destroyed)
        )
        return base_requirement / max(1, discount)

    def advice_groups(self) -> dict[str, list[Advice]]:
        from models.general.session_data import session_data

        resource_required = self.resources_remaining
        resource_remaining = resource_required - self.resources_collected
        progress_percent = 100 * (self.resources_collected / resource_required)

        return {
            "Cavern Stats": [
                self.objective_advice(
                    f"Use your characters to collect {self.resource_type} while "
                    f"{self.resource_skill} and break Layers to collect Opals",
                    resource=self.resource_skill,
                ),
                self.opals_found_advice(),
            ],
            "Layer Stats": [
                Advice(
                    label=(
                        f"Layer {self.layers_destroyed + 1} {self.resource_skill} "
                        f"Efficiency Required: "
                        f"{notateNumber('Basic', self._efficiency_required(), 1)}"
                    ),
                    picture_class=self.resource_skill,
                ),
                session_data.account.caverns.skilling_resource_discount_advice,
                Advice(
                    label=(
                        f"{self.resource_type} remaining to break Layer "
                        f"{self.layers_destroyed + 1}: "
                        f"{notateNumber('Basic', resource_remaining, 1)}"
                    ),
                    picture_class=f"motherlode-{self.resource_type}",
                    progression=f"{min(100, progress_percent):.1f}",
                    goal=100,
                    unit="%",
                ),
            ],
        }
