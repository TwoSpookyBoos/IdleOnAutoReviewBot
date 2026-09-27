from consts.consts_w3 import printer_all_indexes_being_printed
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_get
from utils.text_formatting import getItemDisplayName

logger = get_logger(__name__)


class Printer:
    def __init__(self, raw_data: dict):
        # Stored samples, best first
        self.samples: dict[str, list[float]] = {}
        self.printing: dict[str, list] = {}

        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.gold_relic_days: int = safer_get(raw_optlacc, 125, 0)
        self.supreme_wiring_days: int = safer_get(raw_optlacc, 323, 0)
        self.biggole_mole_days: int = safer_get(raw_optlacc, 354, 0)
        self.moon_of_print_days: int = safer_get(raw_optlacc, 364, 0)

        raw_print = safe_loads(raw_data.get("Print", [0, 0, 0, 0, 0, "Blank"]))[5:]
        raw_printer_xtra = safe_loads(raw_data.get("PrinterXtra", []))
        sample_names = raw_print[0::2] + raw_printer_xtra[0:119:2]
        sample_values = raw_print[1::2] + raw_printer_xtra[1:119:2]

        for sample_index, codename in enumerate(sample_names):
            if not codename:
                continue
            name = getItemDisplayName(codename)
            if sample_index in printer_all_indexes_being_printed:
                values = self.printing.setdefault(name, [])
                try:
                    values.append(sample_values[sample_index])
                except IndexError:
                    logger.exception(f"Failed on sample {sample_index} '{codename}'")
            elif codename != "Blank":
                values = self.samples.setdefault(name, [])
                try:
                    values.append(float(sample_values[sample_index]))
                except (IndexError, TypeError, ValueError):
                    logger.exception(f"Failed on sample {sample_index} '{codename}'")
        for values in self.samples.values():
            values.sort(reverse=True)

    def best_sample(self, name: str) -> float:
        return max(self.samples.get(name) or [0])

    def is_printing(self, name: str) -> bool:
        return name in self.printing
