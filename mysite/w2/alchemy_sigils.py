from collections import defaultdict

from consts.consts_autoreview import ValueToMulti, break_you_best, build_subgroup_label
from consts.idleon.lava_func import lava_func
from consts.w1.stamps import stamp_maxes
from consts.consts_w2 import max_sigil_level, max_vial_level, sigils_dict
from consts.consts_w5 import max_sailing_artifact_level
from consts.progression_tiers import sigils_progressionTiers, true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.models_util import get_gem_shop_purchase_advice, get_summoning_bonus_advice, get_legend_talent_advice
from models.advice.generators.w2 import get_arcade_advice

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.number_formatting import round_and_trim
from utils.text_formatting import pl
from utils.logging import get_logger

logger = get_logger(__name__)

chilled_yarn_multi = [1, 2, 3, 4, 5, 6]

def get_max_chilled_yarn_multi():
    return max(chilled_yarn_multi)

def get_chilled_yarn_multi(artifact_level: int) -> int:
    # TODO: Ideally, sailing['Artifacts'] would know its own value and not need calculation here
    try:
        return chilled_yarn_multi[artifact_level]
    except:
        logger.error(f"Failed to calculate Chilled Yarn level of {artifact_level}. Returning max value of {max(chilled_yarn_multi)}")
        return get_max_chilled_yarn_multi()

