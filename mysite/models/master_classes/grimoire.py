from math import prod

from consts.consts_autoreview import ValueToMulti
from consts.consts_monster_data import decode_monster_name
from consts.idleon.lava_func import lava_func
from consts.idleon.master_classes.grimoire import (
    grimoire_upgrades, grimoire_bones_list, grimoire_stack_types, grimoire_coded_stack_monster_order
)
from models.advice.advice import Advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, safer_math_log

logger = get_logger(__name__)


class GrimoireUpgrade:
    def __init__(
        self, name: str, index: int, level: int, cost_base: int, cost_increment: float, bone_index: int,
        max_level: int, value_per_level: int, unlock_requirement: int, description: str, scaling_value: bool
    ):
        self.name = name
        self.index = index
        self.level = level
        self.image = f"grimoire-upgrade-{index}"
        self.cost_base = cost_base
        self.cost_increment = cost_increment
        self.bone_name = grimoire_bones_list[bone_index]
        self.bone_image = f"grimoire-bone-{bone_index}"
        self.max_level = max_level
        self.value_per_level = value_per_level
        self.unlock_requirement = unlock_requirement
        self.description = description
        self.scaling_value = scaling_value
        self.unlocked = False
        self.total_value = 0

    def calculate(self, grimoire_multi: float, stacks: dict[str, int]):
        multi = grimoire_multi if self.scaling_value else 1
        #Update description with total value, stack targets, and scaling info
        if '{' in self.description:
            self.total_value = self.level * self.value_per_level * multi
            self.description = self.description.replace('{', f"{self.total_value}")
        if '}' in self.description:
            self.total_value = ValueToMulti(self.level * self.value_per_level * multi)
            self.description = self.description.replace('}', f"{self.total_value:.2f}")
        if 'Target:$' in self.description:
            stack_type = self.name.split('!')[0]
            if stack_type in grimoire_stack_types:
                stack_count = stacks.get(stack_type, 0)
                if len(grimoire_coded_stack_monster_order) < stack_count:
                    next_stack_target = "All done!"
                else:
                    try:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[stack_count])
                    except:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[0])
                self.description = self.description.replace('Target:$', f"Target: {next_stack_target}")
        self.description += (
            f"<br>({self.value_per_level * multi:.2f} per level"
            f"{' after Writhing Grimoire' if self.scaling_value else ': Not scaled by Writhing Grimoire'})"
        )

    def get_advice(self, total_upgrades: int, additional_info_text: str = "") -> Advice:
        return Advice(
            label=(
                f"{self.name}: {self.description}"
                f"<br>Requires {self.unlock_requirement - total_upgrades} more Upgrades to unlock"
                if not self.unlocked else
                f"{self.name}: {self.description}{additional_info_text}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource=self.bone_image
        )


class Grimoire:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[str, GrimoireUpgrade] = {}
        self.total_upgrades: int = 0

        raw_optlacc = safe_loads(raw_data.get('OptLacc', []))
        self.total_bones_collected: float = safer_convert(safer_index(raw_optlacc, 329, 0), 0.0)
        self.bones: list[float] = [
            safer_convert(safer_index(raw_optlacc, 330 + bone_index, 0), 0.0)
            for bone_index in range(len(grimoire_bones_list))
        ]
        self.stacks: dict[str, int] = {
            'Knockout': safer_convert(safer_index(raw_optlacc, 334, 0), 0),
            'Elimination': safer_convert(safer_index(raw_optlacc, 335, 0), 0),
            'Annihilation': safer_convert(safer_index(raw_optlacc, 336, 0), 0),
        }
        self.charred_bones_enabled: bool = safer_convert(safer_index(raw_optlacc, 367, False), False)

        raw_grimoire = safe_loads(raw_data.get('Grimoire', []))
        if not raw_grimoire:
            logger.warning("Grimoire data not present.")
        for upgrade in grimoire_upgrades:
            clean_name = upgrade["Name"]
            if upgrade["Stack Type"]:
                clean_name = clean_name.replace('(#)', f"({self.stacks.get(upgrade['Stack Type'], 0)})")
            level = min(upgrade["Max Level"], int(safer_index(raw_grimoire, upgrade["Index"], 0)))
            self.upgrades[clean_name] = GrimoireUpgrade(
                name=clean_name,
                index=upgrade["Index"],
                level=level,
                cost_base=upgrade["Cost Base"],
                cost_increment=upgrade["Cost Increment"],
                bone_index=upgrade["Bone Index"],
                max_level=upgrade["Max Level"],
                value_per_level=upgrade["Value Per Level"],
                unlock_requirement=upgrade["Unlock Requirement"],
                description=upgrade["Description"],
                scaling_value=upgrade["Scaling Value"],
            )

        self.total_upgrades = sum(upgrade.level for upgrade in self.upgrades.values())
        for upgrade in self.upgrades.values():
            upgrade.unlocked = self.total_upgrades >= upgrade.unlock_requirement

        self.bone_calc: dict[str, float] = {}

    def calculate_upgrades(self):
        grimoire_multi = ValueToMulti(
            self.upgrades['Writhing Grimoire'].level * self.upgrades['Writhing Grimoire'].value_per_level
        )
        for upgrade in self.upgrades.values():
            upgrade.calculate(grimoire_multi, self.stacks)

    def calculate_bone_sources(self, deathbringers, sneaking, caverns, all_assets, arcade, lab_jewels, emperor):
        # if ("GrimoireBonesDropDEC" == e)
        grimoire_preset_level = 100
        tombstone_preset_level = 100
        for db in deathbringers:
            grimoire_preset_level = max(grimoire_preset_level, db.current_preset_talents.get('196', 0), db.secondary_preset_talents.get('196', 0))
            tombstone_preset_level = max(tombstone_preset_level, db.current_preset_talents.get('198', 0), db.secondary_preset_talents.get('198', 0))

        grimoire_percent = lava_func(
            funcType=all_talentsDict[196]['funcX'],
            level=grimoire_preset_level,
            x1=all_talentsDict[196]['x1'],
            x2=all_talentsDict[196]['x2'],
        )

        self.bone_calc = {
            'mga': ValueToMulti(sneaking.pristine_charms['Glimmerchain'].value),
            'mgb': ValueToMulti(grimoire_percent),
            'mgc': ValueToMulti(caverns.caves['Gambit'].bonuses[12].value),
            'mgd': ValueToMulti((25 * min(1, all_assets.get('EquipmentHats112').amount))),
            'mge': ValueToMulti(
                self.upgrades["Bones o' Plenty"].total_value
                + (self.upgrades['Bovinae Hoarding'].total_value * safer_math_log(self.bones[3], 'Lava'))
                + arcade[40].value
                + lab_jewels['Deadly Wrath Jewel']['Value'] * lab_jewels['Deadly Wrath Jewel']['Enabled']
            ),
            'mgf': 1,
            'mgg': ValueToMulti(emperor["Deathbringer Extra Bones"].value)
        }
        self.bone_calc['Total'] = prod(self.bone_calc.values())
