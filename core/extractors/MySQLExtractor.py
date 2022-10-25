from core.extractors.AbstractExtractor import AbstractExtractor
import mysql.connector


class MySQLExtractor(AbstractExtractor):

    def __init__(self):
        self.__tables = []

        super().__init__(connect=None, sdm=None)

    def connect(self):
        return mysql.connector.connect(
            host=super().host(),
            database=super().database(),
            user=super().user(),
            password=super().password(),
            port=super().port())

    def extract(self):
        pass
