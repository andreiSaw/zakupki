import os
import shutil

import pytest

from zakupkiClient import *
# TODO teardown_module fixture resource_setup
from zakupkiClient.util import _check_directory_create

AG_NAME = "Privet"


def teardown_module(module):
    print("\nmodule teardown")
    stub = Stub(query=AG_NAME, numfz="223")
    shutil.rmtree(stub.get_query_dir())
    os.unlink("x.a")


@pytest.fixture(scope="module")
def resource_setup(request):
    return Stub(query=AG_NAME, numfz="223")


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
