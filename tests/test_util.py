from zakupki.zakupkiapi.util import *


# import pytest


def test_preprocess_rus():
    test_str = ["В «Коммерсантъ» нужен СММ-специалист."]
    res = preprocess(data=test_str, q="df", flag="RU")
    ans = ["в коммерсантъ нужен сммспециалист"]
    assert res == ans


def test_preprocess_eng():
    test_str = ["to others today, Libra, and your communication will prove to be quite valuable. You"]
    res = preprocess(data=test_str, q="df", flag="EN")
    ans = ["to others today libra and your communication will prove to be quite valuable you"]
    assert res == ans


def test_isauto():
    assert isauto({"category": "29.10.2"})
    assert not isauto({"category": "Бензин"})
