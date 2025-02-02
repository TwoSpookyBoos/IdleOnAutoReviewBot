import collections
import functools
import math

from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import gaming_progressionTiers, break_you_best

logger = get_logger(__name__)

def getSnailResetTarget(snail_rank):
    if snail_rank == 0:
        return 0 # Can't actually happen, but...
    if snail_rank < 5:
        return 1 # Special case
    return snail_rank - snail_rank % 5

# Cache the info since iteration is involved (up to ~0.035 seconds)
@functools.cache
def getSnailLevelUpInfo(final_ballad_bonus, target_confidence_levels):
    MAX_SNAIL_LEVEL = 25

    def success_chance(snail_level, encouragement):
        return min(1,
                   (1 - 0.1 * snail_level ** 0.72) * (1 + 100 * encouragement / (25 + encouragement) / 100) * final_ballad_bonus)

    def reset_chance(snail_level, encouragement):
        return max(0,
                   ((snail_level + 1) ** 0.07 - 1) / (1 + 300 * encouragement / (100 + encouragement) / 100))

    reset_target = getSnailResetTarget

    def compute_best_encouragements():
        cost_to_level = {}

        def test_encouragement(level, encourage):
            s_chance = success_chance(level, encourage)
            r_chance = reset_chance(level, encourage)

            true_r_chance = (1-s_chance) * r_chance
            r_return_cost = cost_to_level[reset_target(level), level]
            r_cost = r_return_cost + encourage
            expected_tries_to_success = 1 / s_chance
            expected_attempt_cost = 3 * expected_tries_to_success
            expected_r_cost = true_r_chance * r_cost* expected_tries_to_success

            return encourage + expected_attempt_cost + expected_r_cost

        encouragements = {}

        for level in range(MAX_SNAIL_LEVEL):
            cost_to_level[level, level] = 0

            base = test_encouragement(level, 0)
            encourage = 0
            while True:
                test = test_encouragement(level, encourage+1)
                if test < base:
                    base = test
                    encourage += 1
                else:
                    break

            encouragements[level] = encourage

            cost_to_level[reset_target(level), level+1] = cost_to_level[reset_target(level), level] + base

        return encouragements

    encouragements = compute_best_encouragements()

    def compute_safety_limits(start):
        targets = sorted(target_confidence_levels)

        levels_to_check = range(reset_target(start), start+2)

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
                if level+1 >= start:
                    # Don't count encouragement, this is good enough!
                    probabilities[mail_used+3, level+1] += success
                else:
                    next_encourage = encouragements[level+1]
                    probabilities[mail_used+3+next_encourage, level+1] += success

                reset = fail * r_chance
                fail = fail * (1 - r_chance) # Just a failure

                # Standard failure
                probabilities[mail_used+3, level] += fail

                # Reset
                probabilities[mail_used+3, reset_target(level)] += reset

            while targets and overall_safety_chance >= targets[0]:
                yield targets.pop(0), mail_used, overall_safety_chance

            mail_used += 1

    encouragement_info = {}

    for level in range(MAX_SNAIL_LEVEL):
        encourage = encouragements[level]
        encouragement_info[level] = (encourage,
                                     success_chance(level, encourage),
                                     reset_chance(level, encourage))

    safety_limits = {}
    for level in range(MAX_SNAIL_LEVEL):
        for target_confidence, mail, safety_chance in compute_safety_limits(level):
            safety_limits[level, target_confidence] = (mail, safety_chance)

    return encouragement_info, safety_limits

