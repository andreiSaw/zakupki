from .parserinterface import ParserInterface
from .util import _dump_JSON_data, _checkDirectory_if_not_create
from .webutils import *


class Parser223(ParserInterface):
    def __init__(self, stub):
        self.__stub = stub

    def search_save(self, p_limit, offset=1):
        page = offset
        path = self.get_stub().get_search_folder_path()
        while page <= p_limit:
            print('Loading page #%d' % (page))
            _checkDirectory_if_not_create(path)
            filepath = path + self.get_stub().get_page_filename()
            data = load_search_page(stub=self.get_stub(), p=page)
            if contain_purchase_data(data):
                with open(filepath % page, 'w', encoding="UTF-8") as output_file:
                    print('Saving page #%d' % page)
                    output_file.write(data)
                    page += 1
            else:
                break

    def parse_save_search_entries(self, p_limit, offset=1):
        purchase_list = []
        page = offset
        filepath = self.get_stub().get_search_folder_path() + self.get_stub().get_page_filename()
        print("Openning dir " + filepath)
        while page <= p_limit:
            filename = filepath % page
            if os.path.isfile(filename):
                res = parse_search_page(stub=self.get_stub(), filepath=filename)
                purchase_list.extend(res)
                page += 1
            else:
                print("No file " + filename)
                break

        saving(data=purchase_list, stub=self.get_stub(), filename=self.get_stub().get_purchase_db_name())
        return purchase_list

    def create_save_lots(self):
        purchases = load_JSON_data(stub=self.get_stub(), filename=self.get_stub().get_purchase_db_name())
        lots = []
        for p in purchases:
            if p['lots_num'] > 0:
                lotslist = p['lots']
                for item in lotslist:
                    item["p_id"] = p['purchase_id']
                    item["buyer"] = p['Наименование организации']
                    item["type"]=p["Способ размещения закупки"]
                    # TODO: add clear text to name
                    lots.append(item)
        saving(data=lots, filename=self.get_stub().get_lots_db_name(), stub=self.get_stub())
        return lots

    def get_vendors_save_lots(self, lots):
        for item in lots:
            item["vendor"] = parse_protocols(stub=self.get_stub(), p_id=item["p_id"])
            _dump_JSON_data(stub=self.get_stub(), data=lots, filename=self.get_stub().get_lots_db_name())
        return lots

    def get_stub(self):
        return self.__stub
