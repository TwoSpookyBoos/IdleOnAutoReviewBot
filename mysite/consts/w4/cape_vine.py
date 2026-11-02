from consts.consts_item_data import ITEM_DATA

# MenuType2 110 in source: every cape but Lava Wings. Last updated in v2.561.0
cape_vine_capes = [
    item
    for item in ITEM_DATA.values()
    if item.type == "CAPE" and item.code_name != "EquipmentCape1"
]
