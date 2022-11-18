from shutil import rmtree

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader

from core.extractors.DatabaseInfoExtractor import DatabaseInfoExtractor
from core.loaders.WorkspaceLoader import WorkspaceLoader
from core.models.mm.Migration import Migration
from core.models.sdm import SimpleDatabaseModel
from flamapy.core.discover import DiscoverMetamodels

from core.writers.MySQLWriter import MySQLWriter


def _check_is_migration_is_abstract(migration: Migration) -> None:

    if migration.is_abstract():
        raise Exception('Error! Actions cannot be defined on an abstract migration.')


class MigrationModel:

    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel, uvl_file: str):

        # flama kernel
        self._dm = DiscoverMetamodels()
        self._uvl = UVLReader(uvl_file)
        self._fm: FeatureModel = self._uvl.transform()

        # transformo kernel
        self._sdm_source: SimpleDatabaseModel = sdm_source
        self._sdm_target: SimpleDatabaseModel = sdm_target
        self._workspace: str = WorkspaceLoader().name()
        self._uvl_file: str = uvl_file
        self._migrations = {}

        # operations
        self._read_migrations()

    def migrations(self) -> {}:
        return self._migrations

    def _read_migrations(self):

        for f in self._fm.get_features():
            migration = Migration(migration_model=self, feature=f)
            self._migrations[f.name] = migration

    def define(self, migration_name: str) -> None:

        try:

            migration = self._migrations[migration_name]

            _check_is_migration_is_abstract(migration)

            try:
                rmtree("workspaces/{workspace}/migrations/{migration_name}".format(
                    workspace=self._workspace, migration_name=migration_name))
            except:
                pass

            migration.define()

        except KeyError as e:
            print("Error! '{}' not found in migration model".format(migration_name))

    '''
    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel):
        self._sdm_source = sdm_source
        self._sdm_target = sdm_target
        self._migrations: list[Migration] = list()
        self._available_migrations: list[Migration] = list()
        self._selected_migrations: list[Migration] = list()
        self._eligible_migrations: list[Migration] = list()
        self._uvl: str = ''
        self._dm = DiscoverMetamodels()
        self._exported_to_uvl = False
        self._workspace = WorkspaceLoader().name()
        self._root: str = self._workspace
    '''

    def sdm_source(self) -> SimpleDatabaseModel:
        return self._sdm_source

    def sdm_target(self) -> SimpleDatabaseModel:
        return self._sdm_target

    def root(self):
        return self._fm.root

    def workspace(self) -> str:
        return self._workspace

    '''
    def add_migration(self, name: str, migration_type: MigrationType = MigrationType.Optional) -> Migration:
        migration = Migration(migration_name=name, migration_type=migration_type)

        self._migrations.append(migration)

        if migration.type() == MigrationType.Mandatory:
            self._selected_migrations.append(migration)
        else:
            self._available_migrations.append(migration)

        migration.add_migration_model(self)

        return migration
    '''

    '''
    def migrations(self) -> list[Migration]:
        return self._migrations

    def print_available_migrations(self):

        print("Available migrations")

        i = 0

        for m in self._available_migrations:
            print("({}) ".format(i) + m.name())
            i = i + 1

    def print_selected_migrations(self):

        print("#####")
        print("Selected migrations:")

        i = 0

        for m in self._selected_migrations:
            print("-> " + m.name())
            i = i + 1

        print("#####")
        print()

    def finish(self):
        print()
        self.print_selected_migrations()
        print("Finish selection")

    def is_valid(self):
        return self._dm.use_operation_from_file("Valid", './models/' + self._uvl)

    def is_valid_product(self):
        return self._dm.use_operation_from_file("ValidProduct", './models/' + self._uvl,
                                                configuration_file='./models/D2W.csvconf')

    def is_valid_configuration(self):
        return self._dm.use_operation_from_file("ValidConfiguration", './models/' + self._uvl,
                                                configuration_file='./models/D2W.csvconf')

    def selection(self):

        if len(self._available_migrations) == 0:
            return self.finish()

        self.print_selected_migrations()

        self.print_available_migrations()

        try:

            inputted = str(input("\nSelect migration(s) ('q' for quit): "))

            if inputted == "q":
                return self.finish()

            option = int(inputted)

            migration = self._available_migrations[option]

            self._selected_migrations.append(migration)
            self._available_migrations.remove(migration)

            self._select_migration()

            return self.selection()

        except:

            return self.selection()

    def _export_selected_migrations(self, available_migration: Migration = None):

        with open('models/temp.csvconf', 'w') as f:

            f.write('{}\n'.format('D2W'))

            for s in self._selected_migrations:
                f.write('{}\n'.format(s.name().replace(' ', '_')))

            if not available_migration is None:
                f.write('{}\n'.format(available_migration.name().replace(' ', '_')))

    def _select_migration(self):

        self._eligible_migrations.clear()

        for a in self._available_migrations:

            print("checking... " + a.name())

            self._export_selected_migrations(available_migration=a)
            valid_product_with_available_migration = self._dm.use_operation_from_file("ValidProduct",
                                                                                      './models/' + self._uvl,
                                                                                      configuration_file='./models/temp.csvconf')

            self._export_selected_migrations()
            valid_product_without_available_migration = self._dm.use_operation_from_file("ValidProduct",
                                                                                         './models/' + self._uvl,
                                                                                         configuration_file='./models/temp.csvconf')

            # print("valid_product_with_available_migration: " + str(valid_product_with_available_migration))
            # print("valid_product_without_available_migration: " + str(valid_product_without_available_migration))

            # detected excludes
            if not valid_product_with_available_migration and valid_product_without_available_migration:

                print("detectado excludes")
                self._available_migrations.remove(a)

            # detected requires
            elif not valid_product_with_available_migration:

                print("detectado requires")

                self._selected_migrations.append(a)

                # mutates selected migration in temp file (csvconf)
                self._export_selected_migrations()

                self._available_migrations.remove(a)

                return self._select_migration()

            else:

                if valid_product_with_available_migration and valid_product_without_available_migration:
                    self._selected_migrations.append(a)

                    # self._eligible_migrations.append(a)

        # self._available_migrations.clear()
        # self._available_migrations = self._eligible_migrations.copy()

    

    def write_sql(self, selected_migrations: list[Migration]) -> None:
        database_info_extractor = DatabaseInfoExtractor(self._sdm_source, self._sdm_target)
        mysql_writer = MySQLWriter(selected_migrations=selected_migrations, root=self.root(), database_info_extractor=database_info_extractor)
        mysql_writer.write()

    '''