from math import ceil, floor
from dataclasses import dataclass

from consts.consts_general import equipment_by_bonus_dict
from consts.consts_item_data import ITEM_DATA
from consts.idleon.w7.gallery import podium_multi_by_level, nametag_multi_by_level
from consts.w7.gallery import (
    nametag_max_level,
    bonus_image,
    prisma_palette_index,
    prisma_palette_max,
    exalted_palette_index,
    exalted_palette_max,
    killroy_kills_optlacc_index,
    w6_trophy_codename,
    gallery_card_codename,
)
from models.advice.advice import Advice
from models.general.companions import Companions
from models.general.item_definitions import ItemDefinition
from models.w7.clam_work import ClamWork
from models.w7.sushi_station import SushiStation

from utils.logging import get_logger
from utils.number_formatting import parse_number, round_and_trim
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)


class GalleryTrophy:
    def __init__(self, trophy_info: ItemDefinition):
        self.index = parse_number(trophy_info.code_name.removeprefix("Trophy"))
        self.name = trophy_info.name
        self._item = trophy_info
        self._multi = 1
        self.level = None

    def set_level(self, level: int):
        self.level = level

    def calculate_bonus(self, multi: float):
        self._multi = self._get_multi() * multi

    def get_how_get_advice(self) -> Advice:
        advice = self.get_bonus_advice(link_to_section=False)
        advice.change_progress(0, 1)
        return advice

    def get_bonus_advice(self, stats: set[str] | None = None, link_to_section: bool = True) -> Advice:
        link_to_section_text = "{{ Gallery|#gallery }} - " if link_to_section else ""
        label = f"{link_to_section_text}{self.name}"
        if stats is None or _misc_bonus_stat(self.name, 1) in stats:
            misc1_value = self._item.bonus.misc1.value * self._multi
            label += f"<br>{round_and_trim(misc1_value)}{self._item.bonus.misc1.effect}"
        if self._item.bonus.misc2.effect != "0" and (stats is None or _misc_bonus_stat(self.name, 2) in stats):
            misc2_value = self._item.bonus.misc2.value * self._multi
            label += f"<br>{round_and_trim(misc2_value)}{self._item.bonus.misc2.effect}"
        resource = ""
        if self.level is not None:
            multi = podium_multi_by_level[self.level]
            if self.level == 0:
                label += f"<br>Inventory Multi: {round_and_trim(multi)}x"
            else:
                resource = f"gallery-slot-{self.level - 1}"
                label += f"<br>Podium Multi: {round_and_trim(multi)}x"
        return Advice(label=label, picture_class=self.name, resource=resource)

    def add_bonus_to(self, total: dict[str, float]):
        self._item.bonus.add_to(total, self._multi)

    def _get_multi(self):
        if self.level is None:
            return 1
        return podium_multi_by_level[self.level]


def _js_round(value: float) -> int:
    # JS Math.round, halves up
    return floor(value + 0.5)


def _misc_bonus_stat(item_name: str, slot: int) -> str | None:
    """Which stat (e.g. 'DropRate') item_name's MiscN bonus represents, per
    equipment_by_bonus_dict, or None if that curated dataset doesn't cover this item."""
    for stat_entries in equipment_by_bonus_dict.values():
        data = stat_entries.get(item_name)
        if data:
            return data.get(f"Misc{slot}", {}).get("Bonus")
    return None


class GalleryNametag:
    def __init__(self, nametag_info: ItemDefinition):
        self.index = self._get_index(nametag_info.code_name)
        self.name = nametag_info.name
        self._item = nametag_info
        self.level = 0
        self._multi = 1

    def _get_index(self, code_name: str) -> int:
        match code_name.removeprefix("EquipmentNametag"):
            case "6b":
                return 6
            case Value:
                return parse_number(Value)

    def set_level(self, level: int):
        self.level = level

    def calculate_bonus(self, multi: float):
        self._multi = self._get_level_multi() * multi

    def add_bonus_to(self, total: dict[str, float]):
        self._item.bonus.add_to(total, self._multi)

    def get_how_get_advice(self) -> Advice:
        advice = self.get_bonus_advice(link_to_section=False)
        advice.change_progress(0, 1)
        return advice

    def get_bonus_advice(self, stats: set[str] | None = None, link_to_section: bool = True) -> Advice:
        link_to_section_text = "{{ Gallery|#gallery }} - " if link_to_section else ""
        label = f"{link_to_section_text}{self.name}"
        if stats is None or _misc_bonus_stat(self.name, 1) in stats:
            misc1_value = self._item.bonus.misc1.value * self._multi
            label += f"<br>{round_and_trim(misc1_value)}{self._item.bonus.misc1.effect}"
        if self._item.bonus.misc2.effect != "0" and (stats is None or _misc_bonus_stat(self.name, 2) in stats):
            misc2_value = self._item.bonus.misc2.value * self._multi
            label += f"<br>{round_and_trim(misc2_value)}{self._item.bonus.misc2.effect}"
        if self.level > 0:
            label += f"<br>Level Multi: {round_and_trim(self._get_level_multi())}x"
        return Advice(
            label=label,
            picture_class=self.name,
            progression=self.level,
            goal=nametag_max_level,
        )

    def _get_level_multi(self):
        if self.level == 0:
            return 1
        return nametag_multi_by_level[min(nametag_max_level, self.level) - 1]


