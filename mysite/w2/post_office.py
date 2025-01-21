from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from utils.text_formatting import kebab
from consts import poBoxDict

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
        postOffice_AdviceGroupDict['Boxes' + character.character_name] = getBoxesAdviceGroup(character)
    
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
    postOffice_advices = {}

    totalPointInvested = 0
    for box in poBoxDict.values():
        boxName = box['Name']
        boxLevel = character.po_boxes_invested[boxName]['Level']
        totalPointInvested += boxLevel

        advice = Advice(
            label=boxName,
            picture_class=getPictureClassFromName(boxName),
            progression=boxLevel,
            goal=box['max_level'],
            completed=boxLevel >= box['max_level']
        )
        if boxLevel >= box['max_level']:
            mark_advice_completed(advice)
            
        if not box['Tab'] in postOffice_advices:
            postOffice_advices[box['Tab']] = []    
        postOffice_advices[box['Tab']].append(advice)

    return AdviceGroup(
        tier="",
        pre_string=f"Info- Boxes for {character.character_name} the {character.class_name}",
        advices=postOffice_advices,
        post_string=f"Available points : {session_data.account.postOffice["Total Boxes Earned"] - totalPointInvested}",
        informational=True,
    )

def getPictureClassFromName(name):
    match name:
        case "Magician Starterpack":
            return "magician-starter-pack"
        case "Civil War Memory Box":
            return "civil-war-memory"
        case _:
            return kebab(name)