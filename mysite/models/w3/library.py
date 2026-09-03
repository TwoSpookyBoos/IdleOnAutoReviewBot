from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class Library:
    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        self.books_ready: int = safer_convert(safer_index(raw_optlacc, 55, 0), 0)  # convert: used in maths
        self.static_sum: int = 0
        self.scaling_sum: int = 0
        self.max_book_level: int = 100

    def calculate_max_book_levels(
        self, construction_buildings: dict, achievements: dict, atom_collider: dict,
        sailing: dict, merits: list, saltlick, summoning
    ):
        self.static_sum = (
            0
            + (25 * (0 < construction_buildings['Talent Book Library']['Level']))
            + (5 * achievements['Checkout Takeout']['Complete'])
            + (10 * (0 < atom_collider['Atoms']['Oxygen - Library Booker']['Level']))
            + (25 * sailing['Artifacts']['Fury Relic']['Level'])
        )
        self.scaling_sum = (
            0
            + 2 * merits[2][2]['Level']
            + 2 * saltlick.upgrades['Max Book'].level
        )
        self.max_book_level = (
            100 + self.static_sum + self.scaling_sum
            + summoning.bonuses["Library Max"].value
        )

    def get_checkout_alert_advice(self) -> Advice:
        return Advice(
            label=f"{self.books_ready // 20} perfect {{{{ checkouts|#library }}}} available",
            picture_class='talent-book-library',
        )
