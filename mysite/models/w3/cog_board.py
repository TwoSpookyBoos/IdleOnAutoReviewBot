from utils.safer_data_handling import safe_loads

# Board slots before the cog-making characters
board_slots = 95


class CogBoard:
    def __init__(self, raw_data: dict):
        try:
            raw_cogs = safe_loads(raw_data.get("CogO", []))
            self.blank_slots: int | None = sum(
                1 for cog in raw_cogs[0:board_slots] if cog == "Blank"
            )
        except (TypeError, ValueError):
            self.blank_slots = None
