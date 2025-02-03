from consts import labBonusesDict
from mysite.models.utils.Position import Position

class Bonus:
    BONUS_CLASSES = {
        0: "AnimalFarmBonus",
        8: "SpelunkerObolBonus",
        9: "FungiFingerBonus",
        11: "UnadulteratedBankingBonus",
        13: "ViralConnectionBonus",
        15: "SlabSovereigntyBonus",
        17: "DepotStudiesPhD",
    }

    def __new__(cls, bonus_id: int):
        """ Factory method that returns an instance of the appropriate subclass. """
        subclass = cls.BONUS_CLASSES.get(bonus_id, Bonus)
        return super().__new__(globals()[subclass]) if subclass in globals() else super().__new__(cls)

    def __init__(self, bonus_id: int):
        self.bonus_id = bonus_id
        bonus_data = labBonusesDict[bonus_id]
        self.name = bonus_data["Name"]
        self.description = bonus_data["Description"]
        self.position = Position(x=bonus_data["Coordinates"][0], y=bonus_data["Coordinates"][1])
        self.unlocked = bonus_id < 14
        self.active = False

    def get_range(self, connection_bonus: float, extra_px_from_bonuses: float):
        return int((80 * (1 + connection_bonus / 100)) + extra_px_from_bonuses)


class AnimalFarmBonus(Bonus):
    def __init__(self, bonus_id: int):
        super().__init__(bonus_id)
        self.total_species = 0

    def get_bonus_text(self):
        return self.description.replace("{", str(self.get_bonus()))

    def get_bonus(self):
        return self.bonus_on * self.total_species


class FungiFingerBonus(Bonus):
    def __init__(self, bonus_id: int):
        super().__init__(bonus_id)
        self.green_mushroom_killed = 0
        self.jewel_boost = 0

    def get_bonus_text(self):
        return self.description.replace("{", str(self.get_bonus()))

    def get_bonus(self):
        return (self.bonus_on + self.jewel_boost) * (self.green_mushroom_killed // 1e6)


class UnadulteratedBankingBonus(Bonus):
    def __init__(self, bonus_id: int):
        super().__init__(bonus_id)
        self.green_stacks = 0

    def get_bonus_text(self):
        return self.description.replace("{", str(self.get_bonus()))

    def get_bonus(self):
        return self.bonus_on * self.green_stacks


class ViralConnectionBonus(Bonus):
    def get_range(self):
        return 80


class SpelunkerObolBonus(Bonus):
    def __init__(self, bonus_id: int):
        super().__init__(bonus_id)
        self.jewel_boost = 0

    def get_range(self):
        return 80

    def get_bonus(self):
        return self.bonus_on + self.jewel_boost if self.active else self.bonus_off


class SlabSovereigntyBonus(Bonus):
    def __init__(self, bonus_id: int):
        super().__init__(bonus_id)
        self.jewel_boost = 0

    def get_bonus(self):
        return self.bonus_on + self.jewel_boost if self.active else self.bonus_off


class DepotStudiesPhD(Bonus):
    def __init__(self, bonus_id: int):
        super().__init__(bonus_id)
        self.jewel_boost = 0

    def get_bonus(self):
        return self.bonus_on + self.jewel_boost if self.active else self.bonus_off