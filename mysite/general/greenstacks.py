from consts import missableGStacksDict, break_you_best
from models.models import AdviceSection, AdviceGroup, Advice, gstackable_codenames_expected, Assets
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
        item_data = missableGStacksDict[quest_item.name]
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

    already_missed = len(missableGStacksDict) - len(advice_ObtainedQuestGStacks) - len(advice_EndangeredQuestGStacks)
    already_obtained = len(advice_ObtainedQuestGStacks)
    still_obtainable = len(advice_EndangeredQuestGStacks)
    possible = len(missableGStacksDict)

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
            tier="",
            pre_string="Still obtainable",
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

    if len(advice_MissedQuestGStacks) > 0:
        tier_missed = f"{len(advice_MissedQuestGStacks)}/{len(missableGStacksDict)}"
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
            tier="",
            pre_string="Already missed",
            advices=questGStacks_AdviceDict['Missed'],
            informational=True
        )

    questGStacks_AdviceSection = AdviceSection(
        name="Endangered Greenstacks",
        tier=tier_obtainable,
        header=header_obtainable,
        picture="Greenstack.png",
        note=note,
        groups=questGStacks_AdviceGroupDict.values(),
        unrated=True,
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
    expectedStackablesCount = len(set(gstackable_codenames_expected))
    expectedGStacksCount = len(all_owned_stuff.items_gstacked_expected)
    remainingToDoGStacksByTier = all_owned_stuff.items_gstackable_tiered

    groups = list()
    for tier, categories in remainingToDoGStacksByTier.items():
        tier_subsection = {
            category: [
                Advice(
                    label=item.name,
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
                tier=str(tier),
                pre_string="",
                advices=tier_subsection,
                informational=True
            )
        )

    cheat_group = AdviceGroup(
        tier="",
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
    if expectedGStacksCount >= 200 or equinoxDreamsStatus.get("Dream29", False) == True:
        header += f"{break_you_best} (until Lava adds further Dream tasks)<br>Other possible targets are still listed below."
        show_limit = 4
    elif expectedGStacksCount >= 75 or equinoxDreamsStatus.get("Dream12", False) == True:
        header += " Equinox Dream 29 requires 200. Aim for items up through Tier 10!<br>Tiers 11-14 are optional without much extra benefit to collecting than +1 GStack."
        show_limit = 3
    elif expectedGStacksCount >= 20 or equinoxDreamsStatus.get("Dream1", False) == True:
        header += " Equinox Dream 12 requires 75. Aim for items up through Tier 4!<br>Continue buying those Timegated items too :)"
        show_limit = 2
    elif expectedGStacksCount < 20 and equinoxDreamsStatus.get("Dream1", False) == False:
        header += " Equinox Dream 1 requires 20. Aim for items in Tier 1.<br>Start buying items listed in the Timegated tier from shops every day!"
        show_limit = 2
    else:

        show_limit = 2

    for group in groups[show_limit:]:
        group.hide = True

    #Dream Review
    overall_GreenstacksTier = 0
    for dream in [1, 12, 29]:
        if equinoxDreamsStatus.get(f"Dream{dream}", False) == True:
            overall_GreenstacksTier += 1

    section_regular_gstacks = AdviceSection(
        name="Greenstacks",
        tier=tier,
        pinchy_rating=overall_GreenstacksTier,
        header=header,
        picture="Greenstack.png",
        groups=groups,
    )

    return questGStacks_AdviceSection, section_regular_gstacks
