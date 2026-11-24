from functools import cached_property
from math import ceil

from consts.consts_autoreview import default_huge_number_replacement
from consts.w5.divinity import (
    default_offering_cost_after_3,
    divinity_gods,
    divinity_offerings,
    divinity_styles,
)
from models.advice.advice import Advice
from models.general.character import Character
from models.general.session_data import session_data
from utils.logging import get_logger
from utils.safer_data_handling import (
    safe_loads,
    safer_convert,
    safer_get,
    safer_math_pow,
)
from utils.text_formatting import pl

logger = get_logger(__name__)


class GodBlessing:
    """Account-wide, no link needed"""

    def __init__(self, god_name: str, level: int, value_per_level: int, material: str):
        self.god_name: str = god_name
        self.level: int = level
        self.material: str = material
        # "BlesssBonus" in source. Last updated in v2.561.0
        # Not modelled yet: Nobisect's own formula, the Jade Emporium multiplier
        self.value: int = level * value_per_level

    def get_advice(self, additional_text: str = "") -> Advice:
        return Advice(
            label=f"{self.god_name} Blessing{additional_text}",
            picture_class=self.god_name,
            progression=self.level,
            goal=100,
            resource=self.material,
        )

    def get_bonus_advice(self) -> Advice:
        return self.get_advice(f": +{self.value}%")


class GodMinorBonus:
    """Account-wide Minor Link bonus: `"Bonus_Minor"` with no character in source"""

    def __init__(self, god_name: str, base_value: int):
        self.god_name: str = god_name
        self.base_value: int = base_value

    @cached_property
    def _linked_character(self) -> Character | None:
        # Depends on: characters
        return next(
            (
                char
                for char in session_data.account.characters.safe
                if char.divinity_link == self.god_name
            ),
            None,
        )

    @cached_property
    def value(self) -> float:
        # "DivMinorBonus" in source: base value scaled by divinity level.
        # Last updated in v2.561.0
        # Not modelled yet: max(1, Big P), the Coral Kid multiplier, several linked
        # characters, King Doot and Pocket Divinity for Harriep and Goharut
        # Depends on: characters, alchemy_bubbles['Big P']
        if self._linked_character is None:
            return 0
        level = self._linked_character.divinity_level
        big_p = session_data.account.alchemy_bubbles["Big P"].base_value
        return level / (60 + level) * big_p * self.base_value

    def get_bonus_advice(self) -> Advice:
        return Advice(
            label=f"Anyone Minor Linked to {self.god_name}: +{self.value:.2f}%",
            picture_class=self.god_name,
            progression=int(self._linked_character is not None),
            goal=1,
        )


class God:
    def __init__(self, index: int, info: dict, unlocked: bool, blessing_level: int):
        self.index: int = index
        self.name: str = info["Name"]
        self.unlocked: bool = unlocked
        self.blessing: GodBlessing = GodBlessing(
            self.name,
            blessing_level,
            info["BlessingPerLevel"],
            info["BlessingMaterial"],
        )
        self.minor: GodMinorBonus = GodMinorBonus(self.name, info["MinorBaseValue"])


