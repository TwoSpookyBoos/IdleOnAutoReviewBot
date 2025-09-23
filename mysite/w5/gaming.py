import collections
import functools
import math

from consts.progression_tiers import true_max_tiers
from consts.consts_autoreview import EmojiType
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import safer_convert, safer_math_log
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_w5 import snail_max_rank

logger = get_logger(__name__)

def getSnailResetTarget(snail_rank):
    if snail_rank == 0:
        return 0  # Can't actually happen, but...
    else:
        return max(1, snail_rank - snail_rank % 5)

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

        for level in range(snail_max_rank):
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
                fail = fail * (1 - r_chance)  # Just a failure

                # Standard failure
                probabilities[mail_used+3, level] += fail

                # Reset
                probabilities[mail_used+3, reset_target(level)] += reset

            while targets and overall_safety_chance >= targets[0]:
                yield targets.pop(0), mail_used, overall_safety_chance

            mail_used += 1

    encouragement_info = {}

    for level in range(snail_max_rank):
        encourage = encouragements[level]
        encouragement_info[level] = (encourage,
                                     success_chance(level, encourage),
                                     reset_chance(level, encourage))

    safety_limits = {}
    for level in range(snail_max_rank):
        for target_confidence, mail, safety_chance in compute_safety_limits(level):
            safety_limits[level, target_confidence] = (mail, safety_chance)

    return encouragement_info, safety_limits

def getSnailInformationGroup() -> AdviceGroup:
    snail_AdviceDict = {
        'General': [],
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
            'Snail import not yet unlocked'
        ),
        picture_class='immortal-snail',
        progression=snail_data['SnailRank'],
        goal=snail_max_rank
    ))
    if snail_data['SnailRank'] > 0:
        snail_AdviceDict['General'].append(Advice(
            label=f"Envelopes owned: {floored_envelopes}",
            picture_class='snail-envelope',
        ))
        
        num_trebel_notes = session_data.account.caverns['Caverns']['The Harp']['NotesOwned'][3]
        final_ballad_bonus = 1.0

        if session_data.account.caverns['Schematics']['Final Ballad of the Snail']['Purchased']:
            num_trebel_stacks = int(safer_math_log(num_trebel_notes, 'Lava') if num_trebel_notes > 0 else 0)
            final_ballad_bonus = 1 + 0.04 * num_trebel_stacks

        if sodium_safety_level + 5 <= snail_data['SnailRank']:
            snail_AdviceDict[f"Current Rank {snail_data['SnailRank']} Info"] = [Advice(
                label=f"{{{{ Sodium|#atom-collider }}}} too low to safely level the Snail any further!",
                picture_class='sodium',
            )]
        else:
            num_trebel_notes = session_data.account.caverns['Caverns']['The Harp']['NotesOwned'][3]

            final_ballad_bonus = 1.0

            if session_data.account.caverns['Schematics']['Final Ballad of the Snail']['Purchased']:
                num_trebel_stacks = int(math.log10(num_trebel_notes) if num_trebel_notes > 0 else 0)
                final_ballad_bonus = 1 + 0.04 * num_trebel_stacks

                snail_AdviceDict['General'].append(Advice(
                    label=f"<br>{num_trebel_stacks} Trebel Note stacks for a bonus of {final_ballad_bonus:0.2f}x",
                    picture_class=session_data.account.caverns['Schematics']['Final Ballad of the Snail']['Image'],
                    progression=num_trebel_stacks,
                    goal=EmojiType.INFINITY.value,
                    resource='harp-note-3'
                ))
            else:
                snail_AdviceDict['General'].append(Advice(
                    label=f"{{{{ Schematic|#villagers }}}}: Final Ballad of the Snail is NOT acquired",
                    picture_class=session_data.account.caverns['Schematics']['Final Ballad of the Snail']['Image'],
                    progression=0,
                    goal=1
                ))

            TARGET_CONFIDENCE_LEVELS = (0.90, 0.95, 0.99, 0.999)

            encouragement_info, safety_thresholds = getSnailLevelUpInfo(final_ballad_bonus, TARGET_CONFIDENCE_LEVELS)

            min_snail_rank = getSnailResetTarget(snail_data['SnailRank'])
            target_snail_rank = min(max(encouragement_info.keys()), sodium_safety_level+4)

            def make_encouragement_advice(level, label_prefix):
                num_encourage, s_chance, r_chance = encouragement_info[level]

                encouragements_short_by = max(0, num_encourage - snail_data['Encouragements'])

                return Advice(
                    label=f"{label_prefix}: Encourage the snail {num_encourage} times."
                          f"<br>Game will display {s_chance:0.2%} success, {r_chance:0.2%} reset chance",
                    picture_class='immortal-snail',
                    progression=snail_data['Encouragements'] if level == snail_data['SnailRank'] else 0,
                    goal=num_encourage,
                    resource='snail-envelope'
                )

            # Current Rank Info
            current_level = snail_data['SnailRank']
            subgroup_label = f'Current Rank {current_level} Info'
            snail_AdviceDict[subgroup_label] = []
            num_encourage, s_chance, r_chance = encouragement_info[current_level]

            encouragements_short_by = max(0, num_encourage - snail_data['Encouragements'])

            snail_AdviceDict[subgroup_label].append(make_encouragement_advice(current_level, "Step 1"))

            for target_idx, target_confidence in enumerate(TARGET_CONFIDENCE_LEVELS):
                mail_needed, overall_chance = safety_thresholds[current_level, target_confidence]
                try:
                    if safety_thresholds[current_level, TARGET_CONFIDENCE_LEVELS[target_idx]][0] == safety_thresholds[current_level, TARGET_CONFIDENCE_LEVELS[target_idx + 1]][0]:
                        # Skip "duplicate" safety level info, that is cases where no extra mail is needed
                        # and no extra mail is needed for a higher confidence level as well.
                        continue
                except IndexError:
                    pass

                snail_AdviceDict[subgroup_label].append(Advice(
                    label=f"Step 2: Choose a safety level. {target_confidence:.1%} safety = {mail_needed} unspent mail",
                    picture_class='snail-envelope',
                    progression=max(0, floored_envelopes - encouragements_short_by),
                    goal=mail_needed
                ))

            # All relevant encouragement info
            subgroup_label = 'Relevant Encouragement Info (for resets or advancement)'
            snail_AdviceDict[subgroup_label] = []

            for level in range(min_snail_rank, target_snail_rank + 1):
                rank_type = (
                    'Previous' if level < snail_data['SnailRank']
                    else 'Future' if level > snail_data['SnailRank']
                    else 'Current'
                )

                snail_AdviceDict[subgroup_label].append(make_encouragement_advice(level, f"{rank_type} Rank {level}"))

    snail_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Snail Ranks',
        post_string='Safety means your chance of not ending up worse than you started due to potential Resets',
        advices=snail_AdviceDict,
        informational=True,
        completed=snail_data['SnailRank'] >= snail_max_rank
    )
    snail_AdviceGroup.remove_empty_subgroups()
    return snail_AdviceGroup

