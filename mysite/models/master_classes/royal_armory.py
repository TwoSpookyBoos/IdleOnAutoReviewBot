from consts.consts_autoreview import ValueToMulti, EmojiType
from consts.consts_w1 import statues_dict
from consts.idleon.master_classes.royal_armory import (
    royal_armory_upgrades, royal_armory_upgrades_list,
    royal_armory_orblet_market_upgrades, royal_armory_orblet_market_glorification_index,
    royal_armory_statue_names, royal_armory_statue_unlock_odds_denom, royal_armory_statue_images,
    royal_armory_statue_marble_images,
    royal_armory_statue_bonus_names, royal_armory_statue_bonus_base, royal_armory_statue_bonus_increment,
    royal_armory_statue_flair_names, royal_armory_statue_flair_max_level,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index, safer_convert

logger = get_logger(__name__)


class RoyalArmoryUpgrade:
    def __init__(
        self, name: str, index: int, slot: int, image: str, level: int, cost_base: float, cost_increment: float,
        resource_index: int, resource_image: str, max_level: int, value_per_level: int,
        unlock_requirement: int, description: str
    ):
        self.name = name
        self.index = index
        self.slot = slot
        self.level = level
        self.image = image
        self.cost_base = cost_base
        self.cost_increment = cost_increment
        self.resource_index = resource_index
        self.resource_image = resource_image
        self.max_level = max_level
        self.value_per_level = value_per_level
        self.unlock_requirement = unlock_requirement
        self.description = description
        self.unlocked = False
        self.total_value = 0

    def calculate(self):
        if '{' in self.description:
            self.total_value = self.level * self.value_per_level
            self.description = self.description.replace('{', f"{self.total_value}")
        if '}' in self.description:
            self.total_value = ValueToMulti(self.level * self.value_per_level)
            self.description = self.description.replace('}', f"{self.total_value:.2f}")

    def get_advice(self, total_levels: int) -> Advice:
        return Advice(
            label=(
                f"{self.name}: {self.description}"
                f"<br>Requires {self.unlock_requirement - total_levels} more Upgrade Levels to unlock"
                if not self.unlocked else
                f"{self.name}: {self.description}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource=self.resource_image
        )


class RoyalStatue:
    # `RGshard`-unlocked "Royal Statue" - separate from the existing W1 Statues that Statue Flair boosts.
    def __init__(
        self, index: int, name: str, tier: int, unlock_odds_denom: int, image: str, marble_image: str,
        bonus_name: str | None, bonus_base: int, bonus_increment: int, royal_reverence_multi: float,
    ):
        self.index = index
        self.name = name
        self.tier = tier
        self.built = tier >= 1
        self.unlock_odds_denom = unlock_odds_denom
        self.image = image
        self.marble_image = marble_image
        self.bonus_name = bonus_name
        # `StatueBon` in source: only meaningful once built (tier >= 1), else it's a flat 0.
        self.bonus_value = (
            (bonus_base + bonus_increment * max(0, tier - 1)) * royal_reverence_multi if tier >= 1 else 0
        )

    def get_bonus_text(self) -> str:
        if self.bonus_name is None:
            return "Bonus unconfirmed"
        return f"{ValueToMulti(self.bonus_value):.2f}x {self.bonus_name}"

    def get_advice(self) -> Advice:
        if self.built:
            return Advice(
                label=f"{self.name}: Tier {self.tier}"
                      f"<br>{self.get_bonus_text()}",
                picture_class=self.image,
                progression=self.tier,
                goal=EmojiType.INFINITY.value,
                informational=True,
                resource='parchment-of-enchantment',
            )
        return Advice(
            label=f"{self.name}: Not built (1/{self.unlock_odds_denom})"
                  f"<br>{self.get_bonus_text()}",
            picture_class=self.image,
            progression=0,
            goal=1,
            resource=self.marble_image,
        )


class StatueFlair:
    # Spends Marble to boost the EXISTING W1 Statues, tracked in a separate levels array (`RoyalG[22]`).
    def __init__(self, index: int, statue_name: str, level: int, max_level: int):
        self.index = index
        self.statue_name = statue_name
        self.level = level
        self.max_level = max_level
        self.flair_name = royal_armory_statue_flair_names[min(level, len(royal_armory_statue_flair_names) - 1)]

    def get_advice(self, statue_image: str) -> Advice:
        # statue_image: session_data.account.statues[self.statue_name]['Image'] at the call site.
        return Advice(
            label=f"{self.statue_name} Flair: {self.flair_name}",
            picture_class=statue_image,
            progression=self.level,
            goal=self.max_level,
        )


class OrbletMarketUpgrade:
    def __init__(self, name: str, index: int, level: int, cost_base: int, cost_increment: float, max_level: int, value_per_level: int, description: str):
        self.name = name
        self.index = index
        self.level = level
        self.image = 'orblet'
        self.cost_base = cost_base
        self.cost_increment = cost_increment
        self.max_level = max_level
        self.value_per_level = value_per_level
        self.description = description
        self.unlocked = False
        self.total_value = 0

    def calculate(self):
        if '{' in self.description:
            self.total_value = self.level * self.value_per_level
            self.description = self.description.replace('{', f"{self.total_value}")
        if '}' in self.description:
            self.total_value = ValueToMulti(self.level * self.value_per_level)
            self.description = self.description.replace('}', f"{self.total_value:.2f}")

    def get_advice(self) -> Advice:
        return Advice(
            label=(
                f"{self.name}: {self.description}"
                if self.unlocked else
                f"{self.name}: {self.description}<br>Locked - level the previous slot first"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
        )


class RoyalArmory:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[str, RoyalArmoryUpgrade] = {}
        self.total_levels: int = 0

        raw_royalg = safe_loads(raw_data.get('RoyalG', []))
        if not raw_royalg:
            logger.warning("RoyalG data not present.")
        while len(raw_royalg) < 24:
            raw_royalg.append([])

        # Resource stockpile (`RoyalG[1]`), indexed by material.
        raw_resources = raw_royalg[1] if isinstance(raw_royalg[1], list) else []
        self.resources: dict[int, float] = {
            resource_index: safer_convert(safer_index(raw_resources, resource_index, 0), 0.0)
            for resource_index in range(len(raw_resources))
        }

        # Upgrades (`RoyalG[2]`, indexed by ArmoryUpg's own array index). Total sums ALL 83 real
        # entries, not just the 69 with a tree slot.
        raw_levels = raw_royalg[2] if isinstance(raw_royalg[2], list) else []
        self.total_levels = sum(
            int(safer_index(raw_levels, real_index, 0))
            for real_index in range(len(royal_armory_upgrades_list))
        )
        for upgrade in royal_armory_upgrades:
            level = min(upgrade["Max Level"], int(safer_index(raw_levels, upgrade["Index"], 0)))
            self.upgrades[upgrade["Name"]] = RoyalArmoryUpgrade(
                name=upgrade["Name"],
                index=upgrade["Index"],
                slot=upgrade["Slot"],
                image=upgrade["Image"],
                level=level,
                cost_base=upgrade["Cost Base"],
                cost_increment=upgrade["Cost Increment"],
                resource_index=upgrade["Resource Index"],
                resource_image=upgrade["Resource Image"],
                max_level=upgrade["Max Level"],
                value_per_level=upgrade["Value Per Level"],
                unlock_requirement=upgrade["Unlock Requirement"],
                description=upgrade["Description"],
            )
        # `unlock_requirement` is already the correct per-slot threshold (royal_armory_slot_unlock_thresholds).
        for upgrade in self.upgrades.values():
            upgrade.unlocked = self.total_levels >= upgrade.unlock_requirement

        # Royal Statues (`RoyalG[0]`). Their bonus scales with Royal Reverence, an upgrade parsed above.
        royal_reverence = self.upgrades.get('Royal Reverence')
        royal_reverence_multi = 1 + (
            (royal_reverence.level * royal_reverence.value_per_level) / 100 if royal_reverence else 0
        )
        raw_statues = raw_royalg[0] if isinstance(raw_royalg[0], list) else []
        self.statues: list[RoyalStatue] = [
            RoyalStatue(
                index=statue_index,
                name=royal_armory_statue_names[statue_index],
                tier=int(safer_index(raw_statues, statue_index, 0)),
                unlock_odds_denom=royal_armory_statue_unlock_odds_denom[statue_index],
                image=royal_armory_statue_images[statue_index],
                marble_image=royal_armory_statue_marble_images[statue_index],
                bonus_name=royal_armory_statue_bonus_names[statue_index],
                bonus_base=royal_armory_statue_bonus_base[statue_index],
                bonus_increment=royal_armory_statue_bonus_increment[statue_index],
                royal_reverence_multi=royal_reverence_multi,
            )
            for statue_index in range(len(royal_armory_statue_names))
        ]

        # Statue Flair (`RoyalG[22]`, boosts the existing W1 Statues - same 32-entry order as `StatueInfo`)
        raw_flairs = raw_royalg[22] if isinstance(raw_royalg[22], list) else []
        self.statue_flairs: list[StatueFlair] = [
            StatueFlair(
                index=statue_index,
                statue_name=statues_dict[statue_index]['Name'],
                level=min(royal_armory_statue_flair_max_level, int(safer_index(raw_flairs, statue_index, 0))),
                max_level=royal_armory_statue_flair_max_level,
            )
            for statue_index in statues_dict
        ]

        # Lil' Orblet Shop (`RoyalG[23]`) - sequential unlock, GLORIFICATION (idx 4) isn't a real level
        raw_orblet_market = raw_royalg[23] if isinstance(raw_royalg[23], list) else []
        self.orblet_market: dict[str, OrbletMarketUpgrade] = {}
        for slot in royal_armory_orblet_market_upgrades:
            level = min(slot["Max Level"], int(safer_index(raw_orblet_market, slot["Index"], 0)))
            self.orblet_market[slot["Name"]] = OrbletMarketUpgrade(
                name=slot["Name"],
                index=slot["Index"],
                level=level,
                cost_base=slot["Cost Base"],
                cost_increment=slot["Cost Increment"],
                max_level=slot["Max Level"],
                value_per_level=slot["Value Per Level"],
                description=slot["Description"],
            )
        for slot_upgrade in self.orblet_market.values():
            if slot_upgrade.index == royal_armory_orblet_market_glorification_index:
                slot_upgrade.unlocked = True  # not a real level - see model docstring / consts note
                continue
            previous_index = slot_upgrade.index - 1
            slot_upgrade.unlocked = slot_upgrade.index == 0 or any(
                s.index == previous_index and s.level >= 1 for s in self.orblet_market.values()
            )

        # Outposts (`RoyalMaps`) - a built row is 13 elements long, `[12]` the GLORIFICATION flag.
        # Only built/Glorified counted here - the full Outpost economy isn't modeled.
        raw_maps = safe_loads(raw_data.get('RoyalMaps', []))
        self.outposts_built = sum(1 for row in raw_maps if isinstance(row, list) and len(row) >= 3)
        self.outposts_glorified = sum(
            1 for row in raw_maps if isinstance(row, list) and len(row) >= 13 and safer_convert(row[12], 0) == 1
        )

    def calculate_upgrades(self):
        for upgrade in self.upgrades.values():
            upgrade.calculate()
        for slot_upgrade in self.orblet_market.values():
            slot_upgrade.calculate()

    def get_outposts_glorified_advice(self) -> Advice:
        return Advice(
            label=f"Outposts Glorified: {self.outposts_glorified}/{self.outposts_built}",
            picture_class='orblet',
            progression=self.outposts_glorified,
            goal=self.outposts_built,
        )
