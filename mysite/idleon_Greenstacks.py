import json
from collections import defaultdict

from consts import missableGStacksDict
from models import AdviceSection, AdviceGroup, Advice, gstackable_codenames, gstackable_codenames_expected, Assets
from utils import get_logger


logger = get_logger(__name__)


def getEquinoxDreams(inputJSON) -> dict:
    try:
        rawDreams = json.loads(inputJSON["WeeklyBoss"])
    except Exception as reason:
        logger.error("Unable to access WeeklyBoss data from JSON: %s", reason)
        return dict(
            Dream1=False,
            Dream12=False,
            Dream29=False
        )

    results = dict(
        Dream1=rawDreams.get("d_0") == -1,
        Dream12=rawDreams.get("d_11") == -1,
        Dream29=rawDreams.get("d_28") == -1,
    )
    logger.debug("OUTPUT results: %s", results)

    return results


def all_owned_items(inputJSON: dict, playerCount: int) -> Assets:
    name_quantity_key_pairs = tuple((f"InventoryOrder_{i}", f"ItemQTY_{i}") for i in range(playerCount)) + (("ChestOrder", "ChestQuantity"),)
    all_stuff_owned = defaultdict(int)

    for codename in gstackable_codenames:
        all_stuff_owned[codename] = 0

    for name_key, quantity_key in name_quantity_key_pairs:
        for name, count in zip(inputJSON[name_key], inputJSON[quantity_key]):
            all_stuff_owned[name] += count

    return Assets(all_stuff_owned)


def getMissableGStacks(inputJSON, playerCount, owned_stuff: Assets):
    advice_ObtainedQuestGStacks = owned_stuff.quest_items_gstacked
    advice_EndangeredQuestGStacks = list(owned_stuff.quest_items_gstackable)
    advice_MissedQuestGStacks = []

    quest_statuses_per_player = [json.loads(inputJSON.get(f"QuestComplete_{i}", "{}")) for i in range(playerCount)]
    quest_names = quest_statuses_per_player[0].keys()
    quest_completed = [
        name
        for name in quest_names
        if all(quests[name] == 1 for quests in quest_statuses_per_player)
        # Quest value one of (-1, 0, 1). -1 means not started.
    ]

    for quest_item in list(advice_EndangeredQuestGStacks):
        item_data = missableGStacksDict[quest_item.name]
        quest_codename = item_data[1]

        if quest_codename in quest_completed:
            quest_item.quest = item_data[2]
            advice_MissedQuestGStacks.append(quest_item)
            advice_EndangeredQuestGStacks.remove(quest_item)

    sections = list()

    note = (
        "These items are currently recommended for players trying to complete the "
        "endgame Equinox Dreams to collect 20, 75, and 200 greenstacks. If you're "
        "nowhere near that, don't worry about collecting them right away. Simply "
        "leave the quest uncompleted on your Wizard/Elemental Sorcerer and your "
        "Squire/Divine Knight to clean up later!"
    )

    if len(advice_ObtainedQuestGStacks) > 0:
        tier_obtained = f"{len(advice_ObtainedQuestGStacks)}/{len(missableGStacksDict)}"
        if len(advice_ObtainedQuestGStacks) == len(missableGStacksDict):
            header_obtained = f"You have obtained all {tier_obtained} missable quest item Greensacks! Way to go, you heap hoarder ❤️"
        else:
            header_obtained = f"You have obtained {tier_obtained} missable quest item Greenstacks"

        section_obtained = AdviceSection(
            name="Obtained Greenstacks",
            tier=tier_obtained,
            header=header_obtained,
            picture="Greenstack.png",
            note=note
        )
        # sections.append(section_obtained)

    if len(advice_EndangeredQuestGStacks) > 0:
        tier_obtainable = f"{len(advice_EndangeredQuestGStacks)}/{len(missableGStacksDict)}"
        header_obtainable = f"You can still obtain {tier_obtainable} missable quest item Greenstacks. Be sure <strong>NOT</strong> to turn in their quests until GStacking them:"
        sections.append(
            AdviceSection(
                name="Endangered Greenstacks",
                tier=tier_obtainable,
                header=header_obtainable,
                picture="Greenstack.png",
                note=note,
                groups=[
                    AdviceGroup(
                        tier="",
                        pre_string="",
                        advices=[
                            Advice(label=item.name, picture_class=item.name, progression=item.progression, unit="%")
                            for item in advice_EndangeredQuestGStacks
                        ]
                    )
                ]
            )
        )

    if len(advice_MissedQuestGStacks) > 0:
        tier_missed = f"{len(advice_MissedQuestGStacks)}/{len(missableGStacksDict)}"
        header_missed = f"You have already missed {tier_missed} missable quest item Greenstacks. You're locked out of these until you get more character slots :("
        section_missed = AdviceSection(
            name="Missed Greenstacks",
            tier=tier_missed,
            header=header_missed,
            picture="Greenstack.png",
            note=note,
            groups=[
                AdviceGroup(
                    tier="",
                    pre_string="",
                    advices=[
                        Advice(label=item.name, picture_class=item.name, progression=item.quest)
                        for item in advice_MissedQuestGStacks
                    ]
                )
            ]
        )
        # sections.append(section_missed)

    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_ObtainedQuestGStacks:", advice_ObtainedQuestGStacks)
    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_EndangeredQuestGStacks:", advice_EndangeredQuestGStacks)
    #print("GreenStacks.getMissableGStacks~ OUTPUT advice_MissedQuestGStacks:", advice_MissedQuestGStacks)

    return sections
    #return [advice_ObtainedQuestGStacks, advice_EndangeredQuestGStacks, advice_MissedQuestGStacks]


