from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    caverns_cavern_names, max_cavern,
    caverns_villagers, getMaxEngineerLevel, caverns_engineer_schematics, caverns_engineer_schematics_unlock_order,
    max_schematics,
    max_majiks,
    max_measurements,
    break_you_best, infinity_string, released_schematics, total_placeholder_majiks, stamp_maxes
)

#villagers_progressionTiers,

logger = get_logger(__name__)

def getVillagersAdviceGroups():
    villager_ags = {
        'Explorer': getExplorerAdviceGroup(),
        'Engineer': getEngineerAdviceGroup(),
        'Conjuror': getConjurorAdviceGroup(),
        'Measurer': getMeasurerAdviceGroup(),
        'Librarian': getLibrarianAdviceGroup()
    }
    return villager_ags

def getExplorerAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    c_stats = 'Cavern Unlock Status'
    v_u_stats = 'Villager Unlock Status'
    villager_advice = {
        v_stats: []
    }

    villager_name = 'Polonai'
    villager = session_data.account.caverns['Villagers'][villager_name]

    # Generate Alert
    if villager['LevelPercent'] >= 100:
        session_data.account.alerts_AdviceDict['The Caverns Below'].append(Advice(
            label=f"{{{{ Polonai|#villagers }}}} ready to level!",
            picture_class=villager_name
        ))

# Villager Stats
    #Practical Max Level
    villager_advice[v_stats].append(Advice(
        label=f"{villager['Title']} level for all implemented unlocks",
        picture_class=villager_name,
        progression=villager['Level'],
        goal=max_cavern
    ))
    villager_advice[v_stats].append(Advice(
        label="Next level progress",
        picture_class=villager_name,
        progression=f"{villager['LevelPercent']:.1f}",
        goal=100,
        unit='%'
    ))
    #Invested Opals
    villager_advice[v_stats].append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=villager['Opals'],
    ))
# Cavern Unlocks
    if villager['Level'] < max_cavern:
        villager_advice[c_stats] = [
            Advice(
                label=f"Discover Cavern {session_data.account.caverns['Caverns'][cavern_name]['CavernNumber']}- {cavern_name}",
                picture_class=session_data.account.caverns['Caverns'][cavern_name]['Image'],
                progression=villager['Level'],
                goal=session_data.account.caverns['Caverns'][cavern_name]['CavernNumber']
            )
            for cavern_name in session_data.account.caverns['Caverns'] if not session_data.account.caverns['Caverns'][cavern_name]['Unlocked']
        ]
# Villager Unlocks
    if not session_data.account.caverns['Villagers'][caverns_villagers[-1]['Name']]['Unlocked']:
        villager_advice[v_u_stats] = [
            Advice(
                label=f"Discover Villager {villager_details['VillagerNumber']}- {villager_details['Title']} at Cavern {villager_details['UnlockedCavern']}",
                picture_class=f"{villager_name}-undiscovered",
                progression=villager['Level'],
                goal=villager_details['UnlockedCavern']
            )
            for villager_name, villager_details in session_data.account.caverns['Villagers'].items() if not villager_details['Unlocked']
        ]

    for subgroup in villager_advice:
        for advice in villager_advice[subgroup]:
            mark_advice_completed(advice)

    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- Level {villager['Level']} {villager['Title']}",
        advices=villager_advice,
        informational=True,
        completed=villager['Level'] >= max_cavern
    )
    return villager_ag

def getEngineerAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    s_stats = 'Schematic Stats'
    unpurchased_stats = 'Unpurchased Schematics'
    unreleased_schematics = 'Unreleased Schematics'
    villager_advice = {
        v_stats: [],
        s_stats: [],
        unpurchased_stats: [],
        unreleased_schematics: []
    }

    villager_name = 'Kaipu'
    villager = session_data.account.caverns['Villagers'][villager_name]
    unlocked_schematics = min(max_schematics, 1 + (villager['Level'] * 3) + (villager['Level'] // 5))
    max_engi_level_needed = getMaxEngineerLevel()

    # Generate Alert
    if villager['LevelPercent'] >= 100:
        session_data.account.alerts_AdviceDict['The Caverns Below'].append(Advice(
            label=f"{{{{ Kaipu|#villagers }}}} ready to level!",
            picture_class=villager_name
        ))

# Villager Stats
    # Practical Max Level
    villager_advice[v_stats].append(Advice(
        label=f"{villager['Title']} level for all implemented unlocks",
        picture_class=villager_name,
        progression=villager['Level'],
        goal=max_engi_level_needed
    ))
    villager_advice[v_stats].append(Advice(
        label="Next level progress",
        picture_class=villager_name,
        progression=f"{villager['LevelPercent']:.1f}",
        goal=100,
        unit='%'
    ))
    # Invested Opals
    villager_advice[v_stats].append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=villager['Opals'],
    ))
