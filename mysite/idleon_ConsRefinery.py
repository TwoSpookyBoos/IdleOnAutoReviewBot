import json
import progressionResults
from idleon_SkillLevels import getSpecificSkillLevelsList
from models import AdviceSection, AdviceGroup, Advice
from utils import pl
from math import floor

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

def parseConsRefinery(inputJSON):
    refineryList = json.loads(inputJSON["Refinery"])
    meritList = json.loads(inputJSON["TaskZZ2"])
    consRefineryDict = {
        #Combustion = Tab1
        'Red Rank': refineryList[3][1],
        'Red AutoRefine': refineryList[3][4],
        'Orange Rank': refineryList[4][1],
        'Orange AutoRefine': refineryList[4][4],
        'Blue Rank': refineryList[5][1],
        'Blue AutoRefine': refineryList[5][4],

        #Synthesis = Tab2
        'Green Rank': refineryList[6][1],
        'Green AutoRefine': refineryList[6][4],
        'Purple Rank': refineryList[7][1],
        'Purple AutoRefine': refineryList[7][4],
        'Nullo Rank': refineryList[8][1],
        'Nullo AutoRefine': refineryList[8][4],

        #W3 Merit
        'Salt Merit': meritList[2][6]
    }
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

def setConsRefineryProgressionTier(inputJSON, progressionTiers, characterDict):
    refinery_AdviceDict = {
        "AutoRefine": [],
        "Merits": [],
        "ExcessAndDeficits": [],
        "Ranks": [],
    }
    refinery_AdviceGroupDict = {}
    refinery_AdviceSection = AdviceSection(
        name="Refinery",
        tier="Not Yet Evaluated",
        header="Best Refinery tier met: Not Yet Evaluated. Recommended Refinery actions:",
        picture="Construction_Refinery.gif",
        collapse=False
    )
    constructionLevelsList = getSpecificSkillLevelsList(inputJSON, len(characterDict), "Construction")
    if max(constructionLevelsList) < 1:
        refinery_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return refinery_AdviceSection

    max_tier = progressionTiers[-1][0]
    tier_AutoRefine = max_tier
    tier_W3Merits = 0
    consRefineryDict = parseConsRefinery(inputJSON)

    # AutoRefine Advice
    if consRefineryDict['RedSalt'].auto_refine != 0:
        tier_AutoRefine = 0
        refinery_AdviceDict['AutoRefine'].append(
            Advice(label=consRefineryDict['RedSalt'].salt_name, picture_class=consRefineryDict['RedSalt'].image,
                   progression=consRefineryDict['RedSalt'].auto_refine, goal=0, unit="%")
        )
    if consRefineryDict['GreenSalt'].auto_refine != 0:
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
    tier_W3Merits = consRefineryDict['Salt Merit']
    if consRefineryDict['Salt Merit'] < sum_SaltsRank2Plus:
        refinery_AdviceDict["Merits"].append(
            Advice(label="W3 Taskboard Merits Purchased", picture_class="iceland-irwin", progression=str(consRefineryDict['Salt Merit']),
                   goal=str(sum_SaltsRank2Plus))
        )

    # #Excess and Deficits Advice
    # refinery_AdviceDict["ExcessAndDeficits"].append(
    #     Advice(
    #         label=f"Red Salt {consRefineryDict['RedSalt'].excess_or_deficit}",
    #         picture_class=consRefineryDict['RedSalt'].image,
    #         progression=consRefineryDict['RedSalt'].excess_amount)
    # )
    # refinery_AdviceDict["ExcessAndDeficits"].append(
    #     Advice(
    #         label=f"Orange Salt {consRefineryDict['OrangeSalt'].excess_or_deficit}",
    #         picture_class=consRefineryDict['OrangeSalt'].image,
    #         progression=consRefineryDict['OrangeSalt'].excess_amount)
    # )
    # refinery_AdviceDict["ExcessAndDeficits"].append(
    #     Advice(
    #         label=f"Blue Salt {consRefineryDict['BlueSalt'].excess_or_deficit}",
    #         picture_class=consRefineryDict['BlueSalt'].image,
    #         progression=consRefineryDict['BlueSalt'].excess_amount)
    # )
    # refinery_AdviceDict["ExcessAndDeficits"].append(
    #     Advice(
    #         label=f"Green Salt {consRefineryDict['GreenSalt'].excess_or_deficit}",
    #         picture_class=consRefineryDict['GreenSalt'].image,
    #         progression=consRefineryDict['GreenSalt'].excess_amount)
    # )
    # refinery_AdviceDict["ExcessAndDeficits"].append(
    #     Advice(
    #         label=f"Purple Salt {consRefineryDict['PurpleSalt'].excess_or_deficit}",
    #         picture_class=consRefineryDict['PurpleSalt'].image,
    #         progression=consRefineryDict['PurpleSalt'].excess_amount)
    # )
    # refinery_AdviceDict["ExcessAndDeficits"].append(
    #     Advice(
    #         label=f"Nullo Salt {consRefineryDict['NulloSalt'].excess_or_deficit}",
    #         picture_class=consRefineryDict['NulloSalt'].image,
    #         progression=consRefineryDict['NulloSalt'].excess_amount)
    # )

    # Ranks Advice
    refinery_AdviceDict["Ranks"].append(
        Advice(label="Red Salt", picture_class=consRefineryDict['RedSalt'].image, progression=consRefineryDict['RedSalt'].salt_rank, goal="∞")
    )
    refinery_AdviceDict["Ranks"].append(
        Advice(label="Orange Salt", picture_class=consRefineryDict['OrangeSalt'].image, progression=consRefineryDict['OrangeSalt'].salt_rank,
               goal=consRefineryDict['OrangeSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Ranks"].append(
        Advice(label="Blue Salt", picture_class=consRefineryDict['BlueSalt'].image, progression=consRefineryDict['BlueSalt'].salt_rank,
               goal=consRefineryDict['BlueSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Ranks"].append(
        Advice(label="Green Salt", picture_class=consRefineryDict['GreenSalt'].image, progression=consRefineryDict['GreenSalt'].salt_rank, goal="∞")
    )
    refinery_AdviceDict["Ranks"].append(
        Advice(label="Purple Salt", picture_class=consRefineryDict['PurpleSalt'].image, progression=consRefineryDict['PurpleSalt'].salt_rank,
               goal=consRefineryDict['PurpleSalt'].max_rank_with_excess)
    )
    refinery_AdviceDict["Ranks"].append(
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
        pre_string="Invest more points into the W3 Salt Merit to reduce your salt consumption!",
        advices=refinery_AdviceDict['Merits'],
        post_string=""
    )
    refinery_AdviceGroupDict['ExcessAndDeficits'] = AdviceGroup(
        tier="",
        pre_string="Salt Excess/Deficit per Synthesis Cycle",
        advices=refinery_AdviceDict['ExcessAndDeficits'],
        post_string=""
    )
    refinery_AdviceGroupDict['Ranks'] = AdviceGroup(
        tier="",
        pre_string="Recommended Ranks without causing a Salt Deficit",
        advices=refinery_AdviceDict['Ranks'],
        post_string="Or just YOLO rank up everything if balancing is too much of a pain ¯\_(ツ)_/¯"
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

def OLDsetConsRefineryProgressionTier(inputJSON, progressionTiers):
    tier_Tab1 = 0
    tier_Tab2 = 0
    tier_AutoRefine = 0
    tier_W3Merits = 0
    max_tier = progressionTiers[-1][0]
    advice_Tab1 = ""
    advice_Tab2 = ""
    advice_AutoRefine = ""
    advice_W3Merits = ""
    advice_ConsRefineryCombined = ""

    consRefineryDict = parseConsRefinery(inputJSON)
    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = dict Tab1 Ranks
        #tier[2] = dict Tab2 Ranks
        #tier[3] = dict Tab3 Ranks
        #tier[4] = dict All-tab AutoRefine
        #tier[5] = int W3Merits purchased
        #tier[6] = str Notes

        #Tab1 checks
        if tier_Tab1 == (tier[0]-1):  #Only check if they already met previous tier
            required_Tab1 = tier[1]
            all_Tab1 = True
            for key, value in required_Tab1.items():
                if consRefineryDict[key] < required_Tab1[key]:
                    all_Tab1 = False
                    advice_Tab1 = ""  #TODO
            if all_Tab1 == True:
                tier_Tab1 = tier[0]

        #Tab2 checks
        if tier_Tab2 == (tier[0]-1):  #Only check if they already met previous tier
            required_Tab2 = tier[2]
            all_Tab2 = True
            for key, value in required_Tab2.items():
                if consRefineryDict[key] < required_Tab2[key]:
                    all_Tab2 = False
            if all_Tab2 == True:
                tier_Tab2 = tier[0]

        #AutoRefine checks
        if tier_AutoRefine == (tier[0]-1):  #Only check if they already met previous tier
            required_AutoRefine = tier[4]
            all_AutoRefine = True
            for key, value in required_AutoRefine.items():
                if consRefineryDict[key] != required_AutoRefine[key]:  #This is the only comparison we want to make sure is exactly equal
                    all_AutoRefine = False
                    if consRefineryDict['Red AutoRefine'] > 0 or consRefineryDict['Green AutoRefine'] > 0:
                        advice_AutoRefine = "Tier 0- The first salt per tab should always be ranking up (aka auto-refine at 0%)! Setting max tier to 0 until this is fixed :("
                else:
                    all_AutoRefine = True  #for clarity lol. Being equal is the desired outcome. This value should already be true from before. Being unequal is the bad outcome that would result in it turning False.
            if all_AutoRefine == True:
                tier_AutoRefine = tier[0]

        #W3 Merits check
        if tier_W3Merits == (tier[0]-1):
            required_W3Merits = tier[5]
            if consRefineryDict['Salt Merit'] >= required_W3Merits:
                tier_W3Merits = tier[0]

    #Generate all the advice
    overall_ConsRefineryTier = min(progressionTiers[-1][0], tier_AutoRefine, tier_W3Merits, tier_Tab1, tier_Tab2)

    #W3Merits Advice
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
        advice_W3Merits = "Tier " + str(tier_W3Merits) + "- Invest more points into the W3 Salt Merit to reduce your salt consumption! Currently " + str(consRefineryDict['Salt Merit']) + "/" + str(sum_SaltsRank2Plus)

    #Tab1 Advice
    if consRefineryDict['Combustion AutoRefine'] > 0:
        if tier_Tab1 < 16:
            #Red Salt
            advice_Tab1 = ("Tier " + str(tier_Tab1) + "- Next Tab1 Balanced tier needs "
            + "Red: " + str(consRefineryDict['Red Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Red Rank']))
            #Orange Salt
            if (consRefineryDict['Orange Rank'] > progressionTiers[tier_Tab1+1][1]['Orange Rank']) and progressionTiers[tier_Tab1+1][1]['Orange Rank'] != 0:
                advice_Tab1 += ", Orange: " + str(consRefineryDict['Orange Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Orange Rank']) + " (Overleveled!)"
            else:
                advice_Tab1 += ", Orange: " + str(consRefineryDict['Orange Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Orange Rank'])
            #Blue Salt
            if (consRefineryDict['Blue Rank'] > progressionTiers[tier_Tab1+1][1]['Blue Rank']) and progressionTiers[tier_Tab1+1][1]['Blue Rank'] != 0:
                advice_Tab1 += ", Blue: " + str(consRefineryDict['Blue Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Blue Rank']) + " (Overleveled!)"
            else:
                advice_Tab1 += ", Blue: " + str(consRefineryDict['Blue Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Blue Rank'])
            #Tab1 trailing auto-refine
            if tier_Tab1 >= 8:
                if consRefineryDict['Red Rank'] < 22:
                    advice_Tab1 += ". After your Red Salt reaches rank 22, consider setting all of Tab1 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab1 to Tier 17+. This style isn't for everyone though!)"
                else:
                    advice_Tab1 += ". Now that your Red Salt is rank 22+, consider setting all of Tab1 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab1 to Tier 17+. This style isn't for everyone though!)"
        elif tier_Tab1 >= 17:
            advice_Tab1 = "Tier " + str(tier_Tab1) + "- " + progressionTiers[17][6]
    elif consRefineryDict['Combustion AutoRefine'] == 0:
        if consRefineryDict['Red Rank'] >= 22:
            tier_Tab1 = progressionTiers[-1][0]  #19 currently
            advice_Tab1 += "Tier " + str(tier_Tab1) + "- Red is already rank 22+ where ranks become faster instead of slower, and all Tab1 salts are set to 0% AutoRefine. Tab1 should be relatively smooth sailing ❤️"

        else:
            tier_Tab1 = progressionTiers[-3][0]  #17 currently
            advice_Tab1 += "Tier " + str(tier_Tab1) + "- Tab1 still has scaling time because Red Salt's rank is under 22, and all Tab1 salts are set to 0% AutoRefine :( Pay attention to Tab1 salt requirements for upcoming crafting and building in advance to avoid long delays."

    #Tab2 Advice
    if consRefineryDict['Synthesis AutoRefine'] > 0:
        if tier_Tab2 < 16:
            advice_Tab2 = ("Tier " + str(tier_Tab2) + "- Next Tab2 Balanced tier needs "
            + "Green: " + str(consRefineryDict['Green Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Green Rank']))
            if (consRefineryDict['Purple Rank'] > progressionTiers[tier_Tab2+1][2]['Purple Rank']) and progressionTiers[tier_Tab2+1][2]['Purple Rank'] != 0:
                advice_Tab2 += ", Purple: " + str(consRefineryDict['Purple Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Purple Rank']) + " (Overleveled!)"
            else:
                advice_Tab2 += ", Purple: " + str(consRefineryDict['Purple Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Purple Rank'])
            if (consRefineryDict['Nullo Rank'] > progressionTiers[tier_Tab2+1][2]['Nullo Rank']) and progressionTiers[tier_Tab2+1][2]['Nullo Rank'] != 0:
                advice_Tab2 += ", Nullo: " + str(consRefineryDict['Nullo Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Nullo Rank']) + " (Overleveled!)"
            else:
                advice_Tab2 += ", Nullo: " + str(consRefineryDict['Nullo Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Nullo Rank'])
            if tier_Tab2 >= 9:
                if consRefineryDict['Green Rank'] < 22:
                    advice_Tab2 += ". After your Green Salt reaches rank 22, consider setting all of Tab2 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab2 to Tier 18+. This style isn't for everyone though!)"
                else:
                    advice_Tab2 += ". Now that your Green Salt is rank 22+, consider setting all of Tab2 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab2 to Tier 18+. This style isn't for everyone though!)"
        elif tier_Tab2 >= 17:
            advice_Tab2 = "Tier " + str(tier_Tab2) + "- " + progressionTiers[18][6]
    elif consRefineryDict['Synthesis AutoRefine'] == 0:
        if consRefineryDict['Green Rank'] >= 22:
            tier_Tab2 = progressionTiers[-1][0]  #19 currently
            advice_Tab2 += "Tier " + str(tier_Tab2) + "- Green is already rank 22+ where ranks become faster instead of slower, and all Tab2 salts are set to 0% AutoRefine. Tab2 should be relatively smooth sailing ❤️"

        else:
            tier_Tab2 = progressionTiers[-2][0]  #18 currently
            advice_Tab2 += "Tier " + str(tier_Tab2) + "- Tab2 still has scaling time because Green Salt's rank is under 22, and all Tab2 salts are set to 0% AutoRefine :( Pay attention to Tab2 salt requirements for upcoming crafting and building in advance to avoid long delays."

    #AutoRefine advice
    if tier_AutoRefine == progressionTiers[-1][0] and consRefineryDict['Red Rank'] >= 2:
        overall_ConsRefineryTier = tier_AutoRefine  #Rank 19 is full yolo, but only if they already have Red Salts to level 2 or higher to prevent this triggering on pre-w3 accounts
        advice_AutoRefine = "Tier " + str(tier_AutoRefine) + "- You've got all Salts set to 0% auto-refine, the infinite-scaling portion of Refinery."
        #Another comment for clarity. I only want AutoRefine advice to show up in the extreme cases of Tier0 or Max tier. Anything inbetween doesn't need advice.
        if tier_Tab1 == progressionTiers[-1][0] and tier_Tab2 == progressionTiers[-1][0]:
            advice_AutoRefine += " You best ❤️"

    #Generate advice statement
    advice_ConsRefineryCombined = ["Best Refinery tier met: " + str(overall_ConsRefineryTier) + "/" + str(progressionTiers[-1][-0]), advice_AutoRefine, advice_W3Merits, advice_Tab1, advice_Tab2]
    #TODO
    #print("Tiers: Overall",overall_ConsRefineryTier, ", AutoRefine", tier_AutoRefine, ", Merits", tier_W3Merits, ", Tab1", tier_Tab1, ", Tab2", tier_Tab2, ", Tab3", tier_Tab3)
    #print("Determined lowest refinery tier met to be: " + str(overall_ConsRefineryTier) + "/19")
    #print(advice_ConsRefineryCombined)
    consRefineryPR = progressionResults.progressionResults(overall_ConsRefineryTier,advice_ConsRefineryCombined,"")
    return consRefineryPR
