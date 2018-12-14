import json
import os
import re
from string import punctuation

import requests
from bs4 import BeautifulSoup

_HEADERS = {
    'Referer': 'http://www.kinopoisk.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}
QUERY = "default"
_SEARCH_FOLDER = "search/"
PAGES_LIMIT = 10
FILENAME = "page_%s.html"
_STOPLISTNAME = "stopwords.json"
_DATA_FOLDER = "./../data/%s/"
_PURCHACE_INFO = "http://zakupki.gov.ru/223/purchase/public/purchase/info/%s.html?regNumber=%s"
_TAB = "common-info"
_DB_NAME = "test.json"
LEN_LOT_LIST = 6
LOTS_DB_NAME = "lots.json"


def _get_session(headers=_HEADERS):
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
    filepath = _STOPLISTNAME
    if not os.path.isfile(filepath):
        return []
    with open(filepath, "r") as json_data:
        statelist = json.load(json_data)
        if isinstance(statelist, list):
            return statelist
        return []


def load_JSON_data(filename=_DB_NAME, q=QUERY):
    filepath = get_filename(q=q, filename=filename)
    if not os.path.isfile(filepath):
        return []
    with open(filepath, "r") as json_data:
        statelist = json.load(json_data)
        if isinstance(statelist, list):
            return statelist
        return []


def dump_JSON_data(statelist, filename=_DB_NAME, q=QUERY):
    filepath = get_filename(q=q, filename=filename)
    with open(filepath, "w", encoding="UTF-8") as f:
        json.dump(statelist, f)


def _contain_purchase_data(text):
    htmlsoup = BeautifulSoup(text, features="lxml")
    purchase_list = htmlsoup.find('div', {'class': "registerBox registerBoxBank margBtm20"})
    return purchase_list is not None


def load_search_page(p, s, q=QUERY):
    """

    :param p: page number
    :param s: session
    :param q: query
    :return: text
    """
    url = 'http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?searchString=%s&pageNumber=%d&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz223=on&pc=on&currencyId=-1&regionDeleted=false&sortBy=UPDATE_DATE' % (
        q, p)
    return load_page(url, s)


def load_page(p_link, session):
    request = session.get(p_link)
    return request.text


def get_filename(filename, q=QUERY):
    return (_DATA_FOLDER % q) + filename


def get_search_folder_path(q=QUERY):
    return (_DATA_FOLDER % q) + _SEARCH_FOLDER


def get_stoplist_path(q=QUERY):
    return (_DATA_FOLDER % q) + _STOPLISTNAME


def get_purchase_tab(p_id, tab=_TAB):
    return _PURCHACE_INFO % (tab, p_id)


def isauto(lot):
    if '29.10.2' in lot['category']:
        return True
    return False


def clear_text(content):
    return content.replace("\n", "").replace("\t", "").replace("\r", "")


def clear_price(content):
    """
    Removes words from price cell and kopeiki as well
    :param content:
    :return:
    """
    numbers = re.findall('\d+', content)
    return "".join(numbers[:-1])


def get_id_from_url(content):
    return content[content.find("regNumber=") + len("regNumber="):]


def clear_purchace_row(content, element):
    element[re.sub(' +', ' ', content[0])] = re.sub(' +', ' ', content[1])


def _parse_search_page(filepath, session):
    """
    Parsing one single page to retrieve all data (purchase url, id, etc.)
    :param filepath:  saved page path
    :param session:
    :return: results[] represents all search entries from that page
    """
    results = []
    text = _read_file(filepath)

    soup = BeautifulSoup(text, features="lxml")
    purchase_list = soup.find('div', {'class': 'parametrs margBtm10'})
    items = purchase_list.find_all('div', {'class': ['registerBox registerBoxBank margBtm20']})
    for item in items:
        p_link = item.find('td', {'class': 'descriptTenderTd'}).find('a').get('href')
        p_id = get_id_from_url(p_link)

        # TODO parse purchase online
        temp_item = {
            'purchase_link': p_link,
            'purchase_id': p_id
        }
        ppp = parse_purchase_page(p_id, session)
        temp_item.update(ppp)
        results.append(temp_item)
        print("Parsed %s page" % p_id)
    return results


def parse_purchase_page(p_id, session):
    """
    Walk through purchase page and take first 3 divs then asks to get lots
    :param p_link: puchase link
    :param session:
    :return: dict element represents purchase
    """
    p_link = get_purchase_tab(p_id)
    page = load_page(p_link, session)
    soup = BeautifulSoup(page, features="lxml")
    divs = soup.find('div', {'class': "contentTabBoxBlock"}).find_all('div', {'class': "noticeTabBoxWrapper"})
    element = {}
    i = 0
    for div in divs:
        trs = div.find_all('tr')
        for tr in trs:
            row = [clear_text(el.text) for el in tr.find_all(['td', 'th']) if el.text]
            if len(row) > 1:
                clear_purchace_row(row, element)
        i += 1
        if i > 2:
            break
    element.update(parse_lots(p_id, session))
    return element


def parse_lots(p_id, session):
    """
    Walk through purchase page and parse lots tab
    :param p_id: purchase id
    :param session:
    :return: dict {lots[],lots_num}
    """
    p_link = get_purchase_tab(p_id, tab="lot-list")
    page = load_page(p_link, session)
    soup = BeautifulSoup(page, features="lxml")
    trs = soup.find('table', {'id': 'lot'}).find('tbody').find_all('tr')
    lots_num = 0
    lots = []
    for row in trs:
        cells = [el for el in row.find_all(['td', 'th']) if el.text]
        if len(cells) == LEN_LOT_LIST:
            tmp = clear_text(cells[1].find('a', {'class': "dLink epz_aware"}).text)
            lots_num += 1
            lot = {"name": tmp,
                   "category": clear_text(cells[5].text),
                   "price": clear_price(clear_text(cells[3].text))}
            lots.append(lot)
    return {"lots": lots, 'lots_num': lots_num}


def preprocess(q, lst):
    if lst is None:
        lst = load_JSON_data(q)
    # lowers all
    text_lower = [text.lower() for text in lst]
    # delete punctuation
    text_letters = [''.join(c for c in s if c not in punctuation) for s in text_lower]
    return text_letters


def preprocess_eng(q=QUERY, lst=None):
    text_letters = preprocess(q, lst)
    # delete all besides letters
    text_final = [re.sub(r'[^A-Za-z]+', ' ', x) for x in text_letters]
    return text_final


def preprocess_rus(q=QUERY, lst=None):
    text_letters = preprocess(q, lst)
    # delete all besides letters
    text_final = [re.sub(r'[^А-Яа-я]+', ' ', x) for x in text_letters]
    return text_final
