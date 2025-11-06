from flask import g as session_data
from consts.consts_idleon import companions_data
from utils.logging import get_logger

logger = get_logger(__name__)

def has_companion(companion_name: str) -> bool:
    if companion_name not in companions_data:
        # raise ValueError(f"Querying unknown companion {companion_name}")
        logger.error(f"Unknown Companion name: {companion_name}. Returning False / not owned.")
        return False
    return companion_name in session_data.account.companions
