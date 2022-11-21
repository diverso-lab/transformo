from core.configurators.WorkspaceConfigurator import WorkspaceConfigurator
from core.extractors.mysql.MySQLExtractor import MySQLExtractor
from core.models.mm.MigrationModel import MigrationModel
from core.readers.MigrationModelReader import MigrationModelReader


def main():

    print()
    print("########################################")
    print("You're execute TEST DOMAIN ENGINEERING")
    print("Definition of migration model")
    print("########################################")
    print()

    # Setting workspace
    WorkspaceConfigurator(name='D2W')

    # Reading migration feature model
    migration_model = MigrationModelReader().migration_model()

    migration_model.wizard()


if __name__ == "__main__":
    main()
