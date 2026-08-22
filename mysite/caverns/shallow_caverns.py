from math import ceil

from consts.progression_tiers import true_max_tiers
from consts.consts_autoreview import EmojiType

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data
from utils.logging import get_logger

# from consts.consts import shallow_caverns_progressionTiers, break_you_best, ValueToMulti
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

def getDenAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['The Den']
    return AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True
    )

def getBraveryAdviceGroup(schematics) -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['Bravery Monument']
    cavern_ag = AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True
    )
    cavern_ag.mark_advice_completed()
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
    shallow_caverns_AdviceGroupDict['The Den'] = getDenAdviceGroup()
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
