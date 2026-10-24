from consts.general.world_progress import world_reached_requirements
from models.general.achievements import Achievements
from models.w3.death_note import DeathNote
from utils.safer_data_handling import safe_loads, safer_get


class WorldProgress:
    def __init__(self, raw_data: dict):
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.optlacc_reached: dict[int, bool] = {
            world: safer_get(raw_optlacc, info["OptLaccIndex"], 0) > 0
            for world, info in world_reached_requirements.items()
            if info["OptLaccIndex"] is not None
        }
        self.highest_reached: int = 1

    def calculate(self, achievements: Achievements, death_note: DeathNote):
        self.highest_reached = next(
            (
                world
                for world, info in world_reached_requirements.items()
                if self.optlacc_reached.get(world, False)
                or (
                    info["Achievement"] is not None
                    and achievements[info["Achievement"]].complete
                )
                or death_note.worlds[world].maps_dict[info["FirstMap"]].kill_count > 0
            ),
            1,
        )
