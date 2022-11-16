from flamapy.metamodels.fm_metamodel.transformations import UVLReader

from core.configurators.WorkspaceConfigurator import WorkspaceConfigurator
from core.extractors.mysql.MySQLExtractor import MySQLExtractor
from core.models.mm.MigrationModel import MigrationModel


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

    # Migration feature model
    migration_model = MigrationModel(sdm_source, sdm_target, 'workspaces/D2W/uvl/D2W.uvl')



if __name__ == "__main__":
    main()
