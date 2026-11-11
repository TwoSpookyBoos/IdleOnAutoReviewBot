from dataclasses import dataclass
from typing import TYPE_CHECKING

from flask import g
from flask.ctx import _AppCtxGlobals
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    # Type-only: a runtime import would be circular, account imports every model
    from models.general.account import Account


@dataclass
class SessionData(_AppCtxGlobals):
    account: "Account"

session_data: SessionData = LocalProxy(lambda: g)