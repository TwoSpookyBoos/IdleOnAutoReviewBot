from models.models import Advice, AdviceGroup, AdviceSection
from consts.consts_autoreview import break_you_best
from consts.consts_w2 import max_vial_level
from consts.consts_w1 import statue_type_list, statue_count
from consts.progression_tiers import statues_progressionTiers, true_max_tiers
from utils.data_formatting import mark_advice_completed, safer_get
from utils.logging import get_logger
from flask import g as session_data

from utils.text_formatting import pl

logger = get_logger(__name__)


def getPreOnyxAdviceGroup() -> AdviceGroup:
    crystal_Advices = []
    deposit_Advices = []

    if not session_data.account.onyx_statues_unlocked:
        crystal_Advices.append(Advice(
            label="Complete the Monolith NPC's questline to unlock Onyx Statues",
            picture_class='monolith',
            resource='onyx-tools',
            progression=0,
            goal=1
        ))
    crystal_Advices.append(Advice(
        label='Chocolatey Chip for more Crystal Mobs',
        picture_class="chocolatey-chip",
        progression=session_data.account.labChips.get('Chocolatey Chip', 0),
        goal=1
    ))
    cards = ['Demon Genie', 'Poop']
    for card_name in cards:
        crystal_Advices.append(next(c for c in session_data.account.cards if c.name == card_name).getAdvice('Minimum 3 star'))

    crystal_Advices.append(Advice(
        label=f"Minimum 100 Crystallin Stamp: {session_data.account.stamps['Crystallin']['Level']} (+{session_data.account.stamps['Crystallin']['Total Value']:.3f}%)",
        picture_class='crystallin',
        progression=session_data.account.stamps['Crystallin']['Level'],
        goal=100  #stamp_maxes['Crystallin']
    ))
    crystal_Advices.append(Advice(
        label=f"Star Talent 'Crystals 4 Dayys' obtained by completing Picnic Stowaway's quest: \"The Last Supper, at Least for Today\"",
        picture_class='crystals-4-dayys',
        progression=int(any([char.max_talents.get('619', 0) > 0 for char in session_data.account.all_characters])),
        goal=1
    ))
    crystal_Advices.append(Advice(
        label=f"{{{{ Sailing|#sailing }}}}: Moai Head artifact to apply Shrines everywhere",
        picture_class='moai-head',
        progression=session_data.account.sailing['Artifacts']['Moai Head']['Level'],
        goal=1
    ))
    crystal_Advices.append(Advice(
        label=f"Minimum 1% (1 in 100) {{{{ Crystal Spawn Chance|#active }}}} on Non-Jman:"
              f"<br>{session_data.account.highest_crystal_spawn_chance*100:.4f}%"
              f" (1 in {100/(session_data.account.highest_crystal_spawn_chance*100):.2f})",
        picture_class='crystal-carrot',
        progression=f"{session_data.account.highest_crystal_spawn_chance * 100:.4f}",
        goal=1,
        unit="%"
    ))
    best_orb_book = 0
    for dk in session_data.account.dks:
        best_orb_book = max(best_orb_book, dk.max_talents.get("168", 0))
    crystal_Advices.append(Advice(
        label=f"Level {best_orb_book}/{session_data.account.library['MaxBookLevel']} booked Orb of Remembrance talent (Divine Knight only)",
        picture_class='orb-of-remembrance',
        progression=best_orb_book,
        goal=session_data.account.library['MaxBookLevel']
    ))
    tome_DropChance = safer_get(session_data.account.raw_optlacc_dict, 200, 1)
    crystal_Advices.append(Advice(
        label=f"Minimum 10x Drop Rate (per Tome): {tome_DropChance:.2f}x",
        picture_class='drop-rate',
        progression=f"{tome_DropChance:.2f}",
        goal=10,
    ))

    #Statue Value
    deposit_Advices.append(Advice(
        label=f"Startue Exp bubble: "
              f"{session_data.account.alchemy_bubbles['Startue Exp']['BaseValue']:.3f}/20%+ minimum",
        picture_class='startue-exp',
        progression=session_data.account.alchemy_bubbles['Startue Exp']['Level'],
        goal=240,
        resource=session_data.account.alchemy_bubbles['Startue Exp']['Material']
    ))

    vial_value = session_data.account.alchemy_vials['Skinny 0 Cal (Snake Skin)']['Value']

    deposit_Advices.append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Skinny 0 Cal (Snake Skin) to level {max_vial_level}",
        picture_class='snake-skin',
        progression=session_data.account.alchemy_vials['Skinny 0 Cal (Snake Skin)']['Level'],
        goal=max_vial_level
    ))
    deposit_Advices.append(Advice(
        label='Total Vial value (100% hardcap)',
        picture_class='vials',
        progression=f'{min(100, vial_value):.2f}',
        goal=100,
    ))

    for advicelist in [crystal_Advices, deposit_Advices]:
        for advice in advicelist:
            mark_advice_completed(advice)

    crystal_AG = AdviceGroup(
        tier='',
        pre_string='To-Do list before dedicated Onyx Statue farming',
        advices={'Crystal Chance and Drop Rate': crystal_Advices, 'Statue Value': deposit_Advices},
        informational=True
    )
    return crystal_AG

