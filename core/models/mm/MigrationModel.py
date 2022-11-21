import os
from os.path import exists
from shutil import rmtree

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, UVLWriter

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
        self._leaf_migrations = {}

        # operations
        self._read_migrations()
        self._read_leaf_migrations()
        self._set_sdm_contexts()

    def migrations(self) -> {}:
        return self._migrations

    def get_migration_by_name(self, migration_name: str):
        return self._migrations[migration_name]

    def _read_migrations(self):

        for f in self._fm.get_features():
            migration = Migration(migration_model=self, feature=f)
            self._migrations[f.name] = migration

    def _read_leaf_migrations(self) -> {}:

        self._leaf_migrations = {}

        for k in self._migrations:
            migration = self._migrations[k]
            if migration.is_leaf():
                self._leaf_migrations [migration.name()] = migration

        return self._leaf_migrations

    def _set_sdm_contexts(self):
        self._sdm_source.set_as_source()
        self._sdm_target.set_as_target()

    def wizard(self):

        os.system('cls')
        print("########################################")
        print("{workspace}: MIGRATION WIZARD".format(workspace=self._workspace))
        print("########################################")
        print()

        option = 0
        for m in self._leaf_migrations:

            undefined = ""
            if not os.path.exists('workspaces/{workspace}/migrations/{migration_name}'.format(
                    workspace=self._workspace,
                    migration_name=self._leaf_migrations[m])):
                undefined = "(UNDEFINED)"

            print("[{option}] {name} {undefined}".format(option=option,
                                                         name=self._leaf_migrations[m],
                                                         undefined=undefined))
            option = option + 1

        print()
        inputted = str(input("Select an available migration to manage ('q' for quit): "))

        if inputted == "q":
            return

        try:
            migrations = list(self._leaf_migrations.keys())
            migration_name = migrations[int(inputted)]
            migration = self.get_migration_by_name(migration_name)
            migration.define()
        except:
            return self.wizard()

        return self.wizard()

    '''
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

    def sdm_source(self) -> SimpleDatabaseModel:
        return self._sdm_source

    def sdm_target(self) -> SimpleDatabaseModel:
        return self._sdm_target

    def root(self):
        return self._fm.root

    def workspace(self) -> str:
        return self._workspace

    def export(self):
        uvl_writer = UVLWriter(self._fm, 'workspaces/{workspace}/uvl/{root}.uvl'.format(workspace=self._workspace,
                                                                                        root=self.root()))
        uvl_writer.transform()

    '''
    def is_valid(self):
        return self._dm.use_operation_from_file("Valid", './models/' + self._uvl)

    def is_valid_product(self):
        return self._dm.use_operation_from_file("ValidProduct", './models/' + self._uvl,
                                                configuration_file='./models/D2W.csvconf')

    def is_valid_configuration(self):
        return self._dm.use_operation_from_file("ValidConfiguration", './models/' + self._uvl,
                                                configuration_file='./models/D2W.csvconf')

    '''

    def write_sql(self, selected_migrations_name: list[str]) -> None:
        database_info_extractor = DatabaseInfoExtractor(self._sdm_source, self._sdm_target)

        selected_migrations = list()

        for s in selected_migrations_name:
            migration = self.get_migration_by_name(s)
            selected_migrations.append(migration)

        mysql_writer = MySQLWriter(selected_migrations=selected_migrations,
                                   root=self.root().name,
                                   database_info_extractor=database_info_extractor)
        mysql_writer.write()
