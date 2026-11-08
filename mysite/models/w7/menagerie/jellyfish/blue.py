from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from utils.text_formatting import notateNumber


class BlueJellyfish(Jellyfish):
    """Deposited Ladles are used on Cooking automatically every day, without being
    consumed: each one adds 1 hour of Cooking, with no meal level cap"""

    def parse_feature(self, raw_menagerie: list):
        self.ladles_deposited: float = self._misc(raw_menagerie, 5)

    def _feature_advices(self) -> list[Advice]:
        advices = [
            Advice(
                label=(
                    "Ladles deposited:"
                    f" {notateNumber('Basic', self.ladles_deposited, 2)}"
                    "<br>All of them are used on Cooking automatically every day,"
                    " without being consumed"
                ),
                picture_class="cooking-ladle",
            )
        ]
        deposit_advice = self.get_deposit_advice()
        if deposit_advice is not None:
            advices.append(deposit_advice)
        return advices

    @property
    def _ladles_in_storage(self) -> float:
        from models.general.session_data import session_data

        return session_data.account.stored_assets.get("Ladle").amount

    def _deposit_label(self, jellyfish: str) -> str:
        ladles = notateNumber("Basic", self._ladles_in_storage, 2)
        return f"Deposit {ladles} Ladles from your storage into the {jellyfish}"

    def get_deposit_advice(self) -> Advice | None:
        if self._ladles_in_storage <= 0:
            return None
        return Advice(
            label=self._deposit_label("Blue Jellyfish"),
            picture_class="cooking-ladle",
            progression=0,
            goal=1,
        )

    def get_deposit_alert(self) -> Advice | None:
        if not self.unlocked or self._ladles_in_storage <= 0:
            return None
        return Advice(
            label=self._deposit_label("{{ Blue Jellyfish|#luminous-menagerie }}"),
            picture_class="cooking-ladle",
        )
