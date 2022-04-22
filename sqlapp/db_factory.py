from sqlapp.sourcelayer import mssqlserver

DB_TYPES = {'sqlserver': mssqlserver}


class db_factory(object):
    @staticmethod
    def get_db(db_type, **kwargs):
        print("object: ", db_type)
        print("return val: ", db_type.lower())
        try:
            return DB_TYPES[db_type.lower()](**kwargs)
        except Exception as e:
            print(f"Error creating factory object: {e}")
            return None
