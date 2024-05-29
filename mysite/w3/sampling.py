from flask import g as session_data
from consts import maxStaticBookLevels, maxScalingBookLevels, maxSummoningBookLevels
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.data_formatting import safe_loads

def getBookLevelAdviceGroup() -> AdviceGroup:
    bookLevelAdvices = {
    }

    #Static Sources
    static_sum = (0
                  + (25 * (0 < session_data.account.construction_buildings.get('Talent Book Library', 0)))
                  + (5 * (0 < session_data.account.achievements.get('Checkout Takeout', False)))
                  + (10 * (0 < session_data.account.atoms.get('Oxygen - Library Booker', 0)))
                  + (25 * session_data.account.artifacts.get('Fury Relic', 0))
                  )
    staticSubgroup = f"Static Sources: +{static_sum}/{maxStaticBookLevels}"
    bookLevelAdvices[staticSubgroup] = []

    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Construction: Talent Book Library built: +{25 * (0 < session_data.account.construction_buildings.get('Talent Book Library', 0))}",
        picture_class="talent-book-library",
        progression=min(1, session_data.account.construction_buildings.get('Talent Book Library', 0)),
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"W3 Achievement: Checkout Takeout: +{5 * (0 < session_data.account.achievements.get('Checkout Takeout', False))}",
        picture_class="checkout-takeout",
        progression=1 if session_data.account.achievements.get('Checkout Takeout', False) else 0,
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Atom Collider: Oxygen: +{10 * (0 < session_data.account.atoms.get('Oxygen - Library Booker', 0))}",
        picture_class="oxygen",
        progression=1 if 0 < session_data.account.atoms.get('Oxygen - Library Booker', 0) else 0,
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Sailing: Base Fury Relic: +{25 * (0 < session_data.account.artifacts.get('Fury Relic', 0))}",
        picture_class="fury-relic",
        progression=1 if 0 < session_data.account.artifacts.get('Fury Relic', 0) else 0,
        goal=1
    ))
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Sailing: Ancient Fury Relic: +{25 * (1 < session_data.account.artifacts.get('Fury Relic', 0))}",
        picture_class="fury-relic",
        progression=1 if 1 < session_data.account.artifacts.get('Fury Relic', 0) else 0,
        goal=1
    ))
    eldritch_unlockNote = ". Eldritch Artifacts are unlocked by reaching Rift 31" if not session_data.account.eldritch_artifacts_unlocked else ""
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Sailing: Eldritch Fury Relic: +{25 * (2 < session_data.account.artifacts.get('Fury Relic', 0))}{eldritch_unlockNote}",
        picture_class="eldritch-artifact",
        progression=1 if 2 < session_data.account.artifacts.get('Fury Relic', 0) else 0,
        goal=1
    ))
    sov_unlockNote = ". Sovereign Artifacts are unlocked from the Jade Emporium" if "Sovereign Artifacts" not in session_data.account.jade_emporium_purchases else ""
    bookLevelAdvices[staticSubgroup].append(Advice(
        label=f"Sailing: Sovereign Fury Relic: +{25 * (3 < session_data.account.artifacts.get('Fury Relic', 0))}{sov_unlockNote}",
        picture_class="sovereign-artifacts",
        progression=1 if 3 < session_data.account.artifacts.get('Fury Relic', 0) else 0,
        goal=1
    ))

    #Scaling Sources
    scaling_sum = (0
                   + 2 * session_data.account.merits[2][2]['Level']
                   + 2 * session_data.account.saltlick.get('Max Book', 0)
                   )
    scalingSubgroup = f"Scaling Sources: +{scaling_sum}/{maxScalingBookLevels}"
    bookLevelAdvices[scalingSubgroup] = []

    bookLevelAdvices[scalingSubgroup].append(Advice(
        label=f"W3 Max Book level Merit: +{2 * session_data.account.merits[2][2]['Level']}",
        picture_class="",
        progression=session_data.account.merits[2][2]["Level"],
        goal=session_data.account.merits[2][2]["MaxLevel"]
    ))
    bookLevelAdvices[scalingSubgroup].append(Advice(
        label=f"Salt Lick: +{2 * session_data.account.saltlick.get('Max Book', 0)}",
        picture_class="salt-lick",
        progression=session_data.account.saltlick.get('Max Book', 0),
        goal=10
    ))

    summGroupA = (1 + (.25 * session_data.account.artifacts.get('The Winz Lantern', 0))
                    + .01 * session_data.account.merits[5][4]['Level']
                    + .01 * (0 < session_data.account.achievements.get('Spectre Stars', False))
                    + .01 * (0 < session_data.account.achievements.get('Regalis My Beloved', False))
                  )
    summGroupB = 1 + (.3 * session_data.account.sneaking.get('PristineCharms', {}).get('Crystal Comb', 0))
    summoning_sum = round(0
                          + 10.5 * ('w6d3' in session_data.account.summoning['BattlesWon'])
                          * summGroupA * summGroupB
                          )
    summoningSubgroup = f"Summoning Winner Bonus: +{summoning_sum}/{maxSummoningBookLevels}"
    bookLevelAdvices[summoningSubgroup] = []
    #W6 Summoning Cyan14 fight, times Winner Output bonuses
    cyan14beat = 'w6d3' in session_data.account.summoning['BattlesWon']
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"Summoning Cyan14: +{10.5 * cyan14beat}",
        picture_class="samurai-guardian",
        progression=1 if 'w6d3' in session_data.account.summoning['BattlesWon'] else 0,
        goal=1
    ))
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"Sailing: The Winz Lantern: {1 + (.25 * session_data.account.artifacts.get('The Winz Lantern', 0))}x",
        picture_class="the-winz-lantern",
        progression=session_data.account.artifacts.get('The Winz Lantern', 0),
        goal=4
    ))
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f":Pristine Charm: Crystal Comb: {1.3 * session_data.account.sneaking.get('PristineCharms', {}).get('Crystal Comb', 0)}x{' once Cyan14 beat' if not cyan14beat else ''}",
        picture_class="crystal-comb",
        progression=1 if session_data.account.sneaking.get("PristineCharms", {}).get('Crystal Comb', False) else 0,
        goal=1
    ))
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"W6 Larger Winner bonuses merit: +{session_data.account.merits[5][4]['Level']}%{' once Cyan14 beat' if not cyan14beat else ''}",
        picture_class="",
        progression=session_data.account.merits[5][4]["Level"],
        goal=session_data.account.merits[5][4]["MaxLevel"]
    ))
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"W6 Achievement: Spectre Stars: +{1 * (0 < session_data.account.achievements.get('Spectre Stars', False))}%{' once Cyan14 beat' if not cyan14beat else ''}",
        picture_class="spectre-stars",
        progression=1 if session_data.account.achievements.get('Spectre Stars', False) else 0,
        goal=1
    ))
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"W6 Achievement: Regalis My Beloved: +{1 * (0 < session_data.account.achievements.get('Regalis My Beloved', False))}%{' once Cyan14 beat' if not cyan14beat else ''}",
        picture_class="regalis-my-beloved",
        progression=1 if session_data.account.achievements.get('Regalis My Beloved', False) else 0,
        goal=1
    ))
    bookLevelAdvices[summoningSubgroup].append(Advice(
        label=f"TODO: Verify if this uses ceiling or rounding",
        picture_class="",
    ))

    bookLevelAdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Info- Sources of Max Book Levels ({100 + static_sum + scaling_sum + summoning_sum}/{100 + maxStaticBookLevels + maxScalingBookLevels + maxSummoningBookLevels})",
        advices=bookLevelAdvices
    )
    return bookLevelAdviceGroup

