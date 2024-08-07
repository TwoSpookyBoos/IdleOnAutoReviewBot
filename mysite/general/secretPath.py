import json
from models.models import AdviceSection, AdviceGroup, Advice, Character
from utils.logging import get_logger
from flask import g as session_data
from consts import numberOfSecretClasses
from utils.text_formatting import pl

logger = get_logger(__name__)

skillsToReview_RightHand = ["Mining", "Choppin", "Fishing", "Catching", "Trapping", "Worship"]

def getHandsAdviceGroupCatchUp(vmans, maestros, beginners):
    # This function returns the skills maestros aren't best in.
    janky_skills = maestros_goal_levels(maestros)
    zero_count = sum(1 for skill, (_, _, next_highest_non_maestro_char) in janky_skills.items() if not next_highest_non_maestro_char)
    if zero_count == len(skillsToReview_RightHand):
        # No maestros ahead in any skill. I think?
        return
    tier = f"{zero_count}/{len(skillsToReview_RightHand)}"
    hands_pre_string = create_hands_pre_string(janky_skills, maestros, beginners, tier)

    post_string = ""
    if "Worship" in janky_skills \
            or "Trapping" in janky_skills:
        post_string = (f"Right Hand gives about 8% more Souls and Critters, and Species Epoch gives about 6% PER Trapping and Worship level! "
                       f"Don't steal {'Vman' if vmans else 'Mman'}'s Worship Charge, and don't slack on your Crystal Countdowns!")

    advices = []

    for skill, (maestro, goal, next_highest_non_maestro_char) in janky_skills.items():
        if not next_highest_non_maestro_char:
            if len(maestros) == 1:
                fancy_label = skill
            else:
                fancy_label = f"Best {skill} Maestro: {maestro.character_name}"
            advices.append(Advice(
                label=fancy_label,
                picture_class=skill,
                progression=maestro.skills[skill],
                goal=goal,
            ))

    if advices:
        session_data.account.alerts_AdviceDict['General'].append(Advice(
            label=f"Your {{{{ Maestro|#secret-class-path }}}} isn't best in {len(advices)} Skill{pl(advices)}",
            picture_class='right-hand-of-action',
        ))

    group = AdviceGroup(
        tier="", pre_string=hands_pre_string, post_string=post_string, advices=advices
    )
    return group


def getHandsAdviceGroupStayAhead(maestros):
    # This function returns the skills maestros are best in.
    janky_skills = maestros_goal_levels(maestros)
    zero_count = sum(1 for skill, (_, _, next_highest_non_maestro_char) in janky_skills.items() if not next_highest_non_maestro_char)
    if zero_count == len(skillsToReview_RightHand):
        # No maestros ahead in any skill. I think?
        return
    tier = f"{zero_count}/{len(skillsToReview_RightHand)}"
    if len(maestros) == 1:
        hands_pre_string = (f"Your Maestro is the highest level in {len(skillsToReview_RightHand)-zero_count}/{len(skillsToReview_RightHand)}"
                            f" Right Hand skills. Be careful not to let other characters overtake")
    else:
        hands_pre_string = (f"Your Maestros are not the highest level in {len(skillsToReview_RightHand)-zero_count}/{len(skillsToReview_RightHand)}"
                            f" Right Hand skills. Be careful not to let other characters overtake")

    post_string = ""
    # if "Worship" in janky_skills \
    #         or "Trapping" in janky_skills:
    #     post_string = (f"Right Hand gives about 8% more Souls and Critters, and Species Epoch gives about 6% PER Trapping and Worship level! "
    #                    f"Don't steal Mman's Worship Charge, and don't slack on your Crystal Countdowns!")

    advices_first = []

    for skill, (maestro, goal, next_highest_non_maestro_char) in janky_skills.items():
        if next_highest_non_maestro_char:
            if next_highest_non_maestro_char.skills[skill] == maestro.skills[skill] - 1:
                fancy_label = f"🛑 {next_highest_non_maestro_char} should not level {skill} any further."
            else:
                fancy_label = f"{next_highest_non_maestro_char} can level {skill} to {maestro.skills[skill] - 1}"
            advices_first.append(Advice(
                label=fancy_label,
                #label=f"{'🛑 ' if next_highest_non_maestro_char.skills[skill] == maestro.skills[skill]-1 else ''}"
                #f"{maestro.character_name} has {maestro.skills[skill]} {skill}. Next closest is {next_highest_non_maestro_char} at {next_highest_non_maestro_char.skills[skill]}",

                picture_class=skill,
                progression=next_highest_non_maestro_char.skills[skill],
                goal=maestro.skills[skill]-1
            ))

    group = AdviceGroup(
        tier="", pre_string=hands_pre_string, post_string=post_string, advices=advices_first
    )
    return group


