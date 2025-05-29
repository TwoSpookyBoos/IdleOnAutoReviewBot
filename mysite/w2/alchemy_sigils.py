from flask import g as session_data

from consts.consts import ValueToMulti, break_you_best, build_subgroup_label
from consts.consts_idleon import lavaFunc
from consts.consts_w1 import stamp_maxes
from consts.consts_w2 import max_sigil_level, max_vial_level, arcade_max_level
from consts.consts_w5 import max_sailing_artifact_level
from consts.progression_tiers import sigils_progressionTiers
from consts.progression_tiers_updater import true_max_tiers
from models.models import AdviceGroup, Advice, AdviceSection
from utils.data_formatting import mark_advice_completed


def getSigilSpeedAdviceGroup(practical_maxed: bool) -> AdviceGroup:
    # Multi Group A = several
    peapod_values = [0, 25, 50, 100]
    chilled_yarn_multi = [1, 2, 3, 4, 5]
    player_peapod_value = (
        peapod_values[session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level']]
        * chilled_yarn_multi[session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']]
    )
    willow_vial_value = session_data.account.alchemy_vials['Willow Sippy (Willow Logs)']['Value']

    player_sigil_stamp_value = session_data.account.stamps['Sigil Stamp']['Total Value']
    goal_sigil_stamp_value = lavaFunc('decay', stamp_maxes['Sigil Stamp'], 40, 150)
    # The Sigil Stamp is a MISC stamp, thus isn't multiplied by the Lab bonus or Pristine Charm

    mga = ValueToMulti(
        (20 * session_data.account.achievements['Vial Junkee']['Complete'])
        + (20 * session_data.account.gemshop['Sigil Supercharge'])
        + player_peapod_value
        + willow_vial_value
        + player_sigil_stamp_value
    )
    mga_label = f"Multi Group A: {mga:.3f}x"

    # Multi Group B = Summoning Winner Bonuses
    bd = session_data.account.summoning['BattleDetails']
    player_matches_total = (
        bd['Green'][9]['RewardBaseValue'] * bd['Green'][9]['Defeated']
        + bd['Yellow'][5]['RewardBaseValue'] * bd['Yellow'][5]['Defeated']
        + bd['Blue'][5]['RewardBaseValue'] * bd['Blue'][5]['Defeated']
        + bd['Purple'][7]['RewardBaseValue'] * bd['Green'][7]['Defeated']
        + bd['Cyan'][3]['RewardBaseValue'] * bd['Green'][3]['Defeated']
    )
    matches_total = (
        bd['Green'][9]['RewardBaseValue']
        + bd['Yellow'][5]['RewardBaseValue']
        + bd['Blue'][5]['RewardBaseValue']
        + bd['Purple'][7]['RewardBaseValue']
        + bd['Cyan'][3]['RewardBaseValue']
    )
    mgb = ValueToMulti(matches_total * session_data.account.summoning['WinnerBonusesMultiFull'])
    mgb_label = f"Multi Group B: {mgb:.3f}x"

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

    total_multi = max(1, mga * mgb * mgc * mgd * mge)

    speed_Advice = {
        mga_label: [],
        mgb_label: [],
        mgc_label: [],
        mgd_label: [],
        mge_label: [],
    }

    # Multi Group A
    speed_Advice[mga_label].append(Advice(
        label=f"W2 Achievement: Vial Junkee: "
              f"+{20 * session_data.account.achievements['Vial Junkee']['Complete']}/20%",
        picture_class='vial-junkee',
        progression=int(session_data.account.achievements['Vial Junkee']['Complete']),
        goal=1
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Gem Shop|#gem-shop }}}}: Sigil Supercharge: "
              f"+{20 * session_data.account.gemshop['Sigil Supercharge']}/{20 * 10}%",
        picture_class='sigil-supercharge',
        progression=session_data.account.gemshop['Sigil Supercharge'],
        goal=10,
        completed=not practical_maxed
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"Sigil: Level {session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level']}"
              f" Pea Pod: +{player_peapod_value}/{peapod_values[-1] * chilled_yarn_multi[-1]}%",
        picture_class='pea-pod',
        progression=session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level'],
        goal=max_sigil_level
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Artifact|#sailing}}}}: Chilled Yarn: {chilled_yarn_multi[session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']]}"
              f"/{chilled_yarn_multi[-1]}x"
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
    speed_Advice[mga_label].append(Advice(
        label=f"Sigil Stamp: +{player_sigil_stamp_value:.3f}/{goal_sigil_stamp_value:.3f}%",
        picture_class='sigil-stamp',
        progression=session_data.account.stamps['Sigil Stamp']['Level'],
        goal=stamp_maxes['Sigil Stamp'],
        resource=session_data.account.stamps['Sigil Stamp']['Material'],
    ))

    # Multi Group B
    for color, battleNumber in {"Green": 9, "Yellow": 5, "Blue": 5, "Purple": 7, "Cyan": 3}.items():
        speed_Advice[mgb_label].append(Advice(
            label=f"Summoning match {color} {battleNumber}: "
                  f"+{session_data.account.summoning['BattleDetails'][color][battleNumber]['RewardBaseValue'] * session_data.account.summoning['BattleDetails'][color][battleNumber]['Defeated']}"
                  f"/{session_data.account.summoning['BattleDetails'][color][battleNumber]['RewardBaseValue']}",
            picture_class=session_data.account.summoning['BattleDetails'][color][battleNumber]['Image'],
            progression=1 if session_data.account.summoning['BattleDetails'][color][battleNumber]['Defeated'] else 0,
            goal=1
        ))
    speed_Advice[mgb_label].append(Advice(
        label=f"Summoning matches total: +{player_matches_total}/{matches_total}",
        picture_class='summoning',
        progression=player_matches_total,
        goal=matches_total
    ))
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        speed_Advice[mgb_label].append(advice)
    speed_Advice[mgb_label].extend(session_data.account.summoning['WinnerBonusesSummaryFull'])

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
    speed_Advice[mge_label].append(Advice(
        label=f"Arcade Bonus 43: {ab43['Display']}",
        picture_class=ab43['Image'],
        progression=ab43['Level'],
        goal=arcade_max_level + 1,
        resource=ab43['Material'],
    ))

    for group_name in speed_Advice:
        for advice in speed_Advice[group_name]:
            mark_advice_completed(advice)

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

    # Assess Tiers
    for tier_number, requirements in sigils_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        if 'Ionized Sigils' in requirements.get('Other', {}) and not session_data.account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']:
            if (
                subgroup_label not in sigils_Advices['Sigils']
                and len(sigils_Advices['Sigils']) < session_data.account.max_subgroups
            ):
                sigils_Advices['Sigils'][subgroup_label] = []
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
                if (
                    subgroup_label not in sigils_Advices['Sigils']
                    and len(sigils_Advices['Sigils']) < session_data.account.max_subgroups
                ):
                    sigils_Advices['Sigils'][subgroup_label] = []
                if subgroup_label in sigils_Advices['Sigils']:
                    sigils_Advices['Sigils'][subgroup_label].append(Advice(
                        label=f"Unlock {requiredSigil}",
                        picture_class=requiredSigil,
                        progression=f"{player_sigils[requiredSigil]['PlayerHours']:.2f}",
                        goal=player_sigils[requiredSigil]['Requirements'][requiredLevel - 1]
                    ))

        # Level Up unlocked Sigils
        for requiredSigil, requiredLevel in requirements.get('LevelUp', {}).items():
            if player_sigils[requiredSigil]['PrechargeLevel'] < requiredLevel:
                if (
                    subgroup_label not in sigils_Advices['Sigils']
                    and len(sigils_Advices['Sigils']) < session_data.account.max_subgroups
                ):
                    sigils_Advices['Sigils'][subgroup_label] = []
                if subgroup_label in sigils_Advices['Sigils']:
                    if player_sigils[requiredSigil]['PlayerHours'] < 100:
                        prog = f"{player_sigils[requiredSigil]['PlayerHours']:.2f}"
                    else:
                        prog = f"{player_sigils[requiredSigil]['PlayerHours']:.0f}"
                    sigils_Advices['Sigils'][subgroup_label].append(Advice(
                        label=f"Level up {requiredSigil}"
                              f"{'. Go look at the Sigils screen to redeem your level!' if player_sigils[requiredSigil]['PlayerHours'] > player_sigils[requiredSigil]['Requirements'][requiredLevel - 1] else ''}",
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
    highest_lab_level = max(session_data.account.all_skills['Lab'])
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
