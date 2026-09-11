from utils.safer_data_handling import safe_loads, safer_convert


class ColoScores(dict[int, int]):
    """Personal best Colosseum scores, keyed by Colosseum index."""

    def __init__(self, raw_data: dict):
        super().__init__()
        raw_colo_scores = safe_loads(raw_data.get('FamValColosseumHighscores', []))
        for colo_index, colo_score in enumerate(raw_colo_scores):
            self[colo_index] = safer_convert(colo_score, 0)