# Schematic Stats
    villager_advice[s_stats].append(Advice(
        label=f"Total Schematics unlocked by leveling Kaipu",
        picture_class='empty-schematic',
        progression=unlocked_schematics,
        goal=released_schematics
    ))
    villager_advice[s_stats].append(Advice(
        label=f"Total Schematics purchased",
        picture_class='empty-schematic',
        progression=session_data.account.caverns['TotalSchematics'],
        goal=released_schematics
    ))
    if session_data.account.caverns['TotalSchematics'] < max_schematics:
        for list_index, schematic_number in enumerate(caverns_engineer_schematics_unlock_order):
            clean_name = caverns_engineer_schematics[int(schematic_number)][0].replace("_", " ")
            schematic_details = session_data.account.caverns['Schematics'][clean_name]
            if not schematic_details['Purchased']:
                villager_advice[unreleased_schematics if list_index+1 > released_schematics else unpurchased_stats].append(Advice(
                    label=f"Schematic {list_index+1}: {clean_name}- {schematic_details['Description']}",
                    picture_class=schematic_details['Image'],
                    progression=int(schematic_details['Purchased']),
                    goal=1,
                    resource=schematic_details['Resource']
                ))
            # else:  #uncomment this chunk for testing, if you need to see them all
            #     villager_advice[unpurchased_stats].append(Advice(
            #         label=f"Schematic {list_index + 1}: {clean_name}: {schematic_details['Description']}",
            #         picture_class=schematic_details['Image'],
            #         progression=int(schematic_details['Purchased']),
            #         goal=1,
            #         resource=schematic_details['Resource']
            #     ))

    for subgroup in villager_advice:
        for advice in villager_advice[subgroup]:
            mark_advice_completed(advice)

    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- Level {villager['Level']} {villager['Title']}",
        advices=villager_advice,
        informational=True,
        completed=session_data.account.caverns['TotalSchematics'] >= released_schematics
    )
    villager_ag.remove_empty_subgroups()
    return villager_ag

def getConjurorAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    h_m_stats = 'Hole Majik Stats'
    v_m_stats = 'Village Majik Stats'
    i_m_stats = 'IdleOn Majik Stats'
    villager_advice = {
        v_stats: [],
        h_m_stats: [],
        v_m_stats: [],
        i_m_stats: []
    }

    villager_name = 'Cosmos'
    villager = session_data.account.caverns['Villagers'][villager_name]
    earned_conjuror_points = session_data.account.gemshop['Conjuror Pts'] + villager['Level']
    spent_conjuror_points = session_data.account.caverns['TotalMajiks']

    #Generate Alert
    if villager['LevelPercent'] >= 100:
        session_data.account.alerts_AdviceDict['The Caverns Below'].append(Advice(
            label=f"{{{{ Cosmos|#villagers }}}} ready to level!",
            picture_class=villager_name
        ))

# Majiks
    for majik_name, majik_details in session_data.account.caverns['Majiks'].items():
        subgroup = f"{majik_details['MajikType']} Majik Stats"
        villager_advice[subgroup].append(Advice(
            label=f"{majik_name}: {majik_details['Description']}",
            picture_class=f"{majik_details['MajikType']}-majik-{'un' if majik_details['Level'] == 0 else ''}purchased",
            progression=majik_details['Level'],
            goal=majik_details['MaxLevel']
        ))

