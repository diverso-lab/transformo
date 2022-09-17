from core.models.mm import MigrationModel
from core.models.mm.MigrationType import MigrationType


class Migration:

    def __init__(self, name: str, migration_type: MigrationType = MigrationType.Optional):
        self._name = name
        self._migration_type = migration_type
        self._requires_migrations: list[Migration] = list()
        self._excludes_migrations: list[Migration] = list()
        self._migration_model: MigrationModel = None

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
