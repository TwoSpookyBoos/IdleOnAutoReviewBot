from consts.consts_w1 import event_points_shop_dict
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_get

logger = get_logger(__name__)


class EventShopBonus:
    def __init__(self, name: str, info: dict, owned: bool):
        self.name: str = name
        self.owned: bool = owned
        self.cost: int = info["Cost"]
        self.description: str = info["Description"]
        self.image: str = info["Image"]

    def get_advice(self, points_total: int) -> Advice:
        return Advice(
            label=f"{self.name}: {self.description}",
            picture_class=self.image,
            progression=1 if self.owned else points_total,
            goal=1 if self.owned else self.cost,
            resource="event-point" if not self.owned else "",
        )

    def get_bonus_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Event Shop|#event-shop }}}} - {self.name}: {self.description}",
            picture_class=self.image,
            progression=int(self.owned),
            goal=1,
        )


class EventShop(dict[str, EventShopBonus]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.points_owned: int = safer_get(raw_optlacc, 310, 0)
        raw_purchases = safer_get(raw_optlacc, 311, "")
        if isinstance(raw_purchases, str):
            purchased_codes = list(raw_purchases)
        else:
            logger.warning(
                f"Event Shop Purchases not String type: {type(raw_purchases)} "
                f"with value of: {raw_purchases}"
            )
            purchased_codes = []
        for name, info in event_points_shop_dict.items():
            self[name] = EventShopBonus(name, info, info["Code"] in purchased_codes)
