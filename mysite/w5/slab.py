from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import getItemDisplayName, pl
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    slabList, slab_itemNameReplacementDict,
    reclaimableQuestItems, slab_QuestRewardsAllChars, slab_QuestRewardsOnce,
    vendorItems, anvilItems,
    dungeonWeaponsList, maxDungeonWeaponsAvailable,
    dungeonArmorsList, maxDungeonArmorsAvailable,
    dungeonJewelryList, maxDungeonJewelryAvailable,
    dungeonDropsList,
    anvilTabs, vendors,
    hidden_but_constantly_avaiable_slabList, hidden_gemshopItems,
    maxCharacters, break_you_best
)

logger = get_logger(__name__)

def getHiddenAdviceGroup() -> AdviceGroup:
    hidden_adviceList = []
    hidden_names = {}
    #Just for fun. This does the opposite: Looks for items registered as owned that aren't in the expected Slab list
    for itemName in session_data.account.registered_slab:
        if itemName not in slabList:
            decoded_name = getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]
            hidden_names[itemName] = decoded_name
            decoded_name = 'placeholder' if decoded_name.startswith("Unknown-'") else decoded_name
            hidden_adviceList.append(Advice(
                label=decoded_name,
                picture_class=decoded_name
            ))

    #logger.debug(f"Cards1 length: {len(session_data.account.registered_slab)}")
    #logger.debug(f"{len(hidden_names)} Hidden Slab Items: {hidden_names}")
    hidden_AdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Info- These are included in your total found items, but do not appear visually on The Slab",
        advices=hidden_adviceList,
        informational=True
    )
    return hidden_AdviceGroup

