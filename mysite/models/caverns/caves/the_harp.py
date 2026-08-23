from functools import cached_property
from math import ceil

from consts.caverns.caves.the_harp import (
    harp_chord_effects,
    harp_notes,
    max_harp_chords,
    max_harp_strings,
    schematics_unlocking_harp_chords,
    schematics_unlocking_harp_strings,
)
from consts.caverns.caves.the_well import max_sediments
from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.safer_data_handling import safer_convert, safer_math_pow
from utils.text_formatting import notateNumber


class HarpChord:
    def __init__(
        self, letter: str, index: int, level: float, exp: float, unlocked_by: str | None
    ):
        self.letter = letter
        self.index = index
        self.level = level
        self.exp = exp
        self.unlocked_by = unlocked_by
        self.strum, self.lv_bonus = harp_chord_effects[letter]

    @cached_property
    def _schematic(self):
        assert self.unlocked_by is not None
        from models.general.session_data import session_data

        return session_data.account.caverns_.villagers["Kaipu"].schematics[
            self.unlocked_by
        ]

    @cached_property
    def unlocked(self) -> bool:
        return self.unlocked_by is None or self._schematic.bought

    def get_advice(self) -> Advice:
        if self.unlocked:
            label = (
                f"Level {self.level} {self.letter} chord"
                f"<br>Strum Effect: {self.strum}"
                f"<br>LV Bonus: {self.lv_bonus}"
            )
        else:
            label = (
                f"Unlock {self.letter} chord by purchasing"
                f"<br>{self._schematic.full_name()}"
            )
        return Advice(
            label=label,
            picture_class=f"harp-chord-{self.letter}",
            progression=self.level,
            goal=EmojiType.INFINITY.value,
        )


class HarpNote:
    def __init__(
        self, cavern: "TheHarp", index: int, name: str, amount: float, unlocked: bool
    ):
        self.cavern = cavern
        self.index = index
        self.name = name
        self.amount = amount
        self.unlocked = unlocked

    def _unlock_cost(self) -> int:
        prior_index = self.index - 1
        return ceil(
            150
            * safer_math_pow(1 + prior_index, 1.5)
            * safer_math_pow(4.5, prior_index)
        )

    def get_unlock_advice(self) -> Advice:
        if not self.unlocked:
            unlock_cost = self._unlock_cost()
            previous_note = self.cavern.notes[harp_notes[self.index - 1]]
            target_string = notateNumber("Basic", unlock_cost, 2)
            current_string = notateNumber(
                "Match", min(unlock_cost, previous_note.amount), 2, "", target_string
            )
            return Advice(
                label=(
                    f"Unlock {self.name}s by trading {target_string} "
                    f"of the previous Note"
                ),
                picture_class=f"harp-note-{self.index}",
                resource=f"harp-note-{self.index - 1}",
                progression=current_string,
                goal=target_string,
            )
        return Advice(
            label=f"{self.name}s: {notateNumber('Basic', self.amount, 2)}",
            picture_class=f"harp-note-{self.index}",
            goal=EmojiType.INFINITY.value,
        )


class TheHarp(Cavern):
    def __init__(self):
        super().__init__(name="The Harp", cavern_number=6)

    def parse(self, raw_caverns_list: list):
        try:
            self.harp_power = raw_caverns_list[11][22]
        except Exception:
            self.harp_power = 0
        try:
            self.notes_unlocked = raw_caverns_list[11][20]
        except Exception:
            self.notes_unlocked = 0

        self.chords: dict[str, HarpChord] = {}
        for index, letter in enumerate(harp_chord_effects.keys()):
            try:
                level = raw_caverns_list[19][index * 2]
            except Exception:
                level = 0
            try:
                exp = raw_caverns_list[19][index * 2 + 1]
            except Exception:
                exp = 0
            unlocked_by = (
                None if index < 2 else schematics_unlocking_harp_chords[index - 2]
            )
            self.chords[letter] = HarpChord(
                letter=letter,
                index=index,
                level=level,
                exp=exp,
                unlocked_by=unlocked_by,
            )

        self.notes: dict[str, HarpNote] = {}
        for index, name in enumerate(harp_notes):
            try:
                amount = safer_convert(raw_caverns_list[9][max_sediments + index], 0)
            except Exception:
                amount = 0
            self.notes[name] = HarpNote(
                cavern=self,
                index=index,
                name=name,
                amount=amount,
                unlocked=self.notes_unlocked >= index,
            )

    @cached_property
    def strings_unlocked(self) -> int:
        from models.general.session_data import session_data

        kaipu = session_data.account.caverns_.villagers["Kaipu"]
        cosmos = session_data.account.caverns_.villagers["Cosmos"]
        bought_count = sum(
            1
            for schematic_name in schematics_unlocking_harp_strings
            if kaipu.schematics[schematic_name].bought
        )
        return 1 + bought_count + cosmos.majiks.hole["String is Strung"].level

    def chords_unlocked_count(self) -> int:
        return sum(chord.unlocked for chord in self.chords.values())

    def _string_stats_advice(self) -> list[Advice]:
        from models.general.session_data import session_data

        kaipu = session_data.account.caverns_.villagers["Kaipu"]
        cosmos = session_data.account.caverns_.villagers["Cosmos"]
        return [
            cosmos.majiks.hole["String is Strung"].get_advice(),
            *[
                kaipu.schematics[schematic_name].get_advice()
                for schematic_name in schematics_unlocking_harp_strings
            ],
        ]

    def _chord_stats_advice(self) -> list[Advice]:
        return [
            Advice(
                label=(
                    f"Current Harp Power:"
                    f"<br>{notateNumber('Basic', self.harp_power, 2)}"
                ),
                picture_class=self.image,
            ),
            *[chord.get_advice() for chord in self.chords.values()],
        ]

    def advice_groups(self) -> dict[str, list[Advice]]:
        string_stats = (
            f"String Stats: {self.strings_unlocked}/{max_harp_strings} unlocked"
        )
        chord_stats = (
            f"Chord Stats: {self.chords_unlocked_count()}/{max_harp_chords} unlocked"
        )
        return {
            "Cavern Stats": [
                self.objective_advice(
                    "Spend passively generated Harp Power to collect Notes"
                ),
                self.opals_found_advice(),
            ],
            string_stats: self._string_stats_advice(),
            chord_stats: self._chord_stats_advice(),
            "Note Stats": [note.get_unlock_advice() for note in self.notes.values()],
        }
