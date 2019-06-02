import logging
from sqlalchemy import exc

import sqlalchemy as db


class DbApi:
    def __init__(self):
        engine = db.create_engine('postgresql+psycopg2://postgres@localhost/zakupki')

        self.__db_connection = engine.connect()
        metadata = db.MetaData()

        self.__db = {'procurements': db.Table('procurements', metadata, autoload=True, autoload_with=engine),
                     'buyers': db.Table('buyers', metadata, autoload=True, autoload_with=engine),
                     'bids': db.Table('bids', metadata, autoload=True, autoload_with=engine),
                     'lots': db.Table('lots', metadata, autoload=True, autoload_with=engine),
                     'suppliers': db.Table('suppliers', metadata, autoload=True, autoload_with=engine)}

    def setup(self, db_name, value):
        try:
            query = db.insert(self.__db[db_name]).values(value)
            ResultProxy = self.__db_connection.execute(query)
        except Exception as e:
            logging.warning(f'{db_name}{e}')

        # def run(self):

    def get(self, db_name):
        try:
            query = db.select(self.__db[db_name])
            return self.__db_connection.execute(query)
        except Exception as e:
            logging.warning(f'{db_name}{e}')
