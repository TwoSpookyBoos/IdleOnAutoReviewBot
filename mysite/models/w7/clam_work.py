from consts.idleon.w7.clam_work import clam_bonus
from consts.w7.clam_work import clam_bonus_img

from models.advice.advice import Advice

from utils.safer_data_handling import safer_index
from utils.logging import get_logger

logger = get_logger(__name__)


class ClamBonus:
    def __init__(self, index: int, obtained: bool):
        self.obtained = obtained
        self.bonus = clam_bonus[index]
        self._image = clam_bonus_img[index]

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        return Advice(
            label=self.bonus,
            picture_class=self._image,
            progression=int(self.obtained),
            goal=1,
            resource="clam-pearl",
        )


class ClamWork:
    def __init__(self, raw_data: dict):
        raw_optlacc = raw_data.get("OptLacc", [])
        self.level = safer_index(raw_optlacc, 464, 0)
        bonuses = []
        for bonus_index in range(len(clam_bonus)):
            bonuses.append(ClamBonus(bonus_index, self.level > bonus_index))
        self.bonuses = bonuses
