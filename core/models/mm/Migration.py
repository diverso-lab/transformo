from core.models.mm.MigrationType import MigrationType


class Migration:

    def __init__(self, name: str, migration_type: MigrationType = MigrationType.Optional):
        self._name = name
        self._type = migration_type
        self._requires_migrations: list[Migration] = list()
        self._excludes_migrations: list[Migration] = list()

    def requires(self, migration):
        self._requires_migrations.append(migration)

    def excludes(self, migration):
        self._excludes_migrations.append(migration)
