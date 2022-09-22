from core.models.mm.MigrationModel import MigrationModel
from core.models.mm.MigrationType import MigrationType
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


def main():
    sdm_source = SimpleDatabaseModel('models/source.sdm')
    sdm_target = SimpleDatabaseModel('models/target.sdm')

    migration_model = MigrationModel(sdm_source, sdm_target, root = "D2W")

    common_data = migration_model.add_migration('common data', MigrationType.Mandatory)
    migrate_users = migration_model.add_migration('migrate users')
    migrate_posts = migration_model.add_migration('migrate posts')
    migrate_forums = migration_model.add_migration('migrate forums')
    #migrate_content = migration_model.add_migration('migrate content')

    migrate_posts.requires(migrate_users)
    migrate_posts.excludes(migrate_forums)

    migration_model.export('D2W')

    # migration_model.selection()

    #print(migration_model.is_valid())

    print("Valid product: " + str(migration_model.is_valid_product()))

    print("Valid configuration: " + str(migration_model.is_valid_configuration()))


if __name__ == "__main__":
    main()
