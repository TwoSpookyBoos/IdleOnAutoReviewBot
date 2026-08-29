from consts.progression_tiers import true_max_tiers
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data
from utils.logging import get_logger

logger = get_logger(__name__)


def getJarAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["The Jar"]
    cavern_ag = AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag


def getEvertreeAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["Evertree"]
    return AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )


def getWisdomAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["Wisdom Monument"]
    cavern_ag = AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag


def getGambitAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["Gambit"]
    cavern_ag = AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag


def getTempleAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["The Temple"]
    return AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )


def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    shallow_caverns_AdviceDict = {
        "Tiers": {},
    }
    optional_tiers = 0
    true_max = true_max_tiers["Underground Overgrowth"]
    max_tier = true_max - optional_tiers
    tier_Shallow_Caverns = 0

    # Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Shallow_Caverns,
        pre_string="Progression Tiers",
        advices=shallow_caverns_AdviceDict["Tiers"],
    )
    overall_SectionTier = min(true_max, tier_Shallow_Caverns)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getUndergroundOvergrowthAdviceSection() -> AdviceSection:
    # Check if player has reached this section
    if session_data.account.caverns.villagers["Polonai"].level < 11:
        shallow_caverns_AdviceSection = AdviceSection(
            name="Shallow Caverns",
            tier="Not Yet Evaluated",
            header="Come back after unlocking The Caverns Below in W5!",
            picture="Shallow_Caverns.png",
            unrated=True,
            unreached=True,
            completed=False,
        )
        return shallow_caverns_AdviceSection

    # Generate Alert Advice

    # Generate AdviceGroups
    shallow_caverns_AdviceGroupDict = {}
    (
        shallow_caverns_AdviceGroupDict["Tiers"],
        overall_SectionTier,
        max_tier,
        true_max,
    ) = getProgressionTiersAdviceGroup()
    shallow_caverns_AdviceGroupDict["The Jar"] = getJarAdviceGroup()
    shallow_caverns_AdviceGroupDict["Evertree"] = getEvertreeAdviceGroup()
    shallow_caverns_AdviceGroupDict["Wisdom"] = getWisdomAdviceGroup()
    shallow_caverns_AdviceGroupDict["Gambit"] = getGambitAdviceGroup()
    shallow_caverns_AdviceGroupDict["Temple"] = getTempleAdviceGroup()

    for ag in shallow_caverns_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    shallow_caverns_AdviceSection = AdviceSection(
        name="Underground Overgrowth",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header="The Underground Overgrowth biome",
        picture="customized/Underground_Overgrowth.png",
        groups=shallow_caverns_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return shallow_caverns_AdviceSection
