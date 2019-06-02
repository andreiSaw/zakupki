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


################ IO
def set_proxies():
    proxy_https = os.environ['PROXY_ZAKUPKI_HTTPS']
    proxy_http = os.environ['PROXY_ZAKUPKI_HTTP']
    return {'http': proxy_http, 'https': proxy_https}
