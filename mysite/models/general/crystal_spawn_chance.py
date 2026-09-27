from consts.consts_autoreview import ValueToMulti
from consts.idleon.consts_idleon import base_crystal_chance
from models.general.cards import Card
from models.general.character import Character


class CrystalSpawnChance:
    def __init__(self):
        self.account_wide: float = base_crystal_chance
        self.highest: float = base_crystal_chance
        self.highest_jman: float = base_crystal_chance

    def calculate(
        self,
        poop_card: Card,
        genie_card: Card,
        omega_chips_owned: int,
        crystallin_stamp_value: float,
        characters: list[Character],
        crescent_shrine_value: float,
    ):
        # Assumes the Shrine bonus and the Star Talent are maxed
        poop_value = 10 * (1 + poop_card.getStars())
        genie_value = 15 * (1 + genie_card.getStars())
        # Each Omega chip doubles the stronger remaining card
        if omega_chips_owned >= 2:
            card_chance = 2 * (poop_value + genie_value)
        elif omega_chips_owned == 1:
            card_chance = 2 * max(poop_value, genie_value) + min(
                poop_value, genie_value
            )
        else:
            card_chance = poop_value + genie_value
        self.account_wide = (
            base_crystal_chance
            * ValueToMulti(crystallin_stamp_value)
            * ValueToMulti(card_chance)
        )
        for char in characters:
            char.calculate_crystal_spawn_chance(
                self.account_wide, crescent_shrine_value
            )
        self.highest = max(
            (
                char.crystal_spawn_chance
                for char in characters
                if "Journeyman" not in char.all_classes
            ),
            default=base_crystal_chance,
        )
        self.highest_jman = max(
            (
                char.crystal_spawn_chance
                for char in characters
                if "Journeyman" in char.all_classes
            ),
            default=base_crystal_chance,
        )
