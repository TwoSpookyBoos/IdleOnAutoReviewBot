import os
import sass

from flask import Flask
from pathlib import Path

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["PROJECT_ROOT"] = Path(os.path.dirname(os.path.abspath(__file__)))
app.config["LOGS"] = app.config["PROJECT_ROOT"] / "logs"

static_dir = app.config["PROJECT_ROOT"] / app.static_folder
css_files_dir = static_dir / "styles"
sass_files_dir = static_dir / "assets"

sass.compile(dirname=(sass_files_dir, css_files_dir))
