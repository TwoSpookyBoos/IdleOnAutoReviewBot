from consts.consts_w2 import bubbles_dict, max_implemented_bubble_index
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index
from utils.text_formatting import getItemDisplayName


logger = get_logger(__name__)


def parse_raw_cauldrons(raw_data: dict) -> list[dict[int, int]]:
    """Bubble levels per cauldron, as {bubble_index: level}. Shared by AlchemyBubbles and AlchemyCauldrons."""
    raw_cauldron_info = safe_loads(raw_data.get('CauldronInfo', [0, 0, 0, 0, {}]))
    cauldrons = []
    for cauldron_index in range(4):
        raw = safer_index(raw_cauldron_info, cauldron_index, {})
        if not isinstance(raw, dict):
            raw = {}
        levels = {}
        for key, value in raw.items():
            if key == 'length':
                continue
            try:
                levels[int(key)] = safer_convert(value, 0)
            except:
                continue
        if not levels:
            levels = {k: 0 for k in range(0, max_implemented_bubble_index + 1)}
        cauldrons.append(levels)
    return cauldrons


class Bubble:
    def __init__(self, cauldron_index: int, bubble_index: int, info: dict, level: int):
        self.cauldron_index: int = cauldron_index
        self.bubble_index: int = bubble_index
        self.name: str = info['Name']
        self.level: int = level
        self.material: str = getItemDisplayName(info['Material'])
        self.base_value: float = lava_func(info['funcType'], level, info['x1'], info['x2'])

    def get_advice(self, additional_text: str = '', **kwargs) -> Advice:
        kwargs.setdefault('picture_class', self.name)
        kwargs.setdefault('resource', self.material)
        return Advice(
            label=f"{self.name}{additional_text}",
            progression=self.level,
            **kwargs
        )

    def get_bonus_advice(self, additional_text: str = '', **kwargs) -> Advice:
        """Linked framing, for sections that only cite the bubble's bonus."""
        kwargs.setdefault('picture_class', self.name)
        kwargs.setdefault('resource', self.material)
        return Advice(
            label=f"{{{{ Alchemy Bubbles|#bubbles }}}} - {self.name}: {additional_text}",
            progression=self.level,
            **kwargs
        )


class AlchemyBubbles(dict[str, Bubble]):
    def __init__(self, raw_data: dict):
        super().__init__()
        cauldrons = parse_raw_cauldrons(raw_data)
        for cauldron_index, cauldron in bubbles_dict.items():
            for bubble_index, info in cauldron.items():
                if bubble_index > max_implemented_bubble_index:
                    continue  # don't waste time calculating unimplemented bubbles
                level = cauldrons[cauldron_index].get(bubble_index, 0)
                self[info['Name']] = Bubble(cauldron_index, bubble_index, info, level)
