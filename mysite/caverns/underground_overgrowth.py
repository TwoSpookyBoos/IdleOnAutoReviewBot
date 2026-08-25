from consts.progression_tiers import true_max_tiers

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data
from utils.safer_data_handling import safer_math_pow, safer_math_log
from utils.logging import get_logger

from consts.consts_autoreview import ValueToMulti
from consts.consts_caverns import caverns_cavern_names
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getGambitSearchChance(current_opals, illuminate_multi, torches_owned, torch_overwrite=False):
    if torch_overwrite:
        result = 0.05 * illuminate_multi * safer_math_pow(.7, current_opals) * safer_math_log(max(5, torches_owned), 2)
    else:
        result = 0.05 * illuminate_multi * safer_math_pow(.7, current_opals) * safer_math_log(max(5, torches_owned / 4), 2)
    return result

def getJarAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves["The Jar"]
    cavern_ag = AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag

def getEvertreeAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['Evertree']
    return AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )

def getWisdomAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['Wisdom Monument']
    cavern_ag = AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag

def getGambitAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves["Gambit"]
    cavern_ag = AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    cavern_ag.mark_advice_completed()
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
        if not session_data.account.stamps[stamp_name].delivered:
            cavern_advice[c_stats].append(Advice(
                label=f"Bonus Objective - Collect {stamp_name} from AFK kills,"
                      f" then level with {session_data.account.stamps[stamp_name].material.name}",
                picture_class=stamp_name,
            ))

    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    #FAQs
    cavern_advice[c_faqs].append(Advice(
        label=f"Statues from Active kills don't have their quantity multiplied by Multikill. Farm them AFK instead."
              f"<br>Statues cannot be sampled.",
        picture_class='dragon-warrior-statue'
    ))
    cavern_advice[c_faqs].append(Advice(
        label=f"Respawn% from Amplify only works while Active! Your AFK kills will not be increased.",
        picture_class='temple-torch'
    ))
    cavern_advice[c_faqs].append(Advice(
        label=f"Searching costs 25% of your Torches (minimum of 5). Chance doesn't scale well, so search early and often!",
        picture_class='temple-torch'
    ))

    #Torch Stats
    cavern_advice[torch_stats].append(Advice(
        label=f"Torches owned: {notateNumber('Basic', cavern['Torches Owned'], 3 if cavern['Torches Owned'] >= 1000 else 0)}",
        picture_class='temple-torch'
    ))
    illuminate_multi = ValueToMulti(10 * cavern['Illuminate'])
    cavern_advice[torch_stats].append(Advice(
        label=f"{cavern['Illuminate']} Illuminations: {illuminate_multi}x Search chance",
        picture_class='temple-torch'
    ))
    cavern_advice[torch_stats].append(Advice(
        label=(
            f"Sanctum {cavern['OpalsFound'] + 1} search odds"
            f"<br>5 torches: {getGambitSearchChance(cavern['OpalsFound'], illuminate_multi, 5):.6%}"
            f"<br>500 torches: {getGambitSearchChance(cavern['OpalsFound'], illuminate_multi, 500, True):.6%}"
            f"<br>50K torches: {getGambitSearchChance(cavern['OpalsFound'], illuminate_multi, 50000, True):.6%}"
        ),
        picture_class='temple-torch'
    ))
    cavern_advice[torch_stats].append(Advice(
        label=f"{cavern['Amplify']} Amplifications: +{(5 * cavern['Amplify'])}% Respawn while Active",
        picture_class='temple-torch'
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
    true_max = true_max_tiers['Underground Overgrowth']
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

def getUndergroundOvergrowthAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.caverns_.villagers["Polonai"].level < 11:
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
    shallow_caverns_AdviceGroupDict = {}
    shallow_caverns_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    shallow_caverns_AdviceGroupDict['The Jar'] = getJarAdviceGroup()
    shallow_caverns_AdviceGroupDict['Evertree'] = getEvertreeAdviceGroup()
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