def setSamplingProgressionTier() -> AdviceSection:
    sampling_AdviceDict = {
        "MaxBookLevels": []
    }
    sampling_AdviceGroupDict = {}
    sampling_AdviceSection = AdviceSection(
        name="Sampling",
        tier="Not Yet Evaluated",
        header="",
        picture="3D_Printer.png",
    )
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        sampling_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return sampling_AdviceSection
    elif safe_loads(session_data.account.raw_data["Tower"])[3] < 1:
        sampling_AdviceSection.header = "Come back after unlocking the 3D Printer within the Construction skill in World 3!"
        return sampling_AdviceSection

    max_tier = 0
    tier_bookLevels = 0

    # Generate AdviceGroups
    sampling_AdviceGroupDict["MaxBookLevels"] = getBookLevelAdviceGroup()

    # Generate AdviceSection
    overall_SamplingTier = min(max_tier, tier_bookLevels)  #Looks silly, but may get more evaluations in the future
    tier_section = f"{overall_SamplingTier}/{max_tier}"
    sampling_AdviceSection.tier = tier_section
    sampling_AdviceSection.pinchy_rating = overall_SamplingTier
    sampling_AdviceSection.groups = sampling_AdviceGroupDict.values()
    if overall_SamplingTier == max_tier:
        sampling_AdviceSection.header = f"Best Sampling tier met: {tier_section}<br>You best ❤️"
    else:
        sampling_AdviceSection.header = f"Best Sampling tier met: {tier_section}"
    return sampling_AdviceSection
