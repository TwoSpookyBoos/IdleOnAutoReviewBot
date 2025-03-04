import collections
import functools
import math

from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import safer_convert
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import gaming_progressionTiers, break_you_best, infinity_string, snailMaxRank

logger = get_logger(__name__)

def getSnailResetTarget(snail_rank):
    if snail_rank == 0:
        return 0  # Can't actually happen, but...
    elif snail_rank < 5:
        return 1  # Special case
    else:
        return snail_rank - snail_rank % 5

# Cache the info since iteration is involved (up to ~0.035 seconds)
@functools.cache
def getSnailLevelUpInfo(final_ballad_bonus, target_confidence_levels):

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
            expected_r_cost = true_r_chance * r_cost * expected_tries_to_success

            return encourage + expected_attempt_cost + expected_r_cost

        encouragements = {}

        for level in range(snailMaxRank):
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

    for level in range(snailMaxRank):
        encourage = encouragements[level]
        encouragement_info[level] = (encourage,
                                     success_chance(level, encourage),
                                     reset_chance(level, encourage))

    safety_limits = {}
    for level in range(snailMaxRank):
        for target_confidence, mail, safety_chance in compute_safety_limits(level):
            safety_limits[level, target_confidence] = (mail, safety_chance)

    return encouragement_info, safety_limits

def getSnailInformationGroup() -> AdviceGroup:
    snail_AdviceDict = {
        "General": [],
    }

    sodium_level = session_data.account.atom_collider['Atoms']['Sodium - Snail Kryptonite']['Level']
    snail_data = session_data.account.gaming['Imports']['Snail']
    sodium_safety_level = sodium_level * 5
    floored_envelopes = safer_convert(session_data.account.gaming['Envelopes'], 0)

    #General
    snail_AdviceDict["General"].append(Advice(
        label=(
            f"Current Snail Rank: {snail_data['SnailRank']}"
            if snail_data['Level'] > 0 else
            f"Snail import not yet unlocked"
        ),
        picture_class='immortal-snail',
        progression=snail_data['SnailRank'],
        goal=snailMaxRank
    ))
    snail_AdviceDict["General"].append(Advice(
        label=f"Current Encouragements: {snail_data['Encouragements']}",
        picture_class='snail-envelope',
    ))
    snail_AdviceDict["General"].append(Advice(
        label=f"Envelopes owned: {floored_envelopes}",
        picture_class='snail-envelope',
    ))

    if sodium_safety_level + 5 <= snail_data['SnailRank']:
        snail_AdviceDict["General"].append(Advice(
            label=f"{{{{ Sodium|#atom-collider }}}} too low to safely level the Snail any further!",
            picture_class='sodium',
        ))
    else:
        num_trebel_notes = session_data.account.caverns['Caverns']['The Harp']['NotesOwned'][3]

        final_ballad_bonus = 1.0

        if session_data.account.caverns["Schematics"]["Final Ballad of the Snail"]["Purchased"]:
            num_trebel_digits = int(math.log10(num_trebel_notes) + 1 if num_trebel_notes > 0 else 0)
            final_ballad_bonus = 1 + 0.04 * num_trebel_digits

            snail_AdviceDict['General'].append(Advice(
                label=f"<br>{num_trebel_digits} Trebel Note digits for a bonus of {final_ballad_bonus:0.2f}x",
                picture_class=session_data.account.caverns['Schematics']['Final Ballad of the Snail']['Image'],
                progression=num_trebel_digits,
                goal=infinity_string,
                resource='harp-note-3'
            ))
        else:
            snail_AdviceDict["General"].append(Advice(
                label=f"{{{{ Schematic|#villagers }}}}: Final Ballad of the Snail is NOT acquired",
                picture_class=session_data.account.caverns["Schematics"]["Final Ballad of the Snail"]['Image'],
                progression=0,
                goal=1
            ))

        TARGET_CONFIDENCE_LEVELS = (0.80, 0.90, 0.95, 0.99, 0.999)

        encouragement_info, safety_thresholds = getSnailLevelUpInfo(final_ballad_bonus, TARGET_CONFIDENCE_LEVELS)

        min_snail_rank = getSnailResetTarget(snail_data['SnailRank'])
        target_snail_rank = min(max(encouragement_info.keys()), sodium_safety_level+4)

    #Rank Info

        #for level in range(target_snail_rank, min_snail_rank-1, -1):  #Backwards
        for level in range(min_snail_rank, target_snail_rank + 1):
            rank_type = (
                'Previous' if level < snail_data['SnailRank']
                else 'Future' if level > snail_data['SnailRank']
                else 'Current'
            )
            subgroupName = f"{rank_type} Rank {level} Info"
            snail_AdviceDict[subgroupName] = []
            num_encourage, s_chance, r_chance = encouragement_info[level]

            encouragements_short_by = max(0, num_encourage - snail_data['Encouragements'])
            short_by_note = f"<br>Progress below reduced by {encouragements_short_by} due to incomplete encouragements" if encouragements_short_by > 0 else ''

            snail_AdviceDict[subgroupName].append(Advice(
                label=f"{num_encourage} recommended encouragements."
                      f"<br>Game will display: {s_chance:0.2%} success, {r_chance:0.2%} reset chance"
                      f"{short_by_note}",
                picture_class='immortal-snail',
                progression=snail_data['Encouragements'] if level == snail_data['SnailRank'] else 0,
                goal=num_encourage,
                resource='snail-envelope'
            ))

            if level == snail_data['SnailRank']:
                for target_idx, target_confidence in enumerate(TARGET_CONFIDENCE_LEVELS):
                    mail_needed, overall_chance = safety_thresholds[level, target_confidence]
                    try:
                        if safety_thresholds[level, TARGET_CONFIDENCE_LEVELS[target_idx]][0] == safety_thresholds[level, TARGET_CONFIDENCE_LEVELS[target_idx + 1]][0]:
                            # Skip "duplicate" safety level info, that is cases where no extra mail is needed
                            # and no extra mail is needed for a higher confidence level as well.
                            continue
                    except IndexError:
                        pass

                    snail_AdviceDict[subgroupName].append(Advice(
                        label=f"{mail_needed} mail before clicking Level Up for {target_confidence:.1%} safety",
                        picture_class='snail-envelope',
                        progression=max(0, floored_envelopes - encouragements_short_by),
                        goal=mail_needed
                    ))

    snail_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Snail Information',
        post_string='Safety means your chance of not ending up worse than you started due to potential Resets',
        advices=snail_AdviceDict,
        informational=True
    )
    snail_AdviceGroup.remove_empty_subgroups()
    return snail_AdviceGroup

