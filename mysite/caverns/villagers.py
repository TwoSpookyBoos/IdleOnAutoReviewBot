from consts.caverns.cavern import max_cavern
from consts.caverns.villager.minau import max_measurements
from consts.idleon.caverns.villager.kaipu import available_schematics
from consts.progression_tiers import true_max_tiers
from models.advice.advice import Advice
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data
from utils.logging import get_logger

# villagers_progressionTiers,

logger = get_logger(__name__)


def getVillagersAdviceGroups() -> dict[str, AdviceGroup]:
    villager_ags = {
        "Explorer": getExplorerAdviceGroup(),
        "Engineer": getEngineerAdviceGroup(),
        "Conjuror": getConjurorAdviceGroup(),
        "Measurer": getMeasurerAdviceGroup(),
        "Librarian": getLibrarianAdviceGroup(),
    }
    return villager_ags


def getExplorerAdviceGroup() -> AdviceGroup:
    polonai = session_data.account.caverns_.villagers["Polonai"]
    villager_advice = {"Villager Stats": polonai.stat_advices()}
    discover_advices = polonai.feature_advice()
    if discover_advices:
        villager_advice.update(discover_advices)
    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Level {polonai.level} {polonai.title}",
        advices=villager_advice,
        informational=True,
        completed=polonai.level >= max_cavern,
    )
    villager_ag.mark_advice_completed()
    return villager_ag


def getEngineerAdviceGroup() -> AdviceGroup:
    kaipu = session_data.account.caverns_.villagers["Kaipu"]
    villager_advice = {"Villager Stats": kaipu.stat_advices()}
    schematics_advice = kaipu.feature_advice()
    if schematics_advice:
        villager_advice.update(schematics_advice)
    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Level {kaipu.level} {kaipu.title}",
        advices=villager_advice,
        informational=True,
        completed=kaipu.schematics.bought >= available_schematics,
    )
    villager_ag.remove_empty_subgroups()
    villager_ag.mark_advice_completed()
    return villager_ag


def getConjurorAdviceGroup() -> AdviceGroup:
    gscp = session_data.account.gemshop["Purchases"]["Conjuror Pts"]
    cosmos = session_data.account.caverns_.villagers["Cosmos"]
    villager_advice = {"Villager Stats": cosmos.stat_advices()}
    feature_advice = cosmos.feature_advice()
    if feature_advice:
        villager_advice.update(feature_advice)
    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Level {cosmos.level} {cosmos.title}",
        advices=villager_advice,
        informational=True,
        completed=cosmos.level + gscp["Owned"] >= cosmos.majiks.max_point,
    )
    villager_ag.mark_advice_completed()
    return villager_ag


def getMeasurerAdviceGroup() -> AdviceGroup:
    minau = session_data.account.caverns_.villagers["Minau"]
    villager_advice = {"Villager Stats": minau.stat_advices()}
    feature_advice = minau.feature_advice()
    if feature_advice:
        villager_advice.update(feature_advice)
    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Level {minau.level} {minau.title}",
        advices=villager_advice,
        informational=True,
        completed=minau.level >= max_measurements,
    )
    villager_ag.mark_advice_completed()
    return villager_ag


def getLibrarianAdviceGroup() -> AdviceGroup:
    bolaia = session_data.account.caverns_.villagers["Bolaia"]
    villager_advice = {
        "Villager Stats": bolaia.stat_advices(),
    }
    feature_advice = bolaia.feature_advice()
    if feature_advice:
        villager_advice.update(feature_advice)

    schematics = session_data.account.caverns_.villagers["Kaipu"].schematics
    # Study Speed Sources
    total_base_speed = 5
    max_base_speed = 5
    base_speed_advice = [
        Advice(
            label="Base study speed: 100 + 5/hr per level",
            picture_class=bolaia.name,
            progression=1,
            goal=1,
        )
    ]
    for schematic_name, speed_boost in {
        "Peer Reviewed Books": 2,
        "Cutting Edge Research": 3,
        "Billion Dollar Grant": 5,
    }.items():
        schematic = schematics[schematic_name]
        base_speed_advice.append(schematic.get_advice())
        total_base_speed += speed_boost * int(schematic.bought)
        max_base_speed += speed_boost
    villager_advice["Study Speed"] = [
        Advice(
            label=f"Total Base: {100 + total_base_speed}/hr per level",
            picture_class=bolaia.name,
            progression=total_base_speed,
            goal=max_base_speed,
        )
    ]
    villager_advice["Base"] = base_speed_advice
    multi_speed = "Multi Group I"
    villager_advice[multi_speed] = []
    rosemerald = session_data.account.caverns_.caves["The Jar"].collectibles[
        "Rosemerald"
    ]
    villager_advice[multi_speed].append(rosemerald.get_bonus_advice())
    study_majik = session_data.account.caverns_.villagers["Cosmos"].majiks.village[
        "Study All Nighter"
    ]
    villager_advice[multi_speed].append(study_majik.get_advice())
    villager_advice[multi_speed].append(
        session_data.account.stamps["Study Hall Stamp"].get_advice()
    )
    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Level {bolaia.level} {bolaia.title}",
        advices=villager_advice,
        informational=True,
        completed=False,
    )
    villager_ag.mark_advice_completed()
    return villager_ag


def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    villagers_AdviceDict = {
        "Tiers": {},
    }
    optional_tiers = 0
    true_max = true_max_tiers["Villagers"]
    max_tier = true_max - optional_tiers
    tier_Villagers = 0

    # Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Villagers,
        pre_string="Progression Tiers",
        advices=villagers_AdviceDict["Tiers"],
    )
    overall_SectionTier = min(true_max, tier_Villagers)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getVillagersAdviceSection() -> AdviceSection:
    # Check if player has reached this section
    if session_data.account.caverns_.villagers["Polonai"].level < 0:
        villagers_AdviceSection = AdviceSection(
            name="Villagers",
            tier="Not Yet Evaluated",
            header="Come back after unlocking The Caverns Below in W5!",
            picture="wiki/Hole_Campfire.gif",
            unrated=False,
            unreached=True,
            completed=False,
        )
        return villagers_AdviceSection

    # Generate Alert Advice
    session_data.account.add_alert_list(
        "The Caverns Below",
        [
            villager.level_ready_alert()
            for villager in session_data.account.caverns_.villagers.values()
        ],
    )

    # Generate AdviceGroups
    villagers_AdviceGroupDict = {}
    villagers_AdviceGroupDict["Tiers"], overall_SectionTier, max_tier, true_max = (
        getProgressionTiersAdviceGroup()
    )
    villagers_AdviceGroupDict.update(getVillagersAdviceGroups())

    for ag in villagers_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    villagers_AdviceSection = AdviceSection(
        name="Villagers",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header="Villager Information",
        picture="wiki/Hole_Campfire.gif",
        groups=villagers_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
        informational=True,
    )

    return villagers_AdviceSection
