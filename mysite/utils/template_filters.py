import hashlib
import os
from pathlib import Path

from flask import url_for

from config import app


def get_resource(dir_: str, filename: str) -> str:
    path = Path(dir_) / filename

    return url_for("static", filename=path.as_posix())


@app.template_filter("style")
def style(filename: str):
    return get_resource("styles", f"{filename}.css")


@app.template_filter("script")
def script(filename: str):
    return get_resource("scripts", f"{filename}.js")


@app.template_filter("img")
def img(filename: str):
    return get_resource("imgs", filename)


@app.template_filter("cards")
def cards(filename: str):
    return img(f"cards/{filename}.png")


@app.template_filter("ensure_data")
def ensure_data(results: list):
    return bool(results)
