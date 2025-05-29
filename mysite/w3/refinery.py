from flask import g as session_data
from consts.consts import break_keep_it_up
from consts.progression_tiers_updater import true_max_tiers
from models.emoji_type import EmojiType
from models.models import AdviceSection, AdviceGroup, Advice
from math import floor, ceil
from utils.logging import get_logger

logger = get_logger(__name__)

class Salt:
    def __init__(self, salt_name: str, auto_refine: int, salt_rank: int, next_salt_rank: int, previousSalt, merit_purchased: bool = True, running: bool = False):
        self.salt_name: str = salt_name
        self.salt_rank: int = salt_rank
        self.auto_refine: int = auto_refine
        self.max_rank_with_excess: int = salt_rank
        self.merit_purchased: bool = merit_purchased
        self.running: bool = running
        if self.merit_purchased is True:
            self.salt_consumption_scaling: float = 1.3
        else:
            self.salt_consumption_scaling: float = 1.5
        if salt_name in session_data.account.refinery:
            self.image: str = session_data.account.refinery[salt_name]['Image']
            self.cycles_per_Synthesis_cycle: int = session_data.account.refinery[salt_name]['CyclesPerSynthCycle']
            self.consumption_of_previous_salt: int = session_data.account.refinery[salt_name]['PreviousSaltConsumption']
            self.next_salt_consumption: int = session_data.account.refinery[salt_name]['NextSaltConsumption']
            self.next_salt_cycles_per_Synthesis_cycle: int = session_data.account.refinery[salt_name]['NextSaltCyclesPerSynthCycle']
            self.output: int = int(floor(self.salt_rank ** 1.3)) * self.cycles_per_Synthesis_cycle
            if next_salt_rank != 0:
                self.consumed: int = int(floor(next_salt_rank ** self.salt_consumption_scaling) * self.next_salt_consumption * self.next_salt_cycles_per_Synthesis_cycle)
            else:
                self.consumed: int = 0
            self.excess: bool = self.output >= self.consumed
            if self.excess:
                self.excess_or_deficit: str = "excess"
            else:
                self.excess_or_deficit: str = "deficit"
            self.excess_amount: int = self.output - self.consumed
            if previousSalt is not None:
                if previousSalt.excess is True:
                    if next_salt_rank != 0 or salt_name == 'Nullo':
                        self.max_rank_with_excess: int = max(0, ceil(
                            (previousSalt.output /
                             (self.consumption_of_previous_salt * self.cycles_per_Synthesis_cycle)) ** (1 / self.salt_consumption_scaling)) - 1)
                    if self.max_rank_with_excess >= salt_rank:
                        self.canBeLeveled = True
                    else:
                        self.max_rank_with_excess = salt_rank
                        self.canBeLeveled = False
                else:
                    self.max_rank_with_excess = salt_rank
                    self.canBeLeveled = False

    def __str__(self) -> str:
        return self.salt_name

    def __bool__(self) -> bool:
        return self.excess

