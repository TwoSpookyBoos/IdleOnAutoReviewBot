from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import caverns_cavern_names, max_cavern, max_schematics, max_majiks, break_you_best, max_engi_last_i_checked, \
    caverns_engineer_schematics_unlock_order, caverns_engineer_schematics

#villagers_progressionTiers,

logger = get_logger(__name__)

def getVillagersAdviceGroups():
    explorer_advice: []
    engineer_advice: {}
    conjuror_advice: {}
    measurer_advice: {}

def getExplorerAdviceGroup() -> AdviceGroup:
    explorer_advice = []
    polonai = session_data.account.caverns['Villagers']['Polonai']

    #Practical Max Level
    explorer_advice.append(Advice(
        label=polonai['Title'],
        picture_class='polonai',
        progression=polonai['Level'],
        goal=max_cavern
    ))
    #Invested Opals
    explorer_advice.append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=polonai['Opals'],
    ))

    for advice in explorer_advice:
        mark_advice_completed(advice)

    explorer_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- {polonai['Title']}",
        advices=explorer_advice,
        informational=True
    )
    return explorer_ag

def getMaxEngineerLevel() -> int:
    if max_schematics > (1 + (max_engi_last_i_checked * 3) + (max_engi_last_i_checked // 5)):
        needed_level = 0
        unlocked_schematics = 0
        while unlocked_schematics < max_schematics:
            needed_level += 1
            unlocked_schematics = 1 + (needed_level * 3) + (needed_level // 5)
        logger.warning(f"Update consts.max_engi_last_i_checked! {needed_level} is needed to unlock {max_schematics}")
        return needed_level
    else:
        return max_engi_last_i_checked


def getEngineerAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    s_stats = 'Schematic Stats'
    engineer_advice = {
        v_stats: [],
        s_stats: []
    }
    kaipu = session_data.account.caverns['Villagers']['Kaipu']
    unlocked_schematics = min(max_schematics, 1 + (kaipu['Level'] * 3) + (kaipu['Level'] // 5))
    max_engi_level_needed = getMaxEngineerLevel()

# Villager Stats
    # Practical Max Level
    engineer_advice[v_stats].append(Advice(
        label=kaipu['Title'],
        picture_class='kaipu',
        progression=kaipu['Level'],
        goal=max_engi_level_needed
    ))
    # Invested Opals
    engineer_advice[v_stats].append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=kaipu['Opals'],
    ))
# Schematic Stats
    engineer_advice[s_stats].append(Advice(
        label=f"Total Schematics unlocked by leveling Kaipu",
        picture_class='empty-schematic',
        progression=unlocked_schematics,
        goal=max_schematics
    ))
    engineer_advice[s_stats].append(Advice(
        label=f"Total Schematics purchased",
        picture_class='empty-schematic',
        progression=session_data.account.caverns['TotalSchematics'],
        goal=max_schematics
    ))
    if session_data.account.caverns['TotalSchematics'] < max_schematics:
        remaining_schematics = []
        for list_index, schematic_number in enumerate(caverns_engineer_schematics_unlock_order):
            clean_name = caverns_engineer_schematics[int(schematic_number)][0].replace("_", " ")
            schematic_details = session_data.account.caverns['Schematics'][clean_name]
            if not schematic_details['Purchased']:
                remaining_schematics.append(Advice(
                    label=f"Schematic {list_index+1}: {clean_name}: {schematic_details['Description']}",
                    picture_class=schematic_details['Image'],
                    progression=int(schematic_details['Purchased']),
                    goal=1,
                    resource=schematic_details['Resource']
                ))

    engineer_advice[s_stats].extend(remaining_schematics)
    for subgroup in engineer_advice:
        for advice in engineer_advice[subgroup]:
            mark_advice_completed(advice)

    engineer_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- {kaipu['Title']}",
        advices=engineer_advice,
        informational=True
    )
    return engineer_ag

def getConjurorAdviceGroup() -> AdviceGroup:
    v_stats = 'Villager Stats'
    h_m_stats = 'Hole Majik Stats'
    v_m_stats = 'Village Majik Stats'
    i_m_stats = 'IdleOn Majik Stats'
    conjuror_advice = {
        v_stats: [],
        h_m_stats: [],
        v_m_stats: [],
        i_m_stats: []
    }
    cosmos = session_data.account.caverns['Villagers']['Cosmos']
    earned_conjuror_points = session_data.account.gemshop['Conjuror Pts'] + cosmos['Level']
    spent_conjuror_points = 0
# Majiks
    for majik_name, majik_details in session_data.account.caverns['Majiks'].items():
        subgroup = f"{majik_details['MajikType']} Majik Stats"
        conjuror_advice[subgroup].append(Advice(
            label=f"{majik_name}: {majik_details['Description']}",
            picture_class=f"{majik_details['MajikType']}-majik-{'un' if majik_details['Level'] == 0 else ''}purchased",
            progression=majik_details['Level'],
            goal=majik_details['MaxLevel']
        ))
        spent_conjuror_points += majik_details['Level']

# Villager Stats
    # Practical Max Level
    conjuror_advice[v_stats].append(Advice(
        label=cosmos['Title'],
        picture_class='cosmos',
        progression=cosmos['Level'],
        goal=max_majiks - session_data.account.gemshop['Conjuror Pts']
    ))
    max_conjuror_pts = 12  # TODO Do I not have max levels stored somewhere for gemshop?
    conjuror_advice[v_stats].append(Advice(
        label=f"Up to {max_conjuror_pts} Conjuror Pts can be purchased from the Gem Shop",
        picture_class='conjuror-pts',
        progression=session_data.account.gemshop['Conjuror Pts'],
        goal=max_conjuror_pts
    ))
    if earned_conjuror_points > spent_conjuror_points < max_majiks:
        conjuror_advice[v_stats].append(Advice(
            label=f"You have {earned_conjuror_points-spent_conjuror_points} unspent Conjuror Pts!",
            picture_class='',
            progression=spent_conjuror_points,
            goal=earned_conjuror_points
        ))
    # Invested Opals
    conjuror_advice[v_stats].append(Advice(
        label="Opals Invested",
        picture_class='opal',
        progression=cosmos['Opals'],
    ))

    for subgroup in conjuror_advice:
        for advice in conjuror_advice[subgroup]:
            mark_advice_completed(advice)

    conjuror_ag = AdviceGroup(
        tier="",
        pre_string=f"Informational- {cosmos['Title']}",
        advices=conjuror_advice,
        informational=True
    )
    return conjuror_ag

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
    # highestVillagersSkillLevel = max(session_data.account.all_skills["VillagersSkill"])
    # if session_data.account. > 0:
    #     villagers_AdviceSection = AdviceSection(
    #         name="Villagers",
    #         tier="Not Yet Evaluated",
    #         header="Come back after unlocking Villagers!",
    #         picture="",
    #         unrated=False,
    #         unreached=True,
    #         completed=False
    #     )
    #     return villagers_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    villagers_AdviceGroupDict = {}
    villagers_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    villagers_AdviceGroupDict['Explorer'] = getExplorerAdviceGroup()
    villagers_AdviceGroupDict['Engineer'] = getEngineerAdviceGroup()
    villagers_AdviceGroupDict['Conjuror'] = getConjurorAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    villagers_AdviceSection = AdviceSection(
        name="Villagers",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header="Villager Information",  #f"Best Villagers tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="",
        groups=villagers_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
        informational=True
    )

    return villagers_AdviceSection
