import sqlite3
from sqlite3 import Error
from scripts.classItem import Item


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("drinks.db")

        sql = ''' CREATE TABLE IF NOT EXISTS "drinks" ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT, `store` TEXT,
            `brand` BLOB, `name` NUMERIC, `type` TEXT, `price` REAL, `link` TEXT, `ml` REAL, `percent` REAL,
            `stdDrinks` REAL, `efficiency` REAL, `image` TEXT )'''
        cur = conn.cursor()
        cur.execute(sql)
        print("connected to database")
    except Error as e:
        print(e)

    return conn


def create_entry(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO drinks(store,brand,name,type,price,link,ml,percent,stdDrinks,efficiency,image)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
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
        print(type(row))


def select_all_drinks_by_efficiency(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Ececute a new query at the cursor
    cur.execute("SELECT * FROM drinks ORDER BY efficiency DESC")
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()

    return rows

def select_drink_by_efficiency_and_type(conn, type):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param type: the value in the type column that we are querying for
    :param priority:
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Execute a new query at the cursor
    cur.execute("SELECT * FROM drinks WHERE type LIKE %s ORDER BY efficiency DESC", (type,))
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()

    return rows

def update_drink(conn, drink, newPrice):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param drink:
    :return: project id
    """
    sql = ''' UPDATE drinks
              SET price = ?, link = ?, image = ?
              WHERE name = ?
              AND brand = ?
              AND store = ? '''
    cur = conn.cursor()
    cur.execute(sql, (newPrice, drink.link, drink.image, drink.name, drink.brand, drink.store))
    conn.commit()


def is_drink_in_table(conn, drink):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param drink:
    :return: project id
    """
    sql = ''' SELECT * FROM drinks
              WHERE store = ?
              AND brand = ?
              AND name = ?
              AND link = ?
              '''
    cur = conn.cursor()
    cur.execute(sql, (drink.store, drink.brand, drink.name,  drink.link))

    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False


def dbhandler(conn, list, mode):

    # populate or update mode
    if mode == "p":
        for drink in list:
            drink_task = (drink.store, drink.brand, drink.name, drink.type, float(drink.price), drink.link, float(drink.ml),
                          float(drink.percent), float(drink.stdDrinks), float(drink.efficiency), drink.link)
            create_entry(conn, drink_task)

    elif mode == "u":
        # update entries with the same name / add entries who's names do not exist.
        for drink in list:
            if is_drink_in_table(conn, drink):
                print('//update')
                update_drink(conn, drink, drink.price)

            else:
                print('//create')
                drink_task = (drink.store, drink.brand, drink.name, drink.type, float(drink.price), drink.link,
                              float(drink.ml), float(drink.percent), float(drink.stdDrinks), float(drink.efficiency),
                              drink.image)
                create_entry(conn, drink_task)

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
