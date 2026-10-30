from functools import cached_property
from math import floor

from consts.w7.menagerie import menagerie_boosts, menagerie_missions, menagerie_unlocks
from models.w7.menagerie.boost import MenagerieBoost
from models.w7.menagerie.jellyfish import Jellyfishes
from models.w7.menagerie.mission import MenagerieMission
from models.w7.menagerie.unlock import MenagerieUnlock
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_get, safer_index

logger = get_logger(__name__)


class Menagerie:
    def __init__(self, raw_data: dict):
        raw_menagerie: list = safe_loads(raw_data.get("Menagerie", []))
        if not raw_menagerie:
            logger.warning("Menagerie data not present.")

        # TODO: not parsed yet: Lumi/hr ("LumiGainRate"), Scurge/Musselini
        #  (Menagerie[0][7..8], [5]), Omnijade (Menagerie[6], [7]), Nightmariner bonuses
        # "Menagerie"[0] in source
        misc = safer_index(raw_menagerie, 0, [])
        self.lumi: float = safer_convert(safer_index(misc, 0, 0), 0)
        self.shells: int = round(safer_convert(safer_index(misc, 1, 0), 0))
        self.rank: int = round(safer_convert(safer_index(misc, 2, 0), 0))
        self.shell_req: int = self._shell_req()
        self.visible_unlocks: int = self._unlock_slots(self.rank)
        self.visible_boosts: int = self._boost_slots(self.rank)
        # "Have_ban_k" in source
        # TODO: read from Gem Shop once ban_k is in its bundle list
        raw_bundles = safe_loads(raw_data.get("BundlesReceived", {}))
        self.has_bundle_k: int = int(safer_get(raw_bundles, "ban_k", 0) == 1)

        # "Menagerie"[1] in source: completions per mission
        raw_completions = safer_index(raw_menagerie, 1, [])
        self.missions: list[MenagerieMission] = [
            MenagerieMission(
                index,
                info,
                round(safer_convert(safer_index(raw_completions, index, 0), 0)),
                self,
            )
            for index, info in enumerate(menagerie_missions)
        ]
        # "Menagerie"[2] in source. "UnlockOwned" in source: owned at 1 or more
        raw_unlocks = safer_index(raw_menagerie, 2, [])
        self.unlocks: list[MenagerieUnlock] = [
            MenagerieUnlock(
                index,
                info,
                safer_convert(safer_index(raw_unlocks, index, 0), 0) >= 1,
                self,
            )
            for index, info in enumerate(menagerie_unlocks)
        ]
        # "Menagerie"[3] in source
        raw_boosts = safer_index(raw_menagerie, 3, [])
        self.boosts: list[MenagerieBoost] = [
            MenagerieBoost(
                index,
                info,
                round(safer_convert(safer_index(raw_boosts, index, 0), 0)),
                self,
            )
            for index, info in enumerate(menagerie_boosts)
        ]
        self.jellyfish: Jellyfishes = Jellyfishes(raw_menagerie, self)

    def _shell_req(self) -> int:
        # "ShellEXPreq" in source. Last updated in v2.550.0
        rank = self.rank
        return round(
            min(
                15,
                1
                + min(1, floor(rank / 3))
                + min(1, floor(rank / 1))
                + min(8, floor(max(0, rank - 5) / 5))
                + min(1, floor(rank / 8))
                + min(2, floor(rank / 22)),
            )
        )

    @staticmethod
    def _unlock_slots(rank: int) -> int:
        # "UpgUnlocked" 1 in source
        return round(min(7, rank) + floor(max(0, rank - 7) / 2))

    @staticmethod
    def _boost_slots(rank: int) -> int:
        # "UpgUnlocked" 2 in source
        return round(min(6, rank) + floor(max(0, rank - 6) / 2))

    def next_unlock_slot_rank(self) -> int | None:
        return self._next_slot_rank(self._unlock_slots, len(self.unlocks))

    def next_boost_slot_rank(self) -> int | None:
        return self._next_slot_rank(self._boost_slots, len(self.boosts))

    def _next_slot_rank(self, slots_at, total: int) -> int | None:
        if slots_at(self.rank) >= total:
            return None
        rank = self.rank + 1
        while slots_at(rank) <= slots_at(self.rank):
            rank += 1
        return rank

    @cached_property
    def visible_missions(self) -> int:
        # "UpgUnlocked" 0 in source
        from models.general.session_data import session_data

        account = session_data.account
        # "Grid_Bonus" 164 mode 1 in source: the grid square's raw level
        missionary_level = account.research.grid["Menagerie Missionary"].level
        emporium = account.sneaking.emporium["Menagerie Maxxing"].obtained
        return round(
            min(
                len(self.missions),
                1
                + self.boosts[0].value
                + missionary_level
                + int(emporium)
                + 3 * self.has_bundle_k,
            )
        )
