import os.path

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'Referer': 'http://www.kinopoisk.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}
AGENCY_NAME = "национальный+исследовательский+университет+высшая+школа+экономики"
SEARCH_FILEPATH = "./../data/%s/searchOutput/"
PURCHACE_FILEPATH = "./../data/%s/purchase/"
PAGES_LIMIT = 10
FILENAME = "page_%d.html"


def _getSession(headers=HEADERS):
    # establishing session
    s = requests.Session()
    s.headers.update(headers)
    return s


def _load_search_page(page, session, agency_name=AGENCY_NAME):
    url = 'http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?searchString=%s&pageNumber=%d&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz223=on&pc=on&currencyId=-1&regionDeleted=false&sortBy=UPDATE_DATE' % (
        agency_name, page)

    request = session.get(url)
    return request.text


def _contain_purchase_data(text):
    htmlsoup = BeautifulSoup(text, features="lxml")
    purchase_list = htmlsoup.find('div', {'class': "registerBox registerBoxBank margBtm20"})
    return purchase_list is not None


def find_and_save_search(pages_limit=PAGES_LIMIT, agency_name=AGENCY_NAME, path=SEARCH_FILEPATH,
                         s=_getSession()):
    page = 1
    while True:
        print('Loading page #%d' % (page))
        checkDirectory_if_not_create(path % agency_name)
        filepath = path + FILENAME
        data = _load_search_page(page, s, agency_name)
        if _contain_purchase_data(data):
            with open(filepath % (agency_name, page), 'w',
                      encoding="UTF-8") as output_file:
                print('Saving page #%d' % page)
                output_file.write(data)
                page += 1
                if page > pages_limit:
                    break
        else:
            break


def _read_file(filepath):
    with open(filepath) as input_file:
        text = input_file.read()
    return text


def _parse_page(filepath):
    results = []
    text = _read_file(filepath)

    soup = BeautifulSoup(text, features="lxml")
    purchase_list = soup.find('div', {'class': 'parametrs margBtm10'})
    items = purchase_list.find_all('div', {'class': ['registerBox registerBoxBank margBtm20']})
    for item in items:
        # getting movie_id
        purchase_link = item.find('td', {'class': 'descriptTenderTd'}).find('a').get('href')
        # purchase_desc = item.find('div', {'class': 'nameRus'}).find('a').text
        purchase_id = purchase_link[purchase_link.find("regNumber=") + len("regNumber="):]
        # purchase_price = item.find('td', {'class': 'tenderTd'}).find_all('strong')[1]

        # getting english name
        # name_eng = item.find('div', {'class': 'nameEng'}).text

        # getting watch time
        # watch_datetime = item.find('div', {'class': 'date'}).text
        # date_watched, time_watched = re.match('(\d{2}\.\d{2}\.\d{4}), (\d{2}:\d{2})', watch_datetime).groups()

        # getting user rating
        # user_rating = item.find('div', {'class': 'vote'}).text
        # if user_rating:
        #     user_rating = int(user_rating)

        results.append({
            'purchase_link': purchase_link,
            'purchase_desc': 0,
            'purchase_id': purchase_id,
            'purchase_price': 0
        })
    return results


def load_purchase_page(purchace_url, session=_getSession()):
    request = session.get(purchace_url)
    return request.text


def save_purchace_pages(purchase_id, path=PURCHACE_FILEPATH, agency_name=AGENCY_NAME):
    print('Loading page #%d' % (purchase_id))
    data = load_purchase_page(purchase_id)
    checkDirectory_if_not_create(path)
    filepath = path + FILENAME
    with open(filepath % (agency_name, purchase_id), 'w', encoding="UTF-8") as output_file:
        print('Saving page #%d' % (purchase_id))
        output_file.write(data)


def parse_search_output(agency_name=AGENCY_NAME):
    purchase_list = []
    page = 1
    filepath = SEARCH_FILEPATH + FILENAME
    while True:
        filename = filepath % (agency_name, page)
        if os.path.isfile(filename):
            res = _parse_page(filename)
            purchase_list.extend(res)
            page += 1
        else:
            break
    return purchase_list


def checkDirectory_if_not_create(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
