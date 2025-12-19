
from models.models import AdviceSection, AdviceGroup, Advice, Character, session_data
from utils.safer_data_handling import safe_loads
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, EmojiType
from consts.progression_tiers import secret_class_progressionTiers, true_max_tiers
from utils.text_formatting import pl

logger = get_logger(__name__)

right_hand_skills = ['Mining', 'Chopping', 'Fishing', 'Catching', 'Trapping', 'Worship']

def getRightHandsAdviceGroups(true_max):
    catchup_advices = []
    skills_needing_catchup = []
    stayahead_advices = {}
    sorted_skills = {}
    perfect = True

    for skill in right_hand_skills:
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
        highest_mman_name = next((c.character_name for c in sorted_skills[skill] if 'Maestro' in c.all_classes), '')
        highest_mman_level = max([char.skills[skill] for char in session_data.account.maestros], default=0)
        characters_at_highest = sum(1 for char in sorted_skills[skill] if char.skills[skill] == highest_skill_level)
        mman_uniquely_first = highest_mman_level == highest_skill_level and characters_at_highest == 1

        #If Maestro isn't in first, place into Catchup
        if characters_at_highest > 1:
            skills_needing_catchup.append(skill)
            if highest_mman_level == highest_skill_level:
                catchup_advices.append(Advice(
                    label=f"{highest_mman_name} is tied for best in {skill}."
                          f"<br>Right Hand buff only applies if they're STRICTLY better 🙁",
                    picture_class=skill,
                    progression=highest_mman_level,
                    goal=highest_mman_level + 1
                ))
            else:
                catchup_advices.append(Advice(
                    label=f"{highest_mman_name} {'is the highest leveled Mman but still ' if len(session_data.account.maestros) > 1 else ''}"
                          f"not best in {skill}",
                    picture_class=skill,
                    progression=highest_mman_level,
                    goal=sorted_skills[skill][0].skills[skill]+1
                ))
        elif characters_at_highest == 1 and 'Maestro' not in sorted_skills[skill][0].all_classes:
            skills_needing_catchup.append(skill)
            catchup_advices.append(Advice(
                label=f"{highest_mman_name} {'is the highest leveled Mman but still ' if len(session_data.account.maestros) > 1 else ''}"
                      f"not best in {skill}",
                picture_class=skill,
                progression=highest_mman_level,
                goal=sorted_skills[skill][0].skills[skill] + 1
            ))

        #Now for StayAhead / all specialized characters
        #Display the leader
        if characters_at_highest == 1:
            stayahead_advices[skill].append(Advice(
                label=f"{EmojiType.STOP.value if not mman_uniquely_first else ''}"
                      f" {sorted_skills[skill][0].character_name} is currently best at {skill}",
                      #f"{f'with {sorted_skills[skill][0].skills[skill]}' if not mman_uniquely_first else ''}",
                picture_class=sorted_skills[skill][0].class_name_icon,
                progression=sorted_skills[skill][0].skills[skill],
            ))
        else:
            stayahead_advices[skill].append(Advice(
                label=f"{sorted_skills[skill][0].character_name} is currently TIED for best at {skill}",
                picture_class=sorted_skills[skill][0].class_name_icon,
                progression=sorted_skills[skill][0].skills[skill],
            ))
        no_goal = characters_at_highest > 1 or not mman_uniquely_first
        #Display the rest
        if len(sorted_skills[skill]) > 1:
            for char in sorted_skills[skill][1:]:
                if 'Maestro' not in char.all_classes:
                    if mman_uniquely_first:
                        label_symbol = ''
                    else:
                        label_symbol = EmojiType.STOP.value
                else:
                    # If this character is a maestro and the 1st place character is also a Maestro, warning. Up to Player to decide
                    if 'Maestro' in sorted_skills[skill][0].all_classes:
                        label_symbol = EmojiType.WARNING.value
                    # Else if this character is a Maestro and the 1st place character ISN'T a Maestro, checkmark
                    else:
                        label_symbol = EmojiType.CHECK.value
                if label_symbol == EmojiType.CHECK.value:
                    fancy_label = f"{label_symbol}{char.character_name} should level {skill}"
                elif char.skills[skill] < highest_mman_level-1:
                    fancy_label = f"{char.character_name} can level {skill}"
                elif 'Maestro' not in char.all_classes:
                    if char.skills[skill] > highest_mman_level:
                        fancy_label = f"{label_symbol} {char.character_name} is already better than {highest_mman_name}"
                    elif char.skills[skill] == highest_mman_level:
                        fancy_label = f"{label_symbol} {char.character_name} is tied with {highest_mman_name} and shouldn't be leveled any further"
                    else:
                        fancy_label = f"{label_symbol} {char.character_name} will tie {highest_mman_name} if leveled any further"
                else:
                    fancy_label = f"{char.character_name} can level {skill}"
                if not mman_uniquely_first and 'Maestro' in char.all_classes:
                    fancy_goal = highest_skill_level + 1
                elif not no_goal:
                    fancy_goal = highest_mman_level - 1
                else:
                    fancy_goal = ''
                stayahead_advices[skill].append(Advice(
                    label=fancy_label,
                    picture_class=char.class_name_icon,
                    progression=char.skills[skill],
                    goal=fancy_goal
                ))
                if char.skills[skill] < highest_mman_level - 1 or not mman_uniquely_first:
                    perfect = False
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
        tier=true_max if len(catchup_advices) == 0 else true_max-1,
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
        session_data.account.alerts_Advices['General'].append(Advice(
            label=f"Your {{{{ Maestro|#secret-class-path }}}} isn't best in {len(catchup_advices)} Skill{pl(catchup_advices)}",
            picture_class='right-hand-of-action',
        ))

    #Stay Ahead
    for subgroup in stayahead_advices:
        for advice in stayahead_advices[subgroup]:
            advice.mark_advice_completed()

    stayahead_ag = AdviceGroup(
        tier='',
        pre_string=(
            f"Your Maestro{pl(len(session_data.account.maestros), ' is', 's are')}"
            f" the highest level in {len(right_hand_skills) - len(skills_needing_catchup)}/{len(right_hand_skills)}"
            f" Right Hand skills. Be careful not to let others overtake"
        ),
        advices=stayahead_advices,
        informational=True,
        completed=len(skills_needing_catchup) == 0
    )
    stayahead_ag.remove_empty_subgroups()
    return catchup_ag, len(skills_needing_catchup) == 0, stayahead_ag

