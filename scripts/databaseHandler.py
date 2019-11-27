import sqlite3
from sqlite3 import Error
from scripts.classItem import Item


def create_entry(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO drinks(store,brand,name,type,price,link,ml,percent,stdDrinks,efficiency)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def select_all_drinks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM drinks")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_all_drinks_by_efficiency(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM drinks ORDER BY efficiency DESC")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_drink_by_efficiency_and_type(conn, type):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM drinks WHERE type = '%s' ORDER BY efficiency DESC" % type)

    rows = cur.fetchall()

    for row in rows:
        print(row)


def update_drink_price(conn, drink, newPrice):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param drink:
    :return: project id
    """
    sql = ''' UPDATE drinks
              SET price = ?
              WHERE name = ?
              AND brand = ?
              AND store = ?
              AND type = ? '''
    cur = conn.cursor()
    cur.execute(sql, (newPrice, drink.name, drink.brand, drink.store, drink.type))
    conn.commit()


def dbhandler(conn, list, mode):

    # populate or update mode
    if mode == "p":
        for drink in list:
            drink_task = (drink.store, drink.brand, drink.name, drink.type, float(drink.price), drink.link, float(drink.ml),
                          float(drink.percent), float(drink.stdDrinks), float(drink.efficiency))
            create_entry(conn, drink_task)

    elif mode == "u":
        # update entries with the same name / add entries who's names do not exist.
        for drink in list:
            update_drink_price(conn, drink)

    conn.commit()


def delete_task(conn, name, brand, store, type):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE name=? AND brand=? AND store=? AND type=?'
    cur = conn.cursor()
    cur.execute(sql, (name, brand, store, type))
    conn.commit()


def delete_all(conn):
    """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
    sql = 'DELETE FROM drinks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
