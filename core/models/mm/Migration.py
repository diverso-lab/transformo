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

    def define_migration(self):

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

            '''
            if self.__first_writing_in_file:
                return self.finish()

            self._close_transformations()
            self._generate_sql_script()
            return self.finish()
            '''
            
        option = int(inputed)

        # selection of action from available actions in current SDM
        selected_action = extractor.available_actions()[option]
        selected_actions.append(selected_action)
        print("Selected action: \n")
        print(selected_action)

        # write transformation in STM file
        stm_file = self.write_transformation(selected_action)
        #stm = SimpleTransformationModel(sdm = self._A, file = stm_file)

    def write_transformation(self, action):

        transformation_writer = MigrationWriter(
            filename = self._name,
            available_action = action, 
            first_write = self.__first_writing_in_file)
        transformation_writer.write()

        self.__first_writing_in_file = False

