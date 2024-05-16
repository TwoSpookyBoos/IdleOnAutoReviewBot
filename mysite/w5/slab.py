from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl, getItemDisplayName
from utils.logging import get_logger
from flask import g as session_data
from consts import slabList, reclaimableQuestItems, vendorItems, anvilItems

logger = get_logger(__name__)

def setSlabProgressionTier():
    slab_AdviceDict = {
        "Reclaims": [],
        "Storage": [],
        "Vendors": {},
        "Anvil": {}
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
                break
            if itemName in reclaimableQuestItems.keys():
                for characterIndex, characterQuests in enumerate(session_data.account.all_quests):
                    if reclaimableQuestItems[itemName].get("QuestNameCoded") in characterQuests:
                        if characterQuests[reclaimableQuestItems[itemName].get("QuestNameCoded")] > 0:
                            slab_AdviceDict["Reclaims"].append(Advice(
                                label=f"{getItemDisplayName(itemName)} ({reclaimableQuestItems[itemName].get('QuestGiver')}: {reclaimableQuestItems[itemName].get('QuestName')})",
                                picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                            break  #Only show this once per account, not once per character
            for vendor, vendorList in vendorItems.items():
                # If I search for the item first, these can appear out of order
                if vendor not in slab_AdviceDict["Vendors"]:
                    slab_AdviceDict["Vendors"][vendor] = []
                if itemName in vendorList:
                    slab_AdviceDict["Vendors"][vendor].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                    break
            for anvilTab, anvilTabList in anvilItems.items():
                # If I search for the item first, these can appear out of order
                if anvilTab not in slab_AdviceDict["Anvil"]:
                    slab_AdviceDict["Anvil"][anvilTab] = []
                if itemName in anvilTabList:
                    slab_AdviceDict["Anvil"][anvilTab].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                    break
    #Remove any empty subgroups. Caused by creating the subgroups in order to preserve order.
    for subgroup in slab_AdviceDict["Vendors"]:
        if len(subgroup) == 0:
            slab_AdviceDict["Vendors"].pop(subgroup)
    for subgroup in slab_AdviceDict["Anvil"]:
        if len(subgroup) == 0:
            slab_AdviceDict["Anvil"].pop(subgroup)
    # Generate AdviceGroups
    slab_AdviceGroupDict["Storage"] = AdviceGroup(
        tier='',
        pre_string=f"The following item{pl(slab_AdviceDict['Storage'], ' was', 's were')} found in storage or on a character, but not in Slab",
        advices=slab_AdviceDict["Storage"]
    )
    slab_AdviceGroupDict["Reclaims"] = AdviceGroup(
        tier='',
        pre_string=f"The following item{pl(slab_AdviceDict['Reclaims'])} could be reclaimed from a quest and are not registered in The Slab",
        advices=slab_AdviceDict["Reclaims"]
    )
    slab_AdviceGroupDict["Vendors"] = AdviceGroup(
        tier='',
        pre_string=f"The following item{pl(slab_AdviceDict['Vendors'])} could be purchased from a Vendor",
        advices=slab_AdviceDict["Vendors"]
    )
    slab_AdviceGroupDict["Anvil"] = AdviceGroup(
        tier='',
        pre_string=f"The following item{pl(slab_AdviceDict['Anvil'])} could be crafted at the Anvil",
        advices=slab_AdviceDict["Anvil"]
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
        slab_AdviceSection.header = f"You're missing some easy Slab stacks!"

    return slab_AdviceSection
