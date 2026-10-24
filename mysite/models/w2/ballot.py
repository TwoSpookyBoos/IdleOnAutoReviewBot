from consts.consts_autoreview import ValueToMulti
from consts.consts_w2 import ballot_dict
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_get


class BallotBuff:
    def __init__(self, index: int, info: dict, current_buff: int):
        self.index: int = index
        self.base_value: float = info["BaseValue"]
        self.value: float = self.base_value
        self.image: str = info["Image"]
        self.description: str = info["Description"]
        self.active: bool = current_buff == index
        # 0 means the save has no vote data
        self._status_known: bool = current_buff != 0

    @property
    def status(self) -> str:
        if self.active:
            return "is Active"
        if self._status_known:
            return "is Inactive"
        return "status is not available in provided data"

    @property
    def multi(self) -> float:
        return ValueToMulti(self.value)

    @property
    def active_multi(self) -> float:
        return max(1, self.multi * self.active)

    def calculate_value(self, bonus_multi: float):
        self.value *= bonus_multi
        if "{" in self.description:
            self.description = self.description.replace("{", f"{self.value:.3f}")
        if "}" in self.description:
            self.description = self.description.replace("}", f"{self.multi:.3f}")

    def get_advice(self) -> Advice:
        return Advice(
            label=f"Bonus {self.index}: {self.description}",
            picture_class=self.image,
        )

    def get_bonus_advice(self) -> Advice:
        return Advice(
            label=f"Weekly {{{{ Ballot|#bonus-ballot }}}} - "
            f"{self.active_multi:.3f}/{self.multi:.3f}x<br>(Buff {self.status})",
            picture_class=self.image,
            progression=int(self.active),
            goal=1,
            completed=True,
        )


class Ballot(dict[int, BallotBuff]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_server_vars = safe_loads(
            raw_data.get("serverVars", raw_data.get("servervars", {}))
        )
        raw_votes = safer_get(raw_server_vars, "voteCategories", [0, 0, 0, 0])
        raw_votes = [safer_convert(vote, 0) for vote in raw_votes]
        self.current_buff: int = raw_votes[0]
        self.on_the_ballot: list[int] = raw_votes[1:]
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.week: int = safer_get(raw_optlacc, 309, 0)
        self.bonus_multi: float = 1
        for index, info in ballot_dict.items():
            self[index] = BallotBuff(index, info, self.current_buff)

    def calculate_values(
        self,
        voter_rights_level: int,
        voter_integrity_value: float,
        summoning_value: float,
        gilded_vote_button: bool,
        royal_vote_button: bool,
        mashed_potato_bonus: float,
        crystal_cuttlefish_bonus: float,
        democracy_ftw_value: float,
    ):
        # "VotingBonuszMulti" in source.
        # Last update v2.48 Giftmas Event (December 8, 2025)
        bonus_multi = ValueToMulti(
            voter_rights_level
            + voter_integrity_value
            + summoning_value
            + (17 * gilded_vote_button)
            + (13 * royal_vote_button)
            + mashed_potato_bonus
            + crystal_cuttlefish_bonus
            + democracy_ftw_value
        )
        self.bonus_multi = bonus_multi
        for buff in self.values():
            buff.calculate_value(bonus_multi)
