from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import getItemDisplayName, pl
from utils.logging import get_logger
from flask import g as session_data
from consts import slabList, reclaimableQuestItems, vendorItems, anvilItems, dungeonWeaponsList, maxDungeonWeaponsAvailable, \
    dungeonArmorsList, maxDungeonArmorsAvailable, dungeonJewelryList, maxDungeonJewelryAvailable, dungeonDropsList, anvilTabs, vendors, \
    break_you_best, slab_itemNameReplacementDict, hidden_but_constantly_avaiable_slabList, hidden_gemshopItems, slab_QuestRewards, maxCharacters

logger = get_logger(__name__)

def getHiddenAdviceGroup() -> AdviceGroup:
    hidden_adviceList = []
    hidden_names = {}
    #Just for fun. This does the opposite: Looks for items registered as owned that aren't in the expected Slab list
    for itemName in session_data.account.registered_slab:
        if itemName not in slabList:
            hidden_names[itemName] = getItemDisplayName(itemName)
            hidden_adviceList.append(Advice(
                label=getItemDisplayName(itemName),
                picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))

    #logger.debug(f"Cards1 length: {len(session_data.account.registered_slab)}")
    #logger.debug(f"{len(hidden_names)} Hidden Slab Items: {hidden_names}")
    hidden_AdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Info- These items are registered, but not displayed or included in the max",
        advices=hidden_adviceList
    )
    return hidden_AdviceGroup

