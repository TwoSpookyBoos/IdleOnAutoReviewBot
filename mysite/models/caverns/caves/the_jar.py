from functools import cached_property

from consts.caverns.caves.the_harp import max_harp_notes
from consts.caverns.caves.the_jar import (
    jar_collectibles,
    jar_rupie_sources,
    jar_rupies,
    jar_types,
    max_jar_rupies,
    max_jar_types,
)
from consts.caverns.caves.the_well import max_sediments
from consts.consts_autoreview import EmojiType, ValueToMulti
from models.advice.advice import Advice
from models.caverns.caves.cavern import Cavern
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safer_convert, safer_math_log
from utils.text_formatting import notateNumber


class CollectibleBonus:
    def __init__(self, index: int, entry: dict, level: int):
        self.index = index
        self.name = entry["Name"]
        self.level = level
        self.scaling_value = entry["ScalingValue"]
        self.image = f"jar-collectible-{index}"
        self._raw_description = entry["Description"]

    @cached_property
    def value(self) -> float:
        from models.general.session_data import session_data

        legend_talent_multi = ValueToMulti(
            session_data.account.legend_talents["Talents"]["Whats in your Jar?"][
                "Value"
            ]
        )
        return self.level * self.scaling_value * legend_talent_multi

    @cached_property
    def description(self) -> str:
        description = self._raw_description
        scaling_note = ""
        if "{" in description:
            scaling_note = (
                f"<br>+{self.scaling_value}"
                f"{'%' if '%' in description else ''} per level"
            )
            description = description.replace("{", f"{round_and_trim(self.value)}")
        elif "}" in description:
            multi = ValueToMulti(self.scaling_value)
            scaling_note = f"<br>{round_and_trim(multi - 1)} per level"
            description = description.replace(
                "}", f"{round_and_trim(ValueToMulti(self.value))}"
            )
        return f"{description}{scaling_note}"

    def get_advice(self, link_to_section: bool = False) -> Advice:
        link_text = "{{Cavern 11- The Jar|#underground-overgrowth}} - "
        link = link_text if link_to_section else ""
        return Advice(
            label=f"{link}{self.name}: {self.description}",
            picture_class=self.image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
            informational=True,
        )

    def get_bonus_advice(self) -> Advice:
        advice = self.get_advice(link_to_section=True)
        advice.informational = False
        return advice


class TheJar(Cavern):
    def __init__(self):
        super().__init__(name="The Jar", cavern_number=11)

    def parse(self, raw_caverns_list: list):
        offset = max_sediments + max_harp_notes
        self.rupies_owned = [0.0] * max_jar_rupies
        for index in range(max_jar_rupies):
            try:
                self.rupies_owned[index] = safer_convert(
                    raw_caverns_list[9][offset + index], 0.0
                )
            except Exception:
                continue

        self.jars_destroyed = [0] * max_jar_types
        for index in range(max_jar_types):
            try:
                self.jars_destroyed[index] = raw_caverns_list[11][40 + index]
            except Exception:
                continue

        self.collectibles: dict[str, CollectibleBonus] = {}
        for index, entry in enumerate(jar_collectibles):
            try:
                level = safer_convert(raw_caverns_list[24][index], 0)
            except Exception:
                level = 0
            bonus = CollectibleBonus(index, entry, level)
            self.collectibles[bonus.name] = bonus

    def _rupies_stats_advice(self) -> list[Advice]:
        advices = []
        for rupie_index, rupie_amount in enumerate(self.rupies_owned):
            jar_type_index, threshold, threshold_display = jar_rupie_sources[
                rupie_index
            ]
            jar_name = jar_types[jar_type_index]
            if threshold is None:
                source_text = f"{jar_name} Jars, always"
                unlocked = True
            else:
                prev_amount = self.rupies_owned[rupie_index - 1]
                unlocked = prev_amount >= threshold
                verb = "while" if unlocked else "once"
                source_text = (
                    f"{jar_name} Jars {verb} you have {threshold_display}+ "
                    f"{jar_rupies[rupie_index - 1]} Rupies"
                )
            advices.append(
                Advice(
                    label=(
                        f"{jar_rupies[rupie_index]} Rupies: "
                        f"{notateNumber('Basic', rupie_amount, 2)}"
                        f"<br>Collected from {source_text}"
                    ),
                    picture_class=f"jar-rupie-{rupie_index}",
                    progression=int(unlocked),
                    goal=1,
                    resource=f"jar-type-{jar_type_index}",
                )
            )
        return advices

    def _jar_stats_advice(self) -> list[Advice]:
        from models.general.session_data import session_data

        kaipu = session_data.account.caverns.villagers["Kaipu"]
        advices = [kaipu.schematics["Jar Production Line"].get_advice()]
        for jar_index, destroyed in enumerate(self.jars_destroyed):
            pow10_stacks = safer_math_log(destroyed, "Lava")
            advices.append(
                Advice(
                    label=(
                        f"{jar_types[jar_index]} Jar: {destroyed} destroyed"
                        f"<br>{pow10_stacks:.2f} pow10 stacks = "
                        f"{5 * pow10_stacks:.2f}%"
                    ),
                    picture_class=f"jar-type-{jar_index}",
                    progression=f"{pow10_stacks:.2f}",
                    goal=EmojiType.INFINITY.value,
                    informational=True,
                )
            )
        return advices

    def advice_groups(self) -> dict[str, list[Advice]]:
        from models.advice.generators.w7 import get_legend_talent_advice

        total_collectible_levels = sum(
            bonus.level for bonus in self.collectibles.values()
        )

        return {
            "Cavern Stats": [
                self.objective_advice(
                    "Create Jars passively, then break to collect Rupies, "
                    "Opals, and Collectibles",
                    resource="jar-all-types",
                ),
                self.opals_found_advice(),
            ],
            "Rupies Stats": self._rupies_stats_advice(),
            "Jar Stats": self._jar_stats_advice(),
            f"Collectibles: {total_collectible_levels} total levels": [
                bonus.get_advice() for bonus in self.collectibles.values()
            ],
            "Collectibles bonus Multi": [
                get_legend_talent_advice("Whats in your Jar?")
            ],
        }
