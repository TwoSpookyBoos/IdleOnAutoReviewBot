from consts.consts_w2 import killroy_dict
from utils.safer_data_handling import safe_loads, safer_get


class KillroyUpgrade:
    def __init__(self, name: str, info: dict, upgrades: int, total_fights: int):
        self.name: str = name
        self.upgrades: int = upgrades
        self.image: str = info["Image"]
        self.required_fights: int = info["Required Fights"]
        self.required_equinox: int = info["Required Equinox"]
        self.remaining: int = max(0, self.required_fights - total_fights)
        self.available: bool = False


class SkullShop:
    def __init__(self, raw_optlacc: dict):
        self.third_battle_unlocked: bool = safer_get(raw_optlacc, 227, 0) == 1
        self.artifact_purchases: int = safer_get(raw_optlacc, 228, 0)
        self.crop_purchases: int = safer_get(raw_optlacc, 229, 0)
        self.jade_purchases: int = safer_get(raw_optlacc, 230, 0)

    @staticmethod
    def _purchase_ratio(purchases: int) -> float:
        return purchases / (300 + purchases)

    @property
    def artifact_multi(self) -> float:
        return 1 + self._purchase_ratio(self.artifact_purchases)

    @property
    def crop_multi(self) -> float:
        return 1 + self._purchase_ratio(self.crop_purchases) * 9

    @property
    def next_crop_multi(self) -> float:
        return 1 + self._purchase_ratio(self.crop_purchases + 1) * 9

    @property
    def jade_multi(self) -> float:
        return 1 + self._purchase_ratio(self.jade_purchases) * 2


class Killroy(dict[str, KillroyUpgrade]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.total_fights: int = safer_get(raw_optlacc, 112, 0)
        self.skull_shop: SkullShop = SkullShop(raw_optlacc)
        for name, info in killroy_dict.items():
            upgrades = safer_get(raw_optlacc, info["UpgradesIndex"], 0)
            self[name] = KillroyUpgrade(name, info, upgrades, self.total_fights)

    def calculate_available(self, shades_of_k_level: int):
        for upgrade in self.values():
            upgrade.available = (
                self.total_fights >= upgrade.required_fights or upgrade.upgrades > 0
            ) and shades_of_k_level >= upgrade.required_equinox
