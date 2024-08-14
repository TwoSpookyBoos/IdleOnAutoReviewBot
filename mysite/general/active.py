from models.models import Advice, AdviceGroup, AdviceSection
from consts import maxTiersPerGroup, lavaFunc, stamp_maxes
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getCrystalSpawnChanceAdviceGroup() -> AdviceGroup:
    aw = "Account Wide"
    cs = "Character Specific"
    total = "Total"
    crystal_Advice = {
        aw: [],
        cs: [],
        total: [],
    }
    # Account Wide
    crystal_Advice[aw].append(Advice(
        label="Chocco Chip for more Crystal Mobs",
        picture_class="chocolatey-chip",
        progression=session_data.account.labChips.get('Chocolatey Chip', 0),
        goal=1
    ))
    crystal_Advice[aw].append(Advice(
        label=f"W4 Demon Genie card: +{15 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Demon Genie'))}"
              f"/90% Crystal Mob Spawn Chance",
        picture_class="demon-genie-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Demon Genie"),
        goal=6
    ))
    crystal_Advice[aw].append(Advice(
        label=f"W1 Poop card: +{10 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Poop'))}"
              f"/60% Crystal Mob Spawn Chance",
        picture_class="poop-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Poop"),
        goal=6
    ))
    crystal_Advice[aw].append(Advice(
        label="Omega Nanochip: Top Left card doubler",
        picture_class="omega-nanochip",
        progression=session_data.account.labChips.get('Omega Nanochip', 0),
        goal=1
    ))
    crystal_Advice[aw].append(Advice(
        label="Omega Motherboard: Bottom Right card doubler",
        picture_class="omega-motherboard",
        progression=session_data.account.labChips.get('Omega Motherboard', 0),
        goal=1
    ))
    crystal_Advice[aw].append(Advice(
        label=f"Level {session_data.account.stamps['Crystallin']['Level']}/{stamp_maxes['Crystallin']} Crystallin Stamp: {1 + session_data.account.stamps['Crystallin']['Value'] / 100:.3f}x",
        picture_class="crystallin",
        progression=session_data.account.stamps['Crystallin']['Level'],
        goal=stamp_maxes['Crystallin']
    ))
    crystal_Advice[aw].append(Advice(
        label=f"Level {session_data.account.shrines['Crescent Shrine']['Level']} Crescent Shrine: +{session_data.account.shrines['Crescent Shrine']['Value']:.0f}%",
        picture_class="crescent-shrine",
    ))
    cchizoar_multi = 1 + (5 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Chaotic Chizoar')) / 100)
    crystal_Advice[aw].append(Advice(
        label=f"Chaotic Chizoar card to increase Crescent Shrine ({cchizoar_multi}x multi already included)",
        picture_class="chaotic-chizoar-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Chaotic Chizoar"),
        goal=6
    ))
    crystal_Advice[aw].append(Advice(
        label=f"{{{{ Sailing|#sailing }}}}: Moai Head artifact to apply Shrines everywhere",
        picture_class="moai-head",
        progression=session_data.account.sailing['Artifacts']['Moai Head']['Level'],
        goal=1
    ))

    # Character Specific
    bestCrystalBook = 0
    for jman in session_data.account.jmans:
        bestCrystalBook = max(bestCrystalBook, jman.max_talents.get("26", 0))
    crystal_Advice[cs].append(Advice(
        label=f"Level {bestCrystalBook}/{session_data.account.library['MaxBookLevel']} booked Cmon Out Crystals talent (Jman only)",
        picture_class="cmon-out-crystals",
        progression=bestCrystalBook,
        goal=session_data.account.library['MaxBookLevel']
    ))
    crystals_4_dayys_multi = 1 + lavaFunc('decay', 100, 174, 50) / 100
    crystal_Advice[cs].append(Advice(
        label=f"Crystals 4 Dayys star talent: {crystals_4_dayys_multi}x at level 100",
        picture_class="crystals-4-dayys",
    ))
    box_value = lavaFunc('decay', 300, 65, 200)
    crystal_Advice[cs].append(Advice(
        label=f"Non Predatory Loot Box: +{box_value:.0f}% at 400 crates",
        picture_class="non-predatory-loot-box",
    ))

    # Totals
    crystal_Advice[total].append(Advice(
        label=f"Note: Crescent Shrine and PO Box are additive: {1 + ((session_data.account.shrines['Crescent Shrine']['Value'] + box_value) / 100)}x"
              f"<br>The cards also add together. Everything else is a unique multiplier.",
        picture_class="shrine-box2"
    ))

    crystal_Advice[total].append(Advice(
        label=f"Best Crystal Spawn Chance on Non-Jman:"
              f" {session_data.account.highest_crystal_spawn_chance * 100:.4f}%"
              f" (1 in {100 / (session_data.account.highest_crystal_spawn_chance * 100):.2f})",
        picture_class="crystal-carrot",
    ))
    crystal_Advice[total].append(Advice(
        label=f"Best Crystal Spawn Chance on Jman:"
              f" {session_data.account.highest_jman_crystal_spawn_chance * 100:.4f}%"
              f" (1 in {100 / (session_data.account.highest_jman_crystal_spawn_chance * 100):.2f})",
        picture_class="crystal-crabal",
    ))

    for subgroup in crystal_Advice:
        for advice in crystal_Advice[subgroup]:
            mark_advice_completed(advice)

    crystal_AG = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Crystal Spawn Chance",
        advices=crystal_Advice
    )
    return crystal_AG

def setActiveProgressionTier() -> AdviceSection:
    active_AdviceDict = {}
    active_AdviceGroupDict = {}
    active_AdviceSection = AdviceSection(
        name="Active",
        tier="Not Yet Evaluated",
        header="Best Active tier met: Not Yet Evaluated. Recommended Star Sign actions",
        picture='Auto.png'
    )

    infoTiers = 0
    max_tier = 0
    tier_Active = 0

    # Generate Advice
    # for tierNumber, tierRequirements in active_progressionTiers.items():
    #     subgroupName = f"To reach Tier {tierNumber}"
    #             if subgroupName not in active_AdviceDict["Tiers"] and len(active_AdviceDict["Tiers"]) < maxTiersPerGroup:
    #                 active_AdviceDict["Tiers"][subgroupName] = []
    #             if subgroupName in active_AdviceDict["Tiers"]:
    #                 active_AdviceDict['Tiers'][subgroupName].append(Advice(
    #                     label=f"Level up {statueName}{farmDetails}",
    #                     picture_class=statueName,
    #                     progression=statueDetails['Level'],
    #                     goal=tierRequirements.get('MinStatueLevel', 0),
    #                     resource=farmResource
    #                 ))
    #     if subgroupName not in active_AdviceDict["Tiers"] and tier_Active == tierNumber-1:
    #         tier_Active = tierNumber

    # Generate AdviceGroups
    active_AdviceGroupDict['Crystals'] = getCrystalSpawnChanceAdviceGroup()

    # Generate AdviceSection
    overall_ActiveTier = min(max_tier + infoTiers, tier_Active)
    tier_section = f"{overall_ActiveTier}/{max_tier}"
    active_AdviceSection.pinchy_rating = overall_ActiveTier
    active_AdviceSection.tier = tier_section
    active_AdviceSection.groups = active_AdviceGroupDict.values()
    if overall_ActiveTier >= max_tier:
        active_AdviceSection.header = f"Active Farming Information"
        active_AdviceSection.complete = True
    else:
        active_AdviceSection.header = f"Active Farming Information"

    return active_AdviceSection
