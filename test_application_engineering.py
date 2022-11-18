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


if __name__ == "__main__":
    main()