def getSaltDict() -> dict[str, Salt]:
    saltDict = {}
    saltDict['RedSalt'] = Salt(
        salt_name='Red',
        auto_refine=session_data.account.refinery['Red']['AutoRefine'],
        salt_rank=session_data.account.refinery['Red']['Rank'],
        next_salt_rank=session_data.account.refinery['Orange']['Rank'],
        previousSalt=None,
        merit_purchased=True,
        running=session_data.account.refinery['Red']['Running'],
    )
    saltDict['OrangeSalt'] = Salt(
        salt_name='Orange',
        auto_refine=session_data.account.refinery['Orange']['AutoRefine'],
        salt_rank=session_data.account.refinery['Orange']['Rank'],
        next_salt_rank=session_data.account.refinery['Blue']['Rank'],
        previousSalt=saltDict['RedSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 1,
        running=session_data.account.refinery['Orange']['Running'],
    )
    saltDict['BlueSalt'] = Salt(
        salt_name='Blue',
        auto_refine=session_data.account.refinery['Blue']['AutoRefine'],
        salt_rank=session_data.account.refinery['Blue']['Rank'],
        next_salt_rank=session_data.account.refinery['Green']['Rank'],
        previousSalt=saltDict['OrangeSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 2,
        running=session_data.account.refinery['Blue']['Running'],
    )
    saltDict['GreenSalt'] = Salt(
        salt_name='Green',
        auto_refine=session_data.account.refinery['Green']['AutoRefine'],
        salt_rank=session_data.account.refinery['Green']['Rank'],
        next_salt_rank=session_data.account.refinery['Purple']['Rank'],
        previousSalt=saltDict['BlueSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 3,
        running=session_data.account.refinery['Green']['Running'],
    )
    saltDict['PurpleSalt'] = Salt(
        salt_name='Purple',
        auto_refine=session_data.account.refinery['Purple']['AutoRefine'],
        salt_rank=session_data.account.refinery['Purple']['Rank'],
        next_salt_rank=session_data.account.refinery['Nullo']['Rank'],
        previousSalt=saltDict['GreenSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 4,
        running=session_data.account.refinery['Purple']['Running'],
    )
    saltDict['NulloSalt'] = Salt(
        salt_name='Nullo',
        auto_refine=session_data.account.refinery['Nullo']['AutoRefine'],
        salt_rank=session_data.account.refinery['Nullo']['Rank'],
        next_salt_rank=0,
        previousSalt=saltDict['PurpleSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 5,
        running=session_data.account.refinery['Nullo']['Running'],
    )
    return saltDict

def getRefineryProgressionTierAdviceGroups():
    refinery_AdviceDict = {
        'AutoRefine': [],
        'Merits': [],
        'ExcessAndDeficits': [],
        'Tab1Ranks': [],
        'Tab2Ranks': [],
    }
    refinery_AdviceGroupDict = {}
    optional_tiers = 0
    true_max = true_max_tiers['Refinery']
    max_tier = true_max - optional_tiers
    tier_AutoRefine = 1
    tier_W3Merits = 1
    salt_dict: dict[str, Salt] = getSaltDict()

    # AutoRefine and On/Off Advice
    if not salt_dict['RedSalt'].running:
        if salt_dict['RedSalt'].salt_rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{salt_dict['RedSalt'].salt_name} is not producing",
                picture_class=salt_dict['RedSalt'].image,
                progression='Off',
                goal='On')
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} is not producing",
                picture_class=salt_dict['RedSalt'].image
            ))
    if salt_dict['RedSalt'].auto_refine != 0:
        if salt_dict['RedSalt'].salt_rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(
                Advice(label=salt_dict['RedSalt'].salt_name, picture_class=salt_dict['RedSalt'].image,
                       progression=salt_dict['RedSalt'].auto_refine, goal=0, unit="%")
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} auto-refining early. Recommended to at least reach Rank 100 before auto-refining early.",
                picture_class=salt_dict['RedSalt'].image
            ))

    if not salt_dict['GreenSalt'].running:
        if salt_dict['GreenSalt'].salt_rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{salt_dict['GreenSalt'].salt_name} is not producing",
                picture_class=salt_dict['GreenSalt'].image,
                progression='Off',
                goal='On')
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} is not producing",
                picture_class=salt_dict['GreenSalt'].image
            ))
    if salt_dict['GreenSalt'].auto_refine != 0:
        if salt_dict['GreenSalt'].salt_rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(
                Advice(label=salt_dict['GreenSalt'].salt_name, picture_class=salt_dict['GreenSalt'].image,
                       progression=salt_dict['GreenSalt'].auto_refine, goal=0, unit="%")
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} auto-refining early. Recommended to at least reach Rank 30 before auto-refining early.",
                picture_class=salt_dict['GreenSalt'].image
            ))

    # W3Merits Advice
    sum_salts_rank2_plus = 0
    if salt_dict['OrangeSalt'].salt_rank >= 2:
        sum_salts_rank2_plus += 1
    if salt_dict['BlueSalt'].salt_rank >= 2:
        sum_salts_rank2_plus += 1
    if salt_dict['GreenSalt'].salt_rank >= 2:
        sum_salts_rank2_plus += 1
    if salt_dict['PurpleSalt'].salt_rank >= 2:
        sum_salts_rank2_plus += 1
    if salt_dict['NulloSalt'].salt_rank >= 2:
        sum_salts_rank2_plus += 1
    if session_data.account.merits[2][6]['Level'] < sum_salts_rank2_plus:
        tier_W3Merits = 0
        refinery_AdviceDict['Merits'].append(Advice(
                label='W3 Taskboard Merits Purchased',
                picture_class='iceland-irwin',
                progression=session_data.account.merits[2][6]['Level'],
                goal=sum_salts_rank2_plus
        ))

    # Excess and Deficits Advice
    refinery_AdviceDict['ExcessAndDeficits'].append(Advice(
        label=f"Red Salt {salt_dict['RedSalt'].excess_or_deficit}",
        picture_class=salt_dict['RedSalt'].image,
        goal=f"{salt_dict['RedSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict['ExcessAndDeficits'].append(Advice(
        label=f"Orange Salt {salt_dict['OrangeSalt'].excess_or_deficit}",
        picture_class=salt_dict['OrangeSalt'].image,
        goal=f"{salt_dict['OrangeSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict['ExcessAndDeficits'].append(Advice(
        label=f"Blue Salt {salt_dict['BlueSalt'].excess_or_deficit}",
        picture_class=salt_dict['BlueSalt'].image,
        goal=f"{salt_dict['BlueSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict['ExcessAndDeficits'].append(Advice(
        label=f"Green Salt {salt_dict['GreenSalt'].excess_or_deficit}",
        picture_class=salt_dict['GreenSalt'].image,
        goal=f"{salt_dict['GreenSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict['ExcessAndDeficits'].append(Advice(
        label=f"Purple Salt {salt_dict['PurpleSalt'].excess_or_deficit}",
        picture_class=salt_dict['PurpleSalt'].image,
        goal=f"{salt_dict['PurpleSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict['ExcessAndDeficits'].append(Advice(
        label=f"Nullo Salt {salt_dict['NulloSalt'].excess_or_deficit}",
        picture_class=salt_dict['NulloSalt'].image,
        goal=f"{salt_dict['NulloSalt'].excess_amount:,}"
    ))

    # Ranks Advice
    refinery_AdviceDict['Tab1Ranks'].append(Advice(
        label='Red Salt',
        picture_class=salt_dict['RedSalt'].image,
        progression=salt_dict['RedSalt'].salt_rank,
        goal=EmojiType.INFINITY.value
    ))
    refinery_AdviceDict['Tab1Ranks'].append(Advice(
        label='Orange Salt',
        picture_class=salt_dict['OrangeSalt'].image,
        progression=salt_dict['OrangeSalt'].salt_rank,
        goal=salt_dict['OrangeSalt'].max_rank_with_excess
    ))
    refinery_AdviceDict['Tab1Ranks'].append(Advice(
        label='Blue Salt',
        picture_class=salt_dict['BlueSalt'].image,
        progression=salt_dict['BlueSalt'].salt_rank,
        goal=salt_dict['BlueSalt'].max_rank_with_excess
    ))
    refinery_AdviceDict['Tab2Ranks'].append(Advice(
        label='Green Salt',
        picture_class=salt_dict['GreenSalt'].image,
        progression=salt_dict['GreenSalt'].salt_rank,
        goal=EmojiType.INFINITY.value
    ))
    refinery_AdviceDict['Tab2Ranks'].append(Advice(
        label='Purple Salt',
        picture_class=salt_dict['PurpleSalt'].image,
        progression=salt_dict['PurpleSalt'].salt_rank,
        goal=salt_dict['PurpleSalt'].max_rank_with_excess
    ))
    refinery_AdviceDict['Tab2Ranks'].append(Advice(
        label='Nullo Salt',
        picture_class=salt_dict['NulloSalt'].image,
        progression=salt_dict['NulloSalt'].salt_rank,
        goal=salt_dict['NulloSalt'].max_rank_with_excess
    ))

    # Generate AdviceGroups
    refinery_AdviceGroupDict['AutoRefine'] = AdviceGroup(
        tier=tier_AutoRefine,
        pre_string="Red and Green Salts should always be set to 0% Auto-Refine and On to produce salts",
        advices=refinery_AdviceDict['AutoRefine']
    )
    refinery_AdviceGroupDict['Merits'] = AdviceGroup(
        tier=tier_W3Merits,
        pre_string='W3 Salt Merits Purchased',
        advices=refinery_AdviceDict['Merits'],
        post_string='Leveling this Merit would immediately decrease salt consumption.'
    )
    refinery_AdviceGroupDict['ExcessAndDeficits'] = AdviceGroup(
        tier='',
        pre_string='Salt Excess/Deficit per Synthesis Cycle',
        advices=refinery_AdviceDict['ExcessAndDeficits'],
        informational=True,
        completed=all([int(advice.goal.replace(',', '')) >= 0 for advice in refinery_AdviceDict['ExcessAndDeficits']])
    )
    refinery_AdviceGroupDict['Tab1Ranks'] = AdviceGroup(
        tier='',
        pre_string='Max Tab1 Ranks without causing a Salt Deficit',
        advices=refinery_AdviceDict['Tab1Ranks'],
        post_string=f"Or just YOLO rank up everything if balancing is too much of a pain {EmojiType.WIDE_SHRUG.value}",
        informational=True,
        completed=all([advice.progression >= advice.goal for advice in refinery_AdviceDict['Tab1Ranks']])
    )
    refinery_AdviceGroupDict['Tab2Ranks'] = AdviceGroup(
        tier='',
        pre_string='Max Tab2 Ranks without causing a Salt Deficit',
        advices=refinery_AdviceDict['Tab2Ranks'],
        post_string='',
        informational=True,
        completed=all([advice.progression >= advice.goal for advice in refinery_AdviceDict['Tab2Ranks']])
    )
    overall_SectionTier = min(true_max, tier_AutoRefine, tier_W3Merits)
    return refinery_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getConsRefineryAdviceSection() -> AdviceSection:
    highest_construction_level = max(session_data.account.all_skills['Construction'])
    if highest_construction_level < 1:
        return AdviceSection(
            name='Refinery',
            tier='Not Yet Evaluated',
            header='Come back after unlocking the Construction skill in World 3!',
            picture='Construction_Refinery.gif',
            unreached=True
        )

    #Generate AdviceGroups
    refinery_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getRefineryProgressionTierAdviceGroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    return AdviceSection(
        name='Refinery',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Refinery tier met: {tier_section}{break_keep_it_up if overall_SectionTier >= max_tier else ''}",
        picture='Construction_Refinery.gif',
        groups=refinery_AdviceGroupDict.values(),
        collapse=False
    )
