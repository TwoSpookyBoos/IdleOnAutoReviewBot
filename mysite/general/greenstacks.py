from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_general import missable_gstacks_dict, gstack_unique_expected
from consts.consts_w5 import get_vendor_name
from consts.progression_tiers import greenstack_progressionTiers, true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice, Assets
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)


def getEquinoxDreams() -> dict:
    results = {}
    for dreamNumber in [1, 12, 29]:
        try:
            results[f"Dream{dreamNumber}"] = session_data.account.equinox_dreams[dreamNumber]
        except Exception as reason:
            logger.warning(f"Unable to access Equinox Dream {dreamNumber}: {reason}. Defaulting to False.")
            results[f"Dream{dreamNumber}"] = False

    return results


def getMissableGStacksAdviceSection(owned_stuff: Assets) -> AdviceSection:
    optional_tiers = 0
    true_max = true_max_tiers['Endangered Greenstacks']
    max_tier = true_max - optional_tiers

    advice_ObtainedQuestGStacks = owned_stuff.quest_items_gstacked
    advice_EndangeredQuestGStacks = list(owned_stuff.quest_items_gstackable)
    advice_MissedQuestGStacks = []
    questGStacks_AdviceDict = {
        "Endangered": [],
        "Missed": []
    }
    questGStacks_AdviceGroupDict = {}

    quests_completed_on_all_toons = [
        name
        for name in session_data.account.compiled_quests
        if session_data.account.compiled_quests[name]['CompletedCount'] == session_data.account.character_count
    ]

    for quest_item in list(advice_EndangeredQuestGStacks):
        item_data = missable_gstacks_dict[quest_item.name]
        quest_codename = item_data[1]
        quest_item.quest = item_data[2]
        quest_item.quest_giver = item_data[5]

        if quest_codename in quests_completed_on_all_toons:
            advice_MissedQuestGStacks.append(quest_item)
            advice_EndangeredQuestGStacks.remove(quest_item)

    note = (
        "These items are only recommended for players trying to complete the "
        "endgame Equinox Dream to collect 200 greenstacks. If you're nowhere "
        "near that, simply leave the quest uncompleted on your "
        "Wizard/Elemental Sorcerer and your Squire/Divine Knight "
        "to clean up later!"
    )

    already_missed = len(missable_gstacks_dict) - len(advice_ObtainedQuestGStacks) - len(advice_EndangeredQuestGStacks)
    already_obtained = len(advice_ObtainedQuestGStacks)
    still_obtainable = len(advice_EndangeredQuestGStacks)
    possible = len(missable_gstacks_dict)

    tier_obtainable = f"{still_obtainable}/{possible - still_obtainable}"

    if already_missed > 0:
        header_alreadymissed = f"already missed {already_missed}"
    else:
        header_alreadymissed = f""

    if already_obtained > 0:
        header_alreadyobtained = f"{'and ' if already_missed > 0 and still_obtainable == 0 else ''}already obtained {already_obtained}"
    else:
        header_alreadyobtained = ""

    header_missable = ""
    if still_obtainable > 0:
        header_missable = (f"{',<br> and ' if (header_alreadymissed != '' or header_alreadyobtained != '') else ''}"
                           f"can still obtain {'all ' if still_obtainable == possible else ''}{still_obtainable}")

    header_obtainable = (f"You {header_alreadymissed}"
                         f"{',<br>' if header_alreadymissed != '' and header_alreadyobtained != '' else ''}{header_alreadyobtained}"
                         f"{header_missable}"
                         f" missable quest item Greenstacks."
                         f"{break_you_best if already_obtained == possible else ''}"
                         f"{'<br> Be sure NOT to turn in their quests until GStacking them' if still_obtainable > 0 else ''}")

    if len(advice_EndangeredQuestGStacks) > 0:
        tier_EndangeredGreenstacks = 0
        questGStacks_AdviceDict['Endangered'] = [
            Advice(
                label=f"{item.name}- {item.quest}",
                picture_class=item.name,
                progression=item.progression,
                goal=100,
                unit="%",
                resource=item.quest_giver
            )
            for item in advice_EndangeredQuestGStacks
        ]
        questGStacks_AdviceGroupDict['Endangered'] = AdviceGroup(
            tier=tier_EndangeredGreenstacks,
            pre_string='Still obtainable',
            advices=questGStacks_AdviceDict['Endangered'],
        )
        # endangered_AdviceSection = AdviceSection(
        #         name="Endangered Greenstacks",
        #         tier=tier_obtainable,
        #         header=header_obtainable,
        #         picture="Greenstack.png",
        #         note=note,
        #         groups=[endangered_AdviceGroup],
        #         unrated=True
        #     )
        # endangered_AdviceSection.completed = True if not endangered_AdviceSection.groups else False
        # sections.append(endangered_AdviceSection)
    else:
        tier_EndangeredGreenstacks = 1

    if len(advice_MissedQuestGStacks) > 0:
        tier_missed = f"{len(advice_MissedQuestGStacks)}/{len(missable_gstacks_dict)}"
        header_missed = (f"You have already missed {tier_missed} missable quest item Greenstacks."
                         f"<br>You're locked out of these until you get more character slots :(")
        questGStacks_AdviceDict['Missed'] = [
            Advice(
                label=f"{item.name}- {item.quest}",
                picture_class=item.name,
                progression=item.progression,
                unit="%",
                resource=item.quest_giver
            )
            for item in advice_MissedQuestGStacks
        ]
        questGStacks_AdviceGroupDict['Missed'] = AdviceGroup(
            tier='',
            pre_string='Already missed',
            advices=questGStacks_AdviceDict['Missed'],
            informational=True
        )

    overall_SectionTier = min(true_max, tier_EndangeredGreenstacks)

    tier_section = f"{overall_SectionTier}/{max_tier}"
    questGStacks_AdviceSection = AdviceSection(
        name="Endangered Greenstacks",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=header_obtainable,
        picture='wiki/Greenstack.png',
        note=note,
        groups=questGStacks_AdviceGroupDict.values(),
        completed=still_obtainable == 0
    )

    return questGStacks_AdviceSection

