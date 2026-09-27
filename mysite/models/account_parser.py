from utils.safer_data_handling import safe_loads
from utils.logging import get_logger

logger = get_logger(__name__)


def parse_account(account):
    _parse_wave_1(account)

def _parse_wave_1(account):
    _parse_general(account)
    _parse_w3(account)
    _parse_w4(account)
    _parse_w5(account)

def _parse_general(account):
    account.family_bonuses.calculate_levels(account.characters.safe)
    _parse_general_item_filter(account)
    _parse_general_inventory_slots_account_wide(account)

def _parse_general_item_filter(account):
    account.item_filter = []
    raw_printer_xtra = safe_loads(account.raw_data.get('PrinterXtra', []))
    if len(raw_printer_xtra) >= 121:
        for codeName in raw_printer_xtra[120:]:
            if codeName != 'Blank':
                account.item_filter.append(codeName)

def _parse_general_inventory_slots_account_wide(account):
    account.inventory.calculate_owned(
        account.characters,
        account.autoloot,
        account.event_points_shop['Secret Pouch'].owned,
        account.gemshop.bundles['bon_f'].owned,
    )

def _parse_w3(account):
    _parse_w3_deathnote(account)
    _parse_w3_equinox(account)

def _parse_w3_deathnote(account):
    # Dependency: _parse_character_class_lists
    account.death_note.calculate_apocalypse_characters(account.characters.barbs, account.characters.bbs)
    account.death_note.calculate_kills(account.characters)
    account.death_note.calculate_rift_meowed(account.characters)

def _parse_w3_equinox(account):
    account.equinox.calculate_unlocked(account.achievements, account.research.grid['Equinox Nightmares'].level)

def _parse_w4(account):
    _parse_w4_rift(account)
    _parse_w4_breeding(account)

def _parse_w4_rift(account):
    # Seam: hands the model the already-parsed quest data it needs
    account.rift.calculate_unlocked(account.quests.by_character)

def _parse_w4_breeding(account):
    # Seam: egg slots need gem shop and merits
    account.breeding.calculate_egg_slots(
        account.gemshop.purchases['Royal Egg Cap'].owned,
        account.merits[3][2].level,
    )

def _parse_w5(account):
    _parse_w5_slab(account)
    _parse_w5_divinity(account)

def _parse_w5_slab(account):
    account.registered_slab = set(safe_loads(account.raw_data.get("Cards1", [])))

def _parse_w5_divinity(account):
    account.divinity.link_characters(account.characters.safe)