# Villager Stats
    # Practical Max Level
    villager_advice[v_stats].append(Advice(
        label=f"{villager['Title']} level for all implemented unlocks",
        picture_class=villager_name,
        progression=villager['Level'],
        goal=max_majiks - total_placeholder_majiks - session_data.account.gemshop['Conjuror Pts']
    ))
    villager_advice[v_stats].append(Advice(
        label="Next level progress",
        picture_class=villager_name,
        progression=f"{villager['LevelPercent']:.1f}",
        goal=100,
        unit='%'
    ))
    max_conjuror_pts = 12  # TODO Do I not have max levels stored somewhere for gemshop?
    villager_advice[v_stats].append(Advice(
        label=f"Up to {max_conjuror_pts} Conjuror Pts can be purchased from the Gem Shop",
        picture_class='conjuror-pts',
        progression=session_data.account.gemshop['Conjuror Pts'],
        goal=max_conjuror_pts
    ))
    if earned_conjuror_points > spent_conjuror_points < max_majiks:
        unspent_pts_advice = Advice(
            label=f"You have {earned_conjuror_points-spent_conjuror_points} unspent {{{{Conjuror Pts|#villagers}}}}!",
            picture_class='',
            progression=spent_conjuror_points,
            goal=earned_conjuror_points
        )
        villager_advice[v_stats].append(unspent_pts_advice)
        if villager['Unlocked']:
            session_data.account.alerts_AdviceDict['The Caverns Below'].append(unspent_pts_advice)
    # Invested Opals
    villager_advice[v_stats].append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=villager['Opals'],
    ))

    for subgroup in villager_advice:
        for advice in villager_advice[subgroup]:
            mark_advice_completed(advice)

    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- Level {villager['Level']} {villager['Title']}",
        advices=villager_advice,
        informational=True,
        completed=villager['Level'] >= max_majiks - total_placeholder_majiks - session_data.account.gemshop['Conjuror Pts']
    )
    return villager_ag

def getMeasurerAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    m_stats = 'Measurement Stats'
    villager_advice = {
        v_stats: [],
        m_stats: [],
    }

    villager_name = 'Minau'
    villager = session_data.account.caverns['Villagers'][villager_name]
    measurements = session_data.account.caverns['Measurements']

    # Generate Alert
    if villager['LevelPercent'] >= 100:
        session_data.account.alerts_AdviceDict['The Caverns Below'].append(Advice(
            label=f"{{{{ Minau|#villagers }}}} ready to level!",
            picture_class=villager_name
        ))

# Villager Stats
    # Practical Max Level
    villager_advice[v_stats].append(Advice(
        label=f"{villager['Title']} level for all implemented unlocks",
        picture_class=villager_name,
        progression=villager['Level'],
        goal=max_measurements
    ))
    villager_advice[v_stats].append(Advice(
        label="Next level progress",
        picture_class=villager_name,
        progression=f"{villager['LevelPercent']:.1f}",
        goal=100,
        unit='%'
    ))
    # Invested Opals
    villager_advice[v_stats].append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=villager['Opals'],
    ))
# Measurement Stats
    villager_advice[m_stats] = []
    for measurement_name, measurement_details in measurements.items():
        if measurement_name != 'i' and max_measurements >= measurement_details['MeasurementNumber']:
            if measurement_details['TOT']:
                villager_advice[m_stats].append(Advice(
                    label=(
                        f"{measurement_details['Level']} {measurement_details['Unit']}: "
                        f"+{measurement_details['TotalBaseValue']:.2f}% {measurement_details['Description']}"
                        f"<br>Scales with: {measurement_details['ScalesWith']}"
                    ),
                    picture_class=measurement_details['Image'],
                    progression=f"{(measurement_details['BaseValue'] / measurement_details['HI55']) * 100:.2f}",
                    goal='100',
                    resource=measurement_details['Resource'],
                    unit='%'
                ))
            else:
                villager_advice[m_stats].append(Advice(
                    label=(
                        f"{measurement_details['Level']} {measurement_details['Unit']}: "
                        f"+{measurement_details['TotalBaseValue']:.0f}% {measurement_details['Description']}"
                        f"<br>Scales with: {measurement_details['ScalesWith']}"
                    ),
                    picture_class=measurement_details['Image'],
                    progression='Linear',
                    goal=infinity_string,
                    resource=measurement_details['Resource']
                ))

    for subgroup in villager_advice:
        for advice in villager_advice[subgroup]:
            mark_advice_completed(advice)

    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- Level {villager['Level']} {villager['Title']}",
        advices=villager_advice,
        informational=True,
        completed=villager['Level'] >= max_measurements
    )
    return villager_ag

def getLibrarianAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    speed_stats = 'Study Speed Sources'
    study_stats = 'Study Stats'
    villager_advice = {
        v_stats: [],
        speed_stats: [],
        study_stats: [],
    }

    villager_name = 'Bolaia'
    villager = session_data.account.caverns['Villagers'][villager_name]
    studies = session_data.account.caverns['Studies']
    schematics = session_data.account.caverns['Schematics']
    majiks = session_data.account.caverns['Majiks']

    # Generate Alert
    if villager['LevelPercent'] >= 100:
        session_data.account.alerts_AdviceDict['The Caverns Below'].append(Advice(
            label=f"{{{{ Bolaia|#villagers }}}} ready to level!",
            picture_class=villager_name
        ))

