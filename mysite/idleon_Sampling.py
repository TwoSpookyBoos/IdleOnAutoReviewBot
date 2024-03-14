import json

def parseJSONtoLists(inputJSON):
    samplingList = json.loads(inputJSON["Sampling"])
    return samplingList

#def getGemShopPurchases(inputJSON["GemItemsPurchased"]):

#Tier	Crystal Printer Gemshop	Card Slots	Star Signs	Prayers	Card Pre-Skill Mastery	Cards Post-Skill Mastery	Obols	Lab Chips	Big Alch Bubble	Equipment - Early	Equipment - Mid	Equipment - Late
def setSamplingProgressionTier(inputJSON, progressionTiers):
    tier_Sampling = 0
    overall_SamplingTier = 0
    advice_Sampling1 = ""
    overall_SamplingTier = min(progressionTiers[-1][-0], tier_Sampling)
    advice_SamplingCombined = ["Best Sampling tier met: " + str(overall_SamplingTier) + "/" + str(progressionTiers[-1][-0])]
    #samplingPR = progressionResults.progressionResults(overall_SamplingTier,advice_SamplingCombined,"")
    #return samplingPR