def getSlabProgressionTierAdviceGroups():
    slab_AdviceDict = {
        "Reclaims": [],
        'Quests': [],
        "Storage": [],
        "Vendors": {},
        "Anvil": {},
        "Dungeon": {
            "Drops": [],
            "Armor": [],
            "Weapons": []
        },
        "GemShop": [],
    }
    slab_AdviceGroupDict = {}
    info_tiers = 0
    max_tier = 0 - info_tiers
    tier_Slab = 0

    # Assess Tiers
    for itemList in [slabList, hidden_but_constantly_avaiable_slabList]:
        for itemName in itemList:
            item_display_name = getItemDisplayName(itemName)
            item_picture = item_display_name if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]
            if itemName not in session_data.account.registered_slab:
                # If the item is an Asset, meaning in storage, character inventory, or worn by a character
                if session_data.account.stored_assets.get(itemName).amount > 0:
                    slab_AdviceDict["Storage"].append(Advice(
                        label=f"{item_display_name} (Storage or Inventory)",
                        picture_class=item_picture
                    ))
                    continue
                elif session_data.account.worn_assets.get(itemName).amount > 0:
                    slab_AdviceDict["Storage"].append(Advice(
                        label=f"{item_display_name} (Equipped)",
                        picture_class=item_picture
                    ))
                    continue
                elif session_data.account.npc_tokens.get(itemName, 0) > 0:
                    slab_AdviceDict["Storage"].append(Advice(
                        label=f"{item_display_name} (Retrieve from NPC Tokens)",
                        picture_class=item_picture
                    ))
                    continue
                # If the item is a reclaimable quest item AND the quest has been completed by at least 1 character
                if itemName in reclaimableQuestItems.keys():
                    if session_data.account.compiled_quests.get(reclaimableQuestItems[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0) > 0:
                        slab_AdviceDict["Reclaims"].append(Advice(
                            label=f"{item_display_name} ({reclaimableQuestItems[itemName]['QuestGiver'].replace('_', ' ')}: {reclaimableQuestItems[itemName]['QuestName']})",
                            picture_class=item_picture,
                            resource=reclaimableQuestItems[itemName]['QuestGiver'].replace('_', '-')
                        ))
                    continue
                # If the item comes from a quest that all characters can complete AND at least 1 character hasn't completed it
                if itemName in slab_QuestRewardsAllChars.keys():
                    # logger.debug(f"{itemName} quest {slab_QuestRewards[itemName]['QuestNameCoded']} completed by {session_data.account.compiled_quests.get(slab_QuestRewards[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0)}/{maxCharacters}")
                    if session_data.account.compiled_quests.get(slab_QuestRewardsAllChars[itemName]['QuestNameCoded'], {}).get('CompletedCount',
                                                                                                                               0) < maxCharacters:
                        slab_AdviceDict["Quests"].append(Advice(
                            label=f"{item_display_name} ({slab_QuestRewardsAllChars[itemName]['QuestGiver'].replace('_', ' ')}: {slab_QuestRewardsAllChars[itemName]['QuestName']})",
                            picture_class=item_picture,
                            resource=slab_QuestRewardsAllChars[itemName]['QuestGiver'].replace('_', '-')
                        ))
                    continue
                # If the item comes from a quest that generally only 1 character can complete AND hasn't been completed by ANY characters yet
                if itemName in slab_QuestRewardsOnce.keys():
                    if session_data.account.compiled_quests.get(slab_QuestRewardsOnce[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0) < 1:
                        slab_AdviceDict["Quests"].append(Advice(
                            label=f"{item_display_name} ({slab_QuestRewardsOnce[itemName]['QuestGiver'].replace('_', ' ')}: {slab_QuestRewardsOnce[itemName]['QuestName']})",
                            picture_class=item_picture,
                            resource=slab_QuestRewardsOnce[itemName]['QuestGiver'].replace('_', '-')
                        ))
                    continue
                # If the item is sold by a vendor
                for vendor, vendorList in vendorItems.items():
                    # If I search for the item first, these can appear out of order
                    if vendor not in slab_AdviceDict["Vendors"]:
                        slab_AdviceDict["Vendors"][vendor] = []
                    if itemName in vendorList:
                        slab_AdviceDict["Vendors"][vendor].append(Advice(
                            label=getItemDisplayName(itemName),
                            picture_class=item_picture
                        ))
                        break
                # If the item is craftable at the anvil
                for anvilTab, anvilTabList in anvilItems.items():
                    # If I search for the item first, these can appear out of order
                    if anvilTab not in slab_AdviceDict["Anvil"]:
                        slab_AdviceDict["Anvil"][anvilTab] = []
                    if itemName in anvilTabList:
                        slab_AdviceDict["Anvil"][anvilTab].append(Advice(
                            label=getItemDisplayName(itemName),
                            picture_class=item_picture
                        ))
                        break
                # If the item is a unique Dungeon Drop:
                if itemName in dungeonDropsList:
                    slab_AdviceDict["Dungeon"]["Drops"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=item_picture
                    ))
                    continue
                # If the item is a Dungeon Weapon AND the player has purchased all MaxWeapons
                if itemName in dungeonWeaponsList and session_data.account.dungeon_upgrades.get("MaxWeapon", 0) >= maxDungeonWeaponsAvailable:
                    slab_AdviceDict["Dungeon"]["Weapons"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=item_picture
                    ))
                    continue
                # If the item is a Dungeon Armor AND the player has purchased all MaxArmor
                if itemName in dungeonArmorsList and session_data.account.dungeon_upgrades.get("MaxArmor", [0])[0] >= maxDungeonArmorsAvailable:
                    slab_AdviceDict["Dungeon"]["Armor"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=item_picture
                    ))
                    continue
                    # If the item is a Dungeon Jewelry AND the player has purchased all MaxJewelry
                # If the item is a Dungeon Jewelry AND the player has purchased all MaxJewelry
                if itemName in dungeonJewelryList and session_data.account.dungeon_upgrades.get("MaxJewelry", [0])[0] >= maxDungeonJewelryAvailable:
                    slab_AdviceDict["Dungeon"]["Armor"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=item_picture
                    ))
                    continue
                # If the item can always (or at least regularly) be purchased from the Gem Shop
                if itemName in hidden_gemshopItems:
                    slab_AdviceDict["GemShop"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=item_picture
                    ))
                    continue

    # Remove any empty subgroups. Caused by creating the subgroups in order to preserve order.
    emptyVendorSubgroups = []
    for subgroup in slab_AdviceDict["Vendors"]:
        if len(slab_AdviceDict["Vendors"][subgroup]) == 0:
            emptyVendorSubgroups.append(subgroup)
    for subgroup in vendors:
        if vendors[subgroup] not in session_data.account.registered_slab:
            slab_AdviceDict["Vendors"][subgroup] = [
                Advice(label=f"{subgroup} purchases hidden until Boss Crystal registered in The Slab", picture_class=getItemDisplayName(vendors[subgroup]))]
    for emptySubgroup in emptyVendorSubgroups:
        slab_AdviceDict["Vendors"].pop(emptySubgroup)

    emptyAnvilSubgroups = []
    for subgroup in slab_AdviceDict["Anvil"]:
        if len(slab_AdviceDict["Anvil"][subgroup]) == 0:
            emptyAnvilSubgroups.append(subgroup)
    for subgroup in anvilTabs:
        if anvilTabs[subgroup] not in session_data.account.registered_slab:
            slab_AdviceDict["Anvil"][subgroup] = [Advice(label=f"{subgroup} craftables hidden until tab registered in The Slab", picture_class=subgroup)]
    for removableSubgroup in emptyAnvilSubgroups:
        slab_AdviceDict["Anvil"].pop(removableSubgroup)

    # emptyDungeonSubgroups = []
    # for subgroup in slab_AdviceDict["Dungeon"]:
    #     if len(slab_AdviceDict["Dungeon"][subgroup]) == 0:
    #         emptyDungeonSubgroups.append(subgroup)
    # for emptySubgroup in emptyDungeonSubgroups:
    #     slab_AdviceDict["Dungeon"].pop(emptySubgroup)

    # Generate Alert
    minimal_effort_stacks = len(slab_AdviceDict['Reclaims']) + len(slab_AdviceDict['Storage'])
    if minimal_effort_stacks > 0:
        session_data.account.alerts_AdviceDict['World 5'].append(Advice(
            label=f"{minimal_effort_stacks} minimal effort {{{{ Slab|#slab}}}} stack{pl(minimal_effort_stacks)} available",
            picture_class='the-slab',
            unrated=True,
            informational=True
        ))

    # Generate AdviceGroups
    slab_AdviceGroupDict["Storage"] = AdviceGroup(
        tier='',
        pre_string=f"Found in storage or on a character",
        advices=slab_AdviceDict["Storage"],
        informational=True
    )
    slab_AdviceGroupDict["Quests"] = AdviceGroup(
        tier='',
        pre_string=f"Could be obtained by completing a quest",
        advices=slab_AdviceDict["Quests"],
        informational=True
    )
    slab_AdviceGroupDict["Reclaims"] = AdviceGroup(
        tier='',
        pre_string=f"Could be reclaimed from a completed quest (1 per cloudsave)",
        advices=slab_AdviceDict["Reclaims"],
        informational=True
    )
    slab_AdviceGroupDict["Vendors"] = AdviceGroup(
        tier='',
        pre_string=f"Could be purchased from a Vendor",
        advices=slab_AdviceDict["Vendors"],
        informational=True
    )
    slab_AdviceGroupDict["Anvil"] = AdviceGroup(
        tier='',
        pre_string=f"Could be crafted at the Anvil",
        advices=slab_AdviceDict["Anvil"],
        informational=True
    )
    slab_AdviceGroupDict["Dungeon"] = AdviceGroup(
        tier='',
        pre_string=f"Could be dropped in the Dungeon",
        advices=slab_AdviceDict["Dungeon"],
        informational=True
    )
    slab_AdviceGroupDict["GemShop"] = AdviceGroup(
        tier='',
        pre_string=f"Could be purchased from the Gem Shop",
        advices=slab_AdviceDict["GemShop"],
        informational=True
    )

    overall_SectionTier = min(max_tier, tier_Slab)
    return slab_AdviceGroupDict, overall_SectionTier, max_tier

def getSlabAdviceSection() -> AdviceSection:
    # if session_data.account.highestWorldReached < 5:
    #     slab_AdviceSection = AdviceSection(
    #         name="Slab",
    #         tier="0",
    #         pinchy_rating=0,
    #         header="Come back after reaching W5 town!",
    #         picture="Slab.png",
    #         unrated=True,
    #         unreached=True,
    #     )
    #     return slab_AdviceSection

    #Generate AdviceGroups
    slab_AdviceGroupDict, overall_SectionTier, max_tier = getSlabProgressionTierAdviceGroups()
    slab_AdviceGroupDict["Hidden"] = getHiddenAdviceGroup()

    for ag in slab_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    if len(slab_AdviceGroupDict.values()) == 0:
        header = f"All currently owned items registered in The Slab{break_you_best}"
    else:
        header = f"You're missing some obtainable Slab stacks!"
    slab_AdviceSection = AdviceSection(
        name="Slab",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=header,
        picture="Slab.png",
        groups=slab_AdviceGroupDict.values(),
        unrated=True
    )
    return slab_AdviceSection
