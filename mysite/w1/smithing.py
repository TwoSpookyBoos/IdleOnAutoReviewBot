
from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.progression_tiers import smithing_progressionTiers, true_max_tiers


from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
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
    forge_upgrades = session_data.account.forge_upgrades
    #Static Sources
    cap_Advices['Static Sources'].append(forge_upgrades.get_vitamin_d_advice())
    cap_Advices['Static Sources'].append(session_data.account.bribes['Forge Cap Smuggling'].get_bonus_advice())

    #Verify Skill Mastery itself is unlocked from The Rift
    cap_Advices['Static Sources'].append(session_data.account.rift['SkillMastery'].get_bonus_advice())
    cap_Advices['Static Sources'].append(forge_upgrades.get_skill_mastery_advice())

    #Scaling Sources
    #Forge Upgrade purchased at the forge itself with coins
    cap_Advices['Scaling Sources'].append(forge_upgrades.get_ore_capacity_advice())

    #Godshard Ore card
    cap_Advices['Scaling Sources'].append(next(c for c in session_data.account.cards if c.name == 'Godshard Ore').getAdvice())
    cap_Advices['Scaling Sources'].append(session_data.account.stamps['Forge Stamp'].get_advice())

    #Arcade Bonus 26 gives Forge Ore Capacity
    cap_Advices['Scaling Sources'].append(session_data.account.arcade[26].get_advice())

    #Cosmos > IdleOn Majik #2 Beeg Beeg Forge
    majik_beeg_forge = session_data.account.caverns.villagers["Cosmos"].majiks.idleon['Beeg Beeg Forge']
    cap_Advices['Scaling Sources'].append(majik_beeg_forge.get_advice())

    # Upgrade Vault > Beeg Forge
    cap_Advices['Scaling Sources'].append(session_data.account.vault.get_upgrade_advice("Beeg Forge"))

    for group_name in cap_Advices:
        for advice in cap_Advices[group_name]:
            advice.mark_advice_completed()

    bar_Advices['Total Capacity'].append(forge_upgrades.get_total_capacity_advice())
    bar_Advices['Bars per Forge Slot'].extend(forge_upgrades.get_bar_advice())

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

    player_cash_points = [c.anvil_cash_points for c in session_data.account.characters]
    player_monster_points = [c.anvil_monster_points for c in session_data.account.characters]
    sum_ForgeUpgrades = session_data.account.forge_upgrades.total_purchased

    #Assess Tiers
    for tier_number, requirements in smithing_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        #Cash Points
        for character_index, upgrade_count in enumerate(player_cash_points):
            if upgrade_count < requirements.get('Cash Points', 0):
                add_subgroup_if_available_slot(smithing_Advices['Cash Points'], subgroup_label)
                if subgroup_label in smithing_Advices['Cash Points']:
                    smithing_Advices['Cash Points'][subgroup_label].append(Advice(
                        label=session_data.account.characters[character_index].character_name,
                        picture_class=session_data.account.characters[character_index].class_name_icon,
                        progression=upgrade_count,
                        goal=requirements.get('Cash Points', 0)
                    ))
        if subgroup_label not in smithing_Advices['Cash Points'] and tier_CashPoints == tier_number - 1:
            tier_CashPoints = tier_number

        #Monster Points
        for character_index, upgrade_count in enumerate(player_monster_points):
            if upgrade_count < requirements.get('Monster Points', 0):
                add_subgroup_if_available_slot(smithing_Advices['Monster Points'], subgroup_label)
                if subgroup_label in smithing_Advices['Monster Points']:
                    smithing_Advices['Monster Points'][subgroup_label].append(Advice(
                        label=session_data.account.characters[character_index].character_name,
                        picture_class=session_data.account.characters[character_index].class_name_icon,
                        progression=upgrade_count,
                        goal=requirements.get('Monster Points', 0),
                        resource=requirements.get('Resource', 0)
                    ))
        if subgroup_label not in smithing_Advices['Monster Points'] and tier_MonsterPoints == tier_number - 1:
            tier_MonsterPoints = tier_number

        #Forge Upgrades
        if sum_ForgeUpgrades < requirements.get('Forge Total', 0):
            add_subgroup_if_available_slot(smithing_Advices['Forge Upgrades'], subgroup_label)
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
                    for upgrade in session_data.account.forge_upgrades.values():
                        if not upgrade.maxed and not upgrade.name.startswith('Forge EXP Gain'):
                            smithing_Advices['Forge Upgrades'][subgroup_label].append(upgrade.get_advice())
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
