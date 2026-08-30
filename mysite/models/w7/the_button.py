import math

from consts.consts_autoreview import EmojiType, ValueToMulti
from consts.idleon.w7.the_button import (
    button_bonus_labels,
    button_bonus_per_time,
    button_bonus_picture_classes,
    button_task_order,
    button_tasks,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index
from utils.text_formatting import notateNumber

logger = get_logger(__name__)


class ButtonBonus:
    def __init__(self, index: int, label: str, per_time: float, activation_count: int):
        self.index = index
        self.label = label
        self.per_time = per_time
        self.activation_count = activation_count
        self.value = per_time * activation_count

    def get_advice(self) -> Advice:
        # accumulated value is percentage points; the game applies it as `1 + value/100`
        per_use = f"{round_and_trim(self.per_time / 100)}".lstrip("0")
        return Advice(
            label=(
                f"{self.label}: x{round_and_trim(ValueToMulti(self.value))}"
                f" (x{per_use} per use)"
            ),
            picture_class=button_bonus_picture_classes[self.index],
            progression=self.activation_count,
            goal=EmojiType.INFINITY.value,
        )


class TheButton:
    SLOT_COUNT = len(button_bonus_labels)

    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        if not raw_optlacc:
            logger.warning("The Button data not present.")
        # "OptLacc"[594] in source: raw press counter for The Button
        self.total_clicks = int(safer_index(raw_optlacc, 594, 0))
        full_cycles = self.total_clicks // 5
        self.bonuses: list[ButtonBonus] = []
        for index, (label, per_time) in enumerate(
            zip(button_bonus_labels, button_bonus_per_time)
        ):
            activation_count = (
                full_cycles // self.SLOT_COUNT
                + (1 if index < full_cycles % self.SLOT_COUNT else 0)
            )
            self.bonuses.append(ButtonBonus(index, label, per_time, activation_count))

    def get_bonus_value(self, index: int) -> float:
        # "Button_Bonuses" in source
        return self.bonuses[index].value

    def _get_challenge_advice(self, presses: int, picture_class: str) -> Advice:
        # "Button_Task"/"Button_REQ" in source. Current progress ("Button_uHave")
        # not modeled -- Needs Tome calculation on AR side
        task_index = button_task_order[presses % 100] % len(button_tasks)
        task = button_tasks[task_index]
        match task["FuncType"]:
            case "linear":
                requirement = task["Base"] + presses * task["Coefficient"]
            case "step":
                requirement = task["Base"] + presses / task["Coefficient"]
            case _:
                requirement = task["Base"] * (task["Coefficient"] ** presses)
        requirement = math.ceil(requirement)  # game shows whole numbers only
        description = task["Description"].replace(
            "{", notateNumber("Basic", requirement, 0)
        )
        return Advice(label=description, picture_class=picture_class, progression="", goal="")

    def get_upcoming_bonuses(self, count: int = 5) -> dict[str, list[Advice]]:
        # every 5 presses activates the next slot, round-robin
        activations_done = self.total_clicks // 5
        clicks_remainder = self.total_clicks % 5
        clicks_until_next = 5 - clicks_remainder if clicks_remainder else 5

        result: dict[str, list[Advice]] = {}
        presses_used = 0
        for n in range(count):
            slot = (activations_done + n) % self.SLOT_COUNT
            presses_for_bonus = clicks_until_next if n == 0 else 5
            challenges = [
                self._get_challenge_advice(
                    self.total_clicks + presses_used + i, button_bonus_picture_classes[slot]
                )
                for i in range(presses_for_bonus)
            ]
            presses_used += presses_for_bonus
            header = f"{button_bonus_labels[slot]}: {presses_used} press{'es' if presses_used != 1 else ''} away"
            result[header] = challenges
        return result
