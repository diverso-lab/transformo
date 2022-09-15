from core.sdm.SimpleDatabaseModel import SimpleDatabaseModel


def main():

    sdm_source = SimpleDatabaseModel("assets/source.sdm")
    sdm_source.print()

    sdm2 = SimpleDatabaseModel("assets/target.sdm")
    sdm2.print()


if __name__ == "__main__":
    main()
