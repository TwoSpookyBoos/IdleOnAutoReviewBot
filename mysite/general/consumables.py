from enum import IntEnum
from consts import expectedInventoryBagValuesDict, expectedStorageChestValuesDict, break_you_best, currentMaxUsableInventorySlots
from models.models import AdviceGroup, Advice, AdviceSection, Assets
from utils.data_formatting import safe_loads, mark_advice_completed
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)


class StorageItemMixin:
    @classmethod
    def is_from_quest(cls, chest):
        return chest in cls.from_quest()

    @classmethod
    def is_dropped(cls, chest):
        return chest in cls.dropped()

    @classmethod
    def is_from_gem_shop(cls, chest):
        return chest in cls.from_gem_shop()

    @classmethod
    def is_from_vendor_shop(cls, chest):
        return chest in cls.from_vendor_shop()

    @classmethod
    def is_limited(cls, chest):
        return chest in cls.limited()

    @classmethod
    def is_crafted(cls, chest):
        return chest in cls.crafted()

    @property
    def type(self):
        if self.__class__.is_from_quest(self):
            return "Quest"
        if self.__class__.is_dropped(self):
            return "Dropped"
        if self.__class__.is_from_vendor_shop(self):
            return "Vendor"
        if self.__class__.is_from_gem_shop(self):
            return "Gem Shop"
        if self.__class__.is_crafted(self):
            return "Crafted"
        if self.__class__.is_limited(self):
            return "Limited Availability"

        return f"Unknown {self.__class__.__name__} {self.value}"

    @property
    def pretty_name(self):
        return self.name.replace("_", " ").title()

class StorageChest(StorageItemMixin, IntEnum):
    STORAGE_CHEST_1 = 0
    STORAGE_CHEST_2 = 1
    STORAGE_CHEST_3 = 2
    STORAGE_CHEST_4 = 3
    STORAGE_CHEST_5 = 4
    STORAGE_CHEST_6 = 5
    STORAGE_CHEST_7 = 6
    STORAGE_CHEST_8 = 7
    STORAGE_CHEST_9 = 8
    STORAGE_CHEST_10 = 9
    STORAGE_CHEST_11 = 10
    STORAGE_CHEST_12 = 11
    STORAGE_CHEST_13 = 12
    STORAGE_CHEST_14 = 14
    STORAGE_CHEST_15 = 13
    STORAGE_CHEST_16 = 15
    STORAGE_CHEST_17 = 16
    STORAGE_CHEST_18 = 17
    STORAGE_CHEST_19 = 18
    STORAGE_CHEST_20 = 19
    STORAGE_CHEST_21 = 20
    STORAGE_CHEST_22 = 21
    STORAGE_CHEST_23 = 22
    STORAGE_CHEST_24 = 23
    STORAGE_CHEST_25 = 24
    STORAGE_CHEST_26 = 25
    STORAGE_CHEST_27 = 26
    STORAGE_CHEST_28 = 27
    STORAGE_CHEST_90 = 30
    STORAGE_CHEST_91 = 31
    STORAGE_CHEST_92 = 32
    STORAGE_CHEST_93 = 33
    STORAGE_CHEST_94 = 34
    STORAGE_CHEST_95 = 35
    STORAGE_CHEST_96 = 36
    STORAGE_CHEST_97 = 37
    STORAGE_CHEST_98 = 38
    STORAGE_CHEST_99 = 39
    STORAGE_CHEST_99B = 40
    STORAGE_CHEST_99C = 41
    DANK_PAYPAY_CHEST = 100
    GELATINOUS_CHEST = 101
    CHEESY_CHEST = 102
    WOODLIN_CHEST = 103
    NINJA_CHEST = 104
    HOLIDAY_CHEST = 105
    VALENSLIME_CHEST = 106

    @classmethod
    def dropped(cls):
        return (
            cls.STORAGE_CHEST_14, cls.STORAGE_CHEST_22, cls.STORAGE_CHEST_23,
            cls.STORAGE_CHEST_24, cls.STORAGE_CHEST_25,
            cls.DANK_PAYPAY_CHEST, cls.GELATINOUS_CHEST, cls.CHEESY_CHEST,
            cls.WOODLIN_CHEST
        )

    @classmethod
    def from_vendor_shop(cls):
        return (
            cls.STORAGE_CHEST_2, cls.STORAGE_CHEST_6, cls.STORAGE_CHEST_7,
            cls.STORAGE_CHEST_8, cls.STORAGE_CHEST_9, cls.STORAGE_CHEST_10,
            cls.STORAGE_CHEST_12, cls.STORAGE_CHEST_13, cls.STORAGE_CHEST_15,
            cls.STORAGE_CHEST_16, cls.STORAGE_CHEST_17, cls.STORAGE_CHEST_18,
            cls.STORAGE_CHEST_19, cls.STORAGE_CHEST_20, cls.STORAGE_CHEST_21,
            cls.STORAGE_CHEST_26, cls.STORAGE_CHEST_27, cls.STORAGE_CHEST_28,
        )

    @classmethod
    def from_gem_shop(cls):
        return (
            cls.STORAGE_CHEST_90, cls.STORAGE_CHEST_91, cls.STORAGE_CHEST_92,
            cls.STORAGE_CHEST_93, cls.STORAGE_CHEST_94, cls.STORAGE_CHEST_95,
            cls.STORAGE_CHEST_96, cls.STORAGE_CHEST_97, cls.STORAGE_CHEST_98,
            cls.STORAGE_CHEST_99, cls.STORAGE_CHEST_99B, cls.STORAGE_CHEST_99C,
        )

    @classmethod
    def from_quest(cls):
        return (
            cls.STORAGE_CHEST_1, cls.STORAGE_CHEST_3, cls.STORAGE_CHEST_4,
            cls.STORAGE_CHEST_5, cls.STORAGE_CHEST_11, cls.NINJA_CHEST
        )

    @classmethod
    def limited(cls):
        return (
            cls.HOLIDAY_CHEST, cls.VALENSLIME_CHEST
        )

    @classmethod
    def crafted(cls):
        return tuple()

