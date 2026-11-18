from functools import cached_property
from math import prod

from consts.consts_autoreview import ValueToMulti
from consts.consts_w2 import max_NBLB
from consts.consts_w5 import (
    artifact_tier_names,
    captain_buffs,
    max_sailing_artifact_level,
    sailing_artifacts_description_overrides,
    sailing_artifacts_dict,
    sailing_list,
)
from models.advice.advice import Advice
from models.general.session_data import session_data
from models.w1.star_signs import get_infinite_star_sign_levels
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
        self._base_value: int | float = info["BaseValue"]
        self._form_bonuses: dict[int, str] = info["FormBonuses"]
        self._form_values: dict[int, int | float] = info["Values"]

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

    @property
    def value(self) -> int | float:
        return self._value_at(self.level)

    @property
    def max_value(self) -> int | float:
        return self._value_at(max_sailing_artifact_level)

    @property
    def as_multi(self) -> float:
        return self._multi(self.value)

    @property
    def max_multi(self) -> float:
        return self._multi(self.max_value)

    def _value_at(self, level: int) -> int | float:
        # "ArtifactBonus" in source. Last updated in v2.561.0
        # The effective bonus: the main one, `ArtifactBonus(index, 0)`, is combined
        # with the form's own one, `ArtifactBonus(index, 1)`, as their readers do
        if level == 0:
            return 0
        value = self._base_value
        # Forms either multiply the main bonus by the tier or add a bonus of their own
        if self._form_bonuses[level].startswith("The artifact's main bonus is"):
            value *= level
        form_value = self._form_values[level]
        match self.index:
            case 0:  # Moai Head: shrine level up speed, %. Shrines apply everywhere
                return form_value
            case 4:  # Gold Relic: 3D Printer sample growth, % per day: 2 + form
                return 2 + form_value
            case 12:  # Amberite: No Bubble Left Behind bubbles: 1 + form
                return value + form_value
            case 16:  # Chilled Yarn: read as `1 + value` in source, kept as % here
                return 100 * value
            case 1 | 3 | 5 | 8 | 11 | 13 | 23 | 25 | 27 | 29:
                # Scaled by other systems in source, not modelled yet
                return 0
            case _:
                return value

    def _multi(self, value: int | float) -> float:
        match self.index:
            case 30:  # The Onyx Lantern: on top of the base 2x of Onyx statues
                return ValueToMulti(100 + value)
            case _:
                return ValueToMulti(value)

    def get_bonus_advice(self, note: str = "", link_to_section: bool = True) -> Advice:
        link_text = "{{ Artifact|#sailing }} - " if link_to_section else ""
        note_text = f"<br>{note}" if note else ""
        goal = max_sailing_artifact_level
        match self.index:
            case 0:  # Moai Head: the main bonus is unlocked by the first tier
                bonus = "Shrines apply everywhere"
                goal = 1
            case 16 | 30 | 35:
                multi = round_and_trim(self.as_multi)
                max_multi = round_and_trim(self.max_multi)
                bonus = f"{multi}/{max_multi}x"
            case 12 | 17 | 21:
                value = round_and_trim(self.value)
                max_value = round_and_trim(self.max_value)
                bonus = f"+{value}/{max_value}"
            case _:
                value = round_and_trim(self.value)
                max_value = round_and_trim(self.max_value)
                bonus = f"+{value}/{max_value}%"
        return Advice(
            label=f"{link_text}{self.name}: {bonus}{note_text}",
            picture_class=self.image,
            progression=self.level,
            goal=goal,
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

    @cached_property
    def unlocked_artifact_tier(self) -> int:
        """Highest artifact tier that can be found on the account"""
        account = session_data.account
        # Tiers 3 and up, each one needs the previous
        tier_unlocks = [
            account.rift["EldritchArtifact"].unlocked,
            account.sneaking.emporium["Sovereign Artifacts"].obtained,
            account.spelunk.caves["Pebble Cove"].bonus_obtained,
            account.research.grid["Transcendent Artifacts"].level >= 1,
            # "VerisimilitudeUnlocked" in source: the first Menagerie unlock
            account.menagerie.unlocks[0].owned,
        ]
        return 2 + next(
            (index for index, unlocked in enumerate(tier_unlocks) if not unlocked),
            len(tier_unlocks),
        )

    def get_artifact_tier_unlock_advice(self) -> Advice:
        match self.unlocked_artifact_tier + 1:
            case 3:
                label = (
                    "Unlock Eldritch tier Artifacts by completing {{ Rift|#rift }} 30"
                )
                picture_class = "eldritch-artifact"
            case 4:
                label = (
                    'Purchase "Sovereign Artifacts" from the '
                    "{{ Jade Emporium|#sneaking }} in W6"
                )
                picture_class = "sovereign-artifacts"
            case 5:
                label = (
                    "Unlock Omnipotent tier Artifacts from the first "
                    "{{ Spelunking|#spelunking }} cave, Pebble Cove"
                )
                picture_class = "spelunking"
            case 6:
                label = (
                    'Unlock "Transcendent Artifacts" in the '
                    "{{ Research|#research }} Grid"
                )
                picture_class = "research"
            case _:
                label = "Unlock Verisimilitude tier Artifacts in the Luminous Menagerie"
                picture_class = "sailing"
        return Advice(
            label=label,
            picture_class=picture_class,
            progression=0,
            goal=1,
        )

    @property
    def islands_discovered(self) -> int:
        return sum(island.unlocked for island in self.islands.values())

    @property
    def max_boat_upgrades(self) -> int:
        return max((boat.total_upgrades for boat in self.boats), default=0)

    @property
    def max_captain_level(self) -> int:
        return max((captain.level for captain in self.captains), default=0)

    @cached_property
    def _ad_tablet_bonus(self) -> int | float:
        # Depends on: slab, lab_bonuses['Slab Sovereignty']
        account = session_data.account
        slab_count = len(account.slab)
        slab_sovereignty = account.lab_bonuses["Slab Sovereignty"]
        sovereignty_multi = (
            ValueToMulti(slab_sovereignty.value) * slab_sovereignty.enabled
        )
        return (
            (self.artifacts["10 AD Tablet"].value * ((slab_count - 500) // 10))
            * sovereignty_multi
            if slab_count >= 500
            else 0
        )

    @cached_property
    def _skill_mastery_bonus(self) -> int:
        # "RiftSkillBonus,12" in source: Sailing rank above 1 is 200+ total levels
        # Depends on: rift['SkillMastery'], characters
        account = session_data.account
        total_sailing_level = sum(account.characters.all_skills["Sailing"])
        unlocked = account.rift["SkillMastery"].unlocked
        return 17 * (unlocked and total_sailing_level >= 200)

    @cached_property
    def _c_shanti_bonus(self) -> float:
        # `StarSigns["63"]` in source is for the logged in character: the best one
        # Depends on: star_signs, breeding, characters
        account = session_data.account
        infinite_levels = get_infinite_star_sign_levels(
            account.breeding.total_shiny_bonus_values["Infinite Star Signs"]
        )
        c_shanti = account.star_signs["C. Shanti Minor"]
        seraph_multi = account.star_signs.seraph_multi
        return max(
            (
                c_shanti.value_for(char, 20, infinite_levels, seraph_multi)
                for char in account.characters.safe
            ),
            default=0,
        )

    @cached_property
    def _speed_multis(self) -> dict[str, float]:
        # "BoatSpeed" in source. Last updated in v2.561.0
        # Not modelled yet: the per boat part of "DaveyJonesBonus"
        # Depends on: divinity, cards, alchemy_bubbles['Boaty Bubble'], ballot[24],
        # stamps['Sailboat Stamp'], statues['Boat Statue'], meals['Popped Corn'],
        # alchemy_vials['Oj Jooce (Orange Slice)'], gaming.superbits['MSA Sailing'],
        # worship, vault.upgrades['Speedy Sailing'],
        # gemshop.purchases['Davey Jones Training'],
        # legend_talents['Davey Jones Returns']
        account = session_data.account
        divinity = account.divinity
        msa_sailing = account.gaming.superbits["MSA Sailing"].unlocked
        total_worship_waves = account.worship.total_waves
        davey_jones_owned = account.gemshop.purchases["Davey Jones Training"].owned
        davey_jones_returns = account.legend_talents["Davey Jones Returns"].value
        return {
            "A": 1
            + (
                divinity.named("Purrmep").minor.value
                + 4 * account.cards.named("Crawler").level
                + 6 * account.cards.named("Kattlekruk").level
                + account.alchemy_bubbles["Boaty Bubble"].base_value
            )
            / 125,
            "B": ValueToMulti(divinity.named("Goharut").blessing.value),
            "C": ValueToMulti(divinity.named("Purrmep").blessing.value),
            "D": account.ballot[24].active_multi,
            "E": 1
            + (
                divinity.named("Bagur").blessing.value
                + self._ad_tablet_bonus
                + account.stamps["Sailboat Stamp"].total_value
                + account.statues["Boat Statue"].value
                + account.meals["Popped Corn"].value
                + account.alchemy_vials["Oj Jooce (Orange Slice)"].value
                + self._skill_mastery_bonus
                + msa_sailing * (total_worship_waves // 10)
                + self._c_shanti_bonus
                + account.vault.upgrades["Speedy Sailing"].total_value
            )
            / 125,
            # "DaveyJonesBonus" in source
            "F": ValueToMulti(50 * davey_jones_owned + davey_jones_returns),
        }

    @cached_property
    def speed_multi(self) -> float:
        return prod(self._speed_multis.values())

    def get_speed_advices(self) -> dict[str, list[Advice]]:
        account = session_data.account
        multis = {
            group: round_and_trim(multi) for group, multi in self._speed_multis.items()
        }
        total = round_and_trim(self.speed_multi)
        divinity = account.divinity
        oj_jooce = account.alchemy_vials["Oj Jooce (Orange Slice)"]
        return {
            f"Total: {total}x": [
                Advice(
                    label=f"Total Sailing Speed bonus: {total}x",
                    picture_class="sailing",
                )
            ],
            f"Multi Group A: {multis['A']}x": [
                divinity.named("Purrmep").minor.get_bonus_advice(),
                account.cards.named("Crawler").getAdvice(),
                account.cards.named("Kattlekruk").getAdvice(),
                account.alchemy_bubbles["Boaty Bubble"].get_bonus_advice(goal=max_NBLB),
            ],
            f"Multi Group B: {multis['B']}x": [
                divinity.named("Goharut").blessing.get_bonus_advice()
            ],
            f"Multi Group C: {multis['C']}x": [
                divinity.named("Purrmep").blessing.get_bonus_advice()
            ],
            f"Multi Group D: {multis['D']}x": [account.ballot[24].get_bonus_advice()],
            f"Multi Group E: {multis['E']}x": [
                divinity.named("Bagur").blessing.get_bonus_advice(),
                self._get_ad_tablet_advice(),
                account.stamps["Sailboat Stamp"].get_advice(),
                account.statues["Boat Statue"].get_advice(),
                account.meals["Popped Corn"].get_bonus_advice(),
                oj_jooce.get_advice(full_name=False),
                self._get_skill_mastery_advice(),
                self._get_msa_advice(),
                account.vault.get_upgrade_advice("Speedy Sailing"),
                self._get_c_shanti_advice(),
                account.star_signs.get_seraph_advice(),
                account.star_signs.get_silkrode_advice(),
            ],
            f"Multi Group F: {multis['F']}x": [
                account.gemshop.purchases["Davey Jones Training"].get_advice(),
                account.legend_talents["Davey Jones Returns"].get_advice(),
            ],
        }

    def _get_ad_tablet_advice(self) -> Advice:
        level = self.artifacts["10 AD Tablet"].level
        return Advice(
            label=f"Level {level} 10 AD Tablet: +{self._ad_tablet_bonus}%",
            picture_class="10-ad-tablet",
            progression=level,
            goal=max_sailing_artifact_level,
        )

    def _get_skill_mastery_advice(self) -> Advice:
        unlocked = self._skill_mastery_bonus > 0
        status = f"+{self._skill_mastery_bonus}%" if unlocked else "Locked."
        return Advice(
            label=f"{{{{ Rift|#rift }}}} - Sailing Skill Mastery 200: {status}",
            picture_class="skill-mastery",
            progression=int(unlocked),
            goal=1,
        )

    def _get_msa_advice(self) -> Advice:
        account = session_data.account
        msa_sailing = account.gaming.superbits["MSA Sailing"].unlocked
        total_worship_waves = account.worship.total_waves
        return Advice(
            label=f"MSA Sailing: +{msa_sailing * total_worship_waves // 10}% "
            f"(+1% per 10 waves in Worship)",
            picture_class="worship",
            progression=total_worship_waves,
            goal=account.worship.max_total_waves,
        )

    def _get_c_shanti_advice(self) -> Advice:
        star_signs = session_data.account.star_signs
        unlocked = star_signs["C. Shanti Minor"].unlocked
        if not unlocked:
            status = "Locked."
        elif self._c_shanti_bonus:
            status = f"+{round_and_trim(self._c_shanti_bonus)}%"
        else:
            # What `value_for` gives once it is equipped
            equipped_bonus = round_and_trim(20 * star_signs.seraph_multi)
            status = f"+{equipped_bonus}% if equipped"
        return Advice(
            label=f"{{{{ Star Signs|#star-signs }}}} - C. Shanti Minor: {status}",
            picture_class="c-shanti-minor",
            progression=int(unlocked),
            goal=1,
        )
