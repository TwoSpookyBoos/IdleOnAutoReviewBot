from typing import Dict, TypedDict, Optional

FontDefinition = Dict[int, str]


class SpritesheetDefinition(TypedDict):
    base_name: str
    width: int
    height: int
    num_sprites: Optional[int]


sprite_extractor_dict: Dict[str, FontDefinition | SpritesheetDefinition] = {
    "font-6.fnt": {
        97: "AlchemyLiquid0",
        98: "AlchemyLiquid1",
        99: "AlchemyLiquid2",
        100: "AlchemyLiquid3"
    },
    "sprite-673-16.png": {
        "base_name": "SummoningStone",
        "width": 3,
        "height": 3,
        "num_sprites": 7
    }
}
