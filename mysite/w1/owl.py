from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from consts.consts_autoreview import break_you_best, build_subgroup_label, EmojiType
from consts.progression_tiers import owl_progressionTiers, true_max_tiers
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger


logger = get_logger(__name__)

def getNoFeathersGeneratingAlert():
    if session_data.account.owl['FeatherGeneration'] < 1:
        alert_advice = Advice(
            label='Find the Owl in W1 and start generating Feathers!'
            if not session_data.account.owl['Discovered']
            else f"You aren't generating any {{{{ Owl|#owl }}}} Feathers!",
            picture_class='feather-generation'
        )
        session_data.account.alerts_Advices['World 1'].append(alert_advice)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    owl_AdviceDict = {
        "MegaFeathers": {}
    }
    infoTiers = 1
    true_max = true_max_tiers['Owl']
    max_tier = true_max - infoTiers
    tier_MegaFeathers = 0

    featherResetsDict = {
        0: 6, 1: 6, 2: 7, 3: 8, 4: 9,
        5: 11, 6: 12, 7: 11, 8: 12, 9: 14,
        10: 16, 11: 17, 12: 18, 13: 19, 14: 21,
        15: 22, 16: 23, 17: 24, 18: 25, 19: 27,
        20: 28, 21: 29, 22: 30, 23: 31, 24: 32
    }
    orionDRValues = {
        23: 40, 29: 67.5
    }

    #Assess Tiers
    lastMFShown = -1
    for tier_number, requirements in owl_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        if 'MegaFeathersOwned' in requirements:
            if session_data.account.owl['MegaFeathersOwned'] < requirements['MegaFeathersOwned'] + 1:
                for mf, resets in featherResetsDict.items():
                    if lastMFShown < mf <= requirements['MegaFeathersOwned']:
                        if session_data.account.owl['MegaFeathersOwned'] <= mf:
                            add_subgroup_if_available_slot(owl_AdviceDict['MegaFeathers'], subgroup_label)
                            if subgroup_label in owl_AdviceDict['MegaFeathers']:
                                lastMFShown = mf
                                owl_AdviceDict['MegaFeathers'][subgroup_label].append(Advice(
                                    label=f"MF{mf+1}: Restart {resets} times first",
                                    picture_class=f"megafeather-{mf}" if mf < 10 else "the-great-mega-reset",
                                    progression=session_data.account.owl['FeatherRestarts'] if session_data.account.owl['MegaFeathersOwned'] == mf else 0,
                                    goal=resets
                                ))
        if 'BonusesOfOrion' in requirements:
            if session_data.account.owl['BonusesOfOrion'] < requirements['BonusesOfOrion']:
                add_subgroup_if_available_slot(owl_AdviceDict['MegaFeathers'], subgroup_label)
                if subgroup_label in owl_AdviceDict['MegaFeathers']:
                    orion_advice = Advice(
                            label=f"Before MF{requirements['MegaFeathersOwned']+1}, purchase Bonuses of Orion {requirements['BonusesOfOrion']}",
                            picture_class='bonuses-of-orion',
                            progression=session_data.account.owl['BonusesOfOrion'],
                            goal=requirements['BonusesOfOrion']
                        )
                    if len(owl_AdviceDict['MegaFeathers']) > 0:
                        owl_AdviceDict['MegaFeathers'][subgroup_label].insert(-1, orion_advice)
                    else:
                        owl_AdviceDict['MegaFeathers'][subgroup_label].append(orion_advice)
                    owl_AdviceDict['MegaFeathers'][subgroup_label].append(Advice(
                        label=f"{orionDRValues.get(requirements['BonusesOfOrion'], 'IDK')}% Drop Rate will then be yours {EmojiType.TADA.value}",
                        picture_class='drop-rate'
                    ))

        if subgroup_label not in owl_AdviceDict['MegaFeathers'] and tier_MegaFeathers == tier_number - 1:
            tier_MegaFeathers = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_MegaFeathers,
        pre_string='Collect Mega Feathers and Bonuses of Orion',
        advices=owl_AdviceDict['MegaFeathers'],
    )
    overall_SectionTier = min(true_max, tier_MegaFeathers)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getOwlAdviceSection() -> AdviceSection:
    # Generate Alert Advice
    getNoFeathersGeneratingAlert()

    # Generate AdviceGroups
    owl_AdviceGroupDict = {}
    owl_AdviceGroupDict['MegaFeathers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()

    # Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    owl_AdviceSection = AdviceSection(
        name="Owl",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Owl tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Owl.gif',
        groups=owl_AdviceGroupDict.values()
    )
    return owl_AdviceSection
