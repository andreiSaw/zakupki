import os
import shutil

import pytest

from zakupkiClient import *
from zakupkiClient.util import _dump_JSON_data

AG_NAME = "высшая+школа+экономики"


@pytest.fixture(scope="module")
def resource_setup(request):
    return Stub(query=AG_NAME, numFz="223", target="auto")


def teardown_module(module):
    print("\nmodule teardown")
    stub = Stub(query=AG_NAME, numFz="223", target="auto")
    shutil.rmtree(stub.get_query_dir())


class TestPoisk(object):
    def test_search_save(self, resource_setup):
        stub = resource_setup
        search_save(p_limit=1, stub=stub)
        path = stub.get_search_folder_path()
        if not os.path.exists(path):
            pytest.fail("no dir created")
        if not os.path.exists(path + "page_1.html"):
            pytest.fail("no file created in dir")
        pass

    def test_parse_save_search_entries(self, resource_setup):
        stub = resource_setup
        parse_save_search_entries(stub=stub, p_limit=1)
        if not os.path.exists(stub.get_query_dir()):
            pytest.fail("no db created in dir")
        lst = load_JSON_data(stub=stub, filename=stub.get_purchase_db_name())
        if len(lst) < 1:
            pytest.fail("no entries parsed")
        pass

    def test_load_parse_purchase_page(self, resource_setup):
        stub = resource_setup
        page = load_parse_purchase_page(p_id="31807061497", stub=stub)
        if len(page) < 1:
            pytest.fail("no page parsed")
        pass

    def test_create_save_lots(self, resource_setup):
        stub = resource_setup
        data = [{"lots_num": 2, "purchase_id": "0", "Наименование организации": "default",
                 "lots": [{"p_id": "2", "name": "id=2", "category": "auto"},
                          {"p_id": "4", "name": "id=4", "category": "auto"}]
                 }]
        _dump_JSON_data(data=data, stub=stub, filename=stub.get_purchase_db_name())
        res = create_save_lots(stub=stub, category=stub.get_target())
        ans = [{"p_id": "0", "name": "id=2", "category": "auto", "buyer": "default"},
               {"p_id": "0", "name": "id=4", "category": "auto", "buyer": "default"}]
        assert res == ans
