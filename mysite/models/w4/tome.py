from functools import cached_property
from math import ceil, floor, log

from consts.consts_w4 import tomepct
from consts.idleon.consts_idleon import (
    DeathNoteMobs,
    NinjaInfo,
    RANDOlist,
    SceneNPCquestOrder,
)
from consts.idleon.lava_func import lava_func
from consts.idleon.w1.upgrade_vault import UpgradeVault
from consts.idleon.w7.sushi_station import sushi_max_tier
from consts.w4.tome import (
    tome_breeding_species,
    tome_card_requirements,
    tome_challenge_details,
    tome_deathnote_maps,
    tome_live_talent_max_index,
    tome_star_shiny_per_level,
    tome_star_shiny_pets,
    tome_star_talent_indexes,
)
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_index, safer_math_pow
from utils.text_formatting import numberToLetter


def _num(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0


def _dig(data, *path, default=0):
    for key in path:
        try:
            data = data[key]
        except (IndexError, KeyError, TypeError):
            return default
    return default if data is None else data


def _values(data) -> list:
    data = safe_loads(data)
    if isinstance(data, dict):
        return [value for key, value in data.items() if key != 'length']
    return data if isinstance(data, list) else []


def _js_round(value: float) -> int:
    return floor(value + 0.5)


# `_customBlock_getLOG` in source. Last updated in v2.531.0
def _log(value: float) -> float:
    return log(max(value, 1)) / 2.30259


# "SpecialPassives" in `_customBlock_Breeding`. Last updated in v2.531.0
def _shiny_level(progress: float) -> int:
    return max([1] + [
        tier + 2 for tier in range(19)
        if progress > floor((1 + (tier + 1) ** 1.6) * 1.7 ** (tier + 1))
    ])


# "TalentBannedforAllLV" in source. Last updated in v2.531.0
def _star_talent_level(talent: int, level: float, bonus_levels: float) -> float:
    return 0 if level <= 0 else level + (0 if talent > 614 else bonus_levels)


class TomeChallenge:
    def __init__(self, details: dict, quantity: float, account_level: float):
        self.name: str = details['Name']
        self.target: float = details['Target']
        self.type: int = details['Type']
        self.max_points: int = details['Max Points']
        self.level_required: int = details['Level Required']
        self.quantity: float = quantity
        self.unlocked: bool = account_level >= self.level_required

    # "TomePCT" in `_customBlock_Summoning`. Last updated in v2.531.0
    @cached_property
    def percent(self) -> float:
        if not self.unlocked:
            return 0
        qty, target = self.quantity, self.target
        match self.type:
            case 0:
                return 0 if qty < 0 else (1.7 * qty / (qty + target)) ** 0.7
            case 1:
                return 2.4 * _log(qty) / (2 * _log(qty) + target)
            case 2:
                return min(1, qty / target)
            case 3:
                if qty > 5 * target:
                    return 0
                return (1.2 * (6 * target - qty) / (7 * target - qty)) ** 5
            case 4:
                capped = max(0, min(target, qty))
                return (2 * capped / (capped + target)) ** 0.7
        return 0

    @cached_property
    def points(self) -> int:
        return ceil(self.percent * self.max_points)


class Tome(list[TomeChallenge]):
    def __init__(self, raw_data: dict):
        quantities, self._talent_maxes, self._star_characters, self._star_account = (
            _get_quantities(raw_data)
        )
        self._account_level: float = quantities[5]
        cauldrons = safe_loads(raw_data.get('CauldronInfo', []))
        self._live_talent_bubble: float = _num(
            _dig(_values(_dig(cauldrons, 3, default={})), 5)
        )
        options = safe_loads(raw_data.get('OptLacc', []))
        self.blue_pages_unlocked: bool = bool(_num(safer_index(options, 196, 0)))
        self.red_pages_unlocked: bool = bool(_num(safer_index(options, 197, 0)))
        self._rank_scores = raw_data.get('serverVars', {}).get('TomePct')
        self.score: int = 0
        self.percent: float = 100
        self.drop_rate_bonus: float = 0
        super().__init__(
            TomeChallenge(details, quantities[index], self._account_level)
            for index, details in enumerate(tome_challenge_details)
        )

    # "TotalTalentPoints" in source. Last updated in v2.531.0
    def calculate_live_talent_max(self, buncha_banana_bonus: float):
        live_max = floor(max(1, self._live_talent_bubble + buncha_banana_bonus))
        self._talent_maxes[tome_live_talent_max_index] = max(
            self._talent_maxes.get(tome_live_talent_max_index, 0), live_max
        )
        self[3] = TomeChallenge(
            tome_challenge_details[3],
            sum(self._talent_maxes.values()),
            self._account_level,
        )

    # "TotalTalentPoints" in source. Last updated in v2.531.0
    def calculate_star_talents(
        self, bonus_talent_levels: dict[int, float], account_bonus: float
    ):
        best = 0
        # the game scores whoever is logged in
        for character_index, character in enumerate(self._star_characters):
            bonus_levels = bonus_talent_levels.get(character_index, 0)
            levels = {
                talent: _star_talent_level(talent, level, bonus_levels)
                for talent, level in character['Talents'].items()
            }
            total = (
                character['Base'] + _js_round(levels[275]) + levels[8] + levels[17]
                + lava_func('decay', levels[622], 130, 50)
                + self._star_account + account_bonus
            )
            best = max(best, floor(total))
        self[15] = TomeChallenge(tome_challenge_details[15], best, self._account_level)

    @property
    def total_points(self) -> int:
        return sum(challenge.points for challenge in self)

    def calculate_score(self, manual_score: int | None):
        self.score = self.total_points if manual_score is None else manual_score
        # serverVars ranks live, the consts are the fallback
        live_scores = sorted(self._rank_scores or [])
        for index, percent in enumerate(tomepct):
            score = (
                safer_index(live_scores, index, 99999) if live_scores
                else tomepct[percent]
            )
            if self.score > score:
                self.percent = min(self.percent, percent)

    # "TomeBonus" 2 in `_customBlock_Summoning`. Last updated in v2.531.0
    def calculate_bonuses(self, bonus_multi: float):
        self.drop_rate_bonus = (
            self.red_pages_unlocked
            * 2
            * safer_math_pow(floor(max(0, self.score - 8000) / 100), 0.7)
            * bonus_multi
        )

    def get_bonus_advice(self) -> Advice:
        return Advice(
            label=f"Tome- Red Pages:"
                  f"<br>+{round(self.drop_rate_bonus, 1):g}% Drop Rate"
                  f"<br>{self.score:,} Total Tome Points"
                  f"<br>Increases every 100 points over 8000",
            picture_class='red-tome-pages',
            progression=int(self.red_pages_unlocked),
            goal=1
        )


# `_customEvent_TomeQTY` in source. Last updated in v2.531.0
def _get_quantities(
    raw_data: dict,
) -> tuple[list[float], dict[str, float], list[dict], float]:
    def get(key: str, default):
        value = safe_loads(raw_data.get(key, default))
        return default if value is None else value

    character_count = 0
    while f'Lv0_{character_count}' in raw_data:
        character_count += 1

    def per_character(key: str, default) -> list:
        return [get(f'{key}_{index}', default) for index in range(character_count)]

    options = get('OptLacc', [])

    def opt(index: int) -> float:
        return _num(_dig(options, index))

    levels = per_character('Lv0', [])
    cards = get('Cards0', {})
    found_items = [str(item) for item in get('Cards1', [])]
    achievements = get('AchieveReg', [])
    rift = get('Rift', [])
    spelunk = get('Spelunk', [])
    ninja = get('Ninja', [])
    summon = get('Summon', [])
    holes = get('Holes', [])
    research = get('Research', [])
    breeding = get('Breeding', [])
    sailing = get('Sailing', [])
    gaming = get('Gaming', [])
    sprouts = get('GamingSprout', [])
    royal = get('RoyalG', [])
    cauldrons = get('CauldronInfo', [])
    vault = get('UpgVault', [])

    card_tiers = 4 + (_num(_dig(rift, 0)) >= 45) + (_num(_dig(spelunk, 0, 2)) >= 1)
    six_star_cards = str(_dig(options, 603)).split(',')
    five_star_cards = str(_dig(options, 155)).split(',')

    # "CardLv" in `_customBlock_RunCodeOfTypeXforThingY`. Last updated in v2.531.0
    def card_level(name: str) -> int:
        count = _num(cards.get(name, 0))
        level = 1 if count > 0 else 0
        for star in range(card_tiers):
            if name == 'Boss3B':
                required = 1.5 * (star + 1 + star // 3) ** 2
            else:
                required = tome_card_requirements.get(name, 0) * (
                    star + 1 + star // 3 + 16 * (star // 4) + 100 * (star // 5)
                ) ** 2
            if count > required:
                level = star + 2
        if name in six_star_cards and level < 7:
            return 7
        if name in five_star_cards and level < 6:
            return 6
        return level

    def achieved(index: int) -> bool:
        return _num(_dig(achievements, index)) == -1

    def vault_bonus(index: int) -> float:
        return _num(_dig(vault, index)) * _num(UpgradeVault[index][5])

    q = [0.0] * len(tome_challenge_details)

    q[0] = sum(
        _num(level)
        for stamp_type in _values(get('StampLv', []))
        for level in _values(stamp_type)
    )
    q[1] = max(
        (
            sum(_num(_dig(statue, 0)) for statue in statues)
            for statues in per_character('StatueLevels', [])
        ),
        default=0
    )
    q[2] = sum(card_level(name) for name in cards if name in tome_card_requirements)
    talent_maxes = per_character('SM', {})
    best_talent_maxes = {
        talent: max(
            [0] + [_num(char_maxes.get(talent, 0)) for char_maxes in talent_maxes]
        )
        for talent in {
            talent for char_maxes in talent_maxes
            for talent in char_maxes if talent != 'length'
        }
    }
    q[3] = sum(best_talent_maxes.values())
    completed_quests = per_character('QuestComplete', {})
    q[4] = sum(
        any(_num(char_quests.get(quest, 0)) == 1 for char_quests in completed_quests)
        for quest in SceneNPCquestOrder
    )
    q[5] = sum(_num(_dig(char_levels, 0)) for char_levels in levels)
    q[6] = sum(_num(_dig(row, task)) for row in get('TaskZZ1', []) for task in range(8))
    q[7] = sum(_num(achievement) == -1 for achievement in achievements)
    q[8] = max(opt(198), _num(get('MoneyBANK', 0)))
    q[9] = opt(208)
    q[10] = sum(item.startswith('Trophy') for item in found_items)
    q[11] = sum(
        max(0, _num(_dig(char_levels, skill)))
        for char_levels in levels for skill in range(1, 22)
    )
    q[12] = opt(201)
    q[13] = _num(_dig(get('TaskZZ0', []), 0, 2))
    q[14] = opt(172)

    # "TotalTalentPoints" in source. Last updated in v2.531.0
    star_characters = [
        {
            'Base': (
                _num(_dig(char_levels, 0)) - 1
                + sum(_num(_dig(char_levels, skill)) for skill in range(1, 10)) - 3
            ),
            'Talents': {
                talent: _num(char_talents.get(str(talent), 0))
                for talent in tome_star_talent_indexes
            },
        }
        for char_levels, char_talents in zip(levels, per_character('SL', {}))
    ]
    star_shiny = sum(
        _js_round(
            _shiny_level(_num(_dig(breeding, world + 22, index)))
            * tome_star_shiny_per_level
        )
        for world, index in tome_star_shiny_pets
        if _num(_dig(breeding, world + 22, index)) > 0
    )
    star_account = (
        _num(_dig(get('CYTalentPoints', []), 5))
        + min(5 * card_level('w4b2'), 50)
        + min(15 * card_level('Boss2C'), 100)
        + min(4 * card_level('fallEvent1'), 100)
        + 10 * achieved(212) + 20 * achieved(289) + 20 * achieved(305)
        + vault_bonus(53)
        + star_shiny
        + _num(_dig(get('DungUpg', []), 5, 1))  # Flurbo Shop
        + 100 * (opt(184) >= 20000)  # Fractal Island
    )
    q[15] = max(
        (floor(character['Base'] + star_account) for character in star_characters),
        default=0
    )
    q[16] = 1 / opt(202) if opt(202) else float('inf')
    dungeon_exp = opt(71)
    q[17] = next(
        (rank for rank, exp in enumerate(RANDOlist[29]) if dungeon_exp < _num(exp)), 1
    )
    q[18] = opt(200)
    q[19] = sum(_num(_dig(sign, 1)) == 1 for sign in get('SSprog', []))
    q[20] = opt(203)
    q[21] = sum(item.startswith('Obol') for item in found_items)
    q[22] = sum(
        _num(level)
        for cauldron in range(4)
        for level in _values(_dig(cauldrons, cauldron, default={}))
    )
    q[23] = sum(_num(level) for level in _values(_dig(cauldrons, 4, default={})))
    sigils = _dig(get('CauldronP2W', []), 4, default=[])
    q[24] = sum(
        _num(_dig(sigils, 1 + 2 * sigil)) + 1 for sigil in range(ceil(len(sigils) / 2))
    )
    q[25] = opt(199)
    q[26] = sum(
        _js_round(_num(get(f'CYDeliveryBox{box}', 0)))
        for box in ['Complete', 'Streak', 'Misc']
    )
    q[27] = opt(204)
    q[28] = opt(205)
    q[29] = opt(206)
    q[30] = 1000 - opt(207)
    for sample in range(5):
        q[31 + sample] = opt(211 + sample)
    q[36] = opt(209)
    q[37] = sum(_num(wave) for wave in _dig(get('TotemInfo', []), 0, default=[]))

    kills_left = per_character('KLA', [])
    deathnote_digits = sum(
        ceil(_log(sum(
            requirement - _num(_dig(char_kills, map_index, 0, default=requirement))
            for char_kills in kills_left
        )))
        for map_index, requirement in tome_deathnote_maps
    )
    if numberToLetter(7) in str(_dig(ninja, 102, 9, default='')):
        deathnote_digits += sum(
            ceil(_log(_num(_dig(ninja, 105, boss))))
            for boss in range(len(NinjaInfo[30]))
        )
    q[38] = deathnote_digits
    q[39] = sum(
        str(key).startswith('d_') and _num(value) == -1
        for key, value in get('WeeklyBoss', {}).items()
    )
    q[40] = sum(_num(_dig(get('Refinery', []), salt, 1)) for salt in range(3, 9))
    q[41] = sum(_num(atom) for atom in get('Atoms', []))
    q[42] = sum(_num(building) for building in get('Tower', [])[:27])
    chest_order = get('ChestOrder', [])
    q[43] = (
        _num(_dig(get('ChestQuantity', []), chest_order.index('Critter11A')))
        if 'Critter11A' in chest_order else 0
    )
    q[44] = opt(224)
    q[45] = _num(_dig(rift, 0))
    q[46] = max(
        (_num(_dig(pet, 2)) for pet in get('Pets', []) + get('PetsStored', [])),
        default=0
    )
    q[47] = 1000 - opt(220)
    q[48] = sum(
        _num(_dig(get('Cooking', []), table, upgrade))
        for table in range(10) for upgrade in range(6, 9)
    )

    # "SpecialPassives" and "2ndMulti" in `_customBlock_Breeding`. v2.531.0
    shiny_levels = 0
    breedability_levels = 0
    breedability_unlocked = _num(_dig(breeding, 2, 3)) > 0
    for world, index in tome_breeding_species:
        shiny_levels += _shiny_level(_num(_dig(breeding, world + 22, index)))
        breedability_multi = (
            1 + log(max(1, (_num(_dig(breeding, world + 13, index)) + 1) ** 0.725))
            if breedability_unlocked else 1
        )
        breedability_levels += min(9, floor((breedability_multi - 1) ** 0.8) + 1)
    q[49] = shiny_levels
    q[50] = sum(_num(level) for level in _dig(get('Meals', []), 0, default=[]))
    q[51] = breedability_levels
    q[52] = sum(max(0, _num(chip)) for chip in _dig(get('Lab', []), 15, default=[]))
    q[53] = sum(_num(score) for score in get('FamValColosseumHighscores', []))
    q[54] = opt(217)
    q[55] = 0 if opt(69) < 2 else sum(_num(statue) >= 2 for statue in get('StuG', []))
    q[56] = 1000 - opt(218)
    q[57] = sum(_num(_dig(boat, 3)) + _num(_dig(boat, 5)) for boat in get('Boats', []))
    q[58] = max(0, _num(_dig(get('Divinity', []), 25)) - 10)
    q[59] = _num(_dig(sprouts, 28, 1))
    q[60] = sum(_num(artifact) for artifact in _dig(sailing, 3, default=[]))
    q[61] = _num(_dig(sailing, 1, 0))
    q[62] = max(
        (_num(_dig(get('Captains', []), captain, 3)) for captain in range(20)),
        default=0
    )
    q[63] = max(_num(_dig(sprouts, 32, 1)), opt(210))
    q[64] = _num(_dig(gaming, 8))
    q[65] = len(found_items)
    q[66] = _num(_dig(gaming, 0))
    q[67] = 2 ** opt(219)
    q[68] = len(get('FarmCrop', {}))
    q[69] = sum(_num(stack) for stack in _dig(ninja, 104, default=[]))
    q[70] = sum(_num(level) for level in _dig(summon, 0, default=[]))
    q[71] = opt(319) + sum(
        1 if str(win).startswith('Pet')
        else sum(win in world for world in DeathNoteMobs)
        for win in _dig(summon, 1, default=[])
    )
    if opt(232) > 0:
        q[72] = 12 * opt(232)
    else:
        floors = 1
        for door, door_hp in enumerate(NinjaInfo[3]):
            max_hp = 0 if opt(231) < opt(232) else _num(door_hp)
            if max_hp - _num(_dig(ninja, 100, door)) <= 0:
                floors = min(12, door + 2)
        q[72] = floors
    familiars = 0
    slime_value = 1
    for familiar in range(9):
        familiars += slime_value * _num(_dig(summon, 4, familiar))
        slime_value *= familiar + 3
    q[73] = familiars
    q[74] = len(str(_dig(ninja, 102, 9, default='')))
    q[75] = sum(
        _num(_dig(get('FamValMinigameHiscores', []), game)) for game in range(4)
    ) + opt(99)
    q[76] = sum(_num(level) for level in get('PrayOwned', []))
    q[77] = sum(_num(rank) for rank in _dig(get('FarmRank', []), 0, default=[]))
    q[78] = opt(221)
    q[79] = opt(222)
    q[80] = sum(_num(level) for level in get('ArcadeUpg', []))
    q[81] = min(1500, vault_bonus(57))
    q[82] = sum(_num(_dig(holes, 11, index)) for index in range(65, 71))
    q[83] = sum(ceil(_log(_num(resource))) for resource in _dig(holes, 9, default=[]))
    q[84] = sum(_js_round(max(0, _num(level))) for level in _dig(holes, 1, default=[]))
    q[85] = opt(262)
    q[86] = opt(279)
    for monument in range(3):
        q[87 + monument] = _num(_dig(holes, 11, 73 + monument))
    q[90] = opt(356)
    q[91] = _num(_dig(holes, 11, 8))
    q[92] = sum(
        _js_round(max(0, _num(_dig(holes, 11, layer)))) for layer in [1, 3, 5, 7]
    )
    q[93] = sum(_js_round(max(0, _num(opal))) for opal in _dig(holes, 7, default=[]))
    q[94] = _js_round(min(12, opt(353)) + 1)
    q[95] = _js_round(opt(369))
    q[96] = sum(
        _js_round(_num(get('KRbest', {}).get(f'SummzTrz{stone}', 0)))
        for stone in range(9)
    )
    q[97] = sum(_num(_dig(spelunk, 13, upgrade)) for upgrade in range(6))
    q[98] = max((_num(depth) for depth in _dig(spelunk, 1, default=[])), default=0)
    q[99] = sum(_num(level) for level in _dig(ninja, 103, default=[]))
    q[100] = opt(445)
    q[101] = opt(446)
    q[102] = max((_num(haul) for haul in _dig(spelunk, 2, default=[])), default=0)
    q[103] = sum(max(0, _num(level)) for level in _dig(spelunk, 5, default=[]))
    q[104] = len(_dig(spelunk, 6, default=[]))
    q[105] = max((_num(_dig(char_levels, 19)) for char_levels in levels), default=0)
    q[106] = opt(443)
    q[107] = sum(item.startswith('EquipmentNametag') for item in found_items)
    q[108] = _num(_dig(get('Bubba', []), 1, 8))
    q[109] = len(_dig(spelunk, 46, default=[]))
    q[110] = _num(_dig(research, 7, 4))
    q[111] = len(_dig(research, 11, default=[]))
    q[112] = _js_round(sum(_num(sticker) for sticker in _dig(research, 9, default=[])))
    q[113] = opt(498)
    q[114] = _js_round(sum(_num(square) for square in _dig(research, 0, default=[])))
    q[115] = sum(
        _js_round(max(0, _num(trade))) for trade in _dig(research, 12, default=[])
    )
    unique_sushi = 0
    for tier in range(sushi_max_tier + 1):
        if _num(_dig(get('Sushi', []), 5, tier, default=-1)) < 0:
            break
        unique_sushi = tier + 1
    q[116] = unique_sushi
    q[117] = opt(594)
    q[118] = sum(max(0, _num(level)) for level in _dig(royal, 0, default=[]))
    q[119] = sum(len(outpost) >= 3 for outpost in get('RoyalMaps', []))
    q[120] = sum(_num(grade) for grade in _dig(royal, 5, default=[]))
    q[121] = _num(_dig(research, 7, 9))
    return q, best_talent_maxes, star_characters, star_account
