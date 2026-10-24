from consts.consts_general import equipment_by_bonus_dict
from models.advice.advice import Advice
from models.general.assets import Asset
from models.general.character import Character
from utils.logging import get_logger

logger = get_logger(__name__)


def invalid_weapon_type(base_class, slot):
    if base_class == "Warrior":
        return slot in ["Bow", "Wand", "Fisticuffs"]
    elif base_class == "Archer":
        return slot in ["Spear", "Wand", "Fisticuffs"]
    elif base_class == "Mage":
        return slot in ["Spear", "Bow", "Fisticuffs"]
    elif base_class in ["Journeyman", "Beginner"]:
        return slot in ["Spear", "Bow", "Wand"]
    else:
        logger.warning(f"Provided unknown base_class: {base_class}")
    return True


_lab_chip_picture_classes = {
    "silkrode-motherboard",
    "silkrode-software",
    "silkrode-processor",
}


def merge_equipment_advice_by_slot(
    prefixed_equipment_advices: list[tuple[str, dict[str, list[Advice]]]],
) -> dict[str, list[Advice]]:
    """Combine equipment advice dicts keyed by "{prefix}{Slot}" (e.g. "Drop Rate - Trophy",
    "Drop Rate Multi - Trophy") into one dict keyed by bare Slot (e.g. "Trophy"), so a slot that
    shows up under multiple stats gets a single section instead of one per stat.

    Some info rows (e.g. the Silkrode Motherboard chip note) get generated identically by each
    stat's pass, so exact duplicate labels within a slot are dropped. An item that contributes to
    both stats (e.g. Deadbones Nametag, listed under both Drop Rate and Drop Rate Multi) instead
    gets combined into a single row with one bare stat line per stat (e.g. "+35% Drop Rate" /
    "+25% Drop Rate Multi"), dropping each pass's Note since it only existed to cross-reference
    the other stat's value, which is now redundant once both lines are shown directly.
    """
    merged: dict[str, list[Advice]] = {}
    seen_chip_rows_by_slot: dict[str, set[tuple[str, str]]] = {}
    # Per slot, the already-emitted combined row for each (equipment name, occurrence) seen so
    # far - "occurrence" handles Keychains, where the same name can appear twice in one pass
    # (upper/lower slot) without those two rows being merged into each other.
    item_rows_by_slot: dict[str, dict[tuple[str, int], Advice]] = {}

    for prefix, equipment_advice in prefixed_equipment_advices:
        for slot_key, advices in equipment_advice.items():
            slot = slot_key.removeprefix(prefix)
            merged.setdefault(slot, [])
            seen_chip_rows = seen_chip_rows_by_slot.setdefault(slot, set())
            item_rows = item_rows_by_slot.setdefault(slot, {})
            name_occurrence_so_far: dict[str, int] = {}

            for advice in advices:
                if advice.picture_class in _lab_chip_picture_classes:
                    dedupe_key = (advice.label, advice.picture_class)
                    if dedupe_key in seen_chip_rows:
                        continue
                    seen_chip_rows.add(dedupe_key)
                    merged[slot].append(advice)
                    continue

                name = getattr(advice, "equipment_name", None)
                if name is None:
                    # Not a recognized item row - pass through as-is
                    merged[slot].append(advice)
                    continue

                occurrence = name_occurrence_so_far.get(name, 0)
                name_occurrence_so_far[name] = occurrence + 1
                item_key = (name, occurrence)

                existing_row = item_rows.get(item_key)
                if existing_row is not None:
                    # Already have a row for this item from an earlier pass - rebuild the label
                    # from bare stat lines only (dropping both passes' Notes, since those only
                    # cross-referenced the other stat's value, which is redundant once merged).
                    existing_row.stat_lines.append(advice.stat_line)
                    limited_suffix = (
                        " (Limited availability)"
                        if existing_row.equipment_limited
                        else ""
                    )
                    existing_row.label = f"{name}{limited_suffix}:" + "".join(
                        f"<br>{line}" for line in existing_row.stat_lines
                    )
                else:
                    item_rows[item_key] = advice
                    merged[slot].append(advice)
    return merged


