import json
from collections import defaultdict
from models import Advice, AdviceGroup, AdviceSection
from utils import get_logger
from consts import progressionTiers, numberOfArtifacts, numberOfArtifactTiers, getSpecificSkillLevelsList
from flask import g as session_data

logger = get_logger(__name__)


def try_exclude_SoupedUpTube(exclusionList):
    sum_LabLevels = sum(session_data.account.all_skills["Lab"])
    if sum_LabLevels >= 180:
        exclusionList.append("Souped Up Tube")


def try_exclude_FluorescentFlaggies(exclusionList):
    """
    0 through 95 are cogs placed on the board
    96-98 are gray cog-making characters
    99-101 are yellow cog-making
    102-104 are red cog-making
    105-107 are purple cog-making
    """
    cogList = session_data.account.raw_data["CogO"]
    if isinstance(cogList, str):
        cogList = json.loads(cogList)

    cogBlanks = sum(1 for cog in cogList[0:95] if cog == "Blank")
    if cogBlanks <= 60:
        exclusionList.append("Fluorescent Flaggies")


def try_exclude_BurningBadBooks(exclusionList):
    empty = str([0] * 8)
    autoArmLevel = json.loads(session_data.account.raw_data.get("Tower", empty))[7]

    if int(autoArmLevel) >= 5:
        exclusionList.append("Burning Bad Books")


def try_exclude_ChestSluggo(exclusionList):
    try:
        artifact_tiers = json.loads(session_data.account.raw_data.get("Sailing", []))
        if isinstance(artifact_tiers, str):
            artifact_tiers = json.loads(artifact_tiers)
    except:
        logger.exception(f"Could not retrieve 'Sailing' from JSON")
        return

    sum_artifactTiers = sum(artifact_tiers[3]) if artifact_tiers and len(artifact_tiers) >= 4 else 0

    if sum_artifactTiers == numberOfArtifacts * numberOfArtifactTiers:  # 33 artifacts times 4 tiers each = 132 for v2.00
        exclusionList.append("Chest Sluggo")


def getGemShopExclusions():
    exclusionList = []
    try_exclude_SoupedUpTube(exclusionList)
    try_exclude_FluorescentFlaggies(exclusionList)
    try_exclude_BurningBadBooks(exclusionList)
    try_exclude_ChestSluggo(exclusionList)

    return exclusionList


def getBonusSectionName(bonusName):
    match bonusName:
        case 'Item Backpack Space' | 'Storage Chest Space' | 'Carry Capacity' | 'Food Slot' | 'More Storage Space' | 'Card Presets':
            return "Inventory and Storage"

        case 'Daily Teleports' | 'Daily Minigame Plays':
            return "Dailies N' Resets"

        case 'Extra Card Slot':
            return "Cards"

        case 'Weekly Dungeon Boosters':
            return "Goods & Services"

        case 'Infinity Hammer' | 'Brimstone Forge Slot' | 'Ivory Bubble Cauldrons' | 'Bleach Liquid Cauldrons' | 'Obol Storage Space' | 'Sigil Supercharge':
            return "W1&2"

        case 'Crystal 3d Printer' | 'More Sample Spaces' | 'Burning Bad Books' | 'Prayer Slots' | 'Zen Cogs' | 'Cog Inventory Space' | 'Tower Building Slots' | 'Fluorescent Flaggies':
            return "W3"

        case 'Royal Egg Cap' | 'Richelin Kitchen' | 'Souped Up Tube' | 'Pet Storage' | 'Fenceyard Space':
            return "W4"

        case 'Chest Sluggo' | 'Divinity Sparkie' | 'Golden Sprinkler' | 'Lava Sprouts':
            return "W5"

        case 'Plot of Land' | 'Pristine Charm' | 'Shroom Familiar' | 'Sand of Time' | 'Instagrow Generator' | 'Life Refill' | 'Compost Bag' | 'Summoner Stone':
            return "W6"

        case 'FOMO-1' | 'FOMO-2' | 'FOMO-3' | 'FOMO-4' | 'FOMO-5' | 'FOMO-6' | 'FOMO-7' | 'FOMO-8':
            return "Limited Shop"
        case _:
            return "UnknownShop"

