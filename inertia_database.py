import sqlite3
from pandas import DataFrame

class inertiaDB:
    def __init__(self, db_path:str = None):
        self.m_db_path = None
        self.m_connection = None
        self.m_cursor = None
        if db_path is not None:
            self.m_db_path = db_path
            self.open(self.m_db_path)

    def _create_stock(self, stock_symbol:str, exchange_symbol:str):
        query = '''CREATE TABLE {0}_{1} (DATE CHAR(10) PRIMARY KEY NOT NULL,
                                                       OPEN REAL NOT NULL,
                                                       HIGH REAL NOT NULL,
                                                       LOW  REAL NOT NULL,
                                                       CLOSE REAL NOT NULL, 
                                                    VOLUME REAL NOT NULL);'''.format(exchange_symbol, stock_symbol)
        try:
            self.m_cursor.execute(query)
            self.m_connection.commit()
        except sqlite3.OperationalError as errmsg:
            print(errmsg)



    def _read_stock(self, stock_symbol:str, exchange_symbol:str, date:str):
        """

        Fetches the next row of a query result set, returning a single sequence, or None when no more data is available.

        reference: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchone

        :return: a tuple of next row or 'None'
        """
        query = "select * from {0}_{1} where DATE=?".format(exchange_symbol, stock_symbol)
        print(query)
        t = (date,)
        try:
            self.m_cursor.execute(query, t)
            return self.m_cursor.fetchone()
        except sqlite3.OperationalError as errmsg:
            print(errmsg)
            return None

    def open(self, db_path:str = None):
        if db_path is None and self.m_db_path is None:
            return None
        if db_path is not None:
            self.m_db_path = db_path
        if self.m_connection is not None:
            self.m_connection.close()
        self.m_connection = sqlite3.connect(self.m_db_path)
        self.m_cursor = self.m_connection.cursor()

    def print_members(self):
        print("path={0}".format(self.m_db_path))
        print("connection={0}".format(self.m_connection))
        print("cursor={0}".format(self.m_cursor))
        if self.m_cursor is not None:
            print("   connection test is {0}".format(self.m_cursor.connection == self.m_connection))

    def add(self, stock_symbol:str, exchange_symbol:str, df:DataFrame):
        if len(df):
            self._create_stock(stock_symbol, exchange_symbol)
            data = []
            for item in df.iterrows():
                query = self._read_stock(stock_symbol, exchange_symbol, item[0].date())
                if query is not None:
                    print("already exist record: {0}".format(query))
                else:
                    data.append((item[0].date(), item[1][0], item[1][1], item[1][2], item[1][3], item[1][4]))
            table_name = "{0}_{1}".format(exchange_symbol, stock_symbol)
            syntax = "INSERT INTO {0} VALUES (?,?,?,?,?,?)".format(table_name)
            self.m_cursor.executemany(syntax, data)
            self.m_connection.commit()
        else:
            print("got nothing from google finance. {0}: {1}".format(exchange_symbol, stock_symbol))

    def fetchall(self, stock_symbol:str, exchange_symbol:str):
        if self.m_cursor is None:
            return None
        try:
            self.m_cursor.execute("SELECT * FROM {0}_{1} ORDER BY DATE".format(exchange_symbol, stock_symbol))
            l = self.m_cursor.fetchall()
        except sqlite3.OperationalError as errmsg:# handle the 'no such table' problem
            print(errmsg)
            l = []
        return l



