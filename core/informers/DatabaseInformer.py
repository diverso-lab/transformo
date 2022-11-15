
class DatabaseInformer:

    def __init__(self, host: str, database: str, user: str, password: str, port: int):
        self._host = host
        self._database = database
        self._user = user
        self._password = password
        self._port = port

    def database(self) -> str:
        return self._database