def getGStackAdviceSections():
    equinoxDreamsStatus = getEquinoxDreams()
    all_owned_stuff: Assets = session_data.account.stored_assets
    questGStacks_AdviceSection = getMissableGStacksAdviceSection(all_owned_stuff)

    unprecedented_gstacks = all_owned_stuff.items_gstacked_unprecedented
    if unprecedented_gstacks:
        gstacks = [f"{gstack.name} ({gstack.codename})" for gstack in unprecedented_gstacks.values()]
        logger.warning('Unexpected GStack(s): %s', gstacks)

    #Get count of max expected gstacks
    expectedStackablesCount = len(gstack_unique_expected)
    expectedGStacksCount = len(all_owned_stuff.items_gstacked_expected)
    remainingToDoGStacksByTier = all_owned_stuff.items_gstackable_tiered

    groups = list()
    for tier, categories in remainingToDoGStacksByTier.items():
        tier_subsection = {
            category: [
                Advice(
                    label=f"{item.name}"
                          f"{f' ({get_vendor_name(item.codename)})' if category == 'Vendor Shops' else ''}",
                    picture_class=item.name,
                    progression=item.progression,
                    goal=100,
                    unit="%"
                )
                for item in items
            ]
            for category, items in categories.items()
        }
        groups.append(
            AdviceGroup(
                tier='',
                pre_string=f"{'Difficulty Group ' if tier!= 'Timegated' else ''}{tier} Item recommendations",
                advices=tier_subsection,
                informational=True
            )
        )

    cheat_group = AdviceGroup(
        tier='',
        pre_string="Curious... you also managed to greenstack these unprecedented items",
        post_string="Share your unyielding persistence with us, please!",
        advices=[
            Advice(
                label=asset.name,
                picture_class=asset.name
            )
            for codename, asset in all_owned_stuff.items_gstacked_unprecedented.items()
        ],
        informational=True
    )
    groups.append(cheat_group)

    tier = f"{expectedGStacksCount} out of max (realistic) {expectedStackablesCount}"
    header = f"You currently have {tier} GStacks."
    show_limit = len(groups)
    if (
        expectedGStacksCount >= greenstack_progressionTiers[3]['Required Stacks']
        or equinoxDreamsStatus.get(f"Dream{greenstack_progressionTiers[3]['Dream Number']}", False) == True
    ):
        header += f"{break_you_best} (until Lava adds further Dream tasks)<br>Other possible targets are still listed below."
        show_limit = 4
    elif (
        expectedGStacksCount >= greenstack_progressionTiers[2]['Required Stacks']
        or equinoxDreamsStatus.get(f"Dream{greenstack_progressionTiers[2]['Dream Number']}", False) == True
    ):
        header += (f" Equinox Dream {greenstack_progressionTiers[3]['Dream Number']} requires {greenstack_progressionTiers[3]['Required Stacks']}."
                   f" Aim for items up through Difficulty Group 10!<br>Groups 11-14 are optional without much extra benefit to collecting than +1 GStack.")
        show_limit = 3
    elif (
        expectedGStacksCount >= greenstack_progressionTiers[1]['Required Stacks']
        or equinoxDreamsStatus.get(f"Dream{greenstack_progressionTiers[1]['Dream Number']}", False) == True
    ):
        header += (f" Equinox Dream {greenstack_progressionTiers[2]['Dream Number']} requires {greenstack_progressionTiers[2]['Required Stacks']}."
                   f" Aim for items up through Difficulty Group 4!<br>Continue buying those Timegated items too :)")
        show_limit = 2
    elif (
        expectedGStacksCount < greenstack_progressionTiers[1]['Required Stacks']
        and equinoxDreamsStatus.get(f"Dream{greenstack_progressionTiers[1]['Dream Number']}", False) == False
    ):
        header += (f" Equinox Dream {greenstack_progressionTiers[1]['Dream Number']} requires {greenstack_progressionTiers[1]['Required Stacks']}."
                   f" Aim for items in Difficulty Group 1.<br>Start buying Timegated items from shops every day!")
        show_limit = 2
    else:
        show_limit = 2

    for group in groups[show_limit:]:
        group.hide = True

    #Equinox Dream Review
    overall_SectionTier = 0
    optional_tiers = 2
    true_max = max(greenstack_progressionTiers.keys(), default=0)
    max_tier = true_max - optional_tiers
    dream_advice = {}
    for tier_number, requirements in greenstack_progressionTiers.items():
        subgroup_name = build_subgroup_label(tier_number, max_tier)
        if not equinoxDreamsStatus.get(f"Dream{requirements.get('Dream Number', 29)}", False) or (
                tier_number > max_tier and requirements['Required Stacks'] > expectedGStacksCount
        ):
            dream_advice[subgroup_name] = [
                Advice(
                    label=f"Collect {requirements['Required Stacks']} Greenstacks",
                    picture_class='greenstacks',
                    progression=expectedGStacksCount,
                    goal=requirements['Required Stacks']
                )
            ]
            if tier_number <= max_tier:
                dream_advice[subgroup_name].append(Advice(
                    label=f"Turn in {{{{ Equinox|#equinox }}}} Dream {requirements['Dream Number']}",
                    picture_class='equinox-dreams',
                    progression=int(equinoxDreamsStatus[f"Dream{requirements['Dream Number']}"]),
                    goal=1
                ))
        else:
            overall_SectionTier += 1

    for subgroup in dream_advice:
        for advice in dream_advice[subgroup]:
            mark_advice_completed(advice)

    groups.insert(0, AdviceGroup(
        tier=overall_SectionTier,
        pre_string="Collect Greenstacks to complete Equinox Dreams",
        advices=dream_advice
    ))

    section_regular_gstacks = AdviceSection(
        name="Greenstacks",
        tier=tier,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=header,
        picture="wiki/Greenstack.png",
        groups=groups,
    )

    return questGStacks_AdviceSection, section_regular_gstacks
