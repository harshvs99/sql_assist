import pyodbc


class MSqlConstants:
    dbType = 'sqlserver'


class mssqlserver():
    def __init__(self, server_name, user=None, password=None, database=None, table=None):
        self.server_name = server_name
        self.user = user
        self.password = password
        self.database = database
        self.table = table

        # self.driver = 'ODBC Driver 18 for SQL Server'
        self.driver = 'SQL Driver'
        self.connection = self.create_connection()

    def create_connection(self):
        if len(self.user) == 0 or self.user is None:
            conn_str = f"DRIVER={{{self.driver}}};SERVER={self.server_name};Trusted_Connection=yes"
        else:
            conn_str = f"DRIVER={{{self.driver}}};SERVER={self.server_name};UID={self.user};"
            if self.password is not None:
                conn_str = ''.join([conn_str, f'PWD={self.password};'])
        if self.database is not None:
            conn_str = ''.join([conn_str, f'DATABASE={self.database};'])

        print(conn_str)

        connection = pyodbc.connect(conn_str)
        return connection

    def get_table_metadata(self):
        cursor = self.connection.cursor()
        print(f"Metadata request recieved for table: {self.table}")
        metadata = []
        column_data = cursor.columns(
            table=self.table,
            catalog=self.database
        ).fetchall()
        columns = [column[0] for column in cursor.description]
        for col in column_data:
            metadata.append(dict(zip(columns, col)))
        print(f"Metadata received for table: {self.table}")
        return metadata

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.cursor().close()
            self.connection.close()
