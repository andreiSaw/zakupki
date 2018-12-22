import os
import shutil

import pytest

from zakupki.zakupkiapi import search_save
from zakupki.zakupkiapi.poisk import parse_save_search_entries, load_JSON_data, create_save_lots
from zakupki.zakupkiapi.util import get_session, get_search_folder_path, get_query_dir, load_parse_purchase_page, \
    dump_JSON_data

AG_NAME = "высшая+школа+экономики"


@pytest.fixture(scope="module", params=[(AG_NAME, get_session())])
def resource_setup(request):
    return request.param


def teardown_module(module):
    print("\nmodule teardown")
    shutil.rmtree(get_query_dir(AG_NAME))


class TestPoisk(object):
    def test_search_save(self, resource_setup):
        (ag_name, ses) = resource_setup
        search_save(p_limit=1, query=ag_name, s=ses)
        path = get_search_folder_path(q=ag_name)
        if not os.path.exists(path):
            pytest.fail("no dir created")
        if not os.path.exists(path + "page_1.html"):
            pytest.fail("no file created in dir")
        pass

    def test_parse_save_search_entries(self, resource_setup):
        (ag_name, ses) = resource_setup
        parse_save_search_entries(query=ag_name, session=ses)
        if not os.path.exists(get_query_dir(ag_name)):
            pytest.fail("no db created in dir")
        lst = load_JSON_data(q=ag_name)
        if len(lst) < 1:
            pytest.fail("no entries parsed")
        pass

    def test_load_parse_purchase_page(self, resource_setup):
        (ag_name, ses) = resource_setup
        page = load_parse_purchase_page(p_id="31807061497", session=ses)
        if len(page) < 1:
            pytest.fail("no page parsed")
        pass

    def test_create_save_lots(self, resource_setup):
        (ag_name, ses) = resource_setup
        data = [{"lots_num": 2, "purchase_id": "0",
                 "lots": [{"p_id": "2", "name": "id=2"}, {"p_id": "4", "name": "id=4"}]
                 }]
        dump_JSON_data(data=data, q=ag_name)
        res = create_save_lots(ag_name)
        ans = [{"p_id": "0", "name": "id=2"}, {"p_id": "0", "name": "id=4"}]
        assert res == ans
