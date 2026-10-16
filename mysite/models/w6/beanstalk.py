from consts.consts_item_data import raw_item_data
from consts.general.golden_food import golden_food_data
from consts.w6.beanstalk import (
    golden_food_max_tier,
    golden_food_tier_require,
    golden_food_order,
)

from models.advice.advice import Advice
from models.general.golden_food import (
    GoldenFood,
    GoldenFoodMulti,
    calculate_golden_food_multis,
    get_worn_golden_food,
)

from utils.number_formatting import parse_number, round_and_trim
from utils.safer_data_handling import safe_loads, safer_index
from utils.text_formatting import getItemCodeName, notateNumber

from utils.logging import get_logger

logger = get_logger(__name__)


class BeanstalkDeposit(GoldenFood):

    def __init__(self, golden_food_name: str, tier: int):
        self.tier = min(tier, golden_food_max_tier)
        amount = golden_food_tier_require[self.tier]
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
            goal = notateNumber("Match", next_tier_require, 0, "K")
            progress = notateNumber("Match", amount, matchString=goal)
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
        self.character_multis: dict[int, GoldenFoodMulti] = {}
        self._character_foods: dict[
            tuple[int, str], tuple[GoldenFood | None, BeanstalkDeposit | None]
        ] = {}
        self.emporium_unlocked = False

    def calculate_unlocked_tier(self, emporium):
        tier_1 = emporium["Gold Food Beanstalk"].obtained
        tier_2 = emporium["Supersized Gold Beanstacking"].obtained
        self.emporium_unlocked = bool(tier_1)
        self.unlocked_tier += int(tier_1) + int(tier_2)

    def calculate_golden_food_multi(self, account):
        # Per character, section shows the best
        self._character_foods = {}
        self.character_multis = calculate_golden_food_multis(account)
        self.golden_food_multi = max(
            (multi.total for multi in self.character_multis.values()), default=1
        )
        return self.golden_food_multi

    def calculate_bonuses(self):
        for deposit in self.values():
            deposit.calculate_bonus(self.golden_food_multi)

    def get_deposit_for_effect(self, effect: str) -> BeanstalkDeposit | None:
        # Only the first deposit counts
        if not self.emporium_unlocked:
            return None
        for deposit in self.values():
            item = raw_item_data.get(getItemCodeName(deposit.name), {})
            if item.get("Effect") == effect:
                return deposit if deposit.tier > 0 else None
        return None

    def _get_character_foods(
        self, character, effect: str
    ) -> tuple[GoldenFood | None, BeanstalkDeposit | None]:
        key = (character.character_index, effect)
        if key not in self._character_foods:
            multi = self.character_multis[character.character_index].total
            worn = get_worn_golden_food(character, effect)
            if worn:
                worn.calculate_bonus(multi)
            deposit = self.get_deposit_for_effect(effect)
            if deposit:
                deposit = BeanstalkDeposit(deposit.name, deposit.tier)
                deposit.calculate_bonus(multi)
            self._character_foods[key] = (worn, deposit)
        return self._character_foods[key]

    def get_golden_food_bonus(self, character, effect: str) -> float:
        # "GoldFoodBonuses" in source: worn plus Beanstalk. Last updated in v2.531.0
        worn, deposit = self._get_character_foods(character, effect)
        worn_value = worn.bonus_value if worn else 0
        return worn_value + (deposit.bonus_value if deposit else 0)

    def get_golden_food_bonus_advice(self, character, effect: str) -> list[Advice]:
        multi = self.character_multis[character.character_index].total
        worn, deposit = self._get_character_foods(character, effect)
        advices = []
        if worn:
            advices.append(worn.get_bonus_advice(worn=True))
        if deposit:
            advices.append(deposit.get_bonus_advice())
        advices.append(Advice(
            label=f"{{{{Beanstalk|#beanstalk}}}} - Golden Food Multi: "
            f"{round_and_trim(multi)}x",
            picture_class="beanstalk",
        ))
        return advices
