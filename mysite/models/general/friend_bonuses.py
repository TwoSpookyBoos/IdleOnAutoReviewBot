from consts.consts_autoreview import MultiToValue, ValueToMulti
from consts.general.friend_bonuses import (
    friend_bonus_base,
    friend_bonus_max_slots,
    friend_bonus_optlacc_index,
    friend_bonus_stat_count,
    friend_bonus_stat_names,
)
from models.advice.advice import Advice
from models.general.companions import Companions
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class FriendBonus:
    def __init__(self, stat: int, friend_value: float, friend_name: str):
        self.stat = stat
        self.friend_value = friend_value
        self.friend_name = friend_name
        self.name = friend_bonus_stat_names.get(stat, f"Stat {stat}")
        self.value = 0
        self.max_value = 0

    # "FriendBonusQTY" in source. Last updated in v2.531.0
    def calculate_bonus(self, xtra_multi: float):
        base = safer_index(friend_bonus_base, self.stat, 0)
        clamped = min(3e4, max(0.0, self.friend_value))
        scale = min(1.5, 0.25 + clamped / (clamped + 12e3) * 1.5)
        self.value = base * scale * xtra_multi
        self.max_value = base * 1.5 * xtra_multi

    def get_bonus_advice(self) -> Advice:
        bonus = f"{round_and_trim(self.value)}/{round_and_trim(self.max_value)}"
        friend = self.friend_name.replace("_", " ")
        return Advice(
            label=f"Codex - {self.name} Friend Bonus: +{bonus}% {self.name}"
            f"<br>From {friend} ({round_and_trim(self.friend_value)})",
            picture_class="event-shop-22",
            progression=round_and_trim(self.value),
            goal=round_and_trim(self.max_value),
        )


class FriendBonuses(dict[int, FriendBonus]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        raw_friends = f"{safer_index(raw_optlacc, friend_bonus_optlacc_index, '')}"
        self._entries: list[tuple[int, float, str]] = []
        if raw_friends not in ("", "0", "None"):
            for entry in raw_friends.split(";"):
                fields = entry.split(",")
                self._entries.append(
                    (
                        safer_convert(safer_index(fields, 0, -1), -1),
                        safer_convert(safer_index(fields, 1, 0.0), 0.0),
                        safer_index(fields, 2, ""),
                    )
                )
        self.slots = 0
        self.xtra_multi = 1.0

    def calculate_bonuses(self, companions: Companions, friendly_slot: bool):
        # "FriendBonusSlots" in source. Last updated in v2.531.0
        companion_slots = sum(
            companion.get_value("Friend Bonus Slots")
            for companion in companions.values()
        )
        self.slots = round(
            min(friend_bonus_max_slots, 2 + companion_slots + friendly_slot)
        )
        # "FriendBonusXtraMulti" in source. Last updated in v2.531.0
        self.xtra_multi = ValueToMulti(
            sum(
                MultiToValue(companion.get_multi("Friend Bonuses"))
                for companion in companions.values()
            )
        )
        self.clear()
        # later entries overwrite
        for stat, friend_value, friend_name in self._entries[: self.slots]:
            if 0 <= stat < friend_bonus_stat_count:
                self[stat] = FriendBonus(stat, friend_value, friend_name)
        for bonus in self.values():
            bonus.calculate_bonus(self.xtra_multi)
