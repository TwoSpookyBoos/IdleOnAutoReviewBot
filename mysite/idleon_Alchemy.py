import progressionResults

def getReadableNames(inputNumber):
    try:
        inputNumber = int(inputNumber)
    except:
        return ("Unknown Vial " + inputNumber)
    match inputNumber:
        case 0:
            return "Copper Corona (Copper Ore)"
        case 1:
            return "Sippy Splinters (Oak Logs)"
        case 2:
            return "Mushroom Soup (Spore Cap)"
        case 3:
            return "Spool Sprite (Thread)"
        case 4:
            return "Barium Mixture (Copper Bar)"
        case 5:
            return "Dieter Drink (Bean Slices)"
        case 6:
            return "Skinny 0 Cal (Snake Skin)"
        case 7:
            return "Thumb Pow (Trusty Nails)"
        case 8:
            return "Jungle Juice (Jungle Logs)"
        case 9:
            return "Barley Brew (Iron Bar)"
        case 10:
            return "Anearful (Glublin Ear)"
        case 11:
            return "Tea With Pea (Potty Rolls)"
        case 12:
            return "Gold Guzzle (Gold Ore)"
        case 13:
            return "Ramificoction (Bullfrog Horn)"
        case 14:
            return "Seawater (Goldfish)"
        case 15:
            return "Tail Time (Rats Tail)"
        case 16:
            return "Fly In My Drink (Fly)"
        case 17:
            return "Mimicraught (Megalodon Tooth)"
        case 18:
            return "Blue Flav (Platinum Ore)"
        case 19:
            return "Slug Slurp (Hermit Can)"
        case 20:
            return "Pickle Jar (BobJoePickle)"
        case 21:
            return "Fur Refresher (Floof Ploof)"
        case 22:
            return "Sippy Soul (Forest Soul)"
        case 23:
            return "Crab Juice (Crabbo)"
        case 24:
            return "Void Vial (Void Ore)"
        case 25:
            return "Red Malt (Redox Salts)"
        case 26:
            return "Ew Gross Gross (Mosquisnow)"
        case 27:
            return "The Spanish Sahara (Tundra Logs)"
        case 28:
            return "Poison Tincture (Poison Froge)"
        case 29:
            return "Etruscan Lager (Mamooth Tusk)"
        case 30:
            return "Chonker Chug (Dune Soul)"
        case 31:
            return "Bubonic Burp (Mousey)"
        case 32:
            return "Visible Ink (Pen)"
        case 33:
            return "Orange Malt (Explosive Salts)"
        case 34:
            return "Snow Slurry (Snow Ball)"
        case 35:
            return "Slowergy Drink (Frigid Soul)"
        case 36:
            return "Sippy Cup (Sippy Straw)"
        case 37:
            return "Bunny Brew (Bunny)"
        case 38:
            return "40-40 Purity (Contact Lense)"
        case 39:
            return "Shaved Ice (Purple Salt)"
        case 40:
            return "Goosey Glug (Honker)"
        case 41:
            return "Ball Pickle Jar (BallJoePickle)"
        case 42:
            return "Capachino (Purple Mush Cap)"
        case 43:
            return "Donut Drink (Half Eaten Donut)"
        case 44:
            return "Long Island Tea (Sand Shark)"
        case 45:
            return "Spook Pint (Squishy Soul)"
        case 46:
            return "Calcium Carbonate (Tongue Bone)"
        case 47:
            return "Bloat Draft (Blobfish)"
        case 48:
            return "Choco Milkshake (Crumpled Wrapper)"
        case 49:
            return "Pearl Seltzer (Pearler Shell)"
        case 50:
            return "Krakenade (Kraken)"
        case 51:
            return "Electrolyte (Condensed Zap)"
        case 52:
            return "Ash Agua (Suggma Ashes)"
        case 53:
            return "Maple Syrup (Maple Logs)"
        case 54:
            return "Hampter Drippy (Hampter)"
        case 55:
            return "Dreadnog (Dreadlo Bar)"
        case 56:
            return "Dusted Drink (Dust Mote)"
        case 57:
            return "Oj Jooce (Orange Slice)"
        case 58:
            return "Oozie Ooblek (Oozie Soul)"
        case 59:
            return "Venison Malt (Mongo Worm Slices)"
        case 60:
            return "Marble Mocha (Marble Ore)"
        case 61:
            return "Willow Sippy (Willow Logs)"
        case 62:
            return "Shinyfin Stew (Equinox Fish)"
        case 63:
            return "Dreamy Drink (Dream Particulate)"
        case _:
            return ("Unknown Vial " + inputNumber)

