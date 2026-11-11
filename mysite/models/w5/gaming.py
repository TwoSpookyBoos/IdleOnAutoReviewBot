import collections
from functools import cache, cached_property

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
@cache
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
    def __init__(self, gaming: "Gaming", raw_snail: list, envelopes: int):
        self.gaming = gaming
        self.level: int = safer_index(raw_snail, 0, 0)
        self.rank: int = safer_index(raw_snail, 1, 0)
        self.encouragements: int = safer_index(raw_snail, 2, 0)
        self.envelopes: int = envelopes

    @cached_property
    def max_rank(self) -> int:
        max_rank = snail_base_max_rank + sum(
            bonus_levels
            for superbit_name, bonus_levels in snail_superbit_ranks
            if self.gaming.superbits[superbit_name].unlocked
        )
        # Don't try impossible ranks
        return min(max_rank, snail_max_possible_rank)

    @property
    def maxed(self) -> bool:
        return self.rank >= self.max_rank

    @cached_property
    def sodium_safety_level(self) -> int:
        # Depends on: atom_collider['Sodium - Snail Kryptonite']
        from models.general.session_data import session_data

        atom = session_data.account.atom_collider["Sodium - Snail Kryptonite"]
        return atom.level * 5

    @property
    def sodium_too_low(self) -> bool:
        return self.sodium_safety_level + 5 <= self.rank

    @cached_property
    def _final_ballad_multi(self) -> float:
        # Depends on: caverns.villagers['Kaipu'].schematics
        from models.general.session_data import session_data

        schematics = session_data.account.caverns.villagers["Kaipu"].schematics
        return schematics["Final Ballad of the Snail"].as_multi

    @property
    def _can_level_up(self) -> bool:
        return self.rank > 0 and not self.maxed and not self.sodium_too_low

    # Read only by advice methods that check _can_level_up first
    @property
    def _level_up_info(self) -> tuple[dict, dict]:
        return get_snail_level_up_info(
            self._final_ballad_multi, snail_target_confidence_levels
        )

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
            label=f"Envelopes owned: {self.envelopes}",
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

    def _get_encouragement_advice(self, level: int, label_prefix: str) -> Advice:
        encouragement_info, _ = self._level_up_info
        num_encourage, s_chance, r_chance = encouragement_info[level]
        return Advice(
            label=f"{label_prefix}: Encourage the snail {num_encourage} times."
            f"<br>Game will display {s_chance:0.2%} success, {r_chance:0.2%} "
            f"reset chance at {num_encourage} encourages.",
            picture_class="immortal-snail",
            progression=self.encouragements if level == self.rank else 0,
            goal=num_encourage,
            resource="snail-envelope",
        )

    def get_level_up_advices(self) -> list[Advice]:
        if not self._can_level_up:
            return []
        encouragement_info, _ = self._level_up_info
        num_encourage, _, _ = encouragement_info[self.rank]
        advices = [self._get_encouragement_advice(self.rank, "Step 1")]
        if self.rank > snail_first_consecration_rank and num_encourage > 0:
            advices.append(
                self._get_step_2_advice(
                    "Feel free to try a level up, you're protected by consecration! "
                    "(Remember to encourage again if it fails and resets)",
                    goal=num_encourage,
                )
            )
        else:
            advices.extend(self._get_safety_advices())
        return advices

    def get_relevant_encouragement_advices(self) -> list[Advice]:
        if not self._can_level_up:
            return []
        min_rank = get_snail_reset_target(self.rank)
        target_rank = min(self.sodium_safety_level + 5, self.max_rank)
        advices = []
        for level in range(min_rank, target_rank):
            if level < self.rank:
                rank_type = "Previous"
            elif level > self.rank:
                rank_type = "Future"
            else:
                rank_type = "Current"
            advices.append(
                self._get_encouragement_advice(level, f"{rank_type} Rank {level}")
            )
        return advices

    def _get_step_2_advice(self, label: str, goal: int) -> Advice:
        encouragement_info, _ = self._level_up_info
        num_encourage, _, _ = encouragement_info[self.rank]
        encouragements_short_by = max(0, num_encourage - self.encouragements)
        return Advice(
            label=f"Step 2: {label}",
            picture_class="snail-envelope",
            progression=max(0, self.envelopes - encouragements_short_by),
            goal=goal,
        )

    def _get_safety_advices(self) -> list[Advice]:
        _, safety_thresholds = self._level_up_info
        advices = []
        levels = snail_target_confidence_levels
        for target_idx, target_confidence in enumerate(levels):
            mail_needed, _ = safety_thresholds[self.rank, target_confidence]
            if target_idx + 1 < len(levels):
                next_confidence = levels[target_idx + 1]
                next_mail_needed, _ = safety_thresholds[self.rank, next_confidence]
                # Skip a level that needs no more mail than the next one
                if mail_needed == next_mail_needed:
                    continue
            advices.append(
                self._get_step_2_advice(
                    f"Choose a safety level. {target_confidence:.1%} "
                    f"safety = {mail_needed} unspent mail",
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
        envelopes = 0
        unlocked_codes = ""
        if len(raw_gaming) >= 14:
            self.fertilizer_value = raw_gaming[1]
            self.fertilizer_speed = raw_gaming[2]
            unlocked_codes = str(raw_gaming[12])
            envelopes = safer_convert(raw_gaming[13], 0)

        self.superbits: dict[str, SuperBit] = {
            name: SuperBit(name, info, unlocked_codes)
            for name, info in gaming_superbits_dict.items()
        }

        # [32] = Snail Import
        raw_sprouts = safe_loads(raw_data.get("GamingSprout", []))
        self.snail: Snail = Snail(self, safer_index(raw_sprouts, 32, []), envelopes)
