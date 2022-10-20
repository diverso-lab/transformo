from core.models.mm.MigrationModel import MigrationModel
from core.models.mm.MigrationType import MigrationType
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


def main():

    # Definition of Simple Database Model
    sdm_source = SimpleDatabaseModel('models/D2W/source.sdm')
    sdm_target = SimpleDatabaseModel('models/D2W/target.sdm')

    # Definition of migration model and migrations (abstract level)
    migration_model = MigrationModel(sdm_source, sdm_target, root = "D2W")
    common_migration = migration_model.add_migration('common_migration', MigrationType.Mandatory)
    users_migration = migration_model.add_migration('users_migration')
    posts_migration = migration_model.add_migration('posts_migration')
    comments_migration = migration_model.add_migration('comments_migration')
    forums_migration = migration_model.add_migration('forums_migration')

    # Definition of constraints
    posts_migration.requires(users_migration)
    comments_migration.requires(posts_migration)
    posts_migration.excludes(forums_migration)

    # Export to UVL
    migration_model.export()

    # Interactive definition of each migration
    users_migration.define()

    # Selection of migrations
    '''
        This is a pending implementation in the Flama framework.
        For the moment, let's assume that the dynamic feature selection 
        functionality (constraint propagation) is already implemented.
    '''
    #selected = migration_model.selection()
    selected = [common_migration, users_migration, posts_migration, comments_migration]


if __name__ == "__main__":
    main()
