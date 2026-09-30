from consts.consts_autoreview import ValueToMulti
from consts.idleon.lava_func import lava_func
from consts.idleon.master_classes.grimoire import (
    grimoire_upgrades, grimoire_bones_list, grimoire_stack_types, grimoire_stack_target_monsters
)
from models.advice.advice import Advice
from models.master_classes.multi_groups import MultiGroups
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, safer_math_log
from utils.text_formatting import notateNumber

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
                next_stack_target = (
                    "All done!" if stack_count >= len(grimoire_stack_target_monsters)
                    else grimoire_stack_target_monsters[stack_count]
                )
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

        self.bone_multi: MultiGroups | None = None

    def calculate_upgrades(self):
        grimoire_multi = ValueToMulti(
            self.upgrades['Writhing Grimoire'].level * self.upgrades['Writhing Grimoire'].value_per_level
        )
        for upgrade in self.upgrades.values():
            upgrade.calculate(grimoire_multi, self.stacks)

    def calculate_bone_sources(
        self, deathbringers, sneaking, caverns, all_assets, hatrack_bones, arcade, lab_jewels, emperor, *,
        max_book_level: int
    ):
        # if ("GrimoireBonesDropDEC" == e)
        # Racked hood scales with the rack, else worn
        self.hood_owned = hatrack_bones > 0 or all_assets.get('EquipmentHats112').amount > 0
        self.hood_value = hatrack_bones or 25 * self.hood_owned
        self.max_book_level = max_book_level
        self.charred_fragments = min(1000, all_assets.get('Quest98').amount)
        self.bovinae_stacks = safer_math_log(self.bones[3], 'Lava')
        self._grimoire_db, grimoire_preset_level = self._best_preset(deathbringers, '196')
        self._tombstone_db, tombstone_preset_level = self._best_preset(deathbringers, '198')
        self.grimoire_preset_level = grimoire_preset_level
        self.tombstone_preset_level = tombstone_preset_level
        self.tombstone_per_stack = lava_func(
            funcType=all_talentsDict[198]['funcX'],
            level=tombstone_preset_level,
            x1=all_talentsDict[198]['x1'],
            x2=all_talentsDict[198]['x2'],
        )

        grimoire_percent = lava_func(
            funcType=all_talentsDict[196]['funcX'],
            level=grimoire_preset_level,
            x1=all_talentsDict[196]['x1'],
            x2=all_talentsDict[196]['x2'],
        )

        self.bone_multi = MultiGroups(
            mga=ValueToMulti(sneaking.pristine_charms['Glimmerchain'].value),
            mgb=ValueToMulti(grimoire_percent),
            mgc=ValueToMulti(caverns.caves['Gambit'].bonuses[12].value),
            mgd=ValueToMulti(min(50, self.hood_value)),
            mge=ValueToMulti(
                self.upgrades["Bones o' Plenty"].total_value
                + (self.upgrades['Bovinae Hoarding'].total_value * self.bovinae_stacks)
                + arcade[40].value
                + lab_jewels['Deadly Wrath Jewel'].active_value
            ),
            mgf=1,
            mgg=ValueToMulti(emperor["Deathbringer Extra Bones"].value),
        )

    @staticmethod
    def _best_preset(deathbringers, talent: str):
        # Secondary preset raises the level but keeps the character
        best_db = None
        best_level = 100
        for db in deathbringers:
            if best_db is None:
                best_db = db
            if db.current_preset_talents.get(talent, 0) > best_level:
                best_db = db
                best_level = db.current_preset_talents.get(talent, 0)
            if db.secondary_preset_talents.get(talent, 0) > best_level:
                best_level = db.secondary_preset_talents.get(talent, 0)
        return best_db, best_level

    def get_total_upgrades_tier_advice(self, goal: int) -> Advice:
        return Advice(
            label="Total Grimoire Upgrades",
            picture_class='grimoire',
            progression=self.total_upgrades,
            goal=goal
        )

    def get_specific_upgrade_tier_advice(self, upgrade_name: str, required_level: int) -> Advice:
        upgrade_details = self.upgrades.get(upgrade_name)
        return Advice(
            label=upgrade_name,
            picture_class=upgrade_details.image if upgrade_details else 'grimoire',
            progression=upgrade_details.level if upgrade_details else 0,
            goal=required_level
        )

    def get_stacks_tier_advice(self, stack_type: str, required_stacks: int) -> Advice:
        target_index = required_stacks - 1
        target_monster = (
            grimoire_stack_target_monsters[target_index]
            if 0 <= target_index < len(grimoire_stack_target_monsters)
            else None
        )
        return Advice(
            label=f"{stack_type} Stacks",
            picture_class=target_monster or 'grimoire',
            progression=self.stacks.get(stack_type, 0),
            goal=required_stacks
        )

    def get_total_bones_collected_advice(self) -> Advice:
        return Advice(
            label=f"Total Bones Collected: {notateNumber('Basic', self.total_bones_collected, 3)}",
            picture_class='wraith-overlord'
        )

    def get_charred_bones_advice(self) -> Advice:
        if self.charred_bones_enabled:
            return Advice(
                label="Charred Bones Enabled! Collect 1 per full AFK hour while fighting on a Death Bringer. "
                      "Maximize your /hr display within AFK Info screen before consuming!",
                picture_class='charred-bone',
                progression=1,
                goal=1
            )
        return Advice(
            label="Fight with Wraith Form enabled to collect 1,000 Charred Fragments, then use the stack. "
                  "This enables AFK Fighting on Death Bringers to produce 1 Charred Bone per hour!",
            picture_class='charred-fragment',
            progression=self.charred_fragments,
            goal=1000
        )

    def get_bone_advices(self) -> list[Advice]:
        return [
            Advice(
                label=f"{bone_name}: {notateNumber('Basic', self.bones[bone_index], 3)}",
                picture_class=f'grimoire-bone-{bone_index}'
            ) for bone_index, bone_name in enumerate(grimoire_bones_list)
        ]

    def get_bone_multi_advice(self) -> Advice:
        return Advice(
            label=f"Total Bone multi: {self.bone_multi.total:.3f}x",
            picture_class='grimoire'
        )

    def get_grimoire_talent_advice(self) -> Advice:
        db = self._grimoire_db
        return Advice(
            label=f"{self.grimoire_preset_level}/{self.max_book_level} booked Grimoire:"
                  f"<br>Max Preset Level {self.grimoire_preset_level + db.total_bonus_talent_levels} on "
                  f"{db.character_name} including bonus talent levels",
            picture_class='grimoire',
            progression=self.grimoire_preset_level,
            goal=self.max_book_level
        )

    def get_hood_advice(self) -> Advice:
        return Advice(
            label="Deathbringer Hood of Death: +25%",
            picture_class='deathbringer-hood-of-death',
            progression=int(self.hood_owned),
            goal=1,
            resource='gem'
        )

    def get_bovinae_stacks_text(self) -> str:
        return (
            f"<br>{self.bovinae_stacks:.3f} stacks = "
            f"{self.upgrades['Bovinae Hoarding'].total_value * self.bovinae_stacks:.3f}% total"
        )

    def get_graveyard_shift_advice(self) -> Advice:
        db = self._tombstone_db
        return Advice(
            label=f"{self.tombstone_preset_level}/{self.max_book_level} booked Graveyard Shift:"
                  f"<br>Max Preset Level {self.tombstone_preset_level + db.total_bonus_talent_levels} on "
                  f"{db.character_name} including bonus talent levels",
            picture_class='graveyard-shift',
            progression=self.tombstone_preset_level,
            goal=self.max_book_level
        )

    def get_tombstone_stacks_advice(self) -> Advice:
        per_stack = self.tombstone_per_stack
        return Advice(
            label=f"<br>Per stack: +{per_stack:.3f}%"
                  f"<br>50 stacks: {ValueToMulti(50 * per_stack):.3f}x"
                  f"<br>100 stacks: {ValueToMulti(100 * per_stack):.3f}x"
                  f"<br>200 stacks: {ValueToMulti(200 * per_stack):.3f}x"
                  f"<br>300 stacks: {ValueToMulti(300 * per_stack):.3f}x"
                  f"<br>500 stacks: {ValueToMulti(500 * per_stack):.3f}x",
            picture_class='graveyard-shift-tombstone',
            completed=True,
            informational=True
        )

    def get_total_upgrades_advice(self) -> Advice:
        return Advice(
            label=f"Total Grimoire Upgrades: {self.total_upgrades:,}",
            picture_class='grimoire'
        )
