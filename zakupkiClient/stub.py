import requests

_HEADERS = {
    'Referer': 'http://www.kinopoisk.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}
_PURCHASE_DB_NAME = "db.json"
_SEARCH_FOLDER = "search/"
_FILENAME = "page_%s.html"
_DATA_FOLDER = "./data/%s/"
_PURCHASE_INFO = {"223": "http://zakupki.gov.ru/%s/purchase/public/purchase/info/%s.html?regNumber=%s",
                  "44": "http://zakupki.gov.ru/epz/order/notice/ea44/view/%s.html?regNumber=%s"}
# _STOPLISTNAME = "stopwords.json"
_TAB = "common-info"
_LEN_LOT_LIST = 6
_LOTS_DB_NAME = "lots.json"
_PROTOCOL_PLUG_LINK = "http://zakupki.gov.ru%s"
_SEARCH_PAGE_URL = "http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?searchString=%s&pageNumber=%d&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz%s=on&pc=on&currencyId=-1&regionDeleted=false&sortBy=UPDATE_DATE"


class Stub:
    def __init__(self, query, numFz, target, headers=_HEADERS, purchase_db_name=_PURCHASE_DB_NAME,
                 search_folder_name=_SEARCH_FOLDER, page_filename=_FILENAME, data_folder_name=_DATA_FOLDER,
                 default_tab=_TAB, len_lot_list=_LEN_LOT_LIST, lots_db_name=_LOTS_DB_NAME,
                 protocol_plug_link=_PROTOCOL_PLUG_LINK, search_page_url=_SEARCH_PAGE_URL):
        self.__numFz = numFz
        self.__query = query
        self.__target = target

        self.__headers = headers
        self.__purchase_db_name = purchase_db_name
        self.__search_folder_name = search_folder_name
        self.__page_filename = page_filename
        self.__data_folder_name = data_folder_name
        self.__purchase_link = _PURCHASE_INFO[numFz]
        self.__default_tab = default_tab
        self.__len_lot_list = len_lot_list
        self.__lots_db_name = lots_db_name
        self.__protocol_plug_link = protocol_plug_link
        self.__search_page_url = search_page_url

        self.__establish_session()

    def get_session(self):
        return self.__s

    def get_query(self):
        return self.__query

    def get_numFz(self):
        return self.__numFz

    def get_target(self):
        return self.__target

    def get_purchase_db_name(self):
        return self.__purchase_db_name

    def get_data_folder_name(self):
        return self.__data_folder_name

    def get_search_folder_name(self):
        return self.__search_folder_name

    def get_len_lot_list(self):
        return self.__len_lot_list

    def get_purchase_link(self):
        return self.__purchase_link

    def get_protocol_plug_link(self):
        return self.__protocol_plug_link

    def get_lots_db_name(self):
        return self.__lots_db_name

    def get_page_filename(self):
        return self.__page_filename

    def __establish_session(self):
        self.__s = requests.Session()
        self.__s.headers.update(self.__headers)

    def get_query_dir(self):
        """
        gets dir as "data/query/"
        :param q: query
        :return: directory
        """
        return self.get_data_folder_name() % self.get_query()

    def get_filename(self, filename):
        """
        gets file from "data/query/filename"
        :param filename:
        :param q:
        :return:
        """
        return self.get_query_dir() + filename

    def get_search_folder_path(self):
        return self.get_query_dir() + self.get_search_folder_name()

    def get_purchase_tab(self, p_id, tab=_TAB):
        return self.get_purchase_link() % (self.get_numFz(), tab, p_id)

    def get_search_page_url(self, page_num):
        return self.__search_page_url % (self.get_query(), page_num, self.get_numFz())
