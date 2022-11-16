from abc import abstractmethod
from dotenv import dotenv_values


class AbstractExtractor:

    def __init__(self, env: str) -> None:

        # load environment file
        dotenv_values_dict = dotenv_values(env)

        # save environment variables
        try:
            self._host = dotenv_values_dict['HOST']
            self._port = int(dotenv_values_dict['PORT'])
            self._database = dotenv_values_dict['DATABASE']
            self._user = dotenv_values_dict['USER']
            self._password = dotenv_values_dict['PASSWORD']
        except:
            print("Error! There is a problem while opening '{}' environment file".format(env))

        if self._host is None:
            raise Exception("Error! 'HOST' not found in {} file".format(env))

        if self._port is None:
            raise Exception("Error! 'PORT' not found in {} file".format(env))

        if self._database is None:
            raise Exception("Error! 'DATABASE' not found in {} file".format(env))

        if self._user is None:
            raise Exception("Error! 'USER' not found in {} file".format(env))

        if self._password is None:
            raise Exception("Error! 'WORDPRESS' not found in {} file".format(env))

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
