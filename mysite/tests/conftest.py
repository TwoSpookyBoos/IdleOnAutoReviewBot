import pytest
from flask_app import app


@pytest.fixture()
def app_():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app_):
    return app_.test_client()


@pytest.fixture()
def runner(app_):
    return app_.test_cli_runner()
