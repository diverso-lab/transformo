from core.configurators.WorkspaceConfigurator import WorkspaceConfigurator
from core.extractors.mysql.MySQLExtractor import MySQLExtractor
from core.models.mm.MigrationModel import MigrationModel
from core.models.mm.MigrationType import MigrationType


def main():

    print()
    print("########################################")
    print("You're execute a proof of concept")
    print("########################################")
    print()

    # Setting workspace
    WorkspaceConfigurator(name='D2W')

    # SDM from Drupal
    drupal_mysql_extractor = MySQLExtractor(env=".env.drupal")
    drupal_mysql_extractor.extract()
    sdm_source = drupal_mysql_extractor.sdm()

    # SMD from WordPress
    wordpress_mysql_extractor = MySQLExtractor(env=".env.wp")
    wordpress_mysql_extractor.extract()
    sdm_target = wordpress_mysql_extractor.sdm()

    # Definition of migration model and migrations (abstract level)
    migration_model = MigrationModel(sdm_source, sdm_target)
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
    posts_migration.define()

    # Selection of migrations
    '''
        This is a pending implementation in the Flama framework.
        For the moment, let's assume that the dynamic feature selection 
        functionality (constraint propagation) is already implemented.
    '''

    # selected_migrations = migration_model.selection()
    selected_migrations = [users_migration, posts_migration]

    # Write SQL script
    migration_model.write_sql(selected_migrations)


if __name__ == "__main__":
    main()
