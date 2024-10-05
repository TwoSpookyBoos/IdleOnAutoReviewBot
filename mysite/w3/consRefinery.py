from flask import g as session_data
from consts import break_keep_it_up
from models.models import AdviceSection, AdviceGroup, Advice
from math import floor
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
                        self.max_rank_with_excess: int = int(
                            floor(
                                ((previousSalt.output-1)/(self.consumption_of_previous_salt * self.cycles_per_Synthesis_cycle)) ** (1/self.salt_consumption_scaling)
                            )
                        )
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

def parseConsRefinery():
    consRefineryDict = {}
    consRefineryDict['RedSalt'] = Salt(
        salt_name='Red',
        auto_refine=session_data.account.refinery['Red']['AutoRefine'],
        salt_rank=session_data.account.refinery['Red']['Rank'],
        next_salt_rank=session_data.account.refinery['Orange']['Rank'],
        previousSalt=None,
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 1,
        running=session_data.account.refinery['Red']['Running'],
    )
    consRefineryDict['OrangeSalt'] = Salt(
        salt_name='Orange',
        auto_refine=session_data.account.refinery['Orange']['AutoRefine'],
        salt_rank=session_data.account.refinery['Orange']['Rank'],
        next_salt_rank=session_data.account.refinery['Blue']['Rank'],
        previousSalt=consRefineryDict['RedSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 2,
        running=session_data.account.refinery['Orange']['Running'],
    )
    consRefineryDict['BlueSalt'] = Salt(
        salt_name='Blue',
        auto_refine=session_data.account.refinery['Blue']['AutoRefine'],
        salt_rank=session_data.account.refinery['Blue']['Rank'],
        next_salt_rank=session_data.account.refinery['Green']['Rank'],
        previousSalt=consRefineryDict['OrangeSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 3,
        running=session_data.account.refinery['Blue']['Running'],
    )
    consRefineryDict['GreenSalt'] = Salt(
        salt_name='Green',
        auto_refine=session_data.account.refinery['Green']['AutoRefine'],
        salt_rank=session_data.account.refinery['Green']['Rank'],
        next_salt_rank=session_data.account.refinery['Purple']['Rank'],
        previousSalt=consRefineryDict['BlueSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 4,
        running=session_data.account.refinery['Green']['Running'],
    )
    consRefineryDict['PurpleSalt'] = Salt(
        salt_name='Purple',
        auto_refine=session_data.account.refinery['Purple']['AutoRefine'],
        salt_rank=session_data.account.refinery['Purple']['Rank'],
        next_salt_rank=session_data.account.refinery['Nullo']['Rank'],
        previousSalt=consRefineryDict['GreenSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 5,
        running=session_data.account.refinery['Purple']['Running'],
    )
    consRefineryDict['NulloSalt'] = Salt(
        salt_name='Nullo',
        auto_refine=session_data.account.refinery['Nullo']['AutoRefine'],
        salt_rank=session_data.account.refinery['Nullo']['Rank'],
        next_salt_rank=0,
        previousSalt=consRefineryDict['PurpleSalt'],
        merit_purchased=session_data.account.merits[2][6]['Level'] >= 6,
        running=session_data.account.refinery['Nullo']['Running'],
    )
    #logger.debug(consRefineryDict)
    return consRefineryDict

def setConsRefineryProgressionTier():
    refinery_AdviceDict = {
        "AutoRefine": [],
        "Merits": [],
        "ExcessAndDeficits": [],
        "Tab1Ranks": [],
        "Tab2Ranks": [],
    }
    refinery_AdviceGroupDict = {}
    refinery_AdviceSection = AdviceSection(
        name="Refinery",
        tier="Not Yet Evaluated",
        header="Best Refinery tier met: Not Yet Evaluated. Recommended Refinery actions:",
        picture="Construction_Refinery.gif",
        collapse=False
    )
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        refinery_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        refinery_AdviceSection.collapse = True
        return refinery_AdviceSection

    max_tier = 1  #Pass or Fail
    tier_AutoRefine = 1
    tier_W3Merits = 1
    consRefineryDict = parseConsRefinery()

    # AutoRefine and On/Off Advice
    if not consRefineryDict['RedSalt'].running:
        if consRefineryDict['RedSalt'].salt_rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{consRefineryDict['RedSalt'].salt_name} is not producing",
                picture_class=consRefineryDict['RedSalt'].image,
                progression='Off',
                goal='On')
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} is not producing",
                picture_class=consRefineryDict['RedSalt'].image
            ))
    if consRefineryDict['RedSalt'].auto_refine != 0:
        if consRefineryDict['RedSalt'].salt_rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(
                Advice(label=consRefineryDict['RedSalt'].salt_name, picture_class=consRefineryDict['RedSalt'].image,
                       progression=consRefineryDict['RedSalt'].auto_refine, goal=0, unit="%")
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} auto-refining early. Recommended to at least reach Rank 100 before auto-refining early.",
                picture_class=consRefineryDict['RedSalt'].image
            ))

    if not consRefineryDict['GreenSalt'].running:
        if consRefineryDict['GreenSalt'].salt_rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{consRefineryDict['GreenSalt'].salt_name} is not producing",
                picture_class=consRefineryDict['GreenSalt'].image,
                progression='Off',
                goal='On')
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} is not producing",
                picture_class=consRefineryDict['GreenSalt'].image
            ))
    if consRefineryDict['GreenSalt'].auto_refine != 0:
        if consRefineryDict['GreenSalt'].salt_rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(
                Advice(label=consRefineryDict['GreenSalt'].salt_name, picture_class=consRefineryDict['GreenSalt'].image,
                       progression=consRefineryDict['GreenSalt'].auto_refine, goal=0, unit="%")
            )
            session_data.account.alerts_AdviceDict['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} auto-refining early. Recommended to at least reach Rank 30 before auto-refining early.",
                picture_class=consRefineryDict['GreenSalt'].image
            ))

    # W3Merits Advice
    sum_SaltsRank2Plus = 0
    if consRefineryDict['OrangeSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['BlueSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['GreenSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['PurpleSalt'].salt_rank >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['NulloSalt'].salt_rank >= 2:
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

    #Excess and Deficits Advice
    refinery_AdviceDict["ExcessAndDeficits"].append(
        Advice(
            label=f"Red Salt {consRefineryDict['RedSalt'].excess_or_deficit}",
            picture_class=consRefineryDict['RedSalt'].image,
            progression=consRefineryDict['RedSalt'].excess_amount)
    )
    refinery_AdviceDict["ExcessAndDeficits"].append(
        Advice(
            label=f"Orange Salt {consRefineryDict['OrangeSalt'].excess_or_deficit}",
            picture_class=consRefineryDict['OrangeSalt'].image,
            progression=consRefineryDict['OrangeSalt'].excess_amount)
    )
    refinery_AdviceDict["ExcessAndDeficits"].append(
        Advice(
            label=f"Blue Salt {consRefineryDict['BlueSalt'].excess_or_deficit}",
            picture_class=consRefineryDict['BlueSalt'].image,
            progression=consRefineryDict['BlueSalt'].excess_amount)
    )
    refinery_AdviceDict["ExcessAndDeficits"].append(
        Advice(
            label=f"Green Salt {consRefineryDict['GreenSalt'].excess_or_deficit}",
            picture_class=consRefineryDict['GreenSalt'].image,
            progression=consRefineryDict['GreenSalt'].excess_amount)
    )
    refinery_AdviceDict["ExcessAndDeficits"].append(
        Advice(
            label=f"Purple Salt {consRefineryDict['PurpleSalt'].excess_or_deficit}",
            picture_class=consRefineryDict['PurpleSalt'].image,
            progression=consRefineryDict['PurpleSalt'].excess_amount)
    )
    refinery_AdviceDict["ExcessAndDeficits"].append(
        Advice(
            label=f"Nullo Salt {consRefineryDict['NulloSalt'].excess_or_deficit}",
            picture_class=consRefineryDict['NulloSalt'].image,
            progression=consRefineryDict['NulloSalt'].excess_amount)
    )

    # Ranks Advice
    refinery_AdviceDict["Tab1Ranks"].append(
        Advice(label="Red Salt", picture_class=consRefineryDict['RedSalt'].image, progression=consRefineryDict['RedSalt'].salt_rank, goal="∞")
    )
    refinery_AdviceDict["Tab1Ranks"].append(
        Advice(label="Orange Salt", picture_class=consRefineryDict['OrangeSalt'].image, progression=consRefineryDict['OrangeSalt'].salt_rank,
               goal=consRefineryDict['OrangeSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Tab1Ranks"].append(
        Advice(label="Blue Salt", picture_class=consRefineryDict['BlueSalt'].image, progression=consRefineryDict['BlueSalt'].salt_rank,
               goal=consRefineryDict['BlueSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Tab2Ranks"].append(
        Advice(label="Green Salt", picture_class=consRefineryDict['GreenSalt'].image, progression=consRefineryDict['GreenSalt'].salt_rank, goal="∞")
    )
    refinery_AdviceDict["Tab2Ranks"].append(
        Advice(label="Purple Salt", picture_class=consRefineryDict['PurpleSalt'].image, progression=consRefineryDict['PurpleSalt'].salt_rank,
               goal=consRefineryDict['PurpleSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Tab2Ranks"].append(
        Advice(label="Nullo Salt", picture_class=consRefineryDict['NulloSalt'].image, progression=consRefineryDict['NulloSalt'].salt_rank,
               goal=consRefineryDict['NulloSalt'].max_rank_with_excess)
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
        post_string=""
    )
    refinery_AdviceGroupDict['Tab1Ranks'] = AdviceGroup(
        tier="",
        pre_string="Max Tab1 Ranks without causing a Salt Deficit",
        advices=refinery_AdviceDict['Tab1Ranks'],
        post_string="Or just YOLO rank up everything if balancing is too much of a pain ¯\\_(ツ)_/¯"
    )
    refinery_AdviceGroupDict['Tab2Ranks'] = AdviceGroup(
        tier="",
        pre_string="Max Tab2 Ranks without causing a Salt Deficit",
        advices=refinery_AdviceDict['Tab2Ranks'],
        post_string=""
    )

    # Generate AdviceSection
    overall_ConsRefineryTier = min(max_tier, tier_AutoRefine, tier_W3Merits)
    tier_section = f"{overall_ConsRefineryTier}/{max_tier}"
    refinery_AdviceSection.tier = tier_section
    refinery_AdviceSection.pinchy_rating = overall_ConsRefineryTier
    refinery_AdviceSection.groups = refinery_AdviceGroupDict.values()
    if overall_ConsRefineryTier >= max_tier:
        refinery_AdviceSection.header = f"Best Refinery tier met: {tier_section}{break_keep_it_up}"
        refinery_AdviceSection.complete = True
    else:
        refinery_AdviceSection.header = f"Best Refinery tier met: {tier_section}"
    return refinery_AdviceSection
