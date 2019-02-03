import json
import os


def read_file(filepath):
    with open(filepath) as input_file:
        text = input_file.read()
    return text


def _checkDirectory_if_not_create(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_JSON_data(stub, filename):
    filepath = stub.get_filename(filename=filename)
    if not os.path.isfile(filepath):
        return []
    with open(filepath, "r") as json_data:
        data = json.load(json_data)
        if isinstance(data, list):
            return data
        return []


def _dump_JSON_data(stub, data, filename):
    _checkDirectory_if_not_create(stub.get_query_dir())
    filepath = stub.get_filename(filename=filename)
    with open(filepath, "w", encoding="UTF-8") as f:
        json.dump(data, f)

def saving(stub, data, filename):
    tmp = load_JSON_data(stub=stub, filename=filename)
    if tmp:
        _dump_JSON_data(stub=stub, data=tmp + data, filename=filename)
    else:
        _dump_JSON_data(stub=stub, data=data, filename=filename)