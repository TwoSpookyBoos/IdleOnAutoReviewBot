from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    caverns_cavern_names,
    break_you_best,
    schematics_unlocking_buckets, sediment_names, max_sediments, getSedimentBarRequirement, getWellOpalTrade, getMotherlodeEfficiencyRequired,
    getMotherlodeResourceRequired, getDenOpalRequirement, schematics_unlocking_amplifiers, getBraveryOpalChance, monument_layer_rewards, getBellExpRequired,
    getBellImprovementBonus, infinity_string
    # shallow_caverns_progressionTiers
)
from utils.text_formatting import pl, notateNumber

logger = get_logger(__name__)

def getTemplateCavernAdviceGroup(schematics) -> AdviceGroup:
    c_stats = "Cavern Stats"
    cavern_advice = {
        c_stats: []
    }

    cavern_name = 'The Template'
    cavern = session_data.account.caverns['Caverns'][cavern_name]
# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- ",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
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

def getWellAdviceGroup(schematics) -> AdviceGroup:
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

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Use buckets to collect Sediment",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='well-bucket',
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
        progression=f"{min(100,opal_trade_progress):.1f}{'+' if opal_trade_progress > 100 else ''}",
        goal=100,
        unit='%'
    ))

# Bucket Stats
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

# Sediment Stats
    cavern_advice[s_stats].append(Advice(
        label=f"Expand Full Bars: {'On' if session_data.account.caverns['Caverns']['The Well']['BarExpansion'] else 'Off'}",
        picture_class='engineer-schematic-13'
    ))
    cavern_advice[s_stats].append(Advice(
        label=f"Total expansions: {sum(sediment_levels)}"
              f"<br>Total bonus: {sum(sediment_levels) * 20 * schematics['Expander Extravaganza']['Purchased']:,}%",
        picture_class='engineer-schematic-14'
    ))
    for sediment_index, sediment_value in enumerate(sediments_owned):
        if sediment_index < max_sediments:  # There are lots of placeholders in sediments_owned, so stay within bounds of max_sediments
            target = getSedimentBarRequirement(sediment_index, sediment_levels[sediment_index])
            if target >= 1e9:
                target = notateNumber('Basic', target, 2)
                sedi_owned = notateNumber('Basic', sediment_value, 2)
            else:
                target = f"{target:,.0f}"
                sedi_owned = f"{sediment_value:,}"
            cavern_advice[s_stats].append(Advice(
                label=(
                    f"{sediment_names[sediment_index]}: {sediment_levels[sediment_index]} expansions"
                    f"<br>{sedi_owned} owned"
                    f"<br>{target} to expand"
                    if sediment_value >= 0 else
                    f"Clear the rock layer to discover this Sediment!"
                ),
                picture_class=f"well-sediment-{sediment_index}",
                resource='well-sediment-rock-layer' if sediment_value < 0 else '',
                progression=0 if sediment_value < 0 else f"{100 * (sediment_value / getSedimentBarRequirement(sediment_index, sediment_levels[sediment_index])):.1f}",
                goal=100,
                unit='%'
            ))


    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name if cavern['Unlocked'] else 'To Be Discovered!'}",
        advices=cavern_advice,
        informational=True,
        picture_class='cavern-1'
    )
    return cavern_ag

def getMotherlodeAdviceGroup(schematics):
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
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='mining'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

