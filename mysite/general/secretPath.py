from models.models import AdviceSection, AdviceGroup, Advice, Character
from utils.data_formatting import safe_loads
from utils.logging import get_logger
from flask import g as session_data
from consts import numberOfSecretClasses, break_you_best
from utils.text_formatting import pl

logger = get_logger(__name__)

skillsToReview_RightHand = ["Mining", "Choppin", "Fishing", "Catching", "Trapping", "Worship"]

def getRightHandsAdviceGroups():
    catchup_advices = []
    skills_needing_catchup = []
    stayahead_advices = {}
    sorted_skills = {}

    for skill in skillsToReview_RightHand:
        sorted_skills[skill] = []
        stayahead_advices[skill] = []
        for char in session_data.account.all_characters:
            #Only add specialized characters per skill
            if skill in char.specialized_skills or 'Maestro' in char.all_classes:
                sorted_skills[skill].append(char)
        sorted_skills[skill]: list[Character] = sorted(
            sorted_skills[skill], key=lambda toon: toon.skills[skill], reverse=True
        )
        highest_skill_level = sorted_skills[skill][0].skills[skill]
        characters_at_highest = sum(1 for char in sorted_skills[skill] if char.skills[skill] == highest_skill_level)

        #If Maestro isn't in first, place into Catchup
        if characters_at_highest > 1:
            skills_needing_catchup.append(skill)
            highest_jman_name = ''
            highest_jman_level = 0
            for char in sorted_skills[skill]:
                if 'Maestro' in char.all_classes:
                    highest_jman_name = char.character_name
                    highest_jman_level = char.skills[skill]
                    break
            if highest_jman_level == highest_skill_level:
                catchup_advices.append(Advice(
                    label=f"{highest_jman_name} is tied for best in {skill}."
                          f"<br>Right Hand buff only applies if they're STRICTLY better 🙁",
                    picture_class=skill,
                    progression=highest_jman_level,
                    goal=highest_jman_level + 1
                ))
            else:
                catchup_advices.append(Advice(
                    label=f"{highest_jman_name} {'is the highest leveled Mman but still ' if len(session_data.account.maestros) > 1 else ''}"
                          f"not best in {skill}",
                    picture_class=skill,
                    progression=highest_jman_level,
                    goal=sorted_skills[skill][0].skills[skill]+1
                ))
        elif characters_at_highest == 1 and 'Maestro' not in sorted_skills[skill][0].all_classes:
            skills_needing_catchup.append(skill)
            highest_jman_name = ''
            highest_jman_level = 0
            for char in sorted_skills[skill]:
                if 'Maestro' in char.all_classes:
                    highest_jman_name = char.character_name
                    highest_jman_level = char.skills[skill]
                    break
            catchup_advices.append(Advice(
                label=f"{highest_jman_name} {'is the highest leveled Mman but still ' if len(session_data.account.maestros) > 1 else ''}"
                      f"not best in {skill}",
                picture_class=skill,
                progression=highest_jman_level,
                goal=sorted_skills[skill][0].skills[skill] + 1
            ))

        #Now for StayAhead / all specialized characters
        #Display the leader
        if characters_at_highest == 1:
            stayahead_advices[skill].append(Advice(
                label=f"{'🛑' if 'Maestro' not in sorted_skills[skill][0].all_classes else ''} {sorted_skills[skill][0].character_name} is currently best at {skill}",
                picture_class=sorted_skills[skill][0].class_name_icon,
                progression=sorted_skills[skill][0].skills[skill],
            ))
        else:
            stayahead_advices[skill].append(Advice(
                label=f"{sorted_skills[skill][0].character_name} is currently TIED for best at {skill}",
                picture_class=sorted_skills[skill][0].class_name_icon,
                progression=sorted_skills[skill][0].skills[skill],
            ))
        no_goal = True if characters_at_highest > 1 else False
        #Display the rest
        if len(sorted_skills[skill]) > 1:
            for char in sorted_skills[skill][1:]:
                if 'Maestro' not in char.all_classes:
                    label_symbol = '🛑'
                else:
                    if 'Maestro' in sorted_skills[skill][0].all_classes:
                        label_symbol = '⚠️'
                    else:
                        label_symbol = '✔️'
                stayahead_advices[skill].append(Advice(
                    label=(
                        f"{char.character_name} can level {skill}"  # to {sorted_skills[skill][0].skills[skill]-1}"
                        if char.skills[skill] < sorted_skills[skill][0].skills[skill]-1
                        else f"{label_symbol} {char.character_name} will {'overtake' if char.skills[skill] == highest_skill_level else 'tie'} {skill} if leveled any further"
                    ),
                    picture_class=char.class_name_icon,
                    progression=char.skills[skill],
                    goal=sorted_skills[skill][0].skills[skill] - 1 if not no_goal else ''
                ))
        # except Exception as reason:
        #     logger.exception(f"Couldn't figure out how to evaluate {skill}: {reason}")
        #     stayahead_advices[skill].append(Advice(
        #         label=f"Something went wrong trying to figure out where to place {sorted_skills[skill][0].character_name}"
        #               f"<br>Please contact Scoli with your Data so he can review!",
        #         picture_class=sorted_skills[skill][0].class_name_icon,
        #         progression=sorted_skills[skill][0].skills[skill],
        #     ))

    #Catch Up
    catchup_ag = AdviceGroup(
        tier='',
        pre_string=(
            f"{pl(session_data.account.maestros, f'{session_data.account.maestros[0]} is not', 'Your Maestros are not')}"
            f" best in {len(skills_needing_catchup)} Right Hand Skill{pl(skills_needing_catchup)}"
        ),
        advices=catchup_advices,
        post_string=(
            f"Right Hand gives about 8% more Souls and Critters, and Species Epoch gives about 6% PER Trapping and Worship level! "
            f"Don't steal {'Vman' if session_data.account.vmans else 'Mman'}'s Worship Charge, and don't slack on your Crystal Countdowns!"
            if 'Worship' in skills_needing_catchup or 'Trapping' in skills_needing_catchup
            else ''
        ),
    )
    if catchup_advices:
        session_data.account.alerts_AdviceDict['General'].append(Advice(
            label=f"Your {{{{ Maestro|#secret-class-path }}}} isn't best in {len(catchup_advices)} Skill{pl(catchup_advices)}",
            picture_class='right-hand-of-action',
        ))

    #Stay Ahead
    stayahead_ag = AdviceGroup(
        tier='',
        pre_string=(
            f"Your Maestro{pl(len(session_data.account.maestros), ' is', 's are')}"
            f" the highest level in {len(skillsToReview_RightHand)-len(skills_needing_catchup)}/{len(skillsToReview_RightHand)}"
            f" Right Hand skills. Be careful not to let others overtake"
        ),
        advices=stayahead_advices
    )
    stayahead_ag.remove_empty_subgroups()
    return catchup_ag, stayahead_ag

