from models.models import Advice, AdviceGroup, AdviceSection
from utils.data_formatting import safe_loads
from utils.logging import get_logger
from consts import gemShop_progressionTiers, maxFarmingCrops
from flask import g as session_data

logger = get_logger(__name__)


def try_exclude_DungeonTickets(exclusionList):
    #Scenario 1: All Credit and Flurbo upgrades maxed
    #8 Credit Upgrades with max Rank 100 in [1]
    #8 Flurbo Upgrades with max Rank 50 in [5]
    if sum(session_data.account.dungeon_upgrades.get("CreditShop", [0])) == 100*8 and sum(session_data.account.dungeon_upgrades.get("FlurboShop", [0])) == 50*8:
        if 'Weekly Dungeon Boosters' not in exclusionList:
            exclusionList.append('Weekly Dungeon Boosters')
            return

    #Scenario 2: Over Rank 50 or 200+ tickets
    if session_data.account.raw_optlacc_dict:
        try:
            ##Blatantly stolen list from IE lol
            #https://github.com/Sludging/idleon-efficiency/blob/74f83dd4c0b15f399ffb1f87bc2bc8c9bc9b924c/data/domain/dungeons.tsx#L16
            dungeonLevelsList = [0, 4, 10, 18, 28, 40, 70, 110, 160, 230, 320, 470, 670, 940, 1310, 1760, 2400, 3250, 4000, 5000, 6160, 8000, 10000, 12500,
                                 15000, 18400, 21000, 25500, 30500, 36500, 45400, 52000, 61000, 72500, 85000, 110000, 125000, 145000, 170000, 200000, 250000,
                                 275000, 325000, 400000, 490000, 600000, 725000, 875000, 1000000, 1200000, 1500000, 3000000, 5000000, 10000000, 20000000,
                                 30000000, 40000000, 50000000, 60000000, 80000000, 100000000, 999999999, 999999999, 999999999, 999999999, 999999999, 1999999999,
                                 1999999999, 1999999999, 1999999999, 1999999999]
            playerDungeonXP = session_data.account.raw_optlacc_dict[71]
            playerDungeonRank = 0
            for xpRequirement in dungeonLevelsList:
                if playerDungeonXP >= xpRequirement:
                    playerDungeonRank += 1
            playerCredits = session_data.account.raw_optlacc_dict[72]
            playerFlurbo = session_data.account.raw_optlacc_dict[73]
            playerBoosters = session_data.account.raw_optlacc_dict[76] - 1  #The true value is always 1 less than JSON. Silly Lava
        except:
            playerDungeonRank = 1
            playerCredits = 0
            playerFurbo = 0
            playerBoosters = 0
        if playerDungeonRank >= 50 or playerBoosters >= 200:
            if 'Weekly Dungeon Boosters' not in exclusionList:
                exclusionList.append('Weekly Dungeon Boosters')
                return


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
    try:
        cogList = safe_loads(session_data.account.raw_data.get("CogO", []))
        cogBlanks = sum(1 for cog in cogList[0:95] if cog == "Blank")
        if cogBlanks <= 60:
            exclusionList.append("Fluorescent Flaggies")
    except:
        pass


def try_exclude_BurningBadBooks(exclusionList):
    if session_data.account.construction_buildings['Automation Arm']['Level'] >= 5:
        exclusionList.append("Burning Bad Books")


def try_exclude_ChestSluggo(exclusionList):
    # 33 artifacts times 4 tiers each = 132 for v2.09
    # Minus the new 3 lanterns and giants eye, 29 * 2 = 58 expected count when finishing all Ancient artifacts
    # 58/132 = 43.94% of all possibly artifacts. They know what they're getting into at that point.
    if session_data.account.sum_artifact_tiers >= 58:  #(numberOfArtifacts * numberOfArtifactTiers) * 0.43:
        exclusionList.append("Chest Sluggo")

def try_exclude_GoldenSprinkler(exclusionList):
    if (
        session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked']
        or session_data.account.gaming['BitsOwned'] >= 1e47  #Red 100B
        or session_data.account.gaming['FertilizerValue'] >= 420
        or session_data.account.gaming['FertilizerSpeed'] >= 500
        or session_data.account.farming["CropsUnlocked"] >= maxFarmingCrops * 0.8
    ):
        exclusionList.append("Golden Sprinkler")

def try_exclude_ShroomFamiliar(exclusionList):
    #if Red is at least half-way finished, exclude
    if session_data.account.summoning['Battles']['Red'] >= 8:
        exclusionList.append("Shroom Familiar")

def getGemShopExclusions():
    exclusionList = []
    try_exclude_SoupedUpTube(exclusionList)
    try_exclude_FluorescentFlaggies(exclusionList)
    try_exclude_BurningBadBooks(exclusionList)
    try_exclude_ChestSluggo(exclusionList)
    try_exclude_GoldenSprinkler(exclusionList)

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
    parsedList = safe_loads(session_data.account.raw_data["GemItemsPurchased"])
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
    for k, v in gemShopDict.items():
        if not isinstance(v, int):
            try:
                gemShopDict[k] = int(v)
            except:
                logger.warning(f"Could not force {k}'s {type(v)} {v} to int. Setting to 0.")
                gemShopDict[k] = 0
    session_data.account.gemshop = gemShopDict
    return gemShopDict


def setGemShopProgressionTier():
    boughtItems = getBoughtGemShopItems()
    gemShopExclusions = getGemShopExclusions()

    recommended_stock = {item: count for tier in gemShop_progressionTiers for item, count in tier[2].items()}

    recommended_total = sum(recommended_stock.values())

    recommended_stock_bought = {k: min(v, boughtItems.get(k, 0)) for k, v in recommended_stock.items()}
    recommended_total_bought = sum(recommended_stock_bought.values())

    #Review all tiers
    #progressionTiers[tier][0] = int tier
    #progressionTiers[tier][1] = str tierName
    #progressionTiers[tier][2] = dict recommendedPurchases
    #progressionTiers[tier][3] = str notes

    filtered_groups = ["SS", *"SABCD", "Practical Max"]
    groups = [
        AdviceGroup(
            tier="",
            pre_string=tier,
            post_string=gemShop_progressionTiers[i][3],
            hide=False,
            advices=[
                Advice(label=f"{name} ({getBonusSectionName(name)})", picture_class=name, progression=int(prog), goal=int(goal))
                for name, qty in gemShop_progressionTiers[i][2].items()
                if name in recommended_stock_bought
                and name not in gemShopExclusions
                and (prog := float(recommended_stock_bought[name])) < (goal := float(qty))
            ]
        )
        for i, tier in enumerate(filtered_groups, start=1)
    ]

    unfiltered_groups = ["True Max"]
    for i, tier in enumerate(unfiltered_groups, start=8):
        groups.append(AdviceGroup(
                tier="",
                pre_string=tier,
                post_string=gemShop_progressionTiers[i][3],
                hide=False,
                advices=[
                    Advice(label=f"{name} ({getBonusSectionName(name)})", picture_class=name, progression=int(prog), goal=int(goal))
                    for name, qty in gemShop_progressionTiers[i][2].items()
                    if name in recommended_stock_bought
                    #and name not in gemShopExclusions  #Leaving this as a comment here to show intention. DO NOT FILTER!
                    and (prog := float(recommended_stock_bought[name])) < (goal := float(qty))
                ]
        ))

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
