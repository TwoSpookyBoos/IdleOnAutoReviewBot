import json
from models import Advice, AdviceWorld, WorldName, AdviceSection, AdviceGroup
from utils import pl, get_logger
from flask import g as session_data

logger = get_logger(__name__)


class Tier:
    def __init__(self, tier: int, section: str = None, current: 'Threshold' = None, previous: 'Threshold' = None, next: 'Threshold' = None):
        self.tier = tier
        self.section = section
        self.current = current
        self.previous = previous
        self.next = next

    def __str__(self):
        return f"{self.section}: T{self.tier}"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.section}, T{self.tier}>"


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
    EARLY_W6 = "Early W6"
    MID_W6 = "Mid W6"
    LATE_W6 = "Late W6"
    EARLY_W7_PREP = "Early W7 Prep"
    SOLID_W7_PREP = "Solid W7 Prep"
    W7_WAITING_ROOM = "W7 Waiting Room"
    MAX_TIER = "Maxed for v2.03"
    PLACEHOLDER = "Placeholder"

    thresholdNames = [
        W1,
        EARLY_W2, MID_W2, LATE_W2,
        EARLY_W3, MID_W3, LATE_W3,
        EARLY_W4, MID_W4, LATE_W4,
        EARLY_W5, MID_W5, LATE_W5,
        EARLY_W6, MID_W6, LATE_W6,
        EARLY_W7_PREP, SOLID_W7_PREP, W7_WAITING_ROOM,
        MAX_TIER,
        PLACEHOLDER
    ]

    name_count = len(thresholdNames)

    def __init__(self, tier: int, index: int | None = None, name: str | None = None, parent: 'Thresholds' = None):
        if index is not None and index > len(self.thresholdNames):
            raise IndexError(f"There's less thresholds than you'd want: {index} > {len(self.thresholdNames)}.")
        if name is not None and name not in self.thresholdNames:
            raise ValueError(f"That's not a threshold name: {name}. Available names: {', '.join(self.thresholdNames)}")

        self.tier: int = tier
        self.index: int = index
        self.name: str = name
        self.parent: Thresholds = parent

        if index is None and not name:
            raise ValueError("Either `index` or `name` must be provided.")

        if index is None:
            self.index = self.thresholdNames.index(name)
        elif not name:
            self.name: str = self.thresholdNames[index]

    def __gt__(self, other):
        if isinstance(other, Tier):
            return self.tier > other.tier
        return self.index > other.index

    def __ge__(self, other):
        if isinstance(other, Tier):
            return self.tier > other.tier
        return self.index >= other.index

    def __eq__(self, other):
        if isinstance(other, Tier):
            return self.tier == other.tier
        return all([self.tier == other.tier, self.index == other.index, self.name == other.name])

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.tier}>"

    def next(self):
        return self.parent.next(self)

    def previous(self):
        return self.parent.previous(self)

    @classmethod
    def placeholder(cls):
        return cls(99, -1)


    @classmethod
    def none(cls):
        return cls(0, 0)

    @classmethod
    def fromname(cls, name: str):
        return cls(None, name=name)


