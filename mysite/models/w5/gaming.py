from consts.consts_w5 import gaming_superbits_dict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index

logger = get_logger(__name__)


class SuperBit:
    def __init__(self, name: str, info: dict, unlocked_codes: str):
        self.name: str = name
        self.bonus_text: str = info["BonusText"]
        self.unlocked: bool = info["CodeString"] in unlocked_codes


class Snail:
    def __init__(self, raw_snail: list):
        self.level: int = safer_index(raw_snail, 0, 0)
        self.rank: int = safer_index(raw_snail, 1, 0)
        self.encouragements: int = safer_index(raw_snail, 2, 0)


class Gaming:
    def __init__(self, raw_data: dict):
        raw_gaming = safe_loads(raw_data.get("Gaming", []))
        if not raw_gaming:
            logger.warning("Gaming data not present")
        # Sometimes float, sometimes string
        self.bits_owned: float = safer_convert(safer_index(raw_gaming, 0, 0.0), 0.0)
        self.fertilizer_value = 0
        self.fertilizer_speed = 0
        self.envelopes = 0
        unlocked_codes = ""
        if len(raw_gaming) >= 14:
            self.fertilizer_value = raw_gaming[1]
            self.fertilizer_speed = raw_gaming[2]
            unlocked_codes = str(raw_gaming[12])
            self.envelopes = raw_gaming[13]

        self.superbits: dict[str, SuperBit] = {
            name: SuperBit(name, info, unlocked_codes)
            for name, info in gaming_superbits_dict.items()
        }

        # [32] = Snail Import
        raw_sprouts = safe_loads(raw_data.get("GamingSprout", []))
        self.snail: Snail = Snail(safer_index(raw_sprouts, 32, []))
