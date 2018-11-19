from zakupki.zakupkiapi.poisk import *
import json
if __name__ == '__main__':
    # find_and_save_search()
    lst = parse_search_output()
    # json.dumps(lst)
    for item in lst:
        save_purchace_pages(item['purchase_id'])