from math import ceil

from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.all_talentsDict import all_talentsDict
from utils.data_formatting import mark_advice_completed, safer_math_log
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import (
    # grimoire_progressionTiers, break_you_best, infinity_string,
    ValueToMulti, EmojiType,
)
from consts.consts_idleon import lavaFunc
from consts.consts_master_classes import grimoire_bones_list
from consts.consts_w2 import arcade_max_level
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    grimoire_AdviceDict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Grimoire']
    max_tier = true_max - optional_tiers
    tier_Grimoire = 0

    tiers_ag = AdviceGroup(
        tier=tier_Grimoire,
        pre_string='Progression Tiers',
        advices=grimoire_AdviceDict['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Grimoire)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getGrimoireCurrenciesAdviceGroup(grimoire) -> AdviceGroup:
    currency_advices = {
        'Currencies': [],
    }
    currency_advices['Currencies'].append(Advice(
        label=f"Total Bones Collected: {notateNumber('Basic', grimoire['Total Bones Collected'], 3)}",
        picture_class='wraith-overlord'
    ))
    if grimoire['Charred Bones Enabled']:
        currency_advices['Currencies'].append(Advice(
            label=f"Charred Bones Enabled! Collect 1 per full AFK hour while fighting on a Death Bringer. Maximize your /hr display "
                  f"within AFK Info screen before consuming!",
            picture_class='charred-bone',
            progression=1,
            goal=1
        ))
    else:
        currency_advices['Currencies'].append(Advice(
            label=f"Fight with Wraith Form enabled to collect 1,000 Charred Fragments, then use the stack. "
                  f"This enables AFK Fighting on Death Bringers to produce 1 Charred Bone per hour!",
            picture_class='charred-fragment',
            progression=min(1000, session_data.account.all_assets.get('Quest98').amount),
            goal=1000
        ))
    currency_advices['Currencies'] += [
        Advice(
            label=f"{bone_name}: {notateNumber('Basic', grimoire[f'Bone{bone_index}'], 3)}",
            picture_class=f'grimoire-bone-{bone_index-1}'
        ) for bone_index, bone_name in enumerate(grimoire_bones_list, start=1)
    ]

    #Bone Multi calculation groups
    currency_advices['Currencies'].append(Advice(
        label=f"Total Bone multi: {grimoire['Bone Calc']['Total']:.3f}x",
        picture_class='grimoire'
    ))

    mga_label = f"Bone Multi Group A: {grimoire['Bone Calc']['mga']:.2f}x"
    currency_advices[mga_label] = [
        Advice(
            label=f"{{{{Sneaking|#sneaking}}}}: Pristine Charm: Glimmerchain"
                  f"<br>{session_data.account.sneaking['PristineCharms']['Glimmerchain']['Bonus']}",
            picture_class=session_data.account.sneaking['PristineCharms']['Glimmerchain']['Image'],
            progression=int(session_data.account.sneaking['PristineCharms']['Glimmerchain']['Obtained']),
            goal=1
        )
    ]

    db_index = None
    grimoire_preset_level = 100

    for db in session_data.account.dbs:
        if db_index is None:
            db_index = db.character_index
        if db.current_preset_talents.get('196', 0) > grimoire_preset_level:
            db_index = db.character_index
            grimoire_preset_level = db.current_preset_talents.get('196', 0)
        if db.secondary_preset_talents.get('196', 0) > grimoire_preset_level:
            grimoire_preset_level = db.secondary_preset_talents.get('196', 0)

    mgb_label = f"Bone Multi Group B: {grimoire['Bone Calc']['mgb']:.3f}x"
    currency_advices[mgb_label] = [
        Advice(
            label=f"{grimoire_preset_level}/{session_data.account.library['MaxBookLevel']} booked Grimoire:"
                  f"<br>Max Preset Level {grimoire_preset_level + session_data.account.all_characters[db_index].total_bonus_talent_levels} on "
                  f"{session_data.account.all_characters[db_index].character_name} including bonus talent levels",
            picture_class='grimoire',
            progression=grimoire_preset_level,
            goal=session_data.account.library['MaxBookLevel']
        )
    ]

    mgc_label = f"Bone Multi Group C: {grimoire['Bone Calc']['mgc']:.2f}x"
    gambit = session_data.account.caverns['Caverns']['Gambit']
    currency_advices[mgc_label] = [
        Advice(
            label=(
                f"{{{{Cavern 14- Gambit|#underground-overgrowth}}}}: Bonus 13: +100% Bones"
                if gambit['Bonuses'][12]['Unlocked'] else
                f"{{{{Cavern 14- Gambit|#underground-overgrowth}}}}: Bonus 13: +0% Bones"
                f"<br>{ceil(gambit['Bonuses'][12]['PtsRequired'] - gambit['TotalPts']):,.0f}"
                f" Gambit points remaining to Unlock this bonus"
            ),
            picture_class=gambit['Bonuses'][12]['Image'],
            progression=int(gambit['Bonuses'][12]['Unlocked']),
            goal=1
        )
    ]

    mgd_label = f"Bone Multi Group D: {grimoire['Bone Calc']['mgd']:.2f}x"
    currency_advices[mgd_label] = [
        Advice(
            label=f"Deathbringer Hood of Death: +25%",
            picture_class='deathbringer-hood-of-death',
            progression=int(session_data.account.all_assets.get('EquipmentHats112').amount > 0),
            goal=1,
            resource='gem'
        ),
    ]

    mge_label = f"Bone Multi Group E: {grimoire['Bone Calc']['mge']:.2f}x"
    ab40 = session_data.account.arcade[40]
    currency_advices[mge_label] = []
    bop = grimoire['Upgrades']["Bones o' Plenty"]
    currency_advices[mge_label].append(Advice(
        label=(
            f"Bones o' Plenty: {bop['Description']}"
            f"<br>Requires {bop['Unlock Requirement'] - grimoire['Total Upgrades']} more Upgrades to unlock"
            if not bop['Unlocked'] else
            f"Bones o' Plenty: {bop['Description']}"
        ),
        picture_class=bop['Image'],
        progression=bop['Level'],
        goal=bop['Max Level'],
        resource=bop['Bone Image']
    ))
    bh = grimoire['Upgrades']['Bovinae Hoarding']
    currency_advices[mge_label].append(Advice(
        label=(
            f"Bovinae Hoarding: {bh['Description']}"
            f"<br>Requires {bh['Unlock Requirement'] - grimoire['Total Upgrades']} more Upgrades to unlock"
            if not bh['Unlocked'] else
            f"Bovinae Hoarding: {bh['Description']}"
            f"<br>{safer_math_log(grimoire['Bone4'], 'Lava'):.3f} stacks = "
            f"{bh['Total Value'] * safer_math_log(grimoire['Bone4'], 'Lava'):.3f}% total"
        ),
        picture_class=bh['Image'],
        progression=bh['Level'],
        goal=bh['Max Level'],
        resource=bh['Bone Image']
    ))
    currency_advices[mge_label].append(Advice(
        label=f"Arcade Bonus 40: {ab40['Display']}",
        picture_class=ab40['Image'],
        progression=ab40['Level'],
        goal=arcade_max_level + 1,
        resource=ab40['Material'],
    ))

    lab_jewel = session_data.account.labJewels['Deadly Wrath Jewel']
    lab_jewel_active = lab_jewel['Enabled']
    currency_advices[mge_label].append(Advice(
        label=f"Lab Jewel 'Deadly Wrath Jewel': +{lab_jewel['Value'] * lab_jewel_active}/{lab_jewel['Value']}%",
        picture_class='deadly-wrath-jewel',
        progression=int(lab_jewel_active),
        goal=1
    ))

    mgf_label = f"Bone Multi Group F: {grimoire['Bone Calc']['mgf']:.2f}x"
    db_index = None
    tombstone_preset_level = 100
    for db in session_data.account.dbs:
        if db_index is None:
            db_index = db.character_index
        if db.current_preset_talents.get('198', 0) > tombstone_preset_level:
            db_index = db.character_index
            tombstone_preset_level = db.current_preset_talents.get('198', 0)
        if db.secondary_preset_talents.get('198', 0) > tombstone_preset_level:
            tombstone_preset_level = db.secondary_preset_talents.get('198', 0)

    tombstone_per_stack = lavaFunc(
        funcType=all_talentsDict[198]['funcX'],
        level=tombstone_preset_level,
        x1=all_talentsDict[198]['x1'],
        x2=all_talentsDict[198]['x2'],
    )

    currency_advices[mgf_label] = [
        Advice(
            label=f"{tombstone_preset_level}/{session_data.account.library['MaxBookLevel']} booked Graveyard Shift:"
                  f"<br>Max Preset Level {tombstone_preset_level + session_data.account.all_characters[db_index].total_bonus_talent_levels} on "
                  f"{session_data.account.all_characters[db_index].character_name} including bonus talent levels",
            picture_class='graveyard-shift',
            progression=tombstone_preset_level,
            goal=session_data.account.library['MaxBookLevel']
        ),
        Advice(
            label=f"<br>Per stack: +{tombstone_per_stack:.3f}%"
                  f"<br>50 stacks: {ValueToMulti(50 * tombstone_per_stack):.3f}x"
                  f"<br>100 stacks: {ValueToMulti(100 * tombstone_per_stack):.3f}x"
                  f"<br>200 stacks: {ValueToMulti(200 * tombstone_per_stack):.3f}x"
                  f"<br>300 stacks: {ValueToMulti(300 * tombstone_per_stack):.3f}x"
                  f"<br>500 stacks: {ValueToMulti(500 * tombstone_per_stack):.3f}x",
            picture_class='graveyard-shift-tombstone',
            completed=True,
            informational=True
        )
    ]

    mgg_label = f"Bone Multi Group G: {grimoire['Bone Calc']['mgg']:.2f}x"
    currency_advices[mgg_label] = [
        Advice(
            label=f"{{{{Emperor Showdowns|#emperor}}}}: {session_data.account.emperor['Bonuses'][1]['Description']}"
                  f"<br>{session_data.account.emperor['Bonuses'][1]['Scaling']}",
            picture_class='the-emperor',
            progression=session_data.account.emperor['Bonuses'][1]['Wins'],
            goal=EmojiType.INFINITY.value
        )
    ]

    for subgroup in currency_advices:
        for advice in currency_advices[subgroup]:
            mark_advice_completed(advice)

    currency_ag = AdviceGroup(
        tier='',
        pre_string='Grimoire Currencies',
        advices=currency_advices,
        informational=True
    )
    # currency_ag.remove_empty_subgroups()
    return currency_ag

def getGrimoireUpgradesAdviceGroup(grimoire) -> AdviceGroup:
    upgrades_AdviceDict = {}

    #General Info
    upgrades_AdviceDict['General Info'] = []

    #Upgrades
    upgrades_AdviceDict['Upgrades'] = [Advice(
        label=f"Total Grimoire Upgrades: {grimoire['Total Upgrades']:,}",
        picture_class='grimoire'
    )]
    upgrades_AdviceDict['Upgrades'] += [
        Advice(
            label=(
                f"{upgrade_name}: {upgrade_details['Description']}"
                f"<br>Requires {upgrade_details['Unlock Requirement'] - grimoire['Total Upgrades']} more Upgrades to unlock"
                if not upgrade_details['Unlocked'] else
                f"{upgrade_name}: {upgrade_details['Description']}"
            ),
            picture_class=upgrade_details['Image'],
            progression=upgrade_details['Level'],
            goal=upgrade_details['Max Level'],
            resource=upgrade_details['Bone Image']
        ) for upgrade_name, upgrade_details in grimoire['Upgrades'].items()
    ]

    for subgroup in upgrades_AdviceDict:
        for advice in upgrades_AdviceDict[subgroup]:
            mark_advice_completed(advice)

    upgrades_ag = AdviceGroup(
        tier='',
        pre_string='Grimoire Upgrades',
        advices=upgrades_AdviceDict,
        informational=True
    )
    upgrades_ag.remove_empty_subgroups()
    return upgrades_ag


def getGrimoireAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if 'Death Bringer' not in session_data.account.classes:
        grimoire_AdviceSection = AdviceSection(
            name="The Grimoire",
            tier="Not Yet Evaluated",
            header="Come back after unlocking a Death Bringer in World 6!",
            picture='customized/Wraith.gif',
            unrated=True,
            unreached=session_data.account.highest_world_reached < 6,
            completed=False
        )
        return grimoire_AdviceSection

    grimoire = session_data.account.grimoire
    #Generate Alert Advice

    #Generate AdviceGroups
    grimoire_AdviceGroupDict = {}
    grimoire_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    grimoire_AdviceGroupDict['Currencies'] = getGrimoireCurrenciesAdviceGroup(grimoire)
    grimoire_AdviceGroupDict['Upgrades'] = getGrimoireUpgradesAdviceGroup(grimoire)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    grimoire_AdviceSection = AdviceSection(
        name='The Grimoire',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header='Death Bringer and Grimoire Information',  #tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Wraith.gif',
        groups=grimoire_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return grimoire_AdviceSection