class Bag(StorageItemMixin, IntEnum):
    INVENTORY_BAG_A = 0
    INVENTORY_BAG_B = 1
    INVENTORY_BAG_C = 2
    INVENTORY_BAG_D = 3
    INVENTORY_BAG_E = 4
    INVENTORY_BAG_F = 5
    INVENTORY_BAG_G = 6
    INVENTORY_BAG_H = 7
    INVENTORY_BAG_U = 20
    INVENTORY_BAG_V = 21
    INVENTORY_BAG_W = 22
    INVENTORY_BAG_X = 23
    INVENTORY_BAG_Y = 24
    INVENTORY_BAG_Z = 25
    SNAKESKINVENTORY_BAG = 100
    TOTALLY_NORMAL_AND_NOT_FAKE_BAG = 101
    BLUNDERBAG = 102
    SANDY_SATCHEL = 103
    BUMMO_BAG = 104
    CAPITALIST_CASE = 105
    WEALTHY_WALLET = 106
    PROSPEROUS_POUCH = 107
    SACK_OF_SUCCESS = 108
    SHIVERING_SACK = 109
    MAMOOTH_HIDE_BAG = 110
    PEEPER_POUCH = 111
    FOURTH_ANNIVERSARY_BAG = 112
    TREASURE_TOTEBAG = 113
    RUCKSACK_OF_RICHES = 114

    @classmethod
    def dropped(cls):
        return (
            cls.SNAKESKINVENTORY_BAG, cls.TOTALLY_NORMAL_AND_NOT_FAKE_BAG,
            cls.INVENTORY_BAG_G, cls.MAMOOTH_HIDE_BAG
        )

    @classmethod
    def from_vendor_shop(cls):
        return (
            cls.BUMMO_BAG, cls.CAPITALIST_CASE, cls.WEALTHY_WALLET,
            cls.PROSPEROUS_POUCH, cls.SACK_OF_SUCCESS, cls.TREASURE_TOTEBAG,
            cls.RUCKSACK_OF_RICHES
        )

    @classmethod
    def from_gem_shop(cls):
        return (
            cls.INVENTORY_BAG_U, cls.INVENTORY_BAG_V, cls.INVENTORY_BAG_W,
            cls.INVENTORY_BAG_X, cls.INVENTORY_BAG_Y, cls.INVENTORY_BAG_Z
        )

    @classmethod
    def from_quest(cls):
        return (
            cls.INVENTORY_BAG_A, cls.INVENTORY_BAG_B, cls.INVENTORY_BAG_C,
            cls.INVENTORY_BAG_D, cls.INVENTORY_BAG_E, cls.INVENTORY_BAG_F,
            cls.INVENTORY_BAG_H
        )

    @classmethod
    def crafted(cls):
        return cls.BLUNDERBAG, cls.SANDY_SATCHEL, cls.SHIVERING_SACK, cls.PEEPER_POUCH

    @classmethod
    def limited(cls):
        return cls.FOURTH_ANNIVERSARY_BAG,


