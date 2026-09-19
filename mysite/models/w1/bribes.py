from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from consts.w1.bribes import bribes
from models.advice.advice import Advice
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class Bribe:
    def __init__(self, info: dict, status: int):
        self.set_name: str = info['Set']
        self.name: str = info['Name']
        self.value: float = info['Value']
        self.unpurchasable: bool = info['Unpurchasable']
        self._unit: str = info['Unit']
        # -1 locked, 0 available, 1 purchased
        self.unlocked: bool = status >= 0
        self.purchased: bool = status == 1

    @cached_property
    def bonus(self) -> float:
        return self.value if self.purchased else 0

    @cached_property
    def as_multi(self) -> float:
        return ValueToMulti(self.bonus)

    def get_advice(self) -> Advice:
        available = self.unlocked and not self.unpurchasable
        return Advice(
            label=f"{self.set_name}: {self.name}"
                  f"{'' if available else '<br>Unavailable for Purchase!'}",
            picture_class=self.name,
            progression=int(self.purchased),
            goal=1,
        )

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        match self._unit:
            case 'x':
                amount = f"{round_and_trim(self.as_multi)}/{round_and_trim(ValueToMulti(self.value))}x"
            case '%':
                amount = f"+{round_and_trim(self.bonus)}/{round_and_trim(self.value)}%"
            case _:
                amount = f"+{round_and_trim(self.bonus)}/{round_and_trim(self.value)}"
        return Advice(
            label=f"{'{{ Bribe|#bribes }}: ' if link_to_section else ''}{self.name}: {amount}",
            picture_class=self.name,
            progression=int(self.purchased),
            goal=1,
        )


class Bribes(dict[str, Bribe]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_bribes = safe_loads(raw_data.get('BribeStatus', []))
        for index, info in enumerate(bribes):
            raw_status = safer_index(raw_bribes, index, None)
            # safer_convert treats 0 as missing
            status = -1 if raw_status is None else safer_convert(raw_status, 0)
            self[info['Name']] = Bribe(info, status)

    def purchased_count(self, set_name: str) -> int:
        return sum(bribe.purchased for bribe in self.values() if bribe.set_name == set_name)
