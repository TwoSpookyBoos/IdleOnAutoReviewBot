from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property

from consts.consts_autoreview import ValueToMulti, MultiToValue
from consts.idleon.w6.summoning import (
    summoning_battle_per_color_dict,
    summoning_endless_battle_dict,
    summoning_enemy_per_color_dict,
    summoning_regular_battle_colors,
    summoning_reward_name,
    summoning_reward_template,
    summoning_stone_boss_base_damage,
    summoning_stone_boss_base_hp,
    summoning_upgrades,
)
from consts.consts_w5 import max_sailing_artifact_level
from consts.w6.summoning import (
    summoning_bonus_img,
    summoning_boss_info,
    summoning_not_multi_bonus_indexes,
    summoning_regular_match_colors,
    summoning_regular_reward_indexes,
    summoning_sanctuary_counts,
)
from consts.consts_monster_data import decode_monster_name

from models.advice.advice import Advice

from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, safer_get
from utils.text_formatting import notateNumber

logger = get_logger(__name__)


class SummoningUpgrade:
    def __init__(self, index: int, data: dict, level: int, is_doubled: bool):
        self.name = data["Name"]
        self.is_doubled = is_doubled
        self.level = level
        self.max_level = data["MaxLevel"]
        self._image = f"summoning-upgrade-{index}"
        self.color = summoning_regular_match_colors[data["ColorIndex"]]
        self.lock_by = summoning_upgrades[data["LockedBehindIndex"]]["Name"]
        self.unlocked = level > 0 or data["LockedBehindIndex"] < 0

    def get_bonus_advice(self) -> Advice:
        label = f"{self.name}"
        if not self.unlocked:
            label += f": Unlocked after 1 level into {self.lock_by}"
        return Advice(
            label=label,
            picture_class=self._image,
            progression=self.level,
            goal=self.max_level,
        )

    def get_doubler_advice(self) -> Advice:
        not_doubled = ""
        if not self.is_doubled:
            not_doubled = "Not "
        return Advice(
            label=f"{self.color}: {self.name}<br>{not_doubled}Doubled",
            picture_class=self._image,
            progression=int(self.is_doubled),
            goal=1,
        )


class SummoningBonus:
    def __init__(self, index: int, value: float):
        self.index = index
        self._reward_template = summoning_reward_template[index]
        self.name = summoning_reward_name[index]
        self.value = value
        self.max_value = value
        self.is_regular = index in summoning_regular_reward_indexes
        # "WinBonus" in source. Last update in v2.48 Giftmas Event
        # 3.5 * c.asNumber(a.engine.getGameAttribute("DNSM").h.SummWinBonus[0 | t])
        # Endless Summoning (20 <= t && 33 >= t) does NOT multiply by 3.5
        if self.is_regular:
            self.value *= 3.5
            self.max_value *= 3.5
        self._image = summoning_bonus_img.get(self.name, "placeholder")

    def set_endless_next_bonus(
        self, current_battle_number: int, next_battle_number: int
    ):
        self._endless_current = current_battle_number
        self._ensless_next = next_battle_number

    def get_bonus_display(self) -> str:
        value = f"{round_and_trim(self.as_multi)}"
        return self._reward_template.replace("+{", f"+{value}").replace("<", f"{value}")

    def _get_value_display(self, value: float) -> str:
        if self._reward_template.startswith("+{"):
            return f"{round_and_trim(value)}"
        else:
            return f"{round_and_trim(ValueToMulti(value))}"

    @cached_property
    def as_multi(self):
        if self._reward_template.startswith("+{"):
            return self.value
        else:
            return ValueToMulti(self.value)

    def calculate_bonus(self, multi: float, max_multi: float):
        if self.index in summoning_not_multi_bonus_indexes:
            return
        self.value *= multi
        self.max_value *= max_multi
        if self.name == "Library Max":
            self.value = round(self.value)
            self.max_value = round(self.max_value)

    def get_bonus_advice(
        self, link_to_section: bool = True, goal: int | None = None
    ) -> Advice:
        if self.is_regular:
            section = "Summoning Bonus"
            bonus_value = self._get_value_display(self.value)
            progress_value = bonus_value
            max_value = self._get_value_display(self.max_value)
        else:
            section = "Endless Summoning Bonus"
            bonus_value = round_and_trim(self.value)
            progress_value = self._endless_current
            max_value = self._ensless_next
        label = ""
        image = self._image
        if link_to_section:
            label += f"{{{{{section}|#summoning}}}}:<br>"
            image = "summoning" if self.is_regular else "endless-summoning"
        label += self.get_bonus_display()
        return Advice(
            label=label,
            picture_class=image,
            progression=progress_value,
            goal=max_value,
        )


