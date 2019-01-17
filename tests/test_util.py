import pytest

from zakupkiClient import *

AG_NAME = "Privet"


@pytest.fixture(scope="module")
def resource_setup(request):
    return Stub(query=AG_NAME, numFz="223", target="auto")


def test_preprocess_rus(resource_setup):
    stub = resource_setup
    test_str = ["В «Коммерсантъ» нужен СММ-специалист."]
    res = preprocess(data=test_str, stub=stub, flag="RU")
    ans = ["в коммерсантъ нужен сммспециалист"]
    assert res == ans


def test_preprocess_eng(resource_setup):
    stub = resource_setup
    test_str = ["to others today, Libra, and your communication will prove to be quite valuable. You"]
    res = preprocess(data=test_str, stub=stub, flag="EN")
    ans = ["to others today libra and your communication will prove to be quite valuable you"]
    assert res == ans


def test_iscategory(resource_setup):
    stub = resource_setup
    assert iscategory({"category": "auto"}, stub.get_target())
    assert not iscategory({"category": "29.10.2"}, stub.get_target())
