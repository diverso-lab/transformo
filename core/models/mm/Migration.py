from shutil import rmtree

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature

from core.models.mm import MigrationModel
from core.models.mm.MigrationType import MigrationType
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableActionsExtractor import AvailableActionsExtractor
from core.models.stm.AvailableAction import AvailableAction
from core.models.stm.SimpleTransformationModel import SimpleTransformationModel
from core.mutators.SimpleDatabaseModelMutator import SimpleDatabaseModelMutator
from core.writers.MigrationWriter import MigrationWriter


class Migration:

    def __init__(self, migration_model: MigrationModel, feature: Feature):

        # basic
        self._migration_model = migration_model
        self._feature = feature

        # derivative
        self._migration_name = self._feature.name
        self._current_sdm_source = migration_model.sdm_source()

        # for operations
        self._selected_actions: list[AvailableAction] = list()
        self._actions_counter: int = 0

    def __str__(self):
        return self._feature.__str__()

    # facades method
    def name(self):
        return self._feature.name

    def is_root(self):
        return self._feature.is_root()

    def is_abstract(self):
        return self._feature.is_abstract

    def define(self, opening=True) -> None:

        print(self._migration_model.root())

        # delete previous files

        extractor = AvailableActionsExtractor(sdm_source=self._current_sdm_source,
                                              sdm_target=self._migration_model.sdm_target())

        extractor.extract_available_actions()

        if len(extractor.available_actions()) == 0:
            return self._finish()

        # show migration info
        print()
        print("########################################")
        print("Current migration: {}".format(self._migration_name))
        print("########################################")
        print()

        # show available actions
        extractor.print()

        print("")

        inputted = str(input("Select an available action ('q' for quit): "))

        if inputted == "q":
            return self._finish()

        option = None
        try:
            option = int(inputted)
        except:
            self.define(opening=True)

        # selection of action from available actions in current SDM
        selected_action = extractor.available_actions()[option]
        self._selected_actions.append(selected_action)
        print("Selected action: \n")
        print(selected_action)

        # write transformation in STM file
        migration_writer = MigrationWriter(
            migration_model_name=self._migration_model.root(),
            migration_name=self._migration_name,
            available_action=selected_action,
            opening=opening,
            closing=False
        )
        migration_writer.write()
        last_stm = migration_writer.stm()
        # self._stm = last_stm

        # mutates previous SDM
        sdm_mutator = SimpleDatabaseModelMutator(
            current_sdm_source=self._current_sdm_source,
            last_stm=last_stm,
            actions_counter=self._actions_counter,
            migration_name=self._migration_name,
            folder="{}/{}".format(self._migration_model.root(), self._migration_name))

        sdm_mutator.mutate()
        self._current_sdm_source = sdm_mutator.new_sdm()

        # increments actions counter
        self._actions_counter = self._actions_counter + 1

        # recursive call
        self.define(opening=False)

    def _finish(self):
        pass

    '''
    def __init__(self, migration_name: str, migration_type: MigrationType = MigrationType.Optional):
        self._migration_name = migration_name
        self._migration_type = migration_type
        self._requires_migrations: list[Migration] = list()
        self._excludes_migrations: list[Migration] = list()
        self._migration_model: MigrationModel = None
        self._selected_actions: list[AvailableAction] = list()
        self._current_sdm_source: SimpleDatabaseModel = None
        self._actions_counter: int = 0
        self._stm = None

    def add_migration_model(self, migration_model: MigrationModel):
        self._migration_model = migration_model
        self._current_sdm_source = migration_model.sdm_source()

    def requires(self, migration) -> None:
        self._requires_migrations.append(migration)

    def excludes(self, migration) -> None:

        # to avoid infinite recursion
        if not migration in self._excludes_migrations:
            self._excludes_migrations.append(migration)
            migration.excludes(self)

    def name(self) -> str:
        return self._migration_name

    def type(self) -> MigrationType:
        return self._migration_type

    def stm(self) -> SimpleTransformationModel:
        return self._stm

    def requires_migrations(self) -> list:
        return self._requires_migrations

    def excludes_migrations(self) -> list:
        return self._excludes_migrations

    

    

    '''
