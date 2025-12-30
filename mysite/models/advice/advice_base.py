class AdviceBase:
    """
    Args:
        **extra: a dict of extra information that hasn't been accounted for yet
    """

    _children = "_true"
    _collapse = None
    _true = [True]
    name = ""

    def __init__(self, collapse: bool | None = None, **extra):
        # assign all extra kwargs as a field on the object
        self._collapse: bool | None = collapse
        for k, v in extra.items():
            setattr(self, k, v)

    def __bool__(self) -> bool:
        children = getattr(self, self._children, list())
        if isinstance(children, dict):
            children = sum(children.values(), list())
        return any(filter(bool, children))

    def __str__(self) -> str:
        return self.name

    @property
    def collapse(self) -> bool:
        return self._collapse if self._collapse is not None else not bool(self)

    @collapse.setter
    def collapse(self, _value: bool):
        self._collapse = _value

    @property
    def dataset(self) -> list:
        return [[attr, getattr(self, attr, False)] for attr in ["optional", "completed", "informational", "unrated", "unreached", "overwhelming"]]
