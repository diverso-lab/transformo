from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class SimpleDatabaseModelWriter:

    def __init__(self, sdm: SimpleDatabaseModel, sdm_filename:str) -> None:
        self._sdm = sdm
        self._filename = sdm_filename

    def write(self) -> None:
        pass