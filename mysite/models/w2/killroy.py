from functools import cached_property
from math import ceil, floor

from consts.consts_w2 import killroy_dict
from consts.w2.killroy import skull_shop_bonuses
from models.advice.advice import Advice
from models.general.session_data import session_data
from models.w4.rift import RiftBonus
from utils.misc.next_break_point_tooltip import next_break_point_tooltip
from utils.safer_data_handling import safe_loads, safer_convert, safer_get
from utils.text_formatting import pl


class KillroyUpgrade:
    def __init__(self, name: str, info: dict, upgrades: int, total_fights: int):
        self.name: str = name
        self.upgrades: int = upgrades
        self.image: str = info["Image"]
        self.required_fights: int = info["Required Fights"]
        self.required_equinox: int = info["Required Equinox"]
        self.remaining: int = max(0, self.required_fights - total_fights)
        self.available: bool = False


class SkullShopBonus:
    def __init__(self, index: int, info: dict, purchases: int, billroy_autograph: bool):
        self.index = index
        # Slots 15+ are the shop's last row, it needs Billroy's autograph dialogue
        self._last_row: bool = info["Slot"] >= 15
        self._billroy_autograph = billroy_autograph
        self.name: str = info["Name"]
        self.image = f"killroy-skull-shop-{info['Slot']}"
        self._base: float = info["Base"]
        self._scale: float = info["Scale"]
        self._half_purchases: int = info["Half Purchases"]
        self._cost: int = info["Cost"]
        self.max_value = self._base + self._scale
        self.purchases = purchases
        # "KillroyBonuses" in source. Last updated in v2.561
        self.value = self._base + self._scale * (
            purchases / (self._half_purchases + purchases)
        )
        self._description: str = info["Description"]
        # Until two Gallery purchases succeed, each one is a 5% chance in source
        self._gallery_chance = index == 3 and purchases < 2
        if index == 3 and not self._gallery_chance:
            # Shop slot text in source after the first two Gallery purchases
            self._description = "Permanently boosts your Gallery Multiplier by +{x"

    @cached_property
    def _killroy_prime(self) -> RiftBonus:
        # Depends on: rift['KillroyPrime']
        return session_data.account.rift["KillroyPrime"]

    @cached_property
    def unlocked(self) -> bool:
        # "KillroyXtra" and "KillroyXtra2" in source. Last updated in v2.561
        return self._killroy_prime.unlocked and (
            not self._last_row or self._billroy_autograph
        )

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        if not self.unlocked:
            return self.get_unlock_advice(link_to_section)
        link = "{{ Killroy|#killroy }} - " if link_to_section else ""
        bonus = self._description.replace("{", self._format_number(self.value))
        purchases = f"{self.purchases:,} purchase{pl(self.purchases)}"
        tooltip = ""
        if self._gallery_chance:
            progression = self.purchases
            goal = 2
        else:
            progression = f"{self.value / self.max_value:.2%}"
            goal = "100%"
            if not link_to_section:
                tooltip = next_break_point_tooltip(
                    self.value,
                    self.max_value,
                    self._half_purchases,
                    self._format_bonus,
                    self._base,
                    format_level=self._format_purchases,
                )
        return Advice(
            label=f"{link}{self.name}: {bonus}<br>{purchases}",
            picture_class=self.image,
            progression=progression,
            goal=goal,
            resource="killroy-skull",
            progression_tooltip=tooltip,
        )

    def get_unlock_advice(self, link_to_section: bool = True) -> Advice:
        link = "{{ Killroy|#killroy }} - " if link_to_section else ""
        rift = self._killroy_prime
        if rift.unlocked:
            requirement = "Ask Billroy in W7 for an autograph"
            progression = 0
            goal = 1
        else:
            requirement = (
                f"Unlock {{{{ Rift|#rift }}}} #{rift.displayed_unlock_level}:"
                f" {rift.name}"
            )
            progression = session_data.account.rift.level
            goal = rift.level_required
        return Advice(
            label=f"{link}Skull Shop {self.name}: locked<br>{requirement}",
            picture_class=self.image,
            progression=progression,
            goal=goal,
        )

    def _format_number(self, value: float) -> str:
        # Shop slot text in source: floored for the first three, ceiled for the rest
        match self.index:
            case 0 | 1 | 2:
                return f"{floor(100 * value) / 100:g}"
            case 3:
                # The Gallery % is shown as x/100
                return f"{floor(value) / 100:g}"
            case _:
                return f"{ceil(100 * value) / 100:g}"

    def _format_bonus(self, value: float) -> str:
        unit = "%" if "{%" in self._description else "x"
        return f"{self._format_number(value)}{unit}"

    def _format_purchases(self, purchases: int) -> str:
        skulls = (purchases - self.purchases) * self._cost
        return f"{purchases:,} purchases ({skulls:,} more skulls)"


class SkullShop(dict[str, SkullShopBonus]):
    def __init__(self, raw_optlacc: dict):
        super().__init__()
        self.third_battle_unlocked: bool = safer_get(raw_optlacc, 227, 0) == 1
        # Billroy dialogue step in W7, 3 after the autograph one
        billroy_autograph = safer_get(raw_optlacc, 466, 0) >= 3
        for index, info in enumerate(skull_shop_bonuses):
            purchases = safer_get(raw_optlacc, info["Purchases Index"], 0)
            self[info["Name"]] = SkullShopBonus(
                index, info, purchases, billroy_autograph
            )


class Killroy(dict[str, KillroyUpgrade]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.total_fights: int = safer_get(raw_optlacc, 112, 0)
        self.skull_shop: SkullShop = SkullShop(raw_optlacc)
        # "PrimeKillroyTOT" in source: every KRbest entry that isn't a Summoning trial
        # ("SummzTrz"). Last updated in v2.550.0
        raw_kr_best = safe_loads(raw_data.get("KRbest", {}))
        self.prime_kills: int = round(
            sum(
                safer_convert(kills, 0)
                for key, kills in raw_kr_best.items()
                if "SummzTrz" not in key
            )
            if isinstance(raw_kr_best, dict)
            else 0
        )
        for name, info in killroy_dict.items():
            upgrades = safer_get(raw_optlacc, info["UpgradesIndex"], 0)
            self[name] = KillroyUpgrade(name, info, upgrades, self.total_fights)

    def calculate_available(self, shades_of_k_level: int):
        for upgrade in self.values():
            upgrade.available = (
                self.total_fights >= upgrade.required_fights or upgrade.upgrades > 0
            ) and shades_of_k_level >= upgrade.required_equinox
