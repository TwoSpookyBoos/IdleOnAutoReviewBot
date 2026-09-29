from consts.consts_autoreview import ValueToMulti
from consts.consts_w2 import max_sigil_level, sigils_dict
from consts.consts_w5 import max_sailing_artifact_level
from models.advice.advice import Advice
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

    def calculate_speed(
        self,
        *,
        chilled_yarn,
        chilled_yarn_multi: float,
        max_chilled_yarn_multi: float,
        vial_junkee: bool,
        sigil_supercharge_owned: int,
        willow_vial: float,
        sigil_stamp: float,
        summoning_multi: float,
        tuttle_vial: float,
        ballot_multi: float,
        arcade_bonus: float,
        big_sig_fig: float,
    ):
        # "SigilBonusSpeed" in source. Last updated in v2.49 Dec 24 2025
        # Multi Group A = several
        peapod = self["Pea Pod"]
        self._chilled_yarn = chilled_yarn
        self.chilled_yarn_multi = chilled_yarn_multi
        self.max_chilled_yarn_multi = max_chilled_yarn_multi
        try:
            self.peapod_value = peapod.values[peapod.level] * chilled_yarn_multi
        except IndexError:
            logger.error(
                f"Peapod Sigil Level of {peapod.level} not present in 'sigils_dict'. "
                f"Defaulting to max_sigil_level of {max_sigil_level}"
            )
            self.peapod_value = peapod.values[max_sigil_level] * chilled_yarn_multi
        self.vial_junkee = vial_junkee
        # The Sigil Stamp is a MISC stamp, not multiplied by Lab or Pristine Charm
        self.speed_multi_a = ValueToMulti(
            (20 * vial_junkee)
            + (20 * sigil_supercharge_owned)
            + self.peapod_value
            + willow_vial
            + sigil_stamp
        )
        # Multi Group B = Summoning Winner Bonuses
        self.speed_multi_b = summoning_multi
        # Multi Group C = Tuttle Vial
        self.speed_multi_c = ValueToMulti(tuttle_vial)
        # Multi Group D = Bonus Ballot
        self.speed_multi_d = ballot_multi
        # Multi Group E = Arcade
        self.speed_multi_e = ValueToMulti(arcade_bonus)
        # Multi Group F = Legend Talents
        self.speed_multi_f = ValueToMulti(big_sig_fig)
        self.speed_multi = max(
            1,
            self.speed_multi_a
            * self.speed_multi_b
            * self.speed_multi_c
            * self.speed_multi_d
            * self.speed_multi_e
            * self.speed_multi_f,
        )

    def get_vial_junkee_advice(self) -> Advice:
        return Advice(
            label=f"W2 Achievement: Vial Junkee: +{20 * self.vial_junkee}/20%",
            picture_class="vial-junkee",
            progression=int(self.vial_junkee),
            goal=1,
        )

    def get_peapod_advice(self) -> Advice:
        peapod = self["Pea Pod"]
        return Advice(
            label=f"Sigil: Level {peapod.level} Pea Pod: +{self.peapod_value}/"
            f"{peapod.values[-1] * self.max_chilled_yarn_multi}%",
            picture_class="pea-pod",
            progression=peapod.level,
            goal=max_sigil_level,
        )

    def get_chilled_yarn_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Artifact|#sailing}}}}: Chilled Yarn: "
            f"{self.chilled_yarn_multi}/{self.max_chilled_yarn_multi}x"
            f"<br>(Already applied to Pea Pod Sigil above)",
            picture_class="chilled-yarn",
            progression=self._chilled_yarn.level,
            goal=max_sailing_artifact_level,
        )


class AlchemyP2W:
    def __init__(self, raw_data: dict):
        raw_p2w = safe_loads(raw_data.get("CauldronP2W", []))
        raw_p2w = [v if isinstance(v, list) else [v] for v in raw_p2w]

        self.cauldrons: list = safer_index(raw_p2w, 0, [0] * 12)
        self.liquids: list = safer_index(raw_p2w, 1, [0] * 8)
        self.vials: list = safer_index(raw_p2w, 2, [0] * 2)
        self.player: list = safer_index(raw_p2w, 3, [0] * 2)
        self.sigils: Sigils = Sigils(safer_index(raw_p2w, 4, []))
