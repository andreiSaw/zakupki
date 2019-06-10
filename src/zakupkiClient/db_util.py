import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer
from zakupkiClient.dbclient import DbApi
from zakupkiClient.util import get_list_from_pickle, get_project_root


def create_word_cloud(lots_csv, freq_csv, active_db=None):
    """
    creates freq csv
    :param freq_csv:
    :param lots_csv:
    :param out_csv:
    """
    DbApi(active_db=active_db).dump_table('lots', lots_csv)
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
        DbApi(active_db=active_db).setup('freq', d)
    b.to_csv(freq_csv)


def create_word_table(lots_csv, freq_csv, active_db):
    freqs = pd.read_csv(freq_csv)
    df = pd.read_csv(lots_csv)
    for i, row in freqs.iterrows():
        for ix, r in df.iterrows():
            if row['token'] in r[3]:
                DbApi(active_db=active_db).setup('words', {'word_id': i,
                                                           'guid': r[0],
                                                           'num_words': r[3].count(row['token'])
                                                           })
