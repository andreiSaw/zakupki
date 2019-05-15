from zakupkiClient import *


def test():
    ag_name = "вшэ"
    purchase_db_name = "db_1.json"
    lots_db_name = "lots_1.json"
    numFz = "223"
    stub = Stub(
        query=ag_name,
        numFz=numFz,
        lots_db_name=lots_db_name,
        purchase_db_name=purchase_db_name,
        proxy=False)

    parser = Parser(stub)
    parser.search_save(page_offset=1, page_limit=1)
    parser.parse_save_search_entries(page_offset=1, page_limit=1)
    purchases_json = load_JSON_data(stub=stub, filename=stub.get_purchase_db_name())
    parser.create_save_lots()


if __name__ == "__main__":
    print("main")
