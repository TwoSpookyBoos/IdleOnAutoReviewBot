from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from utils.text_formatting import notateNumber


class BlueJellyfish(Jellyfish):
    """Deposited Ladles are used on Cooking automatically every day"""

    def parse_feature(self, raw_menagerie: list):
        self.ladles_deposited: float = self._misc(raw_menagerie, 5)

    def _feature_advices(self) -> list[Advice]:
        from models.general.session_data import session_data

        ladles_owned = session_data.account.stored_assets.get("Ladle").amount
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
        if ladles_owned > 0:
            advices.append(
                Advice(
                    label=(
                        f"Deposit {notateNumber('Basic', ladles_owned, 2)} more Ladles"
                        " from your storage into the Blue Jellyfish"
                    ),
                    picture_class="cooking-ladle",
                    progression=0,
                    goal=1,
                )
            )
        return advices
