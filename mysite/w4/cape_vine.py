from consts.w4.cape_vine import cape_vine_capes
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data
from utils.number_formatting import round_and_trim

section_name = "Cape Vine"
section_picture = "monster/Catherine.gif"


def get_golden_vines_group() -> AdviceGroup:
    cape_vine = session_data.account.cape_vine
    return AdviceGroup(
        pre_string="Golden Vines",
        post_string="Capes on a Golden Vine get the full multi, others 0.25x of it",
        advices=[
            cape_vine.get_golden_vines_advice(),
            cape_vine.get_bundle_advice(),
        ],
        tier="",
        informational=True,
    )


def get_multi_group() -> AdviceGroup:
    cape_vine = session_data.account.cape_vine
    return AdviceGroup(
        pre_string="Cape Vine Multi",
        advices={
            f"Total: {round_and_trim(cape_vine.multi)}x on a Golden Vine, "
            f"{round_and_trim(cape_vine.plain_multi)}x on other vines": [
                cape_vine.get_deposited_multi_advice(),
                session_data.account.companions["Catherine"].get_advice(),
            ],
        },
        tier="",
        informational=True,
    )


def get_vine_group() -> AdviceGroup:
    cape_vine = session_data.account.cape_vine
    return AdviceGroup(
        pre_string=f"Deposited capes: {cape_vine.deposited_count}"
        f"/{len(cape_vine_capes)}",
        advices=[slot.get_advice() for slot in cape_vine.slots],
        tier="",
        informational=True,
    )


def get_missing_group() -> AdviceGroup:
    return AdviceGroup(
        pre_string="Missing capes",
        advices=[cape.get_advice() for cape in session_data.account.cape_vine.missing],
        tier="",
        informational=True,
    )


def get_unlock_group() -> AdviceGroup:
    return AdviceGroup(
        pre_string="Characters without the Cape Vine",
        advices=[
            character.get_showcase_unlock_advice("Cape Vine", 4, "Cape")
            for character in session_data.account.characters
            if not character.cape_vine_bonus_active
        ],
        tier="",
        informational=True,
    )


def get_section() -> AdviceSection:
    if session_data.account.world_progress.highest_reached < 4:
        return AdviceSection(
            name=section_name,
            tier="Not Yet Evaluated",
            header="Come back after reaching World 4 to visit Catherine's Cape Vine!",
            picture=section_picture,
            unreached=True,
        )

    return AdviceSection(
        name=section_name,
        tier="",
        header=section_name,
        picture=section_picture,
        groups=[
            get_missing_group(),
            get_vine_group(),
            get_multi_group(),
            get_golden_vines_group(),
            get_unlock_group(),
        ],
        informational=True,
        unrated=True,
    )
