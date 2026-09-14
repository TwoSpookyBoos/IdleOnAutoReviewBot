from consts.consts_w5 import npc_tokens

from utils.safer_data_handling import safer_convert, safer_index


class NpcTokens(dict[str, int]):
    """Counts of each NPC token owned, keyed by item codename."""

    def __init__(self, raw_data: dict):
        super().__init__()
        raw_npc_tokens = raw_data.get('CYNPC', [])
        for token_index, token_name in enumerate(npc_tokens):
            self[token_name] = safer_convert(safer_index(raw_npc_tokens, token_index, 0), 0)

    def owned(self, token_name: str) -> bool:
        return self.get(token_name, 0) > 0
