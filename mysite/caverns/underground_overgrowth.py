from math import ceil, log10
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    break_you_best, infinity_string,
    caverns_jar_rupies,
    getMotherlodeEfficiencyRequired, monument_layer_rewards, getMonumentOpalChance, caverns_cavern_names,
    # shallow_caverns_progressionTiers
)
from utils.text_formatting import pl, notateNumber

logger = get_logger(__name__)

def getTemplateCavernAdviceGroup(schematics) -> AdviceGroup:
    cavern_name = 'The Template'
    cavern = session_data.account.caverns['Caverns'][cavern_name]

    c_stats = "Cavern Stats"
    c_faqs = "FAQs"
    cavern_advice = {
        c_stats: [],
        c_faqs: [],
    }

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- ",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getJarAdviceGroup(schematics) -> AdviceGroup:
    cavern_name = caverns_cavern_names[11]
    cavern = session_data.account.caverns['Caverns'][cavern_name]
    rupies_owned = cavern['RupiesOwned']
    collectibles = session_data.account.caverns['Collectibles']
    total_collectible_levels = sum([v['Level'] for v in collectibles.values()])
    jars = cavern['Jars']

    c_stats = 'Cavern Stats'
    rupies_stats = 'Rupies Stats'
    collectible_stats = f'Collectibles: {total_collectible_levels} total levels'
    jar_stats = 'Jar Stats'
    cavern_advice = {
        c_stats: [],
        rupies_stats: [],
        jar_stats: [],
        collectible_stats: [],
    }

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Create Jars passively, then break to collect Rupies, Opals, and Collectibles",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='jar-all-types',
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    # cavern_advice[c_stats].append(Advice(
    #     label=f"Chance for next Opal from Tall Jar: TBD",
    #     picture_class='jar-type-1',
    #     progression=f"TBD",
    #     goal=100,
    #     # unit='%'
    # ))

# Rupies Stats
    rupies_requirements = {
        0: ['Simple Jars, always', True, 'jar-type-0'],  #Red
        1: [f"Simple Jars {'while' if rupies_owned[0] >= 100 else 'once'} you have 100+ {caverns_jar_rupies[0]} Rupies", rupies_owned[0] >= 100, 'jar-type-0'],
        2: [f"Simple Jars {'while' if rupies_owned[1] >= 1e3 else 'once'} you have 1K+ {caverns_jar_rupies[1]} Rupies", rupies_owned[1] >= 1e3, 'jar-type-0'],
        3: ['Great Jars, always', True, 'jar-type-3'],  # Yellow
        4: [f"Great Jars {'while' if rupies_owned[3] >= 1e4 else 'once'} you have 10K+ {caverns_jar_rupies[3]} Rupies", rupies_owned[3] >= 1e4, 'jar-type-3'],
        5: [f"Great Jars {'while' if rupies_owned[4] >= 5e5 else 'once'} you have 500K+ {caverns_jar_rupies[4]} Rupies", rupies_owned[4] >= 5e5, 'jar-type-3'],
        6: ['Epic Jars, always', True, 'jar-type-6'],  # Orange
        7: [f"Epic Jars {'while' if rupies_owned[6] >= 6e6 else 'once'} you have 6M+ {caverns_jar_rupies[6]} Rupies", rupies_owned[6] >= 6e6, 'jar-type-6'],
        8: [f"Epic Jars {'while' if rupies_owned[7] >= 5e7 else 'once'} you have 50M+ {caverns_jar_rupies[7]} Rupies", rupies_owned[7] >= 5e7, 'jar-type-6'],
        9: ['Heirloom Jars, always', True, 'jar-type-9'],  # Master
        10: ['Artisan Jars, always', True, 'jar-type-5'],  # White
        11: ['Ceremony Jars, always', True, 'jar-type-8'],  # Dark

    }
    for rupie_index, rupie_quantity in enumerate(rupies_owned):
        requirement = rupies_requirements.get(rupie_index, ['IDK Sorry', 'IDK', ''])
        cavern_advice[rupies_stats].append(Advice(
            label=f"{caverns_jar_rupies[rupie_index]} Rupies: {notateNumber('Basic', rupie_quantity, 2)}"
                  f"<br>Collected from {requirement[0]}",
            picture_class=f'jar-rupie-{rupie_index}',
            progression=int(requirement[1]) if isinstance(requirement[1], bool) else requirement[1],
            goal=1,
            resource=requirement[2]
        ))

# Jar Stats
    jpl = schematics['Jar Production Line']
    cavern_advice[jar_stats].append(Advice(
        label=f"Schematic {jpl['UnlockOrder']}: Jar Production Line reduces the Create requirement for the next Jar in line"
              f" based on the pow10 stacks of Jars destroyed. Basic Speeds up Tall which speeds up Ornate, etc.",
        picture_class=jpl['Image'],
        progression=int(jpl['Purchased']),
        goal=1
    ))
    for jar_index, jar_details in jars.items():
        pow10_stacks = 0 if jar_details['Destroyed'] <= 0 else log10(jar_details['Destroyed'])
        cavern_advice[jar_stats].append(Advice(
            label=(
                f"{jar_details['Name']}: {jar_details['Destroyed']} destroyed"
                f"<br>{pow10_stacks:.2f} pow10 stacks = {5 * pow10_stacks:.2f}%"
            ),
            picture_class=jar_details['Image'],
            progression=f'{pow10_stacks:.2f}',
            goal=infinity_string,
            informational=True
        ))

