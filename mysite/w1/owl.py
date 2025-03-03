from models.models import Advice, AdviceGroup, AdviceSection
from consts.consts_autoreview import break_you_best, build_subgroup_label, EmojiType, ValueToMulti
from consts.progression_tiers import owl_progressionTiers, true_max_tiers
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getNoFeathersGeneratingAlert():
    if session_data.account.owl['FeatherGeneration'] < 1:
        alert_advice = Advice(
            label='Find the Owl in W1 and start generating Feathers!'
            if not session_data.account.owl['Discovered']
            else f"You aren't generating any {{{{ Owl|#owl }}}} Feathers!",
            picture_class='feather-generation'
        )
        session_data.account.alerts_Advices['World 1'].append(alert_advice)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    owl_AdviceDict = {
        "MegaFeathers": {}
    }
    infoTiers = 1
    true_max = true_max_tiers['Owl']
    max_tier = true_max - infoTiers
    tier_MegaFeathers = 0

    featherResetsDict = {
        0: 6, 1: 6, 2: 7, 3: 8, 4: 9,
        5: 11, 6: 12, 7: 11, 8: 12, 9: 14,
        10: 16, 11: 17, 12: 18, 13: 19, 14: 21,
        15: 22, 16: 23, 17: 24, 18: 25, 19: 27,
        20: 28, 21: 29, 22: 30, 23: 31, 24: 32
    }
    orionDRValues = {
        23: 40, 29: 67.5
    }

    #Assess Tiers
    lastMFShown = -1
    for tier_number, requirements in owl_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        if 'MegaFeathersOwned' in requirements:
            if session_data.account.owl['MegaFeathersOwned'] < requirements['MegaFeathersOwned'] + 1:
                for mf, resets in featherResetsDict.items():
                    if lastMFShown < mf <= requirements['MegaFeathersOwned']:
                        if session_data.account.owl['MegaFeathersOwned'] <= mf:
                            add_subgroup_if_available_slot(owl_AdviceDict['MegaFeathers'], subgroup_label)
                            if subgroup_label in owl_AdviceDict['MegaFeathers']:
                                lastMFShown = mf
                                owl_AdviceDict['MegaFeathers'][subgroup_label].append(Advice(
                                    label=f"MF{mf+1}: Restart {resets} times first",
                                    picture_class=f"megafeather-{mf}" if mf < 10 else "the-great-mega-reset",
                                    progression=session_data.account.owl['FeatherRestarts'] if session_data.account.owl['MegaFeathersOwned'] == mf else 0,
                                    goal=resets
                                ))
        if 'BonusesOfOrion' in requirements:
            if session_data.account.owl['BonusesOfOrion'] < requirements['BonusesOfOrion']:
                add_subgroup_if_available_slot(owl_AdviceDict['MegaFeathers'], subgroup_label)
                if subgroup_label in owl_AdviceDict['MegaFeathers']:
                    orion_advice = Advice(
                            label=f"Before MF{requirements['MegaFeathersOwned']+1}, purchase Bonuses of Orion {requirements['BonusesOfOrion']}",
                            picture_class='bonuses-of-orion',
                            progression=session_data.account.owl['BonusesOfOrion'],
                            goal=requirements['BonusesOfOrion']
                        )
                    if len(owl_AdviceDict['MegaFeathers']) > 0:
                        owl_AdviceDict['MegaFeathers'][subgroup_label].insert(-1, orion_advice)
                    else:
                        owl_AdviceDict['MegaFeathers'][subgroup_label].append(orion_advice)
                    owl_AdviceDict['MegaFeathers'][subgroup_label].append(Advice(
                        label=f"{orionDRValues.get(requirements['BonusesOfOrion'], 'IDK')}% Drop Rate will then be yours {EmojiType.TADA.value}",
                        picture_class='drop-rate'
                    ))

        if subgroup_label not in owl_AdviceDict['MegaFeathers'] and tier_MegaFeathers == tier_number - 1:
            tier_MegaFeathers = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_MegaFeathers,
        pre_string='Collect Mega Feathers and Bonuses of Orion',
        advices=owl_AdviceDict['MegaFeathers'],
    )
    overall_SectionTier = min(true_max, tier_MegaFeathers)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getUpgradeSequenceLinks() -> AdviceGroup:
    secret_owl_bonus = session_data.account.vault['Upgrades']['Go Go Secret Owl']['Total Value']
    gambit_bonus = ValueToMulti(session_data.account.caverns['Caverns']['Gambit']['Bonuses'][8]['Value'])

    def make_link(target, group_by_seconds, fresh_restart):
        params = {}
        params['target'] = target
        params['mega_reset'] = session_data.account.owl['MegaFeathersOwned']
        if fresh_restart:
            params['restart'] = session_data.account.owl['FeatherRestarts']+1
        else:
            params['restart'] = session_data.account.owl['FeatherRestarts']
        params['shiny_feather_count'] = session_data.account.owl['ShinyFeathers']
        params['group_by_seconds'] = group_by_seconds
        params['ignore_less_than'] = 0 # TODO: Remove?
        params['gambit'] = gambit_bonus
        params['secret_owl'] = secret_owl_bonus
        params['orion'] = session_data.account.owl['BonusesOfOrion']
        if fresh_restart:
            params['feather_gen'] = 1
        else:
            params['feather_gen'] = session_data.account.owl['FeatherGeneration']
            params['feather_mult'] = session_data.account.owl['FeatherMultiplier']
            params['cheapener'] = session_data.account.owl['FeatherCheapener']
            params['super_production'] = session_data.account.owl['SuperFeatherProduction']
            params['shiny_feather_level'] = session_data.account.owl['ShinyFeatherLevel']
            params['super_cheapener'] = session_data.account.owl['SuperFeatherCheapener']
            params['feathers'] = session_data.account.owl['Feathers']

        return 'dynamic-owl-calc?' + '&'.join(f'{key}={val}' for key, val in params.items())

    linksDict = {
        'Restart Links': [
            Advice(
                label=f'<a href="{make_link(target="restart", group_by_seconds=0, fresh_restart=False)}">Optimize path to Restart</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="restart", group_by_seconds=1, fresh_restart=False)}">Optimize path to Restart (group by 1 second)</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="restart", group_by_seconds=0, fresh_restart=True)}">Optimize next Restart</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="restart", group_by_seconds=1, fresh_restart=True)}">Optimize next Restart (group by 1 second)</a>',
                picture_class='bonuses-of-orion'
            ),
        ],
        'Mega Reset Links': [
            Advice(
                label=f'<a href="{make_link(target="mega_reset", group_by_seconds=0, fresh_restart=False)}">Optimize path to Mega Reset</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="mega_reset", group_by_seconds=1, fresh_restart=False)}">Optimize path to Mega Reset (group by 1 second)</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="mega_reset", group_by_seconds=0, fresh_restart=True)}">Optimize path to Mega Reset (next restart)</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="mega_reset", group_by_seconds=1, fresh_restart=True)}">Optimize path to Mega Reset (group by 1 second, next restart)</a>',
                picture_class='bonuses-of-orion'
            ),
        ],
        'Bonuses of Orion Links': [
            Advice(
                label=f'<a href="{make_link(target="orion", group_by_seconds=0, fresh_restart=False)}">Optimize path to Bonuses of Orion</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="orion", group_by_seconds=1, fresh_restart=False)}">Optimize path to Bonuses of Orion (group by 1 second)</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="orion", group_by_seconds=0, fresh_restart=True)}">Optimize path to Bonuses of Orion (next restart)</a>',
                picture_class='bonuses-of-orion'
            ),
            Advice(
                label=f'<a href="{make_link(target="orion", group_by_seconds=1, fresh_restart=True)}">Optimize path to Bonuses of Orion (group by 1 second, next restart)</a>',
                picture_class='bonuses-of-orion'
            ),
        ]
    }

    return AdviceGroup(
        tier='',
        pre_string='Upgrade Sequence Links',
        advices=linksDict,
        informational=True
    )

