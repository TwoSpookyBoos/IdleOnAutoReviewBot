from utils.safer_data_handling import safe_loads, safer_index


class Quest:
    def __init__(self, name: str):
        self.name: str = name
        self.completed_chars: list[int] = []
        self.accepted_chars: list[int] = []
        # Unreliable: quests never interacted with are absent entirely
        self.unaccepted_chars: list[int] = []

    @property
    def completed_count(self) -> int:
        return len(self.completed_chars)


class Quests(dict[str, Quest]):
    def __init__(self, raw_data: dict, character_count: int):
        super().__init__()
        # Raw quest statuses per character: 1 completed, 0 accepted, else unaccepted
        self.by_character: list[dict[str, int]] = [
            safe_loads(raw_data.get(f"QuestComplete_{index}", {}))
            for index in range(character_count)
        ]
        for char_index, statuses in enumerate(self.by_character):
            for name, status in statuses.items():
                quest = self.setdefault(name, Quest(name))
                if status == 1:
                    quest.completed_chars.append(char_index)
                elif status == 0:
                    quest.accepted_chars.append(char_index)
                else:
                    quest.unaccepted_chars.append(char_index)
        # Per-quest progress counters, e.g. kills toward a quest goal
        self.progress_by_character: list[dict[str, list]] = [
            safe_loads(raw_data.get(f"QuestStatus_{index}", {}))
            for index in range(character_count)
        ]

    def get_progress(self, character_index: int, name: str) -> int:
        progress = safer_index(self.progress_by_character, character_index, {})
        if not isinstance(progress, dict):
            return 0
        try:
            return int(safer_index(progress.get(name, [0]), 0, 0))
        except (TypeError, ValueError):
            return 0

    def completed_count(self, name: str) -> int:
        quest = self.get(name)
        return quest.completed_count if quest else 0
