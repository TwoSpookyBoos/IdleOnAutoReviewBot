from functools import cached_property
from math import prod

from consts.consts_autoreview import ValueToMulti
from consts.consts_w2 import max_sigil_level, sigils_dict
from models.advice.advice import Advice
from models.general.session_data import session_data
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
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

    @property
    def value(self) -> float:
        # "SigilBonus" in source. Last updated in v2.561.0
        # Depends on: sailing.artifacts['Chilled Yarn'], meritocracy[21]
        account = session_data.account
        return (
            self.values[min(self.level, max_sigil_level)]
            * account.sailing.artifacts["Chilled Yarn"].as_multi
            * ValueToMulti(account.meritocracy[21].value)
        )

    @property
    def max_value(self) -> float:
        account = session_data.account
        return (
            self.values[max_sigil_level]
            * account.sailing.artifacts["Chilled Yarn"].max_multi
            * ValueToMulti(account.meritocracy[21].value)
        )

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        link_text = "{{ Sigils|#sigils }} - " if link_to_section else ""
        return Advice(
            label=f"{link_text}Level {self.level} {self.name}: "
            f"+{round_and_trim(self.value)}/{round_and_trim(self.max_value)}%",
            picture_class=self.name,
            progression=self.level,
            goal=max_sigil_level,
        )


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

    @cached_property
    def _speed_multis(self) -> dict[str, float]:
        # "SigilBonusSpeed" in source. Last updated in v2.49 Dec 24 2025
        # Depends on: achievements, gemshop, alchemy_vials, stamps, summoning, ballot,
        # arcade, legend_talents
        account = session_data.account
        vial_junkee = account.achievements["Vial Junkee"].complete
        supercharge = account.gemshop.purchases["Sigil Supercharge"].owned
        vials = account.alchemy_vials
        return {
            # The Sigil Stamp is a MISC stamp, not multiplied by Lab or Pristine Charm
            "A": ValueToMulti(
                20 * vial_junkee
                + 20 * supercharge
                + self["Pea Pod"].value
                + vials["Willow Sippy (Willow Logs)"].value
                + account.stamps["Sigil Stamp"].total_value
            ),
            "B": account.summoning.bonuses["Sigil SPD"].as_multi,
            "C": ValueToMulti(vials["Turtle Tisane (Tuttle)"].value),
            "D": account.ballot[17].active_multi,
            "E": ValueToMulti(account.arcade[43].value),
            "F": ValueToMulti(account.legend_talents["Big Sig Fig"].value),
        }

    @cached_property
    def speed_multi(self) -> float:
        return max(1, prod(self._speed_multis.values()))

    def get_speed_advices(self, practical_maxed: bool) -> dict[str, list[Advice]]:
        account = session_data.account
        multis = self._speed_multis
        supercharge = account.gemshop.purchases["Sigil Supercharge"]
        supercharge_advice = supercharge.get_advice(
            additional_text=f": +{20 * supercharge.owned}/{20 * supercharge.max_level}%"
        )
        supercharge_advice.completed = not practical_maxed
        willow_vial = account.alchemy_vials["Willow Sippy (Willow Logs)"]
        tuttle_vial = account.alchemy_vials["Turtle Tisane (Tuttle)"]
        chilled_yarn = account.sailing.artifacts["Chilled Yarn"]
        return {
            f"Multi Group A: {multis['A']:.3f}x": [
                self._get_vial_junkee_advice(),
                supercharge_advice,
                self["Pea Pod"].get_bonus_advice(link_to_section=False),
                chilled_yarn.get_bonus_advice(
                    "(Already applied to Pea Pod Sigil above)"
                ),
                willow_vial.get_advice(f"+{willow_vial.value:.3f}"),
                account.stamps["Sigil Stamp"].get_advice(),
            ],
            f"Summoning: {round_and_trim(multis['B'])}x": [
                account.summoning.bonuses["Sigil SPD"].get_bonus_advice()
            ],
            f"Multi Group C: {multis['C']:.3f}x": [
                tuttle_vial.get_advice(f"{multis['C']:.3f}x")
            ],
            f"Multi Group D: {multis['D']:.3f}x": [
                account.ballot[17].get_bonus_advice()
            ],
            f"Multi Group E: {multis['E']:.3f}x": [account.arcade[43].get_advice()],
            f"Multi Group F: {round_and_trim(multis['F'])}x": [
                account.legend_talents["Big Sig Fig"].get_advice()
            ],
        }

    def _get_vial_junkee_advice(self) -> Advice:
        vial_junkee = session_data.account.achievements["Vial Junkee"].complete
        return Advice(
            label=f"W2 Achievement: Vial Junkee: +{20 * vial_junkee}/20%",
            picture_class="vial-junkee",
            progression=int(vial_junkee),
            goal=1,
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