def create_hands_pre_string(janky_skills, maestros, beginners, tier):
    account = session_data.account
    if not maestros:
        header = "Gosh golly, I'm jealous, So many nice things ahead of you!<br>Check this section again once you've acquired a Maestro"

        if len(account.safe_characters) == account.max_toon_count and not beginners:
            header = "Oh… Oh no… Your family is full but I don't see any future Maestros…<br>I wish you the best of luck 😔"

    else:

        # if maestros are the highest in all skills
        if not janky_skills:
            if len(maestros) > 1:
                header = "Your Maestros are a workforce to be dealt with! An arduous bunch, the lot!"
            else:
                header = f"{maestros[0]} is the highest level in all {tier} Right Hand skills! A Jack of trades, this one! ❤️"
        # if maestros are not the highest in all skills
        else:
            if len(maestros) > 1:
                header = f"Your Maestros are not the highest level in {tier} Right Hand skills"
            else:
                header = f"{maestros[0]} is not the highest level in {tier} Right Hand skills"
    return header

def maestros_goal_levels(maestros):
    account = session_data.account
    janky_skills = dict()
    # HOPEFULLY. The dict should look like this:
    # janky_skills["skill"] = (
    #     best_maestro,  # Character object?
    #     required_level,  # int, representing the... highest? level of the skill?
    #     next_highest_non_maestro_char  # False if maestro isn't best, character object if is?
    # )
    # ..... Or an empty dict?
    # This might need some refactoring.
    if not maestros:
        return janky_skills

    for skill in skillsToReview_RightHand:
        chars_ordered: list[Character] = sorted(
            account.safe_characters, key=lambda toon: toon.skills[skill], reverse=True
        )
        best_maestro = next((toon for toon in chars_ordered if toon in maestros), None)
        best_maestro_rank = chars_ordered.index(best_maestro)

        if best_maestro_rank == 0:
            # maestro is already best
            next_highest_non_maestro = next((toon for toon in chars_ordered if toon not in maestros), None)
        else:
            next_highest_non_maestro = False

        required_level = chars_ordered[0].skills[skill] + 1
        janky_skills[skill] = (best_maestro, required_level, next_highest_non_maestro)

    return janky_skills

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
        goldenPeanutsOwned = session_data.account.assets.get("PeanutG").amount
        peanutsOwned = session_data.account.assets.get("Peanut").amount
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
                progression=session_data.account.assets.get("FoodHealth3").amount,
                goal=2 * peanutsRemaining
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Bleach Logs",
                picture_class="bleach-logs",
                progression=session_data.account.assets.get("BirchTree").amount,
                goal=peanutsRemaining
            ))
            secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                label="Copper Ore",
                picture_class="copper-ore",
                progression=session_data.account.assets.get("Copper").amount,
                goal=peanutsRemaining
            ))

            if goldenPeanutsOwned < 5:
                #Add advice for gold bars
                secretClass_AdviceDict["UnlockNextClass"].append(Advice(
                    label="Gold Bars",
                    picture_class="gold-bar",
                    progression=session_data.account.assets.get("GoldBar").amount,
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
            if session_data.account.assets.get("Quest27").amount < 1:  # Quest27 = Bag o Nuts
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
                        playerneb1Int = json.loads(playerneb1Int)
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
                        playerneb3Int = json.loads(playerneb3Int)
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
    secretClass_AdviceGroupDict["MaestroHands"] = getHandsAdviceGroupCatchUp(vmans, maestros, beginners)
    secretClass_AdviceGroupDict["MaestroHandsInTheLead"] = getHandsAdviceGroupStayAhead(maestros)

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
        secretClass_AdviceSection.header = f"Best Secret Class tier met: {tier_section}<br>You best ❤️"
        try:
            if len(secretClass_AdviceGroupDict["MaestroHands"].advices['default']) == 0:
                secretClass_AdviceSection.complete = True
        except:
            pass
    else:
        secretClass_AdviceSection.header = f"Best Secret Class tier met: {tier_section}"

    return secretClass_AdviceSection
