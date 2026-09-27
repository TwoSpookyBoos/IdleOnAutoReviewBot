from functools import cached_property

from consts.consts_autoreview import EmojiType, MultiToValue, ValueToMulti
from consts.consts_item_data import ITEM_DATA, raw_item_data
from consts.consts_w1 import get_seraph_cosmos_multi
from consts.consts_w2 import max_sigil_level, sigils_dict
from consts.general.talents import (
    apocalypse_wow_talent_index,
    haungry_for_gold_talent_index,
)
from consts.idleon.lava_func import lava_func

from models.advice.advice import Advice
from models.w1.star_signs import get_infinite_star_sign_levels

from utils.all_talentsDict import all_talentsDict
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safer_math_log
from utils.text_formatting import getItemCodeName

from utils.logging import get_logger

logger = get_logger(__name__)


class GoldenFood:
    """
    Class for track of golden item, calculate it's bonus and generate advice
    for it
    """

    def __init__(self, name: str, amount: int = 0):
        self.name = name
        self.amount = amount
        item_data = ITEM_DATA[getItemCodeName(name)]
        self.bonus_coefficient = item_data.amount
        self._description = item_data.description
        self.bonus_value = 0
        self.max_bonus = None

    def calculate_bonus(self, golden_food_multi, max_amount: int | None = None):
        self.bonus_value = self._calculate_bonus(golden_food_multi, self.amount)
        if max_amount is not None:
            self.max_bonus = self._calculate_bonus(golden_food_multi, max_amount)

    def _calculate_bonus(self, golden_food_multi, amount):
        # _customBlock_GoldFoodBonuses in source. Last update v2.48 Jan 01 2026
        log_value = safer_math_log(1 + amount, "lava")
        return (
            self.bonus_coefficient
            * 0.05
            * golden_food_multi
            * log_value
            * (1 + log_value / 2.14)
        )

    def get_bonus_advice(
        self, link_to_section: bool = True, worn: bool = False
    ) -> Advice:
        """Advice for golden food bonus"""
        label = ""
        if worn:
            label += "Golden Food (worn) - "
        elif link_to_section:
            label += "{{Beanstalk|#beanstalk}} - "
        if self.max_bonus is not None:
            goal = self.max_bonus
            bonus = f"{round_and_trim(self.bonus_value)}/{round_and_trim(goal)}"
        else:
            bonus = f"{round_and_trim(self.bonus_value)}"
            goal = EmojiType.INFINITY.value
        description = (
            self._description.replace(". Golden foods are never consumed", "")
            .replace("[", bonus)
            .strip()
        )
        label += f"{self.name}:<br>{description}"
        return Advice(
            label=label, picture_class=self.name, progression=self.amount, goal=goal
        )


def get_worn_golden_food(character, effect: str) -> GoldenFood | None:
    # Last matching slot wins
    worn = None
    for food in character.equipment.foods:
        item = raw_item_data.get(food.codename, {})
        if item.get("Type") == "GOLDEN_FOOD" and item.get("Effect") == effect:
            worn = GoldenFood(item["Name"].replace("_", " "), food.amount)
    return worn


class GoldenFoodMulti:
    # "GfoodBonusMULTI" in source, per character. Last updated in v2.531.0

    def __init__(self, outer: float, family: float, sources: dict[str, float]):
        self.outer = outer
        self.family = family
        self.sources = sources

    @cached_property
    def total(self) -> float:
        return self.outer * (self.family + sum(self.sources.values()) / 100)


