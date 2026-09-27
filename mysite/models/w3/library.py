from math import floor

from consts.consts_general import getNextESFamilyBreakpoint
from models.advice.advice import Advice
from models.general.achievements import Achievements
from models.general.merits import Merits
from models.w3.atom_collider import AtomCollider
from models.w3.buildings import Buildings
from models.w5.sailing import Sailing
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class BonusTalentSource:
    def __init__(
        self, value: float, image: str, label: str, progression: int, goal: int
    ):
        self.value: float = value
        self.image: str = image
        self.label: str = label
        self.progression: int = progression
        self.goal: int = goal

    def get_advice(self, complete: bool | None = None) -> Advice:
        return Advice(
            label=self.label,
            picture_class=self.image,
            progression=self.progression,
            goal=self.goal,
            complete=complete,
        )


class Library:
    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        self.books_ready: int = safer_convert(safer_index(raw_optlacc, 55, 0), 0)  # convert: used in maths
        self.static_sum: int = 0
        self.scaling_sum: int = 0
        self.max_book_level: int = 100
        self.bonus_talents: dict[str, BonusTalentSource] = {}

    def calculate_max_book_levels(
        self, construction_buildings: Buildings, achievements: Achievements, atom_collider: AtomCollider,
        sailing: Sailing, merits: Merits, saltlick, summoning
    ):
        self.static_sum = (
            0
            + (25 * (0 < construction_buildings['Talent Book Library'].level))
            + (5 * achievements['Checkout Takeout'].complete)
            + (10 * (0 < atom_collider['Oxygen - Library Booker'].level))
            + (25 * sailing.artifacts['Fury Relic'].level)
        )
        self.scaling_sum = (
            0
            + 2 * merits[2][2].level
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

    @property
    def account_wide_bonus_talents(self) -> int:
        return sum(int(source.value) for source in self.bonus_talents.values())

    def calculate_bonus_talents(
        self, armor_sets, companions, family_bonuses, equinox, achievements: Achievements,
        sneaking, grimoire, tesseract
    ):
        kattlekruk = armor_sets['KATTLEKRUK SET']
        rift_slug = companions['Rift Slug']
        es_family = family_bonuses['Elemental Sorcerer']
        symbols = equinox.upgrades['Equinox Symbols']
        maroon_warship = achievements['Maroon Warship'].complete
        sneaking_mastery = 5 if sneaking.unlocked_mastery >= 3 else 0
        skull = grimoire.upgrades['Skull of Major Talent']
        universe_talent = tesseract.upgrades['Universe Talent']
        self.bonus_talents = {
            'Kattelkruk Set': BonusTalentSource(
                kattlekruk.total_value,
                kattlekruk.image,
                f"{{{{Set bonus|#armor-sets}}}}: Kattlekruk Set: "
                f"+{kattlekruk.total_value:g}/{kattlekruk.base_value:g}",
                int(kattlekruk.owned),
                1,
            ),
            'Rift Slug': BonusTalentSource(
                rift_slug.bonus,
                'rift-slug',
                f"Companion: Rift Slug: +{rift_slug.bonus:g}/{rift_slug.value:g}",
                int(companions.has('Rift Slug')),
                1,
            ),
            'ES Family': BonusTalentSource(
                floor(es_family.value),
                'elemental-sorcerer-icon',
                f"ES Family Bonus: +{floor(es_family.value)}.<br>Next increase at Class Level: ",
                es_family.level,
                getNextESFamilyBreakpoint(es_family.level),
            ),
            'Equinox Symbols': BonusTalentSource(
                symbols.level,
                'equinox-symbols',
                f"{{{{ Equinox|#equinox }}}}: Equinox Symbols: +{symbols.level}/{symbols.final_max_level}",
                symbols.level,
                symbols.final_max_level,
            ),
            'Maroon Warship': BonusTalentSource(
                1 * maroon_warship,
                'maroon-warship',
                f"W5 Achievement: Maroon Warship: +{1 * maroon_warship}/1",
                1 if maroon_warship else 0,
                1,
            ),
            'Sneaking Mastery': BonusTalentSource(
                sneaking_mastery,
                'sneaking-mastery',
                f"{{{{ Rift|#rift }}}}: Sneaking Mastery: +{sneaking_mastery}/5 (Mastery III)",
                sneaking.unlocked_mastery,
                3,
            ),
            'Grimoire': BonusTalentSource(
                skull.level,
                skull.image,
                f"{{{{Grimoire|#the-grimoire}}}}: Skull of Major Talent: +{skull.level}/{skull.max_level}",
                skull.level,
                skull.max_level,
            ),
            'Universe Talent': BonusTalentSource(
                min(5, universe_talent.total_value),
                universe_talent.image,
                f"{{{{Tesseract|#the-tesseract}}}}: Universe Talent: "
                f"+{min(5, universe_talent.total_value):g}/{universe_talent.max_level}",
                universe_talent.level,
                universe_talent.max_level,
            ),
        }