def getOwlAdviceSection() -> AdviceSection:
    # Generate Alert Advice
    getNoFeathersGeneratingAlert()

    # Generate AdviceGroups
    owl_AdviceGroupDict = {}
    owl_AdviceGroupDict['MegaFeathers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    owl_AdviceGroupDict['Links'] = getUpgradeSequenceLinks()

    # Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    owl_AdviceSection = AdviceSection(
        name="Owl",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Owl tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Owl.gif',
        groups=owl_AdviceGroupDict.values()
    )
    return owl_AdviceSection

import collections
import functools

OwlUpgrades = collections.namedtuple('OwlUpgrades',
                                     ('feather_gen', 'orion', 'feather_mult',
                                      'cheapener', 'restart', 'super_production',
                                      'shiny_feather', 'super_cheapener', 'mega_reset'))

UPGRADE_BASE_COST_FACTORS = OwlUpgrades(5, 350, 500,
                                        3000, 1000000, 2000000,
                                        5000000, 50000000, 250000000000)
UPGRADE_COST_EXP_BASES = OwlUpgrades(1.1, 25, 1.11,
                                     1.16, 14, 1.12,
                                     1.4, 1.27, 20)

UPGRADE_NAMES = OwlUpgrades('Feather Generation', 'Bonuses of Orion', 'Feather Multiplier',
                            'Feather Cheapener', 'Feather Restart', 'Super Feather Production',
                            'Shiny Feather', 'Super Feather Cheapener', 'The Great Mega Reset')