class Placements(dict):
    COMBAT_LEVELS = "Combat Levels"
    STAMPS = "Stamps"
    BRIBES = "Bribes"
    SMITHING = "Smithing"
    BUBBLES = "Bubbles"
    VIALS = "Vials"
    P2W = "Pay2Win"
    REFINERY = "Refinery"
    SALT_LICK = "Salt Lick"
    PRAYERS = "Prayers"
    DEATH_NOTE = "Death Note"
    sections = [
        COMBAT_LEVELS,
        STAMPS, BRIBES, SMITHING,
        BUBBLES, VIALS, P2W,
        REFINERY, SALT_LICK, PRAYERS, DEATH_NOTE,
    ]

    sectionThresholds = {
        # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,99] #template
        #               W1   W2          W3              W4              W5              W6              W7              Max   Placeholder
        COMBAT_LEVELS: [0,   3, 7, 8,    10, 14, 15,     16, 17, 18,     19, 21, 23,     24, 25, 27,     28, 29, 29,     29,   99],
        STAMPS:        [0,   1, 2, 3,    4,  5,  6,      7,  8,  9,      10, 11, 13,     16, 19, 22,     26, 30, 34,     36,   99],
        BRIBES:        [0,   1, 1, 1,    2,  2,  2,      3,  3,  3,      4,  4,  4,      5,  5,  5,      5, 5, 5,        6,    99],
        SMITHING:      [0,   0, 0, 0,    0,  0,  0,      0,  0,  0,      1,  2,  3,      4,  5,  6,      6, 6, 6,        6,    99],
        BUBBLES:       [0,   0, 0, 0,    0,  1,  1,      2,  2,  2,      3,  4,  5,      7,  9, 14,      17, 19, 21,     23,   99],
        VIALS:         [0,   0, 0, 0,    1,  1,  2,      3,  4,  5,      6,  6,  7,      8,  9,  10,     12, 20, 25,     26,   99],
        P2W:           [0,   0, 0, 0,    0,  0,  0,      0,  0,  0,      0,  1,  1,      1,  1,  1,      1, 1, 1,        1,    99],
        REFINERY:      [0,   0, 0, 0,    0,  0,  0,      1,  1,  1,      1,  1,  1,      1,  1,  1,      1, 1, 1,        1,    99],
        SALT_LICK:     [0,   0, 0, 0,    0,  0,  0,      0,  0,  1,      2,  3,  4,      5,  5,  6,      7, 8, 9,        10,   99],
        PRAYERS:       [0,   0, 0, 0,    0,  0,  1,      1,  2,  2,      3,  3,  4,      4,  5,  6,      7, 7, 7,        7,    99],
        DEATH_NOTE:    [0,   0, 0, 0,    0,  0,  0,      0,  0,  0,      0,  4,  5,      7, 9, 11,       17, 21, 24,     26,   99],
    }
    section_count = len(sectionThresholds)

    def __init__(self):
        super().__init__()

        for name in Threshold.thresholdNames:
            self[name] = list()

        for name, thresholds in self.sectionThresholds.items():
            self[name] = Thresholds(thresholds)

        self.final = dict()

    def __getitem__(self, item):
        if isinstance(item, str):
            return super().__getitem__(item)
        if isinstance(item, Threshold):
            return super().__getitem__(item.name)
        else:
            raise TypeError(f"{item} is not a Threshold or string")

    def place(self, tier: Tier):
        section_thresholds: Thresholds = self[tier.section]
        placement: Threshold = section_thresholds.place(tier)
        self[placement].append(tier)

    @property
    def lowest(self):
        return next((Threshold.fromname(k) for k in self.final.keys()), Threshold.none())

    @property
    def maxed_count(self):
        return len(self.final.get(Threshold.MAX_TIER, list()))

    def finalise(self):
        for name in Threshold.thresholdNames:
            if len(self[name]) > 0:
                self.final[name] = self[name]

        return self.final

    def per_section(self):
        return {tier.section: placement for placement, tiers in self.final.items() for tier in tiers}


class Thresholds(dict):
    def __init__(self, t_list: list):
        super().__init__()
        self._thresholds = [Threshold(tier=t, index=i, parent=self) for i, t in enumerate(t_list)]

    def previous(self, threshold):
        return self._thresholds[threshold.index - 1] if threshold.index > 0 else threshold

    def next(self, threshold):
        return self._thresholds[threshold.index + 1] if self._thresholds.index(threshold) > 0 else threshold

    @property
    def placeholder(self):
        return self._thresholds[-1]

    def place(self, tier: Tier):
        placeholder = self.placeholder
        threshold_max = placeholder.previous()
        placement = next((t.previous() for t in self._thresholds if t > tier), threshold_max)
        # if pinchy review tier flew off the grid somehow
        if placement == placeholder:
            logger.info(f"Placing '{tier.section}' into final tier because {tier.tier} >= {threshold_max}")
            placement = threshold_max
        # else:
        #     logger.info("%s | %s | %s | %s", tier.section, tier.tier, placement, placement.next())

        previous_threshold = placement.previous()
        next_threshold = placement.next()
        tier.previous = previous_threshold
        tier.current = placement
        tier.next = next_threshold

        return placement


