from consts.progression_tiers import true_max_tiers

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data

from utils.number_formatting import round_and_trim
from utils.logging import get_logger

logger = get_logger(__name__)


def pristine_collector_advice(pristine_collector):
    # This is a multi, so display it as such
    advice = pristine_collector.get_advice()
    advice.label = advice.label.replace(
        f"+{pristine_collector.total_value:.2f}%",
        f"x{round_and_trim(1 + pristine_collector.total_value / 100, 4)}"
    ).replace(
        f"({pristine_collector.value_per_level:.2f} per level)",
        f"(+{round_and_trim(pristine_collector.value_per_level)}% per level)"
    )
    return advice


def getSneakingProgressionTiersAdviceGroups():
    sneaking = session_data.account.sneaking
    pristine_collector = session_data.account.compass.upgrades['Pristine Collector']
    sneaking_AdviceDict = {
        'Gemstones': [
            gemstone.get_bonus_advice() for gemstone in sneaking.gemstones.values()
        ],
        'JadeEmporium': [
            upgrade.get_obtained_advice(False) for upgrade in sneaking.emporium.values()
        ],
        "PristineCharms": [
            pristine.get_obtained_advice(False)
            for pristine in sneaking.pristine_charms.values()
        ],
        "PristineOdds": [
            Advice(
                label=f"Each regular Charm found today lowers this, from 0.15% down to 0% at 120 found "
                      f"(you're at {sneaking.daily_charms_found}/120, resets daily)",
                picture_class='sneaking-meteorite',
                progression=sum(charm.obtained for charm in sneaking.pristine_charms.values()),
                goal=len(sneaking.pristine_charms),
            ),
            pristine_collector_advice(pristine_collector),
        ],
    }
    sneaking_AdviceGroups = {}

    optional_tiers = 0
    true_max = true_max_tiers['Sneaking']
    max_tier = true_max - optional_tiers
    tier_Sneaking = 0

    # Assess Gemstones
    talent_level, talent_multi = sneaking.gemstone_multi_source
    sneaking_AdviceDict["Gemstones"].insert(0, Advice(
        label=f"Wind Walker Tab 5: Generational Gemstones: {round_and_trim(talent_multi, 4)}x"
              f"<br>Highest currently specced talent level shown to the right",
        picture_class='generational-gemstones',
        progression=talent_level,
        goal=max([char.max_talents_over_books for char in session_data.account.all_characters if 'Wind Walker' in char.all_classes], default=100)
    ))

    for category in sneaking_AdviceDict:
        for advice in sneaking_AdviceDict[category]:
            advice.mark_advice_completed()

    # Generate AdviceGroups
    sneaking_AdviceGroups['Gemstones'] = AdviceGroup(
        tier='',
        pre_string='Percentage of Gemstone values',
        # post_string="Formulas thanks to merlinthewizard1313",
        advices=sneaking_AdviceDict["Gemstones"],
        informational=True
    )
    sneaking_AdviceGroups['JadeEmporium'] = AdviceGroup(
        tier='',
        pre_string='Purchase all upgrades from the Jade Emporium',
        advices=sneaking_AdviceDict['JadeEmporium'],
        informational=True
    )
    sneaking_AdviceGroups['PristineCharms'] = AdviceGroup(
        tier='',
        pre_string='Pristine Charm Odds and Collection',
        post_string='Strategy: wear Meteorite charms on F12 at 0% detect chance. Mastery level does not matter.',
        advices={
            f"Pristine Charm Odds: {round_and_trim(sneaking.pristine_chance, 4)}%": sneaking_AdviceDict['PristineOdds'],
            'Collect all Pristine Charms': sneaking_AdviceDict['PristineCharms'],
        },
        informational=True
    )
    overall_SectionTier = min(true_max, tier_Sneaking)
    return sneaking_AdviceGroups, overall_SectionTier, max_tier, true_max

def getSneakingAdviceSection() -> AdviceSection:
    highest_sneaking_level = max(session_data.account.all_skills['Sneaking'])
    if highest_sneaking_level < 1:
        sneaking_AdviceSection = AdviceSection(
            name='Sneaking',
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking the Sneaking skill in W6!',
            picture='Dojo_Ghost.gif',
            unrated=True,  # TODO: Fix once real tiers added
            unreached=True
        )
        return sneaking_AdviceSection

    #Generate AdviceGroups
    sneaking_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getSneakingProgressionTiersAdviceGroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    sneaking_AdviceSection = AdviceSection(
        name='Sneaking',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Sneaking Information',  # f"Best Sneaking tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Dojo_Ghost.gif',
        unrated=True,  # TODO: Fix once real tiers added
        groups=sneaking_AdviceGroupDict.values(),
    )
    return sneaking_AdviceSection
