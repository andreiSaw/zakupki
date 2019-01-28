import logging
import os
import re

from bs4 import BeautifulSoup

from zakupkiClient.parserinterface import ParserInterface
from zakupkiClient.util import _checkDirectory_if_not_create, saving, load_JSON_data
from zakupkiClient.webutils import parse_search_page, load_search_page, contain_purchase_data


class ParserV(ParserInterface):
    def __init__(self, stub):
        self.__stub = stub

    def allRecords(self):
        page = load_search_page(stub=self.get_stub(), p=1)
        soup = BeautifulSoup(page, features="lxml")
        if soup.find("p", {"class": "noRecords"}):
            logging.ERROR("No ans")
            return 0
        a = soup.find("p", {"class": "allRecords"}).text
        ans = int(re.sub(r'[^0-9]+', ' ', a))
        logging.info(f'allRecords = {ans}')
        return ans

    def search_save(self, p_limit, offset=1):
        page = offset
        path = self.get_stub().get_search_folder_path()
        while page <= p_limit:
            logging.info('Loading page #%d' % (page))
            _checkDirectory_if_not_create(path)
            filepath = path + self.get_stub().get_page_filename()
            data = load_search_page(stub=self.get_stub(), p=page)
            if contain_purchase_data(data):
                with open(filepath % page, 'w', encoding="UTF-8") as output_file:
                    logging.info('Saving page #%d' % page)
                    output_file.write(data)
                    page += 1
            else:
                break

    def parse_save_search_entries(self, p_limit, offset=1):
        purchase_list = []
        page = offset
        filepath = self.get_stub().get_search_folder_path() + self.get_stub().get_page_filename()
        logging.info("Openning dir " + filepath)
        while page <= p_limit:
            filename = filepath % page
            if os.path.isfile(filename):
                res = parse_search_page(stub=self.get_stub(), filepath=filename)
                purchase_list.extend(res)
                page += 1
            else:
                logging.ERROR("No file " + filename)
                break

        saving(data=purchase_list, stub=self.get_stub(), filename=self.get_stub().get_purchase_db_name())

    def create_save_lots(self):
        purchases = load_JSON_data(stub=self.get_stub(), filename=self.get_stub().get_purchase_db_name())
        res_lots = []
        for p in purchases:
            if p['lots_num'] > 0:
                lotslist = p['lots']
                for lot in lotslist:
                    lot["p_id"] = p['purchase_id']
                    logging.info(lot["p_id"])
                    lot["buyer_name"] = p['fullName']
                    lot["buyer_inn"] = p['inn']
                    if lot["supplier"]:
                        lot["status"]="OK"
                        lot["supplier_name"] = lot["supplier"]["name"]
                        lot["supplier_inn"] = lot["supplier"]["inn"]
                        lot["price_sold"]=lot["supplier"]["price"]
                        lot.pop("supplier")
                    else:
                        lot["status"]="NA"
                    # TODO: add clear text to name
                    res_lots.append(lot)
        saving(data=res_lots, filename=self.get_stub().get_lots_db_name(), stub=self.get_stub())

    def get_stub(self):
        return self.__stub
