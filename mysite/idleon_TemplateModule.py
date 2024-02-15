import json
import progressionResults

def parseJSONtoLists(inputJSON):
    templateList = json.loads(inputJSON["Template"])
    return templateList

def setTemplateProgressionTier(inputJSON, progressionTiers):
    tier_Template = 0
    overall_TemplateTier = 0
    advice_Template1 = ""
    overall_TemplateTier = min(progressionTiers[-1][0], tier_Template)
    advice_TemplateCombined = ["Best Template tier met: " + str(overall_TemplateTier) + "/" + str(progressionTiers[-1][0]) + ". Recommended Template actions:", advice_Template1]
    templatePR = progressionResults.progressionResults(overall_TemplateTier,advice_TemplateCombined,"")
    return templatePR
