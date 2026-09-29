from consts.consts_w3 import max_trapping_critter_types
from consts.w3.trapping import (
    critter_unlock_quests,
    critters_by_unlock,
    emporium_critters_unlocked,
    nature_trapset_index,
    next_critters_by_unlock,
    trap_slots_by_level,
    trapset_level_requirements,
)
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)


class PlacedTrap:
    def __init__(self, raw_trap: list):
        self.placed: bool = raw_trap[0] != -1
        self.trapset: int = safer_index(raw_trap, 5, None)
        self.duration: int = safer_index(raw_trap, 6, None)
        self.exp_variant: int = safer_index(raw_trap, 7, None)


class Trapping:
    def __init__(self, raw_data: dict, character_count: int):
        self.placed_traps: dict[int, list[PlacedTrap]] = {}
        for index in range(character_count):
            try:
                raw_traps = safe_loads(raw_data[f"PldTraps_{index}"])
            except Exception:
                logger.exception(f"Unable to retrieve 'PldTraps_{index}'")
                raw_traps = []
            self.placed_traps[index] = [PlacedTrap(trap) for trap in raw_traps]
        self.unlocked_critters: int = 0
        self.highest_critter: str = "None"
        self.next_critter: str = "None"
        self.highest_wearable_trapset: int = 0
        # Per character index
        self.max_placeable_traps: list[int] = []
        self.unplaced_traps: dict[int, tuple[str, str]] = {}
        self.non_nature_traps: dict[int, int] = {}

    def calculate(
        self,
        *,
        characters,
        quests_by_character: list[dict[str, int]],
        emporium_new_critter: bool,
        call_me_ash_level: int,
    ):
        if emporium_new_critter:
            self.unlocked_critters = emporium_critters_unlocked
            self.highest_critter = "Tuttle"
            self.next_critter = "None"
        else:
            self._calculate_unlocked_critters(len(characters), quests_by_character)
        trapping_levels = characters.all_skills["Trapping"]
        best_level = max(trapping_levels, default=0)
        for index, requirement in enumerate(trapset_level_requirements):
            if best_level >= requirement:
                self.highest_wearable_trapset = index
        bonus_slot = int(call_me_ash_level >= 1)
        self.max_placeable_traps = [
            next(
                (
                    slots + bonus_slot
                    for req, slots in trap_slots_by_level
                    if level >= req
                ),
                0,
            )
            for level in trapping_levels
        ]
        for index, traps in self.placed_traps.items():
            placed = sum(trap.placed for trap in traps)
            if self.max_placeable_traps[index] - placed > 0:
                self.unplaced_traps[index] = (
                    str(placed),
                    str(self.max_placeable_traps[index]),
                )
        # Beginners past Nature Traps should only place those
        for jman in characters.jmans:
            if jman.trapping_level < trapset_level_requirements[nature_trapset_index]:
                continue
            for trap in self.placed_traps[jman.character_index]:
                if trap.placed and trap.trapset != nature_trapset_index:
                    self.non_nature_traps[jman.character_index] = (
                        self.non_nature_traps.get(jman.character_index, 0) + 1
                    )

    def _calculate_unlocked_critters(
        self, character_count: int, quests_by_character: list[dict[str, int]]
    ):
        highest = len(critters_by_unlock) - 1
        for index in range(character_count):
            quest_name = critter_unlock_quests[0][0]
            try:
                statuses = quests_by_character[index]
                for quest_index, (quest_name, required) in enumerate(
                    critter_unlock_quests
                ):
                    # Missing quests stop this character's scan
                    if statuses[quest_name] >= required and quest_index < highest:
                        highest = quest_index
            except Exception:
                logger.exception(
                    f"Could not retrieve {quest_name} status on Character{index}"
                )
        self.unlocked_critters = len(critters_by_unlock) - highest
        self.highest_critter = critters_by_unlock[highest]
        self.next_critter = next_critters_by_unlock[highest]

    @property
    def all_critters_unlocked(self) -> bool:
        return self.unlocked_critters == max_trapping_critter_types
