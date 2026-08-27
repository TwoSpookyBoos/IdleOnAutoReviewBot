from consts.idleon.caverns.cavern import HolesInfo

bell_ring_images = [
    "well-bucket",
    "opal",
    "cavern-6",
    "cavern-7",
    "jar-rupie-0",
    "temple-torch",
]
bell_ring_bonuses = {}
for i in range(0, 6):
    bell_ring_bonuses[i] = {
        "Description": HolesInfo[59][i * 2].replace("|", " ").replace("_", " ").title(),
        "ScalingValue": float(HolesInfo[59][i * 2 + 1]),
        "Image": bell_ring_images[i],
    }

bell_clean_resources = [
    "coins",
    "well-sediment-3",
    "purple-bits",
    "harp-note-4",
    "particles",
    "jar-rupie-5",
]
bell_improvement_stack_multipliers = [float(v) for v in HolesInfo[61]]
bell_clean_improvements = {}
for i in range(0, 6):
    bell_clean_improvements[i] = {
        "Description": HolesInfo[60][i].replace("|", " ").replace("_", " "),
        "Image": (
            "bell-ring"
            if "Ring" in HolesInfo[60][i]
            else "bell-ping"
            if "Ping" in HolesInfo[60][i]
            else "bell-clean"
            if "Clean" in HolesInfo[60][i]
            else ""
        ),
        "Resource": bell_clean_resources[i],
    }
