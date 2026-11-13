import sys
from dataclasses import dataclass
from functools import cached_property
from math import ceil, floor

from consts.consts_autoreview import ValueToMulti
from consts.consts_general import (
    card_raw_data,
    cards_max_level,
    cardset_names,
    key_cards,
)
from consts.consts_monster_data import decode_monster_name
from consts.consts_w3 import approx_max_talent_level_star_talents
from consts.general.cards import (
    base_card_drop_chance,
    base_player_max_card_stars,
    card_champ_bubble_goal,
    cardiovascular_max_level,
    max_8ball_keychain_card_drop_chance,
    max_obol_card_drop_chance,
    pokaminni_card_drop_chance,
)
from models.advice.advice import Advice
from models.general.character import Character
from models.general.session_data import session_data
from models.general.talents import talents
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.safer_data_handling import safe_loads, safer_get

logger = get_logger(__name__)


class Card:
    def __init__(
        self,
        codename,
        name,
        cardset,
        count,
        coefficient,
        value_per_level,
        description,
        min_level: int = 0
    ):
        self.codename = codename
        self.count = ceil(float(count))
        self.cardset = cardset
        self.name = name
        self.coefficient = coefficient
        # "CardLv" in source: OptLacc floors apply even unowned.
        # Last updated in v2.531.0
        self.star = max(self.getStars(), min_level - 1)
        self.level = self.star + 1 if self.count > 0 or min_level > 0 else 0
        self.css_class = name + " Card"
        self.diff_to_next = (
            ceil(self.getCardsForStar(self.star + 1)) or sys.maxsize
        ) - self.count
        self.value_per_level = value_per_level
        self.description = description
        self.max_level = cards_max_level

    def getStars(self):
        return next(
            (
                i
                for i in range(cards_max_level-1, -1, -1)
                if self.count >= round(self.getCardsForStar(i))
            ),
            -1,
        )

    def getCardsForStar(self, star):
        """
        0 stars always requires 1 card.
        1 star is set per enemy.
        2 stars = 3x additional what 1star took, for a total of 1+3 = 4x (2^2).
        3 stars = 5x additional what 1star took, for a total of 4+5 = 9x (3^2).
        4 stars = 16x additional what 1star took, for a total of 9+16 = 25x (5^2).
        5 stars = 459x additional what 1star took, for a total of 25+459 = 484x (22^2).
        6 stars = 14,670x additional what 1star took, for a total of 484+14,670 = 15,129x  (123^2).
        7 stars = 496x additional what 1star took, for a total of 15,129+496 = 15,625x (125^2).
        """
        if star == 0:
            return 1
        previous_star = star - 1
        if self.name == 'Chaotic Chizoar':
            tier_coefficient = previous_star + 1 + floor(previous_star/3)
            # `_customBlock_RunCodeOfTypeXforThingY , CardLv==e` in source. Last updated in v2.43 Nov 11
            # The formula in the code includes `*1.5` at the end. That's the self.coefficient for Chaotic Chizoar
            # which is accounted for below in the total_cards_needed. Adding it again here will give bad answers.
        else:
            tier_coefficient = previous_star + 1 + (floor(previous_star/3) + (16 * floor(previous_star/4) + 100 * floor(previous_star/5)))
        total_cards_needed = (self.coefficient * tier_coefficient**2) + 1
        # print(f"{star} star {self.name} needs {total_cards_needed:,} cards [({self.coefficient} * {tier_coefficient}^2) + 1]")
        return total_cards_needed

    def getCardDoublerMultiplier(self, optional_character: Character=None):
        card_doubler = 1
        if optional_character and optional_character.equipped_card_doublers and self.codename in optional_character.equipped_cards_codenames:
            equipped_slot = optional_character.equipped_cards_codenames.index(self.codename)
            if (equipped_slot == 0 and "Omega Nanochip" in optional_character.equipped_card_doublers) or (equipped_slot == 7 and "Omega Motherboard" in optional_character.equipped_card_doublers):
                card_doubler = 2
        return card_doubler

    def getCurrentValue(self, optional_character: Character=None):
        return self.level * self.value_per_level * self.getCardDoublerMultiplier(optional_character)

    def getMaxValue(self, optional_character: Character=None):
        return cards_max_level * self.value_per_level * self.getCardDoublerMultiplier(optional_character)

    def getFormattedXY(self, optional_character: Character=None):
        result = (
            f"{'+' if '+' in self.description else ''}"
            + f"{self.getCurrentValue(optional_character):.3g}/{self.getMaxValue(optional_character):.3g}"
            + f"{'%' if '%' in self.description else ''}"
            + f"{self.description.replace('+{', '').replace('%', '')}"
        )
        return result

    def getAdvice(self, optional_starting_note='', optional_ending_note='', optional_character: Character=None):
        a = Advice(
            label=f"{optional_starting_note}{' ' if optional_starting_note else ''}{self.cardset}- {self.name} card:<br>{self.getFormattedXY(optional_character)}"
                  f"{'<br>' if optional_ending_note else ''}{optional_ending_note}",
            picture_class=self.css_class,
            progression=self.level,
            goal=self.max_level,
        )
        return a

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.name}, {self.count}, {self.star}-star]"


