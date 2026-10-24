from math import ceil, floor

from consts.consts_w3 import refinery_dict, refinery_max_powerpercycle
from utils.number_formatting import parse_number
from utils.safer_data_handling import safe_loads, safer_index, safer_math_pow


class Salt:
    def __init__(self, name: str, info: list, raw_salt: list):
        self.name: str = name
        self.rank: int = parse_number(safer_index(raw_salt, 1, 0), 0)
        self.running: bool = bool(parse_number(safer_index(raw_salt, 3, 0), 0))
        self.auto_refine: int = parse_number(safer_index(raw_salt, 4, 0), 0)
        (
            _,
            self.image,
            self.cycles_per_synthesis_cycle,
            self.previous_salt_consumption,
            self.next_salt_consumption,
            self.next_salt_cycles_per_synthesis_cycle,
        ) = info
        self.output: int = 0
        self.output_maxed: bool = False
        self.consumed: int = 0
        self.max_rank_with_excess: int = self.rank

    @property
    def excess(self) -> bool:
        return self.output >= self.consumed

    @property
    def excess_or_deficit(self) -> str:
        return "excess" if self.excess else "deficit"

    @property
    def excess_amount(self) -> int:
        return self.output - self.consumed

    def calculate(
        self,
        next_rank: int,
        previous: "Salt | None",
        merit_purchased: bool,
        panda_bonus: float,
    ):
        consumption_scaling = 1.3 if merit_purchased else 1.5
        output_per_cycle = int(
            floor(
                min(
                    refinery_max_powerpercycle,
                    safer_math_pow(self.rank, 1.3) * (1 + panda_bonus),
                )
            )
        )
        self.output = output_per_cycle * self.cycles_per_synthesis_cycle
        self.output_maxed = output_per_cycle >= refinery_max_powerpercycle
        self.consumed = (
            int(
                floor(safer_math_pow(next_rank, consumption_scaling))
                * self.next_salt_consumption
                * self.next_salt_cycles_per_synthesis_cycle
            )
            if next_rank != 0
            else 0
        )
        self.max_rank_with_excess = self.rank
        if (
            previous is not None
            and previous.excess
            and not self.output_maxed
            and (next_rank != 0 or self.name == "Nullo")
        ):
            # Highest rank the previous salt's output can feed
            supported_rank = max(
                0,
                ceil(
                    safer_math_pow(
                        previous.output
                        / (
                            self.previous_salt_consumption
                            * self.cycles_per_synthesis_cycle
                        ),
                        1 / consumption_scaling,
                    )
                    - 1
                ),
            )
            self.max_rank_with_excess = max(self.rank, supported_rank)


class Refinery(dict[str, Salt]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_refinery = safe_loads(raw_data.get("Refinery", []))
        for name, info in refinery_dict.items():
            self[name] = Salt(name, info, safer_index(raw_refinery, info[0], []))

    def calculate(self, panda_bonus: float, merit_level: int):
        # Each merit level lowers consumption for the next salt in the chain
        salts = list(self.values())
        for index, salt in enumerate(salts):
            next_salt = safer_index(salts, index + 1, None)
            salt.calculate(
                next_salt.rank if next_salt else 0,
                salts[index - 1] if index > 0 else None,
                index == 0 or merit_level >= index,
                panda_bonus,
            )
