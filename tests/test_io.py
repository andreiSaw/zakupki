import os
import shutil

import pytest

from zakupki.zakupkiapi.util import get_filename, load_JSON_data, dump_JSON_data, get_query_dir, _read_file

# TODO teardown_module fixture resource_setup
AG_NAME = "Privet"


def teardown_module(module):
    print("\nmodule teardown")
    shutil.rmtree(get_query_dir(AG_NAME))
    os.unlink("x.a")


@pytest.fixture(scope="module")
def resource_setup(request):
    return AG_NAME


def test_io_json(resource_setup):
    data = ["xx", "yy"]
    fname = "test.json"
    ag_name = resource_setup
    dump_JSON_data(data=data, q=ag_name, filename=fname)
    if not os.path.exists(get_filename(q=ag_name, filename=fname)):
        pytest.fail("no json created")
    data2 = load_JSON_data(q=ag_name, filename=fname)
    if data2 != data:
        pytest.fail("error json")
    pass


def test_read_file():
    res = "page"
    with open("x.a", 'w', encoding="UTF-8") as output_file:
        output_file.write(res)
    ans = _read_file("x.a")
    assert res == ans
