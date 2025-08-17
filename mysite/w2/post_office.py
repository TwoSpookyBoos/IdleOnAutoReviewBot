from models.models import AdviceSection, AdviceGroup, Advice, TabbedAdviceGroup, TabbedAdviceGroupTab
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.progression_tiers import post_office_progression_tiers, true_max_tiers
from utils.text_formatting import kebab

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    po_Advices = {
        'Tiers': {},
    }
    optional_tiers = 1
    true_max = true_max_tiers['Post Office']
    max_tier = true_max - optional_tiers
    tier_PostOffice = 0

    # Assess Tiers
    boxes_advised = {char.character_name: [] for char in session_data.account.all_characters}
    for tier_number, requirements in post_office_progression_tiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        if 'Class Specific' in requirements:
            for char in session_data.account.all_characters:
                for class_name in requirements['Class Specific']:
                    if class_name in char.all_classes:
                        for box_name, box_level in requirements['Class Specific'][class_name].items():
                            if (
                                char.po_boxes_invested[box_name]['Level'] < box_level
                                and box_name not in boxes_advised[char.character_name]
                            ):
                                if (
                                    subgroup_label not in po_Advices['Tiers']
                                    and len(po_Advices['Tiers']) < session_data.account.max_subgroups
                                ):
                                    po_Advices['Tiers'][subgroup_label] = []
                                if subgroup_label in po_Advices['Tiers']:
                                    po_Advices['Tiers'][subgroup_label].append(Advice(
                                        label=f"{char.character_name}: {box_name}",
                                        picture_class=char.class_name_icon,
                                        progression=char.po_boxes_invested[box_name]['Level'],
                                        goal=box_level,
                                        resource=box_name
                                    ))
                                    boxes_advised[char.character_name].append(box_name)
        if 'Myriad' in requirements:
            for char in session_data.account.all_characters:
                for box_name, box_details in char.po_boxes_invested.items():
                    if (
                        (box_name != 'Myriad Crate' and not requirements['Myriad'])
                        or requirements['Myriad']
                    ):
                        if (
                            box_details['Level'] < box_details['Max Level']
                            and box_name not in boxes_advised[char.character_name]
                        ):
                            if (
                                    subgroup_label not in po_Advices['Tiers']
                                    and len(po_Advices['Tiers']) < session_data.account.max_subgroups
                            ):
                                po_Advices['Tiers'][subgroup_label] = []
                            if subgroup_label in po_Advices['Tiers']:
                                po_Advices['Tiers'][subgroup_label].append(Advice(
                                    label=f"{char.character_name}: {box_name}",
                                    picture_class=char.class_name_icon,
                                    progression=char.po_boxes_invested[box_name]['Level'],
                                    goal=box_details['Max Level'],
                                    resource=box_name
                                ))
                                boxes_advised[char.character_name].append(box_name)

        if subgroup_label not in po_Advices['Tiers'] and tier_PostOffice == tier_number - 1:
            tier_PostOffice = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_PostOffice,
        pre_string='Progression Tiers',
        advices=po_Advices['Tiers']
    )
    tiers_ag.remove_empty_subgroups()

    overall_SectionTier = min(true_max, tier_PostOffice)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getBoxesAdviceGroup() -> TabbedAdviceGroup | dict[str, AdviceGroup]:
    tabbed_advices: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]] = {}
    for character in session_data.account.all_characters:
        total_points_invested = sum([boxDetails['Level'] for boxDetails in character.po_boxes_invested.values()])
        remaining_points = max(0, session_data.account.postOffice['Total Boxes Earned'] - total_points_invested)

        po_Advices = {}

        for box_name, box_details in character.po_boxes_invested.items():
            needed_for_completion = (box_details['Max Level'] - box_details['Level'])
            using_points = min(remaining_points, needed_for_completion)
            remaining_points = max(0, remaining_points - using_points)

            advice = Advice(
                label=box_name,
                picture_class=box_name,
                progression=box_details['Level'],
                goal=box_details['Max Level'],
                potential=using_points)

            tab_name = box_details['Tab']
            if tab_name not in po_Advices:
                po_Advices[tab_name] = []

            po_Advices[tab_name].append(advice)
            mark_advice_completed(advice)

        tabbed_advices[character.character_name] = (
            TabbedAdviceGroupTab(kebab(character.class_name_icon), character.character_name),
            AdviceGroup(
                tier='',
                pre_string=f"Boxes for {character.character_name} the {character.class_name}",
                advices=po_Advices,
                post_string=f"Available points : {max(0, session_data.account.postOffice['Total Boxes Earned'] - total_points_invested):,.0f}",
                informational=True,
            )
        )
    return TabbedAdviceGroup(tabbed_advices) if session_data.account.tabbed_advice_groups else {tab.label: advice_group for tab, advice_group in tabbed_advices.values()}


def getPostOfficeAdviceSection() -> AdviceSection:
    if session_data.account.highest_world_reached < 2:
        postOffice_AdviceSection = AdviceSection(
            name='Post Office',
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking the Post Office in W2 town!',
            picture='wiki/Postboy_Pablob.gif',
            unrated=True,
            unreached=True
        )
        return postOffice_AdviceSection

    # Generate AdviceGroups
    postOffice_AdviceGroupDict = {}
    postOffice_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    boxes_advice = getBoxesAdviceGroup()
    if isinstance(boxes_advice, TabbedAdviceGroup):
        postOffice_AdviceGroupDict['Boxes'] = boxes_advice
        postOffice_AdviceGroupDict['Boxes'] = boxes_advice
    else:
        postOffice_AdviceGroupDict = postOffice_AdviceGroupDict | boxes_advice

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    postOffice_AdviceSection = AdviceSection(
        name='Post Office',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Post Office tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='wiki/Postboy_Pablob.gif',
        groups=postOffice_AdviceGroupDict.values(),
    )
    return postOffice_AdviceSection
