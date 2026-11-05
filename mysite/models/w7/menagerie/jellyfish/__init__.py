from typing import TYPE_CHECKING, Literal, overload

from consts.w7.menagerie import menagerie_jellyfish
from models.w7.menagerie.jellyfish.blue import BlueJellyfish
from models.w7.menagerie.jellyfish.green import GreenJellyfish
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from models.w7.menagerie.jellyfish.lumi import LumiJellyfish
from models.w7.menagerie.jellyfish.pink import PinkJellyfish
from models.w7.menagerie.jellyfish.red import RedJellyfish
from models.w7.menagerie.jellyfish.silver import SilverJellyfish
from models.w7.menagerie.jellyfish.yellow import YellowJellyfish

if TYPE_CHECKING:
    from models.w7.menagerie import Menagerie


class Jellyfishes(dict[str, Jellyfish]):
    # In "Jelliefish" PersonalNUM order, matching `menagerie_jellyfish`
    _JELLYFISH_TYPES = (
        LumiJellyfish,
        PinkJellyfish,
        BlueJellyfish,
        RedJellyfish,
        SilverJellyfish,
        YellowJellyfish,
        GreenJellyfish,
    )

    def __init__(self, raw_menagerie: list, menagerie: "Menagerie"):
        super().__init__()
        for index, (cls, info) in enumerate(
            zip(self._JELLYFISH_TYPES, menagerie_jellyfish)
        ):
            jellyfish = cls(index, info, menagerie)
            jellyfish.parse_feature(raw_menagerie)
            self[jellyfish.name] = jellyfish

    @overload
    def __getitem__(self, key: Literal["Menagerie Jellyfish"]) -> LumiJellyfish: ...
    @overload
    def __getitem__(self, key: Literal["Pink Jellyfish"]) -> PinkJellyfish: ...
    @overload
    def __getitem__(self, key: Literal["Blue Jellyfish"]) -> BlueJellyfish: ...
    @overload
    def __getitem__(self, key: Literal["Red Jellyfish"]) -> RedJellyfish: ...
    @overload
    def __getitem__(self, key: Literal["Silver Jellyfish"]) -> SilverJellyfish: ...
    @overload
    def __getitem__(self, key: Literal["Yellow Jellyfish"]) -> YellowJellyfish: ...
    @overload
    def __getitem__(self, key: Literal["Green Jellyfish"]) -> GreenJellyfish: ...
    @overload
    def __getitem__(self, key: str) -> Jellyfish: ...
    def __getitem__(self, key: str) -> Jellyfish:
        return super().__getitem__(key)
