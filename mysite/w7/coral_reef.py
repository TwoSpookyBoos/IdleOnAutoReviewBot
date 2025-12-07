from models.models import AdviceSection, AdviceGroup, Advice
from flask import g as session_data

from models.models_util import get_coral_reef_advice


def get_corals_info_group() -> AdviceGroup:
    coral_advice: list[Advice] = [get_coral_reef_advice(name) for name in session_data.account.coral_reef.keys()]
    return AdviceGroup(
        pre_string='Corals',
        advices=coral_advice,
        tier='',
        informational=True
    )

# TODO: Info group about sources of Coral Reef Corals
def get_sources_of_coral_info_group() -> AdviceGroup:
    ...

def get_coral_reef_section():
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        reef_AdviceSection = AdviceSection(
            name='Coral Reef',
            tier='Not Yet Evaluated',
            header='Come back after unlocking W7!',
            picture='',
            unrated=None,
            unreached=True,
            completed=False
        )
        return reef_AdviceSection

    groups = [get_corals_info_group()]
    return AdviceSection(
        name='Coral Reef',
        tier='',
        header='Coral Reef',
        picture='extracted_sprites/HumbleHugh0.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
