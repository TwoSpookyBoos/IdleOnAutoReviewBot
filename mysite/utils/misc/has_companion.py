from flask import g as session_data

def has_companion(companion_name: str) -> bool:
    return companion_name in session_data.account.companions