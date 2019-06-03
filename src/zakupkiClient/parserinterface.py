class ParserInterface:
    __stub = None

    def search_save(self, p_limit, offset=1):
        """
        Using web scrapping asks search engine to find query through pages_limit pages, and saves search pages
        :param offset: page number to start with
        :param p_limit: number of pages to save
        """
        raise NotImplementedError()

    def parse_save_search_entries(self, p_limit, offset=1):
        """
        Parse all over search entries and then dump them
        :return: purchase_list[] represents all purchases for that query
        """
        raise NotImplementedError()

    @property
    def get_stub(self):
        return self.__stub
