from core.extractors.mysql.Column import Column
from core.extractors.mysql.Key import Key


class Table:

    def __init__(self, table_name: str) -> None:

        self._table_name = table_name
        self._columns = []
        self._keys = []

    def name(self) -> str:
        return self._table_name

    def set_columns(self, bulk_column_data) -> None:

        for column_data in bulk_column_data:
            column = Column(column_data)
            self._columns.append(column)

    def set_keys(self, bulk_key_data) -> None:
        for key_data in bulk_key_data:
            key = Key(key_data)
            self._keys.append(key)

    def columns(self):
        return self._columns

    def keys(self):
        return self._keys

    def primary_keys(self):

        primary_keys = []

        for key in self.keys():
            if key.is_primary():
                primary_keys.append(key)

        return primary_keys

    def __str__(self) -> str:
        string = "Table `" + self.name() + "`"

        string = string + "\n\n\tColumns: " + str(len(self.columns()))

        for column in self.columns():
            string = string + "\n\t" + str(column)

        string = string + "\n\n\tKeys: " + str(len(self.keys()))

        for key in self.keys():
            string = string + "\n\t" + str(key)

        return "\n" + string