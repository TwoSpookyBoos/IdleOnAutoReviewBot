# Critter unlock quests, highest critter first. Honker unlocks once its quest starts
critter_unlock_quests = (
    ("Blobbo2", 1),
    ("Lord_of_the_Hunt10", 0),
    ("Lord_of_the_Hunt9", 0),
    ("Lord_of_the_Hunt8", 0),
    ("Lord_of_the_Hunt7", 0),
    ("Lord_of_the_Hunt6", 0),
    ("Lord_of_the_Hunt5", 0),
    ("Lord_of_the_Hunt4", 0),
    ("Lord_of_the_Hunt3", 0),
    ("Lord_of_the_Hunt2", 0),
)
# Critter each quest above unlocks, then none
critters_by_unlock = (
    "Blobfish",
    "Honker",
    "Dung Beat",
    "Bunny",
    "Pingy",
    "Owlio",
    "Mousey",
    "Scorpie",
    "Crabbo",
    "Froge",
    "None",
)
# Critter after each entry above
next_critters_by_unlock = (
    "Tuttle",
    "Blobfish",
    "Honker",
    "Dung Beat",
    "Bunny",
    "Pingy",
    "Owlio",
    "Mousey",
    "Scorpie",
    "Crabbo",
    "Froge",
    "None",
)
# Tuttles come from the Jade Emporium
emporium_critters_unlocked = 12

# Trapping level to wear each trap set, by trap set index
trapset_level_requirements = (1, 5, 15, 25, 35, 40, 48)
# Placeable traps by the trap set's level requirement, highest first
trap_slots_by_level = ((48, 7), (40, 6), (35, 5), (25, 4), (15, 3), (5, 2), (1, 1))
nature_trapset_index = 3
