import math

from consts.consts_autoreview import ValueToMulti
from consts.consts_w3 import printer_all_indexes_being_printed
from consts.consts_w5 import goldrelic_multis_dict
from consts.idleon.consts_idleon import skill_index_list
from consts.idleon.lava_func import lava_func
from consts.w3.printer import (
    biggole_mole_max_days,
    gold_relic_default_max_days,
    gold_relic_max_days,
    harriep_output_multi,
    king_of_the_remembered_talent,
    moon_of_print_max_days,
    skill_mastery_base_output,
    skill_mastery_output_level,
    supreme_wiring_max_days,
    wired_in_output_multi,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_get
from utils.text_formatting import getItemDisplayName

logger = get_logger(__name__)


class Printer:
    def __init__(self, raw_data: dict):
        # Stored samples, best first
        self.samples: dict[str, list[float]] = {}
        self.printing: dict[str, list] = {}

        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.gold_relic_days: int = safer_get(raw_optlacc, 125, 0)
        self.supreme_wiring_days: int = safer_get(raw_optlacc, 323, 0)
        self.biggole_mole_days: int = safer_get(raw_optlacc, 354, 0)
        self.moon_of_print_days: int = safer_get(raw_optlacc, 364, 0)

        raw_print = safe_loads(raw_data.get("Print", [0, 0, 0, 0, 0, "Blank"]))[5:]
        raw_printer_xtra = safe_loads(raw_data.get("PrinterXtra", []))
        sample_names = raw_print[0::2] + raw_printer_xtra[0:119:2]
        sample_values = raw_print[1::2] + raw_printer_xtra[1:119:2]

        for sample_index, codename in enumerate(sample_names):
            if not codename:
                continue
            name = getItemDisplayName(codename)
            if sample_index in printer_all_indexes_being_printed:
                values = self.printing.setdefault(name, [])
                try:
                    values.append(sample_values[sample_index])
                except IndexError:
                    logger.exception(f"Failed on sample {sample_index} '{codename}'")
            elif codename != "Blank":
                values = self.samples.setdefault(name, [])
                try:
                    values.append(float(sample_values[sample_index]))
                except (IndexError, TypeError, ValueError):
                    logger.exception(f"Failed on sample {sample_index} '{codename}'")
        for values in self.samples.values():
            values.sort(reverse=True)

    def calculate_sample_rate(
        self,
        *,
        snow_slurry: float,
        sample_it: float,
        salt_lick_level: int,
        merit_level: int,
        merit_max_level: int,
        maestro_family: float,
        stample: float,
        amplestample: float,
        arcade_bonus: float,
        saharan_skull: bool,
        max_book_level: int,
        characters,
    ):
        self.snow_slurry = snow_slurry
        self.salt_lick_level = salt_lick_level
        self.merit_level = merit_level
        self.merit_max_level = merit_max_level
        self.saharan_skull = saharan_skull
        self.max_book_level = max_book_level
        self.star_talent_one_point = lava_func("bigBase", 1, 10, 0.075)
        account_sum = 0.0
        account_sum += snow_slurry
        account_sum += sample_it
        account_sum += 0.5 * salt_lick_level
        account_sum += 0.5 * merit_level
        account_sum += maestro_family
        account_sum += stample
        account_sum += amplestample
        account_sum += arcade_bonus
        account_sum += saharan_skull
        account_sum += self.star_talent_one_point
        self.account_sample_rate = account_sum

        self.star_talent_diff_to_max = (
            lava_func("bigBase", 100, 10, 0.075) - self.star_talent_one_point
        )
        character_sum = 0.0
        character_sum += self.star_talent_diff_to_max
        character_sum += lava_func("decay", 400, 5, 200)
        self.character_sample_rate_max = character_sum
        self.squire_super_samples = lava_func("decay", max_book_level, 9, 75)
        self.character_sample_rates = {}
        for char in characters:
            total = (
                account_sum
                + self.star_talent_diff_to_max
                + char.po_boxes_invested["Utilitarian Capsule"].bonus_1_value
            )
            if char.sub_class == "Squire":
                total += self.squire_super_samples
            self.character_sample_rates[char.character_index] = total

    def calculate_output(
        self,
        *,
        skill_mastery_unlocked: bool,
        all_skills: dict[str, list[int]],
        gold_relic_level: int,
        supreme_wiring_owned: bool,
        biggole_mole_bonus: float,
        moon_of_print,
        death_bringers: list,
        max_book_level: int,
        king_of_the_remembered_kills: int,
        lolly_flower: float,
        ballot_multi: float,
        has_king_doot: bool,
        wired_in_enabled: bool,
        harriep_unlocked: bool,
    ):
        self.has_king_doot = has_king_doot
        self.skill_mastery_base = skill_mastery_base_output * skill_mastery_unlocked
        # Combat excluded
        self.skill_mastery_eligible = len(skill_index_list) - 1
        self.skill_mastery_bonus = sum(
            [
                1
                for name, levels in all_skills.items()
                if name != "Combat" and sum(levels) >= skill_mastery_output_level
            ]
        )
        self.skill_mastery_multi = ValueToMulti(
            self.skill_mastery_base + self.skill_mastery_bonus
        )

        self.gold_relic_level = gold_relic_level
        self.gold_relic_max_days = gold_relic_max_days.get(
            gold_relic_level, gold_relic_default_max_days
        )
        self.gold_relic_multi = ValueToMulti(
            self.gold_relic_days * goldrelic_multis_dict.get(gold_relic_level, 0)
        )

        self.supreme_wiring_counted_days = min(
            supreme_wiring_max_days, self.supreme_wiring_days
        )
        self.supreme_wiring_multi = ValueToMulti(
            self.supreme_wiring_counted_days * 2 * supreme_wiring_owned
        )
        biggole_mole_days = min(biggole_mole_max_days, self.biggole_mole_days)
        self.biggole_mole_multi = ValueToMulti(biggole_mole_days * biggole_mole_bonus)
        self._moon_of_print = moon_of_print
        self.moon_of_print_counted_days = min(
            moon_of_print_max_days, self.moon_of_print_days
        )
        self.moon_of_print_multi = ValueToMulti(
            moon_of_print_max_days * moon_of_print.unlocked * moon_of_print.total_value
        )

        self._calculate_king_of_the_remembered(
            death_bringers, max_book_level, king_of_the_remembered_kills
        )
        charm_multi = ValueToMulti(lolly_flower)
        self.lab_multi_aw = wired_in_output_multi if has_king_doot else 1
        self.lab_multi_cs = wired_in_output_multi if wired_in_enabled else 1
        self.harriep_multi_aw = harriep_output_multi if has_king_doot else 1
        self.harriep_multi_cs = harriep_output_multi if harriep_unlocked else 1
        self.account_output_multi = (
            1
            * self.skill_mastery_multi
            * self.gold_relic_multi
            * self.king_of_the_remembered_multi
            * charm_multi
            * ballot_multi
            * self.lab_multi_aw
            * self.harriep_multi_aw
            * self.supreme_wiring_multi
            * self.biggole_mole_multi
            * self.moon_of_print_multi
        )
        self.character_output_multi = self.lab_multi_cs * self.harriep_multi_cs

    def _calculate_king_of_the_remembered(
        self, death_bringers: list, max_book_level: int, kills: int
    ):
        talent = king_of_the_remembered_talent
        self.any_dk_max_booked = False
        self.any_dk_max_leveled = False
        best_book = 0
        best_preset_level = 0
        for dk in death_bringers:
            levels_above_max = dk.max_talents_over_books - max_book_level
            if dk.max_talents.get(talent, 0) >= max_book_level:
                self.any_dk_max_booked = True
            if dk.max_talents.get(talent, 0) > best_book:
                best_book = dk.max_talents.get(talent, 0)
            if (
                dk.current_preset_talents.get(talent, 0) >= max_book_level
                or dk.secondary_preset_talents.get(talent, 0) >= max_book_level
            ):
                self.any_dk_max_leveled = True
            if dk.current_preset_talents.get(talent, 0) >= best_preset_level:
                best_preset_level = (
                    dk.current_preset_talents.get(talent, 0) + levels_above_max
                )
            if dk.secondary_preset_talents.get(talent, 0) >= best_preset_level:
                best_preset_level = (
                    dk.secondary_preset_talents.get(talent, 0) + levels_above_max
                )
        self.king_of_the_remembered_talent_value = lava_func(
            "decay", best_preset_level, 5, 150
        )
        self.king_of_the_remembered_log_kills = math.log(kills, 10) if kills > 0 else 0
        self.king_of_the_remembered_multi = max(
            1,
            ValueToMulti(
                self.king_of_the_remembered_talent_value
                * self.king_of_the_remembered_log_kills
            ),
        )

    def get_salt_lick_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Salt Lick|#salt-lick }}}} bonus: "
            f"+{round(0.5 * self.salt_lick_level, 2):g}/10%",
            picture_class="salt-lick",
            progression=self.salt_lick_level,
            goal=20,
        )

    def get_merit_advice(self) -> Advice:
        return Advice(
            label=f"W3 merit: "
            f"+{round(0.5 * self.merit_level, 1):g}/{0.5 * self.merit_max_level:.0f}%",
            picture_class="merit-2-4",
            progression=self.merit_level,
            goal=self.merit_max_level,
        )

    def get_saharan_skull_advice(self) -> Advice:
        return Advice(
            label=f"W3 Achievement: Saharan Skull: {int(self.saharan_skull)}/1%",
            picture_class="saharan-skull",
            progression=int(self.saharan_skull),
            goal=1,
        )

    def get_star_talent_advice(self) -> Advice:
        return Advice(
            label=f"Star Talent: Printer Sampling: {self.star_talent_one_point:.3f}% "
            f"at minimum level 1",
            picture_class="printer-sampling",
            progression=1,
            goal=1,
        )

    def get_star_talent_max_advice(self) -> Advice:
        return Advice(
            label=f"Star Talent: Printer Sampling: Additional "
            f"{self.star_talent_diff_to_max:.2f}% at max level 100",
            picture_class="printer-sampling",
            progression=1,
            goal=1,
        )

    def get_super_samples_advice(self) -> Advice:
        return Advice(
            label=f"Squire only: Super Samples: +{self.squire_super_samples:.2f}% "
            f"at max book level {self.max_book_level}",
            picture_class="super-samples",
        )

    def get_wired_in_advice(self) -> Advice:
        doot = (
            "2x (Thanks Doot!)"
            if self.has_king_doot
            else "2x if connected to Lab/Arctis"
        )
        return Advice(
            label=f"Lab Bonus: Wired In: {doot}",
            picture_class="wired-in",
            progression=self.lab_multi_aw if self.has_king_doot else "",
            goal=2,
            unit="x",
            completed=self.has_king_doot,
        )

    def get_harriep_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Divinity|#divinity }}}}: Harriep Major Link bonus: "
            f"{'3x (Thanks Doot!)' if self.has_king_doot else '3x if linked'}",
            picture_class="harriep",
            progression=self.harriep_multi_aw if self.has_king_doot else "",
            goal=3,
            unit="x",
            completed=self.has_king_doot,
        )

    def get_skill_mastery_advice(self) -> Advice:
        max_multi = ValueToMulti(
            skill_mastery_base_output + self.skill_mastery_eligible
        )
        return Advice(
            label=f"{{{{Rift|#rift}}}}: Skill Mastery unlocked: "
            f"{self.skill_mastery_base}/{skill_mastery_base_output}%"
            f"<br>Additional 1% per Skill at {skill_mastery_output_level}: "
            f"{self.skill_mastery_bonus}/{self.skill_mastery_eligible}%",
            picture_class="skill-mastery",
            progression=f"{self.skill_mastery_multi:.2f}",
            goal=f"{max_multi:.2f}",
            unit="x",
        )

    def get_king_of_the_remembered_advice(self) -> Advice:
        max_booked = "<br>Not max booked!" if not self.any_dk_max_booked else ""
        max_preset = (
            "<br>Not max leveled in any preset!" if not self.any_dk_max_leveled else ""
        )
        breakdown = (
            f"<br>({self.king_of_the_remembered_talent_value:.3f} talent * "
            f"{self.king_of_the_remembered_log_kills:.3f} pow10 kills)"
            if self.any_dk_max_booked and self.any_dk_max_leveled
            else ""
        )
        return Advice(
            label=f"DK's King of the Remembered: "
            f"{self.king_of_the_remembered_multi:.3f}x"
            f"{max_booked}{max_preset}{breakdown}",
            picture_class="king-of-the-remembered",
            resource="orb-of-remembrance",
            progression=f"{self.king_of_the_remembered_multi:.3f}",
            unit="x",
        )

    def get_gold_relic_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Sailing|#sailing}}}}: "
            f"Level {self.gold_relic_level} Gold Relic:"
            f"<br>{self.gold_relic_multi:.2f}x "
            f"({self.gold_relic_days}/{self.gold_relic_max_days} days)",
            picture_class="gold-relic",
            progression=self.gold_relic_days,
            goal=self.gold_relic_max_days,
        )

    def get_supreme_wiring_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Event Shop|#event-shop}}}}: Supreme Wiring:"
            f"<br>{self.supreme_wiring_multi:.2f}x "
            f"({self.supreme_wiring_counted_days}/{supreme_wiring_max_days} days)",
            picture_class="event-shop-4",
            progression=self.supreme_wiring_counted_days,
            goal=supreme_wiring_max_days,
        )

    def get_moon_of_print_advice(self) -> Advice:
        mop = self._moon_of_print
        return Advice(
            label=f"{{{{Compass|#the-compass}}}}: {mop.path_name}-{mop.path_ordering}: "
            f"Moon of Print: "
            f"<br>{self.moon_of_print_multi:.2f}x "
            f"({self.moon_of_print_counted_days}/{moon_of_print_max_days} days)",
            picture_class=mop.image,
            progression=self.moon_of_print_counted_days,
            goal=moon_of_print_max_days,
        )

    def best_sample(self, name: str) -> float:
        return max(self.samples.get(name) or [0])

    def is_printing(self, name: str) -> bool:
        return name in self.printing