def sort_pinchy_reviews(dictOfPRs) -> Placements:
    placements = Placements()

    for section, pinchy_tier in dictOfPRs.items():
        tier = Tier(pinchy_tier, section)
        placements.place(tier)

    placements.finalise()

    return placements


# https://idleon.wiki/wiki/Portal_Requirements
portalOpeningKills = [
    (Threshold.EARLY_W7_PREP, 264,      100),  #W6 Samurai Spirits
    (Threshold.LATE_W6,       260, 25000000),  # W6 Ceramic Spirits
    (Threshold.MID_W6,        256,  1100000),  # W6 Bamboo Spirits
    (Threshold.EARLY_W6,      251,    30000),  # W6 Sprout Spirits
    (Threshold.LATE_W5,       210,   600000),  # W5 Fire Spirits
    (Threshold.MID_W5,        205,    75000),  # W5 Stiltmoles
    (Threshold.EARLY_W5,      201,    15000),  # W5 Suggmas
    (Threshold.LATE_W4,       160,   190000),  # W4 Clammies
    (Threshold.MID_W4,        155,    40000),  # W4 Soda Cans
    (Threshold.EARLY_W4,      151,     5000),  # W4 Purp Mushrooms
    (Threshold.LATE_W3,       110,    18000),  # W3 Quenchies
    (Threshold.MID_W3,        106,     6000),  # W3 Mamooths
    (Threshold.EARLY_W3,      101,     1000),  # W3 Sheepies
    (Threshold.LATE_W2,        62,     3000),  # W2 Tysons
    (Threshold.MID_W2,         57,     1200),  # W2 Mafiosos
    (Threshold.EARLY_W2,       51,      250),  # W2 Sandy Pots
]
maxExpectedThresholdFromMaps = portalOpeningKills[0][0]


def is_portal_opened(mobKills, monster, portalKC):
    return float(mobKills[monster][0]) < portalKC if len(mobKills) > monster else False


def getHighestPrint():
    awfulPrinterList = json.loads(session_data.account.raw_data["Print"])
    # print("Pinchy~ OUTPUT awfulPrinterList: ", type(awfulPrinterList), awfulPrinterList)
    goodPrinterList = [p for p in awfulPrinterList if isinstance(p, int)]
    highestPrintFound = max(goodPrinterList)
    # print("Pinchy~ OUTPUT Final highest print value found: ", highestPrintFound)

    return highestPrintFound


def threshold_for_highest_portal_opened(mobKills):
    threshold = next((
        threshold
        for threshold, monster, portalKC
        in portalOpeningKills
        if is_portal_opened(mobKills, monster, portalKC)
    ), Threshold.W1)

    return Threshold.fromname(threshold)