def getGamingProgressionTierAdviceGroups():
    gaming_AdviceGroups = {}
    optional_tiers = 0
    true_max = true_max_tiers['Gaming']
    max_tier = true_max - optional_tiers

    # Generate AdviceGroups (none right now!)

    overall_SectionTier = min(true_max, 0)
    return gaming_AdviceGroups, overall_SectionTier, max_tier, true_max

def getGamingAdviceSection() -> AdviceSection:
    highestGamingSkillLevel = max(session_data.account.all_skills.get('Gaming', [0]))
    if highestGamingSkillLevel < 1:
        gaming_AdviceSection = AdviceSection(
            name='Gaming',
            tier='0',
            pinchy_rating=0,
            header='Come back after unlocking the Gaming skill in W5!',
            picture='data/ClassIcons56.png',
            unreached=True
        )
        return gaming_AdviceSection

    # Generate AdviceGroup
    gaming_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getGamingProgressionTierAdviceGroups()
    if session_data.account.gaming['Imports']['Snail']['SnailRank'] < snail_max_rank:
        gaming_AdviceGroupDict['Snail'] = getSnailInformationGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    gaming_AdviceSection = AdviceSection(
        name='Gaming',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header='Gaming Information',  #f"Best Gaming tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='data/ClassIcons56.png',
        groups=gaming_AdviceGroupDict.values(),
        unrated=True
    )

    return gaming_AdviceSection
