from scripts.databaseHandler import *


def davo():
    # conn = create_connection()
    # drinks = select_drink_by_efficiency_and_type(conn, 'beer')
    #
    # for drink in drinks:
    #     print(drink)

    metconn = create_metrics_connection()
    unique = total_search(metconn)
    print(unique)
    mostcommon = most_searched(metconn)
    print(mostcommon)


if __name__ == "__main__":
    davo()