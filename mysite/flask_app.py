import json
import traceback
from datetime import datetime
from json import JSONDecodeError

from flask import g, render_template, request, redirect, Response, send_from_directory

import consts
import taskSuggester
from utils.data_formatting import HeaderData
from models.models import AdviceWorld
from models.custom_exceptions import (
    UserDataException,
    UsernameBanned,
    ProfileNotFound,
    EmptyResponse,
    IEConnectionFailed,
)
from utils.text_formatting import (
    is_username,
    json_schema_valid,
    format_character_name,
)
from utils.logging import get_logger, name_for_logging, log_browser_data
from utils.template_filters import *


logger = get_logger(__name__)
FQDN = "ieautoreview-scoli.pythonanywhere.com"
FQDN_BETA = f"beta-{FQDN}"


def get_user_input() -> str:
    return (request.args.get("player") or json.loads(request.data).get("player", "")).strip()


def parse_user_input() -> str | dict | None:
    data = get_user_input()

    if not data:
        return

    if is_username(data):
        parsed = format_character_name(data)

    elif json_schema_valid(data):
        parsed = json.loads(data)

    else:
        raise UserDataException("Submitted data not valid.", data)

    return parsed


def store_user_preferences():
    if request.method == "POST":
        args = json.loads(request.data)
    elif request.method == "GET":
        args = request.args.to_dict()
    else:
        raise ValueError(f"Unknown request method: {request.method}")

    for switch in consts.switches:
        setattr(g, switch["name"], args.get(switch["name"], False) in ["on", "True", "true", True])


def get_user_preferences():
    return {switch["name"]: getattr(g, switch["name"]) for switch in consts.switches}


def switches():
    return [
        (*switch.values(), ("on" if get_user_preferences()[switch["name"]] else "off"))
        for switch in consts.switches
    ]


@app.route("/results", methods=["POST"])
def results() -> Response | str:
    page: str = "results.html"
    error: str = ""
    reviews: list[AdviceWorld] | None = list()
    headerData: HeaderData | None = None
    is_beta: bool = FQDN_BETA in request.host

    store_user_preferences()

    live_link = "live"
    beta_link = "beta"

    name_or_data: str | dict = ""
    try:
        name_or_data = parse_user_input()

        if name_or_data:
            reviews, headerData = autoReviewBot(name_or_data)

        name = name_for_logging(name_or_data, headerData, "index.html")
        log_browser_data(name)

    except UserDataException as ude:
        logger.error(ude.msg)
        error = ude.msg_display

    except UsernameBanned as ban:
        msg = f"Account banned: {ban.username}"
        data = None
        logger.error(
            "PETTY BITCH MODE ACTIVATED. Banned name entered: %s", ban.username
        )

        create_and_populate_log_files(data, headerData, msg, name_or_data, ban)

        error = "You have been banned from using this tool. Goodbye."

    except ProfileNotFound as e:
        msg = f"Public profile not found: {e.username}"
        data = None

        dirname = create_and_populate_log_files(data, headerData, msg, name_or_data, e)
        error = e.msg_display.format(dirname)

    except EmptyResponse as e:
        msg = f"Empty response: {e.username}"
        data = None

        dirname = create_and_populate_log_files(data, headerData, msg, name_or_data, e)
        error = e.msg_display.format(dirname)

    except IEConnectionFailed as e:
        msg = f"Error connecting to {e.url}"
        data = e.stacktrace

        dirname = create_and_populate_log_files(data, headerData, msg, name_or_data, e)
        error = e.msg_display.format(dirname)

    except JSONDecodeError as e:
        msg = str(e)
        data = e.doc

        e.dirname = "faulty_data"
        dirname = create_and_populate_log_files(data, headerData, msg, name_or_data, e)  # noqa
        error = (
            "Looks like the data you submitted is corrupted. The issue has been "
            "reported and will be investigated. If the problem persists let us "
            f"know in the Discord server, mention '{dirname}'"
        )

    except Exception as e:
        logger.exception("An unexpected error occurred:\n", exc_info=e)
        msg = os.linesep.join([str(e), "", traceback.format_exc()])
        data = get_user_input()

        e.dirname = "other"
        dirname = create_and_populate_log_files(
            data, headerData, msg, name_or_data, e
        )

        error = (
            "Looks like something went wrong while handling your account data. "
            "The issue has been reported and will be investigated. If the "
            "problem persists let us know in the Discord server, mention "
            f"'{dirname}'"
        )
    return render_template(
        page,
        reviews=reviews,
        header=headerData,
        error=error,
        beta=is_beta,
        live_link=live_link,
        beta_link=beta_link,
        switches=switches(),
        **get_user_preferences(),
    )


@app.route("/", methods=["GET"])
def index() -> Response | str:
    is_beta: bool = FQDN_BETA in request.host

    live_link = "live"
    beta_link = "beta"

    player = request.args.to_dict().get("player")

    store_user_preferences()

    return render_template(
        "index.html",
        beta=is_beta,
        live_link=live_link,
        beta_link=beta_link,
        player=player,
        switches=switches(),
    )


def create_and_populate_log_files(data, headerData, msg, name_or_data, error):
    # if os.environ.get("USER") == "niko":
    #     raise error

    username = name_for_logging(name_or_data, headerData)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    dirpath = app.config["LOGS"]/error.dirname/username
    filemsg = dirpath/now/"message.log"
    filedata = dirpath/now/"data.log"

    (dirpath/now).mkdir(parents=True, exist_ok=True)

    with open(filemsg, "w") as user_log:
        user_log.writelines(msg + os.linesep)

    if data:
        with open(filedata, "w") as user_log:
            user_log.writelines(data + os.linesep)

    return f"{error.dirname}/{username}/{now}"


@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt")


# Serve sitemap.xml file
@app.route("/sitemap.xml")
def sitemap_xml():
    return send_from_directory(app.static_folder, "sitemap.xml")


@app.route("/live", methods=["GET", "POST"])
def live() -> Response:
    link = f"https://{FQDN}?" + "&".join(f"{k}={v}" for k, v in request.args.items())
    return redirect(link)


@app.route("/beta", methods=["GET", "POST"])
def beta() -> Response:
    link = f"https://{FQDN_BETA}?" + "&".join(
        f"{k}={v}" for k, v in request.args.items()
    )
    return redirect(link)


@app.route("/logtest", methods=["GET"])
def logtest():
    logger.info("Logging works")
    return "Hello, World!"


def autoReviewBot(
    capturedCharacterInput,
) -> tuple[list[AdviceWorld], HeaderData] | tuple[None, None]:
    reviewInfo: list[AdviceWorld] | None = None
    headerData: HeaderData | None = None

    if capturedCharacterInput:
        reviewInfo, headerData = taskSuggester.main(capturedCharacterInput)

    return reviewInfo, headerData


@app.errorhandler(404)
def page_not_found(e):
    try:
        if len(request.path) < 16:
            capturedCharacterInput = request.path[1:].strip().replace(" ", "_").lower()
            if capturedCharacterInput.find(".") == -1:
                return redirect(url_for("index", player=capturedCharacterInput))
            else:
                return redirect(
                    url_for("index")
                )  # Probably should get a real 404 page at some point
        else:
            return redirect(
                url_for("index")
            )  # Probably should get a real 404 page at some point
    except:  # noqa
        return redirect(
            url_for("index")
        )  # Probably should get a real 404 page at some point


if __name__ == "__main__":
    app.run()
