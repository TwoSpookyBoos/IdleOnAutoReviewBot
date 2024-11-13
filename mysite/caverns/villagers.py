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
    break_you_best, infinity_string
)

#villagers_progressionTiers,

logger = get_logger(__name__)

def getVillagersAdviceGroups():
    villager_ags = {
        'Explorer': getExplorerAdviceGroup(),
        'Engineer': getEngineerAdviceGroup(),
        'Conjuror': getConjurorAdviceGroup(),
        'Measurer': getMeasurerAdviceGroup()
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
        label=f"{villager['Title']} level for all unlocks",
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
                label=f"Discover Cavern {session_data.account.caverns['Caverns'][cavern_name]['CavernNumber']}",
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
                label=f"Discover Villager {villager_details['VillagerNumber']} at Cavern {villager_details['UnlockedCavern']}",
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
        informational=True
    )
    return villager_ag

def getEngineerAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    s_stats = 'Schematic Stats'
    r_s_stats = 'Unpurchased Schematics'
    villager_advice = {
        v_stats: [],
        s_stats: [],
        r_s_stats: []
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
        label=f"{villager['Title']} level for all unlocks",
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
        goal=max_schematics
    ))
    villager_advice[s_stats].append(Advice(
        label=f"Total Schematics purchased",
        picture_class='empty-schematic',
        progression=session_data.account.caverns['TotalSchematics'],
        goal=max_schematics
    ))
    if session_data.account.caverns['TotalSchematics'] < max_schematics:
        for list_index, schematic_number in enumerate(caverns_engineer_schematics_unlock_order):
            clean_name = caverns_engineer_schematics[int(schematic_number)][0].replace("_", " ")
            schematic_details = session_data.account.caverns['Schematics'][clean_name]
            if not schematic_details['Purchased']:
                villager_advice[r_s_stats].append(Advice(
                    label=f"Schematic {list_index+1}: {clean_name}",  #{schematic_details['Description']}",
                    picture_class=schematic_details['Image'],
                    progression=int(schematic_details['Purchased']),
                    goal=1,
                    resource=schematic_details['Resource']
                ))
            # else:  #uncomment this chunk for testing, if you need to see them all
            #     villager_advice[r_s_stats].append(Advice(
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
        informational=True
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
        label=f"{villager['Title']} level for all unlocks",
        picture_class=villager_name,
        progression=villager['Level'],
        goal=max_majiks - session_data.account.gemshop['Conjuror Pts']
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
        villager_advice[v_stats].append(Advice(
            label=f"You have {earned_conjuror_points-spent_conjuror_points} unspent Conjuror Pts!",
            picture_class='',
            progression=spent_conjuror_points,
            goal=earned_conjuror_points
        ))
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
        informational=True
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
        label=f"{villager['Title']} level for all unlocks",
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
    villager_advice[m_stats] = [
        Advice(
            label=(
                f"{measurement_details['Level']} {measurement_details['Unit']}: {measurement_details['Description']}"
                f"<br>Scales with: {measurement_details['ScalesWith']}"
                if villager['Level'] >= measurement_details['MeasurementNumber']
                else f"Unlock {measurement_details['Unit']} by leveling Minau"
            ),
            picture_class=measurement_details['Image'],
            progression=measurement_details['Level'] if villager['Level'] >= measurement_details['MeasurementNumber'] else villager['Level'],
            goal=infinity_string if villager['Level'] >= measurement_details['MeasurementNumber'] else measurement_details['MeasurementNumber'],
            resource=measurement_details['Resource']
        )
        for measurement_name, measurement_details in measurements.items() if measurement_name != 'i' and max_measurements >= measurement_details['MeasurementNumber']
    ]

    for subgroup in villager_advice:
        for advice in villager_advice[subgroup]:
            mark_advice_completed(advice)

    villager_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- Level {villager['Level']} {villager['Title']}",
        advices=villager_advice,
        informational=True
    )
    return villager_ag

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
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
    return tiers_ag, overall_SectionTier, max_tier

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
    villagers_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    villagers_AdviceGroupDict.update(getVillagersAdviceGroups())

    for ag in villagers_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    villagers_AdviceSection = AdviceSection(
        name="Villagers",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header="Villager Information",  #f"Best Villagers tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='wiki/Hole_Campfire.gif',
        groups=villagers_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
        informational=True
    )

    return villagers_AdviceSection
