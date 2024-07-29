import json
from pathlib import Path

import pytest
import yaml

from models.custom_exceptions import UserDataException, UsernameBanned


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_valid_input_post(client, conf):
    response = client.post(
        "/results",
        data=json.dumps(dict(player="nikokoni")),
        headers=conf.headers
    )
    assert response.status_code == 200


testing_data = [
    str(file) for file in Path("tests/testing-data").iterdir() if file.is_file()
]


@pytest.mark.parametrize("datafile", testing_data)
def test_json(client, conf, datafile):
    with open(datafile, "r") as f:
        data = json.load(f)

    response = client.post("/results", data=json.dumps(data), headers=conf.headers)
    assert response.status_code == 200


def test_username_too_long_post(client):
    data = dict(player="username_too_long", follow_redirects=True)
    response = client.post("/results", data=json.dumps(data))
    assert UserDataException.msg_base in response.text


def test_username_banned_post(client, conf):
    with open(Path(conf.static_folder) / "banned.yaml") as f:
        bannedAccountsList = yaml.load(f, yaml.Loader)

    data = dict(player=bannedAccountsList[0])
    response = client.post("/results", data=json.dumps(data), follow_redirects=True)
    assert UsernameBanned.msg_base in response.text