def setAlchemyVialsProgressionTier(inputJSON, progressionTiers):
    alchemyVialsDict = inputJSON["CauldronInfo"][4]
    #print(alchemyVialsDict)
    maxedVialsList = []
    unmaxedVialsList = []
    lockedVialsList = []
    unlockedVials = 0
    for vial in alchemyVialsDict:
        if alchemyVialsDict[vial] == 0:
            lockedVialsList = []
        else:
            unlockedVials += 1
            if alchemyVialsDict[vial] == 13:
                maxedVialsList.append(vial)
            elif alchemyVialsDict[vial] != 'length':
                unmaxedVialsList.append(getReadableNames(vial))
    #print(maxedVialsList)
    tier_TotalVialsUnlocked = 0
    tier_TotalVialsMaxed = 0
    tier_ParticularVialsMaxed = 0
    overall_AlchemyVialsTier = 0
    advice_TotalVialsUnlocked = ""
    advice_TotalVialsMaxed = ""
    advice_ParticularVialsMaxed = ""
    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalVialsUnlocked
        #tier[2] = int TotalVialsMaxed
        #tier[3] = list ParticularVialsMaxed
        #tier[4] = str Notes
        if tier_TotalVialsUnlocked == (tier[0]-1): #Only check if they already met previous tier
            if unlockedVials >= tier[1]:
                tier_TotalVialsUnlocked = tier[0]
            else:
                advice_TotalVialsUnlocked = "*Unlock some more vials: " + str(unlockedVials) + "/" + str(tier[1]) + tier[4] + "For the most unlock chances per day, rapidly drop multiple stacks of items on the cauldron!"
        if tier_TotalVialsMaxed == (tier[0]-1): #Only check if they already met previous tier
            if len(maxedVialsList) >= tier[2]:
                tier_TotalVialsMaxed = tier[0]
            else:
                if len(maxedVialsList) < 27:
                    advice_TotalVialsMaxed = "*Max some more vials: " + str(len(maxedVialsList)) + "/" + str(tier[2]) + ". 27 is the magic number needed to get the Snake Skin vial to 100% chance to double deposited statues :D"
                else:
                    advice_TotalVialsMaxed = "*Max some more vials: " + str(len(maxedVialsList)) + "/" + str(tier[2]) + ". Thanks to the Vial Mastery bonus in W4's Rift, every maxed vial increases the bonus of EVERY vial you have unlocked!"
        if tier_ParticularVialsMaxed == (tier[0]-1): #Only check if they already met previous tier
            allRequirementsMet = True
            for requiredVial in tier[3]:
                #print("Looking for Vial ", requiredVial, " in " , unmaxedVialsList)
                if requiredVial in unmaxedVialsList:
                    allRequirementsMet = False
                    advice_ParticularVialsMaxed += requiredVial + ", "
            if allRequirementsMet == True:
                tier_ParticularVialsMaxed = tier[0]
            else:
                advice_ParticularVialsMaxed = "*Work on maxing these particular vial(s): " + advice_ParticularVialsMaxed[:-2] #strip off the final comma and space
    overall_AlchemyVialsTier = min(tier_TotalVialsUnlocked, tier_TotalVialsMaxed, tier_ParticularVialsMaxed)
    advice_AlchemyVialsCombined = ["Best Alchemy-Vials tier met: " + str(overall_AlchemyVialsTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Alchemy-Vials actions:", advice_TotalVialsUnlocked, advice_TotalVialsMaxed, advice_ParticularVialsMaxed]
    alchemyVialsPR = progressionResults.progressionResults(overall_AlchemyVialsTier,advice_AlchemyVialsCombined,"")
    return alchemyVialsPR

def setAlchemyBubblesProgressionTier(inputJSON, progressionTiers):
    tier_Template = 0
    overall_TemplateTier = 0
    overall_TemplateTier = min(progressionTiers[-1][-0], tier_Template)
    advice_TemplateCombined = ["Best Template tier met: " + str(overall_TemplateTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended template actions:"]
    templatePR = progressionResults.progressionResults(overall_TemplateTier,advice_TemplateCombined,"")
    return templatePR