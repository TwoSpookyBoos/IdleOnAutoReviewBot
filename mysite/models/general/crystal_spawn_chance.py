from consts.consts_autoreview import ValueToMulti
from consts.general.crystal_spawn_chance import (
    crystals_4_dayys_max,
    non_predatory_box_max,
)
from consts.idleon.consts_idleon import base_crystal_chance
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from models.general.cards import Card
from models.general.characters import Characters


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
        characters: Characters,
        crescent_shrine_value: float,
        *,
        moai_head_level: int,
        max_book_level: int,
    ):
        self.moai_head_level = moai_head_level
        self.max_book_level = max_book_level
        self.crescent_shrine_value = crescent_shrine_value
        self.best_cmon_out_book = 0
        for jman in characters.jmans:
            self.best_cmon_out_book = max(
                self.best_cmon_out_book, jman.max_talents.get("26", 0)
            )
        self.crystals_4_dayys_max_multi = 1 + lava_func(*crystals_4_dayys_max) / 100
        self.non_predatory_box_max_value = lava_func(*non_predatory_box_max)
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

    def get_moai_head_advice(self) -> Advice:
        return Advice(
            label="{{ Sailing|#sailing }}: Moai Head artifact to apply Shrines "
            "everywhere",
            picture_class="moai-head",
            progression=self.moai_head_level,
            goal=1,
        )

    def get_cmon_out_crystals_advice(self) -> Advice:
        return Advice(
            label=f"Level {self.best_cmon_out_book}/{self.max_book_level} booked "
            f"Cmon Out Crystals talent (Jman only)",
            picture_class="cmon-out-crystals",
            progression=self.best_cmon_out_book,
            goal=self.max_book_level,
        )

    def get_crystals_4_dayys_advice(self) -> Advice:
        return Advice(
            label=f"Crystals 4 Dayys star talent: {self.crystals_4_dayys_max_multi}x "
            f"at level 100",
            picture_class="crystals-4-dayys",
        )

    def get_non_predatory_box_advice(self) -> Advice:
        return Advice(
            label=f"Non Predatory Loot Box: +{self.non_predatory_box_max_value:.0f}% "
            f"at 400 crates",
            picture_class="non-predatory-loot-box",
        )

    def get_additive_note_advice(self) -> Advice:
        shrine_and_box = 1 + (
            (self.crescent_shrine_value + self.non_predatory_box_max_value) / 100
        )
        return Advice(
            label=f"Note: Crescent Shrine and PO Box are additive: "
            f"{shrine_and_box:.3f}x"
            f"<br>The cards also add together. Everything else is a unique multiplier.",
            picture_class="shrine-box2",
        )

    def get_highest_advice(self) -> Advice:
        return Advice(
            label=f"Best Crystal Spawn Chance on Non-Jman:"
            f" {self.highest * 100:.4f}%"
            f" (1 in {100 / (self.highest * 100):.2f})",
            picture_class="crystal-carrot",
        )

    def get_highest_jman_advice(self) -> Advice:
        return Advice(
            label=f"Best Crystal Spawn Chance on Jman:"
            f" {self.highest_jman * 100:.4f}%"
            f" (1 in {100 / (self.highest_jman * 100):.2f})",
            picture_class="crystal-crabal",
        )
