from consts.consts_general import guild_bonuses_dict
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class GuildBonus:
    def __init__(self, name: str, info: dict, level: int):
        self.name: str = name
        self.level: int = level
        self.max_level: int = info['Max Level']
        self.image: str = info['Image']
        self.value: float = lava_func(info['funcType'], level, info['x1'], info['x2'])
        self.description: str = (
            info['Description']
            .replace('{', f"{self.value:.2f}")
            .replace('}', f"{100 - self.value:.2f}")
        )
        if name == 'Bonus GP for small guilds':
            self.description = self.description.replace(']', f"{10 + level}")

    def get_advice(self) -> Advice:
        return Advice(
            label=f"Guild Bonus - {self.name}:<br>{self.description}",
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
        )


class GuildBonuses(dict[str, GuildBonus]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_guild = safe_loads(raw_data.get('Guild', [[]]))
        raw_levels = safer_index(raw_guild, 0, [])
        for index, (name, info) in enumerate(guild_bonuses_dict.items()):
            level = safer_convert(safer_index(raw_levels, index, 0), 0)
            self[name] = GuildBonus(name, info, level)
