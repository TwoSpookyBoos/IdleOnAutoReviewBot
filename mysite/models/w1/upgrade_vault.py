from consts.consts_autoreview import ValueToMulti
from consts.consts_master_classes import grimoire_coded_stack_monster_order
from consts.consts_monster_data import decode_monster_name
from consts.idleon.w1.upgrade_vault import UpgradeVault, vault_dont_scale, vault_stack_types, vault_section_indexes
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, logger
from utils.text_formatting import vault_string_cleaner


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


class Vault:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[str, VaultUpgrade] = {}
        self.total_upgrades: int = 0
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        self.stacks: dict[str, int] = {"Knockout": safer_index(raw_optlacc, 338, 0)}

        raw_vault = safe_loads(raw_data.get("UpgVault", []))
        if not raw_vault:
            logger.warning("Upgrade Vault data not present.")
        for index, upgrade_values in enumerate(UpgradeVault):
            clean_name = vault_string_cleaner(upgrade_values[0])
            secondary_description = vault_string_cleaner(upgrade_values[10]) if len(upgrade_values) >= 11 else ""
            stack_type = clean_name.split("!")[0]
            if stack_type in vault_stack_types:
                clean_name += f" ({self.stacks.get(stack_type, 0)} stacks)"

            vault_section = 0
            for list_index, vault_section_index in enumerate(vault_section_indexes):
                if index <= vault_section_index:
                    vault_section = list_index + 1
                    break

            try:
                level = min(int(upgrade_values[4]), int(raw_vault[index]))
                description = f"{vault_string_cleaner(upgrade_values[9])} {secondary_description}"
            except:
                level = 0
                description = f"{upgrade_values[9].replace('_', ' ')}{secondary_description}"

            self.upgrades[clean_name] = VaultUpgrade(
                name=clean_name,
                index=index,
                level=level,
                cost_base=safer_convert(upgrade_values[1], 0),
                cost_increment=float(upgrade_values[2]),
                max_level=int(upgrade_values[4]),
                value_per_level=int(upgrade_values[5]),
                unlock_requirement=int(upgrade_values[6]),
                description=description,
                scaling_value=index not in vault_dont_scale,
                vault_section=vault_section,
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
