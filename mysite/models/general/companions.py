from consts.idleon.consts_idleon import companions_data
from models.advice.advice import Advice
from utils.logging import get_logger


logger = get_logger(__name__)


class Companion:
    def __init__(self, companions, name: str, info: dict):
        self._companions = companions
        self.name: str = name
        self.companion_id: int = info['Id']
        self.description: str = info['Description']
        self.image: str = info['Image']
        self.value: float = info['Value']
        self.owned: bool = False

    def get_advice(self, value_is_multi: bool = False) -> tuple[int | float, Advice]:
        data_present = self._companions.data_present
        value = self.value * self.owned
        if value == 0 and value_is_multi:
            value = 1
        return value, Advice(
            label=f"Companions - {self.name}:"
                  f"<br>{self.description}"
                  f"{'' if data_present else '<br>Note: Could be inaccurate. Companion data not found!'}",
            picture_class=self.image,
            progression=int(self.owned) if data_present else 'IDK',
            goal=1
        )


class Companions(dict[str, Companion]):
    def __init__(self, raw_data: dict, doot: bool = False, riftslug: bool = False, sheepie: bool = False):
        super().__init__()
        # Toolbox exports a dict called `companion`, Efficiency a flat list of IDs called `companions`
        raw_companion = raw_data.get('companion', None)
        raw_companions = raw_data.get('companions', None)
        self.data_present: bool = raw_companion is not None or raw_companions is not None

        acquired_ids = set()
        if raw_companion is not None:
            for companion_info in raw_companion.get('l', []):
                try:
                    acquired_ids.add(int(companion_info.split(',')[0]))
                except:
                    continue
        elif raw_companions is not None:
            acquired_ids.update(raw_companions)
        else:
            logger.debug("No companion data present in JSON. Relying only on Switches")

        for name, info in companions_data.items():
            companion = Companion(self, name, info)
            companion.owned = info['Id'] in acquired_ids
            self[name] = companion

        for switch_enabled, name in ((doot, 'King Doot'), (riftslug, 'Rift Slug'), (sheepie, 'Sheepie')):
            if switch_enabled:
                self[name].owned = True

    def has(self, name: str) -> bool:
        if name not in self:
            logger.error(f"Unknown Companion name: {name}. Returning False / not owned.")
            return False
        return self[name].owned

    @property
    def owned_names(self) -> set[str]:
        return {name for name, companion in self.items() if companion.owned}
