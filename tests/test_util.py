from zakupki.zakupkiapi.util import *
# import pytest

def test_preprocess_rus():
    test_str = ["В «Коммерсантъ» нужен СММ-специалист."]
    res = preprocess_rus(lst=test_str)
    ans = ["в коммерсантъ нужен сммспециалист"]
    assert res == ans

def test_preprocess_eng():
    test_str = ["to others today, Libra, and your communication will prove to be quite valuable. You"]
    res = preprocess_eng(lst=test_str)
    ans = ["to others today libra and your communication will prove to be quite valuable you"]
    assert res == ans