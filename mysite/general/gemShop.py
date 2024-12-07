from models.models import Advice, AdviceGroup, AdviceSection
from utils.data_formatting import safe_loads, safer_get
from utils.logging import get_logger
from consts import gemShop_progressionTiers, maxFarmingCrops, currentWorld, breedingTotalPets, cookingCloseEnough, break_you_best
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

    #Scenario 2: Over Rank 40 or 100+ tickets
    try:
        #playerCredits = safer_get(session_data.account.raw_optlacc_dict, 72, 0)
        #playerFlurbo = safer_get(session_data.account.raw_optlacc_dict, 73, 0)
        playerBoosters = safer_get(session_data.account.raw_optlacc_dict, 76, 1) - 1  #The true value is always 1 less than JSON. Silly Lava
    except:
        playerBoosters = 0
    if session_data.account.playerDungeonRank >= 40 or playerBoosters >= 100:
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

def try_exclude_EggCapacity(exclusionList):
    if session_data.account.breeding['Total Unlocked Count'] >= breedingTotalPets - 5:
        exclusionList.append('Royal Egg Cap')

def try_exclude_Kitchens(exclusionList):
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        exclusionList.append('Richelin Kitchen')

def try_exclude_ChestSluggo(exclusionList):
    # 33 artifacts times 4 tiers each = 132 for v2.09
    # Minus the new 3 lanterns and giants eye, 29 * 2 = 58 expected count when finishing all Ancient artifacts
    # 58/132 = 43.94% of all possibly artifacts. They know what they're getting into at that point.
    if session_data.account.sum_artifact_tiers >= 58:  #(numberOfArtifacts * numberOfArtifactTiers) * 0.43:
        exclusionList.append("Chest Sluggo")

def try_exclude_Gaming(exclusionList):
    if (
        session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked']
        or session_data.account.gaming['FertilizerValue'] >= 420
        or session_data.account.gaming['FertilizerSpeed'] >= 500
        or session_data.account.farming['CropsUnlocked'] >= maxFarmingCrops * 0.75
    ):
        exclusionList.append('Golden Sprinkler')
        exclusionList.append('Lava Sprouts')
        return
    try:
        if session_data.account.gaming['BitsOwned'] >= 1e47:  #Red 100B
            exclusionList.append('Golden Sprinkler')
            exclusionList.append('Lava Sprouts')
    except:
        pass

def try_exclude_ShroomFamiliar(exclusionList):
    #if Red is at least half-way finished, exclude
    if session_data.account.summoning['Battles']['Red'] >= 8:
        exclusionList.append('Shroom Familiar')

def try_exclude_IvoryBubbleCauldrons(exclusionList):
    if session_data.account.alchemy_cauldrons['NextWorldMissingBubbles'] > currentWorld:
        exclusionList.append('Ivory Bubble Cauldrons')

def try_exclude_farming(exclusionList):
    if session_data.account.farming["CropsUnlocked"] >= maxFarmingCrops:
        exclusionList.append('Instagrow Generator')
        exclusionList.append('Plot of Land')

def try_exclude_Sigils(exclusionList):
    if (
        session_data.account.alchemy_p2w['Sigils']['Pea Pod']['PrechargeLevel'] >= 3
        or session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level'] >= 3
    ):
        exclusionList.append('Sigil Supercharge')

def getGemShopFullExclusions():
    # Exclusions for SS through Practical Max. Not applied to True Max only
    exclusionList = []
    #W1
    try_exclude_DungeonTickets(exclusionList)
    #W2
    try_exclude_IvoryBubbleCauldrons(exclusionList)
    try_exclude_Sigils(exclusionList)
    #W3
    try_exclude_FluorescentFlaggies(exclusionList)
    try_exclude_BurningBadBooks(exclusionList)
    #W4
    try_exclude_SoupedUpTube(exclusionList)
    try_exclude_EggCapacity(exclusionList)
    try_exclude_Kitchens(exclusionList)
    #W5
    try_exclude_ChestSluggo(exclusionList)
    try_exclude_Gaming(exclusionList)
    #W6

    return exclusionList

def getGemShopPartialExclusions():
    #Exclusions for SS through D only. Not applied to Practical Max or True Max
    exclusionList = []
    #W1
    #W2
    #W3
    #W4
    #W5
    #W6
    try_exclude_farming(exclusionList)
    try_exclude_ShroomFamiliar(exclusionList)

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
        case 'Blinding Lantern' | 'Parallel Villagers The Explorer' | 'Parallel Villagers The Engineer' | 'Parallel Villagers The Conjuror' | 'Parallel Villagers The Measurer' | 'Resource Boost' | 'Conjuror Pts' | 'Opal':
            return "Oddities"
        case _:
            return "UnknownShop"

def getGemShopAdviceSection() -> AdviceSection:
    boughtItems = session_data.account.gemshop
    fullExclusions = getGemShopFullExclusions()  # Exclusions for SS through Practical Max. Not applied to True Max only
    partialExclusions = fullExclusions + getGemShopPartialExclusions()  #Exclusions for SS through D only. Not applied to Practical Max or True Max

    recommended_stock = {item: count for tier in gemShop_progressionTiers for item, count in tier[2].items()}
    recommended_total = sum(recommended_stock.values())
    recommended_stock_bought = {k: min(v, boughtItems.get(k, 0)) for k, v in recommended_stock.items()}
    recommended_total_bought = sum(recommended_stock_bought.values())

    #Review all tiers
    #progressionTiers[tier][0] = int tier
    #progressionTiers[tier][1] = str tierName
    #progressionTiers[tier][2] = dict recommendedPurchases
    #progressionTiers[tier][3] = str notes

    filtered_groups = ["SS", *"SABCD"]
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
                and name not in partialExclusions
                and (prog := float(recommended_stock_bought[name])) < (goal := float(qty))
            ],
            informational=True
        )
        for i, tier in enumerate(filtered_groups, start=1)
    ]

    partially_filtered_groups = ["Practical Max"]
    for i, tier in enumerate(partially_filtered_groups, start=7):
        groups.append(AdviceGroup(
            tier="",
            pre_string=tier,
            post_string=gemShop_progressionTiers[i][3],
            hide=False,
            advices=[
                Advice(label=f"{name} ({getBonusSectionName(name)})", picture_class=name, progression=int(prog), goal=int(goal))
                for name, qty in gemShop_progressionTiers[i][2].items()
                if name in recommended_stock_bought
                and name not in fullExclusions
                and (prog := float(recommended_stock_bought[name])) < (goal := float(qty))
            ],
            informational=True
        ))

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
            ],
            informational=True
        ))

    groups = [g for g in groups if g]
    # show only first 3 groups
    for group in groups[3:]:
        group.hide = True

    tier = f"{recommended_total_bought}/{recommended_total}"
    if not groups:
        section_title = (f"You bought all {tier} Recommended Permanent/Non-Gamba Gem Shop purchases"
                         f"<br>Your shine blinds me, you diamond-donned dragon! 💎"
                         f"{break_you_best}")
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
        note=disclaimer,
        unrated=True,
        informational=True
    )

    return section
