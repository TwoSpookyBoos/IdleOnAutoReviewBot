from consts.progression_tiers import true_max_tiers, grimoire_progressionTiers
from models.general.session_data import session_data

from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, build_subgroup_label
from utils.text_formatting import pl

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup(grimoire) -> tuple[dict[str, AdviceGroup], int, int, int]:
    grimoire_Advices = {
        'Total Upgrades': {},
        'Specific Upgrades': {},
        'Stacks': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['The Grimoire']
    max_tier = true_max - optional_tiers
    tier_TotalUpgrades = 0
    tier_SpecificUpgrades = 0
    tier_Stacks = 0

    #Assess Tiers
    for tier_number, requirements in grimoire_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        #Total Upgrades
        if grimoire.total_upgrades < requirements.get('Total Upgrades', 0):
            add_subgroup_if_available_slot(grimoire_Advices['Total Upgrades'], subgroup_label)
            if subgroup_label in grimoire_Advices['Total Upgrades']:
                grimoire_Advices['Total Upgrades'][subgroup_label].append(
                    grimoire.get_total_upgrades_tier_advice(requirements.get('Total Upgrades', 0))
                )
        if subgroup_label not in grimoire_Advices['Total Upgrades'] and tier_TotalUpgrades == tier_number - 1:
            tier_TotalUpgrades = tier_number

        #Specific Upgrades - account-wide talents
        for upgrade_name, required_level in requirements.get('Specific Upgrades', {}).items():
            upgrade_details = grimoire.upgrades.get(upgrade_name)
            current_level = upgrade_details.level if upgrade_details else 0
            if current_level < required_level:
                add_subgroup_if_available_slot(grimoire_Advices['Specific Upgrades'], subgroup_label)
                if subgroup_label in grimoire_Advices['Specific Upgrades']:
                    grimoire_Advices['Specific Upgrades'][subgroup_label].append(
                        grimoire.get_specific_upgrade_tier_advice(upgrade_name, required_level)
                    )
        if subgroup_label not in grimoire_Advices['Specific Upgrades'] and tier_SpecificUpgrades == tier_number - 1:
            tier_SpecificUpgrades = tier_number

        #Stacks - Knockout/Elimination/Annihilation
        for stack_type, required_stacks in requirements.get('Stacks', {}).items():
            current_stacks = grimoire.stacks.get(stack_type, 0)
            if current_stacks < required_stacks:
                add_subgroup_if_available_slot(grimoire_Advices['Stacks'], subgroup_label)
                if subgroup_label in grimoire_Advices['Stacks']:
                    grimoire_Advices['Stacks'][subgroup_label].append(
                        grimoire.get_stacks_tier_advice(stack_type, required_stacks)
                    )
        if subgroup_label not in grimoire_Advices['Stacks'] and tier_Stacks == tier_number - 1:
            tier_Stacks = tier_number

    #Generate AdviceGroups
    grimoire_AdviceGroupDict = {}
    grimoire_AdviceGroupDict['Total Upgrades'] = AdviceGroup(
        tier=tier_TotalUpgrades,
        pre_string='Purchase more Total Grimoire Upgrades',
        advices=grimoire_Advices['Total Upgrades'],
    )
    grimoire_AdviceGroupDict['Specific Upgrades'] = AdviceGroup(
        tier=tier_SpecificUpgrades,
        pre_string=f"Level up the following account-wide Grimoire Upgrade{pl(grimoire_Advices['Specific Upgrades'])}",
        advices=grimoire_Advices['Specific Upgrades'],
    )
    grimoire_AdviceGroupDict['Stacks'] = AdviceGroup(
        tier=tier_Stacks,
        pre_string='Build up the following Knockout/Elimination/Annihilation Stacks',
        advices=grimoire_Advices['Stacks'],
        post_string='Stack targets rotate through a fixed monster order',
    )

    overall_SectionTier = min(true_max, tier_TotalUpgrades, tier_SpecificUpgrades, tier_Stacks)
    return grimoire_AdviceGroupDict, overall_SectionTier, max_tier, true_max


def getGrimoireCurrenciesAdviceGroup(grimoire) -> AdviceGroup:
    currency_advices = {
        'Currencies': [],
    }
    currency_advices['Currencies'].append(grimoire.get_total_bones_collected_advice())
    currency_advices['Currencies'].append(grimoire.get_charred_bones_advice())
    currency_advices['Currencies'] += grimoire.get_bone_advices()

    #Bone Multi calculation groups
    currency_advices['Currencies'].append(grimoire.get_bone_multi_advice())

    mga_label = f"Bone Multi Group A: {grimoire.bone_multi.mga:.2f}x"
    currency_advices[mga_label] = [
        session_data.account.sneaking.pristine_charms[
            'Glimmerchain'
        ].get_obtained_advice()
    ]

    mgb_label = f"Bone Multi Group B: {grimoire.bone_multi.mgb:.3f}x"
    currency_advices[mgb_label] = [grimoire.get_grimoire_talent_advice()]

    mgc_label = f"Bone Multi Group C: {grimoire.bone_multi.mgc:.2f}x"
    currency_advices[mgc_label] = [
        session_data.account.caverns.caves['Gambit'].bonuses[12].get_bonus_advice()
    ]

    mgd_label = f"Bone Multi Group D: {grimoire.bone_multi.mgd:.2f}x"
    currency_advices[mgd_label] = [grimoire.get_hood_advice()]

    mge_label = f"Bone Multi Group E: {grimoire.bone_multi.mge:.2f}x"
    currency_advices[mge_label] = []
    currency_advices[mge_label].append(grimoire.upgrades["Bones o' Plenty"].get_advice(grimoire.total_upgrades))
    bh = grimoire.upgrades['Bovinae Hoarding']
    bh_stacks_text = grimoire.get_bovinae_stacks_text()
    currency_advices[mge_label].append(bh.get_advice(grimoire.total_upgrades, bh_stacks_text))
    currency_advices[mge_label].append(session_data.account.arcade[40].get_advice())

    currency_advices[mge_label].append(
        session_data.account.lab_jewels['Deadly Wrath Jewel'].get_bonus_advice()
    )

    mgf_label = f"Bone Multi Group F: {grimoire.bone_multi.mgf:.2f}x"
    currency_advices[mgf_label] = [
        grimoire.get_graveyard_shift_advice(),
        grimoire.get_tombstone_stacks_advice(),
    ]

    mgg_label = f"Bone Multi Group G: {grimoire.bone_multi.mgg:.2f}x"
    currency_advices[mgg_label] = [
        session_data.account.emperor["Deathbringer Extra Bones"].get_bonus_advice()
    ]

    for subgroup in currency_advices:
        for advice in currency_advices[subgroup]:
            advice.mark_advice_completed()

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
    upgrades_AdviceDict['Upgrades'] = [grimoire.get_total_upgrades_advice()]
    upgrades_AdviceDict['Upgrades'] += [
        upgrade_details.get_advice(grimoire.total_upgrades) for upgrade_details in grimoire.upgrades.values()
    ]

    for subgroup in upgrades_AdviceDict:
        for advice in upgrades_AdviceDict[subgroup]:
            advice.mark_advice_completed()

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
    if 'Death Bringer' not in session_data.account.characters.classes:
        grimoire_AdviceSection = AdviceSection(
            name="The Grimoire",
            tier="Not Yet Evaluated",
            header="Come back after unlocking a Death Bringer in World 6!",
            picture='customized/Wraith.gif',
            unrated=True,
            unreached=session_data.account.world_progress.highest_reached < 6,
            completed=False
        )
        return grimoire_AdviceSection

    grimoire = session_data.account.grimoire
    #Generate Alert Advice

    #Generate AdviceGroups
    grimoire_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup(grimoire)
    grimoire_AdviceGroupDict['Currencies'] = getGrimoireCurrenciesAdviceGroup(grimoire)
    grimoire_AdviceGroupDict['Upgrades'] = getGrimoireUpgradesAdviceGroup(grimoire)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    grimoire_AdviceSection = AdviceSection(
        name='The Grimoire',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Grimoire tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Wraith.gif',
        groups=grimoire_AdviceGroupDict.values(),
        completed=None,
    )

    return grimoire_AdviceSection