@dataclass
class GalleryMissing:
    trophy: list[GalleryTrophy]
    nametag: list[GalleryNametag]


class Gallery:
    def __init__(self, raw_data: dict):
        spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        # "KillroyBonuses"(3) in source. Last updated in v2.531.0
        killroy_kills = parse_number(
            safer_index(raw_optlacc, killroy_kills_optlacc_index, 0)
        )
        self._killroy_bonus = killroy_kills / (200 + killroy_kills) * 10
        self.gallery_multi = 1.0
        self._gallery_multi_by_chip = {}
        self._bonuses_by_chip = {}
        self._palette_levels = safer_index(spelunk_info, 9, []) or []
        raw_lore = safer_index(spelunk_info, 0, [])
        self._has_lore_8 = parse_number(safer_index(raw_lore, 8, 0)) >= 1
        self.prisma_palette_bonus = 0.0
        self.exalted_palette_bonus = 0.0
        self.has_w6_trophy = w6_trophy_codename in safe_loads(
            raw_data.get("Cards1", [])
        )
        self._bonuses_total = {
            " Weapon Power": 0,
            " STR": 0,
            " AGI": 0,
            " WIS": 0,
            " LUK": 0,
            " Defence": 0,
        }
        # Trophy
        raw_trophy_index_list: list[int] = safer_index(spelunk_info, 16, [])
        self.trophy: dict[str, GalleryTrophy] = {}
        self.inventory: list[GalleryTrophy] = []
        self.podium: list[GalleryTrophy | None] = [None] * (
            len(raw_trophy_index_list) - 48
        )
        self.missing = GalleryMissing([], [])
        self._parse_trophy(raw_trophy_index_list)
        # Nametag
        raw_nametag_level: list[int] = safer_index(spelunk_info, 17, [])
        self.nametag: dict[str, GalleryNametag] = {}
        self._parse_nametag(raw_nametag_level)
        # Total bonuses
        self.bonuses = {}

    def _parse_trophy(self, raw_trophy_index_list: list[int]):
        all_trophy = []
        for trophy_info in ITEM_DATA.get_items_by_type("TROPHY"):
            trophy = GalleryTrophy(trophy_info)
            # "I Made This Game" Lava personal trophy
            if (
                trophy.name == "I Made This Game"
                and trophy.index not in raw_trophy_index_list
            ):
                # Account don't have it, skip
                continue
            self._bonuses_total[trophy_info.bonus.misc1.effect] = 0
            self._bonuses_total[trophy_info.bonus.misc2.effect] = 0
            all_trophy.append(trophy)
            self.trophy[trophy.name] = trophy
        _trophy_by_index = {trophy.index: trophy for trophy in all_trophy}

        for trophy in all_trophy:
            if trophy.index not in raw_trophy_index_list:
                # Trophy not in gallery
                self.missing.trophy.append(trophy)
                continue
        for gallery_index, trophy_index in enumerate(raw_trophy_index_list):
            if trophy_index == -1:
                continue
            if gallery_index < 48:
                # Trophy in inventory
                item = _trophy_by_index[trophy_index]
                item.set_level(0)
                self.inventory.append(item)
            else:
                # Trophy on podium
                self.podium[gallery_index - 48] = _trophy_by_index[trophy_index]

    def _parse_nametag(self, raw_nametag_level: list[int]):
        all_nametag = []
        for nametag_info in ITEM_DATA.get_items_by_type("NAMETAG"):
            nametag = GalleryNametag(nametag_info)
            # "Lava's Awesome Nametag" Lava personal nametag
            if (
                nametag.name == "Lava's Awesome Nametag"
                and safer_index(raw_nametag_level, nametag.index, 0) == 0
            ):
                # Account don't have it, skip
                continue
            self._bonuses_total[nametag_info.bonus.misc1.effect] = 0
            self._bonuses_total[nametag_info.bonus.misc2.effect] = 0
            all_nametag.append(nametag)
        for nametag in all_nametag:
            level = safer_index(raw_nametag_level, nametag.index, 0)
            nametag.set_level(level)
            self.nametag[nametag.name] = nametag
            if nametag.level == 0:
                self.missing.nametag.append(nametag)

    def calculate_palette_bonuses(self, picasso_gaming: float):
        # Before stamps and prisma, which read these
        self.prisma_palette_bonus = self.get_palette_decay_bonus(
            prisma_palette_index, prisma_palette_max, picasso_gaming
        )
        self.exalted_palette_bonus = self.get_palette_decay_bonus(
            exalted_palette_index, exalted_palette_max, picasso_gaming
        )

    def get_palette_decay_bonus(
        self, index: int, max_value: float, picasso_gaming: float
    ) -> float:
        # "PaletteBonus" in source, decay rows only. Last updated in v2.531.0
        palette_level = parse_number(safer_index(self._palette_levels, index, 0))
        return (
            palette_level / (palette_level + 25) * max_value
            * (1 + picasso_gaming / 100)
            * (1 + 0.5 * self._has_lore_8)
        )

    def calculate_bonuses(
        self,
        *,
        highest_world_reached: int,
        characters: list,
        cards: list,
        alchemy_bubbles,
        coral_reef,
        artifacts,
        gemshop,
        emporium,
        spelunk,
        legend_talents,
        event_shop,
        clam_work: "ClamWork",
        companions: "Companions",
        sushi_station: "SushiStation",
    ):
        # Section view: any wearer. Drop rate uses each character's chip
        has_motherboard_chip = highest_world_reached >= 7 and any(
            "Silkrode Motherboard" in character.equipped_lab_chips
            for character in characters
        )
        gallery_card_level = next(
            (card.level for card in cards if card.codename == gallery_card_codename),
            0,
        )
        codfrey_prisma = alchemy_bubbles.get_prisma_value("Codfrey Rulz Ok")
        paragorgia_level = coral_reef["Paragorgia Coral"].level
        deathskull_level = artifacts["Deathskull"].level
        showcases_owned = gemshop.purchases["Gallery Showcases"].owned
        emporium_podium = emporium["Another Gallery Podium"].value
        lunarheim_obtained = spelunk.caves["Lunarheim"].bonus_obtained
        superb_gallerium = legend_talents["Superb Gallerium"].value
        plain_showcase = event_shop["Plain Showcase"].owned
        worldclass_showcase = event_shop["Worldclass Showcase"].owned
        self._gallery_multi_by_chip = {
            chip: self._calculate_gallery_multi(
                chip,
                gallery_card_level,
                codfrey_prisma,
                paragorgia_level,
                clam_work,
                companions,
                sushi_station,
            )
            for chip in (False, True)
        }
        self._set_podium_levels(
            paragorgia_level,
            deathskull_level,
            showcases_owned,
            emporium_podium,
            lunarheim_obtained,
            superb_gallerium,
            plain_showcase,
            worldclass_showcase,
            clam_work,
            companions,
        )
        # Per character chip; section shows the chip once anyone wears it
        self._bonuses_by_chip = {
            chip: self._get_bonuses(self._gallery_multi_by_chip[chip])
            for chip in (False, True)
        }
        self.gallery_multi = self._gallery_multi_by_chip[has_motherboard_chip]
        self.bonuses = self._get_bonuses(self.gallery_multi)

    def get_character_bonus_value(self, name: str, has_motherboard_chip: bool) -> float:
        # "GalleryBonusMulti" reads the current character's chip
        bonuses = self._bonuses_by_chip.get(has_motherboard_chip, {})
        return bonuses.get(name, ("", 0))[1]

    def _get_bonuses(self, gallery_multi: float) -> dict[str, tuple[str, float]]:
        # Leaves items on this multi for their advice
        total = dict.fromkeys(self._bonuses_total, 0)
        for item in [*filter(None, self.podium), *self.inventory]:
            item.calculate_bonus(gallery_multi)
            item.add_bonus_to(total)
        for nametag in self.nametag.values():
            if nametag.level == 0:
                continue
            nametag.calculate_bonus(gallery_multi)
            nametag.add_bonus_to(total)
        return {
            key.split(" ", 1)[1]: (key, value)
            for key, value in total.items()
            if key != "0"
        }

    def _calculate_gallery_multi(
        self,
        has_motherboard_chip: bool,
        gallery_card_level: int,
        codfrey_prisma: float,
        paragorgia_level: int,
        clam_work: "ClamWork",
        companions: "Companions",
        sushi_station: "SushiStation",
    ) -> float:
        # "GalleryBonusMulti" in source. Last updated in v2.531.0
        return 1 + (
            3 * paragorgia_level
            + 10 * has_motherboard_chip
            + 3 * clam_work.bonuses[7].obtained
            + self._killroy_bonus
            + min(20, codfrey_prisma)
            + min(10, gallery_card_level)
            + companions["Bubba the Seal"].bonus
            + sushi_station.get_milestone_bonus_value("Gallery Bonus Multi")
        ) / 100

    def _set_podium_levels(
        self,
        paragorgia_level: int,
        deathskull_level: int,
        showcases_owned: int,
        emporium_podium: float,
        lunarheim_obtained: bool,
        superb_gallerium: float,
        plain_showcase: int,
        worldclass_showcase: int,
        clam_work: "ClamWork",
        companions: "Companions",
    ):
        # PodiumsOwned in source. Last update in 2.48 Giftmas Event
        self.podium_count = min(
            19,
            1
            + ceil(paragorgia_level / 4)
            + emporium_podium
            + floor(showcases_owned / 1)
            + 2 * int(lunarheim_obtained)
            + min(2, deathskull_level)
            + plain_showcase,
        )
        podium_lv4 = self._calculate_podium_lv4(
            companions, worldclass_showcase, deathskull_level
        )
        podium_lv3 = (
            self._calculate_podium_lv3(showcases_owned, deathskull_level)
            + podium_lv4
        )
        podium_lv2 = (
            self._calculate_podium_lv2(
                clam_work, companions, showcases_owned,
                superb_gallerium, deathskull_level,
            )
            + podium_lv3
        )
        for index, podium in enumerate(self.podium):
            if podium is None:
                continue
            if index < podium_lv4:
                podium.set_level(4)
            elif index < podium_lv3:
                podium.set_level(3)
            elif index < podium_lv2:
                podium.set_level(2)
            else:
                podium.set_level(1)

    def _calculate_podium_lv2(
        self,
        clam_work: "ClamWork",
        companions: "Companions",
        showcases_owned: int,
        superb_gallerium: float,
        deathskull_level: int,
    ) -> int:
        # "PodiumsOwned_Lv2" in source, Math.round. Last updated in v2.531.0
        return _js_round(
            2 * clam_work.bonuses[0].obtained
            + min(2, self._killroy_bonus)
            + companions["Eamsy Earl"].bonus  # 2, or 3 upgraded
            + floor(showcases_owned / 2)
            + superb_gallerium
            + max(0, min(2, deathskull_level - 2) - min(1, floor(deathskull_level / 5)))
        )

    def _calculate_podium_lv3(self, showcases_owned: int, deathskull_level: int) -> int:
        # PodiumsOwned_Lv3 in source. Last update in 2.48 Giftmas Event
        return floor(showcases_owned / 3) + min(1, floor(deathskull_level / 5))

    def _calculate_podium_lv4(
        self,
        companions: "Companions",
        worldclass_showcase: int,
        deathskull_level: int,
    ) -> int:
        # "PodiumsOwned_Lv4" in source, Math.round. Last updated in v2.531.0
        return _js_round(
            companions["RIP Tide"].get_value("Showcase Slot")
            + worldclass_showcase
            + min(1, floor(deathskull_level / 6))
        )

    def get_bonus_advice(self, name: str):
        effect, value = self.bonuses[name]
        image = bonus_image.get(name, "placeholder")
        return Advice(label=f"{round_and_trim(value)}{effect}", picture_class=image)

    def get_exalted_palette_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Gallery|#gallery }}}} - Honey Yellow Palette: "
            f"+{round_and_trim(self.exalted_palette_bonus)}%",
            picture_class="palette-slot",
        )

    # TODO Aler if empty podium slot
