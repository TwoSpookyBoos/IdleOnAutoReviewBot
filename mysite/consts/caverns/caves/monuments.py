from consts.idleon.caverns.cavern import HolesInfo
from utils.logging import get_logger

logger = get_logger(__name__)

monument_hours = [
    int(h) for h in HolesInfo[30]
]  # [1, 80, 300, 750, 2000, 5000, 10000, 24000] as of 2.31
monument_names = [f"{monument_name} Monument" for monument_name in HolesInfo[41]]
# Don't increase this without implementing a parse in models first
released_monuments = 3

monument_layer_rewards = {
    monument_names[0]: {
        monument_hours[0]: {
            "Description": "Story Minigame unlocked with 3 Swords",
            "Image": "monument-basic-sword",
        },
        monument_hours[1]: {
            "Description": "+2 additional Swords",
            "Image": "monument-basic-sword",
        },
        monument_hours[2]: {
            "Description": "You can Re-Throw 5 swords per story",
            "Image": "engineer-schematic-40",
        },
        monument_hours[3]: {
            "Description": "+1 additional Sword",
            "Image": "monument-basic-sword",
        },
        monument_hours[4]: {
            "Description": "You get 1 Retelling per story",
            "Image": "measurement-1",
        },
        monument_hours[5]: {
            "Description": "+1 additional Sword",
            "Image": "monument-basic-sword",
        },
        monument_hours[6]: {
            "Description": "+10 Re-Throws per story",
            "Image": "engineer-schematic-40",
        },
        monument_hours[7]: {
            "Description": "+1 additional Sword",
            "Image": "monument-basic-sword",
        },
    },
    monument_names[1]: {
        monument_hours[0]: {
            "Description": "Story Minigame unlocked with Coins",
            "Image": "justice-coin-1",
        },
        monument_hours[1]: {
            "Description": "Start with +1 Mental Health",
            "Image": "justice-currency-2",
        },
        monument_hours[2]: {
            "Description": "You can dismiss 1 case per story",
            "Image": "justice-currency-5",
        },
        monument_hours[3]: {
            "Description": "Start with 1.5x more Coins",
            "Image": "justice-coin-2",
        },
        monument_hours[4]: {
            "Description": "+1 Mental Health and Dismissal",
            "Image": "justice-currency-6",
        },
        monument_hours[5]: {
            "Description": "Start with +7 Popularity",
            "Image": "justice-currency-4",
        },
        monument_hours[6]: {
            "Description": "Start with 3x more Coins",
            "Image": "justice-coin-3",
        },
        monument_hours[7]: {
            "Description": "+2 Mental Health and Dismissals",
            "Image": "justice-currency-6",
        },
    },
    monument_names[2]: {
        monument_hours[0]: {
            "Description": "Start with # Attempts",
            "Image": "wisdom-attempts",
        },
        monument_hours[1]: {
            "Description": "Get +2 Attempts per Board Clear",
            "Image": "wisdom-attempts",
        },
        monument_hours[2]: {
            "Description": "1st attempt each Board reveals row",
            "Image": "wisdom-row",
        },
        monument_hours[3]: {
            "Description": "Start with 4 Insta Matches per story",
            "Image": "wisdom-instamatch",
        },
        monument_hours[4]: {
            "Description": "+4 additional Starting Attempts",
            "Image": "wisdom-attempts",
        },
        monument_hours[5]: {
            "Description": "4th attempt each Board reveals square",
            "Image": "wisdom-square",
        },
        monument_hours[6]: {
            "Description": "Get +1 Attempts per Board Clear",
            "Image": "wisdom-attempts",
        },
        monument_hours[7]: {
            "Description": "+5 additional Insta Matches",
            "Image": "wisdom-instamatch",
        },
    },
}

monument_bonuses_clean_descriptions = [
    d.replace("|", " ").replace("_", " ") for d in HolesInfo[32]
]
monument_bonuses_scaling = [int(v) for v in HolesInfo[37]]
monument_bonuses = {
    monument_names[entry]: {} for entry in range(0, released_monuments + 1)
}

# Layer rewards are in HolesInfo[31], but I wanted to clean up the display a bit
justice_monument_currencies = ["Mental Health", "Coins", "Popularity", "Dismissals"]
for i in range(
    0, 10 * released_monuments
):  # Final number is excluded in range. 10 per released monument
    monument_name = monument_names[i // 10]
    image_prefix = monument_name.lower().replace(" ", "-").replace("-monument", "")
    try:
        monument_bonuses[monument_name][i] = {
            "Description": monument_bonuses_clean_descriptions[i],
            "ScalingValue": monument_bonuses_scaling[i],
            "ValueType": (
                "Percent"
                if "{" in monument_bonuses_clean_descriptions[i]
                else "Multi"
                if "}" in monument_bonuses_clean_descriptions[i]
                else "Flat"
            ),
            "Image": f"{image_prefix}-bonus-{i}",
        }
    except Exception as e:
        logger.exception(f"Couldn't parse {monument_name} bonus {i}: {e}")
        continue
