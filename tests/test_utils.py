import os
import shutil

import pytest

from zakupkiClient import *
from zakupkiClient.util import set_proxies

def test_proxy():
    assert os.environ['PROXY_ZAKUPKI_HTTPS']
    assert os.environ['PROXY_ZAKUPKI_HTTP']
    assert set_proxies() == {'http': os.environ['PROXY_ZAKUPKI_HTTP'], 'https': os.environ['PROXY_ZAKUPKI_HTTPS']}