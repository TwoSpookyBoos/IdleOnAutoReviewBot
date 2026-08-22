from math import ceil

from consts.progression_tiers import true_max_tiers
from consts.consts_autoreview import EmojiType

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data
from utils.logging import get_logger

# from consts.consts import shallow_caverns_progressionTiers, break_you_best, ValueToMulti
from consts.consts_caverns import schematics_unlocking_amplifiers, monument_layer_rewards, \
    getDenOpalRequirement, getMonumentOpalChance
from utils.safer_data_handling import safer_math_pow
from utils.text_formatting import notateNumber

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

def getWellAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['The Well']
    return AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True
    )

def getMotherlodeAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['Motherlode']
    cavern_ag = AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True
    )
    return cavern_ag

def getDenAdviceGroup(schematics) -> AdviceGroup:
    c_stats = "Cavern Stats"
    a_stats = 'Amplifier Stats'
    cavern_advice = {
        c_stats: [],
        a_stats: []
    }

    cavern_name = 'The Den'
    cavern = session_data.account.caverns['Caverns'][cavern_name]

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Fight increasingly difficult Dawgs, using Amplifiers to increase score",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='dawg-den-dawgs'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
    next_opal_score = getDenOpalRequirement(cavern['OpalsFound'])
    cavern_advice[c_stats].append(Advice(
        label=f"High Score: {cavern['HighScore']:,}"
              f"<br>Next Opal:  {next_opal_score:,}",
        picture_class='my-first-trophy',
        progression=f"{100 * (cavern['HighScore']/next_opal_score):.1f}",
        goal=100,
        unit='%'
    ))

