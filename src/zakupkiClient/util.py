import os
import logging
import logging.config
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer

############ IO

logging.getLogger(__name__)


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
    logging.config.fileConfig(Path.joinpath(get_project_root(), "logging_config.ini"), disable_existing_loggers=False)


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent


def get_list_from_pickle(filepath):
    with open(filepath, 'rb') as fp:
        logging.info('opened %s' % filepath)
        return pickle.load(fp)


def get_active_db():
    try:
        active_db = os.environ['ZAKUPKI_ACTIVE_DB']
        return active_db
    except KeyError:
        logging.error('no env vars set')
        return None


class StemmedCountVectorizer(CountVectorizer):
    def __init__(self, stemmer, *args, **kwargs):
        super(StemmedCountVectorizer, self).__init__(*args, **kwargs)
        self.stemmer = stemmer

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (self.stemmer.stem(word) for word in analyzer(doc.replace('\n', ' ')))
