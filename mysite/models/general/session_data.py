from dataclasses import dataclass
from flask import g
from flask.ctx import _AppCtxGlobals
from models.general.account import Account

from werkzeug.local import LocalProxy


@dataclass
class SessionData(_AppCtxGlobals):
    account: Account

session_data: SessionData = LocalProxy(lambda: g)