import json
import os
from math import ceil, floor

from config import app
from consts.consts_w3 import dn_skull_value_list, getSkullNames, getNextSkullNames, dn_skull_requirement_list, \
    reversed_dn_skull_value_list, reversed_dn_skull_requirement_list, apocable_map_index_dict


class EnemyWorld:
    def __init__(self, worldnumber: int, mapsdict: dict):
        self.world_number: int = worldnumber
        self.maps_dict: dict = mapsdict
        self.lowest_skulls_dict: dict = {}
        self.lowest_skull_value: int = -1
        self.total_mk = sum(enemy_map.skull_mk_value for enemy_map in mapsdict.values())
        self.current_lowest_skull_name: str = "None"
        self.next_lowest_skull_name: str = "Normal Skull"
        for skullValue in dn_skull_value_list:
            self.lowest_skulls_dict[skullValue] = []
        if len(mapsdict) > 0:
            for enemy_map_index in self.maps_dict:
                self.lowest_skulls_dict[self.maps_dict[enemy_map_index].skull_mk_value].append([
                    self.maps_dict[enemy_map_index].map_name,
                    self.maps_dict[enemy_map_index].kills_to_next_skull,
                    self.maps_dict[enemy_map_index].percent_toward_next_skull,
                    self.maps_dict[enemy_map_index].monster_image,
                    self.maps_dict[enemy_map_index].kill_count,
                    self.maps_dict[enemy_map_index].monster_name,
                ],)
            for skullDict in self.lowest_skulls_dict:
                self.lowest_skulls_dict[skullDict] = sorted(self.lowest_skulls_dict[skullDict], key=lambda item: item[2], reverse=True)
            for skullDict in self.lowest_skulls_dict:
                if len(self.lowest_skulls_dict[skullDict]) > 0:
                    if self.lowest_skull_value == -1:
                        self.lowest_skull_value = skullDict
            self.current_lowest_skull_name = getSkullNames(self.lowest_skull_value)
            self.next_lowest_skull_name = getNextSkullNames(self.lowest_skull_value)

    def __str__(self):
        if self.world_number == 0:
            return "Barbarian Only Extras"
        else:
            return f"World {self.world_number}"


class EnemyMap:
    def __init__(
            self, mapname: str,
            monstername: str,
            mapindex: int,
            portalrequirement: int,
            zowrating: str,
            chowrating: str,
            meowrating: str,
            wowrating: str,
            monsterimage: str = ""
    ):
        self.map_name: str = mapname
        self.map_index: int = mapindex
        self.monster_name: str = monstername
        self.portal_requirement: int = portalrequirement
        self.zow_rating: str = zowrating
        self.chow_rating: str = chowrating
        self.meow_rating: str = meowrating
        self.wow_rating: str = wowrating
        self.kill_count: float = 0
        self.skull_mk_value: int = 0
        self.skull_name: str = "None"
        self.kills_to_next_skull: int = 0
        self.percent_toward_next_skull: int = 0
        self.zow_dict = {}
        if monsterimage:
            self.monster_image = monsterimage.lower()
        else:
            self.monster_image = monstername

    def __str__(self):
        return self.map_name

    def getRating(self, ratingType: str):
        if ratingType == 'ZOW':
            return self.zow_rating
        elif ratingType == 'CHOW':
            return self.chow_rating
        elif ratingType == 'MEOW':
            return self.meow_rating
        elif ratingType == 'WOW':
            return self.wow_rating
        else:
            return 'Insane'

    def updateZOWDict(self, characterIndex: int, KLAValue: float):
        if characterIndex not in self.zow_dict:
            self.zow_dict[characterIndex] = {}
        self.zow_dict[characterIndex] = int(abs(float(KLAValue) - self.portal_requirement))

    def addRawKLA(self, additionalKills: float):
        try:
            self.kill_count += abs(float(additionalKills) - self.portal_requirement)
        except Exception as reason:
            print(f"models.EnemyMap.addRawKLA()~ Unable to add additionalKills value of {type(additionalKills)} {additionalKills} to {self.map_name} because: {reason}")
            #logger.warning(f"Unable to add additionalKills value of {type(additionalKills)} {additionalKills} to {self.map_name} because: {reason}")

    def generateDNSkull(self):
        self.kill_count = int(self.kill_count)
        for counter in range(0, len(dn_skull_requirement_list)):
            if self.kill_count >= dn_skull_requirement_list[counter]:
                self.skull_mk_value = dn_skull_value_list[counter]
        self.skull_name = getSkullNames(self.skull_mk_value)
        if self.skull_mk_value == reversed_dn_skull_value_list[0]:
            #If map's skull is highest, currently Eclipse Skull, set in defaults
            self.kills_to_next_skull = 0
            self.percent_toward_next_skull = 100
        else:
            for skullValueIndex in range(1, len(reversed_dn_skull_value_list)):
                if self.skull_mk_value == reversed_dn_skull_value_list[skullValueIndex]:
                    self.kills_to_next_skull = ceil(reversed_dn_skull_requirement_list[skullValueIndex - 1] - self.kill_count)
                    self.percent_toward_next_skull = floor(round(self.kill_count / reversed_dn_skull_requirement_list[skullValueIndex - 1] * 100))


def buildMaps() -> dict[int, dict]:
    mapDict = {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {},
        #8: {}
    }
    rawMaps = getJSONDataFromFile(os.path.join(app.static_folder, 'enemy-maps.json'))
    for mapData in rawMaps["mapData"]:
        #["Spore Meadows", 1, "Green Mushroom", 11, "Basic W1 Enemies", "Basic W1 Enemies", "Basic W1 Enemies"],
        #mapData[0]: str = map name
        #mapData[1]: int = map index
        #mapData[2]: str = enemy name
        #mapData[3]: int = portal requirement
        #mapData[4]: str = zow rating
        #mapData[5]: str = chow rating
        #mapData[6]: str = meow rating
        #mapData[7]: str = wow rating
        #mapData[8]: str = image
        if mapData[1] in apocable_map_index_dict[0]:
            world = 0
        else:
            world = floor(mapData[1] / 50) + 1
        mapDict[world][mapData[1]] = EnemyMap(
            mapname=mapData[0],
            mapindex=mapData[1],
            monstername=mapData[2],
            portalrequirement=mapData[3],
            zowrating=mapData[4],
            chowrating=mapData[5],
            meowrating=mapData[6],
            wowrating=mapData[7],
            monsterimage=mapData[8]
        )
    return mapDict


def getJSONDataFromFile(filePath):
    with open(filePath, 'r') as inputFile:
        jsonData = json.load(inputFile)
    inputFile.close()
    return jsonData
