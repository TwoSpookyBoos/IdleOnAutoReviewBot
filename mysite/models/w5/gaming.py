import collections
import functools
import math

from consts.consts_autoreview import EmojiType
from consts.consts_w5 import (
    gaming_superbits_dict,
    snail_first_consecration_rank,
    snail_max_possible_rank,
)
from consts.w5.gaming import (
    snail_base_max_rank,
    snail_superbit_ranks,
    snail_target_confidence_levels,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index

logger = get_logger(__name__)


class SuperBit:
    def __init__(self, name: str, info: dict, unlocked_codes: str):
        self.name: str = name
        self.bonus_text: str = info["BonusText"]
        self.unlocked: bool = info["CodeString"] in unlocked_codes


def get_snail_reset_target(snail_rank):
    if snail_rank == 0:
        return 0  # Can't actually happen, but...
    else:
        return max(1, snail_rank - snail_rank % 5)


# Cache the info since iteration is involved in the computation
@functools.cache
def get_snail_level_up_info(final_ballad_bonus, target_confidence_levels):
    def success_chance(snail_level, encouragement):
        if snail_level < snail_first_consecration_rank:
            return min(
                1,
                (1 - 0.1 * snail_level**0.71)
                * (1 + 110 * encouragement / (25 + encouragement) / 100)
                * final_ballad_bonus,
            )
        else:
            return min(
                1,
                (1 - 0.6 * (snail_level - 24) ** 0.16)
                * (1 + 50 * encouragement / (3 + encouragement) / 100)
                * final_ballad_bonus,
            )

    def reset_chance(snail_level, encouragement):
        if snail_level < snail_first_consecration_rank:
            return max(
                0,
                ((snail_level + 1) ** 0.07 - 1)
                / (1 + 300 * encouragement / (100 + encouragement) / 100),
            )
        else:
            return max(
                0,
                ((snail_level - 24) ** 0.19 - 0.9)
                / (1 + 60 * encouragement / (3 + encouragement) / 100),
            )

    def level_up_cost(snail_level):
        return 3 if snail_level < snail_first_consecration_rank else 5

    def encouragement_cost(snail_level):
        return 1 if snail_level < snail_first_consecration_rank else 30

    reset_target = get_snail_reset_target

    def compute_best_encouragements():
        cost_to_level = {}

        def test_encouragement(level, encourage):
            s_chance = success_chance(level, encourage)
            r_chance = reset_chance(level, encourage)

            true_r_chance = (1 - s_chance) * r_chance
            if level >= snail_first_consecration_rank and encourage > 0:
                r_cost = encouragement_cost(level)
            else:
                r_return_cost = cost_to_level[reset_target(level), level]
                r_cost = r_return_cost + encourage * encouragement_cost(level)
            expected_tries_to_success = 1 / s_chance
            expected_attempt_cost = level_up_cost(level) * expected_tries_to_success
            expected_r_cost = true_r_chance * r_cost * expected_tries_to_success

            return (
                encourage * encouragement_cost(level)
                + expected_attempt_cost
                + expected_r_cost
            )

        encouragements = {}

        for level in range(snail_max_possible_rank):
            cost_to_level[level, level] = 0

            base = test_encouragement(level, 0)
            encourage = 0
            while True:
                test = test_encouragement(level, encourage + 1)
                if test < base:
                    base = test
                    encourage += 1
                else:
                    break

            encouragements[level] = encourage

            cost_to_level[reset_target(level), level + 1] = (
                cost_to_level[reset_target(level), level] + base
            )

        return encouragements

    encouragements = compute_best_encouragements()

    def compute_safety_limits(start):
        targets = sorted(target_confidence_levels)

        if start >= snail_first_consecration_rank and encouragements[start] > 0:
            # Consecrated: nothing to simulate, it's guaranteed safe
            for t in targets:
                yield t, level_up_cost(start), 1
            return

        levels_to_check = range(reset_target(start), start + 2)

        probabilities = collections.defaultdict(float)
        probabilities[0, start] = 1

        overall_safety_chance = 0
        mail_used = 0

        while targets:
            for level in levels_to_check:
                prob = probabilities.pop((mail_used, level), 0)
                if prob == 0:
                    continue

                if level >= start and mail_used > 0:
                    overall_safety_chance += prob
                    continue

                encourage = encouragements[level]
                s_chance = success_chance(level, encourage)
                r_chance = reset_chance(level, encourage)

                # Try one
                success = prob * s_chance
                fail = prob * (1 - s_chance)

                # Success
                if level + 1 >= start:
                    # Don't count encouragement, this is good enough!
                    probabilities[mail_used + level_up_cost(level), level + 1] += (
                        success
                    )
                else:
                    next_encourage = encouragements[level + 1] * encouragement_cost(
                        level
                    )
                    probabilities[
                        mail_used + level_up_cost(level) + next_encourage, level + 1
                    ] += success

                reset = fail * r_chance
                fail = fail * (1 - r_chance)  # Just a failure

                # Standard failure
                probabilities[mail_used + level_up_cost(level), level] += fail

                # Reset
                probabilities[
                    mail_used + level_up_cost(level), reset_target(level)
                ] += reset

            while targets and overall_safety_chance >= targets[0]:
                yield targets.pop(0), mail_used, overall_safety_chance

            mail_used += 1

    encouragement_info = {}

    for level in range(snail_max_possible_rank):
        encourage = encouragements[level]
        encouragement_info[level] = (
            encourage,
            success_chance(level, encourage),
            reset_chance(level, encourage),
        )

    safety_limits = {}
    for level in range(snail_max_possible_rank):
        for target_confidence, mail, safety_chance in compute_safety_limits(level):
            safety_limits[level, target_confidence] = (mail, safety_chance)

    return encouragement_info, safety_limits


class Snail:
    def __init__(self, raw_snail: list):
        self.level: int = safer_index(raw_snail, 0, 0)
        self.rank: int = safer_index(raw_snail, 1, 0)
        self.encouragements: int = safer_index(raw_snail, 2, 0)

    def calculate(
        self,
        *,
        envelopes,
        superbits: dict,
        sodium_level: int,
        treble_notes: float,
        final_ballad,
    ):
        self.floored_envelopes = safer_convert(envelopes, 0)
        self.sodium_safety_level = sodium_level * 5
        self.max_rank = snail_base_max_rank
        for superbit_name, bonus_levels in snail_superbit_ranks:
            if superbits[superbit_name].unlocked:
                self.max_rank += bonus_levels
        # Don't try impossible ranks
        self.max_rank = min(self.max_rank, snail_max_possible_rank)
        self.maxed = self.rank >= self.max_rank
        self.sodium_too_low = self.sodium_safety_level + 5 <= self.rank

        self._final_ballad = final_ballad
        self.final_ballad_bonus = 1.0
        self.treble_stacks = 0
        if final_ballad.bought:
            self.treble_stacks = int(
                math.log10(treble_notes) if treble_notes > 0 else 0
            )
            self.final_ballad_bonus = 1 + 0.04 * self.treble_stacks

        self.encouragement_info = {}
        self.safety_thresholds = {}
        self.min_rank = 0
        self.target_rank = 0
        self.encouragements_short_by = 0
        if self.rank > 0 and not self.maxed and not self.sodium_too_low:
            self.encouragement_info, self.safety_thresholds = get_snail_level_up_info(
                self.final_ballad_bonus, snail_target_confidence_levels
            )
            self.min_rank = get_snail_reset_target(self.rank)
            self.target_rank = min(
                max(self.encouragement_info.keys()) + 1,
                self.sodium_safety_level + 5,
                self.max_rank,
            )
            num_encourage = self.encouragement_info[self.rank][0]
            self.encouragements_short_by = max(0, num_encourage - self.encouragements)

    def get_rank_advice(self) -> Advice:
        return Advice(
            label=(
                f"Current Snail Rank: {self.rank}"
                if self.level > 0
                else "Snail import not yet unlocked"
            ),
            picture_class="immortal-snail",
            progression=self.rank,
            goal=snail_max_possible_rank,
        )

    def get_envelopes_advice(self) -> Advice:
        return Advice(
            label=f"Envelopes owned: {self.floored_envelopes}",
            picture_class="snail-envelope",
        )

    def get_maxed_advice(self) -> Advice:
        return Advice(
            label="Snail rank is currently maxed, unlock more in superbits",
            picture_class="bits",
        )

    def get_sodium_too_low_advice(self) -> Advice:
        return Advice(
            label="{{ Sodium|#atom-collider }} too low to safely level the Snail "
            "any further!",
            picture_class="sodium",
        )

    def get_final_ballad_advice(self) -> Advice:
        if self._final_ballad.bought:
            return Advice(
                label=f"<br>{self.treble_stacks} Trebel Note stacks for a bonus of "
                f"{self.final_ballad_bonus:0.2f}x",
                picture_class=self._final_ballad.image,
                progression=self.treble_stacks,
                goal=EmojiType.INFINITY.value,
                resource="harp-note-3",
            )
        return Advice(
            label="{{ Schematic|#villagers }}: Final Ballad of the Snail is NOT "
            "acquired",
            picture_class=self._final_ballad.image,
            progression=0,
            goal=1,
        )

    def get_encouragement_advice(self, level: int, label_prefix: str) -> Advice:
        num_encourage, s_chance, r_chance = self.encouragement_info[level]
        return Advice(
            label=f"{label_prefix}: Encourage the snail {num_encourage} times."
            f"<br>Game will display {s_chance:0.2%} success, {r_chance:0.2%} "
            f"reset chance at {num_encourage} encourages.",
            picture_class="immortal-snail",
            progression=self.encouragements if level == self.rank else 0,
            goal=num_encourage,
            resource="snail-envelope",
        )

    def get_consecrated_advice(self) -> Advice:
        num_encourage = self.encouragement_info[self.rank][0]
        return Advice(
            label="Step 2: Feel free to try a level up, you're protected by "
            "consecration! (Remember to encourage again if it fails and resets)",
            picture_class="snail-envelope",
            progression=max(0, self.floored_envelopes - self.encouragements_short_by),
            goal=num_encourage,
        )

    def get_safety_advices(self) -> list[Advice]:
        advices = []
        levels = snail_target_confidence_levels
        for target_idx, target_confidence in enumerate(levels):
            mail_needed, overall_chance = self.safety_thresholds[
                self.rank, target_confidence
            ]
            # Skip a level that needs no more mail than the next one
            if (
                target_idx + 1 < len(levels)
                and mail_needed
                == self.safety_thresholds[self.rank, levels[target_idx + 1]][0]
            ):
                continue
            advices.append(
                Advice(
                    label=f"Step 2: Choose a safety level. {target_confidence:.1%} "
                    f"safety = {mail_needed} unspent mail",
                    picture_class="snail-envelope",
                    progression=max(
                        0, self.floored_envelopes - self.encouragements_short_by
                    ),
                    goal=mail_needed,
                )
            )
        return advices


class Gaming:
    def __init__(self, raw_data: dict):
        raw_gaming = safe_loads(raw_data.get("Gaming", []))
        if not raw_gaming:
            logger.warning("Gaming data not present")
        # Sometimes float, sometimes string
        self.bits_owned: float = safer_convert(safer_index(raw_gaming, 0, 0.0), 0.0)
        self.fertilizer_value = 0
        self.fertilizer_speed = 0
        self.envelopes = 0
        unlocked_codes = ""
        if len(raw_gaming) >= 14:
            self.fertilizer_value = raw_gaming[1]
            self.fertilizer_speed = raw_gaming[2]
            unlocked_codes = str(raw_gaming[12])
            self.envelopes = raw_gaming[13]

        self.superbits: dict[str, SuperBit] = {
            name: SuperBit(name, info, unlocked_codes)
            for name, info in gaming_superbits_dict.items()
        }

        # [32] = Snail Import
        raw_sprouts = safe_loads(raw_data.get("GamingSprout", []))
        self.snail: Snail = Snail(safer_index(raw_sprouts, 32, []))
