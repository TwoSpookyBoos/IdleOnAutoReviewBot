from consts.consts_autoreview import EmojiType, ValueToMulti
from consts.general.common import percent_break_point
from consts.idleon.lava_func import lava_func
from consts.idleon.w7.spelunk import (
    spelunking_cave_list,
    spelunk_chapters,
    spelunk_shop_upgrades
)
from consts.w7.spelunk import (
    chapter_name,
    chapter_bonus_img,
    shop_upgrade_image_indexes,
    super_talent_preset_offsets,
    super_talent_preset_slots,
)

from models.advice.advice import Advice

from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index, safer_convert
from utils.logging import get_logger

logger = get_logger(__name__)


class SpelunkCave:
    def __init__(self, index: int, info: dict, state: int):
        self.name = info["Name"]
        self._description = info["Description"]
        self.bonus_obtained = bool(state)
        self._image = f"spelunking-boss-{index}"
        self._resource = f"spelunking-cavern-{index}"

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{ Spelunking|#spelunking }} - "
        label += f"{self.name}:<br>{self._description}"
        return Advice(
            label=label,
            picture_class=self._image,
            progression=int(self.bonus_obtained),
            goal=1,
            resource=self._resource,
        )

    def get_unlock_advice(self) -> Advice:
        return Advice(
            label="{{Spelunking|#spelunking}}:<br>"
            f"Defeat the Boss of the {self.name} Cave",
            picture_class=self._image,
            progression=int(self.bonus_obtained),
            goal=1,
        )


class LoreBonus:
    def __init__(self, chapter_index: int, index: int, info: dict, level: int):
        self.level = level
        self._template = info["Description"]
        self._image = chapter_bonus_img[index]
        self._x1 = info["x1"]
        self._x2 = info["x2"]
        self._lava_fun = info["LavaFun"]
        self._min_page = info["MinPage"]
        self._multi_by_artifact = info["MultiByArtifact"]
        self.value = 0
        self._value_per_level = 0
        self.max_value = None
        self.resource = f"spelunking-chapter-{chapter_index + 1}"

    def calculate_bonus(self, multi):
        multi = self._multi_by_artifact * multi
        self.value = multi * lava_func(self._lava_fun, self.level, self._x1, self._x2)
        match self._lava_fun:
            case "decay":
                self.max_value = self._x1 * multi
            case "decayMulti":
                self.max_value = (1 + self._x1) * multi
            case _:
                self._value_per_level = self._x1 * multi
                self.max_value = None

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{ Lore Chapters Bonus|#spelunking }}:<br>"
        value = f"{round_and_trim(self.value)}"
        if self.max_value is not None:
            value += f"/{round_and_trim(self.max_value)}"
        bonus = self._template.replace("{", value).replace("}", value)
        if not link_to_section:
            label += f"Level {self.level}: {bonus}"
            if self.max_value is not None:
                current_percent = self.value / self.max_value
                progress = f"{current_percent:.2%}"
                goal = "100%"
                for percent in percent_break_point:
                    if current_percent < percent:
                        next_level, next_bonus = self._get_percent_info(percent)
                        label += (
                            "<br>Next Breakpoint:"
                            f"<br>Level {next_level} ({percent:.0%}): {next_bonus}"
                        )
                        break
            else:
                progress = "Linear"
                goal = EmojiType.INFINITY.value
                label += f"<br>+{self._value_per_level} per level"
            label += f"<br>Required pages: {self._min_page}"
        else:
            label += bonus
            progress = self.level
            goal = EmojiType.INFINITY.value
        return Advice(
            label=label,
            picture_class=self._image,
            resource=self.resource,
            progression=progress,
            goal=goal,
        )

    def _get_percent_info(self, percent: float) -> tuple[int, str] | None:
        if percent >= 1.0 or percent < 0 or self.max_value is None:
            return None
        next_value = f"{round_and_trim(self.max_value * percent)}"
        next_bonus = self._template.replace("{", next_value).replace("}", next_value)
        next_level = int(self._x2 * percent / (1 - percent))
        return next_level, next_bonus


class SpelunkShopUpgrade:
    # Raw per-level value only; rows 0-3, 7-10, 19, 25, 38, 54-56, 59-61
    # scale further in source. Last updated in v2.531.0
    def __init__(self, index: int, info: dict, level: int):
        self.index = index
        self.name = info["Name"]
        self.max_level = info["Max Level"]
        self.value_per_level = info["Value Per Level"]
        self._template = info["Description"]
        self.level = max(0, level)
        # "ShopUpgBonus" in source. Last updated in v2.531.0
        self.value = self.value_per_level * self.level

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{ Spelunking|#spelunking }} - "
        is_multi = "}" in self._template and "{" not in self._template
        value = ValueToMulti(self.value) if is_multi else self.value
        max_value = self.value_per_level * self.max_level
        max_value = ValueToMulti(max_value) if is_multi else max_value
        bonus = f"{round_and_trim(value)}/{round_and_trim(max_value)}"
        description = self._template.replace('{', bonus).replace('}', bonus)
        label += f"{self.name}:<br>{description}"
        return Advice(
            label=label,
            picture_class=(
                f"spelunking-shop-upgrade-{self.index}"
                if self.index in shop_upgrade_image_indexes else "placeholder"
            ),
            progression=self.level,
            goal=self.max_level,
        )


class Spelunk:
    def __init__(self, raw_data: dict):
        spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        raw_cave_state: list[int] = safer_index(spelunk_info, 0, [])
        if not raw_cave_state:
            logger.warning("Spelunk Cave data not present.")
        self.caves: dict[str, SpelunkCave] = {}
        for index, cave_info in enumerate(spelunking_cave_list):
            cave_state = safer_index(raw_cave_state, index, 0)
            cave = SpelunkCave(index, cave_info, cave_state)
            self.caves[cave.name] = cave
        self.lore: dict[str, list[LoreBonus]] = {name: [] for name in chapter_name}
        self._parse_chapter_lore(spelunk_info)
        # "Spelunk[5]" in source. Last updated in v2.531.0
        raw_shop_levels: list = safer_index(spelunk_info, 5, [])
        self.shop: dict[str, SpelunkShopUpgrade] = {}
        for index, info in enumerate(spelunk_shop_upgrades):
            level = safer_convert(safer_index(raw_shop_levels, index, 0), 0)
            upgrade = SpelunkShopUpgrade(index, info, level)
            self.shop[upgrade.name] = upgrade
        # "Spelunk[4][3]" in source: exalts found. Last updated in v2.531.0
        raw_exalts = safer_index(spelunk_info, 4, [])
        self.exalt_stamp_bonus = round(
            safer_convert(safer_index(raw_exalts, 3, 0), 0.0)
        )
        self.super_talent_presets: dict[int, list[list[int]]] = {
            char_index: [
                safer_index(spelunk_info, offset + char_index, []) or []
                for offset in super_talent_preset_offsets
            ]
            for char_index in range(super_talent_preset_slots)
        }

    def get_exalt_stamp_bonus_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Spelunking|#spelunking }}}} - Exalts Found: "
            f"+{round_and_trim(self.exalt_stamp_bonus)}%",
            picture_class="spelunking",
        )

    def get_super_talents(self, char_index: int, preset: int) -> set[int]:
        presets = self.super_talent_presets.get(char_index, [])
        return set(safer_index(presets, preset, []))

    def has_super_talent(self, char_index: int, talent_index: int) -> bool:
        return any(
            talent_index in preset
            for preset in self.super_talent_presets.get(char_index, [])
        )

    def _parse_chapter_lore(self, spelunk_info: list):
        raw_chapter_bonus_level: list[int] = safer_index(spelunk_info, 8, [])
        for index, chapter in enumerate(spelunk_chapters):
            name = chapter_name[index]
            for bonus_index, info in enumerate(chapter):
                level_index = index * 4 + bonus_index
                bonus_level = safer_index(raw_chapter_bonus_level, level_index, 0)
                lore_bonus = LoreBonus(index, level_index, info, bonus_level)
                self.lore[name].append(lore_bonus)

    def calculate_lore_bonus(self, artifact):
        # "ChapterBonus" in source. Last upgrade 2.48 Giftmas Event
        self.lore_multi = ValueToMulti(30 * artifact["Level"])
        for chapter_bonuses in self.lore.values():
            for bonus in chapter_bonuses:
                bonus.calculate_bonus(self.lore_multi)
