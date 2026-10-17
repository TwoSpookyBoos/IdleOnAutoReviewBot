from consts.consts_autoreview import ValueToMulti
from consts.idleon.lava_func import lava_func
from consts.idleon.master_classes.compass import (
    compass_upgrades, compass_abominations, compass_medallions, compass_medallions_data, compass_titans,
    compass_dusts_list
)
from models.advice.advice import Advice
from models.master_classes.multi_groups import MultiGroups
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, safer_math_log, safer_math_pow
from utils.text_formatting import notateNumber

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

    def get_advice(self, additional_info_text: str = "", goal: int = 0) -> Advice:
        #A goal means this is a progression tier target, so the description is dropped
        return Advice(
            label=(
                f"{self.path_name}-{self.path_ordering}: {self.name}" if goal
                else f"{self.path_name}-{self.path_ordering}: {self.name}: <br>{self.description}{additional_info_text}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=goal or self.max_level,
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

        self.dust_multi: MultiGroups | None = None

    def calculate_upgrades(self):
        circle_multi = ValueToMulti(
            self.upgrades['Circle Supremacy'].base_value
            + self.upgrades['Abomination Slayer XXI'].base_value
        )
        for upgrade in self.upgrades.values():
            upgrade.calculate(circle_multi)

    def calculate_dust_sources(
        self, wind_walkers, sneaking, all_assets, hatrack_dust, arcade, lab_jewels, emperor, *, max_book_level: int
    ):
        # _customBlock_Windwalker if ("ExtraDust" == e)
        # Racked hood scales with the rack, else worn
        self.hood_owned = hatrack_dust > 0 or all_assets.get('EquipmentHats118').amount > 0
        self.hood_value = hatrack_dust or 25 * self.hood_owned
        self.max_book_level = max_book_level
        self.top_of_the_mornin_total = (
            self.upgrades["Top of the Mornin'"].total_value + self.upgrades['Abomination Slayer XII'].total_value
        )
        self.solardust_stacks = safer_math_log(self.dusts[2], 'Lava')
        self.aether_fragments = min(1000, all_assets.get('Quest100').amount)
        self.tempest_bow_owned = all_assets.get('EquipmentBowsTempest0').amount > 0
        self.tempest_rings_owned = min(all_assets.get('EquipmentRingsTempest6').amount, 2)
        # Eternal Hunt, best preset across Wind Walkers
        self._eternal_hunt_ww, self.eternal_hunt_preset_level = self._best_preset(wind_walkers, '423')
        self.eternal_hunt_per_stack = lava_func(
            funcType='decay',
            level=self.eternal_hunt_preset_level + self._bonus_talent_levels(self._eternal_hunt_ww),
            x1=3,
            x2=200
        )
        # Compass talent, best preset across Wind Walkers
        self._compass_ww, ww_preset_level = self._best_preset(wind_walkers, '421')
        self.compass_preset_level = ww_preset_level
        self.compass_talent_bonus_levels = self._bonus_talent_levels(self._compass_ww)
        # Shown with bonus talent levels; the multi below uses the preset level only
        self.compass_talent_percent = lava_func(
            funcType='decay',
            level=ww_preset_level + self.compass_talent_bonus_levels,
            x1=150,
            x2=300
        )
        compass_percent = lava_func(
            funcType=all_talentsDict[421]['funcX'],
            level=ww_preset_level,
            x1=all_talentsDict[421]['x1'],
            x2=all_talentsDict[421]['x2'],
        )
        self.dust_multi = MultiGroups(
            mga=ValueToMulti(
                self.upgrades['Mountains of Dust'].total_value
                + (self.upgrades['Solardust Hoarding'].total_value * self.solardust_stacks)
            ),
            mgb=self.upgrades['Spire of Dust'].total_value,
            mgc=ValueToMulti(sneaking.pristine_charms['Twinkle Taffy'].value),
            mgd=ValueToMulti(self.hood_value),
            mge=1,
            mgf=ValueToMulti(
                + compass_percent
                + arcade[47].value
                + lab_jewels['North Winds Jewel'].active_value
                + self.upgrades['De Dust I'].total_value
                + self.upgrades['De Dust II'].total_value
                + self.upgrades['De Dust III'].total_value
                + self.upgrades['De Dust IV'].total_value
                + self.upgrades['De Dust V'].total_value
                + self.upgrades['Abomination Slayer IX'].total_value
                + self.upgrades['Abomination Slayer XXX'].total_value
                + self.upgrades['Abomination Slayer XXXIV'].total_value
            ),
            mgg=ValueToMulti(emperor["Windwalker Extra Dust"].value),
        )

    @staticmethod
    def _best_preset(wind_walkers, talent: str):
        best_ww = None
        best_level = 100
        for ww in wind_walkers:
            if best_ww is None:
                best_ww = ww
            if ww.current_preset_talents.get(talent, 0) >= best_level:
                best_ww = ww
                best_level = ww.current_preset_talents.get(talent, 0)
            if ww.secondary_preset_talents.get(talent, 0) >= best_level:
                best_ww = ww
                best_level = ww.secondary_preset_talents.get(talent, 0)
        return best_ww, best_level

    @staticmethod
    def _bonus_talent_levels(ww) -> int:
        return ww.total_bonus_talent_levels if ww is not None else 0

    def get_abominations_slain_advice(self, goal: int) -> Advice:
        return Advice(
            label="Abominations Slain",
            picture_class='slayer-abominator',
            progression=self.total_abominations_slain,
            goal=goal
        )

    def get_medallions_collected_advice(self, goal: int) -> Advice:
        return Advice(
            label="Medallions Collected",
            picture_class='wind-walker-medallion',
            progression=self.total_medallions,
            goal=goal
        )

    def get_top_of_the_mornin_advice(self) -> Advice:
        return Advice(
            label=(
                f"""Daily Top of the Mornin' kills: {self.top_of_the_mornin_total}"""
                f"""<br>Remaining: {self.top_of_the_mornin}"""
            ),
            picture_class=self.upgrades["Top of the Mornin'"].image,
            progression=self.top_of_the_mornin_total - self.top_of_the_mornin,
            goal=self.top_of_the_mornin_total,
            informational=True
        )

    def get_total_dust_collected_advice(self) -> Advice:
        return Advice(
            label=f"Total Dusts Collected: {notateNumber('Basic', self.total_dust_collected, 3)}",
            picture_class='dustwalker',
            informational=True,
            completed=True
        )

    def get_aethermoon_advice(self) -> Advice:
        if self.aethermoons_enabled:
            return Advice(
                label="Aethermoons Enabled! Collect 1 per two full AFK hour while fighting on a Wind Walker. "
                      "Maximize your /hr display within AFK Info screen before consuming!",
                picture_class='aethermoon',
                progression=1,
                goal=1
            )
        return Advice(
            label="Fight with Tempest Form enabled to collect 1,000 Aether Fragments, then use the stack. "
                  "This enables AFK Fighting on Wind Walkers to produce 1 Aethermoon per two hours!",
            picture_class='aether-fragment',
            progression=self.aether_fragments,
            goal=1000
        )

    def get_dust_advices(self) -> list[Advice]:
        return [Advice(
            label=f"{dust_name}: {notateNumber('Basic', self.dusts[dust_index], 3)}",
            picture_class=f'compass-dust-{dust_index}',
            informational=True,
            completed=True
        ) for dust_index, dust_name in enumerate(compass_dusts_list)]

    def get_dust_multi_advice(self) -> Advice:
        return Advice(
            label=f"Total Dust multi: {self.dust_multi.total:.3f}x",
            picture_class='compass'
        )

    def get_solardust_stacks_text(self) -> str:
        return (
            f"<br>{self.solardust_stacks:.3f} stacks = "
            f"{self.upgrades['Solardust Hoarding'].total_value * self.solardust_stacks:.3f}% total"
        )

    def get_windwalker_hood_advice(self) -> Advice:
        return Advice(
            label="Windwalker Hood: +25%",
            picture_class='windwalker-hood',
            progression=int(self.hood_owned),
            goal=1,
            resource='gem'
        )

    def get_tempest_bow_advice(self) -> Advice:
        return Advice(
            label="Tempest Bow of Dust:"
                  "<br>Base Range: 15 - 50%"
                  "<br>Max + 5/5 10 PCT stones: 300%",
            picture_class='tempest-bow-of-dust',
            progression=int(self.tempest_bow_owned),
            goal=1,
            resource='tempest-bow-stone-10-pct',
        )

    def get_tempest_ring_advice(self) -> Advice:
        return Advice(
            label="Tempest Ring of Gold:"
                  "<br>Base Range: 20 - 50%"
                  "<br>Max + 3/3 10 PCT stones: 125%",
            picture_class='tempest-ring-of-gold',
            progression=self.tempest_rings_owned,
            goal=2,
            resource='tempest-ring-stone-10-pct'
        )

    def get_eternal_hunt_advice(self) -> Advice:
        ww = self._eternal_hunt_ww
        return Advice(
            label=f"{self.eternal_hunt_preset_level}/{self.max_book_level} booked Eternal Hunt:"
                  f"<br>Max Preset Level {self.eternal_hunt_preset_level + ww.total_bonus_talent_levels} on "
                  f"{ww.character_name} including bonus talent levels",
            picture_class='eternal-hunt',
            progression=self.eternal_hunt_preset_level,
            goal=self.max_book_level
        )

    def get_eternal_hunt_stacks_advice(self) -> Advice:
        per_stack = self.eternal_hunt_per_stack
        return Advice(
            label=f"<br>Per stack: +{per_stack:.3f}%"
                  f"<br>10 stacks: {ValueToMulti(10 * per_stack):.3f}x"
                  f"<br>20 stacks: {ValueToMulti(20 * per_stack):.3f}x"
                  f"<br>30 stacks: {ValueToMulti(30 * per_stack):.3f}x"
                  f"<br>40 stacks: {ValueToMulti(40 * per_stack):.3f}x"
                  f"<br>50 stacks: {ValueToMulti(50 * per_stack):.3f}x",
            picture_class='eternal-hunt-grave',
            completed=True,
            informational=True
        )

    def get_compass_talent_advice(self) -> Advice:
        return Advice(
            label=f"{self.compass_preset_level}/{self.max_book_level} booked Compass:"
                  f"<br>Max Preset Level {self.compass_preset_level + self.compass_talent_bonus_levels} on "
                  f"{self._compass_ww.character_name} including bonus talent levels"
                  f"<br>+{self.compass_talent_percent:.3f}% boost to Dust found",
            picture_class='compass',
            progression=self.compass_preset_level,
            goal=self.max_book_level
        )

    def get_total_medallions_advice(self) -> Advice:
        return Advice(
            label=f"Total Medallions Collected: {self.total_medallions}/{len(compass_medallions)}",
            picture_class='wind-walker-medallion',
            progression=self.total_medallions,
            goal=len(compass_medallions)
        )

    def get_total_upgrades_advice(self) -> Advice:
        return Advice(
            label=f"Total Compass Upgrades: {self.total_upgrades:,}",
            picture_class='compass',
        )

    def get_total_abominations_advice(self) -> Advice:
        return Advice(
            label=f"Total Abominations Slain: {self.total_abominations_slain:,}",
            picture_class='slayer-abominator',
        )
