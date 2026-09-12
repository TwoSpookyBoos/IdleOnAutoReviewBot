from consts.consts_w4 import lab_chips_dict
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class LabChip:
    def __init__(self, index: int, info: dict, count: int):
        self.index: int = index
        self.name: str = info['Name']
        self.description: str = info['Description']
        self.effect: str = info['Effect']
        self.base_value: float = info['BaseValue']
        self.image: str = info['Image']
        self._advice_label: str = info['AdviceLabel']
        self.count: int = count

    @property
    def owned(self) -> bool:
        return self.count > 0

    def get_advice(self, additional_text: str = '') -> Advice:
        return Advice(
            label=f"{self._advice_label}{additional_text}",
            picture_class=self.image,
            progression=self.count,
            goal=1,
        )


class LabChips(dict[str, LabChip]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_lab = safe_loads(raw_data.get('Lab', []))
        raw_chips = safer_index(raw_lab, 15, [])
        for chip_index, info in lab_chips_dict.items():
            count = max(0, safer_convert(safer_index(raw_chips, chip_index, 0), 0))
            self[info['Name']] = LabChip(chip_index, info, count)