def getSnailInformationGroup():
    snail_AdviceDict = {
        "General": [],
        "Leveling Info": [],
    }

    sodium_level = session_data.account.atom_collider["Atoms"]["Sodium - Snail Kryptonite"]["Level"]
    snail_rank = session_data.account.gaming["Imports"]["Snail"]["SnailRank"]
    sodium_safety_level = sodium_level * 5

    if sodium_safety_level + 5 <= snail_rank:
        snail_AdviceDict["General"].append(Advice(
            label="Sodium too low to safely level the snail any further!",
            picture_class="gaming", # Placeholder
        ))
    else:
        final_ballad_acquired = session_data.account.caverns["Schematics"]["Final Ballad of the Snail"]["Purchased"]
        num_trebel_notes = session_data.account.caverns["Caverns"]["The Harp"]["NotesOwned"][3]

        final_ballad_bonus = 1.0

        if final_ballad_acquired:
            num_trebel_stacks = int(math.log10(num_trebel_notes) if num_trebel_notes > 0 else 0)
            final_ballad_bonus = 1 + 0.04 * num_trebel_stacks

            snail_AdviceDict["General"].append(Advice(
                label=f"Final Ballad of the Snail acquired! {num_trebel_stacks} trebel note stacks for a bonus of {final_ballad_bonus:0.2f}x",
                picture_class="gaming", # Placeholder
            ))
        else:
            snail_AdviceDict["General"].append(Advice(
                label="Final Ballad of the Snail is NOT acquired",
                picture_class="gaming", # Placeholder
            ))

        TARGET_CONFIDENCE_LEVELS = (0.95, 0.99, 0.999)

        encouragement_info, safety_thresholds = getSnailLevelUpInfo(final_ballad_bonus,
                                                                    TARGET_CONFIDENCE_LEVELS)

        min_snail_rank = getSnailResetTarget(snail_rank)
        target_snail_rank = min(max(encouragement_info.keys()),
                                sodium_safety_level+4)

        for level in range(min_snail_rank, target_snail_rank+1):
            num_encourage, s_chance, r_chance = encouragement_info[level]

            snail_AdviceDict["Leveling Info"].append(Advice(
                label=f"Level {level}: {num_encourage} encouragements ({s_chance:0.2%} success chance, {r_chance:0.2%} reset chance)",
                picture_class="gaming", # Placeholder
            ))

            # TODO: This doesn't explain what the "safety limit" means!
            safety_msg = []
            for target_confidence in TARGET_CONFIDENCE_LEVELS:
                mail_needed, overall_chance = safety_thresholds[level, target_confidence]
                safety_msg.append(f"{mail_needed} mail for {target_confidence:.1%}")
            safety_msg = f"Safety limits for {level}: {', '.join(safety_msg)}"

            snail_AdviceDict["Leveling Info"].append(Advice(
                label=safety_msg,
                picture_class="gaming", # Placeholder
            ))

    snail_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Snail Information",
        advices=snail_AdviceDict,
        informational=True
    )
    return snail_AdviceGroup

def getGamingProgressionTierAdviceGroups():
    gaming_AdviceDict = {}
    gaming_AdviceGroupDict = {}
    info_tiers = 0
    max_tier = max(gaming_progressionTiers.keys()) - info_tiers

    # Generate AdviceGroups (none right now!)

    overall_SectionTier = min(max_tier + info_tiers, 0)
    return gaming_AdviceGroupDict, overall_SectionTier, max_tier

def getGamingAdviceSection() -> AdviceSection:
    highestGamingSkillLevel = max(session_data.account.all_skills.get("Gaming", [0]))
    if highestGamingSkillLevel < 1:
        gaming_AdviceSection = AdviceSection(
            name="Gaming",
            tier="0",
            pinchy_rating=0,
            header="Come back after unlocking the Gaming skill in W5!",
            picture="Gaming.png",
            unreached=True
        )
        return gaming_AdviceSection

    # Generate AdviceGroup
    gaming_AdviceGroupDict, overall_SectionTier, max_tier = getGamingProgressionTierAdviceGroups()
    gaming_AdviceGroupDict["Snail"] = getSnailInformationGroup()

    max_tier = 1

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    gaming_AdviceSection = AdviceSection(
        name="Gaming",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Gaming tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Gaming.png",
        groups=gaming_AdviceGroupDict.values()
    )

    return gaming_AdviceSection
