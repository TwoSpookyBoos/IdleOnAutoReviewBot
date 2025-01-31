from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import post_office_tabs

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    postOffice_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0 - info_tiers
    tier_PostOffice = 0

    #Assess Tiers
    tiers_ag = AdviceGroup(
        tier=tier_PostOffice,
        pre_string="Progression Tiers",
        advices=postOffice_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_PostOffice)
    return tiers_ag, overall_SectionTier, max_tier

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
    postOffice_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    for character in session_data.account.all_characters:
        postOffice_AdviceGroupDict[character.character_name] = getBoxesAdviceGroup(character)
    
    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    postOffice_AdviceSection = AdviceSection(
        name="Post Office",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header="Post Office Information",
        picture="wiki/Postboy_Pablob.gif",
        groups=postOffice_AdviceGroupDict.values(),
        unrated=True,
    )
    return postOffice_AdviceSection

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