# Villager Stats
    # Practical Max Level
    villager_advice[v_stats].append(Advice(
        label=f"{villager['Title']} level for all implemented unlocks",
        picture_class=villager_name,
        progression=villager['Level'],
        #goal=
    ))
    villager_advice[v_stats].append(Advice(
        label="Next level progress",
        picture_class=villager_name,
        progression=f"{villager['LevelPercent']:.1f}",
        goal=100,
        unit='%'
    ))
    # Invested Opals
    villager_advice[v_stats].append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=villager['Opals'],
    ))

# Study Speed Sources
    total_base_speed = 5
    max_base_speed = 5
    villager_advice[speed_stats].append(Advice(
        label=f"Base study speed: 100 + 5/sec per level",
        picture_class=villager_name,
        progression=1,
        goal=1
    ))
    for schematic_name, speed_boost in {
        'Peer Reviewed Books': 2,
        'Cutting Edge Research': 3,
        'Billion Dollar Grant': 5
    }.items():
        villager_advice[speed_stats].append(Advice(
            label=f"Schematic {schematics[schematic_name]['UnlockOrder']}: {schematic_name}"
                  f"<br>+{speed_boost}/sec per level",
            picture_class=schematics[schematic_name]['Image'],
            progression=int(schematics[schematic_name]['Purchased']),
            goal=1,
            resource=schematics[schematic_name]['Resource'] if not schematics[schematic_name]['Purchased'] else ''
        ))
        total_base_speed += speed_boost * int(schematics[schematic_name]['Purchased'])
        max_base_speed += speed_boost
    villager_advice[speed_stats].append(Advice(
        label=f"Total Base: {100 + total_base_speed}/sec per level",
        picture_class=villager_name,
        progression=total_base_speed,
        goal=max_base_speed
    ))
    rosemerald = session_data.account.caverns['Collectibles']['Rosemerald']
    villager_advice[speed_stats].append(Advice(
        label=f"Group B: Collectible: Rosemerald: +{rosemerald['Value']:.0f}%",
        picture_class=rosemerald['Image'],
        progression=rosemerald['Level'],
        goal=infinity_string
    ))
    villager_advice[speed_stats].append(Advice(
        label=f"Group B: Study All Nighter Majik: {majiks['Study All Nighter']['Description']}",
        picture_class=f"{majiks['Study All Nighter']['MajikType']}-majik-{'un' if majiks['Study All Nighter']['Level'] == 0 else ''}purchased",
        progression=majiks['Study All Nighter']['Level'],
        goal=majiks['Study All Nighter']['MaxLevel']
    ))
    villager_advice[speed_stats].append(Advice(
        label=f"Group B: Study Hall {{{{ Stamp|#stamps }}}}: +{session_data.account.stamps['Study Hall Stamp']['Value']:.2f}%",
        picture_class='study-hall-stamp',
        progression=session_data.account.stamps['Study Hall Stamp']['Level'],
        goal=stamp_maxes['Study Hall Stamp']
    ))


# Study Stats
    for study_index, study_details in studies.items():
        villager_advice[study_stats].append(Advice(
            label=f"{study_details['CavernName']}: {study_details['Description']}",
            picture_class=f"cavern-{study_details['CavernNumber']}",
            progression=study_details['Level'],
            goal=study_details['MaxLevel']
        ))

    for subgroup in villager_advice:
        for advice in villager_advice[subgroup]:
            mark_advice_completed(advice)

    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- Level {villager['Level']} {villager['Title']}",
        advices=villager_advice,
        informational=True,
        completed=villager['Level'] >= max_measurements
    )
    return villager_ag

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    villagers_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0  #max(villagers_progressionTiers.keys(), default=0) - info_tiers
    tier_Villagers = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Villagers,
        pre_string="Progression Tiers",
        advices=villagers_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Villagers)
    return tiers_ag, overall_SectionTier, max_tier, max_tier + info_tiers

def getVillagersAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.caverns['Villagers']['Polonai']['Level'] < 1:
        villagers_AdviceSection = AdviceSection(
            name="Villagers",
            tier="Not Yet Evaluated",
            header="Come back after unlocking The Caverns Below in W5!",
            picture='wiki/Hole_Campfire.gif',
            unrated=False,
            unreached=True,
            completed=False
        )
        return villagers_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    villagers_AdviceGroupDict = {}
    villagers_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    villagers_AdviceGroupDict.update(getVillagersAdviceGroups())

    for ag in villagers_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    villagers_AdviceSection = AdviceSection(
        name="Villagers",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header="Villager Information",  #f"Best Villagers tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='wiki/Hole_Campfire.gif',
        groups=villagers_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
        informational=True
    )

    return villagers_AdviceSection
