from functools import cached_property
from math import floor

from consts.consts_w3 import (
    apoc_amounts_list,
    apoc_names_list,
    apocable_map_index_dict,
    dn_miniboss_names,
    dn_miniboss_skull_requirement_list,
    dn_skull_value_list,
    getSkullNames,
)
from models.general.enemies import EnemyMap, EnemyWorld, buildMaps
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index

logger = get_logger(__name__)


class Miniboss:
    def __init__(self, name: str, kill_count: int):
        self.name: str = name
        self.kill_count: int = kill_count
        self.kills_to_next_skull: int = 0
        self.percent_toward_next_skull: int = 100
        skull_index = 0
        for requirement_index, skull_requirement in enumerate(dn_miniboss_skull_requirement_list):
            if kill_count >= skull_requirement:
                skull_index = requirement_index
            elif self.kills_to_next_skull == 0:
                self.kills_to_next_skull = skull_requirement - kill_count
                self.percent_toward_next_skull = floor(round(100 * kill_count / skull_requirement))
        self.skull_mk_value: int = safer_index(dn_skull_value_list, skull_index, 0)
        self.skull_name: str = getSkullNames(self.skull_mk_value)

    def __str__(self):
        return self.name


class Minibosses(dict[str, Miniboss]):
    """Death Note miniboss kills, keyed by miniboss name."""

    def __init__(self, raw_data: dict):
        super().__init__()
        raw_ninja = safe_loads(raw_data.get('Ninja', []))
        raw_kills = safer_index(raw_ninja, 105, [0] * len(dn_miniboss_names))
        for mb_index, mb_name in enumerate(dn_miniboss_names):
            try:
                kill_count = safer_convert(safer_index(raw_kills, mb_index, 0), 0)
            except Exception:
                logger.warning(f"Unable to parse Miniboss Deathnote killcount for {mb_name} in index {mb_index}: {raw_kills}. Setting to the default of 0.")
                kill_count = 0
            self[mb_name] = Miniboss(mb_name, kill_count)

    @cached_property
    def total_mk(self) -> int:
        return sum(miniboss.skull_mk_value for miniboss in self.values())


