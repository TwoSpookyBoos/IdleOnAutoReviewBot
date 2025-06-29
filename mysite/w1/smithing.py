import math

from consts.consts_w1 import stamp_maxes
from models.models import Advice, AdviceGroup, AdviceSection
from consts.consts_autoreview import break_you_best, ValueToMulti, build_subgroup_label
from consts.consts_w2 import arcade_max_level
from consts.progression_tiers import smithing_progressionTiers, true_max_tiers
from flask import g as session_data
from utils.data_formatting import mark_advice_completed, safer_convert
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

def getForgeCapacityAdviceGroup() -> list[AdviceGroup]:
    cap_Advices = {
        'Static Sources': [],
        'Scaling Sources': []
    }
    bar_Advices = {
        'Total Capacity': [],
        'Bars per Forge Slot': []
    }
    #Static Sources
    achievement = session_data.account.achievements['Vitamin D-licious']['Complete']
    cap_Advices['Static Sources'].append(Advice(
        label=f"W5 Achievement: Vitamin D-licious: +{50 if achievement else 0}/50%",
        picture_class='vitamin-d-licious',
        progression=int(achievement),
        goal=1
    ))

    #Bribe value of 1 means purchased
    bribe = session_data.account.bribes['W6']['Forge Cap Smuggling'] == 1
    bribe_value = 30 * bribe
    bribe_multi = ValueToMulti(bribe_value)
    cap_Advices['Static Sources'].append(Advice(
        label=f"{{{{ Bribe|#bribes }}}}: Forge Cap Smuggling: {bribe_multi}/1.3x",
        picture_class='forge-cap-smuggling',
        progression=int(bribe),
        goal=1
    ))

    #Verify Skill Mastery itself is unlocked from The Rift
    cap_Advices['Static Sources'].append(Advice(
        label="{{ Rift|#rift }} 16: Skill Mastery unlocked",
        picture_class='skill-mastery',
        progression=int(session_data.account.rift['SkillMastery']),
        goal=1
    ))
    #Account-wide total smithing levels of 300 needed to unlock the bonus
    total_smithing_levels = sum(session_data.account.all_skills['Smithing'])
    skill_mastery_bonus_bool = session_data.account.rift['SkillMastery'] and total_smithing_levels >= 300
    cap_Advices['Static Sources'].append(Advice(
        label=f"Skill Mastery at 300 Smithing: +{25 * skill_mastery_bonus_bool * session_data.account.rift['SkillMastery']}/25%",
        picture_class='smithing',
        progression=total_smithing_levels,
        goal=300
    ))

    #Scaling Sources
    #Forge Upgrade purchased at the forge itself with coins
    forge_upgrades = (2 + 0.5 * (session_data.account.forge_upgrades[1]['Purchased'] - 1)) * session_data.account.forge_upgrades[1]['Purchased'] * 10
    cap_Advices['Scaling Sources'].append(Advice(
        label=f"Forge Upgrade: {session_data.account.forge_upgrades[1]['UpgradeName']}: +{int(forge_upgrades)}/13250",
        picture_class='forge-upgrades',
        progression=session_data.account.forge_upgrades[1]['Purchased'],
        goal=session_data.account.forge_upgrades[1]['MaxPurchases']
    ))

    #Godshard Ore card
    cap_Advices['Scaling Sources'].append(next(c for c in session_data.account.cards if c.name == 'Godshard Ore').getAdvice())
    cap_Advices['Scaling Sources'].append(Advice(
        label=f"{{{{ Forge Stamp|#stamps }}}}: +{session_data.account.stamps['Forge Stamp']['Total Value']:.2f}/57.50%"
              f"<br>Note: Exalting the stamp will take it over the goal listed above",
        picture_class='forge-stamp',
        progression=session_data.account.stamps['Forge Stamp']['Level'],
        goal=stamp_maxes['Forge Stamp']
    ))

    #Arcade Bonus 26 gives Forge Ore Capacity
    cap_Advices['Scaling Sources'].append(Advice(
        label=f"{{{{Arcade|#arcade}}}} Bonus: "
              f"{round(session_data.account.arcade[26]['Value'], 2):g}/"
              f"{session_data.account.arcade[26]['MaxValue']:.0f}%",
        picture_class=session_data.account.arcade[26]['Image'],
        progression=session_data.account.arcade[26]['Level'],
        goal=arcade_max_level+1,
        resource=session_data.account.arcade[26]['Material']
    ))

    #Cosmos > IdleOn Majik #2 Beeg Beeg Forge
    majik_beeg_forge = session_data.account.caverns['Majiks']['Beeg Beeg Forge']
    cap_Advices['Scaling Sources'].append(Advice(
        label=f"Beeg Beeg Forge {{{{ Cavern Majik|#villagers }}}}: {majik_beeg_forge['Description']}",
        picture_class=f"{majik_beeg_forge['MajikType']}-majik-{'un' if majik_beeg_forge['Level'] == 0 else ''}purchased",
        progression=majik_beeg_forge['Level'],
        goal=majik_beeg_forge['MaxLevel']
    ))

    # Upgrade Vault > Beeg Forge
    beeg_forge = session_data.account.vault['Upgrades']['Beeg Forge']
    cap_Advices['Scaling Sources'].append(Advice(
        label=f"{{{{ Vault|#upgrade-vault }}}}: Beeg Forge: {beeg_forge['Description'].split('<')[0]}"
              f"<br>(Additive with Bribe)",
        picture_class=beeg_forge['Image'],
        progression=beeg_forge['Level'],
        goal=beeg_forge['Max Level']
    ))

    for group_name in cap_Advices:
        for advice in cap_Advices[group_name]:
            mark_advice_completed(advice)

    groupA = ValueToMulti((session_data.account.arcade[26]['Value'] + (30 * (next(c.getStars() for c in session_data.account.cards if c.name == 'Godshard Ore')+1))))
    groupB = ValueToMulti(session_data.account.stamps['Forge Stamp']['Total Value'])
    groupC = ValueToMulti(bribe_value + beeg_forge['Total Value'])
    groupD = ValueToMulti((50 * achievement) + (25 * skill_mastery_bonus_bool))
    groupE = majik_beeg_forge['Value']

    final_forgeCapacity = math.ceil(min(2e9, (20 + forge_upgrades) * groupA * groupB * groupC * groupD * groupE))
    bar_Advices['Total Capacity'].append(Advice(
        label=f"Total Capacity: {final_forgeCapacity:,}",
        picture_class='empty-forge-slot'
    ))
    barDict = {
        'Godshard Bar': 15000,
        'Marble Bar': 4000,
        'Dreadlo Bar': 1000,
        'Starfire Bar': 500,
        'Lustre Bar': 250,
        'Void Bar': 100,
        'Dementia Bar': 40,
        'Platinum Bar': 16,
        'Gold Bar': 7,
        'Iron Bar': 4,
        'Copper Bar': 2
    }
    for barName, oreCost in barDict.items():
        nextBar = oreCost - (final_forgeCapacity % oreCost) if final_forgeCapacity % oreCost > 0 else oreCost
        bar_Advices['Bars per Forge Slot'].append(Advice(
            label=f"{math.floor(final_forgeCapacity / oreCost):,} {barName}s."
                  f"<br>{nextBar:,} cap to next bar",
            picture_class=barName,
            progression=oreCost-nextBar,
            goal=oreCost
        ))

    sources_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Forge Ore Capacity',
        advices=cap_Advices,
        informational=True,
    )
    sources_ag.check_for_completeness()
    total_ag = AdviceGroup(
            tier='',
            pre_string='Total Capacity and Bar thresholds',
            advices=bar_Advices,
            post_string='Note: Bar calculation does not include Multi-Bar chance. Also, partial stacks round up to whole bars when claiming AFK',
            informational=True,
            completed=sources_ag.completed
        )
    cap_AdviceGroups = [sources_ag, total_ag]
    return cap_AdviceGroups

