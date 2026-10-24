from collections.abc import Callable
from dataclasses import dataclass
from math import floor

from consts.consts_w4 import lab_bonuses_dict, lab_jewels_dict, max_nblb_bubbles
from consts.idleon.lava_func import lava_func
from consts.w4.lab import (
    lab_arena_bonus_wave,
    lab_arena_line_width,
    lab_base_connection_range,
    lab_base_line_width,
    lab_bling_jewel_levels,
    lab_bonus_emporium_unlocks,
    lab_bonus_fixed_ranges,
    lab_jewel_fixed_ranges,
    lab_line_width_card_cap,
    lab_line_width_per_level,
    lab_merit_range_per_level,
    lab_prism_coords,
    lab_sapphire_rhombol_aura_multi,
    lab_sapphire_rhombol_aura_range,
    lab_shiny_line_width_per_level,
    lab_souped_tube_line_width,
)
from models.advice.advice import Advice
from models.general.cards import Card
from models.general.character import Character
from models.w4.breeding import Breeding
from models.w4.cooking import Meals
from models.w4.lab_chips import LabChip
from utils.all_talentsDict import all_talentsDict
from utils.safer_data_handling import safe_loads, safer_convert, safer_index
from utils.text_formatting import kebab


def lab_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    # "DistanceEqn" in source. Last updated in v2.531.0
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    return 0.9604339 * max(dx, dy) + 0.397824735 * min(dx, dy)


class LabBonus:
    def __init__(self, info: dict):
        self.name: str = info["Name"]
        self.description: str = info["Description"]
        self.x: float = info["XCoord"]
        self.y: float = info["YCoord"]
        self.off_value: float = info["OffValue"]
        self.base_value: float = info["BaseValue"]
        self.value: float = self.off_value
        self.image: str = kebab(self.name)
        self.fixed_range: int | None = lab_bonus_fixed_ranges.get(self.name)
        self.owned: bool = self.name not in lab_bonus_emporium_unlocks
        self.enabled: bool = False

    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        self.value = self.base_value if enabled else self.off_value

    def get_bonus_advice(self, additional_text: str = "") -> Advice:
        return Advice(
            label=f"Lab Bonus - {self.name}: "
            f"{self.value:g}/{self.base_value:g}x{additional_text}",
            picture_class=self.image,
            progression=int(self.enabled),
            goal=1,
        )


class LabBonuses(dict[str, LabBonus]):
    def __init__(self):
        super().__init__()
        for info in lab_bonuses_dict.values():
            self[info["Name"]] = LabBonus(info)

    def calculate_nblb(
        self,
        pyrite_rhinestone: bool,
        amberite_level: int,
        moar_bubbles: bool,
        even_moar_bubbles: bool,
        merit_level: int,
    ):
        nblb = self["No Bubble Left Behind"]
        # Moar Bubbles superbits are chances, not guarantees
        nblb.value = (
            3
            + pyrite_rhinestone
            + amberite_level
            + moar_bubbles
            + even_moar_bubbles
            + merit_level
        ) * nblb.enabled
        nblb.value = min(max_nblb_bubbles, nblb.value)


class LabJewel:
    def __init__(self, info: dict, owned: bool):
        self.name: str = info["Name"]
        self.description: str = info["Description"]
        self.x: float = info["XCoord"]
        self.y: float = info["YCoord"]
        self.base_value: float = info["BaseValue"]
        self.value: float = info["BaseValue"]
        self.image: str = kebab(self.name)
        self.fixed_range: int | None = lab_jewel_fixed_ranges.get(self.name)
        self.owned: bool = owned
        self.enabled: bool = False

    @property
    def active_value(self) -> float:
        return self.value * self.enabled

    def get_bonus_advice(self) -> Advice:
        return Advice(
            label=f"Lab Jewel - {self.name}: +{self.active_value:g}/{self.value:g}%",
            picture_class=self.image,
            progression=int(self.enabled),
            goal=1,
        )