def setGStackProgressionTier(inputJSON, playerCount):
    equinoxDreamsStatus = getEquinoxDreams(inputJSON)
    all_owned_stuff: Assets = all_owned_items(inputJSON, playerCount)
    sections_quest_gstacks = getMissableGStacks(inputJSON, playerCount, all_owned_stuff)

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
                Advice(label=item.name, picture_class=item.name, progression=item.progression, unit="%") for item in sorted(items, key=lambda item: item.progression, reverse=True)
            ]
            for category, items in categories.items()
        }
        groups.append(
            AdviceGroup(
                tier=str(tier),
                pre_string="",
                advices=tier_subsection
            )
        )

    cheat_group = AdviceGroup(
        tier="",
        pre_string="Curious... you also managed to greenstack these unprecedented items:",
        post_string="Share your unyielding persistence with us, please!",
        advices=[
            Advice(label=name, picture_class=name)
            for name, item in all_owned_stuff.items_gstacked_unprecedented.items()
        ]
    )
    groups.append(cheat_group)

    tier = f"{expectedGStacksCount} out of max (realistic) {expectedStackablesCount}"
    header = f"You currently have {tier} GStacks."
    show_limit = len(groups)
    if expectedGStacksCount >= 200 or equinoxDreamsStatus["Dream29"] == True:
        header += " You best ❤️ (until Lava adds further Dream tasks) Other possible targets are still listed below."
        show_limit = 4
    elif expectedGStacksCount >= 75 or equinoxDreamsStatus["Dream12"] == True:
        header += " Equinox Dream 29 requires 200. Aim for items up through Tier 10! Tiers 11-14 are optional without much extra benefit to collecting than +1 GStack."
        show_limit = 3
    elif expectedGStacksCount >= 20 or equinoxDreamsStatus["Dream1"] == True:
        header += " Equinox Dream 12 requires 75. Aim for items up through Tier 4! Continue buying those Timegated items too :)"
        show_limit = 2
    elif expectedGStacksCount < 20 and equinoxDreamsStatus["Dream1"] == False:
        header += " Equinox Dream 1 requires 20. Aim for items in Tier 1, and start buying items listed in the Timegated tier from shops every day!"
        show_limit = 2

    for group in groups[show_limit:]:
        group.hide = True

    section_regular_gstacks = AdviceSection(
        name="Greenstacks",
        tier=tier,
        header=header,
        picture="Greenstack.png",
        groups=groups
    )

    return sections_quest_gstacks, section_regular_gstacks
