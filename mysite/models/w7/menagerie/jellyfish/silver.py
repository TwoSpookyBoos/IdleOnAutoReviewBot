from consts.w7.menagerie import silver_jelly_max_levels
from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from utils.number_formatting import round_and_trim
from utils.text_formatting import notateNumber


class SilverJellyfish(Jellyfish):
    """Spend Obol Fragments on Obol MISC bonuses and the auto-trash Fragment rate"""

    def parse_feature(self, raw_menagerie: list):
        self.misc_level: int = round(self._misc(raw_menagerie, 9))
        self.trash_level: int = round(self._misc(raw_menagerie, 10))
        self.misc_max_level, self.trash_max_level = silver_jelly_max_levels
        # "ObolMISCmulti" in source
        self.misc_multi: float = 1 + self.misc_level / 100
        # "ObolAutoTrashRate" in source
        self.trash_rate: float = (10 + self.trash_level) / 100
        # "SilverJellyCosts" in source, in Obol Fragments
        self.misc_cost: float = (
            2
            * (100 + 25 * self.misc_level + self.misc_level**3)
            * 1.065**self.misc_level
        )
        self.trash_cost: float = (
            25 + 10 * self.trash_level + self.trash_level**2
        ) * 1.056**self.trash_level

    def _feature_advices(self) -> list[Advice]:
        from models.general.session_data import session_data

        fragments = session_data.account.obols.fragments
        advices = []
        for label, level, max_level, cost in (
            (
                f"Obol MISC bonuses: {round_and_trim(self.misc_multi)}x",
                self.misc_level,
                self.misc_max_level,
                self.misc_cost,
            ),
            (
                "Obol auto-trash Fragment rate:"
                f" {round_and_trim(self.trash_rate * 100)}%",
                self.trash_level,
                self.trash_max_level,
                self.trash_cost,
            ),
        ):
            if level < max_level:
                label += (
                    f"<br>Next LV costs {notateNumber('Basic', cost, 2)} Obol Fragments"
                )
            advices.append(
                Advice(
                    label=label,
                    picture_class="obol-fragment",
                    progression=level,
                    goal=max_level,
                )
            )
        advices.append(
            Advice(
                label=f"Obol Fragments owned: {notateNumber('Basic', fragments, 2)}",
                picture_class="obol-fragment",
            )
        )
        return advices
