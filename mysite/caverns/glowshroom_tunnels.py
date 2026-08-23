from consts.progression_tiers import true_max_tiers

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data
from utils.logging import get_logger

# from consts.consts import glowshroom_tunnels_progressionTiers, break_you_best, ValueToMulti
from consts.consts_caverns import caverns_cavern_names
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getHarpAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['The Harp']
    cavern_ag = AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag

def getLampAdviceGroup():
    c_stats = "Cavern Stats"
    c_faqs = "FAQs"
    w_stats = "Wish Type Stats"
    cavern_advice = {
        c_stats: [],
        c_faqs: [],
        w_stats: [],
    }

    cavern_name = caverns_cavern_names[7]
    cavern = session_data.account.caverns['Caverns'][cavern_name]
# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Collect Wishes upon Daily Reset to invest into Wish Types",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='lamp-wish-button'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

# Cavern FAQs
    cavern_advice[c_faqs].append(Advice(
        label=f"Gold Pocketwatches DO NOT grant Wishes!"
              f"<br>Silver Pocketwatches do.",
        picture_class='gold-pocketwatch',
        resource='silver-pocketwatch'
    ))

# Wish Type Stats
    cavern_advice[w_stats] = [
        Advice(
            label=f"Level {wish_details['Level']} {wish_details['Name']}: {wish_details['Description']}",
            picture_class=wish_details['Image'],
            progression=cavern['WishesStored'],
            goal=wish_details['NextCost']
        ) for wish_index, wish_details in cavern['WishTypes'].items()
    ]
    cavern_advice[w_stats].insert(0, Advice(
        label=f"Wishes stored: {cavern['WishesStored']}",
        picture_class='lamp-wish-button'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getHiveAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['The Hive']
    return AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True,
    )

def getGrottoAdviceGroup():
    c_stats = "Cavern Stats"
    c_faqs = "FAQs"
    l_stats = "Colony Stats"
    cavern_advice = {
        c_stats: [],
        c_faqs: [],
        l_stats: []
    }

    cavern_name = caverns_cavern_names[9]
    cavern = session_data.account.caverns['Caverns'][cavern_name]
# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Opal Objective- Kill enough Gloomie Mushrooms to summon and defeat a Monarch.",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='gloomie-mushroom'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Bonus Objective- Collect Villager {{{{Statues|#statues}}}} from AFK kills.",
        picture_class='villager-statue',
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

# FAQs
    cavern_advice[c_faqs].append(Advice(
        label=f"Mushroom HP does NOT increase after defeating a Monarch."
              f"<br>The number of kills required and the Monarch's HP will increase.",
        picture_class='gloomie-mushroom'
    ))
    cavern_advice[c_faqs].append(Advice(
        label=f"Statues from Active kills don't have their quantity multiplied by Multikill. Farm them AFK instead."
              f"<br>Statues cannot be sampled.",
        picture_class='villager-statue'
    ))
    # cavern_advice[c_faqs].append(Advice(
    #     label=f"Standard Monster Respawn% does NOT work in this Cavern. Focus on increasing Multikill and Combat AFK%.",
    #     picture_class='undead-shrine'
    # ))

# Layer/Colony Stats
    target_string = notateNumber('Basic', cavern['KillsRequired'], 2)
    current_string = notateNumber('Match', cavern['PlayerKills'], 2, matchString=target_string)
    cavern_advice[l_stats].append(Advice(
        label=f"Kills before Monarch: {notateNumber('Basic', cavern['KillsRemaining'], 2)}",
        picture_class='gloomie-mushroom',
        progression=current_string,
        goal=target_string
    ))
    if cavern['PercentRemaining'] <= 1:
        session_data.account.alerts_Advices['The Caverns Below'].append(Advice(
            label=f"Challenge {{{{ The Monarch|#glowshroom-tunnels }}}}!",
            picture_class='gloomie-mushroom'
        ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getJusticeAdviceGroup() -> AdviceGroup:
    cavern = session_data.account.caverns_.caves['Justice Monument']
    cavern_ag = AdviceGroup(
        tier='',
        pre_string=cavern.pre_string(),
        advices=cavern.advice_groups(),
        informational=True
    )
    cavern_ag.mark_advice_completed()
    return cavern_ag

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    glowshroom_tunnels_AdviceDict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Glowshroom Tunnels']
    max_tier = true_max - optional_tiers
    tier_Glowshroom_Tunnels = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Glowshroom_Tunnels,
        pre_string="Progression Tiers",
        advices=glowshroom_tunnels_AdviceDict['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Glowshroom_Tunnels)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getGlowshroomTunnelsAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.caverns_.villagers["Polonai"].level < 6:
        glowshroom_tunnels_AdviceSection = AdviceSection(
            name="Glowshroom Tunnels",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Cavern 6+ in W5!",
            picture='Glowshroom_Tunnels.png',
            unrated=True,
            unreached=True,
            completed=False
        )
        return glowshroom_tunnels_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    glowshroom_tunnels_AdviceGroupDict = {}
    glowshroom_tunnels_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict['The Harp'] = getHarpAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict['The Lamp'] = getLampAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict['The Hive'] = getHiveAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict['Grotto'] = getGrottoAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict['Justice Monument'] = getJusticeAdviceGroup()

    for ag in glowshroom_tunnels_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    glowshroom_tunnels_AdviceSection = AdviceSection(
        name='Glowshroom Tunnels',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"The Glowshroom Tunnels biome",  #f"Best Glowshroom Tunnels tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Glowshroom_Tunnels.png',
        groups=glowshroom_tunnels_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return glowshroom_tunnels_AdviceSection
