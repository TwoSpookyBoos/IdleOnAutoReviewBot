
from consts.consts_autoreview import break_you_best
from consts.progression_tiers import equinox_progressionTiers, true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.logging import get_logger

logger = get_logger(__name__)

def getEquinoxProgressionTiersAdviceGroup():
    equinox = session_data.account.equinox
    equinox_Advices = {
        'Dreams': {
            'Complete Dreams': [],
            'Unlock Equinox Bonuses': [],
        },
        'TotalUpgrades': {},
    }

    optional_tiers = 1
    true_max = true_max_tiers['Equinox']
    max_tier = true_max - optional_tiers  # 1 final info tier for completing all dreams

    recommended_upgrades = [equinox.upgrades[name] for name in equinox_progressionTiers['Recommended']]
    optional_upgrades = [equinox.upgrades[name] for name in equinox_progressionTiers['Optional']]
    playerRecommendedBonusTotal = sum(upgrade.level for upgrade in recommended_upgrades)
    playerOptionalBonusTotal = sum(upgrade.level for upgrade in optional_upgrades)
    recommendedBonusTotal = sum(upgrade.final_max_level for upgrade in recommended_upgrades)
    optionalBonusTotal = sum(upgrade.final_max_level for upgrade in optional_upgrades)

    # Dreams Completed
    if equinox.dreams.total_completed >= equinox.dreams.total_possible:  # If the player has completed ALL possible dreams, set to max tier
        tier_TotalDreamsCompleted = max_tier + optional_tiers
    else:
        # Otherwise set to max - 1 (for completing all dreams) - however many upgrades are remaining to be unlocked
        tier_TotalDreamsCompleted = max_tier - len(equinox.dreams.remaining_unlock_dreams)
        for dream in equinox.dreams.remaining_unlock_dreams:
            equinox_Advices["Dreams"]["Complete Dreams"].append(dream.get_advice())
        for upgrade in equinox.upgrades.values():
            if not upgrade.unlocked:
                category = 'Recommended' if upgrade.name in equinox_progressionTiers['Recommended'] else 'Optional'
                equinox_Advices["Dreams"]["Unlock Equinox Bonuses"].append(upgrade.get_unlock_advice(f" ({category})"))

        equinox_Advices["Dreams"]["Complete Dreams"].append(equinox.dreams.get_advice())

    # Recommended Upgrades
    recommendedSubgroupName = f"Recommended Upgrades: {playerRecommendedBonusTotal}/{recommendedBonusTotal}"
    if playerRecommendedBonusTotal < recommendedBonusTotal:
        equinox_Advices["TotalUpgrades"][recommendedSubgroupName] = [
            upgrade.get_advice() for upgrade in recommended_upgrades
            if upgrade.level < upgrade.final_max_level and upgrade.unlocked
        ]
        if len(equinox_Advices["TotalUpgrades"][recommendedSubgroupName]) == 0:
            equinox_Advices["TotalUpgrades"][recommendedSubgroupName].append(Advice(
                label="Nothing good available :( Maybe wait for future unlocks!",
                picture_class="",
            ))

    # Optional Upgrades
    if playerOptionalBonusTotal < optionalBonusTotal:
        optionalSubgroupName = f"Optional Upgrades: {playerOptionalBonusTotal}/{optionalBonusTotal}"
        equinox_Advices["TotalUpgrades"][optionalSubgroupName] = [
            upgrade.get_advice() for upgrade in optional_upgrades
            if upgrade.level < upgrade.final_max_level and upgrade.unlocked
        ]
        if len(equinox_Advices["TotalUpgrades"][optionalSubgroupName]) == 0:
            equinox_Advices["TotalUpgrades"][optionalSubgroupName].append(Advice(
                label="No unlocked, unmaxed Optional upgrades to list",
                picture_class="",
            ))

    # Generate AdviceGroups
    equinox_AdviceGroupDict = {}
    equinox_AdviceGroupDict["Complete Dreams"] = AdviceGroup(
        tier=f"{tier_TotalDreamsCompleted if tier_TotalDreamsCompleted < max_tier else ''}",
        pre_string=f"{'Informational- Complete all Equinox Dreams' if tier_TotalDreamsCompleted >= max_tier else 'Unlock more Equinox Bonuses'}",
        advices=equinox_Advices["Dreams"],
        post_string=f"{'New Bonuses unlock in a set order. They are not tied to certain Dreams.' if tier_TotalDreamsCompleted < max_tier else ''}",
        informational=True if tier_TotalDreamsCompleted >= max_tier else False
    )
    equinox_AdviceGroupDict["Complete Dreams"].remove_empty_subgroups()

    bonus_max_levels = session_data.account.summoning.bonuses["Equinox Max LV"].value
    equinox_AdviceGroupDict["BonusUpgrades"] = AdviceGroup(
        tier="",
        pre_string="Upgrade more Equinox Bonuses",
        post_string=f"+{bonus_max_levels} max levels from Endless Summoning already included" if bonus_max_levels > 0 else '',
        advices=equinox_Advices['TotalUpgrades'],
        informational=True,
        completed=recommendedSubgroupName not in equinox_Advices["TotalUpgrades"]
    )
    overall_SectionTier = min(max_tier + optional_tiers, tier_TotalDreamsCompleted)
    return equinox_AdviceGroupDict, overall_SectionTier, max_tier, max_tier + optional_tiers

def getEquinoxAdviceSection() -> AdviceSection:
    if not session_data.account.equinox.unlocked:
        equinox_AdviceSection = AdviceSection(
            name="Equinox",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Equinox in World 3!",
            picture="Equinox_Valley_Mirror.gif",
            unreached=True
        )
        return equinox_AdviceSection

    #Generate AdviceGroups
    equinox_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getEquinoxProgressionTiersAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    equinox_AdviceSection = AdviceSection(
        name="Equinox",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Equinox tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Equinox_Valley_Mirror.gif",
        groups=equinox_AdviceGroupDict.values()
    )
    return equinox_AdviceSection