def getGamingProgressionTierAdviceGroups():
    gaming_AdviceGroupDict = {}
    info_tiers = 0
    max_tier = 0  #max(gaming_progressionTiers.keys()) - info_tiers

    # Generate AdviceGroups (none right now!)

    overall_SectionTier = min(max_tier + info_tiers, 0)
    return gaming_AdviceGroupDict, overall_SectionTier, max_tier, max_tier + info_tiers

def getGamingAdviceSection() -> AdviceSection:
    highestGamingSkillLevel = max(session_data.account.all_skills.get('Gaming', [0]))
    if highestGamingSkillLevel < 1:
        gaming_AdviceSection = AdviceSection(
            name='Gaming',
            tier='0',
            pinchy_rating=0,
            header='Come back after unlocking the Gaming skill in W5!',
            picture='wiki/Gaming_Skill_Icon.png',
            unreached=True
        )
        return gaming_AdviceSection

    # Generate AdviceGroup
    gaming_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getGamingProgressionTierAdviceGroups()
    gaming_AdviceGroupDict['Snail'] = getSnailInformationGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    gaming_AdviceSection = AdviceSection(
        name='Gaming',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header='Gaming Information',  #f"Best Gaming tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='wiki/Gaming_Skill_Icon.png',
        groups=gaming_AdviceGroupDict.values(),
        unrated=True
    )

    return gaming_AdviceSection
