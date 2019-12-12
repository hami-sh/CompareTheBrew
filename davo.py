from scripts.databaseHandler import *


def davo():
    conn = create_connection()
    drinks = select_all_drinks(conn)

    for drink in drinks:
        print(drink)

if __name__ == "__main__":
    davo()