# Layer Stats
    cavern_advice[l_stats].append(Advice(
        label=f"Layer {cavern['LayersDestroyed']+1} {resource_skill} Efficiency Required: "
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

def getDenAdviceGroup(schematics) -> AdviceGroup:
    c_stats = "Cavern Stats"
    a_stats = 'Amplifier Stats'
    cavern_advice = {
        c_stats: [],
        a_stats: []
    }

    cavern_name = 'The Den'
    cavern = session_data.account.caverns['Caverns'][cavern_name]

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Fight increasingly difficult Dawgs, using Amplifiers to increase score",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='dawg-den-dawgs'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
    next_opal_score = getDenOpalRequirement(cavern['OpalsFound'])
    cavern_advice[c_stats].append(Advice(
        label=f"High Score: {cavern['HighScore']:,}"
              f"<br>Next Opal:  {next_opal_score:,}",
        picture_class='my-first-trophy',
        progression=f"{100 * (cavern['HighScore']/next_opal_score):.1f}",
        goal=100,
        unit='%'
    ))

# Amplifier Stats
    for amp_name, amp_details in schematics_unlocking_amplifiers.items():
        amp_unlocked = amp_details[1] == '' or schematics.get(amp_details[1], {}).get('Purchased', False)
        cavern_advice[a_stats].append(Advice(
            label=(
                f"{amp_name}: {amp_details[0]}"
                if amp_unlocked
                else
                f"Unlock Amplifier {int(amp_details[2][-1])+1} by purchasing"
                f"<br>Schematic {schematics[amp_details[1]]['UnlockOrder']}: {amp_details[1]}"
            ),
            picture_class=amp_details[2],
            resource=(
                '' if amp_unlocked
                else schematics[amp_details[1]]['Resource']
            )
        ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name if cavern['Unlocked'] else 'To Be Discovered!'}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getBraveryAdviceGroup(schematics) -> AdviceGroup:
    c_stats = "Cavern Stats"
    s_stats = 'Sword Stats'
    l_stats = 'Layer Stats'
    b_stats = 'Bonuses Stats'
    cavern_advice = {
        c_stats: [],
        l_stats: [],
        s_stats: [],
        b_stats: []
    }

    cavern_name = 'Bravery Monument'
    cavern = session_data.account.caverns['Caverns'][cavern_name]
    layer_rewards = monument_layer_rewards[cavern_name]
    bonuses = cavern['Bonuses']

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- AFK here to gain Monument Hours that empower your Attacks within the Story minigame",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='bravery-bonus-8'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Chance for next Opal: {getBraveryOpalChance(cavern['OpalsFound'], bonuses[5]['Value']):.2%}",
        picture_class='monument-basic-chest',
    ))

# Sword Stats
    cavern_advice[s_stats].append(Advice(
        label=f"Total Swords: {cavern['Sword Count']}/"
              f"{cavern['Max Swords'] if cavern['Sword Count'] == cavern['Max Swords'] else '?'}",
        picture_class='monument-basic-sword',
        progression=cavern['Sword Count'],
        goal=cavern['Max Swords'] if cavern['Sword Count'] >= cavern['Max Swords'] else '?'
    ))
    cavern_advice[s_stats].append(Advice(
        label=f"Per Sword: {round(cavern['Sword Min']):,} to {round(cavern['Sword Max']):,}"
              f"<br>All Swords: {round(cavern['Sword Count'] * cavern['Sword Min']):,} to {round(cavern['Sword Count'] * cavern['Sword Max']):,}"
              f"<br>'Average' fight: {round(cavern['Sword Count'] * ((cavern['Sword Max'] - cavern['Sword Min']) / 2)):,}",
        picture_class='monument-basic-sword'
    ))

    cavern_advice[s_stats].append(Advice(
        label=f"{cavern['Rethrows']}/"
              f"{cavern['Max Rethrows'] if cavern['Rethrows'] >= cavern['Max Rethrows'] else '?'} "
              f"Sword Rethrows per Fight",
        picture_class='engineer-schematic-40',
        progression=cavern['Rethrows'],
        goal=cavern['Max Rethrows'] if cavern['Rethrows'] >= cavern['Max Rethrows'] else '?'
    ))
    cavern_advice[s_stats].append(Advice(
        label=f"{cavern['Retellings']}/"
              f"{cavern['Max Retellings'] if cavern['Retellings'] >= cavern['Max Retellings'] else '?'} "
              f"Retellings per Story attempt",
        picture_class='engineer-schematic-40',
        progression=cavern['Retellings'],
        goal=cavern['Max Retellings'] if cavern['Retellings'] >= cavern['Max Retellings'] else '?'
    ))

# Layer Stats
    cavern_advice[l_stats] = [
        Advice(
            label=f"{hour_requirement:,} hour bonus: "
                  f"{layer_reward['Description'] if cavern['Hours'] >= hour_requirement else 'To be discovered'}",
            picture_class=layer_reward['Image'],
            progression=cavern['Hours'],
            goal=hour_requirement
        ) for hour_requirement, layer_reward in layer_rewards.items()
    ]

    cavern_advice[l_stats].insert(0, Advice(
        label=f"Monument Hours: {cavern['Hours']:.0f}",
        picture_class='measurement-1'
    ))

# Bonuses Stats
    cavern_advice[b_stats] = [
        Advice(
            label=f"{bonus['Description'] if bonus['Level'] else 'Undiscovered bonus'}",
            picture_class=bonus['Image'],
            progression=bonus['Level'],
            goal=infinity_string
        ) for bonus in bonuses.values()
    ]
    mv = session_data.account.caverns['Majiks']['Monumental Vibes']
    cavern_advice[b_stats].insert(0, Advice(
        label=f"Monumental Vibes {{{{ Majik|#villagers }}}}: {mv['Description']}"
              f"<br>(Already applied below)",
        picture_class=f"{mv['MajikType']}-majik-{'un' if mv['Level'] == 0 else ''}purchased",
        progression=mv['Level'],
        goal=mv['MaxLevel']
    ))

    for subgroup in cavern_advice:
        for advice in cavern_advice[subgroup]:
            mark_advice_completed(advice)

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name if cavern['Unlocked'] else 'To Be Discovered!'}",
        advices=cavern_advice,
        informational=True
    )
    return cavern_ag