def setSlabProgressionTier():
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
    slab_AdviceSection = AdviceSection(
        name="Slab",
        tier="0",
        pinchy_rating=0,
        header="Best Slab tier met: Not Yet Evaluated",
        picture="Slab.png"
    )

    tier_Slab = 0
    max_tier = 0

    #Assess Tiers
    for itemList in [slabList, hidden_but_constantly_avaiable_slabList]:
        for itemName in itemList:
            if itemName not in session_data.account.registered_slab:
                #If the item is an Asset, meaning in storage, character inventory, or worn by a character
                if session_data.account.stored_assets.get(itemName).amount > 0:
                    slab_AdviceDict["Storage"].append(Advice(
                        label=f"{getItemDisplayName(itemName)} (Storage or Inventory)",
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue
                elif session_data.account.worn_assets.get(itemName).amount > 0:
                    slab_AdviceDict["Storage"].append(Advice(
                        label=f"{getItemDisplayName(itemName)} (Equipped)",
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue
                elif session_data.account.npc_tokens.get(itemName, 0) > 0:
                    slab_AdviceDict["Storage"].append(Advice(
                        label=f"{getItemDisplayName(itemName)} (Retrieve from NPC Tokens)",
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue
                #If the item is a reclaimable quest item AND the quest has been completed by at least 1 character
                if itemName in reclaimableQuestItems.keys():
                    if session_data.account.compiled_quests.get(reclaimableQuestItems[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0) > 0:
                        slab_AdviceDict["Reclaims"].append(Advice(
                            label=f"{getItemDisplayName(itemName)} ({reclaimableQuestItems[itemName]['QuestGiver'].replace('_', ' ')}: {reclaimableQuestItems[itemName]['QuestName']})",
                            picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName],
                            resource=reclaimableQuestItems[itemName]['QuestGiver'].replace('_', '-')
                        ))
                    continue
                #If the item comes from a quest AND at least 1 character hasn't completed it
                if itemName in slab_QuestRewards.keys():
                    #logger.debug(f"{itemName} quest {slab_QuestRewards[itemName]['QuestNameCoded']} completed by {session_data.account.compiled_quests.get(slab_QuestRewards[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0)}/{maxCharacters}")
                    if session_data.account.compiled_quests.get(slab_QuestRewards[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0) < maxCharacters:
                        slab_AdviceDict["Quests"].append(Advice(
                            label=f"{getItemDisplayName(itemName)} ({slab_QuestRewards[itemName]['QuestGiver'].replace('_', ' ')}: {slab_QuestRewards[itemName]['QuestName']})",
                            picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName],
                            resource=slab_QuestRewards[itemName]['QuestGiver'].replace('_', '-')
                        ))
                    continue
                #If the item is sold by a vendor
                for vendor, vendorList in vendorItems.items():
                    # If I search for the item first, these can appear out of order
                    if vendor not in slab_AdviceDict["Vendors"]:
                        slab_AdviceDict["Vendors"][vendor] = []
                    if itemName in vendorList:
                        slab_AdviceDict["Vendors"][vendor].append(Advice(
                            label=getItemDisplayName(itemName),
                            picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                        break
                #If the item is craftable at the anvil
                for anvilTab, anvilTabList in anvilItems.items():
                    # If I search for the item first, these can appear out of order
                    if anvilTab not in slab_AdviceDict["Anvil"]:
                        slab_AdviceDict["Anvil"][anvilTab] = []
                    if itemName in anvilTabList:
                        slab_AdviceDict["Anvil"][anvilTab].append(Advice(
                            label=getItemDisplayName(itemName),
                            picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                        break
                # If the item is a unique Dungeon Drop:
                if itemName in dungeonDropsList:
                    slab_AdviceDict["Dungeon"]["Drops"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue
                #If the item is a Dungeon Weapon AND the player has purchased all MaxWeapons
                if itemName in dungeonWeaponsList and session_data.account.dungeon_upgrades.get("MaxWeapon", 0) >= maxDungeonWeaponsAvailable:
                    slab_AdviceDict["Dungeon"]["Weapons"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue
                # If the item is a Dungeon Armor AND the player has purchased all MaxArmor
                if itemName in dungeonArmorsList and session_data.account.dungeon_upgrades.get("MaxArmor", [0])[0] >= maxDungeonArmorsAvailable:
                    slab_AdviceDict["Dungeon"]["Armor"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue
                    # If the item is a Dungeon Jewelry AND the player has purchased all MaxJewelry
                # If the item is a Dungeon Jewelry AND the player has purchased all MaxJewelry
                if itemName in dungeonJewelryList and session_data.account.dungeon_upgrades.get("MaxJewelry", [0])[0] >= maxDungeonJewelryAvailable:
                    slab_AdviceDict["Dungeon"]["Armor"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue
                # If the item can always (or at least regularly) be purchased from the Gem Shop
                if itemName in hidden_gemshopItems:
                    slab_AdviceDict["GemShop"].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=getItemDisplayName(itemName) if itemName not in slab_itemNameReplacementDict else slab_itemNameReplacementDict[itemName]))
                    continue

    #Remove any empty subgroups. Caused by creating the subgroups in order to preserve order.
    emptyVendorSubgroups = []
    for subgroup in slab_AdviceDict["Vendors"]:
        if len(slab_AdviceDict["Vendors"][subgroup]) == 0:
            emptyVendorSubgroups.append(subgroup)
    for subgroup in vendors:
        if vendors[subgroup] not in session_data.account.registered_slab:
            slab_AdviceDict["Vendors"][subgroup] = [Advice(label=f"{subgroup} purchases hidden until Boss Crystal registered in The Slab", picture_class=getItemDisplayName(vendors[subgroup]))]
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

    emptyDungeonSubgroups = []
    for subgroup in slab_AdviceDict["Dungeon"]:
        if len(slab_AdviceDict["Dungeon"][subgroup]) == 0:
            emptyDungeonSubgroups.append(subgroup)
    for emptySubgroup in emptyDungeonSubgroups:
        slab_AdviceDict["Dungeon"].pop(emptySubgroup)

    # Generate Alert
    minimal_effort_stacks = len(slab_AdviceDict['Reclaims']) + len(slab_AdviceDict['Storage'])
    if minimal_effort_stacks > 0:
        session_data.account.alerts_AdviceDict['World 5'].append(Advice(
            label=f"{minimal_effort_stacks} minimal effort {{{{ Slab|#slab}}}} stack{pl(minimal_effort_stacks)} available",
            picture_class='the-slab'
        ))

    # Generate AdviceGroups
    slab_AdviceGroupDict["Storage"] = AdviceGroup(
        tier='',
        pre_string=f"Found in storage or on a character",
        advices=slab_AdviceDict["Storage"]
    )
    slab_AdviceGroupDict["Quests"] = AdviceGroup(
        tier='',
        pre_string=f"Could be obtained by completing a quest",
        advices=slab_AdviceDict["Quests"]
    )
    slab_AdviceGroupDict["Reclaims"] = AdviceGroup(
        tier='',
        pre_string=f"Could be reclaimed from a completed quest (1 per cloudsave)",
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
    slab_AdviceGroupDict["GemShop"] = AdviceGroup(
        tier='',
        pre_string=f"Could be purchased from the Gem Shop",
        advices=slab_AdviceDict["GemShop"]
    )

    #The Hidden group is currently commented out as it was causing a lot of confusion on day one. Might bring it back later though.
    slab_AdviceGroupDict["Hidden"] = getHiddenAdviceGroup()

    # Generate AdviceSection
    overall_SlabTier = min(max_tier, tier_Slab)
    tier_section = f"{overall_SlabTier}/{max_tier}"
    slab_AdviceSection.tier = tier_section
    slab_AdviceSection.pinchy_rating = overall_SlabTier
    slab_AdviceSection.groups = slab_AdviceGroupDict.values()
    if len(slab_AdviceSection.groups) == 0:
        slab_AdviceSection.header = f"All currently owned items registered in The Slab{break_you_best}"
        slab_AdviceSection.complete = True
    else:
        slab_AdviceSection.header = f"You're missing some obtainable Slab stacks!"

    return slab_AdviceSection
