import json
import random
import re
import string
from pathlib import Path

import pytest
import yaml
from markupsafe import Markup, escape

from models.advice.advice import _escape_text
from models.custom_exceptions import UserDataException, UsernameBanned

def execute_test_checks(response: bytes | str):
    if re.findall(r"\.\d{7,}", str(response)):
        raise Exception("Found floating point precision error.")

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_valid_input_post(client, conf):
    response = client.post(
        "/results",
        data=json.dumps(dict(player="callmehein")),
        headers=conf.headers
    )
    assert response.status_code == 200


passing_test_data = [
    str(file) for file in Path("tests/testing-data/passing").iterdir() if file.is_file()
]

failing_test_data = [
    str(file) for file in Path("tests/testing-data/failing").iterdir() if file.is_file()
]

@pytest.mark.parametrize("datafile", passing_test_data)
def test_valid_json(client, conf, datafile):
    with open(datafile, "r") as f:
        data = json.load(f)

    response = client.post("/results", data=json.dumps({'player': json.dumps(data)}), headers=conf.headers)
    execute_test_checks(response.data)
    assert response.status_code == 200 and len(response.data) > 0

@pytest.mark.parametrize("datafile", failing_test_data)
def test_invalid_json(client, conf, datafile):
    with open(datafile, "r") as f:
        data = json.load(f)

    response = client.post("/results", data=json.dumps({'player': json.dumps(data)}), headers=conf.headers)
    execute_test_checks(response.data)
    assert response.status_code != 200 and response.status_code < 500


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

@pytest.mark.parametrize("datafile", passing_test_data)
def test_output_consistency(client, conf, datafile):
    all_responses = []
    for _ in range(3):
        with open(datafile, "r") as f:
            data = json.load(f)

        response = client.post("/results", data=json.dumps({'player': json.dumps(data)}), headers=conf.headers)
        execute_test_checks(response.data)
        assert response.status_code == 200 and len(response.data) > 0
        all_responses.append(response.get_data(as_text=True))
    assert len(set(all_responses)) == 1


def test_escape_text_matches_markupsafe():
    cases = ["", "plain text", "<script>", "a & b", 'say "hi"', "it's", "<>&\"'", "café", 5, 1.5, None]
    for case in cases:
        assert _escape_text(case) == escape(case)


def test_escape_text_matches_markupsafe_fuzzed():
    alphabet = string.printable + "<>&\"'"
    rand = random.Random(0)
    for _ in range(2000):
        text = "".join(rand.choice(alphabet) for _ in range(rand.randrange(12)))
        assert _escape_text(text) == escape(text)


def test_escape_text_passes_markup_through():
    markup = Markup("<b>bold</b>")
    assert _escape_text(markup) == markup == escape(markup)
