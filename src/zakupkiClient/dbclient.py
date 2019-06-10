import logging

import sqlalchemy as db

from zakupkiClient.util import get_active_db


class DbApi:
    def __init__(self, logger=None, active_db=None):
        if not active_db:
            active_db = get_active_db()
        self.__engine = db.create_engine('postgresql+psycopg2://postgres@localhost/%s' % active_db)

        self.__db_connection = self.__engine.connect()
        metadata = db.MetaData()

        self.__db = {'procurements': db.Table('procurements', metadata, autoload=True, autoload_with=self.__engine),
                     'buyers': db.Table('buyers', metadata, autoload=True, autoload_with=self.__engine),
                     'bids': db.Table('bids', metadata, autoload=True, autoload_with=self.__engine),
                     'lots': db.Table('lots', metadata, autoload=True, autoload_with=self.__engine),
                     'suppliers': db.Table('suppliers', metadata, autoload=True, autoload_with=self.__engine),
                     'words': db.Table('words', metadata, autoload=True, autoload_with=self.__engine),
                     'freq': db.Table('freq', metadata, autoload=True, autoload_with=self.__engine)
                     }
        self.logger = logger or logging.getLogger(__name__)

    def setup(self, db_name, value):
        try:
            query = db.insert(self.__db[db_name]).values(value)
            ResultProxy = self.__db_connection.execute(query)
            self.logger.info('inserted %s' % value)
        except Exception as e:
            self.logger.warning(f'{db_name}{e}')

    def get(self, db_name):
        try:
            query = db.select([self.__db[db_name]])
            return self.__db_connection.execute(query)
        except Exception as e:
            self.logger.warning(f'{db_name}{e}')

    def push(self, values):
        # print(values)
        suppliers = [b['supplier'] for l in values['lots'] for b in l['bids']]
        for s in suppliers:
            if s['inn']:
                s['region'] = s['inn'][:2]
            else:
                s['region'] = "Empty"
            self.setup('suppliers', s)

        # print(suppliers)

        buyer_tags = ['fullName', 'inn']
        buyer = {key: val for key, val in values.items() if key in buyer_tags}
        if buyer['inn']:
            buyer['region'] = buyer['inn'][:2]
        else:
            buyer['region'] = "Empty"
        self.setup('buyers', buyer)

        # print(buyer)

        procurement_tags = ['p_id', 'date']
        procurement = {key: val for key, val in values.items() if key in procurement_tags}
        procurement['buyer_inn'] = values['inn']

        self.setup('procurements', procurement)

        # print(procurement)

        blackist_bids = ['supplier']
        blackist_lot = ['bids']

        for ll in values['lots']:
            lot_bids = ll['bids']
            lot = {key: val for key, val in ll.items() if key not in blackist_lot}
            lot['p_id'] = procurement['p_id']
            self.setup('lots', lot)
            # print(lot)
            for b in lot_bids:
                bid = {key: val for key, val in b.items() if key not in blackist_bids}
                bid['guid'] = lot['guid']
                bid['supplier_inn'] = b['supplier']['inn']
                self.setup('bids', bid)
                print(bid)

    def update(self, table_name, values, id):
        try:
            statement = 'UPDATE lots set category= \'%s\' where lots.guid = \'%s\''
            return self.__db_connection.execute(statement % (values, id))
        except Exception as e:
            self.logger.warning(f'{table_name}{e}')

    def update_lots(self, purchase):
        for ll in purchase['lots']:
            self.update('lots', ll['category'], ll['guid'])

    def dump_table(self, table_name, out_csv):
        try:
            statement = 'COPY %s TO \'%s\'DELIMITER \',\' CSV HEADER;'
            return self.__db_connection.execute(statement % (table_name, out_csv))
        except Exception as e:
            self.logger.warning(f'{table_name}{e}')