def getProgressionTiersAdviceGroup():
    smithing_Advices = {
        'Cash Points': {},
        'Monster Points': {},
        'Forge Upgrades': {},
        'Empty Forge Slots': []
    }
    optional_tiers = 0
    true_max = true_max_tiers['Smithing']
    max_tier = true_max - optional_tiers
    tier_CashPoints = 0
    tier_MonsterPoints = 0
    tier_ForgeTotals = 0

    player_cash_points = []
    player_monster_points = []
    sum_CashPoints = 0
    sum_MonsterPoints = 0
    sum_ForgeUpgrades = sum(safer_convert(upgradeData['Purchased'], 0) for upgradeData in session_data.account.forge_upgrades.values())

    # Total up all the purchases across all current characters
    # TODO: Move this parsing to Account
    for character in session_data.account.all_characters:
        try:
            player_cash_points.append(safer_convert(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][1], 0))
            sum_CashPoints += safer_convert(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][1], 0)

            player_monster_points.append(safer_convert(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][2], 0))
            sum_MonsterPoints += safer_convert(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][2], 0)
        except:
            player_cash_points.append(0)
            player_monster_points.append(0)
            logger.exception(f"Unable to retrieve AnvilPAstats_{character.character_index}")

    #Assess Tiers
    for tier_number, requirements in smithing_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        #Cash Points
        for character_index, upgrade_count in enumerate(player_cash_points):
            if upgrade_count < requirements.get('Cash Points', 0):
                if (
                    subgroup_label not in smithing_Advices['Cash Points']
                    and len(smithing_Advices['Cash Points']) < session_data.account.max_subgroups
                ):
                    smithing_Advices['Cash Points'][subgroup_label] = []
                if subgroup_label in smithing_Advices['Cash Points']:
                    smithing_Advices['Cash Points'][subgroup_label].append(Advice(
                        label=session_data.account.all_characters[character_index].character_name,
                        picture_class=session_data.account.all_characters[character_index].class_name_icon,
                        progression=upgrade_count,
                        goal=requirements.get('Cash Points', 0)
                    ))
        if subgroup_label not in smithing_Advices['Cash Points'] and tier_CashPoints == tier_number - 1:
            tier_CashPoints = tier_number

        #Monster Points
        for character_index, upgrade_count in enumerate(player_monster_points):
            if upgrade_count < requirements.get('Monster Points', 0):
                if (
                    subgroup_label not in smithing_Advices['Monster Points']
                    and len(smithing_Advices['Monster Points']) < session_data.account.max_subgroups
                ):
                    smithing_Advices['Monster Points'][subgroup_label] = []
                if subgroup_label in smithing_Advices['Monster Points']:
                    smithing_Advices['Monster Points'][subgroup_label].append(Advice(
                        label=session_data.account.all_characters[character_index].character_name,
                        picture_class=session_data.account.all_characters[character_index].class_name_icon,
                        progression=upgrade_count,
                        goal=requirements.get('Monster Points', 0),
                        resource=requirements.get('Resource', 0)
                    ))
        if subgroup_label not in smithing_Advices['Monster Points'] and tier_MonsterPoints == tier_number - 1:
            tier_MonsterPoints = tier_number

        #Forge Upgrades
        if sum_ForgeUpgrades < requirements.get('Forge Total', 0):
            if (
                subgroup_label not in smithing_Advices['Forge Upgrades']
                and len(smithing_Advices['Forge Upgrades']) < session_data.account.max_subgroups
            ):
                smithing_Advices['Forge Upgrades'][subgroup_label] = []
            if subgroup_label in smithing_Advices['Forge Upgrades']:
                smithing_Advices['Forge Upgrades'][subgroup_label].append(Advice(
                    label=f"Purchase {requirements.get('Forge Total', 0)} total Forge upgrades"
                          f"<br>All unmaxed upgrades shown below",
                    picture_class='forge-upgrades',
                    progression=sum_ForgeUpgrades,
                    goal=requirements.get('Forge Total', 0)
                ))
                if 'All Unmaxed Forge Upgrades' not in smithing_Advices['Forge Upgrades']:
                    smithing_Advices['Forge Upgrades']['All Unmaxed Forge Upgrades'] = []
                    for upgradeIndex, upgradeData in session_data.account.forge_upgrades.items():
                        if upgradeData['Purchased'] < upgradeData['MaxPurchases']:
                            if not upgradeData['UpgradeName'].startswith('Forge EXP Gain'):
                                smithing_Advices['Forge Upgrades'][subgroup_label].append(Advice(
                                    label=upgradeData['UpgradeName'],
                                    picture_class='forge-upgrades',
                                    progression=upgradeData['Purchased'],
                                    goal=upgradeData['MaxPurchases']
                                ))
        if subgroup_label not in smithing_Advices['Forge Upgrades'] and tier_ForgeTotals == tier_number - 1:
            tier_ForgeTotals = tier_number
    
    # Generate AdviceGroups
    smithing_AdviceGroupDict = {}
    smithing_AdviceGroupDict['Cash Points'] = AdviceGroup(
        tier=tier_CashPoints,
        pre_string=f"Purchase Anvil Points with Cash on the following character{pl(smithing_Advices['Cash Points'])}",
        advices=smithing_Advices['Cash Points'],
    )
    smithing_AdviceGroupDict['Monster Points'] = AdviceGroup(
        tier=tier_MonsterPoints,
        pre_string=f"Purchase Anvil Points with Monster Materials on the following character{pl(smithing_Advices['Monster Points'])}",
        advices=smithing_Advices['Monster Points'],
        post_string='The final Monster Material for each tier is shown above',
    )
    smithing_AdviceGroupDict['Forge Upgrades'] = AdviceGroup(
        tier=tier_CashPoints,
        pre_string='Purchase additional Forge Upgrades',
        advices=smithing_Advices['Forge Upgrades'],
        post_string='As of v2.36, Forge EXP Gain does absolutely nothing. Feel free to skip it!'
    )
    
    overall_SectionTier = min(true_max, tier_CashPoints, tier_MonsterPoints, tier_ForgeTotals)
    return smithing_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getSmithingAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    smithing_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    smithing_AdviceGroupDict['OreCapacity'], smithing_AdviceGroupDict['Bars'] = getForgeCapacityAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    smithing_AdviceSection = AdviceSection(
        name='Smithing',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Smithing tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Smithing_Infinity_Hammer.gif',
        groups=smithing_AdviceGroupDict.values()
    )

    return smithing_AdviceSection
