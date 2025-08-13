from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import getItemDisplayName, pl
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import (
    break_you_best
)
from consts.consts_general import max_characters
from consts.consts_w5 import slab_list, dungeon_drops_list, max_dungeon_weapons_available, dungeon_weapons_list, \
    max_dungeon_armors_available, dungeon_armors_list, max_dungeon_jewelry_available, dungeon_jewelry_list, reclaimable_quest_items, slab_quest_rewards_all_chars, \
    slab_quest_rewards_once, vendor_items, vendors, anvil_items, anvil_tabs

logger = get_logger(__name__)

def getSlabProgressionTierAdviceGroups():
    slab_AdviceDict = {
        'Reclaims': [],
        'Quests': [],
        'Storage': [],
        'Vendors': {},
        'Anvil': {},
        'Dungeon': {
            'Drops': [],
            'Armor': [],
            'Weapons': []
        },
        'GemShop': [],
    }
    slab_AdviceGroups = {}
    optional_tiers = 0
    true_max = true_max_tiers['Slab']
    max_tier = true_max - optional_tiers
    tier_Slab = 0

    # Assess Tiers
    for itemName in slab_list:
        item_display_name = getItemDisplayName(itemName)
        if itemName not in session_data.account.registered_slab:
            # If the item is an Asset, meaning in storage, character inventory, or worn by a character
            if session_data.account.stored_assets.get(itemName).amount > 0:
                sources = ", ".join([
                    char.character_name for char in session_data.account.all_characters
                    if item_display_name in char.equipment.inventory
                ])
                sources = 'In Storage' if not sources else f"Inventory of {sources}"
                slab_AdviceDict['Storage'].append(Advice(
                    label=f"{item_display_name} ({sources})",
                    picture_class=item_display_name,
                    progression=0,
                    goal=1
                ))
                continue
            elif session_data.account.worn_assets.get(itemName).amount > 0:
                sources = ", ".join([
                    char.character_name for char in session_data.account.all_characters
                    if item_display_name in char.equipment.equips
                    or item_display_name in char.equipment.tools
                ])
                slab_AdviceDict['Storage'].append(Advice(
                    label=f"{item_display_name} (Equipped by {sources})",
                    picture_class=item_display_name,
                    progression=0,
                    goal=1
                ))
                continue
            elif session_data.account.npc_tokens.get(itemName, 0) > 0:
                slab_AdviceDict['Storage'].append(Advice(
                    label=f"{item_display_name} (Retrieve from NPC Tokens)",
                    picture_class=item_display_name,
                    progression=0,
                    goal=1
                ))
                continue
            # If the item is a reclaimable quest item AND the quest has been completed by at least 1 character
            if itemName in reclaimable_quest_items.keys():
                if session_data.account.compiled_quests.get(reclaimable_quest_items[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0) > 0:
                    slab_AdviceDict['Reclaims'].append(Advice(
                        label=f"{item_display_name} ({reclaimable_quest_items[itemName]['QuestGiver'].replace('_', ' ')}: {reclaimable_quest_items[itemName]['QuestName']})",
                        picture_class=item_display_name,
                        resource=reclaimable_quest_items[itemName]['QuestGiver'].replace('_', '-'),
                        progression=0,
                        goal=1
                    ))
                continue
            # If the item comes from a quest that all characters can complete AND at least 1 character hasn't completed it
            if itemName in slab_quest_rewards_all_chars.keys():
                # logger.debug(f"{itemName} quest {slab_QuestRewards[itemName]['QuestNameCoded']} completed by {session_data.account.compiled_quests.get(slab_QuestRewards[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0)}/{max_characters}")
                if session_data.account.compiled_quests.get(slab_quest_rewards_all_chars[itemName]['QuestNameCoded'], {}).get('CompletedCount',
                                                                                                                              0) < max_characters:
                    slab_AdviceDict["Quests"].append(Advice(
                        label=f"{item_display_name} ({slab_quest_rewards_all_chars[itemName]['QuestGiver'].replace('_', ' ')}: {slab_quest_rewards_all_chars[itemName]['QuestName']})",
                        picture_class=item_display_name,
                        resource=slab_quest_rewards_all_chars[itemName]['QuestGiver'].replace('_', '-'),
                        progression=0,
                        goal=1
                    ))
                continue
            # If the item comes from a quest that generally only 1 character can complete AND hasn't been completed by ANY characters yet
            if itemName in slab_quest_rewards_once.keys():
                if session_data.account.compiled_quests.get(slab_quest_rewards_once[itemName]['QuestNameCoded'], {}).get('CompletedCount', 0) < 1:
                    slab_AdviceDict["Quests"].append(Advice(
                        label=f"{item_display_name} ({slab_quest_rewards_once[itemName]['QuestGiver'].replace('_', ' ')}: {slab_quest_rewards_once[itemName]['QuestName']})",
                        picture_class=item_display_name,
                        resource=slab_quest_rewards_once[itemName]['QuestGiver'].replace('_', '-'),
                        progression=0,
                        goal=1
                    ))
                continue
            # If the item is sold by a vendor
            for vendor, vendorList in vendor_items.items():
                # If I search for the item first, these can appear out of order
                if vendor not in slab_AdviceDict["Vendors"]:
                    slab_AdviceDict["Vendors"][vendor] = []
                if itemName in vendorList:
                    slab_AdviceDict["Vendors"][vendor].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=item_display_name,
                        progression=0,
                        goal=1
                    ))
                    break
            # If the item is craftable at the anvil
            for anvilTab, anvilTabList in anvil_items.items():
                # If I search for the item first, these can appear out of order
                if anvilTab not in slab_AdviceDict["Anvil"]:
                    slab_AdviceDict["Anvil"][anvilTab] = []
                if itemName in anvilTabList:
                    slab_AdviceDict["Anvil"][anvilTab].append(Advice(
                        label=getItemDisplayName(itemName),
                        picture_class=item_display_name,
                        progression=0,
                        goal=1
                    ))
                    break
            # If the item is a unique Dungeon Drop:
            if itemName in dungeon_drops_list:
                slab_AdviceDict["Dungeon"]["Drops"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=item_display_name,
                    progression=0,
                    goal=1
                ))
                continue
            # If the item is a Dungeon Weapon AND the player has purchased all MaxWeapons
            if itemName in dungeon_weapons_list and session_data.account.dungeon_upgrades.get("MaxWeapon", 0) >= max_dungeon_weapons_available:
                slab_AdviceDict["Dungeon"]["Weapons"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=item_display_name,
                    progression=0,
                    goal=1
                ))
                continue
            # If the item is a Dungeon Armor AND the player has purchased all MaxArmor
            if itemName in dungeon_armors_list and session_data.account.dungeon_upgrades.get("MaxArmor", [0])[0] >= max_dungeon_armors_available:
                slab_AdviceDict["Dungeon"]["Armor"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=item_display_name,
                    progression=0,
                    goal=1
                ))
                continue
                # If the item is a Dungeon Jewelry AND the player has purchased all MaxJewelry
            # If the item is a Dungeon Jewelry AND the player has purchased all MaxJewelry
            if itemName in dungeon_jewelry_list and session_data.account.dungeon_upgrades.get("MaxJewelry", [0])[0] >= max_dungeon_jewelry_available:
                slab_AdviceDict["Dungeon"]["Armor"].append(Advice(
                    label=getItemDisplayName(itemName),
                    picture_class=item_display_name,
                    progression=0,
                    goal=1
                ))
                continue

    # Replace any locked Vendors with unlock note
    for vendor_name in vendors:
        if vendors[vendor_name] not in session_data.account.registered_slab:
            slab_AdviceDict["Vendors"][vendor_name] = [
                Advice(
                    label=f"{vendor_name} purchases hidden until Boss Crystal registered in The Slab",
                    picture_class=getItemDisplayName(vendors[vendor_name]),
                    progression=0,
                    goal=1
                )
            ]

    # Replace any locked Anvil Tabs with unlock note
    for subgroup in anvil_tabs:
        if anvil_tabs[subgroup] not in session_data.account.registered_slab:
            slab_AdviceDict["Anvil"][subgroup] = [
                Advice(
                    label=f"{subgroup} craftables hidden until tab registered in The Slab",
                    picture_class=subgroup,
                    progression=0,
                    goal=1
                )
            ]

    # Generate Alert
    minimal_effort_stacks = len(slab_AdviceDict['Reclaims']) + len(slab_AdviceDict['Storage'])
    if minimal_effort_stacks > 0:
        session_data.account.alerts_Advices['World 5'].append(Advice(
            label=f"{minimal_effort_stacks} minimal effort {{{{ Slab|#slab}}}} stack{pl(minimal_effort_stacks)} available",
            picture_class='the-slab',
            unrated=True,
            informational=True
        ))

    # Generate AdviceGroups
    slab_AdviceGroups['Storage'] = AdviceGroup(
        tier='',
        pre_string='Minimal Effort - Found in storage or on a character',
        advices=slab_AdviceDict['Storage'],
        informational=True
    )
    slab_AdviceGroups["Quests"] = AdviceGroup(
        tier='',
        pre_string='Could be obtained by completing a quest',
        advices=slab_AdviceDict['Quests'],
        informational=True
    )
    slab_AdviceGroups['Reclaims'] = AdviceGroup(
        tier='',
        pre_string='Minimal Effort - Could be reclaimed from a completed quest (1 per cloudsave)',
        advices=slab_AdviceDict['Reclaims'],
        informational=True
    )
    slab_AdviceGroups["Vendors"] = AdviceGroup(
        tier='',
        pre_string='Could be purchased from a Vendor',
        advices=slab_AdviceDict['Vendors'],
        informational=True
    )
    slab_AdviceGroups["Anvil"] = AdviceGroup(
        tier='',
        pre_string=f"Could be crafted at the Anvil",
        advices=slab_AdviceDict["Anvil"],
        informational=True
    )
    slab_AdviceGroups["Dungeon"] = AdviceGroup(
        tier='',
        pre_string='Could be dropped in the Dungeon',
        advices=slab_AdviceDict['Dungeon'],
        informational=True
    )
    slab_AdviceGroups["GemShop"] = AdviceGroup(
        tier='',
        pre_string='Could be purchased from the Gem Shop',
        post_string="Note: Check the Gem Shop section for proper recommendations",
        advices=slab_AdviceDict['GemShop'],
        informational=True
    )

    for ag in slab_AdviceGroups.values():
        ag.remove_empty_subgroups()

    overall_SectionTier = min(true_max, tier_Slab)
    return slab_AdviceGroups, overall_SectionTier, max_tier, true_max

def getSlabAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    slab_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getSlabProgressionTierAdviceGroups()

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
        max_tier=max_tier,
        true_max_tier=true_max,
        header=header,
        picture="Slab.png",
        groups=slab_AdviceGroupDict.values(),
        unrated=True
    )
    return slab_AdviceSection
