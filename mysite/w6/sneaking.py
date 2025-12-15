from consts.consts_idleon import lavaFunc
from consts.progression_tiers import true_max_tiers

from models.models import AdviceSection, AdviceGroup, Advice, session_data
from utils.logging import get_logger


logger = get_logger(__name__)

def getSneakingProgressionTiersAdviceGroups():
    sneaking_AdviceDict = {
        'Gemstones': [],
        'JadeEmporium': [],
        'PristineCharms': []
    }
    sneaking_AdviceGroups = {}

    optional_tiers = 0
    true_max = true_max_tiers['Sneaking']
    max_tier = true_max - optional_tiers
    tier_Sneaking = 0

    # Assess Gemstones
    talent_level_multi = lavaFunc('decayMulti', max(0, session_data.account.sneaking['Highest Current Generational Gemstones']), 3, 300)
    sneaking_AdviceDict["Gemstones"].append(Advice(
        label=f"Wind Walker Tab 5: Generational Gemstones: {talent_level_multi:.4f}x"
              f"<br>Highest currently specced talent level shown to the right",
        picture_class='generational-gemstones',
        progression=session_data.account.sneaking['Highest Current Generational Gemstones'],
        goal=max([char.max_talents_over_books for char in session_data.account.all_characters if 'Wind Walker' in char.all_classes], default=100)
    ))

    for gemstoneName, gemstoneData in session_data.account.sneaking['Gemstones'].items():
        emerald_note = (
            f" = {1 - (1/(max(1, session_data.account.sneaking['Gemstones']['Emerald']['BoostedValue'])/100)):.4%} cost reduction"
            if gemstoneName == 'Emerald' else ''
        )
        if session_data.account.sneaking['Gemstones']['Moissanite']['BaseValue'] > 0 and gemstoneName != 'Moissanite':
            boosted_value = (
                f" (+{gemstoneData['BoostedValue']:,.2f}"
                f"{'%' if gemstoneName != 'Firefrost' else ''} total"
                f"{emerald_note})"
            )
        else:
            boosted_value = ''
        sneaking_AdviceDict["Gemstones"].append(Advice(
            label=f"Level {gemstoneData['Level']:,} {gemstoneName}:"
                  f" +{gemstoneData['BaseValue']:,.2f}/{gemstoneData['MaxValue']:,}"
                  f"{'%' if gemstoneName != 'Firefrost' else ''} {gemstoneData['Stat']}"
                  f"{boosted_value}",
            picture_class=gemstoneName,
            progression=f"{gemstoneData.get('Percent', 0):.2f}",
            goal=100,  # if session_data.account.sneaking["Gemstones"]['Moissanite']['Level'] == 0 or gemstoneName == 'Moissanite' else 400,
            unit="%"
        ))

    # Assess Jade Emporium
    for purchaseName, purchaseDict in session_data.account.sneaking["JadeEmporium"].items():
        sneaking_AdviceDict['JadeEmporium'].append(Advice(
            label=purchaseName,
            picture_class=purchaseName,
            progression=int(purchaseDict['Obtained']),
            goal=1
        ))

    # Assess Pristine Charms
    for pristineCharmName, pristineCharmDict in session_data.account.sneaking["PristineCharms"].items():
        sneaking_AdviceDict['PristineCharms'].append(Advice(
            label=f"{pristineCharmName}: {pristineCharmDict['Bonus']}",
            picture_class=f"{pristineCharmDict['Image']}",
            progression=int(pristineCharmDict['Obtained']),
            goal=1
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
        pre_string='Collect all Pristine Charms',
        post_string='Strategy: wear Meteorite charms on F12 at 0% detect chance. Mastery level does not matter.',
        advices=sneaking_AdviceDict['PristineCharms'],
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
