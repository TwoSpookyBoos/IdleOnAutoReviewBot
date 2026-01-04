from models.advice.advice_group import AdviceGroup

class TabbedAdviceGroupTab:
    completed = None
    informational = None
    optional = None

    def __init__(self, picture_class: str = "", label: str = ""):
        self.picture_class = picture_class
        self.label = label

    @property
    def dataset(self) -> list:
        return [[attr, getattr(self, attr, False)] for attr in ["completed", "informational", "optional"]]


class TabbedAdviceGroup:
    completed = None
    informational = None
    optional = None
    _children = "tabbed_advices"
    __compare_by = ["tier"]

    def __init__(self, tabbed_advices: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]]):
        self.tabbed_advices = tabbed_advices
        self.tier = min([advice_group._coerce_to_int("tier") for _, advice_group in tabbed_advices.values()])
        self.check_for_informationalness()

    def check_for_completeness(self):
        if self.completed is not None:
            return
        self.completed = True
        for tab, advice_group in self.tabbed_advices.values():
            advice_group.check_for_completeness()
            if not advice_group.completed:
                self.completed = False
            else:
                tab.completed = True

    def check_for_informationalness(self):
        if self.informational is not None:
            return
        self.informational = True
        for tab, advice_group in self.tabbed_advices.values():
            if not advice_group.informational:
                self.informational = False
            else:
                tab.informational = True

    def check_for_optional(self, max_tier: int):
        self.optional = True
        for tab, advice_group in self.tabbed_advices.values():
            advice_group.check_for_optional(max_tier)
            if not advice_group.optional:
                self.optional = False
            else:
                tab.optional = True

    def set_overwhelming(self, overwhelming: bool):
        for _, group in self.tabbed_advices.values():
            group.set_overwhelming(overwhelming)

    def remove_empty_subgroups(self):
        for _, group in self.tabbed_advices.values():
            group.remove_empty_subgroups()

    @property
    def dataset(self) -> list:
        return [[attr, getattr(self, attr, False)] for attr in ["completed", "informational", "optional"]]

    @property
    def tabbed_advices(self):
        return self._tabbed_advices

    @tabbed_advices.setter
    def tabbed_advices(self, tabbed_advices: dict[str, tuple[TabbedAdviceGroupTab, AdviceGroup]]):
        self._tabbed_advices = {key: tabbed_advice for key, tabbed_advice in tabbed_advices.items() if tabbed_advice[1]}

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
