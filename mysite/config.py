import os
import sass

from flask import Flask
from pathlib import Path

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    PROJECT_ROOT=Path(os.path.dirname(os.path.abspath(__file__))),
    IE="https://www.idleonefficiency.com",
    IT="https://idleontoolbox.com",
    TRELLO="https://trello.com/b/CG6GYsTN/idleon-autoreview-development",
    DISCORD="https://discord.gg/ZmEkqzfjmJ",
    GITHUB="https://github.com/TwoSpookyBoos/IdleOnAutoReviewBot",
    SPREADSHEET="https://docs.google.com/spreadsheets/d/16I-rURrVeyvltK2wxcQSiPgO07QY015RVNG4MAgUsGw/edit?usp=sharing",
    KOFI="https://ko-fi.com/W7W4SRUK5",
    LAVA="https://twitter.com/lavaflame2",
    FQDN="https://ieautoreview-scoli.pythonanywhere.com",

))
app.config.update(dict(
    FQDN_BETA=app.config['FQDN'].replace("://", "://beta-"),
    LOGS=app.config["PROJECT_ROOT"] / "logs",
    IT_DATA=f"{app.config['IT']}/data",
    IE_DATA=f"{app.config['IE']}/raw-data",
    IE_UPLOAD=f"{app.config['IE']}/profile/upload",
    IE_JSON_TEMPLATE="https://cdn2.idleonefficiency.com/profiles/{username}.json",
    IE_PROFILE_TEMPLATE="{username}.idleonefficiency.com"
))

if not Path(app.config["LOGS"]).exists():
    os.mkdir(app.config["LOGS"])

if not Path(app.config["LOGS"] / "browser_data.log").exists():
    open(app.config["LOGS"] / "browser_data.log", "w").close()

static_dir = app.config["PROJECT_ROOT"] / app.static_folder
css_files_dir = static_dir / "styles"
sass_files_dir = static_dir / "assets"

sass.compile(dirname=(sass_files_dir, css_files_dir))
