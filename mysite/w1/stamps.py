from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from consts import (
    break_you_best, maxTiersPerGroup,
    stamps_progressionTiers, stamp_maxes, stampsDict, unavailableStampsList, stampTypes,
    maxOverallBookLevels, max_VialLevel, maxFarmingCrops
)
from flask import g as session_data

logger = get_logger(__name__)


def setMissingStamps():
    return [stampName for stampName, stampValues in session_data.account.stamps.items() if
            not stampValues['Delivered'] and stampName not in unavailableStampsList]

def getStampExclusions() -> dict[str, bool]:
    exclusionsDict = {
        # Capacity
        'Matty Bag Stamp': False,  # Materials
        'Foods': False,  # Doesn't exist currently, placeholder
        "Lil' Mining Baggy Stamp": False,  # Mining Ores
        "Choppin' Bag Stamp": False,  # Choppin Logs
        'Bag o Heads Stamp': False,  # Fish
        'Bugsack Stamp': False,  # Catching Bugs
        'Critters': False,  # Doesn't exist currently, placeholder
        'Souls': False,  # Doesn't exist currently, placeholder
        'Mason Jar Stamp': False,  # All types, but less per level
        # Others
        'Triad Essence Stamp': False,  # Sussy Gene quests
        'Summoner Stone Stamp': False,
        'Void Axe Stamp': False,
        'Crop Evo Stamp': False,
    }
    if session_data.account.stamps['Crystallin']['Level'] >= 270:  # Highest Crystallin in Tiers
        exclusionsDict['Matty Bag Stamp'] = True
    if session_data.account.stamps['Multitool Stamp']['Level'] >= 220:  # Highest Multitool in Tiers
        exclusionsDict['Bugsack Stamp'] = True
        exclusionsDict['Bag o Heads Stamp'] = True
    if exclusionsDict['Matty Bag Stamp'] and exclusionsDict['Bugsack Stamp'] and exclusionsDict['Bag o Heads Stamp']:
        exclusionsDict['Mason Jar Stamp'] = True

    # If all summoning matches are finished, exclude the Sussy Gene stamps if not obtained
    if session_data.account.summoning['AllBattlesWon']:
        exclusionsDict['Triad Essence Stamp'] = True if not session_data.account.stamps['Triad Essence Stamp']['Delivered'] else False
        exclusionsDict['Summoner Stone Stamp'] = True if not session_data.account.stamps['Summoner Stone Stamp']['Delivered'] else False
        exclusionsDict['Void Axe Stamp'] = True if not session_data.account.stamps['Void Axe Stamp']['Delivered'] else False

    if session_data.account.farming['CropsUnlocked'] >= maxFarmingCrops:
        exclusionsDict['Crop Evo Stamp'] = True

    return exclusionsDict