def getBellAdviceGroup(schematics):
    c_stats = "Cavern Stats"
    r_stats = 'Ring Stats'
    clean_stats = 'Clean Stats'
    cavern_advice = {
        c_stats: [],
        r_stats: [],
        clean_stats: []
    }

    cavern_name = 'The Bell'
    cavern = session_data.account.caverns['Caverns'][cavern_name]

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Passively build up Charge in 1 of 4 different categories at a time for various Bonuses",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))

    target_cost = cavern['Charges']['Ping'][2]
    target_string = notateNumber('Basic', target_cost, 2)
    target_letter = str(target_string[-1]) if target_cost > 1000 else ''
    current_number = cavern['Charges']['Ping'][0]
    current_string = notateNumber('Match', current_number, 2, target_letter)
    current_percent = 100 * (cavern['Charges']['Ping'][0] / target_cost)
    cavern_advice[c_stats].append(Advice(
        label=f"Current Ping charge: {current_string}"
              f"<br>Next Opal: {target_string}",
        picture_class='bell-ping',
        progression=f"{current_percent:,.2f}",
        goal=100,
        unit='%'
    ))

# Ring Bonuses
    cavern_advice[r_stats] = [
        Advice(
            label=(
                f"{rb_details['Description']}"
                if rb_details['Level'] > 0 else
                f"Undiscovered Bonus"
            ),
            picture_class=rb_details['Image'],
            progression=rb_details['Level'],
            goal=infinity_string
        ) for rb_index, rb_details in cavern['Ring Bonuses'].items()
    ]
    total_rings = cavern['Charges']['Ring'][1]
    cavern_advice[r_stats].insert(0, Advice(
        label=f"Total Rings: {total_rings}",
        picture_class='bell-ring'
    ))
    total_bonus_levels = sum([rb_details['Level'] for rb_details in cavern['Ring Bonuses'].values()])
    average_level = total_bonus_levels/max(1,total_rings)
    average_level_too_low = average_level < 1.84  #Per Stark: if it's a flat +20, average 2, if it's 20% chance a +2 becomes +3 then it's 1.84
    cavern_advice[r_stats].insert(1, Advice(
        label=f"""Total Bonus levels: {total_bonus_levels}"""
              f"""<br>Avg per ring: {average_level:.4f}"""
              f"""{'<br>Under 1.84: Consider Renewing' if (
                  schematics['Double Dinger Ringer']['Purchased']
                  and schematics['Triple Tap Tinkle']['Purchased']
                  and average_level_too_low
                  and total_rings >= 100
              ) else f'<br>Above 1.84: nice RNG 🙂'
              }""",
        picture_class='bell-ring',
        completed=False,
        informational=True
    ))

# Clean Improvements
    total_improvements = cavern['Total Improvements']
    stack_size = cavern['Stack Size']
    total_stacks = cavern['Total Stacks']
    cavern_advice[clean_stats] = [
        Advice(
            label=(
                ci_details['Description']
                if ci_details['Level'] > 0 else
                f"Undiscovered Bonus"
            ),
            picture_class=ci_details['Image'],
            progression=ci_details['Level'],
            goal=infinity_string,
            resource=ci_details['Resource'],
        ) for ci_index, ci_details in cavern['Improvements'].items()
    ]
    cavern_advice[clean_stats].insert(0, Advice(
        label=f"Total Improvements: {total_improvements} ({total_stacks} stacks)"
              f"<br>Total Bonus: {pow(1.1, total_stacks):.1f}x"
              f"<br>Next stack progress",
        picture_class='engineer-schematic-45',
        progression=total_improvements % stack_size,
        goal=stack_size
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name if cavern['Unlocked'] else 'To Be Discovered!'}",
        advices=cavern_advice,
        informational=True
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
    schematics = session_data.account.caverns['Schematics']
    shallow_caverns_AdviceGroupDict = {}
    shallow_caverns_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    shallow_caverns_AdviceGroupDict['The Well'] = getWellAdviceGroup(schematics)
    shallow_caverns_AdviceGroupDict['Motherlode'] = getMotherlodeAdviceGroup(schematics)
    shallow_caverns_AdviceGroupDict['The Den'] = getDenAdviceGroup(schematics)
    shallow_caverns_AdviceGroupDict['Bravery Monument'] = getBraveryAdviceGroup(schematics)
    shallow_caverns_AdviceGroupDict['The Bell'] = getBellAdviceGroup(schematics)

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
