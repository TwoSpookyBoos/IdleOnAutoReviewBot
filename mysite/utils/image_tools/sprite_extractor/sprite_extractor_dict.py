from typing import Dict, TypedDict, Optional

# a dict to specify which symbol of the font sheet should be parsed.
# Key: the index of the symbol.
# Value: the filename (without the `.png`) it should be saved as
FontDefinition = Dict[int, str]


class SpritesheetDefinition(TypedDict):
    base_file_name: str # shared prefix of each file in the Spritesheet. Individual files then just append their index, e.g. "File0", "File1", "File2", etc.
    columns: int
    rows: int
    num_sprites: Optional[int] # if there are trailing empty slots in the sprite sheet, limit the amount of files generated


sprite_extractor_dict: Dict[str, FontDefinition | SpritesheetDefinition] = {
    "font-6.fnt": {
        97: "AlchemyLiquid0",
        98: "AlchemyLiquid1",
        99: "AlchemyLiquid2",
        100: "AlchemyLiquid3"
    },
    "font-95.fnt": {
        33945: "BasketballShopCurrency",
        32435: "DartsShopCurrency"
    },
    "sprite-673-16.png": {
        "base_file_name": "SummoningStone",
        "columns": 3,
        "rows": 3,
        "num_sprites": 7
    },
    "sprite-84-101.png": {
        "base_file_name": "HumbleHugh",
        "columns": 3,
        "rows": 3,
        "num_sprites": 1
    },
    "sprite-673-33.png": {
        "base_file_name": "Whallamus",
        "columns": 4,
        "rows": 4,
        "num_sprites": 1
    }
}