def tier_from_monster_kills(dictOfPRs) -> Threshold:
    """find highest enemy killed or world unlocked to compare to"""
    expectedThreshold = Threshold.fromname(Threshold.W1)

    highestPrint = getHighestPrint()
    mobKillThresholds = []
    if highestPrint >= 9500000000:  # Sites like IE/IT round up to 10B after 9.5B
        expectedThreshold = Threshold.fromname(Threshold.MAX_TIER)
    elif dictOfPRs[Placements.DEATH_NOTE] >= 24:
        expectedThreshold = Threshold.fromname(Threshold.W7_WAITING_ROOM)
    elif dictOfPRs[Placements.DEATH_NOTE] >= 21:
        expectedThreshold = Threshold.fromname(Threshold.SOLID_W7_PREP)
    else:
        # logger.info(f"Starting to review map kill counts per player because expectedIndex still W1: {dictOfPRs['Construction Death Note']}")
        for character in session_data.account.safe_characters:
            try:
                mobKills = json.loads(session_data.account.raw_data[f'KLA_{character.character_index}'])  # String pretending to be a list of lists yet again
            except:
                logger.exception(f"Could not retrieve KLA_{character.character_index} for Pinchy. Setting mobKills to empty list")
                mobKills = []
            # logger.info("%s, %s", type(playerKillsList), playerKillsList)  # Expected to be a list
            threshold = threshold_for_highest_portal_opened(mobKills)
            mobKillThresholds.append(threshold)

    expectedThreshold = max((expectedThreshold, *mobKillThresholds))

    return expectedThreshold


def generate_advice_list(sections: list[Tier], threshold: Threshold):
    advices = [
        Advice(label=section.section, picture_class=section.section, progression=section.tier, goal=section.next.tier, unit="T",
               value_format="{unit} {value}", as_link=True) for section in sections
    ]
    if threshold == Threshold.fromname(Threshold.MAX_TIER):
        for advice in advices:
            advice.progression = ""
            advice.goal = ""
            advice.unit = ""

    return advices


def generate_advice_groups(sectionsByThreshold: dict):
    advice_groups = []
    for threshold, sections in sectionsByThreshold.items():
        advices = generate_advice_list(sections, Threshold.fromname(threshold))

        advice_group = AdviceGroup(
            tier="",
            pre_string=f"{threshold} rated activit{pl(advices, 'y', 'ies')}",
            advices=advices
        )

        advice_groups.append(advice_group)
    return advice_groups


def generatePinchyWorld(all_sections):
    dictOfPRs = {section.name: section.pinchy_rating for section in all_sections}

    sectionPlacements: Placements = sort_pinchy_reviews(dictOfPRs)
    expectedThreshold: Threshold = tier_from_monster_kills(dictOfPRs)
    lowestThresholdReached: Threshold = sectionPlacements.lowest

    placements_per_section = sectionPlacements.per_section()
    for section in all_sections:
        section.pinchy_placement = placements_per_section[section.name]


    # Generate advice based on catchup
    equalSnippet = ""
    if lowestThresholdReached >= expectedThreshold:
        equalSnippet = ". Your lowest sections are roughly equal with (or better than!) your highest enemy map. Keep up the good work!"

    if expectedThreshold.name == Threshold.PLACEHOLDER:
        pinchyExpected = (
            "Huh. Something went a little wrong here. You landed in the Placeholder tier somehow. "
            "If you weren't expecting this, tell Scoli about it! O.o"
        )
        logger.warning("this really should not happen...")
        logger.warning(pinchyExpected)
    else:
        pinchyExpected = f"Expected Progression, based on highest enemy map: {expectedThreshold}"

    advice_groups = generate_advice_groups(sectionPlacements.final)

    sections_maxed_count = sectionPlacements.maxed_count
    sections_total = Placements.section_count
    sections_maxed = f"{sections_maxed_count}/{sections_total}"

    pinchy_high = AdviceSection(
        name="Pinchy high",
        tier=expectedThreshold.name,
        header=pinchyExpected,
        collapse=True
    )

    pinchy_low = AdviceSection(
        name="Pinchy low",
        tier=lowestThresholdReached.name,
        header=f"Minimum Progression, based on weakest ranked review: {lowestThresholdReached}{equalSnippet}",
        collapse=True
    )

    pinchy_all = AdviceSection(
        name="Pinchy all",
        tier=sections_maxed,
        header=f"Sections maxed: {sections_maxed}",
        picture="Pinchy.gif",
        groups=advice_groups
    )

    return pinchy_high, pinchy_low, pinchy_all
