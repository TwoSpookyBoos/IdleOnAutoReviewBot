from dataclasses import dataclass

from consts.consts_autoreview import EmojiType
from consts.w1.stamps import stamp_maxes
from models.general.item_definitions import ItemDefinition
from models.advice.advice import Advice
from utils.number_formatting import round_and_trim


@dataclass
class Stamp:
    name: str
    code_name: str
    effect: str
    delivered: bool
    level: int
    max_level: int
    material: ItemDefinition | None
    value: float
    stamp_type: str
    exalted: bool
    total_value: float = 0

    def get_advice(self, link_to_section: bool = True, additional_text: str = "", goal_override = ""):
        link_to_section_text = f"{{{{ Stamps|#stamps }}}} - " if link_to_section else ""
        effect_text = f" {self.effect}" if not self.effect.startswith('%') else self.effect
        unlock_text = "Unlock " if not self.delivered else ""
        body_text = f": +{round_and_trim(self.total_value)}{effect_text}{additional_text}" if self.delivered else ""
        return Advice(
            label=f"{link_to_section_text}{unlock_text}{self.name}{body_text}",
            resource=self.material.name,
            progression=self.level,
            goal=(goal_override if goal_override else stamp_maxes.get(self.name, EmojiType.INFINITY.value)) if self.delivered else 1,
            picture_class=self.name,
        )

class Stamps(dict[str, Stamp]):
    def __init__(self):
        super().__init__()
