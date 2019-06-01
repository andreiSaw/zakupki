import os
import shutil

import pytest

from src.zakupkiClient import *
# TODO teardown_module fixture resource_setup
from zakupkiClient.util import _dump_json_data, _check_directory_create

AG_NAME = "Privet"


def teardown_module(module):
    print("\nmodule teardown")
    stub = Stub(query=AG_NAME, numFz="223")
    shutil.rmtree(stub.get_query_dir())
    os.unlink("x.a")


@pytest.fixture(scope="module")
def resource_setup(request):
    return Stub(query=AG_NAME, numFz="223")


def test_io_json(resource_setup):
    data = ["xx", "yy"]
    fname = "test.json"
    stub = resource_setup
    _dump_json_data(stub=stub, data=data, filename=fname)
    if not os.path.exists(stub.get_filename(filename=fname)):
        pytest.fail("no json created")
    data2 = load_json_data(stub=stub, filename=fname)
    if data2 != data:
        pytest.fail("error json")
    pass


def test_read_file():
    res = "page"
    with open("x.a", 'w', encoding="UTF-8") as output_file:
        output_file.write(res)
    ans = read_file("x.a")
    assert res == ans


def test_checkDirectory_if_not_create(resource_setup):
    stub = resource_setup
    directory = f'{stub.get_query_dir()}test'
    assert not os.path.exists(directory)
    _check_directory_create(directory)
    assert os.path.exists(directory)
    shutil.rmtree(directory)
    assert not os.path.exists(directory)
