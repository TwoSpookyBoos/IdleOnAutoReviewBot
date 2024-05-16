from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl, getItemDisplayName
from utils.logging import get_logger
from flask import g as session_data
from consts import slabList, reclaimableQuestItems, vendorItems, anvilItems, knownSlabIgnorablesList, dungeonWeaponsList, maxDungeonWeaponsAvailable, \
    dungeonArmorsList, maxDungeonArmorsAvailable, dungeonJewelryList, maxDungeonJewelryAvailable

logger = get_logger(__name__)

def setSlabProgressionTier():
    slab_AdviceDict = {
        "Reclaims": [],
        "Storage": [],
        "Vendors": {},
        "Anvil": {},
        "Dungeon": [],
        "Deprecated": []
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
            #If the item is an Asset, meaning in storage, character inventory, or worn by a character
            if session_data.account.assets.get(itemName).amount > 0:
                slab_AdviceDict["Storage"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                continue
            #If the item is a reclaimable quest item AND the quest has been completed by at least 1 character
            if itemName in reclaimableQuestItems.keys():
                for characterIndex, characterQuests in enumerate(session_data.account.all_quests):
                    if reclaimableQuestItems[itemName].get("QuestNameCoded") in characterQuests:
                        if characterQuests[reclaimableQuestItems[itemName].get("QuestNameCoded")] > 0:
                            slab_AdviceDict["Reclaims"].append(Advice(
                                label=f"{getItemDisplayName(itemName)} ({reclaimableQuestItems[itemName].get('QuestGiver')}: {reclaimableQuestItems[itemName].get('QuestName')})",
                                picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                            break  #Only show this once per account, not once per character
                continue
            #If the item is sold by a vendor
            for vendor, vendorList in vendorItems.items():
                # If I search for the item first, these can appear out of order
                if vendor not in slab_AdviceDict["Vendors"]:
                    slab_AdviceDict["Vendors"][vendor] = []
                if itemName in vendorList:
                    slab_AdviceDict["Vendors"][vendor].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                    break
            #If the item is craftable at the anvil
            for anvilTab, anvilTabList in anvilItems.items():
                # If I search for the item first, these can appear out of order
                if anvilTab not in slab_AdviceDict["Anvil"]:
                    slab_AdviceDict["Anvil"][anvilTab] = []
                if itemName in anvilTabList:
                    slab_AdviceDict["Anvil"][anvilTab].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))
                    break
            #If the item is a Dungeon Weapon AND the player has purchased all MaxWeapons
            if itemName in dungeonWeaponsList and session_data.account.dungeon_upgrades.get("MaxWeapon", 0) >= maxDungeonWeaponsAvailable:
                slab_AdviceDict["Dungeon"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[
                        itemNameFindList.index(itemName)]))
                continue
            # If the item is a Dungeon Armor AND the player has purchased all MaxArmor
            if itemName in dungeonArmorsList and session_data.account.dungeon_upgrades.get("MaxArmor", 0)[0] >= maxDungeonArmorsAvailable:
                slab_AdviceDict["Dungeon"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[
                        itemNameFindList.index(itemName)]))
                continue
                # If the item is a Dungeon Jewelry AND the player has purchased all MaxJewelry
            if itemName in dungeonJewelryList and session_data.account.dungeon_upgrades.get("MaxJewelry", 0)[0] >= maxDungeonJewelryAvailable:
                slab_AdviceDict["Dungeon"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[
                        itemNameFindList.index(itemName)]))
                continue

    #Just for fun. This does the opposite: Looks for items registered as owned that aren't in the expected Slab list
    # for itemName in session_data.account.registered_slab:
    #     if itemName not in slabList:
    #         slab_AdviceDict["Deprecated"].append(Advice(
    #             label=getItemDisplayName(itemName) if itemName not in knownSlabIgnorablesList else f"{getItemDisplayName(itemName)} (Probably not counted)",
    #             picture_class=getItemDisplayName(itemName) if itemName not in itemNameFindList else itemNameReplacementList[itemNameFindList.index(itemName)]))

    #Remove any empty subgroups. Caused by creating the subgroups in order to preserve order.
    emptyVendorSubgroups = []
    for subgroup in slab_AdviceDict["Vendors"]:
        if len(slab_AdviceDict["Vendors"][subgroup]) == 0:
            emptyVendorSubgroups.append(subgroup)
    for emptySubgroup in emptyVendorSubgroups:
        slab_AdviceDict["Vendors"].pop(emptySubgroup)

    emptyAnvilSubgroups = []
    for subgroup in slab_AdviceDict["Anvil"]:
        if len(slab_AdviceDict["Anvil"][subgroup]) == 0:
            emptyAnvilSubgroups.append(subgroup)
    for emptySubgroup in emptyAnvilSubgroups:
        slab_AdviceDict["Anvil"].pop(emptySubgroup)

    # Generate AdviceGroups
    slab_AdviceGroupDict["Storage"] = AdviceGroup(
        tier='',
        pre_string=f"Found in storage or on a character",
        advices=slab_AdviceDict["Storage"]
    )
    slab_AdviceGroupDict["Reclaims"] = AdviceGroup(
        tier='',
        pre_string=f"Could be reclaimed from a completed quest",
        advices=slab_AdviceDict["Reclaims"]
    )
    slab_AdviceGroupDict["Vendors"] = AdviceGroup(
        tier='',
        pre_string=f"Could be purchased from a Vendor",
        advices=slab_AdviceDict["Vendors"]
    )
    slab_AdviceGroupDict["Anvil"] = AdviceGroup(
        tier='',
        pre_string=f"Could be crafted at the Anvil",
        advices=slab_AdviceDict["Anvil"]
    )
    slab_AdviceGroupDict["Dungeon"] = AdviceGroup(
        tier='',
        pre_string=f"Could be dropped in the Dungeon",
        advices=slab_AdviceDict["Dungeon"]
    )
    slab_AdviceGroupDict["Deprecated"] = AdviceGroup(
        tier='',
        pre_string=f"In your Owned list, but not expected in The Slab. These could cause you to go over the maximum number listed in The Slab",
        advices=slab_AdviceDict["Deprecated"]
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
