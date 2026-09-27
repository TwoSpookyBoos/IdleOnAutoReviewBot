from utils.safer_data_handling import safe_loads


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

    def completed_count(self, name: str) -> int:
        quest = self.get(name)
        return quest.completed_count if quest else 0
