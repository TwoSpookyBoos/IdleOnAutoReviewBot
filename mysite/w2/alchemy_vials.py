from models.models import AdviceSection, AdviceGroup, Advice
from utils.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import ValueToMulti, break_you_best, build_subgroup_label, AdviceType
from consts.consts_w2 import max_index_of_vials, max_vial_level, max_maxable_vials, vial_costs
from consts.progression_tiers import vials_progressionTiers, true_max_tiers

logger = get_logger(__name__)

def getVialsProgressionTiersAdviceGroup():
    vial_Advices = {
        'Early Vials': {},
        'Maxed Vials': {},
        'Vials to max next (preserves Greenstacks)': []
    }
    optional_tiers = 1
    true_max = true_max_tiers['Vials']
    max_tier = true_max - optional_tiers
    max_advices_per_group = session_data.account.max_subgroups * 3
    tier_TotalVialsUnlocked = 0
    tier_TotalVialsMaxed = 0

    player_alchemy_vials = session_data.account.alchemy_vials
    virile_vials_list = [vial_name for vial_name, vial_value in player_alchemy_vials.items() if vial_value['Level'] >= 4]
    max_expected_vv = max_index_of_vials - 4  # Exclude both pickle and both rare drop vials
    maxed_vials_list = [vial_name for vial_name, vial_value in player_alchemy_vials.items() if vial_value['Level'] >= max_vial_level]
    # unmaxed_vials_list = [vial_name for vial_name in player_alchemy_vials if vial_name not in maxed_vials_list]
    # lockedVialsList = [vial_name for vial_name, vialValue in player_alchemy_vials.items() if vialValue['Level'] == 0]
    unlocked_vials = sum(1 for vial in player_alchemy_vials.values() if vial['Level'] > 0)

    #Assess Tiers
    advice_TrailingMaxedVials = ''

    for tier_number, requirements in vials_progressionTiers.items():
        #tier[3] = list ParticularVialsMaxed
        subgroupName = build_subgroup_label(tier_number, max_tier)

        #Total Vials Unlocked
        if unlocked_vials < requirements.get('Unlocked', 0):
            add_subgroup_if_available_slot(vial_Advices['Early Vials'], subgroupName)
            if subgroupName in vial_Advices['Early Vials']:
                vial_Advices['Early Vials'][subgroupName].append(Advice(
                    label=f"Unlock {requirements.get('Unlocked', 0) - unlocked_vials} more "
                          f"vial{pl(requirements.get('Unlocked', 0) - unlocked_vials, '', 's')}",
                    picture_class='vial-1',
                    progression=unlocked_vials,
                    goal=requirements.get('Unlocked', 0),
                    optional=tier_number > max_tier
                ))
        if subgroupName not in vial_Advices['Early Vials'] and tier_TotalVialsUnlocked == tier_number - 1:
            tier_TotalVialsUnlocked = tier_number

        #Total Vials Maxed
        if len(maxed_vials_list) < requirements.get('Maxed', 0):
            if tier_TotalVialsMaxed >= 20:
                advice_TrailingMaxedVials += requirements.get('Notes', '')
            add_subgroup_if_available_slot(vial_Advices['Maxed Vials'], subgroupName)
            if subgroupName in vial_Advices['Maxed Vials']:
                vial_Advices['Maxed Vials'][subgroupName].append(Advice(
                    label=f"Max {requirements.get('Maxed', 0)} total vials",
                    picture_class="vial-13",
                    progression=len(maxed_vials_list),
                    goal=requirements.get('Maxed', 0)
                ))
        if subgroupName not in vial_Advices['Maxed Vials'] and tier_TotalVialsMaxed == tier_number - 1:
            tier_TotalVialsMaxed = tier_number

        #Particular Vials Maxed
        vials_shown_this_tier = False
        for required_vial in requirements.get('Recommended', []):
            if player_alchemy_vials[required_vial]['Level'] < max_vial_level:
                # Rule breaker here. Instead of requiring exact Vials per level, I only require a total amount.
                # So instead of the usual subgroup_label, I just display up to a particular number
                if (
                    len(vial_Advices['Vials to max next (preserves Greenstacks)']) < max_advices_per_group
                    or vials_shown_this_tier  #All vials in a tier are roughly the same difficulty, not perfectly ordered. Show 1, show all
                ):
                    vials_shown_this_tier = True
                    goal = int(vial_costs[player_alchemy_vials[required_vial]['Level']])
                    prog = 100 * ( max(0, session_data.account.all_assets.get(player_alchemy_vials[required_vial]['Material']).amount - 10_000_000) / max(1, goal))
                    # Generate Alerts
                    if prog >= 100 and player_alchemy_vials[required_vial]['Level'] == max_vial_level-1:
                        session_data.account.alerts_Advices['World 2'].append(Advice(
                            label=f"{required_vial} {{{{ Vial|#vials }}}} ready to be maxed!",
                            picture_class="vial-13"
                        ))
                    vial_Advices['Vials to max next (preserves Greenstacks)'].append(Advice(
                        label=f"{required_vial}"
                              f"{'<br>NEEDS TO BE UNLOCKED!' if player_alchemy_vials[required_vial]['Level'] == 0 else ''}"
                              f"{'<br>Ready for level ' if prog >= 100 else ' toward level '}"
                              f"{player_alchemy_vials[required_vial]['Level'] + 1 if prog >= 100 else player_alchemy_vials[required_vial]['Level'] + 1}",
                        picture_class=player_alchemy_vials[required_vial]['Image'],
                        progression=f"{min(1000, prog):.1f}{'+' if min(1000, prog) == 1000 else ''}",
                        goal=100,
                        unit='%'
                    ))

    vial_Advices['Maxed Vials']['Vials to max next (preserves Greenstacks)'] = vial_Advices['Vials to max next (preserves Greenstacks)']  #Ensure this is the last subgroup

    if len(virile_vials_list) < max_expected_vv:
        vial_Advices['Early Vials'][f"{AdviceType.INFO.value}- Shaman's Virile Vials"] = [
            Advice(
                label='Total level 4+ Vials',
                picture_class='vial-4',
                progression=len(virile_vials_list),
                goal=max_expected_vv,
                informational=True
            )
        ]

    #Generate AdviceGroups
    vial_AdviceGroupDict = {}
    vial_AdviceGroupDict['Total Unlocked Vials'] = AdviceGroup(
        tier=tier_TotalVialsUnlocked,
        pre_string='Early Vial Goals',
        post_string=(
            'For the most unlock chances per day, rapidly drop multiple stacks of items on the cauldron!'
            if len(vial_Advices['Early Vials']) > 1 else ''
        ),
        advices=vial_Advices['Early Vials'],
    )

    vial_AdviceGroupDict['Total Maxed Vials'] = AdviceGroup(
        tier=tier_TotalVialsMaxed,
        pre_string='Late Vial Goals',
        post_string=advice_TrailingMaxedVials,
        advices=vial_Advices['Maxed Vials'],
    )

    for ag in vial_AdviceGroupDict:
        vial_AdviceGroupDict[ag].remove_empty_subgroups()

    overall_SectionTier = min(true_max, tier_TotalVialsUnlocked, tier_TotalVialsMaxed)
    return vial_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getVialBonusesAdviceGroup() -> AdviceGroup:
    #Player's values
    total = session_data.account.alchemy_vials_calcs['Total Multi']

    max_mga = session_data.account.vault['Upgrades']['Vial Overtune']['Max Value'] + (0.02 * max_maxable_vials)
    max_mgb = session_data.account.labBonuses['My 1st Chemistry Set']['BaseValue']
    max_total = max_mga * max_mgb

    vb_advices = {
        f"Total: {total:.2f}x": [
            Advice(
                label=f"Total Vial Effect bonus: {total:.2f}x",
                picture_class='vial-1',
                progression=f"{total:.2f}",
                goal=f"{max_total:.2f}",
                unit='x'
            )
        ],
        f"Multi Group A: {session_data.account.alchemy_vials_calcs['mga']:.2f}x": [
            Advice(
                label=f"{{{{ Upgrade Vault|#upgrade-vault }}}}: Vial Overtune: +{session_data.account.vault['Upgrades']['Vial Overtune']['Level'] * session_data.account.vault['Upgrades']['Vial Overtune']['Value Per Level']}%",
                picture_class=session_data.account.vault['Upgrades']['Vial Overtune']['Image'],
                progression=session_data.account.vault['Upgrades']['Vial Overtune']['Level'],
                goal=session_data.account.vault['Upgrades']['Vial Overtune']['Max Level']
            ),
            Advice(
                label=f"{{{{ Rift|#rift}}}}: Vial Mastery: +{(2 * session_data.account.maxed_vials) if session_data.account.rift['VialMastery'] else 0}%",
                picture_class='vial-mastery',
                progression=int(session_data.account.rift['VialMastery']),
                goal=1
            ),
            Advice(
                label=f"You have {session_data.account.maxed_vials}/{max_maxable_vials} maxed Vials",
                picture_class='vial-13',
                progression=session_data.account.maxed_vials,
                goal=max_maxable_vials
            )
        ],
        f"Multi Group B: {session_data.account.alchemy_vials_calcs['mgb']:.2f}x": [
            Advice(
                label=f"Lab Bonus: My 1st Chemistry Set: {session_data.account.labBonuses['My 1st Chemistry Set']['Value']}x",
                picture_class="my-1st-chemistry-set",
                progression=int(session_data.account.labBonuses['My 1st Chemistry Set']['Enabled']),
                goal=1
            )
        ]
    }

    for subgroup in vb_advices:
        for advice in vb_advices[subgroup]:
            mark_advice_completed(advice)

    vb_ag = AdviceGroup(
        tier='',
        pre_string='Sources of bonus Vial Effect',
        advices=vb_advices,
        informational=True
    )
    return vb_ag

def getAlchemyVialsAdviceSection() -> AdviceSection:
    highestAlchemyLevel = max(session_data.account.all_skills['Alchemy'])
    if highestAlchemyLevel < 1:
        vial_AdviceSection = AdviceSection(
            name='Vials',
            tier='Not Yet Evaluated',
            header='Come back after unlocking the Alchemy skill in World 2!',
            picture='data/aVials1.png',
            unreached=True
        )
        return vial_AdviceSection

    #Generate AdviceGroups
    vial_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getVialsProgressionTiersAdviceGroup()
    vial_AdviceGroupDict['Vial Bonuses'] = getVialBonusesAdviceGroup()

    #Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    vial_AdviceSection = AdviceSection(
        name='Vials',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Vial tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='data/aVials1.png',
        groups=vial_AdviceGroupDict.values()
    )
    return vial_AdviceSection