# Collectibles Stats
    cavern_advice[collectible_stats] = [
        Advice(
            label=f"{collectible_name}: {collectible_values['Description']}",
            picture_class=collectible_values['Image'],
            progression=collectible_values['Level'],
            goal=infinity_string,  #caverns_jar_collectibles_max_level
            informational=True
        ) for collectible_name, collectible_values in collectibles.items()  # if collectible_values['Description'] != 'Boosts a future cavern... futuuure..!'
    ]

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True,
    )
    return cavern_ag

def getMotherlodeAdviceGroup():
    c_stats = "Cavern Stats"
    l_stats = 'Layer Stats'
    cavern_advice = {
        c_stats: [],
        l_stats: []
    }

    cavern_name = caverns_cavern_names[12]
    resource_type = 'Logs'
    resource_skill = 'Choppin'
    cavern = session_data.account.caverns['Caverns'][cavern_name]
# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Use your characters to collect {resource_type} while {resource_skill} and break Layers to collect Opals",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource=resource_skill
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

# Layer Stats
    cavern_advice[l_stats].append(Advice(
        label=f"Layer {cavern['LayersDestroyed']+1} {resource_skill} Efficiency Required: "
              f"{notateNumber('Basic', getMotherlodeEfficiencyRequired(cavern['LayersDestroyed']), 1)}",
        picture_class=resource_skill
    ))
    cavern_advice[l_stats].append(session_data.account.caverns['MotherlodeResourceDiscountAdvice'])
    resource_required = session_data.account.caverns['Caverns'][cavern_name]['ResourcesRemaining']
    cavern_advice[l_stats].append(Advice(
        label=f"{resource_type} remaining to break Layer {cavern['LayersDestroyed'] + 1}: "
              f"{notateNumber('Basic', resource_required - cavern['ResourcesCollected'], 1)}",
        picture_class=f'motherlode-{resource_type}',
        progression=f"{min(100, 100 * (cavern['ResourcesCollected'] / resource_required)):.1f}",
        goal=100,
        unit='%'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True,
        picture_class='cavern-2'
    )
    return cavern_ag

def getWisdomAdviceGroup() -> AdviceGroup:
    c_stats = 'Cavern Stats'
    l_stats = 'Layer Stats'
    b_stats = 'Bonuses Stats'
    cavern_advice = {
        c_stats: [],
        l_stats: [],
        b_stats: []
    }

    cavern_name = caverns_cavern_names[13]
    monument_index = 2
    cavern = session_data.account.caverns['Caverns'][cavern_name]
    layer_rewards = monument_layer_rewards[cavern_name]
    bonuses = cavern['Bonuses']

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- AFK here to gain Monument Hours",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='bravery-bonus-8'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Chance for next Opal: {getMonumentOpalChance(cavern['OpalsFound'], bonuses[5 + 10 * monument_index]['Value']):.2%}",
        picture_class='monument-basic-chest',
    ))

# Layer Stats
    cavern_advice[l_stats] = [
        Advice(
            label=f"{hour_requirement:,} hour bonus: {layer_reward['Description']}",
            picture_class=layer_reward['Image'],
            progression=cavern['Hours'],
            goal=hour_requirement
        ) for hour_requirement, layer_reward in layer_rewards.items()
    ]

    cavern_advice[l_stats].insert(0, Advice(
        label=f"Monument Hours: {cavern['Hours']:,.0f}",
        picture_class='wisdom-icon'
    ))

