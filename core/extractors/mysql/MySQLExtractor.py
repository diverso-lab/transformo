from core.extractors.AbstractExtractor import AbstractExtractor
import mysql.connector

from core.extractors.mysql.Table import Table
from core.informers.DatabaseInformer import DatabaseInformer
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.writers.SimpleDatabaseModelWriter import SimpleDatabaseModelWriter


class MySQLExtractor(AbstractExtractor):

    def __init__(self, env=".env"):

        try:
            super().__init__(env=env)
        except Exception as e:
            print(e)

        try:
            connect = self.connect()
            connect.close()
        except:
            print("Error! Cannot connect to database. Check that the environment variables are correct in '{}'.".format(env))

        self._tables = []
        self._sdm: SimpleDatabaseModel = None

    def connect(self):
        return mysql.connector.connect(
            host=super().host(),
            database=super().database(),
            user=super().user(),
            password=super().password(),
            port=super().port())

    def tables(self) -> list[Table]:
        return self._tables

    def extract(self):

        self._extract_tables_names()
        self._extract_columns()
        self._extract_keys()

        self._generate_simple_database_model()

    def _extract_tables_names(self):
        mydb = self.connect()

        cursor = mydb.cursor()

        cursor.execute("SHOW TABLES")

        for (table_name,) in cursor:
            table = Table(table_name=table_name)
            self._tables.append(table)

        mydb.close()

    def _extract_columns(self):

        mydb = self.connect()

        cursor = mydb.cursor()

        for table in self._tables:
            cursor.execute("DESCRIBE " + table.name())

            bulk_column_data = cursor.fetchall()

            table.set_columns(bulk_column_data)

        mydb.close()

    def _extract_keys(self):
        mydb = self.connect()

        cursor = mydb.cursor()

        for table in self._tables:
            cursor.execute("SHOW KEYS FROM " + table.name() + "")

            bulk_key_data = cursor.fetchall()

            table.set_keys(bulk_key_data)

        mydb.close()

    def _generate_simple_database_model(self):

        database_informer = DatabaseInformer(host=super().host(),
                                             database=super().database(),
                                             user=super().user(),
                                             password=super().password(),
                                             port=super().port())

        sdm_writer = SimpleDatabaseModelWriter(tables=self.tables(), database_informer=database_informer)
        sdm_writer.write()

        self._sdm = sdm_writer.sdm()

    def sdm(self) -> SimpleDatabaseModel:
        return self._sdm
        