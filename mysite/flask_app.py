import base64
import json
import traceback
import uuid
import zlib
from datetime import datetime
from pathlib import Path

import jsonpickle
import requests
from flask import g, render_template, request, redirect, Response, send_from_directory

import consts.consts_autoreview
import consts.consts_idleon
import consts.consts_general
import consts.consts_w1
import consts.consts_w2
import consts.consts_w3
import consts.consts_w4
import consts.consts_w5
import consts.consts_w6
import consts.progression_tiers
import consts.manage_consts  #This import is what runs finalize_consts()
import taskSuggester
from models import custom_exceptions
from utils.data_formatting import HeaderData
from models.models import AdviceWorld
from models.custom_exceptions import (
    UserDataException,
    UsernameBanned,
    ProfileNotFound,
    EmptyResponse,
    APIConnectionFailed,
    BaseCustomException,
    JSONDecodeError,
    WtfDataException,
    DataTooLong,
    VeryOldDataException
)
from utils.text_formatting import (
    is_username,
    json_schema_valid,
    format_character_name, InputType,
)
from utils.logging import (
    ResponseCache,
    get_logger,
    name_for_logging,
    key_for_logging_cache,
    # log_browser_data
)
from utils.template_filters import *


logger = get_logger(__name__)


def get_user_input() -> str:
    return (request.args.get("player") or json.loads(request.data).get("player", "")).strip()


def parse_user_input():
    data = get_user_input()
    parsed = ''

    if not data:
        return None, None

    if len(data) >= 1e6:
        raise DataTooLong("Submitted data is too long.", data)

    if is_username(data):
        parsed, source_string = format_character_name(data)

    elif json_schema_valid(data):
        try:
            parsed = json.loads(data)
            source_string = InputType.JSON
        except json.JSONDecodeError:
            raise custom_exceptions.JSONDecodeError(data)

    else:
        raise UserDataException("Submitted data not valid.", data)

    # logger.debug(f"{source_string = }")
    return parsed, source_string


def store_user_preferences():
    if request.method == "POST":
        args = json.loads(request.data)
    elif request.method == "GET":
        args = request.args.to_dict()
    else:
        raise ValueError(f"Unknown request method: {request.method}")

    for switch in consts.consts_autoreview.switches:
        setattr(g, switch["name"], args.get(switch["name"], False) in ["on", "True", "true", True])


def get_user_preferences():
    return {switch["name"]: getattr(g, switch["name"]) for switch in consts.consts_autoreview.switches}


def switches():
    return [
        (*switch.values(), ("on" if get_user_preferences()[switch["name"]] else "off"))
        for switch in consts.consts_autoreview.switches
    ]

def decode_b64_autoreview(b64_autoreview):
    decoded_data = base64.urlsafe_b64decode(b64_autoreview)
    decompressed_data = zlib.decompress(decoded_data)
    reviews, headerData = jsonpickle.decode(decompressed_data.decode())
    return reviews, headerData

def render_world(world_id, b64_autoreview):
    reviews, headerData = decode_b64_autoreview(b64_autoreview)
    target_review = [world for world in reviews if world.id == world_id]
    return render_template(
        "results.html",
        reviews=target_review if world_id != "all-worlds" else reviews,
        all_reviews=reviews,
        header=headerData,
    )

@app.route("/all-worlds", methods=["POST"])
def all_worlds() -> str:
    return render_world("all-worlds", request.data)

@app.route("/pinchy", methods=["POST"])
def pinchy() -> str:
    return render_world("pinchy", request.data)

@app.route("/general", methods=["POST"])
def general() -> str:
    return render_world("general", request.data)

@app.route("/master-classes", methods=["POST"])
def master_classes() -> str:
    return render_world("master-classes", request.data)

@app.route("/blunder-hills", methods=["POST"])
def blunder_hills() -> str:
    return render_world("blunder-hills", request.data)

@app.route("/yum-yum-desert", methods=["POST"])
def yum_yum_desert() -> str:
    return render_world("yum-yum-desert", request.data)

@app.route("/frostbite-tundra", methods=["POST"])
def frostbite_tundra() -> str:
    return render_world("frostbite-tundra", request.data)

@app.route("/hyperion-nebula", methods=["POST"])
def hyperion_nebula() -> str:
    return render_world("hyperion-nebula", request.data)

@app.route("/smolderin--plateau", methods=["POST"])
def smolderin_plateau() -> str:
    return render_world("smolderin--plateau", request.data)

@app.route("/caverns", methods=["POST"])
def caverns() -> str:
    return render_world("caverns", request.data)

@app.route("/spirited-valley", methods=["POST"])
def spirited_valley() -> str:
    return render_world("spirited-valley", request.data)


