from scripts import classItem
from scripts.databaseHandler import *


def func():
    drinks = list()
    a = classItem.Item('bws', 'brand1', 'a', 'vodka', 50, 'https://google.com', 700, 50, 22, 22/50)
    b = classItem.Item('bws', 'brand2', 'b', 'whiskey', 234, 'https://google.com', 700, 50, 123, 123/50)
    c = classItem.Item('bws', 'brand3', 'c', 'vodka', 1, 'https://google.com', 700, 50, 50, 50/50)
    d = classItem.Item('bws', 'brand4', 'd', 'vodka', 788764, 'https://google.com', 700, 50, 32, 32/50)
    e = classItem.Item('bws', 'brand5', 'e', 'vodka', 3234, 'https://google.com', 700, 50, 2, 2/50)
    f = classItem.Item('123', 'brand5', 'e', 'vodka', 3234, 'https://google.com', 700, 50, 2, 2/50)

    drinks.append(a)
    drinks.append(b)
    drinks.append(c)
    drinks.append(d)
    drinks.append(e)

    conn = None
    try:
        conn = sqlite3.connect("drinks.db")
        print(sqlite3.version)
    except Error as e:
        print(e)

    dbhandler(conn, drinks, 'p')

    select_all_drinks(conn)

    print("---")

    update_drink(conn, drinks[0], 999999999)

    select_all_drinks_by_efficiency(conn)

    print(is_drink_in_table(conn, b))
    print(is_drink_in_table(conn, f))

    newB = classItem.Item('bws', 'brand2', 'b', 'whiskey', -10, 'https://google.com', 700, 50, 123, 123/50)

    update_drink(conn, newB, newB.price)

    print("---")

    select_all_drinks(conn)

    delete_all(conn)


if __name__ == "__main__":
    func()
