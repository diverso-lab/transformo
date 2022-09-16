from core.models.mm.Migration import Migration
from core.models.mm.MigrationType import MigrationType
from core.models.sdm import SimpleDatabaseModel
import copy


class MigrationModel:

    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel):
        self._sdm_source = sdm_source
        self._sdm_target = sdm_target
        self._migrations: list[Migration] = list()
        self._available_migrations: list[Migration] = list()
        self._selected_migrations: list[Migration] = list()

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

        for m in migration.excludes_migrations():
            self._available_migrations.remove(m)

        # recursive selection for requires
        for m in migration.requires_migrations():
            self._select_migration(m)

        if not migration in self._selected_migrations:
            self._selected_migrations.append(migration)
            self._available_migrations.remove(migration)
