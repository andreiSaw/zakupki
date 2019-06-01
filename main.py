import sqlalchemy as db

from zakupkiClient import load_parse_purchase_page, Stub, saving, Parser, textutils
from zakupkiClient.webutils import parse_search_page


def start():
    ag_name = "закупка автомобилей"
    purchase_db_name = "db_1.json"
    lots_db_name = "lots_1.json"
    numFz = "223"
    PAGE_OFFSET = 1
    PAGE_LIMIT = 1
    stub = Stub(
        query=ag_name,
        numFz=numFz,
        lots_db_name=lots_db_name,
        purchase_db_name=purchase_db_name,
        proxy=False)
    parser = Parser(stub)

    parser.search_save(page_offset=PAGE_OFFSET, page_limit=PAGE_LIMIT)
    parser.parse_save_search_entries(PAGE_LIMIT, PAGE_OFFSET)


if __name__ == "__main__":
    import logging

    logging.basicConfig(filename='output.log',
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        )
    start()

    print("main")
