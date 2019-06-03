import os
import shutil

import pytest

from zakupkiClient import *

AG_NAME = "высшая школа экономики"


@pytest.fixture(scope="module")
def resource_setup(request):
    return Parser(Stub(query=AG_NAME, numfz="223"))


def teardown_module(module):
    print("\nmodule teardown")
    stub4 = Stub(query=AG_NAME, numfz="223")
    shutil.rmtree(stub4.get_query_dir())


class TestParser(object):
    def test_search_save(self, resource_setup):
        parser2 = resource_setup
        stub_entity = parser2.get_stub()
        parser2.search_save(page_limit=1)
        path = stub_entity.get_search_folder_path()
        if not os.path.exists(path):
            pytest.fail("no dir created")
        if not os.path.exists(path + "page_1.html"):
            pytest.fail("no file created in dir")
        pass

    def test_parse_save_search_entries(self, resource_setup):
        parser1 = resource_setup
        parser1.parse_save_search_entries(page_limit=1)
        rs = DbApi().get('procurements')
        if rs.rowcount < 10:
            pytest.fail("no entries parsed")
        pass

    def test_parse_purchase(self, resource_setup):
        parser3 = resource_setup
        stub3 = parser3.get_stub()
        parse_purchase(p_id="31807061497", stub=stub3)
        rs = DbApi().get('procurements')
        if rs.rowcount < 1:
            pytest.fail("no purchase parsed")
        pass
