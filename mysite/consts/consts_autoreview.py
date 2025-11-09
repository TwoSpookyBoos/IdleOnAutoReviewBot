import yaml
from enum import Enum
from pathlib import Path
from utils.logging import get_logger
from config import app

logger = get_logger(__name__)

with open(Path(app.static_folder) / 'items.yaml', 'r') as f:
    items_codes_and_names = yaml.load(f, yaml.Loader)

###UI CONSTS###
#If you add a new switch here, you need to also add a default in \static\scripts\main.js:defaults
switches = [
    {
        "label": "Autoloot purchased",
        "name": "autoloot",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Rift Slug acquired",
        "name": "riftslug",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Doot acquired",
        "name": "doot",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Sheepie acquired",
        "name": "sheepie",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Order groups by tier",
        "name": "order_tiers",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Group Library by Character",
        "name": "library_group_characters",
        "true": "",
        "false": "",
        "static": "true",
    },
    # {
    #     "label": "Display 1 tier at a time",
    #     "name": "single_tier",
    #     "true": "",
    #     "false": "",
    #     "static": "true",
    # },
    {
        "label": "Display lowest rated sections only",
        "name": "hide_overwhelming",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Hide Optional Tiered Sections",
        "name": "hide_optional",
        "true": "",
        "false": "",
        "static": "false",
    },{
        "label": "Hide Completed",
        "name": "hide_completed",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Hide Pure-Info",
        "name": "hide_informational",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Hide Unrated Sections",
        "name": "hide_unrated",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Show progress bars",
        "name": "progress_bars",
        "true": "",
        "false": "",
        "static": "false",
    },
    {
        "label": "Use tabbed advice groups where possible",
        "name": "tabbed_advice_groups",
        "true": "",
        "false": "",
        "static": "true",
    },
    {
        "label": "Handedness",
        "name": "handedness",
        "true": "L",
        "false": "R",
        "static": "false",
    },
    # {"label": "Legacy style", "name": "legacy", "true": "", "false": ""},
]

###AutoReview consts###
class AdviceType(Enum):
    INFO = 'Info'
    OPT = 'Optional'
    COMP = 'Completed'
    OVR = 'Overwhelming'


class EmojiType(Enum):
    NO = '❌'
    STOP = '🛑'
    WARNING = '⚠️'
    CHECK = '✔️'
    TADA = '🎉'
    HEART = '❤️'
    HEARTBROKEN = '💔'
    HAPPY = '😄'
    FROWN = '🙁'
    WIDE_SHRUG = "¯\\_(ツ)_/¯"
    PRAY = '🙏'
    THUMBSUP = '👍'
    EYEROLL = '🙄'
    INFINITY = '∞'


break_you_best = f'<br>You best {EmojiType.HEART.value}'
break_you_bestest = f'<br>You bestest {EmojiType.HEART.value}'
break_keep_it_up = f"<br>Keep it up! You're on the right track! {EmojiType.HEART.value}"

versions_patches = {
    0: "Unknown",
    190: "v1.92 Falloween Event",  #This should have been the last version number before w6
    211: "v2.07 Rift Expansion",
    217: "v2.10 The Owl",
    218: "v2.11 The Roo",
    219: "v2.12 Land Ranks",
    220: "v2.13 Bonus Ballot",
    221: "v2.14 Summer Break",
    230: "v2.20 The Caverns Below",
    231: "v2.21 Endless Summoning",
    232: "v2.22 The Fixening",
    233: "v2.23 Justice Monument",
    234: "v2.24 Giftmas Event / v2.25 Saveload TD",
    236: "v2.26 Death Bringer Class",
    237: "v2.27 Upgrade Vault",
    241: "v2.28 Valenslimes Event",
    242: "v2.29 Upgrade Vault 2",
    243: "v2.30 Companion Trading",
    248: "v2.31 Caverns Biome 3",
    251: "v2.32 Gambit",
    255: "v2.34 Wisdom Monument",
    262: "v2.35 4th Anniversary Event",
    264: "v2.35 Wind Walker Class",
    265: "v2.36 Charred Bones",
    267: "v2.37 Emperor Boss",
    # TODO: some are missing here
    279: "v2.41 Summoning Bosses",
    297: "v2.43 World 7"
}
ignorable_labels: tuple = ('Weekly Ballot',)

###AutoReview Functions###
def ceilUpToBase(inputValue: int, base: int) -> int:
    toReturn = base
    while toReturn <= inputValue:
        toReturn += base
    return toReturn

def ValueToMulti(value: float, min_value=1.0):
    return max(min_value, 1 + (value / 100))

def MultiToValue(multi: float, min_value=0.0):
    return max(min_value, (multi - 1) * 100)

def build_subgroup_label(tier_number, max_tier, pre='', post=''):
    try:
        optional_note = f"{AdviceType.OPT.value} " if tier_number > max_tier else ''
    except:
        logger.exception(f"Failed to compare {tier_number} >= {max_tier} to determine Optional status")
        optional_note = ''
    pre_note = f'{pre} to' if pre else 'To'
    post_note = f' ({post})' if post else ''
    final = f"{pre_note} reach {optional_note}Tier {tier_number}{post_note}"
    return final
