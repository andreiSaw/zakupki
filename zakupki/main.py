from zakupki.zakupkiapi.poisk import *
import docx
from zakupki.zakupkiapi.util import _get_session

if __name__ == '__main__':

    # dump_JSON_data(parse_purchases(query=ag_name), filename="pchs.json", query=ag_name)
    wordDoc = docx.Document('../data/demo.docx')
    for table in wordDoc.tables:
        for row in table.rows:
            for cell in row.cells:
                print(cell.text)
    page = parse_purchase_page(get_purchase_tab(p_id="31807061497"), ses)
    print(isauto(p_id="31807166861", session=ses))
    print(page)
    # dump_JSON_data([page], "tp.json", ag_name)
    create_save_lots(ag_name)