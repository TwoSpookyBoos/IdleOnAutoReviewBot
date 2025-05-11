from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import post_office_tabs, post_office_progression_tiers, break_you_best, infinity_string

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    postOffice_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 1
    true_max = max(post_office_progression_tiers.keys())
    max_tier = true_max - info_tiers
    tier_PostOffice = 0

    #Assess Tiers
    boxes_advised = {char.character_name:[] for char in session_data.account.all_characters}
    for tier, requirements in post_office_progression_tiers.items():
        subgroup_label = f"To reach {'Informational ' if tier > max_tier else ''}Tier {tier}"
        postOffice_AdviceDict['Tiers'][subgroup_label] = []
        if 'Class Specific' in requirements:
            for char in session_data.account.all_characters:
                for class_name in requirements['Class Specific']:
                    if class_name in char.all_classes:
                        for box_name, box_level in requirements['Class Specific'][class_name].items():
                            if (
                                char.po_boxes_invested[box_name]['Level'] < box_level
                                and box_name not in boxes_advised[char.character_name]
                            ):
                                postOffice_AdviceDict['Tiers'][subgroup_label].append(Advice(
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
                            postOffice_AdviceDict['Tiers'][subgroup_label].append(Advice(
                                label=f"{char.character_name}: {box_name}",
                                picture_class=char.class_name_icon,
                                progression=char.po_boxes_invested[box_name]['Level'],
                                goal=box_details['Max Level'],
                                resource=box_name
                            ))
                            boxes_advised[char.character_name].append(box_name)

        if len(postOffice_AdviceDict['Tiers'][subgroup_label]) == 0 and tier_PostOffice == tier-1:
            tier_PostOffice = tier

    tiers_ag = AdviceGroup(
        tier=tier_PostOffice,
        pre_string="Progression Tiers",
        advices=postOffice_AdviceDict['Tiers']
    )
    tiers_ag.remove_empty_subgroups()

    overall_SectionTier = min(true_max, tier_PostOffice)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getBoxesAdviceGroup(character):
    totalPointInvested = sum([boxDetails['Level'] for boxDetails in character.po_boxes_invested.values()])

    postOffice_advices = {
        tab_name: [
            Advice(
                label=boxName,
                picture_class=boxName,
                progression=boxDetails['Level'],
                goal=boxDetails['Max Level'],
                completed=boxDetails['Level'] >= boxDetails['Max Level']
            ) for boxName, boxDetails in character.po_boxes_invested.items() if boxDetails['Tab'] == tab_name
        ] for tab_name in post_office_tabs
    }

    for subgroup in postOffice_advices:
        for advice in postOffice_advices[subgroup]:
            mark_advice_completed(advice)

    char_ag = AdviceGroup(
        tier="",
        pre_string=f"Info- Boxes for {character.character_name} the {character.class_name}",
        advices=postOffice_advices,
        post_string=f"Available points : {max(0, session_data.account.postOffice['Total Boxes Earned'] - totalPointInvested):,.0f}",
        informational=True,
    )
    return char_ag

def getPostOfficeAdviceSection() -> AdviceSection:
    if session_data.account.highestWorldReached < 2:
        postOffice_AdviceSection = AdviceSection(
            name="Post Office",
            tier="0",
            pinchy_rating=0,
            header="Come back after unlocking the Post Office in W2 town!",
            picture="wiki/Postboy_Pablob.gif",
            unrated=True,
            unreached=True
        )
        return postOffice_AdviceSection

    #Generate AdviceGroups
    postOffice_AdviceGroupDict = {}
    postOffice_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    for character in session_data.account.all_characters:
        postOffice_AdviceGroupDict[character.character_name] = getBoxesAdviceGroup(character)
    
    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    postOffice_AdviceSection = AdviceSection(
        name="Post Office",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Post Office tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="wiki/Postboy_Pablob.gif",
        groups=postOffice_AdviceGroupDict.values(),
    )
    return postOffice_AdviceSection