def _calc_feathers_per_second(upgrade_levels, shiny_feather_count, owl_multiplier):
    feathers_per_sec = 0

    feathers_per_sec += upgrade_levels.feather_gen

    if upgrade_levels.mega_reset >= 5:
        feathers_per_sec += 2 * upgrade_levels.cheapener
        feathers_per_sec += 4 * upgrade_levels.super_cheapener

    feathers_per_sec += 5 * upgrade_levels.super_production

    if upgrade_levels.feather_mult > 0:
        feathers_per_sec *= 1 + (upgrade_levels.feather_mult * 0.05)

    if upgrade_levels.shiny_feather > 0 and shiny_feather_count > 0:
        feathers_per_sec *= 1 + (upgrade_levels.shiny_feather * shiny_feather_count) / 100

    if upgrade_levels.restart > 0:
        if upgrade_levels.mega_reset >= 7:
            feathers_per_sec *= (5 ** upgrade_levels.restart)
        else:
            feathers_per_sec *= (3 ** upgrade_levels.restart)

    if upgrade_levels.mega_reset >= 1:
        feathers_per_sec *= 10

    return feathers_per_sec * owl_multiplier

def _calc_upgrade_costs(upgrade_levels):
    upgrade_costs = []

    discount = 1

    # Cheapeners
    discount *= 1 / (1 + upgrade_levels.cheapener/10)
    discount *= 1 / (1 + upgrade_levels.super_cheapener/5)

    # Mega feather 3 - upgrades cost 1% less per feather gen level
    if upgrade_levels.mega_reset >= 3:
        discount *= 1 / (1 + upgrade_levels.feather_gen/100)

    for idx, count in enumerate(upgrade_levels):
        base = UPGRADE_BASE_COST_FACTORS[idx]
        exp_base = UPGRADE_COST_EXP_BASES[idx]

        if idx == 0:
            # Feather gen is special
            base *= count
            if upgrade_levels.mega_reset >= 9:
                exp_base = 1.075

        upgrade_costs.append(base * pow(exp_base, count) * discount)

    return OwlUpgrades(*upgrade_costs)

class OwlState:
    def __init__(self, upgrade_levels, shiny_feather_count, owl_multiplier):
        self.upgrade_levels = upgrade_levels
        self.shiny_feather_count = shiny_feather_count
        self.owl_multiplier = owl_multiplier

        self.feathers_per_second = _calc_feathers_per_second(upgrade_levels,
                                                            shiny_feather_count,
                                                            owl_multiplier)

        self.upgrade_costs = _calc_upgrade_costs(upgrade_levels)

    def time_to_upgrade_by_idx(self, upgrade_idx, current_feathers=0):
        return max((self.upgrade_costs[upgrade_idx] - current_feathers) / self.feathers_per_second,
                   0)

    def time_to_upgrade(self, upgrade_name, current_feathers=0):
        return max((getattr(self.upgrade_costs, upgrade_name) - current_feathers) / self.feathers_per_second,
                   0)

    def time_to_orion(self, current_feathers=0):
        return self.time_to_upgrade('orion', current_feathers)

    def time_to_restart(self, current_feathers=0):
        return self.time_to_upgrade('restart', current_feathers)

    def time_to_mega_reset(self, current_feathers=0):
        return self.time_to_upgrade('mega_reset', current_feathers)

    # This contract is maybe icky, operating by index
    def return_upgraded_state(self, idx):
        name = OwlUpgrades._fields[idx]
        count = self.upgrade_levels[idx]
        d = {name: count+1}
        return OwlState(self.upgrade_levels._replace(**d),
                        self.shiny_feather_count,
                        self.owl_multiplier)

