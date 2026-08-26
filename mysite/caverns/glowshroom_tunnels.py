from consts.progression_tiers import true_max_tiers
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data
from utils.logging import get_logger

logger = get_logger(__name__)


def getHarpAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["The Harp"]
    cavern_ag = AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag


def getLampAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["The Lamp"]
    return AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )


def getHiveAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["The Hive"]
    return AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )


def getGrottoAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["Grotto"]
    cavern_ag = AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    session_data.account.add_alert_list("The Caverns Below", [cavern.alert_advice()])
    return cavern_ag


def getJusticeAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns.caves["Justice Monument"]
    cavern_ag = AdviceGroup(
        tier="",
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag


def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    glowshroom_tunnels_AdviceDict = {
        "Tiers": {},
    }
    optional_tiers = 0
    true_max = true_max_tiers["Glowshroom Tunnels"]
    max_tier = true_max - optional_tiers
    tier_Glowshroom_Tunnels = 0

    # Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Glowshroom_Tunnels,
        pre_string="Progression Tiers",
        advices=glowshroom_tunnels_AdviceDict["Tiers"],
    )
    overall_SectionTier = min(true_max, tier_Glowshroom_Tunnels)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getGlowshroomTunnelsAdviceSection() -> AdviceSection:
    # Check if player has reached this section
    if session_data.account.caverns.villagers["Polonai"].level < 6:
        glowshroom_tunnels_AdviceSection = AdviceSection(
            name="Glowshroom Tunnels",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Cavern 6+ in W5!",
            picture="Glowshroom_Tunnels.png",
            unrated=True,
            unreached=True,
            completed=False,
        )
        return glowshroom_tunnels_AdviceSection

    # Generate AdviceGroups
    glowshroom_tunnels_AdviceGroupDict = {}
    (
        glowshroom_tunnels_AdviceGroupDict["Tiers"],
        overall_SectionTier,
        max_tier,
        true_max,
    ) = getProgressionTiersAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict["The Harp"] = getHarpAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict["The Lamp"] = getLampAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict["The Hive"] = getHiveAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict["Grotto"] = getGrottoAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict["Justice Monument"] = getJusticeAdviceGroup()

    for ag in glowshroom_tunnels_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    glowshroom_tunnels_AdviceSection = AdviceSection(
        name="Glowshroom Tunnels",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header="The Glowshroom Tunnels biome",
        picture="customized/Glowshroom_Tunnels.png",
        groups=glowshroom_tunnels_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return glowshroom_tunnels_AdviceSection
