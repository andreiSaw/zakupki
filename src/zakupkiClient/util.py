import os
import logging
import logging.config
from pathlib import Path

############ IO
import sys


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
    try:
        proxy_https = os.environ['PROXY_ZAKUPKI_HTTPS']
        proxy_http = os.environ['PROXY_ZAKUPKI_HTTP']
        return {'http': proxy_http, 'https': proxy_https}
    except KeyError:
        logging.error('no env vars set')
        return None


def set_logger():
    logging.config.fileConfig(Path.joinpath(get_project_root(), "logging_config.ini"))


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent
