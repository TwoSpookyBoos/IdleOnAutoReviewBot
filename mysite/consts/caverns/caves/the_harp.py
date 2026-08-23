from consts.idleon.caverns.villager.cosmos import majiks as _cosmos_majiks

schematics_unlocking_harp_strings = [
    "Loaded Harp",
    "Packed Harp",
    "Hefty Harp",
    "Multitudinal Harp",
    "Sumptuous Harp",
]
schematics_unlocking_harp_chords = [
    "Eee String",
    "Eff String",
    "Geez String",
    "Aye String",
    "Bee String",
]
harp_chord_effects = {
    "C": ["Generate the tuned Note", "Harp Note Gain"],
    "D": ["Chance for an Opal", "Harp Note Gain"],
    "E": ["Nothing", "Harp Power/hr"],
    "F": ["Generate the tuned Note and both nearby Notes", "Harp Note Gain"],
    "G": ["Generate EXP for all unlocked Chords", "String EXP Gain"],
    "A": ["Generate every Note you have unlocked", "Harp Note Gain"],
    "B": ["TBD", "TBD"],
}
harp_notes = [
    "Crotchet Note",
    "Natural Note",
    "Bass Note",
    "Treble Note",
    "Eighth Note",
    "Quaver Note",
    "Sharp Note",
    "(F)Clef Note",
    "(G)Clef Note",
    "Sixteenth Note",
]
max_harp_notes = len(harp_notes)

_harp_string_max_level = 1 + next(
    bonus["MaxEnchantLevel"]
    for bonus in _cosmos_majiks[0]
    if bonus["Name"] == "String is Strung"
)
max_harp_strings = 1 + len(schematics_unlocking_harp_strings) + _harp_string_max_level
max_harp_chords = 2 + len(schematics_unlocking_harp_chords)