class Battle:
    def __init__(self, index: int, info: dict, enemy_code: str = ""):
        self.number = index + 1
        self.enemy_code = info.get("EnemyID", enemy_code)
        self._enemy_name = decode_monster_name(self.enemy_code, False)
        self.bonus = SummoningBonus(info["RewardIndex"], info["RewardQTY"])
        self._opponent_name = info.get("OpponentName", None)
        self.is_win = False
        self._challenge = info.get("Challenge", None)

    def get_info_advice(self, current_battle_number: int) -> Advice:
        label = ""
        if self._opponent_name is not None:
            label += f"{self._opponent_name}<br>"
        if self._challenge is not None:
            label += f"{self._challenge}<br>"
        label += f"Reward: {self.bonus.get_bonus_display()}"
        return Advice(
            label=label,
            picture_class=self._enemy_name,
            progression=current_battle_number,
            goal=self.number,
            completed=current_battle_number >= self.number,
        )


class RegularBattles:
    def __init__(self, win_enemy_list: list):
        self.total_win = 0
        total_battle = 0
        self.win = {}
        self.battle: dict[str, list[Battle]] = {}
        for color, color_battle_list in summoning_battle_per_color_dict.items():
            if color not in summoning_regular_battle_colors:
                continue
            self.battle[color] = []
            self.win[color] = 0
            for battle_index, battle_info in enumerate(color_battle_list):
                battle = Battle(battle_index, battle_info)
                battle.is_win = battle.enemy_code in win_enemy_list
                self.battle[color].append(battle)
                self.win[color] += int(battle.is_win)
            total_battle += len(color_battle_list)
            self.total_win += self.win[color]
        self.all_win = self.total_win == total_battle

    def add_bonuses(self, bonuses: dict[str, SummoningBonus]):
        for battle_list in self.battle.values():
            for battle in battle_list:
                bonuses[battle.bonus.name].value += (
                    int(battle.is_win) * battle.bonus.value
                )
                bonuses[battle.bonus.name].max_value += battle.bonus.value


