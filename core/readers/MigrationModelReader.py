from core.loaders.WorkspaceLoader import WorkspaceLoader
from core.models.mm.MigrationModel import MigrationModel
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class MigrationModelReader:

    def __init__(self):

        self._workspace = WorkspaceLoader().name()
        self._root_folder = 'workspaces/{workspace}'.format(workspace=self._workspace)

    def sdm_source(self) -> SimpleDatabaseModel:

        sdm_source_filename = self._root_folder + '/models/source.sdm'
        return SimpleDatabaseModel(filename=sdm_source_filename)

    def sdm_target(self) -> SimpleDatabaseModel:
        sdm_target_filename = self._root_folder + '/models/target.sdm'
        return SimpleDatabaseModel(filename=sdm_target_filename)

    def uvl_filename(self) -> str:
        return self._root_folder + '/uvl/{workspace}.uvl'.format(workspace=self._workspace)

    def migration_model(self) -> MigrationModel:

        return MigrationModel(sdm_source=self.sdm_source(), sdm_target=self.sdm_target(), uvl_file=self.uvl_filename())