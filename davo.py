from scripts.databaseHandler import *


def davo():
    conn = create_connection()
    drinks = select_drink_by_efficiency_and_type(conn, 'vodka')

    for drink in drinks:
        print(drink)

if __name__ == "__main__":
    davo()