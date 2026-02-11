from math import ceil, floor
from dataclasses import dataclass

from consts.consts_item_data import ITEM_DATA, ItemBonus
from consts.idleon.w7.gallery import podium_multi_by_level, nametag_multi_by_level
from consts.w7.gallery import nametag_max_level, bonus_image
from models.advice.advice import Advice
from models.general.item_definitions import ItemDefinition

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
        advice = self.get_bonus_advice()
        advice.change_progress(0, 1)
        return advice

    def get_bonus_advice(self) -> Advice:
        misc1_value = self._item.bonus.misc1.value * self._multi
        label = (
            f"{self.name}"
            f"<br>{round_and_trim(misc1_value)}{self._item.bonus.misc1.effect}"
        )
        if self._item.bonus.misc2.effect != "0":
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
        _add_item_bonus_to_total(self._item.bonus, total, self._multi)

    def _get_multi(self):
        if self.level is None:
            return 1
        return podium_multi_by_level[self.level]


def _add_item_bonus_to_total(
    item_bonus: ItemBonus, total: dict[str, float], multi: float
):
    if multi == 0:
        return
    total[" Weapon Power"] += item_bonus.weapon_power * multi
    total[" STR"] += item_bonus.str * multi
    total[" AGI"] += item_bonus.agi * multi
    total[" WIS"] += item_bonus.wis * multi
    total[" LUK"] += item_bonus.luk * multi
    total[" Defence"] += item_bonus.defence * multi
    total[item_bonus.misc1.effect] += item_bonus.misc1.value * multi
    total[item_bonus.misc2.effect] += item_bonus.misc2.value * multi


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
        _add_item_bonus_to_total(self._item.bonus, total, self._multi)

    def get_how_get_advice(self) -> Advice:
        advice = self.get_bonus_advice()
        advice.change_progress(0, 1)
        return advice

    def get_bonus_advice(self) -> Advice:
        misc1_value = self._item.bonus.misc1.value * self._multi
        label = (
            f"{self.name}"
            f"<br>{round_and_trim(misc1_value)}{self._item.bonus.misc1.effect}"
        )
        if self._item.bonus.misc2.effect != "0":
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
            if trophy_info.name == "I Made This Game":
                # "I Made This Game" Lava personal trophy
                continue
            self._bonuses_total[trophy_info.bonus.misc1.effect] = 0
            self._bonuses_total[trophy_info.bonus.misc2.effect] = 0
            all_trophy.append(GalleryTrophy(trophy_info))
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
            if nametag_info.name == "Lava's Awesome Nametag":
                # "Lava's Awesome Nametag" Lava personal nametag
                continue
            self._bonuses_total[nametag_info.bonus.misc1.effect] = 0
            self._bonuses_total[nametag_info.bonus.misc2.effect] = 0
            all_nametag.append(GalleryNametag(nametag_info))
        for nametag in all_nametag:
            level = safer_index(raw_nametag_level, nametag.index, 0)
            nametag.set_level(level)
            self.nametag[nametag.name] = nametag
            if nametag.level == 0:
                self.missing.nametag.append(nametag)

    def calculate_bonuses(self, account: "Account"):
        # TODO "GalleryBonusMulti" in source
        gallery_multi = 1.0
        self._calculate_trophy_bonuses(account, gallery_multi)
        self._calculate_nametag_bonuses(gallery_multi)
        for key, value in self._bonuses_total.items():
            if key == "0":
                continue
            self.bonuses[key.split(" ", 1)[1]] = (key, value)

    def _calculate_trophy_bonuses(self, account: "Account", gallery_multi: float):
        # PodiumsOwned in source. Last update in 2.48 Giftmas Event
        self.podium_count = min(
            19,
            1
            + ceil(account.coral_reef["Reef Corals"]["Paragorgia Coral"]["Level"] / 4)
            + account.sneaking.emporium["Another Gallery Podium"].value
            + floor(account.gemshop["Purchases"]["Gallery Showcases"]["Owned"] / 1)
            + 2 * int(account.spelunk.caves["Lunarheim"].bonus_obtained)
            + min(2, account.sailing["Artifacts"]["Deathskull"]["Level"])
            + account.event_points_shop["Bonuses"]["Plain Showcase"]["Owned"],
        )
        podium_lv4 = self._calculate_podium_lv4(account)
        podium_lv3 = self._calculate_podium_lv3(account) + podium_lv4
        podium_lv2 = self._calculate_podium_lv2(account) + podium_lv3
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
            podium.calculate_bonus(gallery_multi)
            podium.add_bonus_to(self._bonuses_total)
        for item in self.inventory:
            item.calculate_bonus(gallery_multi)
            item.add_bonus_to(self._bonuses_total)

    def _calculate_podium_lv2(self, account):
        # PodiumsOwned_Lv2 in source. Last update in 2.48 Giftmas Event
        deathskull_level = account.sailing["Artifacts"]["Deathskull"]["Level"]
        return (
            2 * account.clam_work.bonuses[0].obtained
            # TODO: + Math.min(2, m._customBlock_RandomEvent("KillroyBonuses", 3, 0))
            + 2 * ("Eamsy Earl" in account.companions)
            + floor(account.gemshop["Purchases"]["Gallery Showcases"]["Owned"] / 2)
            + account.legend_talents["Talents"]["Superb Gallerium"]["Value"]
            + max(0, min(2, deathskull_level - 2) - min(1, floor(deathskull_level / 5)))
        )

    def _calculate_podium_lv3(self, account):
        # PodiumsOwned_Lv3 in source. Last update in 2.48 Giftmas Event
        return floor(
            account.gemshop["Purchases"]["Gallery Showcases"]["Owned"] / 3
        ) + min(1, floor(account.sailing["Artifacts"]["Deathskull"]["Level"] / 5))

    def _calculate_podium_lv4(self, account):
        # PodiumsOwned_Lv4 in source. Last update in 2.48 Giftmas Event
        return (
            1 * ("RIP Tide" in account.companions)
            + account.event_points_shop["Bonuses"]["Worldclass Showcase"]["Owned"]
        )

    def _calculate_nametag_bonuses(self, gallery_multi: float):
        for nametag in self.nametag.values():
            if nametag.level == 0:
                continue
            nametag.calculate_bonus(gallery_multi)
            nametag.add_bonus_to(self._bonuses_total)

    def get_bonus_advice(self, name: str):
        (effect, value) = self.bonuses[name]
        image = bonus_image.get(name, "placeholder")
        return Advice(label=f"{round_and_trim(value)}{effect}", picture_class=image)

    # TODO Aler if empty podium slot
