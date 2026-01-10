import re
from typing import Any

from consts.consts_autoreview import ignorable_labels
from models.advice.advice_base import AdviceBase
from utils.text_formatting import kebab

class LabelBuilder:
    wrapper = "span"

    def __init__(self, label):
        matches = re.findall(r"\{\{.+?}}", label)

        if not matches:
            self.label = label
            return

        for match in matches:
            text, url = match.strip("{} ").split("|")
            link = f'<a href="{url}">{text}</a>'

            label = label.replace(match, link)

        self.label = f"<{self.wrapper}>{label}</{self.wrapper}>"


class Advice(AdviceBase):
    """
    Args:
        label (str): the display name of the advice
        picture_class (str): CSS class to link the image icon to the advice, e.g. 'bean-slices'
        progression: numeric (usually), how far towards the goal did the item progress?
        goal: the target level or amount of the advice
        unit (str): if there is one, usually "%" or x
    """

    def __init__(
            self, label: str,
            picture_class: str,
            progression: Any = "",
            goal: Any = "",
            unit: str = "",
            value_format: str = "{value}{unit}",
            resource: str = "",
            completed: bool | None = None,
            unrated: bool = False,
            overwhelming: bool = False,
            optional: bool = False,
            potential: Any = "",
            **extra
    ):
        super().__init__(**extra)

        self.label: str = label if extra.get("as_link") else LabelBuilder(label).label
        if picture_class and picture_class[0].isdigit():
            picture_class = f"x{picture_class}"
        self.picture_class: str = picture_class
        self.potential: str = str(potential)
        self.unit: str = unit
        self.value_format: str = value_format
        self.resource: str = kebab(resource)
        self.percent: float = 0.0
        self.change_progress(progression, goal)
        if completed is True:
            self.completed = completed
            self.mark_advice_completed(True)
        self.unrated: bool = unrated
        self.overwhelming = overwhelming
        self.optional = optional

    @property
    def css_class(self) -> str:
        name = kebab(self.picture_class)
        return name

    def __str__(self) -> str:
        return self.label

    def __extract_float(self, value: str | float | int) -> float | None:
        """
        Extracts a float from a string,
        """
        if (value is None):
            return None
        if (isinstance(value, str)):
            float_re = re.compile(r'((?:\d+|,)+(?:\.\d+)?)')
            res = float_re.search(value)
            if res is None or len(res.groups()) != 1:
                return None

            # Sanitize the value from all commas
            val = res[0].replace(',', '')
            try:
                return float(val)
            except ValueError:
                # Just in case
                return None
        elif (isinstance(value, (int, float))):
            return float(value)
        return value

    def __calculate_progress_box_width_numeric(self, calc_num: float, goal_num: float) -> float:
        if calc_num is None or goal_num is None:
            return 0.0

        if goal_num == 0:
            return 0.0 # A goal of 0 currently makes no sense, since descending progression is not supported

        percentage = round(100 * calc_num / goal_num, 2)
        return min(percentage, 100.0)

    def update_optional(self, parent_value: bool):
        self.optional = parent_value

    def mark_advice_completed(self, force=False):
        def complete():
            self.progression = ""
            self.goal = "✔"
            self.completed = True
            self.status = "gilded"

        if force:
            complete()

        # Only let the automated completion run if self.completed has not been manually set already
        if self.completed is None:
            if not self.goal and str(self.progression).endswith('+'):
                self.completed = True

            elif not self.goal and str(self.progression).endswith('%'):
                try:
                    if float(str(self.progression).strip('%')) >= 100:
                        complete()
                except:
                    pass

            elif self.percent == '100%':
                # If the progress bar is set to 100%
                complete()

            else:
                try:
                    prog = str(self.progression).strip('x%')
                    goal = str(self.goal).strip('x%')
                    if self.goal and self.progression and float(prog) >= float(goal):
                        complete()
                except:
                    pass

    def change_progress(self, progression: Any, goal: Any):
        self.progression = str(progression)
        self.goal = str(goal)
        if self.unit:
            if self.progression:
                self.progression = self.value_format.format(
                    value=self.progression, unit=self.unit
                )
            if self.goal:
                self.goal = self.value_format.format(
                    value=self.goal, unit=self.unit
                )
        self.completed = None
        if self.goal in ("✔", "") or self.label.startswith(ignorable_labels):
            self.completed = True
        self.status = None
        if self.goal == "✔":
            self.status = "gilded"
        self.__calculate_percent()

    def __calculate_percent(self):
        numeric_progression = self.__extract_float(self.progression)
        numeric_potential = self.__extract_float(self.potential)
        numeric_goal = self.__extract_float(self.goal)
        self.percent = 0.0
        if (numeric_goal is not None and numeric_progression is not None):
            # NOTE: This was an idea to handle cases, where progras is decending
            # Ill have to look into the overwhelming attr
            # if(numeric_goal < numeric_progression):
            #     numeric_progression, numeric_goal = numeric_goal, numeric_progression
            #     numeric_potential = numeric_goal - numeric_progression

            self.percent = self.__calculate_progress_box_width_numeric(
                numeric_progression, numeric_goal
            )
            self.potential_percent = self.__calculate_progress_box_width_numeric(
                numeric_potential, numeric_goal
            )

            # prevent overflow of potential percent
            if (self.percent + self.potential_percent) > 100:
                self.potential_percent = 100 - self.percent
