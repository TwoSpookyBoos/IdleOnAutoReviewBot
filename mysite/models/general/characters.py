from consts.idleon.consts_idleon import max_characters
from models.general.character import Character
from utils.data_formatting import getCharacterDetails


class Characters(list[Character]):
    def __init__(self, raw_data: dict, run_type: str):
        _, self.names, _, character_details, self.all_skills = getCharacterDetails(
            raw_data, run_type
        )
        super().__init__(
            Character(raw_data, **char) for char in character_details.values()
        )
        # Use this if touching raw_data instead of all characters
        self.safe: list[Character] = [char for char in self if char]
        self.safe_indexes: list[int] = [char.character_index for char in self.safe]
        self.classes: set[str] = {
            class_name
            for char in self
            for class_name in char.all_classes
            if class_name != "None"
        }
        # All characters created and none can/went down the Secret Class path
        self.no_beginners: bool = (
            not self._with_class("Beginner", "Journeyman")
            and len(self) >= max_characters
        )
        self.jmans: list[Character] = self._with_class("Journeyman")
        self.maestros: list[Character] = self._with_class("Maestro")
        self.vmans: list[Character] = self._with_class("Voidwalker")
        self.barbs: list[Character] = self._with_class("Barbarian")
        self.bbs: list[Character] = self._with_class("Blood Berserker")
        self.dbs: list[Character] = self._with_class("Death Bringer")
        self.dks: list[Character] = self._with_class("Divine Knight")
        self.mages: list[Character] = self._with_class("Mage")
        self.bubos: list[Character] = self._with_class("Bubonic Conjuror")
        self.acs: list[Character] = self._with_class("Arcane Cultist")
        self.wws: list[Character] = self._with_class("Wind Walker")

    def calculate_bonus_talent_levels(
        self,
        *,
        account_wide_bonus: int,
        account_wide_arctis: bool,
        big_p_value: float,
        coral_kid_level: float,
        timmy_talented: bool,
        max_book_level: int,
        es_family_value: float,
        spelunk,
        super_talent_levels: int,
    ):
        for char in self.safe:
            char.calculate_bonus_talent_levels(
                account_wide_bonus,
                account_wide_arctis or char.isArctisLinked(),
                big_p_value,
                coral_kid_level,
                timmy_talented,
                max_book_level,
                es_family_value,
            )
            char.active_super_talents = spelunk.get_super_talents(
                char.character_index, char.active_talent_preset
            )
            # Character has no account access
            char.super_talent_levels = super_talent_levels

    def _with_class(self, *class_names: str) -> list[Character]:
        return [
            char
            for char in self
            if any(class_name in char.all_classes for class_name in class_names)
        ]
