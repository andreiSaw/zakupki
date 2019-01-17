import os.path

from zakupkiClient.util import _dump_JSON_data, _checkDirectory_if_not_create
from .webutils import *


def search_save(stub, p_limit, offset=1):
    """
    Using webcrapping asks search engine to find query through pages_limit pages, and saves search pages
    :param offset: page number to start with
    :param p_limit: number of pages to save
    :param query: query to search
    :param session: session
    """
    page = offset
    path = stub.get_search_folder_path()
    while page <= p_limit:
        print('Loading page #%d' % (page))
        _checkDirectory_if_not_create(path)
        filepath = path + stub.get_page_filename()
        data = load_search_page(stub=stub, p=page)
        if contain_purchase_data(data):
            with open(filepath % page, 'w', encoding="UTF-8") as output_file:
                print('Saving page #%d' % page)
                output_file.write(data)
                page += 1
        else:
            break


def parse_save_search_entries(stub, p_limit, offset=1):
    """
    Parse all over search entries and then dump them
    :param stub:
    :return: purchase_list[] represents all purchases for that query
    """
    # TODO pagelimit
    purchase_list = []
    page = offset
    filepath = stub.get_search_folder_path() + stub.get_page_filename()
    print("Openning dir " + filepath)
    while page <= p_limit:
        filename = filepath % page
        if os.path.isfile(filename):
            res = parse_search_page(stub=stub, filepath=filename)
            purchase_list.extend(res)
            page += 1
        else:
            print("No file " + filename)
            break

    saving(data=purchase_list, stub=stub, filename=stub.get_purchase_db_name())
    return purchase_list


def create_save_lots(stub):
    # TODO: add
    """
    :param stub:
    :return:
    """
    purchases = load_JSON_data(stub=stub, filename=stub.get_purchase_db_name())
    lots = []
    for p in purchases:
        if p['lots_num'] > 0:
            lotslist = p['lots']
            for item in lotslist:
                if iscategory(item, stub.get_target()):
                    item["p_id"] = p['purchase_id']
                    item["buyer"] = p['Наименование организации']
                    # TODO: add clear text to name
                    lots.append(item)
    saving(data=lots, filename=stub.get_lots_db_name(), stub=stub)
    return lots


def get_vendors_save_lots(stub, lots):
    for item in lots:
        item["vendor"] = parse_protocols(stub=stub, p_id=item["p_id"])
        _dump_JSON_data(stub=stub, data=lots, filename=stub.get_lots_db_name())
    return lots
