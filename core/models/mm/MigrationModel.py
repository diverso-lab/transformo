from core.models.mm.Migration import Migration
from core.models.mm.MigrationType import MigrationType
from core.models.sdm import SimpleDatabaseModel


class MigrationModel:

    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel):
        self._sdm_source = sdm_source
        self._sdm_target = sdm_target
        self._migrations: list[Migration] = list()

    def add_migration(self, name: str, migration_type: MigrationType = MigrationType.Optional) -> Migration:
        migration = Migration(name=name, migration_type=migration_type)
        self._migrations.append(migration)
        return migration