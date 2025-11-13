from consts.consts_autoreview import break_you_best
from consts.consts_general import inventory_bags_dict, storage_chests_dict, inventory_slots_max_usable, inventory_accountwide_bags, \
    inventory_slots_max_usable_without_bundles
from models.general.models_consumables import StorageChest
from models.models import AdviceGroup, Advice, AdviceSection, Assets
from models.models_util import get_upgrade_vault_advice
from utils.data_formatting import safe_loads, mark_advice_completed
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)


def get_candy_hour_advicesections():
    bank: Assets = session_data.account.stored_assets

    # Standard Time Candies: 1hr - 72hr
    normal_candy = (bank.get(f"Timecandy{i}").amount for i in range(1, 7))
    normal_candy_times = 1, 2, 4, 12, 24, 72
    guaranteedCandyHours = sum(
        qty * hr
        for qty, hr in zip(normal_candy, normal_candy_times)
    )

    if guaranteedCandyHours > 0:
        tier_regular = str(guaranteedCandyHours)
        guaranteedCandyString = f"You have {guaranteedCandyHours:,} hours ({guaranteedCandyHours / 24:,.2f} days) of guaranteed candy."
    else:
        tier_regular = "no guaranteed candy"
        guaranteedCandyString = f"You have {tier_regular}. Wow."

    if guaranteedCandyHours >= 10000:
        guaranteedCandyString += "<br>Don't forget about them!"

    section_regular = AdviceSection(
        name="Regular Candy",
        tier=tier_regular,
        header=guaranteedCandyString,
        picture="Candy_1hr.png",
        unrated=True,
        informational=True,
        completed=guaranteedCandyHours == 0
    )

    # Variable Time Candies: Steamy, Spooky, Cosmic
    variable_candy = (bank.get(f"Timecandy{i}").amount for i in range(7, 10))
    variable_candy_times = (1/6, 24), (1/3, 12), (5, 500)
    variableCandyHoursMin = 0
    variableCandyHoursMax = 0

    for qty, (hrs_min, hrs_max) in zip(variable_candy, variable_candy_times):
        variableCandyHoursMin += qty * hrs_min
        variableCandyHoursMax += qty * hrs_max

    tier_variable = "no variable candy"
    variableCandyString = f"You have {tier_variable}."

    if variableCandyHoursMin > 0:
        hours_range = f"{variableCandyHoursMin:,.2f} - {variableCandyHoursMax:,.2f}"
        days_range = f"{variableCandyHoursMin / 24:,.2f} - {variableCandyHoursMax / 24:,.2f}"
        tier_variable = hours_range
        variableCandyString = f"You have somewhere between {hours_range} hours ({days_range} days) of variable candy."

    # TODO: Maybe Black / Divinity Pearls?

    section_variable = AdviceSection(
        name="Variable Candy",
        tier=tier_variable,
        header=variableCandyString,
        picture="Candy_Cosmic.png",
        unrated=True,
        informational=True,
        completed=variableCandyHoursMin == 0
    )

    return section_regular, section_variable