def getCapacityAdviceGroup() -> AdviceGroup:
    capacity_Advices = {"Stamps": [], "Account Wide": [], "Character Specific": []}

    starsignBase = 0
    starsignBase += 30 * bool(session_data.account.star_signs['Mr No Sleep']['Unlocked'])
    starsignBase += 10 * bool(session_data.account.star_signs['Pack Mule']['Unlocked'])
    starsignBase += 5 * bool(session_data.account.star_signs['The OG Skiller']['Unlocked'])
    totalStarsignValue = starsignBase * session_data.account.star_sign_extras['SilkrodeNanoMulti'] * session_data.account.star_sign_extras['SeraphMulti']

    # Stamps
    capacity_Advices["Stamps"].append(Advice(
        label="{{ Jade Emporium|#sneaking }}: Level Exemption",
        picture_class="level-exemption",
        progression=1 if session_data.account.sneaking['JadeEmporium']['Level Exemption']['Obtained'] else 0,
        goal=1
    ))
    capacity_Advices["Stamps"].append(Advice(
        label=f"Lab: Certified Stamp Book: "
              f"{max(1, 2 * session_data.account.labBonuses['Certified Stamp Book']['Enabled'])}/2x",
        picture_class="certified-stamp-book",
        progression=int(session_data.account.labBonuses['Certified Stamp Book']['Enabled']),
        goal=1
    ))
    # I'm kinda doubting Lava ever fixes this bug, so hiding it
    # capacity_Advices["Stamps"].append(Advice(
    #     label="Lab Jewel: Pure Opal Navette (lol jk, this is bugged)",
    #     picture_class="pure-opal-navette",
    # ))
    capacity_Advices["Stamps"].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Liqorice Rolle: "
              f"{'1.25' if session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained'] else '1'}/1.25x",
        picture_class=session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Image'],
        progression=int(session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']),
        goal=1
    ))
    for capStamp in ["Mason Jar Stamp", "Lil' Mining Baggy Stamp", "Choppin' Bag Stamp", "Matty Bag Stamp", "Bag o Heads Stamp", "Bugsack Stamp"]:
        capacity_Advices["Stamps"].append(Advice(
            label=f"{capStamp}: "
                  f"{session_data.account.stamps.get(capStamp, {}).get('Level', 0)}/{stamp_maxes.get(capStamp, 999)}%",
            picture_class=capStamp,
            progression=session_data.account.stamps.get(capStamp, {}).get('Level', 0),
            goal=stamp_maxes.get(capStamp, 999),
            resource=session_data.account.stamps.get(capStamp, {}).get('Material', 0),
        ))

    # Account-Wide
    capacity_Advices["Account Wide"].append(Advice(
        label=f"{{{{ Bribe|#bribes }}}}: Bottomless Bags: "
              f"{'5' if session_data.account.bribes['W4']['Bottomless Bags'] >= 1 else '0'}/5%",
        picture_class="bottomless-bags",
        progression=1 if session_data.account.bribes['W4']['Bottomless Bags'] >= 1 else 0,
        goal=1
    ))
    capacity_Advices["Account Wide"].append(Advice(
        label="Guild Bonus: Rucksack",
        picture_class="rucksack",
        progression=f"{session_data.account.guildBonuses.get('Rucksack', 0) if session_data.account.guildBonuses.get('Rucksack', 0) > 0 else 'IDK'}",
        goal=50
    ))
    capacity_Advices["Account Wide"].append(session_data.account.shrine_advices['Pantheon Shrine'])
    capacity_Advices["Account Wide"].append(session_data.account.shrine_advices['Chaotic Chizoar Card'])
    capacity_Advices["Account Wide"].append(Advice(
        label=f"{{{{ Gem Shop|#gem-shop }}}}: Carry Capacity: "
              f"{(25 * session_data.account.gemshop.get('Carry Capacity', 0))}%/250%",
        picture_class="carry-capacity",
        progression=session_data.account.gemshop.get("Carry Capacity", 0),
        goal=10
    ))
    capacity_Advices["Account Wide"].append(session_data.account.star_sign_extras['SeraphAdvice'])

    # Character Specific
    capacity_Advices["Character Specific"].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Starsign: Mr No Sleep: {30 * session_data.account.star_signs['Mr No Sleep']['Unlocked']}/30% base",
        picture_class="mr-no-sleep",
        progression=int(session_data.account.star_signs['Mr No Sleep']['Unlocked']),
        goal=1
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Starsign: Pack Mule: {10 * session_data.account.star_signs['Pack Mule']['Unlocked']}/10% base",
        picture_class="pack-mule",
        progression=int(session_data.account.star_signs['Pack Mule']['Unlocked']),
        goal=1
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Starsign: The OG Skiller: {5 * session_data.account.star_signs['The OG Skiller']['Unlocked']}/5% base",
        picture_class="the-og-skiller",
        progression=int(session_data.account.star_signs['The OG Skiller']['Unlocked']),
        goal=1
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Total Starsign Value: {totalStarsignValue:.2f}%",
        picture_class="telescope",
    ))
    # This only checks if they are max booked, not if they are actually maxed in either of their presets
    bestJmanBagBook = max([jman.max_talents.get("78", 0) for jman in session_data.account.jmans], default=0)
    capacity_Advices["Character Specific"].append(Advice(
        label="Jman's Extra Bags talent (Materials only)",
        picture_class="extra-bags",
        progression=bestJmanBagBook,
        goal=maxOverallBookLevels
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label="80 available {{ Inventory Slots|#storage }}",
        picture_class="storage"
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label="Highest Type-Specific Capacity Bag crafted",
        picture_class="herculean-matty-pouch",
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"{{{{ Prayer|#prayers }}}}: Ruck Sack: {session_data.account.prayers['Ruck Sack']['BonusValue']}/177%",
        picture_class="ruck-sack",
        progression=session_data.account.prayers['Ruck Sack']['Level'],
        goal=50
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"{{{{ Prayer|#prayers }}}}: REMOVE ZERG RUSHOGEN ({session_data.account.prayers['Zerg Rushogen']['CurseString']})",
        picture_class="zerg-rushogen",
        progression="❌"
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label="Star Talent: Telekinetic Storage",
        picture_class="telekinetic-storage",
        progression=5 * session_data.account.merits[2][3]['Level'],
        goal=5 * session_data.account.merits[2][3]['MaxLevel']
    ))

    for group_name in capacity_Advices:
        for advice in capacity_Advices[group_name]:
            mark_advice_completed(advice)

    # Build the AdviceGroup
    capacity_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Carry Capacity",
        advices=capacity_Advices,
        post_string="",
        informational=True
    )
    return capacity_AdviceGroup

