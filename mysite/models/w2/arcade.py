from functools import cached_property

from consts.consts_w2 import arcade_bonuses, arcade_max_level
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


logger = get_logger(__name__)


class ArcadeUpgrade:
    def __init__(self, index: int, info: dict, level: int):
        self.index: int = index
        self.level: int = level
        self.stat: str = info['Stat']
        self.image: str = info['Image']
        self.max_value: float = info['MaxValue']
        self._display_type: str = info['displayType']
        self.cosmic: bool = level >= arcade_max_level
        self._base_value: float = lava_func(
            info['funcType'], min(arcade_max_level, level), info['x1'], info['x2']
        )
        self.value: float = self._base_value

    @cached_property
    def material(self) -> str:
        if self.level == arcade_max_level:
            return ''
        return 'arcade-cosmic-ball' if self.level == arcade_max_level - 1 else 'arcade-gold-ball'

    def calculate_value(self, has_reindeer: bool):
        self.value = self._base_value * max(1, 2 * self.cosmic) * max(1, 2 * has_reindeer)

    def get_advice(self, link_to_section: bool = True) -> Advice:
        label = '{{Arcade|#arcade}} ' if link_to_section else ''
        label += f"Bonus {self.index}: +{round_and_trim(self.value)}"
        if self.level < arcade_max_level:
            label += f"/{round_and_trim(self.max_value)}"
        label += f"{self._display_type} {self.stat}"
        return Advice(
            label=label,
            picture_class=self.image,
            progression=self.level,
            goal=arcade_max_level,
            resource=self.material,
        )


class Arcade(dict[int, ArcadeUpgrade]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = safe_loads(raw_data.get('OptLacc', []))
        self.currency: dict[str, int] = {
            # convert: displayed with thousands separators
            name: safer_convert(safer_index(raw_optlacc, index, 0), 0)
            for name, index in (('Balls', 74), ('Gold Balls', 75), ('Cosmic Balls', 324))
        }
        raw_upgrades = safe_loads(raw_data.get('ArcadeUpg', []))
        for index, info in arcade_bonuses.items():
            level = safer_convert(safer_index(raw_upgrades, index, 0), 0)
            self[index] = ArcadeUpgrade(index, info, level)

    def calculate_values(self, companions):
        has_reindeer = companions.has('Spirit Reindeer')
        for upgrade in self.values():
            upgrade.calculate_value(has_reindeer)

    def get_currency_advice(self) -> list[Advice]:
        return [
            Advice(
                label=f"{name} owned: {amount:,}",
                picture_class=f'arcade-{name[:-1]}',
                completed=True,
                informational=True,
            ) for name, amount in self.currency.items()
        ]