class DeathNote:
    """Kill counts and skull tiers for every apocable map, plus Barbarian Apocalypse progress."""

    def __init__(self, raw_data: dict):
        self.maps: dict[int, dict[int, EnemyMap]] = buildMaps()
        self.worlds: dict[int, EnemyWorld] = {}
        self.minibosses: Minibosses = Minibosses(raw_data)
        self.apoc_character_indexes: list[int] = []
        self.bb_character_indexes: list[int] = []
        self.apocalypse_character_index: int | None = None
        self.rift_meowed: bool = False

    def calculate_apocalypse_characters(self, barbs: list, bbs: list):
        self.apoc_character_indexes = [c.character_index for c in barbs]
        self.bb_character_indexes = [c.character_index for c in bbs]
        # Super CHOW/WOW tracks on the LAST Blood Berserker/Death Bringer in the roster, not the 2nd
        self.apocalypse_character_index = self.bb_character_indexes[-1] if self.bb_character_indexes else None

    def calculate_kills(self, all_characters: list):
        # total up all kills across characters
        for characterIndex, characterData in enumerate(all_characters):
            characterKillsDict = characterData.kill_dict

            # If the character's subclass is Barbarian, add their special Apoc-Only kills to EnemyMap's zow_dict
            if characterIndex in self.apoc_character_indexes:
                for worldIndex in range(0, len(apocable_map_index_dict)):
                    for mapIndex in apocable_map_index_dict[worldIndex]:
                        try:
                            self.maps[worldIndex][mapIndex].updateZOWDict(characterIndex, characterKillsDict.get(mapIndex, [0])[0])
                        except:
                            self.maps[worldIndex][mapIndex].updateZOWDict(characterIndex, 0)

            # Regardless of class, for each map within each world, add this player's kills to EnemyMap's kill_count
            for worldIndex in range(1, len(apocable_map_index_dict)):
                for mapIndex in apocable_map_index_dict[worldIndex]:
                    try:
                        self.maps[worldIndex][mapIndex].addRawKLA(characterKillsDict.get(mapIndex, [0])[0])
                    except:
                        self.maps[worldIndex][mapIndex].addRawKLA(0)

        # Have each EnemyMap calculate its Skull Value, Name, Count to Next, and Percent to Next now that all kills are totaled
        # Barbarian Only in worldIndex 0
        for worldIndex in range(1, len(self.maps)):
            for enemy_map in self.maps[worldIndex]:
                self.maps[worldIndex][enemy_map].generateDNSkull()
            # After each Map in that World has its Skull Info, create the corresponding EnemyWorld
            self.worlds[worldIndex] = EnemyWorld(worldIndex, self.maps[worldIndex])

        # Barbarian Only in 0
        for barbCharacterIndex in self.apoc_character_indexes:
            for worldIndex in range(0, len(self.maps)):
                for enemy_map in self.maps[worldIndex]:
                    if barbCharacterIndex in self.maps[worldIndex][enemy_map].zow_dict:
                        kill_count = self.maps[worldIndex][enemy_map].zow_dict[barbCharacterIndex]
                        for apoc_index, apoc_amount in enumerate(apoc_amounts_list):
                            if (
                                kill_count < apoc_amount  #normal trigger for not meeting the apocalypse amount
                                or apoc_index+1 == len(apoc_amounts_list)  #secondary trigger to make sure every map shows up in Unfiltered
                            ):
                                all_characters[barbCharacterIndex].addUnmetApoc(
                                    apoc_names_list[apoc_index],
                                    self.maps[worldIndex][enemy_map].getRating(apoc_names_list[apoc_index]),
                                    [
                                        self.maps[worldIndex][enemy_map].map_name,  # map name
                                        apoc_amount - kill_count if apoc_index < len(apoc_amounts_list) - 1 else kill_count,  # kills short of Apoc stack
                                        # Note: The final entry in apoc_amounts_list is a placeholder used for the unfiltered display with no goal
                                        min(99, floor(round((kill_count / apoc_amount) * 100))),  # percent toward Apoc stack
                                        self.maps[worldIndex][enemy_map].monster_image,  # monster image
                                        worldIndex,
                                        self.maps[worldIndex][enemy_map].monster_name
                                    ]
                                )
                            else:
                                all_characters[barbCharacterIndex].increaseApocTotal(apoc_names_list[apoc_index])
                    else:
                        # This condition can be hit when reviewing data from before a World release
                        # For example, JSON data from w5 before w6 is released hits this to populate 0% toward W6 kills
                        # If you get this right after a new world, check that the new world and map indexes are added in consts_w3.apocable_map_index_dict
                        logger.debug(f"barbCharacterIndex {barbCharacterIndex} not in DeathNote.maps[{worldIndex}][{enemy_map}].zow_dict")
                        for apoc_index, apoc_amount in enumerate(apoc_amounts_list):
                            all_characters[barbCharacterIndex].addUnmetApoc(
                                apoc_names_list[apoc_index],
                                self.maps[worldIndex][enemy_map].getRating(apoc_names_list[apoc_index]),
                                [
                                    self.maps[worldIndex][enemy_map].map_name,  # map name
                                    apoc_amounts_list[apoc_index],  # kills short of zow/chow/meow
                                    0,  # percent toward zow/chow/meow
                                    self.maps[worldIndex][enemy_map].monster_image,  # monster image
                                    worldIndex,
                                    self.maps[worldIndex][enemy_map].monster_name
                                ]
                            )
            # Sort them
            all_characters[barbCharacterIndex].sortApocByProgression()

    def calculate_rift_meowed(self, all_characters: list):
        if self.apocalypse_character_index is None:
            return
        remaining_maps = all_characters[self.apocalypse_character_index].apoc_dict['MEOW']['Medium Extras']
        self.rift_meowed = not any(remaining_map[0] == 'The Rift' for remaining_map in remaining_maps)
