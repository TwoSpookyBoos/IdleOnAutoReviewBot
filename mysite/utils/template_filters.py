import hashlib
import os

from flask import url_for

from config import app


def get_resource(dir_: str, filename: str, autoversion: bool = False) -> str:
    path = f"{dir_}/{filename}"
    suffix = ""

    # cache invalidation
    if autoversion:
        full_path = os.path.join(app.static_folder, path)
        mtime = os.path.getmtime(full_path)
        suffix = hashlib.md5(str(mtime).encode()).hexdigest()[:8]
        suffix = f"?v={suffix}"

    return url_for("static", filename=f"{path}") + suffix


@app.template_filter("style")
def style(filename: str):
    return get_resource("styles", f"{filename}.css", True)


@app.template_filter("script")
def script(filename: str):
    return get_resource("scripts", f"{filename}.js", True)


@app.template_filter("img")
def img(filename: str):
    return get_resource("imgs", filename)


@app.template_filter("cards")
def cards(filename: str):
    return img(f"cards/{filename}.png")


@app.template_filter("ensure_data")
def ensure_data(results: list):
    return bool(results)
