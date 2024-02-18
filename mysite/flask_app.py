import hashlib
import json
import os
from json import JSONDecodeError
from config import app
from flask import g, render_template, request, url_for, redirect, Response
import idleonTaskSuggester
import traceback

from utils import get_logger

logger = get_logger(__name__)
FQDN = "ieautoreview-scoli.pythonanywhere.com"
FQDN_BETA = f"beta-{FQDN}"


def format_character_name(name: str) -> str:
    name = name.strip().lower().replace(' ', '_')

    return name


def get_character_input() -> str:
    data: str = request.args.get('player') or request.form.get("player", '')

    try:
        parsed = json.loads(data)
    except JSONDecodeError:
        parsed = data

    if isinstance(parsed, str):
        parsed = format_character_name(parsed)

    if not isinstance(parsed, (str, dict)):
        raise ValueError('Submitted data neither player name nor raw data.', parsed)

    return parsed


def store_user_preferences():
    if request.method == 'POST':
        args = request.form
    elif request.method == 'GET':
        args = request.args
    else:
        raise ValueError(f'Unknown request method: {request.method}')
    g.autoloot = args.get('autoloot', False) in ['on', "True"]
    g.sheepie = args.get('sheepie', False) in ['on', "True"]
    g.doot = args.get('doot', False) in ['on', "True"]
    g.order_tiers = args.get('order_tiers', False) in ['on', "True"]
    g.handedness = args.get('handedness', False) in ['on', "True"]


def get_user_preferences():
    return dict(
        autoloot=g.autoloot,
        sheepie=g.sheepie,
        doot=g.doot,
        order_tiers=g.order_tiers,
        handedness=g.handedness,
    )


def switches():
    vals = [
        ("Autoloot purchased", "autoloot", "", ""),
        ("Sheepie pet acquired", "sheepie", "", ""),
        ("Doot pet acquired", "doot", "", ""),
        ("Order groups by tier", "order_tiers", "", ""),
        ("Handedness", "handedness", "L", "R"),
    ]
    return [
        (label, name, on, off, ("on" if get_user_preferences()[name] else "off"))
        for label, name, on, off in vals
    ]


@app.route("/", methods=["GET", "POST"])
def index() -> Response | str:
    page: str = 'results.html'
    error: bool = False
    pythonOutput: list | None = None
    is_beta: bool = FQDN_BETA in request.host
    logger.info(request.host)
    url_params = request.query_string.decode("utf-8")
    live_link = f"live?{url_params}"
    beta_link = f"beta?{url_params}"

    store_user_preferences()

    try:
        capturedCharacterInput: str | dict = get_character_input()
        logger.info("request.args.get('player'): %s %s", type(capturedCharacterInput), capturedCharacterInput)
        if request.method == 'POST' and isinstance(capturedCharacterInput, str):
            return redirect(url_for('index', player=capturedCharacterInput, **get_user_preferences()))

        if capturedCharacterInput:
            pythonOutput = autoReviewBot(capturedCharacterInput)

    except Exception as reason:
        traceback.print_exc()
        if os.environ.get("USER") == 'niko':
            raise reason
        logger.exception('Could not get Player from Request Args: %s', reason, exc_info=reason)
        error = True

    return render_template(
        page,
        htmlInput=pythonOutput, error=error, beta=is_beta,
        live_link=live_link, beta_link=beta_link,
        switches=switches(), **get_user_preferences()
    )


@app.route("/live", methods=["GET", "POST"])
def live() -> Response:
    link = f"https://{FQDN}?" + '&'.join(f"{k}={v}" for k, v in request.args.items())
    return redirect(link)


@app.route("/beta", methods=["GET", "POST"])
def beta() -> Response:
    link = f"https://{FQDN_BETA}?" + '&'.join(f"{k}={v}" for k, v in request.args.items())
    return redirect(link)


@app.route("/logtest", methods=["GET"])
def logtest():
    logger.info("Logging works")
    return "Hello, World!"


# @app.route("/")
def autoReviewBot(capturedCharacterInput) -> list | None:
    reviewInfo: list | None = None
    if capturedCharacterInput:
        reviewInfo = idleonTaskSuggester.main(capturedCharacterInput)
    # Do review stuff function, pass into array
    return reviewInfo


@app.errorhandler(404)
def page_not_found(e):
    try:
        if len(request.path) < 16:
            capturedCharacterInput = request.path[1:].strip().replace(" ", "_").lower()
            if capturedCharacterInput.find(".") == -1:
                return redirect(url_for('index', player = capturedCharacterInput))
            else:
                return redirect(url_for('index')) # Probably should get a real 404 page at some point
        else:
            return redirect(url_for('index')) # Probably should get a real 404 page at some point
    except:  # noqa
        return redirect(url_for('index')) # Probably should get a real 404 page at some point


def get_resource(dir_: str, filename: str, autoversion: bool = False) -> str:
    path = f'{dir_}/{filename}'
    suffix = ''

    # cache invalidation
    if autoversion:
        full_path = os.path.join(app.root_path, 'static', path)
        mtime = os.path.getmtime(full_path)
        suffix = hashlib.md5(str(mtime).encode()).hexdigest()[:8]
        suffix = f"?v={suffix}"

    return url_for('static', filename=f"{path}") + suffix


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


app.jinja_env.globals['img'] = img


if __name__ == '__main__':
    app.run()
