from consts.consts_autoreview import MultiToValue
from consts.consts_w2 import (
    bubbles_dict,
    class_passive_bubble_by_cauldron,
    class_passive_bubble_max_index,
    max_implemented_bubble_index,
    prisma_bubbles_optlacc_index,
)
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from models.general.companions import Companions
from models.master_classes.tesseract import Tesseract
from models.w2.alchemy_p2w import Sigils
from models.w2.arcade import Arcade
from models.w6.farming import ExoticMarketUpgrade
from models.w7.gallery import Gallery
from models.w7.jelly_operator import JellyOperator
from models.w7.legend_talents import LegendTalents
from models.w7.sushi_station import SushiStation
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index
from utils.text_formatting import getItemDisplayName

logger = get_logger(__name__)


def parse_raw_cauldrons(raw_data: dict) -> list[dict[int, int]]:
    """Bubble levels per cauldron, as {bubble_index: level}.

    Shared by AlchemyBubbles and AlchemyCauldrons.
    """
    raw_cauldron_info = safe_loads(raw_data.get("CauldronInfo", [0, 0, 0, 0, {}]))
    cauldrons = []
    for cauldron_index in range(4):
        raw = safer_index(raw_cauldron_info, cauldron_index, {})
        if not isinstance(raw, dict):
            raw = {}
        levels = {}
        for key, value in raw.items():
            if key == "length":
                continue
            try:
                levels[int(key)] = safer_convert(value, 0)
            except ValueError:
                continue
        if not levels:
            levels = {k: 0 for k in range(0, max_implemented_bubble_index + 1)}
        cauldrons.append(levels)
    return cauldrons


class Bubble:
    def __init__(self, cauldron_index: int, bubble_index: int, info: dict, level: int):
        self.cauldron_index: int = cauldron_index
        self.bubble_index: int = bubble_index
        self.name: str = info["Name"]
        self.level: int = level
        self.material: str = getItemDisplayName(info["Material"])
        self.base_value: float = lava_func(
            info["funcType"], level, info["x1"], info["x2"]
        )
        self.max_value: float = {"decay": info["x1"], "decayMulti": 1 + info["x1"]}.get(
            info["funcType"], 0
        )
        self.is_prisma: bool = False

    def get_advice(self, additional_text: str = "", goal="") -> Advice:
        return Advice(
            label=f"{self.name}{additional_text}",
            picture_class=self.name,
            progression=self.level,
            goal=goal,
            resource=self.material,
        )

    def get_tier_advice(self, goal, additional_text: str = "") -> Advice:
        return Advice(
            label=f"Level {self.name} {additional_text}",
            picture_class=self.name,
            progression=self.level,
            goal=goal,
            resource=self.material,
        )

    def get_bonus_advice(self, additional_text: str = "", goal="", cap=None) -> Advice:
        """Linked framing, for sections that only cite the bubble's bonus."""
        cap = self.max_value if cap is None else cap
        cap = f"/{round_and_trim(cap)}" if cap else ""
        return Advice(
            label=f"{{{{ Alchemy Bubbles|#bubbles }}}} - {self.name}: "
            f"+{round_and_trim(self.base_value)}{cap}%{additional_text}",
            picture_class=self.name,
            progression=self.level,
            goal=goal,
            resource=self.material,
        )


class AlchemyBubbles(dict[str, Bubble]):
    def __init__(self, raw_data: dict):
        super().__init__()
        cauldrons = parse_raw_cauldrons(raw_data)
        for cauldron_index, cauldron in bubbles_dict.items():
            for bubble_index, info in cauldron.items():
                if bubble_index > max_implemented_bubble_index:
                    continue  # don't waste time calculating unimplemented bubbles
                level = cauldrons[cauldron_index].get(bubble_index, 0)
                self[info["Name"]] = Bubble(cauldron_index, bubble_index, info, level)
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        prisma_tags = f"{safer_index(raw_optlacc, prisma_bubbles_optlacc_index, '')}"
        self.prisma_multi: float = 1.0
        for bubble in self.values():
            tag = f"{'_abc'[bubble.cauldron_index]}{bubble.bubble_index},"
            bubble.is_prisma = tag in prisma_tags

    def calculate_prisma_multi(
        self,
        tesseract: Tesseract,
        arcade: Arcade,
        sushi_station: SushiStation,
        jelly_operator: JellyOperator,
        gallery: Gallery,
        sigils: Sigils,
        exotic_market: dict[str, ExoticMarketUpgrade],
        legend_talents: LegendTalents,
        companions: Companions,
    ):
        # "PrismaBonusMult" in source. Last updated in v2.531.0
        purple_sigils = sum(1 for sigil in sigils.values() if sigil.level >= 3)
        self.prisma_multi = min(4, 2 + (
            tesseract.upgrades["Pinnacle of Prisma"].level
            + arcade[54].value
            + sushi_station.get_milestone_bonus_value("Prisma Bubble Bonus")
            + jelly_operator.obstructions["Bowling Pin"].bonus_value
            + 10 * gallery.has_w6_trophy
            + gallery.prisma_palette_bonus
            + 0.2 * purple_sigils
            + exotic_market["PRISMA PETAL"].value
            + legend_talents["Wowa Woowa"].value
            + MultiToValue(
                companions.get_multi("Rift Hivemind", "Prisma Bubble Bonus")
            )
        ) / 100)

    def get_prisma_value(self, name: str) -> float:
        bubble = self.get(name)
        if not bubble:
            return 0
        if bubble.is_prisma:
            return bubble.base_value * max(1, self.prisma_multi)
        return bubble.base_value

    def get_class_bubble_value(self, base_class: str, name: str) -> float:
        # Boosted by its cauldron's class passive bubble
        value = self.get_prisma_value(name)
        bubble = self.get(name)
        passive = (
            class_passive_bubble_by_cauldron.get(bubble.cauldron_index)
            if bubble
            else None
        )
        if (
            passive
            and base_class == passive[0]
            and bubble.bubble_index < class_passive_bubble_max_index
        ):
            value *= max(1, self.get_prisma_value(passive[1]))
        return value
