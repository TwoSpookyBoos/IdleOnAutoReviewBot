import idleon_SkillLevels
from models import AdviceSection, AdviceGroup, Advice
from utils import get_logger


logger = get_logger(__name__)


class Beginner:
    def __init__(self, char_index: int, name: str, class_index: int):
        self.index: int = char_index
        self.name: str = name
        self.classname: str = idleon_SkillLevels.getHumanReadableClasses(class_index)
        self.janky_skills: list[tuple] = list()

    @property
    def fullname(self):
        return f"{self.name} the {self.classname}"

    @property
    def jankiness(self):
        return len(self.janky_skills)

    @property
    def is_jack_of_trades(self):
        return self.jankiness == 0

    @property
    def should_be_more_pious(self):
        return "Worship" in (e[0] for e in self.janky_skills)


def getHandsStatus(inputJSON, playerCount, playerNames):
    skillsToReview_RightHand = ["Mining", "Choppin", "Fishing", "Catching", "Trapping", "Worship"]
    class_indices = [3, 4, 5, 6]  # Includes the placeholder numbers after Vman
    beginners: list[Beginner] = list()

    for char_index, charname in enumerate(playerNames):
        try:
            class_index = inputJSON['CharacterClass_'+str(char_index)]

            if class_index not in class_indices:
                continue

            beginners.append(Beginner(char_index, charname, class_index))

        except Exception as reason:
            logger.error("Unable to get Class name for character %s because: %s", char_index, reason)

    #print("MaestroHands.getHandsStatus~ OUTPUT characterClassesList:",characterClassesList)
    #print("MaestroHands.getHandsStatus~ OUTPUT handsCharactersDict:",handsCharactersDict)

    allSkillsDict = idleon_SkillLevels.getAllSkillLevelsDict(inputJSON, playerCount)

    for beginner in beginners:
        for skill in skillsToReview_RightHand:  # string, the name of the skill
            skill_levels = allSkillsDict[skill]
            best_level = max(skill_levels)
            beginners_skill_level = skill_levels[beginner.index]

            if beginners_skill_level < best_level:
                logger.info("Adding skill to %s's Right Hand skills because their %s level of %s is less than max of %s", beginner.name, skill, beginners_skill_level, best_level)
                beginner.janky_skills.append((skill, beginners_skill_level, best_level))
    #print("MaestroHands.getHandsStatus~ OUTPUT handsCharactersDict:",handsCharactersDict)

    # in case some unfortunate soul or an absolute madlad chose to have more than one beginner, choose the one that's the most skilled
    main_beginner = min(beginners, key=lambda b: b.jankiness, default=None)

    tier = f"{main_beginner.jankiness or 6}/{len(skillsToReview_RightHand)}" if main_beginner else ""

    if not main_beginner:
        header = "Gosh golly, I'm jealous, So many nice things ahead of you! Check this section again once you've acquired a Maestro"
    elif main_beginner.is_jack_of_trades:
        header = f"{main_beginner.fullname} is the highest level in all {tier} Right Hand skills! A Jack of trades, this one! ❤️"
    else:
        header = f"{main_beginner.fullname} is not the highest level in {tier} Right Hand skills:"

    post_string = ""
    if main_beginner and main_beginner.should_be_more_pious:
        post_string = "Worship matters moreso for Species Epoch than Right Hand. Don't steal charge away from this character!"

    advices = [
        Advice(
            label=skill,
            item_name=skill,
            progression=progression,
            goal=goal
        )
        for skill, progression, goal in (main_beginner.janky_skills if main_beginner else [])
    ]

    groups = [
        AdviceGroup(
            tier="",
            pre_string="Get grindin'",
            post_string=post_string,
            advices=advices
        )
    ]

    maestro = AdviceSection(
        name="Maestro Right Hands",
        tier=tier,
        header=header,
        picture="Maestro.png",
        groups=groups,
    )

    #print("MaestroHands.getHandsStatus~ OUTPUT advice_LeftHands:",advice_LeftHands)
    #print("MaestroHands.getHandsStatus~ OUTPUT advice_RightHands:",advice_RightHands)

    return maestro
