import functools

from models.advice.advice_base import AdviceBase
from models.advice.advice import Advice
from utils.text_formatting import kebab


@functools.total_ordering
class AdviceGroup(AdviceBase):
    """
    Contains a list of `Advice` objects

    Args:
        tier (str): alphanumeric tier of this group's advices (e.g. 17, S)
        pre_string (str): the start of the group title
        post_string (str): trailing advice
        formatting (str): HTML tag name (e.g. strong, em)
        collapsed (bool): should the group be collapsed on load?
        advices (list<Advice>): a list of `Advice` objects, each advice on a separate line
    """

    _children = "advices"
    __compare_by = ["tier"]

    def __init__(
        self,
        tier: str | int,
        pre_string: str,
        post_string: str = "",
        formatting: str = "",
        picture_class: str = "",
        collapse: bool | None = None,
        advices: list[Advice] | dict[str, list[Advice]] = [],
        completed: bool = None,
        informational: bool = False,
        overwhelming: bool | None = False,
        optional: bool = False,
        **extra,
    ):
        super().__init__(collapse, **extra)

        self.tier: str = str(tier)
        self.pre_string: str = pre_string
        self.post_string: str = post_string
        self.formatting: str = formatting
        self._picture_class: str = picture_class
        self.advices = advices
        self.completed = completed
        self.informational = informational
        self.overwhelming = overwhelming
        self.optional = optional

    def __str__(self) -> str:
        return ", ".join(map(str, self.advices))

    @property
    def advices(self):
        return self._advices

    @advices.setter
    def advices(self, _advices):
        self._advices = (
            {"default": _advices} if isinstance(_advices, list) else _advices
        )

    @property
    def picture_class(self) -> str:
        name = kebab(self._picture_class)
        return name

    @property
    def heading(self) -> str:
        text = ""
        if self.tier:
            text += f"{'Optional ' if self.optional else ''}Tier {self.tier}"
        if self.informational:
            text += "Info"
        if self.pre_string:
            text += f"{' - ' if text else ''}{self.pre_string}"
        if text:
            text += ":"

        return text

    def _is_valid_operand(self, other):
        return all(hasattr(other, field) for field in self.__compare_by)

    def _coerce_to_int(self, field):
        try:
            return int(getattr(self, field))
        except ValueError:
            return 999

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return all(
            self._coerce_to_int(field) == other._coerce_to_int(field)
            for field in self.__compare_by
        )

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return all(
            self._coerce_to_int(field) < other._coerce_to_int(field)
            for field in self.__compare_by
        )

    def remove_empty_subgroups(self):
        if isinstance(self.advices, list):
            self.advices = [value for value in self.advices if value]
        if isinstance(self.advices, dict):
            self.advices = {
                key: filtered_advice_list
                for key, advice_list in self.advices.items()
                if (filtered_advice_list := [v for v in advice_list if v])
            }

    def sort_advices(self, reverseBool):
        if 'default' in self.advices:
            if isinstance(self.advices['default'], list):
                try:
                    self.advices['default'] = list[Advice] = sorted(
                        self.advices['default'],
                        key=lambda a: float(str(a.progression).strip('%')),
                        reverse=reverseBool
                    )
                except:
                    pass

    def check_for_completeness(self, ignorable=tuple('Weekly Ballot')):
        """
        Used when a bool for complete was not passed in during initialization of the AdviceGroup
        """
        if self.completed is not None:
            return
        elif self.tier != '':
            return False
        else:
            if isinstance(self.advices, list):
                temp_advices = [advice for advice in self.advices if not advice.completed]
            elif isinstance(self.advices, dict):
                temp_advices = []
                for key, value in self.advices.items():
                    if isinstance(value, list):
                        #flattern to a single list
                        temp_advices.extend([advice for advice in value if not advice.completed])
            else:
                temp_advices = []
            self.completed = len(temp_advices) == 0  #True if 0 length, False otherwise

    def set_overwhelming(self, overwhelming):
        self.overwhelming = overwhelming
        if isinstance(self.advices, list):
            for advice in self.advices:
                advice.overwhelming = overwhelming
        if isinstance(self.advices, dict):
            for value in self.advices.values():
                for advice in value:
                    advice.overwhelming = overwhelming

    def check_for_optional(self, max_tier: int, override=None):
        if override is not None:
            self.optional = override
        if self.optional is not True:
            if self.tier.isdigit():
                self.optional = int(self.tier) > max_tier
        if self.optional:
            # If Optional, all Children will be Optional too
            if isinstance(self.advices, list):
                for advice in self.advices:
                    advice.update_optional(self.optional)
            if isinstance(self.advices, dict):
                for value in self.advices.values():
                    for advice in value:
                        advice.update_optional(self.optional)

    def mark_advice_completed(self):
        if isinstance(self.advices, list):
            [advice.mark_advice_completed() for advice in self.advices]
        elif isinstance(self.advices, dict):
            for advice_list in self.advices.values():
                if isinstance(advice_list, list):
                    [advice.mark_advice_completed() for advice in advice_list]