class Divinity(dict[int, God]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_divinity = safe_loads(raw_data.get("Divinity", []))
        if not raw_divinity:
            logger.warning("Divinity data not present")
        while len(raw_divinity) < 40:
            raw_divinity.append(0)
        self._raw_divinity: list = raw_divinity
        # Toolbox provides serverVars, Efficiency provides servervars
        raw_server_vars = safe_loads(
            raw_data.get("serverVars", raw_data.get("servervars", {}))
        )
        self.div_cost_after_3: float = safer_get(
            raw_server_vars, "DivCostAfter3", default_offering_cost_after_3
        )

        self.points = raw_divinity[24]
        if isinstance(self.points, str):
            try:
                self.points = int(float(self.points))
            except ValueError:
                logger.exception(
                    f"Could not convert {self.points} to int. Defaulting to 0"
                )
                self.points = 0
        self.gods_unlocked: int = min(10, raw_divinity[25])
        self.god_rank: int = max(0, raw_divinity[25] - 10)
        self.low_offering: int = raw_divinity[26]
        self.high_offering: int = raw_divinity[27]
        self.low_offering_goal: float = 0
        self.high_offering_goal: float = 0
        self.account_wide_arctis: bool = False

        for index, info in enumerate(divinity_gods, start=1):
            # Snake is index 1, its Blessing level is stored in 28
            self[index] = God(
                index, info, self.gods_unlocked >= index, raw_divinity[index + 27]
            )

    def named(self, name: str) -> God:
        return next(god for god in self.values() if god.name == name)

    def link_characters(self, characters: list[Character]):
        for character in characters:
            try:
                character.setDivinityStyle(
                    self._style_name(self._raw_divinity[character.character_index])
                )
                character.setDivinityLink(
                    self._link_name(self._raw_divinity[character.character_index + 12])
                )
            except (IndexError, TypeError):
                continue

    @staticmethod
    def _style_name(style_index: int) -> str:
        if 0 <= style_index < len(divinity_styles):
            return divinity_styles[style_index]["Name"]
        return f"UnknownStyle{style_index}"

    @staticmethod
    def _link_name(god_index: int) -> str:
        # -1 is saved for no link
        if god_index == -1:
            return "Unlinked"
        if 0 <= god_index < len(divinity_gods):
            return divinity_gods[god_index]["Name"]
        return f"UnknownDivinity{god_index + 1}"

    @staticmethod
    def get_style_advices(highest_divinity_level: int) -> dict[str, list[Advice]]:
        points_advices = []
        # Best first, by `DivStyle` index. Mantra and TranQi give no points
        for index in [7, 6, 2, 4, 1, 0]:
            style = divinity_styles[index]
            if highest_divinity_level >= style["UnlockLevel"]:
                points_advices.append(
                    Advice(
                        label=f"{style['Points']}/hr: {style['Name']}",
                        picture_class=style["Name"],
                        completed=True,
                    )
                )
        exp_advices = []
        for index in [7, 6, 4, 5, 1, 3, 2, 0]:
            style = divinity_styles[index]
            if highest_divinity_level >= style["UnlockLevel"]:
                exp_advices.append(
                    Advice(
                        label=f"{style['Exp']}/hr: {style['Name']} {style['Notes']}",
                        picture_class=style["Name"],
                        completed=True,
                    )
                )
        return {
            "Highest Points per hour": points_advices,
            "Highest EXP per hour": exp_advices,
        }

    @staticmethod
    def _get_offering(offering_index: int) -> dict:
        if 0 <= offering_index < len(divinity_offerings):
            return divinity_offerings[offering_index]
        return {"Name": f"UnknownOffering{offering_index}", "Image": "", "Odds": 0.01}

    def get_offering_advices(self) -> list[Advice]:
        return [
            self._get_offering_advice(self.low_offering, self.low_offering_goal),
            self._get_offering_advice(self.high_offering, self.high_offering_goal),
        ]

    def _get_offering_advice(self, offering_index: int, goal: float) -> Advice:
        offering = self._get_offering(offering_index)
        purchases = safer_convert(self.points // goal, 0)
        purchases_text = (
            f"<br>Could be bought {purchases} time{pl(purchases)}"
            if self.points >= goal
            else ""
        )
        return Advice(
            label=f"{offering['Odds']:.0%} Offering: {offering['Name']}"
            f"{purchases_text}",
            picture_class=offering["Image"],
            progression=f"{max(0, min(1, self.points / max(1, goal))):.2%}",
            goal="100%",
        )

    def calculate(self, account_wide_arctis: bool):
        self.account_wide_arctis = account_wide_arctis
        unlocked = self.gods_unlocked + self.god_rank
        self.low_offering_goal = self._offering_cost(self.low_offering, unlocked)
        self.high_offering_goal = self._offering_cost(self.high_offering, unlocked)

    def _offering_cost(self, offering_index: int, unlocked: int) -> float:
        # "OfferingCost" in source. Last updated in v2.561.0
        try:
            cost = (
                20 * safer_math_pow(unlocked + 1.3, 2.3) * safer_math_pow(2.2, unlocked)
                + 60
            ) * self._get_offering(offering_index)["Odds"]
            if unlocked >= 3:
                cost = cost * safer_math_pow(
                    min(1.8, max(1, 1 + self.div_cost_after_3 / 100)), unlocked - 2
                )
            return ceil(cost)
        except OverflowError:
            logger.exception(
                f"Could not calc Divinity Offering cost with {unlocked} unlocked. "
                f"Returning {default_huge_number_replacement}"
            )
            return default_huge_number_replacement