def getSigilSpeedAdviceGroup(practical_maxed: bool) -> AdviceGroup:
    # "SigilBonusSpeed" in source. Last updated in v2.49 Dec 24 2025
    # Multi Group A = several
    peapod_values = sigils_dict['Pea Pod']['Values']
    player_peapod_value = (
            peapod_values[session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level']]
            * get_chilled_yarn_multi(session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'])
    )
    willow_vial_value = session_data.account.alchemy_vials['Willow Sippy (Willow Logs)']['Value']

    player_sigil_stamp_value = session_data.account.stamps['Sigil Stamp'].total_value
    goal_sigil_stamp_value = lava_func('decay', stamp_maxes['Sigil Stamp'], 40, 150)
    # The Sigil Stamp is a MISC stamp, thus isn't multiplied by the Lab bonus or Pristine Charm

    mga = ValueToMulti(
        (20 * session_data.account.achievements['Vial Junkee']['Complete'])
        + (20 * session_data.account.gemshop['Purchases']['Sigil Supercharge']['Owned'])
        + player_peapod_value
        + willow_vial_value
        + player_sigil_stamp_value
    )
    mga_label = f"Multi Group A: {mga:.3f}x"

    # Multi Group B = Summoning Winner Bonuses
    mgb = session_data.account.summoning['Bonuses']['<x Sigil SPD']['Value']
    mgb_label = f"Summoning: {round_and_trim(mgb)}x"

    # Multi Group C = Tuttle Vial
    tuttle_vial_multi = ValueToMulti(session_data.account.alchemy_vials['Turtle Tisane (Tuttle)']['Value'])
    mgc = tuttle_vial_multi
    mgc_label = f"Multi Group C: {mgc:.3f}x"

    # Multi Group D = Bonus Ballot
    ballot_active = session_data.account.ballot['CurrentBuff'] == 17
    if ballot_active:
        ballot_status = 'is Active'
    elif not ballot_active and session_data.account.ballot['CurrentBuff'] != 0:
        ballot_status = 'is Inactive'
    else:
        ballot_status = 'status is not available in provided data'
    ballot_multi = ValueToMulti(session_data.account.ballot['Buffs'][17]['Value'])
    ballot_multi_active = max(1, ballot_multi * ballot_active)

    mgd = ballot_multi_active
    mgd_label = f"Multi Group D: {mgd:.3f}x"

    # Multi Group E = Arcade
    ab43 = session_data.account.arcade[43]
    mge = ValueToMulti(ab43['Value'])
    mge_label = f"Multi Group E: {mge:.3f}x"

    # Multi Group F = Legend Talents
    mgf = ValueToMulti(session_data.account.legend_talents['Talents']['Big Sig Fig']['Value'])
    mgf_label = f"Multi Group F: {round_and_trim(mgf)}x"

    total_multi = max(1, mga * mgb * mgc * mgd * mge * mgf)

    speed_Advice = {
        mga_label: [],
        mgb_label: [],
        mgc_label: [],
        mgd_label: [],
        mge_label: [],
        mgf_label: [],
    }

    # Multi Group A
    speed_Advice[mga_label].append(Advice(
        label=f"W2 Achievement: Vial Junkee: "
              f"+{20 * session_data.account.achievements['Vial Junkee']['Complete']}/20%",
        picture_class='vial-junkee',
        progression=int(session_data.account.achievements['Vial Junkee']['Complete']),
        goal=1
    ))
    gsss_advice = get_gem_shop_purchase_advice(
        purchase_name='Sigil Supercharge',
        link_to_section=True,
        secondary_label=(
            f": +{20 * session_data.account.gemshop['Purchases']['Sigil Supercharge']['Owned']}/"
            f"{20 * session_data.account.gemshop['Purchases']['Sigil Supercharge']['MaxLevel']}%"
        )
    )
    gsss_advice.completed = not practical_maxed
    speed_Advice[mga_label].append(gsss_advice)
    speed_Advice[mga_label].append(Advice(
        label=f"Sigil: Level {session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level']}"
              f" Pea Pod: +{player_peapod_value}/{peapod_values[-1] * get_max_chilled_yarn_multi()}%",
        picture_class='pea-pod',
        progression=session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level'],
        goal=max_sigil_level
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Artifact|#sailing}}}}: Chilled Yarn: {get_chilled_yarn_multi(session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'])}"
              f"/{get_max_chilled_yarn_multi()}x"
              f"<br>(Already applied to Pea Pod Sigil above)",
        picture_class='chilled-yarn',
        progression=session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'],
        goal=max_sailing_artifact_level
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Willow Sippy (Willow Logs): +{willow_vial_value:.3f}",
        picture_class='willow-logs',
        progression=session_data.account.alchemy_vials['Willow Sippy (Willow Logs)']['Level'],
        goal=max_vial_level
    ))
    speed_Advice[mga_label].append(session_data.account.stamps['Sigil Stamp'].get_advice())

    # Multi Group B
    speed_Advice[mgb_label].append(get_summoning_bonus_advice('<x Sigil SPD'))

    # Multi Group C
    speed_Advice[mgc_label].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Turtle Tisane (Tuttle): {tuttle_vial_multi:.3f}x",
        picture_class='tuttle',
        progression=session_data.account.alchemy_vials['Turtle Tisane (Tuttle)']['Level'],
        goal=max_vial_level
    ))

    # Multi Group D
    speed_Advice[mgd_label].append(Advice(
        label=f"Weekly {{{{ Ballot|#bonus-ballot }}}}: {ballot_multi_active:.3f}/{ballot_multi:.3f}x"
              f"<br>(Buff {ballot_status})",
        picture_class='ballot-17',
        progression=int(ballot_active),
        goal=1,
        completed=True
    ))

    # Multi Group E
    speed_Advice[mge_label].append(get_arcade_advice(43))

    # Multi Group F
    speed_Advice[mgf_label].append(get_legend_talent_advice('Big Sig Fig'))

    for group_name in speed_Advice:
        for advice in speed_Advice[group_name]:
            advice.mark_advice_completed()

    speed_AdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Sources of Sigil Charging Speed. Grand total: {total_multi:.3f}x",
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
    player_sigils = session_data.account.alchemy_p2w['Sigils']
    player_sigil_assignments = defaultdict(lambda: 0)
    for char in session_data.account.safe_characters:
        if char.alchemy_job_group == 'Sigils':
            player_sigil_assignments[char.alchemy_job_string] += 1

    # Assess Tiers
    for tier_number, requirements in sigils_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        if 'Ionized Sigils' in requirements.get('Other', {}) and not session_data.account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']:
            add_subgroup_if_available_slot(sigils_Advices['Sigils'], subgroup_label)
            if subgroup_label in sigils_Advices['Sigils']:
                sigils_Advices['Sigils'][subgroup_label].append(Advice(
                    label=f"{{{{ Jade Emporium|#sneaking }}}}: Purchase Ionized Sigils to unlock Red sigils",
                    picture_class='ionized-sigils',
                    progression=int(session_data.account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']),
                    goal=1
                ))
        # Unlock new Sigils
        for requiredSigil, requiredLevel in requirements.get('Unlock', {}).items():
            if player_sigils[requiredSigil]['PrechargeLevel'] < requiredLevel:
                add_subgroup_if_available_slot(sigils_Advices['Sigils'], subgroup_label)
                has_chars_assigned = player_sigil_assignments[requiredSigil] > 0
                info_text = ''
                if has_chars_assigned:
                    info_text = f' (Being unlocked by {player_sigil_assignments[requiredSigil]} character{pl(player_sigil_assignments[requiredSigil])})'
                if subgroup_label in sigils_Advices['Sigils']:
                    sigils_Advices['Sigils'][subgroup_label].append(Advice(
                        label=f"Unlock {requiredSigil}{info_text}",
                        picture_class=requiredSigil,
                        progression=f"{player_sigils[requiredSigil]['PlayerHours']:.2f}",
                        goal=player_sigils[requiredSigil]['Requirements'][requiredLevel - 1]
                    ))

        # Level Up unlocked Sigils
        for requiredSigil, requiredLevel in requirements.get('LevelUp', {}).items():
            if player_sigils[requiredSigil]['PrechargeLevel'] < requiredLevel:
                add_subgroup_if_available_slot(sigils_Advices['Sigils'], subgroup_label)
                if subgroup_label in sigils_Advices['Sigils']:
                    if player_sigils[requiredSigil]['PlayerHours'] < 100:
                        prog = f"{player_sigils[requiredSigil]['PlayerHours']:.2f}"
                    else:
                        prog = f"{player_sigils[requiredSigil]['PlayerHours']:.0f}"
                    sigil_level_ready = player_sigils[requiredSigil]['PlayerHours'] > player_sigils[requiredSigil]['Requirements'][requiredLevel - 1]
                    has_chars_assigned = player_sigil_assignments[requiredSigil] > 0
                    info_text = ''
                    if has_chars_assigned:
                        info_text = f' (Being leveled by {player_sigil_assignments[requiredSigil]} character{pl(player_sigil_assignments[requiredSigil])})'
                    if sigil_level_ready:
                        info_text = '. Go look at the Sigils screen to redeem your level!'
                    sigils_Advices['Sigils'][subgroup_label].append(Advice(
                        label=f"Level up {requiredSigil}{info_text}",
                        picture_class=f"{requiredSigil}-{requiredLevel}",
                        progression=f"{0 if requiredLevel > player_sigils[requiredSigil]['PrechargeLevel'] + 1 else prog}",
                        goal=f"{player_sigils[requiredSigil]['Requirements'][requiredLevel - 1]}"
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
    highest_lab_level = max(session_data.account.all_skills['Laboratory'])
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
