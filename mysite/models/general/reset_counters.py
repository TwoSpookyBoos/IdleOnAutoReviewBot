from utils.safer_data_handling import safe_loads, safer_get


class ResetCounters:
    # Daily and weekly progress tracked in OptLacc
    def __init__(self, raw_data: dict):
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.minigame_plays_remaining: int = safer_get(raw_optlacc, 33, 0)
        self.particle_clicks_remaining: int = safer_get(raw_optlacc, 135, 0)
        self.weekly_boss_kills: int = safer_get(raw_optlacc, 189, 0)
        self.world_boss_kills: int = safer_get(raw_optlacc, 195, 0)