def calculate_golden_food_multis(account) -> dict[int, GoldenFoodMulti]:
    # "GfoodBonusMULTI" in source, per character. Last updated in v2.531.0
    companions = account.companions
    secret_set = MultiToValue(account.armor_sets["SECRET SET"].total_value)
    verminous_multi = companions.get_multi("Verminous", "Gold Food")
    outer = ValueToMulti(secret_set + MultiToValue(verminous_multi))
    family = max(1, account.family_bonuses["Shaman"].value)

    # Apocalypse Wow: best Death Bringer, times WOW maps
    apoc_talent = all_talentsDict[apocalypse_wow_talent_index]
    apoc_index = account.death_note.apocalypse_character_index
    wow_maps = (
        account.all_characters[apoc_index].apoc_dict["WOW"]["Total"]
        if apoc_index is not None
        else 0
    )

    sigil = account.alchemy_p2w.sigils["Emoji Veggie"]
    sigil_multi = (
        account.sailing.artifacts.chilled_yarn_multi
        * ValueToMulti(account.meritocracy[21].value)
    )
    sigil_value = sigils_dict["Emoji Veggie"]["Values"][
        min(sigil.level, max_sigil_level)
    ]
    beanbie = account.star_signs["Beanbie Major"]
    infinite_levels = get_infinite_star_sign_levels(
        account.breeding.total_shiny_levels["Infinite Star Signs"]
    )
    seraph_unlocked = account.star_signs["Seraph Cosmos"].unlocked
    cultism_level = account.tesseract.upgrades["Astrology Cultism"].level
    card_levels = {card.codename: card.level for card in account.cards}
    achievements = account.achievements
    obstructions = account.jelly_operator.obstructions
    # Per character ones filled below; order kept for the sum
    sources = {
        # EtcBonuses("8") not modelled
        "Haungry For Gold Talent": 0,
        "Golden Apple Stamp": account.stamps["Golden Apple Stamp"].total_value,
        "Nutty Crafter Achievement": 5 * achievements["Nutty Crafter"]["Complete"],
        "Shimmeron Bubble": 0,
        "Emoji Veggie Sigil": sigil_value * sigil_multi,
        "Yumi Peachring Meal": account.meals["Yumi Peachring"].value,
        "Beanbie Major Star Sign": 0,
        "Gold from Lead Bribe": account.bribes["Gold from Lead"].bonus,
        "Gumm Stick Pristine Charm": (
            account.sneaking.pristine_charms["Gumm Stick"].value
        ),
        "Beanstacker Achievements": (
            2 * achievements["Beanstacker Trainee"]["Complete"]
            + 3 * achievements["Beanstacker Prodigy"]["Complete"]
        ),
        "Ballot": (
            account.ballot[26].value
            * account.ballot[26].active
        ),
        "Apocalypse Wow Talent": 0,
        "Purp Mushroom Companion": companions["Purp Mushroom"].bonus,
        "Midusian Appetite Legend Talent": (
            account.legend_talents["Midusian Appetite"].value
        ),
        "Bort The Cornhusk Card": min(4 * card_levels.get("cropfallEvent1", 0), 50),
        "IdleOn 5th Anniversary Card": min(5 * card_levels.get("anni5Event1", 0), 50),
        "Vanillie Companion": companions["Vanillie"].bonus,
        "Verminous Companion": companions.get_value("Verminous", "Gold Food Effect"),
        "24 Karat Foods Vault": account.vault.upgrades["24 Karat Foods"].total_value,
        "Jelly Obstructions": (
            obstructions["Spinine"].bonus_value
            + obstructions["Smooth Stone"].bonus_value
        ),
    }

    multis = {}
    for character in account.all_characters:
        apoc_level = account.get_best_talent_level(
            apocalypse_wow_talent_index, character
        )
        seraph_multi = (
            get_seraph_cosmos_multi(cultism_level, character.summoning_level)
            if seraph_unlocked
            else 1
        )
        multis[character.character_index] = GoldenFoodMulti(outer, family, sources | {
            "Haungry For Gold Talent": character.get_talent_value(
                haungry_for_gold_talent_index
            ),
            "Shimmeron Bubble": account.alchemy_bubbles.get_class_bubble_value(
                character.base_class, "Shimmeron"
            ),
            "Beanbie Major Star Sign": beanbie.value_for(
                character, 20, infinite_levels, seraph_multi
            ),
            "Apocalypse Wow Talent": lava_func(
                apoc_talent["funcX"], apoc_level, apoc_talent["x1"], apoc_talent["x2"]
            ) * wow_maps,
        })
    return multis
