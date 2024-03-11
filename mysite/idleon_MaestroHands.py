from models import AdviceSection, AdviceGroup, Advice, Character
from utils import get_logger

from flask import g as session_data

logger = get_logger(__name__)

skillsToReview_RightHand = ["Mining", "Choppin", "Fishing", "Catching", "Trapping", "Worship"]


def getHandsStatus():
    maestros: list[Character] = [
        toon for toon in session_data.account.all_characters if toon.sub_class == "Maestro"
    ]
    beginners: list[Character] = [
        toon for toon in session_data.account.all_characters if toon.base_class == "Beginner" or toon.base_class == "Journeyman"
    ]

    janky_skills = maestros_goal_levels(maestros)
    tier = f"{len(janky_skills) or 6}/{len(skillsToReview_RightHand)}"
    header = create_header(janky_skills, maestros, beginners, tier)

    post_string = ""
    if "Worship" in janky_skills:
        post_string = "Worship matters moreso for Species Epoch than Right Hand. Don't steal charge away from this character!"

    advices = [
        Advice(
            label=maestro.character_name,
            picture_class=skill,
            progression=maestro.skills[skill],
            goal=goal,
        )
        for skill, (maestro, goal) in janky_skills.items()
    ]

    groups = [
        AdviceGroup(
            tier="", pre_string="Get grindin'", post_string=post_string, advices=advices
        )
    ]

    section = AdviceSection(
        name="Maestro Right Hands",
        tier=tier,
        header=header,
        picture="Maestro.png",
        groups=groups,
    )

    return section


def create_header(janky_skills, maestros, beginners, tier):
    account = session_data.account
    if not maestros:
        header = "Gosh golly, I'm jealous, So many nice things ahead of you!<br>Check this section again once you've acquired a Maestro"

        if len(account.characters) == account.max_toon_count and not beginners:
            header = "Oh… Oh no… Your family is full but I don't see any future Maestros…<br>I wish you the best of luck 😔"

    else:

        if not janky_skills:
            if len(maestros) > 1:
                header = "Your Maestros are a workforce to be dealt with! An arduous bunch, the lot!"
            else:
                header = f"{maestros[0]} is the highest level in all {tier} Right Hand skills! A Jack of trades, this one! ❤️"
        else:
            if len(maestros) > 1:
                header = f"Your Maestros are not the highest level in {tier} Right Hand skills:"
            else:
                header = f"{maestros[0]} is not the highest level in {tier} Right Hand skills:"
    return header


def maestros_goal_levels(maestros):
    account = session_data.account
    janky_skills = dict()

    if not maestros:
        return janky_skills

    for skill in skillsToReview_RightHand:
        chars_ordered: list[Character] = sorted(
            account.characters, key=lambda toon: toon.skills[skill], reverse=True
        )
        best_maestro = next((toon for toon in chars_ordered if toon in maestros), None)
        best_maestro_rank = chars_ordered.index(best_maestro)

        if best_maestro_rank == 0:
            # maestro is already best
            continue

        required_level = chars_ordered[best_maestro_rank - 1].skills[skill] + 1
        janky_skills[skill] = (best_maestro, required_level)

    return janky_skills
