import pytest
from bs4 import BeautifulSoup
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
        t = clear_text_from_xml(s1.text)
        if t != "L AsstrA 115.138.470 ШВЕЙЦАРИЯ 756":
            pytest.fail("wrong answer")
    pass


def test_get_id_from_url():
    url1 = "http://zakupki.gov.ru/223/purchase/public/purchase/info/protocols.html?regNumber=31704861041"
    test_id = get_id_from_url(url1)
    if test_id != "31704861041":
        pytest.fail("wrong answer")
    pass
