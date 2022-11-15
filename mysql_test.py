from core.extractors.mysql.MySQLExtractor import MySQLExtractor


def main():
    # MySQL extraction
    mysql_extractor = MySQLExtractor(env=".env.drupal")
    mysql_extractor.extract()

    for t in mysql_extractor.tables():
        print(t)

    print("ok")


if __name__ == "__main__":
    main()
