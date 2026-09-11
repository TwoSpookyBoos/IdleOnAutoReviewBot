from consts.consts_w4 import rift_rewards_dict
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class RiftBonus:
    def __init__(self, level_required: int, info: dict, rift_level: int):
        self.level_required: int = level_required
        self.name: str = info['Name']
        self.shorthand: str = info['Shorthand']
        self._rift_level: int = rift_level
        self.unlocked: bool = rift_level >= level_required

    def get_advice(self, label: str = '') -> Advice:
        """Progress toward the rift level that unlocks this bonus."""
        return Advice(
            label=label or self.name,
            picture_class=self.name,
            progression=self._rift_level,
            goal=self.level_required,
        )

    def get_unlock_advice(self, label: str) -> Advice:
        """Binary have-it-or-not framing, for sections that only care that the bonus is live."""
        return Advice(
            label=label,
            picture_class=self.name,
            progression=int(self.unlocked),
            goal=1,
        )


class Rift(dict[str, RiftBonus]):
    """Rift bonuses keyed by shorthand name, e.g. 'SkillMastery'."""

    def __init__(self, raw_data: dict):
        super().__init__()
        self.level: int = safer_convert(safer_index(safe_loads(raw_data.get('Rift', [0])), 0, 0), 0)
        self.unlocked: bool = self.level > 0
        for level_required, info in rift_rewards_dict.items():
            self[info['Shorthand']] = RiftBonus(level_required, info, self.level)

    def calculate_unlocked(self, all_quests: list[dict]):
        # Reaching level 1 isn't the only way in: the Rift Ripper quest unlocks it too
        if not self.unlocked:
            self.unlocked = any(quests.get('Rift_Ripper1', 0) == 1 for quests in all_quests)

    def bonus_at_level(self, level: int) -> RiftBonus:
        """The bonus unlocked at this rift level, or a placeholder for levels that award nothing."""
        for bonus in self.values():
            if bonus.level_required == level:
                return bonus
        return RiftBonus(level, {'Name': f'UnknownRiftReward-{level}', 'Shorthand': ''}, self.level)
