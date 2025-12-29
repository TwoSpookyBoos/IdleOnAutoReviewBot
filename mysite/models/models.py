from typing import Union

from consts.consts_general import greenstack_amount, gstackable_codenames, gstackable_codenames_expected, quest_items_codenames, \
    greenstack_item_difficulty_groups
from utils.text_formatting import getItemCodeName, getItemDisplayName

# TODO: move Assets to their own file too once Nevar is merged
class Asset:
    def __init__(self, codename: Union[str, "Asset"], amount: float, name: str = "", **stats):
        if isinstance(codename, Asset):
            self.name: str = codename.name
            self.codename: str = codename.codename
            self.amount: float = codename.amount
            self.image: str = self.__image__(codename.codename, codename.name)
            self.quest: str = codename.quest
            self.quest_giver: str = codename.quest_giver
        else:
            self.name: str = name if name else getItemDisplayName(codename)
            self.codename: str = codename if codename else getItemCodeName(name)
            self.amount: float = amount
            self.image: str = self.__image__(codename, self.name)
            self.quest: str = ""
            self.quest_giver: str = ""
            self.stats = {}
            self.set_stats(stats)
            pass

    def __image__(self, codename: str, name: str) -> str:
        # codename == 'WorshipSkull11' and codename == 'WorshipSkull12' has same name.
        # Name used in picture_class processed by "kebab" that clash with each other.
        if codename == 'WorshipSkull12':
            return 'prehistoric-skull'
        return name

    def set_stats(self, stats: dict):
        wanted_stats = {
            'UQ1txt': 'misc_1_txt',
            'UQ1val': 'misc_1_val',
            'UQ2txt': 'misc_2_txt',
            'UQ2val': 'misc_2_val'
        }
        for key, value in stats.items():
            try:
                if value != 0:
                    self.stats[wanted_stats[key]] = value
                    pass
            except KeyError:
                pass

    def __eq__(self, other):
        match other:
            case str():
                return other == self.codename or other == self.name
            case Assets():
                return other.codename == self.codename and other.name == self.name

    def __str__(self):
        return f"{self.name}: {self.amount}"

    def __repr__(self):
        return f"<class {self.__class__.__name__}: {self.__str__()}>"

    def __hash__(self):
        return str(self.__dict__).__hash__()

    def __add__(self, other: Union["Asset", int]):
        return Asset(self, 0).add(other)

    def __iadd__(self, other: Union["Asset", int]):
        match other:
            case Asset():
                self.amount += other.amount
            case int():
                self.amount += other
            case _:
                print(f"RHS operand not of valid type: '{type(other)}'. Not added.")

        return self

    def add(self, other: Union["Asset", int]):
        return self.__iadd__(other)

    @property
    def greenstacked(self) -> bool:
        return self.amount >= greenstack_amount

    @property
    def progression(self) -> int:
        return self.amount * 100 // greenstack_amount

class Assets(dict):
    def __init__(self, assets: Union[dict[str, int], "Assets", None] = None):
        self.tiers = greenstack_item_difficulty_groups

        if assets is None:
            assets = dict()

        if isinstance(assets, Assets):
            super().__init__(
                tuple(
                    (codename, Asset(asset, 0)) for codename, asset in assets.items()
                )
            )
        else:
            super().__init__(
                tuple(
                    (codename, Asset(codename, count)) for codename, count in assets.items()
                )
            )

    def __add__(self, other: Union["Assets", Asset, dict[str, int]]):
        """Creates a new Assets object as a sum of the two Asset-like operands"""
        return Assets(self).add(other)

    def add(self, other):
        return self.__iadd__(other)

    def __iadd__(self, other: Union["Assets", Asset, dict[str, int]]):
        """Adds the other resource to self in-place"""
        match other:
            case Assets() | dict():
                for codename, asset in other.items():
                    self.get(codename).add(asset)
            case Asset():
                self.get(other.codename).add(other)
            case _:
                print(f"RHS operand not of valid type: '{type(other)}'. Not added.")

        return self

    def get(self, item, default=None):
        return super().get(item, default if default else Asset(item, 0))

    @property
    def items_gstacked(self) -> dict[str, Asset]:
        """Not used since it includes the "Cheater" group"""
        return {asset.codename: asset for asset in self.values() if asset.greenstacked}

    @property
    def items_gstacked_expected(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items_gstacked.items()
            if codename in gstackable_codenames
        }

    @property
    def items_gstacked_cheater(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items_gstacked.items()
            if codename not in gstackable_codenames_expected
        }

    @property
    def items_gstacked_unprecedented(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items_gstacked.items()
            if codename not in gstackable_codenames
        }

    @property
    def items_gstackable(self) -> dict[str, Asset]:
        """Not used since it includes the "Cheater" group"""
        return {
            codename: asset
            for codename, asset in self.items()
            if codename in gstackable_codenames and not asset.greenstacked
        }

    @property
    def items_gstackable_expected(self) -> dict[str, Asset]:
        return {
            codename: asset
            for codename, asset in self.items()
            if codename in gstackable_codenames_expected and not asset.greenstacked
        }

    @property
    def items_gstackable_tiered(self) -> dict[int, dict[str, list[Asset]]]:
        tiered = dict()

        for tier, categories in self.tiers.items():
            categorised = dict()
            for category, items in categories.items():
                item_list = [
                    self.get(item)
                    for item in items
                    if item in self.items_gstackable_expected
                    and self.get(item) not in self.quest_items_missed
                ]
                if item_list:
                    categorised[category] = sorted(item_list, key=lambda item: item.progression, reverse=True)
            if categorised:
                tiered["Timegated" if tier == 0 else tier] = categorised

        return tiered

    @property
    def quest_items(self) -> set[Asset]:
        return {self.get(codename) for codename in quest_items_codenames}

    @property
    def quest_items_gstacked(self) -> set[Asset]:
        return {asset for asset in self.quest_items if asset.greenstacked}

    @property
    def quest_items_gstackable(self) -> set[Asset]:
        return self.quest_items.difference(self.quest_items_gstacked)

    @property
    def quest_items_missed(self) -> set[Asset]:
        return self.quest_items.difference(self.quest_items_gstacked)

