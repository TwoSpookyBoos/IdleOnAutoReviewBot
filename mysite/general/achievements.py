from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts import break_you_best, achievements_progressionTiers, achievement_categories
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getAchievementExclusions() -> set[str]:
    exclusionsSet = set()
    if session_data.account.highestWorldReached >= 6:
        exclusionsSet.add('Golden Fly')
    if (
        session_data.account.playerDungeonRank >= 40 or
        (
            sum(session_data.account.dungeon_upgrades.get("CreditShop", [0])) == 100*8
            and sum(session_data.account.dungeon_upgrades.get("FlurboShop", [0])) == 50*8
        )
    ):
        exclusionsSet.add('Mutant Massacrer')
    return exclusionsSet

def getAchievementStatus(achievementName):
    #logger.debug(f"Looking up data for {achievementName}")
    try:
        match achievementName:
            #EZ Access
            case 'Platinum 200G':
                return notateNumber('Match', min(200000, session_data.account.all_assets.get('Plat').amount), 0, 'K'), '200K', 'platinum-ore'
            case 'Half a Mill-log':
                return notateNumber('Match', min(500000, session_data.account.all_assets.get('StumpTree').amount), 0, 'K'), '500K', 'veiny-logs'
            case 'Super Cereal':
                return notateNumber('Match', min(50000, session_data.account.all_assets.get('Bug3').amount), 0, 'K'), '50K', 'sentient-cereal'
            case 'Cool Score!':
                return notateNumber('Match', min(2500000, session_data.account.colo_scores[3]), 0, 'K'), '2500K', ''
            case 'Doctor Repellant':
                return min(10000, int(session_data.account.farming['Crops'].get(0, 0))), 10000, 'apple-crop'
            case 'Good Plate':
                return min(11, max([meal['Level'] for meal in session_data.account.meals.values()], default=0)), 11, ''
            case 'Bonsai Bonanza':
                return min(100, session_data.account.achievements[achievementName]['Raw']), 100, 'bonsai'

            #Monster Respawn
            case 'Two-Time Savior':
                return min(2, session_data.account.all_assets.get('Trophy6').amount), 2, 'blunder-hero'
            case 'Lavathian Skulls':
                return min(130, session_data.account.enemy_worlds[5].total_mk), 130, 'death-note'
            case 'Two Desserts!':
                return int(min(2, session_data.account.all_assets.get('Trophy11').amount)), 2, 'yumyum-sheriff'

            #Recipes
            case 'The Goose is Loose':
                return notateNumber('Match', min(1000000, session_data.account.all_assets.get('Critter9').amount), 0, 'K'), '1000K', 'honker'

            #Dungeon RNG
            case '2 Tons of Iron':
                return min(2000, session_data.account.all_assets.get('Iron').amount), 2000, 'iron-ore'
            case "Croakin' Froge":
                return min(250, session_data.account.all_assets.get('Critter1').amount), 250, 'froge'
            case 'Souped Up Salts':
                return min(10, session_data.account.refinery['Red']['Rank']), 10, session_data.account.refinery['Red']['Image']

            #Other Nice Rewards
            #W2
            case 'Ink Blot':
                return min(101, session_data.account.achievements[achievementName]['Raw']), 101, 'silver-pen'
            case 'Vial Junkee':
                return sum(1 for vial in session_data.account.alchemy_vials.values() if vial['Level'] >= 9), 10, 'vial-9'
            case 'Fruit Salad':
                return notateNumber('Match', min(1000000, session_data.account.all_assets.get('Bug4').amount), 0, 'K'), '1000K', 'fruitfly'
            #W3
            case 'Checkout Takeout':
                return min(1000, session_data.account.achievements[achievementName]['Raw']), 1000, 'talent-book-library'
            #W4
            case 'Cabbage Patch':
                if session_data.account.meals['Cabbage']['Level'] > 0:
                    return min(5, session_data.account.cooking['Tables Owned']), 5, 'cooking-table'
                else:
                    return 0, 5, 'cabbage'
            case 'Le Pretzel Bleu':
                if session_data.account.meals['Pretzel']['Level'] > 0:
                    return min(8,session_data.account.cooking['Tables Owned']), 8, 'cooking-table'
                else:
                    return 0, 8, 'pretzel'
            case 'Gilded Shells':
                return min(12, session_data.account.breeding['Egg Slots']), 12, 'egg-nest'
            #W5
            case 'Artifact Finder':
                return min(15, sum(1 for artifact in session_data.account.sailing['Artifacts'].values() if artifact['Level'] > 0)), 15, ''
            case 'Gilded Vessel':
                return min(100, max([boat['TotalUpgrades'] for boat in session_data.account.sailing['Boats'].values()], default=0)), 100, 'sailing-ship-tier-4'
            case 'True Naval Captain':
                return min(20, session_data.account.sailing['BoatsOwned']), 20, ''
            case 'Grand Captain':
                return min(10, max([captain['Level'] for captain in session_data.account.sailing['Captains'].values()], default=0)), 10, 'captain-0-idle'
            case 'Voraci Vantasia':
                return min(500, session_data.account.achievements[achievementName]['Raw']), 500, 'voraci'
            case 'Vitamin D-licious':
                return notateNumber('Match', min(5000000, session_data.account.all_assets.get('LavaB3').amount), 0, 'K'), '5000K', 'orange-slice'
            case 'Maroon Warship':
                return min(300, max([boat['TotalUpgrades'] for boat in session_data.account.sailing['Boats'].values()], default=0)), 300, 'sailing-ship-tier-6'
            #W6
            case 'Big Time Land Owner':
                return min(27, session_data.account.farming['Total Plots']), 27, ''
            case 'Best Bloomie':
                return min(12, session_data.account.summoning['SanctuaryTotal']), 12, ''
            case 'Regalis My Beloved':
                return min(360, session_data.account.summoning['SanctuaryTotal']), 360, ''
            case "Scorin' the Ladies":
                return notateNumber('Match', min(250000, session_data.account.all_assets.get('Bug12').amount), 0, 'K'), '250K', 'ladybug'
            case 'Effervess Enthusiess':
                return notateNumber('Match', min(5000000, session_data.account.all_assets.get('Tree13').amount), 0, 'K'), '5000K', 'effervescent-logs'
            case 'Summoning GM':
                return min(58, session_data.account.summoning['Battles']['NormalTotal']), 58, ''
            case _:
                #logger.debug(f"{achievementName} didn't match a special case")
                return session_data.account.achievements[achievementName]['Raw'], 'IDK', ''
    except Exception as reason:
        logger.exception(f"Defaulting {achievementName} because {reason}")
        return 0, 1, ''

