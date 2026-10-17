from consts.consts_general import greenstack_amount
from consts.consts_w2 import fishing_toolkit_dict
from consts.consts_w5 import filter_never, filter_only_after_gstack, filter_recipes
from models.advice.advice import Advice
from models.general.assets import Assets
from utils.safer_data_handling import safe_loads, safer_index
from utils.text_formatting import getItemDisplayName


class ItemFilter(list[str]):
    """Item codenames in the loot filter"""

    def __init__(self, raw_data: dict):
        super().__init__()
        # Filter slots start at PrinterXtra[120]
        raw_printer_xtra = safe_loads(raw_data.get("PrinterXtra", []))
        if len(raw_printer_xtra) >= 121:
            self.extend(
                codename for codename in raw_printer_xtra[120:] if codename != "Blank"
            )
        raw_toolkit = safe_loads(
            raw_data.get("FamValFishingToolkitOwned", [{"0": 0, "length": 1}])
        )
        self._toolkit_lures: dict = safer_index(raw_toolkit, 0, {})
        self._toolkit_lines: dict = safer_index(raw_toolkit, 1, {})

    def get_alerts(
        self,
        slab: set[str],
        stored_assets: Assets,
        all_assets: Assets,
        autoloot: bool,
        luckier_lad_dream_completed: bool,
    ) -> list[Advice]:
        alerts = []
        lucky_lads = stored_assets.get("Trophy2").amount
        if lucky_lads >= 75 and luckier_lad_dream_completed:
            alerts.append(
                Advice(
                    label=f"You have {lucky_lads}/75 Lucky Lads "
                    f"to craft a Luckier Lad!",
                    picture_class="luckier-lad",
                )
            )
        for codename in self:
            name = getItemDisplayName(codename)
            if codename == "Trophy2" and "Trophy20" not in slab and lucky_lads < 75:
                alerts.append(
                    Advice(
                        label="Lucky Lad filtered before 75 for Luckier Lad",
                        picture_class="lucky-lad",
                        resource="luckier-lad",
                    )
                )
            elif codename in filter_recipes:
                alerts.extend(
                    Advice(
                        label=f"{name} filtered, "
                        f"{getItemDisplayName(craftable)} not in Slab",
                        picture_class=name,
                        resource=craftable,
                    )
                    for craftable in filter_recipes[codename]
                    if craftable not in slab
                )
            elif codename in filter_never and autoloot:
                alerts.append(
                    Advice(label=f"Why did you filter {name}?", picture_class=name)
                )
            elif (
                codename in filter_only_after_gstack
                and autoloot
                and all_assets.get(codename).amount < greenstack_amount
            ):
                alerts.append(
                    Advice(
                        label=f"Unfilter {name} until Greenstacked", picture_class=name
                    )
                )
            elif codename not in slab:
                alerts.append(
                    Advice(label=f"{name} filtered, not in Slab", picture_class=name)
                )
            elif self._missing_from_toolkit(codename):
                alerts.append(
                    Advice(
                        label=f"{name} filtered, not in Fishing Toolkit",
                        picture_class=name,
                    )
                )
        return alerts

    def _missing_from_toolkit(self, codename: str) -> bool:
        # index + 1 skips the default lure/line, which isn't a Slab item
        for kind, owned in (
            ("Lures", self._toolkit_lures),
            ("Lines", self._toolkit_lines),
        ):
            if codename in fishing_toolkit_dict[kind]:
                return (
                    fishing_toolkit_dict[kind].index(codename) + 1 not in owned.values()
                )
        return False
