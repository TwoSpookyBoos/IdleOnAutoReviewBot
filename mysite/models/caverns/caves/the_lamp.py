from math import floor

from consts.caverns.caves.the_lamp import lamp_wishes
from consts.consts_autoreview import EmojiType
from consts.idleon.caverns.caves.the_lamp import lamp_world_wish_values
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.number_formatting import parse_number
from utils.safer_data_handling import safer_convert, safer_math_pow


class LampWish:
    def __init__(
        self,
        index: int,
        details: dict,
        level: float,
        unlocked: bool,
        wishes_stored: float,
        cavern_image: str,
    ):
        self.index = index
        self.name = details["Name"]
        self.base_cost = details["BaseCost"]
        self.cost_increaser = details["CostIncreaser"]
        self.image = f"lamp-wish-{index}"
        self.level = level
        self.unlocked = unlocked
        self.wishes_stored = wishes_stored
        self._cavern_image = cavern_image

        self.value_list = self._value_list()

        cost = (
            ". Cost does not increase." if details["DoesCostIncrease"] is False else ""
        )
        self.description = f"{details['Description']}{cost}"
        for placeholder, value in zip("{}~", self.value_list):
            self.description = self.description.replace(placeholder, str(value), 1)

        self.next_cost = self._next_cost()

    def _value_list(self) -> list[float]:
        if not self.name.startswith("World "):
            return []
        world_number = safer_convert(self.name.split("World ")[1][0], 0)
        return [
            value * self.level
            for value in lamp_world_wish_values.get(world_number, [0, 0, 0])
        ]

    def _next_cost(self) -> int:
        # `_customBlock_Holes "LampWishCost"` in source. Last updated in v2.43 Nov 6
        match self.index:
            case 0:  # New Wish Type
                if 11 > self.level:
                    return floor(1 + (2 * self.level) + safer_math_pow(self.level, 2))
                return 999999
            case 2:  # Opal
                return floor(1 + (2 * self.level) + safer_math_pow(self.level, 1.7))
            case _:  # Everything else
                return floor(self.base_cost + (self.level * self.cost_increaser))

    def get_advice(self) -> Advice:
        return Advice(
            label=f"Level {self.level} {self.name}: {self.description}",
            picture_class=self.image,
            progression=self.wishes_stored,
            goal=self.next_cost,
        )

    def get_bonus_advice(self, value_index: int) -> Advice:
        """For display outside The Lamp's own advice_groups(), e.g. as a
        contributor to some other cross-cutting total."""
        assert self.value_list, f"{self.name} has no per-level value_list"
        value = self.value_list[value_index]
        return Advice(
            label=f"{{{{Lamp|#glowshroom-tunnels}}}} Wish: {self.name}: +{value}%",
            picture_class=self._cavern_image,
            progression=value,
            goal=EmojiType.INFINITY.value,
        )


class TheLamp(Cavern):
    def __init__(self):
        super().__init__(name="The Lamp", cavern_number=7)

    def parse(self, raw_caverns_list: list):
        try:
            self.wishes_stored = raw_caverns_list[11][25]
        except Exception:
            self.wishes_stored = 0
        try:
            polonai_level: int = raw_caverns_list[1][0]
        except Exception:
            polonai_level = 0
        cavern_unlocked = polonai_level >= self.cavern_number
        try:
            wish_types_unlocked: int = raw_caverns_list[21][0] + (1 * cavern_unlocked)
        except Exception:
            wish_types_unlocked = 1 * cavern_unlocked

        self.wishes: dict[str, LampWish] = {}
        for index, details in enumerate(lamp_wishes):
            try:
                wish_unlocked = wish_types_unlocked > index
                level = parse_number(raw_caverns_list[21][index])
            except Exception:
                wish_unlocked = False
                level = 0
            wish = LampWish(
                index=index,
                details=details,
                level=level,
                unlocked=wish_unlocked,
                wishes_stored=self.wishes_stored,
                cavern_image=self.image,
            )
            self.wishes[wish.name] = wish

    def advice_groups(self) -> dict[str, list[Advice]]:
        return {
            "Cavern Stats": [
                self.objective_advice(
                    "Collect Wishes upon Daily Reset to invest into Wish Types",
                    resource="lamp-wish-button",
                ),
                self.opals_found_advice(),
            ],
            "FAQs": [
                Advice(
                    label=(
                        "Gold Pocketwatches DO NOT grant Wishes!"
                        "<br>Silver Pocketwatches do."
                    ),
                    picture_class="gold-pocketwatch",
                    resource="silver-pocketwatch",
                ),
            ],
            "Wish Type Stats": [
                Advice(
                    label=f"Wishes stored: {self.wishes_stored}",
                    picture_class="lamp-wish-button",
                ),
                *[wish.get_advice() for wish in self.wishes.values()],
            ],
        }