@app.route("/results", methods=["POST"])
def results() -> Response | str:
    page: str = "results.html"
    reviews: list[AdviceWorld] | None = list()
    headerData: HeaderData | None = None
    is_beta: bool = app.config["DOMAIN_BETA"] in request.host
    g.request_id = uuid.uuid4().hex[:8]

    store_user_preferences()

    live_link = "live"
    beta_link = "beta"

    name_or_data: str | dict = ""
    try:
        name_or_data, source_string = parse_user_input()
        response = ""
        if name_or_data:
            reviews, headerData = autoReviewBot(name_or_data, source_string)
            pickled_data = jsonpickle.encode([reviews, headerData])
            compressed_data = zlib.compress(pickled_data.encode())
            b64_data = base64.urlsafe_b64encode(compressed_data)
            response = b64_data
            pass

        name = name_for_logging(name_or_data, headerData, "index.html")
        # log_browser_data(name)
        render_template(
            page,
            reviews=reviews,
            header=headerData,
            beta=is_beta,
            live_link=live_link,
            beta_link=beta_link,
            switches=switches(),
            **get_user_preferences(),
        )

    except UserDataException as ude:
        logger.error(ude.msg)
        error = ude.msg_display
        response = error, 400

    except UsernameBanned as ban:
        logger.error("PETTY BITCH MODE ACTIVATED. Banned name entered: %s", ban.username)

        create_and_populate_log_files(None, headerData, ban.log_msg, name_or_data, ban)

        error = ban.msg_base
        response = error, 403

    except ProfileNotFound as e:
        dirname = create_and_populate_log_files(None, headerData, e.log_msg, name_or_data, e)
        error = e.msg_display.format(dirname)
        response = error, 404

    except EmptyResponse as e:
        dirname = create_and_populate_log_files(None, headerData, e.log_msg, name_or_data, e)
        error = e.msg_display.format(dirname)
        response = error, 500

    except APIConnectionFailed as e:
        dirname = create_and_populate_log_files(e.stacktrace, headerData, e.log_msg, name_or_data, e)
        error = e.msg_display.format(dirname)
        response = error, 500

    except JSONDecodeError as e:
        dirname = create_and_populate_log_files(e.data, headerData, str(e), name_or_data, e)
        error = e.msg_display.format(dirname)
        response = error, 400

    except WtfDataException as e:
        #2025-02-14: Commenting out creating a log as the Steam Workaround JSONs from Toolbox land here and are upwards of 10mb in size.
        #I'm not paying extra to store that garbage. -Scoli
        # dirname = create_and_populate_log_files(e.data, headerData, str(e), name_or_data, e)
        # error = e.msg_display.format(dirname)
        error = e.msg_display
        response = error, 400

    except VeryOldDataException as e:
        error = e.msg_display
        response = error, 400

    except Exception as e:
        logger.exception("An unexpected error occurred:\n", exc_info=e)
        msg = os.linesep.join([str(e), "", traceback.format_exc()])
        data = get_user_input()

        setattr(e, "dirname", "other")
        dirname = create_and_populate_log_files(data, headerData, msg, name_or_data, e)  # noqa

        faq = BaseCustomException.let_us_know.format(dirname)
        error = (
            "Looks like something went wrong while handling your account data.<br>"
            f"The issue has been reported and will be investigated.<br>{faq}"
        )
        response = error, 500

    return response


@app.route("/", methods=["GET"])
def index() -> Response:
    is_beta: bool = app.config["DOMAIN_BETA"] in request.host

    live_link = "live"
    beta_link = "beta"

    player = request.args.to_dict().get("player")

    store_user_preferences()

    page = render_template(
        "index.html",
        beta=is_beta,
        live_link=live_link,
        beta_link=beta_link,
        player=player,
        switches=switches(),
    )
    return Response(page, headers={"Cache-Control": "must-revalidate"})


__handled_log_keys = ResponseCache()

def create_and_populate_log_files(data, headerData, msg, name_or_data, error):
    # if os.environ.get("USER") == "niko":
    #     raise error

    if data:
        if isinstance(data, dict):
            data = json.dumps(data, indent=4)

    username = name_for_logging(name_or_data, headerData)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    key = key_for_logging_cache(username, error.dirname, data, msg)

    with __handled_log_keys.get_response_obj(key) as response:
        if response.handled:
            return response.value

        log_subdir = Path(error.dirname)/username/now
        dirpath = app.config["LOGS"]/log_subdir
        filemsg = dirpath/"message.log"
        filedata = dirpath/"data.log"

        dirpath.mkdir(parents=True, exist_ok=True)

        with open(filemsg, "w") as user_log:
            user_log.writelines(msg + os.linesep)

        if data:
            with open(filedata, "w") as user_log:
                user_log.writelines(data + os.linesep)

        val = str(app.config["SERVER_TYPE"]/log_subdir).replace("/", " ▸ ").replace("\\", " ▸ ")
        response.complete(val)
        return val


@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt")


# Serve sitemap.xml file
@app.route("/sitemap.xml")
def sitemap_xml():
    return send_from_directory(app.static_folder, "sitemap.xml")


def format_uri(to_beta=False):
    link = requests.Request(
        "GET",
        app.config["FQDN_BETA" if to_beta else "FQDN"],
        params=request.args or request.form.to_dict()
    ).prepare().url
    return link


@app.route("/live", methods=["GET", "POST"])
def live() -> Response:
    link = format_uri()
    return redirect(link)


@app.route("/beta", methods=["GET", "POST"])
def beta() -> Response:
    link = format_uri(to_beta=True)
    return redirect(link)


@app.route("/logtest", methods=["GET"])
def logtest():
    logger.info("Logging works")
    return "Hello, World!"


def autoReviewBot(
    capturedCharacterInput,
    source_string
) -> tuple[list[AdviceWorld] | None, HeaderData | None]:
    reviewInfo: list[AdviceWorld] | None = None
    headerData: HeaderData | None = None

    if capturedCharacterInput:
        reviewInfo, headerData = taskSuggester.main(capturedCharacterInput, source_string)

    return reviewInfo, headerData


@app.errorhandler(404)
def page_not_found(e):
    try:
        if len(request.path) < 16:
            capturedCharacterInput = request.path[1:].strip().replace(" ", "_")  #.lower()
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
