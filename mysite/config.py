import os

from flask import Flask
from pathlib import Path

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["PROJECT_ROOT"] = Path(os.path.dirname(os.path.abspath(__file__)))
app.config["LOGS"] = app.config["PROJECT_ROOT"] / "logs"
