import json
from pathlib import Path

import pytest
import yaml

from models.custom_exceptions import UserDataException, UsernameBanned


def test_valid_input_get(client):
    response = client.get("/", query_string=dict(player="scoli"))
    assert response.status_code == 200


testing_data = [
    str(file) for file in Path("tests/testing-data").iterdir() if file.is_file()
]


@pytest.mark.parametrize("datafile", testing_data)
def test_json(client, conf, datafile):
    data = json.load(open(datafile))
    response = client.post("/", data=data, headers=conf.headers)
    assert response.status_code == 200


def test_username_too_long_post(client):
    data = dict(player="username_too_long", follow_redirects=True)
    response = client.post("/", data=data)
    assert UserDataException.msg_base in response.text


def test_username_banned_post(client, conf):
    bannedAccountsList = yaml.load(
        open(Path(conf.static_folder) / "banned.yaml"), yaml.Loader
    )
    data = dict(player=bannedAccountsList[0])
    response = client.post("/", data=data, follow_redirects=True)
    assert UsernameBanned.msg_base in response.text


def test_username_too_long_get(client):
    data = dict(player="username_too_long")
    response = client.get("/", query_string=data)
    assert UserDataException.msg_base in response.text


def test_username_banned_get(client, conf):
    bannedAccountsList = yaml.load(
        open(Path(conf.static_folder) / "banned.yaml"), yaml.Loader
    )
    data = dict(player=bannedAccountsList[0])
    response = client.get("/", query_string=data)
    assert UsernameBanned.msg_base in response.text
