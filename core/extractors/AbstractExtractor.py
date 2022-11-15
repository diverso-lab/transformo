from abc import abstractmethod
from typing import Any
import os
from dotenv import load_dotenv

from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class AbstractExtractor:

    def __init__(self) -> None:

        # load environment variables for connection
        load_dotenv()
        self._host = os.getenv('HOST')
        self._port = int(os.getenv('PORT'))
        self._database = os.getenv('DATABASE')
        self._user = os.getenv('USER')
        self._password = os.getenv('PASSWORD')

        self._sdm = None
        self._connect = None

    def host(self) -> str:
        return self._host

    def port(self) -> int:
        return self._port

    def database(self) -> str:
        return self._database

    def user(self) -> str:
        return self._user

    def password(self) -> str:
        return self._password

    def sdm(self):
        return self._sdm

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def extract(self):
        pass
