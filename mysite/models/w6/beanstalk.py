from consts.general.golden_food import golden_food_data
from consts.w6.beanstalk import (
    golden_food_max_tier,
    golden_food_tier_require,
    golden_food_order,
)

from models.advice.advice import Advice
from models.general.golden_food import GoldenFood

from utils.number_formatting import parse_number
from utils.safer_data_handling import safe_loads, safer_index
from utils.text_formatting import notateNumber

from utils.logging import get_logger

logger = get_logger(__name__)


class BeanstalkDeposit(GoldenFood):

    def __init__(self, golden_food_name: str, tier: int):
        self.tier = tier
        amount = golden_food_tier_require[tier]
        super().__init__(golden_food_name, amount)

    def calculate_bonus(self, golden_food_multi):
        max_amount = None
        if self.tier < golden_food_max_tier:
            max_amount = golden_food_tier_require[golden_food_max_tier]
        super().calculate_bonus(golden_food_multi, max_amount)

    def next_tier_progress_advice(self, amount: int) -> Advice | None:
        next_tier = self.tier + 1
        if next_tier > golden_food_max_tier:
            logger.error(f"Can't create advice for max tier Golden Food: {self.name}")
            return None

        next_tier_require = golden_food_tier_require[next_tier]
        if amount >= next_tier_require:
            progress = notateNumber("Basic", next_tier_require, 0)
            goal = "Deposit"
        else:
            goal = notateNumber("Basic", next_tier_require, 0)
            progress = notateNumber("Match", amount, 0, matchString=goal)
        golden_food_info = golden_food_data.get(self.name, {})
        resource = golden_food_info.get("Resource Image", "placeholder")
        source = golden_food_info.get("Source", "Unknown")
        return Advice(
            label=f"{self.name}: {source}",
            picture_class=self.name,
            progression=progress,
            goal=goal,
            resource=resource,
        )

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        advice = super().get_bonus_advice(link_to_section)
        advice.change_progress(self.tier, golden_food_max_tier)
        return advice

    def alert_advice(self, have_amount: int) -> Advice | None:
        next_tier = self.tier + 1
        if next_tier > golden_food_max_tier:
            return None
        next_tier_require = golden_food_tier_require[next_tier]
        if have_amount < next_tier_require:
            return None
        return Advice(
            label=f"{{{{Beanstalk|#beanstalk}}}} - {self.name} is ready to deposit!",
            picture_class="beanstalk",
            resource=self.name,
        )


class Beanstalk(dict[str, BeanstalkDeposit]):
    """
    Class for Beanstalk and Golden Food that deposited to it.
    Use Beanstalk[golden_food_name] to get deposited info.
    """

    def __init__(self, raw_data: dict):
        raw_ninja_list = safe_loads(raw_data.get("Ninja", []))
        raw_beanstalk_list = safer_index(raw_ninja_list, 104, [])
        if not raw_beanstalk_list:
            logger.warning("Beanstalk data not present")
            raw_beanstalk_list = [0] * len(golden_food_order)
        for index, golden_food_name in enumerate(golden_food_order):
            tier = raw_beanstalk_list[index]
            self[golden_food_name] = BeanstalkDeposit(golden_food_name, tier)
        raw_optlacc = raw_data.get("OptLacc", [])
        self.unlocked_tier = int(parse_number(safer_index(raw_optlacc, 475, 0), 0) >= 1)
        self.golden_food_multi = 1

    def calculate_unlocked_tier(self, emporium):
        tier_1 = emporium["Gold Food Beanstalk"]
        tier_2 = emporium["Supersized Gold Beanstacking"]
        self.unlocked_tier += int(tier_1["Obtained"]) + int(tier_2["Obtained"])

    def calculate_golden_food_multi(self):
        # TODO: add calculate Golden Food Bonus Multi
        self.golden_food_multi = 1
        return self.golden_food_multi

    def calculate_bonuses(self):
        for deposit in self.values():
            deposit.calculate_bonus(self.golden_food_multi)