def getCandyHourSections():
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


def getBagType(inputBagNumber):
    return getStorageItemType(inputBagNumber, Bag)


def getChestType(inputChestNumber):
    return getStorageItemType(inputChestNumber, StorageChest)


def getStorageItemType(storageItemIndex, cls):
    try:
        bag = cls(int(storageItemIndex))
    except ValueError as e:
        logger.exception(f"failed to parse {cls.__name__} '{storageItemIndex = }'", exc_info=e)
        return f"Unknown Bag '{storageItemIndex}'"

    return bag.type

def parseInventoryBagSlots() -> AdviceGroup:
    inventorySlots_AdviceDict = {}
    currentMaxInventorySlots = 96  #As of v2.35 4th Anniversary
    currentMaxWithoutAutoloot = currentMaxInventorySlots - 5
    defaultInventorySlots = 16  # Characters have 16 inventory slots by default
    account_wide_inventory_bags = ['Fourth Anniversary Bag']
    character_bag_dict = {}
    character_missing_bags_dict = {}
    character_bag_slots_dict = {}
    characters_with_max_bag_slots = []
    characters_missing_usable_bag_slots = []

    fourth_anni_bag_owned = any([char.character_name for char in session_data.account.all_characters if '112' in char.inventory_bags])
    aw_total = (
        defaultInventorySlots
        + (5 * session_data.account.autoloot)
        + (3 * session_data.account.event_points_shop['Bonuses']['Secret Pouch']['Owned'])
        + (8 * fourth_anni_bag_owned)
    )
    aw_max = defaultInventorySlots + 5 + 3 + 8
    aw_label = f"Account Wide: {aw_total}/{aw_max} Inventory Slots for all characters"
    inventorySlots_AdviceDict[aw_label] = [
        Advice(
            label=f"Base: 16 slots",
            picture_class='ui-inventory-bag-0',
            progression=1,
            goal=1
        ),
        Advice(
            label=f"Autoloot Bundle: 5 slots",
            picture_class='cash',
            progression=int(session_data.account.autoloot),
            goal=1
        ),
        Advice(
            label=f"{{{{ Event Shop|#event-shop }}}}: Secret Pouch: 3 slots",
            picture_class='event-shop-12',
            progression=int(session_data.account.event_points_shop['Bonuses']['Secret Pouch']['Owned']),
            goal=1
        ),
        Advice(
            label=f"4th Anniversary Bag: 8 slots (Limited Availability)",
            picture_class='fourth-anniversary-bag',
            progression=int(fourth_anni_bag_owned),
            goal=1
        )
    ]

    for character in session_data.account.all_characters:
        character_bag_dict[character.character_index] = character.inventory_bags
        character_missing_bags_dict[character.character_index] = [bag for bag in Bag if str(bag.value) not in character.inventory_bags]

    for chararacter_index, bagDict in character_bag_dict.items():
        sumSlots = aw_total
        for bag in bagDict:
            if isinstance(bagDict[bag], int | float | str):
                try:
                    sumSlots += int(bagDict[bag])
                except:
                    logger.exception(f"Could not increase character {chararacter_index}'s bagslots by {type(bagDict[bag])} {bagDict[bag]}")
            else:
                logger.warning(f"Funky bag value found in {chararacter_index}'s bagsDict for bag {bag}: {type(bagDict[bag])} {bagDict[bag]}. Searching for expected value.")
                if int(bag) in expectedInventoryBagValuesDict:
                    logger.debug(f"Bag {bag} has a known value: {expectedInventoryBagValuesDict.get(int(bag), 0)}. All is well :)")
                else:
                    logger.error(f"Bag {bag} has no known value. Defaulting to 0 :(")
                sumSlots += expectedInventoryBagValuesDict.get(int(bag), 0)
        character_bag_slots_dict[chararacter_index] = sumSlots
        if sumSlots >= currentMaxUsableInventorySlots:
            characters_with_max_bag_slots.append(chararacter_index)
        elif sumSlots == currentMaxWithoutAutoloot and session_data.account.autoloot == False:
            characters_with_max_bag_slots.append(chararacter_index)
        else:
            characters_missing_usable_bag_slots.append(chararacter_index)
    # logger.info(f"character_bag_dict: {character_bag_dict}")
    # logger.info(f"characters_missing_usable_bag_slots: {characters_missing_usable_bag_slots}")
    for character_index in characters_missing_usable_bag_slots:
        subgroupName = (
            f"{session_data.account.all_characters[character_index].character_name}"
            f" the {session_data.account.all_characters[character_index].class_name}: "
            f"{min(currentMaxUsableInventorySlots, character_bag_slots_dict[character_index])}"
            f"/{currentMaxUsableInventorySlots} usable Inventory slots"
        )
        inventorySlots_AdviceDict[subgroupName] = [
            Advice(
                label=f"{bag.pretty_name}: {expectedInventoryBagValuesDict[bag.value]} slots ({bag.type})",
                picture_class=bag.pretty_name,
                progression=0,
                goal=1,
                completed=False
            ) for bag in character_missing_bags_dict[character_index] if bag.pretty_name not in account_wide_inventory_bags
        ]

    for subgroupName in inventorySlots_AdviceDict:
        for advice in inventorySlots_AdviceDict[subgroupName]:
            mark_advice_completed(advice)

    inventorySlots_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Collect more inventory space",
        advices=inventorySlots_AdviceDict,
        informational=True
    )
    inventorySlots_AdviceGroup.remove_empty_subgroups()
    return inventorySlots_AdviceGroup

