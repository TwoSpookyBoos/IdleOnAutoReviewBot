from consts.consts_w2 import sigils_dict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index

logger = get_logger(__name__)


class Sigil:
    def __init__(self, name: str, info: dict):
        self.name: str = name
        self.index: int = info["Index"]
        self.description: str = info["Description"]
        self.requirements: list = info["Requirements"]
        self.values: list = info["Values"]
        self.player_hours: float = 0.0
        # -1 not unlocked, 0 Blue, 1 Yellow, 2 Red; +1 applied on read so 0/1/2/3
        self.level: int = info["Level"]
        self.precharge_level: int = info["PrechargeLevel"]

    def calculate_precharge_level(self, has_ionized_sigils: bool):
        if self.level == 2:
            if has_ionized_sigils:
                # with Ionized Sigils the hours needed for Gold are already subtracted
                red_hours = self.requirements[2]
            else:
                # precharging Red before buying the upgrade needs Gold + Red hours
                red_hours = self.requirements[1] + self.requirements[2]
            self.precharge_level = 3 if self.player_hours >= red_hours else self.level
        elif self.level == 3:
            self.precharge_level = 3
        else:
            self.precharge_level = self.level


class Sigils(dict[str, Sigil]):
    def __init__(self, raw_sigils: list):
        super().__init__()
        for name, info in sigils_dict.items():
            sigil = Sigil(name, info)
            sigil.player_hours = safer_convert(
                safer_index(raw_sigils, sigil.index, 0), 0.0
            )
            sigil.level = (
                safer_convert(safer_index(raw_sigils, sigil.index + 1, -1), 0) + 1
            )
            self[name] = sigil

    def calculate_precharge_levels(self, has_ionized_sigils: bool):
        for sigil in self.values():
            sigil.calculate_precharge_level(has_ionized_sigils)


class AlchemyP2W:
    def __init__(self, raw_data: dict):
        raw_p2w = safe_loads(raw_data.get("CauldronP2W", []))
        raw_p2w = [v if isinstance(v, list) else [v] for v in raw_p2w]

        self.cauldrons: list = safer_index(raw_p2w, 0, [0] * 12)
        self.liquids: list = safer_index(raw_p2w, 1, [0] * 8)
        self.vials: list = safer_index(raw_p2w, 2, [0] * 2)
        self.player: list = safer_index(raw_p2w, 3, [0] * 2)
        self.sigils: Sigils = Sigils(safer_index(raw_p2w, 4, []))