def _optimize_upgrades(state, target, current_feathers, group_by_seconds, ignore_less_than):
    theoretical_time = 0
    upgrades = []

    while True:
        time_to_upgrade = state.time_to_upgrade(target, current_feathers)

        best_improvement_ratio = 0
        this_upgrade_time = None
        next_state = None
        next_current_feathers = None
        this_name = None
        this_idx = None

        for idx in range(9):
            if idx in (1, 4, 8):
                continue # Don't try to upgrade orion, restart, or reset

            upgrade_time = state.time_to_upgrade_by_idx(idx, current_feathers)

            if upgrade_time >= time_to_upgrade:
                continue

            test_state = state.return_upgraded_state(idx)
            test_current_feathers = max(current_feathers - state.upgrade_costs[idx], 0)
            total_time = upgrade_time + test_state.time_to_upgrade(target, test_current_feathers)

            if total_time >= time_to_upgrade:
                continue

            savings = time_to_upgrade - total_time
            if savings < ignore_less_than:
                continue

            improvement_ratio = savings / state.upgrade_costs[idx]

            if improvement_ratio > best_improvement_ratio:
                best_improvement_ratio = improvement_ratio
                next_state = test_state
                next_current_feathers = test_current_feathers
                this_upgrade_time = upgrade_time
                this_name = OwlUpgrades._fields[idx]
                this_idx = idx

        if next_state is None:
            return theoretical_time + state.time_to_upgrade(target, current_feathers), state, upgrades

        state = next_state
        current_feathers = next_current_feathers
        theoretical_time += this_upgrade_time
        upgrades.append((this_name, this_upgrade_time))

        # Keep upgrade while each level is
        # <group_by_seconds second to upgrade
        while True:
            upgrade_time = state.time_to_upgrade_by_idx(this_idx, current_feathers)
            if upgrade_time > group_by_seconds:
                break

            test_state = state.return_upgraded_state(this_idx)
            test_current_feathers = max(current_feathers - state.upgrade_costs[idx], 0)
            total_time = upgrade_time + test_state.time_to_upgrade(target, test_current_feathers)

            if total_time >= time_to_upgrade:
                break

            savings = time_to_upgrade - total_time
            if savings < ignore_less_than:
                break

            state = test_state
            current_feathers = test_current_feathers
            theoretical_time += upgrade_time
            upgrades.append((this_name, upgrade_time))

def runDynamicOwlCalc(request_args):
    target = request_args['target']

    target_pretty_name = {
        'restart': 'Restart',
        'mega_reset': 'Mega Reset',
        'orion': 'Bonuses of Orion',
    }[target]

    initial_upgrade_levels = OwlUpgrades(
        int(request_args.get('feather_gen', '0')),
        int(request_args.get('orion', '0')),
        int(request_args.get('feather_mult', '0')),
        int(request_args.get('cheapener', '0')),
        int(request_args.get('restart', '0')),
        int(request_args.get('super_production', '0')),
        int(request_args.get('shiny_feather_level', '0')),
        int(request_args.get('super_cheapener', '0')),
        int(request_args.get('mega_reset', '0'))
    )
    shiny_feather_count = int(request_args.get('shiny_feather_count', '0'))
    secret_owl = float(request_args.get('secret_owl', '0'))
    gambit = float(request_args.get('gambit', '1.0'))
    current_feathers = int(float(request_args.get('feathers', '0')))

    group_by_seconds = float(request_args.get('group_by_seconds', '1'))
    ignore_less_than = float(request_args.get('ignore_less_than', '0')) # TODO: Drop?

    owl_multiplier = gambit * (1 + secret_owl / 100)

    state = OwlState(initial_upgrade_levels, shiny_feather_count, owl_multiplier)

    yield f'Current time to {target_pretty_name}:'

    seconds = state.time_to_upgrade(target, current_feathers)
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24

    yield f'{seconds} seconds'
    yield f'{minutes} minutes'
    yield f'{hours} hours'
    yield f'{days} days'

    theory_time, optimized, upgrade_order = _optimize_upgrades(state, target, current_feathers, group_by_seconds, ignore_less_than)

    yield ''
    yield ''
    yield 'Target upgrades:'
    for name, count in zip(UPGRADE_NAMES, optimized.upgrade_levels):
        yield f'{name}: {count}'

    yield ''
    yield ''
    yield f'Theoretical time: {theory_time} seconds'
    yield f'Theoretical time: {theory_time/60} minutes'
    yield f'Theoretical time: {theory_time/60/60} hours'
    yield f'Theoretical time: {theory_time/60/60/24} days'

    yield ''
    yield 'Upgrade path:'

    last_upgrade = None
    current_delta = 0
    upgrade_counts = collections.Counter()

    for name, count in zip(OwlUpgrades._fields, initial_upgrade_levels):
        if count != 0:
            upgrade_counts[name] = count

    for upgrade_name, _ in upgrade_order:
        if upgrade_name != last_upgrade and last_upgrade is not None:
            yield f'{last_upgrade} to {upgrade_counts[last_upgrade]} (delta of {current_delta})'
            current_delta = 0
        last_upgrade = upgrade_name
        upgrade_counts[upgrade_name] += 1
        current_delta += 1

    if last_upgrade is not None: # In case of no upgrades
        yield f'{last_upgrade} to {upgrade_counts[last_upgrade]} (delta of {current_delta})'

    # TODO: Return the upgrade sequence as JSON, including meta info such as "time left buying upgrades", "time to target upgrade", "remaining savings"
    # TODO: Of course, this requires a proper UI exposure too!
