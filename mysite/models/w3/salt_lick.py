from consts.idleon.w3.salt_lick import salt_lick_name_list, salt_lick_list
from utils.safer_data_handling import safe_loads, logger


class SaltLickUpgrade:
    def __init__(self, index: int, name: str, level: int, material: str):
        self.index = index
        self.name = name
        self.level = level
        self.material = material


class SaltLick:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[str, SaltLickUpgrade] = {}
        raw_saltlick_list = safe_loads(raw_data.get("SaltLick"))
        if not raw_saltlick_list:
            logger.warning("Salt Lick data not present.")
        for index, name in enumerate(salt_lick_name_list):
            try:
                level = int(raw_saltlick_list[index])
            except:
                level = 0
            self.upgrades[name] = SaltLickUpgrade(index, name, level, salt_lick_list[index]["material"])
