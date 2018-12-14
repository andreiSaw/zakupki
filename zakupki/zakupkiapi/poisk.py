import os.path

from zakupki.zakupkiapi.util import _checkDirectory_if_not_create, _contain_purchase_data, _parse_search_page
from .util import *


def search_save(s, query, p_limit):
    """
    Using webcrapping asks search engine to find query through pages_limit pages, and saves search pages
    :param p_limit: number of pages to save
    :param query: query to search
    :param s: session
    """
    page = 1
    path = get_search_folder_path(query)
    while page <= p_limit:
        print('Loading page #%d' % (page))
        _checkDirectory_if_not_create(path)
        filepath = path + FILENAME
        data = load_search_page(p=page, s=s, q=query)
        if _contain_purchase_data(data):
            with open(filepath % page, 'w', encoding="UTF-8") as output_file:
                print('Saving page #%d' % page)
                output_file.write(data)
                page += 1
        else:
            break


def parse_save_search_entries(session, query):
    """
    Parse all over search entries and then dump them
    :param query: agency name
    :return: purchase_list[] represents all purchases for that query
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
    dump_JSON_data(data=purchase_list, q=query)
    return purchase_list


def create_save_lots(query):
    """

    :param query:
    :return:
    """
    purchases = load_JSON_data(q=query)
    lots = []
    for p in purchases:
        if p['lots_num'] > 0:
            d = p['lots']
            for item in d:
                item["p_id"] = p['purchase_id']
            lots.extend(d)
    dump_JSON_data(data=lots, filename=LOTS_DB_NAME, q=query)
    return lots
