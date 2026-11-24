from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from utils.text_formatting import notateNumber


class PinkJellyfish(Jellyfish):
    """Spend coins on Shells and on +1% Lumi gains rate"""

    def parse_feature(self, raw_menagerie: list):
        self.shells_bought: int = round(self._misc(raw_menagerie, 3))
        # "PinkJellyBonus" in source: +1% Lumi gains rate per purchase
        self.lumi_bonus: int = round(self._misc(raw_menagerie, 4))
        # "PinkJellyCosts" in source, in coins
        self.shell_cost: float = (
            10**35 * (350 + 150 * self.shells_bought) ** self.shells_bought
        )
        self.lumi_bonus_cost: float = 10**30 * 6**self.lumi_bonus

    def get_shell_advice(self) -> Advice:
        if not self.unlocked:
            return self.get_unlock_advice()
        return Advice(
            label=(
                f"{self.name}: buy Shells with coins"
                f"<br>Next Shell costs {notateNumber('Basic', self.shell_cost, 2)}"
                " coins"
            ),
            picture_class="menagerie-shell",
            progression=self.shells_bought,
            goal=EmojiType.INFINITY.value,
            resource="coins",
        )

    def _feature_advices(self) -> list[Advice]:
        return [
            self.get_shell_advice(),
            Advice(
                label=(
                    f"Buy Lumi gains rate with coins: +{self.lumi_bonus}%"
                    "<br>Next +1% costs"
                    f" {notateNumber('Basic', self.lumi_bonus_cost, 2)} coins"
                ),
                picture_class="lumi",
                progression=self.lumi_bonus,
                goal=EmojiType.INFINITY.value,
                resource="coins",
            ),
        ]
