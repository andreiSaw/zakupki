import os
import shutil

import pytest
import datetime
import json

from zakupkiClient.util import set_proxies, default_json_datetime
from zakupkiClient.textutils import parse_datetime


def teardown_module(module):
    print(f"\nmodule {module.__name__} teardown")
    os.unlink("zero.json")


def teardown_function(function):
    print(f"\nfunction {function.__name__} teardown")


def test_proxy():
    assert os.environ['PROXY_ZAKUPKI_HTTPS']
    assert os.environ['PROXY_ZAKUPKI_HTTP']
    assert set_proxies() == {'http': os.environ['PROXY_ZAKUPKI_HTTP'], 'https': os.environ['PROXY_ZAKUPKI_HTTPS']}


def test_default_json_datetime():
    our_val = "2019-05-06T12:48:15"

    with open("zero.json", "w", encoding="UTF-8") as f:
        json.dump(
            parse_datetime(our_val),
            default=default_json_datetime,
            fp=f
        )
    with open('zero.json', "r") as json_data:
        data = json.load(json_data)
    assert data == our_val
