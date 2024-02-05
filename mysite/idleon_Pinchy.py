import json
from models import Advice, AdviceWorld, WorldName, AdviceSection, AdviceGroup
from utils import pl, get_logger


logger = get_logger(__name__)


class Threshold:
    W1 = "W1"
    EARLY_W2 = "Early W2"
    MID_W2 = "Mid W2"
    LATE_W2 = "Late W2"
    EARLY_W3 = "Early W3"
    MID_W3 = "Mid W3"
    LATE_W3 = "Late W3"
    EARLY_W4 = "Early W4"
    MID_W4 = "Mid W4"
    LATE_W4 = "Late W4"
    EARLY_W5 = "Early W5"
    MID_W5 = "Mid W5"
    LATE_W5 = "Late W5"
    EARLY_W6_PREP = "Early W6 Prep"
    SOLID_W6_PREP = "Solid W6 Prep"
    W6_WAITING_ROOM = "W6 Waiting Room"
    MAX_TIER = "Max for v1.91"
    PLACEHOLDER = "Placeholder"

    thresholdNames = [
        W1,
        EARLY_W2, MID_W2, LATE_W2,
        EARLY_W3, MID_W3, LATE_W3,
        EARLY_W4, MID_W4, LATE_W4,
        EARLY_W5, MID_W5, LATE_W5,
        EARLY_W6_PREP, SOLID_W6_PREP, W6_WAITING_ROOM,
        MAX_TIER,
        PLACEHOLDER
    ]

    __activityThresholds = {
        # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,99] #template
        #                W1/W2           W3              W4              W5              W6              Max/Placeholder
        "Combat Levels": [0, 3, 7, 8,    10, 14, 15,     16, 17, 18,     19, 21, 23,     25, 27, 28,     29, 99],
        "Stamps":        [0, 1, 2, 3,    4,  5,  6,      7,  8,  9,      10, 11, 15,     22, 28, 34,     36, 99],
        "Bribes":        [0, 1, 1, 1,    2,  2,  3,      3,  3,  3,      4,  4,  4,      5,  5,  5,      5,  99],
        "Smithing":      [0, 0, 0, 0,    0,  0,  0,      0,  0,  0,      1,  2,  3,      4,  5,  6,      6,  99],
        "Bubbles":       [0, 0, 0, 1,    1,  1,  1,      2,  2,  2,      3,  4,  5,      7,  12, 18,     23, 99],
        "Vials":         [0, 0, 0, 0,    0,  0,  0,      1,  2,  3,      4,  5,  6,      7,  16, 19,     20, 99],
        "Refinery":      [0, 0, 0, 0,    0,  0,  0,      0,  0,  0,      1,  1,  2,      3,  4,  5,      6,  99],
        "Salt Lick":     [0, 0, 0, 0,    0,  0,  0,      0,  0,  1,      2,  3,  4,      5,  6,  7,      10, 99],
        "Prayers":       [0, 0, 0, 0,    0,  0,  1,      1,  2,  3,      3,  4,  5,      5,  6,  7,      7,  99],
        "Death Note":    [0, 0, 0, 0,    0,  0,  0,      0,  0,  0,      0,  4,  5,      12, 15, 19,     23, 99],
    }
    name_count = len(thresholdNames)
    activity_count = len(__activityThresholds.keys())

    def __init__(self, tier: int, index: int):
        self.tier: int = tier
        self.index: int = index
        self.name: str = self.thresholdNames[index]

    def __gt__(self, other: int):
        return self.tier > other

    def __eq__(self, other):
        return all([self.tier == other.tier, self.index == other.index, self.name == other.name])

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.tier}>"

    @property
    def previous(self):
        return self.index - 1 if self.index > 0 else None

    @property
    def previous_name(self):
        return self.thresholdNames[self.index - 1] if self.index > 0 else None

    @property
    def next(self):
        return self.index + 1 if self.index < self.name_count else -1

    @property
    def next_name(self):
        return self.thresholdNames[self.index + 1] if self.index < self.name_count else None

    @classmethod
    def placeholder(cls):
        return cls(99, -1)

    @classmethod
    def none(cls):
        return cls(0, 0)

    @classmethod
    def activity_thresholds(cls):
        """give each individual tier its name"""
        return {
            activity: [cls(tier, i) for i, tier in enumerate(thresholds)]
            for activity, thresholds in cls.__activityThresholds.items()
        }


