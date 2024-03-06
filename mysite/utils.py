import logging
import os
import sys

from flask import g


def pl(_list: list, suffix_singular: str = "", suffix_plural: str = 's') -> str:
    """Pluralize"""
    return suffix_plural if len(_list) > 1 else suffix_singular


DEFAULT_FORMAT = '%(asctime)s | %(name)s | %(funcName)s:%(lineno)d~ [%(levelname)s] %(message)s'


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not _try_colorise(logger):
        _set_regular_logger(logger)

    return logger


def _try_colorise(logger):
    is_local_instance = os.environ.get('PYTHONANYWHERE_DOMAIN', None) is None
    if is_local_instance:
        import coloredlogs

        coloredlogs.DEFAULT_FIELD_STYLES['levelname']['color'] = 'white'
        coloredlogs.install(
            level='DEBUG',
            fmt=DEFAULT_FORMAT,
            stream=sys.stdout,
            logger=logger
        )
    return is_local_instance


def _set_regular_logger(logger: logging.Logger):
    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def letterToNumber(inputLetter: str) -> int:
    return "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(inputLetter)


def session_singleton(cls):
    def getinstance(*args, **kwargs):
        if not hasattr(g, "data"):
            return cls(*args, **kwargs)
        return g.data
    return getinstance
