from core.models.mm.Migration import Migration
from core.models.mm.MigrationType import MigrationType
from core.models.sdm import SimpleDatabaseModel
from flamapy.core.discover import DiscoverMetamodels


class MigrationModel:

    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel, root: str):
        self._sdm_source = sdm_source
        self._sdm_target = sdm_target
        self._migrations: list[Migration] = list()
        self._available_migrations: list[Migration] = list()
        self._selected_migrations: list[Migration] = list()
        self._eligible_migrations: list[Migration] = list()
        self._uvl: str = ''
        self._dm = DiscoverMetamodels()
        self._exported_to_uvl = False
        self._root = root

    def add_migration(self, name: str, migration_type: MigrationType = MigrationType.Optional) -> Migration:
        migration = Migration(name=name, migration_type=migration_type)

        self._migrations.append(migration)

        if migration.type() == MigrationType.Mandatory:
            self._selected_migrations.append(migration)
        else:
            self._available_migrations.append(migration)

        self.export(file_name=self._root)

        return migration

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
            self._select_migration(migration)

            return self.selection()

        except:

            return self.selection()

    def _export_selected_migrations(self, available_migration: Migration = None):

        with open('models/temp.csvconf', 'w') as f:

            f.write('{}\n'.format('D2W'))

            for s in self._selected_migrations:
                f.write('{}\n'.format(s.name().replace(' ','_')))

            if not available_migration is None:
                f.write('{}\n'.format(available_migration.name().replace(' ','_')))

    def _select_migration(self, migration: Migration):

        self._selected_migrations.append(migration)
        self._available_migrations.remove(migration)
        self._eligible_migrations.clear()

        print("selecting... " + migration.name())

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

            print("valid_product_with_available_migration: " + str(valid_product_with_available_migration))
            print("valid_product_without_available_migration: " + str(valid_product_without_available_migration))

            # detected requires
            if valid_product_with_available_migration and not valid_product_without_available_migration:

                print("detectadi requires")

                # self._available_migrations.remove(a)
                self._selected_migrations.append(a)

            # detected excludes
            if not valid_product_with_available_migration and valid_product_without_available_migration:

                print("detectado excludes")
                # self._available_migrations.remove(a)

            if valid_product_with_available_migration and valid_product_without_available_migration:

                self._eligible_migrations.append(a)

        self._available_migrations.clear()
        self._available_migrations = self._eligible_migrations.copy()

    def export(self, file_name):
        with open('models/' + file_name + ".uvl", 'w') as f:

            f.write('namespace {}\n\n'.format(file_name))

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
                        string = '\t{} => ! {}\n'.format(m.name().replace(" ", "_"),
                                                         exclude_migration.name().replace(' ', '_'))
                        f.write(string)

        self._uvl = file_name + '.uvl'

        self._exported_to_uvl = True