def getQuestAdvice(tier_SecretClass, jmans, maestros):
    secretClass_AdviceDict = {
        'UnlockNextClass': [],
    }

    # No Journeyman
    if tier_SecretClass == 0:
        bush1_complete = False
        bush2_complete = False
        bush3_complete = False
        rock1_complete = False
        rock2_complete = False
        for characterIndex in range(0, len(session_data.account.all_quests)):
            if session_data.account.all_quests[characterIndex].get('Bushlyte1', 0) == 1:
                bush1_complete = True
            if session_data.account.all_quests[characterIndex].get('Bushlyte2', 0) == 1:
                bush2_complete = True
            if session_data.account.all_quests[characterIndex].get('Bushlyte3', 0) == 1:
                bush3_complete = True
            if session_data.account.all_quests[characterIndex].get('Rocklyte1', 0) == 1:
                rock1_complete = True
            if session_data.account.all_quests[characterIndex].get('Rocklyte2', 0) == 1:
                rock2_complete = True
        total_quest_peanuts = 1651 - (51 * bush1_complete) - (200 * bush2_complete) - (400 * bush3_complete) - (500 * rock1_complete) - (500 * rock2_complete)
        golden_peanuts_owned = session_data.account.all_assets.get('PeanutG').amount
        peanuts_owned = session_data.account.all_assets.get('Peanut').amount
        if golden_peanuts_owned < 6:
            peanuts_remaining = total_quest_peanuts - peanuts_owned - (golden_peanuts_owned * 100)
        else:
            peanuts_remaining = total_quest_peanuts - peanuts_owned - 500
        secretClass_AdviceDict['UnlockNextClass'].append(Advice(
            label="On your 7th or later character, create a Journeyman. Only make 1 Secret Class character!",
            picture_class='journeyman-icon'
        ))
        secretClass_AdviceDict['UnlockNextClass'].append(Advice(
            label="Skip this fool's quest. You need to stay a Beginner to become a Journeyman!",
            picture_class='promotheus'
        ))
        secretClass_AdviceDict['UnlockNextClass'].append(Advice(
            label="Start the Journeyman quest chain by finding this NPC in World 1! You'll need 1651 Peanuts in total.",
            picture_class='bushlyte'
        ))
        secretClass_AdviceDict['UnlockNextClass'].append(Advice(
            label='Peanuts are crafted at the anvil',
            picture_class='peanut',
            progression=peanuts_owned,
            goal=total_quest_peanuts
        ))
        if peanuts_remaining > 0:
            peanuts_subgroup = f'Ingredients for the remaining {peanuts_remaining} Peanuts:'
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label=peanuts_subgroup,
                picture_class='',
            ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label='Hot Dogs can be purchased from both W1 Vendors daily',
                picture_class='hot-dog',
                progression=session_data.account.all_assets.get('FoodHealth3').amount,
                goal=2 * peanuts_remaining
            ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label='Bleach Logs',
                picture_class='bleach-logs',
                progression=session_data.account.all_assets.get('BirchTree').amount,
                goal=peanuts_remaining
            ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label='Copper Ore',
                picture_class='copper-ore',
                progression=session_data.account.all_assets.get('Copper').amount,
                goal=peanuts_remaining
            ))

            if golden_peanuts_owned < 5:
                # Add advice for gold bars
                secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                    label='Gold Bars',
                    picture_class='gold-bar',
                    progression=session_data.account.stored_assets.get('GoldBar').amount,
                    goal=250 - (50 * golden_peanuts_owned)
                ))
            else:
                # Add advice for golden peanuts
                secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                    label='Gold Peanuts',
                    picture_class='golden-peanut',
                    progression=golden_peanuts_owned,
                    goal=5
                ))
            for advice in secretClass_AdviceDict['UnlockNextClass']:
                try:
                    if int(advice.progression) >= int(advice.goal):
                        advice.label += ' (Ready!)'
                except:
                    pass

    # No Maestro
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
            if session_data.account.stored_assets.get('Quest27').amount < 1:  # Quest27 = Bag o Nuts
                secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                    label="First, you'll need to finish Goldric's quest: Dress to Impress",
                    picture_class="goldric"
                ))
                secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                    label="This will reward you with a Bag o Nuts needed to start the Maestro quest",
                    picture_class="bag-o-nuts"
                ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Offer the Bag o Nuts to this NPC in World 2!",
                picture_class="cactolyte"
            ))
        for jman in jmans:
            if not cact1complete:
                if jman.mining_level < 32:
                    secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                        label=f"Level {jman.character_name}'s Mining",
                        picture_class='mining',
                        progression=jman.mining_level,
                        goal=32
                    ))
                if jman.smithing_level < 35:
                    secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                        label=f"Level {jman.character_name}'s Smithing",
                        picture_class='smithing',
                        progression=jman.smithing_level,
                        goal=35
                    ))
                if jman.choppin_level < 33:
                    secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                        label=f"Level {jman.character_name}'s Chopping",
                        picture_class='chopping',
                        progression=jman.choppin_level,
                        goal=33
                    ))
            if not cact2complete:
                if jman.fishing_level < 23:
                    secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                        label=f"Level {jman.character_name}'s Fishing",
                        picture_class='fishing',
                        progression=jman.fishing_level,
                        goal=23
                    ))
                if jman.alchemy_level < 25:
                    secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                        label=f"Level {jman.character_name}'s Alchemy",
                        picture_class='alchemy',
                        progression=jman.alchemy_level,
                        goal=25
                    ))
                if jman.catching_level < 25:
                    secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                        label=f"Level {jman.character_name}'s Catching",
                        picture_class='catching',
                        progression=jman.catching_level,
                        goal=25
                    ))
        if (len(secretClass_AdviceDict['UnlockNextClass']) == 0 and cact2complete and not cact3complete) or (cact3Started and not cact3complete):
            # if session_data.account.assets.get("Quest35").amount < 1:  # Quest35 = Googley Eyes to spawn Biggie Hours
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Find the Googley Eyes recipe from Crabcakes to spawn Biggie Hours",
                picture_class='googley-eyes'
            ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Remember to have Pete the Peanut in your Inventory before spawning Biggie Hours!",
                picture_class='pete-the-peanut'
            ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="594 Defense is needed to take 0 damage from Biggie Hours. You can use your best Fisticuffs safely if you reach this amount of defense.",
                picture_class='bucklered-up'
            ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Alternative to stacking Defense: Use the Wooden Bow to attack from a distance. Hide down the rope if he gets too close!",
                picture_class='wooden-bow'
            ))
        if len(secretClass_AdviceDict['UnlockNextClass']) == 0 and cact3complete:
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Congrats on killing Biggie Hours! Maestro! The Stro! Mman! Now turn in the quest, silly billy.",
                picture_class='club-maestro'
            ))

    # No Voidwalker
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
                    neb1status = session_data.account.all_quests[maestro.character_index]["Nebulyte1"] if "Nebulyte1" in session_data.account.all_quests[
                        maestro.character_index] else -1
                except:
                    continue
            if neb1status >= 0:
                neb1platskulls = 0
                try:
                    playerneb1Int = session_data.account.raw_data.get(f"QuestStatus_{maestro.character_index}", "{\"Nebulyte1\": [\"0\", \"0\"]}")
                    # logger.debug(f"playerneb1Int = {type(playerneb1Int)}: {playerneb1Int}")
                    if isinstance(playerneb1Int, str):
                        playerneb1Int = safe_loads(playerneb1Int)
                        playerneb1Int = playerneb1Int.get('Nebulyte1', ['0', '0'])
                        playerneb1Int = int(playerneb1Int[0])
                        # logger.debug(f"After json.loads, playerneb1Int = {type(playerneb1Int)}: {playerneb1Int}")
                    # playerneb1Int = int(session_data.account.raw_data.get(f"QuestStatus_{maestro.character_index}", {"Nebulyte1":[0,0]})[0])
                    neb1platskulls = max(playerneb1Int, neb1platskulls)
                except Exception as reason:
                    logger.warning(f"Could not retrieve 'Nebulyte1' in QuestStatus_{maestro.character_index} because: {reason}")
            if neb2status == -1:
                try:
                    neb2status = (
                        session_data.account.all_quests[maestro.character_index]['Nebulyte2']
                        if 'Nebulyte2' in session_data.account.all_quests[maestro.character_index]
                        else -1
                    )
                except:
                    continue
            if neb3status == -1:
                try:
                    neb3status = (
                        session_data.account.all_quests[maestro.character_index]['Nebulyte3']
                        if 'Nebulyte3' in session_data.account.all_quests[maestro.character_index]
                        else -1
                    )
                except:
                    continue
            if neb3status == 0:
                try:
                    playerneb3Int = session_data.account.raw_data.get(f"QuestStatus_{maestro.character_index}", "{\"Nebulyte3\": [\"0\"]}")
                    # logger.debug(f"playerneb3Int = {type(playerneb3Int)}: {playerneb3Int}")
                    if isinstance(playerneb3Int, str):
                        playerneb3Int = safe_loads(playerneb3Int)
                        playerneb3Int = playerneb3Int.get('Nebulyte1', ['0', '0'])
                        playerneb3Int = int(playerneb3Int[0])
                        # logger.debug(f"After json.loads, playerneb3Int = {type(playerneb3Int)}: {playerneb3Int}")
                    neb3gmushkills = max(playerneb3Int, neb3gmushkills)
                except Exception as reason:
                    logger.warning(f"Could not retrieve 'Nebulyte1' in QuestStatus_{maestro.character_index} because: {reason}")
            if neb4status == -1:
                try:
                    neb4status = (
                        session_data.account.all_quests[maestro.character_index]['Nebulyte4']
                        if 'Nebulyte4' in session_data.account.all_quests[maestro.character_index]
                        else -1
                    )
                except:
                    continue
        if neb1status == -1:
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Start the quest chain by finding this NPC in World 4!",
                picture_class='nebulyte'
            ))
            addLevelAdvice = True
            for maestro in maestros:
                if maestro.combat_level >= 150:
                    addLevelAdvice = False
            if addLevelAdvice:
                secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                    label="Hint: You'll need a minimum Combat level of 150",
                    picture_class='maestro-icon'
                ))
        elif neb1status == 0:
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Earn Platinum skulls (1 million kills) on all 40 W1-W3 enemies. You may use ALL characters to speed this up.",
                picture_class='platinum-skull',
                progression=neb1platskulls,
                goal=40
            ))
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Check out the {{Death Note|#death-note}} section to see remaining enemies",
                picture_class='death-note'
            ))
        if neb2status == 0:
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="What are you waiting for? Go punch Chaotic Chizoar in the face. Easy!",
                picture_class='chaotic-chizoar-card'
            ))
        if neb3status == 0:
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="Kill 12 million Green Mushrooms in W1 with ONLY your Maestro on the quest!",
                picture_class='green-mushroom',
                progression=neb3gmushkills,
                goal=12000000
            ))
        if (len(secretClass_AdviceDict['UnlockNextClass']) == 0 and neb3status >= 1) or neb4status == 0:
            secretClass_AdviceDict['UnlockNextClass'].append(Advice(
                label="One of us! One of us! One of us! Now turn in the quest, silly billy.",
                picture_class='voidwalker-icon'
            ))

    # No Infinilyte
    # elif tier_SecretClass == 3:
    #     secretClass_AdviceDict['UnlockNextClass'].append(Advice(
    #         label="Welcome to the Infinilyte waiting room",
    #         picture_class="infinilyte-icon"
    #     ))

    return secretClass_AdviceDict

