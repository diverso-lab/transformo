from core.configurators.WorkspaceConfigurator import WorkspaceConfigurator
from core.extractors.mysql.MySQLExtractor import MySQLExtractor


def main():

    # Setting workspace
    WorkspaceConfigurator(name='D2W')

    # MySQL extraction for Drupal
    drupal_mysql_extractor = MySQLExtractor(env=".env.drupal")
    drupal_mysql_extractor.extract()
    sdm_source = drupal_mysql_extractor.sdm()
    print(sdm_source.database_name())

    # MySQL extraction for WordPress
    wordpress_mysql_extractor = MySQLExtractor(env=".env.wp")
    wordpress_mysql_extractor.extract()
    sdm_target = wordpress_mysql_extractor.sdm()
    print(sdm_target.database_name())

    '''
    # MySQL extraction
    #mysql_extractor = MySQLExtractor()

    # Definition of Simple Database Model
    sdm_source = SimpleDatabaseModel('models/D2W/source.sdm')
    sdm_target = SimpleDatabaseModel('models/D2W/target.sdm')

    # Definition of migration model and migrations (abstract level)
    migration_model = MigrationModel(sdm_source, sdm_target, root="D2W")
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

        This is a pending implementation in the Flama framework.
        For the moment, let's assume that the dynamic feature selection 
        functionality (constraint propagation) is already implemented.

    # selected_migrations = migration_model.selection()
    selected_migrations = [users_migration, posts_migration]

    # Write SQL script
    migration_model.write_sql(selected_migrations)
    '''


if __name__ == "__main__":
    main()
