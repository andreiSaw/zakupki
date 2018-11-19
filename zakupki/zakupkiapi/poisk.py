import requests
from bs4 import BeautifulSoup

# establishing session
s = requests.Session()
s.headers.update({
    'Referer': 'http://www.kinopoisk.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
})
AGENCY_NAME = "национальный+исследовательский+университет+высшая+школа+экономики"


def load_search_page(agency_name, page, session):
    url = 'http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?searchString=%s&pageNumber=%d&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz223=on&pc=on&currencyId=-1&regionDeleted=false&sortBy=UPDATE_DATE' % (

        agency_name, page)
    # print url
    request = session.get(url)
    return request.text


def contain_purchase_data(text):
    htmlsoup = BeautifulSoup(text, features="lxml")
    purchase_list = htmlsoup.find('div', {'class': "registerBox registerBoxBank margBtm20"})
    return purchase_list is not None


def save_pages():
    page = 1
    while True:
        print('Loading page #%d' % (page))
        data = load_search_page(AGENCY_NAME, page, s)
        if contain_purchase_data(data):
            with open('../user_data/page_%d.html' % (page), 'w', encoding="UTF-8") as output_file:
                print('Saving page #%d' % (page))
                output_file.write(data)
                page += 1
        else:
            break


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


def parse_page(filename):
    results = []
    text = read_file(filename)

    soup = BeautifulSoup(text, features="lxml")
    purchase_list = soup.find('div', {'class': 'parametrs margBtm10'})
    items = purchase_list.find_all('div', {'class': ['registerBox registerBoxBank margBtm20']})
    for item in items:
        # getting movie_id
        purchase_link = item.find('td', {'class': 'descriptTenderTd'}).find('a').get('href')
        # purchase_desc = item.find('div', {'class': 'nameRus'}).find('a').text
        purchase_id = item.find('td', {'class': 'descriptTenderTd'}).find('a').text
        purchase_price = item.find('td', {'class': 'tenderTd'}).find_all('strong')[1]

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
            'purchase_price': purchase_price,
            'user_rating': 0,
            'movie_desc': 0
        })
    return results
