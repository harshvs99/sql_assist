from sqlapp.sourcelayer import mssqlserver
import logging

logging.basicConfig(filename="main.log", encoding='utf-8', level=logging.INFO)

DB_TYPES = {'sqlserver': mssqlserver}


class db_factory(object):
    @staticmethod
    def get_db(db_type, **kwargs):
        logging.info(f'DB Driver :: Database type {db_type}')
        try:
            return DB_TYPES[db_type.lower()](**kwargs)
        except Exception as e:
            logging.error(f"DB Driver :: Error creating factory object: {e}")
            return None
