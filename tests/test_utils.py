import os
import pytest

from zakupkiClient.util import set_proxies


def teardown_function(function):
    print(f"\nfunction {function.__name__} teardown")


def test_proxy():
    assert os.environ['PROXY_ZAKUPKI_HTTPS']
    assert os.environ['PROXY_ZAKUPKI_HTTP']
    assert set_proxies() == {'http': os.environ['PROXY_ZAKUPKI_HTTP'], 'https': os.environ['PROXY_ZAKUPKI_HTTPS']}
