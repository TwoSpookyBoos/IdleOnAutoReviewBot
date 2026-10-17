from utils.safer_data_handling import safe_loads


class Slab(set[str]):
    """Item codenames registered in The Slab"""

    def __init__(self, raw_data: dict):
        super().__init__(safe_loads(raw_data.get("Cards1", [])))
