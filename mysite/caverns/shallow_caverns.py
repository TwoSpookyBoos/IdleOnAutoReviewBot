from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    caverns_cavern_names,
    break_you_best, schematics_unlocking_buckets, sediment_names,
    # shallow_caverns_progressionTiers
)

logger = get_logger(__name__)

def getTemplateCavernAdviceGroup() -> AdviceGroup:
    c_stats = "Cavern Stats"
    cavern_advice = {
        c_stats: []
    }

    cavern_name = 'The Template'
    cavern = session_data.account.caverns[cavern_name]

    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
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
    sediments = session_data.account.caverns['Caverns'][cavern_name]['SedimentsOwned']
    schematics = session_data.account.caverns['Schematics']

    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Next Opal trade TBD",
        picture_class='',
        resource='well-sediment-0'
    ))

    # if cavern['BucketsUnlocked'] >= max_buckets:
    #     pass
    # else:
    for bucket_index, bucket_target in enumerate(buckets):
        cavern_advice[b_stats].append(Advice(
            label=(
                f"Bucket {bucket_index+1}: {'Collecting' if sediments[bucket_target-1] > 0 else 'Unlocking next sediment'}"
                f" {sediment_names[bucket_target] if sediments[bucket_target-1] > 0 else ''}"
                if bucket_target > 0 else
                f"Unlock Bucket {bucket_index+1} by purchasing <br>"
                f"Schematic {schematics[schematics_unlocking_buckets[bucket_index-1]]['UnlockOrder']}:"
                f" {schematics_unlocking_buckets[bucket_index-1]}"
            ),
            picture_class=f"well-sediment-{bucket_target}" if bucket_target > 0 else schematics[schematics_unlocking_buckets[bucket_index-1]]['Image'],
            resource='' if bucket_target > 0 else schematics[schematics_unlocking_buckets[bucket_index-1]]['Resource']
        ))

    cavern_advice[s_stats].append(Advice(
        label="Sediments WIP :D",
        picture_class=''
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Informational- {cavern_name}",
        advices=cavern_advice,
        informational=True,
        picture_class='cavern-1'
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
