from math import prod

from consts.consts_autoreview import ValueToMulti
from consts.idleon.lava_func import lava_func
from consts.idleon.master_classes.compass import (
    compass_upgrades, compass_abominations, compass_medallions_data, compass_titans, compass_dusts_list
)
from models.advice.advice import Advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, safer_math_log, safer_math_pow

logger = get_logger(__name__)


class CompassAbomination:
    def __init__(self, name: str, map_index: int, image: str, weakness: str):
        self.name = name
        self.map_index = map_index
        self.world = 1 + (map_index // 50)
        self.image = image
        self.weakness = weakness
        self.defeated = False

    def get_advice(self) -> Advice:
        if self.defeated:
            return Advice(
                label=f"{self.name} defeated in W{self.world}"
                      f"<br>Weakness: {self.weakness}",
                picture_class=self.image,
                progression=1,
                goal=1
            )
        return Advice(
            label=f"{self.name[:3]}... undefeated in W{self.world}"
                  f"<br>Weakness: {self.weakness}",
            picture_class='placeholder',
            progression=0,
            goal=1
        )


class CompassUpgrade:
    def __init__(
        self, name: str, index: int, level: int, cost_base: int, cost_increment: float, dust_index: int,
        max_level: int, value_per_level, shape: str, path_name: str, path_ordering: int, description: str
    ):
        self.name = name
        self.index = index
        self.level = level
        self.image = f"compass-upgrade-{index}"
        self.cost_base = cost_base
        self.cost_increment = cost_increment
        self.dust_name = compass_dusts_list[dust_index]
        self.dust_image = f"compass-dust-{dust_index}"
        self.max_level = max_level
        self.value_per_level = value_per_level
        self.shape = shape
        self.path_name = path_name
        self.path_ordering = path_ordering
        self.description = description
        self.base_value = level * value_per_level
        self.unlocked = False
        self.abomination_name = None
        self.total_value = 0

    def calculate(self, circle_multi: float):
        multi = circle_multi if self.shape == 'Circle' else 1
        value = self.base_value * multi * (safer_math_pow(2, self.level // 50) if self.name == 'Moon of Sneak' else 1)
        #Update description with total value and scaling info
        if '{' in self.description:
            self.total_value = value
            self.description = self.description.replace('{', f"{self.total_value:.2f}")
        if '}' in self.description:
            self.total_value = ValueToMulti(value)
            self.description = self.description.replace('}', f"{self.total_value:.2f}")
        self.description += (
            f"<br>({self.value_per_level * multi:.2f} per level"
            f"{' after Circle Multis' if self.shape == 'Circle' else ''})"
        )

    def get_advice(self, additional_info_text: str = "") -> Advice:
        return Advice(
            label=f"{self.path_name}-{self.path_ordering}: {self.name}: <br>{self.description}{additional_info_text}",
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource=self.dust_image
        )

    def get_abomination_locked_advice(self, world) -> Advice:
        return Advice(
            label=(
                f"{self.path_name}-{self.path_ordering}: {self.name}:"
                f"<br>Defeat {self.abomination_name[:3]}... in W{world} to reveal!"
            ),
            picture_class='placeholder',
            progression=self.level,
            goal=self.max_level,
            resource=self.dust_image
        )


class CompassMedallion:
    def __init__(self, code_name: str, enemy_name: str, image: str):
        self.code_name = code_name
        self.enemy_name = enemy_name
        self.image = image
        self.obtained = False

    def get_advice(self) -> Advice:
        return Advice(
            label=f"{self.enemy_name}",
            picture_class=f"{self.image}",
            progression=int(self.obtained),
            goal=1
        )


class Compass:
    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get('OptLacc', []))
        self.total_dust_collected: float = safer_convert(safer_index(raw_optlacc, 362, 0), 0.0)
        self.dusts: list[float] = [
            safer_convert(safer_index(raw_optlacc, 357 + dust_index, 0), 0.0)
            for dust_index in range(len(compass_dusts_list))
        ]
        self.top_of_the_mornin: int = max(0, safer_convert(safer_index(raw_optlacc, 365, 0), 0))
        self.elements: dict[int, str] = {0: 'Fire', 1: 'Wind', 2: 'Grass', 3: 'Ice'}
        self.aethermoons_enabled: bool = safer_convert(safer_index(raw_optlacc, 401, False), False)

        raw_compass = safe_loads(raw_data.get('Compass', []))
        if not raw_compass:
            logger.warning("Compass data not present.")
        while len(raw_compass) < 5:
            raw_compass.append([])

        #Abominations - need their defeated status before parsing Upgrades
        raw_abom_status = [safer_convert(v, 0) for v in raw_compass[1]]
        self.total_abominations_slain: int = sum(raw_abom_status)
        self.abominations: dict[str, CompassAbomination] = {}
        for abom_index, abom in enumerate(compass_abominations):
            abomination = CompassAbomination(
                name=abom["Name"],
                map_index=abom["Map Index"],
                image=abom["Image"],
                weakness=self.elements.get(abom["Weakness Index"], 'Unknown'),
            )
            abomination.defeated = safer_index(raw_abom_status, abom_index, 0) > 0
            self.abominations[abom["Name"]] = abomination

        #Upgrades
        raw_compass_upgrades = [safer_convert(v, 0) for v in raw_compass[0]]
        self.total_upgrades: int = sum(raw_compass_upgrades)
        self.upgrades: dict[str, CompassUpgrade] = {}
        for upgrade in compass_upgrades:
            level = min(upgrade["Max Level"], int(safer_index(raw_compass_upgrades, upgrade["Index"], 0)))
            self.upgrades[upgrade["Name"]] = CompassUpgrade(
                name=upgrade["Name"],
                index=upgrade["Index"],
                level=level,
                cost_base=upgrade["Cost Base"],
                cost_increment=upgrade["Cost Increment"],
                dust_index=upgrade["Dust Index"],
                max_level=upgrade["Max Level"],
                value_per_level=upgrade["Value Per Level"],
                shape=upgrade["Shape"],
                path_name=upgrade["Path Name"],
                path_ordering=upgrade["Path Ordering"],
                description=upgrade["Description"],
            )

        #Determine Unlock Status
        for upgrade_name, upgrade_details in self.upgrades.items():
            path_upgrade_name = f"{upgrade_details.path_name} Path"
            if path_upgrade_name == 'Default Path':
                if upgrade_name == 'Pathfinder':
                    upgrade_details.unlocked = True
                else:
                    upgrade_details.unlocked = self.upgrades['Pathfinder'].level >= 1
            elif path_upgrade_name == 'Abomination Path':
                if 'Titan doesnt exist' not in upgrade_details.description:
                    try:
                        upgrade_details.abomination_name = compass_titans[upgrade_details.path_ordering - 1][0].replace('_', ' ')
                        upgrade_details.unlocked = self.abominations[upgrade_details.abomination_name].defeated
                    except:
                        upgrade_details.abomination_name = '??????'
                        logger.exception(f"Could not look up Abomination defeated status for {upgrade_name}")
                        upgrade_details.unlocked = False
            else:
                upgrade_details.unlocked = self.upgrades[path_upgrade_name].level >= upgrade_details.path_ordering

        #Medallions
        raw_medallions = raw_compass[3]
        self.total_medallions: int = len(raw_medallions)
        self.medallions: dict[str, CompassMedallion] = {}
        for medallion_data in compass_medallions_data:
            medallion = CompassMedallion(
                code_name=medallion_data["Code Name"],
                enemy_name=medallion_data["Enemy Name"],
                image=medallion_data["Image"],
            )
            medallion.obtained = medallion_data["Code Name"] in raw_medallions
            self.medallions[medallion_data["Code Name"]] = medallion

        self.total_exalted: int = len(raw_compass[4])

        self.dust_calc: dict[str, float] = {}

    def calculate_upgrades(self):
        circle_multi = ValueToMulti(
            self.upgrades['Circle Supremacy'].base_value
            + self.upgrades['Abomination Slayer XXI'].base_value
        )
        for upgrade in self.upgrades.values():
            upgrade.calculate(circle_multi)

    def calculate_dust_sources(self, wind_walkers, sneaking, all_assets, arcade, lab_jewels, emperor):
        # _customBlock_Windwalker if ("ExtraDust" == e)
        ww_preset_level = 100
        for ww in wind_walkers:
            if ww.current_preset_talents.get('421', 0) >= ww_preset_level:
                ww_preset_level = ww.current_preset_talents.get('421', 0)
            if ww.secondary_preset_talents.get('421', 0) >= ww_preset_level:
                ww_preset_level = ww.secondary_preset_talents.get('421', 0)
        compass_percent = lava_func(
            funcType=all_talentsDict[421]['funcX'],
            level=ww_preset_level,
            x1=all_talentsDict[421]['x1'],
            x2=all_talentsDict[421]['x2'],
        )
        self.dust_calc = {
            'mga': ValueToMulti(
                self.upgrades['Mountains of Dust'].total_value
                + (self.upgrades['Solardust Hoarding'].total_value * safer_math_log(self.dusts[2], 'Lava'))
            ),
            'mgb': self.upgrades['Spire of Dust'].total_value,
            'mgc': ValueToMulti(sneaking.pristine_charms['Twinkle Taffy'].value),
            'mgd': ValueToMulti(
                (25 * min(1, all_assets.get('EquipmentHats118').amount))
            ),
            'mge': 1,
            'mgf': ValueToMulti(
                + compass_percent
                + arcade[47]['Value']
                + lab_jewels['North Winds Jewel']['Value'] * lab_jewels['North Winds Jewel']['Enabled']
                + self.upgrades['De Dust I'].total_value
                + self.upgrades['De Dust II'].total_value
                + self.upgrades['De Dust III'].total_value
                + self.upgrades['De Dust IV'].total_value
                + self.upgrades['De Dust V'].total_value
                + self.upgrades['Abomination Slayer IX'].total_value
                + self.upgrades['Abomination Slayer XXX'].total_value
                + self.upgrades['Abomination Slayer XXXIV'].total_value
            ),
            'mgg': ValueToMulti(emperor["Windwalker Extra Dust"].value)
        }
        self.dust_calc['Total'] = prod(self.dust_calc.values())
