from consts.progression_tiers_updater import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from consts.consts import break_you_best, build_subgroup_label
from consts.consts_w3 import conditional_prayers, ignorable_prayers
from consts.progression_tiers import prayers_progressionTiers
from flask import g as session_data
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

def get_antifun_spirit_next_level_cost(current_prayer_level: int) -> int:
    max_cost = round(9 + (conditional_prayers['Antifun Spirit'] * .9))  #Max level
    if current_prayer_level >= conditional_prayers['Antifun Spirit']:
        return max_cost
    else:
        result = round(9 + (current_prayer_level+1 * .9))
        return result

def setPrayersProgressionTierAdviceGroup():
    prayers_Advices = {
        'Recommended': {},
        'Conditional': [],
        'Ignorable': []
    }
    prayers_AdviceGroups = {}

    optional_tiers = 0
    true_max = true_max_tiers['Prayers']
    max_tier = true_max - optional_tiers  # Final tier_number is ignorable, second to final is optional
    tier_WorshipPrayers = 0

    player_prayers = session_data.account.prayers

    # Check Recommended Prayers
    for tier_number, requirements in prayers_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        for prayer_name, prayer_level in requirements.items():
            if player_prayers[prayer_name]['Level'] < prayer_level:
                if (
                    subgroup_label not in prayers_Advices['Recommended']
                    and len(prayers_Advices['Recommended']) < session_data.account.max_subgroups
                ):
                    prayers_Advices['Recommended'][subgroup_label] = []
                if subgroup_label in prayers_Advices['Recommended']:
                    prayers_Advices['Recommended'][subgroup_label].append(Advice(
                        label=prayer_name,
                        picture_class=prayer_name,
                        progression=player_prayers[prayer_name]['Level'],
                        goal=prayer_level,
                        resource=player_prayers[prayer_name]['Material']
                    ))
        if subgroup_label not in prayers_Advices['Recommended'] and tier_WorshipPrayers == tier_number - 1:
            tier_WorshipPrayers = tier_number

    # Check Optional Prayers
    next_antifun_cost = get_antifun_spirit_next_level_cost(player_prayers['Antifun Spirit']['Level'])
    for prayer_name, prayer_level in conditional_prayers.items():
        if player_prayers[prayer_name]['Level'] < prayer_level:
            if (
                prayer_name == 'Antifun Spirit'
                and session_data.account.minigame_plays_daily < next_antifun_cost
            ):
                #logger.debug(f"Skipping Antifun Spirit because next level costs {next_antifun_cost} while player has {session_data.account.minigame_plays_daily} daily minigame plays")
                continue
            else:
                prayers_Advices['Conditional'].append(Advice(
                    label=prayer_name,
                    picture_class=prayer_name,
                    progression=player_prayers[prayer_name]['Level'],
                    goal=prayer_level,
                    resource=player_prayers[prayer_name]['Material']
                ))

    # Check Ignorable Prayers
    for prayer_name, prayer_level in ignorable_prayers.items():
        if player_prayers[prayer_name]['Level'] < ignorable_prayers[prayer_name]:
            prayers_Advices['Ignorable'].append(Advice(
                label=prayer_name,
                picture_class=prayer_name,
                progression=player_prayers[prayer_name]['Level'],
                goal=ignorable_prayers[prayer_name],
                resource=player_prayers[prayer_name]['Material']
            ))

    # Generate Advice Groups
    prayers_AdviceGroups['Recommended'] = AdviceGroup(
        tier=tier_WorshipPrayers,
        pre_string=f"Recommended Prayer{pl(prayers_Advices['Recommended'])}",
        advices=prayers_Advices['Recommended'],
    )
    prayers_AdviceGroups['Conditional'] = AdviceGroup(
        tier='',
        pre_string=f"Situational Prayer{pl(prayers_Advices['Conditional'])} you may consider leveling",
        advices=prayers_Advices['Conditional'],
        post_string="These are niche use prayers. They have different benefits/purposes at low level and high levels",
        informational=True,
        completed=True
    )
    prayers_AdviceGroups['Ignorable'] = AdviceGroup(
        tier='',
        pre_string=f"Ignorable Prayer{pl(prayers_Advices['Ignorable'])}",
        advices=prayers_Advices['Ignorable'],
        post_string="Prayers in this group should still be unlocked, but can stay at level 1 after that as of v2.36",
        informational=True,
        completed=True
    )
    overall_SectionTier = min(true_max, tier_WorshipPrayers)
    return prayers_AdviceGroups, overall_SectionTier, max_tier, true_max

def getPrayersAdviceSection() -> AdviceSection:
    highest_worship_level = max(session_data.account.all_skills['Worship'])
    if highest_worship_level < 1:
        prayers_AdviceSection = AdviceSection(
            name='Prayers',
            tier='0/0',
            header='Come back after unlocking the Worship skill in World 3!',
            picture='Prayer_Stone.gif',
            unreached=True
        )
        return prayers_AdviceSection

    #Generate AdviceGroups
    prayers_AdviceGroupDict, overall_SectionTier, max_tier, true_max = setPrayersProgressionTierAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    prayers_AdviceSection = AdviceSection(
        name='Prayers',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Prayer tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Prayer_Stone.gif',
        groups=prayers_AdviceGroupDict.values()
    )
    return prayers_AdviceSection