class LabJewels(dict[str, LabJewel]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_lab = safe_loads(raw_data.get("Lab", []))
        raw_jewels = safer_index(raw_lab, 14, [])
        for index, info in lab_jewels_dict.items():
            owned = safer_index(raw_jewels, index, 0) == 1
            self[info["Name"]] = LabJewel(info, owned)


class LabPlayer:
    def __init__(
        self,
        index: int,
        x: float,
        y: float,
        afk_in_lab: bool,
        lab_level: int,
        chips: list,
    ):
        self.index: int = index
        self.x: float = x
        self.y: float = y
        self.afk_in_lab: bool = afk_in_lab
        self.lab_level: int = lab_level
        self.chips: list = chips
        self.in_tube: bool = afk_in_lab
        self.souped: bool = False
        self.line_width: int = 0


@dataclass
class _LineWidthBonuses:
    # "Dist","Player" in source. Last updated in v2.531.0
    px_line: float
    line_pct: float
    card: float
    purple_tube: float
    bubonic_index: int
    motherboard_index: int
    motherboard_value: float
    arena: float
    shiny: float


class LabMainframe:
    def __init__(self, raw_data: dict, bonuses: LabBonuses, jewels: LabJewels):
        self._bonuses: LabBonuses = bonuses
        self._jewels: LabJewels = jewels
        raw_lab = safe_loads(raw_data.get("Lab", []))
        raw_coords = safer_index(raw_lab, 0, [])
        self.players: list[LabPlayer] = []
        index = 0
        while f"Lv0_{index}" in raw_data:
            self.players.append(
                LabPlayer(
                    index,
                    safer_convert(safer_index(raw_coords, 2 * index, 0), 0.0),
                    safer_convert(safer_index(raw_coords, 2 * index + 1, 0), 0.0),
                    raw_data.get(f"AFKtarget_{index}") == "Laboratory",
                    safer_index(safe_loads(raw_data[f"Lv0_{index}"]), 12, 0),
                    safer_index(raw_lab, 1 + index, []),
                )
            )
            index += 1
        self.connected_players: list[LabPlayer] = []

    @property
    def total_lab_levels(self) -> int:
        return sum(player.lab_level for player in self.players)

    def calculate(
        self,
        characters: list[Character],
        account_wide_arctis: bool,
        souped_tubes: int,
        emporium: dict,
        meals: Meals,
        crystal_card: Card,
        motherboard: LabChip,
        breeding: Breeding,
        range_merit_level: int,
        flat_range: float,
        calculate_meals: Callable[[], None],
    ):
        self._calculate_unlocks(emporium)
        arctis_linked = {
            char.character_index: account_wide_arctis or char.isArctisLinked()
            for char in characters
        }
        self._calculate_tubes(arctis_linked, souped_tubes)
        flat_range += range_merit_level * lab_merit_range_per_level
        black_diamond = self._jewels["Black Diamond Rhinestone"]
        # Black Diamond boosts meals, and meals boost line width
        for _ in range(2):
            was_enabled = black_diamond.enabled
            calculate_meals()
            self._calculate_line_widths(
                self._line_width_bonuses(
                    characters, meals, crystal_card, motherboard, breeding
                )
            )
            self._calculate_connections(flat_range)
            if black_diamond.enabled == was_enabled:
                break

    def _calculate_unlocks(self, emporium: dict):
        for bonus_name, matrix in lab_bonus_emporium_unlocks.items():
            self._bonuses[bonus_name].owned = emporium[matrix].obtained
        if emporium["Laboratory Bling"].obtained:
            for jewel_name, levels in lab_bling_jewel_levels.items():
                if self.total_lab_levels >= levels:
                    self._jewels[jewel_name].owned = True

    def _line_width_bonuses(
        self,
        characters: list[Character],
        meals: Meals,
        crystal_card: Card,
        motherboard: LabChip,
        breeding: Breeding,
    ) -> _LineWidthBonuses:
        # "BubonicPurple" in source: the last Bubonic with Purple Tube sets the line.
        # Last updated in v2.531.0
        bubonic = next(
            (
                char
                for char in reversed(characters)
                if char.current_preset_talents.get("535", 0) > 0
                or char.secondary_preset_talents.get("535", 0) > 0
            ),
            None,
        )
        purple_tube = all_talentsDict[535]
        purple_tube_value = lava_func(
            purple_tube["funcX"],
            # Base level only: bonus talent levels come in wave 3
            max(
                (char.current_preset_talents.get("535", 0) for char in characters),
                default=0,
            ),
            purple_tube["x1"],
            purple_tube["x2"],
        )
        return _LineWidthBonuses(
            px_line=meals.stat_total("PxLine"),
            line_pct=meals.stat_total("LinePct"),
            card=min(crystal_card.getCurrentValue(), lab_line_width_card_cap),
            purple_tube=purple_tube_value,
            bubonic_index=bubonic.character_index if bubonic else 0,
            motherboard_index=motherboard.index,
            motherboard_value=motherboard.base_value,
            arena=lab_arena_line_width
            * (breeding.arena_max_wave >= lab_arena_bonus_wave),
            shiny=sum(
                round(pet.shiny_level * lab_shiny_line_width_per_level)
                for pet in breeding.shiny_bonus_pets["Line Width in Lab"]
            ),
        )

    def _calculate_tubes(self, arctis_linked: dict[int, bool], souped_tubes: int):
        # "BonusLineWidth" in source. Last updated in v2.531.0
        lab_afk = [player.index for player in self.players if player.afk_in_lab]
        souped_slots = 2 * souped_tubes
        for player in self.players:
            arctis = arctis_linked.get(player.index, False)
            player.in_tube = player.afk_in_lab or arctis
            if player.afk_in_lab:
                player.souped = lab_afk.index(player.index) < souped_slots
            else:
                player.souped = arctis and player.index < souped_slots

    def _calculate_line_widths(self, widths: _LineWidthBonuses):
        sapphire_rhombol = self._jewels["Sapphire Rhombol"]
        bubonic = safer_index(self.players, widths.bubonic_index, None)
        for player in self.players:
            base = lab_base_line_width + lab_line_width_per_level * player.lab_level
            # Aura works even when the jewel is off
            if (
                sapphire_rhombol.owned
                and lab_distance(
                    player.x, player.y, sapphire_rhombol.x, sapphire_rhombol.y
                )
                < lab_sapphire_rhombol_aura_range
            ):
                base *= lab_sapphire_rhombol_aura_multi
            purple = widths.purple_tube if bubonic and player.x >= bubonic.x else 0
            motherboards = player.chips.count(widths.motherboard_index)
            player.line_width = floor(
                (base + widths.px_line + widths.card)
                * (
                    1
                    + (
                        purple
                        + widths.line_pct
                        + motherboards * widths.motherboard_value
                        + widths.arena
                        + lab_souped_tube_line_width * player.souped
                        + widths.shiny
                    )
                    / 100
                )
            )

    def _calculate_connections(self, flat_range: float):
        for node in [*self._bonuses.values(), *self._jewels.values()]:
            node.enabled = False
        # Range bonuses light up more nodes, so repeat until nothing changes
        lit = None
        while True:
            new_lit = self._connect(flat_range)
            if new_lit == lit:
                break
            lit = new_lit
            for bonus in self._bonuses.values():
                bonus.set_enabled(bonus.name in lit)
            for jewel in self._jewels.values():
                jewel.enabled = jewel.name in lit
        self._apply_jewel_multi()

    def _spelunker_multi(self) -> float:
        # "MainframeBonus"(8) in source. Last updated in v2.531.0
        spelunker = self._bonuses["Spelunker Obol"]
        if not spelunker.enabled:
            return spelunker.off_value
        navette = self._jewels["Pure Opal Navette"]
        return spelunker.base_value + navette.base_value / 100 * navette.enabled

    def _connection_range(self, fixed_range: int | None, flat_range: float) -> int:
        # "Dist","Bonus"/"Gem" in source. Last updated in v2.531.0
        if fixed_range is not None:
            return fixed_range
        pyrite_rhombol = self._jewels["Pyrite Rhombol"]
        viral = self._bonuses["Viral Connection"]
        range_pct = (
            pyrite_rhombol.base_value * self._spelunker_multi() * pyrite_rhombol.enabled
            + viral.base_value * viral.enabled
        )
        return floor(lab_base_connection_range * (1 + range_pct / 100) + flat_range)

    def _connect(self, flat_range: float) -> set[str]:
        tubes = [player for player in self.players if player.in_tube]
        # Only the first player in reach of the prism starts the chain
        first = next(
            (
                player
                for player in tubes
                if lab_distance(*lab_prism_coords, player.x, player.y)
                < player.line_width
            ),
            None,
        )
        self.connected_players = [first] if first else []
        nodes = [bonus for bonus in self._bonuses.values() if bonus.owned] + [
            jewel for jewel in self._jewels.values() if jewel.owned
        ]
        lit = set()
        for source in self.connected_players:
            for player in tubes:
                if (
                    player not in self.connected_players
                    and lab_distance(source.x, source.y, player.x, player.y)
                    < player.line_width
                ):
                    self.connected_players.append(player)
            for node in nodes:
                if lab_distance(
                    source.x, source.y, node.x, node.y
                ) < self._connection_range(node.fixed_range, flat_range):
                    lit.add(node.name)
        return lit

    def _apply_jewel_multi(self):
        spelunker = self._bonuses["Spelunker Obol"]
        spelunker.value = self._spelunker_multi()
        for jewel in self._jewels.values():
            # Navette's own value skips the multi
            multi = 1 if jewel.name == "Pure Opal Navette" else spelunker.value
            jewel.value = jewel.base_value * multi
