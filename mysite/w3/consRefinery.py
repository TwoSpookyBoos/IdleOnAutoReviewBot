from flask import g as session_data
from consts import break_keep_it_up, infinity_string
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
                             (self.consumption_of_previous_salt * self.cycles_per_Synthesis_cycle)) ** (1 / self.salt_consumption_scaling))- 1)
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
        "AutoRefine": [],
        "Merits": [],
        "ExcessAndDeficits": [],
        "Tab1Ranks": [],
        "Tab2Ranks": [],
    }
    refinery_AdviceGroupDict = {}
    info_tiers = 0
    max_tier = 1 - info_tiers  #Pass or Fail
    tier_AutoRefine = 1
    tier_W3Merits = 1
    saltDict: dict[str, Salt] = getSaltDict()

    # AutoRefine and On/Off Advice
    if not saltDict['RedSalt'].running:
        if saltDict['RedSalt'].salt_rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{saltDict['RedSalt'].salt_name} is not producing",
                picture_class=saltDict['RedSalt'].image,
                progression='Off',
                goal='On')
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} is not producing",
                picture_class=saltDict['RedSalt'].image
            ))
    if saltDict['RedSalt'].auto_refine != 0:
        if saltDict['RedSalt'].salt_rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(
                Advice(label=saltDict['RedSalt'].salt_name, picture_class=saltDict['RedSalt'].image,
                       progression=saltDict['RedSalt'].auto_refine, goal=0, unit="%")
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} auto-refining early. Recommended to at least reach Rank 100 before auto-refining early.",
                picture_class=saltDict['RedSalt'].image
            ))

    if not saltDict['GreenSalt'].running:
        if saltDict['GreenSalt'].salt_rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{saltDict['GreenSalt'].salt_name} is not producing",
                picture_class=saltDict['GreenSalt'].image,
                progression='Off',
                goal='On')
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} is not producing",
                picture_class=saltDict['GreenSalt'].image
            ))
    if saltDict['GreenSalt'].auto_refine != 0:
        if saltDict['GreenSalt'].salt_rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(
                Advice(label=saltDict['GreenSalt'].salt_name, picture_class=saltDict['GreenSalt'].image,
                       progression=saltDict['GreenSalt'].auto_refine, goal=0, unit="%")
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} auto-refining early. Recommended to at least reach Rank 30 before auto-refining early.",
                picture_class=saltDict['GreenSalt'].image
            ))

    # W3Merits Advice
    sum_SaltsRank2Plus = 0
    if saltDict['OrangeSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if saltDict['BlueSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if saltDict['GreenSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if saltDict['PurpleSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if saltDict['NulloSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if session_data.account.merits[2][6]['Level'] < sum_SaltsRank2Plus:
        tier_W3Merits = 0
        refinery_AdviceDict["Merits"].append(
            Advice(
                label="W3 Taskboard Merits Purchased",
                picture_class="iceland-irwin",
                progression=session_data.account.merits[2][6]['Level'],
                goal=sum_SaltsRank2Plus)
        )

    # Excess and Deficits Advice
    refinery_AdviceDict["ExcessAndDeficits"].append(Advice(
        label=f"Red Salt {saltDict['RedSalt'].excess_or_deficit}",
        picture_class=saltDict['RedSalt'].image,
        goal=f"{saltDict['RedSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict["ExcessAndDeficits"].append(Advice(
        label=f"Orange Salt {saltDict['OrangeSalt'].excess_or_deficit}",
        picture_class=saltDict['OrangeSalt'].image,
        goal=f"{saltDict['OrangeSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict["ExcessAndDeficits"].append(Advice(
        label=f"Blue Salt {saltDict['BlueSalt'].excess_or_deficit}",
        picture_class=saltDict['BlueSalt'].image,
        goal=f"{saltDict['BlueSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict["ExcessAndDeficits"].append(Advice(
        label=f"Green Salt {saltDict['GreenSalt'].excess_or_deficit}",
        picture_class=saltDict['GreenSalt'].image,
        goal=f"{saltDict['GreenSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict["ExcessAndDeficits"].append(Advice(
        label=f"Purple Salt {saltDict['PurpleSalt'].excess_or_deficit}",
        picture_class=saltDict['PurpleSalt'].image,
        goal=f"{saltDict['PurpleSalt'].excess_amount:,}"
    ))
    refinery_AdviceDict["ExcessAndDeficits"].append(Advice(
        label=f"Nullo Salt {saltDict['NulloSalt'].excess_or_deficit}",
        picture_class=saltDict['NulloSalt'].image,
        goal=f"{saltDict['NulloSalt'].excess_amount:,}"
    ))

    # Ranks Advice
    refinery_AdviceDict["Tab1Ranks"].append(
        Advice(label="Red Salt", picture_class=saltDict['RedSalt'].image, progression=saltDict['RedSalt'].salt_rank, goal=infinity_string)
    )
    refinery_AdviceDict["Tab1Ranks"].append(
        Advice(label="Orange Salt", picture_class=saltDict['OrangeSalt'].image, progression=saltDict['OrangeSalt'].salt_rank,
               goal=saltDict['OrangeSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Tab1Ranks"].append(
        Advice(label="Blue Salt", picture_class=saltDict['BlueSalt'].image, progression=saltDict['BlueSalt'].salt_rank,
               goal=saltDict['BlueSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Tab2Ranks"].append(
        Advice(label="Green Salt", picture_class=saltDict['GreenSalt'].image, progression=saltDict['GreenSalt'].salt_rank, goal=infinity_string)
    )
    refinery_AdviceDict["Tab2Ranks"].append(
        Advice(label="Purple Salt", picture_class=saltDict['PurpleSalt'].image, progression=saltDict['PurpleSalt'].salt_rank,
               goal=saltDict['PurpleSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Tab2Ranks"].append(
        Advice(label="Nullo Salt", picture_class=saltDict['NulloSalt'].image, progression=saltDict['NulloSalt'].salt_rank,
               goal=saltDict['NulloSalt'].max_rank_with_excess)
    )

    # Generate AdviceGroups
    refinery_AdviceGroupDict['AutoRefine'] = AdviceGroup(
        tier=str(tier_AutoRefine),
        pre_string="Red and Green Salts should always be set to 0% Auto-Refine and On to produce salts",
        advices=refinery_AdviceDict['AutoRefine'],
        post_string=""
    )
    refinery_AdviceGroupDict['Merits'] = AdviceGroup(
        tier=str(tier_W3Merits),
        pre_string="W3 Salt Merits Purchased",
        advices=refinery_AdviceDict['Merits'],
        post_string="Leveling this Merit would immediately decrease salt consumption."
    )
    refinery_AdviceGroupDict['ExcessAndDeficits'] = AdviceGroup(
        tier="",
        pre_string="Salt Excess/Deficit per Synthesis Cycle",
        advices=refinery_AdviceDict['ExcessAndDeficits'],
        post_string="",
        informational=True,
        completed=all([int(advice.goal.replace(',', '')) >= 0 for advice in refinery_AdviceDict['ExcessAndDeficits']])
    )
    refinery_AdviceGroupDict['Tab1Ranks'] = AdviceGroup(
        tier="",
        pre_string="Max Tab1 Ranks without causing a Salt Deficit",
        advices=refinery_AdviceDict['Tab1Ranks'],
        post_string="Or just YOLO rank up everything if balancing is too much of a pain ¯\\_(ツ)_/¯",
        informational=True,
        completed=all([advice.progression >= advice.goal for advice in refinery_AdviceDict['Tab1Ranks']])
    )
    refinery_AdviceGroupDict['Tab2Ranks'] = AdviceGroup(
        tier="",
        pre_string="Max Tab2 Ranks without causing a Salt Deficit",
        advices=refinery_AdviceDict['Tab2Ranks'],
        post_string="",
        informational=True,
        completed=all([advice.progression >= advice.goal for advice in refinery_AdviceDict['Tab2Ranks']])
    )
    overall_SectionTier = min(max_tier, tier_AutoRefine, tier_W3Merits)
    return refinery_AdviceGroupDict, overall_SectionTier, max_tier

def getConsRefineryAdviceSection() -> AdviceSection:
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        return AdviceSection(
            name="Refinery",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Construction skill in World 3!",
            picture="Construction_Refinery.gif",
            unreached=True
        )

    #Generate AdviceGroups
    refinery_AdviceGroupDict, overall_SectionTier, max_tier = getRefineryProgressionTierAdviceGroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    return AdviceSection(
        name="Refinery",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Refinery tier met: {tier_section}{break_keep_it_up if overall_SectionTier >= max_tier else ''}",
        picture="Construction_Refinery.gif",
        groups=refinery_AdviceGroupDict.values(),
        collapse=False
    )
