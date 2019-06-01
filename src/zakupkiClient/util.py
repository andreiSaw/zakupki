import json
import os


############ IO
def read_file(filepath):
    with open(filepath) as input_file:
        text = input_file.read()
    return text


def _check_directory_create(directory):
    """
    check if dir exists and if not create dir
    :param directory: dir name
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_json_data(stub, filename):
    filepath = stub.get_filename(filename=filename)
    if not os.path.isfile(filepath):
        return []
    with open(filepath, "r") as json_data:
        data = json.load(json_data)
        if isinstance(data, list):
            return data
        return []


def _dump_json_data(stub, data, filename):
    _check_directory_create(stub.get_query_dir())
    filepath = stub.get_filename(filename=filename)
    with open(filepath, "w", encoding="UTF-8") as f:
        json.dump(obj=data, fp=f)


################ IO
def set_proxies():
    proxy_https = os.environ['PROXY_ZAKUPKI_HTTPS']
    proxy_http = os.environ['PROXY_ZAKUPKI_HTTP']
    return {'http': proxy_http, 'https': proxy_https}
