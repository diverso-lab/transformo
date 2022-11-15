from abc import abstractmethod
from typing import Any
import os
from dotenv import load_dotenv

from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class AbstractExtractor:

    def __init__(self, env) -> None:

        # load environment file
        load_dotenv(env)

        # load environment variables 
        try:
            self._host = os.getenv('TRANSFORMO_HOST')
            self._port = int(os.getenv('TRANSFORMO_PORT'))
            self._database = os.getenv('TRANSFORMO_DATABASE')
            self._user = os.getenv('TRANSFORMO_USER')
            self._password = os.getenv('TRANSFORMO_PASSWORD')
        except:
            print("Error! There is a problem while opening '{}' environment file".format(env))

        if self._host == None:
            raise Exception("Error! 'TRANSFORMO_HOST' not found in {} file".format(env))

        if self._port == None:
            raise Exception("Error! 'TRANSFORMO_PORT' not found in {} file".format(env))

        if self._database == None:
            raise Exception("Error! 'TRANSFORMO_DATABASE' not found in {} file".format(env))

        if self._user == None:
            raise Exception("Error! 'TRANSFORMO_USER' not found in {} file".format(env))
        
        if self._password == None:
            raise Exception("Error! 'TRANSFORMO_WORDPRESS' not found in {} file".format(env))
        
   
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
