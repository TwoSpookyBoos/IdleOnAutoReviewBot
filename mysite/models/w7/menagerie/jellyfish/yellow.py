from math import floor

from consts.consts_autoreview import ValueToMulti
from consts.w7.menagerie import yellow_jelly_buildings
from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from utils.number_formatting import round_and_trim
from utils.text_formatting import notateNumber


class YellowJellyfish(Jellyfish):
    """Builds 4 buildings with account-wide bonuses from Construction build progress"""

    def parse_feature(self, raw_menagerie: list):
        self.building_levels: list[int] = [
            round(self._misc(raw_menagerie, 11 + building))
            for building in range(len(yellow_jelly_buildings))
        ]
        self.build_progress: float = self._misc(raw_menagerie, 15)
        # "ConstBuildREQ" in source
        total_levels = sum(self.building_levels)
        self.build_req: float = (
            10**5 * max(3.2, 8 - 0.15 * total_levels) ** total_levels
        )
        # "ConstBuildBONUSES" in source
        self.building_bonuses: list[float] = [
            building["Value Per Level"] * level
            for building, level in zip(yellow_jelly_buildings, self.building_levels)
        ]

    def _feature_advices(self) -> list[Advice]:
        progress = notateNumber("Basic", self.build_progress, 2)
        req = notateNumber("Basic", self.build_req, 2)
        advices = [
            Advice(
                label=(
                    f"Build progress: {progress}/{req}"
                    "<br>Filled by Construction build slot 8; each new LV of any"
                    " building raises the next requirement"
                ),
                picture_class=self.image,
                progression=min(100, floor(100 * self.build_progress / self.build_req)),
                goal=100,
                unit="%",
            )
        ]
        for building, level, bonus in zip(
            yellow_jelly_buildings, self.building_levels, self.building_bonuses
        ):
            per_level = building["Value Per Level"]
            if building["Multiplicative"]:
                total = f"{round_and_trim(ValueToMulti(bonus))}x"
                step = f"+{per_level}% multi per LV"
            else:
                total = f"+{round_and_trim(bonus)}%"
                step = f"+{per_level}% per LV"
            advices.append(
                Advice(
                    label=f"{building['Name']}: {total}<br>LV {level}, {step}",
                    picture_class=self.image,
                    progression=level,
                )
            )
        return advices
