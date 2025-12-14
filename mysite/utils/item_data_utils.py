from consts.generated.item_data import item_data

def get_item_from_codename(codename: str) -> dict:
    return next(item for code, item in item_data.items() if code == codename)

def get_all_stamps():
    return [item for item in item_data.values() if 'Type' in item and item['Type'] == "STAMP"]

def get_capacity_stamps():
    return [stamp for stamp in get_all_stamps() if 'Carry Cap' in stamp['Stamp Bonus']['Effect']]