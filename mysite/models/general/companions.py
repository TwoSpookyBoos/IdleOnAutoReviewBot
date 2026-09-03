from consts.general.companions import companion_bonuses
from consts.idleon.consts_idleon import companions_data
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


logger = get_logger(__name__)

# Pet Bonus Token indexes
pet_bonus_tokens_owned_index = 605
pet_bonus_token_targets_index = 606


class Companion:
    def __init__(self, companions, name: str, info: dict):
        self._companions = companions
        self.name: str = name
        self.companion_id: int = info['Id']
        self.image: str = info['Image']
        self.tour_power: int = info['TourPower']
        self.upgraded_tour_power: int = info['UpgradedTourPower']
        self._base_description: str = info['Description']
        self._upgraded_description: str = info['UpgradedDescription']
        self._base_value: float = info['Value']
        self._upgraded_value: float = info['UpgradedValue']

        self.copies: int = 0
        self.level: int = 0  # Pet Mart+ level, max across copies
        self.via_token: bool = False

    @property
    def owned(self) -> bool:
        """Copy owned, or granted by a Pet Bonus Token."""
        return self.copies > 0 or self.via_token

    @property
    def upgraded(self) -> bool:
        """`_customBlock_CompLV2` in source: the "+" tier."""
        return self.copies > 0 and self.level >= 1

    @property
    def value(self) -> float:
        """`CompanionBon` in source: field 11 upgraded, else field 2."""
        return self._upgraded_value if self.upgraded else self._base_value

    @property
    def bonus(self) -> float:
        """`_customBlock_Companions` in source: value, or 0 unowned."""
        return self.value if self.owned else 0

    @property
    def description(self) -> str:
        return self._upgraded_description if self.upgraded else self._base_description

    def _get_bonus(self, stat: str, form: str, absent: float) -> float:
        if not self.owned:
            return absent
        got_form, base, upgraded = companion_bonuses.get(self.name, {}).get(stat, (form, absent, absent))
        if got_form != form:
            return absent
        return upgraded if self.upgraded else base

    def get_multi(self, stat: str) -> float:
        """Multi for `stat`, or 1.0 if none / unowned."""
        return self._get_bonus(stat, 'multi', 1.0)

    def get_value(self, stat: str) -> float:
        """Additive `stat` bonus the formula scales out of Value, or 0 if none / unowned."""
        return self._get_bonus(stat, 'value', 0)

    def get_advice(self, value_is_multi: bool = False) -> tuple[int | float, Advice]:
        data_present = self._companions.data_present
        value = self.value * self.owned
        if value == 0 and value_is_multi:
            value = 1
        notes = ''
        if not data_present:
            notes += '<br>Note: Could be inaccurate. Companion data not found!'
        elif self.upgraded:
            notes += '<br>Upgraded with Pet Mart+'
        elif self.via_token:
            notes += '<br>Bonus granted by a Pet Bonus Token'
        return value, Advice(
            label=f"Companions - {self.name}{'+' if self.upgraded else ''}:"
                  f"<br>{self.description}"
                  f"{notes}",
            picture_class=self.image,
            progression=int(self.owned) if data_present else 'IDK',
            goal=1
        )


class Companions(dict[str, Companion]):
    def __init__(self, raw_data: dict, doot: bool = False, riftslug: bool = False, sheepie: bool = False):
        super().__init__()
        # Toolbox: `companion` dict. Efficiency: `companions` id list
        raw_companion = raw_data.get('companion', None)
        raw_companions = raw_data.get('companions', None)
        self.data_present: bool = raw_companion is not None or raw_companions is not None

        copies: dict[int, int] = {}
        levels: dict[int, int] = {}
        if raw_companion is not None:
            for companion_info in raw_companion.get('l', []):
                fields = f"{companion_info}".split(',')
                try:
                    companion_id = int(fields[0])
                except:
                    logger.warning(f"Unparseable companion entry: {companion_info}. Skipping")
                    continue
                copies[companion_id] = copies.get(companion_id, 0) + 1
                # field 4 = Pet Mart+ level, absent pre-2.3.525
                level = safer_convert(safer_index(fields, 4, 0), 0)
                levels[companion_id] = max(levels.get(companion_id, 0), level)
        elif raw_companions is not None:
            # id-only, no Pet Mart+ level
            for companion_id in raw_companions:
                try:
                    companion_id = int(companion_id)
                except:
                    logger.warning(f"Unparseable companion Id: {companion_id}. Skipping")
                    continue
                copies[companion_id] = copies.get(companion_id, 0) + 1
        else:
            logger.warning("Companion data not present. Relying only on Switches")

        raw_optlacc = safe_loads(raw_data.get('OptionsListAccount', []))
        if not isinstance(raw_optlacc, list):
            raw_optlacc = []
        self.tokens_owned: int = min(1, safer_convert(
            safer_index(raw_optlacc, pet_bonus_tokens_owned_index, 0), 0
        ))
        # comma list of token'd ids
        raw_targets = f"{safer_index(raw_optlacc, pet_bonus_token_targets_index, '')}"
        token_ids = set()
        if raw_targets not in ('', '0', 'None'):
            for target in raw_targets.split(','):
                try:
                    token_ids.add(int(target))
                except:
                    logger.warning(f"Unparseable Pet Bonus Token target: {target}. Skipping")
                    continue
        self.tokens_used: int = len(token_ids)

        for name, info in companions_data.items():
            companion = Companion(self, name, info)
            companion.copies = copies.get(info['Id'], 0)
            companion.level = levels.get(info['Id'], 0)
            companion.via_token = companion.copies == 0 and info['Id'] in token_ids
            self[name] = companion

        for switch_enabled, name in ((doot, 'King Doot'), (riftslug, 'Rift Slug'), (sheepie, 'Sheepie')):
            if switch_enabled and self[name].copies == 0:
                self[name].copies = 1

    def has(self, name: str) -> bool:
        if name not in self:
            logger.error(f"Unknown Companion name: {name}. Returning False / not owned.")
            return False
        return self[name].owned

    def get_multi(self, name: str, stat: str) -> float:
        if name not in self:
            logger.error(f"Unknown Companion name: {name}. Returning 1.0 / no multi.")
            return 1.0
        return self[name].get_multi(stat)

    def get_value(self, name: str, stat: str) -> float:
        if name not in self:
            logger.error(f"Unknown Companion name: {name}. Returning 0 / no bonus.")
            return 0
        return self[name].get_value(stat)

    @property
    def owned_names(self) -> set[str]:
        return {name for name, companion in self.items() if companion.owned}

    @property
    def upgraded_names(self) -> set[str]:
        return {name for name, companion in self.items() if companion.upgraded}
