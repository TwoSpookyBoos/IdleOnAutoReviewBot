from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.general import get_gem_shop_purchase_advice
from utils.safer_data_handling import safe_loads, safer_get, safer_convert
from utils.logging import get_logger
from consts.consts_autoreview import break_you_best, EmojiType
from consts.consts_general import gem_shop_optlacc_dict
from consts.idleon.consts_idleon import current_world, max_characters
from consts.w6.farming import max_farming_crops
from consts.consts_caverns import max_cavern, max_majiks, caverns_max_measurements, getMaxEngineerLevel
from consts.consts_w4 import cooking_close_enough, breeding_total_pets
from consts.progression_tiers import gemShop_progressionTiers


logger = get_logger(__name__)


def try_exclude_DungeonTickets(exclusionLists):
    #Scenario 1: All Credit and Flurbo upgrades maxed
    #8 Credit Upgrades with max Rank 100 in [1]
    #8 Flurbo Upgrades with max Rank 50 in [5]
    if sum(session_data.account.dungeon_upgrades.get('CreditShop', [0])) == 100*8 and sum(session_data.account.dungeon_upgrades.get('FlurboShop', [0])) == 50*8:
        if 'Weekly Dungeon Boosters' not in exclusionLists:
            for sublist in exclusionLists:
                sublist.append('Weekly Dungeon Boosters')
            return

    #Scenario 2: Over Rank 40 or 100+ tickets
    try:
        playerBoosters = safer_get(session_data.account.raw_optlacc_dict, 76, 1) - 1  #The true value is always 1 less than JSON. Silly Lava
    except:
        playerBoosters = 0
    if session_data.account.playerDungeonRank >= 40 or playerBoosters >= 100:
        if 'Weekly Dungeon Boosters' not in exclusionLists:
            for sublist in exclusionLists:
                sublist.append('Weekly Dungeon Boosters')
            return

def try_exclude_SoupedUpTube(exclusionLists):
    sum_LabLevels = sum(session_data.account.all_skills['Laboratory'])
    if sum_LabLevels >= 180:
        for sublist in exclusionLists:
            sublist.append('Souped Up Tube')

def try_exclude_FluorescentFlaggies(exclusionLists):
    """
    0 through 95 are cogs placed on the board
    96-98 are gray cog-making characters
    99-101 are yellow cog-making
    102-104 are red cog-making
    105-107 are purple cog-makingss_through_d_exclusions
    """
    try:
        cogList = safe_loads(session_data.account.raw_data.get('CogO', []))
        cogBlanks = sum(1 for cog in cogList[0:95] if cog == 'Blank')
        if cogBlanks <= 60:
            for sublist in exclusionLists:
                sublist.append('Fluorescent Flaggies')
    except:
        pass

def try_exclude_BurningBadBooks(exclusionLists):
    if session_data.account.construction_buildings['Automation Arm']['Level'] >= 5:
        for sublist in exclusionLists:
            sublist.append('Burning Bad Books')

def try_exclude_EggCapacity(exclusionLists):
    if session_data.account.breeding['Total Unlocked Count'] >= breeding_total_pets - 5:
        for sublist in exclusionLists:
            sublist.append('Royal Egg Cap')

def try_exclude_Kitchens(exclusionLists):
    if session_data.account.cooking['MaxRemainingMeals'] < cooking_close_enough:
        for sublist in exclusionLists:
            sublist.append('Richelin Kitchen')

def try_exclude_ChestSluggo(exclusionLists):
    # 33 artifacts times 4 tiers each = 132 for v2.26
    # Minus the new 3 lanterns and giants eye, 29 * 2 = 58 expected count when finishing all Ancient artifacts
    # 58/132 = 43.94% of all possibly artifacts. They know what they're getting into at that point.
    if session_data.account.sum_artifact_tiers >= 58:  #(sailing_artifacts_count * max_sailing_artifact_level) * 0.43:
        for sublist in exclusionLists:
            sublist.append('Chest Sluggo')

def try_exclude_Gaming(exclusionLists):
    if (
        session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked']
        or session_data.account.gaming['FertilizerValue'] >= 420
        or session_data.account.gaming['FertilizerSpeed'] >= 500
        or session_data.account.farming.crops.unlocked >= max_farming_crops * 0.75
    ):
        for sublist in exclusionLists:
            sublist.append('Golden Sprinkler')
            sublist.append('Lava Sprouts')
        return
    try:
        if session_data.account.gaming['BitsOwned'] >= 1e47:  #Red 100B
            for sublist in exclusionLists:
                sublist.append('Golden Sprinkler')
                sublist.append('Lava Sprouts')
    except:
        pass
    