def getCostReductionAdviceGroup() -> AdviceGroup:
    costReduction_Advices = {"Vials": [], "Uncapped": []}

    costReduction_Advices["Vials"].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Blue Flav (Platinum Ore)",
        picture_class="platinum-ore",
        progression=session_data.account.alchemy_vials['Blue Flav (Platinum Ore)']['Level'],
        goal=max_VialLevel
    ))
    costReduction_Advices["Vials"].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Venison Malt (Mongo Worm Slices)",
        picture_class="mongo-worm-slices",
        progression=session_data.account.alchemy_vials['Venison Malt (Mongo Worm Slices)']['Level'],
        goal=max_VialLevel
    ))
    costReduction_Advices["Vials"].append(Advice(
        label="Lab: My 1st Chemistry Set",
        picture_class="my-1st-chemistry-set",
        progression=int(session_data.account.labBonuses['My 1st Chemistry Set']['Enabled']),
        goal=1
    ))

    blueFavReduction = session_data.account.alchemy_vials['Blue Flav (Platinum Ore)']['Value']
    venisonMaltReduction = session_data.account.alchemy_vials['Venison Malt (Mongo Worm Slices)']['Value']
    totalVialReduction = blueFavReduction + venisonMaltReduction
    totalVialReduction *= session_data.account.vialMasteryMulti
    if session_data.account.labBonuses['My 1st Chemistry Set']['Enabled']:
        totalVialReduction *= 2
    costReduction_Advices["Vials"].append(Advice(
        label=f"{{{{ Rift|#rift }}}}: Vial Mastery: {session_data.account.vialMasteryMulti:.2f}x",
        picture_class="vial-mastery",
        progression=f"{1 if session_data.account.rift['VialMastery'] else 0}",
        goal=1
    ))
    costReduction_Advices["Vials"].append(Advice(
        label="Total Vial reduction (90% hardcap)",
        picture_class="vials",
        progression=f"{totalVialReduction:.2f}",
        goal=90,
        unit="%"
    ))

    costReduction_Advices["Uncapped"].append(Advice(
        label="{{ Jade Emporium|#sneaking }}: Ionized Sigils",
        picture_class="ionized-sigils",
        progression=int(session_data.account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']),
        goal=1
    ))
    if (session_data.account.alchemy_p2w.get('Sigils', {}).get('Envelope Pile', {}).get('PrechargeLevel', 0)
            > session_data.account.alchemy_p2w.get('Sigils', {}).get('Envelope Pile', {}).get('Level', 0)):
        envelope_pile_precharged = '(Precharged)'
    else:
        envelope_pile_precharged = ''
    costReduction_Advices["Uncapped"].append(Advice(
        label=f"Sigil: Envelope Pile {envelope_pile_precharged}",
        picture_class="envelope-pile",
        progression=session_data.account.alchemy_p2w.get("Sigils", {}).get("Envelope Pile", {}).get("PrechargeLevel", 0),
        goal=3
    ))
    costReduction_Advices["Uncapped"].append(Advice(
        label=f"{{{{ Artifact|#sailing }}}}: Chilled Yarn increases sigil by {1 + session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']}x",
        picture_class="chilled-yarn",
        progression=session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'],
        goal=4
    ))

    for group_name in costReduction_Advices:
        for advice in costReduction_Advices[group_name]:
            mark_advice_completed(advice)

    # Build the AdviceGroup
    costReduction_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Stamp Cost Reduction",
        advices=costReduction_Advices,
        post_string="",
        informational=True
    )
    return costReduction_AdviceGroup

