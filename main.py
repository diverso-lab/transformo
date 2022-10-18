from core.models.mm.MigrationModel import MigrationModel
from core.models.mm.MigrationType import MigrationType
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


def main():

    # Definition of Simple Database Model
    sdm_source = SimpleDatabaseModel('models/source.sdm')
    sdm_target = SimpleDatabaseModel('models/target.sdm')

    # Definition of migration model and migrations (abstract level)
    migration_model = MigrationModel(sdm_source, sdm_target, root = "D2W")
    common_data = migration_model.add_migration('common data', MigrationType.Mandatory)
    users = migration_model.add_migration('migrate users')
    posts = migration_model.add_migration('migrate posts')
    comments = migration_model.add_migration('migrate comments')
    forums = migration_model.add_migration('migrate forums')
    posts.requires(users)
    comments.requires(posts)
    posts.excludes(forums)

    # Export to UVL
    migration_model.export('D2W')

    # Interactive definition of each migration
    users.define_migration()

    # Selection of migrations
    '''
        This is a pending implementation in the Flama framework.
        For the moment, let's assume that the dynamic feature selection 
        functionality (constraint propagation) is already implemented.
    '''
    #selected = migration_model.selection()
    selected = [common_data, users, posts, comments]


if __name__ == "__main__":
    main()
