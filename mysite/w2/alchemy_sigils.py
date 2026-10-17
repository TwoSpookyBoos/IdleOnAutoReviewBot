from collections import defaultdict

from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.progression_tiers import sigils_progressionTiers, true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.number_formatting import round_and_trim
from utils.text_formatting import pl
from utils.logging import get_logger

logger = get_logger(__name__)

def getSigilSpeedAdviceGroup(practical_maxed: bool) -> AdviceGroup:
    sigils = session_data.account.alchemy_p2w.sigils
    willow_vial = session_data.account.alchemy_vials['Willow Sippy (Willow Logs)']
    summoning_bonus = session_data.account.summoning.bonuses["Sigil SPD"]
    tuttle_vial = session_data.account.alchemy_vials['Turtle Tisane (Tuttle)']
    ballot_buff = session_data.account.ballot[17]

    mga_label = f"Multi Group A: {sigils.speed_multi_a:.3f}x"
    mgb_label = f"Summoning: {round_and_trim(sigils.speed_multi_b)}x"
    mgc_label = f"Multi Group C: {sigils.speed_multi_c:.3f}x"
    mgd_label = f"Multi Group D: {sigils.speed_multi_d:.3f}x"
    mge_label = f"Multi Group E: {sigils.speed_multi_e:.3f}x"
    mgf_label = f"Multi Group F: {round_and_trim(sigils.speed_multi_f)}x"

    speed_Advice = {
        mga_label: [],
        mgb_label: [],
        mgc_label: [],
        mgd_label: [],
        mge_label: [],
        mgf_label: [],
    }

    # Multi Group A
    speed_Advice[mga_label].append(sigils.get_vial_junkee_advice())
    sigil_supercharge = session_data.account.gemshop.purchases['Sigil Supercharge']
    gsss_advice = sigil_supercharge.get_advice(
        additional_text=f": +{20 * sigil_supercharge.owned}/{20 * sigil_supercharge.max_level}%"
    )
    gsss_advice.completed = not practical_maxed
    speed_Advice[mga_label].append(gsss_advice)
    speed_Advice[mga_label].append(sigils.get_peapod_advice())
    speed_Advice[mga_label].append(sigils.get_chilled_yarn_advice())
    speed_Advice[mga_label].append(willow_vial.get_advice(f"+{willow_vial.value:.3f}"))
    speed_Advice[mga_label].append(session_data.account.stamps['Sigil Stamp'].get_advice())

    # Multi Group B
    speed_Advice[mgb_label].append(summoning_bonus.get_bonus_advice())

    # Multi Group C
    speed_Advice[mgc_label].append(tuttle_vial.get_advice(f"{sigils.speed_multi_c:.3f}x"))

    # Multi Group D
    speed_Advice[mgd_label].append(ballot_buff.get_bonus_advice())

    # Multi Group E
    speed_Advice[mge_label].append(session_data.account.arcade[43].get_advice())

    # Multi Group F
    speed_Advice[mgf_label].append(session_data.account.legend_talents['Big Sig Fig'].get_advice())

    for group_name in speed_Advice:
        for advice in speed_Advice[group_name]:
            advice.mark_advice_completed()

    speed_AdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Sources of Sigil Charging Speed. Grand total: {sigils.speed_multi:.3f}x",
        advices=speed_Advice,
        informational=True,
    )
    return speed_AdviceGroup

