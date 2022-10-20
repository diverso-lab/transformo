from core.models.mm import MigrationModel
from core.models.mm.MigrationType import MigrationType
from core.models.stm.AvailableActionsExtractor import AvailableActionsExtractor
from core.models.stm.AvailableAction import AvailableAction
from core.writers.MigrationWriter import MigrationWriter


class Migration:

    def __init__(self, name: str, migration_type: MigrationType = MigrationType.Optional):
        self._name = name
        self._migration_type = migration_type
        self._requires_migrations: list[Migration] = list()
        self._excludes_migrations: list[Migration] = list()
        self._migration_model: MigrationModel = None
        self.__first_writing_in_file = True

    def add_migration_model(self, migration_model : MigrationModel):
        self._migration_model = migration_model

    def requires(self, migration):
        self._requires_migrations.append(migration)

    def excludes(self, migration):

        # to avoid infinite recursion
        if not migration in self._excludes_migrations:
            self._excludes_migrations.append(migration)
            migration.excludes(self)

    def name(self):
        return self._name

    def type(self):
        return self._migration_type

    def requires_migrations(self):
        return self._requires_migrations

    def excludes_migrations(self):
        return self._excludes_migrations

    def define_migration(self, opening = True):

        extractor = AvailableActionsExtractor(sdm_source = self._migration_model.sdm_source(), sdm_target = self._migration_model.sdm_target())
        selected_actions : list[AvailableAction] = list()

        # show current source SDM
        extractor.A().print()

        extractor.extract_available_actions()

        # show available actions
        extractor.print()

        print("")

        inputed = str(input("Select an available action ('q' for quit): "))

        if inputed == "q":

            migration_writer = MigrationWriter(
                migration_model_name = self._migration_model.root(),
                migration_name = self._name,
                available_action= None,
                opening = opening,
                closing = True
            )

            return self._finish()
            
        option = int(inputed)

        # selection of action from available actions in current SDM
        selected_action = extractor.available_actions()[option]
        selected_actions.append(selected_action)
        print("Selected action: \n")
        print(selected_action)

        # write transformation in STM file
        migration_writer = MigrationWriter(
            migration_model_name = self._migration_model.root(),
            migration_name = self._name,
            available_action = selected_action,
            opening = opening,
            closing = False
        )

        self.define_migration(opening = False)

    def _finish(self):
        pass

