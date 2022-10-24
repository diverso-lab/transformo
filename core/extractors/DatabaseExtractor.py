from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class DatabaseExtractor:

    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel) -> None:
        self._sdm_source = sdm_source
        self._sdm_target = sdm_target

    def database_source_name(self):
        return self._sdm_source.database_name()

    def database_target_name(self):
        return self._sdm_target.database_name()
        