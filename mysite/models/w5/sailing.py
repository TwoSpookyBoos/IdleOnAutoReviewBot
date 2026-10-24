from consts.consts_autoreview import ValueToMulti
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
from utils.number_formatting import parse_number, round_and_trim
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

    def calculate_speed(
        self,
        *,
        purrmep,
        goharut,
        bagur,
        characters: list,
        crawler_level: int,
        kattlekruk_level: int,
        boaty_bubble: float,
        big_p: float,
        ballot_buff,
        slab_count: int,
        slab_sovereignty,
        sailboat_stamp: float,
        boat_statue,
        popped_corn: float,
        oj_jooce: float,
        skill_mastery_unlocked: bool,
        total_sailing_level: int,
        msa_sailing: bool,
        total_worship_waves: int,
        c_shanti_unlocked: bool,
        davey_jones_owned: int,
        davey_jones_returns: float,
    ):
        # "BoatSpeed" in source. Last updated in v2.49 Dec 24 2025
        # Group A: Purrmep Minor Link, Cards, Bubble
        self._purrmep = purrmep
        self.purrmep_linked = next(
            (char for char in characters if char.divinity_link == "Purrmep"), None
        )
        self.purrmep_minor_bonus = 0
        if self.purrmep_linked is not None:
            level = self.purrmep_linked.divinity_level
            self.purrmep_minor_bonus = level / (60 + level) * big_p * 50
        self.speed_multi_a = round(
            1
            + (
                self.purrmep_minor_bonus
                + 4 * crawler_level
                + 6 * kattlekruk_level
                + boaty_bubble
            )
            / 125,
            2,
        )
        # Groups B and C: Goharut and Purrmep blessings
        self.goharut_bonus = 4 * goharut.blessing_level
        self.speed_multi_b = round(ValueToMulti(self.goharut_bonus), 2)
        self.purrmep_blessing_bonus = 3 * purrmep.blessing_level
        self.speed_multi_c = round(ValueToMulti(self.purrmep_blessing_bonus), 2)
        # Group D: Ballot
        self._ballot_buff = ballot_buff
        self.ballot_multi = ValueToMulti(ballot_buff.active * ballot_buff.value)
        self.speed_multi_d = round(self.ballot_multi, 2)
        # Group E: everything else
        self.bagur_bonus = 5 * bagur.blessing_level
        self.ad_tablet_level = self.artifacts["10 AD Tablet"].level
        sovereignty_multi = (
            ValueToMulti(slab_sovereignty.value) * slab_sovereignty.enabled
        )
        self.ad_tablet_bonus = (
            (4 * self.ad_tablet_level * ((slab_count - 500) // 10)) * sovereignty_multi
            if slab_count >= 500
            else 0
        )
        self._boat_statue = boat_statue
        self.skill_mastery_unlocked = skill_mastery_unlocked
        self.total_sailing_level = total_sailing_level
        self.msa_sailing = msa_sailing
        self.total_worship_waves = total_worship_waves
        self.c_shanti_unlocked = c_shanti_unlocked
        self.speed_multi_e = round(
            1
            + (
                self.bagur_bonus
                + self.ad_tablet_bonus
                + sailboat_stamp
                + (boat_statue.type != "Normal") * boat_statue.value
                + popped_corn
                + oj_jooce
                + skill_mastery_unlocked * (total_sailing_level > 200) * 15
                + msa_sailing * (total_worship_waves // 10)
                + c_shanti_unlocked * 20
            )
            / 125,
            2,
        )
        # Group F: Davey Jones. "DaveyJonesBonus" in source
        self.speed_multi_f = round_and_trim(
            ValueToMulti(50 * davey_jones_owned + davey_jones_returns)
        )
        self.speed_multi = round(
            self.speed_multi_a
            * self.speed_multi_b
            * self.speed_multi_c
            * self.speed_multi_d
            * self.speed_multi_e
            * self.speed_multi_f,
            2,
        )

    def get_speed_advice(self) -> Advice:
        return Advice(
            label=f"Total Sailing Speed bonus: {self.speed_multi}x",
            picture_class="sailing",
        )

    def get_purrmep_minor_advice(self) -> Advice:
        return Advice(
            label=f"Anyone Minor Linked to {self._purrmep.name}: "
            f"+{self.purrmep_minor_bonus:.2f}%",
            picture_class=self._purrmep.name,
            progression=int(self.purrmep_linked is not None),
            goal=1,
        )

    def get_ballot_advice(self) -> Advice:
        buff = self._ballot_buff
        return Advice(
            label=f"Weekly Ballot: {round(self.ballot_multi, 2)}x/"
            f"{round(buff.multi, 2)}x"
            f"<br>(Buff {'is Active' if buff.active else 'is Inactive'})",
            picture_class=buff.image,
            progression=int(buff.active),
            goal=1,
        )

    def get_ad_tablet_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Sailing|#sailing }}}}: Level {self.ad_tablet_level} "
            f"10 AD Tablet: +{self.ad_tablet_bonus}%",
            picture_class="10-ad-tablet",
            progression=self.ad_tablet_level,
            goal=max_sailing_artifact_level,
        )

    def get_boat_statue_advice(self) -> Advice:
        statue = self._boat_statue
        gold_note = "(must be at least gold)" if statue.type == "Normal" else ""
        return Advice(
            label=f"Level {statue.level} Boat Statue: "
            f"+{(statue.type != 'Normal') * statue.value:.2f}% {gold_note}",
            picture_class=statue.image,
        )

    def get_skill_mastery_advice(self) -> Advice:
        unlocked = self.skill_mastery_unlocked and self.total_sailing_level >= 200
        return Advice(
            label=f"{{{{ Rift|#rift }}}} - Sailing Skill Mastery > 200: "
            f"{'+15%' if unlocked else 'Locked.'}",
            picture_class="skill-mastery",
            progression=self.msa_sailing * self.total_sailing_level,
            goal=200,
        )

    def get_msa_advice(self, max_total_waves: int) -> Advice:
        return Advice(
            label=f"MSA Sailing: +{self.msa_sailing * self.total_worship_waves // 10}% "
            f"(+1% per 10 waves in Worship)",
            picture_class="worship",
            progression=self.total_worship_waves,
            goal=max_total_waves,
        )

    def get_c_shanti_advice(self) -> Advice:
        status = "+20% if equipped" if self.c_shanti_unlocked else "Locked."
        return Advice(
            label=f"{{{{ Star Signs|#star-signs }}}} - C. Shanti Minor: {status}",
            picture_class="c-shanti-minor",
            progression=int(self.c_shanti_unlocked),
            goal=1,
        )
