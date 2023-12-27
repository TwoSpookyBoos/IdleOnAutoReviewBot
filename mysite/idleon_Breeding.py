import json
import progressionResults

def parseJSONtoLists(inputJSON):
    breedingList = json.loads(inputJSON["Breeding"])
    return breedingList

def setBreedingProgressionTier(inputJSON, progressionTiers):
    tier_Breeding = 0
    overall_BreedingTier = 0
    advice_Breeding1 = ""
    overall_BreedingTier = min(progressionTiers[-1][-0], tier_Breeding)
    advice_BreedingCombined = ["Best Breeding tier met: " + str(overall_BreedingTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Breeding actions:", advice_Breeding1]
    breedingPR = progressionResults.progressionResults(overall_BreedingTier,advice_BreedingCombined,"")
    return breedingPR

#1) If not all Pets unlocked, recommend next high priority
#2) If not all Arena Pet slots unlocked, or not all Territories unlocked, recommend what to aim for unlocking based on Abiltiy / meta teams.
    #2a) Possibly list sources of pet chance? Splicing and other dead dna bonsues, vial, stamp, meals, whatever else
    #2b) Maybe a recommended order to spend Dead DNA? Does such a list exist
#3) Spice collecting meta setups. I'm not sure I agree with all of them since I don't follow them.

#"Breeding" - Scoli
#[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0], #20 long: 15 1s, 5 0s. Is this somehow spices?
#[17,17,18,16,1,0,0,0], #Number of unlocked pets per world, I think?
#[22,17,5,7,10,9,7,4,2,5,6,2,0], #Upgrades to buy with Dead DNA
#[21141.5709903892,1021818.97364565,2097037.99208773,390.247777185068,0,0,0,0,1134.3082191807812], #DNA. W1-W8 DNA Spirals, then Dead DNA
#[0,0,0,0,0,0,3,5,4,10,62,10,5,0,42,32,50], #W1 DNA-upgrades, out of 100
#[0,0,0,0,0,0,0,0,0,0,0,0,0,16,33,37,0], #W2 DNA-upgrades
#[0,0,0,0,0,0,0,0,0,0,0,0,0,28,2,0,0,0], #W3 DNA-upgrades
#[0,0,0,0,0,0,0,0,0,0,0,0,0,0,21,0], #W4 DNA-upgrades
#[0], #W5 DNA-upgrades
#[0], #W6 DNA-upgrades
#[0], #W7 DNA-upgrades
#[0], #W8 DNA-upgrades
#[0], #W9 / Placeholder?
#[0,0,0,0,0,0,8.54542145544896,9.67669382236569,13.9186275318536,56.8838868925486,108.12959046347,17.7275208448953,428.250412152119,188.17696756662,533.637843188357,31.6947627578853,50.6309737233113], #W1 Breedability
#[0,69.6907387579612,36.8624747405442,42.619881976793,90.5887539141593,75.2953835158683,53.3276501946464,43.9653587970605,3.17308787999769,73.3571867703604,107.662438825258,60.616056483778,329.151037257164,612.005139442894,145.895286055577,183.145416782817,0], #W2 Breedability
#[103.040564979713,58.2568256691571,19.0606882755539,102.131258957944,170.070554986395,375.639671436722,492.018925272567,64.6609049775532,68.6318514931719,7.54784574450273,15.6091679626235,19.3914401528672,90.6720479304566,504.047297646569,82.8581180135961,50.3331402195651,51.8917665295114,0], #W3 Breedability
#[580.255857513367,283.248552628347,30.6135018833672,64.8798289308786,228.18513297356,197.31242935006,61.2364786210382,7.06284071452882,37.9240819188968,23.3026988248251,17.5876022491411,23.3987263792769,5.01756845138902,28.9874174297304,77.8406287947309,0], #W4 Breedability
#[0], #W5 Breedability
#[0], #W6 Breedability
#[0], #W7 Breedability
#[0], #W8 Breedability
#[0], #W9 / Placeholder?
#[967.6427531949479,200.850893997598,85.379905938739,88.6166372329163,449.5572214705597,85.3663230190753,211.7990207825749,151.28916066805976,459.51795577433506,203.2772533291009,965.7539663269783,448.6740839737442,88.48767896451032,200.87007201094087,87.7725235235931,267.3716241429878,136.74041856337135], #W1 shiny days
#[0.000462793981481479,89.3440758688517,85.58850406897812,85.4332982674152,0.000172796296296296,87.73902741288245,88.6456760094775,452.3115661811872,92.3514901852824,89.9778021185147,85.2502114033624,462.86156186628796,85.538540037469,266.4501648625571,88.39219685848585,969.8143969797454,205.6059705825701], #W2 shiny days
#[450.0216154722705,89.3439221038063,202.02724103880504,85.4267015944297,88.39121962121693,85.1091190727122,92.3513852825045,"4.18055555555556e-05",206.74087635835951,96.1591280737122,965.7179840078996,89.3440375065843,87.73777363510344,85.250171355909,224.83373765861742,85.1081353944701,221.8178901809632,88.7116939265482], #W3 shiny days
#[221.81835044716334,85.363978772235,200.4110125337882,87.6787722774939,87.7998735219069,85.4740287918881,92.3409251808435,131.98556202420357,88.1560091621406,0.00018269675925926,87.73742329482216,96.15882007371248,200.9672410938143,87.79872637260169,85.5644422736844,87.1930508112687], #W4 shiny days
#[0], #W5 shiny days, probably
#[0], #W6 shiny days, probably
#[0], #W7 shiny days, probably
#[0], #W8 shiny days, probably
#[0] #W9 / Placeholder?
#
#"Pets" : First 27 = fenceyard, rest = spicebattles
#["carrotO", #pet name/type as string
#4, #pet ability? 4 = Breedability, 5 = Shiny
#219.653862318461, #Pet power
#0] # Shiny color? I see 0 all on non-shinies. Shiny pets seem to be multiples of 60 up to 300.
#
#"PetsStored" for those in the inventory. Same data as within Pets.
#
#"Territory" seems to hold spice info
#[7130.1609064918075, #Progress toward next spice
#232, #Unknown, but seems to be increasing over time
#0, #Unknown
#"CookingSpice0", #Type of spice being collected, 0 through 19. Can be "Blank" even if unlocked.
#583, #Spices ready to be collected
#"Blank", #Unused / Placeholder
#0, #Unused / Placeholder
#"Blank", #Unused / Placeholder
#0] #Unused / Placeholder