def getCurrentLevelsAdviceGroup() -> AdviceGroup:
    advices = {
        'Effect bonuses': session_data.account.statue_effect_advice,
        'Statue Effects': [
            Advice(
                label=f"Level {details['Level']} {name}:"
                      f"<br> +{round(details['Value'], 2):,g}{' ' if not details['Effect'].startswith('%') else ''}{details['Effect']}",
                picture_class=details['Image'],
                progression=details['Level'],
                goal=EmojiType.INFINITY.value,
                resource=details['Target']
            ) for name, details in session_data.account.statues.items()
        ]
    }

    for category in advices:
        for advice in advices[category]:
            mark_advice_completed(advice)

    levels_ag = AdviceGroup(
        tier='',
        pre_string='Statue Effect multis and Statue bonuses',
        advices=advices,
        informational=True
    )
    levels_ag.remove_empty_subgroups()
    return levels_ag

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    statues_AdviceDict = {
        'Tiers': {}
    }
    info_tiers = 0
    true_max = true_max_tiers['Statues']
    max_tier = true_max - info_tiers
    tier_Statues = 0
    depositable_statues = 0

    # Assess Tiers
    for tier_number, requirements in statues_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        for statue_name, statue_details in session_data.account.statues.items():
            # Trying to futureproof new tiers - If at least Gold, but not the max tier
            farm_details = f": {statue_details['Farmer']}" if 0 <= statue_details['TypeNumber'] < len(statue_type_list) else ''
            farm_resource = statue_details['Target'] if 0 <= statue_details['TypeNumber'] < len(statue_type_list) else ''
            if statue_name in requirements.get('SpecificLevels', {}):
                if statue_details['Level'] < requirements['SpecificLevels'][statue_name]:
                    if (
                        subgroup_label not in statues_AdviceDict['Tiers']
                        and len(statues_AdviceDict['Tiers']) < session_data.account.max_subgroups
                    ):
                        statues_AdviceDict['Tiers'][subgroup_label] = []
                    if subgroup_label in statues_AdviceDict['Tiers']:
                        statues_AdviceDict['Tiers'][subgroup_label].append(Advice(
                            label=f"Level up {statue_name}{farm_details}",
                            picture_class=statue_name,
                            progression=statue_details['Level'],
                            goal=requirements['SpecificLevels'][statue_name],
                            resource=farm_resource
                        ))
            if statue_name in requirements.get('SpecificTypes', []):
                if statue_details['TypeNumber'] < requirements.get('MinStatueTypeNumber', 0):
                    if (
                        subgroup_label not in statues_AdviceDict['Tiers']
                        and len(statues_AdviceDict['Tiers']) < session_data.account.max_subgroups
                    ):
                        statues_AdviceDict['Tiers'][subgroup_label] = []
                    if subgroup_label in statues_AdviceDict['Tiers']:
                        statues_AdviceDict['Tiers'][subgroup_label].append(Advice(
                            label=f"Raise {statue_name} to {requirements.get('MinStatueType', 'UnknownStatueType')}"
                                  f"{farm_details if requirements.get('MinStatueType', 'UnknownStatueType') != 'Gold' else ''}"
                                  f"{'<br>Reminder: You need to raise this statue to Gold first!' if requirements.get('MinStatueType', 'UnknownStatueType') == 'Onyx' and statue_details['Level'] == 0 else ''}",
                            picture_class=statue_details['Image'],
                            progression=statue_details['TypeNumber'] if statue_details['TypeNumber'] < 1 else session_data.account.stored_assets.get(
                                statue_details['ItemName']).amount,
                            goal=20000 if requirements.get('MinStatueType', 'UnknownStatueType') == 'Onyx' else requirements.get(
                                'MinStatueTypeNumber', 0),
                            resource="coins" if requirements.get('MinStatueType', 'UnknownStatueType') == 'Gold' else farm_resource
                        ))
                    if session_data.account.stored_assets.get(statue_details['ItemName']).amount >= 20000 and statue_details['Type'] != statue_type_list[-1]:
                        depositable_statues += 1
        if subgroup_label not in statues_AdviceDict['Tiers'] and tier_Statues == tier_number - 1:
            tier_Statues = tier_number

    # Generate Alerts
    if depositable_statues > 0 and session_data.account.onyx_statues_unlocked:
        session_data.account.alerts_Advices['World 1'].append(Advice(
            label=f"You can upgrade {depositable_statues} {{{{ Statue{pl(depositable_statues)}|#statues }}}} to {statue_type_list[-1]}!",
            picture_class="town-marble"
        ))

    tiers_ag = AdviceGroup(
        tier=tier_Statues,
        pre_string='Beef up those statues',
        advices=statues_AdviceDict['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Statues)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getStatuesAdviceSection() -> AdviceSection:
    # Generate AdviceGroups
    statues_AdviceGroupDict = {}
    statues_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    if session_data.account.maxed_statues < statue_count:
        statues_AdviceGroupDict['Crystals'] = getPreOnyxAdviceGroup()
    statues_AdviceGroupDict['Current'] = getCurrentLevelsAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    statues_AdviceSection = AdviceSection(
        name='Statues',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Statues tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Town_Marble.gif',
        groups=statues_AdviceGroupDict.values()
    )

    return statues_AdviceSection