@dataclass
class CardSetProgress:
    stars_sum: int
    star: int
    stars_over: int
    next_star_sum: int
    maxed: bool

    @property
    def rank(self) -> int:
        return self.star + self.maxed


class CardSet(list[Card]):
    def __init__(self, name: str, cards: list[Card]):
        super().__init__(sorted(cards, key=lambda card: card.diff_to_next))
        self.name = name

    def get_progress(self, max_stars: int) -> CardSetProgress:
        stars_sum = sum(min(card.star, max_stars) + 1 for card in self)
        star, stars_over = divmod(stars_sum, len(self))
        star = min(star, max_stars)
        next_star_sum = (star + 1) * len(self)
        # 96/96 Blunder Hills, for instance
        maxed = stars_sum == next_star_sum
        return CardSetProgress(stars_sum, star, stars_over, next_star_sum, maxed)


class Cards(list[Card]):
    def __init__(self, raw_data: dict, characters: list[Character]):
        card_counts = safe_loads(raw_data.get(key_cards, {}))
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        # "OptionsListAccount"[603]/[155] in source: card level floors.
        # Last updated in v2.531.0
        min_7_cards = set(f"{safer_get(raw_optlacc, 603, '')}".split(','))
        min_6_cards = set(f"{safer_get(raw_optlacc, 155, '')}".split(','))

        cards_by_name: dict[str, Card] = {}
        unknown_cards = []
        for cardset_index, cardset_details in enumerate(card_raw_data):
            if cardset_index < len(cardset_names):
                cardset_name = cardset_names[cardset_index]
            else:
                logger.warning(f"No name found for Card Set Index {cardset_index}!")
                cardset_name = f"UnknownSet-{cardset_index}"
            for card_info in cardset_details:
                # ["mushG", "A0", "5", "+{_Base_HP", "12"]
                codename = card_info[0]
                if codename == 'Blank':
                    continue
                name = decode_monster_name(codename, card=True)
                if name.startswith('Unknown'):
                    unknown_cards.append(card_info)
                cards_by_name[name] = Card(
                    codename=codename,
                    name=name,
                    cardset=cardset_name,
                    count=safer_get(card_counts, codename, 0),
                    coefficient=parse_number(card_info[2], 1.0),
                    value_per_level=parse_number(card_info[4], 0.0),
                    description=card_info[3].replace('_', ' '),
                    min_level=(
                        7 if codename in min_7_cards
                        else 6 if codename in min_6_cards
                        else 0
                    ),
                )
        if unknown_cards:
            logger.error(f"Unknown Card name(s) found: {unknown_cards}")
        super().__init__(cards_by_name.values())

        cards_by_codename: dict[str, Card] = {}
        for card in self:
            cards_by_codename.setdefault(card.codename, card)
        for character in characters:
            for codename in character.equipped_cards_codenames:
                if codename in cards_by_codename:
                    character.equipped_cards.append(cards_by_codename[codename])
                else:
                    logger.warning(f"Unknown equipped_card_codename: {codename}. Skipping")

        cards_by_set: dict[str, list[Card]] = {}
        for card in self:
            cards_by_set.setdefault(card.cardset, []).append(card)
        self.cardsets: dict[str, CardSet] = {
            name: CardSet(name, cards) for name, cards in cards_by_set.items()
        }

    def named(self, name: str) -> Card:
        return next(card for card in self if card.name == name)

    @cached_property
    def player_max_card_stars(self) -> int:
        # Depends on: rift['RubyCards'], spelunk.caves['Rustbelt 03']
        account = session_data.account
        return (
            base_player_max_card_stars
            + (1 * account.rift["RubyCards"].unlocked)
            + (1 * account.spelunk.caves["Rustbelt 03"].bonus_obtained)
        )

    @cached_property
    def cardset_progress(self) -> dict[str, CardSetProgress]:
        return {
            name: cardset.get_progress(self.player_max_card_stars)
            for name, cardset in self.cardsets.items()
        }

    @cached_property
    def cardset_rank_total(self) -> int:
        return sum(progress.rank for progress in self.cardset_progress.values())

    @cached_property
    def _cards_galore_bonus(self) -> float:
        # JMAN ONLY
        return talents["Cards Galore"].value_at_level(
            approx_max_talent_level_star_talents
        )

    @cached_property
    def _drop_chance_multis(self) -> dict[str, float]:
        # Depends on: bribes['Five Aces in the Deck'], star_signs['Pokaminni'],
        # alchemy_vials['Anearful (Glublin Ear)'], stamps['Card Stamp'],
        # guild_bonuses['C2 Card Spotter'], alchemy_bubbles['Card Champ']
        account = session_data.account
        cardiovascular = talents["Cardiovascular!"].value_at_level(
            cardiovascular_max_level
        )
        cardiovascular_multi = round(ValueToMulti(cardiovascular), 2)
        pokaminni_unlocked = account.star_signs["Pokaminni"].unlocked
        # Summed left to right in this order; Cards Galore goes after Card Stamp
        before_cards_galore = (
            account.bribes["Five Aces in the Deck"].bonus
            + int(pokaminni_unlocked) * pokaminni_card_drop_chance
            + 5 * self.named("Gigafrog").level
            + 8 * self.named("Snelbie").level
            + 9 * self.named("Sir Stache").level
            + 1 * self.named("Egggulyte").level
            + account.alchemy_vials["Anearful (Glublin Ear)"].value
            + account.stamps["Card Stamp"].total_value
        )
        card_spotter = account.guild_bonuses["C2 Card Spotter"].value
        max_equipment_bonus = (
            max_obol_card_drop_chance + max_8ball_keychain_card_drop_chance
        )
        card_champ_bubble = account.alchemy_bubbles["Card Champ"].base_value
        return {
            # Multi Group A: all other bonuses
            "A": round(
                (
                    before_cards_galore
                    + card_spotter
                    + max_equipment_bonus
                    + card_champ_bubble
                )
                / 100,
                2,
            ),
            "A Jman": round(
                (
                    before_cards_galore
                    + self._cards_galore_bonus
                    + card_spotter
                    + max_equipment_bonus
                    + card_champ_bubble
                )
                / 100,
                2,
            ),
            # Multi Group B: Cardiovascular
            "B": cardiovascular_multi,
        }

    def get_drop_chance_advices(self) -> dict[str, list[Advice]]:
        account = session_data.account
        multis = self._drop_chance_multis
        total = round(base_card_drop_chance + multis["A"] * multis["B"], 2)
        total_jman = round(base_card_drop_chance + multis["A Jman"] * multis["B"], 2)
        return {
            f"Total: {total}x ({total_jman}x if Jman)": [
                Advice(
                    label=f"Total Card Drop Chance bonus: {total}x "
                    f"({total_jman}x if Jman)",
                    picture_class="dementia-obol-of-cards",
                )
            ],
            "Base Chance: +20%": [
                Advice(
                    label="Passive +20% bonus. Not multiplied by other Multi Groups",
                    picture_class="",
                )
            ],
            f"Multi Group A: {multis['A']}x ({multis['A Jman']}x if Jman)": [],
            "Multi Group A - account-wide": [
                account.bribes["Five Aces in the Deck"].get_bonus_advice(),
                account.alchemy_vials["Anearful (Glublin Ear)"].get_advice(
                    full_name=False
                ),
                account.stamps["Card Stamp"].get_advice(),
                account.alchemy_bubbles["Card Champ"].get_bonus_advice(
                    goal=card_champ_bubble_goal
                ),
                account.guild_bonuses["C2 Card Spotter"].get_advice(),
            ],
            "Multi Group A - character-specific": [
                self.named("Gigafrog").getAdvice(),
                self.named("Snelbie").getAdvice(),
                self.named("Sir Stache").getAdvice(),
                self.named("Egggulyte").getAdvice(),
                self._get_pokaminni_advice(),
                Advice(
                    label=f"Full Card Drop Chance Obols: "
                    f"+{max_obol_card_drop_chance}%<br>Both personal and family, "
                    f"all rerolled for +1% Card Drop Chance",
                    picture_class="dementia-obol-of-cards",
                ),
                Advice(
                    label="2x 8 Ball Keychains: 2x +10%",
                    picture_class="x8-ball-chain",
                ),
            ],
            "Multi Group A - class-specific": [
                Advice(
                    label=f"Cards Galore Talent: +{self._cards_galore_bonus:.2f}% "
                    f"if maxed (Jman only)",
                    picture_class="cards-galore",
                )
            ],
            f"Multi Group B: {multis['B']}x (character-specific)": [
                Advice(
                    label=f'Star Talent "Cardiovascular!": {multis["B"]}x if maxed',
                    picture_class="cardiovascular",
                )
            ],
        }

    def _get_pokaminni_advice(self) -> Advice:
        unlocked = session_data.account.star_signs["Pokaminni"].unlocked
        status = (
            f"+{pokaminni_card_drop_chance}% if equipped" if unlocked else "Locked."
        )
        return Advice(
            label=f"{{{{ Star Signs|#star-signs }}}} - Pokaminni: {status}",
            picture_class="pokaminni",
            progression=int(unlocked),
            goal=1,
        )
