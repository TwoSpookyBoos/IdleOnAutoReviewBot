from enum import IntEnum
from utils.logging import get_logger

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
        return self.name.replace("_", " ").title().replace('Fourth', '4th')


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
    STORAGE_CHEST_29 = 28
    STORAGE_CHEST_30 = 29
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
    BURIED_TREASURE_CHEST = 107

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
            cls.STORAGE_CHEST_29, cls.STORAGE_CHEST_30
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
            cls.HOLIDAY_CHEST, cls.VALENSLIME_CHEST, cls.BURIED_TREASURE_CHEST
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
    FOURTH_ANNIVERSARY_BAG = 112  #Cannot start with a number, bummer
    TREASURE_TOTEBAG = 113
    RUCKSACK_OF_RICHES = 114
    LOOT_LUGGAGE = 115

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
            cls.RUCKSACK_OF_RICHES, cls.LOOT_LUGGAGE
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
