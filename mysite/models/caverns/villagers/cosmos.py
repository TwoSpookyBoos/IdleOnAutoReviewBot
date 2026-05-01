from dataclasses import dataclass

from consts.consts_autoreview import ValueToMulti
from consts.consts_w5 import divinity_divinities_dict
from consts.idleon.caverns.villager.cosmos import majiks
from models.advice.advice import Advice
from models.caverns.villagers.villager import Villager
from utils.logging import get_logger

logger = get_logger(__name__)


class MajiksBonus:
    MAJIKS_TYPE = {0: "hole", 1: "village", 2: "idleon"}

    def __init__(self, data: dict, level: int, index: int, type_index: int):
        self.name = data["Name"]
        self.index = index
        self.level = level
        self.max_level = data["MaxEnchantLevel"] + 1
        self._template = data["Template"]
        self._base_value = data["BaseValue"]
        self._type = self.MAJIKS_TYPE.get(type_index)
        self._is_multi = "{" not in self._template

    def calculate_bonus(self):
        # "CosmoBonusQTY" in source. Last update v2.526
        if self._type == self.MAJIKS_TYPE[2] and self.index == 1:
            self.value = max(1, 3**self.level)
            self.max_value = max(1, 3**self.max_level)
        else:
            self.value = self._base_value * self.level
            self.max_value = self._base_value * self.max_level
        if self._is_multi:
            self.as_multi = ValueToMulti(self.value)

    def get_advice(self, link_to_section: bool = True) -> Advice:
        if self.name == "Pocket Divinity" and self._template != "{% All Stats":
            description = self._template + "".join(f"<br> {name}" for name in self.link)
        else:
            current = ValueToMulti(self.value) if self._is_multi else self.value
            max_value = ""
            if self.level < self.max_level:
                target = (
                    ValueToMulti(self.max_value) if self._is_multi else self.max_value
                )
                max_value = f"/{target}"
            char_to_replace = "}" if self._is_multi else "{"
            value = f"{current}{max_value}"
            description = self._template.replace(char_to_replace, value)
        prefix = "un" if self.level == 0 else ""
        link_text = "{{Villager Cosmos Majik|#villagers}} - " if link_to_section else ""
        return Advice(
            label=f"{link_text}{self.name}: {description}",
            picture_class=f"{self._type}-majik-{prefix}purchased",
            progression=self.level,
            goal=self.max_level,
        )


@dataclass
class Majiks:
    hole: dict[str, MajiksBonus]
    village: dict[str, MajiksBonus]
    idleon: dict[str, MajiksBonus]
    spend_point: int
    max_point: int


class Cosmos(Villager):
    def __init__(self, **kwargs):
        super().__init__(name="Cosmos", unlock_at=5, role="The Conjuror", **kwargs)

    def parse_feature(self, raw_caverns_list: list):
        hole_majiks = raw_caverns_list[4]
        village_majiks = raw_caverns_list[5]
        idleon_majiks = raw_caverns_list[6]
        spend_point = sum([sum(hole_majiks), sum(village_majiks), sum(idleon_majiks)])
        majiks_levels = [hole_majiks, village_majiks, idleon_majiks]
        type_bonuses = []
        max_point = 0
        for type_index, majiks_bonuses in enumerate(majiks):
            bonuses = {}
            for majik_index, majik_data in enumerate(majiks_bonuses):
                level = majiks_levels[type_index][majik_index]
                majik_bonus = MajiksBonus(majik_data, level, majik_index, type_index)
                bonuses[majik_bonus.name] = majik_bonus
                max_point += majik_bonus.max_level
            type_bonuses.append(bonuses)
        self.majiks = Majiks(
            hole=type_bonuses[0],
            village=type_bonuses[1],
            idleon=type_bonuses[2],
            spend_point=spend_point,
            max_point=max_point,
        )
        # Pocket Divinity
        extras = raw_caverns_list[11]
        try:
            raw_pocket_div_links = [int(v) for v in extras[29:31] if v is not None]
        except Exception:
            logger.exception(
                "Could not parse Pocket Divinity link values. Defaulting to no links."
            )
            raw_pocket_div_links = [-1, -1]
        pocket_majik = self.majiks.idleon["Pocket Divinity"]
        pocket_majik.link = []
        for entry_index, entry_value in enumerate(raw_pocket_div_links):
            god_index = int(entry_value) + 1
            if god_index == 0 or entry_index >= pocket_majik.level:
                break
            if god_index not in divinity_divinities_dict:
                logger.exception(f"Unknown God in Pocket Divinity #{god_index}")
                continue
            pocket_majik.link.append(divinity_divinities_dict[god_index]["Name"])

    def calculate_bonuses(self, have_doot: bool):
        if have_doot:
            self.majiks.idleon["Pocket Divinity"]._base_value = 15
            self.majiks.idleon["Pocket Divinity"]._template = "{% All Stats"
            self.majiks.idleon["Pocket Divinity"]._is_multi = False
        majiks = (self.majiks.hole, self.majiks.village, self.majiks.idleon)
        for majik_type in majiks:
            for bonus in majik_type.values():
                bonus.calculate_bonus()

    def stat_advices(self) -> list[Advice]:
        from models.general.session_data import session_data

        gscp = session_data.account.gemshop["Purchases"]["Conjuror Pts"]
        # Practical Max Level
        advice_list = self.base_stat_advice(self.majiks.max_point - gscp["Owned"])
        advice_list.append(
            Advice(
                label=(
                    f"Up to {gscp['MaxLevel']} Conjuror Pts can be purchased"
                    f" from the {{{{Gem Shop|#gem-shop}}}}"
                ),
                picture_class="conjuror-pts",
                progression=gscp["Owned"],
                goal=gscp["MaxLevel"],
            )
        )
        earned_conjuror_points = gscp["Owned"] + self.level
        if earned_conjuror_points > self.majiks.spend_point < self.majiks.max_point:
            unspent = earned_conjuror_points - self.majiks.spend_point
            advice_list.append(
                Advice(
                    label=f"You have {unspent} unspent Conjuror Pts!",
                    picture_class="cosmos",
                    progression=self.majiks.spend_point,
                    goal=earned_conjuror_points,
                )
            )
        return advice_list

    def feature_advice(self) -> dict[str, list[Advice]] | None:
        return {
            "Hole Majik Stats": [
                bonus.get_advice(link_to_section=False)
                for bonus in self.majiks.hole.values()
            ],
            "Village Majik Stats": [
                bonus.get_advice(link_to_section=False)
                for bonus in self.majiks.village.values()
            ],
            "IdleOn Majik Stats": [
                bonus.get_advice(link_to_section=False)
                for bonus in self.majiks.idleon.values()
            ],
        }
