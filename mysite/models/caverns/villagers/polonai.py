from consts.caverns.cavern import cavern_names, max_cavern
from models.advice.advice import Advice
from models.caverns.villagers.villager import Villager


class Polonai(Villager):
    def __init__(self, **kwargs):
        super().__init__(name="Polonai", unlock_at=0, role="The Explorer", **kwargs)

    def parse_feature(self, raw_caverns_list: list):
        pass

    def stat_advices(self) -> list[Advice]:
        return self.base_stat_advice(max_cavern)

    def feature_advice(self) -> dict[str, list[Advice]] | None:
        if self.level >= max_cavern:
            return None

        from models.general.session_data import session_data

        villagers = session_data.account.caverns_.villagers.values()
        return {
            "Cavern Unlock Status": [
                self._get_caver_unlock_advice(index, name)
                for index, name in cavern_names.items()
                if index > self.level
            ],
            "Villager Unlock Status": [
                villager.get_unlock_advice(self.level)
                for villager in villagers
                if villager.unlock_at > self.level
            ],
        }

    def _get_caver_unlock_advice(self, index: int, name: str) -> Advice:
        return Advice(
            label=f"Discover Cavern #{index}: {name}",
            picture_class=f"cavern-{index}",
            progression=self.level,
            goal=index,
        )
