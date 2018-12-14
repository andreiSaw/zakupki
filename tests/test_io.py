import os
import shutil

import pytest

from zakupki.zakupkiapi.util import get_filename, load_JSON_data, dump_JSON_data, get_query_dir


def test_io_json():
    data = ["xx", "yy"]
    ag_name = "Privet"
    fname = "test.json"
    dump_JSON_data(data=data, q=ag_name, filename=fname)
    if not os.path.exists(get_filename(q=ag_name, filename=fname)):
        pytest.fail("no json created")
    data2 = load_JSON_data(q=ag_name, filename=fname)
    if data2 != data:
        pytest.fail("error json")
    shutil.rmtree(get_query_dir(ag_name))
    pass
