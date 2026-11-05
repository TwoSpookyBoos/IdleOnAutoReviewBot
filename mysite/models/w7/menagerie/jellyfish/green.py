from functools import cached_property

from consts.w7.menagerie import green_jelly_nametags_required
from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish

tome_nametag_name = "Tome Legend Nametag"


class GreenJellyfish(Jellyfish):
    """Takes Top 0.1% Tome Nametags for the Top 0.01% Tome Nametag"""

    def parse_feature(self, raw_menagerie: list):
        pass

    @cached_property
    def nametags_deposited(self) -> int:
        # "Spelunk"[17][28] in source: Gallery level of the Top 0.1% Tome nametag
        from models.general.session_data import session_data

        nametag = session_data.account.gallery.nametag.get(tome_nametag_name)
        return nametag.level if nametag else 0

    def _feature_advices(self) -> list[Advice]:
        deposited = min(self.nametags_deposited, green_jelly_nametags_required)
        return [
            Advice(
                label=(
                    f"Top 0.1% Tome Nametags in the Gallery: {deposited}"
                    f"/{green_jelly_nametags_required}"
                    "<br>At 12, the Green Jellyfish gives the Top 0.01% Tome Nametag."
                    " No stats, just bragging rights"
                ),
                picture_class=tome_nametag_name,
                progression=deposited,
                goal=green_jelly_nametags_required,
            )
        ]
