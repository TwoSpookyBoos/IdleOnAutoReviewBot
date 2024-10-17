from consts import sneakingGemstonesMaxValueDict, break_you_best
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def setSneakingProgressionTier():
    sneaking_AdviceDict = {
        "Gemstones": [],
        "JadeEmporium": [],
        "PristineCharms": []
    }
    sneaking_AdviceGroupDict = {}
    sneaking_AdviceSection = AdviceSection(
        name="Sneaking",
        tier="0",
        pinchy_rating=0,
        header="Best Sneaking tier met: Not Yet Evaluated",
        picture="Dojo_Ghost.gif"
    )
    highestSneakingSkillLevel = max(session_data.account.all_skills.get("Sneaking", [0]))
    if highestSneakingSkillLevel < 1:
        sneaking_AdviceSection.header = "Come back after unlocking the Sneaking skill in W6!"
        sneaking_AdviceSection.unreached = True
        return sneaking_AdviceSection

    tier_Sneaking = 0
    max_tier = 0

    #Assess Gemstones
    for gemstoneName, gemstoneData in session_data.account.sneaking["Gemstones"].items():
        if session_data.account.sneaking["Gemstones"]['Moissanite']['BaseValue'] > 0 and gemstoneName != 'Moissanite':
            boosted_value = f" (+{gemstoneData['BoostedValue']:.2f}% total)"
        else:
            boosted_value = ''
        sneaking_AdviceDict["Gemstones"].append(Advice(
            # label="{} (Level {}: +{:.2f}% {})".format(
            #     gemstoneName,
            #     gemstoneData.get('Level', 0),
            #     gemstoneData.get('Value', 0),
            #     gemstoneData.get('Stat', '')),
            label=f"Level {gemstoneData['Level']} {gemstoneName}:"
                  f" +{gemstoneData['BaseValue']:.2f}/{sneakingGemstonesMaxValueDict.get(gemstoneName, 0)}% {gemstoneData['Stat']}"
                  f"{boosted_value}",
            picture_class=gemstoneName,
            progression=f"{gemstoneData.get('Percent', 0):.2f}",
            goal=100,  # if session_data.account.sneaking["Gemstones"]['Moissanite']['Level'] == 0 or gemstoneName == 'Moissanite' else 400,
            unit="%"
        ))

    # Assess Jade Emporium
    for purchaseName, purchaseDict in session_data.account.sneaking["JadeEmporium"].items():
        if not purchaseDict['Obtained']:
            sneaking_AdviceDict['JadeEmporium'].append(Advice(
                label=purchaseName,
                picture_class=purchaseName
            ))

    # Assess Pristine Charms
    for pristineCharmName, pristineCharmDict in session_data.account.sneaking["PristineCharms"].items():
        if not pristineCharmDict['Obtained']:
            sneaking_AdviceDict['PristineCharms'].append(Advice(
                label=f"{pristineCharmName}: {pristineCharmDict['Bonus']}",
                picture_class=f"{pristineCharmDict['Image']}"
            ))

    # Generate AdviceGroups
    sneaking_AdviceGroupDict["Gemstones"] = AdviceGroup(
        tier="",
        pre_string="Percentage of Gemstone values",
        #post_string="Formulas thanks to merlinthewizard1313",
        advices=sneaking_AdviceDict["Gemstones"]
    )
    sneaking_AdviceGroupDict["JadeEmporium"] = AdviceGroup(
        tier="",
        pre_string="Purchase all upgrades from the Jade Emporium",
        advices=sneaking_AdviceDict["JadeEmporium"]
    )
    sneaking_AdviceGroupDict["PristineCharms"] = AdviceGroup(
        tier="",
        pre_string="Collect all Pristine Charms",
        advices=sneaking_AdviceDict["PristineCharms"]
    )

    # Generate AdviceSection
    overall_SneakingTier = min(max_tier, tier_Sneaking)
    tier_section = f"{overall_SneakingTier}/{max_tier}"
    sneaking_AdviceSection.tier = tier_section
    sneaking_AdviceSection.pinchy_rating = overall_SneakingTier
    sneaking_AdviceSection.groups = sneaking_AdviceGroupDict.values()
    if overall_SneakingTier >= max_tier:
        sneaking_AdviceSection.header = f"Best Sneaking tier met: {tier_section}{break_you_best}"
    else:
        sneaking_AdviceSection.header = f"Best Sneaking tier met: {tier_section}"

    return sneaking_AdviceSection
