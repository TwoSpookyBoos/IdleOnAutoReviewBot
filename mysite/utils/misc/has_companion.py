from flask import g as session_data
from consts.consts_idleon import companions_data

def has_companion(companion_name: str) -> bool:
    if companion_name not in companions_data:
        raise ValueError(f"Querying unknown companion {companion_name}")
    return companion_name in session_data.account.companions