activityThresholds = Threshold.activity_thresholds()


def activities_to_threshold_tiers(dictOfPRs) -> dict[str, list[tuple[str, int, Threshold]]]:
    PRsByProgression: dict[str, list[tuple[str, int, Threshold]]] = {name: list() for name in Threshold.thresholdNames}

    for activity, pinchy_tier in dictOfPRs.items():
        placeholder = Threshold.placeholder()
        thresholds = activityThresholds[activity]
        next_threshold = next((t for t in thresholds if t > pinchy_tier), placeholder)

        # if pinchy review tier flew off the grid somehow
        if next_threshold == placeholder:
            logger.info(f"Placing '{activity}' into final tier because {pinchy_tier} >= {thresholds[-2]}")
            next_threshold = thresholds[-2]
        else:
            logger.info("%s | %s | %s | %s", activity, pinchy_tier, next_threshold.previous_name, next_threshold)

        PRsByProgression[next_threshold.previous_name].append((activity, pinchy_tier, next_threshold))

    # remove empty lists
    for prog_name, prs in list(PRsByProgression.items()):
        if len(prs) == 0:
            del PRsByProgression[prog_name]

    return PRsByProgression


# https://idleon.wiki/wiki/Portal_Requirements
# W2 Sandy Pots = [51][0], starts at 250
# W2 Mafiosos = [57][0], starts at 1200
# W2 Tysons = [62][0], starts at 3000
# W3 Sheepies = [101][0], starts at 1000
# W3 Mamooths = [106][0], starts at 6000
# W3 Quenchies = [110][0], starts at 18000
# W4 Purp Mushroom = [151][0], starts at 5000
# W4 Soda Can = [155][0], starts at 40000
# W4 Clammies = [160][0], starts at 190000
# W5 Suggma = [201][0], starts at 25000
# W5 Stiltmole = [205][0], starts at 125000
# W5 Fire Spirit = [210][0], starts at 3000000
# W5 Tremor Wurms = [213][0], starts at 60000
# Until W6 drops, Solid W6 prep = DeathNote tier 15+
# Until W6 drops, W6 waiting room = DeathNote tier 19+
# Until W6 drops, Max = 1b+ sample

portalOpeningKills = [
    (Threshold.EARLY_W6_PREP, 213, 60000),
    (Threshold.LATE_W5, 210, 3000000),
    (Threshold.MID_W5, 205, 125000),
    (Threshold.EARLY_W5, 201, 25000),
    (Threshold.LATE_W4, 160, 190000),
    (Threshold.MID_W4, 155, 40000),
    (Threshold.EARLY_W4, 151, 5000),
    (Threshold.LATE_W3, 110, 18000),
    (Threshold.MID_W3, 106, 6000),
    (Threshold.EARLY_W3, 101, 1000),
    (Threshold.LATE_W2, 62, 3000),
    (Threshold.MID_W2, 57, 1200),
    (Threshold.EARLY_W2, 51, 250),
]
maxExpectedThresholdFromMaps = portalOpeningKills[0][0]  # The Worm Nest (Tremor Wurms) corresponds to "Late W5".


def is_portal_opened(mobKills, monster, portalKC):
    return mobKills[monster][0] < portalKC if len(mobKills) > monster else False


def getHighestPrint(inputJSON):
    awfulPrinterList = json.loads(inputJSON["Print"])
    # print("Pinchy~ OUTPUT awfulPrinterList: ", type(awfulPrinterList), awfulPrinterList)
    goodPrinterList = [p for p in awfulPrinterList if isinstance(p, int)]
    highestPrintFound = max(goodPrinterList)
    # print("Pinchy~ OUTPUT Final highest print value found: ", highestPrintFound)

    return highestPrintFound


def threshold_for_highest_portal_opened(mobKills):
    return next((
        threshold
        for threshold, monster, portalKC
        in portalOpeningKills
        if is_portal_opened(mobKills, monster, portalKC)
    ), Threshold.W1)


