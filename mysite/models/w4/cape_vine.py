from collections import defaultdict
from collections.abc import Collection
from functools import cached_property

from consts.consts_item_data import ITEM_DATA
from consts.w4.cape_vine import cape_vine_capes
from models.advice.advice import Advice
from models.general.item_definitions import ItemDefinition
from models.general.session_data import session_data
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index

_section_link = "{{ Cape Vine|#cape-vine }} - "


class CapeVineCape:
    """A cape in vine slot `index`, or not deposited when `index` is None."""

    def __init__(self, cape_vine: "CapeVine", cape: ItemDefinition, index: int | None):
        self.cape_vine = cape_vine
        self.cape = cape
        self.index = index

    @property
    def deposited(self) -> bool:
        return self.index is not None

    @property
    def golden(self) -> bool:
        return self.deposited and self.index < self.cape_vine.golden_vines

    @property
    def multi(self) -> float:
        # "CapevineBonusMulti" in source. Last updated in v2.561.0
        if not self.deposited:
            return 1
        return self.cape_vine.multi if self.golden else self.cape_vine.plain_multi

    def add_bonus_to(self, total: dict[str, float]):
        self.cape.bonus.add_to(total, self.multi)

    def get_advice(
        self, stats: Collection[str] | None = None, link_to_section: bool = False
    ) -> Advice:
        link = _section_link if link_to_section else ""
        misc_lines = "".join(
            f"<br>{misc.get_label(self.multi)}"
            for misc in self.cape.bonus.get_misc_bonuses(stats)
        )
        return Advice(
            label=f"{link}{self.cape.name}{misc_lines}<br>{self._get_vine_label()}",
            picture_class=self.cape.name,
            resource="golden-vine" if self.golden else "",
            progression="" if self.deposited else 0,
            goal="" if self.deposited else 1,
        )

    def _get_vine_label(self) -> str:
        if not self.deposited:
            return "Not deposited"
        vine = "Golden" if self.golden else "Plain"
        return f"{vine} Vine: {round_and_trim(self.multi)}x"


class CapeVine:
    def __init__(self, raw_data: dict):
        spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        # "Spelunk"[54] in source: deposited cape codes, in vine order
        raw_capes: list[str] = safer_index(spelunk_info, 54, []) or []
        self.deposited_count: int = len(raw_capes)
        self.slots: list[CapeVineCape] = [
            CapeVineCape(self, ITEM_DATA[code], index)
            for index, code in enumerate(raw_capes)
            if code in ITEM_DATA
        ]
        self.missing: list[CapeVineCape] = [
            CapeVineCape(self, cape, None)
            for cape in cape_vine_capes
            if cape.code_name not in raw_capes
        ]
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        # "OptionsListAccount"[669] in source: Golden Vines asked from Cathie
        self._golden_vines_asked: int = round(
            safer_convert(safer_index(raw_optlacc, 669, 0), 0)
        )
        self._next_golden_vine_level: int = 1000 + 500 * self._golden_vines_asked

    @cached_property
    def golden_vines(self) -> int:
        # "GoldCapeVinesOwned" in source. Last updated in v2.561.0
        bundle_owned = session_data.account.gemshop.bundles["ban_o"].owned
        return 1 + self._golden_vines_asked + 3 * bundle_owned

    @cached_property
    def multi(self) -> float:
        # "CapevineBonusMulti" in source, Golden Vine part. Last updated in v2.561.0
        catherine = session_data.account.companions["Catherine"].bonus
        return 1 + (self.deposited_count + catherine) / 100

    @property
    def plain_multi(self) -> float:
        # "CapevineBonusMulti" in source, outside a Golden Vine
        return 0.25 * self.multi

    @cached_property
    def bonuses(self) -> dict[str, tuple[str, float]]:
        # "InitializeCapeBonuses" in source, misc lines only. Last updated in v2.561.0
        total = defaultdict(float)
        for slot in self.slots:
            slot.add_bonus_to(total)
        return {
            key.split(" ", 1)[1]: (key, value)
            for key, value in total.items()
            if key.startswith("%")
        }

    def get_bonus_value(self, name: str) -> float:
        return self.bonuses.get(name, ("", 0.0))[1]

    def get_cape_advices(self, stats: tuple[str, ...]) -> list[Advice]:
        # For other sections, linked here
        return [
            cape.get_advice(stats, link_to_section=True)
            for cape in self._get_capes_with(stats)
        ]

    def _get_capes_with(self, stats: tuple[str, ...]) -> list[CapeVineCape]:
        # Most important stat first (earlier in `stats`), then the biggest value
        return sorted(
            (
                cape
                for cape in [*self.slots, *self.missing]
                if cape.cape.bonus.get_misc_bonuses(stats)
            ),
            key=lambda cape: min(
                (stats.index(misc.effect), -misc.value)
                for misc in cape.cape.bonus.get_misc_bonuses(stats)
            ),
        )

    def get_deposited_multi_advice(self) -> Advice:
        return Advice(
            label=f"+1% Cape Vine Multi per deposited cape: +{self.deposited_count}%",
            picture_class="golden-vine",
            progression=self.deposited_count,
            goal=len(cape_vine_capes),
        )

    def get_golden_vines_advice(self) -> Advice:
        # Asked with the current character in source, so any character's class Lv
        highest_level = max(
            (character.combat_level for character in session_data.account.characters),
            default=0,
        )
        return Advice(
            label=f"Golden Vines: {self.golden_vines}"
            f"<br>Ask Cathie for the next one at class Lv "
            f"{self._next_golden_vine_level}",
            picture_class="golden-vine",
            progression=highest_level,
            goal=self._next_golden_vine_level,
        )

    def get_bundle_advice(self) -> Advice:
        gemshop = session_data.account.gemshop
        bundle = gemshop.bundles["ban_o"]
        return Advice(
            label=f"{{{{ Gem Shop|#gem-shop }}}} - {bundle.display}: +3 Golden Vines",
            picture_class="gem",
            progression=int(bundle.owned) if gemshop.bundle_data_present else "IDK",
            goal=1,
        )