def getBoughtGemShopItems():
    parsedList = json.loads(session_data.account.raw_data["GemItemsPurchased"])
    gemShopDict = {
        #Inventory and Storage
        'Item Backpack Space': 0,
        'Storage Chest Space': 0,
        'Carry Capacity': 0,
        'Food Slot': 0,
        'More Storage Space': 0,
        'Card Presets': 0,

        #Dailies N' Resets
        'Daily Teleports': 0,
        'Daily Minigame Plays': 0,

        #Cards
        'Extra Card Slot': 0,

        #Goods & Services
        'Weekly Dungeon Boosters': 0,

        #World 1&2
        'Infinity Hammer': 0,
        'Brimstone Forge Slot': 0,
        'Ivory Bubble Cauldrons': 0,
        'Bleach Liquid Cauldrons': 0,
        'Obol Storage Space': 0,
        'Sigil Supercharge': 0,

        #World 3
        'Crystal 3d Printer': 0,
        'More Sample Spaces': 0,
        'Burning Bad Books': 0,
        'Prayer Slots': 0,
        'Zen Cogs': 0,
        'Cog Inventory Space': 0,
        'Tower Building Slots': 0,
        'Fluorescent Flaggies': 0,

        #World 4
        'Royal Egg Cap': 0,
        'Richelin Kitchen': 0,
        'Souped Up Tube': 0,
        'Pet Storage': 0,
        'Fenceyard Space': 0,

        #World 5
        'Chest Sluggo': 0,
        'Divinity Sparkie': 0,
        'Golden Sprinkler': 0,
        'Lava Sprouts': 0,

        #World 6
        'W6-Placeholder1': 0,  # TODO: DELETE ME AFTER UPDATING GEMSHOP RECOMMENDATIONS
        'Plot of Land': 0,
        'Pristine Charm': 0,
        'Shroom Familiar': 0,
        'Sand of Time': 0,
        'Instagrow Generator': 0,
        'Life Refill': 0,
        'Compost Bag': 0,
        'Summoner Stone': 0,

        #Fomo
        'FOMO-1': 0,
        'FOMO-2': 0,
        'FOMO-3': 0,
        'FOMO-4': 0,
        'FOMO-5': 0,
        'FOMO-6': 0,
        'FOMO-7': 0,
        'FOMO-8': 0
    }  # Default 0s
    try:
        gemShopDict = {
            #Inventory and Storage
            'Item Backpack Space': parsedList[55],
            'Storage Chest Space': parsedList[56],
            'Carry Capacity': parsedList[58],
            'Food Slot': parsedList[59],
            'More Storage Space': parsedList[109],
            'Card Presets': parsedList[66],

            #Dailies N' Resets
            'Daily Teleports': parsedList[71],
            'Daily Minigame Plays': parsedList[72],

            #Cards
            'Extra Card Slot': parsedList[63],

            #Goods & Services
            'Weekly Dungeon Boosters': parsedList[84],

            #World 1&2
            'Infinity Hammer': parsedList[103],
            'Brimstone Forge Slot': parsedList[104],
            'Ivory Bubble Cauldrons': parsedList[105],
            'Bleach Liquid Cauldrons': parsedList[106],
            'Obol Storage Space': parsedList[57],
            'Sigil Supercharge': parsedList[110],

            #World 3
            'Crystal 3d Printer': parsedList[111],
            'More Sample Spaces': parsedList[112],
            'Burning Bad Books': parsedList[113],
            'Prayer Slots': parsedList[114],
            'Zen Cogs': parsedList[115],
            'Cog Inventory Space': parsedList[116],
            'Tower Building Slots': parsedList[117],
            'Fluorescent Flaggies': parsedList[118],

            #World 4
            'Royal Egg Cap': parsedList[119],
            'Richelin Kitchen': parsedList[120],
            'Souped Up Tube': parsedList[123],
            'Pet Storage': parsedList[124],
            'Fenceyard Space': parsedList[125],

            #World 5
            'Chest Sluggo': parsedList[129],
            'Divinity Sparkie': parsedList[130],
            'Golden Sprinkler': parsedList[131],
            'Lava Sprouts': parsedList[133],

            #World 6
            'Plot of Land': parsedList[135],
            'Pristine Charm': parsedList[136],
            'Shroom Familiar': parsedList[137],
            'Sand of Time': parsedList[138],
            'Instagrow Generator': parsedList[139],
            'Life Refill': parsedList[140],
            'Compost Bag': parsedList[141],
            'Summoner Stone': parsedList[142],

            #Fomo
            'FOMO-1': parsedList[87],
            'FOMO-2': parsedList[88],
            'FOMO-3': parsedList[89],
            'FOMO-4': parsedList[90],
            'FOMO-5': parsedList[91],
            'FOMO-6': parsedList[92],
            'FOMO-7': parsedList[93],
            'FOMO-8': parsedList[94]
        }
    except Exception as reason:
        logger.exception("Unable to parse Gem Shop:", exc_info=reason)
    # logger.debug(gemShopDict)
    return gemShopDict


