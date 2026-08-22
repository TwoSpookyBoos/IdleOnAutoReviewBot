import math
from functools import cached_property

from consts.caverns.caves.the_well import (
    max_buckets,
    max_sediments,
    schematics_unlocking_buckets,
    sediment_bars,
    sediment_names,
)
from consts.consts_autoreview import ValueToMulti, default_huge_number_replacement
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from models.caverns.villagers.kaipu import SchematicBonus
from utils.logging import get_logger
from utils.safer_data_handling import safer_convert, safer_math_pow
from utils.text_formatting import notateNumber

logger = get_logger(__name__)


class Sediment:
    def __init__(self, index: int, owned: int, level: int):
        self.index = index
        self.name = sediment_names[index]
        self.image = f"well-sediment-{index}"
        self.owned = owned
        self.level = level

    def _bar_requirement(self):
        try:
            return (
                100
                * safer_math_pow(1.5, self.level)
                * ValueToMulti(sediment_bars[self.index])
            )
        except OverflowError:
            logger.exception(
                f"Overflow error calculating SedimentBarRequirement for sediment "
                f"{self.index}, level {self.level}. "
                f"Returning {default_huge_number_replacement}."
            )
            return default_huge_number_replacement

    def advice(self) -> Advice:
        if self.owned < 0:
            return Advice(
                label=f"Clear the rock layer to discover {self.name}!",
                picture_class=self.image,
                resource="well-sediment-rock-layer",
                progression=0,
                goal=100,
                unit="%",
            )
        target = self._bar_requirement()
        if target >= 1e9:
            target_str = notateNumber("Basic", target, 2)
            owned_str = notateNumber("Basic", self.owned, 2)
        else:
            target_str = f"{target:,.0f}"
            owned_str = f"{self.owned:,}"
        return Advice(
            label=(
                f"{self.name}: {self.level} expansions"
                f"<br>{owned_str} owned"
                f"<br>{target_str} to expand"
            ),
            picture_class=self.image,
            progression=f"{100 * (self.owned / target):.1f}",
            goal=100,
            unit="%",
        )


class Bucket:
    def __init__(
        self,
        index: int,
        sediment: Sediment,
        unlocked: bool,
        schematic: SchematicBonus,
    ):
        self.index = index
        self._sediment = sediment
        self.unlocked = unlocked
        self._schematic = schematic

    def advice(self) -> Advice:
        if self.unlocked:
            collecting = self._sediment.owned >= 0
            state = (
                f"Collecting {self._sediment.name}"
                if collecting
                else "Unlocking next sediment"
            )
            return Advice(
                label=f"Bucket {self.index + 1}: {state}",
                picture_class=self._sediment.image,
            )
        return Advice(
            label=(
                f"Unlock Bucket {self.index + 1} by purchasing"
                f"<br>{self._schematic.full_name()}"
            ),
            picture_class=self._schematic.image,
            resource=self._schematic.resource,
        )


class TheWell(Cavern):
    def __init__(self):
        super().__init__(name="The Well", cavern_number=1)

    def parse(self, raw_caverns_list: list):
        self._bucket_targets = []
        for i in range(max_buckets):
            try:
                self._bucket_targets.append(safer_convert(raw_caverns_list[10][i], 0))
            except IndexError:
                self._bucket_targets.append(0)

        self._sediments = []
        for i in range(max_sediments):
            try:
                owned = safer_convert(raw_caverns_list[9][i], sediment_bars[i] * -1)
            except IndexError:
                owned = sediment_bars[i] * -1
            try:
                level = safer_convert(raw_caverns_list[8][i], 0)
            except IndexError:
                level = 0
            self._sediments.append(Sediment(index=i, owned=owned, level=level))

        try:
            self._bar_expansion = "On" if raw_caverns_list[11][10] else "Off"
        except Exception:
            self._bar_expansion = "Off"

        # holes_11_9 looks like just the number of previously completed opal trades.
        # Maybe it changes higher up at some point /shrug
        self._holes_11_9 = safer_convert(raw_caverns_list[11][9], 0)

    @cached_property
    def _schematics(self):
        from models.general.session_data import session_data

        return session_data.account.caverns_.villagers["Kaipu"].schematics

    @cached_property
    def buckets(self) -> list[Bucket]:
        schematics = self._schematics
        buckets_unlocked = 1 + sum(
            1
            for schematic_name in schematics_unlocking_buckets
            if schematics[schematic_name].bought
        )
        return [
            Bucket(
                index=index,
                sediment=self._sediments[target],
                unlocked=index + 1 <= buckets_unlocked,
                schematic=schematics[schematics_unlocking_buckets[index - 1]],
            )
            for index, target in enumerate(self._bucket_targets)
        ]

    def _opal_trade_cost(self):
        holes_11_9 = self._holes_11_9
        if holes_11_9 == 1:
            return 6
        elif holes_11_9 == 2:
            return 60
        else:
            result = (
                1 + (3 * holes_11_9) + safer_math_pow(holes_11_9, 2)
            ) * safer_math_pow(3.5 + holes_11_9 / 10, holes_11_9)
            return math.ceil(result) if 1e9 > result else math.floor(result)

    def advice_groups(self) -> dict[str, list[Advice]]:
        opal_trade_cost = self._opal_trade_cost()
        opal_trade_progress = 100 * (self._sediments[0].owned / opal_trade_cost)
        total_expansions = sum(sediment.level for sediment in self._sediments)
        expander = self._schematics["Expander Extravaganza"]
        uber_bar_expand = self._schematics["UBER Bar Expand-o-rama-hala"]

        return {
            "Cavern Stats": [
                self.objective_advice(
                    "Use buckets to collect Sediment",
                    resource="well-bucket",
                ),
                self.opals_found_advice(),
                Advice(
                    label=(
                        f"Next Opal trade: "
                        f"{notateNumber('Basic', opal_trade_cost, 2)} Gravel"
                    ),
                    picture_class="bucketlyte",
                    resource="well-sediment-0",
                    progression=(
                        f"{min(100, opal_trade_progress):.1f}"
                        f"{'+' if opal_trade_progress > 100 else ''}"
                    ),
                    goal=100,
                    unit="%",
                ),
            ],
            "Bucket Stats": [bucket.advice() for bucket in self.buckets],
            "Sediment Stats": [
                Advice(
                    label=f"Expand Full Bars: {self._bar_expansion}",
                    picture_class=uber_bar_expand.image,
                ),
                Advice(
                    label=f"Total expansions: {total_expansions}"
                    f"<br>Total bonus: "
                    f"{total_expansions * 20 * expander.bought:,}%",
                    picture_class=expander.image,
                ),
                *[sediment.advice() for sediment in self._sediments],
            ],
        }
