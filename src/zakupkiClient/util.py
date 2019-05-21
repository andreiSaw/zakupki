import json
import os
import datetime


############ IO
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
        json.dump(obj=data, fp=f, default=default_json_datetime)


def saving(stub, data, filename):
    tmp = load_JSON_data(stub=stub, filename=filename)
    if tmp:
        _dump_JSON_data(stub=stub, data=tmp + data, filename=filename)
    else:
        _dump_JSON_data(stub=stub, data=data, filename=filename)


def default_json_datetime(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


################ IO
def set_proxies():
    proxy_https = os.environ['PROXY_ZAKUPKI_HTTPS']
    proxy_http = os.environ['PROXY_ZAKUPKI_HTTP']
    return {'http': proxy_http, 'https': proxy_https}
