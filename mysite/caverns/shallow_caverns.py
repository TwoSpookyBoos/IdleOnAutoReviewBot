from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    caverns_cavern_names,
    break_you_best, schematics_unlocking_buckets, sediment_names, max_sediments, getSedimentBarRequirement, getWellOpalTrade, getMotherlodeEfficiencyRequired,
    getMotherlodeResourceRequired,
    # shallow_caverns_progressionTiers
)
from utils.text_formatting import pl, notateNumber

logger = get_logger(__name__)

def getTemplateCavernAdviceGroup() -> AdviceGroup:
    c_stats = "Cavern Stats"
    cavern_advice = {
        c_stats: []
    }

    cavern_name = 'The Template'
    cavern = session_data.account.caverns['Caverns'][cavern_name]

    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name if cavern['Unlocked'] else 'To Be Discovered!'}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getWellAdviceGroup() -> AdviceGroup:
    c_stats = "Cavern Stats"
    b_stats = "Bucket Stats"
    s_stats = "Sediment Stats"
    cavern_advice = {
        c_stats: [],
        b_stats: [],
        s_stats: [],
    }

    cavern_name = 'The Well'
    cavern = session_data.account.caverns['Caverns'][cavern_name]
    buckets = session_data.account.caverns['Caverns'][cavern_name]['BucketTargets']
    sediments_owned = session_data.account.caverns['Caverns'][cavern_name]['SedimentsOwned']
    sediment_levels = session_data.account.caverns['Caverns'][cavern_name]['SedimentLevels']
    schematics = session_data.account.caverns['Schematics']

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Use buckets to collect Sediment",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
    opal_trade_cost = getWellOpalTrade(cavern['Holes-11-9'])
    #opal_trades_list = [notateNumber('Basic', getWellOpalTrade(i), 1) for i in range(0, 100)]
    opal_trade_progress = 100 * (sediments_owned[0] / opal_trade_cost)
    cavern_advice[c_stats].append(Advice(
        label=f"Next Opal trade: {notateNumber('Basic', opal_trade_cost, 2)} Gravel",
        picture_class='bucketlyte',
        resource='well-sediment-0',
        progression=f"{opal_trade_progress:.1f}",
        goal=100,
        unit='%'
    ))

# Bucket Stats
    # if cavern['BucketsUnlocked'] >= max_buckets:
    #     pass
    # else:
    for bucket_index, bucket_target in enumerate(buckets):
        cavern_advice[b_stats].append(Advice(
            label=(
                f"Bucket {bucket_index+1}: {'Collecting' if sediments_owned[bucket_target-1] > 0 else 'Unlocking next sediment'}"
                f" {sediment_names[bucket_target] if sediments_owned[bucket_target-1] > 0 else ''}"
                if bucket_index + 1 <= cavern['BucketsUnlocked'] else
                f"Unlock Bucket {bucket_index+1} by purchasing <br>"
                f"Schematic {schematics[schematics_unlocking_buckets[bucket_index-1]]['UnlockOrder']}:"
                f" {schematics_unlocking_buckets[bucket_index-1]}"
            ),
            picture_class=f"well-sediment-{bucket_target}" if bucket_index + 1 <= cavern['BucketsUnlocked'] else schematics[schematics_unlocking_buckets[bucket_index-1]]['Image'],
            resource='' if bucket_index + 1 <= cavern['BucketsUnlocked'] else schematics[schematics_unlocking_buckets[bucket_index-1]]['Resource']
        ))

    cavern_advice[s_stats] = [
        Advice(
            label=(
                f"{sediment_names[sediment_index]}'s bar has been expanded {sediment_levels[sediment_index]} times"
                f"<br>{sediment_value:,} owned"
                f"<br>{getSedimentBarRequirement(sediment_index, sediment_levels[sediment_index]):,.0f} required to expand the bar"
                if sediment_value >= 0 else
                f"Clear the rock layer to discover this Sediment!"
            ),
            picture_class=f"well-sediment-{sediment_index}",
            resource='well-sediment-rock-layer' if sediment_value < 0 else '',
            progression=0 if sediment_value < 0 else f"{100 * (sediment_value / getSedimentBarRequirement(sediment_index, sediment_levels[sediment_index])):.1f}",
            goal=100,
            unit='%'
        )
        for sediment_index, sediment_value in enumerate(sediments_owned) if sediment_index < max_sediments
        # There are lots of placeholders in sediments_owned, so stay within bounds of max_sediments
    ]
    cavern_advice[s_stats].insert(0, Advice(
        label=f"Expand Full Bars: {'On' if session_data.account.caverns['Caverns']['The Well']['BarExpansion'] else 'Off'}",
        picture_class='engineer-schematic-13'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name if cavern['Unlocked'] else 'To Be Discovered!'}",
        advices=cavern_advice,
        informational=True,
        picture_class='cavern-1'
    )
    return cavern_ag

def getMotherlodeAdviceGroup():
    c_stats = "Cavern Stats"
    l_stats = 'Layer Stats'
    cavern_advice = {
        c_stats: [],
        l_stats: []
    }

    cavern_name = 'Motherlode'
    resource_type = 'Ore'
    resource_skill = 'Mining'
    cavern = session_data.account.caverns['Caverns'][cavern_name]
# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Use your characters to mine up Ore and break Layers",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

# Layer Stats
    cavern_advice[l_stats].append(Advice(
        label=f"Layer {cavern['LayersDestroyed']+1} {resource_skill} Efficiency Required:"
              f"{notateNumber('Basic', getMotherlodeEfficiencyRequired(cavern['LayersDestroyed']), 1)}",
        picture_class=resource_skill
    ))
    resource_required = getMotherlodeResourceRequired(cavern['LayersDestroyed'])
    cavern_advice[l_stats].append(Advice(
        label=f"{resource_type} remaining to break Layer {cavern['LayersDestroyed'] + 1}: {notateNumber('Basic', resource_required - cavern['ResourcesCollected'], 1)}",
        picture_class=f'motherlode-{resource_type}',
        progression=f"{min(100, 100 * (cavern['ResourcesCollected'] / resource_required)):.1f}",
        goal=100,
        unit='%'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name if cavern['Unlocked'] else 'To Be Discovered!'}",
        advices=cavern_advice,
        informational=True,
        picture_class='cavern-2'
    )
    return cavern_ag

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    shallow_caverns_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0  #max(shallow_caverns_progressionTiers.keys(), default=0) - info_tiers
    tier_Shallow_Caverns = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Shallow_Caverns,
        pre_string="Progression Tiers",
        advices=shallow_caverns_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Shallow_Caverns)
    return tiers_ag, overall_SectionTier, max_tier



def getShallowCavernsAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.caverns['Villagers']['Polonai']['Level'] < 1:
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
    shallow_caverns_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    shallow_caverns_AdviceGroupDict['The Well'] = getWellAdviceGroup()
    shallow_caverns_AdviceGroupDict['Motherlode'] = getMotherlodeAdviceGroup()

    for ag in shallow_caverns_AdviceGroupDict.values():
        ag.remove_empty_subgroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    shallow_caverns_AdviceSection = AdviceSection(
        name="Shallow Caverns",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"The Shallow Caverns biome",  #f"Best Shallow Caverns tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Shallow_Caverns.png',
        groups=shallow_caverns_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return shallow_caverns_AdviceSection