def setSecretClassProgressionTier():
    secretClass_AdviceDict = {
        "UnlockNextClass": [],
    }
    secretClass_AdviceGroupDict = {}
    secretClass_AdviceSection = AdviceSection(
        name="Secret Class Path",
        tier="0",
        pinchy_rating=0,
        header="Best Secret Class Path tier met: Not Yet Evaluated",
        picture="Stone_Peanut.png"
    )

    max_tier = numberOfSecretClasses
    tier_SecretClass = 0

    beginners = session_data.account.beginners
    jmans = session_data.account.jmans
    maestros = session_data.account.maestros
    vmans = session_data.account.vmans

    if "Infinilyte" in session_data.account.classes:
        tier_SecretClass = 4
    elif "Voidwalker" in session_data.account.classes:
        tier_SecretClass = 3
    elif "Maestro" in session_data.account.classes:
        tier_SecretClass = 2
    elif "Journeyman" in session_data.account.classes:
        tier_SecretClass = 1

    #No Journeyman
    if tier_SecretClass == 0:
        bush1complete = False
        bush2complete = False
        bush3complete = False
        rock1complete = False
        rock2complete = False
        for characterIndex in range(0, len(session_data.account.all_quests)):
            if session_data.account.all_quests[characterIndex].get("Bushlyte1", 0) == 1:
                bush1complete = True
            if session_data.account.all_quests[characterIndex].get("Bushlyte2", 0) == 1:
                bush2complete = True
            if session_data.account.all_quests[characterIndex].get("Bushlyte3", 0) == 1:
                bush3complete = True
            if session_data.account.all_quests[characterIndex].get("Rocklyte1", 0) == 1:
                rock1complete = True
            if session_data.account.all_quests[characterIndex].get("Rocklyte2", 0) == 1:
                rock2complete = True
        totalQuestPeanuts = 1651 - (51*bush1complete) - (200*bush2complete) - (400*bush3complete) - (500*rock1complete) - (500*rock2complete)
        goldenPeanutsOwned = session_data.account.all_assets.get("PeanutG").amount
        peanutsOwned = session_data.account.all_assets.get("Peanut").amount
        if goldenPeanutsOwned < 6:
            peanutsRemaining = totalQuestPeanuts - peanutsOwned - (goldenPeanutsOwned*100)
        else:
            peanutsRemaining = totalQuestPeanuts - peanutsOwned - 500
        secretClass_AdviceDict["UnlockNextClass"].append(Advice(
            label="On your 7th or later character, create a Journeyman. Only make 1 Secret Class character!",
            picture_class="journeyman-icon"
        ))
        secretClass_AdviceDict["UnlockNextClass"].append(Advice(
            label="Skip this fool's quest. You need to stay a Beginner to become a Journeyman!",
            picture_class="promotheus"
        ))
        secretClass_AdviceDict["UnlockNextClass"].append(Advice(
            label="Start the Journeyman quest chain by finding this NPC in World 1! You'll need 1651 Peanuts in total.",
            picture_class="bushlyte"
        ))
        secretClass_AdviceDict["UnlockNextClass"].append(Advice(
            label="Peanuts are crafted at the anvil",
            picture_class="peanut",
            progression=peanutsOwned,
            goal=totalQuestPeanuts
        ))
        if peanutsRemaining > 0:
            peanuts_subgroup = f"Ingredients for the remaining {peanutsRemaining} Peanuts:"
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label=peanuts_subgroup,
                picture_class="",
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Hot Dogs can be purchased from both W1 Vendors daily",
                picture_class="hot-dog",
                progression=session_data.account.all_assets.get("FoodHealth3").amount,
                goal=2 * peanutsRemaining
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Bleach Logs",
                picture_class="bleach-logs",
                progression=session_data.account.all_assets.get("BirchTree").amount,
                goal=peanutsRemaining
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Copper Ore",
                picture_class="copper-ore",
                progression=session_data.account.all_assets.get("Copper").amount,
                goal=peanutsRemaining
            ))

            if goldenPeanutsOwned < 5:
                #Add advice for gold bars
                secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                    label="Gold Bars",
                    picture_class="gold-bar",
                    progression=session_data.account.stored_assets.get("GoldBar").amount,
                    goal=250 - (50 * goldenPeanutsOwned)
                ))
            else:
                #Add advice for golden peanuts
                secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                    label="Gold Peanuts",
                    picture_class="golden-peanut",
                    progression=goldenPeanutsOwned,
                    goal=5
                ))
            for advice in secretClass_AdviceDict["UnlockNextClass"]:
                try:
                    if int(advice.progression) >= int(advice.goal):
                        advice.label += " (Ready!)"
                except:
                    pass

    #No Maestro
    elif tier_SecretClass == 1:

        cact1Started = False
        cact1complete = False
        cact2complete = False
        cact3Started = False
        cact3complete = False
        for jman in jmans:
            if not cact1Started:
                try:
                    cact1Started = session_data.account.all_quests[jman.character_index]["Cactolyte1"] >= 0
                except:
                    continue
            if not cact1complete:
                try:
                    cact1complete = session_data.account.all_quests[jman.character_index]["Cactolyte1"] >= 1
                except:
                    continue
            if not cact2complete:
                try:
                    cact2complete = session_data.account.all_quests[jman.character_index]["Cactolyte2"] >= 1
                except:
                    continue
            if not cact3Started:
                try:
                    cact3Started = session_data.account.all_quests[jman.character_index]["Cactolyte3"] >= 0
                except:
                    continue
            if not cact3complete:
                try:
                    cact3complete = session_data.account.all_quests[jman.character_index]["Cactolyte3"] >= 1
                except:
                    continue
        if not cact1Started:
            if session_data.account.stored_assets.get("Quest27").amount < 1:  # Quest27 = Bag o Nuts
                secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                    label="First, you'll need to finish Goldric's quest: Dress to Impress",
                    picture_class="goldric"
                ))
                secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                    label="This will reward you with a Bag o Nuts needed to start the Maestro quest",
                    picture_class="bag-o-nuts"
                ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Offer the Bag o Nuts to this NPC in World 2!",
                picture_class="cactolyte"
            ))
        for jman in jmans:
            if not cact1complete:
                if jman.mining_level < 32:
                    secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                        label=f"Level {jman.character_name}'s Mining",
                        picture_class="mining",
                        progression=jman.mining_level,
                        goal=32
                    ))
                if jman.smithing_level < 35:
                    secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                        label=f"Level {jman.character_name}'s Smithing",
                        picture_class="smithing",
                        progression=jman.smithing_level,
                        goal=35
                    ))
                if jman.choppin_level < 33:
                    secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                        label=f"Level {jman.character_name}'s Choppin",
                        picture_class="choppin",
                        progression=jman.choppin_level,
                        goal=33
                    ))
            if not cact2complete:
                if jman.fishing_level < 23:
                    secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                        label=f"Level {jman.character_name}'s Fishing",
                        picture_class="fishing",
                        progression=jman.fishing_level,
                        goal=23
                    ))
                if jman.alchemy_level < 25:
                    secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                        label=f"Level {jman.character_name}'s Alchemy",
                        picture_class="alchemy",
                        progression=jman.alchemy_level,
                        goal=25
                    ))
                if jman.catching_level < 25:
                    secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                        label=f"Level {jman.character_name}'s Catching",
                        picture_class="catching",
                        progression=jman.catching_level,
                        goal=25
                    ))
        if (len(secretClass_AdviceDict["UnlockNextClass"]) == 0 and cact2complete and not cact3complete) or (cact3Started and not cact3complete):
            #if session_data.account.assets.get("Quest35").amount < 1:  # Quest35 = Googley Eyes to spawn Biggie Hours
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Find the Googley Eyes recipe from Crabcakes to spawn Biggie Hours",
                picture_class="googley-eyes"
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Remember to have Pete the Peanut in your Inventory before spawning Biggie Hours!",
                picture_class="pete-the-peanut"
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="594 Defense is needed to take 0 damage from Biggie Hours. You can use your best Fisticuffs safely if you reach this amount of defense.",
                picture_class="bucklered-up"
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Alternative to stacking Defense: Use the Wooden Bow to attack from a distance. Hide down the rope if he gets too close!",
                picture_class="wooden-bow"
            ))
        if len(secretClass_AdviceDict["UnlockNextClass"]) == 0 and cact3complete:
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Congrats on killing Biggie Hours! Maestro! The Stro! Mman! Now turn in the quest, silly billy.",
                picture_class="club-maestro"
            ))

    #No Voidwalker
    elif tier_SecretClass == 2:
        neb1status = -1
        neb1platskulls = 0
        neb2status = -1
        neb3status = -1
        neb3gmushkills = 0
        neb4status = -1
        for maestro in maestros:
            if neb1status == -1:
                try:
                    neb1status = session_data.account.all_quests[maestro.character_index]["Nebulyte1"] if "Nebulyte1" in session_data.account.all_quests[maestro.character_index] else -1
                except:
                    continue
            if neb1status >= 0:
                neb1platskulls = 0
                try:
                    playerneb1Int = session_data.account.raw_data.get(f"QuestStatus_{maestro.character_index}", "{\"Nebulyte1\": [\"0\", \"0\"]}")
                    #logger.debug(f"playerneb1Int = {type(playerneb1Int)}: {playerneb1Int}")
                    if isinstance(playerneb1Int, str):
                        playerneb1Int = safe_loads(playerneb1Int)
                        playerneb1Int = playerneb1Int.get("Nebulyte1", ["0", "0"])
                        playerneb1Int = int(playerneb1Int[0])
                        #logger.debug(f"After json.loads, playerneb1Int = {type(playerneb1Int)}: {playerneb1Int}")
                    #playerneb1Int = int(session_data.account.raw_data.get(f"QuestStatus_{maestro.character_index}", {"Nebulyte1":[0,0]})[0])
                    neb1platskulls = max(playerneb1Int, neb1platskulls)
                except Exception as reason:
                    logger.warning(f"Could not retrieve 'Nebulyte1' in QuestStatus_{maestro.character_index} because: {reason}")
            if neb2status == -1:
                try:
                    neb2status = session_data.account.all_quests[maestro.character_index]["Nebulyte2"] if "Nebulyte2" in session_data.account.all_quests[maestro.character_index] else -1
                except:
                    continue
            if neb3status == -1:
                try:
                    neb3status = session_data.account.all_quests[maestro.character_index]["Nebulyte3"] if "Nebulyte3" in session_data.account.all_quests[maestro.character_index] else -1
                except:
                    continue
            if neb3status == 0:
                try:
                    playerneb3Int = session_data.account.raw_data.get(f"QuestStatus_{maestro.character_index}", "{\"Nebulyte3\": [\"0\"]}")
                    #logger.debug(f"playerneb3Int = {type(playerneb3Int)}: {playerneb3Int}")
                    if isinstance(playerneb3Int, str):
                        playerneb3Int = safe_loads(playerneb3Int)
                        playerneb3Int = playerneb3Int.get("Nebulyte1", ["0", "0"])
                        playerneb3Int = int(playerneb3Int[0])
                        #logger.debug(f"After json.loads, playerneb3Int = {type(playerneb3Int)}: {playerneb3Int}")
                    neb3gmushkills = max(playerneb3Int, neb3gmushkills)
                except Exception as reason:
                    logger.warning(f"Could not retrieve 'Nebulyte1' in QuestStatus_{maestro.character_index} because: {reason}")
            if neb4status == -1:
                try:
                    neb4status = session_data.account.all_quests[maestro.character_index]["Nebulyte4"] if "Nebulyte4" in session_data.account.all_quests[maestro.character_index] else -1
                except:
                    continue
        if neb1status == -1:
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Start the quest chain by finding this NPC in World 4!",
                picture_class="nebulyte"
            ))
            addLevelAdvice = True
            for maestro in maestros:
                if maestro.combat_level >= 150:
                    addLevelAdvice = False
            if addLevelAdvice:
                secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                    label="Hint: You'll need a minimum Combat level of 150",
                    picture_class="maestro-icon"
                ))
        elif neb1status == 0:
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Earn Platinum skulls (1 million kills) on all 40 W1-W3 enemies. You may use ALL characters to speed this up.",
                picture_class="platinum-skull",
                progression=neb1platskulls,
                goal=40
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Check out the Death Note section to see remaining enemies",
                picture_class="death-note",
                as_link=True
            ))
        if neb2status == 0:
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="What are you waiting for? Go punch Chaotic Chizoar in the face. Easy!",
                picture_class="chaotic-chizoar-card"
            ))
        if neb3status == 0:
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Kill 12 million Green Mushrooms in W1 with ONLY your Maestro on the quest!",
                picture_class="green-mushroom",
                progression=neb3gmushkills,
                goal=12000000
            ))
        if (len(secretClass_AdviceDict["UnlockNextClass"]) == 0 and neb3status >= 1) or neb4status == 0:
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="One of us! One of us! One of us! Now turn in the quest, silly billy.",
                picture_class="voidwalker-icon"
            ))

    #No Infinilyte
    # elif tier_SecretClass == 3:
    #     secretClass_AdviceDict["UnlockNextClass"].append(Advice(
    #         label="Welcome to the Infinilyte waiting room",
    #         picture_class="infinilyte-icon"
    #     ))

    group_pre_strings = [
        "Create a Journeyman",
        "Create a Maestro",
        "Create a Voidwalker",
        "Wait for Lava to release the next Secret Class"
    ]
    #Generate AdviceGroups
    secretClass_AdviceGroupDict["UnlockNextClass"] = AdviceGroup(
        tier=str(tier_SecretClass),
        pre_string=group_pre_strings[tier_SecretClass],
        advices=secretClass_AdviceDict["UnlockNextClass"]
    )
    #secretClass_AdviceGroupDict["MaestroHands"] = getHandsAdviceGroupCatchUp(vmans, maestros, beginners)
    #secretClass_AdviceGroupDict["MaestroHandsInTheLead"] = getHandsAdviceGroupStayAhead(maestros)
    if len(session_data.account.maestros) > 0:
        secretClass_AdviceGroupDict['RightHandsCatchup'], secretClass_AdviceGroupDict['RightHandsStayAhead'] = getRightHandsAdviceGroups()

    #Generate AdviceSection
    if len(maestros) > 1:
        secretClass_AdviceSection.note = (
            f"Important! Only one Maestro's Right and Left Hands buffs work."
            f"<br>On Steam, this is the last created Maestro."
            f"<br>I'm not totally sure about other platforms, sorry 🙁"
        )

    overall_SecretClassTier = min(max_tier, tier_SecretClass)
    tier_section = f"{overall_SecretClassTier}/{max_tier}"
    secretClass_AdviceSection.pinchy_rating = overall_SecretClassTier
    secretClass_AdviceSection.tier = tier_section
    secretClass_AdviceSection.groups = secretClass_AdviceGroupDict.values()
    if overall_SecretClassTier >= max_tier:
        secretClass_AdviceSection.header = f"Best Secret Class tier met: {tier_section}{break_you_best}️"
        #logger.debug(f"Number of Catchup advices: {len(secretClass_AdviceGroupDict['RightHandsCatchup'].advices['default'])}")
        if 'RightHandsCatchup' in secretClass_AdviceGroupDict:
            secretClass_AdviceSection.complete = True if len(secretClass_AdviceGroupDict['RightHandsCatchup'].advices['default']) == 0 else False
    else:
        secretClass_AdviceSection.header = f"Best Secret Class tier met: {tier_section}"

    return secretClass_AdviceSection
