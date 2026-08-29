from consts.consts_autoreview import ValueToMulti
from consts.consts_monster_data import decode_monster_name
from consts.idleon.master_classes.grimoire import grimoire_coded_stack_monster_order
from consts.idleon.w1.upgrade_vault import vault_upgrades, vault_stack_types
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)


class VaultUpgrade:
    def __init__(
        self, name: str, index: int, level: int, cost_base: int, cost_increment: float,
        max_level: int, value_per_level: int, unlock_requirement: int, description: str,
        scaling_value: bool, vault_section: int
    ):
        self.name = name
        self.index = index
        self.level = level
        self.image = f"vault-upgrade-{index}"
        self.cost_base = cost_base
        self.cost_increment = cost_increment
        self.max_level = max_level
        self.value_per_level = value_per_level
        self.unlock_requirement = unlock_requirement
        self.description = description
        self.scaling_value = scaling_value
        self.vault_section = vault_section
        self.unlocked = False
        self.total_value = 0
        self.max_value = 0

    def calculate(self, scaling_multiplier: float, scaling_multiplier_max: float, stacks: dict[str, int]):
        total_value = self.level * self.value_per_level * scaling_multiplier
        total_value_max = self.max_level * self.value_per_level * scaling_multiplier_max
        if "{" in self.description:
            self.total_value = total_value
            self.max_value = total_value_max
            self.description = self.description.replace("{", f"{self.total_value:.2f}")
        if "}" in self.description:
            self.total_value = ValueToMulti(total_value)
            self.max_value = ValueToMulti(total_value_max)
            self.description = self.description.replace("}", f"{self.total_value:.2f}")
        if "Target:&" in self.description:
            stack_type = self.name.split("!")[0]
            if stack_type in vault_stack_types:
                stack_count = stacks.get(stack_type, 0)
                if len(grimoire_coded_stack_monster_order) < stack_count:
                    next_stack_target = "All done!"
                else:
                    try:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[stack_count])
                    except:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[0])
                self.description = self.description.replace("Target:&", f"Target: {next_stack_target}")
        self.description += (
            f"<br>({self.value_per_level * scaling_multiplier:.2f} per level"
            f"{' after Vault Mastery ' if self.scaling_value else ': Not scaled by Vault Mastery '}"
            f"{self.vault_section}"
            f")"
        )

    def get_advice(self, total_upgrades: int, link_to_section: bool = True, additional_info_text: str = "") -> Advice:
        main_line = f"""{f"{{{{ Upgrade Vault|#upgrade-vault }}}} - {self.name}" if link_to_section else self.name}: {self.description}"""
        unlock_line = f"<br>Requires {self.unlock_requirement - total_upgrades} more Upgrades to unlock" if not self.unlocked else ""
        return Advice(
            label=main_line + unlock_line + additional_info_text,
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
        )

    def get_tier_advice(self, total_upgrades: int) -> Advice:
        return Advice(
            label=(
                f"Max {self.name}"
                f"<br>Requires {self.unlock_requirement - total_upgrades} more Upgrades to unlock"
                if not self.unlocked else
                f"{self.name}: {self.description}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
        )


class Vault:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[str, VaultUpgrade] = {}
        self.total_upgrades: int = 0
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        self.stacks: dict[str, int] = {"Knockout": safer_index(raw_optlacc, 338, 0)}

        raw_vault = safe_loads(raw_data.get("UpgVault", []))
        if not raw_vault:
            logger.warning("Upgrade Vault data not present.")
        for upgrade in vault_upgrades:
            clean_name = upgrade["Name"]
            if upgrade["Stack Type"]:
                clean_name += f" ({self.stacks.get(upgrade['Stack Type'], 0)} stacks)"

            try:
                level = min(upgrade["Max Level"], int(raw_vault[upgrade["Index"]]))
            except:
                level = 0

            self.upgrades[clean_name] = VaultUpgrade(
                name=clean_name,
                index=upgrade["Index"],
                level=level,
                cost_base=upgrade["Cost Base"],
                cost_increment=upgrade["Cost Increment"],
                max_level=upgrade["Max Level"],
                value_per_level=upgrade["Value Per Level"],
                unlock_requirement=upgrade["Unlock Requirement"],
                description=upgrade["Description"],
                scaling_value=upgrade["Scaling Value"],
                vault_section=upgrade["Vault Section"],
            )

        self.total_upgrades = sum(upgrade.level for upgrade in self.upgrades.values())
        for upgrade in self.upgrades.values():
            upgrade.unlocked = self.total_upgrades >= upgrade.unlock_requirement

    def calculate(self):
        mastery = self.upgrades["Vault Mastery"]
        mastery_ii = self.upgrades["Vault Mastery II"]
        vault_multi = [
            ValueToMulti(mastery.level * mastery.value_per_level),
            ValueToMulti(mastery_ii.level * mastery_ii.value_per_level),
        ]
        vault_multi_max = [
            ValueToMulti(mastery.max_level * mastery.value_per_level),
            ValueToMulti(mastery_ii.max_level * mastery_ii.value_per_level),
        ]
        for upgrade in self.upgrades.values():
            scaling_multiplier = vault_multi[upgrade.vault_section - 1] if upgrade.scaling_value else 1
            scaling_multiplier_max = vault_multi_max[upgrade.vault_section - 1] if upgrade.scaling_value else 1
            upgrade.calculate(scaling_multiplier, scaling_multiplier_max, self.stacks)
