from models.advice.advice import Advice
from models.w7.menagerie.jellyfish.jellyfish import Jellyfish
from utils.text_formatting import notateNumber


class LumiJellyfish(Jellyfish):
    """Jellyfish 0, the Menagerie itself: always there, opens the Menagerie menu"""

    def parse_feature(self, raw_menagerie: list):
        pass

    def _feature_advices(self) -> list[Advice]:
        menagerie = self.menagerie
        advices = [
            Advice(
                label=(
                    f"Menagerie Rank {menagerie.rank}:"
                    f" {menagerie.shells}/{menagerie.shell_req} Shells"
                    f" to Rank {menagerie.rank + 1}"
                    "<br>Claim Missions and buy Shells from the Pink Jellyfish"
                ),
                picture_class="menagerie-shell",
                progression=menagerie.shells,
                goal=menagerie.shell_req,
            ),
            Advice(
                label=f"Lumi: {notateNumber('Basic', menagerie.lumi, 2)}",
                picture_class="lumi",
            ),
            Advice(
                label=(
                    f"Mission slots: {menagerie.visible_missions}"
                    "<br>From Boost 1, Research Grid E4, the Jade Emporium"
                    " and a Gem Shop pack"
                ),
                picture_class="menagerie-mission-0",
                progression=menagerie.visible_missions,
                goal=len(menagerie.missions),
            ),
        ]
        for name, visible, total, next_rank, image in (
            (
                "Unlock",
                menagerie.visible_unlocks,
                len(menagerie.unlocks),
                menagerie.next_unlock_slot_rank(),
                "menagerie-unlock-0",
            ),
            (
                "Boost",
                menagerie.visible_boosts,
                len(menagerie.boosts),
                menagerie.next_boost_slot_rank(),
                "menagerie-boost-0",
            ),
        ):
            label = f"{name} slots: {visible}"
            if next_rank is not None:
                label += f"<br>Next slot at Rank {next_rank}"
            advices.append(
                Advice(
                    label=label,
                    picture_class=image,
                    progression=visible,
                    goal=total,
                )
            )
        return advices
