from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from models.general.session_data import session_data
from utils.safer_data_handling import safe_loads


class Slab(set[str]):
    """Item codenames registered in The Slab"""

    def __init__(self, raw_data: dict):
        super().__init__(safe_loads(raw_data.get("Cards1", [])))

    @cached_property
    def bonus_multi(self) -> float:
        # Last updated in v2.561.0
        # Depends on: lab_bonuses['Slab Sovereignty'],
        # lab_jewels['Pure Opal Rhinestone'], meritocracy[23],
        # legend_talents['+1 Slab'], vault.upgrades['Super Slab']
        account = session_data.account
        # 1. "MainframeBonus(15)" in source: the Slab Sovereignty lab bonus, 1x while
        # off. The Pure Opal Rhinestone jewel adds to it only while it is on
        sovereignty = account.lab_bonuses["Slab Sovereignty"]
        rhinestone = account.lab_jewels["Pure Opal Rhinestone"]
        sovereignty_multi = ValueToMulti(
            (sovereignty.value + rhinestone.active_value) * sovereignty.enabled
        )
        # 2. "SlabboBonus_AllMulti" in source
        all_multi = (
            ValueToMulti(account.meritocracy[23].value)
            * ValueToMulti(account.legend_talents["+1 Slab"].value)
            * account.vault.upgrades["Super Slab"].total_value
        )
        return sovereignty_multi * all_multi

    def bonus_steps(self, start: int, step: int) -> int:
        """Slab bonuses grow once per `step` items above `start`"""
        return max(0, len(self) - start) // step
