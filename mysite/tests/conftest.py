import pytest
from flask_app import app
from collections import namedtuple


@pytest.fixture()
def app_():
    app.config.update(dict(TESTING=True))

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app_):
    return app_.test_client()


@pytest.fixture()
def runner(app_):
    return app_.test_cli_runner()


@pytest.fixture()
def conf(app_):
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    Conf = namedtuple("Conf", ["headers", "static_folder"])
    return Conf(headers, app_.static_folder)
