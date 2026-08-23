from functools import cached_property
from math import ceil

from consts.caverns.caves.the_bell import (
    bell_clean_improvements,
    bell_improvement_stack_multipliers,
    bell_ring_bonuses,
)
from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_convert, safer_math_pow
from utils.text_formatting import notateNumber

_CHARGE_NAMES = ("Ring", "Ping", "Clean", "Renew")


class BellCharge:
    def __init__(self, name: str, index: int, current: float, uses: float):
        self.name = name
        self.index = index
        self.current = current
        self.uses = uses

    def required(self) -> float:
        match self.index:
            case 0:  # Ring
                return (5 + 3 * self.uses) * safer_math_pow(1.05, self.uses)
            case 1:  # Ping
                return (
                    10 + (10 * self.uses + safer_math_pow(self.uses, 2.5))
                ) * safer_math_pow(1.75, self.uses)
            case 2:  # Clean
                return 100 * safer_math_pow(3, self.uses)
            case _:  # Renew falls into this else
                return 250


class BellRingBonus:
    def __init__(self, index: int, details: dict, level: int):
        self.index = index
        self.description = details["Description"]
        self.image = details["Image"]
        self.level = level
        self.value = level * details["ScalingValue"]

    def advice(self) -> Advice:
        rendered_description = self.description.replace("{", f"{self.value:.2f}")
        return Advice(
            label=rendered_description,
            picture_class=self.image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
        )


class BellImprovement:
    def __init__(self, cavern: "TheBell", index: int, details: dict, level: int):
        self.cavern = cavern
        self.index = index
        self.description = details["Description"]
        self.image = details["Image"]
        self.resource = details["Resource"]
        self.level = level

    @cached_property
    def value(self) -> float:
        # `BellMethodsQTY` in source. Last updated in v2.43 Nov 6
        # Yes, the stack multiplier only applies AFTER the schematic is purchased.
        # Probably a bug in game but must be replicated for accuracy.
        from models.general.session_data import session_data

        schematic_bought = (
            session_data.account.caverns_.villagers["Kaipu"]
            .schematics["Improvement Stackin'"]
            .bought
        )
        try:
            multiplier = bell_improvement_stack_multipliers[self.index]
            return (
                2
                * self.level
                * max(1, self.cavern.stack_multi * schematic_bought * multiplier)
            )
        except Exception:
            return 0

    def advice(self) -> Advice:
        rendered_description = self.description.replace("{", f"{self.value:,.0f}")
        return Advice(
            label=rendered_description,
            picture_class=self.image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
            resource=self.resource,
        )


class TheBell(Cavern):
    STACK_SIZE = 25

    def __init__(self):
        super().__init__(name="The Bell", cavern_number=5)

    def parse(self, raw_caverns_list: list):
        self.charges: dict[str, BellCharge] = {}
        for index, name in enumerate(_CHARGE_NAMES):
            try:
                current = safer_convert(raw_caverns_list[18][index * 2], 0)
            except Exception:
                current = 0
            try:
                uses = safer_convert(raw_caverns_list[18][index * 2 + 1], 0)
            except Exception:
                uses = 0
            self.charges[name] = BellCharge(
                name=name, index=index, current=current, uses=uses
            )

        self.ring_bonuses: list[BellRingBonus] = []
        ring_levels = raw_caverns_list[17]
        for index, details in bell_ring_bonuses.items():
            try:
                level = int(ring_levels[index])
            except Exception:
                level = 0
            self.ring_bonuses.append(
                BellRingBonus(index=index, details=details, level=level)
            )

        self.improvements: list[BellImprovement] = []
        improvement_levels = raw_caverns_list[16]
        for index, details in bell_clean_improvements.items():
            try:
                level = improvement_levels[index]
            except Exception:
                level = 0
            self.improvements.append(
                BellImprovement(cavern=self, index=index, details=details, level=level)
            )

    @cached_property
    def total_improvements(self) -> int:
        return sum(improvement.level for improvement in self.improvements)

    @cached_property
    def total_stacks(self) -> int:
        return self.total_improvements // self.STACK_SIZE

    @cached_property
    def stack_multi(self) -> float:
        return safer_math_pow(1.1, self.total_stacks)

    def advice_groups(self) -> dict[str, list[Advice]]:
        ping = self.charges["Ping"]
        target_cost = ceil(ping.required())
        target_string = notateNumber("Basic", target_cost, 2)
        current_string = notateNumber("Match", ping.current, 2, "", target_string)
        current_percent = 100 * (ping.current / target_cost)

        total_rings = self.charges["Ring"].uses
        total_bonus_levels = sum(bonus.level for bonus in self.ring_bonuses)
        average_level = total_bonus_levels / max(1, total_rings)

        return {
            "Cavern Stats": [
                self.objective_advice(
                    "Passively build up Charge in 1 of 4 different categories at a "
                    "time for various Bonuses"
                ),
                self.opals_found_advice(),
                Advice(
                    label=(
                        f"Current Ping charge: {current_string}"
                        f"<br>Next Opal: {target_string}"
                    ),
                    picture_class="bell-ping",
                    progression=f"{current_percent:,.2f}",
                    goal=100,
                    unit="%",
                ),
            ],
            "Ring Stats": [
                Advice(label=f"Total Rings: {total_rings}", picture_class="bell-ring"),
                Advice(
                    label=(
                        f"Total Bonus levels: {total_bonus_levels}"
                        f"<br>Avg per ring: {average_level:.4f}"
                    ),
                    picture_class="bell-ring",
                    completed=False,
                    informational=True,
                ),
                *[bonus.advice() for bonus in self.ring_bonuses],
            ],
            "Improvement Stats": [
                Advice(
                    label=(
                        f"Total Improvements: {self.total_improvements} "
                        f"({self.total_stacks} stacks)"
                        f"<br>Total Bonus: {self.stack_multi:.1f}x"
                        f"<br>Next stack progress"
                    ),
                    picture_class="engineer-schematic-45",
                    progression=self.total_improvements % self.STACK_SIZE,
                    goal=self.STACK_SIZE,
                ),
                *[improvement.advice() for improvement in self.improvements],
            ],
        }
