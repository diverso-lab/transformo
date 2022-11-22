from core.configurators.WorkspaceConfigurator import WorkspaceConfigurator
from core.readers.MigrationModelReader import MigrationModelReader


def main():

    print()
    print("########################################")
    print("You're execute TEST APPLICATION ENGINEERING")
    print("########################################")
    print()

    # Setting workspace
    WorkspaceConfigurator(name='D2W')

    # Reading migration feature model
    migration_model = MigrationModelReader().migration_model()

    # Selection of migrations
    '''
        This is a pending implementation in the Flama framework.
        For the moment, let's assume that the dynamic feature selection 
        functionality (constraint propagation) is already implemented.
    '''

    # selected_migrations = migration_model.selection()
    selected_migrations = ['migrate_user_data']

    # Write SQL script
    migration_model.write_sql(selected_migrations_name=selected_migrations)


if __name__ == "__main__":
    main()
