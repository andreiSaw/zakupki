import logging
import os
import re

from bs4 import BeautifulSoup

from zakupkiClient.db_util import create_word_table, create_word_cloud
from zakupkiClient.parserinterface import ParserInterface
from zakupkiClient.util import _check_directory_create
from zakupkiClient.webutils import parse_search_page, load_search_page, contain_purchase_data


class Parser(ParserInterface):
    def __init__(self, stub, logger=None):
        self.__stub = stub
        self.logger = logger or logging.getLogger(__name__)

    def allRecords(self):
        page = load_search_page(stub=self.get_stub(), p=1)
        soup = BeautifulSoup(page, features="lxml")
        if soup.find("p", {"class": "noRecords"}):
            self.logger.ERROR("No ans")
            return 0
        a = soup.find("p", {"class": "allRecords"}).text
        ans = int(re.sub(r'[^0-9]', "", a))
        self.logger.info(f'allRecords = {ans}')
        return ans

    def search_save(self, page_limit, page_offset=1):
        page = page_offset
        path = self.get_stub().get_search_folder_path()
        while page <= page_limit:
            self.logger.info('Loading page #%d' % (page))
            _check_directory_create(path)
            filepath = path + self.get_stub().get_page_filename()
            data = load_search_page(stub=self.get_stub(), p=page)
            if contain_purchase_data(data):
                with open(filepath % page, 'w', encoding="UTF-8") as output_file:
                    self.logger.info('Saving page #%d' % page)
                    output_file.write(data)
                    page += 1
            else:
                break

    def parse_save_search_entries(self, page_limit, page_offset=1):
        page_n = page_offset
        filepath = self.get_stub().get_search_folder_path() + self.get_stub().get_page_filename()
        self.logger.info("Openning dir " + filepath)
        while page_n <= page_limit:
            filename = filepath % page_n
            if os.path.isfile(filename):
                parse_search_page(stub=self.get_stub(), filepath=filename)
                page_n += 1
            else:
                self.logger.ERROR("No file " + filename)
                break

        self.logger.info('parse_save_search_entries done')

    @staticmethod
    def create_words_database(lots_csv, freq_csv,active_db=None):
        create_word_cloud(lots_csv, freq_csv, active_db)
        create_word_table(lots_csv, freq_csv, active_db)

    def get_stub(self):
        return self.__stub
