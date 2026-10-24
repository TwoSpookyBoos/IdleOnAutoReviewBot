from consts.consts_item_data import raw_item_data
from models.general.assets import Asset
from utils.safer_data_handling import safe_loads, safer_convert


class Equipment:
    def __init__(self, raw_data, toon_index, safeStatus: bool):
        if safeStatus:
            order = raw_data.get(f"EquipOrder_{toon_index}", [])
            quantity = raw_data.get(f"EquipQTY_{toon_index}", [])

            equips_data = safe_loads(raw_data.get(f'EMm0_{toon_index}', ''))
            equips_data = [{index: item_data} for index, item_data in equips_data.items()]
            for i in range(len(order[0]) - 1):
                key = str(i)
                if not any(key in d.keys() for d in equips_data):
                    equips_data.insert(i, {key: {}})
            equips_data = sorted(equips_data, key=lambda sub_dict: int(list(sub_dict.keys())[0]))
            equips_data = [list(item.values())[0] for item in equips_data]
            equips_data = [equips_data, [{} for _ in range(len(order[1]) - 1)], [{} for _ in range(len(order[2]) - 1)]]

            groups = list()
            for o, q, d in zip(order, quantity, equips_data):
                o.pop("length", None)
                q.pop("length", None)
                o = dict(sorted(o.items(), key=lambda i: int(i[0]))).values()
                q = dict(sorted(q.items(), key=lambda i: int(i[0]))).values()
                groups.append([Asset(name, float(count), **stats) for name, count, stats in zip(o, q, d)])

            inv_order = raw_data.get(f"InventoryOrder_{toon_index}", [])
            inv_quantity = raw_data.get(f"ItemQTY_{toon_index}", [])
            all_inventory = {}
            for o, q in zip(inv_order, inv_quantity):
                if o in all_inventory:
                    all_inventory[o] += safer_convert(q, 0.0)
                else:
                    all_inventory[o] = safer_convert(q, 0.0)
            groups.append([Asset(name, count) for name, count in all_inventory.items()])

            # equips, tools, foods = groups

            self.equips = groups[0] if groups else []
            self.tools = groups[1] if groups else []
            self.foods = groups[2] if groups else []
            self.inventory = groups[3] if groups else []
        else:
            self.equips = []
            self.tools = []
            self.foods = []
            self.inventory = []

    def get_misc_bonus(self, slot: int, codename: str, tools: bool = False) -> float:
        items = self.tools if tools else self.equips
        if slot >= len(items):
            return 0
        item = items[slot]
        item_data = raw_item_data.get(item.codename, {})
        total = 0
        for line in (1, 2):
            item_text = item_data.get(f"Misc {line} (Text)", "0")
            rolled_text = item.stats.get(f"misc_{line}_txt", "0")
            rolled_value = safer_convert(item.stats.get(f"misc_{line}_val", 0), 0)
            # Rolled text only when item has none
            text = rolled_text if item_text == "0" and rolled_value > 0 else item_text
            if text == codename:
                base_value = safer_convert(item_data.get(f"Misc {line} (Value)", 0), 0)
                total += base_value + rolled_value
        return total

    def get_item_misc_bonus(self, item: Asset, codenames: tuple[str, ...]) -> float:
        for tools, items in ((False, self.equips), (True, self.tools)):
            for slot, worn in enumerate(items):
                if worn is item:
                    return sum(
                        self.get_misc_bonus(slot, codename, tools=tools)
                        for codename in codenames
                    )
        return 0
