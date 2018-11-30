import json
import os

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'Referer': 'http://www.kinopoisk.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}
QUERY = "default"
SEARCH_FILEPATH = "./../data/%s/search/"
PURCHACE_FILEPATH = "./../data/%s/purchase/"
PAGES_LIMIT = 10
FILENAME = "page_%s.html"
DBNAME = "db.json"
STOPLISTNAME = "./../data/stopwords.json"
DATADIR = "./../data/%s/"


def _get_session(headers=HEADERS):
    """
    establishing session
    :param headers:
    :return:
    """
    s = requests.Session()
    s.headers.update(headers)
    return s


def _read_file(filepath):
    with open(filepath) as input_file:
        text = input_file.read()
    return text


def _checkDirectory_if_not_create(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def getStopList():
    filepath = STOPLISTNAME
    if not os.path.isfile(filepath):
        return []
    with open(filepath, "r") as json_data:
        statelist = json.load(json_data)
        if isinstance(statelist, list):
            return statelist
        return []


def load_JSON_data(filename=DBNAME, query=QUERY):
    filepath = (DATADIR + filename) % query
    if not os.path.isfile(filepath):
        return []
    with open(filepath, "r") as json_data:
        statelist = json.load(json_data)
        if isinstance(statelist, list):
            return statelist
        return []


def dump_JSON_data(statelist, filename=DBNAME, query=QUERY):
    filepath = (DATADIR + filename) % query
    with open(filepath, "w", encoding="UTF-8") as f:
        json.dump(statelist, f)


def _contain_purchase_data(text):
    htmlsoup = BeautifulSoup(text, features="lxml")
    purchase_list = htmlsoup.find('div', {'class': "registerBox registerBoxBank margBtm20"})
    return purchase_list is not None


def load_search_page(page, session, query=QUERY):
    url = 'http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?searchString=%s&pageNumber=%d&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz223=on&pc=on&currencyId=-1&regionDeleted=false&sortBy=UPDATE_DATE' % (
        query, page)
    return load_page(url, session)


def load_page(p_link, session):
    request = session.get(p_link)
    return request.text
