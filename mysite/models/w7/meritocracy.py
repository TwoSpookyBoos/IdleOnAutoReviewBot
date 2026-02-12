import math
import time

from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.meritocracy import meritocracy_week_time_offset
from consts.w7.meritocracy import merit_bonus

from models.advice.advice import Advice

from utils.safer_data_handling import safer_index, safer_get
from utils.number_formatting import round_and_trim

from utils.logging import get_logger

logger = get_logger(__name__)


class MeritocracyBonus:
    def __init__(self, index: int, info: dict):
        self._template = info["Bonus"]
        self._base_value = info["Value"]
        self._image = f"meritocracy-{index}"
        self.value = 0
        self._bonus_value = 0
        self._is_active = 0

    def calculate_bonus(self, multi: float):
        # "MeritocBonusz" in source. Last update in v2.48 Giftmas Event
        self._bonus_value = self._base_value * multi
        self.value = self._is_active * self._bonus_value

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{Meritocracy|#meritocracy}}<br>"
        description = self._template.replace(
            "}", f"{round_and_trim(ValueToMulti(self._bonus_value))}"
        )
        label += description
        if link_to_section:
            match self._is_active:
                case 0:
                    label += "<br>Bonus not active"
                case 1:
                    label += "<br>Bonus active"
        return Advice(label=label, picture_class=self._image, progression="", goal="")

    def set_vote_percent(self, value: int):
        self._vote_percent = value / 100

    def get_vote_advice(self) -> Advice:
        advice = self.get_bonus_advice(False)
        advice.change_progress("", f"{self._vote_percent:.0%}")
        return advice

    def activate_bonus(self):
        self._is_active = 1


class Meritocracy(list[MeritocracyBonus]):
    def __init__(self, raw_data: dict):
        raw_optlacc = raw_data.get("OptLacc", [])
        # "MeritocCanVote" in source
        self.can_vote = bool(safer_index(raw_optlacc, 472, 0))
        self.extend(
            [
                MeritocracyBonus(index, bonus_info)
                for index, bonus_info in enumerate(merit_bonus)
            ]
        )
        # a.engine.getGameAttribute("OptionsListAccount")[451] in source.
        # Last update in v2.48 Giftmas Event
        self._week = safer_index(raw_optlacc, 451, 0)
        # calculate "OptionsListAccount"[451] by hand to know current week
        current_week = math.floor((time.time() + meritocracy_week_time_offset) / 604800)
        if current_week != self._week:
            self.active = None
            self.on_vote = []
        else:
            raw_server_vars = raw_data.get("serverVars", raw_data.get("servervars", {}))
            raw_vote_categories = safer_get(raw_server_vars, "voteCat2", [0, 0, 0, 0])
            self.active = self[raw_vote_categories[0]]
            self.active.activate_bonus()
            vote_percent = safer_get(raw_server_vars, "votePercent2", [60, 30, 10])
            self.on_vote = [self[index] for index in raw_vote_categories[1:]]
            [
                bonus.set_vote_percent(vote_percent[index])
                for index, bonus in enumerate(self.on_vote)
            ]

    def calculate_bonuses(self):
        # TODO: "MeritocBonuszMulti"
        bonus_multi = 1
        for bonus in self:
            bonus.calculate_bonus(bonus_multi)

    def get_active_bonus_advice(self) -> Advice | None:
        if self.active is None:
            return None
        return self.active.get_bonus_advice(False)
