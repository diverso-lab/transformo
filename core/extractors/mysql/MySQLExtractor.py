from core.extractors.AbstractExtractor import AbstractExtractor
import mysql.connector

from core.extractors.mysql.Table import Table


class MySQLExtractor(AbstractExtractor):

    def __init__(self, env = ".env"):

        try:
            super().__init__(env = env)
        except Exception as e:
            print(e)
        
        try:
            connect = self.connect()
            connect.close()
        except:
            print("Error! Cannot connect to database. Check that the environment variables are correct in '{}'.".format(env))

        self._tables = []

    def connect(self):
        return mysql.connector.connect(
            host=super().host(),
            database=super().database(),
            user=super().user(),
            password=super().password(),
            port=super().port())

    def extract(self):
        self._extract_tables_names()

    def _extract_tables_names(self):
        mydb = self.connect()

        cursor = mydb.cursor()

        cursor.execute("SHOW TABLES")

        for (table_name,) in cursor:
            table = Table(table_name=table_name)
            self._tables.append(table)

        mydb.close()
