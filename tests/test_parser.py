import json
import os
import shutil

import pytest

from zakupkiClient import *

AG_NAME = "высшая школа экономики"


@pytest.fixture(scope="module")
def resource_setup(request):
    return Parser(Stub(query=AG_NAME, numFz="223"))


def teardown_module(module):
    print("\nmodule teardown")
    stub = Stub(query=AG_NAME, numFz="223")
    shutil.rmtree(stub.get_query_dir())


class TestParser(object):
    def test_search_save(self, resource_setup):
        parser = resource_setup
        stub = parser.get_stub()
        parser.search_save(page_limit=1)
        path = stub.get_search_folder_path()
        if not os.path.exists(path):
            pytest.fail("no dir created")
        if not os.path.exists(path + "page_1.html"):
            pytest.fail("no file created in dir")
        pass

    def test_parse_save_search_entries(self, resource_setup):
        parser = resource_setup
        stub = parser.get_stub()
        parser.parse_save_search_entries(page_limit=1)
        lst = load_json_data(stub=stub, filename=stub.get_purchase_db_name())
        if len(lst) < 1:
            pytest.fail("no entries parsed")
        pass

    def test_load_parse_purchase_page(self, resource_setup):
        parser = resource_setup
        stub = parser.get_stub()
        page = load_parse_purchase_page(p_id="31807061497", stub=stub)
        if len(page) < 1:
            pytest.fail("no page parsed")
        pass
