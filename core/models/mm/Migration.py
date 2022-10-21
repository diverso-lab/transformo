from core.models.mm import MigrationModel
from core.models.mm.MigrationType import MigrationType
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableActionsExtractor import AvailableActionsExtractor
from core.models.stm.AvailableAction import AvailableAction
from core.mutators.SimpleDatabaseModelMutator import SimpleDatabaseModelMutator
from core.writers.MigrationWriter import MigrationWriter


class Migration:

    def __init__(self, migration_name: str, migration_type: MigrationType = MigrationType.Optional):
        self._migration_name = migration_name
        self._migration_type = migration_type
        self._requires_migrations: list[Migration] = list()
        self._excludes_migrations: list[Migration] = list()
        self._migration_model: MigrationModel = None
        self._selected_actions: list[AvailableAction] = list()
        self._current_sdm_source:SimpleDatabaseModel = None
        self._actions_counter:int = 0

    def add_migration_model(self, migration_model : MigrationModel):
        self._migration_model = migration_model
        self._current_sdm_source = migration_model.sdm_source()

    def requires(self, migration):
        self._requires_migrations.append(migration)

    def excludes(self, migration):

        # to avoid infinite recursion
        if not migration in self._excludes_migrations:
            self._excludes_migrations.append(migration)
            migration.excludes(self)

    def name(self):
        return self._migration_name

    def type(self):
        return self._migration_type

    def requires_migrations(self):
        return self._requires_migrations

    def excludes_migrations(self):
        return self._excludes_migrations

    def define(self, opening = True):

        extractor = AvailableActionsExtractor(sdm_source = self._current_sdm_source, sdm_target = self._migration_model.sdm_target())

        # show current source SDM
        extractor.A().print()

        extractor.extract_available_actions()

        # show available actions
        extractor.print()

        print("")

        inputed = str(input("Select an available action ('q' for quit): "))

        if inputed == "q":

            return self._finish()
            
        option = int(inputed)

        # selection of action from available actions in current SDM
        selected_action = extractor.available_actions()[option]
        self._selected_actions.append(selected_action)
        print("Selected action: \n")
        print(selected_action)

        # write transformation in STM file
        migration_writer = MigrationWriter(
            migration_model_name = self._migration_model.root(),
            migration_name = self._migration_name,
            available_action = selected_action,
            opening = opening,
            closing = False
        )
        migration_writer.write()
        last_stm = migration_writer.stm()

        print("HOLAAAA")
        print(last_stm)

        # mutates previous SDM
        sdm_mutator = SimpleDatabaseModelMutator(
            current_sdm_source=self._current_sdm_source,
            last_stm=last_stm,
            actions_counter = self._actions_counter,
            migration_name = self._migration_name)
        # TODO: mutate
        sdm_mutator.mutate()
        # TODO: return new SDM
        # self._current_sdm_source = sdm_mutator.new_sdm()

        self._actions_counter = self._actions_counter + 1

       

        # recursive 
        self.define(opening = False)

    def _finish(self):
        pass

