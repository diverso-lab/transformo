from core.models.mm.MigrationModel import MigrationModel
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


def main():

    sdm_source = SimpleDatabaseModel("assets/source.sdm")
    sdm_target = SimpleDatabaseModel("assets/target.sdm")

    migration_model = MigrationModel(sdm_source, sdm_target)

    migrate_users = migration_model.add_migration('migrate users')
    migrate_posts = migration_model.add_migration('migrate posts')
    migrate_forums = migration_model.add_migration('migrate forums')

    migrate_posts.requires(migrate_users)


if __name__ == "__main__":
    main()