def getReadableStampName(stampNumber, stampType):
    # logger.debug(f"Fetching name for {stampType} + {stampNumber}")
    return stampsDict.get(stampType, {}).get(stampNumber, f"Unknown{stampType}{stampNumber}")

def getProgressionTiersAdviceGroup():
    stamp_AdviceDict = {
        "StampLevels": [],
        "FindStamps": {
            "Combat": {},
            "Skill": {},
            "Misc": {},
            "Optional": {}
        },
        "Specific": {},
    }
    info_tiers = 3
    max_tier = max(stamps_progressionTiers.keys()) - info_tiers
    tier_StampLevels = 0
    tier_FindStamps = {"Combat": 0, "Skill": 0, "Misc": 0}
    tier_SpecificStamps = 0
    adviceCountsDict = {"Combat": 0, "Skill": 0, "Misc": 0, "Specific": 0}
    playerStamps = session_data.account.stamps
    missingStampsList = setMissingStamps()
    exclusionsDict = getStampExclusions()

    #Assess Tiers
    for tier in stamps_progressionTiers:
        subgroupName = f"To reach {'Informational ' if tier > max_tier else ''}Tier {tier}"
        # TotalLevelStamps
        if tier_StampLevels == tier - 1:
            if session_data.account.stamp_totals.get("Total", 0) >= stamps_progressionTiers[tier].get("TotalStampLevels", 0):  # int
                tier_StampLevels = tier
            else:
                advice_StampLevels = stamps_progressionTiers[tier].get("TotalStampLevels", 0)
                stamp_AdviceDict["StampLevels"].append(
                    Advice(
                        label="Total Stamp Levels",
                        picture_class="stat-graph-stamp",
                        progression=session_data.account.stamp_totals.get("Total", 0),
                        goal=advice_StampLevels)
                )

        # Collect important Combat, Skill, and Misc stamps
        for stampType in stampTypes:
            for rStamp in stamps_progressionTiers[tier].get("Stamps").get(stampType, []):
                if rStamp in missingStampsList and exclusionsDict.get(rStamp, False) == False:
                    if subgroupName not in stamp_AdviceDict["FindStamps"][stampType] and len(stamp_AdviceDict["FindStamps"][stampType]) < maxTiersPerGroup:
                        stamp_AdviceDict["FindStamps"][stampType][subgroupName] = []
                    if subgroupName in stamp_AdviceDict["FindStamps"][stampType]:
                        adviceCountsDict[stampType] += 1
                        stamp_AdviceDict["FindStamps"][stampType][subgroupName].append(
                            Advice(
                                label=f"{rStamp}, leveled with {playerStamps.get(rStamp, {}).get('Material', '').replace('-', ' ').title()}",
                                picture_class=rStamp,
                                resource=playerStamps.get(rStamp, {}).get('Material', ''),
                            ))
            if tier_FindStamps[stampType] == tier - 1 and adviceCountsDict[stampType] == 0:  # Only update if they already met previous tier
                tier_FindStamps[stampType] = tier

        # SpecificStampLevels
        for stampName, stampRequiredLevel in stamps_progressionTiers[tier].get("Stamps", {}).get("Specific", {}).items():
            if playerStamps.get(stampName, {}).get("Level", 0) < stampRequiredLevel and exclusionsDict.get(stampName, False) == False:
                # logger.debug(f"Tier {tier} requirement for {stampName} failed: {playerStamps.get(stampName, {}).get('Level', 0)} is less than {stampRequiredLevel}")
                if subgroupName not in stamp_AdviceDict["Specific"] and len(stamp_AdviceDict["Specific"]) < maxTiersPerGroup:
                    stamp_AdviceDict["Specific"][subgroupName] = []
                if subgroupName in stamp_AdviceDict["Specific"]:
                    adviceCountsDict["Specific"] += 1
                    stamp_AdviceDict["Specific"][subgroupName].append(
                        Advice(
                            label=stampName,
                            picture_class=stampName,
                            progression=playerStamps.get(stampName, {}).get("Level", 0),
                            goal=stampRequiredLevel,
                            resource=playerStamps.get(stampName, {}).get('Material', ''),
                        ))

        if tier_SpecificStamps == tier - 1 and adviceCountsDict["Specific"] == 0:
            tier_SpecificStamps = tier

        # Optional Stamps
        for rStamp in stamps_progressionTiers[tier].get("Stamps").get("Optional", []):
            if rStamp in missingStampsList and exclusionsDict.get(rStamp, False) == False:
                subgroupName = f"Previously Tier {tier}"
                if subgroupName not in stamp_AdviceDict["FindStamps"]["Optional"]:  # and len(stamp_AdviceDict["FindStamps"]["Optional"]) < maxTiersPerGroup:
                    stamp_AdviceDict["FindStamps"]["Optional"][subgroupName] = []
                if subgroupName in stamp_AdviceDict["FindStamps"]["Optional"]:
                    # adviceCountsDict["Optional"] += 1
                    stamp_AdviceDict["FindStamps"]["Optional"][subgroupName].append(
                        Advice(
                            label=f"{rStamp} ({playerStamps.get(rStamp).get('StampType')})",
                            picture_class=rStamp,
                            resource=playerStamps.get(rStamp, {}).get('Material', ''),
                        ))

    # Generate AdviceGroups
    stamp_AdviceGroupDict = {
        "StampLevels": AdviceGroup(
            tier=tier_StampLevels if tier_StampLevels < max_tier else '',
            pre_string=f"{'Informational- ' if tier_StampLevels >= max_tier else ''}"
                       f"Improve your total stamp levels",
            advices=stamp_AdviceDict["StampLevels"],
            informational=tier_StampLevels >= max_tier
        ),
        "SpecificStamps": AdviceGroup(
            tier=tier_SpecificStamps if tier_SpecificStamps < max_tier else '',
            pre_string=f"{'Informational- ' if tier_SpecificStamps >= max_tier else ''}"
                       f"Improve high-priority stamp{pl([''] * adviceCountsDict['Specific'])}",
            advices=stamp_AdviceDict["Specific"],
            informational=tier_SpecificStamps >= max_tier
        ),
        "Combat": AdviceGroup(
            tier=tier_FindStamps["Combat"],
            pre_string=f"Collect the following Combat stamp{pl([''] * adviceCountsDict['Combat'])}",
            advices=stamp_AdviceDict["FindStamps"]['Combat']
        ),
        "Skill": AdviceGroup(
            tier=tier_FindStamps["Skill"],
            pre_string=f"Collect the following Skill stamp{pl([''] * adviceCountsDict['Skill'])}",
            advices=stamp_AdviceDict["FindStamps"]["Skill"]
        ),
        "Misc": AdviceGroup(
            tier=tier_FindStamps["Misc"],
            pre_string=f"Collect the following Misc stamp{pl([''] * adviceCountsDict['Misc'])}",
            advices=stamp_AdviceDict["FindStamps"]["Misc"]
        ),
        "Optional": AdviceGroup(
            tier='',
            pre_string=f"Owning every stamp slightly reduces your chances for the BEST stamps to be chosen by the Sacred Methods bundle on each daily reset."
                       f" These stamps are Optional",
            advices=stamp_AdviceDict["FindStamps"]["Optional"]
        )
    }
    overall_SectionTier = min(
        max_tier + info_tiers, tier_StampLevels,
        tier_FindStamps["Combat"], tier_FindStamps["Skill"], tier_FindStamps["Misc"],
        tier_SpecificStamps
    )
    return stamp_AdviceGroupDict, overall_SectionTier, max_tier

def getStampAdviceSection() -> AdviceSection:
    # Generate AdviceGroups
    stamp_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    stamp_AdviceGroupDict["Capacity"] = getCapacityAdviceGroup()
    stamp_AdviceGroupDict["CostReduction"] = getCostReductionAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    stamp_AdviceSection = AdviceSection(
        name="Stamps",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Stamp tier met: {tier_section}"
               f"{break_you_best if overall_SectionTier >= max_tier else ''}"
               f"{'<br>Let me know what important stamps you re aiming for next!' if overall_SectionTier >= max_tier else ''}",
        picture="Stamps_Header.png",
        groups=stamp_AdviceGroupDict.values()
    )
    return stamp_AdviceSection
