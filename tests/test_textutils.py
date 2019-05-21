import pytest
from bs4 import BeautifulSoup
import datetime
from zakupkiClient import *

DATA_PATH = "./data/"


def test_create_query():
    q = "тамбовская область"
    r = create_query(q)
    if r != "тамбовская+область":
        pytest.fail("wrong answer")
    pass


def test_clear_text():
    filename = "31704861041-02"
    page = read_file(f'{DATA_PATH}{filename}.xml')
    soup = BeautifulSoup(page, "xml")
    s1 = soup.find("nonResidentInfo")
    if s1:
        t = clear_text(s1.text)
        # print(t)
        if t != "L AsstrA 115.138.470 ШВЕЙЦАРИЯ 756":
            pytest.fail("wrong answer")
    pass


def test_get_id_from_url():
    url1 = "http://zakupki.gov.ru/223/purchase/public/purchase/info/protocols.html?regNumber=31704861041"
    id = get_id_from_url(url1)
    if id != "31704861041":
        pytest.fail("wrong answer")
    pass


def test_parse_datetime():
    timestr = "2019-05-06T12:48:15"
    ans = parse_datetime(timestr)
    anticipated_ans = datetime.datetime(2019, 5, 6, 12, 48, 15)
    if ans != anticipated_ans:
        pytest.fail("wrong answer")
    pass
