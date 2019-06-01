import logging
import os
import re

from bs4 import BeautifulSoup

from zakupkiClient.parserinterface import ParserInterface
from zakupkiClient.util import _check_directory_create
from zakupkiClient.webutils import parse_search_page, load_search_page, contain_purchase_data


class Parser(ParserInterface):
    def __init__(self, stub):
        self.__stub = stub

    def allRecords(self):
        page = load_search_page(stub=self.get_stub(), p=1)
        soup = BeautifulSoup(page, features="lxml")
        if soup.find("p", {"class": "noRecords"}):
            logging.ERROR("No ans")
            return 0
        a = soup.find("p", {"class": "allRecords"}).text
        ans = int(re.sub(r'[^0-9]', "", a))
        logging.info(f'allRecords = {ans}')
        return ans

    def search_save(self, page_limit, page_offset=1):
        page = page_offset
        path = self.get_stub().get_search_folder_path()
        while page <= page_limit:
            logging.info('Loading page #%d' % (page))
            _check_directory_create(path)
            filepath = path + self.get_stub().get_page_filename()
            data = load_search_page(stub=self.get_stub(), p=page)
            if contain_purchase_data(data):
                with open(filepath % page, 'w', encoding="UTF-8") as output_file:
                    logging.info('Saving page #%d' % page)
                    output_file.write(data)
                    page += 1
            else:
                break

    def parse_save_search_entries(self, page_limit, page_offset=1):
        page_n = page_offset
        filepath = self.get_stub().get_search_folder_path() + self.get_stub().get_page_filename()
        logging.info("Openning dir " + filepath)
        while page_n <= page_limit:
            filename = filepath % page_n
            if os.path.isfile(filename):
                parse_search_page(stub=self.get_stub(), filepath=filename)
                page_n += 1
            else:
                logging.ERROR("No file " + filename)
                break

        logging.info('parse_save_search_entries done')

    def get_stub(self):
        return self.__stub