def tier_from_monster_kills(dictOfPRs, inputJSON, playerCount) -> str:
    """find highest enemy killed or world unlocked to compare to"""
    expectedThreshold = Threshold.W1

    highestPrint = getHighestPrint(inputJSON)
    if highestPrint >= 999000000:
        expectedThreshold = Threshold.W6_WAITING_ROOM
    elif dictOfPRs["Death Note"] >= 19:
        expectedThreshold = Threshold.SOLID_W6_PREP
    elif dictOfPRs["Death Note"] >= 15:
        expectedThreshold = Threshold.EARLY_W6_PREP
    else:
        # logger.info(f"Starting to review map kill counts per player because expectedIndex still W1: {dictOfPRs['Construction Death Note']}")
        for playerCounter in range(0, playerCount):
            mobKills = json.loads(inputJSON['KLA_' + str(playerCounter)])  # String pretending to be a list of lists yet again
            # logger.info("%s, %s", type(playerKillsList), playerKillsList)  # Expected to be a list
            expectedThreshold = threshold_for_highest_portal_opened(mobKills)

            if expectedThreshold >= maxExpectedThresholdFromMaps:
                break

    return expectedThreshold


def lowest_populated_threshold(activitiesByThreshold):
    return next((k for k in activitiesByThreshold.keys()), Threshold.none().name)


def generate_advice(activities, threshold):
    advices = [
        Advice(
            label=activity[0],
            item_name=activity[0],
            progression=activity[1],
            goal=activity[2].tier,
            unit="T",
            value_format="{unit} {value}"
        ) for activity in activities
    ]
    if threshold == Threshold.thresholdNames[-2]:
        for advice in advices:
            advice.progression = ""
            advice.goal = ""
    return advices


def generate_groups(activitiesByThreshold):
    advice_groups = []
    for threshold, activities in activitiesByThreshold.items():
        advices = generate_advice(activities, threshold)

        advice_group = AdviceGroup(
            tier="",
            pre_string=f"{threshold} rated activit{pl(advices, 'y', 'ies')}",
            advices=advices
        )

        advice_groups.append(advice_group)
    return advice_groups


def setPinchyList(inputJSON, playerCount, dictOfPRs):
    activitiesByThreshold = activities_to_threshold_tiers(dictOfPRs)
    expectedThreshold: str = tier_from_monster_kills(dictOfPRs, inputJSON, playerCount)
    lowestThresholdReached: str = lowest_populated_threshold(activitiesByThreshold)

    # Generate advice based on catchup
    equalSnippet = ""
    if Threshold.thresholdNames.index(lowestThresholdReached) >= Threshold.thresholdNames.index(expectedThreshold):
        equalSnippet = "Your lowest sections are roughly equal with (or better than!) your highest enemy map. Keep up the good work!"

    advice_groups = generate_groups(activitiesByThreshold)

    if expectedThreshold == Threshold.placeholder().name:
        pinchyExpected = (
            "Huh. Something went a little wrong here. You landed in the Placeholder tier somehow. "
            "If you weren't expecting this, tell Scoli about it! O.o"
        )
    else:
        pinchyExpected = f"Expected Progression, based on highest enemy map: {expectedThreshold}."

    sections_maxed_count = (
            len(activitiesByThreshold.get(Threshold.thresholdNames[-1], list())) +
            len(activitiesByThreshold.get(Threshold.thresholdNames[-2], list()))
    )
    sections_total = Threshold.activity_count
    sections_maxed = f"{sections_maxed_count}/{sections_total}"

    pinchy_high = AdviceSection(
        name="Pinchy high",
        tier=expectedThreshold,
        header=pinchyExpected,
        collapse=True
    )

    pinchy_low = AdviceSection(
        name="Pinchy low",
        tier=lowestThresholdReached,
        header=f"Minimum Progression, based on weakest ranked review: {lowestThresholdReached}.",
        collapse=True
    )

    pinchy_all = AdviceSection(
        name="Pinchy all",
        tier=sections_maxed,
        header=f"Activities maxed: {sections_maxed}.",
        picture="Pinchy.gif",
        groups=advice_groups
    )

    pinchy = AdviceWorld(
        name=WorldName.PINCHY,
        sections=[pinchy_high, pinchy_low, pinchy_all],
        equalSnippet=equalSnippet
    )

    return pinchy
