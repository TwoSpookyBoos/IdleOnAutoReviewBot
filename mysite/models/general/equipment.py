from models.models import Asset
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