def parseStorageChests():
    usedStorageChests = safe_loads(session_data.account.raw_data.get('InvStorageUsed', []))
    missing_chests = [chest for chest in StorageChest if str(chest.value) not in usedStorageChests.keys()]
    other_storage = {
        'Event Shop': {
            'Storage Chest': 12,
            'Storage Vault': 16
        },
        'Vault': {
            'Storage Slots': session_data.account.vault['Upgrades']['Storage Slots']['Max Level']
        },
        'Construction Buildings': {
            'Chest Space': 2 * (session_data.account.construction_buildings['Chest Space']['MaxLevel'] - 1)
        },
    }

    advices = {
        'Other Bonuses': [],
        'Usable Chests': []
    }

    for source, details in other_storage.items():
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
                if session_data.account.vault['Upgrades'][upgrade_name]['Level'] < upgrade_slots:
                    advices['Other Bonuses'].append(Advice(
                        label=f"{{{{ Upgrade Vault|#upgrade-vault }}}}: {upgrade_name}: {upgrade_slots} total slots",
                        picture_class=session_data.account.vault['Upgrades'][upgrade_name]['Image'],
                        progression=session_data.account.vault['Upgrades'][upgrade_name]['Level'],
                        goal=session_data.account.vault['Upgrades'][upgrade_name]['Max Level']
                    ))
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
                label=f"{chest.pretty_name}: {expectedStorageChestValuesDict[chest.value]} slots ({chest.type})",
                picture_class=chest.pretty_name,
                completed=False
            ) for chest in missing_chests
        ]

    group = AdviceGroup(
        tier="",
        pre_string=(
            f"Collect {len(missing_chests)} more storage chest{pl(missing_chests)} for your bank"
            if advices else
            f"You've collected all current Storage Chests!{break_you_best}"
        ),
        advices=advices,
        informational=True
    )
    group.remove_empty_subgroups()

    return group


def getConsumablesAdviceSections():
    sections_candy = getCandyHourSections()
    group_bags = parseInventoryBagSlots()
    group_chests = parseStorageChests()

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