def setGemShopProgressionTier():
    boughtItems = getBoughtGemShopItems()
    gemShopExclusions = getGemShopExclusions()

    recommended_stock = {item: count for tier in progressionTiers["Gem Shop"] for item, count in tier[2].items()}

    for exclusion in gemShopExclusions:
        boughtItems.pop(exclusion, None)
        recommended_stock.pop(exclusion, None)

    recommended_total = sum(recommended_stock.values())

    recommended_stock_bought = {k: min(v, boughtItems.get(k, 0)) for k, v in recommended_stock.items()}
    recommended_total_bought = sum(recommended_stock_bought.values())

    #Review all tiers
    #progressionTiers[tier][0] = int tier
    #progressionTiers[tier][1] = str tierName
    #progressionTiers[tier][2] = dict recommendedPurchases
    #progressionTiers[tier][3] = str notes

    all_groups = ["SS", *"SABCD", "Practical Max", "True Max"]
    groups = [
        AdviceGroup(
            tier="",
            pre_string=tier,
            post_string=progressionTiers["Gem Shop"][i][3],
            hide=False,
            advices=[
                Advice(label=f"{name} ({getBonusSectionName(name)})", picture_class=name, progression=int(prog), goal=int(goal))
                for name, qty in progressionTiers["Gem Shop"][i][2].items()
                if name in recommended_stock_bought
                and (prog := float(recommended_stock_bought[name])) < (goal := float(qty))
            ]
        )
        for i, tier in enumerate(all_groups, start=1)
    ]

    groups = [g for g in groups if g]
    # show only first 3 groups
    for group in groups[3:]:
        group.hide = True

    tier = f"{recommended_total_bought}/{recommended_total}"
    if not groups:
        section_title = f"You bought all {tier} Recommended Permanent/Non-Gamba Gem Shop purchases<br>Your shine blinds me, you diamond-donned dragon! 💎"
    else:
        section_title = f"Bought {tier} Recommended Permanent/Non-Gamba Gem Shop purchases"
    disclaimer = (
        "DISCLAIMER: Recommended Gem Shop purchases are listed in their World order. "
        "All purchases within the same Ranking are approximately the same priority. "
        "Remember that items in the Limited Shop section could be more important than "
        "these always-available upgrades! Check the Limited Shop after each new "
        "patch/update."
    )
    section = AdviceSection(
        name="Gem Shop",
        tier=tier,
        header=section_title,
        picture="gemshop.png",
        groups=groups,
        note=disclaimer
    )

    return section
