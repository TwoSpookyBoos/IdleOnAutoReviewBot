from consts.consts_autoreview import ValueToMulti
from models.w7.research import Research
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class Glimbo:
    def __init__(self, raw_data: dict):
        raw_research_info = safe_loads(raw_data.get("Research", []))
        # "Research"[12] in source: trades per Research[26] slot.
        # Last updated in v2.531.0
        self.trades_by_slot: list[float] = [
            safer_convert(trades, 0.0)
            for trades in safer_index(raw_research_info, 12, [])
        ]
        # "GlimboTotalTrades" in source. Last updated in v2.531.0
        self.total_trades: int = round(sum(self.trades_by_slot))
        self.drop_rate_multi: float = 1.0

    def calculate_drop_rate_multi(self, research: Research):
        # "GlimboDRmulti" in source. Last updated in v2.531.0
        insider_trading = research.grid["Glimbo Insider Trading Secrets"]
        if insider_trading.value >= 1:
            self.drop_rate_multi = max(1.0, ValueToMulti(insider_trading.total_value))
        else:
            self.drop_rate_multi = 1.0
