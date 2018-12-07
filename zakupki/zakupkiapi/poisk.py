import os.path
import re

from zakupki.zakupkiapi.util import _read_file, _checkDirectory_if_not_create, _contain_purchase_data
from .util import *


def search_save(s, p_limit=PAGES_LIMIT, query=QUERY):
    """
    Using webcrapping asks search engine to find query through pages_limit pages, and saves search pages
    :param p_limit:
    :param query:
    :param path:
    :param s:
    """
    page = 1
    path = get_search_folder_path(query)
    while True:
        print('Loading page #%d' % (page))
        _checkDirectory_if_not_create(path)
        filepath = path + FILENAME
        data = load_search_page(page, s, query)
        if _contain_purchase_data(data):
            with open(filepath % page, 'w',
                      encoding="UTF-8") as output_file:
                print('Saving page #%d' % page)
                output_file.write(data)
                page += 1
                if page > p_limit:
                    break
        else:
            break


def parse_lots(p_id, session):
    p_link=get_purchase_tab(p_id, tab="lot-list")
    page = load_page(p_link, session)
    soup = BeautifulSoup(page, features="lxml")
    trs = soup.find('table', {'id': 'lot'}).find('tbody').find_all('tr')
    lots_num = 0
    lots=[]
    for row in trs:
        cells = [el.text.replace("\n", "").replace("\t", "").replace("\r", "") for el in row.find_all(['td', 'th']) if
               el.text]
        if len(cells) == 6:
            lots_num += 1
            lot = {"name": cells[1], "category": cells[5], "price": cells[3]}
            lots.append(lot)
    return {"lots": lots, 'lots_num': lots_num}


def parse_purchase_page(p_id, session):
    """
    Walk through purchase page and take first 3 divs then asks to get lots
    :param p_link:
    :param session:
    :return:
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
            row = [el.text.replace("\n", "").replace("\t", "").replace("\r", "") for el in tr.find_all(['td', 'th']) if
                   el.text]
            if len(row) > 1:
                element[re.sub(' +', ' ', row[0])] = re.sub(' +', ' ', row[1])
        i += 1
        if i > 2:
            break
    element.update(parse_lots(p_id, session))
    return element


def _parse_search_page(filepath, session):
    results = []
    text = _read_file(filepath)

    soup = BeautifulSoup(text, features="lxml")
    purchase_list = soup.find('div', {'class': 'parametrs margBtm10'})
    items = purchase_list.find_all('div', {'class': ['registerBox registerBoxBank margBtm20']})
    for item in items:
        p_link = item.find('td', {'class': 'descriptTenderTd'}).find('a').get('href')
        p_id = p_link[p_link.find("regNumber=") + len("regNumber="):]

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


def parse_search_entries(session, query=QUERY):
    """
    Parse all over search entries
    :param query: agency name
    :return:
    """
    # TODO pagelimit
    purchase_list = []
    page = 1
    filepath = get_search_folder_path(query) + FILENAME
    while True:
        filename = filepath % page
        if os.path.isfile(filename):
            res = _parse_search_page(filename, session)
            purchase_list.extend(res)
            page += 1
        else:
            break
    dump_JSON_data(purchase_list, query=query)
    return purchase_list