def try_exclude_ConjurorPts(exclusionLists):
    if session_data.account.gemshop['Purchases']['Conjuror Pts']['Owned'] >= max_majiks - session_data.account.caverns['Villagers']['Cosmos']['Level']:
        for sublist in exclusionLists:
            sublist.append('Conjuror Pts')
    
def try_exclude_ParallelVillagers(exclusionLists):
    if session_data.account.caverns['Villagers']['Polonai']['Level'] >= max_cavern:
        for sublist in exclusionLists:
            sublist.append('Parallel Villagers The Explorer')
        
    if session_data.account.caverns['Villagers']['Kaipu']['Level'] >= getMaxEngineerLevel():
        for sublist in exclusionLists:
            sublist.append('Parallel Villagers The Engineer')
        
    if session_data.account.caverns['Villagers']['Cosmos']['Level'] >= (max_majiks - session_data.account.gemshop['Purchases']['Conjuror Pts']['Owned']):
        for sublist in exclusionLists:
            sublist.append('Parallel Villagers The Conjuror')
        
    if session_data.account.caverns['Villagers']['Minau']['Level'] >= caverns_max_measurements:
        for sublist in exclusionLists:
            sublist.append('Parallel Villagers The Measurer')

def try_exclude_ShroomFamiliar(exclusionLists):
    #if Red is at least half-way finished, exclude
    if session_data.account.summoning['Battles']['Red'] >= 8:
        for sublist in exclusionLists:
            sublist.append('Shroom Familiar')

def try_exclude_IvoryBubbleCauldrons(exclusionLists):
    if session_data.account.alchemy_cauldrons['NextWorldMissingBubbles'] > current_world:
        for sublist in exclusionLists:
            sublist.append('Ivory Bubble Cauldrons')

def try_exclude_Farming(exclusionLists):
    if session_data.account.farming.crops.unlocked >= max_farming_crops:
        for sublist in exclusionLists:
            sublist.append('Instagrow Generator')
            sublist.append('Plot of Land')

def try_exclude_Sigils(exclusionLists):
    if (
        session_data.account.alchemy_p2w['Sigils']['Pea Pod']['PrechargeLevel'] >= 3
        or session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level'] >= 3
    ):
        for sublist in exclusionLists:
            sublist.append('Sigil Supercharge')

def getGemShopExclusions():
    s_through_d = []
    practical = []
    #W1
    try_exclude_DungeonTickets([s_through_d, practical])
    #W2
    try_exclude_IvoryBubbleCauldrons([s_through_d, practical])
    try_exclude_Sigils([s_through_d, practical])
    #W3
    try_exclude_FluorescentFlaggies([s_through_d, practical])
    try_exclude_BurningBadBooks([s_through_d, practical])
    #W4
    try_exclude_SoupedUpTube([s_through_d, practical])
    try_exclude_EggCapacity([s_through_d, practical])
    try_exclude_Kitchens([s_through_d, practical])
    #W5
    try_exclude_ChestSluggo([s_through_d, practical])
    try_exclude_Gaming([s_through_d, practical])
    #Caverns
    try_exclude_ConjurorPts([s_through_d])  #I specifically don't want these excluded from Practical Max as of 2025-01-26
    try_exclude_ParallelVillagers([s_through_d])  #I specifically don't want these excluded from Practical Max as of 2025-01-26
    #W6
    try_exclude_Farming([s_through_d])  #I specifically don't want these excluded from Practical Max as of 2025-01-26
    try_exclude_ShroomFamiliar([s_through_d])  #I specifically don't want these excluded from Practical Max as of 2025-01-26

    return s_through_d, practical