class EndlessBattles:
    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        self.total_win = safer_index(raw_optlacc, 319, 0)
        self.next_battle: list[Battle] = []
        # Next endless battle
        for index in range(self.total_win, max(40, self.total_win + 20)):
            enemy_index = min(4, index // 20)
            endless_battle_index = index % 40
            battle_info = summoning_endless_battle_dict[endless_battle_index]
            enemy_code = summoning_enemy_per_color_dict["Endless"][enemy_index]
            battle = Battle(index, battle_info, enemy_code)
            self.next_battle.append(battle)

    def get_bonus_next_battle(self, bonus_name: str) -> int:
        next_winner_bonus = 0
        endless_battles = self.next_battle
        while next_winner_bonus < len(self.next_battle):
            if endless_battles[next_winner_bonus].bonus.name == bonus_name:
                break
            next_winner_bonus += 1
        return self.total_win + next_winner_bonus + 1

    def add_bonuses(self, bonuses: dict[str, SummoningBonus]):
        # Won Endless battle
        for index in range(0, self.total_win):
            endless_battle_index = index % 40
            battle_info = summoning_endless_battle_dict[endless_battle_index]
            bonus_name = summoning_reward_name[battle_info["RewardIndex"]]
            bonuses[bonus_name].value += battle_info["RewardQTY"]


class SummoningBoss:
    def __init__(self, index: int, color: str, boss_info: dict, win_count: int):
        self._color = color
        self._base_hp = summoning_stone_boss_base_hp[index]
        self._base_damage = summoning_stone_boss_base_damage[index]
        self._win_count = win_count
        self._enemy_code = boss_info["EnemyID"]
        self._enemy_name = decode_monster_name(self._enemy_code, False)
        self._stone_image = f"{color}-summoning-stone"
        self._location = boss_info["Location"]
        self._name = boss_info["Name"]

    def hp(self) -> Decimal:
        return Decimal(2.0) * self._base_hp * (4000**self._win_count)

    def damage(self) -> Decimal:
        return Decimal(0.8) * self._base_damage * (4000**self._win_count)

    def get_info_advice(self) -> Advice:
        return Advice(
            label=(
                f"{self._name} ({self._location})"
                f"<br>{self._win_count} wins: {self._win_count + 1}x multi"
                f" to {self._color} upgrades"
                f"<br>DMG: {notateNumber('Basic', self.damage())}"
                f"<br>HP: {notateNumber('Basic', self.hp())}"
            ),
            picture_class=self._stone_image,
            resource=self._enemy_name,
        )


@dataclass
class SummoningDoubler:
    own: int = 0
    spent: int = 0
    spentable: int = 0


class Summoning:
    def __init__(self, raw_data: dict):
        raw_summoning_list = safe_loads(raw_data.get("Summon", []))
        if not raw_summoning_list:
            logger.warning("Summoning data not present.")
        if len(raw_summoning_list) < 5:
            raw_summoning_list.exted([[]] * (5 - len(raw_summoning_list)))
        self.upgrades: dict[str, SummoningUpgrade] = {}
        self._parse_upgrade(raw_data, safer_index(raw_summoning_list, 0, []))
        enemy_list = [
            safer_convert(v, "") for v in safer_index(raw_summoning_list, 1, [])
        ]
        self.bonuses: dict[str, SummoningBonus] = {}
        for index, _ in enumerate(summoning_reward_template[1:], start=1):
            bonus = SummoningBonus(index, 0)
            self.bonuses[bonus.name] = bonus
        self.regular: RegularBattles = RegularBattles(enemy_list)
        self.regular.add_bonuses(self.bonuses)
        self.endless: EndlessBattles = EndlessBattles(raw_data)
        self.endless.add_bonuses(self.bonuses)
        for name, bonus in self.bonuses.items():
            if bonus.is_regular:
                continue
            bonus.set_endless_next_bonus(
                self.endless.total_win, self.endless.get_bonus_next_battle(name)
            )
        self._parse_sanctuary(safer_index(raw_summoning_list, 4, []))
        self.bosses: dict[str, SummoningBoss] = {}
        self._parse_bosses(raw_data)

    def _parse_upgrade(self, raw_data: dict, raw_upgrades: list[int]):
        # Summoning Upgrade doublers
        raw_caverns_list = safe_loads(raw_data.get("Holes", []))
        self.doubler = SummoningDoubler()
        try:
            raw_doubled_upgrades = [
                int(entry) for entry in raw_caverns_list[28] if int(entry) >= 0
            ]
            self.doubler.spentable = len(raw_caverns_list[28])
        except:
            logger.exception("Can't parse doubler list: raw_data->Holes[28]")
            raw_doubled_upgrades = []
            self.doubler.spentable = 30
        self.doubler.spent = len(raw_doubled_upgrades)
        for index, data in enumerate(summoning_upgrades):
            is_doubled = index in raw_doubled_upgrades
            level = safer_index(raw_upgrades, index, 0)
            upgrade = SummoningUpgrade(index, data, level, is_doubled)
            self.upgrades[upgrade.name] = upgrade
        for upgrade in self.upgrades.values():
            if upgrade.unlocked:
                continue
            upgrade.unlocked = self.upgrades[upgrade.lock_by].level >= 1

    def _parse_sanctuary(self, raw_sanctuary: list[int]):
        total = 0
        for index, count in enumerate(raw_sanctuary):
            total += raw_sanctuary[index] * summoning_sanctuary_counts[index]
        self.sanctuary_count = total

    def _parse_bosses(self, raw_data: dict):
        raw_kr_best = safe_loads(raw_data.get("KRbest", {}))
        for color_index, color in enumerate(summoning_regular_battle_colors):
            if color == "Teal":
                # Not implemented yet
                continue
            win_count = safer_get(raw_kr_best, f"SummzTrz{color_index}", 0)
            boss_info = summoning_boss_info[color]
            self.bosses[color] = SummoningBoss(color_index, color, boss_info, win_count)

    def calculate_winner_bonus_multi(self, account: "Account"):
        # "WinBonus" in source. Last update in v2.48 Giftmas Event
        # The 'base' value of a normal match is multiplied by 3.5. This is
        # handled by SummoningBonus itself, not part of this function.
        # Multi Group A: Pristine Charm - Crystal Comb
        max_mga = 1.3
        player_mga = ValueToMulti(
            account.sneaking.pristine_charms["Crystal Comb"].value
        )
        # Multi Group B: Gem Shop - King of all Winners
        max_mgb = ValueToMulti(
            10 * account.gemshop["Purchases"]["King Of All Winners"]["MaxLevel"]
        )
        player_mgb = ValueToMulti(
            10 * account.gemshop["Purchases"]["King Of All Winners"]["Owned"]
        )
        # Multi Group C: Summoning Winner Bonuses
        max_mgc_rest = ValueToMulti(
            (25 * max_sailing_artifact_level)
            + account.merits[5][4]["MaxLevel"]  # World 6 Merit Shop
            + 1  # int(account.achievements['Spectre Stars'])
            + 1  # int(account.achievements['Regalis My Beloved'])
            + MultiToValue(account.armor_sets["Sets"]["GODSHARD SET"]["Total Value"])
            # Not for Library
            + self.bonuses["Winner Bonuses"].value
            + account.emperor["Summoning Winner Bonuses"].value  # Technically infinity
        )
        max_mgc_library = ValueToMulti(
            # 19 == t ? Library bonus's index
            (25 * max_sailing_artifact_level)
            + account.merits[5][4]["MaxLevel"]  # World 6 Merit Shop
            + 1  # int(account.achievements['Spectre Stars'])
            + 1  # int(account.achievements['Regalis My Beloved'])
            + 15  # max value of account.armor_sets['Sets']['GODSHARD SET']
        )
        player_mgc_rest = ValueToMulti(
            (25 * account.sailing["Artifacts"]["The Winz Lantern"]["Level"])
            + account.merits[5][4]["Level"]
            + int(account.achievements["Spectre Stars"]["Complete"])
            + int(account.achievements["Regalis My Beloved"]["Complete"])
            + MultiToValue(account.armor_sets["Sets"]["GODSHARD SET"]["Total Value"])
            # Not for library
            + self.bonuses["Winner Bonuses"].value
            + account.emperor["Summoning Winner Bonuses"].value
        )
        player_mgc_library = ValueToMulti(
            (25 * account.sailing["Artifacts"]["The Winz Lantern"]["Level"])
            + account.merits[5][4]["Level"]
            + int(account.achievements["Spectre Stars"]["Complete"])
            + int(account.achievements["Regalis My Beloved"]["Complete"])
            + MultiToValue(account.armor_sets["Sets"]["GODSHARD SET"]["Total Value"])
        )
        self.multi = {}
        # Library
        self.multi["Library"] = {}
        self.multi["Library"]["Value"] = max(
            1, player_mga * player_mgb * player_mgc_library
        )
        self.multi["Library"]["Max"] = max(1, max_mga * max_mgb * max_mgc_library)
        # Not Library
        self.multi["Bonuses"] = {}
        self.multi["Bonuses"]["Value"] = max(
            1, player_mga * player_mgb * player_mgc_rest
        )
        self.multi["Bonuses"]["Group"] = (
            (player_mga, player_mgb, player_mgc_rest),
            (max_mga, max_mgb, max_mgc_rest),
        )

    def calculate_bonuses(self):
        for name, bonus in self.bonuses.items():
            multi = self.multi["Bonuses"]["Value"]
            max_multi = multi
            if name == "Library Max":
                multi = self.multi["Library"]["Value"]
                max_multi = self.multi["Library"]["Max"]
            bonus.calculate_bonus(multi, max_multi)

    def calculate_doublers(self, account: "Account"):
        self.doubler.own = (
            account.caverns["Caverns"]["Gambit"]["Bonuses"][0]["Value"]
            + 10 * account.event_points_shop["Bonuses"]["Summoning Star"]["Owned"]
        )
        self.doubler.spentable = min(self.doubler.spentable, self.doubler.own)

    def get_doubler_spent_advice(self) -> Advice:
        return Advice(
            label=f"{self.doubler.spent}/{self.doubler.spentable} total doublers spent",
            picture_class="summoning",
            progression=self.doubler.spent,
            goal=self.doubler.spentable,
        )

    def get_doubler_alert(self) -> Advice | None:
        available = self.doubler.spentable - self.doubler.spent
        if available <= 0:
            return None
        return Advice(
            label=f"{available} available {{{{Summoning|#summoning}}}} Upgrade doublers",
            picture_class="summoning",
        )
