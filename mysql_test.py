
from core.extractors.mysql.MySQLExtractor import MySQLExtractor


def main():

    # MySQL extraction
    mysql_extractor = MySQLExtractor(env = ".env.drupal")

    print("ok")

if __name__ == "__main__":
    main()