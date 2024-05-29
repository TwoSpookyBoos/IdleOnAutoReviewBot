import json
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from math import floor

from utils.data_formatting import safe_loads


saltValuesDict = {
    # "salt": [advice image name, cycles per Synth cycle, consumption of previous salt, next salt consumption, next salt cycles per Synth cycle]
    "Red": ["redox-salts", 4, 0, 2, 4],
    "Orange": ["explosive-salts", 4, 2, 2, 4],
    "Blue": ["spontaneity-salts", 4, 2, 1, 1],
    "Green": ["dioxide-synthesis", 1, 1, 2, 1],
    "Purple": ["purple-salt", 1, 2, 2, 1],
    "Nullo": ["nullo-salt", 1, 2, 0, 0]
}

class Salt:
    def __init__(self, salt_name: str, auto_refine: int, salt_rank: int, next_salt_rank: int, previousSalt, merit_purchased: bool = True):
        self.salt_name: str = salt_name
        self.salt_rank: int = salt_rank
        self.auto_refine: int = auto_refine
        self.max_rank_with_excess: int = salt_rank
        self.merit_purchased: bool = merit_purchased
        if self.merit_purchased is True:
            self.salt_consumption_scaling: float = 1.3
        else:
            self.salt_consumption_scaling: float = 1.5
        if salt_name in saltValuesDict:
            self.image: str = saltValuesDict[salt_name][0]
            self.cycles_per_Synthesis_cycle: int = saltValuesDict[salt_name][1]
            self.consumption_of_previous_salt: int = saltValuesDict[salt_name][2]
            self.next_salt_consumption: int = saltValuesDict[salt_name][3]
            self.next_salt_cycles_per_Synthesis_cycle: int = saltValuesDict[salt_name][4]
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
                    if next_salt_rank != 0:
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
    refineryList = safe_loads(session_data.account.raw_data.get("Refinery", []))
    consRefineryDict = {
        # Combustion = Tab1
        'Red Rank': 0,
        'Red AutoRefine': 0,
        'Orange Rank': 0,
        'Orange AutoRefine': 0,
        'Blue Rank': 0,
        'Blue AutoRefine': 0,

        # Synthesis = Tab2
        'Green Rank': 0,
        'Green AutoRefine': 0,
        'Purple Rank': 0,
        'Purple AutoRefine': 0,
        'Nullo Rank': 0,
        'Nullo AutoRefine': 0,

        # W3 Merit
        'Salt Merit': 0
    }  #Default 0s
    if refineryList:
        # Combustion = Tab1
        consRefineryDict['Red Rank'] = refineryList[3][1]
        consRefineryDict['Red AutoRefine'] = refineryList[3][4]
        consRefineryDict['Orange Rank'] = refineryList[4][1]
        consRefineryDict['Orange AutoRefine'] = refineryList[4][4]
        consRefineryDict['Blue Rank'] = refineryList[5][1]
        consRefineryDict['Blue AutoRefine'] = refineryList[5][4]

        #Synthesis = Tab2
        consRefineryDict['Green Rank'] = refineryList[6][1]
        consRefineryDict['Green AutoRefine'] = refineryList[6][4]
        consRefineryDict['Purple Rank'] = refineryList[7][1]
        consRefineryDict['Purple AutoRefine'] = refineryList[7][4]
        consRefineryDict['Nullo Rank'] = refineryList[8][1]
        consRefineryDict['Nullo AutoRefine'] = refineryList[8][4]

    consRefineryDict['Salt Merit'] = session_data.account.merits[2][6]["Level"]

    consRefineryDict['Combustion AutoRefine'] = consRefineryDict['Red AutoRefine'] + consRefineryDict['Orange AutoRefine'] + consRefineryDict['Blue AutoRefine']
    consRefineryDict['Synthesis AutoRefine'] = consRefineryDict['Green AutoRefine'] + consRefineryDict['Purple AutoRefine'] + consRefineryDict['Nullo AutoRefine']
    consRefineryDict['Sum AutoRefine'] = consRefineryDict['Combustion AutoRefine'] + consRefineryDict['Synthesis AutoRefine']
    consRefineryDict["RedSalt"] = Salt(
        salt_name='Red',
        auto_refine=consRefineryDict['Red AutoRefine'],
        salt_rank=consRefineryDict['Red Rank'],
        next_salt_rank=consRefineryDict['Orange Rank'],
        previousSalt=None,
        merit_purchased=consRefineryDict["Salt Merit"] >= 1
    )
    consRefineryDict["OrangeSalt"] = Salt(
        salt_name="Orange",
        auto_refine=consRefineryDict['Orange AutoRefine'],
        salt_rank=consRefineryDict["Orange Rank"],
        next_salt_rank=consRefineryDict["Blue Rank"],
        previousSalt=consRefineryDict["RedSalt"],
        merit_purchased=consRefineryDict["Salt Merit"] >= 2
    )
    consRefineryDict["BlueSalt"] = Salt(
        salt_name="Blue",
        auto_refine=consRefineryDict['Blue AutoRefine'],
        salt_rank=consRefineryDict["Blue Rank"],
        next_salt_rank=consRefineryDict["Green Rank"],
        previousSalt=consRefineryDict["OrangeSalt"],
        merit_purchased=consRefineryDict["Salt Merit"] >= 3
    )
    consRefineryDict["GreenSalt"] = Salt(
        salt_name="Green",
        auto_refine=consRefineryDict['Green AutoRefine'],
        salt_rank=consRefineryDict["Green Rank"],
        next_salt_rank=consRefineryDict["Purple Rank"],
        previousSalt=consRefineryDict["BlueSalt"],
        merit_purchased=consRefineryDict["Salt Merit"] >= 4
    )
    consRefineryDict["PurpleSalt"] = Salt(
        salt_name="Purple",
        auto_refine=consRefineryDict['Purple AutoRefine'],
        salt_rank=consRefineryDict["Purple Rank"],
        next_salt_rank=consRefineryDict["Nullo Rank"],
        previousSalt=consRefineryDict["GreenSalt"],
        merit_purchased=consRefineryDict["Salt Merit"] >= 5
    )
    consRefineryDict["NulloSalt"] = Salt(
        salt_name="Nullo",
        auto_refine=consRefineryDict['Nullo AutoRefine'],
        salt_rank=consRefineryDict["Nullo Rank"],
        next_salt_rank=0,
        previousSalt=consRefineryDict["PurpleSalt"],
        merit_purchased=consRefineryDict["Salt Merit"] >= 6
    )
    #print(consRefineryDict)
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

    # AutoRefine Advice
    if consRefineryDict['RedSalt'].auto_refine != 0:
        if consRefineryDict['RedSalt'].salt_rank < 100:
            tier_AutoRefine = 0
        refinery_AdviceDict['AutoRefine'].append(
            Advice(label=consRefineryDict['RedSalt'].salt_name, picture_class=consRefineryDict['RedSalt'].image,
                   progression=consRefineryDict['RedSalt'].auto_refine, goal=0, unit="%")
        )
    if consRefineryDict['GreenSalt'].auto_refine != 0:
        if consRefineryDict['GreenSalt'].salt_rank < 30:
            tier_AutoRefine = 0
        refinery_AdviceDict['AutoRefine'].append(
            Advice(label=consRefineryDict['GreenSalt'].salt_name, picture_class=consRefineryDict['GreenSalt'].image,
                   progression=consRefineryDict['GreenSalt'].auto_refine, goal=0, unit="%", value_format="{value}{unit}")
        )

    # W3Merits Advice
    sum_SaltsRank2Plus = 0
    if consRefineryDict['Orange Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Blue Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Green Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Purple Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Nullo Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Salt Merit'] < sum_SaltsRank2Plus:
        tier_W3Merits = 0
        refinery_AdviceDict["Merits"].append(
            Advice(
                label="W3 Taskboard Merits Purchased",
                picture_class="iceland-irwin",
                progression=str(consRefineryDict['Salt Merit']),
                goal=5)
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
        pre_string="Red and Green Salts should always be set to 0% Auto-Refine",
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
        post_string="Or just YOLO rank up everything if balancing is too much of a pain ¯\_(ツ)_/¯"
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
    if overall_ConsRefineryTier == max_tier:
        refinery_AdviceSection.header = f"Best Refinery tier met: {tier_section}<br>You best ❤️"
    else:
        refinery_AdviceSection.header = f"Best Refinery tier met: {tier_section}"
    return refinery_AdviceSection
