from models import AdviceSection, AdviceGroup, Advice, Character
from utils import get_logger

from flask import g as session_data

logger = get_logger(__name__)

skillsToReview_RightHand = ["Mining", "Choppin", "Fishing", "Catching", "Trapping", "Worship"]


class Maestro:
    def __init__(self, character: Character):
        self.index: int = character.character_index
        self.name: str = character.character_name
        self.classname: str = character.class_name
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
    account = session_data.data
    maestros: list[Character] = [toon for toon in account.all_characters if toon.sub_class == "Maestro"]

    janky_skills = dict()
    post_string = ""
    tier = ""
    if not maestros:
        header = "Gosh golly, I'm jealous, So many nice things ahead of you! Check this section again once you've acquired a Maestro"

        if len(account.characters) == account.max_toon_count:
            header = "Oh no... Your family is full but you haven't created any Beginners... I wish you the best of luck 😔"

    else:
        janky_skills = maestros_goal_levels(account, maestros)

        tier = f"{len(janky_skills) or 6}/{len(skillsToReview_RightHand)}"

        if not janky_skills:
            if len(maestros) > 1:
                header = "Your Maestros are a workforce to be dealt with! An arduous bunch, the lot!"
            else:
                header = f"{maestros[0]} is the highest level in all {tier} Right Hand skills! A Jack of trades, this one! ❤️"
        else:
            header = f"{maestros[0]} is not the highest level in {tier} Right Hand skills:"
            if "Worship" in janky_skills:
                post_string = "Worship matters moreso for Species Epoch than Right Hand. Don't steal charge away from this character!"

    advices = [
        Advice(label=skill, picture_class=skill, progression=maestro.skills[skill], goal=goal)
        for skill, (maestro, goal) in janky_skills.items()
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

    return maestro


def maestros_goal_levels(account, maestros):
    janky_skills = dict()

    for skill in skillsToReview_RightHand:
        chars_ordered: list[Character] = sorted(account.characters, key=lambda toon: toon.skills[skill])
        best_maestro = next((toon for toon in chars_ordered if toon in maestros), None)
        best_maestro_rank = chars_ordered.index(best_maestro)

        if best_maestro_rank == 0:
            # maestro is already best
            continue

        required_level = chars_ordered[best_maestro_rank - 1].skills[skill] + 1
        janky_skills[skill] = (best_maestro, required_level)

    return janky_skills