# Amplifier Stats
    for amp_name, amp_details in schematics_unlocking_amplifiers.items():
        amp_unlocked = amp_details[1] == '' or schematics[amp_details[1]].bought
        cavern_advice[a_stats].append(Advice(
            label=(
                f"{amp_name}: {amp_details[0]}"
                if amp_unlocked
                else
                f"Unlock Amplifier {int(amp_details[2][-1])+1} by purchasing"
                f"<br>Schematic {schematics[amp_details[1]].unlock_order}: {amp_details[1]}"
            ),
            picture_class=amp_details[2],
            resource=(
                '' if amp_unlocked
                else schematics[amp_details[1]].resource
            )
        ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getBraveryAdviceGroup(schematics) -> AdviceGroup:
    c_stats = "Cavern Stats"
    s_stats = 'Sword Stats'
    l_stats = 'Layer Stats'
    b_stats = 'Bonuses Stats'
    cavern_advice = {
        c_stats: [],
        l_stats: [],
        s_stats: [],
        b_stats: []
    }

    cavern_name = 'Bravery Monument'
    monument_index = 0
    cavern = session_data.account.caverns['Caverns'][cavern_name]
    layer_rewards = monument_layer_rewards[cavern_name]
    bonuses = cavern['Bonuses']

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- AFK here to gain Monument Hours that empower your Attacks within the Story minigame",
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

# Sword Stats
    cavern_advice[s_stats].append(Advice(
        label=f"Total Swords: {cavern['Sword Count']}/{cavern['Max Swords']}",
        picture_class='monument-basic-sword',
        progression=cavern['Sword Count'],
        goal=cavern['Max Swords']
    ))
    cavern_advice[s_stats].append(Advice(
        label=f"Per Sword: {round(cavern['Sword Min']):,} to {round(cavern['Sword Max']):,}"
              f"<br>All Swords: {round(cavern['Sword Count'] * cavern['Sword Min']):,} to {round(cavern['Sword Count'] * cavern['Sword Max']):,}"
              f"<br>'Average' fight: {round(cavern['Sword Count'] * ((cavern['Sword Max'] - cavern['Sword Min']) / 2)):,}",
        picture_class='monument-basic-sword'
    ))

    cavern_advice[s_stats].append(Advice(
        label=f"{cavern['Rethrows']}/{cavern['Max Rethrows']} Sword Rethrows per Fight",
        picture_class='engineer-schematic-40',
        progression=cavern['Rethrows'],
        goal=cavern['Max Rethrows']
    ))
    cavern_advice[s_stats].append(Advice(
        label=f"{cavern['Retellings']}/{cavern['Max Retellings']} Retellings per Story attempt",
        picture_class='engineer-schematic-40',
        progression=cavern['Retellings'],
        goal=cavern['Max Retellings']
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
        picture_class='bravery-bonus-9'
    ))

# Bonuses Stats
    cavern_advice[b_stats] = [
        Advice(
            label=(
                f"Level {bonus['Level']}: {bonus['Description']}"
                f"<br>{bonus['BaseValue']:.2f}/{bonus['ScalingValue']} max from Levels"
                if bonus['ScalingValue'] > 30 else
                f"Level {bonus['Level']}: {bonus['Description']}"
                f"<br>+{bonus['ScalingValue'] if '%' in bonus['Description'] else '0.' if bonus['ScalingValue'] >= 10 else '0.0'}"
                f"{'' if '%' in bonus['Description'] else bonus['ScalingValue']}"
                f"{'%' if '%' in bonus['Description'] else 'x'} "
                f"per level before multis"
            ),
            picture_class=bonus['Image'],
            progression=f"{(bonus['BaseValue'] / bonus['ScalingValue']) * 100:.2f}" if bonus['ScalingValue'] > 30 else 'Linear',
            goal=100 if bonus['ScalingValue'] > 30 else EmojiType.INFINITY.value,
            unit='%' if bonus['ScalingValue'] > 30 else ''
        ) for bonus in bonuses.values()
    ]
    mv = session_data.account.caverns_.villagers["Cosmos"].majiks.hole['Monumental Vibes']
    cavern_advice[b_stats].insert(0, mv.get_advice())

    for subgroup in cavern_advice:
        for advice in cavern_advice[subgroup]:
            advice.mark_advice_completed()

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getBellAdviceGroup(schematics):
    c_stats = "Cavern Stats"
    r_stats = 'Ring Stats'
    improvement_stats = 'Improvement Stats'
    cavern_advice = {
        c_stats: [],
        r_stats: [],
        improvement_stats: []
    }

    cavern_name = 'The Bell'
    cavern = session_data.account.caverns['Caverns'][cavern_name]

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Passively build up Charge in 1 of 4 different categories at a time for various Bonuses",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    target_cost = ceil(cavern['Charges']['Ping'][2])
    target_string = notateNumber('Basic', target_cost, 2)
    current_number = cavern['Charges']['Ping'][0]
    current_string = notateNumber('Match', current_number, 2, '', target_string)
    current_percent = 100 * (cavern['Charges']['Ping'][0] / target_cost)
    cavern_advice[c_stats].append(Advice(
        label=f"Current Ping charge: {current_string}"
              f"<br>Next Opal: {target_string}",
        picture_class='bell-ping',
        progression=f"{current_percent:,.2f}",
        goal=100,
        unit='%'
    ))

# Ring Bonuses
    cavern_advice[r_stats] = [
        Advice(
            label=f"{rb_details['Description']}",
            picture_class=rb_details['Image'],
            progression=rb_details['Level'],
            goal=EmojiType.INFINITY.value
        ) for rb_index, rb_details in cavern['Ring Bonuses'].items()
    ]
    total_rings = cavern['Charges']['Ring'][1]
    cavern_advice[r_stats].insert(0, Advice(
        label=f"Total Rings: {total_rings}",
        picture_class='bell-ring'
    ))
    total_bonus_levels = sum([rb_details['Level'] for rb_details in cavern['Ring Bonuses'].values()])
    average_level = total_bonus_levels/max(1,total_rings)

    cavern_advice[r_stats].insert(1, Advice(
        label=f"Total Bonus levels: {total_bonus_levels}"
              f"<br>Avg per ring: {average_level:.4f}",
        picture_class='bell-ring',
        completed=False,
        informational=True
    ))

# Clean Improvements
    total_improvements = cavern['Total Improvements']
    stack_size = cavern['Stack Size']
    total_stacks = cavern['Total Stacks']
    cavern_advice[improvement_stats] = [
        Advice(
            label=ci_details['Description'],
            picture_class=ci_details['Image'],
            progression=ci_details['Level'],
            goal=EmojiType.INFINITY.value,
            resource=ci_details['Resource'],
        ) for ci_index, ci_details in cavern['Improvements'].items()
    ]
    cavern_advice[improvement_stats].insert(0, Advice(
        label=f"Total Improvements: {total_improvements} ({total_stacks} stacks)"
              f"<br>Total Bonus: {safer_math_pow(1.1, total_stacks):.1f}x"
              f"<br>Next stack progress",
        picture_class='engineer-schematic-45',
        progression=total_improvements % stack_size,
        goal=stack_size
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
    optional_tiers = 0
    true_max = true_max_tiers['Shallow Caverns']
    max_tier = true_max - optional_tiers
    tier_Shallow_Caverns = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Shallow_Caverns,
        pre_string="Progression Tiers",
        advices=shallow_caverns_AdviceDict['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Shallow_Caverns)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getShallowCavernsAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.caverns_.villagers["Polonai"].level < 1:
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
    schematics = session_data.account.caverns_.villagers["Kaipu"].schematics
    shallow_caverns_AdviceGroupDict = {}
    shallow_caverns_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    shallow_caverns_AdviceGroupDict['The Well'] = getWellAdviceGroup()
    shallow_caverns_AdviceGroupDict['Motherlode'] = getMotherlodeAdviceGroup()
    shallow_caverns_AdviceGroupDict['The Den'] = getDenAdviceGroup(schematics)
    shallow_caverns_AdviceGroupDict['Bravery Monument'] = getBraveryAdviceGroup(schematics)
    shallow_caverns_AdviceGroupDict['The Bell'] = getBellAdviceGroup(schematics)

    for ag in shallow_caverns_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    shallow_caverns_AdviceSection = AdviceSection(
        name="Shallow Caverns",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"The Shallow Caverns biome",  #f"Best Shallow Caverns tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Shallow_Caverns.png',
        groups=shallow_caverns_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return shallow_caverns_AdviceSection