def get_equipment_advice_for_stat(
    character: Character,
    stat: str,
    stat_codenames: tuple[str, ...],
    stat_human_readable_format: str,
    advice_group_prefix: str,
    highest_world_reached: int,
):
    equipment_advice: dict[str, list[Advice]] = {}
    equipment_dict: dict[str, list] = {}

    motherboard_equipped = "Silkrode Motherboard" in character.equipped_lab_chips
    software_equipped = "Silkrode Software" in character.equipped_lab_chips
    processor_equipped = "Silkrode Processor" in character.equipped_lab_chips
    motherboard_boosts_gallery = highest_world_reached >= 7
    # Gallery/Hatrack take over these slots once open for this character
    showcased_types = ("Trophy", "Nametag") * character.gallery_bonus_active + (
        "Premium Hat",
    ) * character.hatrack_bonus_active

    if stat == "DropRate":
        # Equipping the chip is per-character even though its effect is account-wide
        equipment_advice.setdefault(advice_group_prefix + "Trophy", []).append(
            Advice(
                label=(
                    "Lab Chips - Silkrode Motherboard<br>+10% Trophy Gallery Bonus Multi"
                    if motherboard_boosts_gallery
                    else "Lab Chips - Silkrode Motherboard<br>Doubles Misc. Bonuses of equipped Trophy"
                ),
                picture_class="silkrode-motherboard",
                progression=int(motherboard_equipped),
                goal=1,
            )
        )

    for equipment_name, equipment_data in equipment_by_bonus_dict[stat].items():
        if equipment_data["Type"] in showcased_types:
            continue
        is_keychain = equipment_data["Type"] == "Keychain"
        misc1 = equipment_data.get("Misc1", {})
        misc2 = equipment_data.get("Misc2", {})
        equipment_drop_rate_base = (
            (misc1.get("Bonus", "") == stat) * misc1.get("Value", 0)
        ) + ((misc2.get("Bonus", "") == stat) * misc2.get("Value", 0))
        equipped_equipment: list[Asset | None] = [
            equipment
            for equipment in character.equipment.equips
            if equipment_name == equipment.name
        ] + [tool for tool in character.equipment.tools if equipment_name == tool.name]
        if not equipped_equipment:
            equipped_equipment = [None]  # So the loop below is executed once
            if is_keychain:
                equipped_equipment = [None, None]  # So the loop below is executed twice
        if len(equipped_equipment) == 1 and is_keychain:
            equipped_equipment.append(None)  # So the loop below is executed twice

        for index, item in enumerate(equipped_equipment):
            equipped_equipment_bonus = 0
            slot = equipment_data.get("Type")
            can_be_boosted = slot in ["Trophy", "Keychain", "Pendant"] and index == 0
            is_boosted = (
                motherboard_equipped
                and slot == "Trophy"
                or software_equipped
                and is_keychain
                and index == 0
                or processor_equipped
                and slot == "Pendant"
            )
            if item is not None:
                # Own misc lines only; chip doubling below, no gown multi
                equipped_equipment_bonus = character.equipment.get_item_misc_bonus(
                    item, stat_codenames
                )
            if is_boosted:
                equipped_equipment_bonus *= 2

            if advice_group_prefix + slot not in equipment_dict:
                equipment_dict[advice_group_prefix + slot] = []

            equipment_dict[advice_group_prefix + slot].append(
                {
                    "Name": equipment_name,
                    "Slot": slot,
                    stat: equipped_equipment_bonus
                    if is_keychain
                    else equipment_drop_rate_base,
                    "Image": equipment_data["Image"],
                    "EquippedAndMaxed": int(
                        (
                            (not is_boosted)
                            and equipped_equipment_bonus >= equipment_drop_rate_base
                        )
                        or (
                            is_boosted
                            and equipped_equipment_bonus >= 2 * equipment_drop_rate_base
                        )
                    ),  # >= because the gem shop can sell items with boosted stats, if you have those you're fine
                    "Limited": equipment_data.get("Limited", False),
                    "Note": equipment_data.get("Note", ""),
                    "Can be boosted": can_be_boosted,
                }
            )

    for slot, equipment_list in equipment_dict.items():
        if invalid_weapon_type(character.base_class, slot[len(advice_group_prefix) :]):
            continue
        if slot not in equipment_advice:
            equipment_advice[slot] = []

        if "Keychain" in slot:
            equipment_advice[slot].append(
                Advice(
                    label="Lab Chips - Silkrode Software"
                    "<br>Doubles Misc. Bonuses of (upper) equipped Keychain",
                    picture_class="silkrode-software",
                    progression=int(software_equipped),
                    goal=1,
                )
            )

        if "Pendant" in slot:
            equipment_advice[slot].append(
                Advice(
                    label="Lab Chips - Silkrode Processor"
                    "<br>Doubles Misc. Bonuses of equipped Pendant",
                    picture_class="silkrode-processor",
                    progression=int(processor_equipped),
                    goal=1,
                )
            )

        for index, equipment in enumerate(equipment_list):
            if (
                motherboard_equipped
                and equipment["Slot"] == "Trophy"
                and equipment["Can be boosted"]
            ):
                equipment[stat] *= 2
                equipment["Note"] += "<br>Boosted by Silkrode Motherboard"
            if (
                software_equipped
                and equipment["Slot"] == "Keychain"
                and equipment["Can be boosted"]
            ):
                # We don't mult by 2 here because it's already handled in the parsing of the "real" stats. Only Keychains have variable Drop Rate so we have to handle it there.
                equipment["Note"] += "<br>Boosted by Silkrode Software"
            if (
                processor_equipped
                and equipment["Slot"] == "Pendant"
                and equipment["Can be boosted"]
            ):
                equipment[stat] *= 2
                equipment["Note"] += "<br>Boosted by Silkrode Processor"

            # stat_line/detail_html are stashed separately so merge_equipment_advice_by_slot can
            # combine an item that contributes to both Drop Rate and Drop Rate Multi (e.g.
            # Deadbones Nametag) into a single row with one bare stat line per stat, instead of
            # two rows each also repeating a now-redundant Note about the other stat's value.
            stat_line = f"+{equipment[stat]}% {stat_human_readable_format}"
            detail_html = f"<br>{stat_line}{'<br>' + equipment['Note'] if equipment['Note'] else ''}"
            item_advice = Advice(
                label=f"{equipment['Name']}{' (Limited availability)' if equipment['Limited'] else ''}:{detail_html}",
                picture_class=equipment["Image"],
                progression=equipment["EquippedAndMaxed"],
                goal=1,
            )
            item_advice.equipment_name = equipment["Name"]
            item_advice.equipment_limited = equipment["Limited"]
            item_advice.stat_line = stat_line
            item_advice.stat_lines = [stat_line]
            item_advice.detail_html = detail_html
            equipment_advice[slot].append(item_advice)
            if (
                equipment["EquippedAndMaxed"]
                and index != len(equipment_list) - 1
                and equipment["Name"] != equipment_list[index + 1]["Name"]
            ):
                # Don't check items that come after the equipped item because they are worse than the equipped item
                break
    return equipment_advice


def get_equipment_advice(
    character: Character,
    flat_codenames: tuple[str, ...],
    multi_codenames: tuple[str, ...],
    highest_world_reached: int,
) -> dict[str, list[Advice]]:
    # One section per slot, flat and multi merged
    return merge_equipment_advice_by_slot(
        [
            (
                "Drop Rate - ",
                get_equipment_advice_for_stat(
                    character,
                    "DropRate",
                    flat_codenames,
                    "Drop Rate",
                    "Drop Rate - ",
                    highest_world_reached,
                ),
            ),
            (
                "Drop Rate Multi - ",
                get_equipment_advice_for_stat(
                    character,
                    "DropRateMulti",
                    multi_codenames,
                    "Drop Rate Multi",
                    "Drop Rate Multi - ",
                    highest_world_reached,
                ),
            ),
        ]
    )
