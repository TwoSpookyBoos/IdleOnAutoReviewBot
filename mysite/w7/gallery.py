from models.general.session_data import session_data
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup


def get_missing_item() -> AdviceGroup:
    advices = {
        "Trophy": [
            trophy.get_how_get_advice()
            for trophy in session_data.account.gallery.missing.trophy
        ],
        "Nametag": [
            nametag.get_how_get_advice()
            for nametag in session_data.account.gallery.missing.nametag
        ],
    }
    group = AdviceGroup(
        pre_string="Get and bring to Codfrey",
        advices=advices,
        tier="",
        informational=True,
    )
    group.remove_empty_subgroups()
    return group


def get_gallery_show() -> AdviceGroup:
    gallery = session_data.account.gallery
    advices = {
        "Trophy podium": [
            gallery.podium[index].get_bonus_advice()
            for index in range(0, gallery.podium_count)
            if gallery.podium[index] is not None
        ],
        "Trophy inventory": [trophy.get_bonus_advice() for trophy in gallery.inventory],
        "Nametag": [
            nametag.get_bonus_advice()
            for nametag in gallery.nametag.values()
            if nametag.level > 0
        ],
    }
    group = AdviceGroup(
        pre_string="Gallery Showcase",
        advices=advices,
        tier="",
        informational=True,
    )
    group.remove_empty_subgroups()
    group.mark_advice_completed()
    return group


def get_gallery_bonus() -> AdviceGroup:
    gallery = session_data.account.gallery
    advices = [gallery.get_bonus_advice(name) for name in gallery.bonuses.keys()]
    group = AdviceGroup(
        pre_string="Gallery Bonuses",
        advices=advices,
        tier="",
        informational=True,
    )
    return group


def get_section() -> AdviceSection:
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="Gallery",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Gallery in W7!",
            picture="",
            unreached=True,
        )
    groups = [get_missing_item(), get_gallery_show(), get_gallery_bonus()]
    return AdviceSection(
        name="Gallery",
        tier="",
        header="Gallery WIP",
        picture="extracted_sprites/Codfrey.gif",
        groups=groups,
        informational=True,
        unrated=True,
    )