def getGemShopAdviceSection() -> AdviceSection:
    gsp = session_data.account.gemshop['Purchases']
    ss_through_d_exclusions, practical_max_exclusions = getGemShopExclusions()

    recommended_stock = {item: count for tier in gemShop_progressionTiers for item, count in tier[2].items()}
    recommended_total = sum(recommended_stock.values())
    recommended_stock_bought = {k: min(v, gsp[k]['Owned']) for k, v in recommended_stock.items()}
    recommended_total_bought = sum(recommended_stock_bought.values())

    #Review all tiers
    #progressionTiers[tier][0] = int tier
    #progressionTiers[tier][1] = str tierName
    #progressionTiers[tier][2] = dict recommendedPurchases
    #progressionTiers[tier][3] = str notes

    s_through_d_groups = [*'SABCD']
    groups = [
        AdviceGroup(
            tier='',
            pre_string=tier,
            post_string=gemShop_progressionTiers[i][3],
            hide=False,
            advices=[
                get_gem_shop_purchase_advice(name, False, goal)
                for name, qty in gemShop_progressionTiers[i][2].items()
                if name in recommended_stock_bought
                and name not in ss_through_d_exclusions
                and gsp[name]['Owned'] < (goal := int(qty))
            ],
            informational=True
        )
        for i, tier in enumerate(s_through_d_groups, start=1)
    ]

    practical_max_groups = ['Practical Max']
    for i, tier in enumerate(practical_max_groups, start=len(s_through_d_groups)+1):
        groups.append(AdviceGroup(
            tier='',
            pre_string=tier,
            post_string=gemShop_progressionTiers[i][3],
            hide=False,
            advices=[
                get_gem_shop_purchase_advice(name, False, goal)
                for name, qty in gemShop_progressionTiers[i][2].items()
                if name in recommended_stock_bought
                and name not in practical_max_exclusions
                and gsp[name]['Owned'] < (goal := int(qty))
            ],
            informational=True
        ))

    unfiltered_groups = ['True Max']
    for i, tier in enumerate(unfiltered_groups, start=len(s_through_d_groups)+len(practical_max_groups)+1):
        groups.append(AdviceGroup(
            tier='',
            pre_string=tier,
            post_string=gemShop_progressionTiers[i][3],
            hide=False,
            advices=[
                get_gem_shop_purchase_advice(name, False, goal)
                for name, qty in gemShop_progressionTiers[i][2].items()
                if name in recommended_stock_bought
                #and name not in gemShopExclusions  #Leaving this as a comment here to show intention. DO NOT FILTER!
                and gsp[name]['Owned'] < (goal := int(qty))
            ],
            informational=True
        ))

    # FOMO tracked through OptionsListAccount entries
    fomo_advice = []
    for purchase_name, purchase_details in gem_shop_optlacc_dict.items():
        advice = get_gem_shop_purchase_advice(purchase_name, False)
        advice.informational = True
        advice.completed = False if gsp[purchase_name]['MaxLevel'] == EmojiType.INFINITY.value else None
        fomo_advice.append(advice)

    # FOMO Equipment
    fomo_equipment = {
        'Dune Killer Ring (W2)': {
            'Code Name': 'EquipmentRings33',
            'Goal': 2 * max_characters,
            'Image': 'dune-killer-ring'
        },
        'Tundra Killer Ring (W3)': {
            'Code Name': 'EquipmentRings31',
            'Goal': 2 * max_characters,
            'Image': 'tundra-killer-ring'
        },
        'Nebula Killer Ring (W4)': {
            'Code Name': 'EquipmentRings32',
            'Goal': 2 * max_characters,
            'Image': 'nebula-killer-ring'
        },
        'Magma Killer Ring (W5)': {
            'Code Name': 'EquipmentRings34',
            'Goal': 2 * max_characters,
            'Image': 'magma-killer-ring'
        },
        'Spirit Killer Ring (W6)': {
            'Code Name': 'EquipmentRings37',
            'Goal': 2 * max_characters,
            'Image': 'spirit-killer-ring'
        },

        'Deathbringer Hood of Death': {
            'Code Name': 'EquipmentHats112',
            'Goal': 1,
            'Image': 'deathbringer-hood-of-death'
        },
        'Windwalker Hood': {
            'Code Name': 'EquipmentHats118',
            'Goal': 1,
            'Image': 'windwalker-hood'
        },
    }
    for display, details in fomo_equipment.items():
        prog = safer_convert(session_data.account.all_assets.get(details['Code Name']).amount, 0)
        fomo_advice.append(Advice(
            label=display,
            picture_class=details['Image'],
            progression=prog,
            goal=details['Goal'],
            resource='gem' if prog < details['Goal'] else '',
            informational=True,
            completed=(
                False if details['Goal'] == EmojiType.INFINITY.value
                else session_data.account.all_assets.get(details['Code Name']).amount >= details['Goal']
            )
        ))

    for advice in fomo_advice:
        advice.mark_advice_completed()

    groups.append(AdviceGroup(
        tier='',
        pre_string='Limited Shop purchases',
        advices=fomo_advice,
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
        name='Gem Shop',
        tier=tier,
        header=section_title,
        picture='gemshop.png',
        groups=groups,
        note=disclaimer,
        unrated=True,
        informational=True
    )
    return section
