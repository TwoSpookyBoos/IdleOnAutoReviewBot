import sys
from math import ceil, floor

from consts.consts_general import cards_max_level
from models.advice.advice import Advice
from models.general.character import Character


class Card:
    def __init__(self, codename, name, cardset, count, coefficient, value_per_level, description):
        self.codename = codename
        self.count = ceil(float(count))
        self.cardset = cardset
        self.name = name
        self.coefficient = coefficient
        self.star = self.getStars()
        self.level = self.star + 1 if self.count > 0 else 0
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
