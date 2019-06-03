import logging

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

    def get(self, db_name):
        try:
            query = db.select([self.__db[db_name]])
            return self.__db_connection.execute(query)
        except Exception as e:
            logging.warning(f'{db_name}{e}')

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

        blackist_lot = ['bids']

        for ll in values['lots']:
            lot = {key: val for key, val in ll.items() if key not in blackist_lot}
            lot['p_id'] = procurement['p_id']
            self.setup('lots', lot)
            # print(lot)

        blackist_bids = ['supplier']

        bids = [b for l in values['lots'] for b in l['bids']]
        for b in bids:
            bid = {key: val for key, val in b.items() if key not in blackist_bids}
            self.setup('bids', bid)
            # print(bid)
