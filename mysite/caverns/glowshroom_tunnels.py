from consts.progression_tiers import true_max_tiers
from consts.consts_autoreview import EmojiType
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
# from consts.consts import glowshroom_tunnels_progressionTiers, break_you_best, ValueToMulti
from consts.consts_caverns import caverns_cavern_names, schematics_unlocking_harp_strings, monument_layer_rewards, justice_monument_currencies, harp_notes, \
    getMotherlodeEfficiencyRequired, getMonumentOpalChance, getHarpNoteUnlockCost
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getHarpAdviceGroup(schematics):
    cavern_name = caverns_cavern_names[6]
    cavern = session_data.account.caverns['Caverns'][cavern_name]

    c_stats = "Cavern Stats"
    c_faqs = "FAQs"
    string_stats = f"String Stats: {cavern['Strings']}/{cavern['Max Strings']} unlocked"
    chord_stats = f"Chord Stats: {cavern['ChordsUnlockedCount']}/{cavern['Max Chords']} unlocked"
    n_stats = "Note Stats"
    cavern_advice = {
        c_stats: [],
        c_faqs: [],
        string_stats: [],
        chord_stats: [],
        n_stats: [],
    }

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Spend passively generated Harp Power to collect Notes",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
# Cavern FAQs
# String Stats
    string_is_strung = session_data.account.caverns['Majiks']['String is Strung']
    cavern_advice[string_stats].append(Advice(
        label=f"String is Strung {{{{ Cavern Majik|#villagers }}}}: {string_is_strung['Description']}",
        picture_class=f"{string_is_strung['MajikType']}-majik-{'un' if string_is_strung['Level'] == 0 else ''}purchased",
        progression=string_is_strung['Level'],
        goal=string_is_strung['MaxLevel']
    ))
    for schematic_name in schematics_unlocking_harp_strings:
        cavern_advice[string_stats].append(Advice(
            label=f"Schematic {schematics[schematic_name]['UnlockOrder']}: {schematic_name}",
            picture_class=schematics[schematic_name]['Image'],
            progression=int(schematics[schematic_name]['Purchased']),
            goal=1
        ))

# Chord Stats
    cavern_advice[chord_stats] = [
        Advice(
            label=(
                f"Level {chord_details['Level']} {chord_letter} chord"
                f"<br>Strum Effect: {chord_details['Strum']}"
                f"<br>LV Bonus: {chord_details['LVBonus']}"
                if chord_details['Unlocked']
                else f"Unlock {chord_letter} chord by purchasing Schematic {schematics[chord_details['UnlockedBy']]['UnlockOrder']}: {chord_details['UnlockedBy']}"
            ),
            picture_class=f"harp-chord-{chord_letter}",
            progression=chord_details['Level'],
            goal=EmojiType.INFINITY.value
        ) for chord_letter, chord_details in cavern['Chords'].items()
    ]
    cavern_advice[chord_stats].insert(0, Advice(
        label=f"Current Harp Power:"
              f"<br>{notateNumber('Basic', cavern['HarpPower'], 2)}",
        picture_class=f"cavern-{cavern['CavernNumber']}"
    ))
# Note Stats
    for note_index, note_amount in enumerate(cavern['NotesOwned']):
        if cavern['NotesUnlocked'] < note_index:
            unlock_cost = getHarpNoteUnlockCost(note_index-1)
            target_string = notateNumber('Basic', unlock_cost, 2)
            current_string = notateNumber('Match', min(unlock_cost, cavern['NotesOwned'][note_index-1]), 2, '', target_string)
            note_advice = Advice(
                label=f"Unlock {harp_notes[note_index]}s by trading {target_string} of the previous Note",
                picture_class=f'harp-note-{note_index}',
                resource=f'harp-note-{note_index-1}',
                progression=current_string,
                goal=target_string
            )
        else:
            note_advice = Advice(
                f"{harp_notes[note_index]}s: {notateNumber('Basic', note_amount, 2)}",
                picture_class=f'harp-note-{note_index}',
                goal=EmojiType.INFINITY.value,
            )
        cavern_advice[n_stats].append(note_advice)

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
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

def getMotherlodeAdviceGroup():
    c_stats = "Cavern Stats"
    l_stats = 'Layer Stats'
    cavern_advice = {
        c_stats: [],
        l_stats: []
    }

    cavern_name = caverns_cavern_names[8]
    resource_type = 'Bugs'
    resource_skill = 'Catching'
    cavern = session_data.account.caverns['Caverns'][cavern_name]
# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- Use your characters to collect {resource_type} while {resource_skill} and break Layers to collect Opals",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource=resource_skill
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
    cavern_advice[l_stats].append(session_data.account.caverns['MotherlodeResourceDiscountAdvice'])
    resource_required = session_data.account.caverns['Caverns'][cavern_name]['ResourcesRemaining']
    cavern_advice[l_stats].append(Advice(
        label=f"{resource_type} remaining to break Layer {cavern['LayersDestroyed'] + 1}: {notateNumber('Basic', resource_required - cavern['ResourcesCollected'], 1)}",
        picture_class=f'motherlode-{resource_type}',
        progression=f"{min(100, 100 * (cavern['ResourcesCollected'] / resource_required)):.1f}",
        goal=100,
        unit='%'
    ))

    cavern_ag = AdviceGroup(
        tier='',
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True,
        picture_class=f"cavern-{cavern['CavernNumber']}"
    )
    return cavern_ag

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
    c_stats = "Cavern Stats"
    curr_stats = 'Currency Stats'
    l_stats = 'Layer Stats'
    b_stats = 'Bonuses Stats'
    cavern_advice = {
        c_stats: [],
        l_stats: [],
        curr_stats: [],
        b_stats: []
    }

    cavern_name = caverns_cavern_names[10]
    monument_index = 1
    cavern = session_data.account.caverns['Caverns'][cavern_name]
    layer_rewards = monument_layer_rewards[cavern_name]
    bonuses = cavern['Bonuses']

# Cavern Stats
    cavern_advice[c_stats].append(Advice(
        label=f"Objective- AFK here to gain Monument Hours that empower your Rulings within the Story minigame",
        picture_class=f"cavern-{cavern['CavernNumber']}",
        resource='bravery-bonus-8'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Total Opals Found: {cavern['OpalsFound']}",
        picture_class='opal'
    ))
    cavern_advice[c_stats].append(Advice(
        label=f"Chance for next Opal: {getMonumentOpalChance(cavern['OpalsFound'], bonuses[5 + 10 * monument_index]['Value']):.2%}",
        picture_class='monument-basic-chest',
    ))

# Currency Stats
    cavern_advice[curr_stats] = [
        Advice(
            label=f"{cavern[currency_name]}/{cavern[f'Max {currency_name}']} starting {currency_name}",
            picture_class=f'justice-currency-{currency_index + 2}',
            progression=cavern[currency_name],
            goal=cavern[f'Max {currency_name}']
        ) for currency_index, currency_name in enumerate(justice_monument_currencies)
    ]

# Layer Stats
    cavern_advice[l_stats] = [
        Advice(
            label=f"{hour_requirement:,} hour bonus: {layer_reward['Description']}",
            picture_class=layer_reward['Image'],
            progression=cavern['Hours'],
            goal=hour_requirement
        ) for hour_requirement, layer_reward in layer_rewards.items()
    ]

    cavern_advice[l_stats].insert(0, Advice(
        label=f"Monument Hours: {cavern['Hours']:,.0f}",
        picture_class='justice-bonus-19'
    ))

# Bonuses Stats
    cavern_advice[b_stats] = [
        Advice(
            label=(
                f"Level {bonus['Level']}: {bonus['Description']}"
                f"<br>{bonus['BaseValue']:.2f}/{bonus['ScalingValue']} max from Levels"
                if bonus['ScalingValue'] > 30 else
                f"Level {bonus['Level']}: {bonus['Description']}"
                f"<br>+{bonus['ScalingValue'] if '%' in bonus['Description'] else '0.' if bonus['ScalingValue'] >= 10 else '0.0'}"
                f"{'' if '%' in bonus['Description'] else bonus['ScalingValue']}"
                f"{'%' if '%' in bonus['Description'] else 'x'} "
                f"per level before multis"
            ),
            picture_class=bonus['Image'],
            progression=f"{(bonus['BaseValue'] / bonus['ScalingValue']) * 100:.2f}" if bonus['ScalingValue'] > 30 else 'Linear',
            goal=100 if bonus['ScalingValue'] > 30 else EmojiType.INFINITY.value,
            unit='%' if bonus['ScalingValue'] > 30 else ''
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
        pre_string=f"Cavern {cavern['CavernNumber']}- {cavern_name}",
        advices=cavern_advice,
        informational=True
    )
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
    if session_data.account.caverns['Villagers']['Polonai']['Level'] < 6:
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
    schematics = session_data.account.caverns['Schematics']
    glowshroom_tunnels_AdviceGroupDict = {}
    glowshroom_tunnels_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict['The Harp'] = getHarpAdviceGroup(schematics)
    glowshroom_tunnels_AdviceGroupDict['The Lamp'] = getLampAdviceGroup()
    glowshroom_tunnels_AdviceGroupDict['The Hive'] = getMotherlodeAdviceGroup()
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