def get_inventory_advicegroup() -> AdviceGroup:
    inventorySlots_AdviceDict = {}
    characters_missing_usable_bag_slots = []

    inventory = session_data.account.inventory
    aw_owned = inventory['Account Wide Inventory Slots Owned']
    aw_max = inventory['Account Wide Inventory Slots Max']
    awi = inventory['Account Wide Inventory']
    aw_label = f"Account Wide: {aw_owned}/{aw_max} Inventory Slots for all characters"

    inventorySlots_AdviceDict[aw_label] = [
        Advice(
            label=f"{entry['Description']}: "
                  f"{entry['Owned Slots']}/{entry['Max Slots']} slots",
            picture_class=entry['Image'],
            progression=int(entry['Owned']),
            goal=1
        )
        for entry in awi.values()
    ]

    for character in session_data.account.all_characters:
        if (
            character.inventory_slots >= inventory_slots_max_usable
            or
            (
                character.inventory_slots == inventory_slots_max_usable_without_bundles
                and awi['Autoloot']['Owned'] is False
                and awi['bon_f']['Owned'] is False
            )
        ):
            continue
        else:
            subgroupName = (
                f"{character.character_name} the {character.class_name}: "
                f"{min(inventory_slots_max_usable, character.inventory_slots)}"
                f"/{inventory_slots_max_usable} usable Inventory slots"
            )
            inventorySlots_AdviceDict[subgroupName] = [
                Advice(
                    label=f"{bag.pretty_name}: {inventory_bags_dict[bag.value]} slots ({bag.type})",
                    picture_class=bag.pretty_name,
                    progression=0,
                    goal=1,
                    completed=False
                ) for bag in inventory['Characters Missing Bags'][character.character_index] if bag.pretty_name not in inventory_accountwide_bags
            ]

    for subgroupName in inventorySlots_AdviceDict:
        for advice in inventorySlots_AdviceDict[subgroupName]:
            mark_advice_completed(advice)

    inventorySlots_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Collect more inventory space',
        advices=inventorySlots_AdviceDict,
        informational=True
    )
    inventorySlots_AdviceGroup.remove_empty_subgroups()
    return inventorySlots_AdviceGroup

def get_storage_advicegroup() -> AdviceGroup:
    advices = {
        'Other Bonuses': [],
        'Usable Chests': []
    }

    storage = session_data.account.storage

    for source, details in storage['Other Storage'].items():
        if source == 'Event Shop':
            for bonus_name, bonus_slots in details.items():
                if not session_data.account.event_points_shop['Bonuses'][bonus_name]['Owned']:
                    advices['Other Bonuses'].append(Advice(
                        label=f"{{{{ Event Shop|#event-shop }}}}: {bonus_name}: {bonus_slots} slots",
                        picture_class=session_data.account.event_points_shop['Bonuses'][bonus_name]['Image'],
                        progression=0,
                        goal=1
                    ))
        elif source == 'Vault':
            for upgrade_name, upgrade_slots in details.items():
                if session_data.account.vault['Upgrades'][upgrade_name]['Total Value'] < session_data.account.vault['Upgrades'][upgrade_name]['Max Value']:
                    advices['Other Bonuses'].append(get_upgrade_vault_advice(upgrade_name))
        elif source == 'Construction Buildings':
            for building_name, building_slots in details.items():
                if session_data.account.construction_buildings[building_name]['Level'] < session_data.account.construction_buildings[building_name]['MaxLevel']:
                    advices['Other Bonuses'].append(Advice(
                        label=f"{{{{ Construction Building|#buildings }}}}: {building_name}: {building_slots} total slots",
                        picture_class=session_data.account.construction_buildings[building_name]['Image'],
                        progression=session_data.account.construction_buildings[building_name]['Level'],
                        goal=session_data.account.construction_buildings[building_name]['MaxLevel']
                    ))

    advices['Usable Chests'] = [
            Advice(
                label=f"{chest.pretty_name}: {storage_chests_dict[chest.value]} slots ({chest.type})",
                picture_class=chest.pretty_name,
                progression=0,
                goal=1,
                completed=False
            ) for chest in storage['Missing Chests']
        ]

    group = AdviceGroup(
        tier='',
        pre_string=(
            f"Collect {len(storage['Missing Chests'])} more storage chest{pl(storage['Missing Chests'])} for your bank"
            if advices else
            f"You've collected all current Storage Chests!{break_you_best}"
        ),
        advices=advices,
        informational=True
    )
    group.remove_empty_subgroups()

    return group


def get_consumables_advicesections():
    sections_candy = get_candy_hour_advicesections()
    group_bags = get_inventory_advicegroup()
    group_chests = get_storage_advicegroup()

    groups = [group for group in [group_bags, group_chests] if group]

    section_storage = AdviceSection(
        name="Storage",
        tier="",
        header=(
            f"Collect more space for your bank and inventories:"
            if groups else
            f"You've collected all current Storage Chests and Inventory Bags!{break_you_best}"
        ),
        picture="Cosmic_Storage_Chest.png",
        groups=groups,
        unrated=True,
    )

    return *sections_candy, section_storage