def getSigilsProgressionTiersAdviceGroup():
    sigils_Advices = {
        'Sigils': {}
    }
    optional_tiers = 6
    true_max = true_max_tiers['Sigils']
    max_tier = true_max - optional_tiers
    tier_Sigils = 0
    player_sigils = session_data.account.alchemy_p2w.sigils
    player_sigil_assignments = defaultdict(lambda: 0)
    for char in session_data.account.characters.safe:
        if char.alchemy_job_group == 'Sigils':
            player_sigil_assignments[char.alchemy_job_string] += 1

    # Assess Tiers
    for tier_number, requirements in sigils_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        if (
            "Ionized Sigils" in requirements.get("Other", {})
            and not session_data.account.sneaking.emporium["Ionized Sigils"].obtained
        ):
            add_subgroup_if_available_slot(sigils_Advices['Sigils'], subgroup_label)
            if subgroup_label in sigils_Advices['Sigils']:
                sigils_Advices['Sigils'][subgroup_label].append(
                    session_data.account.sneaking.emporium['Ionized Sigils'].get_obtained_advice()
                )
        # Unlock new Sigils
        for requiredSigil, requiredLevel in requirements.get('Unlock', {}).items():
            if player_sigils[requiredSigil].precharge_level < requiredLevel:
                add_subgroup_if_available_slot(sigils_Advices['Sigils'], subgroup_label)
                has_chars_assigned = player_sigil_assignments[requiredSigil] > 0
                info_text = ''
                if has_chars_assigned:
                    info_text = f' (Being unlocked by {player_sigil_assignments[requiredSigil]} character{pl(player_sigil_assignments[requiredSigil])})'
                if subgroup_label in sigils_Advices['Sigils']:
                    sigils_Advices['Sigils'][subgroup_label].append(Advice(
                        label=f"Unlock {requiredSigil}{info_text}",
                        picture_class=requiredSigil,
                        progression=f"{player_sigils[requiredSigil].player_hours:.2f}",
                        goal=player_sigils[requiredSigil].requirements[requiredLevel - 1]
                    ))

        # Level Up unlocked Sigils
        for requiredSigil, requiredLevel in requirements.get('LevelUp', {}).items():
            if player_sigils[requiredSigil].precharge_level < requiredLevel:
                add_subgroup_if_available_slot(sigils_Advices['Sigils'], subgroup_label)
                if subgroup_label in sigils_Advices['Sigils']:
                    if player_sigils[requiredSigil].player_hours < 100:
                        prog = f"{player_sigils[requiredSigil].player_hours:.2f}"
                    else:
                        prog = f"{player_sigils[requiredSigil].player_hours:.0f}"
                    sigil_level_ready = player_sigils[requiredSigil].player_hours > player_sigils[requiredSigil].requirements[requiredLevel - 1]
                    has_chars_assigned = player_sigil_assignments[requiredSigil] > 0
                    info_text = ''
                    if has_chars_assigned:
                        info_text = f' (Being leveled by {player_sigil_assignments[requiredSigil]} character{pl(player_sigil_assignments[requiredSigil])})'
                    if sigil_level_ready:
                        info_text = '. Go look at the Sigils screen to redeem your level!'
                    sigils_Advices['Sigils'][subgroup_label].append(Advice(
                        label=f"Level up {requiredSigil}{info_text}",
                        picture_class=f"{requiredSigil}-{requiredLevel}",
                        progression=f"{0 if requiredLevel > player_sigils[requiredSigil].precharge_level + 1 else prog}",
                        goal=f"{player_sigils[requiredSigil].requirements[requiredLevel - 1]}"
                    ))

        if tier_Sigils == tier_number - 1 and subgroup_label not in sigils_Advices['Sigils']:
            tier_Sigils = tier_number

    # Generate AdviceGroups
    sigils_AdviceGroupDict = {}
    sigils_AdviceGroupDict['Sigils'] = AdviceGroup(
        tier=tier_Sigils,
        pre_string=f"Unlock and level {'all' if tier_Sigils >= max_tier else 'important'} Sigils",
        advices=sigils_Advices['Sigils'],
    )
    overall_SectionTier = min(true_max, tier_Sigils)
    return sigils_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getAlchemySigilsAdviceSection() -> AdviceSection:
    highest_lab_level = max(session_data.account.characters.all_skills['Laboratory'])
    if highest_lab_level < 1:
        sigils_AdviceSection = AdviceSection(
            name='Sigils',
            tier="Not Yet Evaluated",
            header='Come back after unlocking the Laboratory skill in World 4!',
            picture='Sigils.png',
            unreached=True
        )
        return sigils_AdviceSection
    sigils_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getSigilsProgressionTiersAdviceGroup()
    sigils_AdviceGroupDict['Speed'] = getSigilSpeedAdviceGroup(overall_SectionTier >= max_tier)

    # #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    sigils_AdviceSection = AdviceSection(
        name='Sigils',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Sigils tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Sigils.png',
        groups=sigils_AdviceGroupDict.values()
    )
    return sigils_AdviceSection
