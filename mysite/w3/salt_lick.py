from consts.consts import break_you_best
from consts.progression_tiers import salt_lick_progression_tiers
from flask import g as session_data

from consts.progression_tiers_updater import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    saltlick_Advices = []
    optional_tiers = 0
    true_max = true_max_tiers['Salt Lick']
    max_tier = true_max - optional_tiers
    sum_maxed_upgrades = 0
    player_salt_lick = session_data.account.saltlick

    # Assess tiers
    for tier_number, requirements in salt_lick_progression_tiers.items():
        if player_salt_lick[requirements['Upgrade']] < requirements['Level']:
            saltlick_Advices.append(Advice(
                label=requirements['Upgrade'],
                picture_class=requirements['Material'],
                progression=player_salt_lick[requirements['Upgrade']],
                goal=requirements['Level']
            ))
        else:
            sum_maxed_upgrades += 1

    tier_RequiredSaltLickUpgrades = sum_maxed_upgrades

    # Generate AdviceGroups
    tiers_ag = AdviceGroup(
        tier=tier_RequiredSaltLickUpgrades,
        pre_string=f"{pl(saltlick_Advices, 'Final Upgrade', 'Remaining Upgrades')} to max",
        advices=saltlick_Advices,
        post_string='Shown upgrades are in recommended order.'
    )
    overall_SectionTier = min(true_max, tier_RequiredSaltLickUpgrades)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getSaltLickAdviceSection() -> AdviceSection:
    if session_data.account.construction_buildings['Salt Lick']['Level'] < 1:
        saltlick_AdviceSection = AdviceSection(
            name='Salt Lick',
            tier='Not Yet Evaluated',
            header='Come back after unlocking the Salt Lick within the Construction skill in World 3!',
            picture='Construction_Salt_Lick.gif',
            unreached=True
        )
        return saltlick_AdviceSection

    #Generate AdviceGroup
    saltlick_AdviceGroupDict = {}
    saltlick_AdviceGroupDict['UnmaxedUpgrades'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    saltlick_AdviceSection = AdviceSection(
        name='Salt Lick',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Salt Lick tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Construction_Salt_Lick.gif',
        groups=saltlick_AdviceGroupDict.values()
    )
    return saltlick_AdviceSection
