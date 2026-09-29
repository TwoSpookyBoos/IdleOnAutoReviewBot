from consts.consts_autoreview import EmojiType, ValueToMulti
from consts.w7.coral_reef import coral_reef_bonus_data
from models.advice.advice import Advice
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import (
    safe_loads,
    safer_convert,
    safer_index,
    safer_math_pow,
)


class CoralReefBonus:
    def __init__(self, index: int, info: dict, unlocked: bool, level: int):
        self.name = info["Name"]
        self.description = info["Description"]
        self.max_level = info["Max Level"]
        self.image = f"coral-{index}"
        self.unlocked = unlocked
        self.level = level
        self.next_cost = int(
            info["Coefficient"] * safer_math_pow(info["Exponent Base"], self.level, 0)
        )

    def get_advice(self) -> Advice:
        unlock_or_upgrade_text = "Level up" if self.unlocked else "Unlock"
        next_level_cost_text = (
            f"<br>Next level costs {self.next_cost} corals"
            if self.unlocked and self.level < self.max_level
            else ""
        )
        return Advice(
            label=(
                f"{unlock_or_upgrade_text} {self.name}: {self.description}"
                f"{next_level_cost_text}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource="coral",
        )


class CoralReef(dict[str, CoralReefBonus]):
    def __init__(self, raw_data: dict):
        raw_spelunk = safe_loads(raw_data.get("Spelunk", []))
        self.town_corals = safer_convert(
            safer_index(safer_index(raw_spelunk, 4, []), 5, 0), 0
        )

        unlocked_reef_corals = safer_index(raw_spelunk, 12, [])
        coral_levels = safer_index(raw_spelunk, 13, [])

        for index, info in enumerate(coral_reef_bonus_data):
            unlocked = bool(safer_index(unlocked_reef_corals, index, False))
            level = safer_index(coral_levels, index, 0)
            bonus = CoralReefBonus(index, info, unlocked, level)
            self[bonus.name] = bonus

        self.total_level = sum(bonus.level for bonus in self.values())

    def calculate_daily_corals(
        self,
        *,
        shellslug_multi: float,
        coolral_owned: bool,
        more_coral_owned: int,
        coral_kid: float,
        dancing_coral: float,
        clam_work_level: int,
        killroy_coral_level: int,
        corale_stamp: float,
        scale_on_ice: float,
        coral_restoration: float,
        arcade_bonus: float,
        coral_conservationism: float,
        demonblub_card: float,
        coral_statue,
    ):
        # `"ReefDayGains" == e` in source. Last updated in v2.46 Dec 7
        self.base_daily_corals = 10
        # Groups A-C
        self.shellslug_multi = shellslug_multi
        self.coolral_owned = coolral_owned
        self.coolral_multi = 1 + 0.3 * coolral_owned
        self.more_coral_multi = 1 + 0.2 * more_coral_owned
        # Group D
        self.clam_work_level = clam_work_level
        self.clam_work_value = 20 if clam_work_level > 5 else 0
        self.killroy_coral_level = killroy_coral_level
        self.killroy_coral_value = round_and_trim(
            killroy_coral_level / (250 + killroy_coral_level) * 25, 0
        )
        self._coral_statue = coral_statue
        self.multi_group_d_value = sum(
            (
                coral_kid,
                dancing_coral,
                self.clam_work_value,
                self.killroy_coral_value,
                corale_stamp,
                scale_on_ice,
                coral_restoration,
                arcade_bonus,
                coral_conservationism,
                demonblub_card,
                coral_statue.value,
            )
        )
        self.multi_group_d_mult = ValueToMulti(self.multi_group_d_value)
        self.total_daily_corals = (
            self.base_daily_corals
            * self.shellslug_multi
            * self.coolral_multi
            * self.more_coral_multi
            * self.multi_group_d_mult
        )

    def get_base_daily_corals_advice(self) -> Advice:
        return Advice(
            label=f"Base daily corals: {self.base_daily_corals}",
            picture_class="coral",
            completed=True,
        )

    def get_coolral_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Event Shop|#event-shop }}}} - Coolral: "
            f"x{self.coolral_multi}/x1.3 Daily Corals",
            resource="event-point",
            picture_class="event-shop-25",
            progression=int(self.coolral_owned),
            goal=1,
        )

    def get_clam_work_advice(self) -> Advice:
        return Advice(
            label=f"Clam Work: +{self.clam_work_value}% Daily Corals past level 5",
            picture_class="clam-pearl",
            progression=self.clam_work_level,
            goal=6,
        )

    def get_killroy_advice(self) -> Advice:
        return Advice(
            label=f"Killroy: +{self.killroy_coral_value:g}% Daily Corals",
            picture_class="killroy-skull",
            progression=self.killroy_coral_level,
            goal=EmojiType.INFINITY.value,
        )

    def get_coral_statue_advice(self) -> Advice:
        statue = self._coral_statue
        gold_note = "(must be at least gold)" if statue.type == "Normal" else ""
        return Advice(
            label=f"Level {statue.level} Coral Statue: +{statue.value:.2f}% "
            f"{gold_note}",
            picture_class=statue.image,
            progression=statue.level,
            goal=EmojiType.INFINITY.value,
        )
