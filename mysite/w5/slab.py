from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl, getItemDisplayName
from utils.logging import get_logger
from flask import g as session_data
from consts import slabList, reclaimableQuestItems

logger = get_logger(__name__)

def setSlabProgressionTier():
    slab_AdviceDict = {
        "Reclaims": [],
        "Storage": []
    }
    slab_AdviceGroupDict = {}
    slab_AdviceSection = AdviceSection(
        name="Slab",
        tier="0",
        pinchy_rating=0,
        header="Best Slab tier met: Not Yet Evaluated",
        picture="Slab.png"
    )
    # highestSlabSkillLevel = max(session_data.account.all_skills.get("Slab", [0]))
    # if highestSlabSkillLevel < 1:
    #     slab_AdviceSection.header = "Come back after unlocking the Slab in W5!"
    #     return slab_AdviceSection

    tier_Slab = 0
    max_tier = 0

    itemNameFindList = ["Timecandy1", "Timecandy2", "Timecandy3", "Timecandy4", "Timecandy5", "Timecandy6",
                        "EquipmentHats108", "EquipmentNametag10"]
    itemNameReplacementList = ["time-candy-1-hr", "time-candy-2-hr", "time-candy-4-hr", "time-candy-12-hr", "time-candy-24-hr", "time-candy-72-hr",
                               "third-anniversary-ice-cream-topper", "third-anniversary-idleon-nametag"]

    #Assess Tiers
    for itemName in slabList:
        if itemName not in session_data.account.registered_slab:
            if session_data.account.assets.get(itemName).amount > 0:
                slab_AdviceDict["Storage"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
            elif itemName in reclaimableQuestItems.keys():
                for characterIndex, characterQuests in enumerate(session_data.account.all_quests):
                    if reclaimableQuestItems[itemName].get("QuestNameCoded") in characterQuests:
                        if characterQuests[reclaimableQuestItems[itemName].get("QuestNameCoded")] > 0:
                            slab_AdviceDict["Reclaims"].append(Advice(
                                label=f"{getItemDisplayName(itemName)} ({reclaimableQuestItems[itemName].get('QuestGiver')}: {reclaimableQuestItems[itemName].get('QuestName')})",
                                picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                            break  #Only show this once per account, not once per character
    # Generate AdviceGroups
    slab_AdviceGroupDict["Storage"] = AdviceGroup(
        tier='',
        pre_string=f"The following item{pl(slab_AdviceDict['Storage'], ' was', 's were')} found in storage or on a character, but not in Slab",
        advices=slab_AdviceDict["Storage"]
    )
    slab_AdviceGroupDict["Reclaims"] = AdviceGroup(
        tier='',
        pre_string=f"The following item{pl(slab_AdviceDict['Storage'])} could be reclaimed from a quest and are not registered in The Slab",
        advices=slab_AdviceDict["Reclaims"]
    )

    # Generate AdviceSection
    overall_SlabTier = min(max_tier, tier_Slab)
    tier_section = f"{overall_SlabTier}/{max_tier}"
    slab_AdviceSection.tier = tier_section
    slab_AdviceSection.pinchy_rating = overall_SlabTier
    slab_AdviceSection.groups = slab_AdviceGroupDict.values()
    if len(slab_AdviceSection.groups) == 0:
        slab_AdviceSection.header = f"All currently owned items registered in The Slab<br>You best ❤️"
    else:
        slab_AdviceSection.header = f"You're missing some free Slab count!"

    return slab_AdviceSection
