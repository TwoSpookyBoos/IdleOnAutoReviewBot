from consts.consts_w5 import (
    artifact_tier_names,
    captain_buffs,
    max_sailing_artifact_level,
    sailing_artifacts_description_overrides,
    sailing_artifacts_dict,
    sailing_list,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.safer_data_handling import safe_loads, safer_convert, safer_index
from utils.text_formatting import kebab

logger = get_logger(__name__)


class Artifact:
    def __init__(self, index: int, info: dict, level: int):
        self.index: int = index
        self.name: str = info["Name"]
        self.level: int = level
        if level > max_sailing_artifact_level:
            logger.warning(
                f"{self.name} level {level} above max {max_sailing_artifact_level}"
            )
        self.island: str = info["Island"]
        self.image: str = kebab(self.name)
        self.description: str = sailing_artifacts_description_overrides.get(
            self.name, {}
        ).get(level, info["Description"])
        self.form: str | None = artifact_tier_names.get(level)
        self.form_bonus: str = info["FormBonuses"].get(level, "Unknown Bonus")

    def get_advice(
        self, include_island_name: bool = False, link_to_section: bool = True
    ) -> Advice:
        link_text = "{{ Artifact|#sailing }} - " if link_to_section else ""
        island_text = f"{self.island} - " if include_island_name else ""
        return Advice(
            label=f"{link_text}{island_text}{self.name}"
            f"<br>{self.description}"
            f"<br>{self.form} Bonus: {self.form_bonus}",
            picture_class=self.image,
            progression=self.level,
            goal=max_sailing_artifact_level,
        )


class Artifacts(dict[str, Artifact]):
    def __init__(self, raw_levels: list):
        super().__init__()
        for index, info in sailing_artifacts_dict.items():
            level = parse_number(safer_index(raw_levels, index, 0), 0)
            self[info["Name"]] = Artifact(index, info, level)

    @property
    def total_tiers(self) -> int:
        return sum(artifact.level for artifact in self.values())

    @property
    def found_count(self) -> int:
        return sum(artifact.level > 0 for artifact in self.values())

    @property
    def chilled_yarn_multi(self) -> int:
        # "ArtifactBonus" in source: base 1 x tier. Last updated in v2.531.0
        return 1 + self["Chilled Yarn"].level

    @property
    def max_chilled_yarn_multi(self) -> int:
        return 1 + max_sailing_artifact_level


class Island:
    def __init__(self, info: dict, unlocked: bool):
        self.name: str = info["Name"]
        self.unlocked: bool = unlocked
        self.distance: str = info["Distance"]
        self.normal_treasure: str = info["NormalTreasure"]
        self.rare_treasure: str = info["RareTreasure"]


class Boat:
    def __init__(self, raw_boat: list):
        self.captain: int = safer_convert(safer_index(raw_boat, 0, -1), -1)
        self.destination: int = safer_convert(safer_index(raw_boat, 1, -1), -1)
        self.loot_upgrades: int = safer_convert(safer_index(raw_boat, 3, 0), 0)
        self.speed_upgrades: int = safer_convert(safer_index(raw_boat, 5, 0), 0)

    @property
    def total_upgrades(self) -> int:
        return self.loot_upgrades + self.speed_upgrades


class Captain:
    def __init__(self, raw_captain: list):
        self.tier: int = safer_convert(safer_index(raw_captain, 0, 0), 0)
        self.top_buff: str = safer_index(
            captain_buffs, safer_index(raw_captain, 1, -1), "None"
        )
        self.bottom_buff: str = safer_index(
            captain_buffs, safer_index(raw_captain, 2, -1), "None"
        )
        self.level: int = safer_convert(safer_index(raw_captain, 3, 0), 0)
        self.top_buff_base_value: float = safer_convert(
            safer_index(raw_captain, 5, 0), 0.0
        )
        self.bottom_buff_base_value: float = safer_convert(
            safer_index(raw_captain, 6, 0), 0.0
        )


class Sailing:
    def __init__(self, raw_data: dict):
        # Some saves are double-encoded
        raw_sailing = safe_loads(safe_loads(raw_data.get("Sailing", [])))
        if not raw_sailing:
            logger.warning("Sailing data not present")
        raw_owned = safer_index(raw_sailing, 2, [])
        self.captains_owned: int = 1 + safer_convert(safer_index(raw_owned, 0, 0), 0)
        self.boats_owned: int = 1 + safer_convert(safer_index(raw_owned, 1, 0), 0)

        raw_islands = safer_index(raw_sailing, 0, [])
        self.islands: dict[str, Island] = {
            info["Name"]: Island(info, safer_index(raw_islands, index, 0) == -1)
            for index, info in enumerate(sailing_list)
        }
        self.artifacts: Artifacts = Artifacts(safer_index(raw_sailing, 3, []))

        raw_boats = safe_loads(safe_loads(raw_data.get("Boats", [])))
        self.boats: list[Boat] = [Boat(raw_boat) for raw_boat in raw_boats]
        raw_captains = safe_loads(safe_loads(raw_data.get("Captains", [])))
        self.captains: list[Captain] = [
            Captain(raw_captain) for raw_captain in raw_captains
        ]

    @property
    def islands_discovered(self) -> int:
        return sum(island.unlocked for island in self.islands.values())

    @property
    def max_boat_upgrades(self) -> int:
        return max((boat.total_upgrades for boat in self.boats), default=0)

    @property
    def max_captain_level(self) -> int:
        return max((captain.level for captain in self.captains), default=0)
