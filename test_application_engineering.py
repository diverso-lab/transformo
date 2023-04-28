from core.configurators.WorkspaceConfigurator import WorkspaceConfigurator
from core.readers.MigrationModelReader import MigrationModelReader
import time


def main():

    print()
    print("########################################")
    print("You're execute TEST APPLICATION ENGINEERING")
    print("########################################")
    print()

    start = time.time()

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

    # Get products
    products = migration_model.get_all_products()
    for p in products:
        print(p)

    # Get all scripts
    migration_model.get_all_scripts()

    end = time.time()

    print("Execution time: {} milliseconds".format((end - start) * 1000))
    


if __name__ == "__main__":
    main()
