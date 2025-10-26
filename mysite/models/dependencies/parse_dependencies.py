from models.account_parser import _parse_general, _parse_w6, _parse_characters, _parse_w5, _parse_w4, _parse_w3, \
    _parse_w2, _parse_w1, _parse_switches, _parse_master_classes, _parse_companions, _parse_caverns


def parse_args(account, run_type):
    return {
        _parse_caverns: [account],
        _parse_characters: [account, run_type],
        _parse_companions: [account],
        _parse_general: [account],
        _parse_master_classes: [account],
        _parse_switches: [account],
        _parse_w1: [account],
        _parse_w2: [account],
        _parse_w3: [account],
        _parse_w4: [account],
        _parse_w5: [account],
        _parse_w6: [account],
    }


def parse_dependencies():
    return {
        _parse_caverns: [_parse_general],
        _parse_characters: [],
        _parse_companions: [],
        _parse_general: [_parse_characters],
        _parse_master_classes: [_parse_general],
        _parse_switches: [],
        _parse_w1: [_parse_general],
        _parse_w2: [_parse_general],
        _parse_w3: [_parse_general],
        _parse_w4: [_parse_characters, _parse_general],
        _parse_w5: [_parse_characters],
        _parse_w6: [_parse_general],
    }