# Bonuses Stats
    cavern_advice[b_stats] = [
        Advice(
            label=(
                f"Level {bonus['Level']}: {bonus['Description']}"  # <br>({bonus['BaseValue']:.2f} / {bonus['ScalingValue']} of pre-multi max)"
                if bonus['ScalingValue'] > 30 else
                f"Level {bonus['Level']}: {bonus['Description']}"  # <br>(Linear: {bonus['ScalingValue']} per level)"
            ),
            picture_class=bonus['Image'],
            progression=f"{(bonus['BaseValue'] / bonus['ScalingValue']) * 100:.2f}" if bonus['ScalingValue'] > 30 else 'Linear',
            goal=100 if bonus['ScalingValue'] > 30 else infinity_string,
            unit='%' if bonus['ScalingValue'] > 30 else ''
        ) for bonus in bonuses.values()
    ]
    mv = session_data.account.caverns['Majiks']['Monumental Vibes']
    cavern_advice[b_stats].insert(0, Advice(
        label=f"Monumental Vibes {{{{ Majik|#villagers }}}}: {mv['Description']}"
              f"<br>(Already applied below)",
        picture_class=f"{mv['MajikType']}-majik-{'un' if mv['Level'] == 0 else ''}purchased",
        progression=mv['Level'],
        goal=mv['MaxLevel']
    ))

    for subgroup in cavern_advice:
        for advice in cavern_advice[subgroup]:
            mark_advice_completed(advice)

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getGambitAdviceGroup() -> AdviceGroup:
    cavern_name = caverns_cavern_names[14]
    cavern = session_data.account.caverns['Caverns'][cavern_name]

    c_stats = "Cavern Stats"
    c_faqs = "FAQs"
    challenge_stats = 'Challenge Stats'
    cavern_advice = {
        c_stats: [],
        c_faqs: [],
        challenge_stats: [],
    }

    # Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Survive as long as possible against various Summoning challenges",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    #FAQs
    cavern_advice[c_faqs].append(Advice(
        label=f"Your opponent does not have a health bar, and there is no reward for your units reaching the right edge.",
        picture_class='engineer-schematic-78'
    ))

    #Challenge Stats
    cavern_advice[challenge_stats] = [
        Advice(
            label=f"{challenge_name}"
                  f"<br>{challenge_details['TimeDisplay']} = {challenge_details['BasePts']:,.2f} base points",
            picture_class=challenge_details['Image'],
        ) for challenge_name, challenge_details in cavern['Challenges'].items()
    ]
    cavern_advice[challenge_stats].insert(0, Advice(
        label=f"Base Points: {session_data.account.caverns['Caverns'][cavern_name]['BasePts']:,.2f}",
        picture_class=''
    ))
    cavern_advice[challenge_stats].insert(1, Advice(
        label=f"Points Multi: TBD",  #{session_data.account.caverns['Caverns'][cavern_name]['PtsMulti']:,.2f}",
        picture_class=''
    ))
    cavern_advice[challenge_stats].insert(2, Advice(
        label=f"Total Points: {session_data.account.caverns['Caverns'][cavern_name]['TotalPts']:,.2f}",
        picture_class='measurement-13'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getTempleAdviceGroup() -> AdviceGroup:
    cavern_name = caverns_cavern_names[15]
    cavern = session_data.account.caverns['Caverns'][cavern_name]

    c_stats = "Cavern Stats"
    c_faqs = "FAQs"
    torch_stats = "Torch Stats"
    cavern_advice = {
        c_stats: [],
        c_faqs: [],
        torch_stats: []
    }

    # Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Fight Ancient Golems, collect Temple Torches, and Search for Centurions to collect Opals",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='ancient-golem'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Bonus Objective- Collect Dragon Warrior {{{{Statues|#statues}}}} from AFK kills.",
        picture_class='dragon-warrior-statue',
    ))
    for stamp_name in ['Cavern Resource Stamp', 'Study Hall Stamp']:
        if not session_data.account.stamps[stamp_name]['Delivered']:
            cavern_advice[c_stats].append(Advice(
                label=f"Bonus Objective- Collect {stamp_name} from AFK kills,"
                      f" then level with {session_data.account.stamps[stamp_name]['Material'].replace('-', ' ').title()}",
                picture_class=stamp_name,
            ))

    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    cavern_advice[c_faqs].append(Advice(
        label=f"Statues from Active kills don't have their quantity multiplied by Multikill. Farm them AFK instead."
              f"<br>Statues cannot be sampled.",
        picture_class='dragon-warrior-statue'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    shallow_caverns_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0  #max(shallow_caverns_progressionTiers.keys(), default=0) - info_tiers
    tier_Shallow_Caverns = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Shallow_Caverns,
        pre_string="Progression Tiers",
        advices=shallow_caverns_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Shallow_Caverns)
    return tiers_ag, overall_SectionTier, max_tier, max_tier + info_tiers

def getUndergroundOvergrowthAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.caverns['Villagers']['Polonai']['Level'] < 1:
        shallow_caverns_AdviceSection = AdviceSection(
            name="Shallow Caverns",
            tier="Not Yet Evaluated",
            header="Come back after unlocking The Caverns Below in W5!",
            picture='Shallow_Caverns.png',
            unrated=True,
            unreached=True,
            completed=False
        )
        return shallow_caverns_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    schematics = session_data.account.caverns['Schematics']
    shallow_caverns_AdviceGroupDict = {}
    shallow_caverns_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    shallow_caverns_AdviceGroupDict['The Well'] = getJarAdviceGroup(schematics)
    shallow_caverns_AdviceGroupDict['Evertree'] = getMotherlodeAdviceGroup()
    shallow_caverns_AdviceGroupDict['Wisdom'] = getWisdomAdviceGroup()
    shallow_caverns_AdviceGroupDict['Gambit'] = getGambitAdviceGroup()
    shallow_caverns_AdviceGroupDict['Temple'] = getTempleAdviceGroup()


    for ag in shallow_caverns_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    shallow_caverns_AdviceSection = AdviceSection(
        name="Underground Overgrowth",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"The Underground Overgrowth biome",  #f"Best Shallow Caverns tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Underground_Overgrowth.png',
        groups=shallow_caverns_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return shallow_caverns_AdviceSection
