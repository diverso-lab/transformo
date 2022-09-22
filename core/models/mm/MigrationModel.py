from core.models.mm.Migration import Migration
from core.models.mm.MigrationType import MigrationType
from core.models.sdm import SimpleDatabaseModel
import copy

from flamapy.core.discover import DiscoverMetamodels


class MigrationModel:

    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel):
        self._sdm_source = sdm_source
        self._sdm_target = sdm_target
        self._migrations: list[Migration] = list()
        self._available_migrations: list[Migration] = list()
        self._selected_migrations: list[Migration] = list()
        self._uvl: str = ''
        self._dm = DiscoverMetamodels()

    def add_migration(self, name: str, migration_type: MigrationType = MigrationType.Optional) -> Migration:
        migration = Migration(name=name, migration_type=migration_type)

        self._migrations.append(migration)

        if migration.type() == MigrationType.Mandatory:
            self._selected_migrations.append(migration)
        else:
            self._available_migrations.append(migration)

        return migration

    def migrations(self) -> list[Migration]:
        return self._migrations

    def available_migrations(self):

        print("Available migrations")

        i = 0

        for m in self._available_migrations:
            print("({}) ".format(i) + m.name())
            i = i + 1

    def selected_migrations(self):

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
        self.selected_migrations()
        print("Finish selection")

    def is_valid(self):
        return self._dm.use_operation_from_file("Valid", './models/' + self._uvl)

    def is_valid_product(self):
        return self._dm.use_operation_from_file("ValidProduct", './models/' + self._uvl,
                                                configuration_file='./models/D2W.csvconf')

    def selection(self):

        if len(self._available_migrations) == 0:
            return self.finish()

        self.selected_migrations()

        self.available_migrations()

        try:

            inputted = str(input("\nSelect migration(s) ('q' for quit): "))

            if inputted == "q":
                return self.finish()

            option = int(inputted)

            migration = self._available_migrations[option]
            self._select_migration(migration)

            return self.selection()

        except:

            return self.selection()

    def _select_migration(self, migration: Migration):

        # migrations that are 'excludes' are removed from available migrations
        for m in migration.excludes_migrations():
            self._available_migrations.remove(m)

        # recursive selection for requires
        for m in migration.requires_migrations():
            self._select_migration(m)

        if not migration in self._selected_migrations:
            self._selected_migrations.append(migration)
            self._available_migrations.remove(migration)

    def export(self, file_name):
        with open('models/' + file_name + ".uvl", 'w') as f:

            # print features
            f.write('features\n')
            f.write('\t' + file_name + ' { abstract }\n')
            # print mandatory features
            f.write('\t\tmandatory\n')
            for m in self._migrations:
                if m.type() == MigrationType.Mandatory:
                    string = "\t\t\t{}\n".format(m.name().replace(" ", "_"))
                    f.write(string)

            # print optional features
            f.write('\t\toptional\n')
            for m in self._migrations:
                if m.type() == MigrationType.Optional:
                    string = "\t\t\t{}\n".format(m.name().replace(" ", "_"))
                    f.write(string)

            # print constraints
            f.write('constraints\n')
            for m in self._migrations:

                if len(m.requires_migrations()) > 0:
                    for require_migration in m.requires_migrations():
                        string = '\t{} => {}\n'.format(m.name().replace(" ", "_"),
                                                       require_migration.name().replace(' ', '_'))
                        f.write(string)

                if len(m.excludes_migrations()) > 0:
                    for exclude_migration in m.excludes_migrations():
                        string = '\t{} => !{}\n'.format(m.name().replace(" ", "_"),
                                                        exclude_migration.name().replace(' ', '_'))
                        f.write(string)

        self._uvl = file_name + '.uvl'
