import os
import logging
import logging.config
import pickle
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

############ IO
from zakupkiClient.dbclient import DbApi

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


def create_word_cloud(lots_csv, freq_csv):
    """
    creates freq csv
    :param freq_csv:
    :param lots_csv:
    :param out_csv:
    """
    DbApi().dump_table('lots', lots_csv)
    df = pd.read_csv(lots_csv, header=None)
    vectorizer = CountVectorizer(ngram_range=(1, 1),
                                 min_df=0.02,
                                 max_df=0.1,
                                 stop_words=get_list_from_pickle(
                                     Path.joinpath(get_project_root(), 'stop_words.pickle')))
    cv_fit = vectorizer.fit_transform(df[3]).toarray()
    s = set(zip(cv_fit.sum(axis=0), vectorizer.get_feature_names()))
    b = pd.DataFrame(s, columns=['freq', 'token'])
    b.index.name = 'id'
    for i, x in b.iterrows():
        d = x.to_dict()
        d['id'] = i
        DbApi().setup('freq', d)
    b.to_csv(freq_csv)


def create_word_table(lots_csv, freq_csv):
    freqs = pd.read_csv(freq_csv)
    df = pd.read_csv(lots_csv)
    for i, row in freqs.iterrows():
        for ix, r in df.iterrows():
            if row['token'] in r[3]:
                DbApi().setup('words', {'word_id': i,
                                        'guid': r[0],
                                        'num_words': r[3].count(row['token'])
                                        })


def create_words_database(lots_csv, freq_csv):
    create_word_cloud(lots_csv, freq_csv)
    create_word_table(lots_csv, freq_csv)


def get_active_db():
    try:
        active_db = os.environ['ZAKUPKI_ACTIVE_DB']
        return active_db
    except KeyError:
        logging.error('no env vars set')
        return None
