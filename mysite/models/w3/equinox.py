from functools import cached_property

from consts.w3.equinox import (
    equinox_dreams,
    equinox_possible_dream_count,
    equinox_superbit_max_levels,
    equinox_unlock_dreams,
    equinox_upgrade_level_offset,
    equinox_upgrades,
)
from models.advice.advice import Advice
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class EquinoxDream:
    def __init__(self, info: dict, raw_progress):
        self.number: int = info['Number']
        self.display_name: str = info['Display Name']
        self.nightmare: bool = info['Nightmare']
        self.completed: bool = safer_convert(raw_progress, 0) == -1
        self.locked: bool = self.nightmare

    def get_advice(self) -> Advice:
        locked_text = " (unlock with {{ Research|#research }}: Equinox Nightmares)" if self.locked else ""
        return Advice(
            label=f"{self.display_name}{locked_text}",
            picture_class="ballot-32",
        )


class EquinoxDreams(dict[int, EquinoxDream]):
    def __init__(self, raw_weekly_boss: dict):
        super().__init__()
        for info in equinox_dreams:
            self[info['Number']] = EquinoxDream(info, raw_weekly_boss.get(f"d_{info['Number'] - 1}", 0))

    @cached_property
    def total_completed(self) -> int:
        return sum(dream.completed for dream in self.values())

    @cached_property
    def total_possible(self) -> int:
        return equinox_possible_dream_count

    @cached_property
    def remaining_unlock_dreams(self) -> list[EquinoxDream]:
        return [self[number] for number in equinox_unlock_dreams if not self[number].completed]

    @cached_property
    def upgrades_unlocked(self) -> int:
        # "UpgUnlocked" in source. Last updated in v2.528.0
        return 1 + len(equinox_unlock_dreams) - len(self.remaining_unlock_dreams)

    def get_advice(self) -> Advice:
        return Advice(
            label=f"Complete all {self.total_possible} possible Dreams",
            picture_class="equinox-mirror",
            progression=self.total_completed,
            goal=self.total_possible,
        )


class EquinoxUpgrade:
    def __init__(self, info: dict, level: int, dreams: EquinoxDreams):
        self.name: str = info['Name']
        self.level: int = level
        self.unlocked: bool = info['Unlock Order'] < dreams.upgrades_unlocked
        self.value_per_level: int = info['Value Per Level']
        increases: dict[int, int] = info['Max Level Increases']
        self.remaining_dreams: list[EquinoxDream] = [
            dreams[number] for number in increases if not dreams[number].completed
        ]
        self._max_level: int = info['Base Max Level'] + sum(
            amount for number, amount in increases.items() if dreams[number].completed
        )
        self._final_max_level: int = info['Final Max Level']
        self._summoning_expands: bool = info['Summoning Expands']
        self._superbit_expands: bool = info['Superbit Expands']
        self._bonus_max_levels: float = 0
        self._description: str = info['Description']
        self._image: str = info['Image']

    @property
    def max_level(self) -> int:
        return round(self._max_level + self._bonus_max_levels)

    @property
    def final_max_level(self) -> int:
        return round(self._final_max_level + self._bonus_max_levels)

    @property
    def value(self) -> int:
        return self.level * self.value_per_level

    @property
    def max_value(self) -> int:
        return self.final_max_level * self.value_per_level

    def calculate_max_level(self, summoning_max_levels: float, has_superbit: bool):
        self._bonus_max_levels = (
            summoning_max_levels * self._summoning_expands
            + equinox_superbit_max_levels * (self._superbit_expands and has_superbit)
        )

    def get_advice(self) -> Advice:
        remaining_text = ""
        if self.remaining_dreams:
            remaining_names = ', '.join(dream.display_name for dream in self.remaining_dreams)
            remaining_text = f" (Increase max level by completing {remaining_names})"
        return Advice(
            label=f"{self.name}{remaining_text}",
            picture_class=self._image,
            progression=self.level,
            goal=self.final_max_level,
        )

    def get_bonus_advice(self, additional_text: str = "") -> Advice:
        bonus = f"{round_and_trim(self.value)}/{round_and_trim(self.max_value)}"
        # Upgrades without a per level value have no bonus to describe
        description = f": {self._description.replace('{', bonus)}" if self._description else ""
        return Advice(
            label=f"{{{{ Equinox|#equinox }}}}: {self.name}{description}{additional_text}",
            picture_class=self._image,
            progression=self.level,
            goal=self.final_max_level,
        )

    def get_unlock_advice(self, additional_text: str = "") -> Advice:
        return Advice(
            label=f"{self.name}{additional_text}",
            picture_class=self._image,
        )


class EquinoxUpgrades(dict[str, EquinoxUpgrade]):
    def __init__(self, raw_dream: list, dreams: EquinoxDreams):
        super().__init__()
        for info in equinox_upgrades:
            raw_level = safer_index(raw_dream, info['Unlock Order'] + equinox_upgrade_level_offset, 0)
            self[info['Name']] = EquinoxUpgrade(info, safer_convert(raw_level, 0), dreams)


class Equinox:
    def __init__(self, raw_data: dict):
        self.unlocked: bool = False
        self.dreams: EquinoxDreams = EquinoxDreams(safe_loads(raw_data.get('WeeklyBoss', {})) or {})
        self.upgrades: EquinoxUpgrades = EquinoxUpgrades(safe_loads(raw_data.get('Dream', [])) or [], self.dreams)

    def calculate_unlocked(self, achievements: dict, nightmares_research_level: int):
        self.unlocked = achievements['Equinox Visitor']['Complete']
        for dream in self.dreams.values():
            dream.locked = dream.nightmare and nightmares_research_level < 1

    def calculate_max_levels(self, summoning_max_levels: float, has_superbit: bool):
        for upgrade in self.upgrades.values():
            upgrade.calculate_max_level(summoning_max_levels, has_superbit)