def getProgressionTiersAdviceGroup(jmans, maestros):
    optional_tiers = 1
    true_max = true_max_tiers['Secret Class Path']
    max_tier = true_max - optional_tiers
    tier_SecretClass = 0

    #Required Tiers
    for tier, requirements in secret_class_progressionTiers.items():
        if 'Required Class' in requirements:
            if requirements['Required Class'] in session_data.account.classes and tier_SecretClass == tier-1:
                tier_SecretClass = tier

    secret_class_advices = getQuestAdvice(tier_SecretClass, jmans, maestros)
    group_pre_strings = [
        'Create a Journeyman',
        'Create a Maestro',
        'Create a Voidwalker',
        'Wait for Lava to release the next Secret Class'
    ]
    secret_class_advice_groups = {
        'UnlockNextClass': AdviceGroup(
            tier=tier_SecretClass,
            pre_string=group_pre_strings[tier_SecretClass],
            advices=secret_class_advices['UnlockNextClass']
        )
    }

    no_catchup_needed = True
    if len(maestros) > 0:
        secret_class_advice_groups['RightHandsCatchup'], no_catchup_needed, secret_class_advice_groups['RightHandsStayAhead'] = getRightHandsAdviceGroups(true_max)

    #Optional Tier
    for tier, requirements in secret_class_progressionTiers.items():
        if 'No Catchup Needed' in requirements:
            if no_catchup_needed and tier_SecretClass == max_tier:
                tier_SecretClass = true_max

    overall_SectionTier = min(true_max, tier_SecretClass)
    return secret_class_advice_groups, overall_SectionTier, max_tier, true_max

def getSecretClassAdviceSection() -> AdviceSection:
    jmans = session_data.account.jmans
    maestros = session_data.account.maestros
    secret_class_advice_groups, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup(jmans, maestros)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    secretClass_AdviceSection = AdviceSection(
        name='Secret Class Path',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Secret Class tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Stone_Peanut.png',
        groups=secret_class_advice_groups.values(),
        note=(
            f"Important! Only one Maestro's Right and Left Hands buffs work."
            f"<br>On Steam, this is the last created Maestro."
            f"<br>I'm not totally sure about other platforms, sorry {EmojiType.FROWN.value}"
        ) if len(maestros) > 1 else ''
    )

    return secretClass_AdviceSection
