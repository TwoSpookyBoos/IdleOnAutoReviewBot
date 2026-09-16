from consts.consts_w2 import vials_dict, max_index_of_vials, max_vial_level, getReadableVialNames
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index
from utils.text_formatting import getItemDisplayName


logger = get_logger(__name__)


class Vial:
    def __init__(self, index: int, info: dict, level: int):
        self.index: int = index
        self.name: str = getReadableVialNames(index)
        self.short_name: str = info['Name']
        self.level: int = level
        self.material: str = info['Material']
        self.image: str = getItemDisplayName(info['Material'])
        self.base_value: float = lava_func(info['funcType'], level, info['x1'], info['x2'])
        self.value: float = self.base_value

    @property
    def maxed(self) -> bool:
        return self.level >= max_vial_level

    def calculate_value(self, total_multi: float):
        self.value = total_multi * self.base_value

    def get_advice(self, additional_text: str = '', include_material: bool = True,
                   goal_override: int | None = None, **kwargs) -> Advice:
        """Vial name and bonus, with progress toward max level."""
        kwargs.setdefault('picture_class', self.image)
        return Advice(
            label=f"{{{{ Vial|#vials }}}}: {self.name if include_material else self.short_name}: {additional_text}",
            progression=self.level,
            goal=max_vial_level if goal_override is None else goal_override,
            **kwargs
        )


class AlchemyVials(dict[str, Vial]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_cauldron_info = safe_loads(raw_data.get('CauldronInfo', [0, 0, 0, 0, {}]))
        raw_vials = safer_index(raw_cauldron_info, 4, {})
        if not isinstance(raw_vials, dict):
            raw_vials = {}
        raw_vials = {k: v for k, v in raw_vials.items() if k != 'length'}
        if len(raw_vials) < max_index_of_vials:
            logger.warning(f'Vials list shorter than expected by {max_index_of_vials - len(raw_vials)}')

        levels = {}
        for key, value in raw_vials.items():
            try:
                levels[int(key)] = int(value)
            except:
                logger.warning(f'Unable to normalize Vials level to int: {type(value)}: {value}. Replacing with 0.')
                levels[int(key)] = 0

        for index, info in vials_dict.items():
            self[getReadableVialNames(index)] = Vial(index, info, levels.get(index, 0))

        # multi sources, filled in by calculate_values
        self.mga: float = 0
        self.mgb: float = 0
        self.total_multi: float = 0

    @property
    def maxed_count(self) -> int:
        return sum(vial.maxed for vial in self.values())

    def calculate_values(self, vault, rift, lab_bonuses):
        self.mga = (
            vault.upgrades['Vial Overtune'].total_value
            + ((self.maxed_count * .02) if rift['VialMastery'].unlocked else 0)
        )
        self.mgb = lab_bonuses['My 1st Chemistry Set']['Value']
        self.total_multi = self.mga * self.mgb
        for vial in self.values():
            vial.calculate_value(self.total_multi)
