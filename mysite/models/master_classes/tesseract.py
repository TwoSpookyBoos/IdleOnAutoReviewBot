from math import prod

from consts.consts_autoreview import ValueToMulti
from consts.idleon.lava_func import lava_func
from consts.idleon.master_classes.tesseract import tesseract_upgrades, tesseract_tachyon_list
from models.advice.advice import Advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, safer_math_log

logger = get_logger(__name__)


class TesseractUpgrade:
    def __init__(
        self, name: str, index: int, level: int, cost_base: int, cost_increment: float, tachyon_index: int,
        max_level: int, value_per_level: int, unlock_requirement: int, description: str
    ):
        self.name = name
        self.index = index
        self.level = level
        self.image = f"tesseract-upgrade-{index}"
        self.cost_base = cost_base
        self.cost_increment = cost_increment
        self.tachyon_name = tesseract_tachyon_list[tachyon_index]
        self.tachyon_image = f"tesseract-tachyon-{tachyon_index}"
        self.max_level = max_level
        self.value_per_level = value_per_level
        self.unlock_requirement = unlock_requirement
        self.description = description
        self.unlocked = False
        self.total_value = 0

    def calculate(self):
        if '{' in self.description:
            self.total_value = self.level * self.value_per_level
            self.description = self.description.replace('{', f"{self.total_value}")
        if '}' in self.description:
            self.total_value = ValueToMulti(self.level * self.value_per_level)
            self.description = self.description.replace('}', f"{self.total_value:.2f}")

    def get_advice(self, total_upgrades: int) -> Advice:
        return Advice(
            label=(
                f"{self.name}: {self.description}"
                f"<br>Requires {self.unlock_requirement - total_upgrades} more Upgrades to unlock"
                if not self.unlocked else
                f"{self.name}: {self.description}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource=self.tachyon_image
        )

    def get_bonus_advice(self) -> Advice:
        return Advice(
            label=f"Tesseract Upgrade '{self.name}':"
                  f"<br>+{self.total_value}% Tachyons",
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource=self.tachyon_image
        )

    def get_tier_advice(self, required_level: int) -> Advice:
        return Advice(
            label=self.name,
            picture_class=self.image,
            progression=self.level,
            goal=required_level,
            resource=self.tachyon_image
        )


class Tesseract:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[str, TesseractUpgrade] = {}
        self.total_upgrades: int = 0

        raw_optlacc = safe_loads(raw_data.get('OptLacc', []))
        self.total_tachyons_collected: float = safer_convert(safer_index(raw_optlacc, 394, 0), 0.0)
        self.tachyons: list[float] = [
            safer_convert(safer_index(raw_optlacc, 388 + tachyon_index, 0), 0.0)
            for tachyon_index in range(len(tesseract_tachyon_list))
        ]
        self.prisma_bubbles: float = safer_convert(safer_index(raw_optlacc, 395, 0), 0.0)
        self.arcane_rocks_enabled: bool = safer_convert(safer_index(raw_optlacc, 452, False), False)

        raw_tesseract = safe_loads(raw_data.get('Arcane', []))
        if not raw_tesseract:
            logger.warning("Tesseract data not present.")
        for upgrade in tesseract_upgrades:
            level = min(upgrade["Max Level"], int(safer_index(raw_tesseract, upgrade["Index"], 0)))
            self.upgrades[upgrade["Name"]] = TesseractUpgrade(
                name=upgrade["Name"],
                index=upgrade["Index"],
                level=level,
                cost_base=upgrade["Cost Base"],
                cost_increment=upgrade["Cost Increment"],
                tachyon_index=upgrade["Tachyon Index"],
                max_level=upgrade["Max Level"],
                value_per_level=upgrade["Value Per Level"],
                unlock_requirement=upgrade["Unlock Requirement"],
                description=upgrade["Description"],
            )

        self.total_upgrades = sum(upgrade.level for upgrade in self.upgrades.values())
        for upgrade in self.upgrades.values():
            upgrade.unlocked = self.total_upgrades >= upgrade.unlock_requirement

        self.tachyon_calc: dict[str, float] = {}
        self.tesseract_talent_bonus_value: float = 0.0

    def calculate_upgrades(self):
        for upgrade in self.upgrades.values():
            upgrade.calculate()

    def calculate_tachyon_sources(self, arcane_cultists, lab_jewels, arcade, emperor, alchemy_bubbles, sneaking, gemshop, alchemy_vials, has_balloonfish: bool):
        # Dependency: _calculate_w2_vials(account) for alchemy_vials' Value
        # _customBlock_ArcaneType: "ExtraTachyon" == d
        tesseract_talent_index = 586
        backup_energy_talent_index = 599
        tesseract_preset_level = 100
        backup_energy_preset_level = 100

        for ac in arcane_cultists:
            tesseract_preset_level = max(
                tesseract_preset_level,
                ac.current_preset_talents.get(str(tesseract_talent_index), 0),
                ac.secondary_preset_talents.get(str(tesseract_talent_index), 0),
            )
            backup_energy_preset_level = max(
                backup_energy_preset_level,
                ac.current_preset_talents.get(str(backup_energy_talent_index), 0),
                ac.secondary_preset_talents.get(str(backup_energy_talent_index), 0),
            )

        self.tesseract_talent_bonus_value = lava_func(
            funcType=all_talentsDict[tesseract_talent_index]['funcX'],
            level=tesseract_preset_level,
            x1=all_talentsDict[tesseract_talent_index]['x1'],
            x2=all_talentsDict[tesseract_talent_index]['x2'],
        )

        backup_energy_bonus_value = lava_func(
            funcType=all_talentsDict[backup_energy_talent_index]['funcX'],
            level=backup_energy_talent_index,  # NOTE: pre-existing quirk carried over verbatim from the old dict-based calc; looks like it should be backup_energy_preset_level
            x1=all_talentsDict[backup_energy_talent_index]['x1'],
            x2=all_talentsDict[backup_energy_talent_index]['x2'],
        )

        self.tachyon_calc = {
            'mga': ValueToMulti(
                self.upgrades['Ripple in Spacetime'].total_value
                + self.tesseract_talent_bonus_value
                + self.upgrades['Verdon Hoarding'].total_value * safer_math_log(self.tachyons[2], 10)
                + self.upgrades['Aurion Hoarding'].total_value * safer_math_log(self.tachyons[5], 10)
                # + Extra Tachyon from Equipment
                + lab_jewels['Eternal Energy Jewel']['Value'] * lab_jewels['Eternal Energy Jewel']['Owned']
                + arcade[50]['Value']
            ),
            'mgb': ValueToMulti(
                emperor["Arcane Cultist Extra Tachyons"].value
                + alchemy_bubbles['Tachyon Bubble']['BaseValue']
            ),
            'mgc': ValueToMulti(sneaking.pristine_charms['Mystery Fizz'].value),
            'mgd': ValueToMulti(backup_energy_bonus_value),
            'mge': 1 + 0.2 * gemshop['Bundles']['bun_x']['Owned'],
            'mgf': ValueToMulti(alchemy_vials["Paper Pint (Chapter Three 'This is Gospel')"]['Value']),
            'mgg': 4 * has_balloonfish,
        }
        self.tachyon_calc['Total'] = prod(self.tachyon_calc.values())

    def get_tesseract_talent_advice(self) -> Advice:
        return Advice(
            label=f"Tesseract Talent: +{self.tesseract_talent_bonus_value:.2f}% Tachyons",
            picture_class='tesseract'
        )

    def get_backup_energy_advice(self) -> Advice:
        return Advice(
            label=f"Backup Energy Talent: {self.tachyon_calc['mgd']:.2f}x Tachyons",
            picture_class='backup-energy',
        )
