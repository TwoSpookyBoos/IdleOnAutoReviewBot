from consts.progression_tiers import armor_sets_progressionTiers
from consts.progression_tiers_updater import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts.consts import break_you_best, build_subgroup_label
from utils.text_formatting import getItemDisplayName

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup(player_sets: dict) -> tuple[AdviceGroup, int, int, int]:
    armor_sets_Advices = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Armor Sets']
    max_tier = true_max - optional_tiers
    tier_ArmorSets = 0

    smithy_unlocked = session_data.account.armor_sets['Unlocked']
    days_toward_unlock = session_data.account.armor_sets['Days toward Unlock']

    if (
        not smithy_unlocked
        and days_toward_unlock >= 30
    ):
        session_data.account.alerts_AdviceDict['World 3'].append(Advice(
            label=f"{{{{Smithy|#armor-sets}}}} ready to accept Armor Sets",
            picture_class='smithy'
        ))

    #Assess Tiers
    for tier_number, requirements in armor_sets_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        # Unlock the Smithy interface
        if (
            requirements.get('Unlocked', False) == True
            and not smithy_unlocked
        ):
            if (
                subgroup_label not in armor_sets_Advices['Tiers']
                and len(armor_sets_Advices['Tiers']) < session_data.account.max_subgroups
            ):
                armor_sets_Advices['Tiers'][subgroup_label] = []
            if subgroup_label in armor_sets_Advices['Tiers']:
                armor_sets_Advices['Tiers'][subgroup_label].append(Advice(
                    label=f"Unlock the Smithy by having purchased 2000 gems or waiting 30 days",
                    picture_class='smithy',
                    progression=min(30, days_toward_unlock),
                    goal=30
                ))

        # Unlock particular sets
        for set_name in requirements.get('Sets', []):
            if not player_sets[set_name]['Owned']:
                if (
                    subgroup_label not in armor_sets_Advices['Tiers']
                    and len(armor_sets_Advices['Tiers']) < session_data.account.max_subgroups
                ):
                    armor_sets_Advices['Tiers'][subgroup_label] = []
                if subgroup_label in armor_sets_Advices['Tiers']:
                    armor_sets_Advices['Tiers'][subgroup_label].append(Advice(
                        label=f"Complete the {set_name.title()}: {player_sets[set_name]['Description']}",
                        picture_class=player_sets[set_name]['Image'],
                        progression=0,
                        goal=1
                    ))

        if subgroup_label not in armor_sets_Advices['Tiers'] and tier_ArmorSets == tier_number - 1:
            tier_ArmorSets = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_ArmorSets,
        pre_string='Progression Tiers',
        advices=armor_sets_Advices['Tiers']
    )
    overall_SectionTier = min(true_max, tier_ArmorSets)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getAllSetsAdviceGroups(player_sets: dict) -> dict[str, AdviceGroup]:
    sets_Advices = {}

    for name, details in player_sets.items():
        if not details['Owned']:
            # Armors
            all_armors = []
            for item_codename in details['Armor']:
                if item_codename != 'none':
                    display_name = getItemDisplayName(item_codename)
                    all_armors.append(Advice(
                        label=display_name,
                        picture_class=display_name,
                        progression=min(1, session_data.account.all_assets.get(item_codename).amount),
                        goal=1
                    ))
            obtained_armors = sum([1 for advice in all_armors if int(advice.progression) > 0])

            # Tools
            all_tools = []
            for item_codename in details['Tools']:
                if item_codename != 'none':
                    display_name = getItemDisplayName(item_codename)
                    all_tools.append(Advice(
                        label=display_name,
                        picture_class=display_name,
                        progression=min(1, session_data.account.all_assets.get(item_codename).amount),
                        goal=1
                    ))
            obtained_tools = sum([1 for advice in all_tools if int(advice.progression) > 0])

            # Tools
            all_weapons = []
            for item_codename in details['Weapons']:
                if item_codename != 'none':
                    display_name = getItemDisplayName(item_codename)
                    all_weapons.append(Advice(
                        label=display_name,
                        picture_class=display_name,
                        progression=min(1, session_data.account.all_assets.get(item_codename).amount),
                        goal=1
                    ))
            obtained_weapons = sum([1 for advice in all_weapons if int(advice.progression) > 0])

            sets_Advices[name] = {
                f"Required Armor: {obtained_armors}/{len(details['Armor'])}": all_armors,
                f"Required Tools: {obtained_tools}/{details['Required Tools']}": all_tools,
                f"Required Weapons: {obtained_weapons}/{details['Required Weapons']}": all_weapons
            }

            # Generate alert if set ready
            if (
                obtained_armors >= len(details['Armor'])
                and obtained_tools >= details['Required Tools']
                and obtained_weapons >= details['Required Weapons']
                and session_data.account.armor_sets['Unlocked']
            ):
                session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                    label=f"{name.title()} can be {{{{completed|#armor-sets}}}}",
                    picture_class=details['Image']
                ))

    for set_name in sets_Advices:
        for advice_type in sets_Advices[set_name]:
            for advice in sets_Advices[set_name][advice_type]:
                mark_advice_completed(advice)

    sets_ags = {
        name: AdviceGroup(
            tier='',
            pre_string=f'{name.title()} requirements',
            advices=sets_Advices[name],
            informational=True
        )
        for name in sets_Advices
    }

    set_bonuses_Advice = [
        Advice(
            label=f"{set_name.title()}: {player_sets[set_name]['Description']}",
            picture_class=player_sets[set_name]['Image'],
            progression=int(details['Owned']),
            goal=1
        ) for set_name, details in player_sets.items()
    ]

    for advice in set_bonuses_Advice:
        mark_advice_completed(advice)

    sets_ags['Total Set Bonuses'] = AdviceGroup(
        tier='',
        pre_string='Completed Set Bonuses',
        advices=set_bonuses_Advice,
        informational=True
    )

    for ag in sets_ags:
        sets_ags[ag].remove_empty_subgroups()

    return sets_ags

def getArmorSetsAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.highest_world_reached < 3:
        armor_sets_AdviceSection = AdviceSection(
            name='Armor Sets',
            tier='0/0',
            header='Come back after unlocking World 3!',
            picture='customized/smithy.gif',
            unreached=True,
            completed=False
        )
        return armor_sets_AdviceSection

    player_sets = session_data.account.armor_sets['Sets']

    #Generate Alert Advice

    #Generate AdviceGroups
    armor_sets_AdviceGroups = {}
    armor_sets_AdviceGroups['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup(player_sets)
    armor_sets_AdviceGroups.update(getAllSetsAdviceGroups(player_sets))

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    armor_sets_AdviceSection = AdviceSection(
        name='Armor Sets',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Armor Sets tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/smithy.gif',
        groups=armor_sets_AdviceGroups.values(),
    )

    return armor_sets_AdviceSection
