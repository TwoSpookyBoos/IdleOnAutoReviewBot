from math import floor

from consts.w7.spelunk import chapter_name
from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from utils.safer_data_handling import safer_convert, safer_index
from utils.text_formatting import notateNumber


class RedJellyfish(Jellyfish):
    """Keeps a copy of every Spelunking page you read and re-reads them all at once,
    with a multi that grows with the days since the last re-read"""

    def parse_feature(self, raw_menagerie: list):
        self.days_rested: int = round(self._misc(raw_menagerie, 6))
        self.reading_multi: int = self._reading_multi(self.days_rested)
        # "Menagerie"[4] in source: pages stored per Spelunking chapter
        self.pages_stored: list[float] = [
            safer_convert(amount, 0) for amount in safer_index(raw_menagerie, 4, [])
        ]

    @staticmethod
    def _reading_multi(days: int) -> int:
        # "RedJellyReadingMulti" in source
        return floor(max(1, days**0.74))

    def _next_multi_day(self) -> int:
        day = self.days_rested + 1
        while self._reading_multi(day) <= self.reading_multi:
            day += 1
        return day

    def _feature_advices(self) -> list[Advice]:
        next_day = self._next_multi_day()
        advices = [
            Advice(
                label=(
                    f"{self.days_rested} days rested:"
                    f" {self.reading_multi}x page reading gains"
                    f"<br>{self._reading_multi(next_day)}x after {next_day} days."
                    " Re-reading resets the days"
                ),
                picture_class=self.image,
                progression=self.days_rested,
                goal=next_day,
            )
        ]
        for index, name in enumerate(chapter_name):
            pages = safer_index(self.pages_stored, index, 0)
            advices.append(
                Advice(
                    label=f"{name}: {notateNumber('Basic', pages, 2)} pages stored",
                    picture_class=f"spelunking-chapter-{index + 1}",
                )
            )
        return advices
