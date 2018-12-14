import os

import pytest

from zakupki.zakupkiapi import search_save
from zakupki.zakupkiapi.poisk import parse_save_search_entries, get_default_db_path, load_JSON_data
from zakupki.zakupkiapi.util import _get_session, get_search_folder_path


class TestPoisk(object):
    def test_search_save_parse_save(self):
        ses = _get_session()
        ag_name = "высшая+школа+экономики"
        search_save(p_limit=1, query=ag_name, s=ses)
        path = get_search_folder_path(q=ag_name)
        if not os.path.exists(path):
            pytest.fail("no dir created")
        if not os.path.exists(path + "page_1.html"):
            pytest.fail("no file created in dir")
        pass

    def test_parse_save_search_entries(self):
        ses = _get_session()
        ag_name = "высшая+школа+экономики"
        parse_save_search_entries(query=ag_name, session=ses)
        if not os.path.exists(get_default_db_path(ag_name)):
            pytest.fail("no db created in dir")
        lst = load_JSON_data(q=ag_name)
        if len(lst) < 1:
            pytest.fail("no entries parsed")
        pass
    # shutil.rmtree(get_query_dir(ag_name))