def getProgressionTiersAdviceGroup():
    infoTiers = 0
    max_tier = max(achievements_progressionTiers.keys(), default=0) - infoTiers
    achievements_AdviceDict = {category: {} for category in achievement_categories}
    tiers = {category: 0 for category in achievement_categories}
    exclusionsSet = getAchievementExclusions()

    #Assess Tiers
    for tierNumber, tierRequirements in achievements_progressionTiers.items():
        subgroupName = f"To reach Tier {tierNumber}"
        for categoryName, categoryAchievementsDict in tierRequirements.items():
            for achievementName, achievementDetailsDict in categoryAchievementsDict.items():
                if not session_data.account.achievements.get(achievementName)['Complete'] and achievementName not in exclusionsSet:
                    if subgroupName not in achievements_AdviceDict[categoryName]:
                        achievements_AdviceDict[categoryName][subgroupName] = []
                    prog, goal, resource = getAchievementStatus(achievementName)
                    achievements_AdviceDict[categoryName][subgroupName].append(Advice(
                        label=f"W{achievementDetailsDict['World']} {achievementName}: {achievementDetailsDict['Reward']}",
                        picture_class=achievementName,
                        progression=prog,
                        goal=goal,
                        resource=resource,
                        completed=False
                    ))
            if subgroupName not in achievements_AdviceDict[categoryName] and tiers[categoryName] == tierNumber - 1:
                tiers[categoryName] = tierNumber

    # Generate Advice Groups
    achievements_AdviceGroupDict = {}
    for category in achievement_categories:
        achievements_AdviceGroupDict[category] = AdviceGroup(
            tier=tiers[category],
            pre_string=f"Complete achievements for {category}",
            advices=achievements_AdviceDict[category]
        )
    overall_SectionTier = min(max_tier + infoTiers, min(tiers.values()))
    return achievements_AdviceGroupDict, overall_SectionTier, max_tier

def getAchievementsAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    achievements_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    achievements_AdviceSection = AdviceSection(
        name="Achievements",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Achievements tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Grasslands_Gary.gif",
        groups=achievements_AdviceGroupDict.values(),
    )
    return achievements_AdviceSection
