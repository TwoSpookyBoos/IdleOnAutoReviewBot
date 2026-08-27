from consts.idleon.caverns.cavern import HolesInfo

cavern_name_overrides = {
    "BRAVERY": "Bravery Monument",
    "JUSTICE": "Justice Monument",
    "WISDOM": "Wisdom Monument",
    "TEMPLE": "The Temple",
    "THE_JARS": "The Jar",
}

cavern_names = {0: "Camp"}
for index, raw_name in enumerate(HolesInfo[68]):
    cavern_names[index + 1] = cavern_name_overrides.get(
        raw_name, raw_name.replace("_", " ").title()
    )
max_cavern = max(cavern_names.keys())


def get_resource_image(resource_number: int) -> str:
    """
    Return string for image of caverns resource.
     0 -  9 -> well ore
    10 - 19 -> harp note
    20 - 29 -> jar rupie
    Example: 12 -> 'harp-note-2'
    """
    prefixes = ("well-sediment", "harp-note", "jar-rupie")
    idx = resource_number // 10
    if 0 <= idx < len(prefixes):
        return f"{prefixes[idx]}-{resource_number % 10}"
    return "placeholder"
